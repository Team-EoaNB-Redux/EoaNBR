# M15: Shares and capital markets

**Spec:** §19, §21.3. **Depends on:** M10, M11, M13. **Questions:** Q40, Q66, Q127, Q128, decided; [ui_planning.md](../ui_planning.md) UQ12 and UQ23, decided 2026-11-14; the open ones below. **Status:** not started.

**Order:** after M13 and before M16, M17 and M14. Strat added it on 2026-11-14 (UQ23), after the milestones were numbered, and balance stays last. On 2026-11-16 Strat split the companies work after M10 into three milestones (Q127): this one, [M16](M16_company_strategy.md) (company strategy) and [M17](M17_branches_and_influence.md) (branches and influence). This file kept its name.

## Goal
Give M10's companies owners and a share price. M10's companies earn, invest from retained earnings, get founded and fail. This milestone adds shares and the stock market, so companies can raise equity, be bought into, and reorganise instead of failing. The economy window already has greyed places for it (ui_planning.md §5.3's financial markets, §5.4, and §7's Global → Companies), so finishing a part means switching its place on.

## Exists now
- **After M10:** companies as owner slices beside the generic owner, national accounts, investment through the M09 tiers, founding by incorporation, liquidation and the player bailout. A public company works like a private one. All of a company's dividends go to its HQ state's upper class, or to the treasury for a state-owned company.
- **After M11:** company loans from the bank, and defaults written off against bank capital (spec §19.2).
- **After M13:** the insolvency laws (`insolvency_law_tokens`) and the ownership actions (acquire or nationalise, privatise).
- **Strat's notepad** (`toi/documentation/Strats_notepad_while_hes_at_uni.txt`, "Failing Companies"): Chapter 11 reorganisation, which M10 left for when shares exist.
- **[Company_System_Design.md](../Company_System_Design.md)** (Strat, 2026-11-16): the ownership buckets, valuation, company types, Chapter 11, buybacks and treasury stock. Older than the spec, which wins where they differ (Q128).

## Build
1. **Shares and ownership.** Each company has shares outstanding, in four buckets: private investors, the state, creditors and the company itself (treasury stock). Private shares are held by the general pool and the HQ state's upper class (Q128). Dividends go to holders by share, so a founded company's dividends start reaching the general pool, which subscribed its capital (Q136).
2. **Equity issuance:** a company raises capital by selling shares, beside retained earnings (M10) and bank loans (M11). Private companies raise from retained earnings and loans only, public ones also by issuing shares (Q128).
3. **Valuation and the stock market:** a share price from the valuation formula (assets + trajectory + margins + modifiers); a market index, market capitalisation, volatility, and top gainers and losers.
4. **Speculation and bubble risk** (0–100), read by the financial warnings and Financial System, and able to end in a crash that hits banking confidence.
5. **Buybacks and treasury stock.**
6. **Reorganisation** (Chapter 11, Q66), gated by the insolvency laws, as the alternative to liquidation: dividends suspended, throughput bonuses halved, no expansion, a valuation hit, some assets sold and shares passed to creditors, who sell them back over time. The design document's figures are starting ranges to tune (Q128): a 35–60% valuation hit, 15–40% of non-core assets sold, and 20–50% of the equity to creditors, sold back over 12–36 months. Its anti-cheat rules and reputation penalties for repeat bankruptcies replace M10's 5-year bailout limit.
7. **The player's company actions** that need shares: buying a stake. A bailout can then take a state stake instead of being a grant (Q141).
8. **UI:** switch on the M15 parts of ui_planning.md (§8, With M15).

## Open questions (raise with Strat before starting)
- One stock market per country, or one per market (Q45's currency areas)?
- How a company's own valuation relates to M10's asset value (`industry_asset_value_calc`, a margin-scaled build cost), which sets its debt pause and insolvency.

## Done when
- Each company's shares add up to 100%, and dividends reach holders by share.
- In the simulator, share prices follow company results, and the index and bubble risk rise in a boom.
- Under a reorganisation law, a failing company reorganises instead of being liquidated.
- Every M15 part of the economy window shows live figures.
