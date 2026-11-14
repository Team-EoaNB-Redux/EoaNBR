# Economy rework: index

**Strat's decision, 2026-11-11:** build the economy to the new spec first, then balance the 1857 start. Until then the map stays stripped to subsistence, and a few small test industries in Britain are fine for checking that mechanisms work. Balance waits for M14. Debt is off for every country for the same reason (`global.eco_debt_enabled = 0`, from M00).

- **Target design:** [EOANB_Redux_Economy_Redesign_Updated.md](EOANB_Redux_Economy_Redesign_Updated.md) ("the spec"). The old spec is in [archive/](archive/redux_economy_redesign_spec.md) for history.
- **Decisions:** [decisions.md](decisions.md). Strat answered every question, Q1–Q84, on 2026-11-12. Each milestone lists the questions it depends on.

## Milestones
Each one is a self-contained piece of work for a fresh session. Do them in order, since each builds on the ones before. The order itself is Q1.

| # | Milestone | Spec | Questions | Status |
|---|---|---|---|---|
| M00 | [Test bed](milestones/M00_test_bed.md) | — | Q1–Q5 | Done |
| M01 | [Gradual prices](milestones/M01_prices.md) | §7 | Q6–Q7, Q56 | Done |
| M02 | [Pops and labour](milestones/M02_pops_and_labour.md) | §5, §23–30 | Q8–Q14, Q57, Q58, Q61, Q62, Q73–Q80 | Done; checked in-game (month-1 autosave) |
| M03 | [Wealth and demand](milestones/M03_wealth_and_demand.md) | §24–25, §31–32 | Q15–Q17, Q59, Q60, Q81–Q84 | Done in the simulator; in-game check to do |
| M04 | [National sectors and target utilisation](milestones/M04_national_sectors.md) | §2–4, §6 | Q18–Q23, Q55, Q85–Q91 | In progress: the systems are done, in the simulator and in Strat's month-1 save; the UI rework remains |
| M05 | [Land, agriculture and subsistence](milestones/M05_land_and_subsistence.md) | §10–11, §25 | Q24–Q27, Q63, Q71 | Not started |
| M06 | [Natural resources](milestones/M06_resources.md) | §9 | Q28–Q30, Q68 | Not started |
| M07 | [Infrastructure](milestones/M07_infrastructure.md) | §8 | Q31 | Not started, mostly built |
| M08 | [Manufacturing Base and HOI4 factories](milestones/M08_manufacturing_base.md) | §12 | Q32–Q33, Q64 | Not started |
| M09 | [Investment](milestones/M09_investment.md) | §13 | Q34–Q39, Q60 | Not started |
| M10 | [Companies](milestones/M10_companies.md) | §19 | Q40–Q41, Q66 | Not started |
| M11 | [Banking, credit and base money](milestones/M11_banking_and_credit.md) | §14–16 | Q42–Q44, Q59, Q65, Q69, Q72 | Not started |
| M12 | [Money, inflation and currency](milestones/M12_money_and_currency.md) | §16–18 | Q45–Q49, Q67, Q69, Q70 | Not started |
| M13 | [Government, laws and controls](milestones/M13_government_and_laws.md) | §20–22 | Q50–Q51, Q61 | Not started |
| M14 | [Startup balance](milestones/M14_startup_balance.md) | all | — | Not started |
| — | [Backlog](milestones/backlog.md) | — | — | Small items, any time |

Q52 to Q54 apply across milestones.

**The reasoning behind the order:**
- The test bed comes first, so tests aren't spoiled by unrelated bankruptcies.
- Gradual prices are small and on their own, and they steady every later test.
- Pops come before sectors because everything after them employs and pays by class.
- The sector layer comes before land, resources and infrastructure, so those are written once, into the new structure.
- Investment needs the physical caps in place. Companies need investment. Banking needs borrowers, and brings base money with it, since reserves are built from base money. Currency needs bank money.
- Controls and balance come last.

## Rules for the rework
- **Implementation, not balance.** Values only need to be sane enough to show a mechanism working. Don't retune the sheet to fix balance; note the issue for M14.
- **Before a milestone:** reread its spec sections and its questions in `decisions.md`. Raise any open ones with Strat, and make a simulator baseline: `runs/<milestone>_base`, `world_1857_eng`, 60 months.
- **`redux-eco-sim` may be edited freely** (Q5). Strat commits it separately.
- **To finish a milestone:**
  - `ecosim_cli.exe check --parse-only` is clean.
  - A 60-month run is compared against the previous baseline.
  - The game loads, with a smoke test in-game.
- **After a milestone:** update its status here, then `economy_overview.md` and the "Current status" section of `AGENTS.md`.
- **Delete what a milestone replaces** (Q4). Old code clutters the mod and confuses coding agents, and git keeps the history.
- **Leave the stripped map alone.** Test industries go only inside `# >>> rework test industries` blocks, and test slaves inside `# >>> rework test slaves` blocks (Virginia, South Carolina and Mississippi).

