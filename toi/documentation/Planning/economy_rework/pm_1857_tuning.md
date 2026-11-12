# Tuning the 1857 PMs

**Status, 2026-10-31:** applied and regenerated, uncommitted. Simulated, not yet run in-game. To change balance: download the sheet over `EoaNBR Economy.xlsx`, run `generate_pm_data.py`, then start a new game.

Revenue and VA are per K of base workforce per month, before modifiers, as in the sheet. At 1,000 treasury = £1M, 1.0 per K is £1 a worker a month, or £12 a year.

**The docs are a guide, not a rule (Strat).** `eng_economy.md` and `raj_economy.md` set the scale and the shape. Game balance wins where they disagree.

## Decisions
- **Target:** UK GDP/c about 2.3 a month before modifiers. The GDP tab's 1860 row is now 2.3. Hiding services leaves it nearer 1.9 before modifiers and 2.7 after.
- **UK levels** come from the doc's workers. Domestic service (1.39M workers) and housing are hidden, as neither has a building. That takes the listed jobs from 9.29M to 7.90M, inside the game's 9.89M.
- **India's levels** come from the doc's value, so it starts with few industries: 12.4M jobs in levels, 73M on subsistence, and 55 urban levels. China should work the same way.
- **The pre-industrial tier stays higher than India alone would need,** because Russia and others use it too. At VA 1.0 a tag fully on this tier is about £4.8 a head a year, roughly twice India.
- **A smaller step up** also stops a poor tag getting a huge industry by upgrading a PM. The step is now about 4–5× in most families.

## What's in the sheet
| Pre-industrial | Revenue | Inputs | VA |
|---|---:|---:|---:|
| Basic Planting | 1.0 | 0 | 1.0 |
| Simple Forestry | 1.0 | 0 | 1.0 |
| Basic Extraction | 0.8 | 0.17 | 0.63 |
| Manual Sewing | 1.6 | 0.32 | 1.28 |
| Live Performance | 1.0 | 0.19 | 0.81 |
| Artisanal Goods | 2.5 | 0.3 | 2.2 |
| Crude Tools | 1.2 | 0.5 | 0.7 |
| Primitive Steelmaking | 2.0 | 0.98 | 1.02 |
| Craft Machinery | 4.0 | 2.3 | 1.7 |
| Batch Chemical Production | 4.5 | 1.24 | 3.26 |
| Anchorage | 3.0 | 0.54 | 2.46 |

| Industrial | Revenue | Inputs | VA |
|---|---:|---:|---:|
| Intensive Agriculture | 5.2 | 0.84 | 4.36 |
| Iron Tools | 6.0 | 1.45 | 4.55 |
| Mechanized Workshops | 12.0 | 3.15 | 8.85 |
| Mercantile Services | 6.0 | 0.66 | 5.34 |
| Machine Tools | 14.0 | 6.05 | 7.95 |
| Bessemer Process | 16.0 | 5.6 | 10.4 |

`pm_1857_tuning.csv` is the first-pass suggestion, kept for reference, and its Blister row is out of date. The workbook is the source of truth.

## Applied, 2026-10-31
- **Sheet:** Blister Steel is back at revenue 4, inputs 2.12, VA 1.88, so steel runs 2 → 4 → 16 → 17.6. Subsistence is 0.38. The audit has 0 mismatches.
- **UK start PMs:** Bessemer for steel, standing in for puddled wrought iron: 8.6 levels and the doc's 69K workers make the doc's 229 steel a month after modifiers. Spinning Machines for textiles makes 1.7× the doc after modifiers.
- **Wages:** `base_wage` is 1.8 for ENG and 0.3 for the 16 Indian tags, set in their history files just before `set_tech_*`.
- **Wage floor:** `base_wage_finalize` floored every state at 1.0, which cancelled the Indian wages and left laborers at 2.0 against a tier with VA around 1.0. It's now subsistence productivity / 2, at least `global.minimum_base_wage`.

## Worth a look
- **Basic Extraction (VA 0.63) and Crude Tools (0.7)** stayed near the first pass while the rest of the tier rose. At a Russian wage of 0.3 they barely pay. Basic Extraction at output 0.6 and Crude Tools at 0.3 would match the tier.
- **Mercantile Services** can go back to 5.0. Hiding domestic service and housing means it no longer needs 6.0: at 5.0 it makes about 1.1× the doc after modifiers.
- **Tags with no `starting_pm` lines** (GWA, KAS, MYS, REW, RJP, BTR) start on Intensive Agriculture and Blasting. Fine if they should outproduce RAJ.
- **Ranches** aren't in the sheet: they're in `pm_legacy_data.json`. Slaughterhouses is 8.2 and makes 1.5× the doc after modifiers. The split is also off: about 3 fiber to 5 food by value, and the UK's was 1 to 8.
- **Other inversions** already in the sheet: Modern Machinery revenue is below Specialized Machinery, Electrochemical Processing is below Industrial Chemical Synthesis, and Electric Arc's VA is below Open Hearth's.

## Wages
Payroll per K is `base_wage × (2 × laborer share + 4 × worker share)`. Keep it near 60% of VA, so `base_wage` ≈ 0.3 × VA per K.

| | `base_wage` now | Suggested | Laborer pay |
|---|---:|---:|---:|
| ENG | 3.2 | 1.8 | £43 a year |
| Indian tags | 1.7–2.4 | 0.3 | £7 a year |
| Others, VA about 1.0 | 1.2–4.0 | about 0.3 | £7 a year |

**Only ENG and the Indian tags have been set.** Every other tag is still on the `set_tech_*` seeds of 1.2 to 4.0, which is far too high for a pre-industrial tag once the map has industry. Wages float by at most 2% a month, so they only need to be close.

## Subsistence
The sheet already has the cut: revenue 1.26 → 0.39. Its effect in the sim, 12 months on the stripped map:

| | India, £ a year | Per head | Food supply / demand | Food price |
|---|---:|---:|---:|---:|
| Old sheet | £1,116M | £4.57 | 33,149 / 35,725 | 2.32 |
| Current sheet | £515M | £2.11 | 9,945 / 32,070 | 8.00 (cap) |

India lands on the doc, but until commercial farms exist, food and wood stay at the price cap. ENG's GDP is 6.0K and world GDP about 227K. That's expected on a stripped map. Raising `peasant_market_interaction` doesn't help: at 0.667, food demand tripled to 97,064 and food stayed at the cap.

## How far to trust this
The subsistence cut has been simulated, for 60 months. The other PM values can't be tested until the map has industry again. The levels are a guide, and fractional.
