# Segment 06: investment rework

> **Archived 2026-11-11.** Superseded by the milestone plan in [../00_README.md](../00_README.md), built on the new spec [EOANB_Redux_Economy_Redesign_Updated.md](../EOANB_Redux_Economy_Redesign_Updated.md). Kept for history: status and file references below are as they were when archived.

From the redesign spec (§13–30, 33). Not started. Investment is off: `global.eco_investment_enabled = 0`.

## What's disabled and must come back
- `io_*`, `investment_funds_monthly`, `investment_opportunities_monthly`, `national_opportunities_monthly` (`_economy_main.txt`, `_economy_setup.txt`)
- Company projects in `companies_monthly` (`_economy_companies.txt`). `companies_update` still runs
- **Downsizing** in `industry_update`. **Retune it when re-enabling:** scrap is 10% of asset value and construction is about 4× cheaper than before, so one bad month sheds about 4× as many sizes. That wiped out machinery and steel within 6 months. Consider a cap on sizes shed per month
- `_economy_investment.txt` and `_economy_investment_buckets.txt` still read removed fields (`building_base_output_value`, `controller:pm_*`). Unreachable while gated; replace or delete
- AI PM/AM upgrades run through `io_upgrade_pm` / `io_upgrade_am`. With investment off, nothing upgrades, and steel stays stuck
- Pop investment money still accumulates in `investment_fund`

`_economy_investment_buckets.txt` is an earlier untracked attempt at local/national pools. Worth reading for reuse, but it isn't hooked up.

## Design (spec)
**Opportunities, not profitability.** Existing profitability says how well current capital does. An opportunity says how much new capital could go in at what return. Gold can be hugely profitable with almost no room left.

**Money in tiers, per sector:** Exceptional >20% ROI, Good 10–20%, Fair 5–10%, Marginal −5–5%, below that ignored. Fund best first. Only the tier is stored, not exact ROI. Advertised opportunity may far exceed available money.

**Brownfield:** existing state-industries estimate ROI, plausible near-term size, and cost. Simple labor estimate: Available Expansion Labor = Unemployment + a small fraction of employment (example 0.03%). Several industries may assume the same labor; don't build a solver. Best projects go first, wages rise, weak ones lose profit. **One expansion per state-industry at a time.**

**Limited industries:** hard caps from deposits, arable land, forests, port sites. Gold at 40% ROI with $3m of room offers $3m.

**Greenfield:** industries absent from a state. Coarse pre-filter first, using national prices, rough wages, best-IE state, hard eligibility; stop if below Marginal even then. Search budget: small countries (under about 5 states) check few absent industries a month, larger get more; newly unlocked ones get priority. Throttle: about one new establishment per sector per month, and unfinished greenfield projects lower the tier of more (1 underway −1 tier, 2 −2, ...).

**Capital:** no per-industry money pools. Investor pools instead:
- Landowner/Particular: agriculture, plantations, livestock, forestry, ports. Not modern factories.
- Capitalist/General: factories, mining, railways, ports, other industrial.
- Investor type filters which opportunities are visible.
- Dividends feed pools: farm profits to landowners, factory profits to capitalists.
- Non-agricultural GDP share moves capital from Particular to General.
- Capital-market development sets geographic mobility: fragmented means Illinois money stays in Illinois; integrated means it finances anywhere. A central gameplay distinction (Qing vs Japan vs industrial economies).

**Attractiveness:** no second profitability system. ROI tier sets desirability, investor type sets eligibility, other modifiers lightly weight.

**Philosophy:** don't predict feedback the simulation will resolve itself.

## Open balance values
Labor percentage, tier thresholds, search budgets, greenfield penalty, non-ag transfer function, local/national mobility rules, weighting within a tier, which financial history stays persistent.

## AM ROI (from the notepad and ROI tab)
`R = (W−N)/(E+W)`, monthly saving = `R × current wages`, `ROI years = C / (saving + V) / 12`. E, W, N are wage mults of PM, old AM, new AM. C is cost, V the value-add change. Desired about 5 years. The ROI tab assumes wages are 95% of VA.

## Flow
Profits → owner dividends → pools → market transfers → local/national availability → opportunities → best permitted funded → construction → opportunity suppressed while building → completion → employment, wages, prices, infrastructure adjust.
