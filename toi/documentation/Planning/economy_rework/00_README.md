# Economy rework: handoff index

Written 2026-10-30, at the end of the session that did the PM + Infrastructure pass. Each numbered file is one self-contained segment for a fresh session. Do them in order.

| # | Segment | State |
|---|---|---|
| 01 | [Array math + getters](01_fix_array_math_and_getters.md) | Done. Its original diagnosis was wrong: read it before trusting old notes |
| 02 | [PM assumptions](02_pm_assumptions_review.md) | Reviewed. Open: RGO employees (Strat's call), and how AMs cut workers |
| 03 | [Startup balance](03_startup_balance.md) | **Next.** Not started |
| 04 | [Infrastructure tuning](04_infrastructure.md) | Built, untuned |
| 05 | [Country-level industries](05_country_level_industries.md) | Not started. Do after 01–03 |
| 06 | [Investment rework](06_investment_rework.md) | Not started. Investment is off behind a flag until this |
| 07 | [Content backlog](07_content_backlog.md) | Techs, icons, localisation, moving base prices |

Other files here:
- `pm_rework_plan.md`: the approved plan, with every locked decision and why.
- `redux_economy_redesign_spec.md`: **not saved yet, Strat needs to drop it in.** The full design spec only existed as a chat attachment. 05 and 06 carry the key points, but the original has the detail.

## Current state of the code
- All work is uncommitted in the working tree, on top of commit `017c0d6bc` (153 files). Nothing was committed because Strat didn't ask.
- The rework's production code works in-game: production matched the sim to about 10% after 4 months.
- In-game ENG GDP after the rework: June 80.7K, July 62.0K (bankruptcy), August 52.5K, September 79.7K. Everything in the market is expensive except coal, iron and machinery. That's real balance, not a bug: see 03.

## Tools
All run from the repo. Sim details: `redux-eco-sim/CLAUDE.md`.

| Task | Command |
|---|---|
| Regenerate PM data | `python toi/documentation/scripts/generate_pm_data.py` |
| Check script values against the sheet | `python -B toi/documentation/scripts/verify_pm_audit.py` |
| Run the sim | `redux-eco-sim/bin/ecosim_cli.exe run --months 60 --out runs/<name>`, then read `runs/<name>/report.md` |
| **Read real in-game state** | `python redux-eco-sim/tools/read_save.py --country ENG`, `--state 952`, `--var ENG.gdp_amount`. Uses the newest autosave, no dump needed |
| Compare in-game probes | in-game `effect eco_sim_probes = yes`, then `ecosim_cli.exe calibrate` |
| Compare in-game state | in-game `effect eco_sim_parity_dump = yes`, then `ecosim_cli.exe parity` |
| Sim the old code | `git archive HEAD toi/common toi/history toi/events toi/localisation/english toi/map/definition.csv` into a scratch dir, then `run --mod <dir>/toi` |

Baselines in `redux-eco-sim/runs/` (gitignored): `pre_pm_rework` (old code, eng_1857, 24 months), `head_world` (old code, world, 12 months).

`documentation/Planning/pm_generation_report.md` lists every default the generator filled in.

## Rules learned the hard way
- **Generated files are never hand-edited.** Edit the workbook or the tables in `generate_pm_data.py`, then regenerate. Generated: `_economy_definitions_pms.txt`, `_economy_definitions_pm_assignments.txt`, `_economy_pm_modifier_factors.txt`, `01_economy_pm_modifiers.txt`, `economy_pms_l_english.yml`, `economy_pm_icons.gfx`, and the marked blocks in `eoanbr_tokens.txt` and `script_enums.txt`.
- **Check a save before believing a theory.** `read_save.py` shows what the game actually computed. Segment 01's first diagnosis came from probes alone and was wrong.
- **A console probe isn't a tick.** `arr^i` in math and math in `all_of` work in ticks but read 0 from the console.
- **Stage `arr^i` into a temp before a math expression, and keep math out of trigger blocks.** Both are unreliable outside ticks, and the getters also run from the GUI. The sim reports any new use (`math_array_read`, `math_in_trigger`).
- **A sim pass is not an in-game pass.** It's close, though: after 4 months production matched to about 10%.
- **Read the xlsx, not pasted CSVs.** CSV rounding hid real values (Steam Engine machinery is 0.005, not 0.01).
- **Tech links set startup PMs.** States with no starting PM begin on `latest_production_method`.
- Strat prefers math expressions, and temps only when a value is reused. Array reads and trigger blocks are the exceptions.
