# M02: Pops and labour

**Spec:** §5, §23–30. **Depends on:** M00. **Questions:** Q8–Q14, Q57, Q58, Q61, Q62, all decided. **Status:** not started.

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
