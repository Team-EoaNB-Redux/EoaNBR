# M11: Banking, credit and base money

**Spec:** §14, §15, §16 (base money). **Depends on:** M09, M10. **Questions:** Q22, Q42–Q44, Q59, Q65, Q69, Q72, all decided. **Status:** not started.

## Goal
Finance accelerates the real economy, and it's where deliberate instability comes from. Credit lets investment run ahead of retained capital. Defaults destroy bank capital, which shrinks credit. A crisis should mainly hit investment, construction, employment and indebted sectors, not routinely wipe out current output.

Base money moves here from M12 (Q65), because bank reserves are built from it.

## Exists now
- **Old bank:** `_economy_banking.txt` has a country-level bank, but `bank_update` is commented out.
- **Pop debt:** M03 builds the pop debt stock, with no creditor yet (Q59).
- **Related levers:** `banking_confidence_modifier` (0–100). The politics rework's `financial_system_tokens` (no banking system, commercial banking, capital markets, independent central bank, central-bank interference, bank nationalisation) and `financial_regulations_tokens` will set the coefficients.
- **Government debt:** `national_debt_update` handles domestic and foreign debt. Interest is about 8%, cheaper for great powers. `0_eoanb_debt_effects.txt` and the bankruptcy event handle default.

## Build
1. **Base money** (Q65), one stock per market:
   - It's seeded at game start, and only the market leader mints more.
   - Seigniorage goes to the treasury: the minted quantity ÷ P, which is 1 until M12 (Q49).
   - Each country's share of the market's base money (its GDP share) is worked out every month. Its bank draws reserves from that share × its own banking confidence (Q44, Q69).
   - **Leaving a market:** the leaver keeps that share. Money and money demand move in proportion, so neither side's price level or inflation rate jumps.
   - **Joining a market** (Q69): the joiner's base money converts into the market's currency at the ratio of price levels (M × P_market ÷ P_joiner), so it keeps its real value. Valuables reserves move the same way in both directions. Bank money needs nothing, since each country keeps its own bank.
2. **One bank per country** (Q42), holding reserves, outstanding loans, bank capital, banking confidence and the interest rate. Specialist banks are lending priorities on it.
3. **Reserves** (Q44): the target = the country's share of base money × banking confidence ÷ 100. Reserves move slowly toward it, but bank runs can drain them fast.
4. **Credit capacity** = min(reserves ÷ reserve requirement, capital ÷ capital requirement).
5. **Borrowers** (Q43):
   - Sectors and companies, with interest in their accounts. This lifts the M04 rule that sectors can't borrow (Q22).
   - Pops: the bank becomes the creditor for M03's pop debt and charges interest. The bank holds the country total, not per-pop records.
   - Domestic government bonds stay separate for now. Ideally they'll draw on the same credit market eventually.
   - **Foreign government debt** (Q72) is already stored per creditor (`debt_to_bank_k@<tag>`). It becomes a loan on the creditor country's bank. Interest is charged at that bank's lending rate plus a premium for the borrower's credit rating, replacing the single `foreign_interest_rate`, and it's income for the creditor's bank. A default hits the creditor bank's capital. Until this milestone, the interest disappears, as now.
6. **Defaults:** performing loans go down and bank capital takes the loss. Capital below requirement cuts lending, and insolvency triggers a banking crisis.
7. **Central-bank basics:** a policy rate and a lender of last resort. Their player controls come in M13.
8. **Delete** the old bank code.

## Done when
In the simulator:
- a profitable run-up raises lending and investment;
- forcing defaults cuts credit and investment;
- a foreign government's default cuts the creditor country's bank capital and lending;
- output falls less than investment does;
- a confidence shock drains reserves quickly, and they recover slowly;
- a country leaving or joining a market moves base money without a jump in either side's money per unit of GDP.
