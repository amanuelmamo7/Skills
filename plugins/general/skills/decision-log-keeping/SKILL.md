---
name: decision-log-keeping
description: Maintain a DECISIONS.md architectural decision log with LOCKED/PROPOSED/OPEN statuses, append-only history, and section numbering. Use whenever a project needs durable records of structural decisions that code and docs can cite.
---

# Decision Log Keeping

Keep every structural decision in a single `DECISIONS.md` at the repo root. It is the running memory of the project — the file a future reviewer, a fresh AI session, or you-in-six-months reads to understand why things are the way they are.

## File header (copy this convention)

Open the file with a "How to use this file" block stating:
- Every structural decision lives here.
- Each entry carries a status: **LOCKED** (approved — do not change without re-opening), **PROPOSED** (recommendation awaiting owner approval), or **OPEN** (question not yet answered).
- When a decision changes, **do not edit history** — append a new dated section below the old one and update the status.

## Entry structure

Number sections (`## 1.`, `## 2.` … with subsections `§21.4` style) and never renumber. Each entry follows:

```
## N. Topic (Rule X if it maps to a house rule) — STATUS

**Proposal / Decision.** The concrete choice, stated so it can be executed.

**Alternatives.** 2–3 rejected options, each with a one-line reason.

**Why.** The trade-off reasoning, honestly including what was given up.

**Owner note (YYYY-MM-DD).** The approval, plus any conditions
("approved for now; revisit with the Phase 2 reviewer").
```

Include concrete implications ("this means the free tier caps at X; budget the upgrade in week 8") — a decision log that omits consequences forces re-derivation later.

## The append-don't-edit discipline

- **Amending**: preserve the locked text; add a dated `*Amendment (YYYY-MM-DD, §N):*` block beneath it describing what changed and why. Never silently rewrite.
- **Superseding**: the old section keeps its number and text; the new section states "supersedes §N" and the old one gains a one-line pointer forward.
- **Locking**: a PROPOSED entry becomes LOCKED only with an explicit dated owner note. "Looks reasonable" in a review counts; silence does not.

## How decisions get cited

- Code comments cite `§N` ("per DECISIONS.md §21.4") so a reader can trace any non-obvious choice to its rationale.
- Other contract docs (deferred-work register, runbook, cost budgets) name their source-of-truth section explicitly.
- When an audit finds a citation to a section that doesn't exist or was renumbered, that's a finding — stale references mislead the next reader.

## Cadence and hygiene

- Append the end-of-session structural-decisions summary from each AI build session.
- One dated section per decision, even small ones (a dependency choice, a tier cap) — the small ones are what you forget.
- Quarterly: re-read for drift against the codebase and the other contract docs.
- The file will get large. That's fine — it's append-only history. Navigate by section number, not by reading linearly.

## Anti-patterns

- Editing a LOCKED entry in place (destroys the audit trail).
- Recording the decision without the rejected alternatives (the alternatives are what stop you re-litigating).
- Decisions living only in chat transcripts or commit messages.
- Renumbering sections during cleanup (breaks every citation in code and docs).
