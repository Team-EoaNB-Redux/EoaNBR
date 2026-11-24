# M13: Government, laws and player controls

**Spec:** §20, §21, §22. **Depends on:** M02–M12. **Questions:** Q50, Q51, Q61, plus Strat's detailed budget clarification on 2026-11-17. **Status:** implemented and simulator-tested; not fully signed off: universal AI solvency and the in-game smoke test remain open. UQ26 is implemented as a separate public-works cost.

## Goal

Bring the budget into line with the new pops, sectors and finance, and add the national controls each system needs. Laws decide which controls a country may use and who sets the targets. They don't replace the economic systems. Laws come from the politics rework (Q50).

## Implementation plan — 2026-11-17 clarification

1. Replace budget slider calculations with independent VL/L/M/H/VH adjustments (0–4). Interpolate each law's lower and upper cost and effect coefficients at 0, .25, .5, .75 and 1. Taxation-level laws separately multiply tax rates by .25/.5/1/2/3. Defaults remain usable without the new politics laws.
2. Income tax combines four free-class rates, a per-head charge and marginal income slices (below national average, average to three times average, above that). Slaves pay nothing. Laws supply the distribution and a disabling modifier. Asset tax combines used land, wealth-based property, peasant yield and estimated owned capital; exact ownership valuations remain M15.
3. Cache household tax bases and purchased goods during existing monthly aggregation. Sales tax uses selected goods' actual price times financed quantity, excluding home consumption. Per-good import/export tariffs feed both settlement and trade AI. Budget changes do not rescan states for taxes.
4. Give spending lines independent law cost/effect bounds. Bureaucracy changes recruitment targets; welfare transfers reach poor free classes; industrial and infrastructure subsidies reach their recipients. Public works has its own cost and speeds construction. Preserve the existing procurement mechanism and factory contracts.
5. Apply daily political-power upkeep from adjustments: base costs -.02/-.01/0/.02/.05, weighted more heavily for taxation than expenditure. These are ongoing costs, not law changes or click fees.
6. Wire the existing budget mockup to real values and controls, add goods/sector selection and monetary/target-utilisation controls, and enforce restrictions in effects as well as UI.
7. Verify cached calculations, household/treasury and subsidy ledgers, marginal bands, law bounds, controls and idempotence; compare a 60-month world run against `runs/m13_base`, including a debt-enabled variant. Update onboarding and economy documentation. In-game smoke testing needs a fresh load/save after implementation.

Deferred explicitly: daily combat sampling for Operations and stockpile decay from underfunded maintenance. Literacy/education hooks use existing demographic systems where available. Values are provisional mechanism tuning until M14; no map or generated PM changes.
## Starting point before M13
- **Budget:** the sliders, taxes and spending lines are in `_economy_budget.txt`. The AI runs `ai_budget`, and the `budgetary_spending` dynamic modifier turns the sliders into HOI4 bonuses. The UI rework's phase U1 replaces the sliders with five levels per line before this milestone (ui_planning.md §3.5).
- **Old economic laws:** trade, mobilisation, tax rates, child labour, work hours and land property (`0_eoanb_economic_laws.txt`). The new set replaces them.
- **New laws:** `toi/common/ideas/_internal_politics_tokens.txt`. Each law sets `current_law@token:<category>`. They're still skeletons, with empty modifiers and `allowed = { always = no }`, and no country history sets them yet. The economic categories are:
  - **Economic system:** customary, agrarian, extraction, rentier, free-market capitalism, state-guided capitalism, market socialism, command economy.
  - **Money and finance:** monetary system, financial system, financial regulations.
  - **Industry and markets:** property law, industrial policy, regulatory structure, corporate affairs, commodity regulations, land development.
  - **Trade and foreign capital:** trade, foreign direct investment.
  - **Tax:** personal taxation, asset taxation, taxation level.
  - **Labour:** work hours, worker protections, labour associations.
  - **Society and state:** bureaucracy, insolvency law, social mobility, slavery, citizenship.
- **Bureaucratic capacity** (from M02) is meant to drive tax and spending effectiveness (`vanadiums_notepad_while_hes_crashing_planes.txt`).
- **Debt:** domestic and foreign, ending in bankruptcy at about 200% of GDP.

## Build
1. **Budget rework** against the new classes, sectors, bureaucratic payroll, active manpower and the Manufacturing Base. Debt is sized to GDP. Tax and spending effectiveness come from bureaucratic capacity.
   - **Funding effects** (UQ18). Extra funding on a funding line buys, scaled by its funding factor: personnel, army morale and recruitable manpower; administration, administrative capacity and so tax collection; law and order, stability and resistance suppression; education, the qualifications stock's growth; healthcare, population growth; public works, construction speed of HOI4 buildings (`production_speed_buildings_factor`) and of industries (`industry_construction_speed_factor`). Any of them can come sooner, since each stands alone.
   - **Public works' base cost** (UQ26, open): its own per-head and per-GDP cost, as the other public services have, so it never costs nothing while still speeding construction. The country projects' cost stays in construction spending.
