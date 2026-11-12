# End of a New Beginning Redux — Economy Redesign Specification

## Status

This document replaces the earlier economy redesign notes as the current high-level specification for the End of a New Beginning Redux economic simulation.

The mod begins in 1857 and aims to provide a deep economic simulation while remaining performant inside HOI4's scripting environment. The design intentionally prioritizes stable real-economy behavior, cheap aggregation, and country-level player interaction. Financial systems deliberately introduce some instability through leverage, credit, and banking stress, but ordinary economic fluctuations should not routinely produce catastrophic collapses.

---

# 1. Core Design Philosophy

The economy should be complex internally but understandable externally.

The player should mostly interact with the economy at the national level through broad policy, investment, trade, financial, company, and planning tools. State-level information should remain available as explanation and diagnosis, not as a requirement for constant micromanagement.

The simulation should favor:
- stable negative feedback in the real economy,
- slow-changing physical capacity,
- faster changes in prices and utilization,
- state-based physical production,
- country-level economic decision-making,
- cached national calculations,
- minimal repeated state loops,
- as few independent persistent variables as practical,
- more goods/sectors where each remains cheap and compartmentalized,
- laws and institutions that modify shared systems rather than replacing them with entirely different economic models.

A useful overall framing is:

> **Country-sector = primary economic decision and optimization unit.**  
> **State-industry = physical and local realization of that sector.**

Finance then sits above the real economy as an accelerator. It allows investment to exceed accumulated retained capital, but introduces leverage, defaults, banking stress, and credit contraction.

---

# 2. Simulation Layers

The economy is divided into several interacting layers.

## 2.1 State Layer

States store persistent physical and local economic data:
- industry capacity/size,
- industry employment,
- PM and AM configuration,
- local ownership shares,
- local profitability helpers where useful,
- construction progress,
- infrastructure efficiency,
- labor availability,
- wages,
- arable land quantity,
- land quality,
- crop eligibility,
- resource potential,
- known deposits,
- resource quality,
- physical extraction capacity,
- local company footprints.

States remain the authoritative home for physical productive assets because state ownership can change through conquest or diplomacy.

## 2.2 National Sector Layer

Each country-sector stores or derives:
- total capacity,
- target utilization,
- actual output,
- input use,
- payroll,
- operating profit,
- retained capital,
- debt,
- interest expense,
- PM/AM cache economics,
- sector investment opportunities,
- generic/non-company ownership accounting.

The national sector determines broad economic behavior. States then attempt to realize those targets subject to local constraints.

## 2.3 Company Layer

Named companies are separate country-wide cached economic entities layered over state industries.

They maintain:
- controlled capacity,
- local ownership shares,
- PM/AM composition,
- geographical footprint,
- revenue,
- input costs,
- payroll,
- operating profit,
- retained capital,
- debt,
- interest expense,
- productivity or management modifiers,
- investment behavior.

Companies do not require local financial statements to be accumulated every tick. Local ownership and PM/AM composition determine where their operations exist and where their bonuses apply, while their financial accounting is performed at the cached national level.

## 2.4 Financial Layer

The financial system manages:
- sector capital,
- general investment capital,
- credit,
- bank reserves,
- bank capital,
- outstanding loans,
- interest rates,
- banking confidence,
- reserve requirements,
- capital requirements.

It amplifies growth and can create booms and busts.

## 2.5 Currency Layer

The currency system manages:
- commodity reserves,
- money minting/printing,
- base money,
- bank-created money,
- total money supply,
- money demand,
- inflation/deflation,
- exchange-rate or external-currency-value effects.

The system does not require literal circulating cash transactions.

---

# 3. Industries

An industry is fundamentally a productive sector with a physical location.

It:
- produces goods,
- consumes inputs,
- employs workers,
- pays wages,
- can earn or lose money,
- can expand when profitable,
- can contract when persistently unprofitable.

Industries remain state-based physically but are increasingly managed and evaluated nationally.

## 3.1 State-Industry Persistent Data

