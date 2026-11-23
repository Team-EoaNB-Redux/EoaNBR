# EoaNBR Economy: How It Works

A plain-English briefing for an AI assistant (ChatGPT, Claude or similar) that can't see the code. It explains what the economy simulates, how the parts affect each other, what is switched on, and what limits any new idea has to live within. It describes behaviour, not syntax.

Last checked against the code: 2026-11-17 (M11).

## How to use this briefing

- You're helping design the economy of a Hearts of Iron IV mod. The person prompting you is usually Strat, the economy lead, who writes the script. Strat wants design thinking: mechanisms, trade-offs, failure modes, tuning levers. Don't write code unless asked.
- Each system below is marked **[LIVE]**, **[PARTIAL]**, **[OFF]** or **[PLANNED]**. Don't assume a system affects play because it's described here.
- Before you propose anything, read sections 9 to 11 (design principles, scripting limits, how to pitch). Most ideas that sound good fail one of those.
- Numbers given here are rough anchors for scale. Exact values live in a spreadsheet and change often.

## 1. What the game is

End of a New Beginning Redux (EoaNBR) is a total-conversion mod for Hearts of Iron IV (HOI4). It starts in 1857 and can run to the modern day. HOI4's own economy is little more than civilian and military factories, so the mod builds a full economic simulation in HOI4's scripting language: pops, industries, goods, prices, wages, trade, budgets, debt and investment. The spirit is close to Victoria, but it is much simpler inside, because HOI4 script is slow and every stored number makes save games bigger. Saves already take 5 to 10 minutes to load.

The economy ticks once a month for every country. Trade ticks weekly. Players act on it through a budget screen (tax and spending sliders), trade settings, building and upgrading industries, laws and national ideas, and events and focus trees. Content reaches the economy through modifiers and a set of documented effects such as "add treasury", "add debt", "add industries" and "construct industries".

## 2. The whole system in one paragraph

Every state has a population split into five classes, and a set of industries. Industries hire pops, turn input goods into output goods with a production method, sell the output at the market price, pay wages, and pass profit to their owners. Pops spend toward a target set by their income and consumer confidence, on a basket of goods that grows with their wealth. They hold no savings, and the classes that can borrow run into debt when they overspend. All production and consumption in a country and its subjects is pooled into one market, with one price per good, and each price moves with the ratio of demand to supply. Markets trade with each other weekly through a global market. Governments tax income, spending, dividends and trade, and spend on administration, the military, research, construction and subsidies. Deficits become debt, and too much debt ends in bankruptcy. Each state's wage floats with how tight its labour market is. The growth engine is investment (M09): retained profit and pops' investment build and upgrade industries where they pay best, and grow the sectors that are working near capacity.

## 3. The building blocks

### States and countries [LIVE]
- **States** hold everything physical: population, industries, arable land, resource deposits, infrastructure and the local wage.
- **Countries** hold technology, laws, modifiers, the budget, the treasury and debt. A country runs the economy of the states it *controls*, so occupation moves a state's economy to the occupier.
- Tribal countries are left out of the economy.
- Countries are processed in order of industrial power, biggest first. That matters wherever there is a shared pool or first pick, such as investment.

### Pops [LIVE]
Population comes from HOI4's state population, counted in thousands. A fixed 35% of everyone is workforce; the rest are dependants. Each class in each state tracks its workforce, employment, earnings, spending, debt, wealth and consumer confidence. Unemployment is a class's workforce minus its employed, not a separate pop.

