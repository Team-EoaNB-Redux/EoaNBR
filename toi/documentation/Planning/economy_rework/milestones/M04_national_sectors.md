# M04: National sectors and target utilisation

**Spec:** §1, §2.1–2.2, §3, §4, §6. **Depends on:** M01, M03. **Questions:** Q18–Q23, Q38, Q55, and the follow-ups Q85–Q91, all decided. **Status:** in progress. Steps 1, 2, 3, 5, 6, 7, 8 and 9 are done, in the simulator and in Strat's month-1 save. Step 4 is built as far as Q88 goes. The national figures a sector screen needs are stored (Q91), checked the same way. Still to do: the national sector UI. Strat's order: step 2, then 1, 3 and 6, then the rest. Reference run: `redux-eco-sim/runs/m04_q91` (`world_1857_eng`, 60 months, `--watch-file watches/m04.txt`). The M03-code baseline is `runs/m04_base`.

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

## Decided while building
- **Q85:** subsistence farms and the three government buildings (arms factory, industrial complex, dockyard) stay outside the sector layer until M05 and M08.
- **Q86:** sectors pay corporate tax on positive operating profit only. Dividends and subsistence rent aren't taxed again.
- **Q87:** capacity decay applies to buildings only, and is gated behind `global.eco_investment_enabled` until M09.
- **Q88:** each sector is the generic owner's slice. Company slices wait for M10.
- **Q89:** states keep no per-good figures. National supply and demand come from the sectors, state GDP is each industry's value added, and the market screen's per-state lists go. Each sector lists its biggest states instead.
- **Q90:** a state-industry stores only what calculations need, where dropping it would cost performance. What only the localisation reads is worked out there.
- **Q91:** the national figures a sector screen needs, which no state-industry stores, are added up monthly in the passes that already visit every state-industry. Per-good figures are left to the localisation, since they loop over a sector's own methods, not its states.
- **Step 5's numbers** weren't specified (the spec leaves "the exact controller" open). They follow Q20's shape and are globals for M14 to tune: start at 80% (where every industry started), rise above a 10% national margin, fall below 0, 1 point plus 50 per unit of margin beyond those, at most 5 points a month, floor 10%. The local shift is 50 points per unit of margin above or below the national margin, at most 5 points. The trailing margin moves a fifth of the way to each month's. The old controller's damping in tight local labour markets is gone: job fulfilment and the floating wage already limit hiring where workers are scarce.
- **Step 7's numbers** likewise: a building whose trailing margin is below −5% loses 1% of its generic size a month, and its generic share closes below size 0.1.

## What was built
### Step 2: the PM/AM cache (2026-11-13)
- **Market layer** (`market_cache_update`, `_economy_market.txt`). It runs at the end of `market_prices_update`, so whenever a market's actual prices change: monthly, and at each startup snap. For every sector and method a member uses, it works out, at the market's prices and before modifiers:
  - `market_output_value@<sector>`: what one size of the sector makes, per unit of its PM's output amount. Output separates into industry × PM, since a PM's output is one scalar (`global.pm_output_amount@`) and each industry's goods split is fixed.
  - `method_input_cost@<method>` and `method_construction_cost@<method>`: what a PM's or AM's inputs and construction list cost, per K of base workforce. A state-industry's input cost is its PM's plus its AM's.

  So the cache holds one value per sector and per method, not one per PM/AM combination, and needs no two-key variables. The leader keeps the market's copy, stamped with the price update it belongs to (`market_cache_stamp`), and copies it to each member that uses it. Countries and states read their own copy, one hop away (`controller:market_output_value@var:bu_token`).
- **Country layer:** the country's existing per-sector and per-method modifiers, `industry_*_factor@<sector>` and `pm_*_factor@<method>`, recomputed monthly after modifiers change (`r_update_modifiers_country_effects`, `update_pm_modifier_factors`). A state-industry multiplies them in when it reads the market values. That costs a few multiplications per industry, and nothing has to be invalidated when prices or modifiers change.
- **Registration** (`cache_register_industry`, `_economy_industries.txt`): `industry_update` puts each industry's sector and methods on the controller's `sectors` and `methods_in_use` lists. The first time a country meets one, it works out its own value at once (`cache_sector_calc`, `cache_method_calc`), and the next price update adds it to the market's. This covers startup (states register before the first snap), conquest and new construction.
- **Readers:** `industry_update` takes goods revenue, input costs and asset value from the cache instead of looping over goods and prices. The asset value no longer calls `get_construction_cost` for every industry every month. The getters (`get_pm_values`, `get_am_values`, `get_construction_cost`, `get_retooling_cost`) read the cache through three new trigger helpers (`get_sector_output_value`, `get_method_input_cost`, `get_method_construction_cost`), which fall back to the controller's prices for a sector or method the country doesn't use, such as a PM in the selection list. They stay trigger-safe.
- **Deleted:** the per-good money arrays `revenue_goods@<industry>^i`, `input_cost@<industry>^i`, and the full-production arrays `production_max@` and `input_max@`. The two tooltips that read the money arrays now work them out from `production@`/`input_amount@` and the price. `industry_productivity_sort` no longer runs every month: only the startup wage fallback (`base_wage_calculation`) reads its output.
- **Step 9 (AM labour cuts)** needed no change: `industry_update_size_jobs` adds the AM's share to the PM's, and floors each class at zero (`max = 0`) before jobs and the payroll multiplier are worked out.

