# Redux Economy Redesign Specification

## Purpose

This document summarizes the chosen design direction for the **End of a New Beginning Redux** economy overhaul.

The primary goals are:

1. **Improve performance**, especially by reducing expensive state-scope economic work.
2. **Simplify the economy substantially** without removing the state-level economic geography that makes the system interesting.
3. Preserve:
   - State-based industry locations.
   - Production Methods (PMs).
   - Automation Methods (AMs).
   - Employment/unemployment behavior.
   - Investment.
   - Ownership and dividends.
   - Pops interacting through employment, wages, dividends, and consumption.
   - Infrastructure as a major economic mechanic.
   - State economic specialization.
   - RGOs/resource deposits.
   - State-specific comparative advantages.

This is **not** intended to recreate Victoria 3's economy in full. The objective is to preserve the important causal relationships while aggressively reducing unnecessary calculations and state-side economic bookkeeping.

---

# 1. Core Architectural Principle

The economy should follow the rule:

> **States host industry; countries perform as much repeated economic arithmetic as possible.**

States remain economically meaningful because they determine:

- Where industries physically exist.
- Local wages.
- Employment.
- Infrastructure Efficiency.
- Resource and land constraints.
- Local economic modifiers.
- Which Production Methods and Automation Methods are in use.
- Where local investment capital exists.

However, calculations that are common across many state industries should be moved upward or precomputed whenever possible.

The key optimization target is not necessarily reducing the number of goods or industries. The important reduction is eliminating repeated expensive scripted work such as:

- State scope traversal.
- Modifier lookup.
- Recomputing PM recipes.
- Recomputing state modifiers every tick.
- Reconstructing the same country-side economic values from scratch.

---

# 2. State Industry Structure

A state-industry should persist only the values that actually need memory between ticks.

## Required persistent values

Each state-industry should approximately store:

- **Size**
- **Employment**
- **Production Method (PM)**
- **Automation Method (AM)**
- **Financial state/history**, but only where needed by future decisions

Examples of financial state that may need persistence:

- Profitability or trailing profitability if used for decisions.
- Construction state/progress.
- Any other value that genuinely depends on previous months.

## Values that should preferably be derived rather than permanently stored

Where practical, do not permanently store:

- Gross output.
- Input consumption.
- Payroll.
- Revenue.
- Infrastructure usage.
- Other values that can be cheaply recomputed from persistent state for UI or aggregation.

The goal is to avoid having every state-industry behave as a miniature independent economy with a large variable footprint.

---

# 3. Production Methods and Automation Methods

Production Methods and Automation Methods remain state-specific.

They **cannot** be made purely country-wide because empires may contain territories at very different stages of development.

Examples:

- Core British industry may use advanced PMs.
- Colonial Indian industry may use older PMs.
- Recently industrializing territories may use an intermediate regime.

Therefore aggregation must preserve PM/AM differences.

A useful national aggregation key is approximately:

> **Country × Industry Archetype × PM/AM Combination**

rather than only:

> Country × Industry

This preserves colonial and regional technological differences while still allowing common calculations to be shared.

---

# 4. Effective State Contributions

Slow-moving state modifiers should be resolved **before** repeated national calculations wherever possible.

Example:

```text
Illinois Farm
Size: 15
Land productivity modifier: +20%
Input modifier: -10%
```

Instead of repeatedly evaluating those modifiers during economic calculations, Illinois can contribute effective coefficients such as:

```text
Effective output contribution: 18.0
Effective input contribution: 13.5
```

The exact implementation may differ, but the important principle is:

> **Bake slow/static local modifiers into effective production coefficients before aggregation.**

Possible effective values include:

- Effective output.
- Effective inputs.
- Effective labor requirement.
- Effective construction requirement.
- Any other coefficient strongly tied to PM/AM and slow local conditions.

Recompute these when relevant state or industry conditions change, rather than rediscovering them every economic tick.

---

# 5. National / Country-Level Economic Aggregation

