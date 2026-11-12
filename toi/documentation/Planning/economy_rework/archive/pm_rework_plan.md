# Production Method & Infrastructure Rework

> **Archived 2026-11-11.** Superseded by the milestone plan in [../00_README.md](../00_README.md), built on the new spec [EOANB_Redux_Economy_Redesign_Updated.md](../EOANB_Redux_Economy_Redesign_Updated.md). Kept for history: status and file references below are as they were when archived.

## Context

The PM system derives output from a value-based multiplier (`pm_output_multiplier × base_output_value / base_price`) and keeps per-country copies of every PM's inputs so 663 per-input modifiers can edit them. This pass replaces it with quantity-per-K PMs from `toi/documentation/Planning/EoaNBR Economy.xlsx`, adopts the sheet's 1857 base prices, replaces the state capacity market and roads with Infrastructure Efficiency (spec §7–9), and removes per-input modifiers.

It comes first so the later country-level industry and investment rewrites build on the final data model. Moving base prices, country-level aggregation and the investment rewrite are out of scope.

**Definition of done (Strat's choice: mechanical only):** everything loads, runs with no new script errors, and matches the sheet's per-K numbers. Balance tuning comes afterwards. Long runs may still collapse, and that doesn't block completion.

## Locked decisions

| Topic | Decision |
|---|---|
| Job tiers | Wrk → laborers, Mid → workers. `wage_multiplier@workers` 5 → 4. Professionals/specialists get no PM jobs until the pop-type rework |
| Output | PM holds one quantity per K. The industry holds which goods it makes and a production multiplier per good |
| Multipliers | Value parity for shared PMs: reference price ÷ good's price (iron 0.67, gold 0.08, cotton 0.67, luxuries 0.33, rubber 0.14). Everything else 1.0 |
| Transport | Industries stop paying. Sheet transport rows become demand only, so each PM's VA rises by that amount. Farms add no demand |
| IE curve | S/D < 1: IE = S/D, floor 25%. S/D ≥ 1: IE = 1 + 0.2 × (1 − D/S). Sector modifier = 1 + (IE − 1) × dependence, applied to inputs and outputs, never employment |
| Roads | Removed. Base infrastructure from population, with a tech factor |
| Ports | Keep national shipping; a global share of port output also counts as state transport (default keeps today's ~4.6 per size) |
| Rail/port income | Paid for service with no payer, at state rate `$1 × clamp(D/S, floor, 2)` |
| Missing families | Livestock, oil extraction, extra farm AMs, govt: converted from old values, preserving $/K |
| Construction | Sheet rows win. Other PMs use the notepad's era baskets (`Machinery = 200 × input`, `Electronics = 20 × electricity input`, `Computers = 100 × computer input`) |
| Upgrades | Pay the new method's full construction list over its duration. New builds pay PM + AM, duration PM + AM |
| Workforce gaps | Interpolate within family; else Forestry rows (land sectors) or Tools rows (factories) by year |
| Tech links | Sheet > same/renamed token > always (first in family) > never. `tech_steelmaking` → `tech_steelworking`, `tech_open_hearth_process` → `tech_open_hearth_furnace`. Hot Blast stays empty |
| PM modifiers | One throughput + one employment modifier per method (true %). All existing PM modifier entries are stripped from techs for now |
| Maintenance | Global rate × construction value, paid by size even when idle |
| Investment | Disabled behind one flag. Player expand/retool stays |
| Base prices | Goods `B-1857` column, static. Transport and shipping base $1 |
| Consumption | C-1857 stays a price index only. Pop weights unchanged (`/base_price` already keeps needs constant in $) |

## Data model

**PM (global only, no per-country copies):**
- `global.pm_output_amount@pm`: quantity per base K (AMs have none)
- `global.pm_input@pm`, `global.pm_input_amount@pm`: quantity per base K
- `global.pm_construction_input@pm`, `..._amount@pm`: **total** per base K (was per month)
- `global.pm_construction_duration@pm`; `pm_retooling_duration` is removed
- `global.pm_workforce_laborers/workers/peasants@pm`
- `global.pm_industrial_capacity_use@pm` (transport demand), `global.pm_industrial_capacity@pm` (rail output), `global.pm_shipping_capacity@pm`: quantity per K
- `global.pm_construction_value@pm`: precomputed at startup at base prices, used for upkeep
- Country: `pm_throughput_factor@pm`, `pm_employment_factor@pm` (unset reads 0, always used as `1 + x`)

**Industry:**
- `global.building_base_production@b`: goods (unchanged, so GUI loops and parallel arrays still work)
- `global.building_production_multiplier@b`: replaces `building_base_production_amount`. Subsistence `[1, 0.2, 0.04]` reproduces the sheet's 0.5/0.1/0.02
- `global.building_infrastructure_dependence@b`, seeded by type: farming 0.3, resource 0.6, factories 1, urban 0.5 (my assumption), transport/govt/subsistence 0
- `global.building_base_output_value` is removed

**Formulas (per size, with `employees = building_base_employees`):**
```
output_mods = (1+industry_output) × (1+industry_throughput) × eco_of_scale × (1+pm_tp[pm]+pm_tp[am]) × infra_mod
input_mods  = (1+industry_input)  × (1+industry_throughput) × eco_of_scale × (1+pm_tp[pm]+pm_tp[am]) × infra_mod
production_max[i] = pm_output_amount × multiplier[i] × employees × output_mods
input_max[i]      = (pm_qty[i] + am_qty[i]) × employees × input_mods
share[tier]       = max(0, pm[tier]×(1+emp[pm]) + am[tier]×(1+emp[am]))
infra_mod         = 1 + (infrastructure_efficiency − 1) × dependence
```

**State infrastructure (replaces `calc_industrial_capacity` in `_economy_market.txt`):**
```
base = global.base_industrial_capacity + rate × pops × (1 + controller:modifier@base_infrastructure_factor)
S = base + Σ rail capacity + Σ port shipping × global.port_transport_share + modifier@local_industrial_capacity_modifier
D = Σ transport demand + modifier@local_industrial_capacity_use_modifier
infrastructure_efficiency = S/D (floor 0.25) when S<D, else 1 + 0.2 × (1 − D/S); D=0 → 1.2
price_industrial_capacity = base_price × clamp(D/S, 0.25, 2)
```
- Demand excludes `infra_mod`, so IE can't feed back into its own demand. It keeps the existing one-tick lag (`calc_industrial_capacity` runs at the top of `special_buildings_update`).
- `price_industrial_capacity` is kept as the pay rate, so existing readers stay valid.
- Rail revenue = capacity × that rate. Port revenue = shipping × that rate.
- Math expressions divide by zero to 42949.67, so every S/D division needs a guard.
- Country scope needs a constant `infrastructure_efficiency = 1`, so `get_pm_values` works at both scopes.
- `rate` is calibrated so ENG's 1857 base + roads total is preserved given its gravel-road tech (about 0.0055/K with gravel +0.6). The tech factor scales the pop term only, not the flat 5. This differs slightly from the formula in the question.
- `base_infrastructure_factor` is a new modifier. Old road techs add +0.6, +1.4, +2.0, +3.5 (the old PM steps 1.0 → 8.5).

## Implementation

Phases 1–5 land together: the data format change is all-or-nothing, so the mod won't run correctly partway through.

### 0. Baseline
`bin\ecosim_cli.exe run --months 24 --out runs\pre_pm_rework` on eng_1857, plus `check --parse-only`, before any edit. The existing `runs/baseline` predates the parity fixes.

### 1. Generator: `toi/documentation/scripts/generate_pm_data.py`
Stdlib only (`zipfile` + `xml`, since openpyxl isn't installed). Reads the workbook at full precision: the CSVs hid values, e.g. Steam Engine machinery is 0.005, not 0.01. Config tables at the top: rename map (from the comments in `eoanbr_tokens.txt`), family → building, spelling overrides (`pm_artisanal_goods`, `pm_integrated_gasification_combined_cycle`), era baskets, era durations, tech aliases, legacy conversions.

Family → building notes: Hydro family → `electricity` RGO; thermal, nuclear and renewables → `power_plant`. Mining family → all mined RGOs; Farming → crop, rice and plantations; Forestry → `wood`. Baseline AMs (`pm_no_automation`, `pm_manual_farming`, `pm_hand_picks_and_tools`, `pm_muscle_power`, `pm_open_field`) stay as zero-effect tokens, which leaves ~1,800 history lines untouched. Zero-quantity rows are skipped (9 exist). Legacy professionals/specialists shares fold into workers.

Generates:
- `toi/common/scripted_effects/_economy_definitions_pms.txt` (full file, replaces hand-written one), with a `define_all_production_methods` effect replacing the ~200 calls at `_economy_setup.txt:1383`
- `toi/common/scripted_effects/_economy_definitions_pm_assignments.txt`: per-building PM/AM arrays and multipliers (arrays removed from `_economy_definitions_industries.txt`)
- `toi/common/scripted_effects/_economy_pm_modifier_factors.txt`: `update_pm_modifier_factors`, generated `set_variable` lines
- `toi/common/modifier_definitions/01_economy_pm_modifiers.txt`: replaces the `pm_*` block in `00_economy_modifiers.txt` (starts at line ~2382)
- Marker-delimited PM blocks in `common/synchronized_dynamic_tokens/eoanbr_tokens.txt` and `common/script_enums.txt` (unregistered tokens fail silently)
- `toi/localisation/english/economy_pms_l_english.yml`: names and `_unlock_tt` (old keys removed from `economy_l_english.yml`; Korean/Russian fall back until translated)
- `toi/interface/economy_pm_icons.gfx`: `GFX_pm_*` sprites, reusing the renamed PM's existing art, else a generic icon
- `toi/documentation/Planning/pm_generation_report.md`: every filled workforce value, basket-filled construction, `never` tech, and PM + AM combo where Wrk clamps at 0

### 2. Core PM model
- `toi/common/scripted_effects/_economy_setup.txt`: base prices (lines 1961–1998), `base_price_industrial_capacity = 1`, remove base output value blocks (1675–1713, 1735), new tunables (infrastructure, port share, pay floor/cap, maintenance rate), `wage_multiplier@workers = 4`, RGO arrays for the new multiplier
- `toi/common/scripted_effects/_economy_industries.txt`: rewrite jobs, `industry_production_update` and subsistence as math expressions. Use `global.wage_multiplier@` instead of literal 2/5/10/20 (jobs, `total_prod_temp`, bonuses, getters). Recompile the merged PM+AM input list only when PM/AM changes, not every tick
- Subsistence: `quantity × multiplier × (employed + 0.7 × marginal)`. This implements the code comment; today marginal peasants aren't scaled by good, so they make 14× an employed peasant's fiber
- `toi/common/scripted_effects/_economy_main_rework.txt`: replace `update_national_production_methods`' 950 lines of modifier application and `init_national_pm_method` with unlock logic plus `update_pm_modifier_factors`, gated on the existing `tech_dirty_var_*` flags. Remove `pm_token_array_*` categories
- `toi/common/scripted_triggers/_economy_getter_functions.txt` → move `get_pm_values` and construction/retooling cost to **scripted effects** using `for_each_loop`. They're triggers today, which is why they nest 11 levels. Update live callers (`_economy_industries.txt:1165, 2283, 2323`) to call before the `limit`. `calc_construction_cost` already exists as the loop version; reuse it and delete the trigger duplicates

### 3. Infrastructure
- `_economy_market.txt`: new infrastructure calc as above; remove old price logic and `industrial_capacity_service`
- `_economy_industries.txt`: apply `infra_mod`; revenue via the pay rate; remove `expenses_industrial_capacity` from costs, productivity and `calculate_projected_profitability` (`_economy_main.txt`)
- `_economy_main_rework.txt` `gdp_update`: replace `ind_tmp`/`shp_tmp` with state transport + shipping revenue
- Remove the `infrastructure` building: `define_infrastructure`, `special_token_array` entry, the size branches (`_economy_industries.txt:126`, `_economy_setup.txt:2164`), `special_buildings_update`, tech factor block (`_economy_main_rework.txt:4400`). The vanilla HOI4 infrastructure building is untouched
- `common/technologies/43_transportation_infrastructure.txt`: road techs lose PM unlocks, gain `base_infrastructure_factor`

### 4. Construction, retooling, maintenance
- `industry_update_construction_retooling`: walk PM **and** AM lists for builds (today only the PM list is charged) as `total ÷ duration × employees`. Retooling uses the target method's construction list
- `industry_update` asset value and `expenses_maintenance`; `initial_cost_temp` (`_economy_industries.txt:2848`)
- Update durations/costs read by `common/scripted_guis/economy_and_demographics.txt:1535` and scripted loc

### 5. Investment flag and dead code
- `global.eco_investment_enabled = 0`, gating the block in `_country_advance_time` (`_economy_main.txt`, `io_cleanup_flags` through `national_opportunities_monthly`) and startup (`_economy_setup.txt:429–439`). `companies_update` keeps running for dividends
- `_economy_investment.txt` and `_economy_investment_buckets.txt` are left unedited; their old field reads are unreachable while gated. Next rework replaces them
- Delete `_economy_cache_temp.txt` (confirmed no callers)

### 6. Content migration (one-time scripts, not kept)
- **Techs:** strip all `pm_*_modifier = x` entries and their tooltips from `common/technologies/*`. Keep unlock tooltips, re-pointed through the rename map
- **History swaps:**

| Old | New | Uses |
|---|---|---|
| `pm_shaft_mining` | `pm_basic_extraction` | 250 |
| `pm_basic_consumer_goods` | `pm_artisanal_goods` | 74 |
| `pm_wooden_buildings`, `pm_brick_buildings` | `pm_mercantile_services` | 117 |
| `pm_saw_mills` | `pm_steam_sawmills` | 47 |
| `pm_hot_blast_process` (ENG) | `pm_blister_steel_process` | 1 |
| `pm_mechanical_goods` (ENG) | `pm_mechanized_workshops` | 1 |

The last row departs from the rename comment (`→ pm_industrial_molded_goods`), because that is a 1900 PM needing plastics nobody makes in 1857.

### 7. UI
- `toi/interface/economy.gui`: remove the infrastructure row (~2590); relabel the capacity display (~2344) to show Infrastructure Efficiency
- `economy_and_demographics.txt`: remove infrastructure PM buttons (~329, ~892); `economy_scripted_loc.txt`: remove infra lines (~2804–2851), add IE tooltip with S, D and sector effect

### 8. Sim
- `redux-eco-sim/scenarios/eng_1857.txt`: rescale pins to new base prices (trade × old/new, `global_market_price` × new/old). Without this, ENG's imports are mispriced
- Add `infrastructure_efficiency` watches; grep `project/ui` panels for old field names
- `toi/common/scripted_effects/_economy_sim_probes.txt`: add `eco_sim_pm_audit` (logs per-K revenue, inputs, wage mult and construction for every PM at base prices) and an array-read-inside-math-expression probe. That read works in the sim but is unconfirmed in-game

### 9. Afterwards
Update `memory/economy-architecture.md` and add a memory for this model. No commits unless asked.

## Verification

1. `bin\ecosim_cli.exe check --parse-only`: no new syntax errors. `bin\ecosim_tests.exe` passes.
2. Grep: no `pm_output_multiplier`, `pm_retooling_duration`, `building_base_output_value`, `token:infrastructure` or old PM tokens outside gated investment code. Every `token:pm_*` is registered and defined; no building references an undefined PM (28 do today).
3. **Sheet match:** run `eco_sim_pm_audit` via the CLI and diff against the workbook (a small script): revenue, inputs (excluding transport), wage mult and construction for all sheet PMs, within 0.00002.
4. `run --months 60 --out runs\pm_rework` on eng_1857: compare diagnostics against `runs\pre_pm_rework`. No new `math_expr_error`, `unknown_effect`, `unknown_scripted_effect`, `undefined_modifier`, `div_by_zero`, `array_index` or `overflow` from economy files.
5. Hand-check one state (London) in the CLI: S, D, IE, pay rate, a factory's and a farm's modifier, railway and port revenue against the formulas.
6. `--scenario scenarios\world_1857.txt`, 12 months: runs clean.
7. Godot UI smoke test (`--smoke`).
8. **Needs Strat in-game:** game loads, PM and state screens display correctly, sprites resolve, then `effect eco_sim_probes = yes` to confirm the array-in-expression read, and `eco_sim_parity_dump` for `parity`.

## Consequences to review

- **ENG steel will sit at the 4× cap.** Blister makes about 133 against about 544 needed, and with investment off nothing upgrades it. Expect this in every test until investment returns or you retool by hand.
- **Primitive, Blister and Craft Machinery lose money on inputs alone**, tested as-is by your choice. With the point above, steel-using sectors will look worse than they eventually should.
- **Basic Extraction drops mining output about 30%** in those 250 states, tightening iron and coal.
- **Professionals and specialists have no PM jobs.** `pops_balance` will likely push them into other types or unemployment at startup, which affects spending and SoL.
- **`tech_precision_made_furniture` unlocks Industrial Molded Goods** under the rename rule, a PM needing plastics, available in 1857. Harmless with AI investment off, but worth reassigning.
- **Rural states with zero demand get IE +20%**, so about +6% farm output, and nothing limits it. Tunable.
- **Port income uses the state pay rate with a 0.25 floor** (my addition, matching the old price floor). Without a floor, colonial ports (Trinidad D/S ≈ 0.07) would earn almost nothing and downsize, cutting national shipping.
- **Late-game PM + AM shares clamp.** The sheet's AM deltas assume additive shares, but e.g. Modern Machinery + Industrial Electrification reaches 0 Wrk. The generator report lists every case; the ROI tab's numbers won't hold for those.
