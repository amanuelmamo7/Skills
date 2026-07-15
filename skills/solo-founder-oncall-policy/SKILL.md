---
name: solo-founder-oncall-policy
description: Write an honest incident-response policy for a one-person on-call: acknowledgment SLOs, alert routing, a severity taxonomy mapped to response windows, and an explicit named gap where a backup human should be. Use when setting up production ops for a solo or tiny team.
---

# Solo-Founder On-Call Policy

Write an `incident-response.md` policy doc covering the **what / who / when** of incidents; the runbook covers the **how**. The defining discipline: describe the on-call posture you actually have, not the one that sounds professional.

## Response SLOs

Set two acknowledgment windows and write them down:

| Condition | Acknowledgment time |
|---|---|
| Business hours (your local TZ, e.g. 8am–8pm Mon–Fri) | 15 minutes |
| Off-hours: nights, weekends, holidays | 60 minutes |

State plainly: with a single-person rotation these are **commitments to yourself, not commitments to users** — a posture to aspire to, not a guarantee the world is owed. They become user-facing commitments only when a published status-page SLA or a ToS uptime promise exists.

## Alert routing

- Route error-tracker alerts to an inbox you actually check within the SLO.
- Channel separation is fine (a dedicated ops inbox filtered from the primary), but document that it is **the same human** — a second inbox is not a second responder.
- List the configured alert rules in a table (rule name, trigger, filter, destination) so an audit can verify them against the dashboard. Note known gaps explicitly (e.g., "old issues that suddenly re-spike aren't caught by the new-issue rule; acceptable at current scale, revisit if an incident is missed").

## Severity taxonomy

Map your error-capture levels to response expectations, and list which code sites emit each:

| Level | Used for | Response window |
|---|---|---|
| fatal | Total outage, security-control violations (outbound-allowlist breach, secret-compromise indicators), dropped production config | Immediate, per SLOs above |
| error | Business-logic failures, unhandled exceptions in API routes | 4 business hours |
| warning | Suspicious-but-handled activity (rejected webhook signatures), degraded upstreams (circuit opened) | Same business day |
| info | Observability only | No SLA |

Keep an inventory of every capture site (event name → level → category) so the taxonomy stays real as code grows.

## The backup-human gap — name it

If no second responder exists, write "**Backup human channel: none currently. This is an explicit gap.**" Do not let the doc imply redundancy that doesn't exist — if you're asleep or on a flight, no automatic escalation occurs.

Define the **trigger event** for adding a secondary human (e.g., the first launch with real users), and the bar they must meet:
- Technically apt enough to triage an alert: recognize an error, open the runbook, judge severity.
- Reachable out-of-band (SMS/phone), so they can escalate to you even when email is down.
- Enrolled with hardware-key 2FA on any account they're added to — a backup human is an addition to your root of trust, and inherits its hardening bar.

Treat "backup on-call exists" as a hard launch blocker in your pre-launch checklist, not a nice-to-have.

## Initial triage checklist

1. Read the alert subject and body — severity + tag usually identify the class.
2. Open the tracker issue; read the structured context attached.
3. Check the releases view: if the issue first appeared right after a deploy, the deploy is the prime suspect and revert is the fastest mitigation.
4. Check logs/uptime monitoring and the health endpoint.
5. Check CDN analytics if it looks traffic-shaped.
6. Mitigate: follow the runbook if covered; revert if revert is right; hot-fix on a branch with CI guards intact if needed.
7. Document: every real incident gets a changelog entry, and every deviation from the script becomes a runbook diff.

## Maintenance cadence

Review monthly (are the SLOs still realistic? channels still active?), when a secondary human is added (remove the gap callout), when alert rules or capture sites change, and after every real incident (were the SLOs met? did the taxonomy classify correctly?).