**Results** (`runs/m04_s2` against `m04_base`, 60 months): every watch matches within rounding, the largest gap 0.005% (Lancashire coal profit). The machine ran about 6% slower during the second run (untouched effects such as `r_weekly_trade` and `trade_update` rose 6–7%). Against that, `industry_update` fell from 0.67 s to 0.58 s and `industry_productivity_sort`'s 0.34 s is gone, while the cache costs 0.10 s (`market_cache_update` 0.06 s, `cache_register_industry` 0.04 s). On the stripped map the industries are a small cost. The large ones are in the market: `market_update` (52 s of 129 s), and within it `national_market_update` (19 s) and `state_market_update` (14 s), which the weekly tick re-sums from every state although production only changes monthly. Step 3 moves that sum to the sectors.

### Steps 1, 6 and 8: sector records, the profit split and losses (2026-11-13)
- **Sector records** (`sectors_update`, `_economy_industries.txt`, country scope). After the state loop, each country adds up every sector's state-industries (Q85: not subsistence farms or the government buildings, `is_sector`) into one record per industry token: `sector_size@`, `sector_generic_size@` (less what companies hold), `sector_jobs@`, `sector_employed@` (split by class since Q91), `sector_revenue@`, `sector_inputs@`, `sector_payroll@`, `sector_maintenance@`, then `sector_profit@` (operating profit) and `sector_margin@`. It reads each state-industry's stored figures in a pass of its own, rather than adding them up inside `industry_update`, because content, construction and the GUI also call `industry_update` mid-month, and that would count them twice. Target utilisation (step 5) will join the record.
- **The profit split** (Q21, Q39, Q86):
  - A positive profit pays corporate tax at `corporate_tax_percentage_actual` (`sector_profit_tax@`). The budget's corporate tax is now the sectors' total (`sectors_profit_tax`), less corruption. The upper class no longer pays corporate tax on its dividends, so `pops_corporate_tax_spending` is gone, and so is its line in the pops-finance tooltip (all three languages).
  - The sector keeps `global.sector_retained_share` (0.3, new in `buildings_global_var_setup`) × investment appetite (`calculate_investment_appetite`, from incentives; at most 0.8) of what's left (`sector_retained@`), and pays the rest as dividends (`sector_dividends@`, `sector_dividend_per_size@`).
  - `sectors_monthly` moves last month's retained earnings into `sector_capital@` before `sectors_update` runs, as companies do, so the update stays idempotent. Startup runs `sectors_update` before and after the states' finalization, so their first dividends exist.
- **Losses** (Q22): a loss comes out of `sector_capital@` first (negative retained earnings, never taking capital below 0), and what capital can't cover comes out of dividends, which go negative.
- **Dividends by size** (Q11 a): `industries_update` pays each state's upper class `sector_dividend_per_size@` × the generic size there (`owner_sizes_local@`), from last month's accounts, the same one-month lag as before. Each state-industry's `dividends@` is its size's share, which the companies MVP and the finance tooltip read. Subsistence rent and the government buildings pay their own `dividends@` as before.
- **Deleted:** the employees' bonuses (`pops_bonuses@`, `working_bonuses@`, `middle_bonuses@`), the per-industry cash reserve (`money@`, `money_limit@`, `money_accumulation@`, `global.building_money_limit`, the startup block that filled it, and its rows in the finance tooltip), and the scrap-based downsizing plan and its execution (`downsize_amount@`). The hiring AI's extra firing on low cash is gone with the cash, and so are its console test (`test_target`) and `calculate_projected_profitability`, which nothing called.

**Results** (`runs/m04_s16` against `m04_base`, 60 months):

