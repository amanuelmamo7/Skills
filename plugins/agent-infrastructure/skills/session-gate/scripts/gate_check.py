#!/usr/bin/env python3
"""PreToolUse hook: block substantive file edits until session triage is recorded.

Fail-open by design: any internal error warns and exits 0 — this gate must never
be the thing that breaks a session. Kill switch: SESSION_GATE_DISABLE=1 (must be
set in the environment that LAUNCHES claude — hooks inherit the parent process
env, not a tool call's shell).

Matcher (set in settings.json): Edit|Write|MultiEdit|NotebookEdit plus MCP write
tools. Bash is deliberately NOT gated: the gate script itself runs via Bash, and
gating Bash deadlocks the unblock path.

Gate-dir protection: writes into ~/.claude/gate/ via edit tools are ALWAYS
blocked — state is written only by gate.py (via Bash) and manifest.md is
human-edited only. This prevents the model from unblocking itself or planting
persistent context injection without a log entry.
"""
import datetime
import json
import os
import re
import sys
from pathlib import Path

GATE_DIR = Path.home() / ".claude" / "gate"
STATE_DIR = GATE_DIR / "state"
LOG = GATE_DIR / "gate-log.jsonl"
SETTINGS_PROPOSED = str(Path.home() / ".claude" / "settings.json.proposed")


def clean_session(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]", "", s or "")


def log_blocked(session: str, tool: str, path: str) -> None:
    try:
        GATE_DIR.mkdir(parents=True, exist_ok=True)
        with LOG.open("a") as f:
            f.write(json.dumps({
                "blocked": True, "tool": tool, "file": Path(path).name,
                "session": session,
                "ts": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
            }) + "\n")
    except OSError:
        pass  # blocked-attempt logging is best-effort


def main() -> int:
    if os.environ.get("SESSION_GATE_DISABLE") == "1":
        return 0
    data = json.load(sys.stdin)
    session = clean_session(data.get("session_id", ""))
    tool = data.get("tool_name", "")
    path = str(data.get("tool_input", {}).get("file_path", ""))

    # Exact-path allow: the installer's own staging file only.
    if path == SETTINGS_PROPOSED:
        return 0

    # Deny always: the gate's own directory (state via gate.py/Bash only;
    # manifest.md human-edited only — it is injected into every session).
    try:
        if path and Path(path).expanduser().resolve().is_relative_to(GATE_DIR):
            sys.stderr.write(
                "SESSION GATE: files under ~/.claude/gate/ are not editable by "
                "tools — state is written by gate.py, manifest.md by the human.\n")
            return 2
    except (OSError, ValueError):
        pass

    if session and (STATE_DIR / f"{session}.json").exists():
        return 0

    log_blocked(session, tool, path)
    sys.stderr.write(
        "SESSION GATE: no triage recorded for this session — substantive edits "
        "are blocked until Phase 0 runs.\n"
        "First: consult the skills-dispatcher and model-delegation skills (the "
        "begin-task skill walks the full ritual). Then record it:\n"
        f"  python3 \"$HOME/.claude/gate/gate.py\" --session {session or 'UNKNOWN'} "
        "--category <build|research|legal|market|ops|writing> --band "
        "<ROUTINE|STANDARD|COMPLEX|FRONTIER> --risk <LOW|HIGH> "
        "--skills '<skills actually consulted>'\n"
        "A --skip path exists for genuinely trivial sessions; skips and blocked "
        "attempts are both logged and audited weekly — a dodged gate is visible.\n"
    )
    return 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # fail-open, loudly
        sys.stderr.write(f"session-gate: internal error ({exc}); failing OPEN\n")
        sys.exit(0)
