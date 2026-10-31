#!/usr/bin/env python3
"""
Checks that the PM data the game script actually reads matches the planning workbook.

    python toi/documentation/scripts/verify_pm_audit.py

Runs eco_sim_pm_audit through redux-eco-sim, which reads every method back through the real scripted variables,
and compares each building + method against what the sheet says, per K of base workforce at 1857 base prices.
Transport inputs aren't in the input total: industries no longer pay for them.
"""
import pathlib
import re
import subprocess
import sys

import generate_pm_data as gen

SIM = gen.TOI.parent / "redux-eco-sim"
TOLERANCE = 0.00002       # one or two units of fixed-point truncation
PARITY_TOLERANCE = 0.002  # production multipliers are truncated to 5 decimals, so these carry that rounding
SUM_TOLERANCE = 0.00012   # totals of up to ten rows, each truncated separately


def main():
    out = subprocess.run([str(SIM / "bin/ecosim_cli.exe"), "effect", "--scope", "ENG", "eco_sim_pm_audit = yes"],
                         cwd=SIM, capture_output=True, stdin=subprocess.DEVNULL, timeout=180).stdout.decode("utf-8", "replace")
    rows = [m[1].strip().split("|") for m in re.finditer(r"EOPM\|([^\r\n]*)", out)]
    if not rows:
        sys.exit("No EOPM lines: did the sim fail to start?")

    methods, _ = gen.load_methods()
    _, price = gen.resolve_assignments(methods)
    pg = gen.load_sheet(gen.WORKBOOK, "PM_Goods")

    revenue, inputs, sheet_construction = {}, {}, {}
    for r, row in pg.items():
        if r == 1 or not row.get("A"):
            continue
        t = gen.tokenize(row["A"])
        qty = float(row.get("E", 0) or 0)
        good = row.get("D")
        if row.get("C") == "output" and good not in ("transport", "shipping"):
            revenue[t] = revenue.get(t, 0) + qty * price[good]
        elif row.get("C") == "input" and good != "transport":
            inputs[t] = inputs.get(t, 0) + qty * price[good]
        elif row.get("C") == "construction":
            sheet_construction[t] = sheet_construction.get(t, 0) + qty * price[good]

    bad, checked, seen = [], 0, set()
    parity = {b for b, g in gen.PARITY_GOOD.items() if gen.PARITY_REFERENCE["mining"] != g and gen.PARITY_REFERENCE["farming"] != g}
    for b, t, rev, inp, wrk, mid, use, cap, ship, con, dur in rows:
        m = methods.get(t)
        if m is None:
            bad.append((b, t, "not in the generator's output"))
            continue
        seen.add(t)
        tol = PARITY_TOLERANCE if b in parity else TOLERANCE
        expected_rev = revenue.get(t, 0) if not getattr(m, "legacy", False) else None
        expected_in = inputs.get(t, 0) if not getattr(m, "legacy", False) else sum(q * price[g] for g, q in m.inputs)
        expected_con = sheet_construction.get(t, sum(q * price[g] for g, q in m.construction))
        wanted = [("inputs", inp, expected_in), ("wrk", wrk, m.wrk or 0), ("mid", mid, m.mid or 0), ("transport use", use, m.transport_use),
                  ("transport out", cap, m.transport_out), ("shipping", ship, m.shipping), ("construction", con, expected_con),
                  ("duration", dur, m.duration)]
        if expected_rev is not None and not m.kind == "am":
            wanted.append(("revenue", rev, expected_rev))
        if t == "pm_subsistence_farming":
            wanted = [w for w in wanted if w[0] not in ("wrk",)]
        for name, got, want in wanted:
            checked += 1
            limit = max(tol, tol * abs(want), SUM_TOLERANCE if name in ("construction", "inputs") else 0)
            if abs(float(got or 0) - want) > limit:
                bad.append((b, t, f"{name}: script {got}, sheet {want:.5f}"))

    missing = sorted(set(methods) - seen)
    print(f"{len(rows)} building + method rows, {len(seen)} methods, {checked} values compared")
    print(f"methods never read: {missing or 'none'}")
    print(f"mismatches: {len(bad)}")
    for row in bad[:40]:
        print("  ", *row)
    sys.exit(1 if bad or missing else 0)


if __name__ == "__main__":
    main()
