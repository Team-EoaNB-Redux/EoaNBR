"""Comment out the economy in the state history files, so the map starts as subsistence farming. See economy_rework/03.

    python toi/documentation/scripts/strip_state_economy.py toi/history/states [--keep-transport]

Comments out resource entries and every industry size, in place, so the old numbers stay readable.
--keep-transport leaves port_size and railway_size active. Engine buildings (arms_factory, industrial_complex, dockyard,
infrastructure, naval_base) and arable_land are never touched.
"""
import collections, glob, os, re, sys

SIZE_VAR = re.compile(r"set_variable\s*=\s*\{\s*(\w+)\s*=\s*-?[\d.]+\s*\}")
LINE_START = re.compile(r"^([^#\n]*)(set_variable\s*=\s*\{\s*\w+\s*=\s*-?[\d.]+\s*\})", re.M)
# Typos in the history files. They set nothing the economy reads, but they are still industry sizes.
BARE_SIZES = {"synthetic_oil_refinery", "tooling_workshop", "textile_mill", "rice_paddy", "entertainment_hub", "urban_center"}
RES_ENTRY = re.compile(r"\b\w+\s*=\s*-?[\d.]+")
RES_OPEN = re.compile(r"\bresources\s*=\s*\{")


def is_size(name, keep):
    return name not in keep and (name.endswith("_size") or name.endswith("_sizesize") or name in BARE_SIZES)


def split_comment(line):
    i = line.find("#")
    return (line, "") if i < 0 else (line[:i], line[i:])


def strip_text(text, keep, counts):
    # 45 sizes are written over several lines: put them on one so the pass below sees them
    def one_line(m):
        name = SIZE_VAR.search(m.group(2)).group(1)
        return m.group(1) + (re.sub(r"\s+", " ", m.group(2)) if is_size(name, keep) else m.group(2))

    text = LINE_START.sub(one_line, text)
    out = []
    in_res = False
    changed = False
    for raw in text.split("\n"):
        cr = raw.endswith("\r")
        line = raw[:-1] if cr else raw
        code, comment = split_comment(line)
        moved = []

        def take(m):
            moved.append(m.group(0))
            return ""

        def take_size(m):
            if not is_size(m.group(1), keep):
                return m.group(0)
            counts[m.group(1)] += 1
            moved.append(m.group(0))
            return ""

        if in_res or RES_OPEN.search(code):
            # Only what sits between this block's braces is a resource entry
            start = RES_OPEN.search(code).end() if not in_res else 0
            end = code.find("}", start)
            body = code[start:] if end < 0 else code[start:end]
            counts["resource entries"] += sum(float(m.group(0).split("=")[1]) != 0 for m in RES_ENTRY.finditer(body))
            new = code[:start] + RES_ENTRY.sub(take, body) + ("" if end < 0 else code[end:])
            in_res = end < 0
        else:
            new = SIZE_VAR.sub(take_size, code)

        if not moved:
            out.append(raw)
            continue
        changed = True
        if new.strip():
            line = new.rstrip() + " #" + " ".join(moved) + (" " + comment if comment else "")
        else:
            line = re.match(r"\s*", code).group(0) + "#" + code.strip() + (" " + comment if comment else "")
        out.append(line + ("\r" if cr else ""))
    return "\n".join(out), changed


def main():
    keep = {"port_size", "railway_size"} if "--keep-transport" in sys.argv else set()
    counts = collections.Counter()
    files = 0
    for p in glob.glob(os.path.join(sys.argv[1], "*.txt")):
        raw = open(p, "rb").read()
        bom = raw.startswith(b"\xef\xbb\xbf")
        # latin-1 round-trips every byte, and everything edited here is ASCII
        new, changed = strip_text((raw[3:] if bom else raw).decode("latin-1"), keep, counts)
        if changed:
            files += 1
            open(p, "wb").write((b"\xef\xbb\xbf" if bom else b"") + new.encode("latin-1"))
    print(f"{files} files changed")
    for k, v in counts.most_common():
        print(f"  {k:40}{v:6}")


if __name__ == "__main__":
    main()
