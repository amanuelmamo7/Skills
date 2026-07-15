---
name: secret-rotation-drill
description: Rotate production secrets in blast-radius order — root-of-trust accounts first, application keys last — both as a quarterly scheduled drill and as the emergency response to suspected compromise.
---

# Secret Rotation Drill

Two modes, one procedure: a **quarterly scheduled rotation** (calendar-driven, calm) and an **emergency rotation** (compromise suspected, urgent). The ordering logic is identical; the emergency adds session revocation and forensics.

## The ordering principle: blast radius first

Rotate the highest-leverage secret first. Rotating a low-leverage secret is pointless while a higher-leverage one is still hot — an attacker holding the account that *controls* the others just re-issues whatever you rotated.

1. **Source-control account** (root of trust — controls the code, and often SSO into everything else): revoke all personal access tokens, sign out all sessions, rotate the password, verify the hardware keys on file are yours and remove any unrecognized 2FA method.
2. **Primary email / identity account** (recovery path for most other services): same treatment.
3. **DNS / CDN account** (whoever controls DNS can redirect all traffic to their own server): revoke API tokens, sign out sessions, verify DNS records and registrar nameservers against your documented-known-good configuration.
4. **Deploy platform** (controls what code ships): revoke tokens, sign out sessions, review recent deploys for anything unfamiliar; revert if needed.
5. **Application-layer secrets, in one sweep**: auth-provider secret + webhook signing secret, database password/connection string, job-runner signing + event keys, cache/rate-limiter tokens, log-ingestion tokens, any hashing salts (note: rotating a salt invalidates existing hashes — coordinate reconciliation), and anything else in the deploy platform's env-var inventory.
6. **Redeploy** so the new values take effect, then verify each service works: sign-in test, webhook test event, health endpoint.

## Emergency additions (compromise suspected)

- First identify scope and blast radius: which secret, what can it access? Check each provider's audit log for actions you didn't take; check your off-system audit-log mirror for unfamiliar actors or IPs.
- If your device or hardware key may be compromised, work from a known-clean device, revoke **sessions** everywhere before rotating (rotation from a compromised session is theater), remove the missing key from every service's 2FA list, and fall back to the backup key. Order a replacement so you return to N+1 key redundancy.
- Preserve evidence: export the audit-log window before cleanup.

## Quarterly cadence mechanics (house-rule discipline)

- Every production secret has a **documented rotation date in a single rotation calendar** — one file listing each secret, its owner, where it rotates (which dashboard), where it's consumed (which env var), and its next-rotation-by date.
- Rotation is a **checklist run, not an ad-hoc event**. Walk the calendar top to bottom; tick each secret.
- Every rotation writes an **audit-log entry** (what rotated, when, by whom). Rotations that leave no trace can't be verified by the next audit.
- Dev and prod credentials are separate; rotating prod never requires touching a dev env file, and no production-prefixed value ever lands outside the hosting provider's secret store. Finding one there mid-drill is a P0 incident, not a chore.

## Verification checklist (both modes)

- [ ] Every calendar entry ticked with a new next-rotation-by date
- [ ] Fresh deploy completed after the sweep
- [ ] Sign-in flow works end to end
- [ ] Webhook test event verifies against the new signing secret
- [ ] Background job runs clean with the new keys
- [ ] Old credentials confirmed revoked (attempt one call with an old token — expect failure)
- [ ] Audit-log entries written
- [ ] Any surprises folded back into the runbook

## After the first real emergency

Tabletop the procedure again: did the rotation order hold under pressure? Re-evaluate which secrets deserve a shorter-than-quarterly cadence.
