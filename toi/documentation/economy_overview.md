# EoaNBR Economy: How It Works

A plain-English briefing for an AI assistant (ChatGPT, Claude or similar) that can't see the code. It explains what the economy simulates, how the parts affect each other, what is switched on, and what limits any new idea has to live within. It describes behaviour, not syntax.

Last checked against the code: 2026-11-11.

## How to use this briefing

- You're helping design the economy of a Hearts of Iron IV mod. The person prompting you is usually Strat, the economy lead, who writes the script. Strat wants design thinking: mechanisms, trade-offs, failure modes, tuning levers. Don't write code unless asked.
- Each system below is marked **[LIVE]**, **[PARTIAL]**, **[OFF]** or **[PLANNED]**. Don't assume a system affects play because it's described here.
- Before you propose anything, read sections 9 to 11 (design principles, scripting limits, how to pitch). Most ideas that sound good fail one of those.
- Numbers given here are rough anchors for scale. Exact values live in a spreadsheet and change often.

## 1. What the game is

End of a New Beginning Redux (EoaNBR) is a total-conversion mod for Hearts of Iron IV (HOI4). It starts in 1857 and can run to the modern day. HOI4's own economy is little more than civilian and military factories, so the mod builds a full economic simulation in HOI4's scripting language: pops, industries, goods, prices, wages, trade, budgets, debt and investment. The spirit is close to Victoria, but it is much simpler inside, because HOI4 script is slow and every stored number makes save games bigger. Saves already take 5 to 10 minutes to load.

The economy ticks once a month for every country. Trade ticks weekly. Players act on it through a budget screen (tax and spending sliders), trade settings, building and upgrading industries, laws and national ideas, and events and focus trees. Content reaches the economy through modifiers and a set of documented effects such as "add treasury", "add debt", "add industries" and "construct industries".

## 2. The whole system in one paragraph

Every state has a population split into pop types, and a set of industries. Industries hire pops, turn input goods into output goods with a production method, sell the output at the market price, pay wages, and pass profit to their owners. Pops spend their income on a basket of goods that grows as their standard of living rises. All production and consumption in a country and its subjects is pooled into one market, with one price per good, and each price moves with the ratio of demand to supply. Markets trade with each other weekly through a global market. Governments tax income, spending, dividends and trade, and spend on administration, the military, research, construction and subsidies. Deficits become debt, and too much debt ends in bankruptcy. Each state's wage floats with how tight its labour market is. The intended growth engine is investment, where owners' savings build and upgrade industries. It is switched off while it's rewritten, so nothing grows on its own at the moment.

## 3. The building blocks

### States and countries [LIVE]
- **States** hold everything physical: population, industries, arable land, resource deposits, infrastructure and the local wage.
- **Countries** hold technology, laws, modifiers, the budget, the treasury and debt. A country runs the economy of the states it *controls*, so occupation moves a state's economy to the occupier.
- Tribal countries are left out of the economy.
- Countries are processed in order of industrial power, biggest first. That matters wherever there is a shared pool or first pick, such as investment.

### Pops [LIVE]
Population comes from HOI4's state population, counted in thousands. A fixed 35% of everyone is workforce; the rest are dependants. Each pop type in each state tracks its workforce, employment, earnings, spending, savings, standard of living and consumer confidence.

| Pop type | Role now | Pay relative to the state's base wage |
|---|---|---|
| Peasants | Subsistence farmers | Share of subsistence output |
| Laborers | Unskilled industrial jobs | 2× |
| Workers | Skilled and middle jobs | 4× |
| Professionals | No jobs yet (open problem) | 10× |
| Specialists | No jobs yet (open problem) | 20× |
| Capitalists | Own factories, commercial farms, urban buildings and railways; live on dividends | — |
| Landowners | Own mines and other resource extraction, ports, and a 20% cut of subsistence farming | — |
| Slaves, bureaucrats, soldiers | Defined, but play little part in the monthly loop | — |

Owners' numbers follow what they own: each industry holds a small number of owner places, about 2% of its jobs.