2. **Economic effects for the new laws:** what each economic-system law unlocks (§22), plus the coefficients the other categories set (financial, monetary, incentives, slavery, qualifications). Laws act only through modifiers in their `modifier` blocks, defined in `00_economy_modifiers.txt`, with `value_type = yes_no` for switches (Q61). The economy reads the modifiers, never the law tokens. Defaults are the permissive case, so a modifier marks a restriction, as the slavery ban does.
3. **The controls in scope** (Q51), with defaults the AI can live with:
   - existing: the budget lines and tariffs, as levels since U1;
   - new: sector subsidies (not sector taxes, UQ20), government investment, target utilisation (planned economies), the policy rate, the reserve requirement and minting, and the Manufacturing Base allocation.
4. GUI for the new controls, as ui_planning.md plans them (§8, With M13).

## Done when
- Each control in scope has a visible effect in the simulator.
- AI budgets stay solvent over 60 months, with debt switched back on in a test copy.

## Implemented behaviour (2026-11-18)

The new **Budget** button in the existing economy window opens the functional budget panel. Back returns to the existing screens, including factory allocation and borrowing. No new law is enacted by a budget button. New politics laws retain their existing availability/history rules; M13 supplies modifiers without making the politics rework available prematurely. The narrow Q51 controls are implemented; ownership transactions, bankruptcy policy and company strategy controls outside Q51 remain later content/M15–M17.

### Rates, bounds and upkeep

Every budget line has a persistent adjustment 0–4 (VL through VH), normally defaulting to M. Interpolation uses `adjustment / 4`. Spending law modifiers `eco_<line>_cost_per_k_min/max`, `cost_per_gdp_min/max` and `effect_min/max` are **additive endpoint deltas** to the no-law defaults in `budget_clamp`. Thus explicit zero endpoints are possible without using zero to mean "unset". Costs are monthly real money: 0.1 per thousand people means £100 per thousand people, not £100 per person. Benefits are multiplied by administrative capacity, capped at 1. Specific benefit endpoint deltas also exist, e.g. `eco_personnel_army_morale_min/max`, `eco_personnel_manpower_min/max`, `eco_order_stability_min/max` and `eco_order_resistance_min/max`.

Universal Healthcare sets effective cost endpoints 0.1–0.18 and growth endpoints 0.3–1.2. Its five cost values are .10/.12/.14/.16/.18; growth is .30/.525/.75/.975/1.20 before administrative effectiveness. These are mechanism values, not an 1857 balance pass.

The independent taxation-level multiplier is `1 + eco_tax_level_factor`: minimal −.75, low −.5, moderate 0, high +1 and extreme +2 give ×.25/.5/1/2/3. It applies to income, asset, corporate and sales taxes and tariffs. Actual collection uses the existing tax-efficiency and administrative-capacity calculation. Collection and corruption are separate; existing corruption reduces treasury receipts after the payer's deduction.

Daily PP upkeep uses −.02/−.01/0/.02/.05. Each of the four tax rows weighs 4, each spending row 1, and each import/export good adjustment .5. Negative upkeep is a PP benefit. Tariffs use the same convex schedule. Patronage adds its separate PP benefit. There are no click charges. `infrastructure_budget_level` deliberately avoids the engine getter named `infrastructure_level`.

### Tax bases and settlement

- **Income:** four rates, `income_tax_rate@<free class>`, plus `income_tax_per_head`, plus three marginal slices. Rates come from `eco_income_tax_<class>`, `eco_poll_tax`, and `eco_income_slice_low/middle/high`. Default class rates are 10% before the adjustment, law multiplier and collection. Slices span 0–average, average–3×average, and above; `eco_income_band_multiple` adjusts the upper threshold. `eco_income_tax_disabled` disables every component. The class plus marginal percentage is capped at 95%; poll taxes remain a separate charge. Gross wages, base income and dividends are taxable; welfare and patronage transfers are added afterward. Slaves have no tax bases or payments.
- **Assets:** `eco_asset_land/property/yield/capital` independently set components. Land is quality-weighted commercial use plus half subsistence land for upper-class owners, and half subsistence land for peasants. Property proxy is wealth level × population × .1. Yield is the peasants' subsistence payroll. Capital is private generic-sector and company assets plus cash minus debt, excluding SOEs, allocated across upper-class households. This is an ownership proxy until M15 records shareholders; it does not claim to distinguish individual owners. The no-law default asset rates are zero.
- **Corporate:** positive generic-sector profit and each company's positive profit; company holdings are excluded from generic profit. The forecast responds immediately to rates without visiting states. Settlement uses the actual corporate deductions that produced retained earnings/dividends.
- **Sales:** all goods default to taxable; `sales_tax_exempt@<good>` is the selection. `household_goods@<good>` caches financed purchased quantities, not industrial inputs or home-grown peasant consumption. Revenue is the sum of quantity × actual price × actual tax rate. Household basket quotation applies the same selection, and credit rationing scales goods and sales tax together.
- **Tariffs:** `import_tariff_level@<good>` and `export_tariff_level@<good>` feed actual settlement and the trade AI's profit/quantity calculation. New trade laws set endpoint bounds; negative bounds support subsidies. Public enterprises retain the M10 dividend source.

