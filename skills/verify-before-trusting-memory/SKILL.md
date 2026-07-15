---
name: verify-before-trusting-memory
description: Method for treating remembered facts (endpoints, auth patterns, "X doesn't work", prices, capabilities) as hypotheses to live-test before acting on them, and for dating fact updates. Use whenever an agent with persistent memory is about to rely on a note about an external system or current-state data.
---

# Verify Before Trusting Memory

Memory files are notes about the past, not guarantees about the present. Any "established fact" written by a previous session — an endpoint URL, an auth pattern, "X doesn't work," "the API requires Y" — is a **hypothesis** until re-verified with a live test in the current run.

Motivating failure: a stale memory note claimed an API rejected a valid token; a scheduled job believed the note, skipped the live call, and shipped a placeholder output the user had to debug. The note was simply wrong. One cheap HTTP request would have prevented it.

## Operating rules

1. **Before treating any endpoint, auth pattern, capability, or system fact as established, run a live test in the current turn.** A 200 from the actual endpoint beats any note in memory. A small GET or HEAD is enough — you're testing reachability and auth, not re-doing the work.

2. **When a memory note says "X doesn't work," test once before believing it.** If it still fails, fine — update the note with today's date and the specific error. If it works, the note was stale — fix it immediately.

3. **Treat "unavailable / not supported" in user-facing output as a smell.** Before writing that sentence, ask: did I verify this run, or did I read a note and quit? Verify first.

4. **Notes about external systems decay fastest.** Routes change, APIs add auth modes, third-party services rotate tokens, sites change their bot policies. The world moved while you were asleep — apply extra skepticism to anything external.

5. **Date every fact you write or update.** "As of YYYY-MM-DD, X works via Y." Future sessions can then judge staleness at a glance instead of treating all notes as equally fresh.

## Domain rule for time-sensitive data

Any claim about current-state numbers — prices, yields, FX, rates, filing dates, release data, account/positions state — must be backed by a live fetch *in the current turn*. Never quote such values from memory. Concretely:

- Live-market values (prices, yields, FX): always live-fetch.
- Scheduled facts (earnings dates, release calendars): live-fetch — they get revised.
- Documents/filings: live-fetch the most recent, don't assume the last one you saw is still the latest.
- Auth/session state for scraping or APIs: re-verify with a HEAD or small GET before assuming.

If a fetch fails, say so explicitly. Do not fall back to memory and present it as current.

## Verification ladder (cheapest sufficient test)

1. **HEAD / small GET** — is the endpoint alive and is my auth accepted?
2. **Sentinel round-trip** — for another agent or service: send a request demanding an exact known reply and grep for it.
3. **One-record real call** — for data APIs: fetch a single known record and sanity-check the shape.
4. **Full dry run** — only when the fact being tested is the pipeline itself.

Pick the lowest rung that actually tests the remembered claim.

## When to skip verification

- Facts internal to files you can read right now (just read them — that IS the verification).
- Explicitly historical analysis, where the user asked about a past period — but state the period clearly.
- Immutable identifiers (a git commit hash, a published document's content).

Everything else that gates an action or a user-facing claim: verify.

## Cost asymmetry (the reason this skill exists)

An extra HTTP request costs seconds. A silently-degraded output built on a stale note costs the user a debugging session and costs the agent trust. When in doubt, spend the request.
