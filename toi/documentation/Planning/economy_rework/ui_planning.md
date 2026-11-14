# Economy UI plan

**Status (2026-11-14):** Strat answered UQ1–UQ16 and corrected the budget header, the funding lines, sorting and the Macro tab on 2026-11-13, then answered UQ17–UQ25 on 2026-11-14. The plan below follows those answers, and §9 records them as **Decided**. One question, UQ26, is open, and the plan is written as if its recommendation is taken. Mechanic decisions live with the work that builds them: the funding effects and sector subsidies in M13, player downsizing in the backlog, and the rest of the companies work in M15.

**Sources.** The mockups in this folder set the look and the rough layout: `budget_window.png`, `macro_window.png`, `financial_system_window.png`, `companies_window.png`, `industries_window.png` and `global_economy.png`. They were drawn from prompts written before the rework, which are kept word for word in the appendix.
- **Where a mockup disagrees with the rework, the rework wins:** the spec (`EOANB_Redux_Economy_Redesign_Updated.md`), `decisions.md` and the milestone files.
- **A system that isn't built yet is not a disagreement.** Its block stays in the layout, greyed, so the layout never has to be planned again when the system arrives (Strat, 2026-11-13). Only what a decision removed is cut: pop savings (Q15), cash reserves (Q21) and per-state goods and trade (Q89). "Show on map" is also cut, because no script effect can move the camera.
- Each tab section ends with what changed from its mockup and why.

**How to use it.** Build in the order of §8. Each phase (U0–U5, then the parts tied to later milestones) is a self-contained piece of work for a fresh session: read §2 and §3, then the phase's own section.

## 1. Scope

The top tabs are scopes and the subtabs are sections within a scope (UQ1).

| Tab | Scope | Subtabs | Mockup | Phase |
|---|---|---|---|---|
| Budget | the country's finances | — | `budget_window.png` | U1 |
| Macro | the country's economy | General, Sectors, Financial System, Companies | `macro_window.png`; Sectors has none; `financial_system_window.png`; `companies_window.png` | General U4; Sectors U2; Financial System with M11–M12; Companies with M10 |
| States | the country's states | Overview, Industries, Population (UQ21) | `industries_window.png`, its state view | U3 |
| Global | the world economy | Overview, Industry, Finance, Companies (UQ21) | `global_economy.png` | U5 |

There's also one side panel for details (§3.1) and a few popups.

**Out of scope, left as they are:** the trade and market screens (`countryinternationalmarketview.gui`, the `trade_tab` and `market_tab` scripted GUIs), apart from receiving the tariff controls (§4.1, UQ19); the map-selected state economy window (`state_economy_window`); and the topbar, apart from pointing its buttons at the new window.

**Replaced and deleted** (Q4):
- `country_economy_window`, the old budget window, once U1 does everything it does.
- `population_economy_window`, which despite its name is an old economy overview: a GDP graph, investment opportunities, national opportunities and the MVP companies list. It goes once U4 is in: General takes the graph, Sectors the opportunities (M09) and Companies the list (M10).

## 2. Rules for every window
1. **National first** (spec §1, §20). The player decides about the country, and Macro → Sectors is where industry is decided. The States tab explains and diagnoses, and carries the actions on one state-industry.
2. **Everything planned has its place** (UQ14). A block or control for a system that isn't built yet is in the layout from the start, greyed, with a tooltip naming its milestone, or "not built yet" for the systems with none (§8.1). A greyed figure reads "–". No placeholder numbers.
3. **Everything shown is precomputed** (§3.4). Localisation never loops over states, and nothing evaluated every frame does either.
4. **Money** is shown in pounds at the code's scale (1,000 = £1M), per month, as the game shows it now (UQ3). Green is income or good news, red is cost or bad news.
5. **Controls call wrappers:** `set_budget_level` (§3.5), `construct_x_industries`, `downsize_x_industries` (§6.5), the borrow and repay windows. A control never writes a simulation variable directly.
6. **The AI never runs UI code.** Every scripted GUI has `ai_enabled = { always = no }`, and refresh effects run only for players. The AI uses the same budget levels as players, through its own effect (`ai_budget`).
7. **The script rules still apply.** The getters are triggers, so no math expressions in them or in `visible` and `*_enabled` triggers. Guard every divide. Stage `arr^i` into a temp before using it.
8. **No dropdowns.** Lists sort by clicking a column's header, filters are rows of buttons, and graphs switch metric by clicking the figure or a button (Strat, 2026-11-13).

## 3. The frame (U0)

### 3.1 Size and grid
- `economy_window_container` is 772 wide and runs the height of the screen from y = 138, sliding in from the left, as now. Content uses two 386-wide columns or one 772-wide block. The States tab is the exception: a 256-wide state list and a 516-wide state panel.
- Top to bottom: the tab bar (40 px, as now), a subtab bar on tabs that have subtabs (30 px), the content, and a footer (44 px). At 1080p that leaves about 858 px for content without subtabs and 828 px with them. Every tab must fit there at 1080p; long lists scroll inside their own block, never the whole tab.
- **No title banner.** The mockups' banners cost about 100 px the window doesn't have. The tab bar is the header.
- **Footer**, on every tab: GDP, GDP growth (year on year), treasury and net budget, each with a tooltip.
- **Side panel** `economy_detail_container` (UQ13): 386 wide, the window's height, docked to the window's right edge (x = 766). One panel serves every detail view (sector, state-industry, company), switching on `eco_ui_detail`. It has its own close button and closes with the window.
- **Popups** (borrow, repay, pickers, budget policy) are small centred windows, like the existing borrow and repay windows.

### 3.2 Containers and scripted GUIs
Each child is its own top-level `containerWindowType` in `interface/economy_window.gui`, attached with `parent_window_name`, as `budget_container` is now. The scripted GUIs go at the end of `common/scripted_guis/economy_and_demographics.txt`, beside `economy_window` and `budget_window`.

| Container | Parent | Visible when |
|---|---|---|
| `economy_window_container` | — | the `country_economy_view_open` flag (topbar) |
| `budget_container` | `economy_window_container` | `eco_ui_tab = 1` |
| `macro_container` | `economy_window_container` | `eco_ui_tab = 2` |
| `macro_general_container`, `macro_sectors_container`, `macro_finance_container`, `macro_companies_container` | `macro_container` | `eco_ui_macro_subtab` = 1, 2, 3, 4 |
| `states_container` | `economy_window_container` | `eco_ui_tab = 3` |
| `states_list_container` | `states_container` | always: the list stays while the subtab changes |
| `states_overview_container`, `states_industries_container`, `states_population_container` | `states_container` | `eco_ui_states_subtab` = 1, 2, 3 |
| `global_container` | `economy_window_container` | `eco_ui_tab = 4` |
| `global_overview_container`, `global_industry_container`, `global_finance_container`, `global_companies_container` | `global_container` | `eco_ui_global_subtab` = 1, 2, 3, 4 |
| `economy_detail_container` | none (top level) | the window is open and `eco_ui_detail > 0` |

