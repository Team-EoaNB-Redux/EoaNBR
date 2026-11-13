# M03: Wealth and demand

**Spec:** §24, §25, §31, §32. **Depends on:** M02. **Questions:** Q15–Q17, Q36, Q52, Q59, Q60, and the follow-ups Q81–Q84, all decided. **Status:** done in the simulator 2026-11-12; the in-game check is still to do (see Left over). Baseline: `redux-eco-sim/runs/m03_base` (`world_1857_eng`, 60 months, `--watch-file watches/m03.txt`). Result: `runs/m03_a`.

## Goal
Pop demand comes from population, wealth, class basket, market participation and target spending. SoL is renamed to wealth, which keeps the current scale and the current baskets per level, just optimised. Pops hold no savings: they spend toward a target set by consumer confidence. Income they don't spend disappears, and spending above income becomes debt owed to the banking sector.

## Exists now
- **SoL:** each pop type has a standard of living from 1 to 200 (`pops_sol`). The basket per level is `global.pops_spending_need_at_sol@<good>^<level>` (`pops_global_var_setup`, `get_pop_needs`). Its value doubles every 10 SoL and is defined in base-price value. Technology gates swap in substitutes.
- **Spending and savings:** `pops_calculate_spending_targets` sets the target spending = earnings × consumer confidence. `pops_calculate_savings_targets` sets a savings target of earnings × banking confidence × 12, and pops spend savings down when the target drops.
- **Consumer confidence** (`pops_update_confidence`, 0.2–2): built from the country's `consumer_confidence_modifier`, less penalties for debt service, debt panic and high interest, plus a small bonus for savings.
- **Pop debt stubs:** `p_bank_lent_to_pops_k`, creditworthiness, debt interest and repayment spending. The bank is off.
- **Peasants:** `global.peasant_market_interaction` is 0.2. About 20% of subsistence output reaches the market, and about 20% of peasant needs show up as market demand.
- **Pop investment:** capitalists and landowners divert part of their income into `p_pops_investment`. It's subtracted from their earnings but never reaches anything while investment is off.

## Build
1. **Rename SoL to wealth** (Q17), keeping the variable's scale and the per-level baskets. A separate SoL, derived from wealth plus modifiers such as pollution, comes later. Refactor `get_pop_needs` for speed while it's open.
2. **Spending** (Q15, Q16): keep target spending = earnings × consumer confidence. Remove the savings stock, the savings target and the confidence bonus for savings. Unspent income disappears.
3. **Pop debt** (Q59): spending above income becomes debt, stored per state and class for the working, middle and upper classes. Peasants and slaves don't borrow. Build the stock and its repayment here, without interest, and let the existing confidence penalties limit it. The bank becomes the creditor in M11.
4. **Upper-class demand** from ownership income: dividends and subsistence rent.
5. **Pop investment** (Q36, Q60): keep `p_pops_investment`.
   - Only the middle and upper classes invest.
   - The share is taken from after-tax income before target spending is worked out, and incentives scale it (Q39).
   - It reaches the general pool in M09; until then it disappears, as now.
6. Peasant market participation stays one scalar.

There's no money-closure probe: money is created and destroyed all the time (Q52).

## Done when
- No savings variables remain.
- Spending tracks the target, and pop debt stays bounded over 60 months.
- `world_1857_eng` runs 60 months with no runaway in wealth, up or down.
- The pop screens read "wealth", and their values match the M02 baseline at month 1.

## What was built (2026-11-12)
1. **Wealth** (Q17). SoL is renamed wealth everywhere, on the same scale (1–200) and with the same baskets.
   - Variables: `pops_wealth@<class>` and `pops_wealth_progress@<class>` on states, `pops_wealth` as the state's and country's averages, and the basket tables `global.pops_need_at_wealth@<good>^<level>`, `global.pops_spending_at_wealth`, `global.pops_spending_weight_at_wealth` and `global.pops_spending_weight_wealth@<good>`. `calculate_standard_of_living` is now `calculate_starting_wealth`. The unused `readjust_standard_of_living` is deleted.
   - Readers outside the economy now read wealth: the pandemic chances (their `pandemic_min_sol` / `max_sol` thresholds keep their names until SoL is split from wealth), the state map mode, the ledger column and its sort, and the simulator's panels.
   - **The country average is fixed.** `update_country_pop_stats` never reset its per-class sums and multiplied them by the class's workforce, so it overflowed about 3,000 times in 60 months. Each class's country wealth is now its states' wealth weighted by workforce, and the country average is weighted the same way. A state's average leaves soldiers out and counts slaves.
