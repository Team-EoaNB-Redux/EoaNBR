# Segment 05: country-level industries

> **Archived 2026-11-11.** Superseded by the milestone plan in [../00_README.md](../00_README.md), built on the new spec [EOANB_Redux_Economy_Redesign_Updated.md](../EOANB_Redux_Economy_Redesign_Updated.md). Kept for history: status and file references below are as they were when archived.

From the redesign spec (§1–6, 12, 31–32). Not started. Do once PMs work in-game and startup is sane. Strat's reason for the order: move PMs first so the data model isn't done twice.

## Principle
> States host industry; countries perform as much repeated economic arithmetic as possible.

States stay meaningful: where industry is, local wages, employment, Infrastructure Efficiency, resources and land, local modifiers, which PM/AM is used, where capital sits. There are no local commodity prices. The aim is to cut state-scope traversal, modifier lookups, PM recomputation, and reconstructing country values from scratch. Not to cut goods or industries.

## Target
- **State-industry keeps only:** size, employment, PM, AM, and financial history actually used by later decisions (trailing profitability, construction state). Output, inputs, payroll, revenue and infrastructure use should be derived, not stored, where practical.
- **Aggregation key:** country × industry archetype × PM/AM combination, because colonial and core territory differ.
- **Bake slow modifiers** into effective coefficients per state-industry, recomputed when something changes, not each tick.
- **Country level does:** prices, shared PM input and output valuation, sector totals, supply/demand, trade, opportunity aggregation.
- **Dirty updates:** rebuild contributions on owner change, annex, split, PM/AM change or modifier change. Border change isn't a reason to rebuild everything.
- **Employment stays state-side,** and should be the main remaining state calculation: wages differ, and profitability differs by state.
- **Base Activity = Size × Employment Rate.** Then inputs and outputs follow from PM, AM, effective modifiers and Infrastructure Efficiency.

## Ticks
Main economy monthly. Trade weekly, using already-available country data, without recomputing state production.

## Monthly flow
State persistent data → slow modifiers cached → country/archetype economics → state employment → IE throughput → actual inputs, outputs, payroll, profit → country supply/demand/sector totals → owner dividends → capital pools → opportunity allocation → construction.

## Why the PM pass helps
- PM values are linear in size: quantity per K × employees × size. Easy to aggregate.
- All PM data is global, so per-country copies are already gone. Only `pm_throughput_factor` and `pm_employment_factor` are per country.
- `get_pm_values` is a natural place for shared valuation: compute per market once, read everywhere. Remember triggers (GUI, localisation) call it, so it stays in plain temp effects.

## Likely wins, biggest first (from the sim profile)
`r_weekly_trade`, `market_update`, `market_calculations`, `_country_advance_time`, `trade_update`. Most `input@bu` arrays can go once values are aggregated. `industry_production_update` is still per industry per tick; its `industry_dirty_var` gate is commented out.

## Risks
Economy of scale and per-industry factors are size- or state-dependent, which breaks pure archetype keys. Bake them per state. GUI reads `production@bu^i`, `input_amount@bu^i`: derive on demand or keep cheap copies. Save-game size matters too: fewer variables is a goal in itself.

## Test
Compare against a pre-change sim run with `ecosim_cli.exe compare`. Totals should match closely, since this is a performance refactor rather than a redesign.