A state-industry should generally store:
- floating capacity/size,
- employment,
- PM,
- AM,
- local ownership shares,
- local profitability or margin helper,
- construction progress/state if needed.

Floating size is preferred over discrete integer levels because it allows gradual capacity decay and avoids abrupt disappearance of marginal industries.

Chronically unprofitable generic/local capacity can slowly shrink. Company-owned capacity may follow more deliberate company decisions.

---

# 4. National Target Utilization

Each national sector has a target utilization.

This is one of the central simplifying mechanisms of the redesign.

The broad process is:

1. The national sector evaluates current profitability and market conditions.
2. It chooses a target utilization.
3. Each state-industry attempts to reach that utilization.
4. Local labor constraints may prevent full fulfillment.
5. Local profitability may shift actual utilization slightly above or below the national target.
6. Over the long term, investment expands stronger locations and weak locations gradually contract.

Conceptually:

`local utilization = national target utilization + local adjustment`

The adjustment should remain small enough that the national target remains the dominant signal.

This makes market behavior more stable because a sector responds as a coordinated national aggregate rather than every state independently optimizing output.

---

# 5. Employment and Wages

Employment is stored on state industries because it is both useful for UI and cheap as a helper variable.

For each state:
- state-industries produce desired jobs from capacity and target utilization,
- desired employment is summed,
- working-class and middle-class labor pools attempt to fill those jobs,
- actual employment determines realized production,
- wages respond to labor-market tightness.

Infrastructure does not directly determine employment. It affects throughput/productivity.

Better PMs and AMs can change the required balance between working-class and middle-class labor.

Unemployment is not a separate pop type. It is the difference between the available class labor pool and employed members of that class.

---

# 6. Local Profitability and PM/AM Caching

Local profitability remains useful for:
- company decisions,
- state comparisons,
- investment placement,
- contraction,
- local utilization adjustment,
- player information,
- debugging.

It should be cheap.

The country can cache the base economics of each PM/AM combination under current national prices:
- output value,
- input cost,
- labor requirement,
- productivity.

Then local calculations only apply:
- local wage,
- local infrastructure,
- state modifiers,
- deposit/land quality where relevant,
- company modifiers where relevant.

A local operating margin can therefore be computed without reconstructing a full financial statement.

---

# 7. Prices and Market Stability

The real economy should be intrinsically stable.

Prices should use target prices derived from supply and demand, but actual prices should move gradually toward those targets.

Small discrepancies should adjust slowly. Large shortages or surpluses should produce much faster movement.

Conceptually:

`price change = price gap × nonlinear adjustment rate`

Possible behavior:
- tiny gap: no movement or very small movement,
- ordinary gap: gradual adjustment,
- extreme shortage: rapid jump,
- extreme surplus: rapid decline.

This prevents the market from instantly snapping between equilibria.

Short-run hierarchy:
- prices: relatively fast,
- utilization/employment: medium,
- physical capacity: slow.

Demand shocks should therefore first change prices, then utilization and employment, then capacity if conditions persist.

---

# 8. Infrastructure

Infrastructure is primarily represented through **Infrastructure Efficiency**.

It is a state-level throughput/productivity scalar rather than a locally priced commodity.

Poor infrastructure reduces the amount of inputs and outputs processed by a given amount of productive capacity and labor.

Employment itself is not directly reduced by infrastructure.

A useful generic formula is:

`effective infrastructure modifier = 1 + (Infrastructure Efficiency - 1) × Infrastructure Dependence`

Sector dependence differs:
- subsistence: none,
- agriculture: low,
- extraction/RGOs: moderate,
- factories: high.

Railroads and ports raise infrastructure efficiency and remain industries with revenue/profit tied to usage.

Poor infrastructure can reduce output and inputs together so profitability is not automatically destroyed purely because throughput is lower.

---

# 9. Natural Resources and Extraction

Vanilla HOI4 resource values should no longer be treated as the authoritative economic production system.

The redesigned extraction model distinguishes:

