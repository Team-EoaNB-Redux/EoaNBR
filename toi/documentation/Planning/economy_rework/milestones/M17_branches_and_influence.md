# M17: Branches and influence

**Spec:** §19, §21.3. **Depends on:** M10, M13, M15, M16, and the politics rework's interest groups. **Questions:** Q127, Q128, decided 2026-11-16; the open ones below. **Status:** not started.

**Order:** after M16 and before M14. Strat split the companies work after M10 into three milestones on 2026-11-16 (Q127).

## Goal
Let companies work abroad and in politics. M10's companies hold capacity only in their own country: a holding in a state their country no longer owns passes to the new owner's generic owner (Q135), and they invest only in their country's states (Q132). This milestone gives them branches abroad, under the foreign direct investment law, and political weight at home.

## Exists now
- **After M10:** companies headquartered where they were founded, holdings only at home.
- **After M13:** the foreign direct investment law, five levels in the politics rework's `foreign_direct_investment_tokens`, ending in `law_foreign_concessions` (Q128).
- **[Company_System_Design.md](../Company_System_Design.md)** (Strat, 2026-11-16): FDI branches, a four-level law ladder with exclusive economic zones as a decision, and political interactions. Older than the spec, which wins where they differ (Q128).

## Build
1. **Foreign branches:** capacity owned abroad, with the revenue from each branch, the investment into it and its valuation, within what the foreign direct investment law allows. Holdings abroad then work for their company instead of passing to the generic owner (Q135).
2. **Concessions** (Q128): the law's last level, where foreign companies may dominate local ones. It stands for the design document's chartered zones.
3. **Profit repatriation**, and **nationalising a branch.**
4. **Lobbying and interest groups:** companies fund interest groups and lobby for laws.
5. **State-issued monopolies.**
6. **UI:** switch on the M17 parts of ui_planning.md.

## Open questions (raise with Strat before starting)
- Does a branch's dividend go to its company's HQ state, and is it taxed where it's earned or at home?
- How does a branch count in the host country's sectors: as a company slice there, or outside its accounts?

## Done when
- In the simulator, a company invests in a foreign state its law allows, and the branch's profit reaches its HQ.
- Nationalising a branch passes it to the host's generic owner or a state-owned company.
