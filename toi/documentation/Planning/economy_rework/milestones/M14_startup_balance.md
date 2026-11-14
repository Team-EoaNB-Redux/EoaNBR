# M14: Startup balance

**Spec:** all of it, as built. **Depends on:** everything before it. **Status:** not started.

## Goal
Rebuild the 1857 map on the finished systems, so world supply and demand start roughly in balance for every good. Then turn debt back on with real starting values. This is the old segment 03, moved to the end.

## Inputs
- [archive/03](../archive/03_startup_balance.md): the strip, the targets, the bankruptcy trace and how to measure.
- [pm_1857_tuning.md](../pm_1857_tuning.md): the 1857 PM values and wages already in the sheet.
- [eng_economy.md](../eng_economy.md) and [raj_economy.md](../raj_economy.md): scale and shape for the British Isles and India. They're a guide, not a rule. The targets are comments in the history files, written by `catalogue_1857_targets.py`.

## Build
1. Remove the M00 test industries and turn the debt switch back on.
2. Rebuild each sector across the map, checking each good's world supply against demand.
3. **Land data:** set arable land, land quality and crop eligibility in state history wherever possible. The population fallback (Q24) stays only for states nobody has set.
4. **Deposits:** potential, known and quality per state (M06), with `set_variable = { <rgo>_size = N }` for the worked part. Sources:
   - the old map's values, commented out in each state's `resources` block (wood, coal, iron, chemicals, copper, fiber and food had the most);
   - the state lists in `_eoanbsys_state_resources_scripted_triggers.txt` (`has_coal_desposits`, `has_oil`, `has_aluminum`, `has_tungsten`, `has_chromium`, `has_titanium`, `has_rare_earth_deposits`), which startup used for random potential until M06 (Q100);
   - `_economy_states_setup_rework.txt`, deleted in M06 (Q101) and still in commit `9612e4cfb`: arable land, deposits and a soil quality for 108 US states.
   - The dated discoveries in `_eoanbsys_resource_deposits.txt` and other content add worked deposits through `add_x_deposit` since M06 (Q96), at the old HOI4 amounts. Check their sizes against the rebuilt map, and decide which should be known deposits for investors instead.
   - The sheet's RGO rows for the 15 manufactured goods are unused since M06 (Q97) and can go.
5. **Debt:** bring back the real starting debts. ENG's `starting_debt = 1500` is commented out in `ENG - Britain.txt`.
6. **Wages:** base wages for every tag. Only ENG and the Indian tags are set; the rest still use the `set_tech_*` seeds.
7. **Money, banks and companies:** starting base money, reserves, bank stocks and companies.
8. **Infrastructure (M07):** size railways and ports to transport demand (on the stripped map railways are paid the floor rate), and decide which techs, laws or content grant `base_infrastructure_cap_modifier` and `base_infrastructure_cap_factor`. Until something does, a road tech adds nothing in a state at the cap of 40 (Q103). Check the shipping price's floor and cap (0.25–2, Q104).

## Done when
The bar is the one from archive/03:
- `world_1857_eng` stays stable for 60 months;
- startup GDP is near target;
- most goods sit between 0.5× and 2× base.
