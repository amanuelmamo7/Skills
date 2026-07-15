---
name: cloud-account-hardening
description: Bootstrap and harden the cloud accounts a new project depends on — root-of-trust ordering, hardware-key 2FA everywhere, secret-handling rules from day one, and deferring services until needed. Use when standing up accounts for a new build.
---

# Cloud Account Hardening

The account-creation session is the highest-leverage security moment of the project: every choice made here (which identity owns what, how secrets travel, which 2FA method) becomes the trust foundation everything else inherits. Write the setup as a guide with per-service sections, and harden as you create — retrofitting 2FA across a dozen accounts never happens.

## Root-of-trust ordering

Create accounts in dependency order, because later accounts authenticate via earlier ones:

1. **Primary email / identity account** — the recovery path for everything. Harden first, hardest.
2. **Source-control account** — owns the code and is the SSO identity most dev services sign up through. Everything created "Continue with GitHub"-style chains its security to this account.
3. **Deploy platform, database, auth provider, observability** — created via the source-control SSO, in whatever order the build needs them.

Consequence: compromising account #1 or #2 compromises the chain. That is acceptable *only* because you harden them to hardware-key standard — and it is why the emergency rotation drill starts at the top of this same list.

## Hardening checklist — apply to every account at creation time

- [ ] **Hardware-key 2FA** enrolled (two keys: primary + backup). SMS-2FA is explicitly insufficient — port-out attacks defeat it.
- [ ] **Recovery codes stored offline** (printed / safe), never in a synced notes app or cloud drive.
- [ ] **Least-privilege scopes**: when a service asks for repo access, grant only the one repo. "The dashboard suggested this scope" is not a justification.
- [ ] **Unique strong password** from a password manager — SSO where possible, but the accounts that *are* the SSO roots get their own.
- [ ] Note the account in a **dependency-graph inventory**: service, owning identity, tier, what it can access. This inventory later drives the rotation calendar and monthly access-log review.

## Secret-handling rules from minute one

- **Never paste secret keys or API tokens into chat** — including chat with an AI assistant. Secrets go directly into a gitignored local env file (`.env.local`); the assistant reads them from disk during scaffolding, never from the conversation.
- Distinguish explicitly, per service, which values are **safe to share** (project URLs, slugs, region names, app names) and which are **secret** (anything prefixed `sk_`, connection strings, signing keys). Write "send back to chat: X" vs "save to .env.local: Y" in every setup section.
- Gitignore the env file before the first secret exists.
- Production values will later live only in the hosting provider's secret store; dev accounts get dev-scoped keys. Set that expectation now.

## Per-service section format (for the setup guide)

For each service: **What it does** (one paragraph, plain language) / **Cost** (free-tier limits and the price + week at which you'll outgrow them) / **Steps** (numbered clicks, exact names to enter, which region and why — e.g., match the DB region to the future KMS region) / **Save to .env.local** (the exact variable names) / **Send back** (only the safe values).

## Defer what you don't need yet

End the guide with a "What we are NOT setting up today (and why)" section: each deferred service, why it isn't needed yet, and when it will be resurfaced with its own setup guide ("KMS — needed only when payment tokens arrive, week 10+; will resurface ~1 week before"). Minimum account surface = minimum attack surface = minimum credential-rotation burden.

## Ongoing obligations this bootstrap creates

- **Monthly**: review access logs on every account in the inventory; verify the 2FA key list on each account contains only your keys.
- **Quarterly**: rotation drill across the inventory (see the rotation skill).
- **On adding any service later**: full checklist above, plus a row in the inventory, a cap in the cost-budget table, and a mention in the privacy policy if it touches user data.
- **On adding any human** (backup on-call, contractor): they enroll hardware-key 2FA before receiving access — they are joining the root of trust.
