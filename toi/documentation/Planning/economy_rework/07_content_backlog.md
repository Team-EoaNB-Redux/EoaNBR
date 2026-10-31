# Segment 07: content backlog

Smaller items, in any order, after the game runs. Full lists are in `documentation/Planning/pm_generation_report.md`.

- **Techs:** 63 PMs have no tech (`never`), mostly post-1900. Reassign `pm_professional_services` and `pm_industrial_molded_goods` in `TECH_OVERRIDES` once real techs exist. `tech_hot_blast_furnace` unlocks nothing, deliberately (it makes pig iron). `tech_shaft_mining` unlocks nothing now.
- **Tech effects:** all 388 PM modifier entries and their tooltips were stripped from techs. Re-add as `pm_<x>_throughput_modifier` / `pm_<x>_employment_modifier`. The old road and factory techs lost their PM bonuses, so techs give less right now. Modifiers are true percentages, unlike the old additive ones. Unlock tooltips are in place.
- **Modifier semantics, as built:** throughput adds PM + AM values, then scales inputs and outputs. Employment scales each method's own shares. Confirm that's what Strat wants.
- **Missing sheet rows:** livestock, oil extraction, farm AMs after Tractors, and government buildings are legacy conversions from `pm_legacy_data.json`. Strat said these won't work for later PMs. Planned tokens exist: `pm_industrial_meatpacking`, `pm_mechanized_barns`, `pm_advanced_refining`, `pm_rotary_drilling`, `pm_top_drive_systems`, `pm_computer_aided_farming`, and more. Git has the rename comments that were in `eoanbr_tokens.txt` (commit `017c0d6bc`).
- **Sheet gaps:** 119 workforce values and 137 construction lists are defaults.
- **Icons:** 127 PMs use placeholder art (`interface/economy_pm_icons.gfx`, `gfx/interface/productionmethods/`).
- **Localisation:** Korean and Russian lack the new PM names and still hold old keys. Old per-tech `_tt` strings were removed from English only. Old sprites for removed PMs remain in `interface/economy.gfx`, harmlessly.
- **GUI:** infrastructure row removed, and railway and port rows moved up. Capacity display now shows IE. Never checked in-game in a working economy.
- **Moving base prices:** Goods tab has B-1857 to B-2000 and normalised 1857–2000 columns (each year's prices scaled so the C-year basket costs $3.61). Strat hasn't decided how it should work; it's meant to stop early PMs staying relevant. `global.base_price` is static at B-1857 now. If it moves, `pops_spending_need_at_sol` (precomputed at startup with `/base_price`) and `pm_construction_value` must recompute. C-1857 is only a price index for now; pop weights weren't changed.
- **Pop types:** workers multiplier is 4, professionals 10, specialists 20, with no PM jobs for the last two. Strat's notepad suggests collapsing to Working and Middle class eventually.
- **Sim:** `pow` and token-number differences are accepted. `all_of_sum` and `array_in_expression` differ from the console only (segment 01).