| ENG at month 60 | Baseline | Steps 1, 2, 6, 8 | |
|---|---:|---:|---|
| GDP | 9,579 | 9,559 (−0.2%) | |
| Revenue | 5,642 | 5,464 (−3.2%) | Income tax −6.7% on lower earnings |
| Pop earnings | 12,862 | 11,840 (−7.9%) | No bonuses |
| Pop debt | 34,836 | 28,907 (−17%) | Lower income, so less to overspend |
| Test industries' profit | | +42 to +49% | No bonuses |
| London's upper-class dividends | 1,204 | 1,233 (+2.4%) | 70% of a larger profit |
| Sector capital | — | consumer goods 19,336, textiles 9,700 | Accumulates, unspent until M09 |

Employment, prices and wages are within 0.4%, except West Midlands' wage (+2.6%), where the steel foundry and tooling workshop now hire faster: without bonuses their margins are higher. Britain's sectors retain about 1.3K a month, which leaves circulation as pop investment does until M09. Profit tax is checked by hand: ENG's corporate tax rate is 0 and no other country has a profitable sector on the test bed, so at a 10% rate the consumer goods sector's 1,047 profit pays 104.7, retains 32.5% of the rest, and the budget collects the total less 1% corruption.

### Step 3, part 1: the market adds up each country's states once a month (2026-11-13)
The weekly trade tick and the leaders' monthly market update used to add up every member's states again (`state_market_update` per state, then a loop over every state and good in `national_market_update`), and to rebuild the market screen's top-five lists for every good, though production and pop demand only change in the monthly tick.
- Each state now works out its goods supply and demand (`state_market_update`) at the end of its own monthly update, and the country adds them up once, after its state loop (`national_market_states_update`: `states_need@<good>`, `states_production@<good>`, and its per-good lists of producing and consuming states).
- `national_market_update` adds military demand and HOI4's resource use to those totals. With `ignore_state_market_temp` (set by the monthly and weekly ticks) it uses the cached totals; otherwise it works out and adds up the states again, which is still the default for startup, joining a market, content and the budget buttons.
- The market screen's top producers and consumers left `market_calculations`, which trade runs several times a week, for `market_statistics_update`, run monthly by each leader and at startup.

The numbers can't change. A member that ticks after its leader showed its previous month's states to the leader's monthly update before as well, since its states hadn't updated yet, and its cache holds exactly those values.

**Results** (`runs/m04_mk` against `runs/m04_s16`, 60 months): every watched value matches exactly, every month. The ticks take 89 s instead of 140 s (129 s in the baseline): 1.49 s a month against 2.15. `r_weekly_trade` takes 35 s instead of 75 s in the baseline, `market_update` 15 s instead of 52, `market_calculations` 9 s instead of 29, `state_market_update` 1.9 s instead of 14, and `national_market_update` 7 s instead of 19. The two new effects cost 4.6 s together.

### Step 3, part 2: no per-good state figures, and a slim state-industry (2026-11-13)
- **Goods by sector and method** (Q89). Each state-industry stores two scalars instead of its per-good arrays:
  - `output@`: bundles of its base production made this month (PM output amount × production multiplier × base workforce × modifiers × size × production percentage). It makes `output@` × each good's `global.building_base_production_amount@`, and its goods revenue is `market_output_value@` × `output@`, so the cache's output value is now the value of one bundle.
  - `input_scale@`: K of base workforce at work in input terms. It uses `input_scale@` × each of its PM's and AM's input amounts, and its input cost is (PM's + AM's `method_input_cost@`) × `input_scale@`.
  - `national_market_states_update` adds these up by sector (`output@<sector>` on the country) and by method (`method_scale@<method>`, split by sector since Q91), then turns them into `states_production@<good>` and `states_need@<good>` once per country. Subsistence farms (not a sector) add their goods, and each state its pops' demand (`pops_need@`, the 15 goods pops buy), construction and retooling. `state_market_update` and every state's per-good `production@`, `demand@`, `demand_input@` and `supply@` are gone.
