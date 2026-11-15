# M09: Investment

**Spec:** §13, §3.1. **Depends on:** M04–M07. **Questions:** Q34–Q39, Q60, Q117–Q126, all decided. **Status:** done in the simulator, and checked in-game in Strat's July 1857 autosave (2026-11-15).

## Goal
Capital comes from:
- **Sector retained capital**, which expands the sector that earned it. Incentives set how much profit is retained rather than paid out (Q39).
- **One general investment pool,** fed by:
  - a share of each sector's retained earnings, set by the financial laws;
  - pops' own investment, out of after-tax income (Q36);
  - the government;
  - foreign capital and bank credit, which arrive with M11 and M12.

There are no investor-type pools, and no geographic mobility rules: states aren't independent economic units (Q34).

Opportunities are ranked in ROI tiers. Retained capital uses the tiers to choose locations within its sector, and the general pool uses them to choose between sectors. Hard caps, throttles and one project per state-industry keep it cheap. Bad incentives should mean little growth.

## Built
All of it is in `_economy_investment.txt`, which replaced the old opportunity system. The file's header explains the whole flow.

**The monthly flow** adds no state loop:
1. `investment_prepare` (country, after `sectors_monthly`):
   - clears last month's opportunities;
   - pauses the construction of sectors over their debt limit;
   - picks the greenfield search list.
2. `investment_state_opportunities` (in the state loop, after `industries_monthly`) finds each state-industry's opportunity from last month's accounts, and each searching sector's best new state.
3. `investment_monthly` (country, after `sectors_update` and `update_country_pop_stats`) takes in the month's money, pays construction bills, funds the opportunities best tier first, and starts what's funded at once.

