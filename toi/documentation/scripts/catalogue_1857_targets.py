#!/usr/bin/env python
"""Writes the 1857 employment and output targets into the history files, as comments. Active script never changes.

The doc figures are in catalogue_1857_data.py. This file does five steps, and an edit to the data needs only a rerun.

  1. split()      Each doc line has a value and a worker count. Weights share both out across states.
  2. make_row()   Target output = GBP M a year x 1000 / 12 / base price. UK levels = workers / jobs a level.
                  India's levels are whatever makes the target on its owner's PMs, and the rest stay on subsistence.
  3. make_row()   Those levels at the sheet's PM give output_now. target / output_now is x, how far off the PM is.
  4. The tables   One for each state, and totals for ENG, RAJ and each other Indian tag.
  5. write_block() Puts each table between the markers, replacing the old one.

Example, coal in Yorkshire: coal is GBP 16.5M and 237K miners, and Yorkshire has 8.9 of the 65.4M tons, so it gets GBP 2.25M
and 32.3K miners. ENG's coal PM and AM use 0.82K jobs a level, so that's 39.4 levels. GBP 2.25M is 187.6 treasury a month, or
93.8 coal at $2. Those levels on ENG's PM make 4.63 coal each, plus 20% economy of scale, so 219 coal. x = 93.8 / 219 = 0.43.

Running it:
  redux-eco-sim/bin/ecosim_cli.exe run --scenario scenarios/world_1857_eng.txt --months 0 --dump-json start.json
  python toi/documentation/scripts/catalogue_1857_targets.py --dump start.json

The dump supplies population, start PMs, national modifiers, prices and per-K quantities. Add --dry-run to print only.
"""
import argparse
import collections
import glob
import json
import os
import re

import catalogue_1857_data as data

# 1,000 treasury = GBP 1M. The doc's figures are a year and the game's output is a month.
TREASURY_PER_GBP_M = 1000
MONTHS = 12
DOC_PARTICIPATION = 0.4

BEGIN, END = "# >>> 1857 economy target", "# <<< 1857 economy target"
SCRIPT = "documentation/scripts/catalogue_1857_targets.py"
TOI = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

ORDER = """crop_farm rice_paddy livestock_ranch cotton_plantation luxuries_plantation fiber wood coal iron copper valuables
steel_foundry tooling_workshop mechanical_works chemical_plant consumer_goods_factory textile_mill urban_center
entertainment_hub railway port""".split()
SHORT = dict(crop_farm="crop", rice_paddy="rice", livestock_ranch="ranch", cotton_plantation="cotton", luxuries_plantation="lux",
             fiber="fiber", wood="wood", coal="coal", iron="iron", copper="cop", valuables="val", steel_foundry="steel",
             tooling_workshop="tools", mechanical_works="mach", chemical_plant="chem", consumer_goods_factory="cons",
             textile_mill="text", urban_center="urban", entertainment_hub="ent", railway="rail", port="port")
RGO = {"fiber", "wood", "coal", "iron", "copper", "valuables"}
FARMS = {"crop_farm", "rice_paddy", "livestock_ranch", "cotton_plantation", "luxuries_plantation", "fiber"}
GOODS = """food luxuries fiber wood coal iron copper valuables steel tools machinery chemicals consumer_goods textiles
services entertainment transport shipping""".split()

Share = collections.namedtuple("Share", "building good label gbp_m workers")
Level = collections.namedtuple("Level", "goods jobs pm am revenue_per_k")
Row = collections.namedtuple("Row", "building levels workers doc_workers target gbp_m labels now target_value now_value")


