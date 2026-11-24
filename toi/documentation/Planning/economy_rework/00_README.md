# Economy rework: index

**Strat's decision, 2026-11-11:** build the economy to the new spec first, then balance the 1857 start. Until then the map stays stripped to subsistence, and a few small test industries in Britain are fine for checking that mechanisms work. Balance waits for M14. Debt is off for every country for the same reason (`global.eco_debt_enabled = 0`, from M00).

- **Target design:** [EOANB_Redux_Economy_Redesign_Updated.md](EOANB_Redux_Economy_Redesign_Updated.md) ("the spec"). The old spec is in [archive/](archive/redux_economy_redesign_spec.md) for history.
- **Decisions:** [decisions.md](decisions.md). Strat answered every question: Q1–Q84 on 2026-11-12, Q85–Q91 on 2026-11-13, Q92–Q125 on 2026-11-14, Q126 on 2026-11-15 and Q127–Q146 on 2026-11-16. Each milestone lists the questions it depends on.

## Milestones
Each one is a self-contained piece of work for a fresh session. Do them in order, since each builds on the ones before. The order itself is Q1.

| # | Milestone | Spec | Questions | Status |
|---|---|---|---|---|
| M00 | [Test bed](milestones/M00_test_bed.md) | — | Q1–Q5 | Done |
| M01 | [Gradual prices](milestones/M01_prices.md) | §7 | Q6–Q7, Q56 | Done |
| M02 | [Pops and labour](milestones/M02_pops_and_labour.md) | §5, §23–30 | Q8–Q14, Q57, Q58, Q61, Q62, Q73–Q80 | Done; checked in-game (month-1 autosave) |
| M03 | [Wealth and demand](milestones/M03_wealth_and_demand.md) | §24–25, §31–32 | Q15–Q17, Q59, Q60, Q81–Q84 | Done; figures checked in-game (July 1857 autosave), screens to check |
| M04 | [National sectors and target utilisation](milestones/M04_national_sectors.md) | §2–4, §6 | Q18–Q23, Q55, Q85–Q91 | In progress: the systems are done, in the simulator and in Strat's month-1 save; the UI rework remains |
| M05 | [Land, agriculture and subsistence](milestones/M05_land_and_subsistence.md) | §10–11, §25 | Q24–Q27, Q63, Q71, Q92–Q95 | Done; figures checked in-game (July 1857 autosave), screens to check |
| M06 | [Natural resources](milestones/M06_resources.md) | §9 | Q28–Q30, Q68, Q96–Q101 | Done; figures checked in-game (July 1857 autosave), screens to check |
| M07 | [Infrastructure](milestones/M07_infrastructure.md) | §8 | Q31, Q102–Q105 | Done; figures checked in-game (July 1857 autosave), screens to check |
| M08 | [Manufacturing Base and HOI4 factories](milestones/M08_manufacturing_base.md) | §12 | Q32–Q33, Q64, Q106–Q116 | Done; figures checked in-game (July 1857 autosave), screens to check |
| M09 | [Investment](milestones/M09_investment.md) | §13 | Q34–Q39, Q60, Q117–Q126 | Done; checked in-game (July 1857 autosave) |
| M10 | [Companies](milestones/M10_companies.md) | §19 | Q40–Q41, Q66, Q127–Q146 | Done in the simulator; in-game check to do |
| M11 | [Banking, credit and base money](milestones/M11_banking_and_credit.md) | §14–16 | Q42–Q44, Q59, Q65, Q69, Q72 | Done; checked in-game (startup, June and July 1857 saves) |
| M12 | [Money, inflation and currency](milestones/M12_money_and_currency.md) | §16–18 | Q45–Q49, Q52, Q67, Q69, Q70 | Simulator and in-game currency settlement verified; final investment tolerance sim-only |
| M13 | [Government, laws and controls](milestones/M13_government_and_laws.md) | §20–22 | Q50–Q51, Q61 | Implemented/tested; universal AI solvency and in-game smoke test remain open |
| M15 | [Shares and capital markets](milestones/M15_companies_completion.md) | §19, §21.3 | Q40, Q66, Q127, Q128, UQ23 | Not started; runs before M14 |
| M16 | [Company strategy](milestones/M16_company_strategy.md) | §19 | Q127, Q128 | Not started; runs before M14 |
| M17 | [Branches and influence](milestones/M17_branches_and_influence.md) | §19, §21.3 | Q127, Q128 | Not started; runs before M14 |
| M14 | [Startup balance](milestones/M14_startup_balance.md) | all | — | Not started |
| — | [Backlog](milestones/backlog.md) | — | — | Small items, any time |

