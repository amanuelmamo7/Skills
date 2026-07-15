---
name: ai-build-house-rules
description: A 26-rule structural contract for building an application safely with AI coding assistance. Load at the start of any AI-assisted build session so architectural decisions that compound (tenancy, auth, secrets, cost) are locked before code is written.
---

# AI Build House Rules

Treat this list as a hard contract for the session. These are decisions that compound if wrong and are very expensive to fix late. Adapt names to the project's stack; the structure is the point.

## Structural rules (do not violate without explicit approval)

1. **MULTI-TENANCY**: every table carries a `tenant_id` from its first migration. Every read and write scopes by it. No "single-tenant for now" path.
2. **AUTH**: use a managed auth provider. Never roll custom password/session/JWT logic. Never store passwords. If a flow seems to require custom auth, stop and ask.
3. **SENSITIVE TOKENS**: third-party access tokens (bank, OAuth, payment) are encrypted at rest with a key from a real KMS. No plaintext tokens in the database, env vars, or logs. Re-auth webhooks wired from day one.
4. **CORE-LOGIC AS CONFIG**: business-differentiating logic (scoring, recommendations, pricing) is a rule/scoring system with named inputs. Client- or partner-specific behavior is configuration, not nested if/else code.
5. **LOGS + AUDIT**: all logs structured JSON. Every state-changing operation writes to an `audit_log` table (who, what, when, tenant). No `console.log` in production paths.
6. **MIGRATIONS**: one migration tool only. Never edit a migration after it has been applied to any environment.
7. **SECRETS**: no secrets in the repo. Local dev uses a gitignored env file; production uses the hosting provider's secret store. Surface any new secret you introduce.
8. **API VERSIONING**: external-facing endpoints namespaced under `/v1/`. Request/response shapes validated with schemas at the boundary. Breaking changes go to `/v2/`, never edit `/v1/`.
9. **IDEMPOTENCY**: any retryable mutating endpoint (webhooks, partner writes, payment-adjacent) accepts an idempotency key and is safe to call twice.
10. **WEBHOOK SIGNATURES**: every incoming webhook verifies its signature before processing. No exceptions, even in development.
11. **PII + DELETION**: user PII encrypted at rest. A documented "delete this user's data" path exists from the first user-creation feature. Privacy-law ready by construction, not retrofit.
12. **BACKGROUND WORK**: anything >~500ms or calling a third party runs through a job queue. HTTP handlers may make at most one bounded, read-only third-party lookup when UX requires it, via the safe outbound client (Rule 17); third-party-derived writes always queue.
13. **DATABASE**: one engine (default Postgres) unless a documented reason exists. No mixing engines without approval.
14. **RATE LIMITING**: every public or authenticated endpoint enforces a per-actor rate limit before business logic runs. Public: by IP. Authenticated: by user id. Webhooks: rejected signatures get a tighter limit than verified ones. No endpoint ships without a documented limit and a clean 429 path.
15. **PRODUCTION-SECRET ISOLATION**: production secret values never appear in dev env files, shared config, screenshots, chat, or commit messages. They live exclusively in the hosting provider's secret store. A production-prefixed key found anywhere else is a P0 incident.
16. **DEPENDENCY HYGIENE**: the lockfile is source of truth; every lockfile change is reviewed as code. Dependency updates are a privileged operation run against a checklist (changelog, >24h since publication, audit). Register your package namespace publicly to block dependency confusion. CI never grants fork PRs write access or secrets.
17. **EXTERNAL DATA VALIDATION**: every byte from a third-party API or LLM passes a schema validator before persistence. JSONB columns have application-layer schemas. All outbound HTTPS goes through a single client module with a domain allowlist; no handler fetches a user-controlled URL.
18. **FORENSIC INTEGRITY**: audit-log writes go to two destinations — the database and an append-only off-system log stream. A database compromise cannot erase the trail. Unauthenticated forensic writes are rate-limited so attackers can't drown real evidence in garbage.
19. **CLOUD-ACCOUNT HARDENING**: every cloud service in the dependency graph requires hardware-key 2FA. SMS-2FA is insufficient. Recovery codes offline. Access logs reviewed monthly. Least-privilege scopes; "the dashboard suggested it" is not a justification.
20. **SAFE RENDERING + CSP**: every page ships a CSP that disallows inline scripts and `unsafe-eval`. No `dangerouslySetInnerHTML` (or equivalent). External URLs render only via sanitized tags with domain allowlists — never interpolated into CSS, iframes, or hrefs unchecked.
21. **SECRETS ROTATION CADENCE**: every production secret rotates at least quarterly, tracked in a single rotation calendar. Rotation is a checklist run, not an ad-hoc event, and appears in the audit log.
22. **ORIGIN PROTECTION**: a CDN/WAF fronts every production endpoint before any external traffic — including soft launch. The origin IP is never publicly resolvable; origin firewall accepts CDN edge ranges only.
23. **COST AS ATTACK SURFACE**: every cloud service has a hard billing cap or documented alert threshold. Every endpoint has a per-invocation cost budget. Paid outbound APIs are circuit-broken per window. A cost-DoS is a P1 security incident, not "just a bill."
24. **GRACEFUL DEGRADATION + REVERSIBILITY**: every outbound call has timeout, retry with backoff/jitter, and a documented fallback. Every migration ships with a verified rollback path. Every deploy is reversible within 5 minutes. Forward-only changes require written justification before they ship.
25. **COMPLIANCE INFRASTRUCTURE**: Privacy Policy and ToS are versioned artifacts in the repo, linked from the app. Data access, rectification, and deletion paths exist from the first user feature. Every analytics/error provider is named in the policy. Under-age signups are rejected, not silently allowed.
26. **INCIDENT RESPONSE POSTURE**: documented on-call with escalation path, a status page on a separate domain before launch, alert routing with acknowledgment SLOs, and a written runbook covering the likely incidents. One tabletop exercise before launch, annually thereafter.

## Session behavior for the AI agent

- Before any decision in one of the 26 lanes: STOP. Surface (a) what you're about to do, (b) 2–3 alternatives, (c) one-sentence trade-offs, (d) your pick and why. Wait for explicit approval; silence is not approval.
- Flag every new dependency, library, or external service: name, what it replaces, rough cost at expected scale.
- Surface every schema change before applying it.
- No multi-module refactors without warning first.
- If asked to violate a rule, push back: name the rule, why it matters, what you'd recommend instead.

## End-of-session checklist

Output a "STRUCTURAL DECISIONS THIS SESSION" block listing: lanes touched and what was decided; new dependencies/services; migrations applied or proposed; any decision made without explicit approval (flag with a warning marker); any existing rule violation noticed. If none apply, say so — only if actually true.

## Remember

The cost of stopping to ask is minutes; the cost of a wrong structural call discovered six months in is weeks. If in doubt whether something is in one of the 26 lanes, treat it as if it is. False positives cost nothing; false negatives cost a rebuild.