class Model:
    """What one level does, read from the dump. Mirrors industry_production_update, with Infrastructure Efficiency at 1."""

    def __init__(self, dump):
        self.d, self.g = dump, dump["global"]
        self.step = self.g["buildings_economy_of_scale_factor"]
        self.cap = self.g["buildings_economy_of_scale_max"]

    def price(self, good):
        return self.g.get("base_price@" + good, 1)

    def value(self, goods):
        return sum(q * self.price(g) for g, q in goods.items())

    def scale(self, levels):
        return 1 + self.step * min(max(levels - 1, 0), self.cap)

    def levels_for(self, value, per_level):
        """Levels making value a month: output per level grows with the state's economy of scale."""
        low, high = 0.0, value / per_level + 1 if per_level else 0.0
        for _ in range(50):
            mid = (low + high) / 2
            low, high = (mid, high) if mid * per_level * self.scale(mid) < value else (low, mid)
        return high

    def level(self, tag, b):
        c, g = self.d[tag], self.g
        pm = c.get("starting_pm@" + b) or c.get("latest_production_method@" + b) or g.get("building_production_methods@%s^0" % b)
        am = c.get("starting_am@" + b) or c.get("latest_automation_method@" + b)
        emp, mult = g["building_base_employees@" + b], g["building_production_multiplier@" + b]
        modifier = (1 + c.get("industry_output_factor@" + b, 0)) * (1 + c.get("industry_throughput_factor@" + b, 0))
        modifier *= 1 + c.get("pm_throughput_factor@%s" % pm, 0) + c.get("pm_throughput_factor@%s" % am, 0)

        per_k = {}
        for i in range(int(g.get("building_base_production@%s^num" % b, 0)) or 1):
            good = g.get("building_base_production@%s^%d" % (b, i), b)
            per_k[good] = g.get("pm_output_amount@%s" % pm, 0) * mult * g.get("building_base_production_amount@%s^%d" % (b, i), 1)
        if b == "railway":
            per_k["transport"] = g.get("pm_industrial_capacity@%s" % pm, 0) + g.get("pm_industrial_capacity@%s" % am, 0)
        if b == "port":
            per_k["shipping"] = g.get("pm_shipping_capacity@%s" % pm, 0) + g.get("pm_shipping_capacity@%s" % am, 0)

        def tier(name):
            def part(m):
                return g.get("pm_workforce_%s@%s" % (name, m), 0) * (1 + c.get("pm_employment_factor@%s" % m, 0))
            return max(0, part(pm) + part(am))

        jobs = emp * sum(tier(t) for t in ("laborers", "workers", "peasants"))
        return Level({good: q * emp * modifier for good, q in per_k.items()}, jobs, pm, am, self.value(per_k))


def split(items, farm_workers, subsistence):
    """Step 1: every doc line as a value and a worker count per state. Food and farm workers lose the subsistence share."""
    gross = collections.Counter()  # Each state's value, before subsistence, of the farm lines with no workers of their own
    rows = collections.defaultdict(list)
    peasants = collections.Counter()
    for it in items:
        total = sum(it.weights.values())
        farm = it.building in FARMS
        for s, w in it.weights.items():
            gbp = it.gbp_m * w / total
            kept = 1 - subsistence.get(s, 0) if farm else 1
            sold = gbp * kept if it.good == "food" else gbp
            if farm and it.workers is None:
                gross[s] += gbp
                rows[s].append(Share(it.building, it.good, it.label, sold, None))
            else:
                workers = (it.workers or 0) * w / total
                rows[s].append(Share(it.building, it.good, it.label, sold, workers * kept))
                peasants[s] += workers * (1 - kept)

    # Farm workers left in each country follow the value of its farm lines, and those lines share them by value sold
    for states, total in farm_workers:
        fixed = sum(it.workers * w / sum(it.weights.values()) for it in items if it.building in FARMS and it.workers for s, w in it.weights.items() if s in states)
        value = sum(gross[s] for s in states)
        for s in states:
            workers = (total - fixed) * gross[s] / value
            kept = 1 - subsistence.get(s, 0)
            peasants[s] += workers * (1 - kept)
            sold = sum(r.gbp_m for r in rows[s] if r.workers is None)
            rows[s] = [r._replace(workers=workers * kept * r.gbp_m / sold) if r.workers is None else r for r in rows[s]]
    return rows, peasants


