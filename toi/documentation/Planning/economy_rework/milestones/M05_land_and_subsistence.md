# M05: Land, agriculture and subsistence

**Spec:** §10, §11, §25. **Depends on:** M02, M04. **Questions:** Q24–Q27, Q63, Q71, and the follow-ups Q92–Q95, all decided. **Status:** done in the simulator 2026-11-14; the in-game check is still to do (see Left over). Baseline: `redux-eco-sim/runs/m05_base` (`world_1857_eng`, 60 months, `--watch-file watches/m05.txt`). Result: `runs/m05_a`.

## Goal
Each state has an amount of arable land, a land quality and a list of crops it can grow. Commercial farms compete for the land, and subsistence farming uses what's left, through carrying capacity. Arable land should eventually be set in every state's history. Until then the population formula stays as a fallback.

## Exists now
- **Arable land:** `state_eco_arable_land_init` (`_economy_setup.txt`) sets `arable_land = workforce / 20 + 1` unless history sets it. Only 76 of 1,455 state files do.
- **Who uses it:** `subsist_and_arable_update` gives commercial farms their land first. Subsistence takes the rest, and peasants beyond what it holds farm marginal land at 70% productivity.
- **Who gets the output:** landowners take 20% of subsistence. About 20% of subsistence output reaches the market.
- **Peasants are too poor** (Strat, 2026-11-12, during M01): "currently they're about 2/3 as poor as they should be, so, if they are given a proper amount of land, they shouldn't be pinned at 1 SoL." On the M01 test bed, all of ENG's market's peasants (98.5% of its pops) sat at SoL 1 with food at its 4× cap. M01 cut `global.pops_base_spending` from 0.3 to 0.1 so food isn't pinned. Strat doesn't want peasants pinned at SoL 1 at the lower value either, so this milestone's land is what should lift them off it. Check peasant SoL when it lands.

## Build
1. **Arable land** (Q24): keep `state_eco_arable_land_init` as the fallback. History values win wherever they're set.
2. **Land quality:** a scalar per state, defaulting to 1 unless history sets it.
3. **Crop eligibility** (Q26, Q63, Q71): one yes/no per farm sector per state. It blocks construction and investment where a crop can't grow.
   - Common crops are eligible unless history says otherwise. Uncommon crops are eligible only where history says so.
   - Crop farm and livestock ranch are common. Everything else is uncommon: rice paddy and the cotton, luxuries and rubber plantations (Q71).
   - There's no generator script.
4. **Carrying capacity:** K = remaining arable land × land quality × subsistence yield technology.
5. **Subsistence output** (Q25): (min(P, K) + 0.5 × max(0, P − K)) × a fixed yield per peasant, where technology raises K only. It doesn't depend on Infrastructure Efficiency, and there's no harvest-quality mechanic.
6. **Rent** (Q27): the upper class takes a rent share of subsistence output only. Commercial farms pay no rent.

## Done when
- History land values are used where set, and the fallback only where they aren't.
- World subsistence food output in the simulator stays in the same range as M04's, unless the new land data deliberately changes it.
- Farms can't be built where the crop isn't allowed.
- Peasants in states with a proper amount of land are above SoL 1 at `pops_base_spending = 0.1`.

## What the baseline showed (Q92–Q95)
- **Land alone couldn't lift peasants off wealth 1.** Under Q25, land past carrying capacity adds nothing, so unlimited land only raised East Anglia's peasants from 75% to 82% of what wealth 1 cost them (the median state from 75% to 79%). Their income counted the 80% they eat at base price, but their basket charged all of it at market price, and the stripped map's prices sat well above base: ENG's wealth-1 basket cost 0.245 per K pops at month 12, against 0.100 at base prices. Q92 charges the home-grown share at base price.
- **The fallback left 44.5% of the world's peasants past carrying capacity**, so half returns there would have cut world subsistence output about 10%. Q93 changes the fallback to workforce / 15 + 1, which keeps it flat.

## What was built (2026-11-14)
1. **Arable land** (Q24, Q93). `state_eco_arable_land_init` keeps history's value and otherwise falls back to `pops_workforce / 15 + 1` (it was / 20).
2. **Land quality** (Q95). `land_quality` on each state, 1 unless history sets it. It scales carrying capacity, and the output of every farm that uses arable land, from the same inputs (`industry_production_update`, and `get_pm_values` in state scope; country scope has no land quality and takes none).
3. **Crop eligibility** (Q26, Q63, Q71). `crop_eligible@<farm>` on each state, 1 where the crop grows.
   - `global.building_common_crop@` marks the crop farm and the livestock ranch (`_economy_definitions_industries.txt`), and startup sets them to 1 unless history set them.
   - History allows an uncommon crop with `set_variable = { crop_eligible@token:rice_paddy = 1 }`, and forbids a common one with `= 0`.
   - `can_build_industry_no_tech_check` requires it, which covers construction and the gated investment code. The construction list hides farms whose crop can't grow (`refresh_construction_list`), and the new trigger `is_crop_eligible` checks it.
