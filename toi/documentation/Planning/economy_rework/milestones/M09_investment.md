# M09: Investment

**Spec:** §13, §3.1. **Depends on:** M04–M07. **Questions:** Q34–Q39, Q60, all decided. **Status:** not started.

## Goal
Capital comes from:
- **Sector retained capital**, which expands the sector that earned it. Incentives set how much profit is retained rather than paid out (Q39).
- **One general investment pool,** fed by:
  - a share of each sector's retained earnings, set by the financial laws;
  - pops' own investment, out of after-tax income (Q36);
  - the government;
  - foreign capital and bank credit, which arrive with M11 and M12.

There are no investor-type pools, and no geographic mobility rules: states aren't independent economic units (Q34).

Opportunities are ranked in ROI tiers. Retained capital uses the tiers to choose locations within its sector, and the general pool uses them to choose between sectors. Hard caps, throttles and one project per state-industry keep it cheap. Bad incentives should mean little growth.

## Exists now
- **Old investment system:** `_economy_investment.txt` holds the investment opportunities, the investment fund and national opportunities (company founding). It's all gated off by `global.eco_investment_enabled = 0`, and it reads PM fields that no longer exist.
- **Prototype:** `_economy_investment_buckets.txt` is an earlier, unhooked attempt at capital pools.
- **Pop investment:** `p_pops_investment` (kept by M03) has nowhere to go yet.
- **Construction:** construction and retooling (`industries_update_construction_retooling`, `construct_x_industries`, `retool_industry_no_update`) deliver goods bills over a build time. The financer encoding is in the companies memory note.
- **Superseded design:** [archive/06](../archive/06_investment_rework.md) is the old design.

## Build
1. **Pools:** sector retained capital from the M04 profit split, and the general pool with the inflows listed above. Pop investment from the middle and upper classes (Q60) finally lands here.
2. **Opportunities** per sector per location, in tiers: Exceptional over 20%, Good 10–20%, Fair 5–10%, Marginal −5% to 5%, and anything lower ignored. Only the tier is stored.
   - **Brownfield labour estimate:** unemployment plus a small share of employment.
   - **Hard caps:** known deposits, arable land, crop eligibility and port sites. What an RGO can still open up is `known_deposits@` − `size@` − `construction@`, which `can_build_industry` checks (M06).
3. **Who pays** (Q35):
   - A sector new to the country needs outside capital: the general pool, credit, the government or foreign money.
   - A sector opening in a new state pays from its own retained capital, under the §13.5 throttle.
   - Established sectors can always draw on the outside sources as well.
4. **Greenfield throttles** (§13.5): a coarse country-level pre-filter, a search budget that's smaller for small countries, and one new establishment per sector per month.
5. **Construction** is paid for out of the pool that chose it. Government-funded capacity is a grant to the generic owner by default (Q37).
6. **Upgrades** (Q38): PM and AM upgrades are an opportunity type, funded from retained capital through the same tiers, using the additive labour cuts from M04.
7. **Prospecting** (Q30) is an opportunity type too. M06 kept the state screen's government-paid Prospect button and its search (`update_prospecting`, `rgo_discovery`). The button hides while known deposits wait to be worked, so before M09 a state can find each good only once.
8. **Delete** the old investment files, the buckets prototype and the `eco_investment_enabled` flag (Q4).

## Done when
- On the test bed, ENG's profitable sectors grow at believable rates over 60 months.
- Nothing is built without capital.
- A sector new to the country waits for outside money.
- Lowering incentives visibly slows growth.
- Investment never spends more than its pool holds.