2. **`get_pop_needs` refactored.** It now adds each class's demand straight into the state's `pops_need@<good>`, skips goods not yet in the basket at the class's wealth, and checks for replacements only on the seven goods that have one. Each class now loops over the goods once instead of four times. It's 51% cheaper (see Cost).
   - **Food modifier fixed.** `pops_food_consumption_factor` (−0.01 to −0.03 from the agriculture techs) used to *add* its share to the food pops bought and take its cost off their spending. It now scales both the same way. ENG's is −0.06, so its pops now buy 6% less food instead of 6% more, which accounts for part of the lower food price below (4.20 against 4.43 at month 60).
3. **Spending** (Q15, Q16). Target spending = (earnings − investment) × consumer confidence, and spending = goods + income tax + sales tax + corporate tax + debt repayments.
   - The savings stock, the savings target and the confidence bonus for savings are gone (`pops_handle_savings`, `pops_calculate_savings_targets`, `pops_savings*`, and the savings set-up in `_state_fin`). Unspent income disappears.
   - **Earnings are gross** (Q83): `pops_earnings` no longer has investment taken off, so income tax is charged on all of it.
   - **The upper class pays the corporate tax** on its dividends, which the budget already collected without charging anyone. The investment fund no longer books it too. ENG's corporate tax is 0, so this changes nothing on the test bed.
   - **Wealth step** (`pops_wealth_monthly`, which replaces `pops_update_standard_of_living`): progress += `global.pops_wealth_speed` (6) × (target − spending) ÷ goods spending, and each whole point moves wealth one level. The old step added the cash gap on top of the target gap, which counted the same gap twice at confidence 1, so 6 keeps its speed.
4. **Pop debt** (Q59, Q82). `pops_debt_monthly` replaces the savings, surplus, deficit and repayment stubs.
   - For the classes in `global.pops_borrows@` (working, middle and upper), last month's spending above their income after investment becomes `pops_debt@<class>` on the state. State and country totals are `pops_debt`.
   - They repay `global.pops_debt_repayment_rate` (0.00333, 4% a year) of it each month, as part of spending, and `global.pops_debt_surplus_repayment` (half) of any surplus repays more. No interest until M11.
   - The confidence penalties limit it: confidence falls by the share of income that goes on repayments, and the debt-panic penalty starts once that share passes `debt_service_limit_temp` (0.1 + 0.05 × banking confidence + 0.025 × consumer confidence). That limit never worked before: it added an unset `limit_temp` instead of the banking term. The tiers in `pops_handle_deficit` that refused to lend past the limit are gone, so every overspend is owed.
   - Peasants can't borrow, so their confidence is capped at 1 (Q82).
   - A class that empties has its debt written off.
   - `calculate_creditworthiness` keeps its debt terms for M11 but loses the savings term, and pops no longer call it: nothing read `pops_creditworthiness`. The bank's pop deposit and withdrawal effects, and its interest to savers, are deleted.