- **State GDP** (`gdp_update`) is Σ (`revenue@` − `expenses_input@`) over the state's industries: value added. That covers subsistence farms (their own food at base prices), railways and ports, and the government buildings, as before.
- **The market screen's per-state lists** (`market_production_states@`, `market_consumption_states@`, and each country's `production_states@`/`consumption_states@`) are gone. `sectors_update` lists each sector's five biggest states by size (`sector_states@<sector>`, biggest first) for the UI to use.
- **What a state-industry stores** (Q90): size, PM and AM, construction and retooling state, ownership (`owner_sizes@`, `owner_sizes_local@`), jobs and employment per class (`working_jobs@`, `middle_jobs@`, `owner_jobs@`, `working_employed@`, `middle_employed@`), `payroll_multiplier@` and `production_percentage@` (read in a later pass), `output@` and `input_scale@`, the money the accounts and GDP add up (`revenue@`, `expenses_input@`, `expenses_payroll@`, `expenses_maintenance@`), `dividends@` (the companies MVP reads it), the trailing `margin@` (step 5), and transport capacity (`industrial_capacity_use@`, and for railways and ports `industrial_capacity@` and `shipping_capacity@`). The government buildings and subsistence farms keep their own records until M08 and M05.
- **Deleted from each state-industry:** `jobs@`, `jobs_available@`, `employed@`, `employment_percentage@`, `employment_target@` (step 5), `profitability@`, `profit@`, `expenses@`, `productivity@`, `asset_value@`, `revenue_goods@`, `revenue_shipping_capacity@`, `revenue_industrial_capacity@`, `arable_land_use@` (`subsist_and_arable_update` works it out from size), the three `*_max` transport figures, the `production@`, `input@`, `input_base_amount@` and `input_amount@` arrays, `input_compiled_pm@`/`am@`, and the unused dirty flag (`prev_size@`, `industry_dirty_var@`, and the monthly modifier comparison in `r_update_modifiers_country_effects` that set it).
- **Readers moved:**
  - Tooltips: the scripted localisation works the dropped figures out through three new trigger getters, `get_industry_figures` (employment, transport revenue, goods revenue, expenses, profit, margin, productivity), `get_industry_input` (the goods used, the PM's and AM's merged) and `get_industry_utilisation`. The RGO and subsistence tooltips read `GetIndustryOutputAmount0`–`2`.
  - Productivity is now (revenue − inputs − maintenance) per wage-weighted worker. That's the old figure with its production-percentage adjustment folded in, but it reads 0 when nobody works there, where the old one showed what the PM could earn.
  - The companies MVP adds up expenses and employment from the per-class figures, and its asset value calls `industry_asset_value_calc`.
  - The startup wage fallback (`base_wage_calculation`, for states whose history and controller set no wage) now uses subsistence productivity alone, and `industry_productivity_sort` is gone. No state on the 1857 map uses the fallback.
  - The gated investment file still reads `asset_value@`, `profitability@`, `employment_target@` and state `production@`, alongside the PM fields it already lacked. M09 replaces it.

**Results** (`runs/m04_s3b` against `runs/m04_pre3`, the same code before this step, 60 months):
- The goods totals match to rounding, and so does everything that depends only on them.
- **Market GDP** values a member's month at that month's prices: it reads each state's stored revenue. The old GDP multiplied last month's quantities by this month's prices for members that tick after their leader. The same quantities at current prices reproduce the old figure exactly (44,086.91 against 44,086.92 at month 3), so the gap is the price timing alone. It's +3.7% at month 3, while prices fall, and +0.16% by month 12. ENG's own GDP is within 0.01%.
- Trade shares within a market follow GDP, so small differences follow: coal demand +1.3% at its largest (month 29), wealth +0.2%, pop debt +0.1%.
- **Speed:** the monthly ticks take 26.6 s instead of 36.2 s, and the whole run 0.95 s a month instead of 1.17. The national goods totals take 0.4 s instead of 3.6 s (with `state_market_update`), state GDP 0.15 s instead of 1.2 s, the market screen's lists 0.5 s instead of 1.7 s, and `r_update_modifiers_country_effects` 1.6 s instead of 2.5 s.

### Step 5: target utilisation (2026-11-13)
- Each sector has a national target utilisation, `sector_utilisation@<sector>` (%), set to `global.sector_utilisation_start` (80) when the country first registers the sector. `sectors_monthly`, which now runs before the state loop, steps it once a month from last month's national margin (Q20's damped step; the numbers are above).
- A state-industry offers that share of its jobs, shifted a few points by how its trailing margin `margin@` compares with the national margin (`industry_utilisation_calc`, and `get_industry_utilisation` for tooltips). The government buildings always offer 100%.
- `industries_monthly` replaces `on_monthly_industry_ai` in the state loop. It moves each sector state-industry's trailing margin toward last month's profit over revenue, worked out from the stored figures. A new state-industry's trailing margin starts at its first month's.
- **Deleted:** `employment_target@` and `on_monthly_industry_ai`, the 80% startup loop in `state_eco_employment_init`, and the employment-target carry-over on resizes in `add_x_industry_internal` and `add_rgo_internal`. New capacity works at its sector's target at once, within what the state's labour can fill.