- **Potential Deposits** — geological potential not yet discovered,
- **Known Deposits** — discovered capacity that can be developed,
- **Extraction Capacity** — actual developed industry size,
- **Deposit Quality** — productivity/grade/accessibility.

Constraints:

`Extraction Capacity <= Known Deposits`

Prospecting converts:

`Potential Deposits -> Known Deposits`

Investment converts unused known deposits into extraction capacity.

Production is approximately:

`output = capacity × utilization × PM productivity × deposit quality × infrastructure effect`

Quantity and quality remain separate variables.

---

# 10. Agriculture and Land

Agriculture is primarily a state phenomenon.

Each state should have:

- **Arable Land Quantity** — how much land can physically be used,
- **Land Quality** — general productivity/carrying-capacity quality,
- **Crop Eligibility** — whether particular crop sectors are viable.

Land quantity must not be derived primarily from population.

Crop differentiation should usually be binary or categorical:
- can grow,
- cannot grow,
rather than maintaining crop-specific yield matrices for every state.

Commercial agriculture sectors compete for available land.

---

# 11. Subsistence Agriculture

Subsistence agriculture uses remaining arable land.

The core concept is **carrying capacity**:

`K = Remaining Arable Land × Land Quality × Subsistence Yield Technology`

Yield improvements should primarily increase carrying capacity rather than generating proportional market surplus.

When population is below carrying capacity, higher yields may reduce labor intensity or increase security rather than massively increase market output.

When population exceeds carrying capacity, additional peasants can work marginal land at diminishing returns.

The older simple approximation remains valid:

For `P > K`:

`effective subsistence production = K + 0.5 × (P - K)`

A smoother diminishing-return curve may be preferable if HOI4 expression support makes it cheap.

Subsistence is effectively independent of infrastructure.

Peasants should also have reduced market participation because much of their consumption is produced internally.

---

# 12. Industrial Capacity and Vanilla Factories

Civilian factories, military factories, and dockyards should not be fundamental economic industries.

Instead, the economy has underlying productive industrial capacity.

The government can hire or allocate industrial capacity for:
- civilian/construction use,
- military production,
- naval/shipbuilding use.

Vanilla civ/mil/dockyard counts can become implementation shadows of this allocation rather than real economic assets.

This keeps the economic simulation and HOI4 production mechanics connected without duplicating whole sectors.

---

# 13. Investment

Investment is divided into several capital sources.

## 13.1 Sector Retained Capital

Successful sectors retain part of their earnings.

This retained capital primarily finances further expansion of the same sector.

This creates path dependence:

> profitable textiles accumulate textile capital and expand textiles.

This reduces the need for a giant national solver to compare every sector against every other sector every month.

## 13.2 General Investment Pool

A portion of sector retained earnings flows into a general investment pool.

The share transferred is determined largely by the financial system and capital-market laws.

This is the main mechanism for cross-sector private capital allocation.

A financially primitive economy may keep most capital trapped in the sector where it originated.

A financially developed economy can redirect a larger share toward new opportunities.

## 13.3 Greenfield Investment

New sectors have no retained sector capital.

They therefore usually require:
- general investment capital,
- bank credit,
- government investment,
- foreign investment,
- company investment.

This naturally makes industrial takeoff harder in backward economies and gives finance, state intervention, and foreign capital a real role.

## 13.4 Investment Opportunity Tiers

Investment opportunities can still use broad ROI buckets:

- Exceptional: >20%
- Good: 10–20%
- Fair: 5–10%
- Marginal: roughly -5% to +5%
- below Marginal: ignored

These tiers can be used primarily to compare geographic expansion locations within a sector and to allocate scarce general capital.

## 13.5 Greenfield Throttling

Potential anti-spam rules:
- one new establishment per sector per month,
- one construction project per state-industry at a time,
- coarse country-level opportunity prefilters,
- limited search budgets for very small countries.

These should remain lightweight and may be reduced if financing constraints already sufficiently limit expansion.

---

# 14. Finance and Credit

The real economy should generally self-stabilize.

