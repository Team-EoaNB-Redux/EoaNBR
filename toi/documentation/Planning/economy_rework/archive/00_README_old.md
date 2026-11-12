# Economy rework: handoff index

> **Archived 2026-11-11.** Superseded by the milestone plan in [../00_README.md](../00_README.md), built on the new spec [EOANB_Redux_Economy_Redesign_Updated.md](../EOANB_Redux_Economy_Redesign_Updated.md). Kept for history: status and file references below are as they were when archived.

Written 2026-10-30, at the end of the session that did the PM + Infrastructure pass. Each numbered file is one self-contained segment for a fresh session. Do them in order.

| # | Segment | State |
|---|---|---|
| 01 | [Array math + getters](01_fix_array_math_and_getters.md) | Done. Its original diagnosis was wrong: read it before trusting old notes |
| 02 | [PM assumptions](02_pm_assumptions_review.md) | Reviewed. RGO employees done. Open: how AMs cut workers |
| 03 | [Startup balance](03_startup_balance.md) | **Next.** Strat's call: rebuild the map from subsistence. State economy stripped. Next: debt and budgets, then build up |
| 04 | [Infrastructure tuning](04_infrastructure.md) | Built, untuned |
| 05 | [Country-level industries](05_country_level_industries.md) | Not started. Do after 01–03 |
| 06 | [Investment rework](06_investment_rework.md) | Not started. Investment is off behind a flag until this |
| 07 | [Content backlog](07_content_backlog.md) | Techs, icons, localisation, moving base prices |

Other files here:
- `pm_rework_plan.md`: the approved plan, with every locked decision and why.
- `redux_economy_redesign_spec.md`: The full design spec. 05 and 06 carry the key points, but the original has the detail.
- `eng_economy.md`, `raj_economy.md`: 1857 output of the British Isles and India. Their targets are comments in the history files: see 03.
- `pm_1857_tuning.md`, `pm_1857_tuning.csv`: how to tune the 1857 PMs and wages to those targets, with the sheet rows to change.

## Current state of the code
- Committed by Strat as `487bd9311`. Uncommitted since: the RGO table in `_economy_definitions_industries.txt`, the state history strip (1,095 files), `strip_state_economy.py`, and these planning docs.
- **The 1857 PMs and wages are retuned:** see `pm_1857_tuning.md`. That's uncommitted too, and simulated but not run in-game.
- **The map has no economy right now:** only subsistence farms and the 303 engine factories, and ports and railways are gone. `git checkout -- toi/history/states` restores the old map, and also discards any later map work in that folder that isn't committed.
- The rework's code works in-game, and the sim reproduced it to within 0.5% of ENG GDP at startup and June 1, on the old map. Saves from before the RGO change and the strip no longer match the code (segment 03).
- In-game ENG GDP after the rework, old RGO table: June 80.7K, July 62.0K (bankruptcy), August 52.5K, September 79.7K, later 16.3K. The Netherlands went bankrupt in December. The market spike in September came from the bankruptcy: see 03.

## Tools
All run from the repo. Sim details: `redux-eco-sim/CLAUDE.md`.

| Task | Command |
|---|---|
| Change PM balance | Download the Google Sheet over `toi/documentation/Planning/EoaNBR Economy.xlsx`, run `python toi/documentation/scripts/generate_pm_data.py`, then start a new game |
| Check script values against the sheet | `python -B toi/documentation/scripts/verify_pm_audit.py` |
| Run the sim | `redux-eco-sim/bin/ecosim_cli.exe run --months 60 --out runs/<name>`, then read `runs/<name>/report.md` |
| **Read real in-game state** | `python redux-eco-sim/tools/read_save.py --country ENG`, `--state 952`, `--var ENG.gdp_amount`. Uses the newest autosave, no dump needed |
| **Diff a save against the sim** | `ecosim_cli.exe run --scenario scenarios/world_1857_eng.txt --months 1 --dump-json sim.json`, then `python tools/compare_save.py --save autosave.hoi4 --sim sim.json --scope ENG` |
| Compare in-game probes | in-game `effect eco_sim_probes = yes`, then `ecosim_cli.exe calibrate` |
| Compare in-game state | in-game `effect eco_sim_parity_dump = yes`, then `ecosim_cli.exe parity` |
| Rewrite the 1857 target comments in the history files | Dump month 0 with `--dump-json`, then `python toi/documentation/scripts/catalogue_1857_targets.py --dump <file>` |
| Sim the old code, or try a map change on a copy | `git archive HEAD toi/common toi/history toi/events toi/localisation/english toi/map/definition.csv` into a scratch dir, then `run --mod <dir>/toi` |

Baselines in `redux-eco-sim/runs/` (gitignored): `pre_pm_rework` (old code, eng_1857, 24 months), `head_world` (old code, world, 12 months).

`documentation/Planning/pm_generation_report.md` lists every default the generator filled in.

## Rules learned the hard way
- **Generated files are never hand-edited.** Edit the workbook or the tables in `generate_pm_data.py`, then regenerate. Generated: `_economy_definitions_pms.txt`, `_economy_definitions_pm_assignments.txt`, `_economy_pm_modifier_factors.txt`, `01_economy_pm_modifiers.txt`, `economy_pms_l_english.yml`, `economy_pm_icons.gfx`, and the marked blocks in `eoanbr_tokens.txt` and `script_enums.txt`.
- **Check a save before believing a theory.** `read_save.py` shows what the game actually computed. Segment 01's first diagnosis came from probes alone and was wrong.
- **A console probe isn't a tick.** `arr^i` in math and math in `all_of` work in ticks but read 0 from the console.
- **Stage `arr^i` into a temp before a math expression, and keep math out of trigger blocks.** Both are unreliable outside ticks, and the getters also run from the GUI. The sim reports any new use (`math_array_read`, `math_in_trigger`).
- **Compare with a save on `world_1857_eng.txt` only, and only a save made on the current code.** It has ENG as the player, the armies, default laws and difficulty. A gap there is worth chasing. Early gaps compound, so compare a startup save first, then one tick.
- **Strat's test games are on easy.** That's a free 1% of GDP a month and −0.02 input factor for ENG. If the setting changes, change `difficulty` in that scenario.
- **Read the xlsx, not pasted CSVs.** CSV rounding hid real values (Steam Engine machinery is 0.005, not 0.01).
- **Tech links set startup PMs.** States with no starting PM begin on `latest_production_method`.
- Strat prefers math expressions, and temps only when a value is reused. Array reads and trigger blocks are the exceptions.
