# EoaNBR Economy: How It Works

A plain-English briefing for an AI assistant (ChatGPT, Claude or similar) that can't see the code. It explains what the economy simulates, how the parts affect each other, what is switched on, and what limits any new idea has to live within. It describes behaviour, not syntax.

Last checked against the code: 2026-11-12.

## How to use this briefing

- You're helping design the economy of a Hearts of Iron IV mod. The person prompting you is usually Strat, the economy lead, who writes the script. Strat wants design thinking: mechanisms, trade-offs, failure modes, tuning levers. Don't write code unless asked.
- Each system below is marked **[LIVE]**, **[PARTIAL]**, **[OFF]** or **[PLANNED]**. Don't assume a system affects play because it's described here.
- Before you propose anything, read sections 9 to 11 (design principles, scripting limits, how to pitch). Most ideas that sound good fail one of those.
- Numbers given here are rough anchors for scale. Exact values live in a spreadsheet and change often.

## 1. What the game is

End of a New Beginning Redux (EoaNBR) is a total-conversion mod for Hearts of Iron IV (HOI4). It starts in 1857 and can run to the modern day. HOI4's own economy is little more than civilian and military factories, so the mod builds a full economic simulation in HOI4's scripting language: pops, industries, goods, prices, wages, trade, budgets, debt and investment. The spirit is close to Victoria, but it is much simpler inside, because HOI4 script is slow and every stored number makes save games bigger. Saves already take 5 to 10 minutes to load.

The economy ticks once a month for every country. Trade ticks weekly. Players act on it through a budget screen (tax and spending sliders), trade settings, building and upgrading industries, laws and national ideas, and events and focus trees. Content reaches the economy through modifiers and a set of documented effects such as "add treasury", "add debt", "add industries" and "construct industries".

## 2. The whole system in one paragraph

Every state has a population split into five classes, and a set of industries. Industries hire pops, turn input goods into output goods with a production method, sell the output at the market price, pay wages, and pass profit to their owners. Pops spend toward a target set by their income and consumer confidence, on a basket of goods that grows with their wealth. They hold no savings, and the classes that can borrow run into debt when they overspend. All production and consumption in a country and its subjects is pooled into one market, with one price per good, and each price moves with the ratio of demand to supply. Markets trade with each other weekly through a global market. Governments tax income, spending, dividends and trade, and spend on administration, the military, research, construction and subsidies. Deficits become debt, and too much debt ends in bankruptcy. Each state's wage floats with how tight its labour market is. The intended growth engine is investment, where retained profit and pops' investment build and upgrade industries. It is switched off while it's rewritten, so nothing grows on its own at the moment.

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
- **Resource extraction (RGOs):** mining, forestry and some raw farm goods. Size is the part of the state's deposit that is being worked.
- **Farms and plantations:** crop farms, rice paddies, livestock ranches, and cotton, luxuries and rubber plantations. They use arable land.
- **Factories:** steel foundry, mechanical works, tooling workshop, textile mill, consumer goods factory, chemical plant, and later electronics, vehicles, computers, synthetic fuels and more.
- **Urban:** urban centre (services), power plant, entertainment hub.
- **Transport:** railways and ports. They make transport capacity, not goods.
- **Subsistence farms:** automatic. They fill all arable land nobody else uses and are worked by peasants.
- **Government buildings:** HOI4's own civilian factories, military factories and dockyards. Their size follows the HOI4 building, they're always fully staffed, and the state budget pays their wages. They don't sell goods.

Industries unlock with technology. Every industry runs one production method and one automation method.

