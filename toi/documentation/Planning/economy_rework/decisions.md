# Design decisions

Questions raised against the new spec, [EOANB_Redux_Economy_Redesign_Updated.md](EOANB_Redux_Economy_Redesign_Updated.md) ("the spec"), before implementation starts. Each one says why it matters, gives the options, and recommends one.

When Strat answers, write the answer under the question, mark it **Decided** with the date, and update the milestone file it belongs to. The tuning values the spec leaves to testing (§34) aren't asked here: they get settled in the milestone that builds them.

**Status:** Strat answered Q1–Q54 on 2026-11-12. Where an answer differs from the recommendation, it says "Not as recommended". The answers raised follow-up questions Q55–Q68, which Strat also answered on 2026-11-12. Those raised Q69–Q72, also answered the same day. M02's code reading raised Q73–Q80, and M03's raised Q81–Q84. Strat answered all of them on 2026-11-12. M04's raised Q85–Q91, answered on 2026-11-13.

---

## Process and test bed (M00)

**Q1. Milestone order.** Proposed order: test bed, prices, pops and labour, wealth and demand, national sectors, land, resources, infrastructure, industrial capacity, investment, companies, banking, currency, government and laws, startup balance. The main alternative is national sectors before pops.
*Recommend:* pops first. Every later system employs and pays by class. Writing the sector layer against ten pop types and then rewriting it for five would do that work twice. Halving the pop types is also the cheapest performance win in the spec (§23).

> **Decided 2026-11-12:** pops first.

**Q2. Debt in other countries.** ENG's starting debt is off, but the others' debt and spending were sized for the old GDPs. On the stripped map the Netherlands (`debt_level` 96) went bankrupt in month 1, and MNC and BRE within the year. After the PM retune, FRA, RUS, SWE and SPR all ran treasuries below −50K. Their bankruptcies reach ENG through the shared world market.
- (a) Comment out every country's starting debt, as was done for ENG.
- (b) Add one global switch that turns off interest and bankruptcy while the rework runs.
- (c) Live with it.

*Recommend:* (b). It's one line to turn back on in M14, and it also covers deficits that build up during testing.

> **Decided 2026-11-12:** one switch. It can turn off interest and bankruptcy, skip debt initialisation, or set debt to zero after init, whichever is simplest. It's turned back on in M14.

**Q3. Test industries in a subsistence world.** Outside the test industries, the whole world is subsistence farming. World prices for manufactured goods will sit at the 4× cap, so ENG will export everything it makes at high prices.
*Recommend:* accept that, since we're testing mechanics. Put the test industries in a marked block (`# >>> rework test industries` / `# <<<`) in about five British states, so they're easy to find and remove in M14. M00 has a proposed list.

> **Decided 2026-11-12:** as recommended. That was the plan.

**Q4. Replace or gate?** Old systems can be deleted when their replacements land, or kept behind flags, as investment is now.
*Recommend:* delete them: the old investment files, the buckets prototype, the old bank, the old pop types and downsizing. Git keeps the history, and simulator baselines give the A/B comparison.

> **Decided 2026-11-12:** delete them. Old files clutter the mod and confuse coding agents, and git keeps the history.

**Q5. Simulator edits.** Some milestones will need small changes to `redux-eco-sim`: scenario files, `save_inputs_1857.txt`, and tools that name `token:laborers` and the like. It's a separate repo.
*Recommend:* milestone work may edit it, committed separately there.

> **Decided 2026-11-12:** edit it freely during the rework. Strat commits those changes later.

---

## Prices (M01)

**Q6. Target price and how fast the price moves.** The proposal is to keep today's formula, base × (D/S)² clamped to 0.25–4× base, as the *target* price. The actual price then moves toward the target each tick at a rate that grows with the gap, with a small dead band where it doesn't move at all.
*Recommend:* yes. The exact rate curve is a §34 tuning value.

> **Decided 2026-11-12:** yes.

**Q7. Which tick moves prices.** Prices are now recomputed weekly, alongside trade. The weekly trade tick costs about 3 seconds.
*Recommend:* move prices once a month. Once prices are gradual, consider moving trade to monthly as well: weekly trade looks like it exists to let trade settle against prices that snap. Is there another reason trade is weekly?

> **Decided 2026-11-12:** prices move monthly, but trade stays weekly. Trade is weekly because of HOI4 military factories: waiting a month for the resources they need would feel bad, while a week is fine. Moving prices on the monthly tick is fine, since that's when money actually changes hands. Resource supply is what needs the weekly tick. Follow-up: Q56.

---

## Pops and labour (M02)

**Q8. Mapping the old pop types.** Laborers become working class, and workers, professionals and specialists become middle class. Capitalists and landowners become upper class. Bureaucrats become middle-class government jobs (Q13), and soldiers become active manpower (Q14). The sheet's Wrk and Mid columns map to working and middle class with no change. Should the new classes get new tokens (`token:working_class` and so on), or reuse old ones (laborers for working class)?
*Recommend:* this mapping, with new tokens. Reused names would mislead every later reader. Pop tokens appear outside the economy scripts only in economy localisation, scripted localisation and the getters, so the rename is cheap.

> **Decided 2026-11-12:** this mapping, with new tokens. The soldier and bureaucrat pop types can simply be removed, since nothing uses them now. Bureaucratic jobs (Q13) and active manpower (Q14) take their place.

**Q9. One wage or two per state.** Each state now has one floating `base_wage`, with fixed multiples: laborers 2×, workers 4×. With a single wage, a middle-class shortage raises working-class wages too. The spec, though, has PMs and AMs shifting demand between the classes (§5, §27).
*Recommend:* two floating wages per state, one per class, each driven by its own utilisation and seeded at today's 1 : 2 ratio. It adds one variable per state.

> **Decided 2026-11-12:** not as recommended. Keep one floating wage per state, with fixed multiples per class. Two wages may come later, but the current system works fine.

**Q10. Moving between classes.** Today `pops_convert` moves pops toward open jobs. Peasants become laborers at a rate limited by arable land, and the literacy and education caps sit at 100%. The spec doesn't say how classes change.
*Recommend:* keep moves driven by jobs. Cap working → middle by a qualification rate, tied to education later. Middle → working happens on unemployment, and working → peasant when wages fall below subsistence. Total population must still never change in this step.

> **Decided 2026-11-12:** yes. Qualifications cap the moves between classes, and they should be a major barrier to industrialisation. They were partway through being reworked when the economy was stripped. Follow-up: Q57.

**Q11. Where the upper class lives and gets paid.** Owners today are about 2% of jobs, sitting in the state where the industry is. Once sector accounts are national (M04), someone has to decide which states' upper class receives the generic sector's dividends.
- (a) In proportion to local capacity, so income stays where the industry is.
- (b) Into a country pool, split by each state's upper-class population.
- (c) To the capital, or an HQ state.

*Recommend:* (a) for the generic sector, while companies keep their HQ routing. The upper-class population stays at about 2% of jobs.

> **Decided 2026-11-12:** (a). Ideally the upper-class population would vary more than a flat 2% of jobs, but that's fine for now.

**Q12. Slaves.** The spec has slaves filling working-class jobs where slavery is legal, with employers paying their upkeep at minimum-basket cost.
- Do slaves fill jobs before free workers? They're cheaper.
- Who feeds slaves without a job?
- Is legality taken from the existing laws (`law_legacy_slavery`, `law_colonial_slavery`, `usa_slavery_law`, `law_slavery_banned`)?

*Recommend:* yes, slaves fill jobs first; unemployed slaves are fed out of the state's upper-class income; and yes, legality comes from those laws.

> **Decided 2026-11-12:**
> - Slaves fill jobs before free workers.
> - Legality comes from the slavery laws *and* cultural marginalisation: only pops of marginalised cultures can be enslaved.
> - Not as recommended: the upper class doesn't pay for slaves' needs, since that could bankrupt them. Slaves simply receive no income, and their needs should be so small as to be irrelevant.
>
> Follow-ups: Q61, Q62.

