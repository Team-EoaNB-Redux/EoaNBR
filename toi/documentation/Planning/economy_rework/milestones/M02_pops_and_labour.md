# M02: Pops and labour

**Spec:** §5, §23–30. **Depends on:** M00. **Questions:** Q8–Q14, Q57, Q58, Q61, Q62, and the follow-ups Q73–Q80, all decided. **Status:** done 2026-11-12, checked in the simulator and in Strat's month-1 autosave (see Left over). New baseline after the simulator's clamp fix: `runs/m02_d`. Baseline: `redux-eco-sim/runs/m02_base` (`world_1857_eng`, 60 months, `--watch-file watches/m02_base.txt`), identical to `m01_final`. Result: `runs/m02_b` (`--watch-file watches/m02.txt`).

## Goal
Collapse the ten pop types into five: slaves, peasants, working class, middle class and upper class. Unemployment is the gap between a class's pool and the jobs it fills, not a separate pop. Qualifications become a real barrier to industrialisation. Bureaucrats become government jobs and soldiers become active manpower.

## Exists now
- **Pop types:** ten in `global.pops_array` (`_economy_setup.txt`, `pops_global_var_setup`). `pops_update` runs the full pipeline once per type per state, so each type costs about the same. Soldiers and bureaucrats aren't used for anything.
- **Wages:** wage multiples are laborers 2, workers 4, professionals 10 and specialists 20. Professionals and specialists have no PM jobs: the sheet's Wrk and Mid columns are laborers and workers. Each state has one floating `base_wage` (`base_wage_update`, `base_wage_finalize`).
- **Moving between types:** `pops_balance` and `pops_convert` move pops toward jobs and must never change total population.
- **Qualifications:** `pops_convert` has a cap model. Literacy caps workers, professionals, specialists and bureaucrats, schooling caps professionals and specialists, and education caps specialists. The education check compares a variable with itself, so it never applies. All caps sit at 100%, so nothing binds. Strat's notepad (`toi/documentation/Strats_notepad_while_hes_at_uni.txt`, "Qualifications") has the stock model that was planned instead.
- **Slaves:** a pop type. The slavery laws are old ideas (`0_eoanb_demographic_laws.txt`). Cultures: each state has `pops_culture_array` (shares), and each country has `pops_marginalized_culture_array` (`_eoanbr_country_effects.txt`).
- **Laws:** the politics rework's laws are in `toi/common/ideas/_internal_politics_tokens.txt` as skeletons that set `current_law@token:<category>`. Their modifier blocks are empty, and no country history sets them yet. Yes/no modifiers already exist in `00_economy_modifiers.txt`, for example `state_land_allowed` with `value_type = yes_no`.
- **Government buildings** are always fully staffed. Their wages come from the state budget. M08 removes them.
- **Budget:** income tax brackets compare each pop type's average earnings with the national average (`_economy_budget.txt`). Administration and military payroll scale with earnings.
- **Where the tokens appear:** outside the economy effects, pop tokens are used only in `economy_scripted_loc.txt`, the English and Korean economy localisation, and the getters.

## Build
1. **Classes** (Q8): new tokens for the five classes. Laborers map to working class; workers, professionals and specialists to middle class; capitalists and landowners to upper class. Soldiers and bureaucrats are removed as pop types. Remove the old types everywhere, including `script_enums.txt`, the localisation and the GUI.
2. **Jobs per class** from PM and AM shares (Wrk to working class, Mid to middle class). Unemployment per class is the pool minus the employed. The upper class stays at about 2% of jobs (Q11).
3. **Wages** (Q9): keep one floating `base_wage` per state, with fixed multiples: working class 2 and middle class 4, the old laborer and worker values.
4. **Qualifications** (Q10, Q57): class mobility follows jobs, capped by qualifications. Build the notepad's stock model with a **single** qualifications value per state, not separate skilled and educated stocks.
   - Pops gain qualifications monthly from literacy, schooling, education, wealth and the workforce mix.
   - They lose them through death, conversion and decay.
   - Gains are cut for oppressed and non-accepted cultures, and under serfdom.
   - The middle and upper classes both need qualifications. The amounts are tuning.
   - Delete the cap model in `pops_convert`, which was a stopgap.