### Production methods (PMs) and automation methods (AMs) [LIVE]
- A **PM** is a recipe. Per thousand base workers it sets how much the industry makes, which inputs it needs, how the jobs split between the working and middle classes, how much transport it uses, and what it costs to build and how long that takes. PMs come in four eras: 1857, 1900, 1950 and 2000.
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
- **Target price:** base price × (demand ÷ supply)², held between a quarter of base and four times base. A 10% shortage raises it about 21%, and a large shortage pins it at 4×. Valuables are fixed at twice base, money-like.
- **The actual price moves toward the target gradually,** once a month at the start of the tick, before anyone is paid. Each month it closes a share of the gap: 30% for a small gap, 20 points more for every 100% of gap, and at most 70%. A gap under 2% doesn't move it. The gap counts a doubling and a halving the same. A 4× shortage therefore lifts the price about 3.1× in its first month. An ordinary 10% gap halves in about two months and is inside the dead band after five. The four values are globals in `resources_global_var_setup`. At startup, and for a new country, prices start at their targets.
- Revenue, wages, pop spending, GDP, trade income and tariffs all use the actual price. The trade AI uses the target (see Trade).
- Supply is production plus imports. Demand is pops' needs, industry inputs, materials for construction and retooling, military demand, and exports.
- The target is recomputed weekly as trade changes, and monthly as production and consumption change.