def make_row(model, tag, building, shares, by_value):
    """Steps 2 and 3 for one industry in one state."""
    level = model.level(tag, building)
    target = collections.Counter()
    labels = collections.Counter()
    for share in shares:
        target[share.good] += share.gbp_m * TREASURY_PER_GBP_M / MONTHS / model.price(share.good)
        labels[share.label] += share.gbp_m
    doc_workers = sum(share.workers for share in shares)
    if by_value:
        levels = model.levels_for(model.value(target), model.value(level.goods))
        workers = levels * level.jobs
    else:
        workers = doc_workers
        levels = workers / level.jobs if level.jobs else 0
    now = {g: q * levels * model.scale(levels) for g, q in level.goods.items()}
    return Row(building, levels, workers, doc_workers, dict(target), sum(share.gbp_m for share in shares), labels, now, model.value(target), model.value(now))


def state_rows(model, tag, shares, by_value=False):
    by_building = collections.defaultdict(list)
    for share in shares:
        by_building[share.building].append(share)
    return [make_row(model, tag, b, by_building[b], by_value) for b in ORDER if b in by_building]


# Text
def num(x):
    return f"{x:,.1f}" if abs(x) < 100 else f"{x:,.0f}"


def goods_text(goods):
    names = dict(consumer_goods="consumer goods")
    order = sorted(goods.items(), key=lambda kv: GOODS.index(kv[0]))
    return ", ".join(f"{names.get(g, g)} {num(q)}" for g, q in order if q >= 0.05)


def row_table(rows, with_labels=True):
    out = [f"{'industry':<31}{'levels':>7}{'jobs K':>8}  {'makes a month':<36}{'GBP M/yr':>8}" + ("  mostly" if with_labels else "")]
    for r in rows:
        name = r.building + " (resources)" if r.building in RGO else r.building
        line = f"{name:<31}{num(r.levels):>7}{num(r.workers):>8}  {goods_text(r.target):<36}{num(r.gbp_m):>8}"
        out.append(line + ("  " + ", ".join(k for k, _ in r.labels.most_common(3)) if with_labels else ""))
    return out


def state_block(rows, doc, home, tag, workforce, arable, peasants, by_value):
    jobs, farms = sum(r.workers for r in rows) + peasants, sum(r.levels for r in rows if r.building in FARMS and r.building != "fiber")
    basis = "its value" if by_value else "its workers"
    out = [f"{BEGIN} (generated by {SCRIPT})", f"A guide, from {doc}: levels come from {basis}, on {tag}'s start PMs. Key and totals: {home}"]
    out += row_table([r for r in rows if r.levels >= 0.05])
    if peasants:
        out.append(f"{'subsistence farmers':<31}{'':>7}{num(peasants):>8}")
    out.append(f"{'all':<31}{'':>7}{num(jobs):>8}  {'':<36}{num(sum(r.gbp_m for r in rows)):>8}")
    left = "on subsistence" if by_value else "left over"
    note = f"Workforce {num(workforce)}K, {num(workforce - jobs)}K {left}" if jobs <= workforce else f"Workforce {num(workforce)}K: SHORT by {num(jobs - workforce)}K"
    out.append(note + f". Arable land {num(arable)}, farms need {num(farms)}" + (f": SHORT by {num(farms - arable)}." if farms > arable else "."))
    return out + [END]


def total(rows, b):
    return sum(r.levels for r in rows if r.building == b)


def good_total(rows, good):
    return sum(r.target.get(good, 0) for r in rows)


def matrix(columns, row_names, value, width=9, label_width=24):
    out = [f"{'':<{label_width}}" + "".join(f"{c[:width - 1]:>{width}}" for c in columns)]
    for name in row_names:
        cells = [value(name, c) for c in columns]
        if any(cells):
            out.append(f"{name:<{label_width}}" + "".join(f"{(num(x) if x >= 0.05 else '.'):>{width}}" for x in cells))
    return out


