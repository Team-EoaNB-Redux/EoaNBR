# M07: Infrastructure

**Spec:** §8. **Depends on:** M04. **Questions:** Q31 decided. **Status:** not started; mostly built.

## Goal
Infrastructure Efficiency is already built, and the spec keeps it. What's left: the free rural bonus goes, ports are paid from shipping use, and railways and ports become normal national sectors.

## Exists now
Formulas and knobs are in [archive/04](../archive/04_infrastructure.md). `calc_industrial_capacity` is in `_economy_market.txt`. Dependence by sector is subsistence 0, farming 0.3, extraction 0.6, factories 1 and urban 0.5, which matches §8.

Open problems:
1. States with no transport demand get the full +20% bonus for free.
2. Ports are paid from the state's demand-to-supply ratio, not from shipping use.
3. Rail and port pay is low in hubs.

Railway and port revenue has no payer, and that stays (Q31). Industries pay for congestion through lower throughput, and charging them a fee would localise the cost and remove part of the optimisation problem. The extra money only nudges prices up.

## Build
1. Scale the spare-capacity bonus by real supply per head, or drop it.
2. Pay ports from shipping use.
3. Run railways and ports through the M04 sector layer. Building more of them is investment, in M09.

## Done when
- Infrastructure Efficiency in ENG's hubs is about where it was before the change.
- Rural states no longer get a bonus they didn't build.
- Railways and ports show up as sectors with sensible revenue.
