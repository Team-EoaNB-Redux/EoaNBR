# Company System Design Document
**HOI4 Mod — Victorian Era Economic System**

This document summarizes design decisions for the Company (Corporation) layer of the custom economic system. It is intended as a reference for implementation.

---

## 1. Core Concept

Companies are large-scale corporate entities that sit between individual buildings and the national economy. They are the primary vehicles for capital mobilization, large-scale coordination, vertical/horizontal integration, foreign investment, and political influence.

They are deliberately more powerful and more risky than ordinary private investment.

**Key Constraints (Coding-Driven):**
- One Company HQ per state.
- One primary industry specialization type per country (for a given Company).

---

## 2. Ownership Structure

Ownership is split across four buckets:

| Bucket | Description | Notes |
|--------|-------------|-------|
| **Private** | Investment Fund + Capitalists in the HQ state | Main recipients of dividends |
| **State** | Government ownership | Full control for SEOs |
| **Creditor** | Temporary equity held by the Banking System | Created during reorganization; sold back over time via Investment Opportunities |
| **Treasury** | Shares held by the Company itself | From buybacks; no dividends, not counted in outstanding shares; re-issuable or cancellable |

- Only Companies can own foreign assets (via Branches).
- Dividends are split according to Private and State ownership percentages.
- Creditor and Treasury shares do not receive dividends while held.

---

## 3. Valuation & Stock

- **Valuation** = Current Asset Value + Projected Earnings modifiers + Moat/Reputation modifiers + Tech/Department synergy bonuses.
- **Stock Price** = Total Valuation / Outstanding Shares.
- Outstanding shares = Private + State + Creditor shares (Treasury shares are excluded).
- Companies can issue new shares (dilution) to raise capital.
- Investment Funds and the Government can buy/sell shares.
- Private Companies do not use the stock market.

---

## 4. Company Types

| Type | Stock Market | Capital Raising | Shareholder Pressure | Efficiency / R&D | Player Control |
|------|--------------|-----------------|----------------------|------------------|----------------|
| **Private** | No | Retained earnings only | Low | High (flexible) | Medium |
| **Publicly Traded** | Yes | Shares + debt | High (dividends) | Medium | Low |
| **State-Owned Enterprise (SEO)** | Optional | State funds + shares | Political | Lower (bureaucracy) | High |

---

## 5. Departments & Specialization

- Every Company has a **Primary Department** that receives permanent bonuses (throughput, input efficiency, etc.).
- Additional **Departments** can be unlocked via R&D or large investment.
- Companies can only invest in / acquire assets in industries matching their Departments.
- Primary Department gets a permanent specialization boost.
- Branching out is uncommon unless the Company is in aggressive expansion mode **and** has high market dominance in its core industry (Zaibatsu-style).

### R&D
- Companies allocate a portion of profits (or raised capital) to R&D.
- R&D generates progress toward bonuses in their departments:
  - Throughput
  - Output
  - Input efficiency
  - Construction cost/speed
  - Retooling cost/speed
  - Chance of accelerating national tech
- Sufficient R&D in a new area unlocks a new Department.
- SEOs are less efficient at R&D but can be forced by the player.

---

## 6. Integration

### Vertical Integration
- Acquiring upstream suppliers or downstream customers.
- Unlocked / boosted by Vertical Integration tech.
- Bonuses: reduced internal transfer costs, lower exposure to market volatility, throughput/output bonuses on integrated chains.

### Horizontal Integration
- Acquiring competitors in the same industry.
- Unlocked / boosted by Horizontal Integration tech.
- Bonuses: market share consolidation, economies of scale scaling with controlled capacity, modest pricing power.
- Risk: increased labor unrest and political backlash at high dominance.

High market dominance does **not** automatically allow price gouging for private companies. Price gouging is primarily a feature of state-protected / state-issued monopolies.

---

## 7. Foreign Direct Investment (Branches)

- Companies perform FDI by opening **Branches** rather than investing directly.
- Each Branch is a mini-company with its own HQ (in one state), budget, assets, and potential specialization shift.
- Branches enable capital controls and compartmentalized valuation.
- Profit repatriation is governed by the host country’s FDI law.

### FDI Law Ladder
1. FDI Banned
2. Capital Controls
3. Regulated Foreign Investment
4. FDI Encouraged

**Exclusive Economic Zones (EEZs)** are treated as a toggleable Policy/Decision rather than a core law (historically post-Victorian). They can represent chartered resource zones or spheres of influence.

### Branch Nationalization
- Converts the Branch into an independent Company in the host country.
- Becomes an SEO by default.
- Can have a different primary specialization than the parent.
- Parent may retain a minority stake depending on compensation.

