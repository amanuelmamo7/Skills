---
name: meeting-reminder
description: Deterministic spoken meeting reminders with no LLM in the loop — a small script polls today's calendar every few minutes and voice-announces any timed event starting within 20 minutes, exactly once, with quiet hours and dedup state. Use when the user wants reliable meeting alerts on their machine, "remind me before meetings," calendar voice notifications, or a no-AI fallback layer for time-critical reminders.
---

# Meeting Reminder (Deterministic)

Time-critical reminders should not depend on an agent being awake. This is a pure-shell daemon: poll the calendar, announce once, stay silent otherwise.

## Design (why it's built this way)

- **No LLM in the loop** — an announcement 20 minutes before a meeting must fire every time; determinism beats intelligence here.
- **Dedup state file** — each event is announced exactly once (`memory/meeting-reminder-state.json`), so a 5-minute poll never nags.
- **Quiet hours** — silent before 08:00 and after 22:00.
- **Single owner** — this daemon owns meeting announcements; any coexisting assistant heartbeat must not also voice-announce meetings, or the user gets doubles.
- **Self-limiting log** — the rolling log truncates itself so it can run for years.

## How to use

1. `scripts/meeting-reminder.sh` is the reference implementation (macOS: `say` for voice, launchd every 5 minutes, calendar fetched from a private JSON endpoint — see the `daily-brief-export` skill).
2. To adapt: swap the calendar source (any endpoint/CLI returning today's timed events), the announcer (`say`, notify-send, push), and the schedule (launchd/cron/systemd timer). Keep the dedup-state, quiet-hours, and announce-once semantics — they're the design.

## Bundled resources

- `scripts/meeting-reminder.sh` — the original, working macOS implementation (machine-specific endpoint and paths).

Related skills: `daily-brief-export` (the calendar JSON source), `assistant-heartbeat` (must defer to this for meeting announcements).

> Source: OpenClaw "EA stack" — `~/.openclaw/workspace/meeting-reminder.sh`.
