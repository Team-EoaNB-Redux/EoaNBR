# Segment 02: PM assumptions review

Reviewed by Strat 2026-10-30. Most assumptions stand. "PM calculations look way off" turned out not to be these assumptions: production in-game matched the sim, and the getters that feed the GUI were the likely cause (segment 01). The RGO employees decision is done. How AMs cut workers is still open.

## Strat's answers
| Assumption | Answer | Status |
|---|---|---|
| Quantity is per K of **base** workforce | Right | Closed |
| RGO `base_employees` kept at old values | Needs revisiting | Done 2026-10-31, below |
| A building's multiplier is one scalar | Applies to all outputs, one scalar | Done, below |
| AM shares add to PM shares, floored at 0 | Wanted more detail | Explained below. Open design choice |
| Base tier PMs with no data are 100% Wrk | Generally fine. Not happy with *all*, tune later | Later |
| 1800 basket only if first in family with no machinery input | Fine | Closed |
| Era durations | Unclear what they were | Explained below |
| The rest of the list | Fine | Closed |

Strat's earlier explicit decisions still stand: Wrk = laborers, Mid = workers, workers multiplier 4, value-parity multipliers, transport is demand only, era basket construction, upgrades pay the full new-method cost, workforce gaps from analogs, tech priority sheet > renames > never, Shaft Mining → Basic Extraction, ENG steel on Blister, negative VA on Primitive, Blister and Craft Machinery.

## Done: one scalar multiplier
- `global.building_production_multiplier@b` is now one number, applied to every output.
- `global.building_base_production_amount@b` holds the per-good split, parallel to `building_base_production`. `[1]` for single-output buildings. This reuses the old name and meaning.
- `global.pm_output_amount@pm` stays one number.

So `output[i] = pm_output_amount × multiplier × amount[i] × employees × modifiers`. Only subsistence `[1, 0.2, 0.04]` and livestock `[0.5, 0.06667, 0.2]` have more than one amount, and both have multiplier 1. Generator table: `OUTPUT_AMOUNTS`. Sim results moved by at most 0.17%, from truncation order.

## Done: RGO base employees
**Rule now, for the eight pre-1900 RGOs:** `base_employees = 0.5 × base price`, set in `_economy_definitions_industries.txt`. That's the inverse of the value parity multiplier, so employees × multiplier = 1. One size makes the PM's quantity per K whatever the good (2 a month on Basic Extraction or Simple Forestry, 1.5 on Basic Planting). Jobs and value per size both scale with the price, and they now agree with `_init_resources`, which divides reserves by the same price. "Pre-1900" means the RGOs with 1857 consumption in the sheet's C-1857 column.

Valuables used to be an exception (5, not 12.5). The rule now covers them.

World jobs at the current map's sizes (sim, startup):

| Good | Base price | Employees, old → new | World sizes | World jobs (K), old → new |
|---|---:|---|---:|---:|
| wood | 2 | 0.5 → 1 | 26,635 | 13,167 → 26,333 |
| iron | 3 | 1 → 1.5 | 1,964 | 1,799 → 2,699 |
| coal | 2 | 1 → 1 | 2,616 | 2,300 |
| copper | 4 | 3 → 2 | 602 | 1,794 → 1,196 |
| fiber | 3 | 2 → 1.5 | 568 | 1,123 → 842 |
| food | 2 | 1.25 → 1 | 564 | 704 → 563 |
| luxuries | 6 | 2 → 3 | 149 | 281 → 422 |
| valuables | 25 | 5 → 12.5 | 123 | 610 → 1,524 |

That's 21.8M to 35.9M jobs, almost all of it wood. On the current map wood is then badly oversupplied (103K against 42K demand, price at the $0.50 floor), and ENG's startup GDP rises to 98.9K but still collapses to about 25K within a year. Neither matters: the map is being rebuilt (segment 03).

**What this doesn't change:** value per K. Mines and wood still gross $4/K and farms $3/K. `base_employees` sets jobs and value per size only. An asymmetry, such as oil being really good, belongs in the multiplier or the PM's output, not here.

