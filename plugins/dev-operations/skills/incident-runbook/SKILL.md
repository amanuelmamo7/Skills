---
name: incident-runbook
description: Write and maintain a production incident runbook using the Symptoms→Diagnosis→Immediate mitigation→Recovery→Post-incident format with a symptom-to-scenario quick-reference table. Use when creating ops documentation for a production service.
---

# Incident Runbook

The runbook is the document you read **during** an incident. Write it imperative, terse, and biased toward action — polish prose elsewhere. Enumerate the likely incident scenarios for your stack (managed DB down, auth provider down, CDN/DNS outage, job runner down, third-party API unavailable, secret compromise, operator-device compromise, sustained DDoS, bad migration, bad-code regression, deploy failure, email delivery failure, rate-limit false positives, observability degraded) and give each one the same five-section skeleton.

## Document skeleton

1. **Solo/limited on-call disclaimer** if true: name honestly that there is one responder and no automatic escalation. "Escalate" steps then mean "recognize you're past your skill and slow down," not "page another human."
2. **How to use this doc**: open the matching scenario, follow steps in order, document timestamps and actions as you go (the post-incident writeup is built from these notes), and update the runbook whenever the procedure was wrong.
3. **Quick-reference table** mapping what you actually see to a scenario:

| You see / received | Likely scenario | Go to |
|---|---|---|
| Alert naming DB connection errors | Database down | §1 |
| Error count surges right after a deploy | Bad-code regression | §N |
| Outbound-allowlist violation alert | Secret compromise suspected | §N |

Key the rows on **observables** (alert names, error strings, dashboards) — not on causes, which you don't know yet.

4. **General triage flow**: 2 minutes before committing to a scenario — read the alert, check the status page, hit the health endpoint directly, check upstream providers' status pages, then match. If nothing matches: "this is novel — slow down" mode; read the newest error carefully and decide whether reverting the last deploy is a safe holding action.
5. **Per-scenario sections**, each with exactly five parts.

## The five-part scenario format

- **Symptoms** — the alerts, log patterns, and user reports that indicate this scenario, including which signals will be *absent* (e.g., "health endpoint may still be green — this failure is logic-level").
- **Diagnosis** — ordered checks that discriminate between causes (provider status page; is the error "unreachable" vs "auth failed" vs "pool exhausted"? — different causes, different owners).
- **Immediate mitigation** — one branch per diagnosed cause. Include explicit "nothing app-side can do; update status page and wait" branches — knowing when to do nothing is a mitigation.
- **Recovery** — ordered verification that the system is actually healthy: health endpoint, lightest real read, a full user-path smoke test, reconcile any dual-written logs, status page back to operational.
- **Post-incident** — changelog entry, SLO-met check, and the standing question: if this was our fault, what guardrail prevents recurrence? Update the runbook if any step failed.

## Example scenario 1 — Managed database down

**Symptoms**: stack traces with connection errors; health endpoint 5xx; dependent webhook handlers failing. **Diagnosis**: provider status page; then read the actual error — unreachable (their outage) vs. auth failed (credential rotated without updating the deploy env) vs. too many connections (your leak). **Immediate mitigation**: outage → status page update, wait, no fallback exists; credential → fix env var, redeploy; pool → redeploy for a fresh pool, then find the leak. **Recovery**: health check, lightest DB read returns 200, reconcile off-system audit-log mirror against the DB for rows lost mid-outage. **Post-incident**: their fault → nothing to fix; your fault → follow-up task + runbook diff.

## Example scenario 2 — Production regression from bad code

**Symptoms**: error tracker surges within minutes of a deploy; new error class; infra all green. **Diagnosis**: releases view → which issues are new in this release; identify the deploy's commit; diff against the last green deploy. **Immediate mitigation**: instant-rollback / promote the last known-good deploy — production first, investigation later. Nuance: app rollback does not roll back DB migrations; if a migration shipped in the same release, run the bad-migration scenario in parallel. **Recovery**: confirm the error class stopped; investigate on a branch at leisure; write the regression test that would have caught it; re-ship with the test. **Post-incident**: why didn't CI catch it — add the missing check class.

## Example scenario 3 — Secret compromise suspected (abridged)

**Symptoms**: outbound-allowlist violation alerts, unrecognized commits or deploys, anomalous bills, login notifications you didn't cause. **Rule**: when in doubt, assume worst case and rotate — in blast-radius order (see the secret-rotation drill skill). **Post-incident**: full post-mortem; re-evaluate rotation cadences; tabletop the section afterward.

## Maintenance

Run one tabletop exercise before launch (acceptance criterion: it produces at least one documented runbook fix) and annually after. Every real incident that deviates from the script produces a runbook diff. Add scenarios when reality presents one the table doesn't cover.
