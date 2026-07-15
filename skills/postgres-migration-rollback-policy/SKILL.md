---
name: postgres-migration-rollback-policy
description: A forward-fix-first policy for Postgres schema migrations — .down.sql files as documentation and disaster path, a when-to-rollback matrix, and PITR-branch recovery. Use when establishing migration discipline or responding to a bad migration.
---

# Postgres Migration Rollback Policy

Maintain a `migrations-rollback.md` policy doc alongside the migration files. The policy is the default stance; per-migration notes are the specifics; the actual reverse SQL lives in `*.down.sql` files adjacent to each migration.

## Default policy: forward-fix > rollback

For any production-deployed migration, the first-choice response to a problem is a **new forward migration that fixes it**, not a rollback. Reasons:

- Postgres DDL is largely irreversible without data loss.
- Most ORMs' migration tooling is forward-only by design; down migrations run outside the tool's bookkeeping.
- A rollback destroys downstream data that future state assumes.
- If audit logs dual-write off-system, rollbacks create reconciliation gaps.

The strong default: if you're considering rollback, ask "could a forward-fix migration achieve the same result?" ~95% of the time the answer is yes — even "wrong column type" is better solved by an ALTER in a new migration.

## Why write .down.sql at all (two reasons, neither is "use routinely")

1. **Documentation** — writing the down SQL forces clarity about exactly what the migration changes; reviewing it in the PR surfaces "what breaks if this reverts" questions.
2. **Disaster path** — if forward movement becomes impossible (schema corrupted, compromised DB rebuilt from scratch), the down SQL is the bookmarked recovery script.

## When-to-rollback matrix

| Situation | Forward-fix | Rollback |
|---|---|---|
| Migration is wrong but data intact | Always | No |
| Partially applied; production broken | Almost always (complete or reverse via new migration) | Rare |
| Migration corrupted data | Restore from PITR + forward-fix | No |
| Tables need dropping | New migration to drop them — same effect, cleaner audit trail | No |
| Full schema reset (compromise, fresh dev DB) | No | Yes — run the down SQL |
| CI validation of reversibility | N/A | Yes — against a fresh container |

## Data-corruption recovery: PITR branch, not down SQL

1. **Stop the writes first**: revert the application deploy so further writes don't compound the corruption. (App instant-rollback does not revert schema — handle both.)
2. Create a **point-in-time branch** of the database from just before the migration applied (managed Postgres providers with branching make this minutes).
3. Decide: **promote the branch to primary** (fast, loses post-migration good data) or **write a data-repair script** (slow, preserves more, riskier). Document the decision before executing.

## Manual rollback procedure (when the matrix says yes)

1. Confirm forward-fix was explicitly ruled out.
2. **Branch/snapshot current state first** — the recovery anchor if the rollback itself goes wrong; promoting it back undoes the rollback in seconds.
3. Run the down SQL: `psql "$DATABASE_URL" -f migrations/<name>.down.sql`
4. Verify the schema matches the expected post-rollback shape.
5. Remove the migration's entry from the tool's journal so it can re-apply later.
6. Changelog entry: what rolled back, why.

## Pattern for every future migration

- Ship the `*.down.sql` **in the same commit** (CREATE TABLE → DROP ... CASCADE; ADD COLUMN → DROP COLUMN IF EXISTS; seed INSERTs → scoped DELETEs; irreversible data transforms documented as such explicitly).
- Add a section to the policy doc: **what it does / rollback file / destructiveness / realistic rollback scenario / forward-fix preferred for**. For the initial-schema migration, say plainly that its rollback destructiveness is *total* and there is no realistic production invocation.
- PR review explicitly checks the down SQL: every DDL op reversed? data loss noted? expectations set correctly?
- If a migration ships without a down file, add it retroactively and note the lapse — the pattern only works if it's universal.

## CI verification (deferred with a trigger)

A CI job that applies each migration to a fresh Postgres container, runs the down SQL, verifies the schema returned to prior shape, and re-applies forward is the gold standard. Reasonable to defer while migrations are few; set the trigger explicitly (e.g., 5+ migrations, or any migration whose reversibility is doubted in review). At minimum, CI should always verify migrations **apply cleanly** to an ephemeral database.

## Maintenance

Per migration added: doc section + down file in the same PR. Per rollback invoked: changelog entry + update the migration's section with "actually invoked on DATE for REASON." Annually: re-check the CI-step trigger against the migration count.