| Class | Role | Pay relative to the state's base wage |
|---|---|---|
| Slaves | Fill working-class jobs before free workers, unpaid. No income and no needs | — |
| Peasants | Subsistence farmers | Share of subsistence output |
| Working class | Manual and industrial jobs (the sheet's Wrk share) | 2× |
| Middle class | Skilled and professional jobs (the sheet's Mid share), and bureaucratic jobs | 4× |
| Upper class | Owns every industry and lives on dividends and the 20% subsistence rent. Also fills senior government jobs in the capital | 10× for those jobs only |

- **Owners' numbers follow what they own:** each industry holds owner places for the upper class, about 2% of its jobs.
- **Slaves** exist only where history sets a starting share (for now, test shares in three US southern states). They're capped at the state's share of marginalised cultures, and freed into the working class wherever the controller's laws ban slavery. Nobody is newly enslaved.
- **Bureaucratic jobs** come from population: 1.5 per 1,000 people in core states, half that elsewhere, plus 5% more in the capital for the upper class. The government pays them. They compete with private jobs for the middle class, and administrative capacity is the share filled.
- **Active manpower:** HOI4's fielded and training manpower is taken out of the peasants and the working class, by state population, and returned when soldiers demobilise. Their pay and upkeep stay on the military budget lines.
- **Qualifications** limit moves up into the middle and upper classes. They're one stock per state (see "Pops changing class").

### Goods [LIVE]
There are 32 goods. Raw goods are food, luxuries, wood, fiber, iron, coal, copper, valuables, oil, rubber, aluminum, tungsten, chromium, titanium, silicon and rare earths. Made goods are steel, tools, machinery, chemicals, plastics, composites, electronics, portable power, consumer goods, textiles, vehicles, appliances, computers, electricity, services and entertainment.

- Each good has a fixed base price, for example food 2, wood 2, coal 2, iron 3, textiles 4, consumer goods 5, steel 8, machinery 20, valuables 25.
- Goods are also HOI4's strategic resources. The economy tells HOI4 how much of each good a country has, so military factories making equipment draw on the same steel and iron, and military use counts as market demand.
- Transport and shipping capacity are services, not tradeable goods (see Infrastructure Efficiency).

### Industries [LIVE]
An industry is one building type in one state, with a **size** (a number of levels). Kinds:
- **Resource extraction (RGOs):** mining, forestry and some gathered farm goods: wood, coal, iron, copper, valuables, oil, rubber, aluminum, tungsten, chromium, titanium, silicon, rare earths, chemicals (nitrates, guano, sulphur), food, fiber and luxuries. Size is the part of the state's known deposit that is being worked. Manufactured goods have only factories (M06).
- **Farms and plantations:** crop farms, rice paddies, livestock ranches, and cotton, luxuries and rubber plantations. They use arable land, need their crop to grow in the state, and yield in proportion to its land quality.
- **Factories:** steel foundry, mechanical works, tooling workshop, textile mill, consumer goods factory, chemical plant, and later electronics, vehicles, computers, synthetic fuels and more.
- **Urban:** urban centre (services), power plant, entertainment hub.
- **Transport:** railways and ports. They make transport capacity, not goods.
- **Subsistence farms:** automatic. They fill all arable land nobody else uses and are worked by peasants.
- HOI4's civilian factories, military factories and dockyards **aren't industries** since M08: they're offmap, and follow the Manufacturing Base (section 5).

Industries unlock with technology. Every industry runs one production method and one automation method.

### Production methods (PMs) and automation methods (AMs) [LIVE]
- A **PM** is a recipe. Per thousand base workers it sets how much the industry makes, which inputs it needs, how the jobs split between the working and middle classes, how much transport it uses, and what it costs to build and how long that takes. PMs come in four eras: 1857, 1900, 1950 and 2000.
- An **AM** is a second layer on top: steam engines, electrification, assembly lines, robots and so on. AMs mainly cut labour and add inputs such as machinery.
- Technology unlocks PMs and AMs. New buildings start on the latest unlocked method. Existing buildings only change method by retooling, which costs goods and time. Investment retools them when the newer method pays (M09).
- Every PM number is generated from Strat's "EoaNBR Economy" spreadsheet by a script. The sheet is where balancing happens.
- Technology bonuses to individual PMs were stripped out in the October 2026 rework and haven't been added back.

### Land and resources [LIVE]
- **Arable land** (M05): each state has some, set in history. Where history doesn't set it, it falls back to the workforce / 15 + 1 until every state's history does. Commercial farms take it up, and whatever is left becomes subsistence farming.
- **Land quality** (M05): a number per state, 1 unless history sets it. It scales the land's carrying capacity and the output of every commercial farm in the state.
- **Crop eligibility** (M05): one yes or no per farm per state (`crop_eligible@<farm>`). Crop farms and livestock ranches grow everywhere unless history forbids them. Rice paddies and the cotton, luxuries and rubber plantations grow only where history allows them. Farms can't be built where their crop doesn't grow. No history sets eligibility or land quality yet, so the uncommon crops can't be built anywhere.
- **Subsistence** (M05): the land left has a **carrying capacity** = land × land quality × subsistence yield technology × 10 thousand peasants per unit. Peasants up to it make the full yield, and those past it farm marginal land at half the yield, so nobody is stranded without work. Technology raises the capacity, never the yield, while ideas and laws (`subsistence_farm_output_factor`) scale the yield. Infrastructure doesn't matter. The upper class takes 20% of the output as rent (`global.subsistence_rent_share`). Commercial farms pay no rent.
- **Deposits** (M06) are state data, set in history per good: *potential* (`potential_deposits@`, not found yet), *known* (`known_deposits@`, found, worked or not) and *worked*, which is the RGO's size. An RGO can't be bigger than its known deposit, and building one opens up known deposits nobody works yet. Nothing depletes. **Deposit quality** (`deposit_quality@`, 1 unless history sets it) scales the RGO's output from the same inputs and workers, so an RGO makes size × utilisation × its methods' productivity × quality × the infrastructure effect. HOI4's state resources play no part: the army gets its goods from the economy through `resource_trade`.
- **Prospecting** (M06) finds only what history put there. The state screen's Prospect button starts a government-paid search that resolves the next month: a normal find moves 10–30% of the remaining potential into known deposits (times prospecting ability), and a major find, rarer as more of the deposit is found, moves 50–100% and tells the player. Investors prospect too from M09.

### Markets and prices [LIVE]
- Every independent country leads its own market. Subjects join their overlord's market, and other countries can be placed in another's market, like a customs union.
- There is **one price per good per market.** Production and consumption from every state of every member are pooled.
- **Target price:** base price × (demand ÷ supply)², held between a quarter of base and four times base. A 10% shortage raises it about 21%, and a large shortage pins it at 4×. Valuables are fixed at twice base, money-like.
- **The actual price moves toward the target gradually,** once a month at the start of the tick, before anyone is paid. Each month it closes a share of the gap: 30% for a small gap, 20 points more for every 100% of gap, and at most 70%. A gap under 2% doesn't move it. The gap counts a doubling and a halving the same. A 4× shortage therefore lifts the price about 3.1× in its first month. An ordinary 10% gap halves in about two months and is inside the dead band after five. The four values are globals in `resources_global_var_setup`. At startup, and for a new country, prices start at their targets.
- Revenue, wages, pop spending, GDP, trade income and tariffs all use the actual price. The trade AI uses the target (see Trade).
- Supply is production plus imports. Demand is pops' needs, industry inputs, materials for construction and retooling, military demand (unit upkeep, and a tenth of a good for each resource military production uses, M08), and exports.
- The target is recomputed weekly as trade changes, and monthly as production and consumption change.

### Trade [LIVE]
- Each market sets a route per good: an amount to import or export, run weekly.
- All markets together form a **global market** with a world price per good, priced by the same rule over world supply and demand. Each market leader sees the world without the countries it can't trade with. The world price also has a weekly target and an actual price that moves monthly, by the same curve.
- Imports add to a market's supply and exports add to its demand, which pulls local prices toward world prices.
- Trade is limited by partners (you can't import more than others offer) and by shipping capacity from ports and convoys. If shipping is overloaded, all trade scales down.
- **The shipping price** follows use (M07): it's the market's shipping usage (use over capacity), between 0.25 and 2, times a base price of 2. At a base of 1 ports lost money even at full usage, so they shrank, and a market that ran short of shipping had all its trade scaled down. Traders pay it per unit of shipping they use, and ports are paid it per unit of capacity. It's set monthly, from the last weekly trade.
- Trade profit is the gap between local and world price, minus tariffs and shipping cost.
- An automatic trade AI opens routes where trade profit per trade job is well above average earnings, and closes unprofitable ones. It doesn't nudge volumes: it solves for the volume that brings the market's target price to the world price plus costs. It judges routes at target prices, so trade answers a shortage within the week, while the money a route makes is counted at actual prices. A market with no production of a good but some need for it, or the reverse, keeps a 1-unit minimum route. National ideas such as Closed Economy shut trade off.

### Infrastructure Efficiency [LIVE, untuned]
Infrastructure Efficiency replaced an older system, in which transport was a priced good, in October 2026.
- Each state has **transport supply** and **transport demand**. Supply is a baseline from population and road technology, plus railways, plus part of port capacity. Demand comes from each industry's method.
- **Supply from population is capped** (M07) at 40, which roads don't raise: roads only carry so much freight, so huge states, China's above all, can't industrialise on population alone. London, at 34, sits under it. Two modifiers raise the cap, an absolute one and then a relative one, and nothing grants them yet.
- Their ratio sets the state's **Infrastructure Efficiency.** A shortage cuts throughput, down to a floor of 25%. Spare capacity gives a small bonus, up to +20%.
- It scales inputs and outputs, never jobs. Poor infrastructure makes workers less productive rather than unemployed, which suits poor, labour-heavy economies.
- Sectors depend on it to different degrees: farms 30%, resource extraction 60%, factories 100%, urban 50%. Subsistence doesn't depend on it at all.
- Railways and ports earn a fee per unit of transport, which is higher when the state is congested. Nobody pays the fee: the money appears and counts toward GDP (Q31). Ports also earn the shipping price on their shipping capacity. Railways and ports are national sectors like any other, with target utilisation.

## 4. The monthly loop

First, currency-market changes settle and every country gets its GDP share of base money. Every market leader moves its actual prices (market and world) toward the targets the last weekly tick set, and copies them to its members and their states. It then works out the market's PM/AM cache at the new prices (M04): what each sector in use makes, and what each method's inputs and construction cost. Then the market's investment headroom: how much more of each good it can take before the price falls below base (M10).

Banks then move reserves toward their confidence-based targets and fix the month's lending rates. Each country settles in rank order:

1. Last month's net budget goes into the treasury. AI countries adjust their budget, and the spending sliders' bonuses update.
2. Technology unlocks and their modifiers refresh. Each state's bureaucratic jobs and its share of active manpower are set.
3. Each sector's target utilisation steps toward what last month's margin calls for (M04). Companies lose holdings in states their country no longer owns, and pause, or are liquidated, when their debt is too high (M10). Last month's investment opportunities are cleared, sectors over their debt limit pause their construction, and the country picks the sectors that will look for a new state (M09).
4. For each state the country controls:
   1. Construction and retooling are paid from reserves, cash and available bank credit before they progress, including the final month. An unaffordable project pauses and buys no goods. Finished projects add size.
   2. Prospecting searches resolve.
   3. Pops settle last month's finances: overspending becomes debt for the classes that borrow, and wealth moves toward the level where spending meets the target. Population grows, slaves above their cap are freed, soldiers are drawn or returned, qualifications are gained and lost, and peasants and the working class move between farming and industry.
   4. The state's base wage moves according to last month's labour market.
   5. Each industry's trailing margin moves toward last month's. A building that keeps losing money shrinks.
   6. Each industry's investment opportunity for the month, if it has one, this state's place as a new home for the searching sectors (M09), and the country's best seed for a new company (M10).
   7. Pops move between the working, middle and upper classes to fit the jobs on offer, within their qualifications.
   8. Everything is recomputed: arable land and subsistence, jobs and employment (bureaucratic jobs included), production and each industry's finances, the upper class's dividends from last month's sector accounts, then each class's earnings, needs, taxes, confidence and targets.
5. The country works out the goods its industries and pops make and use, by sector and method rather than state by state, which its market reads until next month. Then each sector's national accounts: this month's revenue, costs and profit, then each company's accounts (M10), and the generic owner's profit tax, retained share and dividends, from the sector's less its companies' (M04). Then HOI4's offmap factories move toward last month's contract targets, and the Manufacturing Base and its targets are recomputed (M08).
6. Investment (M09): retained earnings, pops' investment and the government's lines come in, construction bills are paid, companies' earnings, losses and bills go through their treasuries and debt, and the month's opportunities are funded, best tier first, companies first in each tier, with the month's new company if there is one. What's funded starts at once.
7. Market leaders recompute supply, demand and target prices for their whole market from the members' totals, the market screen's statistics, and GDP.
8. The budget is recomputed: taxes, spending, debt and interest.
9. Statistics and graphs. The boom and recession check would run here from the second year, but it's switched off during the rework.

After all countries have settled, banks retain interest received, pay dividends when sufficiently capitalised, and repay emergency loans. This keeps foreign interest independent of country processing order. GDP money shares refresh.

Weekly: markets recompute supply, demand and target prices with current trade and military demand, from each member's goods totals of its last monthly tick (industries and pops only change monthly), the global market updates, the trade AI adjusts routes, and trade flows recompute. Actual prices don't change during the month. Trade stays weekly so that HOI4's military factories get their resources within a week.

**The lags matter.** Wages react to last month's labour market, target utilisation to last month's margins, investment to last month's accounts, and pops act on last month's earnings. These one-month delays are a big part of why the economy can swing (see section 6).

## 5. How the pieces work

### Production and employment [LIVE]
- An industry's potential output comes from its size and method. Actual output depends on how fully it's staffed, Infrastructure Efficiency, economy of scale (bigger industries in one state get up to +20%), and national and sector modifiers.
- Partial staffing is slightly more productive per worker: a half-staffed plant makes about 59% of its full output.
- **Target utilisation (M04)** is the hiring decision, made nationally for each sector: the share of its jobs on offer, from 10% to 100%. Every sector starts at 80%.
  - National margin above 10%: it rises, by 1 point plus half a point per percentage point of margin beyond 10%.
  - Margin below 0: it falls the same way.
  - In between: it holds steady.
  - It moves at most 5 points a month. The old per-industry targets could jump 20 points.
- **Local shift:** each state-industry works at its sector's target, shifted up to 5 points by how its own trailing margin compares with the national margin.
- Jobs are filled by pops of the matching class. If a state is short of a class, every industry there, and the bureaucracy, is short-staffed in proportion. Slaves take working-class jobs first.

### Profit and where the money goes [LIVE]
- **Revenue:** output sold at the market price. Railways and ports get their transport fee instead. A state-industry stores only what the accounts add up (revenue, inputs, payroll, maintenance) and a trailing margin. The industry screens work out the rest.
- **Costs:** wages (base wage × the class's multiple × employees, with nothing paid for slaves), inputs bought at market price, and **maintenance**. Maintenance is a fixed upkeep of about 3% of build cost a year, paid even on idle capacity.
- **Sectors keep the accounts (M04).** Every industry token except subsistence farms is a national sector. Each month a country adds up each sector's revenue, inputs, payroll and maintenance from its states into one record (`sector_*@<sector>`), with its operating profit and margin. The record also holds what a national screen shows (Q91): jobs and employment per class, transport, construction and retooling under way, reserves, and the method mix.
- **The generic owner** is the sector less its companies (M10): its size and profit are the sector's less what the country's companies hold and earn.
- **Profit** pays corporate tax when it's positive, at the country's rate. The sector keeps `global.sector_retained_share` (30%) of what's left as **retained earnings**, scaled by investment appetite from incentives, and pays the rest as dividends. Retained earnings repay the sector's debt, a share goes to the general investment pool, and the rest is its capital (M09). Employees get no bonuses: wages are their share.
- **Loss** uses sector capital, then available bank credit up to its collateral limit (M11). Owners cover a refused operating loss through negative dividends. Interest is in sector accounts; companies have their own interest expense.
- **Dividends** are paid by size: each state's upper class gets the generic owner's dividend per size × the generic size it owns there, a month later. Subsistence rent (20% of subsistence output) goes to its own state's upper class directly.
- **Ownership:** the upper class owns every industry's generic share, its size less what the controller's companies hold. Companies can own slices of an industry (see below).
- **The PM/AM cache (M04).** Each market works out, once per price change, the value of one bundle of each sector's goods and what each method's inputs and construction cost. Each country applies its own sector and method modifiers, and each state its local factors. The industry screens and getters read the same values.

### Manufacturing Base and HOI4 factories [LIVE, M08]
- **The Manufacturing Base** is the total size of a country's manufacturing industries (the Factories category), plus what focuses, decisions and events have added. Idle plants count: the state contracts factories that exist.
- **Contracts:** the state contracts a share of the base, set by its economic mobilisation law: 5% under either isolation law, 10% in a civilian economy, then 20%, 30% and 40%, up to 50% under total mobilisation. The AI follows its law like the player. Idle factories cost nothing.
- **The split:** the contracted factories divide 20% civilian, 50% military and 30% naval to start. Only the player changes it, in a popup opened from the production screen. A country without a coast gives the naval share to the military.
- **HOI4's factories** are those contracts, held offmap. The contracts are targets, and the factories move toward them gradually, so a law change can't swing a war overnight: each month civilian and military factories close a tenth of the gap, dockyards a twenty-fifth, and cuts a quarter, by at least one factory. A switch to War Economy gets half way in about 7 months. Startup puts the factories at their targets. Nobody can build a factory on the map, and history has none.
- **Cost:** each contracted factory in use costs £0.1M a month, a mandatory military budget line. The money goes to no one, since contracts don't take output from the factories yet; the planned option (b) would have the state buy that output.
- **Content** that used to add or remove a factory adds or removes ten factories' worth of base, so at the civilian economy's share it's still about one factory in use. It moves the targets, and the factory arrives at the usual pace.
- **Military resources:** a production-screen resource is a tenth of a good. Equipment costs ten times the resources it did (ships twice), so land equipment needs the same goods and ships a fifth. Only part of a country's resources reach the production screen: the economic mobilisation law's share, from 10% (undisturbed isolation) to 80% (total mobilisation), shown above the resource grid. Military production buys a tenth of a good for each resource it uses, at the market price.

### Wages [LIVE]
- Each state has one **base wage**, and each class earns a fixed multiple of it.
- It floats monthly on the private labour market: private working- and middle-class jobs against the slave, working-class and middle-class workforce. Slaves count as supply, so plentiful slaves hold wages down. Bureaucrats are left out, since the government pays the going wage. If jobs exceed workforce (more than 99% utilisation), wages rise. Below 95% they fall, about five times more slowly, so wages are sticky downward. Between those bands they hold. The change is capped at ±2% a month.
- There's a floor: the working class never earns less than subsistence farming would give it.
- It's seeded at game start from history. A state's own value wins, then the country's, then a default for its technology tier, which rises from about 1.2 for tribes to about 4 for early mechanisation.
- Wages are a cost for industry and income for pops. A tight labour market raises wages, which squeezes margins, which slows hiring.

### Pops: income, spending, wealth and debt [LIVE]
Built in M03. Pops hold no savings.
- **Income** is gross: a small universal base income, plus wages (or the subsistence share for peasants), and for the upper class its dividends, which include the subsistence rent. Slaves get nothing. Income tax is charged on all of it.
- **Taxes** are part of what a class spends: income tax by bracket (lower, middle or upper, depending on a class's average earnings against the national average), and sales tax on what it spends on goods. Corporate tax is paid by the sectors before dividends.
- **Investment:** the middle and upper classes put a share of their after-tax income into the investment pool (`middle_class_investment_contribution_factor`, base 10%, and `upper_class_investment_contribution_factor`, base 20%, at most 80%), scaled by incentives. It goes into the general investment pool (M09).
- **Wealth,** from 1 to 200, sets each class's basket of goods (it was called standard of living until M03). The wealth-1 basket is worth `global.pops_base_spending` per thousand pops a month at base prices: 0.1 since M01, cut from 0.3, which had pinned food at its cap. Food comes first. Textiles, consumer goods and services follow, then luxuries from around wealth 21, and later electricity, appliances, vehicles and computers. The basket's value roughly doubles every 10 levels. It's defined in base-price value and bought at market price, so expensive goods squeeze pops. A separate SoL, worked out from wealth plus things like pollution, comes later.
- **Technology gates needs.** If a good isn't available yet, such as electricity, an older substitute fills the need. A state's electrification shifts the basket over time, although nothing sets electrification yet.
- **Target spending** = (income − investment) × consumer confidence. Spending is goods, taxes and debt repayments. Each month, wealth moves toward the level where spending meets the target: progress builds by `global.pops_wealth_speed` (6) × the gap ÷ goods spending, and each whole point moves wealth one level.
- **Debt:** for the working, middle and upper classes, spending above income after investment becomes debt (`pops_debt@<class>` on the state). They repay 4% of it a year as part of their spending, and half of any surplus repays more. The rest of a surplus disappears. Since M11 the owner's bank charges interest, approves the spending it can finance, and holds the country total. Refused credit cuts the goods purchased and their sales tax. Debt above 24 months of after-tax income after an income collapse, or the debt of an empty class, is written off against bank capital. Peasants and slaves don't borrow, so a peasant's target is capped at its income.
- **Consumer confidence,** from 0.2 to 2, starts from national modifiers (100 at peace, plus a stability bonus). Debt repayments lower it by their share of income, and faster once that share passes what pops tolerate (10% plus a little from banking and consumer confidence). Above 1, the classes that borrow spend more than they earn, and their debt grows until its repayments take half of confidence's excess over 1, as a share of income. At ENG's 108.7 that's about 4% of income, from a debt of about 13 months' income, which takes decades to reach.
- **Peasants** live mostly off their own farms. Only about 20% of subsistence output reaches the market, and only about 20% of their needs show up as market demand. They pay for all of their basket out of their subsistence income: the 20% they buy at market price, and what they grow at base price, the same value their income gives it (M05).

### Pops changing class [LIVE]
- Each month, pops move toward the jobs on offer: a class short of workers takes them, in proportion, from classes with too many. Total population never changes in this step. Slaves never move.
- If the working and middle classes are short of hands, peasants join the working class, at a rate limited by arable land and never more than the shortfall. If the working class has too many and wages are low compared with farming, its surplus goes back to the land.
- **Qualifications** are one stock per state, in thousands of qualified people. The middle class needs 1 per head and the upper class 2, and a move up is scaled down to what's free. Moving down loses nothing.
  - **Gains:** literacy, schooling and education (state percentages, by default 20%, 10% and 0.5%; Britain's history sets 60%, 40% and 2%), wealth above level 10, and the share of the workforce already middle or upper class.
  - **Cuts:** half for marginalised cultures, a tenth for cultures that are neither primary nor promoted, and serfdom laws can cut peasants' gains, all through modifiers. Slaves gain nothing.
  - **Losses:** 0.5% of the stock a month.
  - **Start:** the stock starts at exactly what the starting classes need, so growing the middle class always waits on new qualifications. It's meant as a major barrier to industrialisation.

### Government budget [LIVE]
- **Revenue:** the taxes above, corporate tax on the sectors' positive profit, import and export tariffs and trade income. Effective rates are scaled by tax efficiency, and tariffs by bureaucratic efficiency. A short bureaucracy collects less income, sales and corporate tax: from half the rate with no bureaucrats, rising to the full rate at full administrative capacity.
- **Spending:** administration (the bureaucrats' pay, plus per-head and per-GDP costs), military payroll (manpower × average earnings), factory contracts (M08), military procurement (goods for equipment), research, construction (builds the government pays for), projects, subsidies, order and intelligence, and social spending.
- **Sliders have political effects.** Taxes cost political power, stability, war support and *incentives*, a property-rights mood that drives investment appetite. Spending buys HOI4 bonuses: military spending improves army organisation and morale, research spending speeds research, and procurement raises production efficiency and lowers equipment cost.
- **Debt:** a negative treasury becomes debt, domestic or foreign. Interest starts around 8%, is cheaper for great and secondary powers, and rises when the lending pool is scarce. The *debt level* tracks debt against annual GDP. Passing roughly 200% fires **bankruptcy**: debt is wiped and spending is cut, but stability takes a heavy hit. Lower stability means lower productivity and consumer confidence, so pops spend less.
- **Debt switch:** while the rework runs, `global.eco_debt_enabled = 0` skips every starting debt, sets both interest rates to 0 and stops bankruptcy. Deficits still borrow up to the lending cap (24 months of GDP). Past it, the treasury goes negative with no consequence. M14 turns the switch back on.
- AI countries repay debt when they can and raise taxes when they're in deficit.

### GDP [LIVE]
- A state's GDP is value added: each industry's revenue minus the goods it bought (M04). That counts subsistence food peasants eat themselves at base price and transport fees. Government buildings' output counted until M08 removed them. A market's GDP, added up when its leader ticks, values each member's last month at that month's prices.
- **Money scale:** 1,000 money units = £1 million, and every flow is per month. The historical UK national income in 1857 was roughly £665M a year, which would be about 55K a month. That's the reference scale for the rebuild, not a value the game currently hits.
- GDP drives debt ratios, administration cost, each country's share of market trade, and the statistics screens.

### Investment [LIVE, M09]
All of it is in `_economy_investment.txt`, whose header explains the flow.

**Where the money comes from:**
- **Sector capital** (`sector_capital@`) is what each sector keeps of its profit, so profitable textiles build more textiles. Retained earnings repay the sector's debt first. Then `sector_capital_mobility` of them (20% before laws, for the financial-system laws to set) goes to the general pool.
- **The general pool** (`investment_fund`) also takes the middle and upper classes' investment and the government's development fund. A sector new to a country can only be built with it, or with the government's money. Bank credit is live in M11; foreign capital follows the later currency and company milestones.
- **The infrastructure fund** is the government's second line. It builds railways where states are short of transport and ports on the coast while the market is short of shipping, whatever they earn. Both government lines are a share of GDP that nothing sets until the Budget tab gets its controls.

**Opportunities**, one per state-industry a month, and none while it's building or retooling:
- **More of an existing plant,** while its sector's target utilisation is above 80%: up to size × (utilisation ÷ 80% − 1), within its known deposits, free farmland and the state's free labour (unemployed, peasants and 3% of the employed).
- **A first plant in a new state** for each sector that looks for one. That's sectors that want to grow, and, when the general pool can afford it, the best sectors new to the country. The search is shorter for small countries, and each sector opens at most one new establishment a month.
- **An upgrade** to the sector's newest PM or AM, priced as the plant would be against the plant as it is. A plant that could also expand offers whichever pays better.
- **Prospecting,** by an RGO that wants to grow but works all its known deposits.
- **Infrastructure,** from the infrastructure fund.

Each opportunity is ranked in an **ROI tier**, a year's operating profit over a level's full cost: Exceptional over 20%, Good 10–20%, Fair 5–10%, Marginal −5% to 5%, and anything lower is ignored. A sector's tiers show how much each can absorb, at capital cost.

**Funding**, best tier first:
- Upgrades and prospecting are funded whole.
- Expansions are funded **pro rata by sector**:
  - each sector's capital pays the investment cost (25%) of as much of its own as it can;
  - the general pool funds the same share of every sector's remainder, at full cost;
  - within a sector, the money builds whole projects in turn;
  - a project the money can only part-fund needs the sector's minimum: a full level in the month after the sector last started one, falling 0.1 a month to 0.1, so money waits and builds up instead of opening slivers that hold a plant for a whole build (Q126). Pool money a sector declines goes to the tier's other declined projects, and what's still left waits for next month.
- What's built belongs to the sector's local owners.

**Market headroom (M10, Q147, Q148):** expansions and new plants are cut to what the market can still take before a good's price falls below base: demand less supply, trade included, less what the construction under way anywhere in the market will make. It's worked out once a month on the market leader, each country's funding uses it up in rank order, and a sector that makes several goods gets the value-weighted mean of their headroom. Upgrades, prospecting, railways and ports aren't limited.

**Surplus capital (M10, Q150):** after the month's funding, a sector's capital above its reserve, the bills it still has to pay plus 10% of its plants' value, goes out as its dividends.

**Construction bills and debt:**
- The goods are bought over the build time, and their cost comes from the money the pool set aside, then the sector's capital, then available sector bank credit, with interest (M11). Payment comes before progress, including the final month; unaffordable work pauses.
- A sector whose debt passes half of its plants' value pauses its construction until retained earnings bring it down.

**Capacity decay:** a building whose trailing margin is below −5% loses 1% of its size a month, every owner alike (M10).

### Companies [LIVE, M10]
- **Slices:** companies own slices of state-industries by size: a size-14 mill might be 2 levels Company A, 4 levels Company B and 8 levels generic owner. The plant keeps one PM and AM and one workforce, but each company applies its own bonuses to its own slice, and the plant is its owners' slices recombined, as if each had its own copy of the mill sharing the workers. A company's slice earns its share of the plant's output and inputs at its bonuses, and pays its share of wages and maintenance by size.
- **Bonuses:** +10% throughput in a private or public company's primary industry, plus whatever history and content give it. A state-owned company gets no base bonus.
- **Accounts** are national: revenue, costs, profit, corporate tax, retained earnings and dividends. A company keeps the sectors' retained share (30%, scaled by incentives) in its treasury and pays the rest to the upper class of its headquarters state, or to the treasury if it's state-owned. A loss, and construction bills, come out of the treasury, then borrow from the bank within its credit and collateral limits (M11). Interest is a cost in the accounts. Its construction pauses above half its plants' value, or whenever it cannot pay the bill before progress.
- **Investment:** in each tier, before the sectors, each company funds the expansions, new plants and prospects in its own industry, in its own country, whoever holds the plant. What it builds becomes its holding. It pays a quarter up front, and the bills follow. An upgrade to a plant several owners share is paid by each, by size, and goes ahead only if all can pay.
- **Founding:** each month the country's best profitable plant (Good or Exceptional ROI, at least 2 levels of generic size, its ROI halved for each company already in that industry and divided by 1.2 for each company the country has) can incorporate, if its market has room for another level. The general pool puts in the new company's reserve, 10% of the value of its holding, and the new company, headquartered in that state, takes half the plant's generic share.
- **Surplus:** after each month's funding, a company pays out as dividends whatever its treasury holds above its reserve: the bills its construction still has to pay plus 10% of its asset value. Sector capital above the same reserve goes out as the sector's dividends. Nothing is paid out while in debt.
- **Changing hands:** a holding works for its company only while its country controls the state; otherwise it counts with the controller's generic owner. When its country loses the state, the holding passes to the new owner's generic owner, and a company left with nothing is liquidated.
- **Failure:** a company whose debt passes its plants' value, or whose operating bills cannot be financed, is insolvent. The player can bail it out, paying its debt down to half its plants' value, once in five years, or let it fail. The AI lets it fail. Its plants go to the generic owner, its construction stops, its debt is written off, and what's left in its treasury goes to the general pool.
- **At startup:** two test companies, Horrockses, Miller & Co. (half of Lancashire's textile mill) and Powell's Steam Coal (Wales's coal). Their holdings are state history data.
- Planned (M15–M17): shares and a stock market, reorganisation instead of liquidation, behaviour states, departments, R&D, mergers, and branches abroad.

### Banking and finance [LIVE, M11]
- **One bank per country** holds reserves, capital, performing loans, banking confidence and an annual lending rate. Borrower records remain on states, sectors, companies, the pool and government creditors; the bank re-sums them. Domestic government bonds remain separate.
- **Base money** is one nominal stock per market. Startup seeds 12 months of real GDP at price level 1, with no treasury grant. A country's GDP share, times its own banking confidence /100, is the target for bank reserves. Reserves recover by 10% of the gap each month, but a run drains 50% of the gap. There are no explicit deposits or pop savings.
- **Credit capacity** is the smaller of reserves / reserve requirement and capital / capital requirement. The reserve requirement defaults to 20%, capital to 8%. Existing loans and approved household spending consume capacity. The initial bank capital is two months of country GDP. These are provisional coefficients for M14 balancing, not historical estimates.
- **Interest** starts with a 4% policy rate, adds a 4-point lending spread and up to 2 points for scarcity. Sector and company interest is in their accounts; pops pay from income. Actual interest received adds to bank capital; half goes to the capital state's upper class as dividends if the capital requirement is covered. All banks close after every country settles, so a creditor processed before its debtor still receives the same payment.
- **Investment credit:** the general pool has its own debt and interest. After companies, retained capital and cash have funded a tier, it may borrow for Good or Exceptional opportunities whose ROI clears the lending rate. It repays unused advances immediately. Debt is limited to six months of pool contributions; 25% of monthly contributions services principal before fresh investment.
- **Defaults:** write-offs reduce performing loans and bank capital together. Companies liquidate through the existing insolvency process; sectors with debt above collateral restructure to half that collateral; a pool that loses contributions writes off debt above its limit; households default on debt above 24 months of after-tax income after an income collapse. These coefficients are provisional. Existing plants survive financial write-offs. Capital at or below zero triggers a banking crisis and stops new lending.
- **Foreign government loans** are assets of the creditor country's bank. They use that bank's lending rate plus the borrower's debt/GDP risk premium (2-10 points). Interest reaches the creditor once per month; bankruptcy writes principal off against its capital. National interest and bankruptcy still respect the rework's debt switch, currently off until M14.
- **Central-bank basics:** content can change the policy rate, mint base money, lend repayable emergency liquidity to a solvent bank, or recapitalise it from positive treasury cash. Minting is leader-only and gives the treasury the minted quantity / price level. Emergency lending creates base money without a treasury grant, and repayment retires it; it cannot repair insolvency. M13 adds player controls and law coefficients.
- **Market changes:** a member carries its GDP share of base money and physical valuables. A whole market brings its entire stock. Joining converts base money at the destination/source price-level ratio; leaving inherits the old price level. Each country keeps its own bank and loans. The price level remains 1 in ordinary play until M12 adds inflation.

### Projects [LIVE]
Projects are country-level works, such as work programmes, with a goods bill and a build speed. Each month a project buys as many goods as it can toward its bill, and when it finishes it fires an effect. Content uses them for reforms and public works.

### Economic cycle [built, OFF]
From the second year, every month, each state's GDP is compared with its 3-year average, weighted by size. If most of the economy is falling, the country enters a recession, depression or free fall. If most is prospering, it gets a boom. Players get events, the AI gets the national idea directly, and stability moves. M00 fixed the month counter it depended on, then put it behind `global.eco_cycle_enabled = 0` until M14. On the test bed it was driven by month-to-month GDP swings and added noise to every comparison: in the simulator, 14 of 130 countries were in a downturn or recession by month 60, and Britain's consumer confidence flipped by 5 points.

## 6. Feedback loops to know

- **Price-employment swing (destabilising, much reduced by M01).** A shortage squares into a price spike, the producers' margins jump, they hire up to 20 points in one month, supply overshoots, the price crashes, and they fire. Revenue uses last month's price and hiring uses last month's profit, so the delays amplify the swing. On the test bed, most of the swing turned out to come from the trade AI toggling routes on and off every other week, which M01 fixed. Gradual prices damp the rest. Over 60 simulated months, ENG's GDP now settles instead of swinging ±5% a month, although on the stripped map many goods also sit still at their price cap. M04's target utilisation moves at most 5 points a month, where the old per-industry targets jumped up to 20: on the test bed the largest monthly swing in London's consumer goods output fell from 11 to 4 points.
- **Wage-labour loop (stabilising).** Tight labour raises wages, which squeezes margins, which slows hiring. Wages are sticky downward, so a slump shows up as unemployment first, and wages fall later.
- **Bankruptcy spiral.** Debt grows faster than GDP, bankruptcy follows, stability crashes, which cuts productivity and confidence, pops cut their spending, real incomes fall, and GDP falls further.
- **Infrastructure loop.** Growth raises transport demand, Infrastructure Efficiency falls, and railways and ports earn more. Where they still lose money, the government's infrastructure line builds them where states are short.
- **Investment loop (stabilising, M09).** A sector working above 80% of its capacity, at a good return, builds more. The new capacity lowers its price and margins, its utilisation falls, and it stops building. Sector debt can make a sector overbuild for a while, until its borrowing limit pauses it. Since M10, building also stops once the market's headroom is used up, before the new capacity pushes the price below base.

## 7. Current state (November 2026)

- **The map has been stripped back to subsistence farming,** on purpose. Every state's industries and deposits are commented out of the history files (the old deposits sit as comments in each state's `resources` block), leaving only subsistence. HOI4's own factories went too in M08: they're offmap and follow the Manufacturing Base, which on the stripped map gives almost no country a factory. On the old map, Britain went bankrupt in its first July, in both the game and the simulator. Historical targets for Britain and India are written as comments in the history files.
- **The plan, decided November 2026: redesign first, balance last.** The economy is being rebuilt to a new design (section 8) in a series of milestones. Only after that will the 1857 map be rebuilt sector by sector so world supply and demand start roughly equal. Until then, the M00 test bed is used to check mechanics: small test industries in five British states (in `# >>> rework test industries` blocks), and debt switched off for every country, so no one goes bankrupt (20 countries did within five years before).
- **Off:** national debt (starting debt, interest, bankruptcy) and the economic cycle. Banking is live (M11): pops, sectors, companies and the general pool borrow with interest and credit limits.
- **Recently done:** companies with their own accounts, bonuses on their own slices, investment, debt and failure, founded by incorporating profitable plants, and two at startup (M10), investment from sector capital and a general pool, in ROI tiers, with construction bills, sector debt and the government's development fund and infrastructure lines (M09), the Manufacturing Base, with HOI4's factories offmap and contracted by the state, and military resources at a tenth of a good, shared out by the mobilisation law (M08), a cap on transport supply from population, and a shipping price that follows use, which ports are paid (M07), deposits as state history data (potential, known and worked, with quality), prospecting that only finds what history put there, and RGOs for natural resources only (M06), land quality, crop eligibility and a carrying capacity for subsistence, with peasants paying base prices for what they grow (M05), national sectors with a PM/AM cache, profit tax, retained capital, dividends by size, target utilisation and capacity decay, with no per-good figures kept by states (M04, in progress: the UI rework remains), wealth, spending toward a target, pop debt and middle-class investment (M03), five pop classes with qualifications, slaves, bureaucrats and active manpower (M02), gradual prices (M01), generated PMs, Infrastructure Efficiency, floating wages, maintenance costs, incentives.
- **Testing:** a headless simulator called redux-eco-sim runs the mod's real economy scripts outside the game. It matched in-game British GDP to within about 0.5% at startup and after one month, so it's trusted for fast experiments. In-game testing is slow.

### Known problems
1. Price-employment oscillation (section 6): much reduced by M01 and M04. On the test bed every sector is profitable enough to sit at 100% utilisation, so the controller hasn't been tested against a real slump.
9. The market screen's per-state lists are empty: M04 dropped per-good state figures. Each country lists its sectors' biggest states (`sector_states@`) for the UI rework.
2. Wherever jobs are filled exactly, which startup does everywhere, utilisation sits at 1.0, just above the stable band, so the wage rises 0.5% a month (London +33% over five years on the test bed).
3. In the slave test states, the idle slaves count as labour supply and push the wage to its floor, because the stripped map has no plantations for them.
4. Budgets and debt don't scale with GDP: some spending lines stay large when the economy is small. On the test bed, Britain spends about twice its revenue (three times since M01's pop spending cut lowered sales tax), and Britain, France, Russia, Sweden and Spain hit the lending cap and run deeply negative treasuries.
5. Railways lose money on the test bed: the population baseline covers all of the stripped map's transport demand, so they're paid the floor rate. Under the old 1857 map they were paid little in hubs too. Sizing them is M14's job.
6. Many late automation upgrades are pointless: once an AM's labour cut hits zero, the extra input cost remains.
7. Urban centres grow fastest on the test bed (2 to 7 levels in five years, and 10 before M10's market headroom), because their margin is about 85%: a balance question for M14. Since Q126, money waits until it can build a sizeable project, but a whole expansion of a small plant can still be 0.1–0.2 levels, and a sector that has waited ten months accepts 0.1 levels again. A country that runs out of opportunities piles up its pool (the USA's holds about £32M by month 60).
8. **Most goods sit at their price cap** on the stripped map. Military upkeep and the missing industry pin wood, fiber, iron, textiles, services, chemicals, machinery, consumer goods and coal. Peasants, about 98% of ENG's market, left wealth 1 in M05 once they stopped paying market prices for what they grow: by month 60 ENG's are at 5.3, India's at 2.0. Their extra demand puts food at about 2.8× base.
10. **Paid-out capital raises GDP:** since companies and sectors pay out their surplus capital, and the market headroom keeps urban centres from flooding services, Britain's GDP over the fifth year is about 13% above M09's, with most sectors smaller. A balance question for M14. The USA's general pool still piles up (about £31M by month 60): Q150 left it alone.

## 8. Where it's heading [PLANNED]

The target design is `documentation/Planning/economy_rework/EOANB_Redux_Economy_Redesign_Updated.md`, built in milestones listed in that folder's `00_README.md`. Strat's design decisions are in `decisions.md` there (Q1–Q72, all answered on 2026-11-12). In short:

- **Country-sectors decide; state-industries are where it physically happens.** Each country keeps one record per sector (capacity, a target utilisation, output, profit, retained capital). Each method's economics are cached once a month as high up as possible: per market at that market's prices, with country modifiers on top. States add only local wages, Infrastructure Efficiency and modifiers. Each industry keeps one PM/AM pair. Company bonuses are applied once, nationally, to each owner's slice. A national target utilisation replaces each industry's own hiring decision, with a small local adjustment. Industry size becomes a floating number, and chronically unprofitable capacity slowly decays.
- **Gradual prices** (built in M01, see section 3). Supply and demand set a target price, and the actual price moves toward it once a month, slowly for small gaps and fast for big ones. Trade stays weekly so military production gets its resources. Prices move fastest, utilisation and employment slower, and capacity slowest.
- **Five pop classes** (built in M02, see section 3): slaves, peasants, working class, middle class and upper class, with one floating wage per state. Unemployment is the gap between a class's labour pool and its jobs. Qualifications limit how fast pops move up, as a major barrier to industrialisation. Bureaucratic jobs come from bureaucratic strain and are paid by the government. Active manpower (fielded and training) is taken out of the civilian pools. Wealth (built in M03, see section 3) keeps the old SoL baskets. Pops hold no savings: they spend toward a target set by consumer confidence, and overspending becomes debt, owed to the bank from M11.
- **Land and resources as state data.** Arable land, land quality and crop eligibility are set in history, with the population formula kept as a fallback for land until every state has it. Subsistence follows a carrying capacity with half returns beyond it, and pays rent to the upper class (built in M05, see section 3). Deposits are potential, known and worked, with quality kept separate from quantity (built in M06, see section 3).
- **Manufacturing Base** (built in M08, see section 5): HOI4's civilian and military factories and dockyards are offmap buildings, a contracted share of the country's manufacturing industries, split by type, at a cost per factory. Later the contracts may take their output from civilian use (Q32's option (b)).
- **Companies** are national accounting entities layered over state industries through ownership shares, competing on productivity, methods and leverage.
- **Finance as the source of booms and busts.** One bank per country holds reserves, loans and capital. Reserves come from base money × banking confidence. Sectors, companies and pops borrow. Credit is capped by both reserves and capital, defaults destroy bank capital, and credit then contracts. The real economy should otherwise settle toward equilibrium.
- **Money and currency.** All stored values stay real (1857 pounds). One currency per market, and the price level concerns only money in circulation: P × Y = M × V. Inflation erodes stored money, loans and wages. Commodity reserves in valuables, fed by the trade balance, set a damped exchange-rate scalar. Monetary laws change coefficients, not formulas.
- **Players act nationally.** Laws decide which controls a country has and who sets the targets. They come from the politics rework's law set (`_internal_politics_tokens.txt`): economic system, monetary system, financial system and others. Laws act on the economy only through modifiers, with yes/no modifiers for switches.

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
- says whether it depends on a system that's off or only planned (future currency controls);
- avoids global optimisation, forecasting and per-tick searches over everything.

If you're unsure whether something exists or is switched on, say so and ask, rather than assuming.

## 12. Glossary

| Term | Meaning |
|---|---|
| Size / level | How big one industry in one state is |
| PM | Production method: the recipe an industry uses |
| AM | Automation method: a labour-saving layer on top of the PM |
| Wrk / Mid | Working- and middle-class job shares in method data |
| Manufacturing Base | The size of a country's manufacturing industries plus content's bonuses. The state contracts its mobilisation law's share of it, and HOI4's offmap factories move toward that target month by month (M08) |
| Mobilisation share | The share of a country's resources the production screen gets, set by its economic mobilisation law (M08) |
| Target utilisation | A sector's national hiring decision, 10–100% of its jobs, which each state-industry shifts by up to 5 points (M04). It replaced each industry's employment target |
| Profitability | Profit ÷ revenue (the margin) |
| Qualifications | A state's stock of people qualified for middle- and upper-class work. Moves up need them |
| Administrative capacity | Filled ÷ required bureaucratic jobs. It scales tax collection |
| Active manpower | Soldiers in the field or in training, taken out of the civilian classes |
| Productivity | Value added per worker; used for comparisons and AI choices |
| RGO | Resource extraction industry, sized by the worked part of its known deposit |
| Subsistence | Peasant farming on leftover arable land, mostly outside the market |
| Base wage | A state's reference wage. Classes earn multiples of it |
| Wealth | 1–200, called standard of living (SoL) until M03. It sets the size and contents of a pop's basket |
| Consumer confidence | Sets a pop's target spending as a multiple of its income after investment. Above 1, pops borrow |
| Incentives | The long-term property-rights mood that drives investment appetite |
| Market leader | The country whose market others belong to. It sets prices for all of them |
| Infrastructure Efficiency | A state's transport supply against demand. It scales throughput |
| Investment fund | The general investment pool: pops' investment, a share of retained earnings and the development fund (M09) |
| ROI tier | An investment opportunity's rank: Exceptional, Good, Fair or Marginal, by a year's profit over its full cost |
| Debt level | Debt against annual GDP. About 200% triggers bankruptcy |
| Money scale | 1,000 units = £1M, per month |

M11 in-game validation started on 2026-11-17 with startup and June 1 saves. The new bank modifier token is now explicitly synchronised; all 13 in-game finance assertions pass. June GDP and bank loans match the simulator within 0.6% and 0.2% respectively, and the loan ledger reconciles exactly. The reserve difference follows different confidence inputs (42.9908 in-game versus 39.33 in the simulator); the monthly reserve formula matches within one raw unit. July's British interest receipts, dividends, retained capital and net loan movements reconcile exactly. An in-game owner probe confirms every active bank and the world total match authoritative household debt exactly. Binary saves retain stale variables for inactive countries, which must be excluded from world audits. The M11 in-game smoke test is complete.
