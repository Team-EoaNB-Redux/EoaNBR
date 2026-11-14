# Backlog

Small items that don't belong to one milestone. Do them when one is convenient. Most come from [archive/07](../archive/07_content_backlog.md), and the full lists are in `documentation/Planning/pm_generation_report.md`.

- **Player downsizing** ([ui_planning.md](../ui_planning.md) UQ16 and UQ22, decided 2026-11-14): a wrapper, `downsize_x_industries`, that removes one level of size from a state-industry at once, with no refund. The workers lose their jobs that month. It's blocked while the industry has construction under way, since cancelling comes first. The AI doesn't use it, and capacity decay (Q23) stays automatic beside it. Content calls the wrapper. Build it before the UI's States tab (U3), which shows the button.
- **Know-how** (ui_planning.md UQ24): Strat wants industrial know-how modelled, but what it is and what drives it are still open. Macro → General keeps a greyed place for it, where the mockup had industrial expertise. M15's company R&D may feed it.
- **Techs:** 63 PMs have no tech, mostly after 1900. Reassign `pm_professional_services` and `pm_industrial_molded_goods` in `TECH_OVERRIDES` once real techs exist. `tech_hot_blast_furnace` and `tech_shaft_mining` unlock nothing.
- **Tech effects:** every PM modifier was stripped from the techs. Add them back as `pm_<x>_throughput_modifier` and `pm_<x>_employment_modifier`, after M04, since the PM/AM cache changes where they apply.
- **Missing sheet rows:** livestock, oil extraction, farm AMs after Tractors, and government buildings are still legacy conversions from `pm_legacy_data.json`. M08 may remove the government rows.
- **Sheet gaps:** 119 workforce values and 137 construction lists use defaults.
- **Icons:** 127 PMs use placeholder art.
- **Localisation:** Korean and Russian lack the new PM names, and the Korean economy file still carries stale PM tooltips from the old PM system. The pop-class names are in all three languages since M02; the Russian tooltips M02 changed are in English, marked #NT!.
- **Moving base prices** by era, so early PMs age out. If base prices start moving, `pops_need_at_wealth` and `pm_construction_value` must be recomputed. This may overlap with the M12 price level.
- **Sheet oddities:** 34 PMs have a tech 30+ years older than their tier. `High Performance Computers` has a transport row priced at 0. Blister Steel is worse than Primitive above about $10.60 steel. Modern Machinery's revenue is below Specialized Machinery's.
- **Data bug:** `1092-Western Colorado.txt` has `owner = HYD`.
- **Content charges the state's treasury:** `add_1_civfac_random_state` and `add_1_milfac_random_state` (`0_eoanb_building_effects.txt`) and five USA focuses (`usa_vic_ft.txt`) call `add_treasury` inside a state scope, so their cost lands on the state's `treasury` variable, not the country's. Wrapping each in `owner = { }` fixes it. `get_total_construction_cost` returns their cost again since M06.
- **Trade AI, found in M01** (`_economy_market.txt`):
  - `trade_ai_calculation` runs before `trade_update` refreshes the world price (`local_global_market_update`), so in the first week of each month the AI sizes routes against last month's world target. In one test, ENG cut its coal exports from 33 to 3 for that week, because the world target it saw was 2.10 instead of 8.00. Refreshing first would double the cost of `local_global_market_update`, which loops over every market for every leader.
  - `trade_ai_remove_unproductive_route` is called but defined nowhere, so a route is only removed when its offers reach 0.
  - Exporters can offer more than they produce. The export formula targets local price = world price − costs, and with the world price at its cap that means roughly twice production (ENG steel: production 28.6, exports 44).
  - Only market leaders run `trade_update`, so members' world prices (`global_market_price@`) stay at their startup values. The trade screen of a player who is a member shows them.

## Later, after the milestone that builds the base version
From Strat's answers in [decisions.md](../decisions.md):
- **SoL separate from wealth** (Q17): SoL derived from wealth plus modifiers such as pollution. Comes after M03.
- **Upper-class population** that varies more than a flat 2% of jobs (Q11). Comes after M02.
- **Two floating wages per state** (Q9), if one wage turns out to be too coarse.
- **Manufacturing Base option (b)** (Q32): the government contracts a slice of the manufacturing sectors, which takes it out of civilian output. Comes after M08.
- **Government bonds in the same credit market** as private loans (Q43). Comes after M11.
- **Nominal values in the UI** (Q46): each currency's value against the pound, applied in scripted localisation only. Comes after M12.
- **Era-gated prospecting** (Strat, on Q99): many deposits were found long after 1857, and Victorian prospecting was mostly looking around and guessing, so modern deposits shouldn't be within reach early. Possibly by technology or by date, per deposit. Comes after M06.
