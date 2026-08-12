#!/usr/bin/env python3
"""SessionStart hook: inject the covenant/routing manifest into session context.

Stdout from a SessionStart hook is added to the model's context. Keep the
manifest short — this runs every session. Edit ~/.claude/gate/manifest.md to
change what gets injected; kill with SESSION_GATE_DISABLE=1.
"""
import os
import sys
from pathlib import Path

DEFAULT = """== SESSION PROTOCOL (injected by session-gate) ==
Before substantive multi-step work: (1) consult the skills-dispatcher for routing;
(2) run model-delegation triage (band, risk, delegate); (3) check applicable
covenants (CLAUDE.md invariants, matter/client rules); (4) record the gate:
substantive edits are blocked until `gate.py` runs for this session.
Delegated subagents execute — they do not re-triage or sub-spawn.
"""

def main() -> int:
    if os.environ.get("SESSION_GATE_DISABLE") == "1":
        return 0
    manifest = Path.home() / ".claude" / "gate" / "manifest.md"
    try:
        text = manifest.read_text() if manifest.exists() else DEFAULT
    except OSError:
        text = DEFAULT
    sys.stdout.write(text.strip() + "\n")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # fail-open
        sys.stderr.write(f"session-gate/session_start: {exc}; failing OPEN\n")
        sys.exit(0)
