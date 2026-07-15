---
name: pre-deploy-gate
description: Encode a project's architectural house rules as CI gate steps — custom lint/grep checks, ephemeral-database migration verification, frozen-lockfile installs — so rule violations cannot ship. Use when setting up or hardening CI for a rules-driven codebase.
---

# Pre-Deploy Gate

House rules that live only in a prompt or a doc decay; rules encoded as CI steps are enforced forever, including against AI-generated code in future sessions that never read the doc. Whenever a rule can be checked mechanically, add a gate. Whenever a rule is violated once, ask "what CI step would have caught this?" and add it.

## Gate architecture — three parallel jobs

Run on every push to main and every PR against main, with concurrency-cancellation of superseded runs.

### Job 1: static — typecheck + lint + rule checks

Order matters: run the **custom rule checks first**, before generic lint — they are the highest-signal failures.

- `pnpm install --frozen-lockfile` — the lockfile is source of truth; a mismatched lockfile is a build failure, not an auto-fix (dependency-hygiene rule enforced structurally).
- **Custom rule check: tenancy scoping** — a script that fails the build if any file outside the DB package imports the raw DB client, forcing every query through the tenant-scoped wrapper. A grep-based check is enough:
  ```bash
  # fails on any raw-client import outside packages/db/
  grep -rn "from '@yourorg/db'.*\brawDb\b" apps/ packages/ \
    --include='*.ts' | grep -v '^packages/db/' && exit 1 || exit 0
  ```
- **Custom rule check: direct-fetch** — fails the build if any route handler calls `fetch(` directly instead of the allowlisted safe-fetch client module (external-data-validation rule).
- Formatter check, typecheck, lint.

The pattern generalizes: each structural rule gets a `check:<rule>` script in package.json wired as a named CI step, so the CI log reads as a rules-compliance report.

### Job 2: test — unit tests

Straight `pnpm test` after a frozen-lockfile install. Keep it a separate job so a rule-check failure and a test failure surface independently.

### Job 3: migrations — apply cleanly against an ephemeral database

Spin a real Postgres service container (with a health check) and prove the migration chain works from zero on every commit:

1. Generate migrations from the schema (catches schema/migration drift — an uncommitted migration fails here).
2. Apply the full migration chain to the empty database.
3. Run the seed script.
4. **Assert a known post-seed fact with real SQL** — e.g., `psql -c "SELECT slug FROM tenant WHERE slug='default';" | grep -q default`. This proves the seed actually ran, not just that the command exited 0.

Use fixed throwaway credentials and CI-only env values (e.g., a fixed dummy salt) — never real secrets. Stretch goal, with an explicit trigger for when migrations multiply: also run each `.down.sql` and re-apply forward to verify reversibility.

## What must never appear in the workflow

- No `pull_request_target` with write access or secrets — fork PRs run read-only (supply-chain rule).
- No production credentials, no deploy keys in test jobs, no secrets echoed to logs.
- No `continue-on-error` on rule checks. A gate that warns is not a gate.

## Choosing what to gate

Gate-worthy: anything greppable (forbidden imports, forbidden APIs like `dangerouslySetInnerHTML` or `console.log` in prod paths, secret-looking prefixes in tracked files), schema/migration drift, lockfile drift, seed integrity. Not gate-worthy in CI: things needing human judgment (decision-log completeness, rate-limit values) — those belong to the fresh-context audit instead. Between the two, every rule has an enforcement home.

## Evolution rule

CI is append-mostly: steps are added when violations occur and removed only with the same ceremony as changing the house rule itself. Deleting a green check because "it never fires" is exactly backwards — it never fires because it exists.
