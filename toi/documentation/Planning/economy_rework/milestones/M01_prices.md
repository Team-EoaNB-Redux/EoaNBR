# M01: Gradual prices

**Spec:** §7. **Depends on:** M00. **Questions:** Q6, Q7, Q56, all decided. **Status:** done 2026-11-12. Strat's July 1857 save on the M01 code shows the actual prices trailing their targets in-game (coal 7.93 against 6.55, steel 26.2 against 22.5, consumer goods 20.0 against 16.4). The pop spending cut (below) came after that save and needs a new game.

## Goal
Prices move toward a target over several ticks instead of snapping to it. Small gaps move slowly or not at all, and large shortages and gluts move fast. Prices should be the fastest-moving part of the economy, with utilisation slower and capacity slowest.

## Exists now
- `get_price` (`_economy_market.txt`) sets P = base × (D/S)², clamped to 0.25–4× base. Valuables are fixed at 2× base.
- Prices are recomputed weekly: `r_weekly_trade` runs `market_update` for each market leader, then `global_market_update`, `trade_ai_calculation` and `trade_update`. Prices carry no memory: each recompute replaces the last.
- The price and employment swing is the biggest stability problem on record ([overview §6](../../../economy_overview.md), [archive/03](../archive/03_startup_balance.md)). In a fantasy test, a straight-line price curve or smaller hiring steps stopped it.

## Build
1. Keep today's formula as the **target** price, per good per market (Q6).
2. Store the **actual** price, and move it toward the target by a step that grows with the gap, with a dead band. One curve serves every good.
3. Apply the same rule to world prices.
4. **Ticks** (Q7, Q56):
   - The actual price steps on the monthly tick, when money changes hands.
   - Trade stays weekly, because HOI4 military factories need resources within a week, not a month.
   - The weekly tick still recomputes supply, demand and the target price, and the trade AI compares against the target. That gap closes as trade adds supply, so trade doesn't overshoot.
5. Revenue, pop spending, GDP and wages read the actual price.

## Done when
- In the simulator, a demand shock (an event, or a knob in a copy) moves prices over several months, not one.
- Weekly trade doesn't overshoot within a month.
- `world_1857_eng` runs 60 months with no new oscillation, compared against `m00_base`.

## What was built (2026-11-12)
All in `_economy_market.txt` unless noted.
1. **Target and actual prices.** `market_calculations` writes `get_price`'s result to `target_price@`, not `price@`. `local_global_market_calculations` does the same for the world price, writing `global_market_target_price@`. `price@` and `global_market_price@` are now the actual prices.
2. **The step.** `price_step` closes part of the gap: a share of `price_step_base + price_step_slope × gap`, at most `price_step_max`, and nothing when the gap is under `price_dead_band`. The gap is max(target/price, price/target) − 1, so a doubling and a halving count the same. Defaults, in `resources_global_var_setup` (`_economy_setup.txt`): dead band 0.02, base 0.3, slope 0.2, max 0.7. A 4× shortage lifts the price about 3.1× in its first month. A 10% gap halves in about two months and is inside the dead band after five.
3. **The monthly tick.** `_advance_time` (`_economy_main.txt`) runs `market_prices_monthly` for every market leader (`global.markets`) before any country's tick. It steps both prices and runs `market_prices_update`, which recomputes `price_compared_to_base@` and `global_market_price_compared_to_base@` and copies the prices to every member and its states. So revenue, wages, pop spending, GDP and the budget all use the same price for the whole month, set from the target the last weekly tick left.
4. **Copies.** States now get prices only from `market_prices_update`, which saves about 90K writes per weekly market pass. Member countries still get the leader's price in `market_calculations` every week, so a country that has just joined a market has prices within the week. Core economy code reads `controller:price@`, never the state copy.
5. **Startup and new countries.** `_reset`, `_country_reset` and `initialize_country` set `prices_snap_temp = 1`, so prices snap to their targets while the economy settles, as before. A good with no price yet (a brand-new country going through `country_eco_setup`) also starts at its target.
6. **The trade AI reads targets** (Q56 (a)): `evaluate_best_trade_quantity`, the hypothetical-route direction, the route productivity that opens and re-evaluates routes, and `set_trade`'s floor check. Trade money stays on actual prices: `trade_value@`, `trade_tariffs@` and `trade_profit@`, which feed the budget and the trade screen. The screen's productivity column is now the target-price figure.
7. **The trade AI's two-week cycle** (see the Q56 note in `decisions.md`). The minimum-trade rules ("1 unit when a market has need but no production", and the reverse) checked `supply@` / `demand@`, which include last week's trade. A route the evaluation had just cut to 0 came back only every other week. About 30 small markets toggled 1-unit coal imports this way, and ENG's coal exports were rationed between 34 and 2 in alternate weeks, with consumer goods doing the same. The rules now check `production@` / `need@`.
8. **Removed:** `global.market_price@` became `global.market_target_price@`, which nothing reads. `global.market_price_compared_to_base@` and `global_market_price_difference@` were never read and are gone.

