---
name: session-gate
description: Hard enforcement that skills, triage, and covenants are consulted before substantive work — a PreToolUse gate blocks file edits until Phase-0 triage is recorded, with session-start manifest injection and a self-silencing per-turn nudge. Use when the user says "install the session gate", "gate my sessions", "why is my edit blocked", "session gate report", or asks how to guarantee protocols are followed. Differentiator - model-delegation decides WHO executes; this skill enforces THAT the deciding happened; begin-task is the human-invoked ritual this gate verifies.
---

# Session Gate

Passive context (covenants, project files, even skill descriptions) has no
enforcement. This skill converts "the protocol should be followed" into mechanics:
substantive edits fail until triage is recorded. Design stance, in order: fail-open
(the gate must never be what breaks a session), auditable (every gate event is
logged for the weekly quality review), removable (one command, no residue).

## Architecture — five thin layers

| Layer | Mechanism | Enforcement |
|---|---|---|
| Injection | SessionStart hook injects `~/.claude/gate/manifest.md` | awareness, every session |
| Nudge | UserPromptSubmit hook, one line, self-silences once gated | awareness, per turn until compliance |
| **Hard gate** | PreToolUse on edit tools blocks until `gate.py` records triage | mechanical reminder with audited self-serve override |
| Ritual | the begin-task skill — human-invoked Phase-0 that ends by running `gate.py` | interface to the gate |
| Audit | `gate.py --report` — rates, categories, boilerplate/Goodhart flags | measurement, weekly (wire into your recurring self-audit routine) |

Deliberate limits: **Bash is not gated** (the gate script runs via Bash — gating it
deadlocks; file edits are the substantive surface). **The gate proves the ritual
ran, not that thinking happened** — arg validation blocks empty triage, and the
weekly report flags copy-paste patterns, but quality enforcement is the audit's
job, not the hook's. **Cowork sessions don't run these hooks** — coverage there is
the injected manifest via global instructions plus delegate-embedded protocol.

## Install (global, deliberately — never ship these hooks in a public repo)

Only on explicit user request — never as a side effect of loading this skill.
`--apply` mutates the user's global settings.json; the proposed-diff step is
mandatory, and the model stops at the proposal unless the user has already
approved applying it.

```bash
python3 scripts/install_gate.py            # writes settings.json.proposed + shows diff
python3 scripts/install_gate.py --apply    # backs up settings.json, applies, copies scripts
```

Idempotent: re-running replaces session-gate entries, never duplicates. Then
restart claude and verify BOTH of:

1. New session, request a file edit before gating → must block with instructions.
2. Ungated session, spawn a subagent that edits → must also block (inheritance).
3. **Gated parent, spawn a subagent that edits** → must PASS. If it blocks, the
   subagent carries a different session_id than the parent — delegation would
   break inside properly-gated sessions. Record which way this surface behaves;
   the delegate agent defs already handle the blocked case by escalating, never
   by running gate.py themselves (delegate-authored triage would pollute the log).
   All three outcomes go in the gate log by hand and into the weekly audit.

## Runtime behavior

Blocked edit → the error names the exact unblock command with the session id:

```bash
python3 "$HOME/.claude/gate/gate.py" --session <id> --category build \
  --band STANDARD --risk LOW --skills "skills-dispatcher, model-delegation"
# trivial sessions:
python3 "$HOME/.claude/gate/gate.py" --session <id> --skip "one-line-fix to README typo"
```

Args are validated for substance (enumerated category/band/risk, ≥1 named skill,
skip reasons ≥10 chars). Every event appends to `~/.claude/gate/gate-log.jsonl`.
State files expire after 14 days; the log is the durable record.

## Weekly audit (wire into your recurring self-audit routine)

```bash
python3 "$HOME/.claude/gate/gate.py" --report --days 7
```

Reports volume, category/band/risk mix, skills-consulted frequency, and quality
flags: skip-rate >50% (miscalibrated skip-floor or dodging), repeated identical
skip reasons, identical skills-lists ≥5× (copy-paste triage). Flags are Goodhart
tripwires — investigate them as compliance-theater evidence, not noise. Also scan
the log for client/matter names before any sync of `~/.claude/gate/` — the log is
privacy-sweep surface.

## Incident runbook

| Symptom | Diagnosis | Immediate mitigation | Recovery |
|---|---|---|---|
| Gate misbehaving mid-session (wrong blocks) | gate script bug or damaged state | quit claude; relaunch with `SESSION_GATE_DISABLE=1 claude` — the variable must be set in the environment that LAUNCHES claude; exporting inside a session's Bash tool does NOT reach hook processes | reinstall via `install_gate.py --apply`; file the incident in the gate log by hand (include a timezone offset in hand-written `ts` values) |
| Gate silently not firing at all | script exception — fail-open hides breakage | none needed in the moment | the tell is a silent weekly report during a working week; reinstall, check `python3 "$HOME/.claude/gate/gate_check.py" </dev/null` by hand |
| Edits pass without gating | hooks not loaded (no restart after install) or settings clobbered | check `grep gate "$HOME/.claude/settings.json"` | re-run installer; restart |
| Gate blocks mid-task after it was passed | state file expired mid-session (>14d session) or state dir wiped | re-run gate.py with same args | none needed |
| Subagent edits bypass gate (ungated parent) | inheritance not holding on this surface | rely on delegate templates' embedded protocol | log it; re-verify after surface updates |
| Delegate blocked inside a GATED session | subagent session_id differs from parent | delegate escalates per its def; orchestrator absorbs or re-spawns after verifying install step 3 | record the surface behavior; consider gating only until first pass if chronic |
| Warnings from two hook stacks collide confusingly | security-guidance + gate firing on same call | read both; gate's message always names gate.py | tune matchers if chronic |
| Nudge appears every turn despite gating | session_id mismatch between hooks | check state dir for the id in the nudge | re-run gate.py with the id the BLOCK message shows |

Uninstall: `install_gate.py --remove` then `--remove --apply` — removes hook
entries, scripts, state, and log. No other residue exists.

## What would make this skill wrong

- Claude Code changes hook events/semantics (PreToolUse matcher syntax, stdin
  schema, exit-2 behavior) — gate_check.py breaks first, fail-open hides it:
  the weekly report going silent is the tell
- Cowork gains project-hook parity — the coverage asymmetry note becomes stale
  and the gate should extend there
- Anthropic ships native protocol-enforcement or memory that supersedes injection
- Skip rate stays >50% for two consecutive audits — the skip-floor is wrong or
  the gate is friction-theater; recalibrate or remove rather than let it rot
- The session_id field disappears from hook stdin — state keying breaks

---

First-party. Composes with: model-delegation (the triage the gate demands),
begin-task (the ritual), your weekly audit routine (the report consumer),
skills-dispatcher (what the manifest points to).
