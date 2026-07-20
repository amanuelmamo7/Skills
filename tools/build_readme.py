#!/usr/bin/env python3
"""Regenerate the bucket tables in README.md from index.json.

index.json is the source of truth. This script rewrites everything between
the GENERATED-BUCKETS markers in README.md; hand-written prose outside the
markers is never touched.

Run from the repo root:  python3 tools/build_readme.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
START = "<!-- GENERATED-BUCKETS:START (run tools/build_readme.py — do not edit by hand) -->"
END = "<!-- GENERATED-BUCKETS:END -->"

BUCKET_NOTES = {
    "market-analysis": " (from Sefer)",
    "personal-assistant": " (from Bari + Cowork, plus reviewed third-party)",
    "web-application": " (third-party, from Agentic Awesome Skills — pinned `5e31f23`)",
    "agent-infrastructure": " (third-party AAS + distilled first-party)",
    "general": " (third-party AAS + distilled first-party)",
    "attorney-workflow": " (first-party, built with skill-distiller)",
    "dev-operations": " (distilled from StreamEZ project practice)",
    "software-architecture": " (third-party, from Agentic Awesome Skills — pinned `ee66a9b`)",
}

FLAG_WORDS = ("RUNS", "DELEGATED", "HIGH CONSEQUENCE", "unvetted", "supply-chain")


def main() -> None:
    index = json.loads((ROOT / "index.json").read_text())
    skills = [n for n in index["nodes"] if n["type"] == "skill"]

    buckets: dict[str, list[dict]] = {}
    for s in skills:
        for b in s.get("buckets", []):
            buckets.setdefault(b, []).append(s)

    lines = ["Buckets are metadata, not folders — a skill can live in more than one.", ""]
    lines += ["| Bucket | Skills | Status |", "|---|---:|---|"]
    ordered = sorted(buckets, key=lambda b: -len(buckets[b]))
    for b in ordered:
        lines.append(f"| {b} | {len(buckets[b])} | active |")
    for b in index.get("buckets", []):
        if b not in buckets:
            lines.append(f"| {b} | 0 | reserved |")
    lines.append("")

    for b in ordered:
        lines.append(f"### {b}{BUCKET_NOTES.get(b, '')}")
        lines += ["", "| Skill | Use it for |", "|---|---|"]
        for s in buckets[b]:
            desc = s["description"]
            if any(w in s.get("risk", "") for w in FLAG_WORDS):
                desc += " — ⚠ see manifest"
            lines.append(f"| [`{s['id']}`](skills/{s['id']}/SKILL.md) | {desc} |")
        lines.append("")

    readme_path = ROOT / "README.md"
    readme = readme_path.read_text()
    if START not in readme or END not in readme:
        raise SystemExit("README.md is missing the GENERATED-BUCKETS markers")
    head, rest = readme.split(START, 1)
    _, tail = rest.split(END, 1)
    readme_path.write_text(head + START + "\n" + "\n".join(lines) + END + tail)
    print(f"README.md: regenerated {len(ordered)} bucket sections, {len(skills)} skills")


if __name__ == "__main__":
    main()