**Q13. Bureaucratic jobs.** The spec turns bureaucrats into middle-class government jobs, with administrative capacity = filled / required (§29).
- What sets the number of required jobs?
- Who pays them?
- Do they compete with private jobs?
- What does administrative capacity affect?

*Recommend:*
- Required jobs = population × a law factor.
- The budget's administration line pays them at the state's middle-class wage.
- When there aren't enough middle-class workers, government and private jobs fall short by the same proportion.
- Administrative capacity scales tax efficiency.

> **Decided 2026-11-12:**
> - Required jobs come from bureaucratic strain.
> - The government pays them, and they compete with private jobs.
> - Administrative capacity affects how well the government functions. The politics rework (`toi/documentation/vanadiums_notepad_while_hes_crashing_planes.txt`, "Bureaucratic Capacity") already sketches this: too few bureaucrats cut tax effectiveness and spending effectiveness.
> - Jobs are spread over states by population, and by whether the state is core territory.
>
> Follow-up: Q58.
>
> **Implementation note (M02, 2026-11-12):** bureaucrats compete with private jobs for workers: when a state is short of middle-class pops, government and private jobs fall short in the same proportion. They're left out of the labour utilisation that moves the wage, though, on both the jobs side and the workforce side. Otherwise every rural state, where bureaucrats are the whole middle class and startup fills their jobs exactly, would sit at utilisation 1.0 and see its wage creep up for good. A middle-class shortage still raises the wage through the private jobs it leaves unfilled.

**Q14. Active manpower.** What counts as active manpower, and who is drawn into it?
*Recommend:* HOI4's own fielded and training manpower. It's taken from peasants and the working class in proportion to their numbers, and spread over states by population. Soldiers' pay and consumption stay on the existing military budget and demand lines.

> **Decided 2026-11-12:** fielded and training manpower, since that's what the budget actually pays for. (Total manpower would follow the manpower law more literally.) The rest is as recommended.

---

## Wealth and demand (M03)

**Q15. Unspent pop income (contradiction).** Today pops save toward a target of about a year's income × banking confidence, and spend savings down when the target drops. The spec drops per-pop savings (§15) and has surplus income slowly raising wealth (§31). If pops hold no savings, any income they don't spend leaves the money flow.
- (a) Pops spend all their income every month: more than their wealth basket when income is above its cost, less when below. Wealth, and so the basket's composition, catches up slowly.
- (b) Unspent surplus becomes bank reserves once banking exists, and is tracked as a leak until then.
- (c) Keep pop savings.

*Recommend:* (a). Money flows close by construction, and no stock is needed per pop type.

> **Decided 2026-11-12:** (a), but keep target spending. Pops spend toward a target set by consumer confidence (Q16), not their whole income. There's no savings stock.
> - Income a pop doesn't spend disappears. Strictly it would become bank deposits, but deposits are abstracted (§15).
> - Spending above income becomes debt owed to the banking sector (Q43).
>
> Follow-up: Q59.

**Q16. Consumer confidence.** Today it shifts pops between saving and spending (0.2 to 2). Under Q15 (a) it has no job left.
*Recommend:* remove it from pops. If the modifier stays, it moves to banking confidence (M11).

> **Decided 2026-11-12:** not as recommended. Keep consumer confidence. It sets each pop's target spending, and pops adjust toward that. Don't move its effect to banking confidence.

**Q17. Wealth and saturation.** Is "wealth" today's standard of living (SoL), on the same scale: 1 to 200, with the basket doubling every 10?
*Recommend:* yes. Keep the variable and its scale, and call it wealth in the UI. Saturation means per-good caps on necessities such as food and textiles. Past the cap, extra spending moves to manufactured goods, services and luxuries.

> **Decided 2026-11-12:** yes, but no new saturation mechanic.
> - **Rename SoL to wealth.** The base value was always a wealth level; calling it SoL came from Victoria III. Later, SoL becomes a separate value derived from wealth, so SoL modifiers (pollution, for example) don't change a pop's wealth.
> - **Consumption stays as in the current mod, just optimised.** Each wealth level has its basket of goods (`global.pops_spending_need_at_sol@<good>`), and those tables already set what each level buys.
>
> So M03 is mostly a rename and some refactoring.

---

## National sectors (M04)

**Q18. What counts as a sector.** Proposed: one sector per industry token per country. That's the 25 buildings, the RGOs, railway and port.
*Recommend:* yes.

> **Decided 2026-11-12:** yes.

**Q19. One PM/AM per state-industry, or one per ownership slice (contradiction).** §3.1 gives a state-industry one PM and one AM. §19 says companies run their own PM/AM locally and talks about "PM/AM buckets".
- (a) One PM/AM per state-industry. Companies differ only through modifiers.
- (b) Each ownership slice (the generic sector plus each company present) has its own PM, AM, size and employment.
- (c) Up to two buckets per state-industry whoever owns them, an old method and a new one. This also allows gradual retooling.

*Recommend:* (b). Ownership slices already exist in the data (company holdings), and it's what §19 describes. The cost is about four variables per slice.

> **Decided 2026-11-12:** (a). The spec's "buckets" got garbled when the design conversation was summarised; they're an optimisation. Each industry has one PM/AM pair. Because the accounts are national, a sector can be split by owner (the generic owner plus each company) once, at the national level, with each company's bonuses applied to its own slice. The results are then passed back to the states by each owner's share of the industry there.

**Q20. The target-utilisation controller.** Does the national target replace each industry's `employment_target` (today 10–100%, moving up to +20 or −25 points a month)? The proposed shape is a damped step on the national operating margin: rise while the margin is above a threshold, fall while it's negative, capped at a few points a month.
*Recommend:* replace it, with that shape. The local adjustment stays within a few points of the national target.

> **Decided 2026-11-12:** yes.

**Q21. Where profit goes.** Today a third of profit goes to employees as bonuses. The rest is split between a per-industry cash reserve (capped at about a month of output) and dividends.
*Recommend:* drop the bonuses, since wages are the workers' share, and drop the per-industry cash reserve. Sector profit pays profit tax, then a retained share goes to sector capital (M09), and the rest is dividends to the upper class.

> **Decided 2026-11-12:** yes. The bonuses force financing onto the state side and make industries less profitable than they should be. They existed because the old wage system tended to undershoot, and the floating wage fixed that. Retained capital is national (Q34), which replaces the per-industry cash reserve.

**Q22. Sector debt before banks exist (sequence).** §2.2 gives each national sector debt and interest, but there's no lender until M11.
*Recommend:* sectors can't borrow until M11. Until then, a loss bigger than retained capital is covered by negative dividends from the upper class, and a sector that keeps losing shrinks (Q23).

> **Decided 2026-11-12:** yes.

**Q23. Capacity decay.** Should decay replace today's scrap-based downsizing (switched off)? It would work per state-industry, based on its own trailing margin, which needs one variable per state-industry. Upkeep on idle capacity stays.
*Recommend:* yes, and delete the downsizing code.

> **Decided 2026-11-12:** yes.

---

## Land and subsistence (M05)

**Q24. Where arable land comes from (contradiction with the code).** `state_eco_arable_land_init` sets `arable_land = workforce / 20 + 1` for every state whose history doesn't set it. Only 76 of 1,455 state files do. The spec says land must not come mainly from population (§10).
- (a) Generate it with a script from province terrain and count, written into marked history blocks.
- (b) Write it by hand.
- (c) Keep the population formula as a placeholder until M14.

*Recommend:* (a), with land quality from the same pass and hand overrides on top.

> **Decided 2026-11-12:** not as recommended: keep the population formula as a fallback. It's a stopgap, so arable land doesn't have to be set everywhere at once. The goal is for every state's history to set it. Follow-up: Q63.

