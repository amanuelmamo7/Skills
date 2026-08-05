#!/usr/bin/env python3
"""Sync contracts_taxonomy.json into contract_anatomy.html and verify integrity.

Usage:
    python3 sync_data.py [taxonomy.json] [game.html]

Defaults assume the skill layout: references/contracts_taxonomy.json and
assets/contract_anatomy.html relative to the skill root (parent of scripts/).

What it does:
  1. Validates the taxonomy JSON (parses, required fields, tag values).
  2. Checks every contract type has >=2 universal and >=1 signature headings
     (the quiz builds its clue ladder from these; fewer breaks rounds).
  3. Re-embeds the JSON into the HTML's `const DATA = ...;` block.
  4. Updates the "N contract types, M headings" header line.
  5. Prints each type's nearest structural neighbors (Jaccard over concept
     keys) so a bad concept mapping is visible immediately.
"""
import json, re, sys
from pathlib import Path

def jaccard(a, b):
    A = {h["c"] for h in a["headings"]}
    B = {h["c"] for h in b["headings"]}
    return len(A & B) / len(A | B)

def main():
    root = Path(__file__).resolve().parent.parent
    json_path = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "references/contracts_taxonomy.json"
    html_path = Path(sys.argv[2]) if len(sys.argv) > 2 else root / "assets/contract_anatomy.html"

    data = json_path.read_text()
    d = json.loads(data)  # raises on invalid JSON
    contracts = d["contracts"]
    errors = []
    ids = set()
    for c in contracts:
        for field in ("id", "name", "family", "blurb", "sources", "headings"):
            if field not in c:
                errors.append(f"{c.get('id','?')}: missing field '{field}'")
        if c["id"] in ids:
            errors.append(f"duplicate id: {c['id']}")
        ids.add(c["id"])
        tags = {"u": 0, "s": 0, "x": 0}
        for h in c["headings"]:
            if h.get("tag") not in tags:
                errors.append(f"{c['id']}: bad tag {h.get('tag')!r} on '{h.get('t')}'")
            else:
                tags[h["tag"]] += 1
            if not h.get("c"):
                errors.append(f"{c['id']}: missing concept key on '{h.get('t')}'")
        if tags["u"] < 2 or tags["x"] < 1:
            errors.append(f"{c['id']}: clue shortage {tags} (need >=2 u, >=1 x for the quiz)")
    if errors:
        print("FAILED integrity checks:")
        for e in errors:
            print("  -", e)
        sys.exit(1)

    n_types = len(contracts)
    n_head = sum(len(c["headings"]) for c in contracts)

    html = html_path.read_text()
    new_html, n = re.subn(r"const DATA = [\s\S]*?;\n\nconst C",
                          "const DATA = " + data.strip() + ";\n\nconst C", html, count=1)
    if n != 1:
        print("FAILED: could not locate `const DATA = ...;` block in HTML")
        sys.exit(1)
    m = re.search(r"\d+ contract types, \d+ headings", new_html)
    if m:
        new_html = new_html.replace(m.group(0), f"{n_types} contract types, {n_head} headings")
    html_path.write_text(new_html)
    print(f"OK: {n_types} types, {n_head} headings embedded into {html_path.name}")

    for c in contracts:
        sims = sorted(((jaccard(c, o), o["name"]) for o in contracts if o["id"] != c["id"]), reverse=True)[:2]
        print(f"  {c['name']:<40} nearest: " + ", ".join(f"{name} {round(v*100)}%" for v, name in sims))

if __name__ == "__main__":
    main()
