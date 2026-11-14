# M15: Companies completion

**Spec:** §19, §21.3. **Depends on:** M10, M11, M13. **Questions:** Q40, Q66, decided; [ui_planning.md](../ui_planning.md) UQ12 and UQ23, decided 2026-11-14; the open ones below. **Status:** not started.

**Order:** after M13 and before M14. Strat added it on 2026-11-14 (UQ23), after the milestones were numbered, and balance stays last.

## Goal
Finish the companies M10 builds as a minimum. M10's companies earn, invest from retained earnings, get founded and fail. This milestone gives them owners and a share price, a stock market, strategies, departments, research and branches abroad. The economy window already has greyed places for all of it (ui_planning.md §5.3's financial markets, §5.4, and §7's Global → Companies), so finishing a part means switching its place on.

## Exists now
- **After M10:** companies as owner slices beside the generic owner, national accounts, investment through the M09 tiers, founding, liquidation and the player bailout.
- **After M11:** company loans from the bank, and defaults written off against bank capital (spec §19.2).
- **After M13:** the insolvency laws (`insolvency_law_tokens`), the foreign direct investment law, and the ownership actions (acquire or nationalise, privatise).
- **Strat's notepad** (`toi/documentation/Strats_notepad_while_hes_at_uni.txt`, "Failing Companies"): Chapter 11 reorganisation, which M10 left for when shares exist.
- **The companies mockup prompt** (ui_planning.md, appendix) names the parts: the valuation formula (assets + trajectory + margins + modifiers), ownership split between private investors, the state, creditors and treasury stock, departments with integration bonuses, R&D, foreign branches, an AI behaviour state and complacency.

## Build
1. **Shares and ownership.** Each company has shares outstanding, held by private investors, the state, creditors and the company itself (treasury stock). Dividends go to holders by share.
2. **Equity issuance:** a company raises capital by selling shares, beside retained earnings (M10) and bank loans (M11).
3. **Valuation and the stock market:** a share price from the valuation formula; a market index, market capitalisation, volatility, and top gainers and losers.
4. **Speculation and bubble risk** (0–100), read by the financial warnings and Financial System, and able to end in a crash that hits banking confidence.
5. **Reorganisation** (Chapter 11, Q66), gated by the insolvency laws, as the alternative to liquidation: 6–24 months with dividends suspended, throughput bonuses halved, no expansion and a valuation hit, with shares passed to creditors. This was the backlog's item.
6. **Behaviour:** an AI behaviour state (rapid growth, monopolisation, optimisation, crisis management and the like) that decides how a company spends its retained earnings, and complacency (0–100%: high means more dividends and less risk-taking and R&D).
7. **Departments:** one industry focus each, with vertical and horizontal integration bonuses.
8. **Research and development:** spending that buys throughput, output, input and construction bonuses on the company's own slice, and progress toward a tech bonus.
9. **Foreign branches:** capacity owned abroad, with the revenue from each branch, the investment into it and its valuation, within what the foreign direct investment law allows.
10. **The player's company actions** that need shares: purchasing a stake. The rest of spec §21.3 (mergers, monopolies, concessions) stays content for later, as Q51 left it.
11. **UI:** switch on the M15 parts of ui_planning.md (§8, With M15).

## Open questions (raise with Strat before starting)
- Who holds private shares: the middle and upper classes directly, the general pool (M09), or the bank?
- One stock market per country, or one per market (Q45's currency areas)?
- Does R&D's "progress toward a tech bonus" mean HOI4 research bonuses for the country, or bonuses for the company only?
- What moves complacency up and down?
- Does company R&D feed the know-how Strat wants modelled (backlog), or is know-how national only?

## Done when
- Each company's shares add up to 100%, and dividends reach holders by share.
- In the simulator, share prices follow company results, and the index and bubble risk rise in a boom.
- Under a reorganisation law, a failing company reorganises instead of being liquidated.
- R&D and departments change a company's margin against the generic owner's in the same sector.
- Every M15 part of the economy window shows live figures.
