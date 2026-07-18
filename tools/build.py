#!/usr/bin/env python3
"""Rebuild everything generated from index.json, in order:

  1. skills-dispatcher SKILL.md    (build_dispatcher.py — must run BEFORE plugins)
  2. plugins/ + marketplace.json   (build_plugins.py)
  3. README bucket tables          (build_readme.py)
  4. graph.html                    (build_graph.py)

Run from the repo root after ANY change to index.json:

  python3 tools/build.py
"""

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

for script in ["build_dispatcher.py", "build_plugins.py", "build_readme.py", "build_graph.py"]:
    print(f"== {script} ==")
    result = subprocess.run([sys.executable, str(HERE / script)])
    if result.returncode != 0:
        sys.exit(result.returncode)
print("== all generated artifacts rebuilt ==")
