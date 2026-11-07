#!/usr/bin/env python3
"""Fail if any SKILL.md frontmatter isn't strict YAML (stdlib-only heuristic).

Claude Code parses frontmatter leniently, but strict parsers (e.g. the eval runner's
js-yaml) reject an unquoted value containing ': ' — such as 'Differentiator: ...'.
Quote those values with single quotes (escape ' as ''). Runs first in tools/build.py.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
bad = []
for f in sorted((ROOT / "skills").glob("*/SKILL.md")):
    m = re.match(r"^---\r?\n([\s\S]*?)\r?\n---", f.read_text())
    if not m:
        bad.append(f"{f.relative_to(ROOT)}: missing frontmatter")
        continue
    for line in m.group(1).splitlines():
        kv = re.match(r"^([A-Za-z_-]+):\s(.*)$", line)
        if kv and not kv.group(2).startswith(("'", '"', ">", "|", "[", "{")) and ": " in kv.group(2):
            bad.append(f"{f.relative_to(ROOT)}: unquoted '{kv.group(1)}' value contains ': '")
    dm = re.search(r"^description:\s*'?(.*?)'?$", m.group(1), re.M)
    if dm and len(dm.group(1).replace("''", "'")) > 1024:
        print(f"⚠ {f.relative_to(ROOT)}: description is {len(dm.group(1))} chars (agentskills.io limit 1024; strict eval runs will reject it)")
for b in bad:
    print("✗", b)
print(f"frontmatter: {'CLEAN' if not bad else str(len(bad)) + ' problem(s)'}")
sys.exit(1 if bad else 0)
