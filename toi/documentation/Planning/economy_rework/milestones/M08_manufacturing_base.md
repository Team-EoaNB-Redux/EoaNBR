# M08: Manufacturing Base and HOI4 factories

**Spec:** §12. **Depends on:** M04. **Questions:** Q32, Q33, Q53, Q64, all decided. **Status:** not started.

## Goal
Civilian factories, military factories and dockyards stop being economic industries. The **Manufacturing Base** (`manufacturing_base`; §12's "underlying productive industrial capacity") is derived from the country's manufacturing sectors. A national allocation splits it into civilian, military and naval use, and HOI4's factory counts follow as **offmap** buildings. All on-map factories are removed.

This is the TNO-like version, option (c) of Q32. Long term, Strat prefers (b): the government contracts a slice of the manufacturing sectors, which takes that slice out of civilian output. Under (b) factories stay a straight conversion, with no employment to track.

## Exists now
- **Government buildings:** arms factories, industrial complexes and dockyards are special industries (`govt_building_update`). Their size follows the HOI4 building, they're always fully staffed, they sell no goods, and the state budget pays their wages. There are 303 of them in history.
- **Military demand:** `calculate_military_demand` and `_economy_definitions_units.txt` turn units and production into goods demand.
- **Offsite buildings:** `add_offsite_building = { type = arms_factory level = 1 }` already appears in several country decisions (BWR, CHO, CSA, DEN).
- **Name clash:** in code, `industrial_capacity` means Infrastructure Efficiency's supply, which is why §12's concept gets its own name (Q53).

## Build
1. **The Manufacturing Base** (Q64): the real output of the manufacturing sectors at base prices, ÷ a constant per factory, so idle plants and price swings don't create factories. There's no cut to civilian output for now; that may come later.
2. **The contract cost:** the state pays a monthly cost per factory in use, as a budget line. For now the money goes to no one: the manufacturing sectors lose no output, so paying them would be a pure subsidy. Under option (b) later, it would go to the sectors whose output it takes.
3. **The allocation:** civilian, military and naval shares, as a player control with AI defaults.
4. **Offmap factories** (Q33): set HOI4's offsite civs, mils and dockyards to the allocated counts each month, adding or removing the difference.
5. **Remove on-map factories:** strip the 303 history factories, block HOI4's own factory construction, and delete `govt_building_update` and the government-building industries.
6. Check what still needs on-map buildings: capture and damage stop mattering for factories, and focuses, decisions or events that add on-map factories need converting.

## Done when
- HOI4's civ, mil and dockyard counts follow the allocation in-game, as offmap buildings.
- No on-map factories remain in history, and players can't build any.
- The contract cost shows in the budget and scales with the factory count.
- Military production still draws goods and resources.