### Goods [LIVE]
There are 32 goods. Raw goods are food, luxuries, wood, fiber, iron, coal, copper, valuables, oil, rubber, aluminum, tungsten, chromium, titanium, silicon and rare earths. Made goods are steel, tools, machinery, chemicals, plastics, composites, electronics, portable power, consumer goods, textiles, vehicles, appliances, computers, electricity, services and entertainment.

- Each good has a fixed base price, for example food 2, wood 2, coal 2, iron 3, textiles 4, consumer goods 5, steel 8, machinery 20, valuables 25.
- Goods are also HOI4's strategic resources. The economy tells HOI4 how much of each good a country has, so military factories making equipment draw on the same steel and iron, and military use counts as market demand.
- Transport and shipping capacity are services, not tradeable goods (see Infrastructure Efficiency).

### Industries [LIVE]
An industry is one building type in one state, with a **size** (a number of levels). Kinds:
- **Resource extraction (RGOs):** mining, forestry and some raw farm goods. Size is the part of the state's deposit that is being worked.
- **Farms and plantations:** crop farms, rice paddies, livestock ranches, and cotton, luxuries and rubber plantations. They use arable land.
- **Factories:** steel foundry, mechanical works, tooling workshop, textile mill, consumer goods factory, chemical plant, and later electronics, vehicles, computers, synthetic fuels and more.
- **Urban:** urban centre (services), power plant, entertainment hub.
- **Transport:** railways and ports. They make transport capacity, not goods.
- **Subsistence farms:** automatic. They fill all arable land nobody else uses and are worked by peasants.
- **Government buildings:** HOI4's own civilian factories, military factories and dockyards. Their size follows the HOI4 building, they're always fully staffed, and the state budget pays their wages. They don't sell goods.

Industries unlock with technology. Every industry runs one production method and one automation method.

### Production methods (PMs) and automation methods (AMs) [LIVE]
- A **PM** is a recipe. Per thousand base workers it sets how much the industry makes, which inputs it needs, how the jobs split between laborers and workers, how much transport it uses, and what it costs to build and how long that takes. PMs come in four eras: 1857, 1900, 1950 and 2000.
- An **AM** is a second layer on top: steam engines, electrification, assembly lines, robots and so on. AMs mainly cut labour and add inputs such as machinery.
- Technology unlocks PMs and AMs. New buildings start on the latest unlocked method. Existing buildings only change method by retooling, which costs goods and time, and the AI only retools through investment, which is off.
- Every PM number is generated from Strat's "EoaNBR Economy" spreadsheet by a script. The sheet is where balancing happens.
- Technology bonuses to individual PMs were stripped out in the October 2026 rework and haven't been added back.

