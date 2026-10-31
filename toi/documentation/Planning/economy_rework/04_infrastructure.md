# Segment 04: Infrastructure Efficiency tuning

Built and hand-checked against formulas in the sim (London, 2026-10-30). Not tuned. Code: `calc_industrial_capacity` in `_economy_market.txt`.

## As built
```
base = global.base_industrial_capacity + base_infrastructure_per_pop × pops × (1 + base_infrastructure_factor)
S    = base + Σ rail transport + Σ port shipping × port_transport_share + local_industrial_capacity_modifier
D    = Σ transport demand + local_industrial_capacity_use_modifier
IE   = S<D: max(S/D, 0.25)   S≥D: 1 + 0.2 × (1 − D/S)   D=0: 1.2
pay  = base price × clamp(D/S, 0.25, 2)     (stored in price_industrial_capacity)
modifier = 1 + (IE − 1) × dependence        (scales inputs and outputs, never jobs)
```
- Demand excludes the modifier, so IE can't feed back on itself. One-tick lag.
- Industries don't pay. Railways and ports get output × pay rate with no payer. That revenue counts in GDP (`gdp_update`).
- Names kept from the old system: `industrial_capacity` = S, `industrial_capacity_use` = D. 119 files use those modifier names.

## Knobs (`buildings_global_var_setup`)
`base_infrastructure_per_pop` 0.0055, `port_transport_share` 0.23, `infrastructure_efficiency_floor` 0.25, `infrastructure_efficiency_bonus` 0.2, `transport_pay_floor` 0.25, `transport_pay_cap` 2, `infrastructure_dependence_by_type` (farming 0.3, resource 0.6, factories 1, urban 0.5). Road techs add `base_infrastructure_factor` +0.6, +1.4, +2.0, +3.5.

The 0.0055 rate preserves ENG's 1857 base + roads (28.9 vs 29.1 in London) given gravel roads at +0.6.

## ENG at startup
S / D / IE / pay: London 437/151/1.13/0.34, Lancashire 714/323/1.11/0.45, West Midlands 344/343/1.00/0.99, Yorkshire 328/354/0.93/1.07, Sussex 191/232/0.82/1.21, Wales 188/277/0.68/1.47.

## Open
1. **Rail and port pay is low in hubs.** Demand fell (old London 286, now 151) because farms have no transport rows and sheet quantities are lower, while supply rose. Railways lose money in ENG at start. Options: raise transport rows, add farm demand, or change the pay curve.
2. **Zero-demand rural states get IE +20%,** so about +6% farm output with no real infrastructure. Maybe scale the bonus by actual supply per pop.
3. **Ports are paid from the state's D/S,** not shipping usage. ENG's national shipping usage is only 0.145 (capacity about 14K vs 2K used), so using it would cut port income badly. Shipping capacity itself fell to about a third of old (Anchorage 12/K old vs 4/K sheet). Check trade doesn't choke.
4. Subsidies for excess infrastructure (spec §9) don't exist yet. `infrastructure_subsidy` budget variables exist but do nothing here.
5. Does the HOI4 infrastructure building matter? Base uses population only, per Strat.
6. Spec wants railway growth to feed back through investment: needs segment 06.