**Q25. Reading the subsistence formula.** Taken literally, below carrying capacity K each peasant makes a fixed amount and yield technology only raises K. Above K, each extra peasant makes half. Is that the intent? It means yield technology only matters once a state is crowded. And what does "security" mean as a mechanic: resistance to famine?
*Recommend:* output = (min(P, K) + 0.5 × max(0, P − K)) × a fixed yield per peasant, where technology raises K only.

> **Decided 2026-11-12:** yes, that formula. There's no "security" or harvest-quality mechanic.

**Q26. Crop eligibility.** Proposed: one yes/no per farm sector per state (crop farm, rice paddy, livestock ranch, cotton, luxuries and rubber plantations), set from climate and terrain.
*Recommend:* yes, generated in the same pass as Q24.

> **Decided 2026-11-12:** yes. Q24 dropped the land pass, so where the data comes from is Q63.

**Q27. Rent.** Landowners now take 20% of subsistence output. §28 lists rents among upper-class income.
*Recommend:* keep one rent share on subsistence and commercial farms, paid to the upper class.

> **Decided 2026-11-12:** rent on subsistence only. Commercial farms are ordinary industries with no extra rent, since their profits go to the upper class anyway.

---

## Resources (M06)

**Q28. Where deposit data comes from.** An RGO's size now comes from `base_resource@`, which is read from HOI4's `resources = {}` blocks (commented out by the strip). The spec says vanilla resources are no longer the economic source (§9).
*Recommend:* potential deposits, known deposits and quality become per-good state history variables. HOI4 resources only receive economy output, through `resource_trade`, as now.

> **Decided 2026-11-12:** yes, with a third stage, active deposits:
> - **Potential:** not found yet.
> - **Known:** found and open for expansion, but working it needs investment.
> - **Active:** being worked now.
>
> Follow-up: Q68.

**Q29. Quality, depletion and wood.**
*Recommend:* quality multiplies throughput only, so jobs per size don't change. Deposits don't deplete for now. Forests are a renewable, deposit-like cap.

> **Decided 2026-11-12:** yes.

**Q30. Prospecting.** Today it's random rolls with a chance of a major find, paid for by the government or a company.
*Recommend:* it becomes an investment opportunity (M09), funded from the RGO sector's capital, the general pool or the government. A government "fund prospecting" control comes in M13.

> **Decided 2026-11-12:** yes.

---

## Infrastructure (M07)

**Q31. Who pays railways and ports.** Their transport fee revenue has no payer: the money appears from nowhere.
*Recommend:* each industry pays the fee × its transport demand, as a cost line. That closes the money loop and makes congestion cost producers. It fits §8, because the fee is a rate set by Infrastructure Efficiency, not a market price.

> **Decided 2026-11-12:** no. Charging each industry localises the cost and removes part of the optimisation problem. The fee is small for any one industry, and industries already pay for congestion through lower throughput. The fee money that appears from nowhere only pushes prices up slightly.

---

## Industrial capacity (M08)

**Q32. What "underlying productive industrial capacity" is (§12).** Today arms factories, industrial complexes and dockyards are special industries. Their size follows the HOI4 building, they're always fully staffed, and the state budget pays their wages. History has 303 of them.
- (a) One sector that produces capacity, which the government hires and splits into civil, military and naval use.
- (b) The government contracts a slice of existing manufacturing sectors, which takes that slice out of civilian output.
- (c) A pool derived from total manufacturing capacity.

*Recommend:* (a). It's the cheapest, and it keeps HOI4 production tied to one clear sector.

> **Decided 2026-11-12:** not as recommended: (c) for now. It's simpler, and it matches the TNO-like system the spec grew out of. Long term Strat prefers (b). Follow-up: Q64.

**Q33. How HOI4 buildings follow the allocation.**
- (a) Script sets HOI4 building levels in the states with the most capacity, and HOI4's own factory construction is disabled.
- (b) Buildings stay fixed, and HOI4 modifiers scale how many can be used.

What happens to the 303 factories in history?
*Recommend:* (a), because players see real factory counts, and remove the history factories once M08 derives them. HOI4 building slots limit how many fit in a state. That needs checking.

> **Decided 2026-11-12:** neither: they become offmap factories (`add_offsite_building`, which some decisions already use). All on-map factories are removed. That's also why (b) appeals for Q32 long term: factories become a straight conversion, with no employment to track.

---

## Investment (M09)

**Q34. Reversals from the old spec (contradiction).** Confirm three changes:
1. Each sector keeps its own retained capital, which reverses the old "no per-industry money pools".
2. The investor-type pools are gone with the upper-class merge: landowner or "particular" capital, and capitalist or "general" capital.
3. Geographic capital mobility ("Illinois money stays in Illinois"). The old spec called it a central difference between Qing, Japan and Britain, and the new spec doesn't mention it. Is it dropped, or kept as a second dimension?

*Recommend:* yes to 1 and 2. Drop 3 for now: capital trapped in its sector already makes takeoff hard for backward economies (§13.3).

> **Decided 2026-11-12:** yes to all three.
> 1. Sectors keep retained capital.
> 2. The investor-type pools merge into one general capital pool, part of which comes from each sector's retained earnings.
> 3. Geographic mobility is dropped. States are no longer independent economic units at all.

**Q35. What counts as greenfield (contradiction within the spec).** §13.3's "new sectors" with no retained capital are new to the *country*. §13.5's throttle, "one new establishment per sector per month", is about new *states*.
*Recommend:* a national sector that opens its first plant in a new state pays for it from its own retained capital, subject to the §13.5 throttle. Only a sector new to the country needs outside capital: the general pool, credit, the government or foreigners.

> **Decided 2026-11-12:** as recommended, but established sectors can always draw on those outside sources as well.

**Q36. Does the upper class invest?** Today capitalists and landowners divert part of their income to the investment fund. While investment is off, that money disappears.
*Recommend:* no. Dividends are spending money only. The general pool is fed by transfers from sectors, credit, the government and foreign money.

> **Decided 2026-11-12:** not as recommended. People invest their own money all the time, so pops can invest. Their money goes into the general pool, which keeps it cheap to compute. Unlike business reinvestment, it comes out of income that has already paid income tax. Follow-up: Q60.

**Q37. Who owns what the government pays to build?** Does capacity the government funds become state-owned (a state slice), or a grant to the generic sector?
*Recommend:* a grant by default. State equity becomes an option once companies exist (M10).

> **Decided 2026-11-12:** grants by default, though it may depend on the case.

**Q38. PM and AM upgrades.**
*Recommend:* an upgrade is an opportunity type, funded from the sector's retained capital through the same tiers. Settle the AM labour-cut clamp first, or the AI will make losing upgrades. Archive segment 02 recommends cuts as a percentage of the PM's share.

> **Decided 2026-11-12:** yes. AM labour cuts are additive percentages, not multiplicative, which makes the maths easier, and jobs never go below zero.

**Q39. Incentives.** `incentives_modifier` now scales pop investment appetite, which goes away under Q36, and it also feeds a tax factor.
*Recommend:* incentives shift the ROI tier thresholds, acting as a property-rights risk premium. Or remove it.

> **Decided 2026-11-12:** not as recommended. Incentives scale pop investment and industry reinvestment, meaning the share of profit kept as retained earnings instead of paid out as dividends. It's a big lever: an economy with bad incentives shouldn't really grow.

---

## Companies (M10)

**Q40. Build on the MVP?** The MVP stores company records globally, keyed by id, with holdings per state and building, and dividends pulled by the HQ state.
- Should the generic sector be one more ownership entity, run through the same code path?
- When a company fails, does its capacity go back to generic ownership, with its loans written off against bank capital?

*Recommend:* yes to all three.

> **Decided 2026-11-12:** yes, build on the MVP. It wasn't finished, and the original full company plans aren't available.
> - Each country has its own generic sector. Companies are more permanent entities.
> - A failed company's capacity goes back to generic ownership, and its loans are written off.
>
> Strat's notepad has a plan for company failure. Follow-up: Q66.