def good_table(model, rows):
    out = [f"{'good':<16}{'GBP M/yr':>10}{'$ a month':>11}{'makes a month':>15}"]
    for g in GOODS:
        q = good_total(rows, g)
        if q:
            out.append(f"{g:<16}{num(q * model.price(g) * MONTHS / TREASURY_PER_GBP_M):>10}{num(q * model.price(g)):>11}{num(q):>15}")
    return out


def pm_check(model, tag, rows):
    """Revenue per K is the sheet's Revenue column for that PM. x is what its output needs multiplying by to hit the doc's value."""
    out = [f"{'industry':<24}{'PM':<31}{'jobs/lvl':>9}{'levels':>8}{'jobs K':>9}{'$ now':>9}{'$ target':>9}{'x':>7}  revenue per K, now -> needs"]
    for b in ORDER:
        group = [r for r in rows if r.building == b]
        if group:
            level = model.level(tag, b)
            now, target = sum(r.now_value for r in group), sum(r.target_value for r in group)
            x = target / now if now else 0
            out.append(f"{b:<24}{str(level.pm).replace('pm_', ''):<31}{level.jobs:>9.1f}{num(total(rows, b)):>8}{num(sum(r.workers for r in group)):>9}"
                       f"{num(now):>9}{num(target):>9}{x:>7.2f}  {level.revenue_per_k:.2f} -> {level.revenue_per_k * x:.2f}")
    now, target = sum(r.now_value for r in rows), sum(r.target_value for r in rows)
    out.append(f"{'all':<24}{'':<31}{'':>9}{'':>8}{num(sum(r.workers for r in rows)):>9}{num(now):>9}{num(target):>9}{target / now:>7.2f}")
    return out


def state_matrix(rows_of, regions, names):
    builds = [b for b in ORDER if any(total(r, b) for r in rows_of.values())]
    out = [f"{'':<22}" + "".join(f"{SHORT[b]:>7}" for b in builds)]
    for _, states in regions:
        for s in states:
            out.append(f"{names[s][:21]:<22}" + "".join(f"{(num(total(rows_of[s], b)) if total(rows_of[s], b) >= 0.05 else '.'):>7}" for b in builds))
    return out


def in_region(states, rows_of):
    return [r for s in states for r in rows_of[s]]


def workforce_table(regions, doc_pop, rows_of, peasants, pop, wf):
    out = [f"{'':<26}{'game pop':>10}{'game work':>11}{'doc pop':>10}{'doc x 40%':>11}{'listed':>9}{'game left':>11}{'doc left':>10}"]
    lines = [(n, s) for n, s in regions] + [("All", [s for _, ss in regions for s in ss])]
    for name, states in lines:
        doc = sum(doc_pop.values()) if name == "All" else doc_pop[name]
        listed = sum(r.workers for r in in_region(states, rows_of)) + sum(peasants[s] for s in states)
        game = sum(wf[s] for s in states)
        out.append(f"{name:<26}{num(sum(pop[s] for s in states)):>10}{num(game):>11}{num(doc):>10}{num(doc * DOC_PARTICIPATION):>11}{num(listed):>9}"
                   f"{num(game - listed):>11}{num(doc * DOC_PARTICIPATION - listed):>10}")
    return out


def region_matrices(regions, rows_of, short=None, width=9, label=24):
    short = short or {}
    columns = {short.get(n, n): ss for n, ss in regions}
    rows = in_region([s for _, ss in regions for s in ss], rows_of)
    goods = [g for g in GOODS if good_total(rows, g)]
    builds = [b for b in ORDER if total(rows, b)]
    out = ["", "Output a month by region, at the doc's value"]
    out += matrix(list(columns), goods, lambda g, c: good_total(in_region(columns[c], rows_of), g), width, label)
    out += ["", "Levels by region"]
    return out + matrix(list(columns), builds, lambda b, c: total(in_region(columns[c], rows_of), b), width, label)


