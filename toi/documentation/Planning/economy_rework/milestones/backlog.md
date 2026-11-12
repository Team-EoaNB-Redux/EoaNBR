# Backlog

Small items that don't belong to one milestone. Do them when one is convenient. Most come from [archive/07](../archive/07_content_backlog.md), and the full lists are in `documentation/Planning/pm_generation_report.md`.

- **Techs:** 63 PMs have no tech, mostly after 1900. Reassign `pm_professional_services` and `pm_industrial_molded_goods` in `TECH_OVERRIDES` once real techs exist. `tech_hot_blast_furnace` and `tech_shaft_mining` unlock nothing.
- **Tech effects:** every PM modifier was stripped from the techs. Add them back as `pm_<x>_throughput_modifier` and `pm_<x>_employment_modifier`, after M04, since the PM/AM cache changes where they apply.
- **Missing sheet rows:** livestock, oil extraction, farm AMs after Tractors, and government buildings are still legacy conversions from `pm_legacy_data.json`. M08 may remove the government rows.
- **Sheet gaps:** 119 workforce values and 137 construction lists use defaults.
- **Icons:** 127 PMs use placeholder art.
- **Localisation:** Korean and Russian lack the new PM names. M02 adds the new pop-class names.
- **Moving base prices** by era, so early PMs age out. If base prices start moving, `pops_spending_need_at_sol` and `pm_construction_value` must be recomputed. This may overlap with the M12 price level.
- **Sheet oddities:** 34 PMs have a tech 30+ years older than their tier. `High Performance Computers` has a transport row priced at 0. Blister Steel is worse than Primitive above about $10.60 steel. Modern Machinery's revenue is below Specialized Machinery's.
- **Data bug:** `1092-Western Colorado.txt` has `owner = HYD`.
- **Overflow:** `pops_sol` overflows when dividing by the population of tiny states (`_economy_main_rework.txt`). It may go away in M02 or M03.
- **`pops_food_consumption_factor`** (`get_pop_needs`, `_economy_main_rework.txt`) subtracts its share of food from the quantity needed, but adds the cost of that share to `needs_spending_temp`. It does nothing while the modifier is 0, but a non-zero value would make pops pay for food they no longer eat.
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
- **Company reorganisation** (Chapter 11 in Strat's notepad), shares and valuations, gated by the insolvency laws (Q66). Comes after M10.
- **Government bonds in the same credit market** as private loans (Q43). Comes after M11.
- **Nominal values in the UI** (Q46): each currency's value against the pound, applied in scripted localisation only. Comes after M12.
