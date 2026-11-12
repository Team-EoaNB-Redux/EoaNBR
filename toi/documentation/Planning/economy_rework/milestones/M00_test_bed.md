# M00: Test bed

**Spec:** none directly. **Depends on:** nothing. **Questions:** Q1–Q5, all decided. **Status:** done 2026-11-12, including the in-game parity check.

## Goal
An 1857 world where each later milestone can be tested without unrelated collapses getting in the way. This is not balance. It only has to stay still long enough to show whether a mechanism works.

## Exists now
- The map is stripped to subsistence farming plus the 303 engine factories (commit `26bd1bfab`). The old values are still in the state files, commented out in place.
- ENG's `starting_debt` is commented out (uncommitted). Every other country's debt and spending were sized for the old GDPs (see [archive/03](../archive/03_startup_balance.md)).
- Nothing increments `global.month`, so `years_passed`, the yearly statistics and `check_economic_cycle` never advance.
- The simulator's `save_inputs_1857.txt` (army production lines, stabilities taken from saves) comes from saves on the old map.

## Build
1. **One debt switch for everyone** (Q2). It can turn off interest and bankruptcy, skip debt initialisation, or zero debt after init: use whichever is simplest. M14 turns it back on.
2. **Fix the month counter.**
3. **Test industries in Britain** (Q3), at sizes of 1–3, inside `# >>> rework test industries` / `# <<<` blocks. Proposed:

   | State | Industries |
   |---|---|
   | Lancashire | textile mill, coal |
   | West Midlands | steel foundry, tooling workshop, iron |
   | London | urban centre, consumer goods factory |
   | East Anglia | crop farm, livestock ranch |
   | Wales | coal, iron |

   The RGOs need deposits. Until M06 changes the format, use the current `resources` lines.
4. **Baselines.** Run `world_1857_eng` for 60 months into `runs/m00_base`. Every later milestone compares against the previous milestone's baseline.
5. **Parity check.** One in-game save at startup and one after a tick, both on the test bed. Rerun `tools/import_save_inputs.py` from them, then compare with the simulator.

`redux-eco-sim` may be edited freely during the rework; Strat commits it (Q5).

## Done when
- `world_1857_eng` runs 60 months in the simulator with no bankruptcies.
- ENG's test industries hire and produce.
- The simulator matches the in-game saves to about 1% at startup and after one tick.
- The month counter advances.

