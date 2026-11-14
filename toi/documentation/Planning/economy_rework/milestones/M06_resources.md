# M06: Natural resources and extraction

**Spec:** §9. **Depends on:** M04. **Questions:** Q28–Q30, Q68, and the follow-ups Q96–Q101, all decided. **Status:** done in the simulator 2026-11-14; the in-game check is still to do (see Left over). Baseline: `redux-eco-sim/runs/m06_base` (`world_1857_eng`, 60 months, `--watch-file watches/m06.txt`). Result: `runs/m06_a`.

## Goal
The economy owns its deposit data, in three stages:
- **Potential:** not found yet. Prospecting turns it into known deposits.
- **Known:** found and open for expansion, but working it needs investment.
- **Active:** being worked now.

Quality is stored separately from quantity, and output = capacity × utilisation × PM productivity × quality × infrastructure effect.

## Exists now
- **Deposits:** the code already has the three stages. An RGO's size comes from `base_resource@`, which is read from HOI4's `resources = {}` blocks. The strip commented those out.
- **Code:** `add_rgo_internal` moves deposits between the stages. Prospecting is random rolls with a chance of a major find. `_init_resources` divides reserves by the good's price.
- **Military link:** the `resource_trade` dynamic modifier pushes economy goods into HOI4 resources, so equipment production can use them.

## Build
1. **Deposit data** (Q28): potential deposits, known deposits and quality per good become state history variables. HOI4's `resources` blocks no longer feed the economy.
2. **Active deposits** (Q68) are the RGO's size, stored once. Known deposits minus size is what investment can still open up.
3. **Rules** (Q29): active capacity can't exceed known deposits. Quality scales throughput, not jobs. There's no depletion, and wood is renewable.
4. **Prospecting** (Q30) becomes an investment opportunity. Its investment side lands in M09.
5. Keep `resource_trade` working.
6. Update `catalogue_1857_targets.py` and the history-block format if the deposit variables change it.

## Done when
- RGO output follows the formula above in the simulator.
- No economy code reads HOI4 state resources.
- HOI4 equipment production still gets its resources in-game.

## What the code reading found (Q96–Q101)
- An RGO's size was the state's HOI4 resource count: `update_base_resource_count` read `resource@` every month, and `add_rgo_internal` called `add_resource`. So content grew RGOs with vanilla `add_resource`, 536 live calls in all (Q96).
- All 32 goods were RGOs, services and computers included, because HOI4 had them all as resources (Q97).
- Known reserves left out the worked part, unlike Q68. A major find created known deposits *and* potential from nothing (Q99), and `rgo_discovery` added each find twice: once directly and again through `add_rgo_internal`.
- Startup rolled random potential reserves (`_init_resources`), so runs and saves differed by the roll (Q100).
- `can_build_industry` checked a `deposits@` variable that nothing set, and `_economy_states_setup_rework.txt` had never been called (Q101).
- 33 US states still had live `resources` entries, in test blocks from the USA economy commit (`8352011a0`): Pennsylvania coal 28, iron 11 and wood 11, and 207 levels across the 33 states. They were the world's coal exporters. The first M06 run dropped them, and ENG's coal price ended at 7.80 instead of 3.92, because it lost its imports.

## What was built (2026-11-14)
1. **Deposits are state history data** (Q28, Q68), in levels of RGO size:
   - `set_variable = { coal_size = 3 }` is the worked deposit, the RGO's `size@`, set like any building's;
   - `known_deposits@token:coal` is what's found, worked or not;
   - `potential_deposits@token:coal` is what isn't found yet;
   - `deposit_quality@token:coal` is 1 unless history sets it.

   `state_eco_building_init` raises known deposits to the size where history sets less, sets quality to 1 where a deposit exists, and gives RGOs their methods once they have any deposit. The three British test RGOs moved from `resources` blocks into the history test blocks. Lancashire's coal has known 5 and potential 20, to show building and prospecting, and Wales's coal has quality 1.25. The 33 US states' entries moved the same way, as `<good>_size` in new history test blocks.