## Results (simulator, `world_1857_eng`)
**Weekly trade, five weekly ticks in a row after month 20, with production fixed:**

| | Old code | M01 |
|---|---|---|
| Consumer goods exports | −108, −56, −109, −91, −109, −91 | −82, −82, −84, −84, −84, −84 |
| Coal exports | −25, 0, −30, −2, −30, −2 | −3 throughout |
| Coal price | 6.4, 1.7, 7.7, 2.1, 7.7, 2.1 (snaps weekly) | 2.52 actual, target steady at 2.34 |

**Demand shock:** +25 services demand in ENG's market from 1859-01-01, in a scratch copy of the mod, on top of supply of about 91 and demand of about 148. Services is non-tradeable, so trade can't absorb it.

| ENG services price | 1859-01 | 02 | 03 | 04 | 05 | 06 | 07 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Old code | 4.94 | **6.86** | 6.95 | 6.96 | 6.80 | 6.69 | 6.73 |
| M01 (target about 7.1) | 5.17 | 5.85 | 6.29 | 6.57 | 6.76 | 6.86 | 6.93 |

**60 months, from month 6:** total variation (the sum of month-to-month changes over the mean) and direction reversals, over 23 watched series: ENG GDP, revenue and trade value, test-industry jobs, ENG and world prices, trade volumes, and French prices.

| Run | Total variation | Reversals | ENG GDP: TV, reversals |
|---|---:|---:|---|
| `m01_base` (old code) | 247 | 532 | 1.62, 35 |
| Gradual prices, old trade AI | 212 | 324 | 1.32, 17 |
| Trade fix, prices snap monthly | 47 | 354 | 0.25, 34 |
| Trade fix, base 0.4 / max 0.8 | 27.7 | 200 | 0.15, 9 |
| **M01 (base 0.3 / max 0.7)** | **24.3** | **175** | **0.15, 2** |
| Trade fix, base 0.25 / slope 0.25 / max 0.6 | 21.9 | 147 | 0.14, 1 |

- The trade fix removes most of the swing, and gradual prices most of the remaining reversals. Snapping monthly is no steadier than snapping weekly: with the old trade AI it scored 232 against 231, and with the fix it still reverses 354 times.
- **ENG's ±5% monthly GDP swing (M00) is gone.** After the startup transient (a peak of 11.3K in the first months), GDP settles at about 9.95K by month 18 and stays within 9.91–9.97K for the last 40 months. The consumer goods factory stays at 16K jobs (it swung 6.6–16K), and the two coal mines hold at 2.0 and 2.1K jobs from 1859 (they swung 0.6–2.5K).
- Against `m00_base` at month 60 (`runs/m01_final_m00w`): ENG GDP −1.4%, consumer goods price 8.4 (was 13.1), coal 2.4 (was 5.1), consumer goods factory 16.0K jobs (was 10.9K). No new diagnostic categories.
- **Cost:** per call, `market_calculations` is 24% cheaper and `r_weekly_trade` 7% cheaper, because the state copies left the weekly tick. These runs ran in parallel, so the timings are rough.
- Runs: `redux-eco-sim/runs/m01_base` (pre-M01, identical to `m00_base`), `m01_base_w` (the same with `watches/m01.txt`), `m01_final_bs03` (M01 at the old pop spending), and the sweeps `m01_*` / `m01b_*`. These results are all at `pops_base_spending = 0.3`. The cut below came after them.