State/class tax bases are refreshed alongside normal pop updates and summed by `update_country_pop_stats`. Goods are summed by the existing market aggregation. Government construction costs are cached monthly too. Clicking a tax level or goods picker never visits states, changes their credit reservations or advances a project.

Budget figures are forecasts. `government_budget_commit` closes each monthly tick using actual household and corporate deductions and actual queued welfare/patronage transfers, and stores the primary balance due. The next tick settles that balance minus freshly calculated debt interest. Button clicks do not rewrite committed cash. Sector/company grants and development funding have matching committed amounts; cash promises erode with M12 currency revaluation. This preserves the existing one-tick financial lag. Construction and service cost estimates otherwise retain their existing accounting conventions.

### Spending and controls

| Line | Cost base and effect |
|---|---|
| Operations | Existing unit operating costs, interpolated activity multiplier (.25–1 by default); organisation/combat readiness. Daily combat sampling deferred as requested. |
| Procurement | Actual military goods, using the existing production-cost/efficiency relationship; independent adjustment. |
| Maintenance & repair | GDP/population cost endpoints; equipment reliability. Stockpile decay deferred as requested. |
| Personnel | Active manpower and earnings benchmark, independent cost multiplier (.5–1.5); morale and recruitable manpower. |
| Patronage | GDP/population funding transferred to upper-class households; political power. |
| Intelligence | Agency maintenance multiplied by 1 + .1 per upgrade (up to 50); no agency means no spending or benefit. Engine upgrades sampled monthly, not daily. Army/navy/air intelligence benefits. |
| Bureaucracy | Actual bureaucratic payroll plus law programme costs. Funding scales recruitment targets, while administrative demand remains independent of that funding. Education, health, policing and welfare add programme strain. |
| Construction | Existing government construction, retooling, prospecting and project bills. Funding scales government construction speed and its quoted bill consistently. |
| Law & order | Stability and resistance target. |
| Education | Monthly literacy, schooling and education gains, plus qualification growth; each has separate benefit endpoint modifiers. |
| Healthcare | Engine population-growth modifier. The simulator does not grow state populations. Disease integration remains outside the current disease system. |
| Welfare | Per-head transfers to peasants and working-class households; no transfers to slaves. |
| Public works | Its own population/GDP cost, even without a construction project; separate HOI4-building and industry-construction benefits. |
| Research subsidies | Research speed. |
| Infrastructure subsidies | 20% of the envelope pays for baseline capacity support; remaining funding goes to railway/port owners, including companies. No recipients means no owner grant, not a free baseline benefit. |
| Sector subsidies | Selected sectors' generic owners and companies receive capital grants proportional to holdings. Actual distributed grants determine spending; no double distribution on a UI refresh. |
| Development fund | Government contribution to the general investment pool, settled at the committed amount. |

The sector picker controls subsidy eligibility. A national utilisation override replaces the market target where permitted; Auto clears it. Free-market and other non-planned laws restrict utilisation overrides, and free-market capitalism also restricts targeted sector subsidies/direct development funding. Monetary buttons call the documented minting/policy-rate/reserve effects, which enforce restrictions themselves. Independent central banks disable direct rate changes and minting. Backing rules still govern actual issuance. Existing Manufacturing Base allocation remains accessible from the original screen.

AI adjusts monthly in response to deficits: raises tax adjustments, lowers discretionary funding, and maintains/increases bureaucracy when administrative capacity is deficient. It never changes laws. This is a default controller for testing, not a guarantee that the stripped M14 map can fund every historical military.

### Verification and limits