### Trade [LIVE]
- Each market sets a route per good: an amount to import or export, run weekly.
- All markets together form a **global market** with a world price per good, priced by the same rule over world supply and demand. Each market leader sees the world without the countries it can't trade with. The world price also has a weekly target and an actual price that moves monthly, by the same curve.
- Imports add to a market's supply and exports add to its demand, which pulls local prices toward world prices.
- Trade is limited by partners (you can't import more than others offer) and by shipping capacity from ports and convoys. If shipping is overloaded, all trade scales down.
- Trade profit is the gap between local and world price, minus tariffs and shipping cost.
- An automatic trade AI opens routes where trade profit per trade job is well above average earnings, and closes unprofitable ones. It doesn't nudge volumes: it solves for the volume that brings the market's target price to the world price plus costs. It judges routes at target prices, so trade answers a shortage within the week, while the money a route makes is counted at actual prices. A market with no production of a good but some need for it, or the reverse, keeps a 1-unit minimum route. National ideas such as Closed Economy shut trade off.

### Infrastructure Efficiency [LIVE, untuned]
Infrastructure Efficiency replaced an older system, in which transport was a priced good, in October 2026.
- Each state has **transport supply** and **transport demand**. Supply is a baseline from population and road technology, plus railways, plus part of port capacity. Demand comes from each industry's method.
- Their ratio sets the state's **Infrastructure Efficiency.** A shortage cuts throughput, down to a floor of 25%. Spare capacity gives a small bonus, up to +20%.
- It scales inputs and outputs, never jobs. Poor infrastructure makes workers less productive rather than unemployed, which suits poor, labour-heavy economies.
- Sectors depend on it to different degrees: farms 30%, resource extraction 60%, factories 100%, urban 50%. Subsistence doesn't depend on it at all.
- Railways and ports earn a fee per unit of transport, which is higher when the state is congested. Nobody pays the fee: the money appears and counts toward GDP. That's a known placeholder.

## 4. The monthly loop

First, every market leader moves its actual prices (market and world) toward the targets the last weekly tick set, and copies them to its members and their states. It then works out the market's PM/AM cache at the new prices (M04): what each sector in use makes, and what each method's inputs and construction cost.

Then each country, in rank order:

1. Last month's net budget goes into the treasury. AI countries adjust their budget, and the spending sliders' bonuses update.
2. Technology unlocks and their modifiers refresh. Each state's bureaucratic jobs and its share of active manpower are set.
3. Each sector's last month's retained earnings become its capital, and its target utilisation steps toward what last month's margin calls for (M04).
4. For each state the country controls:
   1. Construction and retooling progress. Finished projects add size.
   2. Prospecting rolls.
   3. Pops settle last month's finances: overspending becomes debt for the classes that borrow, and wealth moves toward the level where spending meets the target. Population grows, slaves above their cap are freed, soldiers are drawn or returned, qualifications are gained and lost, and peasants and the working class move between farming and industry.
   4. The state's base wage moves according to last month's labour market.
   5. Each industry's trailing margin moves toward last month's. A building that keeps losing money shrinks, but only while investment is on.
   6. Pops move between the working, middle and upper classes to fit the jobs on offer, within their qualifications.
   7. Everything is recomputed: arable land and subsistence, jobs and employment (bureaucratic jobs included), government buildings, production and each industry's finances, the upper class's dividends from last month's sector accounts, then each class's earnings, needs, taxes, confidence and targets.
5. The country works out the goods its industries and pops make and use, by sector and method rather than state by state, which its market reads until next month. Then each sector's national accounts: this month's revenue, costs, profit, profit tax, retained share and dividends (M04).
6. Companies and investment-fund bookkeeping. Investment opportunities are off.
7. Market leaders recompute supply, demand and target prices for their whole market from the members' totals, the market screen's statistics, and GDP.
8. The budget is recomputed: taxes, spending, debt and interest.
9. Statistics and graphs. The boom and recession check would run here from the second year, but it's switched off during the rework.

Weekly: markets recompute supply, demand and target prices with current trade and military demand, from each member's goods totals of its last monthly tick (industries and pops only change monthly), the global market updates, the trade AI adjusts routes, and trade flows recompute. Actual prices don't change during the month. Trade stays weekly so that HOI4's military factories get their resources within a week.

**The lags matter.** Wages react to last month's labour market, target utilisation to last month's margins, and pops act on last month's earnings. These one-month delays are a big part of why the economy can swing (see section 6).

## 5. How the pieces work

### Production and employment [LIVE]
- An industry's potential output comes from its size and method. Actual output depends on how fully it's staffed, Infrastructure Efficiency, economy of scale (bigger industries in one state get up to +20%), and national and sector modifiers.
- Partial staffing is slightly more productive per worker: a half-staffed plant makes about 59% of its full output.
- **Target utilisation (M04)** is the hiring decision, made nationally for each sector: the share of its jobs on offer, from 10% to 100%. Every sector starts at 80%.
  - National margin above 10%: it rises, by 1 point plus half a point per percentage point of margin beyond 10%.
  - Margin below 0: it falls the same way.
  - In between: it holds steady.
  - It moves at most 5 points a month. The old per-industry targets could jump 20 points.
- **Local shift:** each state-industry works at its sector's target, shifted up to 5 points by how its own trailing margin compares with the national margin. Government buildings always work at 100%.
- Jobs are filled by pops of the matching class. If a state is short of a class, every industry there, and the bureaucracy, is short-staffed in proportion. Slaves take working-class jobs first.

### Profit and where the money goes [LIVE]
- **Revenue:** output sold at the market price. Railways and ports get their transport fee instead. A state-industry stores only what the accounts add up (revenue, inputs, payroll, maintenance) and a trailing margin. The industry screens work out the rest.
- **Costs:** wages (base wage × the class's multiple × employees, with nothing paid for slaves), inputs bought at market price, and **maintenance**. Maintenance is a fixed upkeep of about 3% of build cost a year, paid even on idle capacity.
- **Sectors keep the accounts (M04).** Every industry token except subsistence farms and the three government buildings is a national sector. Each month a country adds up each sector's revenue, inputs, payroll and maintenance from its states into one record (`sector_*@<sector>`), with its operating profit and margin. The record also holds what a national screen shows (Q91): jobs and employment per class, transport, construction and retooling under way, reserves, and the method mix.
- **Profit** pays corporate tax when it's positive, at the country's rate. The sector keeps `global.sector_retained_share` (30%) of what's left as **sector capital**, scaled by investment appetite from incentives, and pays the rest as dividends. M09 will spend the capital; until then it only accumulates. Employees get no bonuses: wages are their share.
- **Loss** comes out of the sector's capital first, then out of dividends, which go negative. Sectors can't borrow until M11.
- **Dividends** are paid by size: each state's upper class gets the sector's dividend per size × the size it owns there, a month later. Subsistence rent (20% of subsistence output) and government buildings pay their own state's upper class directly.
- **Ownership:** the upper class owns every industry's generic share, its size less what companies hold. Companies can own slices of an industry (see below).
- **The PM/AM cache (M04).** Each market works out, once per price change, the value of one bundle of each sector's goods and what each method's inputs and construction cost. Each country applies its own sector and method modifiers, and each state its local factors. The industry screens and getters read the same values.

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
- **Investment:** the middle and upper classes put a share of their after-tax income into the investment pool (`middle_class_investment_contribution_factor`, base 10%, and `upper_class_investment_contribution_factor`, base 20%, at most 80%), scaled by incentives. The pool arrives in M09, so for now the money disappears.
- **Wealth,** from 1 to 200, sets each class's basket of goods (it was called standard of living until M03). The wealth-1 basket is worth `global.pops_base_spending` per thousand pops a month at base prices: 0.1 since M01, cut from 0.3, which had pinned food at its cap. Food comes first. Textiles, consumer goods and services follow, then luxuries from around wealth 21, and later electricity, appliances, vehicles and computers. The basket's value roughly doubles every 10 levels. It's defined in base-price value and bought at market price, so expensive goods squeeze pops. A separate SoL, worked out from wealth plus things like pollution, comes later.
- **Technology gates needs.** If a good isn't available yet, such as electricity, an older substitute fills the need. A state's electrification shifts the basket over time, although nothing sets electrification yet.
- **Target spending** = (income − investment) × consumer confidence. Spending is goods, taxes and debt repayments. Each month, wealth moves toward the level where spending meets the target: progress builds by `global.pops_wealth_speed` (6) × the gap ÷ goods spending, and each whole point moves wealth one level.
- **Debt:** for the working, middle and upper classes, spending above income after investment becomes debt (`pops_debt@<class>` on the state). They repay 4% of it a year as part of their spending, and half of any surplus repays more. The rest of a surplus disappears. There's no interest until the bank becomes the creditor in M11. A class that empties has its debt written off. Peasants and slaves don't borrow, so a peasant's target is capped at its income.
- **Consumer confidence,** from 0.2 to 2, starts from national modifiers (100 at peace, plus a stability bonus). Debt repayments lower it by their share of income, and faster once that share passes what pops tolerate (10% plus a little from banking and consumer confidence). Above 1, the classes that borrow spend more than they earn, and their debt grows until its repayments take half of confidence's excess over 1, as a share of income. At ENG's 108.7 that's about 4% of income, from a debt of about 13 months' income, which takes decades to reach.
- **Peasants** live mostly off their own farms. Only about 20% of subsistence output reaches the market, and only about 20% of their needs show up as market demand. They pay for all of their basket out of their subsistence income.

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
- **Spending:** administration (the bureaucrats' pay, plus per-head and per-GDP costs), military payroll (manpower × average earnings), military procurement (goods for equipment), research, construction (builds the government pays for), projects, subsidies, order and intelligence, and social spending.
- **Sliders have political effects.** Taxes cost political power, stability, war support and *incentives*, a property-rights mood that drives investment appetite. Spending buys HOI4 bonuses: military spending improves army organisation and morale, research spending speeds research, and procurement raises production efficiency and lowers equipment cost.
- **Debt:** a negative treasury becomes debt, domestic or foreign. Interest starts around 8%, is cheaper for great and secondary powers, and rises when the lending pool is scarce. The *debt level* tracks debt against annual GDP. Passing roughly 200% fires **bankruptcy**: debt is wiped and spending is cut, but stability takes a heavy hit. Lower stability means lower productivity and consumer confidence, so pops spend less.
- **Debt switch:** while the rework runs, `global.eco_debt_enabled = 0` skips every starting debt, sets both interest rates to 0 and stops bankruptcy. Deficits still borrow up to the lending cap (24 months of GDP). Past it, the treasury goes negative with no consequence. M14 turns the switch back on.
- AI countries repay debt when they can and raise taxes when they're in deficit.

### GDP [LIVE]
- A state's GDP is value added: each industry's revenue minus the goods it bought (M04). That counts subsistence food peasants eat themselves at base price, transport fees and government building output, as before. A market's GDP, added up when its leader ticks, values each member's last month at that month's prices.
- **Money scale:** 1,000 money units = £1 million, and every flow is per month. The historical UK national income in 1857 was roughly £665M a year, which would be about 55K a month. That's the reference scale for the rebuild, not a value the game currently hits.
- GDP drives debt ratios, administration cost, each country's share of market trade, and the statistics screens.

### Investment [OFF, being redesigned]
How the old system works, which is still in the code behind a switch:
- The upper class puts part of its income into a national **investment fund**. The share depends on their contribution rate, the *incentives* level, and how attractive the best opportunity looks. It's damped if the fund already sits on idle money.
- The fund keeps a list of **investment opportunities**: build a new industry in a state, expand one, upgrade its PM or AM, exploit known reserves, prospect, or buy a slice of an industry. Each is scored by *attractiveness*, roughly annual return, where 10% ROI scores 100. The fund only backs opportunities scoring at least 100, up to a monthly spending target.
- A project first pools about 25% of its build cost, then pays the monthly construction cost while it builds. Construction materials are real demand for goods.
- Players can subsidise opportunities from the treasury.
- **While it's off,** nothing builds or upgrades on its own. The money pops set aside for investment, and sector capital, aren't spent on anything. The old scrap-based downsizing is deleted (M04). Capacity decay replaces it (M04): a building whose trailing margin is below −5% loses 1% of its generic owner's size a month, but only once the switch is on.

### Companies [PARTIAL]
- Companies own fractional slices of industries: a size-14 mill might be 2 levels Company A, 4 levels Company B and 8 levels local owners. Each slice earns its share of that industry's profit.
- A company keeps 30% of its dividends as its treasury and pays the rest to the upper class of its headquarters state, which can be a financial hub far from its holdings.
- Companies are founded dynamically, as an investment-fund "national opportunity" that buys a slice of a profitable local industry. Each new company makes the next more expensive. Companies can also expand, exploit and prospect.
- The bookkeeping runs every month, but founding and company investment sit behind the investment switch. In practice no companies exist yet.
- Planned: companies defined at game start, valuations and a stock market, state-owned shares, mergers and acquisitions.

### Banking and finance [mostly OFF]
- A country-level bank exists but is disabled. Pop borrowing and repayment are stubbed out, so pops only save.
- The *incentives* driver is live: a long-term property-rights mood, kept separate from short-term consumer confidence and investor confidence.
- Planned: banking levels (none, domestic, international), inflation from a money supply, credit ratings that set borrowing limits, bank runs, default leading to bankruptcy, and international lending from great powers through explicit credit lines.

### Projects [LIVE]
Projects are country-level works, such as work programmes, with a goods bill and a build speed. Each month a project buys as many goods as it can toward its bill, and when it finishes it fires an effect. Content uses them for reforms and public works.

### Economic cycle [built, OFF]
From the second year, every month, each state's GDP is compared with its 3-year average, weighted by size. If most of the economy is falling, the country enters a recession, depression or free fall. If most is prospering, it gets a boom. Players get events, the AI gets the national idea directly, and stability moves. M00 fixed the month counter it depended on, then put it behind `global.eco_cycle_enabled = 0` until M14. On the test bed it was driven by month-to-month GDP swings and added noise to every comparison: in the simulator, 14 of 130 countries were in a downturn or recession by month 60, and Britain's consumer confidence flipped by 5 points.

## 6. Feedback loops to know

- **Price-employment swing (destabilising, much reduced by M01).** A shortage squares into a price spike, the producers' margins jump, they hire up to 20 points in one month, supply overshoots, the price crashes, and they fire. Revenue uses last month's price and hiring uses last month's profit, so the delays amplify the swing. On the test bed, most of the swing turned out to come from the trade AI toggling routes on and off every other week, which M01 fixed. Gradual prices damp the rest. Over 60 simulated months, ENG's GDP now settles instead of swinging ±5% a month, although on the stripped map many goods also sit still at their price cap. M04's target utilisation moves at most 5 points a month, where the old per-industry targets jumped up to 20: on the test bed the largest monthly swing in London's consumer goods output fell from 11 to 4 points.
- **Wage-labour loop (stabilising).** Tight labour raises wages, which squeezes margins, which slows hiring. Wages are sticky downward, so a slump shows up as unemployment first, and wages fall later.
- **Bankruptcy spiral.** Debt grows faster than GDP, bankruptcy follows, stability crashes, which cuts productivity and confidence, pops cut their spending, real incomes fall, and GDP falls further.
- **Infrastructure loop (partial).** Growth raises transport demand, Infrastructure Efficiency falls, and railways and ports earn more. The planned half, where investment then builds more railways and ports, needs investment back.
- **Investment loop (off).** Profit becomes dividends, dividends feed the investment pool, the pool builds capacity, wages and prices adjust, and the next round of opportunities changes. Without it the economy can only reshuffle labour; it can't grow.

## 7. Current state (November 2026)

- **The map has been stripped back to subsistence farming,** on purpose. Every state's industries and deposits are commented out of the history files, leaving only subsistence and HOI4's own factories. On the old map, Britain went bankrupt in its first July, in both the game and the simulator. Historical targets for Britain and India are written as comments in the history files.
- **The plan, decided November 2026: redesign first, balance last.** The economy is being rebuilt to a new design (section 8) in a series of milestones. Only after that will the 1857 map be rebuilt sector by sector so world supply and demand start roughly equal. Until then, the M00 test bed is used to check mechanics: small test industries in five British states (in `# >>> rework test industries` blocks), and debt switched off for every country, so no one goes bankrupt (20 countries did within five years before).
- **Off:** investment, banking, national debt (starting debt, interest, bankruptcy) and the economic cycle. Pops borrow, but without interest until M11.
- **Recently done:** national sectors with a PM/AM cache, profit tax, retained capital, dividends by size, target utilisation and capacity decay, with no per-good figures kept by states (M04, in progress: the UI rework remains), wealth, spending toward a target, pop debt and middle-class investment (M03), five pop classes with qualifications, slaves, bureaucrats and active manpower (M02), gradual prices (M01), generated PMs, Infrastructure Efficiency, floating wages, maintenance costs, the companies MVP, incentives.
- **Testing:** a headless simulator called redux-eco-sim runs the mod's real economy scripts outside the game. It matched in-game British GDP to within about 0.5% at startup and after one month, so it's trusted for fast experiments. In-game testing is slow.

### Known problems
1. Price-employment oscillation (section 6): much reduced by M01 and M04. On the test bed every sector is profitable enough to sit at 100% utilisation, so the controller hasn't been tested against a real slump.
9. The market screen's per-state lists are empty: M04 dropped per-good state figures. Each country lists its sectors' biggest states (`sector_states@`) for the UI rework.
2. Wherever jobs are filled exactly, which startup does everywhere, utilisation sits at 1.0, just above the stable band, so the wage rises 0.5% a month (London +33% over five years on the test bed).
3. In the slave test states, the idle slaves count as labour supply and push the wage to its floor, because the stripped map has no plantations for them.
4. Budgets and debt don't scale with GDP: some spending lines stay large when the economy is small. On the test bed, Britain spends about twice its revenue (three times since M01's pop spending cut lowered sales tax), and Britain, France, Russia, Sweden and Spain hit the lending cap and run deeply negative treasuries.
5. Railways lose money in busy hubs, while empty rural states get the full +20% Infrastructure Efficiency bonus for free.
6. Many late automation upgrades are pointless: once an AM's labour cut hits zero, the extra input cost remains.
7. Money pops divert to investment disappears while investment is off. So does sector capital: it accumulates (about 1.3K a month for Britain's test industries) until M09 spends it.
8. **Peasants sit at wealth 1 and most goods at their price cap** on the stripped map. Peasants are about 98% of ENG's market and too poor for even the wealth-1 basket. M05's land should lift them. Military upkeep and the missing industry pin wood, fiber, iron, textiles, services, chemicals, machinery, consumer goods and coal. Food is about 1.8× base.

## 8. Where it's heading [PLANNED]

The target design is `documentation/Planning/economy_rework/EOANB_Redux_Economy_Redesign_Updated.md`, built in milestones listed in that folder's `00_README.md`. Strat's design decisions are in `decisions.md` there (Q1–Q72, all answered on 2026-11-12). In short:

- **Country-sectors decide; state-industries are where it physically happens.** Each country keeps one record per sector (capacity, a target utilisation, output, profit, retained capital). Each method's economics are cached once a month as high up as possible: per market at that market's prices, with country modifiers on top. States add only local wages, Infrastructure Efficiency and modifiers. Each industry keeps one PM/AM pair. Company bonuses are applied once, nationally, to each owner's slice. A national target utilisation replaces each industry's own hiring decision, with a small local adjustment. Industry size becomes a floating number, and chronically unprofitable capacity slowly decays.
- **Gradual prices** (built in M01, see section 3). Supply and demand set a target price, and the actual price moves toward it once a month, slowly for small gaps and fast for big ones. Trade stays weekly so military production gets its resources. Prices move fastest, utilisation and employment slower, and capacity slowest.
- **Five pop classes** (built in M02, see section 3): slaves, peasants, working class, middle class and upper class, with one floating wage per state. Unemployment is the gap between a class's labour pool and its jobs. Qualifications limit how fast pops move up, as a major barrier to industrialisation. Bureaucratic jobs come from bureaucratic strain and are paid by the government. Active manpower (fielded and training) is taken out of the civilian pools. Wealth (built in M03, see section 3) keeps the old SoL baskets. Pops hold no savings: they spend toward a target set by consumer confidence, and overspending becomes debt, owed to the bank from M11.
- **Land and resources as state data.** Arable land, land quality and crop eligibility are set in history, with the population formula kept as a fallback for land until every state has it. Subsistence follows a carrying capacity with half returns beyond it, and pays rent to the upper class. Deposits are potential, known and active, with quality kept separate from quantity.
- **Manufacturing Base:** HOI4's civilian and military factories and dockyards become offmap buildings derived from the country's manufacturing sectors and split by a national allocation, rather than economic industries. The state pays a contract cost per factory. All on-map factories go.
- **Investment from capital pools.** Retained capital tends to expand the sector that earned it, and incentives decide how much profit is retained. A share flows into a general pool set by financial laws, alongside pops' own investment, which is how capital crosses sectors. A sector new to a country needs the general pool, credit, government or foreign money. Opportunities are ranked in ROI tiers (Exceptional over 20%, Good 10–20%, Fair 5–10%, Marginal −5% to 5%), with hard caps from deposits and land, and throttles on new establishments.
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
- says whether it depends on a system that's off or only planned (investment, banking, companies);
- avoids global optimisation, forecasting and per-tick searches over everything.

If you're unsure whether something exists or is switched on, say so and ask, rather than assuming.

## 12. Glossary

| Term | Meaning |
|---|---|
| Size / level | How big one industry in one state is |
| PM | Production method: the recipe an industry uses |
| AM | Automation method: a labour-saving layer on top of the PM |
| Wrk / Mid | Working- and middle-class job shares in method data |
| Target utilisation | A sector's national hiring decision, 10–100% of its jobs, which each state-industry shifts by up to 5 points (M04). It replaced each industry's employment target |
| Profitability | Profit ÷ revenue (the margin) |
| Qualifications | A state's stock of people qualified for middle- and upper-class work. Moves up need them |
| Administrative capacity | Filled ÷ required bureaucratic jobs. It scales tax collection |
| Active manpower | Soldiers in the field or in training, taken out of the civilian classes |
| Productivity | Value added per worker; used for comparisons and AI choices |
| RGO | Resource extraction industry, sized by worked deposits |
| Subsistence | Peasant farming on leftover arable land, mostly outside the market |
| Base wage | A state's reference wage. Classes earn multiples of it |
| Wealth | 1–200, called standard of living (SoL) until M03. It sets the size and contents of a pop's basket |
| Consumer confidence | Sets a pop's target spending as a multiple of its income after investment. Above 1, pops borrow |
| Incentives | The long-term property-rights mood that drives investment appetite |
| Market leader | The country whose market others belong to. It sets prices for all of them |
| Infrastructure Efficiency | A state's transport supply against demand. It scales throughput |
| IO | Investment opportunity |
| Investment fund | A country's pool of owners' money for investment |
| Debt level | Debt against annual GDP. About 200% triggers bankruptcy |
| Money scale | 1,000 units = £1M, per month |