5. **Upper-class income** is its dividends, which already include subsistence rent (`industries_update`), plus pay for senior government jobs.
6. **Pop investment** (Q36, Q39, Q60). `pops_calculate_investment`: the middle and upper classes invest `<class>_investment_contribution_factor` (at most 80%) × investment appetite × (earnings − income tax − corporate tax). Appetite comes from incentives (`calculate_investment_appetite`), now worked out once per state. The new `middle_class_investment_contribution_factor` has a base of 0.1 at peace and at war (static modifiers), with its token and localisation. The money still disappears until M09.
7. **Subsistence owner jobs** (Q84, Strat's bug report). `owner_jobs@subsistence_farm` = 2% of all the state's peasants, including those on marginal land, not 2% of the land's capacity. At startup, `state_eco_employment_init` fills the upper class from its other jobs first, then takes landowners out of the peasants who are left: owners × peasants ÷ (peasants + owners), so the remaining peasants need exactly that many.
8. **An empty class cleared its neighbour's data.** `pops_update` set `current_pop_token` only for classes with a workforce, so `pops_clear_inactive_pop_data` zeroed the *previous* class's target, taxes and repayments. In a state with no upper class, the middle class's target read 0 every month. It's set first now, and the clear also zeroes the empty class's earnings, spending and debt.
9. **UI.** The state screen's wealth figure and tooltip, a pops-finance tooltip with investment, corporate tax, debt repayments, target spending and debt, and a debt line with its own tooltip in place of savings (English, Korean and Russian, with the Russian marked #NT!). The map mode and ledger say Wealth. The mock-up national bank tooltip lost its savings line.
10. **Simulator** (Q5): `watches/m03.txt`, the state panel's Wealth and Debt columns, the wealth map mode, and the `CLAUDE.md` example. The parity probes in `_economy_sim_probes.txt` log wealth and debt.

## Results (simulator, `world_1857_eng`, 60 months)
Against `m03_base` (`runs/m03_a`; `runs/m03_b` is a rerun alongside the old code, identical on every watch). The investment fund change came after both, and a 6-month run with it (`runs/m03_final6`) matches `m03_a` on every watch. No new diagnostics. The economy files' 3,027 overflow warnings are gone.

| ENG at month 60 | Baseline | M03 | Why |
|---|---:|---:|---|
| GDP | 9,691 | 9,579 (−1.2%) | Less food bought (the food modifier fix), the middle class investing, and debt repayments counting as spending |
| Revenue | 5,560 | 5,642 (+1.5%) | Income tax +9.5% on gross earnings, sales tax −3.2% |
| Pop earnings | 11,511 | 12,862 (+11.7%) | Gross: investment is no longer taken off |
| Pop investment | 1,462 | 1,424 | Now out of after-tax income, and the middle class invests too |
| Upper class | 121.8K | 202.2K | Landowners are 2% of all peasants (Q84) |
| Pop debt | — | 34,836 (2.7 months of pop income) | |
| Wages, test-industry employment | | within 0.04% | |

**Wealth matches M02 at month 1** for London's working class (36 → 33) and peasants (10 → 7). The upper class starts lower (London 54 against 60), because Q84 gives London 27.7K landowners instead of 17.1K to share the same dividends.

**No runaway in wealth.** ENG's class averages are flat from month 12: working class 28.5 → 29.9, middle 33.4 → 35.0, upper 29.7 → 28.4. The upper class is mostly rural landowners living on subsistence rent, which falls with the price of food (8.0 → 4.2).

**Spending tracks the target,** within the one-level steps wealth moves in: London's working class spends 747 against a target of 730 at month 60.

**Debt is bounded.** Startup overspends for three months (Q81): by month 3 ENG's pops owe 16,243, London's working class 930 (1.5 months' income) and its upper class 1,609. After that, debt grows by about 290 a month and slowly slows: 3,886 in the second year, 3,308 in the fifth. ENG's confidence of 108.7 means every class that borrows aims to spend 8.7% more than it earns. The debt stops growing when repayments take half that excess, about 4% of income, which is about 13 months' income of debt. At 4% repayment a year that takes decades, so by month 60 London's working class owes 4.5 months' income and its confidence has fallen from 1.087 to 1.072.

**The bug is fixed.** South Dakota's upper class is 0.09K of 4.49K (it was 4.46K), and the USA's is 208K (it was 325K). Only two states start above 10% upper class (121 before): Washington DC, from its senior government jobs (11%), and North Sentinel Island. None is above 50% (42 before).

**Cost.** The machine's speed drifted between runs, so the old code was rerun alongside the new (`runs/m03_base_rerun`, identical to `m03_base` on every watch, against `runs/m03_b`). Effects M03 didn't touch agree within about 1%. Seconds over 60 months, from `profile.csv`:

| | Old code | M03 | |
|---|---:|---:|---:|
| `get_pop_needs` | 3.01 | 1.48 | −51% |
| `pops_calculate_needs_spending` (with `get_pop_needs`) | 4.01 | 1.63 | −59% |
| `pops_update` | 7.44 | 4.20 | −44% |
| `on_monthly_pops` | 2.29 | 1.62 | −29% |
| `employment_update` | 3.51 | 3.39 | |
| `update_country_pop_stats` | 1.51 | 1.58 | |
| **Pop pipeline** (with `pops_balance` and `bureaucracy_and_manpower_update`) | **15.02** | **11.08** | **−26%** |
| `_country_advance_time` | 50.5 | 46.4 | −8% |

Together with M02's 5%, the pop pipeline now costs about 30% less than before M02, short of the half M02 first aimed for (Q80). What's left is mostly `employment_update`, the per-class bookkeeping in `pops_update`, and the country statistics.

## Left over
- **In-game test (Strat).** Start a new game: saves from before M03 hold savings, and their all-upper-class states won't fix themselves, because `pops_balance` only moves a surplus into another class's shortfall. Check `error.log` for "Errors occurred while reading math expression", that the state screen shows wealth, the finance and debt tooltips, and the ledger's Wealth column, and that South Dakota's population is mostly peasants.
- **Startup debt** (Q81): accepted until M14, which should set starting wealth at actual prices from steady-state earnings.
- **Tuning for M14 or M11:** the repayment rate (4% a year sets the long-run debt at about 13 months' income at ENG's confidence), the share of a surplus that repays debt, `pops_wealth_speed`, and the middle class's 10% investment share.
- **Finance tests:** `effect finance_tests` passes 9 of 12. The three that fail test `calculate_investment_appetite` against the best opportunity's attractiveness, which the function stopped using before M03 (the old code fails the same three). M09 replaces the function.
- **Not changed:** the disabled bank's own lending code still writes `bank_lent_to_pops_k`. M11 replaces it and makes the bank the creditor for `pops_debt`. `state_electrification` is read by `get_pop_needs` but nothing sets it, so electrified goods are always bought as their replacements.