**Q41. Founding companies.**
- (a) Keep dynamic founding, now funded from the general pool.
- (b) Only companies defined at game start.
- (c) Both.

*Recommend:* (c), with the startup-defined companies built first.

> **Decided 2026-11-12:** (c), as was planned.

---

## Banking (M11)

**Q42. One bank per country.** One aggregate bank per country, as the disabled one is, with the specialist banks of §21.8 acting as lending priorities on it?
*Recommend:* yes.

> **Decided 2026-11-12:** yes. Specialist banks weren't on Strat's original idea sheet (an AI added them while the spec was drafted), but they're not a bad idea.

**Q43. Who borrows.** Sectors and companies borrow from the bank. Does government debt (domestic and foreign, interest around 8%) also become a bank loan, competing with private credit, or does it stay separate?
*Recommend:* it stays separate in this pass.

> **Decided 2026-11-12:** pops borrow from the bank too. The bank doesn't record which pops borrowed: pop debt belongs to the bank of whichever country owns the state. Government bonds stay separate for now, though ideally they'll draw on the same credit market eventually. Follow-up: Q59.

**Q44. Where bank reserves come from.** There are no explicit deposits (§15), and the spec leaves the link between base money and reserves open.
*Recommend:* reserves are a share of base money held by banks, set by financial development, rather than a separate stock.

> **Decided 2026-11-12:** reserves come from the country's base money, created by minting, × its banking confidence. At 100 banking confidence, all base money is held in banks as reserves. Reserves move slowly toward that target rather than jumping, but bank runs can still drain them. Follow-up: Q65.

---

## Money and currency (M12)

**Q45. Currency area.** Does each country have its own currency, or does each market (a customs union of subjects and members) share one?
*Recommend:* one per market. Prices are already per market.

> **Decided 2026-11-12:** one per market.

**Q46. What the price level scales (contradiction risk).** §18.1 says domestic inflation is only a nominal scaling. That only works if trade compares *deflated* prices. Otherwise a country that inflates 2× sees every import as cheap.
*Recommend:*
- The price level P scales base prices, and so target prices, construction costs and upkeep.
- Wages pick up P through the inflation term already designed into `base_wage_update`.
- Trade divides domestic prices by P and applies the exchange scalar before comparing them with world prices.
- Real GDP = nominal GDP / P.
- Every country starts with money supply equal to money demand, so P = 1.

> **Decided 2026-11-12:** not as recommended. Inflating every value risks overflow in HOI4.
> - **Every value stored and computed in-game stays real:** 1857 British pounds, at the current scale (1,000 = £1M).
> - **The price level concerns only money in circulation:** P × Y = M × V. Velocity V is probably a constant, possibly partly driven by consumer confidence.
> - **Trade compares real prices,** adjusted by relative exchange rates, and nothing else.
> - **Nominal values may come later, as UI only.** Each currency would get a value against the pound, and scripted localisation would show nominal amounts.
>
> Follow-up: Q67.

**Q47. Commodity reserves.** Is the one "valuables" good the reserve commodity, covering gold and silver together?
*Recommend:* yes. The government buys valuables on the market into its reserves, and their fixed price of 2× base goes away.

> **Decided 2026-11-12:** yes. Valuables stand for gold, silver, gems and other valuables.

**Q48. Trade balance.** Nothing records import or export value today. There's only trade profit: the gap between local and world price, minus tariffs and shipping.
*Recommend:* record export value − import value per market, settled against reserves.

> **Decided 2026-11-12:** the context above was wrong: trade value is already recorded per good (`trade_value@<good>` is the traded amount × price, less tariffs, and `trade_value` holds the total). Add import value and export value per market, and the total trade balance.

**Q49. Seigniorage.** Does newly created base money go to the treasury?
*Recommend:* yes. That's how printing money pays for deficits and causes inflation.

> **Decided 2026-11-12:** yes. The treasury receives the minted quantity ÷ P, which converts it to real money.

---

## Government and laws (M13)

**Q50. Economic-system laws.** There's no laissez-faire / interventionist / planned category yet. The existing economic laws are trade, mobilisation, tax rates, child labour, work hours and land property, plus the central-bank laws in internal politics.
*Recommend:* a new law category.

> **Decided 2026-11-12:** not as recommended. The politics rework already has a full law set in progress, in `toi/common/ideas/_internal_politics_tokens.txt`, and the economy uses it instead of the old laws. The relevant categories include `economic_system`, `monetary_system` and `financial_system`. Follow-up: Q61.

**Q51. Which controls come before balance.**
*Recommend:* only what each system needs in order to be tested, with the AI on defaults and the existing `ai_budget`:
- existing: budget sliders and tariffs;
- new: sector subsidies and taxes, government investment, target utilisation (planned economies), the policy rate, the reserve requirement and minting.

The rest of §21 is content for later.

> **Decided 2026-11-12:** yes.

---

## Cross-cutting

**Q52. Close every money flow.** Every money flow would have a payer and a receiver: no money from nowhere, no leaks. A simulator probe would check the residual each month. Today's known breaks are transport fees (Q31), pop investment (Q36), pop savings (Q15) and bankruptcy wipes.
*Recommend:* yes. The money supply and inflation in M12 mean nothing without it.

> **Decided 2026-11-12:** no. Money is created and destroyed all the time, and the money in circulation doesn't need tracking. Base money is a value that rises with minting. Inflation affects:
> - stored money (inflation lowers its real value, deflation raises it);
> - loans;
> - wages (inflation cuts real wages);
> - perhaps things outside the economy, such as stability.
>
> Follow-up: Q67.

**Q53. Name clash.** In code, `industrial_capacity` and `industrial_capacity_use` are Infrastructure Efficiency's supply and demand, and their modifier names appear in 119 files. §12 uses "industrial capacity" for productive capacity.
*Recommend:* keep the code names, and give the §12 concept another name in code, such as `factory_capacity`.

> **Decided 2026-11-12:** keep the code names. The §12 concept is called the **Manufacturing Base** (`manufacturing_base` in code).

**Q54. Systems the spec doesn't mention.** These would stay as they are unless a milestone has to touch them: trade routes and the trade AI, tariffs, the budget lines, construction (goods bills delivered over time), projects, technology unlocks, population growth, economy of scale, the economic cycle, and the debt and bankruptcy events.
*Recommend:* yes.

> **Decided 2026-11-12:** yes.
>
> **Amended 2026-11-12 (M00):** the economic cycle is switched off during the rework (`global.eco_cycle_enabled = 0`) and back on in M14, the same as debt. Once the month counter worked, its threshold flips added noise to every simulator comparison.

---

## Follow-up questions (raised 2026-11-12)

These come out of the answers above. Strat answered them on 2026-11-12.

**Q55. Where the PM/AM cache lives (M04).** Strat asked to confirm that a cache exists. It does: §6 has the country cache each PM/AM combination's output value, input cost, labour and productivity, and M04 builds it. But prices are per market (the leader holds them and the members copy them), and after Q7 they change only once a month. So the raw economics are the same for every country in a market. Proposed layers:
- **Global:** static PM and AM data. This exists already (`global.pm_output_amount@` and so on).
- **Market:** output value and input cost per unit of size, and labour per class, at the market's prices. The market leader computes these once a month, after prices move, for the combinations in use.
- **Country:** technology and law modifiers (throughput, employment, input factor), as a few scalars per sector.
- **Owner slice** (Q19): company bonuses.
- **State:** local wage, Infrastructure Efficiency, state modifiers, deposit or land quality, and economy of scale.

*Recommend:* this layering, so the cache lives at the market, not the country. Output value and input cost stay separate, because some modifiers scale only inputs. The getters read the cache and stay trigger-safe.

> **Decided 2026-11-12:** yes, with one addition: each country in a market can have its own modifiers, beyond technology and laws, including per-PM ones such as `pm_<x>_throughput_modifier`. The country layer applies all of them to the market's values, per PM/AM combination where a modifier is per PM, before any state reads them.