def british_catalogue(model, rows_of, peasants, pop, wf, names):
    rows = in_region(sorted(rows_of), rows_of)
    out = [f"{BEGIN}s: British Isles (generated by {SCRIPT}, a rerun replaces this block)"]
    out += f"""
Source: documentation/Planning/economy_rework/eng_economy.md. Each state's own table is in its history file.
The 19 British Isles states only. The doc has nothing on the colonies, so they have no target yet.
Method: a guide, not a rule. Levels = the doc's workers / jobs a level on ENG's start PMs. x below shows how far each PM is from the doc's value after modifiers.
Scale: 1,000 treasury = GBP 1M. The doc's figures are a year and the game makes goods a month, so $ a month = GBP M a year x 1000 / 12.
Modifiers: $ now counts ENG's national output and throughput modifiers and economy of scale, with Infrastructure Efficiency at 1. x changes if those do.
Goods: food = crops + animal products, less the subsistence share. iron = pig iron + lead, ore counted inside pig iron. copper = copper + tin
(the doc has no separate bronze or brass, which stay in tools). fiber = wool + flax, no cotton or silk is grown here. luxuries = hops.
steel = wrought iron + crucible steel. machinery = machines + ships. services = the doc's services, less rail, ports and government.
Splits inside a country are mostly estimates. Coal and ore by state follow the old Hunt notes in the state files, whose coal sums to the doc's 65.4M tons.
Left out: government and defence (GBP 25M, the budget pays for it). Brewing and distilling (GBP 30M+ retail, no building for it).
Domestic service (GBP 30M, 1,385K workers) and housing (GBP 45M) are hidden: neither has a building. The doc's GBP 50M of transport is split by workers:\nrail 16.4M, ports 19.2M, road and canal 14.4M in services.
Ranches need a new split: food and wool only. Today's split makes about 3 fiber to 5 food by value, and the UK's was 1 to 8, so the x on that row is for the total.
""".strip().split("\n")
    out += ["", "Workforce, K. Listed = the industries below. Game work is 35% of game population (global.pops_workforce_participation)"]
    out += workforce_table(data.BRITISH_REGIONS, data.BRITISH_DOC_POP, rows_of, peasants, pop, wf)
    missing = sum(k for _, k in data.BRITISH_NOT_LISTED)
    out += ["", f"Not listed: GB 1851 census occupations the doc leaves out, about {num(missing)}K. The rest of the gap is Ireland off the farm, and family workers."]
    out += [f"  {name:<36}{num(k):>6}" for name, k in data.BRITISH_NOT_LISTED]
    out += ["", "United Kingdom by good"] + good_table(model, rows)
    out += ["", f"PM check. Subsistence farmers ({num(sum(peasants.values()))}K) aren't in it"] + pm_check(model, "ENG", rows)
    out += region_matrices(data.BRITISH_REGIONS, rows_of)
    out += ["", "Levels by state"] + state_matrix(rows_of, data.BRITISH_REGIONS, names)
    return out + [END + "s"]


