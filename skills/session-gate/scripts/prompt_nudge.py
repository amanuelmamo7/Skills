#!/usr/bin/env python3
"""UserPromptSubmit hook: one-line gate reminder that SELF-SILENCES once the
session is gated — zero noise after compliance, fresh reminder each turn before.

Stdout is added to context. Kill with SESSION_GATE_DISABLE=1.
"""
import json
import os
import sys
from pathlib import Path


def main() -> int:
    if os.environ.get("SESSION_GATE_DISABLE") == "1":
        return 0
    data = json.load(sys.stdin)
    session = data.get("session_id", "")
    state = Path.home() / ".claude" / "gate" / "state" / f"{session}.json"
    if session and state.exists():
        return 0  # gated — say nothing
    sys.stdout.write(
        f"[gate] No triage recorded (session id: {session or 'unknown'}). If this "
        "turn starts substantive multi-step work, run the session gate first "
        "(dispatcher -> model-delegation -> covenants -> gate.py, or the "
        "begin-task skill). Trivial/conversational turns: proceed.\n"
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # fail-open
        sys.stderr.write(f"session-gate/prompt_nudge: {exc}; failing OPEN\n")
        sys.exit(0)
