# Segment 03: startup balance

Do after 01 and 02. Goal to agree with Strat first: the last pass was "mechanical only". A sensible next bar is eng_1857 stable for 60 months, startup GDP near target, most goods at 0.5–2× base.

## Numbers
**In-game, a real balance reading:** June 80.7K, July 62.0K + bankruptcy, August 52.5K, September 79.7K. The only bug behind these was maintenance being 0, and that barely moves GDP.

**Sim:**

| | Old code | New |
|---|---|---|
| ENG startup GDP, eng_1857 | 134K | 94K, settling near 57K by year 5 |
| ENG startup GDP, world_1857 | 134K | 74K |
| ENG GDP after 12 months, world_1857 | 73K | 16.6K |
| Monthly budget at startup, eng_1857 | +410 | −23.8K |

eng_1857 startup prices: food 3.27 (base 2), consumer goods 13.48 (5), machinery 27.22 (20), steel 32 (cap), services 3.60 (2), wood 1.00 (2), iron 2.06 (3), luxuries 1.72 (6).

**Game vs sim, September, ENG** (`read_save.py`, sim world_1857 with maintenance off). Output agrees. **Demand doesn't**, so that's the gap to explain first:

| Good | Output, game | Sim | Demand, game | Sim | Price, game | Sim |
|---|---:|---:|---:|---:|---:|---:|
| food | 11,563 | 12,575 | 22,306 | 20,705 | 3.98 | 3.62 |
| wood | 3,765 | 4,283 | 6,471 | 5,056 | 4.49 | 2.79 |
| iron | 1,929 | 1,627 | 1,857 | 1,046 | 2.78 | 1.24 |
| coal | 3,542 | 3,773 | 3,538 | 2,676 | 2.00 | 1.01 |
| consumer goods | 2,303 | 2,376 | 3,066 | 2,113 | 8.87 | 3.95 |
| textiles | 1,216 | 1,296 | 3,091 | 2,402 | 16.00 | 13.74 |
| services | 2,842 | 3,037 | 5,285 | 3,518 | 6.92 | 2.68 |
| entertainment | 52 | 55 | 245 | 87 | 20.00 | 12.40 |

GDP 79.7K vs 56.7K, net budget +7.7K vs −5.3K, treasury +11.8K vs −5.0K. Pops have more to spend in-game than in the sim. Find out why before tuning against sim numbers.

The market is expensive because pop demand is well above output: consumer goods 1.3×, food 1.9×, textiles 2.5×, entertainment 4.7×. Coal, iron and machinery stay cheap because mostly industries buy them, and many industries have shrunk (London: machinery 30% employed, railway 10%, entertainment 10%).

## First decision
**RGO `base_employees`:** see [segment 02](02_pm_assumptions_review.md). Decide first, because it changes every state's startup jobs.

## Known problems
1. **Bankruptcy.** ENG deficit in eng_1857 is almost all `other_spending` (20.2K of 39.5K), which is `trade_spending`, the negative trade value in `_economy_budget.txt`. Pins were rescaled to keep dollar values, so something else moved. In-game trade isn't pinned, so diagnose in world_1857 or with `read_save.py`. Revenue is also 15.7K. Treasury went to −2.4M with `national_debt` at 0 in the sim: find out why it isn't borrowing there, given the game went bankrupt.
2. **World oscillation.** Coal $0.50–8, machinery $5–80. Old notes: P = B·(D/S)², hire/fire steps up to +20/−25 points a month, revenue uses last month's price. Capping steps at 5–10, or a linear price curve, stopped it in a fantasy test. The old code fell 46% in a year too.
3. **Steel at the 4× cap** in ENG: Blister makes about 133 against about 544 needed, and nothing upgrades it with investment off. Prussia and the Primitive starters have it worse. Machinery PMs use steel, so it feeds through.
4. **Consumer goods short:** ENG demand is high after pins, price 2.7× base at start.
5. **Mining output down** about 30% in the 250 Shaft Mining states.
6. **Professionals and specialists have no PM jobs.** Watch `pops_balance`, spending and SoL.
7. **Base wages drift** to about 1.3 in eng_1857 by year 5, from 3.2. Either wages are too sticky at start or VA is too low.

## Where to start
Fix startup supply/demand per good in world_1857, using `read_save.py --json` for the game and `sector_report`-style dumps for the sim: sum `revenue`, `expenses_input`, `expenses_payroll` by industry across ENG states, plus `price`, `production`, `demand`, `trade` per good. (That helper was in a scratch folder; recreate it from a `for_each_loop` over `industries` with `log` lines, via `ecosim_cli.exe effect --scope ENG`.) Then address oscillation, or balance results won't hold.

## Tunables
`global.base_price@`, `global.wage_multiplier@`, `global.maintenance_rate`, `set_tech_*` base wage defaults, and the sheet.
