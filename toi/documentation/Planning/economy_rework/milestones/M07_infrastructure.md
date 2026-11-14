# M07: Infrastructure

**Spec:** §8. **Depends on:** M04. **Questions:** Q31, and the follow-ups Q102–Q105, all decided. **Status:** done in the simulator 2026-11-14; the in-game check is still to do (see Left over). Baseline: `redux-eco-sim/runs/m07_base` (`world_1857_eng`, 60 months, `--watch-file watches/m07.txt`). The old code with the test railways and ports: `runs/m07_rail_pre`. Result: `runs/m07_a`.

## Goal
Infrastructure Efficiency was already built, and the spec keeps it. What was left: cap the transport supply states get from population, price shipping by its use, pay ports from it, and run railways and ports as national sectors.

## Exists now
Formulas and knobs are in [archive/04](../archive/04_infrastructure.md). `calc_industrial_capacity` is in `_economy_market.txt`. Dependence by sector is subsistence 0, farming 0.3, extraction 0.6, factories 1 and urban 0.5, which matches §8.

Railway and port revenue has no payer, and that stays (Q31). Industries pay for congestion through lower throughput, and charging them a fee would localise the cost and remove part of the optimisation problem. The extra money only nudges prices up.

## Build
1. Keep the spare-capacity bonus as it is (Q102): states with excellent infrastructure get a bonus, and that can mean populous states.
2. Cap the supply from population after roads (Q103). The cap is `global.base_infrastructure_cap`, plus an absolute modifier, times a relative one.
3. The shipping price follows the market's shipping usage (Q104). Traders pay it per unit of shipping, and ports are paid it per unit of capacity.
4. Pay a port's local transport share at the state's rate, as a railway's (Q105).
5. Run railways and ports through the M04 sector layer. Building more of them is investment, in M09.

## Done when
- Infrastructure Efficiency in ENG's hubs is about where it was before the change.
- Supply from population stops at the cap.
- Ports earn from shipping use, and railways and ports show up as sectors with revenue that follows use.

## What the code reading found (Q102–Q105)
- **Railways and ports were already sectors.** M04 gave them national accounts, transport figures (`sector_industrial_capacity@`, `sector_shipping_capacity@`, `sector_transport_revenue@`), target utilisation and dividends by size. Only their pay was left.
- **The "free bonus" wasn't Strat's.** M07's first plan said rural states got +20% they didn't build, and that the bonus should be scaled by built supply or dropped. An agent wrote that in segment 04 (2026-10-30), and the plan reorganisation copied it here as if decided. Strat keeps the bonus (Q102).
- **Population supply runs away in big states.** China's biggest states (20,000–26,000K pops) got 140–230 transport supply from population, six times London's 34. That's Q103.
- **Ports weren't paid for shipping use.** A port was paid its whole shipping capacity at its state's railway rate, and its transport share wasn't paid on top ("paid once"). Traders paid a flat shipping price of 1, set in `calc_shipping_capacity`.
- **No railways or ports exist on the test bed,** since the strip. The free population baseline covers all of the stripped world's transport demand, so a railway anywhere in it is paid the 0.25 floor rate.

## What was built (2026-11-14)
1. **The population cap** (Q103), in `calc_industrial_capacity`: supply from population = min(pops × `global.base_infrastructure_per_pop` × (1 + `base_infrastructure_factor`), (`global.base_infrastructure_cap` + `base_infrastructure_cap_modifier`) × (1 + `base_infrastructure_cap_factor`)), never below 0. The cap is 40, just above London. The two new country modifiers are in `00_economy_modifiers.txt`, with English names, and nothing grants them yet. The state's infrastructure tooltip names the cap.
2. **The shipping price** (Q104), in `calc_shipping_capacity`, monthly on the market leader: `price_shipping_capacity` = the latest weekly `shipping_usage`, clamped between `global.shipping_price_floor` (0.25) and `global.shipping_price_cap` (2), × `global.base_price_shipping_capacity`. Members copy it in `market_update`, as before. Trade's shipping costs and the trade AI read it unchanged.
3. **Railway and port pay** (Q104, Q105), in `industry_update`: revenue = goods + `industrial_capacity@` × the state's `price_industrial_capacity` + `shipping_capacity@` × `controller:price_shipping_capacity`. A port's `industrial_capacity@` is its transport share, so it's paid like a railway's. A railway has no shipping. `sectors_update` adds up `sector_transport_revenue@` the same way.
4. **Getters and tooltips:**
   - `get_industry_figures` splits the pay into shipping and transport the same way.
   - `get_pm_values` pays transport and shipping as above. It now also applies the throughput and output modifiers to their capacity, as `industry_production_update` does, so a railway's or port's PM tooltip no longer understates its pay.
   - The industry finances tooltip gains a Shipping line, so a port's lines add up to its revenue.
   - The infrastructure tooltip shows the transport pay rate and the shipping price.