The country level should perform calculations that are common across state industries.

Useful national-level calculations include:

- Commodity prices.
- Shared PM input valuation.
- Shared PM output valuation.
- Industry/sector totals.
- National supply and demand.
- Trade.
- Investment opportunity aggregation.

The system should avoid making the weekly trade tick rebuild expensive values by iterating through all state economic logic.

Country borders can change frequently, but this is primarily a **dirty-update problem**.

When:

- A state changes owner.
- A state is annexed.
- A country splits.
- A state industry changes PM/AM.
- A relevant modifier changes.

then update/rebuild the relevant aggregate contribution.

Do not use possible border changes as a reason to recompute the entire national economy every tick.

---

# 6. Employment

Employment remains state-specific.

This is necessary because:

- Wages differ by state.
- An industry may be profitable in one state but not another.
- Labor-market conditions differ locally.
- Recessions and expansions should affect unemployment.

State-specific employment/utilization is therefore one of the principal calculations that cannot simply be nationalized.

The general goal is to make employment the **main remaining state-side dynamic economic calculation**.

Once employment is known:

```text
Base Activity = Size × Employment Rate
```

Then actual inputs and outputs can be derived from:

- PM.
- AM.
- Effective state modifiers.
- Infrastructure Efficiency.

The exact employment-target formula is outside this document unless already implemented elsewhere.

---

# 7. Infrastructure Redesign

Infrastructure should be simplified away from a locally priced commodity and toward a **throughput/productivity system**.

The main state value is:

> **Infrastructure Efficiency**

Infrastructure Efficiency affects how much economic throughput a given industry can achieve for a given level of employment.

It does **not directly determine employment**.

Example:

```text
Industry employment: 100%
Infrastructure Efficiency: 50%
```

The industry can still employ its full workforce, but it operates at reduced economic throughput.

## Basic effect

Infrastructure Efficiency should multiply both:

- Inputs.
- Outputs.

It should **not** multiply employment.

Conceptually:

```text
Actual Output = Base Output × Infrastructure Throughput
Actual Inputs = Base Inputs × Infrastructure Throughput
```

This means poor infrastructure lowers productivity/output per worker without automatically creating unemployment.

That is useful for representing early economies with:

- High employment.
- Low productivity.
- Low wages.
- Low output.

rather than incorrectly representing undeveloped economies as simply unemployed.

---

# 8. Infrastructure Dependence by Sector

Different industries should be affected by infrastructure to different degrees.

The intended hierarchy is approximately:

```text
Subsistence: little or no infrastructure dependence
Agriculture: low dependence
RGOs / mining: moderate dependence
Factories: high dependence
```

One simple representation is an **Infrastructure Dependence coefficient**.

Example conceptual values:

```text
Subsistence    0.00
Agriculture    0.30
RGO            0.60
Factories      1.00
```

One possible relationship is:

```text
Effective Infrastructure Modifier =
1 + (Infrastructure Efficiency - 1) × Infrastructure Dependence
```

At 50% Infrastructure Efficiency, this would approximately yield:

```text
Subsistence    100%
Agriculture     85%
RGO             70%
Factories       50%
```

The exact numbers are balancing values, not fixed requirements.

Production Methods may optionally alter Infrastructure Dependence if later testing shows value in that distinction, but this should not be added unless useful.

---

# 9. Railroads and Ports

Railroads and ports remain industries.

They are unusual industries because their effective output is infrastructure rather than a normal globally traded good.

Their purpose is to support state Infrastructure Efficiency.

Important intended behaviors:

- High infrastructure usage should make infrastructure industries more profitable.
- Low usage should reduce profitability.
- Subsidies may be needed to maintain excess or strategically important infrastructure.
- Good infrastructure can provide positive productivity bonuses above a normal baseline.
- Positive infrastructure bonuses should have diminishing returns.

This creates a feedback loop:

```text
Economic growth
→ infrastructure demand rises
→ railroads/ports become more valuable/profitable
→ infrastructure investment rises
→ Infrastructure Efficiency improves
→ economic productivity rises
```

The exact railroad revenue mechanism remains an implementation detail and can be simplified as needed.

The major design requirement is that infrastructure producers remain economically meaningful without forcing infrastructure back into a complicated local commodity-price system.

---

# 10. State Economic Characteristics

State-level economic differentiation remains important.

States may provide:

- Wage levels.
- Infrastructure Efficiency.
- Land quality.
- Resource deposits.
- Port access.
- Local production modifiers.
- Available workforce.
- Other permanent or semi-permanent geographic advantages.

These values should shape economic geography without requiring every state to function as an independent market.

There are no general local commodity prices.

---

# 11. Pops and Consumption

Pops continue interacting with the economy through:

- Employment.
- Wages/payroll.
- Dividends.
- Consumption.

Consumption remains based broadly on:

> **Pop type + wealth level → consumption basket**

This may later be optimized by caching or aggregating repeated basket calculations, but the wealth-basket model itself does not need to be removed.

---

# 12. Tick Structure

The main economy runs **monthly**.

Trade runs **weekly**, because resource shortages need faster resolution.

The trade tick should avoid recomputing expensive state-side production logic where possible.

---

# 13. Investment: Core Concept

Investment is organized around **investment opportunities**, not a single national profitability value for each sector.

Important distinction:

> **Existing profitability** answers how profitable current capital is.

> **Investment opportunity** answers how much new capital could plausibly be invested at a given expected return.

This distinction is especially important for limited industries such as gold mining.

A gold sector may be extremely profitable but have almost no remaining expansion opportunity.

---

# 14. Investment Opportunity Tiers

Investment opportunities are stored as **money amounts in tiers**.

Current intended bands:

```text
Exceptional    > 20% ROI
Good           10% to 20%
Fair            5% to 10%
Marginal       -5% to 5%
Below Marginal  ignored
```

Example:

```text
Steel
Exceptional: $10m
Good:        $80m
Fair:       $200m
Marginal:   $300m
```

Investment should prioritize:

1. Exceptional.
2. Good.
3. Fair.
4. Marginal.

This preserves useful information without maintaining an exact continuously updated ROI for every national sector.

The system only needs to store the **tier**, not an exact long-term ROI.

---

# 15. Brownfield Investment

Existing state-industries generate brownfield opportunities.

A state-industry estimates:

- Expected ROI.
- Plausible near-term expansion size.
- Construction cost.

That becomes an opportunity amount assigned to an investment tier.

## Labor-based expansion opportunity

A deliberately simple estimate can use:

```text
Available Expansion Labor =
Unemployment + small fraction of Employment
```

A working example discussed was:

```text
Unemployment + 0.03% of employed workforce
```

The exact percentage is a balancing choice.

It is acceptable for multiple industries in a state to independently assume access to the same labor when estimating opportunity.

Do **not** add an extra competition/allocation solver.

Why:

- Better opportunities will receive investment first.
- New projects will employ workers.
- Wages will rise.
- Lower-return industries will become less profitable.
- Their opportunities will naturally shrink or disappear.

The simulation itself should resolve this competition rather than predicting every interaction in advance.

---

# 16. Construction Lockout

A state-industry should not receive another expansion investment while it already has an expansion under construction.

This prevents repeated investment from endlessly delaying completion under the existing construction architecture.

This rule also naturally limits how quickly a highly profitable industry can absorb capital.

---

# 17. Limited Industries and Resource Caps

Limited industries require hard physical opportunity caps.

Examples:

- Gold: remaining deposit capacity.
- Coal/mining: remaining deposit capacity.
- Agriculture: available suitable/arable land.
- Forestry: resource/land constraints.
- Ports: geographic/port constraints where appropriate.

Example:

```text
Gold ROI: 40%
Remaining viable construction: $3m
```

Then gold contributes only:

