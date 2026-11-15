# M08: Manufacturing Base and HOI4 factories

**Spec:** §12. **Depends on:** M04. **Questions:** Q32, Q33, Q53, Q64, Q106–Q113, all decided. **Status:** done in the simulator (2026-11-14); in-game check to do.

## Goal
Civilian factories, military factories and dockyards stop being economic industries. The **Manufacturing Base** (`manufacturing_base`; §12's "underlying productive industrial capacity") is derived from the country's manufacturing sectors. The state contracts a share of it, split into civilian, military and naval use, and HOI4's factory counts follow as **offmap** buildings. All on-map factories are removed.

This is the TNO-like version, option (c) of Q32. Long term, Strat prefers (b): the government contracts a slice of the manufacturing sectors, which takes that slice out of civilian output (backlog). Under (b) factories stay a straight conversion, with no employment to track.

The same session added Strat's **military resource scale** and **economic mobilisation share** (decisions.md, "Manufacturing Base follow-ups").

## What was built

### The Manufacturing Base (`manufacturing_base_update`, `_economy_industries.txt`)
- **The base** is the total size of the country's manufacturing industries: `sector_size@` of every sector in the Factories category (`global.building_type` 5, all 17), plus content's bonuses (Q113, which amends Q64's "real output"). Idle plants count: the state contracts factories that exist.
- **Content bonuses** (`manufacturing_base_bonus`) are kept in factories in use at the default contracted share, so each is worth 100 / `global.manufacturing_contract_share_start` of base: +1 factory adds 10 base at 10% (Q111). Keeping them in factories lets country history add them before the economy's globals exist.
- **Contracts:** the state contracts `manufacturing_contract_share` % of the base (Q106, Q110: 10% to start, `global.manufacturing_contract_share_start`). Only the player changes it; the AI never does. Idle factories cost nothing and give no HOI4 factory.
- **The split:** `manufacturing_split@<factory type>` divides the contracted factories, 20% civilian, 50% military and 30% naval to start (`global.manufacturing_split_start@`, Q107). A country without a coastal state gives its naval share to the military. The factory types are `global.offmap_factory_types` (`token:industrial_complex`, `token:arms_factory`, `token:dockyard`).
- **Offmap factories (Q33):** each type's count is round(base × share × split). HOI4 can only add or remove offsite buildings, so the effect sends the change from `offmap_factories@<type>` (what this country was last given) through `meta_effect` and `add_offsite_building`, and stores the new count. `manufacturing_contracted` is the total.
- **When it runs:** monthly after `sectors_update`, at startup (`_country_fin`), whenever content changes the base, and when the player changes the contracts.

### The contract cost (`spending_update`)
`manufacturing_contract_spending` = contracted factories × `global.manufacturing_contract_cost` (100, £0.1M a month, Q113). It's part of `military_mandatory_spending`, in place of the arsenals' and dockyards' payroll, as the UI plan's "Factory contracts" row (§4.2). The money goes to no one under option (c).

### On-map factories removed
- **History:** the 275 factory lines in 195 state files are commented out in place, as the map strip did, so M14 can read them.
- **Construction:** the three buildings are `is_buildable = no` (`00_buildings.txt`), so neither the player nor the AI can build them. The state screen's civilian factory, military factory and dockyard rows are gone, with their triggers, effects and scripted loc.
- **The government-building industries are deleted:** `define_arms_factory`, `define_industrial_complex`, `define_dockyard`, `govt_building_update`, `global.building_government_control`, the economy's own completion of government construction, their budget lines (`military_production_payroll_spending`, `public_enterprise_payroll_spending`, `public_enterprise_revenue`, `consumer_goods_earnings`), and their PMs (removed from `generate_pm_data.py` and `pm_legacy_data.json`, then regenerated). The three productivity modifiers that fed their revenue are deleted with their 56 uses in ideas, a trait and technologies. The building tokens stay: they name the offmap factory types.

### Content (Q108, Q111)
`add_manufacturing_base` (country scope, `_economy_effects_documentation.txt`) adds `x_temp` factories' worth of base, or removes it if negative, and updates HOI4's factories at once. A script converted content:
- 382 `add_building_construction` of a factory (state scope) became `owner = { set_temp_variable = { x_temp = N } add_manufacturing_base = yes }`;
- 35 `remove_building` of a factory became the same with −N;
- 42 `add_offsite_building` calls (country scope) became `add_manufacturing_base`, so the economy owns every offmap factory;
- the five factory wrappers (`add_1_civfac_random_state`, `add_1_milfac_random_state`, `add_one_random_civilian_factory`, `add_one_random_military_factory`, `add_one_random_dockyard`) add one factory's worth; `replace_civ_with_arms_factories` had no callers and is deleted. Five USA focus rewards lost their dead government construction cost lines.

### The military resource scale and the mobilisation share
- **Scale:** a production-screen resource is a tenth of a good (`global.military_resource_scale` = 10). Every equipment resource cost was multiplied by 10, except ships: hulls, ship modules, ship engines, convoys, repair and support ships ×2 (2,261 values in 38 files). Land equipment costs the same goods as before; ships cost a fifth.
- **The bridge (`market_update`):** `resource_cost@` = −(production + imports) × 10 × `military_resource_share`.
- **Demand and money:** military production's demand (`national_market_update`) and procurement spending count each resource used, or short, as a tenth of a good. The trade AI's minimum trade for military production does too, and its deficit term now subtracts the deficit, which was a bug: it subtracted consumption, so a deficit zeroed the minimum.
- **Mobilisation share (Q109):** the `military_resource_share` modifier, set by the economic mobilisation laws: undisturbed isolation 10%, isolation 15%, civilian economy 20%, low 30%, partial 45%, war economy 60%, total mobilisation 80%.

### UI
- **Production screen:** above the resource grid, "Economic Mobilisation: 20% of national resources go to military production" (`production_mobilisation_container`). The budget panel's Payroll row is now Contracts, and a Set Contracts button opens the popup.
- **The contracts popup** (`manufacturing_contracts_popup`, Q112): the base, the contracted share (±1%, shift ±10%), and the split (±5%; civilian and naval changes are balanced by military, military changes by civilian, then naval), with each type's factories and a note for landlocked countries. U2's Sectors strip opens the same popup later (UQ9).
- **Budget tooltips:** Factory Contracts replaces Industry Payroll in mandatory military spending; the Industry Payroll and Consumer Goods lines are gone.

### Simulator
`add_offsite_building` is modelled (`effects_world.cpp`): a per-country count by building type, which `num_of_civilian_factories`, `num_of_military_factories` and `num_of_naval_factories` include.

## Results
`redux-eco-sim/runs/m08_a` against `runs/m08_base` (`world_1857_eng`, 60 months, `--watch-file watches/m08.txt`). The parse check is clean apart from six older non-economy files; no load errors; 1.20 s a month against 1.24.
- **The base:** ENG's is 7 (its seven sizes of test factories), which rounds to no factory at 10%. HBC's history bonus (one offmap civilian factory before, now one factory of base) gives a base of 10 and one military factory, costing 100 a month. No other country has a base. With ENG's share set to 100%, it gets 1 civilian factory, 4 military factories and 2 dockyards, costing 700 a month, and HOI4's counts follow (`runs/m08_full100`).
- **Removing the government buildings** is most of the change, at month 60:
  - Jobs: ENG's working class is down 61% (195K jobs) and its middle class down 25%, back into the peasants. Base wages are 26–30% lower in the test states.
  - GDP: down 20% (−2.0K a month), mostly the buildings' revenue, which came from nowhere.
  - Budget: revenue is down 34%, with public enterprise revenue (−1.5K) and the income tax on their payroll gone. Spending is down 15%, with their payroll (−0.9K) gone. The net budget ends 4% better, and the treasury 8% lower.
- **Procurement fell 91% and steel 43%,** but that's partly the simulator: it takes military production's resource use from a save made before the scale (`scenarios/save_inputs_1857.txt`, `resource_consumed_<good>`), at the old equipment costs, and now divides it by 10. In-game, land equipment uses 10× the resources and costs the same goods. Rerun `tools/import_save_inputs.py` on an M08 save.

## Done when
- [x] HOI4's civ, mil and dockyard counts follow the contracts, as offmap buildings (simulator; in-game to check).
- [x] No on-map factories remain in history, and players can't build any.
- [x] The contract cost shows in the budget and scales with the factory count.
- [x] Military production still draws goods and resources, at the new scale.
- [ ] In-game: the game loads with no new `error.log` lines from the economy files or the GUI; the mobilisation line sits above the resource grid; the popup opens, its buttons work and HOI4's factory counts follow; content that adds a factory raises the base.

## Left over
- **Content that reads on-map factories** now always sees 0: 82 state-scope factory level checks in 17 files, 166 `free_building_slots` checks for factories (they always pass), Sweden's focus sums of `building_level@`, and the occupation and resistance scripts. Country triggers (`num_of_civilian_factories` and the rest) still work, on offmap counts. Content work, or M14.
- **The stripped map gives almost no country a factory:** only ENG has manufacturing (base 7, which rounds to 0 at 10%), and only content bonuses give others any. M14's map rebuild fixes it.
- **Other languages'** budget tooltips and production panel still call the deleted scripted loc (`GetPublicEnterpriseRevenue`, `GetPublicEnterprisePayrollSpending`, `GetMilitaryProductionPayrollSpending`); English is updated.
- A tag annexed and re-released keeps its stored `offmap_factories@` while HOI4 has removed its offsite buildings, so its counts would be off until they next change.
- The UI plan's Manufacturing Base strip on Sectors and its Capacity figure come with U2 and U4.
