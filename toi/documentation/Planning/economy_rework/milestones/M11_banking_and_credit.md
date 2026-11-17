# M11: Banking, credit and base money

**Spec:** §14, §15, §16 (base money). **Depends on:** M09, M10. **Questions:** Q22, Q42–Q44, Q59, Q65, Q69, Q72, all decided. **Status:** done; verified in the simulator and in-game on 2026-11-17 (startup, June and July 1857 saves; all 13 finance assertions pass).

## Goal
Finance accelerates the real economy, and it's where deliberate instability comes from. Credit lets investment run ahead of retained capital. Defaults destroy bank capital, which shrinks credit. A crisis should mainly hit investment, construction, employment and indebted sectors, not routinely wipe out current output.

Base money moves here from M12 (Q65), because bank reserves are built from it.

## Before M11
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

## Implemented

`_economy_banking.txt` now contains the new bank and base-money system; the old disabled bank code and its obsolete creditworthiness tests are deleted. The existing content API, budget, market changes, sector/company accounts, monthly construction and pops pipelines call it. Companies and the general investment pool both have bank debt.

- The market leader holds nominal `base_money`, `price_level` (1 until M12) and physical `currency_reserves` (initially 0). Each country receives its GDP share monthly. Leader-only minting grants seigniorage at quantity / P. A member leaving carries its share at the old price level; joining converts nominal money at the ratio of price levels. A whole-market merger moves the entire stock. Each country keeps its bank.
- Country `bank_update` re-sums loans from authoritative borrower records. `bank_credit_update` computes both constraints and subtracts outstanding loans and approved household spending. It is safe to recompute without accruing money or interest. Rates fix before the countries settle; banks close after every country, so foreign interest does not depend on country order.
- Reserves move toward the country's real base-money share times confidence, with faster withdrawals than recovery. Bank money equals performing loans. Loan losses destroy capital, and capital at or below zero triggers a banking crisis and blocks fresh credit. A reserve shortage alone blocks credit without declaring a solvent bank insolvent.
- Construction and retooling pay before progress, including their final month. They buy no goods while a bill is refused. Shared upgrades quote all owners before anyone pays. Generic collateral excludes companies' plants and construction. Sector and company interest is part of their accounts; operating cash shortfalls borrow within collateral and credit limits. Owners cover an unfunded generic loss; unpaid company operating bills trigger its existing bailout/liquidation process.
- The general pool has `investment_fund_debt` and `investment_fund_interest`. After company funding, retained capital and cash, it may use credit for the two best ROI tiers when the return exceeds interest. It repays unused advances immediately and services debt before new investment. A contribution collapse writes down debt beyond its limit.
- Working, middle and upper classes reserve borrowing in `pops_credit@`, then draw it during next month's settlement. Recomputing replaces the reservation. Credit refusal cuts purchased quantities and sales tax together. Wealth reacts to the desired basket, so rationing cannot raise wealth. The state's owner's bank receives interest and takes household write-offs, as Q43/Q59 require.
- Company liquidation writes off its bank principal. Bailouts repay principal and cover unpaid operating bills. A generic sector whose debt exceeds its collateral restructures to the borrowing limit without deleting plants. A household income collapse writes off unserviceable debt; empty classes default once.
- Domestic government bonds keep their separate GDP-based limit. Foreign government loans consume the creditor bank's credit, use its lending rate plus the borrower's debt/GDP premium, and transfer interest once per month. The bankruptcy event now calls `default_debt` so creditors take principal losses. Legacy government *_k records are explicitly converted to the normal money unit at the bank boundary.
- Content has `mint_base_money`, `set_policy_rate`, `lend_emergency_liquidity`, `recapitalize_bank`, `default_debt`, `join_market` and `leave_market`; see `economy_docs.md`. Assistance is repayable liquidity for solvent banks, creates base money without a treasury grant, and retires the money on repayment. Recapitalisation requires positive treasury cash. M13 adds player controls and financial-law coefficients; M12 adds inflation, currency erosion, trade settlement and backing rules.

### Provisional coefficients

These are implementation defaults, exposed in `banking_global_setup`, for balancing in M14. PM and sheet values were not changed.

| Coefficient | Default |
|---|---:|
| Initial market base money | 12 months of real GDP |
| Initial bank capital | 2 months of country GDP |
| Reserve requirement | Existing `reserve_ratio_modifier`, normally 0.2 |
| Capital requirement | 0.08 plus `bank_capital_requirement_modifier` |
| Monthly reserve recovery / withdrawal | 10% / 50% of the gap |
| Annual policy rate / spread / maximum scarcity premium | 4% / 4 points / 2 points |
| Bank interest retained | 50%; dividends only above required capital |
| Crisis confidence penalty | 40 points |
| Household principal limit | 24 months of after-tax income |
| Pool principal limit / principal service | 6 months of contributions / 25% of monthly contributions |
| Generic sector insolvency / restructured debt | 100% / 50% of generic collateral |
| Emergency loan ceiling / monthly repayment | 25% of performing loans / up to 10% of the assistance from excess liquidity |

## Simulator verification

All balance runs use `world_1857_eng.txt`, seed 12345, Easy difficulty, 60 months. `runs/m11_base` records the code before M11; `runs/m11_final` is the M11 reference. Watch file: `watches/m11.txt`. National starting debt, national interest/bankruptcy and the old cycle remain disabled for the normal run, as M00 requires. The targeted foreign-interest check enables national interest explicitly.