2. **No economy code reads HOI4 state resources.** These are deleted: `update_base_resource_count`, `base_resource@`, the RGO branch of `industry_update_size_jobs`, startup's RGO block, the state-scope `resource_cost@` and `resource_additional_production@`, and the `additional_state_production` modifier that nothing applied. The army still gets its goods through the country's `resource_trade` modifier, and military demand still reads the country's `resource@`.
3. **The formula** (Q29, Q98). Quality multiplies the RGO's output in `industry_production_update`, after Infrastructure Efficiency. Inputs and jobs don't change, so output = size × utilisation × PM productivity × quality × infrastructure effect. `get_pm_values` does the same in state scope. Nothing depletes.
4. **The cap** (Q29). `can_build_industry` lets an RGO grow only into known deposits nobody works or is opening up yet: known − size − construction. Finishing construction raises the size and leaves known deposits as they are.
5. **`add_rgo_internal`** takes the changes to size (`deposit_temp`), known (`known_temp`) and potential (`potential_temp`), and keeps known at least the size. It gives a deposit new to the state its methods and quality 1. It clears its inputs, since a tick can call it more than once.
6. **Prospecting** (Q99). It's still the state screen's government-paid Prospect button, resolved the next month by `rgo_discovery`. `update_prospecting` sets the figures:
   - A normal find is 10–30% of the remaining potential, times prospecting ability. A major find is 50–100%.
   - The major chance is 0.25 × ability, less the share already found, less 0.4 per earlier major find, with a floor of 1%.
   - The cost is unchanged: 1,000 × (1 + 9 × share found²) × ability.
   - A find is whole levels, at least 1 and never more than the potential left. Nothing is found from nothing.
   - The constants are `global.prospecting_*` in `resources_global_var_setup`. The major-find event shows the known deposits found.
7. **RGOs for natural goods only** (Q97). The 15 manufactured goods' `define_*_rgo` are gone. Chemicals stays, as nitrates, guano and sulphur, and is now typed as a resource. The rest: wood, coal, iron, copper, valuables, oil, rubber, aluminum, tungsten, chromium, titanium, silicon, rare earths, food, fiber, luxuries.
8. **Content converted** (Q96, Q97), by script: 535 `add_resource` calls in 98 files.
   - 442 add natural deposits through `add_x_deposit`, one for one, and 28 remove them through `remove_x_deposit`.
   - 62 manufactured goods now add their factory through `add_x_industries`, at the same jobs: textiles 10 becomes textile mill 4, steel 8 becomes steel foundry 2. One removes a textile mill.
   - Two with amount 0 were deleted. The 105 country-scope calls with `state =` are wrapped in that state.
   - The 27 commented-out calls are untouched.
9. **Wrappers** (`_economy_effects_documentation.txt`):
   - `add_x_deposit` raises known deposits with the size, and now lists a deposit new to the state before refreshing employment, so it works the same day.
   - `remove_x_deposit` lowers both.
   - `add_known_reserves` and `add_potential_reserves` became `add_known_deposits` and `add_potential_deposits`. The four USA events that call the first were updated.
   - New: `set_deposit_quality` and `change_deposit_quality` (`r_token`, `deposit_quality_temp`), with English tooltips.
10. **Renames:** `known_reserves@` → `known_deposits@`, which now includes the worked part, `potential_reserves@` → `potential_deposits@`, and the sector figures to `sector_known_deposits@` and `sector_potential_deposits@`. `reserves_total@` and `discovery_chance@` are gone. The focus tree's four `base_resource@<good>` reads became `size@token:<good>`.
11. **The state screen:**
    - The RGO tooltip shows the worked deposit, quality, known and potential deposits.
    - The Prospect tooltip shows the normal and major finds and the deposits.
    - The button is enabled while potential remains, and hidden while known deposits wait to be worked, as before. The Korean and Russian tooltips read the new variables.
12. **Deleted** (Q100, Q101): `_init_resources`, `_economy_states_setup_rework.txt`, the five `soil_quality_*` modifiers and their localisation in three languages.
13. **Simulator:** `watches/m06.txt`, and the parity dump logs known and potential deposits instead of `base_resource@` and `resource@`.

## Results (simulator, `world_1857_eng`, 60 months)
Against `m06_base` (`runs/m06_a`):
- **Diagnostics are unchanged:** 243 errors, no `load_error`.
- **Speed:** ticks are 4.5% faster (1.275 s/month against 1.335) and startup 10% faster, since thousands of states no longer carry random potential reserves.
- **PM audit:** `verify_pm_audit.py` finds 0 mismatches. It now lists four methods nothing reads (`pm_hydroelectricity`, `pm_reaction_turbine`, `pm_pumped_storage_hydropower`, `pm_advanced_turbine_systems`), which the sheet gives only to the electricity RGO.

