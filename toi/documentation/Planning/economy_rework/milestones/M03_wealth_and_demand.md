# M03: Wealth and demand

**Spec:** §24, §25, §31, §32. **Depends on:** M02. **Questions:** Q15–Q17, Q36, Q52, Q59, Q60, all decided. **Status:** not started.

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