**Q56. What the weekly trade tick reads (M01, from Q7).** If the actual price moves only monthly, the weekly trade AI sees the same price gap four weeks in a row and keeps adding volume, so trade overshoots within the month.
- (a) The weekly tick still recomputes supply, demand and the target price, and the trade AI reads the target. The target closes as trade adds supply. The actual price, which revenue, wages and pop spending use, steps once a month.
- (b) The trade AI reads the actual price, and each route's volume can change only so much per week.

*Recommend:* (a). The weekly tick keeps its supply and demand recompute, and the price step moves to the monthly tick.

> **Decided 2026-11-12:** (a).
>
> **Implementation note (M01, 2026-11-12):** the trade AI doesn't add volume step by step. `evaluate_best_trade_quantity` solves directly for the volume that brings the market's target price to the world price plus costs, so a stale price couldn't have made it pile on. The weekly overshoot that did exist came from the two "minimum trade" rules. They checked `supply@` / `demand@`, which include last week's trade, so a route the evaluation had just cut to 0 was restored only every other week. About 30 small countries toggled 1-unit coal imports on and off, and ENG's exports were rationed between 34 and 2 in alternate weeks. M01 makes those rules check `production@` / `need@` instead. Weekly trade now settles in one week.

**Q57. How qualifications work (M02, from Q10).** There are two designs:
- **The code** has a cap model inside `pops_convert`. Literacy caps workers, professionals, specialists and bureaucrats. Schooling caps professionals and specialists. Education caps specialists, but that check compares a variable with itself, so it never applies. All the caps sit at 100% today, so nothing binds.
- **Strat's notepad** (`toi/documentation/Strats_notepad_while_hes_at_uni.txt`, "Qualifications") has a stock model:
  - Pops gain skilled and educated qualifications each month from literacy, schooling, education, wealth and the workforce mix.
  - They lose them through death, conversion and decay.
  - Gains are cut for oppressed and non-accepted cultures, and under serfdom.
  - Each pop type needs a set number of qualifications per thousand.

The options:
- (a) Build the stock model in M02, as two stocks per state, skilled and educated. The middle class needs skilled qualifications, and the upper class needs skilled and educated. The culture and serfdom cuts come from laws (Q61) and marginalised cultures.
- (b) Map the cap model onto the classes (literacy caps the middle class, schooling the upper class), and build the stock model later.

*Recommend:* (a). With every cap at 100%, nothing holds back industrialisation today, and the stock model is the plan that was being worked on. The amounts are §34 tuning.

> **Decided 2026-11-12:** (a), the notepad's stock model; the cap model was a stopgap. Not as recommended: use a **single qualifications value** instead of skilled and educated. The upper class needing "educated" isn't the intent. Both the middle and upper classes need qualifications, in amounts settled during tuning.

**Q58. What makes bureaucratic strain (M02, from Q13).** Nothing in the code computes strain yet. Proposed: strain = the sum over states of population × a core weight, × a factor from the bureaucracy law (`bureaucracy_tokens`). In M13, government programmes such as education, welfare and policing add to it. A state's required bureaucratic jobs are its share of the strain.
- Does a non-core state need more bureaucrats per head than a core state, or fewer?
- Are all bureaucrats middle class? The notepad puts upper-level bureaucrats in the upper class.

*Recommend:* non-core states count at half weight, since they're governed lightly, which matches their lower tax yield. All bureaucratic jobs are middle class for now.

> **Decided 2026-11-12:**
> - Non-core states need **fewer** bureaucrats per head than core states.
> - Ordinary bureaucrats are middle class.
> - In addition, the capital has some upper-class government jobs, for department heads and senior bureaucrats who actually make decisions.

**Q59. Pop debt before banks exist, and where it's stored (M03 and M11, from Q15 and Q43).** Target spending = earnings × consumer confidence (0.2–2), so a confident pop can spend up to twice its income, and the excess becomes debt. The bank only arrives in M11. The code already has stubs for this: `p_bank_lent_to_pops_k`, creditworthiness, debt interest and repayment, and confidence penalties for heavy debt service.
- **Before M11:**
  - (a) M03 builds the debt stock and its repayment, with no interest. The bank becomes the creditor in M11.
  - (b) Spending is capped at income until M11.
- **Storage:** one debt stock per state and class, with the bank holding the country total. When a state changes owner, its pops' debt moves to the new owner's bank.

*Recommend:* (a). Store debt per state and class, for the working, middle and upper classes only, since peasants and slaves don't borrow.

> **Decided 2026-11-12:** as recommended: (a), stored per state and class for the working, middle and upper classes.

**Q60. Who invests, and out of what (M03 and M09, from Q36 and Q39).** Proposed: the middle and upper classes put a share of their after-tax income into the general pool, before target spending is worked out. Incentives scale the share. The working class, peasants and slaves don't invest. Until M09 builds the pool, the money vanishes, as it does now.
*Recommend:* this.

> **Decided 2026-11-12:** as recommended.

**Q61. Reading laws before the politics rework lands (M02 onward, from Q12 and Q50).** The new laws are skeletons: empty modifiers, `allowed = { always = no }`, and an `on_add` that sets `current_law@token:<category>`. No country history sets them yet. The old laws (`0_eoanb_demographic_laws.txt`, `0_eoanb_economic_laws.txt`) are the ones in play. M02 already needs slavery legality, and the qualification cuts need citizenship and social mobility (`law_serfdom`).
- When will country history start setting the new laws?

*Recommend:* economy code reads laws only through small scripted triggers, such as `eco_slavery_legal`. Each one checks `current_law@token:...` and falls back to the old ideas until the new laws are set, so the switch happens in one place.

> **Decided 2026-11-12:** read from the new laws only, with no fallback to the old ideas. Laws act on the economy through modifiers in `modifier_definitions`, which support yes/no values (`value_type = yes_no`, as `state_land_allowed` does). The default is that slavery is allowed: the modifier marks the ban, so it comes from banning slavery, not from allowing it. Until country history sets the new laws, every country counts as allowing slavery, and only marginalised cultures can be enslaved anyway.

**Q62. Slaves in the labour market (M02, from Q12).** Slaves get no income, so a slave job costs its employer nothing. Do slaves count as labour supply for the state's floating wage? If they do, plentiful slaves hold down free working-class wages, which is historically right, and farms in slave states are very profitable.
*Recommend:* slave jobs cost nothing, and slaves count in the labour supply that sets the wage.

> **Decided 2026-11-12:** yes.

**Q63. Crop eligibility and land quality without a land pass (M05, from Q24 and Q26).** Q24 keeps the population fallback for arable land, so there's no land-generation pass for crop eligibility to share.
- (a) A script writes crop eligibility into marked history blocks for every state, from province terrain (`map/definition.csv`) and latitude. Land quality defaults to 1 unless history sets it.
- (b) Every crop is eligible everywhere unless history says otherwise.

*Recommend:* (a). With (b), cotton grows in Scotland until someone writes the data.

> **Decided 2026-11-12:** neither. Uncommon crops default to not eligible, and history makes them eligible where they grow. Common crops default to eligible. There's no generator script. Which crops count as uncommon is Q71.

**Q64. What the Manufacturing Base comes from, and what it costs (M08, from Q32 and Q33).**
- Is it derived from manufacturing capacity, or from real output (capacity × utilisation, valued at base prices)?
- Does the government pay for its factories? Does a military allocation take output away from civilian goods?

*Recommend:*
- Real output of the manufacturing sectors at base prices, ÷ a constant per factory, so idle plants and price swings don't create factories.
- Under (c), no payment and no cut to civilian output. Military production already pays through the goods `calculate_military_demand` buys. Option (b) adds both later.
- Offmap counts are set with `add_offsite_building`, split by a national civilian / military / naval allocation.

> **Decided 2026-11-12:** real output, as recommended. There's no cut to civilian output for now; that may come later. Not as recommended: the state does pay to sustain the "contract", as a monetary cost per factory in the budget.

