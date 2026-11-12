# Segment 01: array math and getters

> **Archived 2026-11-11.** Superseded by the milestone plan in [../00_README.md](../00_README.md), built on the new spec [EOANB_Redux_Economy_Redesign_Updated.md](../EOANB_Redux_Economy_Redesign_Updated.md). Kept for history: status and file references below are as they were when archived.

**Done in code, 2026-10-30.** One optional in-game check is left (see the end). It no longer blocks anything.

## The original diagnosis was wrong
This segment said `arr^i` read 0 in math expressions, so production was 0 and the market went to the cap. An autosave from Strat's test (`redux-eco-sim/tools/read_save.py`) showed otherwise:

| Site | In-game value | Verdict |
|---|---|---|
| `production_max`: `multiply = arr@var:b^ii` | Right, and livestock's 3 outputs honour the index | Worked |
| `input_max`: `value = arr@var:b^ii` | Right | Worked |
| Subsistence outputs, `^ii` in an expression | Right, 1 : 0.2 : 0.04 | Worked |
| `get_construction_cost` / `get_pm_values`: math + `^pm_i` inside `all_of` | Non-zero at startup and monthly | Worked |
| `pm_construction_value`, set at startup | **0 on all 226 methods** | **Broken.** No maintenance was charged |
| Console probes `array_in_expression`, `all_of_sum` | 0 | Console only, as far as we know |

The two failing probes are the only ones where a math expression reads a temp, and they ran from the console. The other math probes use literals. So the console, or something about those lines, behaves differently from real ticks. `pm_construction_value` was the only `add_to_variable` with a math RHS in the economy, which may be why it failed. Neither is confirmed.

**Production in-game matched the sim to about 10% after 4 months** (machinery +3%, chemicals 0%, fiber −2%, food +9%), and ENG's GDP had the same shape as the sim (game 80.7 / 62.0 / 52.5 / 79.7K, sim 72.4 / 52.6 / 46.5 / 56.7K with maintenance off). So the expensive market was never an array bug. Most of it comes from the July bankruptcy, covered in [segment 03](03_startup_balance.md). Forcing the array failure on in the sim gave 5.9K GDP, nothing like the game, which is what exposed the wrong diagnosis.

`_economy_market.txt` 1462 and 1466 were also listed here as live and broken. They aren't: `add_to_array = { value = arr^ii }` is a plain operand, not a math expression. Trade sorting is fine.

## What changed
**Script:**
- `pm_construction_value`: plain temp effects. This is the one real fix, and maintenance is charged again.
- Getters (`_economy_getter_functions.txt`): plain temps throughout, not only in `all_of`. They run from GUI and localisation too, and that context is untested. New helpers `get_method_payroll`, `get_method_construction_cost`. Temps are `getter_*` so callers aren't clobbered (`pm_i` was shared).
- Every `^` read in a math expression is staged into a temp first: industries, subsistence, construction, `calculate_projected_profitability` (dead code, kept), the PM audit.

Staging and plain temps are safe whichever explanation is right, so this doesn't depend on the unknowns.

**Sim:** two diagnostics, `math_array_read` and `math_in_trigger`, report any new use. Two knobs, default off, force the 0 for what-if runs. `read_save.py` added.

**Probes:** `eco_sim_probes_math` isolates one variable per line. `on_monthly_UCT` has a one-line debug hook so the same probes can run from a tick.

## Verification
- `verify_pm_audit.py`: 0 mismatches over 6,769 values.
- Sim with both failures forced on vs off: 0 cells differ over 24 months of eng_1857 and 12 of world_1857. So the script no longer depends on either construct.
- Sim pre vs post: same GDP to the decimal. Output is unchanged, as intended.
- 0 `math_array_read` or `math_in_trigger` sites in the economy files. `bin/ecosim_tests.exe` passes, 39 script tests.

The sim charged maintenance all along, so it never showed that bug. In-game, expect profits a little lower than the last test. In the sim the effect on ENG's GDP was small (56.7K vs 58.8K in September).

## Optional: settle why the console failed
Only matters if you want math expressions back in the getters for speed.
1. Console: `effect eco_sim_probes = yes`
2. Console: `effect set_global_flag = eosim_tick_probes`, then let one month pass.
3. `bin\ecosim_cli.exe calibrate` shows the console run, `calibrate --dump 2` the tick run.

Read `temp_in_expression` first: 0 from the console and 10 from the tick means the console can't read temps in math, which explains both failures. `add_to_global_array_math` should show whether the `add_to_variable` form is the startup problem. `all_of_staged_read` must be 38 in both, since the getters rely on it. `all_of_sum` and `array_in_expression` will show as DIFF for the console run. That's expected.
