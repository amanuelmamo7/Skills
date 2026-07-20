#!/usr/bin/env python3
"""Pre-publish privacy sweep. Run before any push to the public remote:

  python3 tools/privacy_sweep.py

Exits non-zero if any pattern matches outside the allowlist, printing every hit.
Add new patterns the moment a category of leak is discovered — this file is the
distilled form of the 2026-07 pre-publication audit.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Things that must never appear in a public tree.
PATTERNS = [
    # live secrets (placeholders like your-api-key-here won't match)
    r"sk-[A-Za-z0-9]{20,}", r"ghp_[A-Za-z0-9]{20,}", r"xox[bp]-[A-Za-z0-9-]{10,}",
    r"AIza[A-Za-z0-9_\-]{30,}", r"AKIA[A-Z0-9]{16}",
    # personal endpoints / infra
    r"daily-brief-beta[a-z0-9\-]*\.vercel\.app", r"192\.168\.1\.79", r"tailscale",
    r"x-bari-token", r"bari-token\.txt",
    # personal data
    r"amanuelmamo7@gmail\.com",
    # skills deliberately kept private
    r"poker-hud-advisor", r"weekday-morning-brief", r"weekly-system-self-audit",
    r"daily-job-search-crawl",
]

# (path-substring, exact-pattern-or-*) pairs that are accepted.
ALLOW = [
    ("tools/privacy_sweep.py", "*"),            # this file lists the patterns
    ("PREP-NOTES.md", "*"),                     # branch review doc — deleted before merge
    (".claude-plugin/", r"amanuelmamo7@gmail\.com"),   # plugin author metadata — deliberate
    ("tools/build_plugins.py", r"amanuelmamo7@gmail\.com"),
]

SKIP_DIRS = {".git", "__pycache__", "node_modules"}
TEXT_EXT = {".md", ".json", ".py", ".sh", ".js", ".html", ".yml", ".yaml", ".txt"}

def allowed(rel: str, pat: str) -> bool:
    return any(sub in rel and (apat == "*" or apat == pat) for sub, apat in ALLOW)

def main() -> int:
    hits = 0
    for f in ROOT.rglob("*"):
        if not f.is_file() or f.suffix not in TEXT_EXT:
            continue
        if any(part in SKIP_DIRS for part in f.parts):
            continue
        rel = str(f.relative_to(ROOT))
        try:
            text = f.read_text(errors="ignore")
        except OSError:
            continue
        for pat in PATTERNS:
            for m in re.finditer(pat, text, re.I):
                if allowed(rel, pat):
                    continue
                line = text.count("\n", 0, m.start()) + 1
                print(f"LEAK  {rel}:{line}  [{pat}]  {m.group(0)[:60]}")
                hits += 1
    if hits:
        print(f"\n{hits} hit(s) — do not publish until resolved.")
        return 1
    print("privacy sweep: CLEAN")
    return 0

if __name__ == "__main__":
    sys.exit(main())
