# M12: Money, inflation and currency

**Spec:** §16–18. **Depends on:** M11. **Questions:** Q45–Q49, Q52, Q67, Q69, Q70; revised by the M12 decisions on 2026-11-17 below. **Status:** implemented; simulator and in-game currency settlement verified. Final investment rounding fix is simulator-verified and postdates the supplied saves.

## Implemented behavior

- One currency per market. `base_money` alone remains a nominal issuance counter; cash, wages, accounts and loans remain real. P starts at 1 but is not held there as the economy changes.
- D is initialized from `(B / P + performing loans) / monthly market GDP`; zero-GDP fallback is 12. The target ratio is `(B / P / GDP + loans / GDP) / D`. P changes by `clamp(0.10 × (ratio − 1), −0.05, 0.05)` monthly, outside a 0.001 dead band. P is bounded to 0.01–100; zero GDP holds P. Loans exclude undrawn commitments.
- Before prices/banks/countries settle, old P / new P revalues all cash, debt, bank capital/reserves/assistance and wages, including company and investment/construction cash. Pending household payments, budget inputs and dividends are revalued consistently. Historical series and physical assets are unchanged. A global month-index guard prevents repeat settlement.
- Foreign asset records are creditor-real; borrower liability = asset × creditor exchange / debtor exchange. Creditor inflation erodes the asset. All debt APIs, interest, repayments, write-offs and inheritance convert across that boundary.
- Mining adds last month's national valuables production to physical reserves, without a treasury charge or diversion of ordinary goods. Valuables use ordinary pricing and can trade. Actual exports minus imports, before domestic tariffs/shipping, settle into reserves at actual valuables price. Reserves floor at zero and report unfunded settlement.
- Exchange adequacy = physical reserves × actual valuables price / (3 × market GDP), capped to 0–10. Target = `1 + sensitivity × (adequacy − 1) / (adequacy + 1)`; actual rate closes 10% monthly, bounded 0.25–4. Higher means stronger. Effective world prices multiply underlying prices by eligible foreign GDP-weighted exchange / own exchange. The partner cache reuses the existing eligibility pass. The trade AI's import/export direction stays on pre-trade need/production against world demand/supply, as before M12; exchange rates move the volume. A price-based direction test was tried and reverted on 2026-11-19: capped prices tied, so short markets stopped importing (no world tools trade at startup, and none at month 60).
- Market splits inherit P and exchange rate. Joins convert nominal money at the P ratio, preserve real cash and physical reserves, and recalibrate D to retain old real-money-weighted target pressure. Foreign liability mirrors refresh at new exchange rates.
- Inflation above 1% per month applies `−min(0.20, 2 × max(0, inflation − 0.01))` through a reversible stability modifier. No permanent monthly subtraction; no deflation penalty.

## Provisional monetary-law coefficients

| Law | Backing | Issuance effectiveness | Exchange sensitivity |
|---|---:|---:|---:|
| Absent / no standard | 0 | 1.00 | 0.25 |
| Single commodity | 0.40 | 0.25 | 0.75 |
| Dual commodity | 0.30 | 0.40 | 0.60 |
| Mixed | 0.15 | 0.70 | 0.40 |
| Fiat | 0 | 1.00 | 0.10 |
| Pegged | 0.30 | 0.40 | 0.60 |

`mint_base_money` scales the requested nominal amount by effectiveness, then caps real issuance at `max(0, reserve_value / backing − B / P)` where backing is positive. Output `minted_temp` is actual nominal issuance; treasury receives actual / P. Emergency lending retains M11's separate collateral rule. Pegged laws supply coefficients only; bilateral peg selection/defense and player controls remain later work. Historical balancing remains M14.

## Verification and reproduction

Run inside `redux-eco-sim/`:

