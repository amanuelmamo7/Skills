# Standing Policy Block (Setup C)

Installs the delegation policy into the user's global CLAUDE.md (CLI:
`~/.claude/CLAUDE.md`; Cowork: global instructions). This is a persistent,
session-spanning behavior change — follow the procedure exactly. Install only on
explicit user request.

## Install procedure (proposed-diff gate — never a blind append)

1. **Idempotency check:** search the target file for `## Model delegation (standing
   policy)`. Present → already installed; offer the update path below instead of
   appending a duplicate.
2. **Propose:** write the block to `<target>.proposed`, show the user the diff
   against the current file, and state in one line what the change does.
3. **Apply on approval only.** Then delete the `.proposed` file.
4. Tell the user the removal path (below) — an install without a known uninstall is
   incomplete.

**Update:** replace the existing block between its `## Model delegation (standing
policy)` header and the next `##` header (or EOF), via the same proposed-diff gate.

**Removal:** delete that same section. No other state exists.

## The block

---

## Model delegation (standing policy)

Scope: this policy binds the TOP-LEVEL session only. A subagent executing a
delegated spec does not re-triage and does not sub-spawn.

For any task expected to exceed ~3 steps or ~50 lines of output, load and follow the
`model-delegation` skill BEFORE executing: classify band and risk, delegate to the
cheapest capable tier per its registry, evaluate per its deterministic gate and
risk-tiered loop. Skip-floor per the skill — including: spec longer than the
expected diff, HIGH-risk with a large diff, and anything the user assigned to the
orchestrator by name — executes directly. Standing red flag (OR-trigger, any one
fires): orchestrator produced ROUTINE-band work 3+ consecutive turns → stop and
triage now. Close every delegated task with the skill's audit line (observables
only).

---

## Calibration

After roughly a week of real use, revisit the step/line thresholds against session
token data (explain-usage skill if installed, manual turn counts otherwise): raise
thresholds if triage overhead appears on small tasks; lower them if orchestrator
ROUTINE-drift persists.
