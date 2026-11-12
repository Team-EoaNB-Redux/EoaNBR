# AGENTS.md: EoaNBR

Onboarding for coding agents (Codex reads this file; Claude Code reads it through `CLAUDE.md`). Keep it current: if you change how the economy behaves, update this file and `toi/documentation/economy_overview.md` in the same change.

## What this repo is
- **End of a New Beginning Redux**, a Hearts of Iron IV total-conversion mod with an 1857 start. The mod root is `toi/` (descriptor `toi.mod`), laid out like any HOI4 mod: `common/`, `events/`, `history/`, `interface/`, `localisation/`, `gfx/`, `map/`.
- Most agent work here is on the **custom economy**, led by Strat (GitHub `Strategy-Gamer`). Focus trees, events and the map are ordinary HOI4 modding.
- There's no build step. Testing means loading the game, which is slow (saves take 5–10 minutes to load), or running the headless simulator (see Testing).

## Read before economy work
1. `toi/documentation/economy_overview.md`: what every system does, the monthly loop, what's on and off, design principles. Start here.
2. `toi/documentation/Planning/economy_rework/00_README.md`: the active work plan, the tools table, and rules learned the hard way. Segments `01`–`07` hold the detail. `redux_economy_redesign_spec.md` is the target design.
3. `toi/documentation/economy_docs.md` and `toi/common/scripted_effects/_economy_effects_documentation.txt`: the effects content is allowed to call.
4. `redux-eco-sim/CLAUDE.md`, if `redux-eco-sim/` exists. It's a separate repo, gitignored here, so it may be missing.
5. `memory/` at the repo root, if present. It's local and gitignored, and holds design-decision notes from earlier sessions. Treat them as history and check them against the code.

## Economy file map (`toi/common/`)
| File | What's in it |
|---|---|
| `on_actions/_eoanbr_eco.txt` | Entry points: `on_startup` → `_reset`; `on_monthly_UCT` → `_advance_time`; `on_weekly_UCT` → `r_weekly_trade`. UCT is the country that hosts the economy tick |
| `scripted_effects/_economy_setup.txt` | `_reset`, `_init_country`, `_init_state`, `market_setup`, and every constant: `global_variables`, `pops_global_var_setup` (wage multipliers, participation, wage knobs, pop needs), `buildings_global_var_setup`, `resources_global_var_setup` (base prices), token arrays, `eco_investment_enabled` |
| `_economy_main.txt` | `_advance_time`, `_country_advance_time` (**the monthly order**), `create_econ_order_array`, `r_weekly_trade`, `on_monthly_industries` (construction, cash, downsizing, prospecting), `on_monthly_pops`, `on_monthly_industry_ai` (employment target), economic cycle, `ai_budget` |
| `_economy_main_rework.txt` | The pops pipeline (`pops_update` and its steps), `employment_update`, `get_pop_needs`, `pops_balance` / `pops_convert`, `update_national_production_methods`, `national_debt_update`, `gdp_update`, `market_calc_gdp`, graphs |
| `_economy_industries.txt` | `industries_update`, `industry_update` (finances, bonuses, dividends, asset value, downsizing plan), `industry_production_update`, `industry_update_size_jobs`, `industry_update_employment`, `govt_building_update`, `subsist_and_arable_update`, `base_wage_seed` / `_update` / `_finalize`, `add_x_industry_internal`, `add_rgo_internal`, construction and retooling internals |
| `_economy_market.txt` | `market_update`, `market_calculations`, `get_price`, `calc_industrial_capacity` (Infrastructure Efficiency), shipping, `calculate_military_demand`, global market, `trade_update`, `trade_ai_calculation` |
| `_economy_budget.txt` | `budget_update` (`taxes_update`, `spending_update`), slider effects, `change_*` slider effects |
| `_economy_investment.txt` | Investment opportunities, the investment fund, national opportunities (company founding). **Gated off**, and it still reads PM fields that were removed (segment 06) |
| `_economy_investment_buckets.txt` | A prototype of local and national capital pools. Not hooked up |
| `_economy_companies.txt` | Companies MVP: fractional ownership, dividend pull, projects |
| `_economy_banking.txt` | Bank. Disabled (`bank_update` is commented out) |
| `_economy_projects.txt` | Country projects (`proj_create`, `proj_update`, `proj_done`) |
| `0_eoanb_debt_effects.txt` | Debt-level checks. `debt_level > 49.9` (about 200% of annual GDP) fires the bankruptcy event |
| `_economy_definitions_industries.txt` | Building and RGO definitions: type, base employees, outputs, tech unlock, arable land use |
| `_economy_definitions_pms.txt`, `_economy_definitions_pm_assignments.txt`, `_economy_pm_modifier_factors.txt` | **Generated.** Don't edit |
| `_economy_definitions_units.txt` | Goods demand from military units |
| `_economy_tests.txt` | `finance_tests` (console: `effect finance_tests`) |
| `_economy_sim_probes.txt` | Debug probes for the simulator |
| `scripted_triggers/_economy_getter_functions.txt` | `get_pm_values`, `get_construction_cost`, `get_retooling_cost`. These are **triggers** because the GUI and localisation call them |
| `modifier_definitions/00_economy_modifiers.txt` | Every economy lever (confidence, incentives, efficiencies, tax limits, sector factors). `01_economy_pm_modifiers.txt` is generated |
| `dynamic_modifiers/economy_dynamic_modifers.txt` | `resource_trade` pushes economy goods into HOI4 resources so military production can use them. `budgetary_spending` applies the slider bonuses |
| `ideas/_economy_tokens.txt`, `ideas/0_eoanb_state_country.txt`, `ideas/eoanb_economic_crisis_ideas.txt` | Tokens; economic-situation ideas; debt-crisis ideas (`edc_bankrupt`) |
| `scripted_effects/_eoanbr_history_effects.txt` | `set_tech_*` tier effects. Each sets its techs and a default `base_wage`, guarded by `has_variable` |

