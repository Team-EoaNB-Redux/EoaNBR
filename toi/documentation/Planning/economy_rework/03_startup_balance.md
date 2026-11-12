# Segment 03: startup balance (rebuild the map)

## Decision
**Strat, 2026-10-31: don't balance the current map. Rebuild it.** Comment out the economy in the state history files, which leaves everything as subsistence farming. Then build the map back up from scratch, so that world supply and demand start roughly equal for every good.

Why: on the current map ENG goes bankrupt in July, and it's a feature of both the sim and the game. In-game after the rework the Netherlands followed in December and ENG's GDP fell to 16.3K. The sim had predicted 12–33K.

Some asymmetry between goods is wanted (oil should be really good). That comes later.

## Steps
1. **RGO employees: done.** See [segment 02](02_pm_assumptions_review.md).
2. **Comment out the state economy: done 2026-10-31, uncommitted.** Ports and railways went too, on Strat's call.
3. **Fix debt and budgets for the new GDPs.** See below. **Next.**
4. **Build the map back up,** one sector at a time, checking each good's world supply against demand. Targets for the British Isles and India are in the history files: see below.

Bar for done, to agree with Strat: world_1857_eng stable for 60 months, startup GDP near target, most goods at 0.5–2× base.

## Step 2: the strip
`toi/documentation/scripts/strip_state_economy.py` commented out, in place, 1,576 non-zero resource entries and about 5,850 size lines across 1,095 state files. The old numbers stay readable as a reference for the rebuild. A check over all 1,455 files found nothing changed except those, and none are left active.

Kept, on Strat's call: 152 arms factories, 79 industrial complexes and 72 dockyards. Also untouched: `arable_land` (subsistence needs it) and the engine's `infrastructure`, `naval_base` and bunkers.

## What the strip does (sim)
`world_1857_eng`, with the new RGO table. No new script errors (246 errors, as before). `verify_pm_audit.py` and all tests pass, and `eng_1857`, `world_1857` and `british_isles` all run.

**It leaves subsistence farming.** 24,761 subsistence sizes and the 303 factories are all that's left. 434M of the 440M workforce are peasants: 235M on farms, 199M on marginal land. Nobody is stranded.

**It's stable for 60 months.** ENG's GDP goes 12.5K, 13.0K, 12.0K, 11.7K, then holds at 11.3K to the end. World GDP goes from 538K to 489K in the first year and stays there. There's no oscillation, so the swings on the old map came from industry and trade. Watch which sector brings them back.

`overflow` warnings grow with run length (3,002 by month 60), all at existing sites: `pops_sol` at `_economy_main_rework.txt:1273` and `1282`, from dividing by the population of tiny states. 140 states have under 10K people, on the old map too. Population doesn't change in these runs.

| Good | World supply | Demand, month 1 | Demand, month 12 | Price, month 12 (base) |
|---|---:|---:|---:|---:|
| food | 33,150 | 48,188 | 35,725 | 2.32 (2) |
| wood | 6,630 | 10,231 | 6,533 | 1.94 (2) |
| fiber | 1,326 | 4,607 | 3,759 | 12 (3) |
| iron | 0 | 2,496 | 1,679 | 12 (3) |
| coal | 0 | 1,072 | 71 | 8 (2) |
| luxuries | 0 | 888 | 106 | 24 (6) |
| consumer goods | 0 | 2,193 | 415 | 20 (5) |
| textiles | 0 | 3,081 | 936 | 16 (4) |
| services | 0 | 5,913 | 1,543 | 8 (2) |

- Subsistence alone almost balances food and wood.
- Everything else sits at the 4× price cap, so its demand here is suppressed. **Read the month 1 and 12 figures as a floor, not as targets.** Pop needs are set in dollars, so demand will rise as prices fall.
- Armies are a large part of what's left. In the June 1 save they took about 3,800 food, 3,400 wood and 2,400 iron a month.

**Debt and budgets break.** This is step 3:
- ENG (`debt_level` 249) and the Netherlands (96) go bankrupt in the first month. MNC and BRE follow within the year. France ends the year at 48.8 of the 49.9 limit, with a treasury of −75K.
- 40 countries hold debt by month 12. Starting debt was sized for the old GDPs.
- Spending doesn't follow GDP. France runs −15.0K a month on a GDP of 16.7K, and Russia −14.1K on 24.8K.
- By month 60, 8 countries are on `edc_bankrupt`, including Russia and Austria. France's treasury is −796K and ENG's −278K, with `national_debt` at 0.

## Step 4: targets
`eng_economy.md` and `raj_economy.md` are comments in the history files, as **a guide, not a rule** (Strat). They're targets only, and nothing active changed.

- **UK:** levels = the doc's workers / jobs a level on ENG's start PMs. Domestic service and housing are hidden, as neither has a building.
- **India:** levels are what makes the doc's value on each owner's PMs. The rest stay on subsistence, so it starts with few industries.
- **Where it is:** a table in each of 19 British Isles and 48 Indian states. Totals are in `ENG - Britain.txt` and `RAJ - British Raj.txt`, and the 15 other Indian tags have their own, including SRS.
- **The script:** the doc figures and splits are in `catalogue_1857_data.py`, and the steps in `catalogue_1857_targets.py`. A rerun replaces the blocks.
- **Tuning:** the PM values, wages and remaining work are in [pm_1857_tuning.md](pm_1857_tuning.md).

**Scale: 1,000 treasury = £1M, and doc figures are a year, so $ a month = £M × 1000 / 12.** £665M a year is 55.4K a month.

