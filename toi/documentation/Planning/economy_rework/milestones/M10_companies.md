# M10: Companies

**Spec:** §2.3, §19. **Depends on:** M04, M09. **Questions:** Q19, Q40, Q41, Q66, all decided. **Status:** not started.

## Goal
A company is a permanent, cached national entity layered over state industries. It owns shares of state industries. Each industry keeps one PM/AM pair (Q19), and the company's bonuses apply to its own slice, which is computed once at the national level and passed back to the states by ownership share. Its accounts are kept nationally: output, inputs, payroll, revenue, operating profit, debt service and retained earnings. Companies compete on productivity, leverage and where they sit, and they can grow or fail. Each country's generic owner is just another ownership entity.

## Exists now
- **MVP** (`_economy_companies.txt`): company records stored globally and keyed by id, holdings per state and building, dividends pulled to the HQ state, and a split between `companies_monthly` and `companies_update`. It was never finished, and the original full plans aren't available.
- **Founding** is a national opportunity in `_economy_investment.txt`, switched off.
- **Gaps** in the memory notes: holdings aren't reconciled when an industry shrinks, a state changing hands isn't handled, and the old upgrade financer convention is still in use.
- **Failure plan:** Strat's notepad (`toi/documentation/Strats_notepad_while_hes_at_uni.txt`, "Failing Companies") describes Chapter 11 reorganisation, Chapter 7 liquidation and player bailouts. The politics rework has insolvency laws (`insolvency_law_tokens`).
- No companies exist in play.

## Build
1. **Companies as owner slices** in the M04 owner-slice code, alongside the generic owner (Q40).
2. **Bonuses:** company bonuses apply where the company owns capacity. Market share follows from compounding profit.
3. **Investment:** companies invest from retained earnings through the M09 tiers.
4. **Founding** (Q41): startup companies first, then dynamic founding from the general pool.
5. **Failure** (Q40, Q66): liquidation and the player bailout. In liquidation, capacity goes back to the generic owner, and loans are written off (against bank capital once M11 exists). Reorganisation (Chapter 11) waits in the backlog until shares exist.
6. Fix the gaps listed above.

## Done when
- A startup company on the test bed earns, keeps earnings, expands, and can fail.
- Generic and company accounts sum to the sector totals.