Finance deliberately introduces positive feedback and overshoot.

Typical boom:

`profitability rises -> borrowing rises -> investment rises -> employment/income rises -> demand rises -> further expansion`

Typical bust:

`profitability falls -> leveraged borrowers struggle -> defaults rise -> bank capital falls -> credit contracts -> investment falls -> unemployment rises`

The intent is not to create routine 50% GDP collapses. Severe crises should primarily hit:
- investment,
- construction,
- employment,
- indebted sectors,
before substantially destroying current productive output.

---

# 15. Banking

The banking system does not need explicit per-pop savings or explicit deposits.

The minimum useful banking stocks are:

- Bank Reserves,
- Outstanding Loans,
- Bank Capital,
- Banking Confidence,
- Interest Rate.

Derived values can include:
- credit capacity,
- available credit,
- capital ratio,
- reserve ratio,
- banking solvency.

## 15.1 Credit Constraints

Credit creation is constrained by both reserves and bank capital.

Reserve-based limit:

`Reserve Credit Limit ~ Bank Reserves / Reserve Requirement`

Capital-based limit:

`Capital Credit Limit ~ Bank Capital / Capital Requirement`

Actual credit capacity is the minimum of the two.

Bank capital absorbs loan losses.

A borrower default:
- reduces outstanding performing loans,
- destroys bank capital,
- does not automatically destroy household savings,
- can therefore sharply reduce new lending capacity.

If banks become severely insolvent, a true banking crisis can occur.

## 15.2 Fractional-Reserve Money Creation

Bank lending creates bank money.

The simulation does not need to model individual deposits or interbank settlement.

The reserve system can be treated as an aggregate constraint on how much bank-created money/credit can exist.

---

# 16. Money Supply

Total money supply is:

`Money Supply = Base Money + Bank-Created Money`

## 16.1 Base Money

Base money is created through:
- minting,
- printing,
- central/state monetary issuance.

Commodity-standard laws may constrain effective issuance through reserve backing.

## 16.2 Bank-Created Money

Bank money is approximately tied to outstanding performing bank loans.

New lending increases bank-created money.

Loan repayment reduces it.

Defaults and write-offs eventually reduce it while also damaging bank capital.

The reserve multiplier is a constraint on lending, not an additional multiplication applied after loans are already counted.

---

# 17. Money Demand and Inflation

Money demand can remain extremely simple.

A baseline form:

`Money Demand = Real GDP × Monetary Demand Multiplier`

The GDP measure should be real/base-price GDP rather than nominal GDP so inflation does not mechanically generate its own money demand.

The multiplier can represent:
- monetization of the economy,
- velocity,
- financial development,
- other broad institutional effects.

Normalize the system so that under baseline conditions:

- GDP = 100,
- Money Demand = 100,
- Money Supply = 100,
- Price Level = 1.0.

Inflation/deflation is driven by the ratio of money supply to money demand.

A simple target concept:

`Price Level Target ~ Money Supply / Money Demand`

Actual price level should move gradually rather than snap.

---

# 18. Commodity Reserves and Exchange Rate

Commodity reserves include monetary valuables such as:
- gold,
- silver,
- possibly broader valuables depending on gameplay abstraction.

They change through:
- trade balance,
- valuables production,
- reserve accumulation,
- reserve spending,
- monetary policy.

A trade deficit can drain commodity reserves.

A trade surplus can increase them.

## 18.1 Structural Exchange-Rate Scalar

The exchange-rate variable should not attempt to model every nominal effect of domestic inflation.

Domestic inflation is treated as a nominal scaling effect.

The exchange-rate scalar instead represents the structural external value of the currency for international trade.

It is driven primarily by commodity reserve adequacy and monetary institutions.

Conceptually:

`Reserve Adequacy = Actual Commodity Reserves / Required Commodity Reserves`

Exchange-rate target depends on reserve adequacy and law-specific coefficients.

Reserve depletion weakens the external currency value:
- exports become cheaper,
- imports become more expensive,
- the trade balance tends to improve.

