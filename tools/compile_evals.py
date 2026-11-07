#!/usr/bin/env python3
"""Compile skill eval specs into agent-skills-eval assertions.

Source of truth:  skills/<id>/evals/spec.json   (structured checks — edit this)
Generated output: skills/<id>/evals/evals.json  (string assertions — never hand-edit)

Pattern adopted from hedera-dev/hedera-skills (scripts/compile-evals.mjs),
ported to stdlib Python to match this repo's tooling. Extra check types:
`absent` (output must NOT contain value) and `rubric` (judge-only check).

Usage (from repo root):
  python3 tools/compile_evals.py            # write evals.json for every spec
  python3 tools/compile_evals.py --check    # CI/pre-push: fail if any evals.json is stale
  python3 tools/compile_evals.py --skill analyst-house-style

Runs automatically as the first step of tools/build.py.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TYPES = {"contains", "regex", "absent", "rubric"}


def rubric_for(check: dict, where: str) -> str:
    if check.get("rubric", "").strip():
        return check["rubric"].strip()
    t, value, desc = check["type"], check.get("value", ""), check.get("description", "").strip()
    if t == "contains":
        return f"The output includes {value}: {desc}" if desc else f"The output includes {value}"
    if t == "absent":
        return f"The output does NOT contain {value!r}: {desc}" if desc else f"The output does NOT contain {value!r}"
    if t == "regex":
        return f"The output satisfies: {desc}" if desc else f"The output matches the expected pattern ({check['name']})"
    raise SystemExit(f"{where}: check '{check['name']}' of type 'rubric' needs a rubric string")


def compile_spec(spec_path: Path) -> dict:
    raw = json.loads(spec_path.read_text())
    rel = spec_path.relative_to(ROOT)
    if not raw.get("skill_name") or not isinstance(raw.get("evals"), list):
        raise SystemExit(f"{rel} must contain skill_name and evals[]")
    if raw["skill_name"] != spec_path.parent.parent.name:
        raise SystemExit(f"{rel}: skill_name '{raw['skill_name']}' does not match folder '{spec_path.parent.parent.name}'")
    out = {"skill_name": raw["skill_name"], "evals": []}
    for i, case in enumerate(raw["evals"]):
        where = f"{rel} evals[{i}]"
        checks = case.get("checks")
        if not isinstance(checks, list) or not checks or not case.get("prompt"):
            raise SystemExit(f"{where} needs a prompt and a non-empty checks[]")
        for c in checks:
            if not c.get("name") or c.get("type") not in TYPES:
                raise SystemExit(f"{where}: invalid check {c!r} (type must be one of {sorted(TYPES)})")
        out["evals"].append({
            "id": case.get("id", i),
            "prompt": case["prompt"],
            "expected_output": case.get("expected_output", ""),
            "files": case.get("files", []),
            "assertions": [rubric_for(c, where) for c in checks],
        })
    if raw.get("defaults"):
        out["defaults"] = raw["defaults"]
    return out


def main() -> int:
    args = sys.argv[1:]
    check_only = "--check" in args
    only = args[args.index("--skill") + 1] if "--skill" in args else None
    specs = sorted((ROOT / "skills").glob("*/evals/spec.json"))
    if only:
        specs = [s for s in specs if s.parent.parent.name == only]
    if not specs:
        print("evals: no specs found")
        return 0
    stale = 0
    for spec in specs:
        target = spec.with_name("evals.json")
        text = json.dumps(compile_spec(spec), indent=2, ensure_ascii=False) + "\n"
        rel = target.relative_to(ROOT)
        if check_only:
            if not target.exists() or target.read_text() != text:
                print(f"✗ {rel} is missing or stale (run: python3 tools/compile_evals.py)")
                stale += 1
            else:
                print(f"✓ {rel}")
        else:
            target.write_text(text)
            print(f"compiled {spec.relative_to(ROOT)} -> {rel}")
    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())