### Land and resources [LIVE]
- **Arable land:** each state has some. Commercial farms take it up, and whatever is left becomes subsistence farming. Peasants beyond what the land can hold farm "marginal land" at 70% productivity, so nobody is ever stranded without work.
- **Deposits** have three stages: *potential* (undiscovered), *known* (discovered but unworked) and *active* (being worked, which is the extraction industry's size). Prospecting turns potential into known, by random rolls with a chance of a major find. Exploiting turns known into active. Downsizing would turn active back into known.

### Markets and prices [LIVE]
- Every independent country leads its own market. Subjects join their overlord's market, and other countries can be placed in another's market, like a customs union.
- There is **one price per good per market.** Production and consumption from every state of every member are pooled.
- **Price rule:** price = base price × (demand ÷ supply)², held between a quarter of base and four times base. A 10% shortage raises the price about 21%, and a large shortage pins it at 4×. Valuables are fixed at twice base, money-like.
- Supply is production plus imports. Demand is pops' needs, industry inputs, materials for construction and retooling, military demand, and exports.
- Prices are recomputed weekly as trade changes. Production and consumption change monthly.

### Trade [LIVE]
- Each market sets a route per good: an amount to import or export, run weekly.
- All markets together form a **global market** with a world price per good, priced by the same rule over world supply and demand.
- Imports add to a market's supply and exports add to its demand, which pulls local prices toward world prices.
- Trade is limited by partners (you can't import more than others offer) and by shipping capacity from ports and convoys. If shipping is overloaded, all trade scales down.
- Trade profit is the gap between local and world price, minus tariffs and shipping cost.
- An automatic trade AI opens routes where trade profit per trade job is well above average earnings, resizes them, and closes unprofitable ones. National ideas such as Closed Economy shut trade off.

### Infrastructure Efficiency [LIVE, untuned]
Infrastructure Efficiency replaced an older system, in which transport was a priced good, in October 2026.
- Each state has **transport supply** and **transport demand**. Supply is a baseline from population and road technology, plus railways, plus part of port capacity. Demand comes from each industry's method.
- Their ratio sets the state's **Infrastructure Efficiency.** A shortage cuts throughput, down to a floor of 25%. Spare capacity gives a small bonus, up to +20%.
- It scales inputs and outputs, never jobs. Poor infrastructure makes workers less productive rather than unemployed, which suits poor, labour-heavy economies.
- Sectors depend on it to different degrees: farms 30%, resource extraction 60%, factories 100%, urban 50%. Subsistence doesn't depend on it at all.
- Railways and ports earn a fee per unit of transport, which is higher when the state is congested. Nobody pays the fee: the money appears and counts toward GDP. That's a known placeholder.

## 4. The monthly loop

Each country, in rank order:

1. Last month's net budget goes into the treasury. AI countries adjust their budget, and the spending sliders' bonuses update.
2. Technology unlocks and their modifiers refresh.
3. For each state the country controls:
   1. Construction and retooling progress. Finished projects add size.
   2. Industries bank last month's retained profit or absorb last month's loss.
   3. Prospecting rolls.
   4. Pops settle last month's finances: savings, shortfalls, standard of living. Population grows, and peasants and laborers move between farming and industry.
   5. The state's base wage moves according to last month's labour market.
   6. Each industry nudges its hiring target according to last month's profitability.
   7. Pops convert between types to fit the jobs on offer.
   8. Everything is recomputed: arable land and subsistence, jobs and employment, government buildings, production, finances and dividends, then each pop's earnings, needs, taxes, confidence and targets.
4. Companies and investment-fund bookkeeping. Investment opportunities are off.
5. Market leaders recompute supply, demand and prices for their whole market, and GDP.
6. The budget is recomputed: taxes, spending, debt and interest.
7. Statistics and graphs. The boom and recession check would run here, but it never triggers (see Known problems).

Weekly: markets re-price with current trade, the global market updates, the trade AI adjusts routes, and trade flows recompute.

**The lags matter.** Wages react to last month's labour market, hiring reacts to last month's profit, and pops act on last month's earnings. These one-month delays are a big part of why the economy can swing (see section 6).

## 5. How the pieces work

### Production and employment [LIVE]
- An industry's potential output comes from its size and method. Actual output depends on how fully it's staffed, Infrastructure Efficiency, economy of scale (bigger industries in one state get up to +20%), and national and sector modifiers.
- Partial staffing is slightly more productive per worker: a half-staffed plant makes about 59% of its full output.
- Each industry has an **employment target** from 10% to 100%, which is its hiring decision:
  - Profit margin above about 15%: it hires, faster the more profitable it is and slower when unemployment is already low.
  - Margin below about 5%: it fires, faster when its cash reserves are low.
  - In between: it holds steady.
  - The step can be as big as +20 or −25 percentage points in one month.
- Jobs are filled by pops of the matching type. If a state is short of a type, every industry there is short-staffed in proportion.

### Profit and where the money goes [LIVE]
- **Revenue:** output sold at the market price. Railways and ports get their transport fee instead.
- **Costs:** wages (base wage × the pop type's multiple × employees), inputs bought at market price, and **maintenance**. Maintenance is a fixed upkeep of about 3% of build cost a year, paid even on idle capacity.
- **Profit:** a third goes to the employees as bonuses. The rest is split between the industry's cash reserve, capped at about one month of full output, and dividends to the owning pop type in that state.
- **Loss:** it comes out of cash reserves, with no dividends paid. When reserves run out, the owners absorb the loss as negative dividends. Downsizing, where a loss-maker sells off capacity, is built but switched off until investment returns, because nothing would rebuild what it sheds.
- **Ownership:** factories, commercial farms, urban buildings and railways belong to the state's capitalists. Extraction, ports and the landlord share of subsistence belong to landowners. Companies can own slices of an industry (see below).

### Wages [LIVE]
- Each state has one **base wage**, and each pop type earns a fixed multiple of it.
- It floats monthly. If jobs exceed workforce (more than 99% utilisation), wages rise. Below 95% they fall, about five times more slowly, so wages are sticky downward. Between those bands they hold. The change is capped at ±2% a month.
- There's a floor: laborers never earn less than subsistence farming would give them.
- It's seeded at game start from history. A state's own value wins, then the country's, then a default for its technology tier, which rises from about 1.2 for tribes to about 4 for early mechanisation.
- Wages are a cost for industry and income for pops. A tight labour market raises wages, which squeezes margins, which slows hiring.

### Pops: income, spending, standard of living [LIVE]
- **Income:** a small universal base income, plus wages (or the subsistence share for peasants), bonuses, and dividends for owners. Capitalists and landowners divert part of their income toward investment.
- **Taxes:** income tax by bracket (lower, middle or upper, depending on a pop type's average earnings against the national average), sales tax on what they spend on goods, and corporate tax on dividends.
- **Standard of living (SoL),** from 1 to 200, sets each pop type's basket of goods. Food comes first. Textiles, consumer goods and services follow, then luxuries from around SoL 21, and later electricity, appliances, vehicles and computers. The basket's value roughly doubles every 10 SoL. It's defined in base-price value and bought at market price, so expensive goods squeeze pops.
- **Technology gates needs.** If a good isn't available yet, such as electricity, an older substitute fills the need. A state's electrification shifts the basket over time.
- **Each month,** pops compare what they want to spend (income × consumer confidence) with what their basket costs. A surplus slowly raises SoL and a shortfall lowers it. Spare income goes into savings up to a target of about a year's income, scaled by banking confidence. When the target falls, they spend down their savings.
- **Consumer confidence,** from 0.2 to 2, comes from national modifiers. Debt burdens and high interest rates lower it, and savings raise it. Below 1 pops save, and above 1 they spend more than they earn.
- **Peasants** live mostly off their own farms. Only about 20% of subsistence output reaches the market, and only about 20% of their needs show up as market demand.

### Pops changing type [LIVE]
- Each month, pops convert toward the jobs on offer: unemployed laborers become workers where workers are wanted, and so on. Total population never changes in this step.
- If industry needs more hands, peasants become laborers, at a rate limited by arable land. If there's a labour surplus and wages are low compared with farming, laborers go back to the land.
- Literacy and education limits exist but are set to 100% for now, so they never bind.

### Government budget [LIVE]
- **Revenue:** the taxes above, plus import and export tariffs and trade income. Effective rates are scaled by tax efficiency, and tariffs by bureaucratic efficiency.
- **Spending:** administration (scales with earnings, population and GDP), military payroll (manpower × average earnings), military procurement (goods for equipment), research, construction (builds the government pays for), projects, subsidies, order and intelligence, and social spending.
- **Sliders have political effects.** Taxes cost political power, stability, war support and *incentives*, a property-rights mood that drives investment appetite. Spending buys HOI4 bonuses: military spending improves army organisation and morale, research spending speeds research, and procurement raises production efficiency and lowers equipment cost.
- **Debt:** a negative treasury becomes debt, domestic or foreign. Interest starts around 8%, is cheaper for great and secondary powers, and rises when the lending pool is scarce. The *debt level* tracks debt against annual GDP. Passing roughly 200% fires **bankruptcy**: debt is wiped and spending is cut, but stability takes a heavy hit. Lower stability means lower productivity and consumer confidence, so pops dump their savings and prices spike.
- AI countries repay debt when they can and raise taxes when they're in deficit.

### GDP [LIVE]
- A state's GDP is value added: the market value of output minus inputs, plus subsistence food valued at base price, plus transport fees, plus government building output.
- **Money scale:** 1,000 money units = £1 million, and every flow is per month. The historical UK national income in 1857 was roughly £665M a year, which would be about 55K a month. That's the reference scale for the rebuild, not a value the game currently hits.
- GDP drives debt ratios, administration cost, each country's share of market trade, and the statistics screens.

### Investment [OFF, being redesigned]
How the old system works, which is still in the code behind a switch:
- Capitalists and landowners put part of their income into a national **investment fund**. The share depends on their contribution rate, the *incentives* level, and how attractive the best opportunity looks. It's damped if the fund already sits on idle money.
- The fund keeps a list of **investment opportunities**: build a new industry in a state, expand one, upgrade its PM or AM, exploit known reserves, prospect, or buy a slice of an industry. Each is scored by *attractiveness*, roughly annual return, where 10% ROI scores 100. The fund only backs opportunities scoring at least 100, up to a monthly spending target.
- A project first pools about 25% of its build cost, then pays the monthly construction cost while it builds. Construction materials are real demand for goods.
- Players can subsidise opportunities from the treasury.
- **While it's off,** nothing builds or upgrades on its own and downsizing is disabled. The money pops set aside for investment isn't spent on anything.

### Companies [PARTIAL]
- Companies own fractional slices of industries: a size-14 mill might be 2 levels Company A, 4 levels Company B and 8 levels local owners. Each slice earns its share of that industry's profit.
- A company keeps 30% of its dividends as its treasury and pays the rest to capitalists in its headquarters state, which can be a financial hub far from its holdings.
- Companies are founded dynamically, as an investment-fund "national opportunity" that buys a slice of a profitable local industry. Each new company makes the next more expensive. Companies can also expand, exploit and prospect.
- The bookkeeping runs every month, but founding and company investment sit behind the investment switch. In practice no companies exist yet.
- Planned: companies defined at game start, valuations and a stock market, state-owned shares, mergers and acquisitions.

### Banking and finance [mostly OFF]
- A country-level bank exists but is disabled. Pop borrowing and repayment are stubbed out, so pops only save.
- The *incentives* driver is live: a long-term property-rights mood, kept separate from short-term consumer confidence and investor confidence.
- Planned: banking levels (none, domestic, international), inflation from a money supply, credit ratings that set borrowing limits, bank runs, default leading to bankruptcy, and international lending from great powers through explicit credit lines.

### Projects [LIVE]
Projects are country-level works, such as work programmes, with a goods bill and a build speed. Each month a project buys as many goods as it can toward its bill, and when it finishes it fires an effect. Content uses them for reforms and public works.

### Economic cycle [built, dormant]
Every month, each state's GDP would be compared with its 3-year average, weighted by size. If most of the economy is falling, the country enters a recession, depression or free fall. If most is prospering, it gets a boom. Players get events, the AI gets the national idea directly, and stability moves. It never fires, because the month counter that should advance the years is never incremented.

## 6. Feedback loops to know

- **Price-employment swing (destabilising).** A shortage squares into a price spike, the producers' margins jump, they hire up to 20 points in one month, supply overshoots, the price crashes, and they fire. Revenue uses last month's price and hiring uses last month's profit, so the delays amplify the swing. In tests, capping the hiring steps at 5 to 10 points, or using a straight-line price curve, stopped it. Trade probably damps it in the real game. This is the biggest open stability problem.
- **Wage-labour loop (stabilising).** Tight labour raises wages, which squeezes margins, which slows hiring. Wages are sticky downward, so a slump shows up as unemployment first, and wages fall later.
- **Bankruptcy spiral.** Debt grows faster than GDP, bankruptcy follows, stability crashes, which cuts productivity and confidence, pops spend their savings, prices rise, real incomes fall, and GDP falls further.
- **Infrastructure loop (partial).** Growth raises transport demand, Infrastructure Efficiency falls, and railways and ports earn more. The planned half, where investment then builds more railways and ports, needs investment back.
- **Investment loop (off).** Profit becomes dividends, dividends feed the investment pool, the pool builds capacity, wages and prices adjust, and the next round of opportunities changes. Without it the economy can only reshuffle labour; it can't grow.

## 7. Current state (November 2026)

- **The map has been stripped back to subsistence farming,** on purpose. Every state's industries and deposits are commented out of the history files, leaving only subsistence and HOI4's own factories. On the old map, Britain went bankrupt in its first July, in both the game and the simulator. The plan is to rebuild the world from scratch, sector by sector, so that world supply and demand start roughly equal for every good. Some asymmetry between goods, such as oil being very valuable, is wanted later. Historical targets for Britain and India are written as comments in the history files.
- **The next step is fixing budgets and debt for the new, smaller GDPs.** Starting debts and spending were sized for the old map, so many countries go bankrupt early.
- **Off:** investment, downsizing, banking, pop borrowing, the economic cycle.
- **Recently done:** generated PMs, Infrastructure Efficiency, floating wages, maintenance costs, the companies MVP, incentives.
- **Testing:** a headless simulator called redux-eco-sim runs the mod's real economy scripts outside the game. It matched in-game British GDP to within about 0.5% at startup and after one month, so it's trusted for fast experiments. In-game testing is slow.

### Known problems
1. Price-employment oscillation (section 6).
2. Professionals and specialists have no jobs.
3. Base wages drift down over the years (in one test, from 3.2 to about 1.3 over five years). Either they start too sticky or industries add too little value.
4. Budgets and debt don't scale with GDP: some spending lines stay large when the economy is small.
5. Railways lose money in busy hubs, while empty rural states get the full +20% Infrastructure Efficiency bonus for free.
6. Many late automation upgrades are pointless: once an AM's labour cut hits zero, the extra input cost remains.
7. The economic cycle never fires (month counter bug).
8. Money pops divert to investment disappears while investment is off.

## 8. Where it's heading [PLANNED]

The agreed direction for the next big rewrite:

- **States host industry; countries do the repeated arithmetic.** States still decide where industry is, the local wage, employment, Infrastructure Efficiency, land and resources, which method is in use, and where capital sits. Shared calculations such as valuing a method's inputs and outputs at market prices move up to the country, grouped by industry and method combination. Colonies on old methods stay distinct from the core on new ones. Slow-changing state modifiers are baked in ahead of time and recomputed only when something changes. The aim is speed, not fewer goods or industries.
- **Employment stays per state** and becomes the main calculation still done state by state.
- **Investment as opportunity money in return tiers.** Each sector advertises how much money it could absorb at what return: Exceptional (over 20%), Good (10–20%), Fair (5–10%) and Marginal (−5% to 5%). Money goes to the best tier first, and only the tier is stored. It's fine if advertised opportunity far exceeds the money available.
  - **Brownfield** (expanding an existing industry): the labour estimate is simply unemployment plus a small share of employment. Several industries may count the same workers, on purpose, and the simulation sorts it out. One expansion at a time per industry.
  - **Greenfield** (a first industry of its kind in a state): a cheap rough check comes first, within a search budget that's smaller for small countries. New establishments are limited to about one per sector per month, and each unfinished one lowers the tier of further ones, so a new industry spreads gradually.
  - **Hard caps** for finite sectors: deposits, arable land, forests, port sites. A gold mine at 40% ROI with $3M of room offers only $3M.
- **Capital pools by investor type,** with no money held per industry:
  - *Landowner, or "particular", capital* can only fund agriculture, plantations, livestock, forestry and ports. A rich farming economy shouldn't bootstrap modern factories on its own.
  - *Capitalist, or "general", capital* funds factories, mining, railways and ports.
  - As the non-agricultural share of GDP rises, landowner capital moves into the general pool.
  - **Capital-market development** decides whether money stays local (money made in Illinois stays in Illinois) or can fund projects anywhere in the country. This is meant to be a central difference between economies such as Qing China, Meiji Japan and Britain.
- **Attractiveness becomes the return tier.** There won't be a second profitability formula.
- **Other planned work:** banking and inflation; finishing the employment overhaul (employment changes, pop-type changes, possibly merging into "working" and "middle" classes, education, qualifications); base prices that shift by era so early methods age out; and adding technology bonuses back to methods.

## 9. Design principles

These are Strat's, stated or shown in past decisions:
1. **Simulate causes, not outcomes.** Keep the causal chain (jobs, wages, prices, profit, capital) and let results emerge.
2. **Don't predict feedback the simulation will resolve by itself.** No solvers, no forecasting of future prices, no allocation step so that two industries can't count the same workers. Let the market correct it next month.
3. **Simple beats clever.** Fewer moving parts. Set a value directly rather than adding a tracking variable and a lookup table. Other modders have to be able to read it.
4. **Performance is a design constraint, not an afterthought** (see section 10).
5. **History is a guide; game balance wins.** Historical figures set scale and shape, not exact targets. When history and balance disagree, check who else uses the value and how a player could exploit it. Round numbers and leave margin.
6. **Approximate but stable signals beat precise but noisy ones.**
7. **Uneven development is the point.** Colonies running old methods, capital stuck in place, infrastructure gaps, landed against industrial wealth.
8. **Recompute and advance stay separate.** Derived values are recomputed from scratch each month; only a few explicit steps move state forward in time. That keeps the tick safe to reorder and test.
9. **Content goes through the API.** Events and focuses use the documented effects, never the internals.

## 10. Limits of HOI4 scripting that shape what's feasible

- **Speed.** All of it runs in an interpreted script. A world tick takes seconds and the weekly trade tick alone takes about 3 seconds. Anything that loops over states × industries × goods every month is expensive, and a new idea's per-tick cost is often what decides it.
- **Save size.** Every stored variable persists in the save, and saves already take minutes to load. An idea that adds a variable per industry per state per good is costly even if it's cheap to compute.
- **Numbers.** Fixed-point decimals with limited precision. Multiplication and division truncate, and very large products overflow (around a billion). There are no real floats or big integers.
- **No engine help.** Every economic decision the AI makes (hiring, trade, budget, investment, upgrades) has to be scripted. If a mechanic needs a decision, someone has to write the AI for it.
- **Silent failures.** A broken formula usually just reads 0, with no error. Complex formulas are risky and need testing in the simulator.
- **A coarse clock.** Monthly ticks, weekly trade. Everything reacts with at least a month's delay.
- **A limited UI.** Anything the player sees has to be precomputed into variables, and the screens are hand-built.
- **Players and multiplayer.** The player can exploit anything they control. Mechanics have to be fair between player and AI, and robust in multiplayer.

## 11. How to pitch an idea

A good proposal for this economy:
- names the problem it solves and the loop it hooks into (section 4);
- traces the causal chain, including second-order effects on prices, wages and employment;
- says what new state it needs to store and how often it runs, and prefers existing levers (modifiers, method data, wages, prices, budget lines) over new variables;
- explains how AI countries will use it, not just players;
- lists its tuning knobs and what values are safe;
- says whether it depends on a system that's off or only planned (investment, banking, companies);
- avoids global optimisation, forecasting and per-tick searches over everything.

If you're unsure whether something exists or is switched on, say so and ask, rather than assuming.

## 12. Glossary

| Term | Meaning |
|---|---|
| Size / level | How big one industry in one state is |
| PM | Production method: the recipe an industry uses |
| AM | Automation method: a labour-saving layer on top of the PM |
| Wrk / Mid | Laborer and worker job shares in method data |
| Employment target | An industry's hiring decision, 10–100% of its jobs |
| Profitability | Profit ÷ revenue (the margin) |
| Productivity | Value added per worker; used for comparisons and AI choices |
| RGO | Resource extraction industry, sized by worked deposits |
| Subsistence | Peasant farming on leftover arable land, mostly outside the market |
| Base wage | A state's reference wage. Pop types earn multiples of it |
| SoL | Standard of living, 1–200. It sets the size and contents of a pop's basket |
| Consumer confidence | A pop's willingness to spend rather than save |
| Incentives | The long-term property-rights mood that drives investment appetite |
| Market leader | The country whose market others belong to. It sets prices for all of them |
| Infrastructure Efficiency | A state's transport supply against demand. It scales throughput |
| IO | Investment opportunity |
| Investment fund | A country's pool of owners' money for investment |
| Debt level | Debt against annual GDP. About 200% triggers bankruptcy |
| Money scale | 1,000 units = £1M, per month |
