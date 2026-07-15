---
name: deferred-work-register
description: Maintain a DEFERRED.md register of consciously postponed work using the what / why-not-now / trigger-condition pattern. Use whenever scope is cut so the omission reads as a decision, not a gap.
---

# Deferred Work Register

Keep a `DEFERRED.md` at the repo root enumerating everything you have **deliberately chosen not to do yet** — so the choice doesn't read as "we forgot" when a future session, reviewer, or auditor looks at the codebase. It is one of the contract documents an external reviewer reads first.

## The three-field entry pattern

Every entry has the same three fields, always in this order:

```
## §Ref — Short name (owning workstream / follow-up context)

**What:** the concrete capability or fix being postponed, specific
enough that a stranger could pick it up.

**Why deferred:** why it is not in scope *now* — usually "the seam
exists, this is wiring not redesign," "additive convenience, not a
blocker," or "premature before X exists." Name what makes deferral
safe today (graceful degradation, a documented workaround, low scale).

**Trigger:** the concrete condition under which it gets picked up —
an event ("the second customer onboards", "5+ migrations exist",
"first pen-test gap"), never a date-you'll-ignore or "someday."
```

Optionally add **What lands at trigger:** — the concrete artifacts to build when the trigger fires (schema, UI, tests, doc updates) — so activation doesn't require re-scoping from scratch.

## Lifecycle rules

- **When you defer something**: add an entry here, in the same commit as the work that skipped it. Cross-reference the decision-log section (`§N`) that made the call.
- **When you pick something up**: delete the entry here and capture the activation in the decision log with a dated section. The register holds only *live* deferrals.
- **When a trigger fires early**: strike through the heading, mark `RESOLVED YYYY-MM-DD (§N)`, and note in one paragraph what actually happened — especially if the resolution went further than the entry anticipated. Prune these on the next bookkeeping pass.

## Writing good triggers

A trigger must be observable without judgment calls:
- Good: "the first partner that needs to build requests dynamically, or the second partner onboarding, whichever comes first."
- Good: "executions exceed 60% of the free-tier quota in any month."
- Bad: "when we have time," "post-launch," "if it becomes a problem" (a problem detected by whom, how?).

Pair risk-accepting deferrals (security hardening, per-user salts, RLS) with the compensating control that makes deferral tolerable, and make audits re-test that the control still holds.

## Why this file earns its keep

- **Audits gate on it**: a finding of "X is missing" is answered by either fixing X or adding a register entry with an explicit trigger. "Missing and undocumented" is the only failing state.
- **It prevents scope creep in both directions**: nothing half-built "just in case," and nothing silently dropped.
- **It's the honest ledger for reviewers**: a security reviewer who sees a documented deferral with a sound trigger scores it very differently from an unexplained gap.

## Anti-patterns

- Deferrals recorded only in code comments or chat.
- Entries without triggers (they become a graveyard).
- Deleting an entry when work lands without logging the activation anywhere.
- Letting the register contradict the decision log — reconcile on every bookkeeping pass.
