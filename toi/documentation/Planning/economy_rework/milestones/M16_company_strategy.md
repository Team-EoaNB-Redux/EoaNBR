# M16: Company strategy

**Spec:** §19. **Depends on:** M10, M15. **Questions:** Q127, Q128, decided 2026-11-16; [ui_planning.md](../ui_planning.md) UQ12; the open ones below. **Status:** not started.

**Order:** after M15 and before M17 and M14. Strat split the companies work after M10 into three milestones on 2026-11-16 (Q127).

## Goal
Make companies behave differently from each other and from the generic owner. M10's companies all keep the sectors' retained share, invest in their own industry first in each tier, and differ only by the bonuses history and content give them. This milestone gives them strategies, departments, research and mergers, so market share follows from how a company is run.

## Exists now
- **After M10:** a base throughput bonus in a company's primary industry (`global.company_throughput_bonus`), per-company throughput, output and input factors (`global.company_*_factor@`), and the sectors' retained share for every company.
- **After M15:** shares and valuations, which price mergers and acquisitions.
- **[Company_System_Design.md](../Company_System_Design.md)** (Strat, 2026-11-16): modes, departments and R&D, vertical and horizontal integration, mergers and acquisitions from 1857. Older than the spec, which wins where they differ (Q128).
- **Strat's notepad and UQ12:** five behaviour states and complacency.

## Build
1. **Behaviour states** (Q128): rapid growth, monopolisation, expansion, optimisation and crisis management. Each sets how a company spends its retained earnings, its retained share, and whether it closes loss-making plants (M10's companies only shrink through capacity decay, Q134).
2. **Complacency** (0–100%, Q128): high means more dividends and less risk-taking and R&D. State backing raises it, and a state-owned company is also less efficient (§4 of the design document).
3. **Departments:** one industry focus each, so a company can work more than its primary industry, with vertical and horizontal integration bonuses.
4. **Research and development:** spending that buys throughput, output, input and construction bonuses on the company's own slice (the M10 factors), and progress toward a tech bonus.
5. **Mergers and acquisitions**, started by companies (Q128): horizontal, vertical, and hostile takeovers, priced from M15's valuations. The player's force-merger and block-merger controls stay content (Q51).
6. **UI:** switch on the M16 parts of ui_planning.md.

## Open questions (raise with Strat before starting)
- Does R&D's "progress toward a tech bonus" mean HOI4 research bonuses for the country, or bonuses for the company only?
- What moves complacency up and down?
- Does company R&D feed the know-how Strat wants modelled (backlog), or is know-how national only?
- In Strat's tests before the rework, companies bought out whole sectors even without bonuses (Q130). What stops one company owning a whole industry: the founding penalty (Q144), monopoly law (M17), or behaviour?

## Done when
- In the simulator, companies in different behaviour states spend and grow differently in the same sector.
- R&D and departments change a company's margin against the generic owner's in the same sector.
- A merger combines two companies' holdings, debt and treasuries.