History data:
- `toi/history/states/*.txt`: `set_variable = { <industry>_size = N }`, `resources = { ... }` for deposits, optional `arable_land` and `base_wage`. Blocks between `# >>> 1857 economy target` and `# <<<` are generated by `catalogue_1857_targets.py`. Don't edit them by hand.
- `toi/history/countries/*.txt`: country `base_wage` (set it *before* `set_tech_*`), tech tier, budget, debt.

## The monthly tick (`_country_advance_time`, per country in rank order)
`national_debt_update` → `add_treasury` (net budget) → `ai_budget` (AI only) → `spending_effects_update` → `update_national_production_methods` → **per controlled state:** `on_monthly_industries` → `on_monthly_pops` → `industry_productivity_sort` → `base_wage_update` → `on_monthly_industry_ai` → `pops_balance` → `fix_negative_workforce` → `update_base_resource_count` → `reload_industries_array` → `subsist_and_arable_update` → `employment_update` → `govt_building_update` → `industries_update_construction_retooling` → `industries_update` → `pops_update` → **country:** (gated) `io_*` → `companies_monthly` → `companies_update` → `investment_fund_update` → (gated) `investment_funds_monthly` / `investment_opportunities_monthly` / `national_opportunities_monthly` → `update_country_pop_stats` → market leader: `calc_shipping_capacity`, `market_update`, `market_calc_gdp` → `budget_update` → `national_debt_update` → statistics → `check_economic_cycle`.

The one-tick lags are intentional: wages use last tick's utilisation, hiring last tick's profitability, revenue last tick's price.

## Data model
- **Tokens** index everything: `token:food`, `token:laborers`, `token:steel_foundry`, `token:pm_x`. Per-token variables are written `var@token:food` (a literal token) or `var@var:t` (a token held in a variable).
- **Static definitions** are globals: `global.base_price@token:food`, `global.pm_output_amount@var:pm`, `global.building_base_employees@var:b`.
- **Per-industry data lives on the state**, keyed by the building token: `size@var:bu_token`, `employment_target@`, `profit@`, and arrays such as `production@var:bu_token` (parallel to `global.building_base_production@`). State arrays: `industries` (everything, including RGOs and special buildings), `buildings`, `rgos`.
- **Prices** sit on the market leader, are copied to every member country and state, and are read as `controller:price@var:r`.
- **Units:** pops in thousands. Money: 1,000 = £1M. Every flow is per month.
- **Temps don't belong to a scope.** A temp keeps its value across scope changes within one effect execution and is cleared when that execution ends. Set a temp, change scope, read it. Don't build `PREV.` plumbing for it.

## Script semantics (confirmed in-game or by the simulator)
- `check_variable` has no `<=` or `>=`. Use `<`, `>`, `=` and `NOT`. Negative literals compare fine (`> -1`).
- Multiply and divide truncate. Dividing by 0 gives 0 in plain variable effects, but **a math expression doesn't** guard against it, so guard it yourself. Raw × raw wraps in 64 bits, so a product above roughly 922M goes wrong.
- **Math expressions** (`set_variable = { x = { value = a multiply = b ... } }`) are preferred for formulas because they're faster. Rules:
  - Globals, normal variables and `@token:` / `@var:` reads work directly inside them.
  - Stage `arr^i` into a temp first.
  - Keep math expressions out of trigger blocks (`all_of`, the getters). Use plain temp effects there.
  - They aren't allowed in `modulo_variable` or `clamp_variable`; use `mod` / `clamp` inside the expression instead.
  - A parse failure silently evaluates to 0.