---

## 8. Company Modes (State Machine)

Companies operate under a behavioral mode that shifts based on conditions:

- **Fast Expansion** — Heavy R&D + aggressive building/acquisitions. High debt risk.
- **Management / Optimization** — Focus on efficiency and dividends. Stable.
- **Monopolizing** — Horizontal focus + lobbying. Strong short-term margins, high backlash.
- **Crisis** — Triggered by losses or high debt. Austerity, layoffs, potential reorganization.
- **Complacent** — Triggered by long dominance + high dividends + private/family control. Penalties to R&D and innovation. SEOs are more resistant but suffer bureaucratic inefficiency.

---

## 9. Company Creation

- Requires a profitable industry of decent size in the state.
- Limit: one primary Company per industry type per state.
- Paths:
  1. Private investors (rich Capitalists in the state).
  2. Investment Opportunity via the national Investment Fund (easier).

---

## 10. Political Interactions

- Companies can bribe or fund Interest Groups to influence taxes, laws, and regulations.
- High political influence generates backlash among certain Interest Groups.
- State-issued monopolies (lobbied for by Companies) are the primary source of consumer price increases.

---

## 11. Bankruptcy & Reorganization (Chapter 11 Analog)

**Trigger:** Crisis Mode with critically high debt to the Banking System and sustained negative cash flow.

### During Reorganization
- R&D near zero
- Dividends suspended or heavily capped
- Throughput penalties
- Cannot open new branches or make acquisitions
- Debt payments frozen or reduced

### Resolution (Painful but Cleansing)
1. **Valuation Hit** — 35–60% immediate drop.
2. **Forced Asset Sales** — Sell 15–40% of non-core assets (secondary departments, underperforming buildings, or branches). Proceeds primarily repay the Banking System. Surviving assets receive efficiency bonuses post-exit.
3. **Equity Restructuring**:
   - Heavy dilution of existing Private and State ownership.
   - Banking System converts debt into a temporary **Creditor** equity stake (20–50%).
   - Treasury shares can be canceled (to reduce dilution) or re-issued to creditors.
4. Creditor equity is gradually sold back to the Private bucket via Investment Opportunities over 12–36 months (unless the State buys it).

### Exit Outcomes
- **Successful**: Exits in Management Mode with lower debt, smaller asset base, higher efficiency, and lower valuation than pre-crisis.
- **Partial**: Lingers with higher State ownership or lingering Creditor stake.
- **Failure**: Full liquidation (assets auctioned, possible branch nationalizations, Company dissolved).

**Anti-Cheat Measures:**
- Serial bankruptcies apply stacking “Distressed Reputation” penalties.
- Aggressive expansion / high dividends / heavy buybacks immediately before distress make asset sales harsher.

---

## 12. Stock Buybacks & Treasury Stock

- Companies can buy back shares from the Private bucket.
- Bought-back shares become **Treasury Stock**:
  - No voting rights
  - No dividends
  - Not counted in outstanding shares (boosts stock price / EPS)
  - Can be re-issued or canceled
- Treated similarly to Creditor equity (actively for sale / re-issuable).
- More common in Management / Complacent modes.
- Heavy buyback activity right before distress increases reorganization severity.

---

## 13. Mergers & Acquisitions

- Available from the start of the timeline (1857), with railway-driven activity in the 1840s–50s as the historical precedent.
- **Horizontal** acquisitions are same-department.
- **Vertical** acquisitions are related supply/demand industries.
- Cross-border acquisitions are limited and high-friction; nationalization is the primary forced-transfer mechanism.
- Full foreign Company takeovers are not allowed (branches only).

---

## 14. Historical Notes (Victorian Era)

- Railway amalgamations in the mid-1840s (e.g. LNWR 1846, Midland Railway 1844) mark the practical start of repeated corporate M&A.
- Standard Oil did not broadly raise consumer prices; prices fell due to efficiency.
- British steel decline involved complacency and under-investment.
- Equity receivership (especially for railways) is the Victorian analog to modern reorganization.
- Buybacks and modern Chapter 11 are later developments; early timeline should feel harsher.

---

## 15. Open Implementation Notes

- Company Modes should drive AI behavior (expansion aggressiveness, R&D allocation, dividend policy, lobbying intensity).
- Valuation modifiers should include revenue trajectory, profit margins, and integration strength.
- Branch valuations can be partially trapped under Capital Controls (listed on the host country’s stock market).
- Visibility: Full Company ledger screen with ownership breakdown, departments, R&D allocation, assets (domestic + foreign), current Mode, and integration status.

---

*Document generated from design discussion. Last updated for implementation reference.*