## What was built (2026-11-12)
1. **Debt switch:** `global.eco_debt_enabled = 0`, set in `global_variables` next to the interest-rate globals (`_economy_setup.txt`). While it's 0:
   - `_country_fin` skips every starting debt (`starting_debt`, `starting_debt_gdp`, `starting_debt@<country>`). ENG's `starting_debt = 1500` is back in its history file, so M14 only has to flip the switch.
   - `national_debt_update` sets `domestic_interest_rate` and `foreign_interest_rate` to 0. Both interest calculations (there's a second one in `spending_update`) read these rates, so no interest is charged anywhere, and the debt tooltip shows 0%.
   - `national_debt_update` skips `debt_related_country_content_effects`, so bankruptcy (`egy_debt_system.7`) can't fire.
   - Deficits still borrow, up to the lending cap (24 months of GDP, `debt_level` 50). Past the cap, the treasury goes negative with no consequence.
2. **Month counter:** `_advance_time` adds 1 to `global.month` each tick. It wraps at 12 and advances `global.years_passed`. The yearly GDP statistic also summed the oldest four quarters (`gdp_amount_quarterly` starts with 41 seeded quarters of back-history), so it now sums the newest four.
3. **Test industries** in `# >>> rework test industries` / `# <<< rework test industries` blocks:

   | State | Industries | Deposits (`resources`) |
   |---|---|---|
   | 132 Lancashire | textile mill 2 | coal 3 |
   | 128 West Midlands | steel foundry 1, tooling workshop 2 | iron 3 |
   | 952 London | urban centre 2, consumer goods factory 2 | — |
   | 125 East Anglia | crop farm 2, livestock ranch 2 | — |
   | 122 Wales | — | coal 3, iron 2 |

   An RGO level is one deposit unit at 1–1.5 base employees, against 10 for a factory level, so the RGOs have about 2.5–3.7K jobs each and the factories 8–20K.
4. **Economic cycle switch:** `global.eco_cycle_enabled = 0`, next to `global.month` in `global_variables`. `_country_advance_time` only calls `check_economic_cycle` when it's 1. Once the counter worked, the cycle fired from year 2: by month 60, 14 of 130 countries were in a downturn or recession, and ENG's consumer confidence flipped between 108.66 and 103.66 during 1859–60, driven by ENG's GDP swinging ±5% a month. Strat put it off until M14 (Q54, amended).
5. **Baseline:** `redux-eco-sim/runs/m00_base` (`world_1857_eng`, 60 months, `--watch-file watches/m00.txt`), with `scenarios/save_inputs_1857.txt` regenerated from the M00 saves. `runs/m00_pre` is the same run on the pre-M00 code, and `runs/m00_base_cycle_on` is the M00 code with the cycle still on. The new watch list follows the debt switch, the counter, the Q2 countries and every test industry.

## Results (simulator, 60 months)
- **Bankruptcies:** none, against 20 on the old code (AUS, BAD, BAV, BEL, BRE, BUE, CAU, CIR, DEN, FRA, GXC, HOL, KIN, MNC, PIE, PRU, PTH, RUS, SPR, SWE). No country has an economic status, and ENG's consumer confidence holds at 108.66.
- **Month counter:** `global.years_passed` reaches 5, and ENG has 5 yearly GDP entries.
- **Test industries:** all of them hire and produce. ENG's startup GDP rises from 6.78K to 10.2K a month. Every industry starts at an 80% employment target, and most are at 100% by month 60. The exceptions are the consumer goods factory, at 68% as its price drops from 20 to 13, Lancashire coal at 38% as coal drops from 8 to 5, and Welsh coal at 82%.
- **Interest:** 0, against 1.88K a month on the old code by month 60.

## Parity with the game (2026-11-12)
Strat's saves on the M00 code: `ENG_1857_05_11_01.hoi4` at the bookmark and `autosave.hoi4` after the first tick (ENG, Easy). `tools/import_save_inputs.py` regenerated the save inputs from them, then `compare_save.py` compared each save with a simulator dump (`--months 0` and `--months 1`).

| ENG | Bookmark: game | sim | | Month 1: game | sim | |
|---|---:|---:|---:|---:|---:|---:|
| GDP | 10,106.7 | 10,198.6 | +0.91% | 11,168.6 | 11,115.8 | −0.47% |
| Revenue | 8,271.7 | 8,265.4 | −0.08% | 8,145.9 | 8,272.6 | +1.56% |
| Spending | 16,087.1 | 16,402.9 | +1.96% | 16,587.6 | 16,643.1 | +0.33% |

- After one month, every ENG price matches within 0.5%. In the test-industry states, employment matches within 0.2%, base wages exactly, state GDP to −0.5–1.0%, and industry profits to −1–2%.
- **The largest gap is steel at startup.** In-game, ENG prices steel at 4.83; in the simulator, 9.64. Both make about 25.6, but `_init_trade` (`evaluate_best_trade_quantity`) exports 20 in-game and 28 in the simulator. The 8 units show up exactly in `resource_cost@steel` (−31 against −23). The export formula takes the global steel price at that moment, so the two sides see a different global price during startup. It closes after one tick, apart from the steel foundry's month-1 profit, which uses the startup price (−29%). Untraced. M01 rewrites price formation, so look again there.

## Left over for later milestones
- **Deficits.** ENG spends about 16.4K a month against 8.3K of revenue. It hits the lending cap in under two years and ends at a treasury of −271K. FRA and RUS end below −560K, SWE at −95K. Nothing reacts to a negative treasury while the switch is off, but M11 (banking and base money) and M14 will.
- **ENG's GDP swings ±5% month to month** on the test bed (the price-employment swing in §6 of `economy_overview.md`). M01 should calm it.
- **`_economy_industries.txt:680`** divides productivity by `payroll_multiplier`, which is still 0 for 11 industries on the startup pass. The path is old; the stripped map just never reached it.
- **`check_economic_cycle`** divides by a state's `gdp_average`, which is 0 for states with no GDP. It's harmless, since those states carry no weight. Recheck when M14 turns the cycle back on.