Reserve accumulation can strengthen the currency:
- imports become cheaper,
- exports become less competitive,
- surpluses tend to shrink.

The relationship should be damped and nonlinear rather than one-for-one.

## 18.2 Monetary Laws

Monetary laws should modify coefficients rather than create entirely separate monetary systems.

Examples:

### Hard Commodity Standard
- strong reserve-backing requirement,
- weak minting flexibility,
- strong reserve influence on external currency value,
- limited monetary discretion.

### Looser Commodity Standard
- lower backing requirement,
- greater issuance flexibility,
- weaker reserve sensitivity.

### Fiat Currency
- little or no commodity-backing constraint on issuance,
- much more effective money creation,
- commodity reserves matter less to domestic issuance,
- monetary mismanagement can produce inflation.

The same underlying variables and formulas remain.

---

# 19. Companies

Companies remain economically distinct even though state industries are physically aggregated.

Local ownership shares remain necessary because they determine:
- where company capacity exists,
- which PM/AM combinations the company uses locally,
- where company productivity bonuses apply,
- exposure to local wages, infrastructure, and state modifiers,
- territorial consequences from conquest or loss.

However, revenue and expenses do not need to be passed upward from each individual state-industry.

Instead, each company is a cached national entity.

Its national accounts calculate:
- total output,
- input use,
- payroll,
- revenue,
- operating profit,
- debt service,
- retained earnings.

Local ownership shares and PM/AM buckets feed those cached totals.

The generic/non-company sector can be treated as another ownership entity for accounting purposes.

## 19.1 Company Competition

Companies can differ by:
- productivity,
- management bonuses,
- PM/AM adoption,
- debt,
- interest burden,
- retained capital,
- geographic exposure.

They can therefore have different profit margins within the same national sector.

Successful companies can compound:
- higher productivity,
- higher profit,
- higher retained capital,
- faster expansion,
- growing market share.

Overleveraged or poorly managed firms can lose market share or fail.

## 19.2 Company Defaults

Company defaults can directly damage the banking system through loan losses.

This makes companies important channels for financial instability.

---

# 20. Player Interaction Philosophy

Player interaction should remain predominantly national.

The player should mostly:
- set incentives,
- redirect capital,
- regulate trade,
- support or suppress sectors,
- manage finance and currency,
- support companies,
- manage strategic priorities.

Economic laws determine which controls are available and how directly the player can intervene.

A useful principle is:

> **Laws do not replace economic systems; they change who is allowed to set the targets.**

---

# 21. Player Economic Controls

## 21.1 Sector Investment
Players may be able to:
- fund expansion of existing sectors,
- fund creation of new sectors,
- set investment priorities,
- offer grants,
- co-invest with private capital,
- guarantee loans,
- create development funds/banks,
- restrict investment,
- set direct capacity targets under planning.

## 21.2 Sector Operations
Players may be able to:
- subsidize sectors,
- tax sectors,
- guarantee purchases,
- grant procurement preference,
- prioritize scarce inputs,
- subsidize PM/AM adoption,
- mandate PM/AM adoption,
- designate strategic sectors,
- restrict obsolete methods,
- set target utilization under planned or wartime systems,
- impose output quotas if needed.

## 21.3 Companies
Players may be able to:
- support a national champion,
- subsidize specific companies,
- grant contracts,
- inject capital,
- guarantee debt,
- bail out firms,
- purchase state equity,
- nationalize,
- privatize,
- force or encourage mergers,
- block mergers,
- break up monopolies,
- grant or revoke concessions,
- restrict foreign ownership,
- grant preferential access to resources or procurement.

## 21.4 Trade
By good:
- import tariff,
- export tariff,
- import subsidy,
- export subsidy,
- import quota,
- export quota,
- import ban,
- export ban,
- embargo,
- preferential tariff treatment,
- strategic import purchasing,
- surplus export dumping.