def indian_catalogue(model, rows_of, pop, wf, owners, names, gdp):
    rows = in_region(sorted(rows_of), rows_of)
    out = [f"{BEGIN}s: India (generated by {SCRIPT}, a rerun replaces this block)"]
    out += f"""
Source: documentation/Planning/economy_rework/raj_economy.md. Each state's own table is in its history file. Each other Indian tag has its own totals.
India is split across tags at start, so this block is the whole subcontinent, and the tag table at the end shows who holds what.
Left out, as the doc doesn't cover them: Ceylon, Nepal, Bhutan, Sikkim, Kalat, Upper Burma, the Andamans, Goa, Pondicherry.
Method: a guide, not a rule. Levels are what makes the doc's value on each state's owner's start PMs, so India starts with few industries and most of its
people on subsistence. That hides most of the doc's workers, which is fine: they were part-time, and many were paid in grain.
Food loses each region's subsistence share. Most of the doc's Indian figures are its own estimates. It gives exports, not output, for several goods: sugar
(GBP 12.5M), cotton (5.4M), jute (0.9M), silk (1.05M) and wool (0.4M) are estimates from its tonnages. Tobacco, hemp, betel and salt tax have no value here.
Indigo and salt are in chemicals. Army and civil government are left out: the budget pays for them. 1857 trade figures are a Rebellion year.
""".strip().split("\n")
    out += ["", "Workforce, K"]
    out += [f"{'':<26}{'game pop':>10}{'game work':>11}{'doc pop':>10}{'in levels':>11}{'subsistence':>13}"]
    for name, states in data.INDIAN_REGIONS + [("All", list(owners))]:
        doc = sum(data.INDIAN_DOC_POP.values()) if name == "All" else data.INDIAN_DOC_POP[name]
        jobs = sum(r.workers for r in in_region(states, rows_of))
        out.append(f"{name:<26}{num(sum(pop[s] for s in states)):>10}{num(sum(wf[s] for s in states)):>11}{num(doc):>10}{num(jobs):>11}{num(sum(wf[s] for s in states) - jobs):>13}")
    out += ["", "Regions, with the tags holding them"]
    for name, states in data.INDIAN_REGIONS:
        out.append(f"{name:<26}{' '.join(sorted({owners[s] for s in states})):<16}sold GBP {num(sum(r.gbp_m for r in in_region(states, rows_of))):>6}M/yr")
    out += ["", "India by good"] + good_table(model, rows)
    out += ["", f"{'industry':<24}{'levels':>8}{'jobs K':>9}{'doc workers K':>15}"]
    for b in ORDER:
        group = [r for r in rows if r.building == b]
        if group:
            out.append(f"{b:<24}{num(total(rows, b)):>8}{num(sum(r.workers for r in group)):>9}{num(sum(r.doc_workers for r in group)):>15}")
    out.append(f"{'all':<24}{'':>8}{num(sum(r.workers for r in rows)):>9}{num(sum(r.doc_workers for r in rows)):>15}")
    out += [f"Subsistence alone gives these states {num(gdp)} GDP a month on the stripped map, about GBP {num(gdp * MONTHS / TREASURY_PER_GBP_M)}M a year. The doc says GBP 450-500M in all."]
    short = {"North-Western Provinces": "NW Prov", "Bengal Presidency": "Bengal", "Bombay and Sind": "Bombay", "Central Provinces": "C Prov", "British Burma": "Burma",
             "Hyderabad": "Hydbad", "Central India": "C India", "Baroda, Kathiawar, Cutch": "Baroda", "Travancore and Cochin": "Travnc", "Rajputana": "Rajput"}
    out += region_matrices(data.INDIAN_REGIONS, rows_of, short, 8, 23)
    out += ["", "Levels by state"] + state_matrix(rows_of, data.INDIAN_REGIONS, names)
    tags = sorted(set(owners.values()))
    by_tag = {t: in_region([s for s in owners if owners[s] == t], rows_of) for t in tags}
    builds = [b for b in ORDER if total(rows, b)]
    out += ["", "Levels by tag"] + matrix(tags, builds, lambda b, t: total(by_tag[t], b), 7, 23)
    return out + [END + "s"]


def tag_block(tag, rows, states, names):
    merged = []
    for b in ORDER:
        group = [r for r in rows if r.building == b]
        if group:
            target = collections.Counter()
            for r in group:
                target.update(r.target)
            merged.append(Row(b, total(group, b), sum(r.workers for r in group), 0, target, sum(r.gbp_m for r in group), None, None, 0, 0))
    out = [f"{BEGIN} for {tag}'s states at start (generated by {SCRIPT})", "Each state's table is in its history file. All of India: history/countries/RAJ - British Raj.txt"]
    out.append("States: " + ", ".join(names[s] for s in states))
    return out + row_table(merged, with_labels=False) + [END]