- Pre-change reference: `redux-eco-sim/runs/m13_base`, 60 months on `world_1857_eng`.
- Integration tests: `python tools/test_m13.py` inside the simulator. Covers law bounds/multipliers, marginal slices, asset components, selected goods, PP upkeep, restrictions, agency upgrades, grants/commit idempotence, tariffs, education/bureaucracy and household/treasury reconciliation.
- Regression suites: `tools/test_m11.py`, `tools/test_m12.py`; native tests include an agency-input golden case. The simulator reads explicit agency inputs (`sim_has_intelligence_agency`, `sim_agency_upgrades`); it does not simulate agency construction/upgrades.
- The full-mod parser still has the same nine pre-existing errors in six unrelated files. New economy parse/load errors are unacceptable. Old economy division warnings remain separately visible.
- Fresh in-game verification is still required: open Budget, change each type of control, inspect enabled/selected states and tooltips, check `error.log`, and save startup plus two monthly ticks. Existing M12 saves predate M13 and are not evidence for it. No claim of an in-game pass is made.

### Final recorded results (2026-11-18)

`runs/m13_release` is the final 60-month player-ENG run; `runs/m13_release_debt` is the all-AI run with `global.eco_debt_enabled=1`, without changing the mod's debt-off default. Both include `final.json`; `tools/analyze_m13.py m13_release m13_release_debt` writes `fiscal_audit.md`. Earlier `candidate`, `final` and `verified` run names precede fixes and are not the final reference.

- All **11 M13 integration cases pass**, including household/treasury reconciliation. All **11 M11** and **12 M12** regression groups passed. Native tests: **18 cases, zero failures**. The parser has only its **nine pre-existing errors in six unrelated files**. Both final runs have no new economy load errors, unknown effects/triggers, overflow or invalid-scope diagnostics; existing division/array warnings remain.
- Final recorded cost: **11,452,600 ops/month**, versus **10,808,201** before M13: **+5.962%**. Tax and spending quotation got cheaper; richer policy interpolation and household accounting account for most added work.
- Player ENG: final monthly GDP **7,649.858**, treasury **−155,619.957**, forecast net budget **−4,467.373**, compared with baseline net budget **−9,241.0**. This is a mechanism comparison on the stripped map, not balanced starting conditions.
- **The universal AI-solvency acceptance criterion is not met.** Of 329 countries with monthly GDP above 1, the debt-enabled final run has **15 negative treasuries below −1** and **14 debt levels above 49.9**. ENG/FRA/USA/PRS/AUS finish with nonnegative treasuries; their debt levels are 21.153/14.385/.365/46.402/12.149 respectively. The audit lists failures, led by SWE/DEN/HBC. Some legacy bankruptcy-event triggers also execute at reduced simulator fidelity, so this is not an in-game bankruptcy proof. Do not erase deficits with unbacked money, silently change laws, or rebuild the stripped map merely to make this test green. Fiscal balance still needs explicit follow-up alongside M14.

M13 is therefore **implemented, with validation outstanding**, not "done". The remaining checks are real in-game UI/loading and startup/two-tick saves, plus the unresolved all-AI fiscal-solvency condition.

### AI follow-up (2026-11-18)

All **12 M13 integration cases pass** after this correction, including the new AI asset-tax case.

The deficit controller now raises asset-tax adjustments alongside income, corporate and sales taxes. Previously it omitted this revenue line. A regression case checks stepping from M to H to VH and clamping at VH. This does not enact an asset-tax law: the no-law zero asset base rates still yield no revenue. The recorded 60-month references above precede this follow-up; their figures are retained as recorded evidence, not claimed as a rerun.

Inspection of their final stocks confirms SWE, DEN and HBC already have income/corporate/sales adjustments at VH and discretionary funding at VL. SWE's remaining military operations cost is 338.907 monthly; DEN's is 207.564. HBC pays 100 monthly for manufacturing contracts. Their administrative capacity is 1. These are concrete residual cost bases for the M14 balance pass; the asset-control omission alone does not establish a solvency fix.


### M13 control repair (2026-11-18)

Strat's WIP UI is `economy_window_container` / `budget_container` (scripted GUIs `economy_window` and `budget_window`); never rename or hide them. M13's temporary controls are `m13_budget_container` / `m13_budget_window`, and the UI rework replaces them. The game log confirmed earlier errors in `economy_and_demographics.txt` zeroed the M13 button math expressions. Those button calculations now use plain temporary-variable operations; target adjustment starts from current utilisation in Auto mode. Selected-good/sector localisation reads explicit display snapshots, refreshed after clicks and budget quotes, and Auto is displayed distinctly from a manual zero target. Tariff changes refresh rates, then trade, then the budget quote. Simulator checks execute the actual button bodies; a fresh in-game reload is still required to verify rendering.

Legacy national tariff readouts and sliders show the unweighted mean of effective per-good rates, labelled in their tooltips. Their buttons still move every good one level and now refresh trade before quoting revenue. This is a display compatibility bridge, not a return to national flat tariffs.