## 21.5 Strategic Stockpiles
Players may:
- set stockpile targets,
- buy into reserves,
- release reserves,
- designate strategic goods,
- create emergency food/fuel/material reserves,
- requisition stockpiles in war.

## 21.6 Currency
Players may:
- mint/print money,
- reduce issuance,
- change backing requirements,
- accumulate reserves,
- spend reserves,
- defend the currency,
- devalue/revalue where permitted,
- suspend convertibility,
- restore convertibility,
- change monetary regime.

## 21.7 Central Banking
Players may:
- set the policy/base rate,
- provide emergency liquidity,
- act as lender of last resort,
- withdraw liquidity,
- defend the currency,
- establish central-bank independence or direct state control.

## 21.8 Banking
Players may:
- set reserve requirements,
- set capital requirements,
- guarantee loans,
- recapitalize banks,
- impose credit controls,
- prioritize lending to sectors,
- nationalize or privatize banks,
- create specialist development/agricultural/industrial banks,
- restrict foreign lending.

## 21.9 Capital Markets
Players may:
- influence how much retained sector capital enters the general pool,
- regulate foreign investment,
- regulate capital exports,
- impose capital controls,
- set foreign ownership limits,
- encourage domestic reinvestment.

## 21.10 Taxation
Potential tools:
- income taxes,
- corporate/profit taxes,
- consumption taxes,
- excises,
- tariffs,
- resource royalties,
- land/property taxes,
- payroll taxes,
- windfall taxes,
- investment tax credits,
- sector exemptions.

## 21.11 Government Spending
Potential tools:
- infrastructure,
- education/qualification spending,
- welfare,
- unemployment support,
- military procurement,
- public payroll,
- industrial development,
- research support,
- direct investment,
- subsidies and transfers.

## 21.12 Government Debt
Potential tools:
- issue debt,
- repay debt,
- adjust borrowing,
- restructure/default in extreme cases,
- guarantee sector/company borrowing.

## 21.13 Labor
Potential tools:
- minimum wage,
- working-hour limits,
- wage subsidies,
- unemployment benefits,
- hiring subsidies,
- severance/layoff restrictions,
- child-labor laws,
- occupational safety,
- training/education,
- migration encouragement/restrictions,
- conscription,
- wartime labor allocation.

## 21.14 Price and Consumption Controls
Potential tools:
- consumption subsidies,
- excise taxes,
- price ceilings,
- price floors,
- guaranteed producer prices,
- rationing,
- state procurement,
- essential-goods designation,
- luxury taxation.

## 21.15 Infrastructure
Potential tools:
- fund railways,
- fund ports,
- subsidize transport,
- set maintenance,
- prioritize strategic infrastructure,
- direct regional development,
- military freight priority,
- industrial freight priority,
- nationalize/privatize transport.

## 21.16 Resources
Potential tools:
- fund prospecting,
- subsidize extraction,
- tax extraction,
- set royalties,
- grant concessions,
- revoke concessions,
- restrict exports,
- reserve resources for domestic use,
- run state extraction,
- regulate foreign concessions.

## 21.17 Agriculture
Potential tools:
- fund agricultural expansion,
- crop subsidies,
- guaranteed prices,
- agricultural tariffs,
- emergency export restrictions,
- land improvements,
- irrigation,
- agricultural credit,
- state procurement,
- land reform,
- planned crop targets.

## 21.18 Ownership
Potential tools:
- nationalization,
- privatization,
- minority or majority state stakes,
- cooperatives,
- public-private partnerships,
- foreign ownership rules,
- forced divestment or transfer.

## 21.19 Regional Development
Potential tools:
- development regions,
- tax incentives,
- infrastructure priority,
- special economic zones,
- reconstruction programs,
- colonial-development programs,
- depressed-region support.

## 21.20 Wartime/Emergency Controls
Potential tools:
- rationing,
- price controls,
- wage controls,
- export bans,
- import prioritization,
- forced utilization,
- forced PM conversion,
- production quotas,
- industrial conversion,
- strategic input allocation,
- labor conscription,
- mandatory procurement,
- capital controls,
- credit controls,
- emergency issuance,
- requisitioning,
- temporary nationalization.