**Q65. Base money comes before banking (sequence, M11 and M12, from Q44, Q45 and Q49).** Reserves need base money, which was planned for M12. Separately, Q45 gives each market one currency, but Q44 talks about a country's base money.

*Recommend:*
- Move base money and minting into M11. M12 keeps the price level, money demand, inflation's effects, valuables reserves, the trade balance and exchange rates. P is 1 until M12, so seigniorage equals the minted amount until then.
- Base money is held per market, and only the market leader mints. Each member country's bank takes reserves from its GDP share of the market's base money × its own banking confidence.

> **Decided 2026-11-12:** yes, plus a transition for a country that leaves a market. It takes a share of the market's base money equal to its share of the market's GDP. Money and money demand then move in proportion, so neither side's price level or inflation rate jumps. Follow-up: Q69.

**Q66. How companies fail (M10, from Q40).** Strat's notepad ("Failing Companies") has two routes, a player bailout, and laws deciding what's allowed:
- **Chapter 11 reorganisation:** 6–24 months with dividends suspended, throughput bonuses halved, no expansion, a valuation hit, and shares passed to creditors.
- **Chapter 7 liquidation:** assets are sold, and shareholders get nothing.

The politics rework has insolvency laws (`insolvency_law_tokens`: peonage, debtors' prison, creditor liquidation, bankruptcy discharge, bankruptcy, debt restructuring). The MVP has no shares or valuations.
*Recommend:* M10 builds liquidation and the player bailout. Liquidation sends capacity to the generic owner, and writes loans off against bank capital once M11 exists. Reorganisation goes to the backlog until shares exist, gated by the insolvency laws.

> **Decided 2026-11-12:** yes.

**Q67. What inflation erodes (M12, from Q46 and Q52).** Proposed:
- Each month, nominal stocks are rescaled by P_old ÷ P_new: the treasury, domestic government debt, bank loans, pop debt, and the floating base wage, which then recovers through utilisation.
- Bank reserves follow base money ÷ P.
- High inflation costs stability.
- Foreign debt is owed in another currency, so domestic inflation doesn't shrink it. It moves with the exchange-rate scalar instead.

*Recommend:* this list.

> **Decided 2026-11-12:** yes, except for foreign debt: it shrinks with *foreign* inflation, the inflation of the currency it's owed in, and also moves with the exchange rate. Follow-up: Q70.

**Q68. Active deposits and RGO size (M06, from Q28).** Is `active_deposits` the same thing as an RGO's size, one unit each, or a separate stock?
*Recommend:* the same value, stored once as the size. Known deposits minus size is what investment can still open up.

> **Decided 2026-11-12:** yes.

---

## Second follow-ups (raised 2026-11-12)

These come out of the answers to Q55–Q68. Strat answered them on 2026-11-12.

**Q69. Joining a market (M11 and M12, from Q65).** Leaving is settled: the country takes the market's base money × its share of the market's GDP. Joining is the mirror image:
- The joiner's base money converts into the market's currency at the ratio of price levels (M × P_market ÷ P_joiner), so the money keeps its real value. If both sides had settled price levels, the merged price level doesn't jump.
- Commodity reserves (valuables) back the currency, so they move the same way: a leaver takes its GDP share, and a joiner adds its own.
- Bank money needs nothing, since each country keeps its own bank.

*Recommend:* this.

> **Decided 2026-11-12:** yes to all three. Each country's share of its market's base money is needed every month anyway, because the part of base money inside a country is what counts toward its bank reserves (Q44). Leaving and joining just reuse that share.

**Q70. Which foreign inflation shrinks foreign debt (M12, from Q67).** Foreign debt in `national_debt_update` has no creditor, so there's no particular foreign currency for it to follow.
- (a) A world price level: the GDP-weighted average of every market's P. The exchange rate is taken against it too.
- (b) The currency of the largest market (Britain's in 1857).
- (c) Record the creditor market for each debt.

*Recommend:* (a). It's one global value, with no new data per debt.

> **Decided 2026-11-12:** (c). A foreign loan comes from a specific creditor: Mexico starts with loans from the UK, Spain and France, for example. Each debt follows the inflation of its creditor's currency, and the exchange rate between the two currencies. The context above was wrong, and the data already works this way: `national_debt_update` stores debt per creditor as `debt_to_bank_k@<tag>`, over the `debt_to_bank_country` array, and Mexico's decisions read `debt_to_bank_k@ENG`, `@FRA` and `@SPR`. Follow-up: Q72.

**Q71. Which crops are uncommon (M05, from Q63).** Six farm sectors use land. Proposed:
- **Common, eligible unless history says no:** crop farm and livestock ranch.
- **Uncommon, eligible only where history says yes:** rice paddy, cotton plantation, luxuries plantation and rubber plantation.

*Recommend:* this. Rice counts as uncommon because outside monsoon Asia it grows in only a few places.

> **Decided 2026-11-12:** as recommended. Crop farm and livestock ranch are common, and everything else isn't.

---

## Final question (raised 2026-11-12)

**Q72. Who receives interest on foreign debt (M11 and M12, from Q70).** The debt is stored per creditor, but `national_debt_update` adds all foreign debt together, charges one `foreign_interest_rate` on it, and pays the interest to no one. The disabled bank was built to hold loans to other countries (`bank_lent_to_countries_k`). Q43 keeps domestic government bonds outside the bank for now.
- (a) The interest disappears, as now (Q52), and a default hurts no one but the borrower.
- (b) The creditor country's bank holds the debt as a loan. The interest is bank income, charged at that bank's lending rate plus a premium for the borrower's credit rating. A default hits that bank's capital, so a Mexican default squeezes credit in Britain.
- (c) The interest goes to the creditor's general investment pool, as bondholders' income.

*Recommend:* (b), from M11 onward. Until then the interest disappears. It ties financial crises across borders, as the spec wants instability to come from finance (§14), and the old bank already has the structure. Q43's domestic bonds stay outside the bank.

> **Decided 2026-11-12:** (b).

---

## Pops and labour follow-ups (raised 2026-11-12, M02)

These came up while reading the code for M02. Two findings first, because they change what the M02 baseline means:
- **Capitalists never exist.** `employment_update` adds each industry's owner jobs from a temp, `i_owner_jobs`, that nothing sets, so no industry has owner jobs. The capitalists start with no workforce, `pops_update` skips them, and their dividends reach no one. In Strat's July 1857 save, ENG's capitalists are booked 2,132 a month in dividends, with no workforce and no earnings. ENG's 94K landowners have no jobs either, so all of them count as unemployed. M02 rewrites this code, so the upper class gets its owner jobs and that income. GDP, prices and sales tax will move against the baseline for this reason alone.
- **The demographics code's state culture tallies don't work.** `is_owner_primary_culture` and the other `is_owner_*_culture` triggers check `culture_temp`, but the loop in `sort_state_culture` sets `cc`. `is_owner_marginalized_culture` reads `OWNER.pops_primary_marginalized_array`, which doesn't exist. The tallies are also refreshed only when an effect changes a state's cultures, never at startup. M02 computes its own culture shares from `pops_culture_array`, so it doesn't depend on them. Strat: leave the demographics code alone.

**Q73. Where slaves come from (contradiction).** No state history sets slaves, so every state starts with none, and nothing creates them. Q12 and Q61 say only pops of marginalised cultures can be enslaved, and that every country counts as allowing slavery until history sets the new laws. ENG's 1857 history marginalises the Irish (USA and CSA marginalise African Americans; BRA and ARG Afro-Brazilians, pardos and Amazonians; TAI the Manchu). So a rule that enslaves marginalised pops by itself would enslave Ireland.
- (a) History sets a starting slave share for each state, as a share of its workforce. Afterwards slaves change only through population growth and emancipation, and nobody is newly enslaved. Each month the slaves are capped at the state's marginalised-culture share, or at 0 where slavery is banned. Freed slaves become working class.
- (b) At startup, every marginalised-culture pop becomes a slave wherever slavery isn't banned. That needs Britain and others to ban slavery in their history first, which needs the new laws.
- (c) Free marginalised pops become slaves each month at some rate, where slavery isn't banned. Same problem as (b).

*Recommend:* (a). In 1857 the big slave populations (the US South, Brazil, Cuba) grew by birth, and the Atlantic trade was nearly closed. To test it while the map is stripped: put the 1860 census shares into a few US southern states (Virginia about 31%, South Carolina 57%, Mississippi 55%), in a marked `# >>> rework test slaves` block. The test bed is British, and Britain has no slaves.

> **Decided 2026-11-12:** (a), with the test shares in a few US southern states. Strat notes that Britain would start with slavery abolished anyway.

**Q74. Do qualifications leave with pops that move down?** The notepad loses qualifications through death, conversion and decay. Its stocks belonged to each pop type, so a pop that changed type took its qualifications with it. Q57 makes it one stock per state, which the middle and upper classes draw on, so there's no type for them to belong to. If a move down still destroys them, every month in which middle-class pops fill working-class jobs destroys qualifications, and industries' hiring swings (+20 / −25 points a month) would wear the stock down.
- (a) As the notepad: a pop that moves down loses its share of qualifications.
- (b) They stay in the state's stock, so the same people can move back up when jobs return. Deaths and decay take a share of the stock each month.

*Recommend:* (b).

> **Decided 2026-11-12:** (b).

**Q75. Qualification inputs are flat today.** The notepad's gains come mostly from literacy, schooling and education. These are state percentages that default to 100 everywhere (`global.pops_literacy_percentage` and the rest), and no history sets them. With the cap model gone, qualifications are the only thing that reads them. At 100, every state gains at the top rate per head, and only wealth, the class mix and the culture cuts make a difference.
- (a) Lower the defaults to rough 1857 world levels (literacy 20%, schooling 10%, education 0.5%), give ENG its own values in country history since it's the test bed (about 60%, 40% and 2%), and set everyone else in M14.
- (b) Keep 100 until M14.

*Recommend:* (a). Otherwise qualifications can't hold anyone back, which is their point (Q10).

> **Decided 2026-11-12:** (a).

**Q76. Culture cuts before the laws exist.** The notepad cuts gains by law: under slavery laws −100% for oppressed cultures and −50% for non-accepted ones, down to −40% and 0 under full equality. In the code's four culture tiers, oppressed is marginalised and non-accepted is normal: anything not primary or promoted. No country has the new laws yet (Q61).
- (a) A base cut from culture status alone, since marginalisation is already history data. Modifiers that the citizenship and slavery laws set later change it.
- (b) No cut until the laws set modifiers.

*Recommend:* (a), starting from the notepad's middle row, limited equality: −50% for marginalised cultures and −10% for non-accepted ones. The serfdom cut for peasants is a law, so it's a modifier with no effect until history sets the law.

> **Decided 2026-11-12:** (a).

**Q77. What the bureaucrats' pay replaces.** `administration_spending` is now 0.5% of pop earnings, plus `administration_cost_per_c` × population and `administration_cost_per_gdp` × GDP, all × (1 + `administration_cost_factor`) and ÷ bureaucratic efficiency. It pays no one. ENG's is about 220 a month, of which the earnings term is about 50 before the factors. The bureaucrats' pay is filled jobs × their class's wage multiple × the state's base wage, and it goes to them as wages. At about 1.5 jobs per 1,000 people (Britain had roughly 40,000 civil servants for 28 million), ENG's payroll would be about 350 a month.
- (a) The payroll replaces the earnings term. The per-capita and per-GDP terms, the cost factor and efficiency stay, applied only to those terms, so content that uses them keeps working and the payroll paid equals the wages received.
- (b) The payroll is added to today's line.
- (c) The payroll replaces the whole line, and the modifiers are reworked to act on required jobs.

*Recommend:* (a). M13 can do (c) when it reworks the budget.

> **Decided 2026-11-12:** (a).

**Q78. Does administrative capacity cut taxes in M02?** Capacity = filled ÷ required bureaucratic jobs. The politics notepad has a shortage cut tax effectiveness and spending effectiveness. Nothing in the code models spending effectiveness yet.
- (a) M02 applies capacity to income, sales and corporate tax collected, so a short bureaucracy loses revenue. How strongly is tuning. Spending effectiveness waits for M13.
- (b) M02 only stores capacity, and M13 applies it.

*Recommend:* (a). Otherwise the bureaucracy costs money and labour from the day it exists but changes nothing.

> **Decided 2026-11-12:** (a).

**Q79. Merging the owners' investment modifiers.** The upper class replaces capitalists and landowners, but `capitalists_investment_contribution_factor` and `landowners_investment_contribution_factor` are used in about 30 places of content: ideas, leader traits, decisions, balance of power and static modifiers. M03 decides who invests (Q60: the middle and upper classes).
- (a) Merge them now into `upper_class_investment_contribution_factor`, adding the two values where a block has both. M03 adds the middle class's.
- (b) Keep both until M03, with the upper class using the capitalists' one.

*Recommend:* (a). The diverted money disappears until M09 anyway, so for now the only effect is on how much the upper class spends.

> **Decided 2026-11-12:** (a).

**Q80. Bureaucrats against the speed target (contradiction).** M02's "done when" asks for the pop pipeline to cost about half what it does now. In the baseline (`runs/m02_base`, 60 months) it costs 12.6 s of the 42 s country tick: `pops_update` 4.6 s, `employment_update` 3.4 s, `update_country_pop_stats` 2.0 s, `on_monthly_pops` 1.6 s and `pops_balance` 0.8 s. `pops_update` already skips pop types with no workforce, and the stripped map's states mostly have two (peasants and landowners). Going from ten types to five halves the loops over every type, but Q58 puts bureaucrats in every state, so almost every state gains a middle class: a third active class, and about 1.4 s more of `pops_update`.
- (a) Keep Q58's spread. M02's target becomes "no slower than now", and the rest of the speed-up comes in M03, which refactors `get_pop_needs` (1.8 s) and removes the savings steps.
- (b) Put bureaucratic jobs only in states above a population threshold, or only in each country's largest states, so most rural states have no middle class.

*Recommend:* (a). (b) would put whole provinces outside the administration, which Q58 didn't intend.

> **Decided 2026-11-12:** (a).
>
> **Measured (M02, 2026-11-12):** run against the old code under the same conditions (`runs/m02_base_rerun`), the pop pipeline costs 13.3 s against 14.0 s, 5% less. `pops_update` grew 27% for the extra class, and every loop over the pop types halved. Details in M02's Results.

## Wealth and demand follow-ups (raised 2026-11-12, M03)

These came up while reading the code for M03, together with a bug Strat reported: sparse states with plenty of land start almost entirely upper class (Q84). The baseline is `runs/m03_base` (`world_1857_eng`, 60 months, `--watch-file watches/m03.txt`).

**Q81. The startup overspend becomes debt (contradiction).** Startup sets each class's wealth against base prices, before the markets open and before the first tick sets bonuses, dividends and taxes. So at month 0 London's pops spend about three times what they earn (working class 866 against 299, upper class 1,163 against 206), and they keep overspending until wealth catches up in month 3. Today that gap is money from nowhere. Under Q15 and Q59 it all becomes debt: about 930 for London's working class (1.5 months' income) and 1,470 for its upper class. At today's repayment rate, 4% of the debt a year, it takes decades to clear, and it lowers confidence by under 1% through the debt-service penalty.
- (a) Accept it until M14, which balances the start.
- (b) No borrowing in the first tick, whose figures come from startup. That removes about 60% of it.
- (c) Set starting wealth at actual prices at the end of startup (`_state_fin`). Month-0 earnings are understated, though, so classes would start too poor and climb back over a few months, and month-1 wealth would no longer match M02.

*Recommend:* (a). Until M14, debt is only being tested as a mechanism.

> **Decided 2026-11-12:** (a). Accept it until M14.

**Q82. Classes that can't borrow.** Target spending is earnings × consumer confidence, and ENG's confidence is 108.7: 100 at peace, plus the stability bonus. So every class aims to spend about 9% more than it earns, every month. The working, middle and upper classes borrow the difference (Q59). Peasants can't borrow.
- (a) Cap peasants' target at their income. Confidence above 100 can't make them overspend, and below 100 it still cuts their spending.
- (b) Leave it. Peasants overspend and owe nothing, which is money from nowhere.

*Recommend:* (a), so spending above income always becomes debt. Peasants sit at the wealth floor until M05 anyway.

> **Decided 2026-11-12:** (a). Peasants' target is capped at their income.

**Q83. Earnings become gross income.** Q36 and Q60 take investment out of income that has already paid income tax. The budget works out income tax from `pops_earnings`, so `pops_earnings` has to be gross income. Today it's net of investment: the upper class's investment is taken off before tax. Gross earnings raise ENG's `pops_earnings_avg` by about 13% (its upper class invests about 1,460 a month). That average also sets military payroll, the research cost, the tax brackets and the trade AI's productivity bounds.
- (a) `pops_earnings` is gross income, and investment is one of its uses, like spending. Accept the knock-ons.
- (b) Keep `pops_earnings` net of investment, and add a second variable for the tax base.

*Recommend:* (a). Everything that reads earnings means gross income.

> **Decided 2026-11-12:** (a). Gross income, and accept the knock-ons.

**Q84. Subsistence owner jobs (Strat's bug report).** Owner jobs on subsistence land are 2% of the land's capacity, not of the peasants who farm it, and startup fills the upper class before it counts the peasants. So a sparse state with plenty of land becomes all upper class. In the simulator, South Dakota's upper class is 4.46K of its 4.49K workforce. 121 states start above 10% upper class, and 42 above 50%. Nothing else causes it: excluding these jobs, only Washington DC (senior government jobs, 9%) is above 5%. The fix: owner jobs follow the peasants, and startup takes the landowners out of the peasants after the other classes have their jobs. Which peasants count?
- (a) Those on the arable land, up to its capacity. States with more peasants than land don't change: London keeps 13.8K.
- (b) All peasants, including those on marginal land. Crowded states gain landowners: London goes from 13.8K to 24.5K, and India and China gain the most.

*Recommend:* (a). It changes only the states that were wrong.

> **Decided 2026-11-12:** not as recommended. (b): owner jobs are 2% of all peasants, including those on marginal land.

Saves made before the fix keep their all-upper-class states, because `pops_balance` only moves a surplus into another class's shortfall. Start a new game.

---

## National sectors follow-ups (raised 2026-11-13, M04)

These came out of reading the industry code for M04. Strat answered Q85–Q91 on 2026-11-13.

**Q85. Which industries become sectors.** Q18 makes every industry token a sector. Subsistence farms are worked by peasants on land, and M05 reworks them. Arms factories, industrial complexes and dockyards are always fully staffed and paid by the state, and M08 reworks them.
*Recommend:* leave these four out of the sector layer until their own milestones, so neither is written twice. Sectors cover the 25 buildings, the RGOs, railway and port.

> **Decided 2026-11-13:** yes.

**Q86. Profit tax (step 6).** Corporate tax is now the rate × the upper class's dividends, subsistence rent included, and the upper class pays it (M03). Step 6 has sectors pay profit tax before the retained share.
*Recommend:* each sector pays corporate tax on its positive operating profit only, with no tax on losses and no carry-forward. Dividends and subsistence rent aren't taxed again, so rent goes untaxed until M05 decides land rent.

> **Decided 2026-11-13:** yes.

**Q87. Capacity decay before investment (step 7).** The old downsizing was switched off along with investment, because nothing could rebuild what it shed.
*Recommend:* build decay and test it in the simulator, but gate it behind `global.eco_investment_enabled` until M09. It applies to buildings only: an RGO's size stays tied to its deposits until M06.

> **Decided 2026-11-13:** yes.

**Q88. Owner slices before companies (step 4).** No companies exist in play, because founding is gated off, and M10 rebuilds companies on the MVP.
*Recommend:* M04 builds each sector as the generic owner's slice (the sector minus company-held size), with room for company slices but no code for them. M10 ports the MVP onto it.

> **Decided 2026-11-13:** yes.

**Q89. Per-state goods figures once the state-industry is slim (step 3).** Slimming drops each state-industry's per-good arrays (`production@<industry>^i`, `input_amount@<industry>^i`). Two things are built from them: each state's GDP, Σ (`production@<good>` − `demand_input@<good>`) × price, and the market screen's five biggest producing and consuming states per good. National supply and demand could come from the sector records instead.
- (a) Keep per-state goods totals. Each state-industry still adds its goods into its state's `production@<good>` and `demand_input@<good>` once a month, but stores no arrays of its own. Everything that reads them keeps working.
- (b) Drop them. State GDP becomes Σ (revenue − input cost) over its industries, the same number, and national supply and demand come from the sectors. The market screen lists producing countries only, or works out its states when it opens.

*Recommend:* (a). Since the market now adds up each state once a month instead of five times, the per-good loop is cheap, and it keeps the market screen and the GDP as they are. (b) saves about 45 variables per state.

> **Decided 2026-11-13:** (b), not as recommended. Iterating over every good for every state is the cost to cut. State GDP is each industry's value added (revenue less goods bought), summed per state. The market loses its per-state lists, which only partly worked; the sectors list their biggest states instead.

**Q90. Which per-industry figures stay stored (step 3).** The industry tooltips show revenue, expenses, payroll, maintenance, profit, profitability, productivity, jobs per class and the goods made and used. `sectors_update` adds up revenue, inputs, payroll, maintenance and employment from what each state-industry stores, rather than inside `industry_update`, because content, construction and the GUI also run `industry_update` mid-month.
- (a) Keep the money figures (revenue, input cost, payroll, maintenance, profit and margin) and employment per class. Drop the rest (jobs available, the payroll multiplier, the transport maxima, `asset_value@`, `productivity@`), working them out in the scripted localisation when a tooltip needs them.
- (b) Keep only the spec's list (size, employment, PM/AM, ownership, a trailing margin, construction state), and work every money figure out on demand. `sectors_update` would then add up during the state loop, and mid-month recomputes would need a guard against double counting.

*Recommend:* (a). About ten variables per state-industry, and the national accounts stay correct whatever calls `industry_update`.

> **Decided 2026-11-13:** keep only what calculations need, where dropping it would cost performance. Anything only the localisation reads goes, and the scripted localisation works it out. Something that has to be worked out anyway can be stored.

**Q91. National sector figures for the UI.** The national sector screen should show most of what the state-industry tooltips show, plus the sector's own accounts. Most of it is stored or derivable already. Six things aren't (the gaps in the M04 file's "National sector UI" section): jobs and employment per class, the method mix, goods used per good, transport, construction under way, and reserves. Q90 would have the localisation work them out, but at national level that means looping over every state for every figure each frame the screen shows. A screen with 30 sectors would loop every state and industry thousands of times a second.
- (a) Store them monthly in the passes that already visit every state-industry (`sectors_update`, `national_market_states_update`). That's about ten values and four short arrays per sector, and a few additions per state-industry a month. Gap 3's arrays would replace `method_scale@`, since they hold the same sums split by sector.
- (b) Work them out in the scripted localisation by looping over the country's states when the screen shows them. Nothing is stored, but every visible figure loops every state each frame.
- (c) Store the cheap sums (gaps 1, 4, 5, 6) and leave the method mix and goods used (gaps 2 and 3) to the localisation.

*Recommend:* (a). By Q90's own test (performance) these belong in storage at national level. They're cheap to add up in passes that already run, and costly to rebuild in the GUI.

> **Decided 2026-11-13:** (a).
