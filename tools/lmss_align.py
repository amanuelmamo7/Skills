#!/usr/bin/env python3
"""Resolve SALI LMSS tags in index.json against the actual LMSS ontology.

Skill nodes may carry an `lmss` list of alignment entries:

    "lmss": [
      {"facet": "Area of Law",
       "query": ["Contract Review", "Contracts Law"],
       "label": null, "iri": null, "status": "unresolved"}
    ]

`query` holds candidate labels (best guess first). This tool downloads the
LMSS OWL, builds a label -> IRI map from its classes (rdfs:label + altLabels),
and resolves each entry to a real label + IRI. Verify-before-trust: an entry
that doesn't match a real LMSS concept stays "unresolved" and is NEVER
rendered by the build tools — proposed tags cannot masquerade as standard ones.

Usage (from repo root):
    python3 tools/lmss_align.py                    # download + resolve
    python3 tools/lmss_align.py --file LMSS.owl    # use a local copy
    python3 tools/lmss_align.py --report           # show current status only

After resolving, run `python3 tools/build.py` to propagate tags into the
README and dispatcher.
"""

import argparse
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LMSS_URL = "https://raw.githubusercontent.com/sali-legal/LMSS/main/LMSS.owl"

NS = {
    "owl": "http://www.w3.org/2002/07/owl#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
}


def load_labels(owl_path: Path) -> dict[str, tuple[str, str]]:
    """Return lowercased label -> (canonical rdfs:label, IRI)."""
    labels: dict[str, tuple[str, str]] = {}
    tree = ET.parse(owl_path)
    for cls in tree.getroot().iter(f"{{{NS['owl']}}}Class"):
        iri = cls.get(f"{{{NS['rdf']}}}about")
        if not iri:
            continue
        canonical = None
        names = []
        for tag in ("rdfs:label", "skos:prefLabel", "skos:altLabel"):
            pre, local = tag.split(":")
            for el in cls.findall(f"{{{NS[pre]}}}{local}"):
                if el.text and el.text.strip():
                    names.append(el.text.strip())
                    if canonical is None and tag != "skos:altLabel":
                        canonical = el.text.strip()
        if canonical is None and names:
            canonical = names[0]
        for n in names:
            labels.setdefault(n.lower(), (canonical, iri))
    return labels


def resolve(entry: dict, labels: dict) -> str:
    for q in entry.get("query", []):
        hit = labels.get(q.lower())
        if hit:
            entry["label"], entry["iri"], entry["status"] = hit[0], hit[1], "resolved"
            return f"resolved  -> {hit[0]}"
    # substring pass REPORTS candidates only — never auto-resolves (a substring
    # hit once matched an absurd concept; exact label match is the only trust path)
    for q in entry.get("query", []):
        subs = sorted({c for k, (c, i) in labels.items() if q.lower() in k})
        if subs:
            return f"candidates for '{q}': {subs[:6]} — put the right one in query[0]"
    return "NO MATCH — refine query or drop the entry"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", help="local LMSS.owl instead of downloading")
    ap.add_argument("--url", default=LMSS_URL)
    ap.add_argument("--report", action="store_true", help="status only, no resolving")
    args = ap.parse_args()

    idx_path = ROOT / "index.json"
    idx = json.loads(idx_path.read_text())
    tagged = [n for n in idx["nodes"] if n.get("type") == "skill" and n.get("lmss")]
    if not tagged:
        print("no lmss entries in index.json")
        return 0

    if args.report:
        for n in tagged:
            for e in n["lmss"]:
                print(f"{n['id']:32s} {e.get('facet','?'):16s} {e.get('status')}: {e.get('label') or e.get('query')}")
        return 0

    if args.file:
        owl = Path(args.file)
    else:
        owl = ROOT / ".lmss-cache.owl"
        if not owl.exists():
            print(f"downloading {args.url} ...")
            urllib.request.urlretrieve(args.url, owl)
    labels = load_labels(owl)
    print(f"LMSS classes with labels loaded: {len(labels)}")

    unresolved = 0
    for n in tagged:
        for e in n["lmss"]:
            if e.get("status") == "resolved":
                continue
            msg = resolve(e, labels)
            if e.get("status") != "resolved":
                unresolved += 1
            print(f"{n['id']:32s} {e.get('facet','?'):16s} {msg}")

    idx_path.write_text(json.dumps(idx, indent=2))
    print(f"\nwritten. unresolved entries: {unresolved} (unresolved tags are never rendered)")
    print("next: python3 tools/build.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