## Pop spending cut (Strat, 2026-11-12)
Strat's first in-game test ran to July 1857, and nearly every price was pinned at its 4× cap. From the autosave (ENG's market, month 2):
- 98.5% of the pops are peasants, all at SoL 1.00, the floor. At the floor, `global.pops_base_spending` (the SoL-1 basket) sets their demand directly. Food demand was 3.35× supply, and 94% of it came from pops.
- Military upkeep (`calculate_military_demand`) was most of the demand for wood (559 of 1,320), iron (285 of 319), services (146 of 295) and chemicals (all of it). The stripped map makes almost none of these.

24 months in the simulator, ENG's price as a multiple of base at month 24:

| `pops_base_spending` | 0.3 | 0.1 | 0.075 | 0.05 |
|---|---:|---:|---:|---:|
| Food | 4 | 1.8 | 1.3 | 0.95 |
| Consumer goods | 1.7 | 4 | 4 | 4 |
| Services | 2.6 | 4 | 4 | 4 |
| Coal | 1.2 | 3.9 | 3.9 | 3.9 |
| ENG revenue | 7,658 | 5,204 | 5,035 | 4,953 |

A cut unpins food but pins consumer goods, services and coal. Startup sets SoL from earnings against the same cost table (`calculate_standard_of_living`), so laborers and workers start about 15 SoL higher. Above the floor their spending follows income, so they buy more manufactured goods. Revenue falls because pops spend less on taxed goods.

**Decided by Strat: 0.1.** Strat doesn't want peasants pinned at SoL 1 at 0.1 either, but they're "about 2/3 as poor as they should be", so a proper amount of land should lift them. That's noted in [M05](M05_land_and_subsistence.md).

**New baseline, `runs/m01_final` (the baseline for M02):** 60 months at 0.1.
- ENG GDP settles at 9.49K from month 12 with no reversals. Food is 1.82× base in ENG and 2.2× in France.
- Peasants start at SoL 10 and are back at 1 by month 6, in London, Gujarat and Corsica alike. London's laborers and workers hold at SoL 34–35.
- Consumer goods, coal, services, textiles, wood, fiber, iron, chemicals and machinery sit at the cap. Much of the steadiness (total variation 2.6 over the same 23 series) is goods that don't move.
- ENG revenue starts at 7.06K (8.27K at 0.3) and settles at 5.2K. The treasury ends at −414K (−279K at 0.3). The M00 parity figures for revenue no longer apply.
- No new diagnostics. One division by zero in the old trade-rationing code (`trade_update_quantity`), once in 60 months.

## Left over
- **Old saves** have no `target_price@`: their prices stay put until the first weekly tick sets the targets. The pop spending cut only takes effect in a new game, since the SoL tables are built at startup.
- **Gradual prices make utilisation look fast.** Hiring still moves up to +20 or −25 points a month, faster than prices now close ordinary gaps. M04's national target utilisation is meant to be slower. Revisit the step defaults then.
- **The startup steel gap from M00** (in-game 4.83 against 9.64 in the simulator) is untouched: `_init_trade` still prices at the snapped startup target.
- **Trade AI items** found along the way are in [backlog.md](backlog.md): the month-boundary lag, the undefined `trade_ai_remove_unproductive_route`, exports above production, and members' frozen world prices.