```text
python tools/test_m12.py
python tools/test_m11.py
bin/ecosim_cli.exe check --parse-only
bin/ecosim_cli.exe run --scenario scenarios/world_1857_eng.txt --months 60 --watch-file watches/m12.txt --out runs/m12_final --dump-json runs/m12_final/final.json
bin/ecosim_cli.exe run --scenario scenarios/world_1857_eng.txt --months 60 --watch-file watches/m12.txt --inject 24:scenarios/m12_mint.txt --out runs/m12_mint
bin/ecosim_cli.exe run --scenario scenarios/world_1857_eng.txt --months 60 --watch-file watches/m12.txt --inject 24:scenarios/m12_deficit.txt --out runs/m12_deficit
bin/ecosim_cli.exe compare runs/m12_base runs/m12_final
```

The fresh pre-edit baseline is `runs/m12_base` (60 months). Assertions cover equilibrium, inflation/deflation and bounds, all revalued stock classes, duplicate settlement, mining/trade reserves, relative-price trade feedback and eligible partners, unequal-currency debt and inheritance, all monetary laws, and explicit/automatic splits and mergers. `finance_tests` includes five reversible currency checks; `eco_currency_report` is a read-only in-game report.

The full parser's nine pre-existing errors in six unrelated files remain. Existing economy division warnings also occur in the baseline; new economy load errors, overflows and invalid scopes are not accepted.

**In-game check pending:** start a fresh game on this code, run `effect finance_tests = yes` (18 expected assertions), save startup and two monthly ticks, and compare with the matching simulator scenario. Check `error.log` for economy math-load errors. Existing saves from the earlier M11 test do not validate M12.


## Simulator results (2026-11-17)

All eleven M12 integration groups and all eleven M11 regression groups pass. The reversible finance harness reports 18 passed, 0 failed. Final runs use the same 60-month world scenario and seed as the fresh pre-edit baseline.

| Check | Result |
|---|---|
| Normal run | ENG P ends at 0.93507; exchange rate 0.75118; GDP 6,963.51 (0.65% above M11-code baseline). |
| Minting shock after month 24 | Nominal base money doubles. Month-25 P is 1.01137 versus control 0.95891, reaching 1.80409 at month 60. High-inflation stability penalties appear and recede. |
| Reserve payment after month 24 | One-off physical reserve drain lowers month-25 exchange to 0.77079 versus control 0.77189. The focused deficit test independently verifies reserves fall, exchange weakens and the resulting actual trade balance improves with other inputs held fixed. |
| World stock audit | All 332 banks and 1,455 states pass loan-category, household principal and credit-reservation reconciliation. No negative loan/reserve stocks or physical capacity; insolvent banks cannot lend. |
| Diagnostics | No new economy errors, currency-file diagnostics, overflows or invalid scopes. The baseline's old division warnings and nine unrelated parser errors remain. |
| Cost | 10,799,505 operations/month versus baseline 10,186,608: +6.02%. Eligibility caching reduced the first pass's +31.42% overhead. |

`python tools/analyze_m12_runs.py` reproduces the stock/shock audit and writes `runs/m12_validation.md`. Detailed evidence is in each run's report and CSVs; assertion logs are in `runs/m12_checks` and `runs/m11_checks`.

M14 observations: the stripped map has prolonged reserve shortages; the USA's test industries produce strong reserve accumulation and its P reaches about 3.06 over five years. These are balance observations, not reasons to tune the workbook during M12. Valuables repricing changes startup output value, so compare fresh games and the fresh baseline, not old saves or M11 endpoints alone.

