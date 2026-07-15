---
name: cloud-cost-guardrails
description: Establish per-service cloud cost guardrails — classify each service as hard-capped, quota-capped, or alert-only, compute a worst-case monthly burn, and define tier-upgrade triggers. Use when setting up or reviewing a small product's cloud spending posture.
---

# Cloud Cost Guardrails

Maintain a `cost-budgets.md` that makes runaway spend structurally impossible and tier upgrades deliberate. Treat cost as attack surface: an attacker driving spend up without exfiltrating a byte is a security incident, not "just a bill."

## Step 1 — Classify every service's enforcement mechanism

For each service in the stack, one row:

| Service | Tier | Enforcement | Threshold | Notes |
|---|---|---|---|---|

Three enforcement classes, in order of preference:
- **Hard auto-shutoff** — an explicit budget cap; the service degrades (e.g., goes read-only) at the cap. Document the degraded behavior and make the app handle it gracefully (a rate limiter that fails open with a flag beats one that takes the app down).
- **Quota-as-cap** — free tiers with no overage billing; hitting quota is service degradation, not a bill. This *is* a hard cap; count it as one.
- **Alert-only** — the provider offers no shutoff, just a spend alert. Every alert-only service needs a documented human response path (who acts, within what window) in the incident policy.

Also flag terms-of-service tripwires: free tiers that prohibit commercial use are a hard upgrade trigger the moment money changes hands, independent of usage.

## Step 2 — Worst-case burn math

Sum the maximum possible monthly bill given the enforcement config: paid base fees + every hard cap, with quota-as-cap services contributing $0. State it as a single number: "Maximum monthly spend at current configuration: $X." If any service is alert-only, its realistic overrun window (alert → human action) is your exposure — say so. Compare the number against the ceiling assumed in your decision log and reconcile.

Also state **realistic** spend at current scale, so the delta between realistic and worst-case is visible.

## Step 3 — Per-endpoint and per-job cost breakdown

For each endpoint: which upstream operations does one invocation trigger (DB ops, cache commands, log ingest, job enqueues, paid-API calls)? Mark the hot paths and the expensive outliers. Do the same for background jobs (frequency × ops per run). This table is what turns "the bill is high" into "which endpoint is being hammered."

## Step 4 — Burn projections at three scales

Project the full table at: (A) today's usage, (B) the next launch milestone, (C) ~10x that. For each service at each scale: operations/month and cost, with a note where a free-tier cap breaks ("quota exceeded — forced to paid tier on bandwidth alone"). Scale C usually reveals which single upgrade dominates future cost.

## Step 5 — Upgrade triggers per service

For each service, write the explicit signals that prompt a tier change:
- **Hard triggers** — immediate action: commercial-use ToS lines, a quota that will be exceeded this month, a compliance feature (e.g., MFA) becoming mandatory.
- **Soft triggers** — usage crossing **60–80% of quota in any single month**, giving a month's lead time to migrate calmly instead of mid-incident.
- On upgrading to a paid tier, immediately configure that tier's spending limit — an upgrade should swap one cap for a higher cap, never for no cap.
- For hard-capped services: when the cap is hit, first check for a runaway (a loop somewhere) before raising the cap for "legitimate growth."

## Wiring into the rest of the system

- Circuit-break outbound calls to paid APIs on a per-window budget, not just on failures.
- Cost-anomaly symptoms ("bill unexpectedly high") get a row in the runbook's symptom table.
- A cost-DoS is a P1 incident: rate limits and CDN bot rules are cost controls as much as availability controls.
- Mid-incident, an upgrade trigger can fire early (e.g., DDoS burning function-hours toward quota) — the doc should authorize that call in advance.

## Maintenance cadence

Monthly: confirm current consumption per service, project next month. When any bill lands outside projection: investigate, then fix the projection. When a service is added: extend the table — every service gets a cap or a documented alert+response, no exceptions. Before any commercial activity: re-read the upgrade-trigger section in full.
