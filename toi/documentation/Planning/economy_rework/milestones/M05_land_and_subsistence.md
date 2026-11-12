# M05: Land, agriculture and subsistence

**Spec:** §10, §11, §25. **Depends on:** M02, M04. **Questions:** Q24–Q27, Q63, Q71, all decided. **Status:** not started.

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