M12 in-game check (2026-11-17): fresh startup save and autosave dated June 17, with `global.month = 2`, were compared with `world_1857_eng` at months 0 and 2. `game.log` records `finance_tests` as 18 passed, 0 failed (the user reported 19). No `_economy_banking.txt` or `_economy_market.txt` load errors appear in `error.log`; pre-existing `_internal_politics_effects.txt` math errors remain. Startup ENG P = 1, demand multiplier = 12, exchange = 1, GDP 5,652.715 vs sim 5,679.559. At tick 2 ENG P = 1.00069 vs 1.00073, exchange = 0.95250 in both, GDP 6,185.872 vs 6,239.723 (-0.863%); ENG bank loans 8,198.387 vs 8,099.337 (+1.223%), and borrower-category sums reconcile exactly. USA P = 1.05 in both, exchange 1.00962 vs 1.00983, reserves 10,227.355 vs 10,042.150; USA GDP 9,738.566 vs 9,191.891 (+5.95%) and pool debt 18,162.399 vs 12,483.552 (+45.49%) need investigation. FRA P = 1.00107 vs 1.00120, exchange 0.95250 in both. The saves do not include a first-month snapshot: keep in-game completion pending until one is available and the US divergence is understood. The US uses scripted startup test industries, so inspect state/order and investment first, not currency assumptions. Extracted files: `redux-eco-sim/runs/m12_start_ingame.json`, `m12_june_ingame.json`, `m12_start_sim.json`, `m12_july_sim.json`.

The US tick-2 difference is concentrated in new pool-funded investment: `investment_funded_credit` is 13,048.97 in-game vs 7,206.00 in the simulator, accounting for almost all of the 5,678.85 pool-debt gap. Sector revenues are broadly closer. This narrows the investigation to investment opportunity/funding and first-tick state, but does not yet establish a cause.

### June save follow-up (2026-11-17)

The new `ENG_1857_06_01_01.hoi4` has `global.month = 1`, with a fresh matching startup save. It confirms the first tick: ENG GDP 6,206.00673 vs sim 6,222.36207 (-0.263%), bank loans 4,820.77400 vs 4,809.10662 (+0.243%), P = 1 and exchange = 0.975 in both. US first-tick pool debt is 6,769.61409 vs 6,917.34365 (-2.14%), so the large second-tick pool gap is not present initially.

`python tools/analyze_m12_ingame.py` passes 688/688 checks: all 332 banks' loan-category totals in both tick saves, startup currency calibration, and ENG/USA/FRA second-tick price, erosion, exchange and capital-after-interest formulas. British second-tick P remains within 0.00004 of the simulator. The existing log records 18 finance assertions passed, 0 failed. These saves validate M12's currency settlement in-game; the second-tick save is from the preceding replay, so no claim is made that every state input is identical across runs.

A funding threshold explains an important investment discontinuity: the simulator's Minnesota tooling opportunity costs 3,778.40664 but its allocated retained-plus-pool funding is 3,778.37010. Five-decimal division yields 0.99999 levels, rejected against the 1.0-level minimum; the game starts 1 level. `investment_try_expansion` now allows 0.0001 levels of tolerance only in minimum admission, and still builds/charges the exact funded amount. The regression first failed on the old code, then passed; materially underfunded starts still wait. The adjustment can change other marginal starts too, so it does not guarantee identical US pool totals.

US first-tick GDP remains about 10.1% above the simulator. Farm output is almost identical (crop-farm bundles 6,453.788 vs 6,451.015), while actual food price is 1.72107 vs 1.63817, following fulfilled food exports 5,953.187 vs 5,416.671. Military production resource spending is also 178.018 vs 1.091. These observed trade/engine-input differences remain a simulator parity limitation; no currency formula failure was found. Do not retune M12 coefficients or the workbook to force matching totals.

Post-tolerance references: `runs/m12_rounding_final`, `runs/m12_rounding_mint`, `runs/m12_rounding_deficit`; the original `m12_final` family remains the pre-fix evidence. The tolerance fix has simulator verification; the supplied game saves predate that final change. Audit detail: `runs/m12_ingame_audit.json`.

Post-fix validation: all 12 M12 groups pass; the three 60-month `m12_rounding_*` runs and world stock/shock audit pass. Normal run: ENG P 0.94962, exchange 0.75054, GDP 7,363.73. Cost is 10,808,201 ops/month, +6.10% versus `m12_base`. `python tools/analyze_m12_runs.py m12_rounding` writes `runs/m12_rounding_validation.md`. The parser still reports only the same nine unrelated errors.