## Current state of the code
- **Committed** in `26bd1bfab`: the map is stripped to subsistence plus 303 engine factories, with the old values commented out in place in about 1,095 state files. The 1857 PM retune is in ([pm_1857_tuning.md](pm_1857_tuning.md)), and the ENG and RAJ targets are comments in the history files.
- **Committed** in `c472e2509`: this plan reorganisation, M00 (the debt and cycle switches, the month counter fix and the test industries) and M01 (gradual prices, the trade AI's minimum-trade fix, and `pops_base_spending` cut from 0.3 to 0.1).
- **Committed** in `94fc8dbbf`: M02 (five classes, qualifications, slaves, bureaucrats, active manpower, the merged upper-class investment modifier).
- **Committed** in `56c941ee2`: M03 (wealth, spending toward a target, pop debt, middle-class investment, the `get_pop_needs` refactor, and subsistence owner jobs from the peasants).
- **Uncommitted:** M04 so far (the PM/AM cache, sector records, the profit split, monthly goods totals by sector and method, the slim state-industry, target utilisation, capacity decay, the national sector figures for the UI).
- **Switched off:** investment (`global.eco_investment_enabled = 0`), debt (`global.eco_debt_enabled = 0`: starting debt, interest and bankruptcy), the economic cycle (`global.eco_cycle_enabled = 0`), downsizing and banking. Pops borrow, but without interest until M11.
- **Known bugs:**
  - Pop investment money disappears until M09 gives it the general pool.
  - Pops start in debt: the first three ticks overspend against startup's figures (Q81, accepted until M14).
  - Wages rise 0.5% a month wherever jobs are filled exactly, since utilisation then sits at 1.0, above the stable band (M02, Left over).

## Other files here
- **M14 reference:** [eng_economy.md](eng_economy.md) and [raj_economy.md](raj_economy.md) give 1857 output for the British Isles and India. The history files cite them by name, so keep them here. [pm_1857_tuning.md](pm_1857_tuning.md) and `pm_1857_tuning.csv` record the 1857 PM values already in the sheet.
- [archive/](archive/): the old segments 01–07, the old README, `pm_rework_plan.md` (the PM rework's locked decisions) and the old spec. Segments 01, 02 and 04 hold findings that still apply: array math in triggers, the AM labour-cut clamp, and the infrastructure formulas.

## Tools
Run them all from the repo. Simulator details are in `redux-eco-sim/CLAUDE.md`.

| Task | Command |
|---|---|
| Parse check | `redux-eco-sim/bin/ecosim_cli.exe check --parse-only` |
| Run the simulator | `ecosim_cli.exe run --scenario scenarios/world_1857_eng.txt --months 60 --out runs/<name>`, then read `runs/<name>/report.md` |
| A/B two runs | `ecosim_cli.exe compare runs/<baseline> runs/<name>` |
| Change PM balance | Download the Google Sheet over `toi/documentation/Planning/EoaNBR Economy.xlsx`, run `python toi/documentation/scripts/generate_pm_data.py`, then start a new game |
| Check script values against the sheet | `python -B toi/documentation/scripts/verify_pm_audit.py` |
| **Read real in-game state** | `python redux-eco-sim/tools/read_save.py --country ENG`, `--state 952`, `--var ENG.gdp_amount`. Reads the newest autosave |
| Diff a save against the simulator | `ecosim_cli.exe run --scenario scenarios/world_1857_eng.txt --months 1 --dump-json sim.json`, then `python tools/compare_save.py --save autosave.hoi4 --sim sim.json --scope ENG` |
| Compare in-game probes | in-game `effect eco_sim_probes = yes`, then `ecosim_cli.exe calibrate` |
| Compare in-game state | in-game `effect eco_sim_parity_dump = yes`, then `ecosim_cli.exe parity` |
| Refresh army and stability inputs from saves | `python redux-eco-sim/tools/import_save_inputs.py` |
| Rewrite the 1857 target comments | Dump month 0 with `--dump-json`, then `python toi/documentation/scripts/catalogue_1857_targets.py --dump <file>` |
| Simulate old code, or a map change on a copy | `git archive HEAD toi/common toi/history toi/events toi/localisation/english toi/map/definition.csv` into a scratch dir, then `run --mod <dir>/toi` |

## Rules learned the hard way
- **Never hand-edit generated files.** Edit the workbook or the tables in `generate_pm_data.py`, then regenerate. The generated files are `_economy_definitions_pms.txt`, `_economy_definitions_pm_assignments.txt`, `_economy_pm_modifier_factors.txt`, `01_economy_pm_modifiers.txt`, `economy_pms_l_english.yml`, `economy_pm_icons.gfx`, and the marked blocks in `eoanbr_tokens.txt` and `script_enums.txt`.
- **Check a save before believing a theory.** `read_save.py` shows what the game actually computed. Segment 01's first diagnosis came from probes alone and was wrong.
- **A console probe isn't a tick.** `arr^i` in math, and math in `all_of`, work in ticks but read 0 from the console.
- **Stage `arr^i` into a temp before a math expression, and keep math out of trigger blocks.** Both are unreliable outside ticks, and the getters also run from the GUI. The simulator reports any new use (`math_array_read`, `math_in_trigger`).
- **Compare with saves on `world_1857_eng.txt` only, and only saves made on the current code.** Early gaps compound, so compare a startup save first, then one tick.
- **Strat's test games are on Easy.** That gives ENG a free 1% of GDP a month and −0.02 input factor. If the setting changes, change `difficulty` in that scenario.
- **Read the xlsx, not pasted CSVs.** CSV rounding hid real values.
- **Tech links set startup PMs.** A state with no starting PM begins on `latest_production_method`.
- **Strat prefers math expressions,** and temps only when a value is reused. Array reads and trigger blocks are the exceptions.
- **A load error zeroes every later math expression in its file.** M02 first loaded with everyone a peasant because `_economy_main_rework.txt` had a `log = ""` at line 124 and `_economy_setup.txt` called two effects that don't exist. Both were harmless until M02 put math expressions after them. Check `error.log` for "Errors occurred while reading math expression" after loading. The simulator has reported these as `load_error` since 2026-11-12.