**Results** (`runs/m04_s5` against `runs/m04_s3b`, 60 months):
- **Smoother ramp:** utilisation climbs 5 points a month from 80% and reaches 100% by month 4, where the old targets got there in one or two months. The steel foundry, which starts at a loss, dips to 75% and recovers (the old target fell to 62%). The largest monthly swing in the London consumer goods factory's production falls from 11.3 to 3.8 points. Wages in both test states move less and no longer reverse.
- **Month 60:** GDP +0.04%, revenue +0.05%, pop earnings −0.09%, pop debt +2.8%, the West Midlands wage −5.2% and London's −1.4%.
- **Startup:** the government buildings offer all their jobs from the first pass, where the old code used the 80% start for one pass. That's 0.8K more upper-class owners in Britain at startup.
- **Local shift:** every test sector's margin is far above the rise threshold, so all sit at 100%, and the shift only shows up by hand. A coal mine with a 0.65 trailing margin against 0.70 nationally works at 97.3%; at 0.30 it hits the 5-point cap, 95%.

### Step 7: capacity decay (2026-11-13)
`industries_monthly` shrinks a building whose trailing margin is below `global.industry_decay_margin` by `global.industry_decay_rate` of its generic size a month, through `add_x_industry_internal`, and closes the generic share once the building is below `global.industry_decay_floor`. Companies' shares are theirs to decide (§3.1). RGOs follow their deposits (Q87). It runs only while `global.eco_investment_enabled` is on, so it's checked by hand: with the gate and a high threshold set in West Midlands, the steel foundry and tooling workshop each lost 1% (1 → 0.99, 2 → 1.98), the iron mine was untouched, and a workshop below the floor closed and left the state's list.

### Q91: national sector figures (2026-11-13)
The figures a national sector screen needs that weren't stored are now kept on the country, added up once a month in the two passes that already visit every state-industry:
- **`sectors_update`:**
  - Jobs and employment per class (`sector_working_jobs@`, `sector_middle_jobs@`, `sector_working_employed@`, `sector_middle_employed@`), replacing `sector_jobs@` and `sector_employed@`.
  - Transport demand (`sector_transport_demand@`) for every sector. For railways and ports, their capacity and what they're paid for transport at each state's rate (`sector_industrial_capacity@`, `sector_shipping_capacity@`, `sector_transport_revenue@`).
  - What's under way: `sector_construction@` (size being built, counted before the first size exists) and `sector_retooling@` (size retooling).
  - RGO reserves (`sector_known_reserves@`, `sector_potential_reserves@`), whether or not a deposit is worked.
- **`national_market_states_update`:** the method mix, in four arrays per sector parallel to the building's method lists: `sector_pm_size@<sector>^i` and `sector_am_size@` (the size on each PM and AM), and `sector_pm_scale@` and `sector_am_scale@` (their `input_scale@`). Each state-industry finds its PM's and AM's places in the lists (at most 14 entries). The scale arrays replace `method_scale@<method>`: the market's goods totals now come from each sector's methods, so a method shared between sectors (most AMs) is split between them.

**Results** (`runs/m04_q91` against `runs/m04_q91_base`, the same code before the change, 60 months):
- Every watched value matches within 0.0003%. The gap is rounding: a shared method's inputs are now multiplied sector by sector.
- The two passes take 0.92 s instead of 0.81 s over 60 months, against 79 s of ticks.
- A console test gives the expected sums. It added 2 railways and a port in Lancashire, started a steel foundry there and started two retools. The railway's 53.27 capacity × 0.25 is its 13.32 transport revenue, and the port's (5.91 − 25.70 × 0.23 + 25.70) × 0.25 is its 6.43.
- **In-game check (2026-11-14), on Strat's month-1 autosave:** no zeroed math expressions, and the arrays have the simulator's lengths, with the same slots filled. In every country with sectors (ENG and USA), each national figure equals the sum of the save's own state figures: jobs and employment per class, transport demand, construction, retooling, revenue, goods made, and the size and input scale on each method. Against the simulator, jobs and employment match exactly, and goods, input scales and transport demand run about 1% higher, the throughput gap below. Reserves differ by state because startup rolls them at random. Five countries' reserves aren't the sum over the simulator's map because control differs: in-game QNG holds the GXC, SIC and YAL states, and D01, a dynamic tag the simulator lacks, holds Prussia's state 492. No railways or ports exist on the test bed, so their figures were checked only by the console test.