| Check | Result |
|---|---|
| Profitable run-up | Cumulative British investment in months 1-24 rises 26.70% over M10. Lending grows and the bank earns interest. |
| Normal five-year economy | British GDP rises from 6,007.4 to 6,918.5 (+15.17%); the M10 endpoint is 7,067.2, so M11 is 2.10% lower. US endpoint is 32,846.9 versus M10's 32,706.2. No bank is insolvent in the final normal world. |
| Foreign-government default | At month 24, a loan equal to 95% of British bank capital is created and written off through the government API. Available credit reaches zero. In months 25-36, cumulative investment falls 11.37% against the M11 normal run while GDP falls 0.61%. |
| Confidence shock and recovery | Confidence is forced to zero after month 24 and restored after month 30. Reserves halve each shocked month, then recover by 10% of the target gap. The unit check confirms both exact speeds. No British insolvency. |
| Systemic private-debt write-off | At month 24, sector, company and pool principal is written off worldwide. The US bank becomes insolvent and cannot lend. Existing capacity survives. Debt relief can increase borrowers' cash investment, so this is a failure-containment check, not a claim that every country's investment must fall. |
| Stock audit | All bank loan totals reconcile to borrower categories; world household debt and credit commitments reconcile to state records. No negative loan/reserve stocks, physical capacity or household debt. Insolvent banks have zero available credit. |
| Diagnostics | No economy errors and no diagnostics in the bank file. The existing non-economy startup errors and old economy warnings remain. |
| Cost | About 8.7% more script operations per month than M10. Most of the added cost quotes and then commits financed pop needs; wall time varies by machine. |

`python tools/test_m11.py` passes eleven integration groups: credit constraints/defaults, household reservations and demand, foreign interest/default, two-price-level currency transfers, confidence, whole-market transfer with colonies, sector restructuring, emergency liquidity/recapitalisation, companies/bailouts, construction, and private/shared retooling. `effect finance_tests = yes` runs the reversible bank and investment-appetite checks in-game. The old appetite tests still used pre-M09 opportunity attractiveness; they now test the current incentives-only formula.

`python tools/analyze_m11_runs.py` audits the recorded worlds and writes `runs/m11_validation.md`. The CLI now supports repeatable `--inject month:path` files for controlled shocks and JSON dumps alongside recorded runs. M11 does not change interpreter semantics. The simulator is a separate, gitignored repository; commit its CLI, scenario, watch and test changes there separately.

Reproduce from `redux-eco-sim/`:

```text
bin/ecosim_cli.exe run --scenario scenarios/world_1857_eng.txt --months 60 --watch-file watches/m11.txt --out runs/m11_final --dump-json runs/m11_final/final.json
bin/ecosim_cli.exe run --scenario scenarios/world_1857_eng.txt --months 60 --watch-file watches/m11.txt --inject 24:scenarios/m11_foreign_default.txt --out runs/m11_final_foreign --dump-json runs/m11_final_foreign/final.json
bin/ecosim_cli.exe run --scenario scenarios/world_1857_eng.txt --months 60 --watch-file watches/m11.txt --inject 24:scenarios/m11_confidence_shock.txt --inject 30:scenarios/m11_confidence_recovery.txt --out runs/m11_final_confidence --dump-json runs/m11_final_confidence/final.json
bin/ecosim_cli.exe run --scenario scenarios/world_1857_eng.txt --months 60 --watch-file watches/m11.txt --inject 24:scenarios/m11_systemic_default.txt --out runs/m11_final_systemic --dump-json runs/m11_final_systemic/final.json
python tools/test_m11.py
python tools/analyze_m11_runs.py
bin/ecosim_cli.exe compare runs/m11_base runs/m11_final
```

### Completed in-game smoke test

The user started a new game, saved at startup, advanced through June and July 1 of the same game on 2026-11-17, and ran `effect finance_tests = yes`: 13 passed, 0 failed. July's first interest settlement is verified below. Existing internal-politics load errors and the six unrelated full-mod parser failures remain outside M11. The multiplayer token-registration correction takes effect on the next game launch.

### First in-game check (2026-11-17)

The startup and June 1 saves loaded and advanced one monthly tick. The game log identifies the existing internal-politics math load errors; none names the economy files. It also exposed an unsynchronised `bank_capital_requirement_modifier` token, now appended outside the generated token blocks without reordering existing tokens. The user ran `effect finance_tests = yes` and reported all 13 checks passed. June British GDP is 6,498.50 versus the simulator's 6,536.75 (-0.585%); bank loans are 5,147.64 versus 5,139.68 (+0.155%). The saved loan total exactly equals household, sector, company, foreign-government and pool principal. Bank capital is positive and there is no British banking crisis. The reserve difference follows different banking-confidence inputs (42.9908 in-game versus 39.33 in the simulator); the saved monthly reserve update matches its formula within one raw unit. The July 1 save subsequently confirmed the first interest settlement on the loans created in June, below.

### July interest settlement checked (2026-11-17)

The July 1 autosave (month 2 of the same test game) confirms British interest receipts exactly: household payments 9.43865 + sector payments 1.46666 + pool payments 23.69115 + company payments 0 = bank income 34.59646. The bank pays dividends 17.29823 and retains 17.29823, exactly matching its capital increase. New lending less principal repayments exactly matches the increase in bank loans. All 332 active country bank totals reconcile to their borrower categories. Established banks' capital movements reconcile to income less dividends and defaults; the newly created civil-war tag D02 also receives its initial bank-capital stock. British bank income differs from the simulator by +0.119%, loans by +1.196%, and GDP by -1.322%.

The read-only `M11OWNER` probe resolves the apparent world household-debt discrepancy: every active country's bank matches its authoritative state-owner debt exactly, and their world total (82,561.27492) equals the sum of state records. The binary save retains stale bank variables for inactive countries; summing every saved country scope was an audit error. No ownership-iterator or banking code change is required. Detailed evidence is in `redux-eco-sim/runs/m11_july_ingame_audit.json`. The in-game smoke test is complete.
