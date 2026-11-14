# M13: Government, laws and player controls

**Spec:** §20, §21, §22. **Depends on:** M02–M12. **Questions:** Q50, Q51, Q61, all decided; [ui_planning.md](../ui_planning.md) UQ18 and UQ20, decided 2026-11-14, and UQ26, open. **Status:** not started.

## Goal
Bring the budget into line with the new pops, sectors and finance, and add the national controls each system needs. Laws decide which controls a country may use and who sets the targets. They don't replace the economic systems.

The laws come from the politics rework, not from the old law files (Q50).

## Exists now
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