### Still to do
- **Step 4** is built as far as Q88 goes: each sector is the generic owner's slice (`sector_generic_size@`), and dividends follow the generic size.
- **In-game check (2026-11-13), on Strat's start save and month-1 autosave:** no load errors and no zeroed math expressions. The new figures match the simulator: target utilisation exactly, the sector state lists, employment per class and production percentages exactly, the trailing margins (except steel and tooling, below). Goods made and used, revenue and costs run about 1% higher in-game. Month 1: GDP within 0.2%, market GDP 0.08%, revenue 0.02%, pop debt 0.003%, sector dividends and retained earnings 0.4%. Two gaps, neither from M04:
  - **Throughput:** HOI4's national industry throughput modifier is 1.3 points higher in-game for every industry (0.145 against 0.132 for coal). That's the 1%.
  - **Steel:** Prussia, Denmark and Spain use 1.5, 3 and 4 less steel for military production in-game. That halves steel's startup price (4.83 against 9.64), so the steel foundry and tooling workshop margins differ.
- The new tooltip getter (`get_industry_figures`) logged thousands of divide-by-zero warnings in-game, for idle and empty industries. Its divides are now guarded.
- **The national sector UI:** what it can show, and where each figure comes from, is in the next section. The screen itself is planned in [ui_planning.md](../ui_planning.md) §5.2, Macro → Sectors (phase U2).

### UI fixes
- **The PM selection tooltip** (`pm_entry_tt`) was deleted from the English localisation in "Economy rework part 1" (`487bd9311`). Korean and Russian still had it. It's restored. Hovering over the active PM worked because that tooltip (`building_production_method_tt`) is a different key around the same inner text (`GetPMLoc`).
- **PM inputs were shown as percentages** (`pm_input_loc`, `|-=1%`), left over from when inputs were modifiers. They're goods per K of base workforce, so they now read like the outputs: `0.50 per K`. English only; Korean and Russian still use the old format.

## National sector UI: what a sector screen can show
For a country-level screen with one entry per sector. No such screen exists yet, and nothing selects a sector (a state screen uses `ROOT.selected_industry`).

**Basics:**
- **Scope:** everything below is on the country. Its `sectors` array lists its sectors: every building, RGO, railway and port with a state-industry anywhere in the country, including one only under construction or an RGO with reserves but no worked deposit. Subsistence farms and the government buildings aren't sectors (Q85).
- **Timing:** the figures are last month's (`sectors_update` and `national_market_states_update`, after the state loop). Target utilisation and capital are this month's (`sectors_monthly`, at the start of the tick).
- **Getters:** the PM getters (`get_pm_values`, `get_construction_cost`) already work in country scope, with an infrastructure efficiency of 1. No sector getters exist yet: the UI work adds what it needs, from the formulas below.
- **Method arrays:** the method mix is kept in arrays parallel to the building's method lists. `sector_pm_size@<sector>^i` is the size running `global.building_production_methods@<sector>^i`, and `sector_pm_scale@<sector>^i` its input scale (K of base workforce at work, in input terms). `sector_am_size@` and `sector_am_scale@` do the same for `global.building_automation_methods@`. A method nobody uses reads 0.

**What the state-industry tooltips show, and the sector's equivalent:**

