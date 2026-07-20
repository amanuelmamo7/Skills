---
name: daily-brief-export
description: A token-protected private JSON endpoint that exports the day's calendar events, filtered unread email threads, and incomplete tasks from Google APIs for consumption by AI assistants and scripts — no browser session required. Use when building an assistant that needs programmatic access to calendar/email/tasks, when the user wants a personal data API for their agents, or as the data layer behind morning-brief/meeting-reminder style automations.
---

# Daily Brief Export (Agent Data Endpoint)

Assistants and cron scripts shouldn't each implement Google OAuth. This is the pattern: one serverless endpoint, token-protected, that returns everything a daily brief needs as clean JSON.

## Design

- **Auth**: a shared secret in the `x-api-token` header (or query param), checked against an env var. No cookies, no browser session — callable from cron, launchd, or an agent.
- **Google access**: a stored OAuth refresh token (env var) → client, so the endpoint works headlessly forever.
- **Email noise filter**: the Gmail query excludes promotions, social, and a maintained blocklist of automated senders — the endpoint returns *signal*, which keeps every downstream consumer simple.
- **Shape**: `{ date, calendar: [{time, summary, location, attendees}], tasks: [...], email: [...] }` — flat, predictable, easy for both scripts (`jq`) and agents.

## How to use

1. `scripts/daily-brief-export.js` is the reference implementation (a Vercel serverless function importing helpers for calendar/threads/tasks).
2. To adapt: deploy alongside helper lib functions for `clientFromRefreshToken`, `listTodaysEvents`, `listThreads`, `listIncompleteTasks`; set `BARI_TOKEN` and `GOOGLE_REFRESH_TOKEN` env vars; tune the email exclusion query to your own noise senders.
3. Consumers: the `morning-brief` and `meeting-reminder` skills in this repository both read from this endpoint in the original stack.

## Bundled resources

- `scripts/daily-brief-export.js` — the reference endpoint source.

> Adapted from the author's personal assistant stack.
