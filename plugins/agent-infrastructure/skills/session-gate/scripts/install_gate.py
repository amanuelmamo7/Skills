#!/usr/bin/env python3
"""Installer for the session gate: copies scripts to ~/.claude/gate/ and merges
hook entries into GLOBAL ~/.claude/settings.json via a proposed-diff gate.

Global on purpose: project-level .claude/settings.json in a public repo ships
hooks to whoever clones it. Idempotent: existing session-gate entries are
replaced, never duplicated. Backup written before any apply.

Usage:
  python3 install_gate.py            # propose: writes settings.json.proposed + prints diff
  python3 install_gate.py --apply    # apply the proposal (backs up settings.json first)
  python3 install_gate.py --remove   # propose removal of all session-gate entries
  python3 install_gate.py --remove --apply
"""
import argparse
import difflib
import json
import shutil
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent
GATE_DIR = Path.home() / ".claude" / "gate"
SETTINGS = Path.home() / ".claude" / "settings.json"
MARKER = "/.claude/gate/"  # identifies our hook commands
SCRIPTS = ["gate.py", "gate_check.py", "session_start.py", "prompt_nudge.py"]

HOOK_ENTRIES = {
    "PreToolUse": {
        "matcher": "Edit|Write|MultiEdit|NotebookEdit|mcp__.+(write|edit|create|patch)",
        "hooks": [{"type": "command",
                   "command": 'python3 "$HOME/.claude/gate/gate_check.py"'}],
    },
    "SessionStart": {
        "hooks": [{"type": "command",
                   "command": 'python3 "$HOME/.claude/gate/session_start.py"'}],
    },
    "UserPromptSubmit": {
        "hooks": [{"type": "command",
                   "command": 'python3 "$HOME/.claude/gate/prompt_nudge.py"'}],
    },
}


def is_ours(entry) -> bool:
    return any(MARKER in h.get("command", "") for h in entry.get("hooks", []))


def build_proposal(remove: bool) -> tuple[str, str]:
    current = SETTINGS.read_text() if SETTINGS.exists() else "{}\n"
    try:
        cfg = json.loads(current)
    except json.JSONDecodeError as exc:
        sys.stderr.write(
            f"install_gate: {SETTINGS} is not valid JSON ({exc}) — it may contain "
            "comments or trailing commas. Fix it or merge the hook entries by hand "
            "per the session-gate SKILL.md; refusing to guess.\n")
        sys.exit(1)
    hooks = cfg.setdefault("hooks", {})
    for event, entry in HOOK_ENTRIES.items():
        kept = [e for e in hooks.get(event, []) if not is_ours(e)]
        hooks[event] = kept if remove else kept + [entry]
        if not hooks[event]:
            del hooks[event]
    if not cfg.get("hooks"):
        cfg.pop("hooks", None)
    proposed = json.dumps(cfg, indent=2) + "\n"
    return current, proposed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--remove", action="store_true")
    ap.add_argument("--purge-log", action="store_true",
                    help="on --remove, delete the audit log instead of archiving it")
    args = ap.parse_args()

    current, proposed = build_proposal(remove=args.remove)
    if current == proposed:
        print("install_gate: settings already in desired state (idempotent no-op)")
        if not args.apply:
            return 0
    diff = "".join(difflib.unified_diff(
        current.splitlines(keepends=True), proposed.splitlines(keepends=True),
        fromfile="settings.json", tofile="settings.json.proposed"))
    prop_path = SETTINGS.with_suffix(".json.proposed")

    if not args.apply:
        prop_path.parent.mkdir(parents=True, exist_ok=True)
        prop_path.write_text(proposed)
        print(diff or "(no settings change)")
        print(f"\nProposal written to {prop_path}")
        print("Review the diff above, then re-run with --apply to install"
              + (" the REMOVAL." if args.remove else "."))
        return 0

    # Apply: scripts first (or cleanup on remove), then settings with backup
    if args.remove:
        if GATE_DIR.exists():
            log = GATE_DIR / "gate-log.jsonl"
            if log.exists() and not args.purge_log:
                import datetime as _dt
                keep = Path.home() / ".claude" / f"gate-log.archived.{_dt.date.today()}.jsonl"
                shutil.copy2(log, keep)
                print(f"audit log preserved at {keep} (use --purge-log to delete instead)")
            shutil.rmtree(GATE_DIR)
            print(f"removed {GATE_DIR}")
    else:
        GATE_DIR.mkdir(parents=True, exist_ok=True)
        (GATE_DIR / "state").mkdir(exist_ok=True)
        for s in SCRIPTS:
            shutil.copy2(SRC / s, GATE_DIR / s)
        manifest = GATE_DIR / "manifest.md"
        if not manifest.exists():
            manifest.write_text(
                "== SESSION PROTOCOL (injected by session-gate; human-edited only) ==\n"
                "Before substantive multi-step work: (1) consult the skills-dispatcher "
                "for routing; (2) run model-delegation triage (band, risk, delegate); "
                "(3) check applicable covenants (CLAUDE.md invariants, matter/client "
                "rules); (4) record the gate: substantive edits are blocked until "
                "gate.py runs for this session.\n"
                "Delegated subagents execute — they do not re-triage or sub-spawn.\n")
            print(f"manifest created: {manifest} (edit it to change what gets injected)")
        print(f"scripts installed to {GATE_DIR}")
    if SETTINGS.exists():
        shutil.copy2(SETTINGS, SETTINGS.with_suffix(".json.bak"))
        print(f"backup: {SETTINGS.with_suffix('.json.bak')}")
    SETTINGS.parent.mkdir(parents=True, exist_ok=True)
    SETTINGS.write_text(proposed)
    prop_path.unlink(missing_ok=True)
    print("settings.json updated. Restart claude for hooks to take effect.")
    if not args.remove:
        print("Kill switch: SESSION_GATE_DISABLE=1 must be set in the environment")
        print("  that LAUNCHES claude (e.g. `SESSION_GATE_DISABLE=1 claude`, or")
        print("  export it in your shell rc) — exporting inside a session's Bash")
        print("  tool does NOT reach the hook processes.")
        print("Note: the settings diff may look large if your settings.json was")
        print("  not 2-space-indented — the reformat is cosmetic; read the +/- on")
        print("  the hooks keys.")
        print("Verify: in a new session, ask for a file edit before gating — "
              "it should block with instructions. Then test a SUBAGENT edit "
              "the same way (inheritance must be verified, not assumed).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
