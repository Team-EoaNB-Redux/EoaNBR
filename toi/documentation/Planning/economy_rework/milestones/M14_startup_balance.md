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
4. **Deposits:** potential, known and quality per state (M06).
5. **Debt:** bring back the real starting debts. ENG's `starting_debt = 1500` is commented out in `ENG - Britain.txt`.
6. **Wages:** base wages for every tag. Only ENG and the Indian tags are set; the rest still use the `set_tech_*` seeds.
7. **Money, banks and companies:** starting base money, reserves, bank stocks and companies.

## Done when
The bar is the one from archive/03:
- `world_1857_eng` stays stable for 60 months;
- startup GDP is near target;
- most goods sit between 0.5× and 2× base.
