---
name: adversarial-fresh-context-audit
description: Run a monthly adversarial audit where multiple fresh-context AI agents independently check code against the project's rules and claimed milestones, with P0/P1/P2 findings gating milestone close. Use before closing any workstream or on a monthly cadence.
---

# Adversarial Fresh-Context Audit

Once a month — and always before declaring a workstream or milestone closed — run an audit by agents that carry **no prior conversation context**. The agents that built the code cannot audit it; they inherit its assumptions and remember its intentions instead of reading its reality.

## Method

1. **Spawn N independent agents** (three is a good default), each with a fresh context, each given the full repo plus the contract documents (house rules, decision log, deferred register, prior audits).
2. **Assign each a lane** so coverage is deliberate, not overlapping:
   - **Lane 1 — Rules vs. code**: every numbered house rule checked against the actual implementation. Evidence required for compliance claims.
   - **Lane 2 — Claims substantiation**: every LOCKED decision and every close-gate checklist item claimed as done. Find the artifact that proves it. "Docs say five integration tests exist" → count the test files.
   - **Lane 3 — Cross-doc consistency + recent-work quality**: stale references between documents (section numbers that don't exist, rule counts that drifted, plan text contradicting locked decisions), plus a quality read of the most recent changes.
3. **Instruct the agents to be adversarial**: their job is to find the reasons the milestone should NOT close. A clean report from a flattering auditor is worthless.
4. **Synthesize** the three reports into one findings document, deduplicated, severity-tagged.

## Severity taxonomy

- **P0** — ship blocker. Launch cannot proceed.
- **P1** — must be fixed **or** explicitly captured in the deferred register / a decision-log amendment before sign-off can credibly be written.
- **P2** — clean up in the next bookkeeping pass; doesn't block close.

Note the P1 definition: documentation is an acceptable resolution. The failing state is a gap that is neither fixed nor consciously owned.

## Findings document format

For each finding: an ID (F1, F2 …), severity, a one-line title, **Evidence** (file:line, quoted text — every claim traceable), and **Decision required** — the 2–3 concrete options with effort estimates ("(a) write the five tests, ~1 day; (b) move to the deferred register with trigger X, 15 minutes"). The auditor proposes; the owner decides.

Group findings: substantive (top of the pile) → bookkeeping (cheap, fix in one pass) → deferrals to echo into the register → minor/cosmetic.

## Gating the close

End the report with:
1. **Close-gate status table**: each gate criterion, its status (pass / partial / blocked), and which findings block it.
2. **Auditor verdict**: what is solid (say so explicitly — the perimeter that held), what is not closed, and the recommendation with an effort range ("close-eligible after F1–F3 are addressed by decision; 30 minutes if all defer, 1.5 days if built now").

The milestone closes only when every P0 is fixed and every P1 is fixed-or-documented, and the owner writes a dated sign-off entry in the decision log. Closing over open P1s is a credibility hit on the next audit — the next fresh-context agent will find the same gap plus the false claim.

## Characteristic catches (what this method finds that self-review misses)

- Claimed-but-nonexistent artifacts (tests, calendars, runbook sections).
- Enforcement that is client-side only while the audit trail records it as server-verified.
- Comments and docs that describe behavior the code explicitly does not have.
- Stale cross-references after renumbering or rule expansion.
- Compensating controls that quietly stopped compensating.

## Cadence

Monthly during active build; additionally at every workstream close. Keep each report as a dated file (`docs/AUDIT_YYYY-MM-DD.md`) so the next audit can verify the last one's findings were resolved.
