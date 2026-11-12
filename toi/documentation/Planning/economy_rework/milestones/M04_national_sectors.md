# M04: National sectors and target utilisation

**Spec:** §1, §2.1–2.2, §3, §4, §6. **Depends on:** M01, M03. **Questions:** Q18–Q23, Q38, Q55, all decided. **Status:** not started.

## Goal
The country-sector becomes the unit that makes decisions and keeps the accounts, and the state-industry is where it physically happens. PM/AM economics are cached once a month as high up as possible, and states only apply local factors. A national target utilisation replaces each industry's own hiring decision.

This milestone also carries the performance goals of [archive/05](../archive/05_country_level_industries.md): fewer state passes, fewer stored variables, nothing rebuilt from scratch that can be cached.

## Exists now
- **Per state-industry:** size, `employment_target` (10–100, from `on_monthly_industry_ai`, moving up to +20 or −25 points a month), production and input arrays, payroll, profit, `money_accumulation`, dividends and `asset_value`.
- **Profit:** a third goes to employees as bonuses. The rest is split between the cash reserve and dividends.
- **PM data:** static PM and AM data are globals (`global.pm_output_amount@` and so on). `get_pm_values` is a trigger, because the GUI and scripted localisation call it. `update_national_production_methods` and `industry_productivity_sort` run every tick.
- **Production:** `industry_production_update` runs per industry per tick, and its `industry_dirty_var` gate is commented out. The biggest costs in the simulator profile are `r_weekly_trade`, `market_update`, `market_calculations`, `_country_advance_time` and `trade_update`.
- **Downsizing** is built but switched off (`global.eco_investment_enabled`).

## Build
1. **Sectors** (Q18): one country-sector record per industry token, holding capacity, target utilisation, output, inputs, payroll, operating profit and retained capital. M09 spends the capital.
2. **The PM/AM cache** (Q55), in layers:
   - **Global:** static PM and AM data, as now.
   - **Market:** output value and input cost per unit of size, and labour per class, at the market's prices. The market leader computes them once a month after prices move, for the combinations in use.
   - **Country:** every country in a market can have its own modifiers, from technology, laws or anything else, including per-PM ones such as `pm_<x>_throughput_modifier`. The country applies them to the market values once a month, per sector, or per PM/AM combination where a modifier is per PM.
   - **Owner slice:** company bonuses (step 4).
   - **State:** local wage, Infrastructure Efficiency, state modifiers, quality and economy of scale.

   Output value and input cost stay separate, since some modifiers scale only inputs. The getters read the cache and stay trigger-safe.
3. **Slim the state-industry** down to floating size, employment, its one PM/AM pair (Q19), ownership shares, a trailing margin and construction state. Values that can be derived aren't stored.
4. **Owner slices** (Q19): each sector is split by owner once, at the national level. The generic owner of each country is one slice and each company another, with company bonuses applied to their own slice. Results go back to states by each owner's share of the industry there. M10 adds the companies.
5. **Target utilisation** (Q20): a national controller, a damped step on the national margin, plus a small local adjustment from the local margin. Delete `employment_target` and `on_monthly_industry_ai`.
6. **Profit split** (Q21):
   - Remove the worker bonuses and `money_accumulation`.
   - Profit pays profit tax, then a retained share goes to sector capital, and the rest is paid as dividends.
   - The retained share is scaled by incentives (Q39).
7. **Capacity decay** (Q23) on a chronic local loss. Delete the scrap-based downsizing.
8. **Losses before banking** (Q22): no sector borrowing until M11. A loss bigger than retained capital comes out of dividends.
9. **AM labour cuts** (Q38): additive percentages, never taking a job class below zero. This replaces the multiplicative clamp question in [archive/02](../archive/02_pm_assumptions_review.md) and must be in place before M09 lets the AI upgrade.

## Done when
- At month 1, simulator totals match the M03 baseline closely, since this is mostly a restructure.
- Over 60 months, employment is smoother than the baseline.
- Each tick costs less in the simulator profile, and each state stores fewer variables.
- The industry screens still show sensible numbers in-game.

## Carried over
From [archive/05](../archive/05_country_level_industries.md): bake slow modifiers into each state-industry, and rebuild an industry's contribution only when its owner, PM/AM or modifiers change. Economy of scale depends on size and state, so it stays at the state layer.