---

# 22. Economic-System Differences

Different economic systems should use the same underlying economy but grant different levels of control.

## 22.1 Laissez-Faire
Mostly indirect tools:
- taxes,
- tariffs,
- monetary policy,
- financial regulation,
- infrastructure,
- government contracts,
- limited emergency intervention.

## 22.2 Interventionist / Developmental State
Adds:
- sector subsidies,
- direct investment,
- loan guarantees,
- favored companies,
- strategic-sector support,
- development banks,
- PM/AM incentives.

## 22.3 Planned Economy
Adds:
- direct capacity construction,
- national utilization targets,
- production quotas,
- input priorities,
- PM mandates,
- wage controls,
- price controls,
- direct ownership.

The strongest planned-economy control should likely be national target utilization rather than state-by-state micromanagement.

---

# 23. Pops

The population system should be heavily simplified because each pop type imposes roughly similar performance cost.

Recommended persistent socioeconomic pop types:

- Slaves
- Peasants
- Working Class
- Middle Class
- Upper Class

The old distinction between:
- laborers,
- workers,
- professionals,
- specialists,
- capitalists,
- landowners,
- bureaucrats,
- soldiers

should largely disappear.

---

# 24. Slaves

Slaves:
- remain at or near minimum wealth,
- earn no normal wages,
- can fill working-class jobs where slavery is allowed,
- reduce an industry's effective wage cost,
- consume a minimum basket.

Their consumption must still be funded.

The simplest accounting is employer/owner maintenance:

`Slave Maintenance Cost = Slave Workers × Minimum Consumption Cost`

This is not a wage but acts as a cheap labor cost.

---

# 25. Peasants

Peasants:
- work subsistence land,
- do not fill ordinary industrial jobs unless transferred out of peasantry,
- receive subsistence output/income,
- participate only partially in the market economy.

Their market demand should be reduced relative to normal wage earners because much of their consumption is internally produced.

A simple market-participation scalar is sufficient.

---

# 26. Working Class

Working-class pops:
- provide ordinary manual/industrial labor,
- receive wages,
- can be unemployed,
- have a wealth level,
- consume market goods according to wealth.

Their aggregate income depends on:
- employed population,
- wages,
- transfers,
- taxes.

---

# 27. Middle Class

Middle-class pops:
- provide skilled/professional/technical labor,
- receive wages,
- can be unemployed,
- have a wealth level,
- consume according to wealth.

Better PMs and AMs may shift labor demand from working-class jobs toward middle-class jobs.

Government administration can also consume middle-class labor.

---

# 28. Upper Class

Capitalists and landowners should probably be merged into a single upper-class pop.

The redesign removes much of the need to distinguish them because capital allocation occurs through:
- sector retained earnings,
- general investment pools,
- financial institutions,
rather than through separate pop savings behavior.

Upper-class income can include:
- dividends,
- rents,
- company distributions,
- interest,
- other ownership income.

If politics needs to distinguish agrarian aristocracy from industrial bourgeoisie, that distinction should be represented through a cheaper derived elite-composition variable rather than a full additional pop type.

---

# 29. Bureaucrats

Bureaucrats do not necessarily need to be a dedicated pop.

Government administration can instead create middle-class jobs.

Administrative capacity can depend on:

`Filled Bureaucratic Jobs / Required Bureaucratic Jobs`

This lets bureaucracy compete with private sectors for skilled labor without adding a full additional pop type.

A separate bureaucrat pop is only justified if bureaucrats need distinct:
- political behavior,
- legal status,
- qualification behavior,
- demographic behavior,
- consumption behavior.

---

# 30. Soldiers and Active Manpower

Soldiers should likely not be a normal socioeconomic pop.

Instead, use **Active Manpower**.

Conscription removes people from civilian labor pools and places them into active manpower.

Demobilization returns them.

This stock can represent:
- active soldiers,
- military labor removed from the economy,
- conscription intensity.