**Fixes to the current files:**
- The tab buttons sit inside the tab containers (`macro_tab_button` in `macro_container`, `states_tab_button` in `states_container`, and the budget's is commented out), so each one vanishes whenever its own tab is hidden. Move them all into `economy_window_container`.
- Four tabs across 772 px need 193-wide buttons; the current sprite, `GFX_eoanbr_header_tab_button1_258x45`, is sized for three. The subtab bars have up to four buttons too, so a 193 × 30 version serves them.
- `states_container` keeps its name: it was always the States tab (UQ2).
- `budget_window`'s `visible` checks two flags. Switch every tab to `eco_ui_tab`.
- The topbar flag opens the old budget window and the new one together. Give the old one a debug-only flag while U1 is built, and delete it when U1 is done.
- The revenue rows are written out by hand, ten buttons each. Replace them with the list row of §3.5.

### 3.3 UI state
Variables on the player's country (`ROOT` in `player_context`). Variables rather than flags, so two tabs can't be open at once. Each tab remembers its own subtab.

| Variable | Holds |
|---|---|
| `eco_ui_tab` | 1 Budget, 2 Macro, 3 States, 4 Global |
| `eco_ui_macro_subtab` | 1 General, 2 Sectors, 3 Financial System, 4 Companies |
| `eco_ui_states_subtab` | 1 Overview, 2 Industries, 3 Population |
| `eco_ui_global_subtab` | 1 Overview, 2 Industry, 3 Finance, 4 Companies |
| `eco_ui_detail` | 0 closed, 1 sector, 2 state-industry, 3 company |
| `eco_ui_sector` | the selected sector's token |
| `eco_ui_state` | the selected state; the capital when the tab first opens |
| `eco_ui_industry` | the selected industry's token in `eco_ui_state` |
| `eco_ui_company` | the selected company's id (M10) |
| `eco_ui_<list>_sort`, `eco_ui_<list>_sort_asc` | each list's sort column and direction (§3.5) |
| `eco_ui_<list>_filter` | each list's filter |
| `eco_ui_budget_collapsed@token:<group>` | an expenditure group folded to its heading |
| `eco_ui_graph_metric` | the Macro indicators graph's metric |

### 3.4 Where each figure comes from
Every table below marks its source:
- **Stored:** a variable the monthly tick sets. Read it directly.
- **Loc:** worked out in scripted localisation from stored values, one entry at a time: a ratio, a short sum, or a loop over one sector's methods. Never a loop over states.
- **Refresh:** built by a UI refresh effect. That covers every list, every sort, and any total that loops over states or countries.
- **New:** a value the tick doesn't store yet, which the phase adds.
- **Mxx:** arrives with that milestone. Greyed until then.
- **Later:** planned, but in no milestone yet (§8.1). Greyed until then.

**Refresh effects** live in a new file, `common/scripted_effects/_economy_ui.txt` (UQ15). The entry point, `eco_ui_refresh`, dispatches on the tab and subtab to `eco_ui_refresh_budget`, `_general`, `_sectors`, `_states`, `_state`, `_global` and `_companies`. Refresh effects:
- run when the window opens, when the tab or subtab changes, when an entry is selected, when a sort or filter changes, and once a month for each player whose window is open (one call at the end of `_country_advance_time`, behind `is_ai = no` and the open flag);
- write only `eco_ui_*` variables and arrays on the player's country, so they can't change the simulation;
- stay cheap. The biggest, the Global refresh, visits each country's sectors once.

### 3.5 Components

**List row.** Every list is a dynamic list over an `eco_ui_*` array, with one entry container per list. The entry's value is `v`, as in the state screen's `building_container`: localisation reads `[?sector_revenue@var:v]`, and triggers set `industry_token = v` before calling a getter. Click effects receive `v` too, so one container serves every row.

**Sortable columns.** Each sortable column's header is a button. Clicking it sorts the list by that column, largest first; clicking the sorted column again reverses it. The sorted column's header shows ▼ or ▲. The click sets `eco_ui_<list>_sort` (the column's number in that list's table) and `eco_ui_<list>_sort_asc`, then calls the list's refresh. `eco_ui_sort` sorts `eco_ui_sort_in` into `eco_ui_sort_out` by selection sort, with the key worked out per entry by the caller's branch for that column. About 30 sectors or 60 states makes under 4,000 comparisons, run on a click.

**Filter buttons.** A row of toggle buttons, "All" first, the active one lit. Clicking one sets `eco_ui_<list>_filter` and refreshes the list.

**Budget levels.** The percentage sliders are scrapped (UQ4). Every adjustable line, in the budget and elsewhere (minting, tariffs, grants, subsidies), works the same way:
- **Level:** `budget_level@token:<line>`, 0–4 (very low to very high). M (2) by default.
- **Band:** laws set each line's base min and max through modifiers, as `budget_clamp` works out `<line>_min` and `<line>_max` now. The modifier names are per line, so the band code stays one block per line.
- **Spread:** five weights per line, `global.budget_level_weight@token:<line>^0` to `^4`, give each level's place in the band. They needn't be even: 0, 0.15, 0.35, 0.6, 1 is as valid as 0, 0.25, 0.5, 0.75, 1.
- **Value:** `budget_value@token:<line>` = min + weight × (max − min), set in `budget_update` each month and on a click. It replaces the line's `*_percentage` wherever that is read, including the `budgetary_spending` dynamic modifier.
- **What the value means** depends on the line: a tax rate (taxes, tariffs); a share of the line's full cost (maintenance, procurement, research, construction, as the percentage is now); or a **funding factor** on the line's base cost (personnel, administration, the public services). A funding line's base cost is what pops, GDP and manpower set, as now. Its band, for example 80–130%, lets the player fund it beyond the law's floor and fine-tune the spend (correction 2, UQ18).
- Every level is always available. A law that moves the band moves the value with it; the level stays.
- **Players** click a level, which calls `set_budget_level` with `budget_line_temp` and `budget_level_temp`. **The AI** sets levels through `ai_budget`, rewritten to step a line one level at a time, until budget policy (§4.5) replaces it.
- **Buttons:** current (`GFX_budget_<level>_button_large`), available (`GFX_budget_inactive_button_large`), and greyed while the line's mechanic isn't built (`GFX_budget_empty_button`, with a large version made if the size differs).
- **Tooltips:** each button gives the level's value, the line's amount at that value (estimated from this month's base), and the line's effects at that level.
- **Read-only rows** use the same row with the buttons hidden: `global.budget_line_adjustable@token:<line> = 0`.
- **Pickers.** Some lines also choose what they apply to (the budget prompts' notes): sales tax chooses the goods it's charged on, industrial subsidies the sectors it subsidises (UQ20), and the development fund the sectors it favours. A small button at the row's end opens a picker popup with a checkbox per good or sector. Each picker is greyed until its milestone.
- **Deleted with the sliders** (Q4): the `change_*` effects, `*_percentage`, `*_percentage_actual`, `*_slider_pos`, and the slider GUI. `ai_budget` (in `_economy_main.txt`) is the only script that calls `change_*` outside the old window.

**Line graph.** Reuse the TNO-style renderer behind `econ_rerender_country_gdp_graph` and `econ_rerender_country_budget_graph`, which turns a history array into line-segment frames in a dynamic list. Make it one effect, `eco_ui_render_graph`: it reads `eco_ui_graph_in` and writes the min, the max and the frames into `eco_ui_graph_out`. Each graph copies the result into its own frames array, since a dynamic list binds one array name. The graphs: Budget debt-to-GDP and net budget, the Macro indicators, the selected state's GDP, and world GDP.

**History arrays.** Kept for every country, so a tag switch still has history, and appended in the statistics block of `_country_advance_time`.
- Existing: `gdp_amount_quarterly` (41 quarters, seeded at startup), `net_budget_array` (33 months), and each state's `gdp_amount_array` (38 months).
- New, quarterly, appended with `gdp_amount_quarterly` and seeded flat at startup: `gdp_per_capita_quarterly`, `unemployment_quarterly`, `inequality_quarterly`, and `inflation_quarterly` with M12.
- New, monthly: `debt_to_gdp_array` (33 months, like `net_budget_array`), and `global.world_gdp_history` (one value a month, written by the tick host).
- New, yearly: `global.world_category_output_last_year@<category>`, for the world industry's growth (§7).

**Pie chart.** Reuse the 100-slice pie of `create_pie_chart_revenue`, with slot colours from `GetValueToBudgetPieSegment`. It has seven colours, enough for the six sector categories. Each legend icon takes its slice's colour, so the pie needs no labels (the idea from the budget prompts). The segment sprite is 1024 px, so each pie sets its own `scale`.

**Money format.** One scripted localisation, `GetEcoMoney`, reading `money_temp`: £K under £1M, £M with two decimals up to £1,000M, £B above. Negative amounts show in red. Build it on the existing currency helpers (`GetCurrencyTextIcon` and the rest), so other currencies can plug in after M12.

**Greyed block.** A block, row or control for an unbuilt system shows its frame, title and buttons, greyed, with figures reading "–" and the tooltip "Arrives with <system> (Mxx)" or "Not built yet".

### 3.6 Style
Reuse what `economy_window.gui` already uses:
- Backgrounds: `GFX_eoanbr_tiled_plain_bg2` for the window, `GFX_tiled_bg_gold_trim_3_green` and `_red` for revenue and expenditure, `GFX_tiled_bg_gold_trim_3` for neutral blocks.
- Headers and rows: `GFX_tiled_header_gold_trim_1` for column headers, `GFX_tiled_header_gold_line_horizontal` for rows, 30–36 px tall.
- Fonts: `vic_36` or `vic_18` for block titles, `hoi_24header` for headline numbers, `hoi_18mbs` for values, `hoi_16mbs` for labels.

### 3.7 U0: build and done when
**Build:** the containers and parents above; the tab and subtab bars; the footer; the side panel shell; the UI state variables; `_economy_ui.txt` with `eco_ui_refresh`, the sort and the graph renderer; `GetEcoMoney`; the list row, sortable header and filter button containers.

**Done when:** every tab and subtab opens and closes without another showing; each tab comes back on the subtab it was left on; the side panel opens and closes; the footer shows live values; `error.log` has nothing new from the GUI files.

## 4. Budget tab (U1)

```
┌──────────────── REVENUE ─── 386 ─────┬────────────── EXPENDITURE ─── 386 ───┐
│  REVENUE                  ┌───────┐  │  EXPENDITURE              ┌───────┐  │
│                           │       │  │                           │       │  │
│  £92.45M                  │  pie  │  │  £88.73M                  │  pie  │  │
│  a month                  │ 110px │  │  a month                  │ 110px │  │
│                           └───────┘  │                           └───────┘  │
│ Source       VL  L  M  H  VH  Amount │ Line         VL  L  M  H  VH  Amount │
│ Personal tax [] [] [] [] []  £18.75M │ ▼ MILITARY                   £25.60M │
│ Asset tax    (greyed)              – │   Operations   (greyed)            – │
│ ...                       (scrolls)  │   ...                     (scrolls)  │
├──────────────── DEBT ────────────────┼──────────── NET BUDGET ──────────────┤
│ Debt-to-GDP graph  │ Total debt      │ £3.72M surplus  │  2.3% of GDP       │
│ (33 months)        │ Credit rating   │ Net budget graph (33 months)         │
│                    │ Interest rate   │                                      │
│                    │ Interest a month│                                      │
│ [Borrow] [Repay] [Declare bankruptcy]│ [Budget policy]   (M13)              │
├──────────────────────────────────────┴──────────────────────────────────────┤
│ GDP £158.76M · growth +2.4% · treasury £x · net budget +£3.72M              │
└──────────────────────────────────────────────────────────────────────────────┘
```

**The section headers** (correction 1): each is 366 × 120. The title (`vic_36`) sits above the total (`hoi_24header`) in the left 236 px, so a total as long as "£1,234.56M" fits. The pie takes the right 120 px, drawn at 110 px (`scale` 0.107). The row icons carry the pie's colours as its legend.

**Height at 1080p:** 858 px of content. The debt and net budget panels take 250, leaving 608 for each section: 120 header, 26 column header, and 462 for rows, about 14 at 32 px. Revenue's 8 rows fit. Expenditure's 27 rows scroll, and each group heading folds its group on a click (`eco_ui_budget_collapsed@`), showing only the group total.

**Rows.** Revenue and expenditure are each one dynamic list (§3.5). Expenditure's group headings are rows too: the entry container holds a heading layout and a line layout, switched by `global.budget_line_is_heading@var:v`. `eco_ui_refresh_budget` builds the row arrays (`eco_ui_revenue_rows`, `eco_ui_expenditure_rows`) from the global line lists, skipping the lines of folded groups. Every line is listed from U1, built or not; an unbuilt line is greyed (UQ8, UQ14).

### 4.1 Revenue

| Row | Control | Binds to | Amount shown | Status |
|---|---|---|---|---|
| Personal tax | 5 levels (UQ5: one row) | One level sets all three income tax brackets, upper, middle and lower, each from its own band and weights (`income_tax_*_strata_min` and `_max`) | `income_tax_revenue`; the tooltip gives each bracket's rate and revenue (`income_tax_*_strata_revenue`) and corruption | Exists |
| Asset tax | 5 levels | the asset taxation law (politics rework) | — | M13 |
| Corporate tax | 5 levels | the corporate tax rate, charged on the sectors' positive profit (Q86) | `corporate_tax_revenue` | Exists |
| Sales tax | 5 levels, and a goods picker | the sales tax rate; the picker chooses the goods it's charged on | `sales_tax_revenue` | Exists; the picker M13 |
| Tariffs | read-only | import and export duties, set on the trade screen by the market leader (UQ6, UQ19) | `import_tariffs` + `export_tariffs`, split in the tooltip | Exists |
| State enterprises | read-only | — | `public_enterprise_revenue`, the government buildings' revenue. After M08 removes those buildings, it becomes dividends on state-owned capacity (Q37, M10) | Exists; changes at M08 and M10 |
| Seigniorage | read-only; minting is set on Financial System (UQ7) | — | the minted amount ÷ P (Q49) | M11 |
| Other | read-only | — | `other_revenue` less `public_enterprise_revenue`: modifiers (`modifier_revenue`), trade (`trade_revenue`) and, once something records it, income from other countries (the mockup's Diplomacy, UQ8), split in the tooltip | Exists |

The header shows `revenue` and the pie (`create_pie_chart_revenue`, with its slots remapped to these rows).

### 4.2 Expenditure

| Group and row | Control | Binds to | Amount shown | Status |
|---|---|---|---|---|
| **Military** | | | | |
| Operations | 5 levels | — | — | Later |
| Procurement | 5 levels | the share of the army's goods bought | `military_production_resources_spending` | Exists |
| Maintenance and repair | 5 levels | unit upkeep, which buys organisation and morale | `military_spending` | Exists |
| Personnel | 5 levels, funding | a funding factor on the pay of fielded manpower | `military_payroll_spending` | The cost exists; the funding effect M13 (UQ18) |
| Arsenals and dockyards | read-only | — | `military_production_payroll_spending`. Factory contracts replace it in M08 | Exists until M08 |
| Factory contracts | read-only; the split is set on Sectors (UQ9) | — | the Manufacturing Base's contract cost (Q64) | M08 |
| **Government** | | | | |
| Patronage | 5 levels | — | — | Later |
| Intelligence | 5 levels | `intelligence_spending_percentage` exists, with no cost or effect, and its buttons are disabled today | — | M13 |
| Administration | 5 levels, funding | a funding factor on the bureaucrats' pay and the per-head and per-GDP costs (Q77) | `administration_spending` | The cost exists; the funding effect M13 (UQ18) |
| Construction | 5 levels | the share of state-paid builds, retools and prospecting funded | `construction_spending` (including projects) | Exists |
| **Public services** | | | | |
| Law and order | 5 levels, funding | a funding factor on its per-head and per-GDP cost | `order_and_intel_spending` | The cost exists; the funding effect M13 (UQ18) |
| Education | 5 levels, funding | as above | `education_spending` | as above |
| Healthcare | 5 levels, funding | as above | `healthcare_spending` | as above |
| Welfare | 5 levels | spec §21.11 | — | M13 |
| Public works | 5 levels, funding | a funding factor on its own per-head and per-GDP cost (UQ26); extra funding speeds construction (UQ18) | — | M13 |
| **Subsidies** | | | | |
| Research | 5 levels | the research share | `research_spending` | Exists |
| Infrastructure | 5 levels | government investment in railways and ports | — | M09 |
| Industrial | 5 levels, and a sector picker (UQ20) | the subsidy rate; the picker chooses the sectors subsidised. There are no sector taxes (UQ20) | the sum of sector subsidies | M13 (Q51) |
| Development fund | 5 levels, and a sector picker | the government's inflow to the general investment pool | — | M09 (Q51's government investment) |
| Trade subsidies | read-only | set with the tariffs on the trade screen | `trade_subsidy` | Exists |
| **Debt** | | | | |
| Interest | read-only | — | `national_debt_interest` (0 while `global.eco_debt_enabled = 0`) | Exists |
| **Other** | read-only | — | `other_spending`: government-building payroll, modifiers and trade, split in the tooltip | Exists |

**What extra funding buys** (UQ18). Each effect scales with the funding factor, within the band the law sets. M13 adds them, though any can come sooner, since each stands alone:
- Personnel: army morale and recruitable manpower.
- Administration: administrative capacity, and so tax collection.
- Law and order: stability and resistance suppression.
- Education: the qualifications stock's growth.
- Healthcare: population growth.
- Public works: construction speed, of HOI4 buildings (`production_speed_buildings_factor`) and of industries (`industry_construction_speed_factor`).

Until a line's effect exists, its buttons are greyed at M, so a click never costs money for nothing.

The header shows `spending` and the pie (`create_pie_chart_spending`, remapped to these groups).

### 4.3 Debt panel

| Element | Source | Status |
|---|---|---|
| Debt-to-GDP graph | `debt_to_gdp_array`, from `debt_to_gdp_ratio` | New |
| Total debt | `debt_to_national_bank_k` + `debt_to_foreign_countries_k`; the tooltip lists foreign debt by creditor (`debt_to_bank_k@<tag>` over `debt_to_bank_country`) | Stored |
| Credit rating | the borrower premium of Q72 | M11 |
| Interest rates | `domestic_interest_rate`, `foreign_interest_rate` | Stored |
| Interest a month | `national_debt_interest` | Stored |
| Debt level | `debt_level` against the bankruptcy threshold (above 49.9, about 200% of a year's GDP) | Stored |
| Borrow, Repay | open the existing `country_borrow_money_window` and `country_repay_debt_window` | Exists |
| Declare bankruptcy | a voluntary default (spec §21.12) | M13 |

While debt is switched off, a one-line note says so, and the interest figures read 0.

### 4.4 Net budget panel

| Element | Source | Status |
|---|---|---|
| Net budget | `net_budget`, labelled surplus or deficit | Stored |
| Share of GDP | `net_budget` ÷ `gdp_amount` | Loc |
| Net budget graph | `net_budget_array` | Stored |
| Budget policy | a button that opens the budget policy popup (§4.5) | After M13 |

### 4.5 Budget policy (after M13, UQ10)
From the budget prompts: four doctrines, each a short list of options, plus an automation toggle.
- The doctrines are **fiscal management** (deficits and surpluses), **economic development** (growing the economy), **sociopolitical policy** (social spending) and **military readiness**.
- With automation on, the doctrines set every line's level. Each line has a score; a threshold moves it up a level, and stickiness holds it there (for example, rise to High at +60, fall back to Medium only below +45).
- Development, social and military set the base scores. Fiscal management acts last: under austerity it steps every spending line down and every tax up, one level at a time, until the budget meets its target, so whatever the other doctrines value most is cut last.
- Each option can carry its own modifiers, so the panel isn't wasted space for players who set the budget by hand.
- The AI uses the same system, which replaces `ai_budget`. The funding lines are what give it room to be particular (correction 2).

U1 leaves room for the button, greyed. A starting list of options, for Strat to cut and give modifiers when it's built:
- **Fiscal management:** austerity, balanced budget, steady deficit, expansionary, debt reduction.
- **Economic development:** laissez-faire, infrastructure first, industrial promotion, developmental state.
- **Sociopolitical policy:** night-watchman state, order first, paternalist, welfare state.
- **Military readiness:** demobilised, peacetime, armed peace, rearmament, total war.

### 4.6 U1: build and done when
U1 changes a mechanic as well as the window: the levels replace the sliders (UQ17). Run a simulator A/B as for a milestone.

**Build:**
- The level system of §3.5 in `_economy_budget.txt`: `budget_level@`, the bands (today's `budget_clamp`, renamed `budget_bands_update`), the weights, `budget_value@`, `set_budget_level`. Every reader of a `*_percentage` reads `budget_value@` instead.
- `ai_budget` stepping levels.
- The line tokens in `eoanbr_tokens.txt` (outside the generated blocks); the line lists, line flags and weights in `_economy_setup.txt` with the other budget globals; `debt_to_gdp_array`.
- The tariff and trade subsidy controls on the trade screen (UQ19), as level lines with signed bands whose lowest levels are subsidies, as the sliders can go negative today. Only the market leader can click them. Members copy the leader's levels each month, when `market_prices_monthly` copies prices, and each country still collects duties on its own trade. They move in U1 because U1 deletes the window that holds them. Per-good tariffs (spec §21.4) come later, on the market screen.
- The Budget tab itself; delete the old budget window.

**Done when:**
- Every row marked Exists reads the same value as the old window did.
- At level M, each line's value is today's default rate, so the 60-month A/B run against the pre-U1 baseline differs only where `ai_budget` steps differently.
- A law modifier that moves a band moves the line's value.
- The tariffs work from the trade screen, for the market leader only.
- Every unbuilt line shows, greyed.

### 4.7 Changes from the mockup
- **Minting** moves to Financial System, where its effect on base money is shown beside it (UQ7). Seigniorage stays as a read-only revenue row.
- **Tariffs** stay a read-only revenue row; their controls move to the trade screen, set by the market leader (UQ6).
- **Diplomacy** joins Other (UQ8).
- **Rows the mockup lacks,** because the code has them: Arsenals and dockyards (until M08), Factory contracts (M08), Trade subsidies, and Other spending.
- **The revenue pie** moves from its own block into the section header, beside the title and total, and the expenditure section gets one too.
- "Bureaucracy" is labelled Administration, as in the code.

## 5. Macro tab

### 5.1 General (U4)
Revisited in depth (correction 4). General answers "how is the economy doing, and why": the cycle, the headline indicators, where GDP comes from and goes, who earns it, and what's going wrong. Industry and investment detail moved to Sectors, so investment opportunities and the construction list live there now (UQ25).

```
┌──────────────────── 386 ─────────────┬──────────────────── 386 ────────────────┐
│ ECONOMIC CYCLE              (greyed) │ WHERE GDP GOES                          │
│ phase wheel · Steady growth · 14 mo  │ Consumers £x 61% · Investment £x 9%     │
│ one-line description                 │ Government £x 22% · Net exports £x 3%   │
├──────────────────────────────────────┤ ████████████████░░░░░ (stacked bar)     │
│ KEY INDICATORS                       ├─────────────────────────────────────────┤
│ graph (10 years, quarterly) │ GDP    │ WHERE GDP COMES FROM                    │
│                             │ /head  │ Farming 32% · Resource 18% · Factories… │
│                             │ Unemp. │ ████████████████████ (stacked bar)      │
│                             │ Infl.  ├─────────────────────────────────────────┤
│                             │ Gini   │ CLASSES   Pop.  Unemp.  Earn.  Wealth  Debt│
├──────────────────────────────────────┤ Slaves · Peasants · Working · Middle ·  │
│ Consumer conf. · Investor conf. ·    │ Upper                                   │
│ Economic incentives                  ├─────────────────────────────────────────┤
├──────────────────────────────────────┤ INVESTMENT FUND                         │
│ SHORTAGES  Coal · Iron · Steel       │ Inflow £x · Spending £x · Fund £x       │
├──────────────────────────────────────┼─────────────────────────────────────────┤
│ WARNINGS (8, in two columns)         │ CAPACITY  Manufacturing Base · Admin.   │
│ Outlook: one line                    │ capacity · Know-how                     │
└──────────────────────────────────────┴─────────────────────────────────────────┘
```

Left column, about 660 px; right, about 590.

| Block and element | Source | Kind |
|---|---|---|
| **Economic cycle** | | |
| Phase | the mockup's wheel of seven phases (economic boom, fast growth, steady growth, stagnation, recession, depression, free fall), mapped onto the phases `check_economic_cycle` sets; the current phase lit, with a one-line description and months in phase; the phase's modifiers in the tooltip. Greyed while `global.eco_cycle_enabled = 0` | Stored; on with M14 |
| **Key indicators** | | |
| Graph | 10 years, quarterly: `gdp_amount_quarterly`, `gdp_per_capita_quarterly`, `unemployment_quarterly`, `inequality_quarterly`; `inflation_quarterly` with M12. Clicking a headline figure switches the graph to it | Stored, New |
| GDP, GDP per head | `gdp_amount`, `gdp_per_capita`, with the change on a year ago | Stored |
| Unemployment | `pops_unemployed` ÷ `pops_workforce` | Loc |
| Inflation | the price level's change | M12 |
| Inequality | a Gini coefficient over the five classes, from `pops@<class>` and `pops_earnings@<class>`, worked out monthly with the histories (five groups, so cheap) | New |
| **Confidence** | consumer confidence, investor confidence and economic incentives: `modifier@consumer_confidence_modifier`, `modifier@investment_confidence_modifier`, `modifier@incentives_modifier`, each against its base of 100; the tooltip says what each drives | Stored |
| **Shortages** | up to eight goods whose market target price is at least `global.eco_ui_shortage_price` × base, read from the market leader; the tooltip gives the price against base | Refresh |
| **Warnings** | eight, in two columns, lit red when active and dim otherwise. Each is a scripted trigger with its threshold in a global: negative growth (year on year), high deficit (net budget below a share of GDP), high government debt (`debt_level`), high private debt (`pops_debt` ÷ GDP), high unemployment, high inequality; high inflation (M12) and bubble risk (M15) greyed. Credit contraction joins with M11 | Refresh |
| Outlook | one line naming the most serious active warning and its usual cause, or the cycle phase's description when none is active. It replaces the mockup's "Economic insight" | Loc |
| **Where GDP goes** | consumer spending (`pops_needs_spending`), investment (capital formed until M09, `sectors_retained` + `pops_investment`; capital spent from M09), government spending (`spending`), net exports (net trade value `trade_value` until M12; exports less imports from M12, Q48). Each with its share of GDP and a stacked bar. GDP is measured as value added, so the four needn't sum to it; the tooltip says so | Stored, M09, M12 |
| **Where GDP comes from** | value added (`sector_revenue@` − `sector_inputs@`) by category, plus subsistence and the government buildings, as shares of GDP in a stacked bar with a legend. Clicking a category opens Sectors filtered to it | Refresh |
| **Classes** | one row per class: population (`pops@<class>`), unemployment (`pops_unemployed@` ÷ `pops_workforce@`), earnings per head (`pops_earnings@` ÷ `pops@`), wealth (`pops_wealth@`), debt (`pops_debt@`). It explains the Gini and the private debt warning | Stored, Loc |
| **Investment fund** | the mockup's three figures. Inflow: pop investment, retained sector earnings and, from M09, the development fund. Spending and the fund's balance: the M09 pools (Q34). Until M09, inflow shows what's formed and the rest is greyed, since none of it is spent yet | Stored, M09 |
| **Capacity** | the Manufacturing Base (M08); administrative capacity (`administrative_capacity`, which scales tax collection); know-how, in place of the mockup's industrial expertise: Strat wants it modelled, and its design is open (backlog, UQ24) | M08, Stored, Later |

**Done when:** every Stored and Refresh figure matches a save; clicking each headline figure switches the graph; the greyed blocks carry their milestones.

**Changes from the mockup:**
- **Investment opportunities** and **industries under construction** move to Sectors (UQ25).
- **Added:** where GDP goes and where it comes from (the notes' "sectoral composition" and "total investment"), and the classes table (the inequality figure's breakdown).
- The **investment fund** becomes the M09 pools; **attractiveness** becomes the ROI tier on Sectors.
- The **manufacturing index** becomes the Manufacturing Base (M08).
- **Industrial expertise** becomes know-how, greyed until it's designed (UQ24).
- **Resource lack** becomes Shortages, of economy goods.
- **Economic insight** becomes the Outlook line, driven by the warnings.
- The metric **dropdown** becomes clickable headline figures.

### 5.2 Sectors (U2)
The national sector screen that M04 still owes, and the place where industry is decided (UQ1, UQ2). Everything it shows has been stored since Q91, and M04's "National sector UI: what a sector screen can show" section gives every source. It also carries the investment that flows into sectors (correction 4).

```
┌──────────────────────────────────────── 772 ──────────────────────────────────┐
│ Output £x · Operating profit £x · Retained £x · Capital £x · Employed 1.2M    │
│ Under construction 12 · Retooling 3                                           │
│ MANUFACTURING BASE  120 factories · civilian 60% · military 30% · naval 10%  [Set] (M08)│
├───────────────────────────────────────────────────────────────────────────────┤
│ [All] [Farming 32%] [Resource 18%] [Factories 30%] [Urban 15%] [Transport 5%] │
├───────────────────────────────────────────────────────────────────────────────┤
│ Sector ▼          Size  Target  Revenue  Margin  Employed  Capital  Building  │
│ (icon) Textile mill 14.0  95% ▲  £2.31M   18%     42.1K    £0.4M     2.0      │
│ ...                                                              (scrolls)    │
├──────────────────────────────────────┬────────────────────────────────────────┤
│ INVESTMENT OPPORTUNITIES       (M09) │ CONSTRUCTION AND RETOOLING             │
│ Sector  State  Tier  Cost  Pool      │ Industry  State  Progress  Left  Payer │
│ (scrolls)                            │ (scrolls)                              │
└──────────────────────────────────────┴────────────────────────────────────────┘
```

The category filter applies to all three lists. Each filter button shows its category's share of national output, so the button row doubles as the composition chart. If the Manufacturing Base strip makes the tab too crowded, it moves to General (UQ9).

| Element | Source | Kind |
|---|---|---|
| Output, operating profit, capital, employed, under construction, retooling | sums over `sectors` of `sector_revenue@`, `sector_profit@`, `sector_capital@`, `sector_working_employed@` + `sector_middle_employed@`, `sector_construction@` and `sector_retooling@` | Refresh |
| Retained, profit tax, dividends | `sectors_retained`, `sectors_profit_tax`, `sectors_dividends` | Stored |
| Manufacturing Base | the factory count, and the civilian, military and naval split, with a popup to set it (UQ9) | M08 |
| Category filter and shares | `global.building_type@<sector>`: 2 transport, 3 resource, 4 farming, 5 factories, 6 urban; shares from the revenue sums | Stored, Refresh |
| Sector list | `eco_ui_sectors_list`, from the country's `sectors`, filtered and sorted | Refresh |
| Investment opportunities | sector icon, state, ROI tier (Exceptional, Good, Fair, Marginal), cost, and the pool that funds it; sorted by tier | M09 |
| Construction and retooling | every controlled state-industry with `construction@` above 0 or a retool under way: industry, state, progress, months left (`construction_time_left@`, `retooling_time_left@`), cost and payer. Built by looping the player's states, so it costs the AI nothing | Refresh |

**Sector list columns,** each sortable (revenue is the default):

| # | Column | Source | Kind |
|---|---|---|---|
| 1 | Sector | icon and name; sorts by name | Stored |
| 2 | Size | `sector_size@`; the tooltip shows `sector_generic_size@`, the rest being companies' | Stored |
| 3 | Target | `sector_utilisation@`. ▲ when `sector_margin@` is above `global.sector_utilisation_rise_margin`, ▼ when it's below 0, – otherwise | Stored, Loc |
| 4 | Revenue | `sector_revenue@` | Stored |
| 5 | Margin | `sector_margin@` | Stored |
| 6 | Employed | working + middle employed. The tooltip gives jobs per class and the wage-weighted employment % | Stored, Loc |
| 7 | Capital | `sector_capital@` (unspent until M09) | Stored |
| 8 | Building | `sector_construction@`, with `sector_retooling@` in the tooltip | Stored |

**Sector detail** (side panel, `eco_ui_detail = 1`), top to bottom:
1. **Header:** icon, name, category, size (generic and companies'), the leading PM and AM.
2. **Utilisation:** the target, where it's heading and why (the margin against the rise threshold and 0, at most `global.sector_utilisation_step_max` points a month), and the band each state works within (`global.local_utilisation_shift`).
3. **Accounts,** monthly: goods revenue (`sector_revenue@` − `sector_transport_revenue@`) and transport revenue, inputs (`sector_inputs@`), payroll, maintenance, operating profit, margin. Then where profit goes: profit tax (`sector_profit_tax@`), retained earnings (`sector_retained@`) into capital (`sector_capital@`), and dividends (`sector_dividends@`, and per size `sector_dividend_per_size@`).
4. **Investment:** capital and this month's retained earnings; the sector's opportunities (M09) and its constructions and retools, both from the lists above; fund expansion (government investment, M09).
5. **Employment:** jobs and employed per class, employment %, and average pay (`sector_payroll@` ÷ employed; in slave states that's pay per worker, not the wage).
6. **Goods:** goods made, per good: `output@<sector>` × `global.building_base_production_amount@<sector>^i`, with its price, value and share of national output (÷ `local_production@<good>`). Goods used: for each method i with a scale, `sector_pm_scale@^i` × the method's input amounts, costed with `method_input_cost@`. Both are Loc, looping over the sector's own methods (14 at most).
7. **Methods:** a bar for each PM and AM in use (`sector_pm_size@^i` ÷ `sector_size@`), the newest unlocked (`latest_production_method@`, `latest_automation_method@`), and each method's tooltip from `get_pm_values` in country scope.
8. **Biggest states:** `sector_states@<sector>`, five rows of state, size, trailing `margin@` and utilisation (`get_industry_utilisation`). Clicking a row opens that state on States → Industries with this industry selected.
9. **Sector-specific:** RGOs show known and potential deposits (`sector_known_deposits@`, which include the worked deposit, and `sector_potential_deposits@`; the worked deposit is the size). Railways and ports show their capacity and transport revenue (`sector_industrial_capacity@`, `sector_shipping_capacity@`, `sector_transport_revenue@`). Every sector shows its transport demand (`sector_transport_demand@`).
10. **National modifiers:** `industry_throughput_factor@`, `industry_output_factor@`, `industry_input_factor@`.
11. **Controls:** whether the sector is subsidised, the same setting as the budget's picker (M13, UQ20); fund expansion (M09); a target utilisation override (planned economies only, M13).

**Done when:** every sector the country has is listed; filters and column sorts work; the construction list matches the state screens; the detail panel's accounts add up to the sector record; the figures match `read_save.py` on a month-1 save.

### 5.3 Financial System (with M11 and M12)
Greyed until M11. The layout follows `financial_system_window.png`: five full-width blocks.

| Block and element | Source | Status |
|---|---|---|
| **Currency** (one per market, Q45) | | |
| Currency, monetary law | the market's currency; the monetary system law, shown only: laws change through politics, and the economy reads them through modifiers (Q61) | M12 |
| Commodity reserves | gold or silver, by value and weight; reserve adequacy (Q47) | M12 |
| Base money | per market (Q65) | M11 |
| Base money change | this month's change, mostly minting | M11 |
| Money supply | base money + bank money | M12 |
| Money demand | real GDP × a multiplier | M12 |
| Exchange rate | the exchange-rate scalar against its base (spec §18.1) | M12 |
| Inflation | the price level's yearly change | M12 |
| Minting | 5 levels, with the current minting rate. Only the market leader mints; members see "set by <leader>" (Q65, UQ7) | M11 |
| **Central bank** | | |
| Status | from the financial system law: none (the block greyed), independent, interference or nationalised | M11 |
| Policy rate | ± 1 point buttons, where the law allows | M11; the control M13 |
| Lending to banks | the lender of last resort's lending outstanding | M11 |
| Liquidity provided | this year's | M11 |
| **Banking system** (one bank per country, Q42) | | |
| Reserve requirement | ± 1 point buttons | M11; the control M13 |
| Reserves | actual against target (the share of base money × banking confidence, Q44) | M11 |
| Bank capital, capital requirement, capital ratio | spec §15.1 | M11 |
| Loan portfolio | outstanding against capacity (the lower of the reserve and capital limits; the tooltip says which binds), by borrower: sectors, companies, pops (Q59) and foreign governments (Q72) | M11 |
| Non-performing loans | the bad debt ratio | M11 |
| Lending rate | the average | M11 |
| Banking confidence | `modifier@banking_confidence_modifier` | Stored |
| Bank status | solvent, strained, distressed, critical or insolvent, in bands of the capital ratio | M11 |
| **Financial markets** | | |
| Credit availability | available credit for investment and lending | M11 |
| Stock performance | the market index | M15 |
| Speculation and bubble risk | 0–100, with a gauge | M15 |
| Foreign capital flows | net, in and out | M11–M12 |
| Retained earnings into the general pool | the share the financial laws set (§13.2) | M09 |
| Lending and borrowing abroad | our bank's loans to other governments; our debt per creditor (`debt_to_bank_k@<tag>`) | M11; the debt is stored now |
| **Financial warnings** | high inflation, high government debt, bubble risk, high private debt, high unemployment, negative growth, draining reserves, capital below requirement, credit contraction | M11–M12; some Stored now (§5.1) |

**Changes from the mockup (UQ11):**
- **Total savings (deposits)** is cut: pops hold no savings, and deposits are abstracted (Q15, spec §15).
- **Added:** base money and its change from minting, bank capital, and the capital requirement, which the credit limit depends on (spec §15.1).
- The **monetary law dropdown** becomes a label, since laws change through politics.

### 5.4 Companies (with M10)
Greyed until M10, and the parts M15 builds (shares, behaviour, departments, R&D, branches) greyed until M15 (UQ12, UQ23). The layout follows `companies_window.png`, with the company detail in the side panel.

| Element | Source | Status |
|---|---|---|
| **Stock market overview** | total market capitalisation graph, volatility, top gainer and top loser | M15 |
| **Aggregate statistics** | total revenue, profit, investment and employment (M10); debt (M11); R&D (M15) | M10, M11, M15 |
| **General grants** | 5 levels, grants to all companies | M13 |
| **Found new SOE** | a button (Q37, Q41) | M13 |
| **Filters** | ownership type (all, private, public, state-owned); region (domestic, foreign, both) | M10 |
| **Company list** | sortable columns: company (icon and name), type, HQ state, industry, market share (its slice ÷ the sector), profit, margin, price trend (M15), complacency (M15), current project (industry, state, funding progress). Capitalisation is the default sort once shares exist; size until then | M10, M15 |

**Company detail** (side panel, `eco_ui_detail = 3`):

| Part | Elements | Status |
|---|---|---|
| Header | icon, name, type, HQ | M10 |
| Income statement | revenue, expenses, profit, margin; interest from M11 | M10 |
| Current debt | | M11 |
| Capital raised | retained earnings (M10); equity issuance (M15); debt financing (M11); government grants (M13) | mixed |
| Stock valuation and shares | the valuation formula (assets + trajectory + margins + modifiers), stock price, shares outstanding | M15 |
| Ownership breakdown | private investors, the state, creditors, treasury stock | M15 |
| Current project | industry, state, cost, funding progress, ROI tier (M09) | M10 |
| Active constructions and upgrades | with progress | M10 |
| Departments | one industry focus each, with integration bonuses | M15 |
| Research and development | throughput, output, input and construction bonuses, and progress to a tech bonus | M15 |
| Branches (foreign) | country, revenue from it, investment to it, its valuation | M15 |
| Actions | purchase stake, nationalise (M13, Q37); bail out (M10, Q66); direct grants, 5 levels (M13) | M10, M13 |
| AI behaviour state | rapid growth, monopolisation, optimisation, crisis management and the like, with a "change policy" button | M15 |
| Complacency | 0–100%: high means more dividends and less risk-taking and R&D | M15 |
| Bankruptcy risk and status | risk score, trend, status (liquidation, Q66) | M10 |

**Changes from the mockup:**
- **Pagination** becomes a scrolling list; the **sort dropdown** becomes the column headers; the **filter dropdowns** become buttons.
- **Attractiveness** becomes the ROI tier (M09).
- Nothing else is cut. The shares, departments, R&D, branches, behaviour state and complacency are greyed until M15 builds them (UQ23).

## 6. States tab (U3)
From `industries_window.png`, cut down only where the state data no longer holds a figure. The state list sits on the left; the panel to its right shows the selected state through three subtabs, the mockup's own Overview, Industries and Population views (UQ21). At 772 wide, only one view fits beside the list.

```
┌── STATES ─── 256 ──┬─────────────────── STATE: LONDON ─── 516 ───────────────┐
│ [All][Core][Other] │ (subtabs) Overview · Industries · Population            │
│ State ▼  Pop.  GDP │                                                         │
│ 1 London 5.4M £23.6M│  the selected subtab's content                         │
│ 2 Lancashire ...   │                                                         │
│ ...      (scrolls) │                                                         │
└────────────────────┴─────────────────────────────────────────────────────────┘
```

### 6.1 State list

| # | Column | Source | Kind |
|---|---|---|---|
| — | the list | `eco_ui_states_list`: controlled states, filtered to all, core or non-core | Refresh |
| 1 | State | rank and name; sorts by name | Stored |
| 2 | Population | `pops`, with its yearly growth | Stored |
| 3 | GDP | `gdp_amount`, with `gdp_growth`; the default sort | Stored |

The mockup's "Show in map" button is cut: no script effect moves the camera or selects a state.

### 6.2 Overview

| Element | Source | Kind |
|---|---|---|
| Key indicator graph | the state's `gdp_amount_array`. Other metrics need a 38-month array per state each (UQ21) | Stored |
| Population, workforce, available workforce, unemployment | `pops`, `pops_workforce`, `pops_unemployed`, and the ratio | Stored, Loc |
| GDP, GDP per capita, growth | `gdp_amount`, `gdp_per_capita`, `gdp_growth` | Stored |
| Wage | `base_wage`; the tooltip gives each class's multiple | Stored |
| Market integration | — | Later |
| Net migration | migration between states isn't modelled; peasants moving into the working class are in Population | Later |
| GDP by sector (pie) | value added (`revenue@` − `expenses_input@`) summed by category over the state's `industries`, with subsistence on its own | Refresh, on selection |
| Production by category | revenue by category over the state's `industries` | Refresh, on selection |
| Consumption | the pops' demand (`pops_need@<good>` × price), the largest goods and the rest | Refresh, on selection |
| Industrial, resource and food output | the factories, resource and farming categories' revenue, with subsistence in food | Refresh, on selection |
| Arable land, its productivity | `arable_land`; subsistence output per hectare | Stored, Loc |
| Pollution, unionisation | — | Later; unionisation goes with the labour associations law (M13) |

### 6.3 Industries

| Element | Source | Kind |
|---|---|---|
| Infrastructure | railway and port levels; Infrastructure Efficiency (`infrastructure_efficiency`) with `industrial_capacity_use` ÷ `industrial_capacity` as used and available | Stored, Loc |
| Industries in state | `eco_ui_state_industries`, the state's `buildings`, copied on selection (a dynamic list binds an array on its context scope, the player's country) | Refresh |
| Resources in state | the state's `rgos`, as the state screen lists them, with a Prospect button where it offers one | Refresh |
| Land and subsistence | arable land, subsistence output per hectare, and subsistence employment | Stored, Loc |

**Columns** of both lists, each sortable: industry (icon), size (`size@`), employment (`get_industry_utilisation`, drawn as figures as on the state screen), productivity (revenue per worker, Loc through `get_industry_figures`), margin (the trailing `margin@`), PM (`production_method@`), AM (`automation_method@`), status (`construction@`, `retooling_pm@` or `prospecting@`), and the row's actions: ▲ build one more, ▼ downsize one level (§6.5).

The existing industry localisation (`GetIndustryEmploymentIcon`, `GetIndustryPMIcon`, the tooltips) assumes state scope, because the state screen uses `selected_state_context`. In the economy window the scope is the player's country, so each reused helper needs a wrapper that switches to `var:eco_ui_state` first. Temps survive the scope change.

### 6.4 Population
The selected state's people as the economy sees them. Demography proper (cultures beyond their shares, religion) stays with the game's own screens.

| Element | Source | Kind |
|---|---|---|
| Classes | one row per class: workforce (`pops_workforce@<class>`), employed and unemployed, earnings, wealth (`pops_wealth@`), debt (`pops_debt@`) | Stored |
| Soldiers | `active_manpower`, outside the classes | Stored |
| Slaves | the slaves' workforce (`pops_workforce@token:slaves`), and whether the controller bans slavery (`slavery_banned`) | Stored |
| Qualifications | the stock, and what moving into each class needs | Stored |
| Bureaucrats | the state's bureaucratic jobs (`bureaucratic_jobs`, `bureaucratic_jobs_upper`) and their pay | Stored |
| Cultures | each culture's share (`percentage@<culture>` over `pops_culture_array`), and the accepted, non-accepted and marginalised shares (`pops_culture_shares_calc`) | Stored, Refresh |
| Class moves this month | from `pops_balance` and the peasant job migration | New |

### 6.5 State-industry detail
Side panel, `eco_ui_detail = 2`: today's `building_tt` and `building_productivity_tt` tooltips laid out as a panel, through the M04 getters (`get_industry_figures`, `get_industry_input`, `get_industry_utilisation`) and `GetIndustryOutputAmount0`–`2`.
1. **Header:** icon, name, state, size.
2. **Inputs and outputs:** each good's amount, price and value, and the totals.
3. **Operating expenses:** payroll, maintenance, inputs.
4. **Financial summary:** revenue, expenses, profit, margin; the trailing margin against the national margin, and the utilisation that gives; dividends paid.
5. **Ownership:** a pie of the generic owner (`owner_sizes_local@`) and each company's holding (M10).
6. **Expansion potential:** the opportunity's ROI tier, if one exists here (M09).
7. **PM and AM,** with any retool under way (cost, time left), and construction under way.
8. **Actions** (UQ16): all of them player decisions, separate from the automatic systems.

| Action | What it does | Status |
|---|---|---|
| Expand | `construct_x_industries`, paid by the government; a grant to the generic owner (Q37) | Exists |
| Cancel construction | as the state screen's minus button | Exists |
| Downsize | removes one level of size, through a new wrapper, `downsize_x_industries`. Separate from capacity decay, which stays automatic (Q23, UQ16). The mechanic is a backlog item (UQ22) | New: the backlog, before U3 |
| Retool | the PM and AM lists; the state screen's `pm_list` belongs to the state window, so the economy window gets its own copy reading `eco_ui_state` | Exists |
| Prospect | RGOs and unexploited deposits | Exists |
| Acquire or nationalise, privatise | ownership actions (spec §21.18) | M13, with M10's ownership |
| Direct grants | 5 levels, a grant to this industry's owners | M13 |

**Done when:** the state list and Overview match the state screen; the Industries lists match the state's industries; the detail panel matches the industry tooltips; each action works from the economy window as it does on the state screen, and Downsize lowers the size by one.

### 6.6 Changes from the mockup
- **The three views** become subtabs, since only one fits beside the list at 772 wide (UQ21).
- **Show in map** is cut: no script effect moves the camera or selects a state.
- **Cash reserves** are cut (Q21).
- **Import and export balance** are cut: trade is national, and states keep no per-good figures (Q89). Production and consumption by category stay, worked out on selection.
- **Projected ROI and the attractiveness stars** become the opportunity's ROI tier (M09, spec §13.4).
- **Downsize** is a new player action (UQ16, UQ22). The old scrap-based downsizing stays deleted.

## 7. Global tab (U5)
Four subtabs, since the mockup's four sections don't fit one screen at 772 wide (UQ21). The mockup's categories (agriculture, extraction, manufacturing, services, government) become the code's: farming, resource, factories, urban, transport, government, and subsistence.

**Overview**

| Element | Source | Kind |
|---|---|---|
| World GDP, growth, GDP per capita, unemployment | sums over countries of `gdp_amount`, `pops`, `pops_unemployed` and `pops_workforce`; growth from `global.world_gdp_history` | Refresh, New |
| Global inflation | | M12 |
| Global investment | | M09 |
| Global trade volume | from each market's import and export values | M12 |
| World market capitalisation | | M15 |
| Global trend graph | world GDP (`global.world_gdp_history`); the other figures as they get world histories. Clicking a figure switches the graph | New |
| Global economic cycle | a donut of countries per phase, countries in recession, greyed while the cycle is off (M14); the share of world GDP contracting (countries with negative growth), live now | Refresh |
| Markets | one row per market leader: members, market GDP (`market_gdp`), share of world GDP; currency and price level with M12 | Refresh |

**Industry**

| Element | Source | Kind |
|---|---|---|
| Category table | sortable columns: output (revenue), share of world GDP (value added ÷ world GDP), yearly growth (against `global.world_category_output_last_year@`), employment, productivity (output per worker), investment (M09), capacity utilisation (size-weighted target utilisation), and the player's share of world output | Refresh, New, M09 |
| Industrial trends | fastest-growing, largest, highest investment (M09), highest productivity, most overcapacity (lowest utilisation) | Loc, from the table |

**Finance** (M11–M12)

| Element | Status |
|---|---|
| Global financial conditions: credit availability, average policy rate, banking confidence, market volatility (M15), bubble risk (M15), total private debt (Stored now), cross-border lending | M11–M12, M15 |
| Major currencies: currency, issuer, value against base, share of world GDP using it, monetary law, inflation | M12 |
| International banks: bank, home country, foreign lending capacity, foreign loans, confidence, risk status | M11 |

**Companies** (M10)

| Element | Status |
|---|---|
| Global company summary: revenue, profit, investment, employment, number of companies (M10); debt (M11); R&D and market capitalisation (M15) | M10, M11, M15 |
| Largest global companies: company, country, industry, ownership, market cap (M15; size until then), profit, global market share, trend | M10, M15 |
| Global corporate structure: a donut of private, public, state-owned and foreign-owned; the top 10's share; the most concentrated industry; bankruptcy risk | M10 |

**Done when:** the world sums match the sum of the countries in a save; the markets table lists every market leader; the category table's totals match the sum of the countries' sectors.

**Changes from the mockup:** the sections become subtabs; the categories are the code's; the markets table is added. Nothing is cut.

## 8. Build order

| Phase | What | Depends on | Notes |
|---|---|---|---|
| U0 | The frame and components (§3) | — | |
| U1 | The Budget tab, the level system and the tariffs on the trade screen (§4) | U0 | Changes a mechanic: A/B in the simulator. Deletes the old budget window |
| U2 | Macro → Sectors and the sector detail (§5.2) | U0 | Finishes M04's UI |
| U3 | States and the state-industry detail, with Downsize (§6) | U2; the backlog's downsizing | |
| U4 | Macro → General (§5.1) | U2 | Deletes `population_economy_window` |
| U5 | Global, Overview and Industry (§7) | U2 | |
| With M08 | The Manufacturing Base strip and popup (Sectors), the factory contracts line, the Capacity figure | M08 | |
| With M09 | The infrastructure and development fund lines; the investment fund; opportunities on Sectors; fund expansion; tiers in the details; global investment | M09 | |
| With M10 | Macro → Companies and the company detail; owners in the state-industry detail; Global → Companies | M10 | |
| With M11 | Financial System's base money, central bank and banking; minting and seigniorage; the credit rating; Global → Finance's banks | M11 | |
| With M12 | The currency block; inflation everywhere; the trade balance; currencies in Global | M12 | |
| With M13 | Asset tax, welfare and intelligence; the funding effects and public works' cost (UQ18, UQ26); the sales tax and subsidy pickers; the sector subsidy toggle; the target utilisation override; ownership actions and direct grants; the bankruptcy button; then budget policy | M13 | |
| With M15 | Stock performance and bubble risk (Financial System); the shares, valuation, ownership, departments, R&D, branches, behaviour state and complacency (Companies); market capitalisation and volatility (Global) | M15 | M15 runs before M14 |
| With M14 | The economic cycle blocks come on | M14 | |

When a milestone from M08 on is next opened, add a UI step to its file that points here.

**Testing.** The simulator doesn't draw the GUI. Run `ecosim_cli.exe check --parse-only` for the script files (effects, scripted GUIs, localisation). The `.gui` and `.gfx` files need an in-game load, then a look at `error.log`. Check figures against `read_save.py` on a save made on the current code. U1 and U3 change mechanics, so they also need a 60-month simulator run compared against a baseline.

### 8.1 Planned, in no milestone yet
These stay greyed, marked "Not built yet", until a milestone takes them on (UQ24):
- **Budget lines:** Operations and Patronage.
- **Figures with no system behind them:** know-how (Strat wants it modelled; its design is open, see the backlog), market integration, net migration between states, and pollution (the backlog's SoL item, Q17).

The companies work after M10 has its own milestone now, M15 (UQ23).

## 9. Questions

### Decided 2026-11-13

**UQ1. Tabs.** **Decided:** four tabs by scope: Budget (country finances), Macro (country economy: General, Sectors, Financial System, Companies), States, Global. Subtabs are sections within a scope.

**UQ2. Sectors before states.** **Decided:** the old Industries tab was the States tab repurposed; States is its own tab, and Sectors goes under Macro.

**UQ3. Monthly or yearly figures.** **Decided:** monthly, as the game shows them now.

**UQ4. Levels and percentages.** **Decided:** the slider and percentage system is scrapped. Laws set each line's base min and max, and the five levels are adjusted positions within that band, not necessarily 0/25/50/75/100. See §3.5.

**UQ5. Personal tax.** **Decided:** one row.

**UQ6. Tariffs.** **Decided:** the controls move to the trade screen, set only by the market leader. The budget shows tariff revenue read-only.

**UQ7. Minting.** **Decided:** on Financial System only, beside what it does to base money, so players see the consequence.

**UQ8. Budget lines with no mechanic yet.** **Decided:** all stay in the UI, greyed, doing nothing until Strat adds their mechanics. Diplomacy merges into Other.

**UQ9. Manufacturing Base allocation.** **Decided:** on Sectors, or on General if Sectors gets too crowded.

**UQ10. Budget policy.** **Decided:** build it later (§4.5).

**UQ11. Financial System.** **Decided:** stock performance and bubble risk stay, greyed. Add base money, base money change from minting, bank capital and the capital requirement.

**UQ12. Companies.** **Decided:** keep the stock market, complacency and the behaviour state in the layout, greyed. Finishing companies is M15 (UQ23).

**UQ13. Side panel.** **Decided:** a detail panel to the right of the main window, 386 wide.

**UQ14. Unbuilt systems.** **Decided:** greyed, for subtabs, blocks and any UI tied to an unbuilt mechanic.

**UQ15. New file.** **Decided:** `common/scripted_effects/_economy_ui.txt` for the refresh, sort and graph effects.

**UQ16. State-industry actions.** **Decided:** expand, downsize, acquire or nationalise, privatise and direct grants are player actions, and stay. Capacity decay is automatic; a player can still downsize an industry separately.

**Corrections, 2026-11-13:**
- The budget sections keep the title above the total, with the pie to the right, and room for both (§4).
- Personnel, administration and the public services keep five levels, to fund them beyond the law's minimum and fine-tune the spend. It also gives the budget AI something to decide (§4.2).
- Lists sort by clicking column headers, not with a dropdown. Category filters stay (§3.5).
- Some investment information belongs on Sectors, and General needed a deeper pass (§5.1, §5.2).

### Decided 2026-11-14

**UQ17. When the levels replace the sliders.** **Decided:** (a). U1 builds the level system (§3.5) on today's law modifiers, and M13 adds effects and new lines on top.

**UQ18. What extra funding buys.** **Decided:** as recommended, except that public works buys construction speed, of HOI4 buildings and of industries, instead of project speed. The list is in §4.2, and M13 builds it.

**UQ19. Tariffs from the market leader.** **Decided:** as recommended. Level lines with signed bands on the trade screen, clicked only by the market leader and copied to members monthly; each country collects its own duties (§4.6).

**UQ20. Industrial subsidies.** **Decided:** subsidies only. The picker marks a sector subsidised or not, and sector taxation is left out. This narrows Q51's "sector subsidies and taxes" for M13.

**UQ21. Subtabs for States and Global.** **Decided:** yes. The state's key indicator stays GDP only.

**UQ22. How a player downsizes.** **Decided:** as recommended: one level of size per click, at once, with no refund; the workers lose their jobs that month; blocked while construction is under way; not used by the AI; content calls `downsize_x_industries`. Strat counts it as an economy question more than a UI one, so the mechanic is a backlog item, built before U3.

**UQ23. The companies work after M10.** **Decided:** a milestone of its own, [M15](milestones/M15_companies_completion.md), which also takes the backlog's reorganisation, shares and valuations item. It runs after M13 and before M14.

**UQ24. Placeholders with no system.** **Decided:** keep them greyed (§8.1). Strat doesn't know yet what industrial expertise should be, but does want know-how modelled, so the placeholder is labelled know-how and the backlog carries its design.

**UQ25. The General and Sectors split.** **Decided:** as laid out. General is the economy's health; Sectors is industry and the investment flowing into it.

### Open

**UQ26. Public works' base cost.** UQ18 makes public works buy construction speed. A funding factor on the country projects' cost, as the line had before, would cost nothing in a month with no project and still speed construction. The projects' cost is also counted in Construction already (`construction_spending` adds `projects_spending`).
*Recommend:* public works gets its own per-head and per-GDP base cost, as law and order, education and healthcare have, added with its effect in M13. The projects' cost stays in Construction.

---

## Appendix: the mockup prompts
Kept word for word. These are the prompts the mockups were drawn from, written before the rework. Where they disagree with the plan above, the plan wins.

### Budget Tab
**Prompt**
Create a mockup-design for a budget tab for a video game set in the Victorian Era. It should have two main sections for Revenue and Expenditure, as well as a smaller section for debt & the net value. The revenue section should have sections for Personal Tax, Asset Tax, Corporate Tax, Sales Tax, and Minting each adjustable with 5 buttons to set rates (very low, low, medium, high, very high) and a value for each for the amount of revenue from each. There should also be a few other rows for revenues from Public Enterprises, Tariffs, Diplomacy, and one from Other sources, but these are not adjustable and just have a value for revenue from these sources. There should be a pie chart for the distribution of these sources. The Expenditure Section should include mini-sections for Military, Government, Public Services, Subsidies, and Debt. The Military sub-section should include Operations, Procurement, Maintenance & Repair & Personnel, all adjustable like those rows in the tax section. The government subsection containing patronage, intelligence, bureaucracy, construction, again all adjustable. Public services containing Law & Order, education, Healthcare, welfare, and public works, all adjustable. Subsidies containing research subsidies, infrastructure subsidies, industrial subsidies, and a development fund, all adjustable. And finally the debt section should have a Debt to GDP graph, the debt amount, credit rating with the interest rate, and the actual interest amount with buttons to borrow, repay, and/or declare bankruptcy. There should then be a small net budget total, with a net budget graph, and net-budget to GDP.

**Later Prompts**
Okay I'm laying out the tab itself now and I can put the pie charts in the top next to the title header, but then I'm wondering *where exactly* the pie chart would go. One alternative is to put the title on the left side, keep the money amount in the middle, and have a sectioned off area on the right with the pie chart (probably works?). I can't really do a "hover over pie chart, reveal details" thing exactly (I guess I could put the details in a tooltip), but I could color the icons of the sources to the colors of the pie chart. That would make it immediately obvious which section belongs to which.

>insert AI response

Completely forgot about budget management AI. I think I could put that into that section. Basically have a list of automation options like Austerity, Balanced, Expansionary, War Economy, etc. What other options could be included here? Looking for an expansive list (with what emphasis to put on it - aimed usually at a specific goal in mind) that I can cut down to a final set. That and the AI can use this system too.

I think there should probably be a broad set of four doctrine sets you choose from:
Fiscal Management (how you treat deficits & surpluses)
Economic Development (how you treat expanding the economy)
Sociopolitical Policy (how you treat social spending)
Military Readiness (how much emphasis is on military spending)

The overlaps are also on purpose. A developmental state with social welfare running austerity will seek to reduce spending (as austerity is more important in this case). What the AI sets will probably be dependent on a single AI value for each slider, where at a threshold they will adjust it up or down (so the threshold for High might be +60, but you also have a stickiness of 10, so once the AI is on High, to reduce it to Medium it'd have to be at +45).

Economic Development, Sociopolitical Policy, and Military Readiness sorta set the "base" values for that, but fiscal management will allocate resources according to the current policy. Total War might set all military spending to +200, but if the state is running austerity (for whatever reason), that will run a separate value on top of every spending level decreasing it by 1 until it runs a surplus and an increase of 1 for each tax as well. Iterating until it achieves surplus. This would likely mean military spending reduction would be reduced last.

Each could have their own modifiers too, but then you have a toggle for AI control. Just to make it more interesting and not a waste of space if you're manually controlling it.

**Aditional Notes**
There are sections for subsidies & development credits & consumption taxes that should be able to have pop-up windows where you choose which industries/goods are affected.

### Macro Tab
**Prompt**
Okay so my next tabs are nowhere near as organized. To note, I got a little inspired off of that design and so there's going to be more an "Economy" tab with budget, macro, and states tabs underneath that.

The next tab would be Macro to work on, and this section would also have subtabs for "General", "Financial System", and "Companies." So the next focus would be on I think the "General" tab.

I have the following notes on this:
	## General ##
	- Economy Cycle Phase (Economic Boom, Fast Growth, Steady Growth, Stagnation, Recession, Depression, Free Fall)
	- GDP, GDP per capita, Unemployment, Inflation, Inequality
		- One large graph with the option to swap between these metrics
	- Total Investment, Consumer Spending, Import/Export Balance, Sectoral/Industry Composition, Manufacturing Index, Industrial Expertise
	- Consumer Confidence (100.0 default), Investor Confidence (100.0 default), Economic Incentives (100.0 default)
	- Resource Lack 
	- Investment Fund (Current inflow, Spending, Current spending)
	- Investment Opportunities
		- List of opportunities with each Industry Type (w Icon), State, Cost & Current Investment, & Attractiveness (list sorted by attractiveness)
	- List of industries under construction or being retooled
	- Economic Warnings (for the player): Negative Growth, High Inflation, High Deficit, High Govt Debt, High Private Debt, Bubble Risk, High Inequality, High Unemployment

I want you to generate a mockup design for this tab, in a similar style to your previous generation.

### Financial System
**Prompt**
Awesome. Next tab, again generate another mockup design, this time for the Financial System tab. 
	## Financial System ##
	- Currency
		- Current Currency used (Pound, Dollar, Mark, etc.)
		- Commodity Reserves (Typically Gold, sometimes Silver)
		- Money Supply (One value)
		- Money Demand (Driven by GDP of countries that use this currency)
		- Exchange Rate / Relative Value of currency (% of base value)
		- Minting/Money Printing (Adjustable here too. 5 buttons)
		- Current Monetary Law (Commodity Standard vs Dual Commodity vs Fiat vs Pegged vs so on)
		- Inflation/Deflation Rate
	- Central Bank 
		- Discount / Policy Interest Rates (adjustable value. Up and down buttons by 1%)
		- Money loaned to Banking System (Lender of last resort)
		- Can be enabled/disabled due to laws. Status is either Nonexistant (grayed out?), Independent, Inteference, Nationalized
	- Banking System
		- Reserve Reqs (adjustable value. Up and down buttons by 1%)
		- Total Savings (pop-driven)
		- Loan Portfolio: Capacity vs Outstanding
		- Non-performing Loans / Bad Debt Ratio
		- Lending Rate
		- Bank Status (Insolvent, Critical, Distressed, Strained, Solvent)
		- Banking Confidence (100.0 default)
	- Financial Markets
		- Credit Availability (tied to investment. This is like a "total" available)
		- Stock Performance
		- Speculation/Bubble Risk
		- Foreign Capital Flows

### Companies
**Prompt**
Awesome. The next tab is companies. The only additional thing of note here is that the actual image will be wider due to the company detail view, but the tab itself should stay the same size. So I want you to generate a mockup design for the Companies tab & Company Detail view using the following notes:
	## Companies ##
	- Stock Market (Market-level summary)
		- Graph of total market capitalization
		- Volatility %
		- Top Gainer, Top Loser
	
	- Companies
		- Aggregate Company Sats: Total Revenue, Profit, Debt, Investment, R&D, Employment
		- General Grants (adjustable, 5 buttons)
		- Found New SOE Button
		- Filters: Ownership Type, Foreign/Domestic/Both
		- Sort: Industry, Capitalization (default), Profit Margin
		- Summary Cards: Mini-Logo/Icon | Name | Type (Private, Public, SOE) | HQ State | Primary Industry | Market Share | Profit | Profit Margin | Stock Price Trend (arrow) | Complacency % | Current Project (Industry, State, Funding Progress)

	- Company Detail View (Click a company. View off to the side of the tab)
		- Header: Logo/Icon | Company Name | Type | HQ
		- Financials:
			- Revenue / Expenses / Profit breakdown
			- Current Debt
			- Capital Raised via Retained Earnings/Equitiy Issuance/Debt/Government Grants
			- Stock Valuation & Shares: Valuation Formula (Assets + Trajectory + Margins + Modifiers) | Stock Price | Shares Outanding | Ownership % (Private vs State vs Creditors vs Treasury Stock)
		- Operations & Departments
			- Current Project (Industry, State, Cost, Funding Progress, Attractiveness)
			- Active constructions/upgrades
			- List of Departments (One industry focus for each, vertical/horizontal integration bonuses. R&D section for throughput, output, input, construction bonuses, progress to tech bonus)
			- List of branches (Foreign Country, current revenue stream *from* branch, current investment *to* branch, valuation of branch)
		- Actions Menu
			- Purchase Stake
			- Bailout
			- Nationalization
			- Direct Grants (adjustable, 5 buttons)
		- Behavior & Risk
			- AI Behavior State: (Rapid Growth / Monopolization / Optimization / Crisis Management etc.)
			- Compacency Level % (High = more dividends, less risk taking/R&D)
			- Bankruptcy Risk & Status