**Left on the old rule:**
- Oil onward (`oil`, `rubber`, `aluminum`, `tungsten`, `chromium`, `titanium`, `silicon`, `rare_earths`). Oil is still 1K per size, which makes 0.33 a month. Its reserves are still divided by the new price, so reserves and jobs disagree there until these get their pass.
- Refined goods in `rgo_token_array` (`chemicals` 983 sizes, `textiles` 124, a few others). They run factory PMs with multiplier 1, so the rule doesn't fit them. `chemicals` has 1K jobs per size where factories have 10K.

## Explained: why the late-game ROI tab won't hold
The ROI tab adds AM wage deltas straight onto the PM: total = E + N. The game can't have negative workers, so each tier floors at 0. Factory AMs cut Wrk by a flat amount: −0.22, −0.40, −0.60, −0.75, −0.82, −0.86, −0.90.

- **Steel PMs have Wrk near 1**, so they never reach 0. Every steel row in the tab is exact.
- **Machinery-style PMs have Wrk 0.5–0.6**, so from Assembly Lines on they hit the floor. The AM's cut has nothing left to remove, but its input cost still applies.

Payback from the tab vs with the floor applied:

| PM | AM upgrade | Wrk + AM cut | Tab | Game |
|---|---|---:|---:|---:|
| Bessemer | Steam Engine → Industrial Machinery | 0.60 | 5.4 yrs | 5.4 yrs |
| Oxygen Converter | Robots → Data Servers | 0.09 | 5.9 yrs | 5.9 yrs |
| Hydrogen Steel | Data Servers → Mass Automation | 0.00 | 15.2 yrs | 15.2 yrs |
| Modern Machinery | Electrification → Assembly Lines | −0.15 | 11.2 yrs | **never** |
| CNC Machines | Assembly Lines → Robots | −0.32 | 21.9 yrs | **never** |
| Smart Robotics | Robots → Data Servers | −0.36 | 11.7 yrs | 28 yrs |
| Autonomous Robotics | Data Servers → Mass Automation | −0.40 | 64.7 yrs | **never** |

CNC + Robots shows the mechanism. The tab has total wage mult going from 0.75 to 0.62, saving 0.13. In the game Wrk is already 0 on Assembly Lines, so it goes from 1.00 to 0.94, saving 0.06. That doesn't cover the extra input cost, so the AM loses money every month.

617 of 1,324 PM + AM pairs clamp, 169 of them same-era. In the same-era ones the AM keeps about 56–58% of the saving the tab assumes. Mostly Wrk (536), a few Mid (81), never both.

**Options:**
1. **Make AM cuts a percentage of the PM's Wrk** (`Wrk × (1 − cut)`). Nothing can clamp, and steel rows stay almost the same since their Wrk is about 1. Recommended: machinery-style PMs get a proportionally smaller cut, so the sheet's numbers need one pass.
2. Give late PMs more Wrk share. Keeps the additive model, but every later PM needs retuning.
3. Accept it, so late AMs are only worth it on some PMs. The AI will need to avoid the bad pairs.

Only matters for AI upgrades once investment is back, or for player retooling, so it can wait for segment 06.

## Explained: era durations
Construction time in months, when neither the sheet nor the old PM gives one: PMs 12 / 18 / 24 / 30 and AMs 4 / 6 / 8 / 8, for the 1857 / 1900 / 1950 / 2000 eras. They're my placeholders. A new build takes PM + AM duration. An upgrade takes the new method's. Only methods listed as `era default` in `pm_generation_report.md` use them. Fill column O of the PMs tab to override any.

## Sheet oddities still unresolved
- Rename map gives some 1900+ PMs early techs (`tech_sulfite_pulping`, 1875, unlocks a 2000 PM). 34 PMs have a tech 30+ years older than their tier: rerun the check when assigning techs.
- `High Performance Computers` transport row has price 0 (lookup slip on the row above). Harmless, only the quantity is used.
- 9 zero-quantity rows are skipped.
- Blister (0.5/K) is worse than Primitive (1.0/K) above about $10.60 steel.

## Output
Corrections go in the sheet or the generator tables, then regenerate and run `verify_pm_audit.py`.