5. **Slaves** (Q12, Q62):
   - They fill working-class jobs before free workers, at no cost to the employer.
   - They count in the labour supply that sets the state's wage.
   - Only pops of marginalised cultures can be enslaved, and only where slavery isn't banned.
   - They receive no income, and their needs are negligible.
6. **Laws through modifiers** (Q61): the economy reads laws only through modifiers that the new laws set, defined in `00_economy_modifiers.txt`. Switches use `value_type = yes_no`.
   - The first is a ban on slavery, added by the new slavery law that bans it.
   - Slavery is allowed by default, so it stays allowed everywhere until country history sets the new laws.
   - Nothing reads the old law ideas.
7. **Bureaucratic jobs** (Q13, Q58):
   - The number comes from bureaucratic strain.
   - The jobs are spread over states by population, with non-core states needing fewer per head.
   - Ordinary bureaucrats are middle class. The capital also gets some upper-class government jobs, for department heads and senior bureaucrats.
   - The government pays them, and they compete with private jobs.
   - Administrative capacity = filled ÷ required, stored as a country value. It's meant to lower tax and spending effectiveness when short, which is the politics rework's "Bureaucratic Capacity" in `vanadiums_notepad_while_hes_crashing_planes.txt`.
8. **Active manpower** (Q14): HOI4's fielded and training manpower, taken from peasants and the working class in proportion to their numbers and spread over states by population.
9. **Budget:** the smallest change that keeps it working, with tax brackets, administration and military payroll on the new classes. The full rework is M13.
10. **Simulator:** update scenarios and tools that name old tokens (Q5).

## Done when
- No references to the removed tokens remain. Grep the whole mod, the simulator scenarios and the tools.
- Total population is conserved every month over 60 months.
- Qualifications bind: on the test bed, middle-class growth stops when qualifications run out.
- The simulator profile shows the pop pipeline costing about half what it did.
- The game loads, the pop screens show five classes, and the budget still balances its own books.

## What was built (2026-11-12)
1. **Classes** (Q8). `global.pops_array` is slaves, peasants, `working_class`, `middle_class` and `upper_class`, in `pops_global_var_setup`, `eoanbr_tokens.txt` and `script_enums.txt`. The old tokens are gone everywhere. So are their variable names:
   - Per industry: `working_jobs@`, `middle_jobs@`, `working_employed@`, `middle_employed@`, `working_bonuses@` and `middle_bonuses@`.
   - Generated PM data: `global.pm_workforce_working@` and `pm_workforce_middle@` (renamed in `generate_pm_data.py`, regenerated; `verify_pm_audit.py` finds 0 mismatches). The sheet's Wrk and Mid values are unchanged.
   - `global.industry_owner@` is gone, because the upper class owns everything.
2. **Jobs per class** (`employment_update`):
   - Each industry's Wrk and Mid shares go to the working and middle classes, and its owner places (`owner_jobs@`, 2% of jobs at the employment target) to the upper class.
   - This fixed a bug. Owner jobs were added from a temp nothing set (`i_owner_jobs`), so capitalists never existed and their dividends reached no one: 2,132 a month for ENG in Strat's July 1857 save. ENG's 94K landowners had no jobs either.
   - A class's unemployment is its workforce minus its employed.
3. **Wages** (Q9). One floating `base_wage` per state: working class 2×, middle class 4×, and upper class 10×, which is paid only for senior government jobs. Owners live on dividends. The per-type wage variables (`laborers_wage` and the rest) were never read, and are gone.
   - **Labour utilisation**, which moves the wage, is private working- and middle-class jobs against the slave, working-class and middle-class workforce.
   - Bureaucrats are left out on both sides: the government pays the going wage and doesn't bid it up. Otherwise every rural state, where the bureaucrats are the whole middle class, would see its wage drift up.
