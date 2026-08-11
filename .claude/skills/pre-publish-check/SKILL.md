---
name: pre-publish-check
description: Pre-push gate for the skills library — privacy sweep, rebuild, and generated-files sync check in one command. Run before every push.
disable-model-invocation: true
---

# Pre-Publish Check

Run the full pre-push gate, in order. **Stop at the first failure** — report it and do not
continue to later steps. A gate that warns is not a gate.

## Steps

1. **Privacy sweep**
   ```bash
   python3 tools/privacy_sweep.py
   ```
   Non-zero exit = hard stop. Report the flagged content verbatim so it can be fixed.

2. **Rebuild generated artifacts**
   ```bash
   python3 tools/build.py
   ```

3. **Generated-files sync check** — prove the committed artifacts match index.json:
   ```bash
   git status --porcelain plugins/ graph.html README.md skills/skills-dispatcher/SKILL.md
   ```
   Any output = generated files were stale (or hand-edited). Report which files changed.
   The fresh build output is the correct version — stage it. If the diff looks like a
   hand-edit being reverted, say so explicitly before staging anything.

4. **Manifest pin check** — every third-party skill in index.json has a manifest.json
   entry with a pinned commit. Report any missing pins.

5. **Report** — one line per step, PASS/FAIL, then overall verdict:
   `READY TO PUSH` or `BLOCKED: <first failing step>`.

## Rules

- Never "fix" a privacy-sweep failure by deleting the check or narrowing the sweep.
- Never push on the user's behalf — this skill gates; the user pushes.