Q52 to Q54 apply across milestones.

**The reasoning behind the order:**
- The test bed comes first, so tests aren't spoiled by unrelated bankruptcies.
- Gradual prices are small and on their own, and they steady every later test.
- Pops come before sectors because everything after them employs and pays by class.
- The sector layer comes before land, resources and infrastructure, so those are written once, into the new structure.
- Investment needs the physical caps in place. Companies need investment. Banking needs borrowers, and brings base money with it, since reserves are built from base money. Currency needs bank money.
- Controls come next. Then M15–M17 finish the companies, since reorganisation and foreign branches need the laws. Strat added M15 on 2026-11-14, after the numbering, and split it into M15 (shares), M16 (strategy) and M17 (branches and influence) on 2026-11-16 (Q127), so they sit above M14 in the table.
- Balance comes last.

## Rules for the rework
- **Implementation, not balance.** Values only need to be sane enough to show a mechanism working. Don't retune the sheet to fix balance; note the issue for M14.
- **Before a milestone:** reread its spec sections and its questions in `decisions.md`. Raise any open ones with Strat, and make a simulator baseline: `runs/<milestone>_base`, `world_1857_eng`, 60 months.
- **`redux-eco-sim` may be edited freely** (Q5). Strat commits it separately.
- **To finish a milestone:**
  - `ecosim_cli.exe check --parse-only` is clean.
  - A 60-month run is compared against the previous baseline.
  - The game loads, with a smoke test in-game.
- **After a milestone:** update its status here, then `economy_overview.md` and the "Current status" section of `AGENTS.md`.
- **Delete what a milestone replaces** (Q4). Old code clutters the mod and confuses coding agents, and git keeps the history.
- **Leave the stripped map alone.** Test industries go only inside `# >>> rework test industries` blocks, and test slaves inside `# >>> rework test slaves` blocks (Virginia, South Carolina and Mississippi).