Military wages and soldier consumption can be handled through government military spending rather than a full soldier wealth/demand system.

---

# 31. Pop Wealth and Demand

Each socioeconomic pop has a wealth level.

Wealth determines the consumption basket.

Current concept:
- every 10 wealth levels roughly doubles total spending,
- surplus income slowly raises wealth,
- deficits slowly lower wealth,
- a neutral range prevents constant oscillation.

This remains a good basis.

However, wealth should change basket composition as well as quantity.

Necessities should saturate.

Higher wealth should increasingly shift expenditure toward:
- manufactured consumer goods,
- services,
- luxuries,
- status goods,
rather than simply multiplying food consumption indefinitely.

---

# 32. Pop Demand

Pop demand is generated from:
- population size,
- wealth level,
- class-specific basket,
- market participation,
- employment/income outcomes.

Aggregate unemployment naturally reduces class income and therefore wealth/demand.

No separate unemployed pop is required.

Peasants use reduced market participation.

Slaves consume minimum goods funded through owner/employer maintenance.

Upper-class demand is based on ownership income.

---

# 33. Final Architecture Summary

The redesigned economy is built around the following hierarchy:

## Physical Economy
**State industries**
- capacity,
- employment,
- PM/AM,
- ownership,
- local conditions.

## Economic Decision Layer
**National sectors**
- target utilization,
- profitability,
- retained capital,
- investment,
- debt,
- national PM/AM economics.

## Corporate Layer
**Companies**
- local ownership shares,
- cached national accounts,
- company-specific PM/AM,
- productivity,
- debt,
- retained capital,
- competition.

## Investment Layer
- sector retained earnings,
- general investment pool,
- state investment,
- foreign investment,
- bank credit.

## Financial Layer
- bank reserves,
- bank capital,
- loans,
- interest,
- credit capacity,
- banking confidence.

## Currency Layer
- commodity reserves,
- minting/printing,
- base money,
- bank money,
- money supply,
- money demand,
- inflation/deflation,
- exchange-rate scalar.

## Population Layer
- slaves,
- peasants,
- working class,
- middle class,
- upper class,
- wealth-driven demand,
- active manpower outside the ordinary pop system.

## Player Layer
Mostly national:
- taxation,
- investment,
- subsidies,
- trade,
- finance,
- currency,
- companies,
- strategic stockpiles,
- planning,
- labor,
- ownership,
- infrastructure,
- emergency controls.

The overall goal is a system where the **real economy naturally converges toward equilibrium**, while **financial leverage, debt, and monetary stress create temporary instability and overshoot**. Physical production remains state-based and geographically meaningful, but economic decision-making and accounting are moved upward into cached national sectors and companies wherever possible.

---

# 34. Open Balancing / Implementation Questions

The following are deliberately not fixed yet and should be resolved through implementation testing rather than further up-front complexity:

- Exact nonlinear price-adjustment function.
- Exact national target-utilization controller.
- Size and speed of local utilization adjustments.
- Capacity decay rate for chronically unprofitable generic industries.
- Exact infrastructure-dependence values by sector.
- Smooth versus piecewise subsistence carrying-capacity curve.
- Exact ROI tier boundaries if balance requires changes.
- How much retained sector capital flows into the general pool under each financial law.
- Reserve requirement and bank-capital requirement values.
- Relationship between M0 and bank reserves.
- Exact bank-money creation constraint.
- Interest-rate formation.
- Banking-confidence behavior.
- Commodity reserve requirements under each monetary law.
- Exact exchange-rate response to reserve adequacy.
- Exact inflation response speed to money-supply/money-demand imbalance.
- Company investment and failure thresholds.
- Whether bureaucrats remain a separate pop after testing.
- Exact source-class tracking for active manpower and demobilization.
- Exact wealth-level basket compositions and transition speeds.
- Which player interventions are unlocked by which laws.

The design preference is to resolve these with the smallest stable formula that produces believable behavior rather than pre-solving every interaction.
