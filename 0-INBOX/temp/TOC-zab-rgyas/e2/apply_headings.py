#!/usr/bin/env python3
"""Apply E2 placements (slice_NN.jsonl) to the commentary as headings.

Dry by default: writes the candidate to --output and a report to --report; never
touches the source. Proves that no prose changed (whitespace-insensitive) once
all inserted heading lines are removed.
"""
import argparse, glob, json, re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf8")

ap = argparse.ArgumentParser()
ap.add_argument("--source", required=True)
ap.add_argument("--tree", required=True)
ap.add_argument("--out-dir", required=True)
ap.add_argument("--output", required=True)
ap.add_argument("--report", required=True)
a = ap.parse_args()

# ---- tree ---------------------------------------------------------------
nodes = []
for l in open(a.tree, encoding="utf8").read().splitlines():
    m = re.match(r"\s*\* ([\d.]+)\s+(.*?)\s*$", l)
    if m:
        nodes.append((m.group(1).strip("."), m.group(2)))
order = {d: i for i, (d, _) in enumerate(nodes)}
title = dict(nodes)

# ---- placements ---------------------------------------------------------
pl = {}
for f in sorted(glob.glob(a.out_dir.rstrip("/\\") + "/slice_*.jsonl")):
    for ln in open(f, encoding="utf8"):
        ln = ln.strip()
        if ln:
            r = json.loads(ln)
            pl[r["id"]] = r

raw = open(a.source, encoding="utf8", newline="").read()
lines = raw.split("\n")


def heading(d):
    t = re.sub(r"[་\s]+$", "", title[d])
    t = re.sub(r"།+$", "", t) + "།"
    seg = d.count(".") + 1
    h = "#" * min(seg + 1, 6)
    if seg + 1 > 6:
        t = f"**{t}**"
    return f"{h} {t} ^{d.replace('.', '-')}-0"


problems = []  # (id, reason)
placed = []    # (order, id, li, pos)
for d, _ in nodes:
    r = pl.get(d)
    if r is None:
        problems.append((d, "no placement returned"))
        continue
    if r.get("status") != "placed":
        problems.append((d, "not_found: " + r.get("note", "")))
        continue
    li = r["line"] - 1
    snip = r["before"].replace("\xa0", " ")
    occ = int(r.get("occ", 1) or 1)
    found = None
    for delta in (0, -1, 1, -2, 2):  # tolerate off-by-one line numbers
        j = li + delta
        if not 0 <= j < len(lines):
            continue
        txt = lines[j].replace("\xa0", " ")
        pos, k = -1, 0
        while k < occ:
            pos = txt.find(snip, pos + 1)
            if pos < 0:
                break
            k += 1
        if pos >= 0:
            found = (j, pos)
            break
    if not found:
        problems.append((d, f"snippet not found near line {r['line']}: {r['before'][:30]}"))
        continue
    j, pos = found
    lead = len(lines[j]) - len(lines[j].lstrip())
    if pos <= lead:
        pos = 0
    placed.append((order[d], d, j, pos, r.get("conf", "")))

# ---- monotonicity -------------------------------------------------------
placed.sort()
bad = []
prev = (-1, -1)
for o, d, j, pos, c in placed:
    if (j, pos) < prev:
        bad.append((d, j + 1, pos, prev))
    prev = max(prev, (j, pos))
for d, j, pos, p in bad:
    problems.append((d, f"out of order: line {j} pos {pos} before previous {p[0]+1}:{p[1]}"))
bad_ids = {b[0] for b in bad}
placed = [p for p in placed if p[1] not in bad_ids]

# ---- apply --------------------------------------------------------------
by_line = {}
for o, d, j, pos, c in placed:
    by_line.setdefault(j, {}).setdefault(pos, []).append(d)

inserted_headings = set()
out = []
for j, l in enumerate(lines):
    if j not in by_line:
        out.append(l)
        continue
    cuts = sorted(by_line[j])
    start = 0
    for pos in cuts:
        frag = l[start:pos]
        if frag.strip():
            out.append(frag)
            out.append("")
        for d in by_line[j][pos]:
            h = heading(d)
            inserted_headings.add(h)
            out.append(h)
            out.append("")
        start = pos
    out.append(l[start:])

result = "\n".join(out)

# ---- proof: prose unchanged --------------------------------------------
stripped = [x for x in out if x not in inserted_headings]
ws = lambda s: re.sub(r"\s+", "", s)
ok = ws("".join(stripped)) == ws(raw)
n_expected = len(placed)
n_found = len(inserted_headings)

open(a.output, "w", encoding="utf8", newline="").write(result)

conf = {}
for o, d, j, pos, c in placed:
    conf[c] = conf.get(c, 0) + 1
rep = []
rep.append(f"nodes in tree: {len(nodes)}")
rep.append(f"headings inserted: {n_found} (expected {n_expected})")
rep.append(f"confidence: {conf}")
rep.append(f"prose preserved (whitespace-insensitive): {ok}")
rep.append(f"source lines {len(lines)} -> output lines {len(out)}")
rep.append(f"unplaced / problems: {len(problems)}")
for d, why in sorted(problems, key=lambda x: order[x[0]]):
    rep.append(f"  {d}\t{title[d]}\t{why}")
rep.append("")
rep.append("low-confidence placements:")
for o, d, j, pos, c in placed:
    if c == "low":
        rep.append(f"  {d}\tline {j+1}\t{pl[d].get('note','')}")
open(a.report, "w", encoding="utf8").write("\n".join(rep) + "\n")
print("\n".join(rep[:8]))
