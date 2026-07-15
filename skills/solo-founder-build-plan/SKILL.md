---
name: solo-founder-build-plan
description: Structure a solo-founder, AI-assisted product build — contract-files discipline, a hard separation between build phase and expert review phase, and rules for when to buy senior-engineer time. Use when planning a months-long build with AI as the primary developer.
---

# Solo-Founder Build Plan

Plan the build as sequential phases with one defining separation: the **build phase** (founder + AI, cheap, fast) and the **review phase** (senior engineer + pen tester, paid, adversarial). The plan's job is to make the AI-built artifact reviewable — a disciplined paper trail is what converts "vibe-coded" into "auditable."

## Contract files — the artifacts that outlive the project

A small set of repo-root files is the single source of truth. The reviewer you eventually hire reads these first; their existence and quality is the signal you ran a disciplined build:

1. **SESSION_RULES.md** — the numbered structural-rules contract, loaded at the start of every AI session, updated as decisions lock.
2. **DECISIONS.md** — append-only log of every structural decision with LOCKED/PROPOSED/OPEN statuses and dated sections.
3. **DEFERRED.md** — everything consciously not done, with what / why-not-now / trigger fields.
4. **FEEDBACK.md** — qualitative input from informal testing, captured continuously.
5. **CHANGELOG.md** — what shipped when, including an "Incidents" section once production exists.

Plus a clean, message-clear git log — the reviewer reads it to understand evolution. These survive because they answer the reviewer's real questions: *what did you decide, what did you skip on purpose, what happened*. Code answers none of those.

## Phase 0 — before any code

- **Buy a pre-build architecture consult**: one senior engineer, 4–8 hours, reviewing the data model, auth choice, tenancy strategy, core-engine architecture, and hosting plan. This is the highest-ROI engineer time in the whole project — a wrong structural call costs weeks; the consult costs a day. Capture the output as the first LOCKED entries in DECISIONS.md.
- Lock the stack: one answer per category (framework, DB, ORM, auth, jobs, secrets, observability), written into DECISIONS.md. Changes require re-opening the consult.
- Commit SESSION_RULES.md and DECISIONS.md before the first feature.

## Build phase — founder + AI

- **Session discipline**: load the rules file at the start of every session; append the structural-decisions summary to DECISIONS.md at the end; resolve any flagged-unapproved decision before the next session.
- **Model tiering**: default model for building; strongest model for architecture-locking decisions, security reviews, third-attempt debugging, and monthly audits; cheapest model for boilerplate and content.
- **Build in dependency order** (foundations/auth → data backend → core engine → external API → UI polish), each block ending with a **sniff test** — a concrete, human-observable acceptance check ("a stranger can integrate from the docs without messaging you", "read 5 recommendations aloud — are any embarrassing?").
- **Monthly fresh-context audit**: hand the repo to an AI session with no prior context and have it audit against the rules and decisions files. Fix or defer-with-trigger every finding.
- No expert involvement during this phase except cheap async milestone check-ins at the riskiest seams (~$300–500 each) and an office-hours escape hatch when you hit a wall the AI can't unblock.

## Review phase — when and how to buy expert review

Trigger: the build is feature-complete for its launch scope. Do not skip this to save money — the cost of a tenancy leak or token-handling incident is the company.

- **Scope the engagement to review, not features**: auth + tenancy audit, rate-limit/DDoS verification, architecture-vs-DECISIONS.md drift review, the deferred structural calls you parked for them (e.g., app-level scoping vs. DB-level row security), production-ops setup, and fixing what they flag as P0/P1. P2/P3 become your backlog. Explicitly out of scope: rewriting the engine, polishing UI, expanding non-critical tests — that discipline keeps it at $5–10k instead of $40k.
- **Pay flat-fee, never hourly, for review work** — hourly incentivizes finding more, which is not what you want.
- **Prefer the same engineer who did the Phase 0 consult** — they can compare what you said you'd build against what you built.
- **Add a focused external pen test** in parallel, black/grey-box against staging, scoped to the launch surface only.

## After review — recurring cadence

Monthly: access-log reviews, dependency audit, fresh-context rules audit. Quarterly: secret rotation, contract-docs drift re-read, backup-restore drill. Annually: re-engage the pen test and the architecture review against the updated DECISIONS.md.

## Plan hygiene

- Budget every phase with low/high ranges and name what gets cut first under overrun (never the consult or the review — keep those sacred).
- Maintain a risks table with per-risk mitigations, including "founder hits a wall the AI can't unblock."
- State what the plan deliberately does not do (feature breadth, growth, hiring) so scope pressure has something to bounce off.
