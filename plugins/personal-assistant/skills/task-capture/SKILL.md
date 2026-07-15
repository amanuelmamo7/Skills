---
name: task-capture
description: Turn a casual chat message ("remind me to X", "todo: X") into a structured task POSTed to a task API, with date parsing, one-line confirmation, and a local fallback so nothing is lost. Use when an assistant receives task-like requests over chat and needs to file them into the user's real task system.
---

# Task Capture from Chat

When the user sends a task-shaped message over any chat channel, capture it into their task system in one turn, confirm in one line, and never lose a task to a failed API call.

## Trigger phrases

Treat these (and close variants) as capture requests:

- "remind me to X"
- "add task X" / "add a task: X"
- "todo: X" / "to-do X"
- "don't let me forget X"

## Procedure

### 1. Parse the message into a task

- **Title:** imperative and short. Strip the trigger phrase ("remind me to call the vet Friday" → "Call the vet"). Keep it under ~8 words.
- **Due date (optional):** resolve relative dates against today's date in the user's timezone. "Friday" → the upcoming Friday; "tomorrow" → tomorrow; "end of month" → last day of month. Emit RFC3339 (e.g. `2026-07-17T00:00:00Z`). If no date is stated, omit the field — do not invent one.
- **Notes:** stamp provenance, e.g. `"via <assistant-name> <date>"`, so the user can see where the task came from.

### 2. POST to the task API

```bash
curl -s -X POST https://<your-task-app>/api/tasks \
  -H "x-auth-token: $(cat <path-to-secrets-file>/task-api-token.txt)" \
  -H "Content-Type: application/json" \
  -d '{"create":{"title":"<title>","notes":"via assistant <date>","due":"<RFC3339 or omit>"}}'
```

Conventions that matter:

- **The token is read from a secrets file at runtime** — a bearer/API token stored in a mode-600 file inside the workspace secrets directory. Never inline the token value in scripts, notes, or memory files.
- The endpoint should land the task where the user actually looks (their task manager, dashboard, and/or daily briefs) — capture into the system of record, not a side list.
- Check the response for success, not just exit code 0.

### 3. Confirm in one short line

```
Added: <title> (due <day>)
```

No due date → `Added: <title>`. Do not restate the whole task or explain what you did.

### 4. Fallback — never lose a task

If the POST fails (non-2xx, timeout, auth error):

1. Say so plainly in the confirmation: "Task API failed (<reason>)."
2. Write the task somewhere durable the user will see — a local notes app CLI, or a workspace file like `memory/unfiled-tasks.md` — so nothing is lost.
3. Note the failure so a later session (or the user) can re-file it into the real system.

## Edge cases

- **Multiple tasks in one message** ("remind me to A and also B"): create one task per item, confirm each on its own line.
- **Ambiguous date** ("sometime next week"): pick the start of that range OR omit the due date and say which you did — one clause, not a clarifying round-trip, unless the task is consequential.
- **Duplicate-looking task:** capture anyway; dedup is the task system's job, not the capture path's.
- **Task embedded in a longer message:** capture the task part, answer the rest normally.

## Setup checklist (first time wiring this up)

- [ ] Task API endpoint identified and reachable from the assistant's host
- [ ] Auth token generated and stored in a secrets file (never in the script, config notes, or chat)
- [ ] One end-to-end test: send a trigger phrase, verify the task appears in the user's real task view
- [ ] Fallback path tested once (point at a bad URL, confirm the local fallback fires)
