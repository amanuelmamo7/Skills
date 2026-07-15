---
name: security-audit-vibe-coded-app
description: Run a full-codebase security audit of an AI-assisted ("vibe-coded") application and write it up as a confidence-scored report. Use when auditing an app built substantially with AI coding tools, before launch or on a recurring cadence.
---

# Security Audit for an AI-Built App

Read the entire codebase, then produce a report in the structure below. The methodology assumes AI-generated code fails in characteristic ways: authorization checks, input sanitization, and secrets handling produce no visible test failure when omitted, so they are omitted disproportionately often. Grade against that curve.

## Report structure

### 1. Header
Date, auditor, scope (repo path, what was read: all packages, API routes, schema, auth, CI, env config).

### 2. Executive summary with confidence-scored table
Two or three sentences of overall posture, naming the top gaps. Then a table scoring each concern lane out of 10, with a one-line status:

| Concern | Confidence Score | Status |
|---|---|---|
| Security — auth, injection, tenancy | n/10 | strengths + fixable gaps |
| Product completeness | n/10 | what's real vs stubbed |
| Feature stability | n/10 | test coverage reality |
| DDoS resilience (current) | n/10 | |
| DDoS resilience (with named mitigations) | n/10 | with effort estimate |

### 3. Threat landscape for AI-built apps
Briefly establish the grading curve: current published vulnerability rates in AI-generated code, recent supply-chain incidents relevant to the toolchain (check the dependency tree and lockfile against known compromised versions and IoCs; state explicitly whether this app is affected), and the root cause — LLMs optimize for "runs correctly in isolation." Include developer-machine risk if AI dev tools are in use: check tool config directories for injected files, and warn about remediation-order traps (e.g., removing a persistence daemon before revoking the token it monitors).

### 4. Strengths, each with a rating
List what is structurally right, each scored (e.g., "Multi-tenant scoping 9.5/10") with the evidence: the file, the pattern, and the CI check that enforces it. Strengths matter — they tell the reader which vulnerability classes are eliminated by construction rather than by vigilance.

### 5. Findings requiring action
One writeup per finding, severity-tagged (CRITICAL / MEDIUM / LOW / INFO), each with:
- **File** (path + line where possible)
- **Finding**: the exact evidence, quoted (redact secret values — show the prefix that identifies the class, never the value)
- **Risk**: the concrete attack this enables, not a generic category
- **Action**: the specific fix, with code sketch where useful, and effort

Priority hunting list for AI-built codebases: production-prefixed secrets in dev env files; missing rate limiting; static salts; missing tenant filter in any single query (grep every WHERE clause); unauthenticated write paths (forensic logging endpoints included); unvalidated third-party data landing in JSONB; external URLs stored raw and rendered; client-exposed analytics/error keys; unbounded payload storage; config files that alter behavior with no audit trail; near-zero test coverage on integration layers.

### 6. Product completeness table
Feature-by-feature: implemented / stub / not implemented. An auditor who conflates "schema exists" with "feature works" misleads the founder.

### 7. DDoS posture
Current score, specific vulnerabilities by layer (volumetric, L7-expensive endpoints, webhook amplification), then a step-by-step mitigation ladder with the score each step buys and its effort.

### 8. Immediate action items — priority table
| Priority | Action | Effort |. P0 = do today (rotate, isolate secrets), P1 = this week (CDN, rate limits), P2 = before next feature (scoping fixes, integration tests), P3 = planned.

### 9. Infiltration-point estimate with confidence interval
State a point estimate of distinct infiltration points with an 80% confidence interval, split into "already documented above" and "identified from code, not yet in prior findings," and say explicitly what the residual uncertainty covers. Then assess the risk that *new* attack methods find *new* points, rated by time horizon (next 3 months / 3–12 months) with the primary driver for each.

## Method notes

- Skim structure first (schema, middleware, CI, env files), then read every auth/tenancy/webhook/ingestion path in full.
- Every claim gets evidence: a path, a line, a quoted pattern. No vibes in the vibe-code audit.
- Known accepted trade-offs (documented in the decision log) are noted as such, not re-litigated — but new leak surfaces on top of an accepted trade-off are new findings.
- Keep the report itself maintained: when fixes ship, add a dated status column rather than editing findings away.