4. **Carrying capacity and output** (Q25, Q94), in `subsist_and_arable_update`:
   - `subsistence_capacity` (K peasants) = land left after commercial farms × `land_quality` × (1 + the PM throughput factor of `pm_subsistence_farming`, where technology goes) × 10 peasants per unit of land (the farm's base employees × the PM's peasant workforce).
   - `peasants_marginal_land` = peasants past it. They make `global.subsistence_marginal_yield` (0.5) of the yield.
   - The yield per peasant = the PM's output amount × the farm's production multiplier × (1 + `subsistence_farm_output_factor`), which ideas and laws set. Infrastructure Efficiency doesn't touch it.
   - Output, revenue and productivity work as before: 20% of output reaches the market as `output@`, and revenue counts that share at market price and the rest at base price.
5. **Rent** (Q27). `global.subsistence_rent_share` (0.2) of subsistence revenue goes to the upper class as `dividends@subsistence_farm`, and the peasants get the rest. `industries_update` only counted rent while the farm had land, so a state whose commercial farms took all of it paid none; it now counts it whenever peasants farm.
6. **The peasant basket** (Q92). `get_pop_needs` charges the share of a basket not bought at market at base price: price = base + market share × (market price − base). Other classes buy all of it at market, so nothing changes for them.
7. **The subsistence farm is slim** (Q90's rule). Nothing read its `jobs@`, `employed@`, `peasants_jobs@`, `peasants_employed@`, `employment_percentage@`, `employment_target@`, `average_wage@`, `expenses@` or `profit@`, so they're gone. It keeps `size@` (the land left, which the state screen shows), `output@`, `revenue@`, `expenses_payroll@` (the peasants' share), `dividends@` (rent), `owner_jobs@` and `productivity@` (the wage floor and peasant migration read it).
8. **Dead land code deleted** (Q4). `on_monthly_land`, `land_update` and `forest_update` (forests, housing, land value and urban land) were never called. Their modifiers in `00_economy_modifiers.txt` stay, since laws define them.
9. **Content wrappers** in `_economy_effects_documentation.txt`: `set_land_quality` and `change_land_quality` (`land_quality_temp`), and `set_crop_eligible` (`industry_token`, `crop_eligible_temp`), with English tooltips.
10. **The subsistence tooltip** shows land quality, carrying capacity, peasants on marginal land and landowners. Its employed and jobs lines had read the working and middle classes since M04, so they showed 0. Expenses and Dividends now read Peasants and Rent.
11. **Simulator:** `watches/m05.txt`.

## Results (simulator, `world_1857_eng`, 60 months)
Against `m05_base` (`runs/m05_a`). No new diagnostics, and ticks are the same speed (1.42 s/month against 1.46).

**World subsistence output stays flat.** At month 12 the market share of subsistence output is 10,571 against 10,640 (−0.6%), and 27.8% of the world's peasants are past carrying capacity, against 44.5%. Rent is up 7.2%, because food costs more.

**Peasants are off wealth 1 everywhere.**

| Peasant wealth at month 60 | Baseline | M05 |
|---|---:|---:|
| ENG | 1.0 | 5.3 |
| FRA | 1.0 | 5.6 |
| USA | 1.0 | 7.2 |
| QNG | 1.0 | 4.0 |
| RAJ | 1.0 | 2.0 |
| RUS | 1.0 | 1.8 |
| East Anglia, Munster (fallback land) | 1 | 5 |
| New York (history land) | 1 | 7 |
| West Bengal (fallback land) | 1 | 2 |
| Beijing (history land: K of 150 for 1,062 peasants) | 1 | 2 |

India and Russia climb more slowly because their peasants' consumer confidence is about 0.85, which holds their target close to their wealth-1 spending.

**Food costs more.** Peasants buy more as they get richer: ENG's food is 5.52 at month 60 against 4.26 (+29%), and the USA's 7.41 against 5.02, close to its cap of 8. ENG's GDP is +4.9% and its market's +6.5%.

**Crop eligibility and land quality work** (simulator effects in East Anglia): a rice paddy is blocked until `set_crop_eligible` allows it, a crop farm is blocked once forbidden, and the construction list grows from 8 to 9 entries when rice is allowed. Land quality 2 doubles the crop farm's output (54.8 → 109.6), the state's carrying capacity (280 → 560) and `get_pm_values`' revenue (237 → 479).

## Left over
- **In-game check:** load a new game, search `error.log` for "Errors occurred while reading math expression", open a state's subsistence tooltip, and check peasants' wealth after a few months.
- **Forbidding a common crop needs `has_variable` to be true for a variable history set to 0.** The simulator treats it that way; the game is unverified. No history does it yet.
- **No history sets land quality or crop eligibility yet,** so uncommon crops (rice, cotton, luxuries, rubber) can't be built anywhere until M14 sets them. The old map's commented-out farm sizes show where they grew.
- **Rent pays income tax only,** as upper-class income. Sector profits pay corporate tax as well (Q86). A land tax would be an M13 law.
- **Sales tax is charged on the peasants' whole basket,** home-grown share included, now at base price. M13 or M14 could limit it to what they buy.
- **Peasant job migration** still moves at most `arable_land / 10` peasants a month (`pops_peasant_job_migration`), so the bigger fallback raised its cap by a third.
- **Food prices are about 30% higher**, and the USA's is near its cap. That's for M14.
- The PM throughput modifier of `pm_subsistence_farming` now raises carrying capacity. Its generated name says throughput, so whoever adds a technology for it should know what it does.
- The subsistence tooltip's Food, Wood and Fiber Output lines show only the market share (`output@`), as before.