4. **Moving between classes** (`pops_balance`, Q10). It's rewritten for three classes, and `pops_convert` and `multiply_pops_change` are deleted, along with the cap model.
   - Classes short of workers take them in proportion from classes with too many.
   - A move that raises the qualifications needed is scaled down to the free stock.
   - The working class takes the other side of every move, so the total is exact.
   - `pops_peasant_job_migration` moves peasants into the working class only up to the shortfall, and back only out of the working class's own surplus. The two migration steps, freed slaves and the soldier draw now update `pops_workforce_balance@`, so `pops_balance` doesn't fill the same shortfall twice.
5. **Qualifications** (Q57, Q74–Q76). Each state has one stock, `qualifications`, in K qualified people. The middle class needs 1 per head and the upper class 2.
   - **Gains:** `pops_qualifications_monthly` adds them each month by Strat's notepad formula, × `global.qualifications_gain_scale` (0.001). Per K pops: (literacy − 10%) × 0.3, (schooling − 5%) × 0.5, education × 0.3, (wealth − 10) × 0.005, and the middle and upper classes' share of the workforce × 0.2.
   - **Cuts:** marginalised cultures −50% and non-accepted −10% (globals), each plus a law modifier. Peasants' gains are also × (1 + `peasant_qualifications_factor`). Slaves gain nothing.
   - **Losses:** 0.5% of the stock a month, for deaths and decay. A pop that moves down loses nothing (Q74).
   - **Start:** the stock starts at exactly what the starting middle and upper classes need, so it binds from day one.
   - **Inputs:** the literacy, schooling and education defaults are now 20%, 10% and 0.5%. ENG's country history sets 60%, 40% and 2% (Q75).
6. **Slaves** (Q12, Q62, Q73).
   - **History:** state history sets `slave_share`, a share of the workforce, taken from the peasants at startup. It's capped each month at the state's marginalised-culture share, or at 0 under `slavery_banned`. Freed slaves join the working class, and nobody is newly enslaved.
   - **Jobs:** slaves fill working-class jobs first. Industries pay no wage and no bonus for the enslaved share of their working-class labour (`slave_labor_share`).
   - **No income or needs:** `pops_update` only counts slaves, and `on_monthly_pops` skips their finances.
   - **Wages:** slaves count in the labour supply.
   - **Test shares:** 1860 census shares in `# >>> rework test slaves` blocks in Virginia (0.31), South Carolina (0.57) and Mississippi (0.55, which the cap trims to 0.53).
   - The culture shares come from `pops_culture_shares_calc`, which reads `pops_culture_array` against the controller's arrays. The demographics code's own tallies don't work, and Strat asked to leave that code alone.
7. **Laws through modifiers** (Q61), in `00_economy_modifiers.txt`:
   - `slavery_banned`: a yes/no modifier, set by `law_slavery_banned`.
   - `marginalized_culture_qualifications_factor`, `non_accepted_culture_qualifications_factor`, `peasant_qualifications_factor` and `bureaucratic_strain_factor`: defined for laws to set later. No law sets them yet.
8. **Bureaucrats** (Q13, Q58, Q77, Q78).
   - **Jobs:** `bureaucracy_and_manpower_update` runs at country scope, in `_init_country` and before each country's states every month. It sets each controlled state's `bureaucratic_jobs` = population × `global.bureaucrats_per_pop` (0.0015) × (1 + `bureaucratic_strain_factor`). Non-core states count at half weight. The capital adds 5% more as upper-class jobs.
   - **Filling and pay:** bureaucratic jobs fill at their class's job fulfillment, so they compete with private jobs. The government pays them through `administration_spending`.
   - **Administrative capacity** = filled ÷ required, a country value. Income, sales and corporate tax are collected at (0.5 + 0.5 × capacity) of their rate.
9. **Active manpower** (Q14): HOI4's deployed army, navy and air manpower, plus the deployment queue ÷ 1,000 (it's counted in people).
   - Each state's share, by population, is drawn from peasants and the working class in proportion to their numbers, and goes back the same way when soldiers demobilise (`pops_active_manpower_monthly`).
   - Soldiers sit in each state's `active_manpower`, outside the classes. Country population totals add them back in.
10. **Budget** (Q77).
    - **Administration** = bureaucrats' pay, plus the per-capita and per-GDP terms. The cost factor and bureaucratic efficiency apply to those two terms only. The 0.5%-of-earnings term and its small-country markup (`administration_base_expense`, `administration_population_expense*`) are deleted.
    - Income tax brackets are unchanged: they loop over the classes.