**Population, 2026-11-11:** the 19 British Isles states now hold the doc's 1857 totals: England 18.0M, Wales 1.25M, Scotland 3.0M and Ireland 5.95M, plus 52K for the Isle of Man in Lancashire. Inside each country the split follows the 1851 and 1861 county censuses, interpolated to 1857. Each county was placed by testing its towns against the map, and border counties are split. The old split looked modern: the Highlands had 108K against 395K, and Leinster 2.67M against 1.81M.

**Workforce:** the UK's listed industries hold 7.90M, including 0.41M subsistence farmers, against 9.89M in-game (35% of 28.25M). The doc's 28.2M at 40% would be 11.28M.
- The 1851 census has about 1.27M more that the doc leaves out: 477K in building trades and brick making, 377K labourers with no branch given, 228K army, navy, police and civil service, and smaller trades. These are GB figures.
- `global.pops_workforce_participation` is one value for everyone (`_economy_setup.txt:756`). At 40% the UK would have 11.30M and India 97.7M. That's untested, and arable land follows workforce.
- Three British states are `SHORT` of workers: Lancashire by 227K, because the doc's cotton jobs sit there, and the East Midlands and Yorkshire by under 20K each. Before the population fix it was nine.

**GDP per capita:** the sheet's 3.0 was Bairoc's UK GNP for 1860: 16,072M 1960 USD / 26.45M people, then converted, gives 3.04. At 26.45M people that's 80.4K a month, 45% above the doc's 55.4K. Strat has set the GDP tab to 2.3 for now, as modifiers will lift it. The tab still multiplies that by 1.2B people, so it applies a UK figure to the whole world.

**Other things it turned up:**
- The doc's population differs by region: Bengal is 69.2M in-game against the doc's 40M. The doc's figure looks low: from memory, not checked, the 1872 count was over 60M.
- Most UK "steel" in 1857 was puddled wrought iron (£19M of £22M). No PM represents it, so Bessemer stands in for it at the UK's start.
- `1092-Western Colorado.txt` has `owner = HYD`, which looks like a bug.

**After the retune, on the stripped map, 60 months:** ENG's GDP holds at 6.0K and world GDP is about 227K. Budgets are worse, so step 3 matters more: ENG runs −9.6K a month, its treasury reaches −425K, and FRA, RUS, SWE and SPR also sit below −50K. The figures under "What the strip does" are from the old PMs.

Colonies have no targets, as the doc has nothing on them. Nor do Ceylon, Nepal, Bhutan, Sikkim, Kalat and Upper Burma. The Hunt notes in the British state files are the source for coal by state: they sum to exactly the doc's 65.4M tons.

## Bankruptcy, for reference
This is what happens on the current map, and it will happen to any country the rebuild leaves over the limit.
1. ENG holds 1.5M of debt, and interest is 16,228 a month. `debt_level` (debt-to-GDP / 4) passes 49.9, which fires `egy_debt_system.7`.
2. The debt is wiped and `edc_bankrupt` is added. Spending falls from 27K to 9.6K, but the idea's `stability_factor = -0.65` takes stability from 72% to about 7%.
3. That costs about 11 points of throughput and 17 of consumer confidence. Lower confidence cuts pops' savings target, so they spend their savings: ENG's laborers earned 33K and spent 89K.

This was the "everything is expensive" market. On June 1 ENG's prices are ordinary (consumer goods 5.39, base 5). In the September autosave they were 8.87.

## How far to trust the sim
On the old RGO table, against saves from 2026-10-31, with nothing tuned:

| ENG | Game | Sim | Gap |
|---|---:|---:|---:|
| GDP, startup | 74,481 | 74,642 | +0.2% |
| GDP, June 1 | 78,346 | 78,749 | +0.5% |
| Net budget, June 1 | −11,007 | −10,781 | 2.1% |
| Trade profit, June 1 | 4,786 | 4,819 | +0.7% |
| GDP, July 1 | 62.0K | 65.0K | +4.8% |

June world prices were 0.9% off on average. **Those saves no longer match the code:** they're from before the RGO change and the strip. Compare only against a save made on the current code, and rerun `tools/import_save_inputs.py` from new saves, because the armies' production lines and backed-out stabilities in `save_inputs_1857.txt` come from the old map.

Still unexplained, and worth rechecking on the new map: why July GDP ran 4.8% high, consumer confidence after bankruptcy (0.87 in-game, 0.94 in the sim), war countries 4–6% high by June (no fighting modelled), and ENG's throughput factor (0.264 in-game, 0.252 in the sim).

## Problems that survive the rebuild
1. **World oscillation** on the current map: coal $0.50–8, machinery $5–80. Old notes: P = B·(D/S)², hire/fire steps up to +20/−25 points a month, revenue uses last month's price. Capping steps at 5–10, or a linear price curve, stopped it in a fantasy test.
2. **Professionals and specialists have no PM jobs.** Watch `pops_balance`, spending and SoL.
3. **Base wages drift** to about 1.3 in eng_1857 by year 5, from 3.2. Either wages are too sticky at start or VA is too low.

Steel and early machinery need checking as they return: on the current map ENG's steel sat at the 4× cap (Blister makes about 133 against about 544 needed), and with investment off nothing upgrades it.

## How to measure
`world_1857_eng.txt` only: `world_1857.txt` plays ENG as an AI, and `eng_1857.txt` fakes the rest of the world. `ecosim_cli.exe run --scenario scenarios/world_1857_eng.txt --months 12 --dump-json out.json`, then read `market_supply@<good>`, `market_demand@<good>` and `market_price@<good>` from `global`. Use `--mod <dir>/toi` to try a map change on a copy.

## Tunables
`global.base_price@`, `global.wage_multiplier@`, `global.maintenance_rate`, `set_tech_*` base wage defaults, and the sheet.