| State-industry shows | Sector equivalent | Status |
|---|---|---|
| Size | `sector_size@`, and `sector_generic_size@` (less companies' holdings) | Stored |
| PM and AM | The method mix: `sector_pm_size@^i` and `sector_am_size@^i` over `sector_size@` is each method's share | Stored |
| Goods made, per good, and their value | `output@<sector>` × `global.building_base_production_amount@<sector>^i`, × `price@<good>` | Loc can work it out |
| Goods used, per good, and their cost | For each method i with a scale, `sector_pm_scale@^i` × each of its input amounts (`global.pm_input@<method>^j`, `global.pm_input_amount@<method>^j`), and the same for the AMs. Method i's input cost is `sector_pm_scale@^i` × `method_input_cost@<method>`, and all of them add up to `sector_inputs@`. A loop over the sector's own methods, not its states | Loc can work it out |
| Transport demand | `sector_transport_demand@` | Stored |
| Transport capacity and revenue (railways, ports) | `sector_industrial_capacity@`, `sector_shipping_capacity@`, `sector_transport_revenue@` (transport at each state's rate, shipping at the shipping price, since M07) | Stored |
| Employed and jobs, per class | `sector_working_jobs@`, `sector_middle_jobs@`, `sector_working_employed@`, `sector_middle_employed@`. The totals are their sums | Stored |
| Employment % | Wage-weighted, as the state tooltip: (working employed × `global.wage_multiplier@token:working_class` + middle employed × `global.wage_multiplier@token:middle_class`) over the same for jobs | Loc |
| Employment target | `sector_utilisation@`, the national target. Each state works within `global.local_utilisation_shift` of it | Stored |
| Revenue, inputs, payroll, maintenance | `sector_revenue@`, `sector_inputs@`, `sector_payroll@`, `sector_maintenance@` | Stored |
| Expenses, profit, profitability | Their sum; `sector_profit@`; `sector_margin@` | Loc / stored / stored |
| Goods revenue vs transport revenue | Goods revenue is `sector_revenue@` − `sector_transport_revenue@` | Loc |
| Dividends | `sector_dividends@`, `sector_dividend_per_size@` | Stored |
| Productivity (the card number) | (revenue − inputs − maintenance) per wage-weighted worker, the employment % numerator | Loc |
| Average pay | `sector_payroll@` over working + middle employed. Slaves are employed but unpaid, so in the slave states this is pay per worker, not the wage | Loc |
| Construction and retooling under way | `sector_construction@` (size being built), `sector_retooling@` (size retooling) | Stored |
| RGO deposits | `sector_known_reserves@`, `sector_potential_reserves@`. The worked deposit is `sector_size@` | Stored |
| PM and AM tooltips (economics per size, retooling cost) | `get_pm_values` and `get_retooling_cost` with `industry_token` = the sector, in country scope. A PM's tooltip should read the same in every state of the country, apart from local wage, Infrastructure Efficiency and economy of scale | Works now |

**Only at sector level:**
- **Profit split:** profit tax (`sector_profit_tax@`), retained earnings (`sector_retained@`) and capital (`sector_capital@`, unspent until M09). The country totals are `sectors_profit_tax`, `sectors_retained` and `sectors_dividends`.
- **Target utilisation:** `sector_utilisation@`, and where it's heading. Above `global.sector_utilisation_rise_margin` (10%) it rises; below 0 it falls; at most `global.sector_utilisation_step_max` (5) points a month.
- **Biggest states:** `sector_states@<sector>`, five states by size, biggest first. Each entry is a state scope, so the state getters work on it: size, its trailing `margin@`, its utilisation (`get_industry_utilisation`) and the rest of `get_industry_figures`.
- **Share of national output:** `output@<sector>` × each good's amount, over `local_production@<good>`.
- **Market prices behind it:** `market_output_value@<sector>` (one bundle of its goods at market prices), and `method_input_cost@` / `method_construction_cost@` for each method.
- **National modifiers:** `industry_throughput_factor@`, `industry_output_factor@`, `industry_input_factor@` on the sector, and `pm_throughput_factor@`, `pm_employment_factor@` on each method.
- **Methods available:** what the country has unlocked (`building_unlocked_pms@` and `building_unlocked_ams@`, per sector), and the newest (`latest_production_method@`, `latest_automation_method@`). Every method a building can use is in `global.building_production_methods@` and `global.building_automation_methods@`.

## UI catalogue: how the state industry screens work
For the UI rework once the systems work. Everything below is in state scope, and the selected industry's token is `v`.

**Windows** (`interface/economy.gui`, `scripted_guis/economy_and_demographics.txt`):
- `state_economy_window` (`state_economy_window_container`) lists the state's industries with two dynamic lists: `urban_buildings_list` over `buildings` (`building_container`) and `rgos_list` over `rgos` (`rgo_container`). Railway, port, the three government buildings and subsistence farms each have a fixed container of their own (`railway_*`, `port_*`, `industrial_complex_*`, `arms_factory_*`, `dockyard_*`, `subs_farm_*`), with their own visibility triggers and click effects.
- `construction_list` (`building_construction_container`) lists `construction_show` (built by `refresh_construction_list`). It reads `controller:latest_production_method@` and calls `get_construction_cost`.
- `pm_list` (`building_pm_list_container`) lists `ROOT.pm_show` (`refresh_pm_list`), every PM or AM of `ROOT.selected_industry`, with `ROOT.selected_pm_type` 0 for PMs and 1 for AMs. Clicking an entry sets `retooling_pm@`, `retooling_financier@` and `retooling_time@`.
- No country-level industry view exists.

**Clicks:** `building_increase_size_button` → `construct_x_industries`; `building_decrease_size_button` lowers `construction@`; the PM and AM buttons open `pm_list`; `rgo_prospecting_button` sets `prospecting@`, `prospecting_financier@` and pays `prospecting_cost@`. The click-enabled triggers call `can_build_industry`, `is_valid_industry` and `get_construction_cost`, against `ROOT.treasury` × `global.start_construction_cost_multiplier`.

**Tooltips** (`localisation/english/economy_l_english.yml`, with scripted localisation in `scripted_localisation/economy_scripted_loc.txt`):

| Tooltip | Text | Reads, per state-industry |
|---|---|---|
| `building_tt`, `rgo_tt` | `GetIndustryPMTotalLoc`, `GetIndustryEmployment`, `GetIndustryFinancesShort`, `GetIndustryConstruction` | `production_method@`, `automation_method@`, `production@^i`, `input@^i`, `input_amount@^i`, `industrial_capacity@`, `shipping_capacity@`, `revenue_*_capacity@`, `industrial_capacity_use@`; `employed@`, `jobs@`, `working_employed@`, `working_jobs@`, `middle_employed@`, `middle_jobs@`, `employment_percentage@`, `employment_target@`; `revenue@`, `expenses@`, `profit@`, `profitability@`, `productivity@`; `size@`, `construction@`. RGOs also read `base_resource@`, `known_reserves@`, `potential_reserves@` |
| `building_productivity_tt`, `rgo_productivity_tt` | `GetIndustryFinances` | `revenue@`, `revenue_goods@`, `revenue_industrial_capacity@`, `revenue_subsidies@`, `expenses@`, `expenses_input@`, `expenses_payroll@`, `expenses_maintenance@`, `profit@`, `profitability@`, `dividends@`, `money@`, `money_limit@`, `money_accumulation@` |
| `building_productivity` (the number on the card) | `GetIndustryProductivityV` | `productivity@`, coloured against `base_wage` |
| `building_production_method_tt`, `building_automation_method_tt`, `rgo_*_method_tt` | `GetIndustryPMLoc`/`GetIndustryAMLoc` → `GetPMLoc` (`pm_main_loc`), plus `GetIndustry*Retooling` | Global PM data, `get_pm_values` for "Base Productivity"; `retooling_pm@`, `retooling_time_left@`, `retooling_cost@`, `retooling_resources@^i`, `retooling_amount@^i`, `retooling_cost@^i` |
| `pm_entry_tt` (the PM list) | `GetPMListTooltip` → `GetPMLoc`, `GetPMListRetoolingLoc` | Same as above, for `v` in the list. `pm_entry_productivity` calls `get_pm_values` for each entry |
| `industry_construction_tt`, the construction section | `GetIndustryConstruction*` | `construction@`, `construction_time_left@`, `construction_cost@`, `construction_resources@^i`, `construction_amount@^i`, `construction_cost@^i`; `get_construction_cost` |
| Card icons (`properties`) | `GetIndustryEmploymentIcon`, `GetIndustryPMIcon`, `GetIndustryAMIcon` | `employment_percentage@`, `production_method@`, `automation_method@` |
| `railway_tt`, `port_tt` and their finances | `GetRailway*`, `GetPort*` | The same variables on `token:railway` and `token:port` |
| `subs_farm_tt` | `GetSubsFarm*` | `production@token:subsistence_farm^i`, `peasants_employed@`, `owner_jobs@`, `revenue@`, `expenses_payroll@`, `dividends@`, `productivity@` |

**Elsewhere:** the market screen's resource tooltips (`GetResourceListSupplyStateList`, `GetResourceListDemandStateList`) showed each market's top five producing and consuming states per good. Step 3 removed those lists (Q89), so they're empty now. Each country's `sector_states@<sector>` (its five biggest states per sector) is there to replace them. The state GDP (`gdp_update`) is now each industry's value added.

**What M04 changed for the UI:** the table above is the state screens as they were. Step 3 removed most of the per-industry figures it lists, and the tooltips now work them out:
- **Getters:** `get_industry_figures` gives employment, transport and goods revenue, expenses, profit, margin and productivity. `get_industry_input` gives the goods used, and `get_industry_utilisation` the share of jobs on offer, which replaces "employment target".
- **Goods made:** they're `output@` × each good's amount. The RGO and subsistence tooltips read them through `GetIndustryOutputAmount0`–`2`.

The finance tooltip's cash rows went with step 6. The numbers should read as before, except productivity (0 when nobody works there) and the employment target (now the target utilisation). That's checked in the simulator only. Nothing in the UI shows the national sectors yet.

**Spotted, not fixed:** the retooling section of the PM tooltip (`pm_retooling_main_loc`) lists the method's operating inputs (`GetPMInput*Loc`, `global.pm_input@`) where retooling pays its construction list (`global.pm_construction_input@`). The retooling cost list in the industry tooltip (`GetIndustryRetoolingInputLoc`) ran to the length of the operating inputs; it now runs to the length of its own list.