11. **Modifiers merged** (Q79). `upper_class_investment_contribution_factor` replaces the capitalists' and landowners' modifiers in about 30 places of content. Blocks that set both now set their sum: the static modifiers 0.2, the Ottoman constitution −0.3, and the anti-trust laws technology 0.15. The gated investment code reads `global.upper_class_per_investment_opportunity` (5).
12. **UI.**
    - The pop pie chart has five classes. Three segment textures are renamed and five are deleted.
    - Updated tooltips: population, building employment (now with bureaucrats, active manpower and qualifications), available workforce, dividends, industry employment and PM requirements.
    - Deleted localisation: the dead legacy pop table (artisans, clerks, officers and so on) and the old `pm_*_<type>_required_modifier` keys, in English, Korean and Russian.
13. **Simulator** (Q5): it now writes `profile.csv` with every effect's timing (the report lists only the top 25). Also new: `watches/m02_base.txt` and `watches/m02.txt`, and updated examples in `CLAUDE.md`, `simulation.h` and `watches/core.txt`.

## Results (simulator, `world_1857_eng`, 60 months)
**Population is conserved.** After 60 months, every one of the 1,455 states has its classes plus active manpower equal to its workforce, to 0.00001K, and no class is negative. Every move is paired, so a gap in any month would still show at month 60.

**Against `m02_base`** (`runs/m02_b`), with no new diagnostics:

| ENG at month 60 | Baseline | M02 | Why |
|---|---:|---:|---|
| GDP | 9,489 | 9,698 (+2.2%) | The upper class now spends its dividends |
| Revenue | 5,222 | 5,587 (+7%) | More pop spending and income to tax |
| Administration | 219 | 547 | Bureaucrats' pay, 408 by month 60 as wages rise |
| Military payroll | 192 | 215 | It follows average earnings, which now include the upper class's |
| Population, workforce | 29,950, 10,482 | the same | |
| Wages and test-industry employment | | within 0.7% | |

- ENG's upper class is 121K. London's goes from 0 capitalists and 12K jobless landowners to an employed upper class of 17K, whose income reaches 736 a month by month 60.
- ENG needs 41.2K bureaucrats, and capacity stays at 1.0. Its 228K soldiers come out of the peasants and the working class: 29.5K from London.
- **Slaves:** Virginia's 132K slaves hold all of its 13.5K working-class jobs (its government factories), so it has no free working class. The idle slaves count as labour supply (Q62), so Virginia's and South Carolina's wages fall 70% to the floor. On the stripped map there are no plantations for them to work.

**Qualifications bind.** A scratch copy added 20 urban-centre levels in London from January 1858, which raised its middle-class jobs from 16.7K to as much as 25.6K (`runs/m02_shock` and `runs/m02_shock_nogain`):

| London, months 0 → 35 | Middle class | Upper class | Qualifications |
|---|---|---|---|
| Normal gains | 16.7K → 19.8K | 17.1K → 18.1K | 51 → 56 |
| Gains set to 0 | 16.7K throughout | 17.1K throughout | 51 → 43 |

With normal gains, the middle class grows only as fast as qualifications arrive, about 0.1K a month. In the unshocked run, London's middle class never runs short: startup fills every job, and the test industries never hire beyond that.

**Cost (Q80: no slower than now).** The machine's speed drifted between runs, so the old code was rerun alongside (`runs/m02_base_rerun`, identical values to `m02_base`). Seconds over 60 months, from `profile.csv`:

| | Old code, same conditions | M02 |
|---|---:|---:|
| `pops_update` | 5.14 | 6.55 |
| `employment_update` | 3.74 | 3.13 |
| `update_country_pop_stats` | 2.29 | 1.37 |
| `on_monthly_pops` (with the new monthly steps) | 1.82 | 1.97 |
| `pops_balance` (with `pops_convert`) | 0.91 | 0.10 |
| `bureaucracy_and_manpower_update` | — | 0.14 |
| **Pop pipeline** | **14.04** | **13.29 (−5%)** |
| `_country_advance_time` | 47.9 | 46.2 |