- The getters are triggers because the GUI and scripted localisation call them, and effects aren't allowed there. Keep them trigger-safe.
- **A console probe isn't a tick.** Some reads return 0 from the console but work in ticks. Judge in-game behaviour from a save, not the console.

## Conventions (Strat's)
- `*_update` and `calculate_*` effects are **idempotent**: they recompute from scratch with `set_*`. `*_monthly` effects **advance state**, run exactly once per tick, and run before the matching `_update`.
- Document temp inputs and outputs in a header comment (`# x_temp - amount`, `# Output: borrow_temp_k`).
- Content (events, focuses, decisions) calls the documented wrappers (`add_x_industries`, `construct_x_industries`, `add_treasury`, `add_debt`, `borrow_money`, ...), never the internals.
- **Temps are for values read many times.** Don't stage a single-use value into a temp; read the source directly.
- **Set the target directly.** Don't add a tracking variable plus a lookup table when the final value can be set in history or in an existing effect.
- Match the surrounding style and comment density, and write comments in plain English. The files mix tabs and spaces, so copy exact lines before an exact-match edit.
- Ask Strat before adding a new file to `toi/`, debug and probe files included.

## Generated data: never hand-edit
- Generated files: `_economy_definitions_pms.txt`, `_economy_definitions_pm_assignments.txt`, `_economy_pm_modifier_factors.txt`, `01_economy_pm_modifiers.txt`, `economy_pms_l_english.yml`, `economy_pm_icons.gfx`, and the marked blocks in `eoanbr_tokens.txt` and `script_enums.txt`.
- Source: `toi/documentation/Planning/EoaNBR Economy.xlsx`, a download of Strat's Google Sheet. Regenerate with `python toi/documentation/scripts/generate_pm_data.py` (stdlib only; openpyxl isn't installed). Check with `python -B toi/documentation/scripts/verify_pm_audit.py`. Defaults the sheet doesn't supply are listed in `toi/documentation/Planning/pm_generation_report.md`.
- Read the xlsx, never pasted CSVs: CSV rounding hides real values.
- Strat balances in the sheet. Give balance changes as sheet values to enter, not as edits to the generated script.

## Testing and verification
Failures are silent, so "it loads" proves nothing. After editing economy script:
1. If `redux-eco-sim/` exists, work from inside it:
   - `bin/ecosim_cli.exe check --parse-only` finds brace and syntax errors across the mod in under a second.
   - `bin/ecosim_cli.exe run --scenario scenarios/world_1857_eng.txt --months 12 --out runs/<name>`, then read `runs/<name>/report.md` first.
   - For an A/B test, make a baseline run before the edit, then `bin/ecosim_cli.exe compare runs/<baseline> runs/<name>`.
   - The simulator interprets the real scripts and matches in-game British GDP to about 0.5%.
2. After any PM or sheet change, run `verify_pm_audit.py`. It needs the simulator binary.
3. For real in-game state, run `python redux-eco-sim/tools/read_save.py --country ENG` (or `--state <id>`, `--var ENG.gdp_amount`). It reads the newest autosave. **Check a save before believing a theory.**
4. Compare against saves only on `world_1857_eng.txt`, and only saves made on the current code. Strat's test games are on Easy difficulty.

The full tools table is in `economy_rework/00_README.md`.

## Current status (2026-11-11). Update this when it changes
- `global.eco_investment_enabled = 0`: investment opportunities, fund spending, national opportunities, company projects and **downsizing** are all off. Nothing builds or retools on its own.
- Banking and pop borrowing are off.
- **The state economy has been stripped to subsistence** (about 1,095 history files, uncommitted, with the old values commented out in place). `git checkout -- toi/history/states` restores the old map *and destroys any uncommitted map work*. Don't run it unless asked.
- Next: debt and budgets sized for the new GDPs (segment 03, step 3), then rebuilding the map sector by sector.
- Known bugs: nothing increments `global.month`, so `years_passed`, the yearly statistics and `check_economic_cycle` never advance. Pops' diverted investment (`p_pops_investment`) is subtracted from their earnings, but it only reaches `investment_fund` inside the gated `investment_funds_monthly`, so the money currently vanishes. Further open problems are listed in `economy_overview.md` §7 and segment 03.
- Tech PM modifiers were stripped. When you re-add them, use `pm_<x>_throughput_modifier` / `pm_<x>_employment_modifier`.

## Working in this repo
- The working tree usually carries a large uncommitted change set. Don't revert, reformat or "tidy" files you weren't asked to touch.
- Commit or push only when asked.
- Historical economy docs (`eng_economy.md`, `raj_economy.md`) set scale and shape. They aren't exact targets, and game balance wins.
