#!/usr/bin/env python3
"""Session gate: record Phase-0 triage for a session, or report on the gate log.

Record mode writes ~/.claude/gate/state/<session>.json (unblocks gate_check.py)
and appends an auditable JSONL line to ~/.claude/gate/gate-log.jsonl.
Anti-boilerplate: args are validated for substance, not just presence — the
weekly audit (--report) then reviews quality.
"""
import argparse
import datetime
import re
import json
import os
import sys
from collections import Counter
from pathlib import Path

GATE_DIR = Path.home() / ".claude" / "gate"
STATE_DIR = GATE_DIR / "state"
LOG = GATE_DIR / "gate-log.jsonl"

CATEGORIES = {"build", "research", "legal", "market", "ops", "writing"}
BANDS = {"TRIVIAL", "ROUTINE", "STANDARD", "COMPLEX", "FRONTIER"}
RISKS = {"LOW", "HIGH"}


def record(args) -> int:
    if args.skip:
        if len(args.skip.strip()) < 10:
            sys.stderr.write("gate: --skip reason too thin (>=10 chars) — say why it's trivial\n")
            return 1
        entry = {"skip": args.skip.strip()}
    else:
        problems = []
        if args.category not in CATEGORIES:
            problems.append(f"--category must be one of {sorted(CATEGORIES)}")
        if args.band not in BANDS:
            problems.append(f"--band must be one of {sorted(BANDS)}")
        if args.risk not in RISKS:
            problems.append("--risk must be LOW or HIGH")
        if args.band == "TRIVIAL":
            problems.append("TRIVIAL is the skip-floor band — use --skip with a reason instead")
        skills = [s.strip() for s in (args.skills or "").split(",") if s.strip()]
        if not skills:
            problems.append("--skills must name at least one consulted skill "
                            "(or 'none-applicable: <why>')")
        if problems:
            sys.stderr.write("gate: " + "; ".join(problems) + "\n")
            return 1
        entry = {"category": args.category, "band": args.band,
                 "risk": args.risk, "skills": skills}
    entry.update({
        "ts": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "session": args.session,
        "cwd": Path(os.getcwd()).name,  # basename only: full paths can carry client/matter names
    })
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    (STATE_DIR / f"{args.session}.json").write_text(json.dumps(entry, indent=1))
    with LOG.open("a") as f:
        f.write(json.dumps(entry) + "\n")
    # Housekeeping: drop state files older than 14 days (log is the durable record)
    cutoff = datetime.datetime.now().timestamp() - 14 * 86400
    for p in STATE_DIR.glob("*.json"):
        if p.stat().st_mtime < cutoff:
            p.unlink(missing_ok=True)
    kind = "SKIP" if args.skip else f"{entry['category']}/{entry['band']}/{entry['risk']}"
    print(f"gate: recorded [{kind}] for session {args.session} — edits unblocked")
    return 0


def report(days: int) -> int:
    if not LOG.exists():
        print("gate report: no log yet")
        return 0
    cutoff = datetime.datetime.now().astimezone() - datetime.timedelta(days=days)
    rows = []
    for line in LOG.read_text().splitlines():
        try:
            r = json.loads(line)
            ts = datetime.datetime.fromisoformat(r["ts"])
            if ts.tzinfo is None:  # hand-written entries may be naive — assume local
                ts = ts.astimezone()
            if ts >= cutoff:
                rows.append(r)
        except (json.JSONDecodeError, KeyError, ValueError, TypeError):
            continue
    blocked = [r for r in rows if r.get("blocked")]
    rows = [r for r in rows if not r.get("blocked")]
    skips = [r for r in rows if "skip" in r]
    gated = [r for r in rows if "skip" not in r]
    blocked_sessions = {r.get("session") for r in blocked}
    gated_sessions = {r.get("session") for r in rows}
    never_gated = blocked_sessions - gated_sessions - {""}
    print(f"gate report — last {days}d: {len(rows)} sessions gated "
          f"({len(gated)} triaged, {len(skips)} skipped); "
          f"{len(blocked)} blocked attempts across {len(blocked_sessions)} sessions")
    if never_gated:
        print(f"  NON-COMPLIANCE: {len(never_gated)} session(s) hit the gate and never gated — "
              "the number that says whether the gate works")
    if gated:
        print("  categories:", dict(Counter(r["category"] for r in gated)))
        print("  bands:     ", dict(Counter(r["band"] for r in gated)))
        print("  risk:      ", dict(Counter(r["risk"] for r in gated)))
        skill_counts = Counter(s for r in gated for s in r.get("skills", []))
        print("  skills consulted:", dict(skill_counts.most_common(10)))
    # Quality flags for the weekly audit (Goodhart watch)
    flags = []
    if rows and len(skips) / len(rows) > 0.5:
        flags.append(f"skip rate {len(skips)}/{len(rows)} — skip-floor may be miscalibrated or gate is being dodged")
    reasons = Counter(r["skip"] for r in skips)
    for reason, n in reasons.items():
        if n >= 3:
            flags.append(f"repeated identical skip reason x{n}: '{reason}' — boilerplate suspect")
    skill_lists = Counter(tuple(r.get("skills", [])) for r in gated)
    for combo, n in skill_lists.items():
        if n >= 5:
            flags.append(f"identical skills-list x{n}: {list(combo)} — copy-paste triage suspect")
    print("  quality flags:" if flags else "  quality flags: none")
    for fl in flags:
        print("   -", fl)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--session", help="session id (from the gate block message)")
    ap.add_argument("--category")
    ap.add_argument("--band")
    ap.add_argument("--risk")
    ap.add_argument("--skills", help="comma-separated skills consulted")
    ap.add_argument("--skip", help="one-line reason this session is trivial")
    ap.add_argument("--report", action="store_true", help="summarize the gate log")
    ap.add_argument("--days", type=int, default=7)
    args = ap.parse_args()
    if args.report:
        return report(args.days)
    if not args.session:
        ap.error("--session is required (shown in the gate block message and the per-turn nudge)")
    args.session = re.sub(r"[^A-Za-z0-9_-]", "", args.session)
    if not args.session:
        ap.error("--session contained no valid characters")
    return record(args)


if __name__ == "__main__":
    sys.exit(main())