**The formula holds:**
- Wales's coal, at quality 1.25, makes 17.10 at startup against 13.68, exactly 1.25×, with the same jobs.
- Every RGO at quality 1 matches the baseline: Lancashire's coal 15.29 at month 60 in both runs, West Midlands' iron within 0.02%, Pennsylvania's coal at size 28.
- ENG's coal output is 13% higher, its coal price ends 4.7% lower (3.73 against 3.92), and its GDP is 0.15% higher.

**Mechanism checks** (simulator effects at month 1, in Lancashire unless noted):

| Check | Result |
|---|---|
| Prospect figures (known 5, potential 20, ability 1.2) | find 2.4–7.2, major 10–20, chance 0.10, cost 1,632, all as calculated |
| Build cap (2 levels free) | building 2 allowed, 3 blocked; East Anglia oil with known 4: 4 allowed, 5 blocked |
| Monthly roll (`on_monthly_industries` with `prospecting@` set) | known 5 → 9, potential 20 → 16, flag cleared, chance falls to 0.01 and cost rises to 2,600 |
| A find bigger than the potential left (0.4) | takes 0.4, potential 0 |
| `add_x_deposit` 2 / `remove_x_deposit` 1 | size 3 → 5 → 4, known 9 → 11 → 10 |
| Quality 2 at size 4 | output doubles (19.0 → 38.0), jobs 3.12 unchanged |
| `add_x_deposit` of iron in East Anglia, which had none | size 2, known 2, quality 1, methods set, output 8.5 the same day |
| Steel | no longer an RGO |

## Left over
- **In-game check:**
  - Load a new game and search `error.log` for "Errors occurred while reading math expression".
  - Check that history's `set_variable = { known_deposits@token:coal = 5 }` and `deposit_quality@token:coal = 1.25` take effect (M05's `crop_eligible@token:` is untested in-game too). Read state 132 and 122 with `read_save.py`.
  - Open an RGO's tooltip and the Prospect button's.
  - Check that equipment production still gets coal and iron.
- **Fixed after M06 (2026-11-14): the missing `get_total_construction_cost`.** "Economy rework part 1" (`487bd9311`) deleted the getter, but `add_x_industries`, `add_1_civfac_random_state` / `add_1_milfac_random_state` (`0_eoanb_building_effects.txt`) and five USA focuses still called it. It caused a load error in `_economy_effects_documentation.txt`, and `add_x_industries` with `cost_factor_temp` charged nothing. It's back in `_economy_getter_functions.txt`: construction cost × (1 + `global.start_construction_cost_multiplier`), divided by government investment efficiency when `is_government` is 1. Its old fallback read `latest_production_method@var:v` instead of `industry_token`, which is fixed too. `add_x_industries` now treats only a country (id above 10500) as a government payer, since companies have small ids. Checked in the simulator: a steel foundry in West Midlands costs 7,272 × 1.25 = 9,090, or 25,971 for ENG's government at 0.35 efficiency. `add_x_industries` of 2 with `cost_factor_temp = 1` took 51,943 from ENG (its 57 of treasury, and the rest borrowed through `add_treasury`). The load error is gone.
- **The content callers charge the wrong treasury:** those seven call `add_treasury` inside the state's scope, so they lower the state's own `treasury` variable, not the country's. Wrapping it in `owner = { }` would fix it. That's content, so it's noted in the backlog.
- **Before M09 a state finds each good once:** the Prospect button hides while known deposits wait to be worked, and only investment or content works them. The state screen has no build button for RGOs.
- **Era-gated prospecting** is in the backlog (Strat, on Q99).
- **Content amounts are the old HOI4 ones.** A focus that gave "wood 40" now adds 40 worked levels of wood. M14 sizes them against the rebuilt map, and may make some known deposits for investors instead. Factory conversions can fail where the RGO wouldn't have: a factory needs a free industry slot.
- **The gated investment, companies, buckets and banking code** still reads `known_reserves@`, `potential_reserves@`, `base_resource@` and `discovery_high@`. M09–M11 replace it.
- **Hydro power:** the sheet gives the electricity RGO four hydro and turbine methods, unused since Q97. They could become power plant methods, or a site-limited RGO, in the sheet.
- **The catalogue** still labels RGOs "(resources)" in the 1857 target comments. The format didn't need to change, so the comment blocks weren't regenerated.
