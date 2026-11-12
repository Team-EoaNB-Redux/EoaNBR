# M12: Money, inflation and currency

**Spec:** §16, §17, §18. **Depends on:** M11. **Questions:** Q45–Q49, Q52, Q67, Q69, Q70, all decided. **Status:** not started.

## Goal
- **Everything stays in real values** (Q46): 1857 pounds at the current scale (1,000 = £1M). Nothing in the simulation is inflated, which avoids overflow.
- **One currency per market** (Q45).
- **The price level** concerns only money in circulation: P × Y = M × V, where:
  - M = base money (from M11) + bank money, which follows performing loans;
  - Y = real GDP;
  - V is probably a constant, possibly partly driven by consumer confidence.

  P moves gradually toward M × V ÷ Y.
- **Inflation erodes stored money** (Q52, Q67): stored money, loans and wages lose real value under inflation and gain it under deflation, and high inflation may hurt stability.
- **Commodity reserves** in valuables rise and fall with the trade balance and valuables production. Reserve adequacy sets a damped exchange-rate scalar.
- **Trade** compares real prices, adjusted by relative exchange rates.
- **Monetary laws** change coefficients, not formulas.

Money doesn't need closing: it's created and destroyed all the time (Q52).

## Exists now
- No money supply, price level or reserves exist. Base money comes from M11.
- Valuables have a fixed price of 2× base.
- Trade value is recorded per good: `trade_value@<good>` is the traded amount × price, less tariffs, and `trade_value` holds the total. There's no split into imports and exports.
- The politics rework's `monetary_system_tokens` cover no standard, single and dual commodity standards, a mixed standard, fiat and a pegged currency.

## Build
1. **Money demand and the price level,** per market, starting at P = 1.
2. **Inflation's effects** (Q67):
   - Each month, rescale the treasury, domestic government debt, bank loans, pop debt and the floating base wage by P_old ÷ P_new. The wage then recovers through utilisation.
   - Foreign debt is held per creditor (`debt_to_bank_k@<tag>`, Q70). Each debt shrinks with the inflation of its creditor's currency, and moves with the exchange rate between the creditor's currency and the debtor's.
   - A stability penalty for high inflation.
3. **Market changes** (Q69): a country leaving a market keeps its GDP share of base money and valuables reserves (M11), and starts its own currency at the market's price level. A joiner's money converts at the ratio of price levels, and its reserves join the market's.
4. **Seigniorage at real value:** the minted quantity ÷ P (Q49).
5. **Commodity reserves in valuables** (Q47), standing for gold, silver, gems and other valuables. The government buys them on the market, and they lose their fixed price.
6. **Trade balance** (Q48): import value and export value per market, plus the total balance, settled against reserves.
7. **The exchange-rate scalar,** damped and non-linear, applied where trade compares prices.
8. **Coefficients for the monetary laws.**
9. **Nominal values in the UI** come later, if at all. Each currency would get a value against the pound, applied only in scripted localisation.

## Done when
In the simulator:
- minting raises the price level gradually, and erodes the treasury and debts as designed;
- a trade deficit drains reserves and weakens the scalar, which then improves the balance;
- at baseline the price level stays at 1;
- a country leaving or joining a market sees no jump in its price level;
- no stored economic value is nominal.