```text
Exceptional Opportunity: $3m
```

even if existing gold mines are extraordinarily profitable.

This prevents finite resources from absorbing unlimited investment.

---

# 18. Greenfield / New Industry Investment

Industries that do not yet exist in a state require a **greenfield** check.

Example:

- Electronics is researched.
- No electronics industry currently exists in a candidate state.

A prospective first industry can be evaluated using:

- National/global archetype economics.
- State wage.
- State Infrastructure Efficiency.
- Local modifiers.
- Construction cost.
- Default/appropriate PM and AM.

The result is classified into an opportunity tier.

The exact ROI does not need to be permanently stored.

---

# 19. Greenfield Coarse Pre-Filter

It is too expensive and unnecessary to thoroughly test every absent industry in every state every month.

Use a cheap pre-filter first.

Possible inputs:

- Global archetype economics.
- National prices.
- Rough/national wage assumptions.
- Best Infrastructure Efficiency state.
- Major hard eligibility conditions.

If the coarse estimate is below Marginal even under favorable conditions, stop.

Do not perform expensive state searching.

Local modifiers are not expected to rescue an industry that is already clearly uneconomic at the coarse stage.

---

# 20. Greenfield Search Budget

Countries should not necessarily evaluate all ~50 absent industries every month.

Use a **greenfield search budget**.

Principles:

- Small countries can check fewer absent industries each month.
- Larger countries can receive more generous budgets.
- The budget can be fairly generous; the purpose is performance, not visibly restricting the player.
- Newly researched/unlocked industries should be evaluated immediately or given high priority.

The user intends to artificially limit very small countries, approximately those below five states, while allowing larger countries more leeway.

The exact search-budget numbers are a balancing/performance decision.

---

# 21. Greenfield Construction Throttling

The system must prevent a large country from simultaneously starting enormous numbers of first-time establishments for a newly unlocked industry.

Example problem:

> The USA researches Electronics and starts 24 electronics industries before the first one finishes.

Chosen solution:

- Limit **new establishments per sector**.
- A reasonable rule is approximately **one new establishment per sector per month**.
- Existing unfinished greenfield projects reduce the tier of further greenfield opportunities.

Conceptual rule:

```text
0 greenfield projects underway → normal tier
1 underway                    → -1 tier
2 underway                    → -2 tiers
3 underway                    → -3 tiers
```

The exact stopping rule is balancing-dependent.

This provides gradual industry diffusion without requiring complex future-price or saturation forecasting.

Once a state has the industry, later investment there becomes ordinary brownfield expansion.

---

# 22. Local and National Investment

A major design goal is representing the development of capital markets.

In less financially integrated economies, capital should remain local.

In more developed economies, money should propagate nationally.

This is important for representing differences between economies such as:

- Qing China.
- Japan.
- More financially integrated industrial economies.

The system should not assume that wealth generated in one state can automatically finance industry anywhere in the country.

---

# 23. No Per-Industry Money Pools

Do **not** maintain a separate persistent investment-money pool for every state-industry.

Investment opportunities are state/sector-specific, but actual money does not need to be stored that way.

Instead use broader investor pools.

This avoids:

- Large numbers of mostly idle money variables.
- Capital becoming permanently trapped inside a now-unprofitable industry.
- Unnecessary state × industry bookkeeping.

---

# 24. Investor-Type Capital Pools

The current simplified design uses investor-type buckets.

## Landowner / Particular Capital

Landowner capital has access to a restricted investment set.

Likely sectors include:

- Agriculture.
- Plantations/livestock where relevant.
- Forestry.
- Ports.
- Other explicitly landed sectors if later desired.

Landowners generally should **not** freely invest in modern factories.

This is intentional.

A wealthy agricultural economy should not automatically bootstrap modern manufacturing simply because landowners have accumulated money.

## Capitalist / General Capital

Capitalist capital has access to the broader industrial economy.

Likely includes:

- Factories.
- Mining.
- Railroads.
- Ports.
- Other industrial/commercial sectors.

The important rule is:

> **Investor type filters which opportunity buckets are visible.**

Do not add a second complicated investment-attractiveness system unless later testing proves it necessary.

---

# 25. Dividends and Capital Formation

Industry earnings pass through owners as dividends.

Those dividends then feed the appropriate investment-capital pool.

Conceptually:

```text
Agricultural profits
→ landowner dividends
→ Particular investment capital
```

```text
Factory profits
→ capitalist dividends
→ General investment capital
```

Because dividends are already routed through ownership, per-industry retained investment pools are not necessary.

---

# 26. Transition From Landowner to General Capital

A portion of the restricted/particular landowner capital should transfer into the broader capitalist/general investment pool as the economy industrializes.

The intended driver is:

> **Non-agricultural GDP share**

As non-ag GDP rises, more capital can leave the landed investment circuit and become available to general industrial investment.

Conceptually:

```text
High agricultural GDP share
→ most landowner capital remains particular/local
```

```text
High non-agricultural GDP share
→ larger share of capital becomes general/capitalist
```

This prevents a late-game industrial economy from having excessive investment permanently trapped in agriculture.

The exact transfer function remains a balancing choice.

---

# 27. Capital-Market Development

Capital-market development should govern **geographic mobility** of capital.

In a fragmented system:

```text
Capital generated in Illinois
→ mostly remains available in Illinois
```

In an integrated national system:

```text
Capital generated in Illinois
→ can finance opportunities elsewhere in the country
```

The exact implementation of local versus national pools can vary, but the intended mechanic is:

> Development of capital markets allows geographically trapped wealth to propagate nationally.

This is a central gameplay distinction, not merely a performance optimization.

---

# 28. Attractiveness

A separate complicated attractiveness calculation is no longer considered necessary.

The preferred simplified structure is:

- **ROI / opportunity tier** determines desirability.
- **Investor type** determines eligibility.
- Other existing modifiers can lightly affect weighting/tier placement if useful.

Avoid duplicating the same economic reasoning in both:

- ROI.
- Attractiveness.

If the existing code already has an attractiveness concept, it may be adapted rather than fully removed, but it should not become a second independent profitability system.

---

# 29. Investment Allocation Philosophy

Investment should generally fund the best opportunities first.

Conceptually:

```text
Exceptional
→ Good
→ Fair
→ Marginal
```

Within a tier, distribution can use whatever lightweight weighting remains useful.

It is acceptable if total advertised opportunity is much larger than actual available investment.

In fact, this is preferable to opportunity being too restrictive.

The system does **not** need to perfectly estimate all future competition for:

- Labor.
- Wages.
- Infrastructure.
- Commodity demand.

Those effects should resolve after projects are funded and completed.

---

# 30. Important Simulation Philosophy

A recurring design principle is:

> **Do not predict feedback that the simulation will naturally resolve later.**

Examples:

Do not build a complicated system to ensure several industries cannot all estimate use of the same workers.

Instead:

```text
Multiple industries appear investable
→ best receive investment first
→ employment rises
→ wages rise
→ weaker industries lose profitability
→ their future opportunity tiers fall
```

Likewise, do not calculate the ultimate maximum manufacturing size of a state.

Only estimate enough near-term opportunity to guide current investment.

This keeps the system understandable and performant.

---

# 31. Important Performance Principles

Especially because HOI4 mod scripting is not normal C++ game code, avoid assumptions about contiguous data or low-level memory layout.

The relevant performance concerns are more likely to be:

- Number of scripted calculations.
- Number of scope changes/traversals.
- Number of modifier lookups.
- Number of persistent variables.
- Frequency of recalculation.
- Repeating the same PM/state calculations unnecessarily.

Important strategies:

1. Precompute/bake slow modifiers.
2. Aggregate common national/archetype calculations.
3. Keep absent industries out of normal monthly industry processing.
4. Use coarse greenfield filters before state searches.
5. Use greenfield search budgets.
6. Recompute aggregates when something meaningful changes rather than blindly rebuilding everything.
7. Keep state-industry persistent data minimal.

---

# 32. High-Level Economy Flow

A simplified monthly flow can be thought of as:

```text
State / Industry persistent state
    Size
    Employment
    PM
    AM
    financial memory
        ↓
Slow local modifiers resolved / cached
        ↓
Country / archetype production economics
        ↓
State-specific employment decisions
        ↓
Infrastructure Efficiency modifies actual throughput
        ↓
Actual inputs / outputs / payroll / profits
        ↓
Country supply / demand / sector aggregates
        ↓
Owner dividends
        ↓
Investment capital pools
        ↓
Investment opportunity allocation
        ↓
Construction
```

Trade continues to resolve weekly using already-available country economic information wherever possible.

---

# 33. High-Level Investment Flow

```text
Industry profits
    ↓
Owner dividends
    ↓
Investor capital pools
    ├── Landowner / Particular
    └── Capitalist / General
    ↓
Capital-market / structural-development transfers
    ↓
Local and/or national capital availability
    ↓
Investment opportunities
    ├── Exceptional
    ├── Good
    ├── Fair
    └── Marginal
    ↓
Best permitted opportunities funded first
    ↓
Construction begins
    ↓
Opportunity suppressed while under construction
    ↓
Project completes
    ↓
Employment / wages / prices / infrastructure adjust
    ↓
Future profitability and opportunity tiers change
```

---

# 34. Settled vs. Open Decisions

## Settled direction

- State industries remain.
- Size, Employment, PM, AM, and financial state are the core persistent state-industry values.
- PMs/AMs remain state-specific.
- Infrastructure becomes primarily a throughput/productivity mechanic.
- Infrastructure affects sectors by different amounts.
- Subsistence is barely/not infrastructure-dependent.
- Factories are highly infrastructure-dependent.
- Railroads and ports remain industries.
- Employment remains state-specific.
- Investment is represented as opportunity money in ROI tiers.
- Existing and greenfield investment are treated differently.
- Resource industries have hard physical opportunity caps.
- One state-industry expansion at a time.
- Greenfield investment is throttled.
- Greenfield opportunities use a coarse pre-filter and search budget.
- Capital can remain local depending on capital-market development.
- No persistent per-industry investment-money pools.
- Landowner and capitalist capital have different eligible investment categories.
- Non-ag GDP share helps move capital from particular/landowner investment toward general/capitalist investment.
- The simulation should resolve labor/wage competition rather than forecasting all of it during investment allocation.

## Open / balancing decisions

- Exact Infrastructure Efficiency curve.
- Exact Infrastructure Dependence values.
- Exact railroad/port revenue formula.
- Exact brownfield labor-opportunity percentage.
- Exact ROI-tier thresholds if later tuning changes them.
- Exact greenfield search budgets.
- Exact greenfield concurrent-construction tier penalty.
- Exact non-ag GDP → capital-transfer function.
- Exact local vs. national capital-market mobility rules.
- Exact weighting within the same investment tier.
- Exact financial-history values that must remain persistent.

---

# 35. Design Intent Summary

The intended economy should feel significantly simpler internally than Victoria 3 while preserving the parts that matter for a long 1857-start simulation:

- Industrial geography.
- Uneven development.
- Colonial technological differences.
- Employment and recessions.
- Resource constraints.
- Infrastructure-driven productivity.
- Capital accumulation.
- Local versus national capital markets.
- Landowner versus capitalist investment behavior.
- Gradual emergence of new industries.
- State comparative advantage.

The central simplification is to avoid making every state a complete standalone market.

Instead:

> **States provide local constraints, wages, employment, technology, resources, infrastructure, and capital location. Countries handle shared market arithmetic and aggregate investment information.**

The system should favor approximate but stable investment signals over expensive attempts to perfectly forecast the future economy.