# Files
def write_block(path, lines, indent, before, dry):
    """Step 5: replaces the old block, or inserts one before the first line matching `before`, else at the top."""
    raw = open(path, "rb").read()
    newline = b"\r\n" if b"\r\n" in raw else b"\n"
    bom = b"\xef\xbb\xbf" if raw.startswith(b"\xef\xbb\xbf") else b""
    body = re.sub(rb"[ \t]*" + re.escape(BEGIN.encode()) + rb".*?" + re.escape(END.encode()) + rb"[^\r\n]*\r?\n", b"", raw[len(bom):], flags=re.S)
    text = newline.join((indent + (l if l.startswith("#") else "# " + l)).rstrip().encode("ascii") if l else (indent + "#").encode() for l in lines) + newline
    if before:
        m = re.search(before, body, re.M)
        if not m:
            raise SystemExit(f"no insertion point in {path}")
        body = body[:m.start()] + text + body[m.start():]
    else:
        body = text + body
    if not dry:
        open(path, "wb").write(bom + body)


def state_file(sid):
    hits = [p for p in glob.glob(os.path.join(TOI, "history", "states", "*.txt")) if re.match(rf"{sid}[- ]", os.path.basename(p))]
    if len(hits) != 1:
        raise SystemExit(f"state {sid}: {hits}")
    return hits[0]


def country_file(tag):
    hits = glob.glob(os.path.join(TOI, "history", "countries", f"{tag} - *.txt"))
    if len(hits) != 1:
        raise SystemExit(f"tag {tag}: {hits}")
    return hits[0]


def start_owner(s):
    text = re.sub(r"#[^\n]*", "", open(state_file(s), "rb").read().decode("latin-1"))
    return re.search(r"\bowner\s*=\s*(\w+)", text[text.find("history"):]).group(1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dump", required=True, help="month 0 --dump-json from the sim")
    ap.add_argument("--dry-run", action="store_true", help="print the totals, write nothing")
    args = ap.parse_args()
    dump = json.load(open(args.dump))
    model = Model(dump)
    names = {s: re.sub(r"^\d+\s*-\s*", "", os.path.basename(state_file(s))[:-4]) for _, ss in data.BRITISH_REGIONS + data.INDIAN_REGIONS for s in ss}

    def run(regions, items, farm_workers, subsistence, owner_of, doc, home, by_value=False):
        states = [s for _, ss in regions for s in ss]
        pop = {s: dump[str(s)]["pops"] for s in states}
        wf = {s: dump[str(s)]["pops_workforce"] for s in states}
        shares, peasants = split(items(pop), farm_workers, subsistence)
        rows = {s: state_rows(model, owner_of(s), shares[s], by_value) for s in states}
        for s in states:
            block = state_block(rows[s], doc, home, owner_of(s), wf[s], dump[str(s)]["arable_land"], 0 if by_value else peasants[s], by_value)
            write_block(state_file(s), block, "\t", rb"^[ \t]*history\s*=\s*\{", args.dry_run)
        return rows, peasants, pop, wf

    rows, peasants, pop, wf = run(data.BRITISH_REGIONS, data.british_items, data.BRITISH_FARM_WORKERS, data.BRITISH_SUBSISTENCE, lambda s: "ENG",
                                  "eng_economy.md", "history/countries/ENG - Britain.txt")
    uk = british_catalogue(model, rows, peasants, pop, wf, names)
    write_block(country_file("ENG"), uk, "\t", rb"^[ \t]*# Economy Techs", args.dry_run)

    owners = {s: start_owner(s) for _, ss in data.INDIAN_REGIONS for s in ss}
    rows, peasants, pop, wf = run(data.INDIAN_REGIONS, data.indian_items, data.INDIAN_FARM_WORKERS, data.INDIAN_SUBSISTENCE, owners.get,
                                  "raj_economy.md", "history/countries/RAJ - British Raj.txt", by_value=True)
    gdp = sum(dump[str(s)].get("gdp_amount", 0) for s in owners)
    raj = indian_catalogue(model, rows, pop, wf, owners, names, gdp)
    write_block(country_file("RAJ"), raj, "\t", rb"^[ \t]*#Economy", args.dry_run)
    for tag in sorted(set(owners.values()) - {"RAJ"}):
        held = [s for s in owners if owners[s] == tag]
        write_block(country_file(tag), tag_block(tag, in_region(held, rows), held, names), "", None, args.dry_run)

    if args.dry_run:
        print("\n".join(uk + raj))


if __name__ == "__main__":
    main()