**Pools:**
- **Sector capital** (`sector_capital@`): retained earnings repay sector debt first. Then `sector_capital_mobility` of them goes to the general pool: `global.sector_capital_mobility_base` (0.2) plus the new modifier of that name, for the financial-system laws to set in M13. The rest is the sector's capital.
- **The general pool** (`investment_fund`, so content's `add_investment_fund` still works) takes that share, pops' investment (Q60) and the development fund.
- **The infrastructure fund** (`infrastructure_fund`) takes the infrastructure line.

**Opportunities** come one per state-industry a month: a plant with both an upgrade and an expansion offers the one with the better ROI. None is offered while a state-industry is building, retooling, losing more than the decay margin or paused (Strat's addition). There are five types:
1. **Expansion**, of an existing plant (Q120). A sector expands while its target utilisation is above `global.investment_target_utilisation` (80). A plant may build size × (its utilisation ÷ 80 − 1), within:
   - its known deposits, for RGOs;
   - the free arable land, for farms;
   - the free labour (Q119): unemployed, plus peasants, plus 3% of the employed, over the plant's employed per level. Each opportunity takes its workers out of the state's figure.
2. **A new plant** in a new state, or in a sector new to the country: `global.investment_new_plant_size` (1) levels at the sector's newest methods. Each searching sector keeps its best state, so at most one new establishment a month (§13.5). The search list holds the sectors that want to grow, best margin first, then the best sectors new to the country while the pool holds `global.investment_new_sector_min_pool`. It's capped at 2 + 0.05 per state, at most 6. Transport is left to the infrastructure fund.
3. **PM or AM upgrade** to the sector's newest (Q38), priced as the plant would be against the plant as it is, from the PM/AM cache. A state prices its upgrades in a quarter of months (`global.investment_upgrade_check_chance`).
4. **Prospecting** (Q30), by an RGO that wants to grow but works all its known deposits.
5. **Infrastructure** (Q122): a railway level where a state is short of transport, and a port level on the coast while the market is short of shipping.

**Tiers** (§13.4): ROI is a year's operating profit over a level's full cost (construction plus investment cost). Existing plants use trailing margin × last month's revenue; new plants and upgrades use the PM/AM cache at the state's wage, Infrastructure Efficiency and quality. Exceptional is above 20%, Good above 10%, Fair above 5% and Marginal above −5% (`global.investment_tier_roi`). `sector_opportunity_value@<sector>^<tier − 1>` is what each tier of each sector can absorb, at capital cost (headroom × construction cost).

**Funding**, tier by tier:
- **Indivisible projects** are funded whole first, in the order found (Q121): upgrades from the sector's capital, prospecting from the sector's capital and then the pool.
- **Expansions are pro rata by sector** (Q125):
  - each sector's capital pays the investment cost (25%) of as much of its own as it can;
  - the pool funds the same share of every sector's remainder at full cost (Q117), the construction cost going into the sector's construction reserve (`sector_construction_reserve@`);
  - within a sector the money funds whole projects in the order found;
  - a project it can only part-fund needs the sector's minimum (Q126, `sector_investment_min@`): `global.investment_min_project_start` (1) levels in the month after the sector's last start (`sector_last_investment@`, a month index that reads 0 until then, which is game start), falling `global.investment_min_project_step` (0.1) a month to `global.investment_min_project` (0.1). The minimum is set once a month, so a sector can start several projects in the month it invests. Upgrades, prospecting and infrastructure are exempt and leave the clock alone;
  - pool money a sector declines goes to the tier's declined projects in the order found, and what's still left waits for next month instead of funding a worse tier, or a lower tier's prospecting;
  - the sector's own unspent capital stays put.
- **Infrastructure** is funded whole, at full cost.
- What's built belongs to the generic owner (financer 0, Q37).

**Construction bills and debt** (Q117, Q118):
- `sectors_update` sums each sector's bills (`sector_construction_bill@`) for the construction and retooling it pays for.
- `investment_monthly` pays them from the reserve, then capital, then `sector_debt@`, which has no interest until M11.
- A sector whose debt is above `global.sector_debt_limit` (0.5) × its plants' value (`sector_asset_value@`, at its newest methods, built and being built) pauses: its construction buys no goods and makes no progress (`industry_update_construction_retooling`, `on_monthly_industries`), and it starts nothing new.
- A sector with nothing under way returns what's left of its reserve to its capital.

**Government lines** (Q122) are `development_fund_spending` and `infrastructure_investment_spending` in `spending_update`, each a share of GDP. They go in `subsidies_spending`, and are set by `change_development_fund` and `change_infrastructure_investment`, at most `global.government_investment_max` (5%). They're 0 for everyone, the AI included, until U1 adds their controls.

**Capacity decay** (Q87) is on. It's folded into the trailing-margin loop, and it skips railways and ports, which aren't paid for what they carry until Q31.

## Deleted (Q4)
- The old opportunity system, national opportunities and the fund's spending (`_economy_investment.txt`), and the buckets prototype (`_economy_investment_buckets.txt`).
- `global.eco_investment_enabled`, its gates, and the old investment and bucket globals.
- `industries_highest_productivity_update`, `industries_retoolable_update`, `industry_get_highest_pm` / `_am`, `calc_construction_cost`, `get_am_values`, `get_io_cost` and `get_size_count`. Only the old system used them.
- Company projects (Q123): `companies_select_project`, `companies_project_update`, `companies_fund_project`, `companies_drop_project`, `calc_company_size_count`, the `global.company_project_*` records, and their GUI.
- The overview window's investment opportunity and national opportunity blocks, their scripted GUI, scripted localisation and localisation keys (Q124). Until U2 builds Sectors, `effect eco_investment_report = yes` logs a country's pools, what they funded and each sector's capital, debt, construction and tiers.

## Fixed along the way
- **`retool_industry_no_update` dropped the financer of every new retool:** its financer check was inverted. A government retool would have been charged to the general pool, and its bills to the sector.
- **The great-power scoring (`0_eoanb_scoring_effects.txt`)** found each country's place by searching the whole country list, for every country, with a break that never fired. `create_econ_order_array` runs it weekly and monthly, so it was 23% of all tick ops. It now loops the score array once. The positions and the ledger are bit-identical in the simulator, and the tick takes 20% fewer ops.
- **`add_x_industry_internal`** takes `skip_update_temp`, which decay and construction completion set because the state loop recomputes the industry later that month.
- **Upgrades crowded out expansions** (found in-game, 2026-11-15). In a state's upgrade month, an upgrade at any tier took the plant's one opportunity, so in Strat's save Sheffield's tooling offered a Marginal upgrade instead of its Exceptional expansion. The plant now offers whichever pays better, at the same ops.
- **Wages fell 2% a month in states with only bureaucrats** (found in-game; M02 code). Population growth and `pops_balance` leave a few hundred-thousandths of middle class above the bureaucratic jobs. `employment_update` read that as an industrial workforce at 0% utilisation, and by month 2, 592 states had taken the cut. An industrial workforce under 10 people now counts as none. The simulator never showed it, because its state populations don't grow.

## Testing
Runs on `world_1857_eng`, 60 months, `--watch-file watches/m09.txt`: `redux-eco-sim/runs/m09` against the M08-code baseline `runs/m09_base`.

**ENG's profitable sectors grow** (end of month 60):

| Sector | Start | End |
|---|---:|---:|
| Urban centres | 2 | 10.3 |
| Tooling | 2 | 5.2 |
| Coal | 6 | 6.8 |
| Textiles | 2 | 2.3 |
| Consumer goods | 2 | 2.4 |
| Crop farms | 2 | 2.8 |
| Steel | 1 | 1.1 |

- The working class ends 66% above the baseline, as peasants take the new jobs.
- Prices of what's built fall (tools −25%, food −17% against the baseline), so nominal GDP ends 6% under the baseline while real output rises.
- Tooling borrows for its bills (about £3.8M of debt by month 60), within its limit.
- Urban centres' growth is fast because their margin is about 85%, which is for M14.

**Nothing is built without capital:**
- The pools never go negative, and the pool spends at most what it holds.
- Sectors with trapped capital keep it: wood (USA) and iron (ENG) work all their known deposits.

**A sector new to the country waits for outside money:** on the stripped map, France, Austria, Prussia, Russia and Portugal found new sectors from their general pools (pops' investment), with no capital of their own; their reserves pay the bills.

**Lowering incentives slows growth** (`scenarios/world_1857_eng_low_incentives.txt` pins ENG's incentives 70 lower):
- pops invest 34% less and sectors retain 41% less;
- urban centres reach 6.5 levels instead of 10.2, and tooling 3.3 instead of 5.

**Government lines** (`--set ENG.development_fund_percentage=1 --set ENG.infrastructure_investment_percentage=1`):
- 1% of ENG's GDP is about 65 a month each, and the development fund reaches the pool.
- No ENG state is short of transport, so its infrastructure fund only accumulates.
- France at 20% on the stress map built a railway level from it.

**Cost:**
- On the stripped map M09 adds about 2% of ops. The scoring fix more than pays for it: 9.37M ops a month against the baseline's 11.50M (−18.6%), and 1.15 s a month against 1.26.
- On `world_1857_stress` (a generated history with industries in all 491 states of 500K people or more, 5,575 state-industries; `redux-eco-sim/tools/make_stress_history.py`), investment adds 2.8% of ops, about 225K a month in `_economy_investment.txt`. With the scoring fix the stress map runs at 10.34M ops a month against 12.31M (−16%). Compare with `runs/m09_stress_base` and `runs/m09_stress`, 12 months.
- The first version added 5.2%. These brought it down:
  - a cheap gate before each plant's check;
  - upgrades priced in a quarter of months;
  - decay folded into the margin loop;
  - no redundant recomputes in decay and completion;
  - the borrowing limit worked out only for indebted sectors.

**Diagnostics:** no new kinds against the baseline, and no `load_error`, `math_in_trigger` or `math_array_read`.

**After the in-game fixes** (`runs/m09b`): ENG's sectors end within 0.3 levels of `runs/m09` (steel 1.3, textiles 2.4, crop farms 2.6, consumer goods 2.2), at the same ops. The wage fix changes nothing in the simulator.

**The minimum investment** (Q126): `runs/m09c` against `runs/m09b`, with every project start logged over 24 months in scratch copies of the mod, one with the old funding:
- The same money goes into fewer, bigger projects: 167 starts and 78.7 levels, against 221 starts and 77.2 levels.
- Partly funded projects fall from 154 to 57, and those of 0.2 levels or less from 82 to 17, none before month 11. New plants funded whole rise from 23 to 42.
- Small projects funded whole rise from 29 to 42. They're exempt by design, being all their plant can take under the 80% rule.
- Urban centres grow in bigger steps and saturate their market about a year earlier. Their target utilisation then falls, as it does a year later in `runs/m09b`.
- ENG's pool now holds money between projects (about £1.2M at month 60), and the USA's idle pool is 39% smaller.
- Ops: −0.3% on the stripped map, where fewer starts mean fewer construction updates, and +0.1% on the stress map against `runs/m09_stress` (`runs/m09c_stress`, 12 months). Diagnostics are unchanged.

**In-game check** (Strat's July 1857 autosave, month 2, on the code before the two fixes):
- `error.log` has no zeroed math expressions, nothing calls a deleted effect, and the economy files' errors are all older (banking, which is off, and GUI buttons for effects that don't exist).
- ENG's month-1 `eco_investment_report` matches the simulator's to 1–2%: the pool took in 953 (simulator 959), sector capital funded 372 (374), and both started 4 projects. The tier values match too (coal's Exceptional 72 in both, consumer goods' 11,925 against 11,873). The exception was tooling, whose upgrade roll differed, which is how the upgrade bug showed.
- At month 2, no country has a negative pool, capital or reserve, nothing is paused, and only the USA holds sector debt (29). Qing founded four sectors from its pool. The USA's construction matches state by state, mostly to 1%.
- Where the in-game and simulated runs went different ways: Qing built in state 594 instead of 126, and ENG's new consumer goods plant went to state 119 instead of 113 (a tie, with identical wage, infrastructure and quality).

## Left over
- **The simulator's fidelity,** from the in-game check:
  - its state populations don't grow, and in-game ENG has 0.2% more people by month 2;
  - it visits a country's states in a different order from the game, so exact ties between states go another way;
  - `read_save.py` leaves the `dockyard` token unnamed (the game numbers it 19446).
- **Railways and ports** expand privately only where they already exist and pay, since investment_economics leaves out their pay. New ones and their upgrades come from the infrastructure line until Q31 gives that pay a payer.
- **Prospecting through investment** happens only in states that already work the RGO. States with only potential deposits rely on the Prospect button.
- **Not in the ROI:** slaves' unpaid labour, in the payroll estimate for new plants and upgrades, and economy of scale.
- **Small projects that remain after Q126:** a whole expansion of a small plant, whose 80% headroom can be 0.1–0.2 levels, still holds its plant for a full build. A sector that has waited ten months accepts 0.1 levels again, so a small pool can still open several thin first plants at once, since every clock starts at game start. `global.investment_min_project_start`, `global.investment_min_project_step` and `global.investment_min_project` are the knobs for M14.
- **Order:** "the order found" is the state loop's order, so lower-numbered states are offered money first within a tier.
- **The general pool fills up** when a country runs out of opportunities (the USA's holds about £37M by month 60), and pops' investment is then damped by `calculate_investment_appetite`, as before.
- **`refresh_construction_list`** runs for every state of every country each month (1.4% of ops) though only the player's screen uses its list. It also keeps unbuilt buildings' methods at the newest, which `get_total_construction_cost` reads, so it was left alone.
- **Left in place, unused:** the old investment `scripted_loc_inline_*` keys in `scripted_localization_in_line_l_english.yml` and the `GFX_investment_opportunity_background` sprite.
- **UI:** the Sectors tab (U2) shows the tiers, opportunities and fund-expansion button; the Budget tab (U1) adds the development fund and infrastructure controls.