5. **Test bed:** railways and ports in the history test blocks: London railway 1 and port 2, Lancashire railway 2 and port 1, West Midlands railway 1, Wales port 1.
6. **Simulator:** `watches/m07.txt`.

## Results (simulator, `world_1857_eng`, 60 months)
Against `m07_rail_pre`, the old code with the same test railways and ports (`runs/m07_a`):
- **Diagnostics are unchanged:** 243 errors, no `load_error`, the same division-by-zero sites. `check --parse-only` finds only the 9 older errors outside the economy, and `verify_pm_audit.py` finds 0 mismatches.
- **Hubs:** Infrastructure Efficiency at month 60 is unchanged: London 1.148, Lancashire 1.182, West Midlands 1.117. No British state reaches the cap.
- **The cap:** China's state 598 (25,855K pops) has 45 transport supply against 232.5 (the cap of 40, plus the flat 5), and state 605 has 45 against 217.6.
- **The shipping price:** ENG's starts at the floor (usage 0.07), and runs 0.37–0.50 from month 6. The USA has no ports on the stripped map, so its pool of 100 is overloaded (usage 1.4–2.2), and its price runs 1.4–2.0. At month 12, 234 of 238 markets are at the floor.
- **Ports:** at month 60, ENG's ports earn 57.7 a month from shipping and transport against 32.1, and their margin is 10.6% against 7.7%, at full utilisation (91% before). At month 12, London's port is paid 25.0 for shipping (56.4 capacity × 0.44), 3.2 for transport and 75.2 for its services.
- **Railways:** unchanged. They lose money (margin −89%) at the 10% utilisation floor, because the population baseline covers all of the stripped world's demand, so they're paid the 0.25 floor rate. That's the mechanism working: there's nothing for them to carry.
- **The world:** at month 12, world GDP is 0.03% higher and traded volume 2% higher, since most markets' traders pay a quarter of the old shipping price. ENG's GDP is 0.5% higher at month 60. No country's GDP changes by more than 3% (Haiti −3.1%, Tuscany −2.6%).
- **London's wage** ends 21% higher (1.73 against 1.43), because its busier port hires more. It's the known 0.5%-a-month rise wherever jobs are filled exactly (M02, Left over).

**Formula checks** (month-12 dump):

| Check | Result |
|---|---|
| A railway's revenue = goods + capacity × the state's rate | London 6.244 + 1.951 = 8.196, Lancashire 13.317 + 4.161 = 17.478, both exact |
| A port's revenue = goods + shipping × the shipping price + transport share × the state's rate | London 75.24 + 25.03 + 3.25 = 103.52 against 103.21. The dump holds the price set at the end of ENG's tick; the ports were paid last month's |
| A port's transport share | `industrial_capacity@` / `shipping_capacity@` = 0.23 in all three ports |
| The shipping price = usage, clamped | ENG 0.4435 at usage 0.4435; USA 2.0 at usage 2.16 |
| `sector_transport_revenue@` = the states' sum | 65.45 against 66.07, the same timing gap |

## Left over
- **In-game check:**
  - Load a new game and search `error.log` for "Errors occurred while reading math expression".
  - Read ENG's `price_shipping_capacity` and state 952's port and railway figures with `read_save.py`.
  - Open the state's infrastructure tooltip and a port's finances tooltip.
- **For M14:**
  - Decide which techs, laws or content grant `base_infrastructure_cap_modifier` and `_factor`. Until then a road tech adds nothing in a state at the cap.
  - Size railways and ports to demand on the rebuilt map. On the stripped map railways are paid the floor rate.
  - The shipping price floor and cap, and whether they should differ from the railway rate's.
- **Rail pay in hubs** (segment 04's open item) is balance: under the old 1857 map, London's railways were paid 0.34 per unit, because the sheet's transport demand fell while supply rose. It's for M14.