## Current state of the code
- **Committed** in `26bd1bfab`: the map is stripped to subsistence plus 303 engine factories, with the old values commented out in place in about 1,095 state files. The 1857 PM retune is in ([pm_1857_tuning.md](pm_1857_tuning.md)), and the ENG and RAJ targets are comments in the history files.
- **Committed** in `c472e2509`: this plan reorganisation, M00 (the debt and cycle switches, the month counter fix and the test industries) and M01 (gradual prices, the trade AI's minimum-trade fix, and `pops_base_spending` cut from 0.3 to 0.1).
- **Committed** in `94fc8dbbf`: M02 (five classes, qualifications, slaves, bureaucrats, active manpower, the merged upper-class investment modifier).
- **Committed** in `56c941ee2`: M03 (wealth, spending toward a target, pop debt, middle-class investment, the `get_pop_needs` refactor, and subsistence owner jobs from the peasants).
- **Committed** in `f1fbcedc7`: M04's systems (the PM/AM cache, sector records, the profit split, monthly goods totals by sector and method, the slim state-industry, target utilisation, capacity decay, the national sector figures for the UI). `9612e4cfb` starts the UI rework.
- **Committed** in `acece860c`: M05 (arable land, land quality, crop eligibility, carrying capacity, half returns past it, rent as a constant, and the peasant basket's home-grown share at base price) and M06 (deposits as state history data, deposit quality, prospecting without finds from nothing, RGOs for natural goods only, and content's `add_resource` calls converted to the economy's wrappers).
- **Committed** in `4c0daf665`: M07 (the cap on transport supply from population, a shipping price that follows use, ports paid from it and for their local transport, and test railways and ports).
- **Committed** in `639e32e9b` and `76855b074`: M08 (the Manufacturing Base, factory contracts and offmap factories, on-map factories removed and content converted, the military resource scale and the economic mobilisation share).
- **Committed** in `619137bcb`: M08's playtest follow-ups (the law sets the contracted share, and HOI4's factories ramp toward their targets, Q114–Q116).
- **Committed** in `94005e41f`: M09 (opportunities in ROI tiers from sector capital and the general pool, construction bills and sector debt, the government's development fund and infrastructure lines, capacity decay on; the old opportunity system, the buckets prototype and company projects deleted), and the scoring system's O(n²) position search replaced.
- **Implemented:** M10 (companies with their own accounts and with bonuses on their own slices, company investment, debt and failure, founding by incorporation, two startup companies on the test bed), and the split of M15 into M15–M17.
- **Uncommitted:** M11 (banking, shared credit, base money, creditor losses and central-bank basics), verified in the simulator and in-game (startup, June and July 1857 saves; 13/13 finance checks). Simulator tooling is in its separate repository.
- **Switched off:** debt (`global.eco_debt_enabled = 0`: starting debt, interest and bankruptcy), the economic cycle (`global.eco_cycle_enabled = 0`) only. Banking is on since M11: pops, sectors, companies, the general pool and foreign governments share each country bank's credit, with interest. Investment is on since M09, and its switch is deleted.
- **Known bugs:**
  - Pops start in debt: the first three ticks overspend against startup's figures (Q81, accepted until M14).
  - Wages rise 0.5% a month wherever jobs are filled exactly, since utilisation then sits at 1.0, above the stable band (M02, Left over).

## Other files here
- **M14 reference:** [eng_economy.md](eng_economy.md) and [raj_economy.md](raj_economy.md) give 1857 output for the British Isles and India. The history files cite them by name, so keep them here. [pm_1857_tuning.md](pm_1857_tuning.md) and `pm_1857_tuning.csv` record the 1857 PM values already in the sheet.
- [ui_planning.md](ui_planning.md): the economy window rework, tab by tab (Budget, Macro, States, Global), in phases U0–U5 plus the parts each later milestone adds. UQ1–UQ25 were decided on 2026-11-13 and 2026-11-14; UQ26 is open. U1 also replaces the budget sliders with five levels per line. The mockups (`*_window.png`, `global_economy.png`) sit beside it.
- [archive/](archive/): the old segments 01–07, the old README, `pm_rework_plan.md` (the PM rework's locked decisions) and the old spec. Segments 01, 02 and 04 hold findings that still apply: array math in triggers, the AM labour-cut clamp, and the infrastructure formulas.

## Tools
Run them all from the repo. Simulator details are in `redux-eco-sim/CLAUDE.md`.

| Task | Command |
|---|---|
| Parse check | `redux-eco-sim/bin/ecosim_cli.exe check --parse-only` |
| Run the simulator | `ecosim_cli.exe run --scenario scenarios/world_1857_eng.txt --months 60 --out runs/<name>`, then read `runs/<name>/report.md` |
| Find what's slow | A recorded run's report lists scripted effects and triggers by self ops, and the hottest source lines (`profile.csv`, `lines.csv`). Ops don't depend on the machine, so `compare` shows real changes in cost |
| Profile at full-map scale | `python redux-eco-sim/tools/make_stress_history.py`, then `run --scenario scenarios/world_1857_stress.txt --months 12`: industries and deposits in every state of 500K people or more |
| A/B two runs | `ecosim_cli.exe compare runs/<baseline> runs/<name>` |
| Change PM balance | Download the Google Sheet over `toi/documentation/Planning/EoaNBR Economy.xlsx`, run `python toi/documentation/scripts/generate_pm_data.py`, then start a new game |
| Check script values against the sheet | `python -B toi/documentation/scripts/verify_pm_audit.py` |
| **Read real in-game state** | `python redux-eco-sim/tools/read_save.py --country ENG`, `--state 952`, `--var ENG.gdp_amount`. Reads the newest autosave |
| Diff a save against the simulator | `ecosim_cli.exe run --scenario scenarios/world_1857_eng.txt --months 1 --dump-json sim.json`, then `python tools/compare_save.py --save autosave.hoi4 --sim sim.json --scope ENG` |
| Compare in-game probes | in-game `effect eco_sim_probes = yes`, then `ecosim_cli.exe calibrate` |
| Compare in-game state | in-game `effect eco_sim_parity_dump = yes`, then `ecosim_cli.exe parity` |
| Refresh army and stability inputs from saves | `python redux-eco-sim/tools/import_save_inputs.py` |
| Rewrite the 1857 target comments | Dump month 0 with `--dump-json`, then `python toi/documentation/scripts/catalogue_1857_targets.py --dump <file>` |
| Simulate old code, or a map change on a copy | `git archive HEAD toi/common toi/history toi/events toi/localisation/english toi/map/definition.csv` into a scratch dir, then `run --mod <dir>/toi` |

## Rules learned the hard way
- **Never hand-edit generated files.** Edit the workbook or the tables in `generate_pm_data.py`, then regenerate. The generated files are `_economy_definitions_pms.txt`, `_economy_definitions_pm_assignments.txt`, `_economy_pm_modifier_factors.txt`, `01_economy_pm_modifiers.txt`, `economy_pms_l_english.yml`, `economy_pm_icons.gfx`, and the marked blocks in `eoanbr_tokens.txt` and `script_enums.txt`.
- **Check a save before believing a theory.** `read_save.py` shows what the game actually computed. Segment 01's first diagnosis came from probes alone and was wrong.
- **A console probe isn't a tick.** `arr^i` in math, and math in `all_of`, work in ticks but read 0 from the console.
- **Stage `arr^i` into a temp before a math expression, and keep math out of trigger blocks.** Both are unreliable outside ticks, and the getters also run from the GUI. The simulator reports any new use (`math_array_read`, `math_in_trigger`).
- **Compare with saves on `world_1857_eng.txt` only, and only saves made on the current code.** Early gaps compound, so compare a startup save first, then one tick.
- **Strat's test games are on Easy.** That gives ENG a free 1% of GDP a month and −0.02 input factor. If the setting changes, change `difficulty` in that scenario.
- **Read the xlsx, not pasted CSVs.** CSV rounding hid real values.
- **Tech links set startup PMs.** A state with no starting PM begins on `latest_production_method`.
- **Strat prefers math expressions,** and temps only when a value is reused. Array reads and trigger blocks are the exceptions.
- **A load error zeroes every later math expression in its file.** M02 first loaded with everyone a peasant because `_economy_main_rework.txt` had a `log = ""` at line 124 and `_economy_setup.txt` called two effects that don't exist. Both were harmless until M02 put math expressions after them. Check `error.log` for "Errors occurred while reading math expression" after loading. The simulator has reported these as `load_error` since 2026-11-12.

## M11 verification (2026-11-17)

The banking implementation replaces the old disabled bank and includes the companies' and the general pool's debt. Baseline: `redux-eco-sim/runs/m11_base` (M10, 60 months). Final run: `runs/m11_final`, `watches/m11.txt`; controlled foreign-default, confidence-run and systemic-default variants are `m11_final_foreign`, `m11_final_confidence` and `m11_final_systemic`. The milestone file records the implementation and results. Run `python tools/test_m11.py` inside the simulator for integration assertions.

The simulator CLI now accepts repeatable `--inject month:path` effect files for controlled interventions and supports `--dump-json` together with recorded runs. The simulation interpreter is unchanged by M11. The full-mod parser still finds nine pre-existing errors in six unrelated files (characters/CIR, decisions/eoanb_AST_decision, national_focus/iceland, scripted_localisation/XU_dyn_mod_scripted_localisation, units/equipment/ship_hull_screen and history/units/URC_1857-alt); economy files have no new parse/load errors. The actual in-game load and smoke test passed on 2026-11-17: startup, June and July saves, all 13 finance assertions, exact July interest settlement and active-country household ledgers.

## M12 implementation (2026-11-17)

Money, inflation, valuables reserves, relative exchange prices and monetary-law coefficients are implemented. The milestone records formulas and test commands. Base money remains the explicit nominal counter; mining adds reserves without treasury spending, while remaining ordinary goods. All stored cash erodes, including company and construction/investment cash. Fresh baseline: `redux-eco-sim/runs/m12_base`. In-game verification needs new saves; M11 saves are historical evidence only.

M12 in-game check (2026-11-17): fresh startup save and autosave dated June 17, with `global.month = 2`, were compared with `world_1857_eng` at months 0 and 2. `game.log` records `finance_tests` as 18 passed, 0 failed (the user reported 19). No `_economy_banking.txt` or `_economy_market.txt` load errors appear in `error.log`; pre-existing `_internal_politics_effects.txt` math errors remain. Startup ENG P = 1, demand multiplier = 12, exchange = 1, GDP 5,652.715 vs sim 5,679.559. At tick 2 ENG P = 1.00069 vs 1.00073, exchange = 0.95250 in both, GDP 6,185.872 vs 6,239.723 (-0.863%); ENG bank loans 8,198.387 vs 8,099.337 (+1.223%), and borrower-category sums reconcile exactly. USA P = 1.05 in both, exchange 1.00962 vs 1.00983, reserves 10,227.355 vs 10,042.150; USA GDP 9,738.566 vs 9,191.891 (+5.95%) and pool debt 18,162.399 vs 12,483.552 (+45.49%) need investigation. FRA P = 1.00107 vs 1.00120, exchange 0.95250 in both. The saves do not include a first-month snapshot: keep in-game completion pending until one is available and the US divergence is understood. The US uses scripted startup test industries, so inspect state/order and investment first, not currency assumptions. Extracted files: `redux-eco-sim/runs/m12_start_ingame.json`, `m12_june_ingame.json`, `m12_start_sim.json`, `m12_july_sim.json`.

M12 June follow-up (2026-11-17): the fresh first-tick save confirms ENG GDP/loans within 0.27% of the simulator and exact P/exchange parity. Currency settlement is verified in-game: `redux-eco-sim/tools/analyze_m12_ingame.py` passes 688 checks of bank categories, currency formulas and capital erosion/interest. The second-tick US investment discrepancy exposed a fixed-point minimum-admission edge: 0.99999 funded levels could wait against a 1.0 minimum. `investment_try_expansion` now tolerates 0.0001 levels in admission, while charging/building only actual funding; its regression passes. Post-fix 60-month references are `m12_rounding_final`, `m12_rounding_mint`, `m12_rounding_deficit`. The supplied saves predate this small investment fix. Remaining US GDP differences follow observed food-price/trade and engine military-resource inputs, not a demonstrated M12 currency formula failure; details and limits are in the M12 milestone.


## M13 implementation (2026-11-18)

The budget and Q51 controls are implemented, including Strat's tax/spending clarification, five adjustments, per-good taxation/tariffs, law endpoint coefficients, PP upkeep and committed transfer accounting. See the milestone for the plan, exact formulas and validation results. The new Budget button opens the functional controls. The unchanged parser failures elsewhere in the mod are separated from economy diagnostics. In-game loading, layout and startup/two-tick saves remain to verify; do not mark M13 fully done from simulator results alone.
