# M06: Natural resources and extraction

**Spec:** §9. **Depends on:** M04. **Questions:** Q28–Q30, Q68, all decided. **Status:** not started.

## Goal
The economy owns its deposit data, in three stages:
- **Potential:** not found yet. Prospecting turns it into known deposits.
- **Known:** found and open for expansion, but working it needs investment.
- **Active:** being worked now.

Quality is stored separately from quantity, and output = capacity × utilisation × PM productivity × quality × infrastructure effect.

## Exists now
- **Deposits:** the code already has the three stages. An RGO's size comes from `base_resource@`, which is read from HOI4's `resources = {}` blocks. The strip commented those out.
- **Code:** `add_rgo_internal` moves deposits between the stages. Prospecting is random rolls with a chance of a major find. `_init_resources` divides reserves by the good's price.
- **Military link:** the `resource_trade` dynamic modifier pushes economy goods into HOI4 resources, so equipment production can use them.

## Build
1. **Deposit data** (Q28): potential deposits, known deposits and quality per good become state history variables. HOI4's `resources` blocks no longer feed the economy.
2. **Active deposits** (Q68) are the RGO's size, stored once. Known deposits minus size is what investment can still open up.
3. **Rules** (Q29): active capacity can't exceed known deposits. Quality scales throughput, not jobs. There's no depletion, and wood is renewable.
4. **Prospecting** (Q30) becomes an investment opportunity. Its investment side lands in M09.
5. Keep `resource_trade` working.
6. Update `catalogue_1857_targets.py` and the history-block format if the deposit variables change it.

## Done when
- RGO output follows the formula above in the simulator.
- No economy code reads HOI4 state resources.
- HOI4 equipment production still gets its resources in-game.