Every loop over the pop types halved. `pops_update` grew 27%, as Q80 expected: bureaucrats give almost every state a middle class, so a typical state now runs three classes instead of two. The rest of the speed-up is M03's refactor of `get_pop_needs` (2.7 s) and its removal of the savings steps.

## Left over
- **In-game test (Strat).** Check that the game loads, the pop pie chart and tooltips show five classes, and the budget screen adds up with the new administration line. Saves from before M02 hold the old token data, so start a new game.
  - **First try, 2026-11-12: everyone was a peasant.** `error.log` showed all 37 math expressions in `_economy_main_rework.txt` from line 539 on, and the 5 in `state_eco_employment_init`, reading 0. Two older load errors came before them in their files: a `log = ""` at `_economy_main_rework.txt:124`, and calls to `_update_state` and `market_pops_industry_recalc`, which don't exist, in `_country_reset`. Fixed by removing the empty log and commenting out the two calls. The probe file's deliberate max-before-min clamp did the same to its later probes, so it's commented out too. The simulator missed it because it compiled effects only when they ran. It now runs a load pass, reports `load_error`, and zeroes the same expressions. A copy with the old lines matches the startup save on every pop and job variable. The dead `trade_ai_remove_unproductive_route` call in `_economy_market.txt` was removed too, before it could do the same.
  - **Second try, the 1857.6.1 autosave: works.** ENG's classes match the simulator within 0.2% (working 293.1K, middle 77.6K, upper 121.4K), as do bureaucrats (41.2K), active manpower (227.7K) and administration spending (461.7 against 461.0). GDP is within 0.3%. Revenue read 4.4% high in the simulator until its `clamp_temp_variable` was fixed. With crossed bounds the game keeps the min, and the simulator kept the max, which zeroed pops' net money in `pops_handle_savings`, so every class lost 2 SoL fewer than in-game. After the fix, Lancashire's SoL matches class for class, and ENG's revenue is within 0.1% (6,707 against 6,713). Over 60 months the fix moves revenue −0.5% and the treasury −0.6% against `m02_c`. Pop savings still run about 6% higher in-game: ENG's banking confidence there is about 41.9 against the scenario's 39.3, an input the simulator takes from older saves.
  - **Slaves were missing from the state pie chart** (an older bug that the test slaves exposed). `create_pie_chart_pop_type` marked unset slices with 1, which is also the slaves' index, so every slave slice was copied over from the one before it and showed as a gap. Unset slices are now 0. The rounding remainder also went to the first class present instead of the largest, because the comparison mixed raw shares with rounded slices. Virginia now shows 31 slave slices (grey) against 0 before.
  - **The budget screen's revenue and spending pies broke** (found 2026-11-13). They had borrowed the ten old pop types' sprites for their colours through `GetValueToPopType`. M02 cut that to five classes, so corporate tax, income tax and government spending drew nothing. The pies now have their own lookup, `GetValueToBudgetPieSegment`, with the same colours as before. The two colours no class uses, dark blue and light blue, are the deleted landowners and bureaucrats textures, recovered from git as `pie_chart_segment_dark_blue.dds` and `pie_chart_segment_light_blue.dds`.
- **Slave wages on the stripped map.** Idle slaves push wages in slave states to the floor. That's the intended direction (Q62), but how far it goes depends on plantations, which come back in M14.
- **Wages creep up wherever jobs are filled exactly** (from before M02). Startup fills every job, so utilisation sits at 1.0, above the 0.99 band, and the wage rises 0.5% a month: +33% in London over 60 months, and state 1007's government factories do the same on the old code. M04's target utilisation should take this on.
- **Tuning for M14:** the qualification rates and needs, bureaucrats per head, the senior share, the tax floor, and the upper class's 10× wage.
- **Not changed:** `toi/documentation/production_method_creator.html`, a legacy PM authoring tool that the generator replaced, still names the old workforce variables. The Korean economy file still carries stale PM tooltips from the old PM system.
- **The country SoL statistic overflows** (`update_country_pop_stats` multiplies a summed SoL by the class's workforce). It's from before M02 and is display-only.
