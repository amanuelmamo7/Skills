---
name: morning-brief
description: Run a daily morning brief — today's calendar with times and attendees, unread email signal (filtered of promotions/noise), open tasks, and a suggested top priority for the day, delivered as a short spoken-style summary plus a written log entry. Use when the user asks for their morning brief, daily rundown, "what's my day look like," "catch me up," or any start-of-day summary of calendar, email, and tasks.
---

# Morning Brief

A weekday start-of-day briefing: what's on the calendar, what came in overnight that matters, what's open, and the one thing to do first.

## How to use

1. Gather inputs: today's calendar events (time, title, location, attendees), unread email from the last day filtered of noise (promotions, social, automated senders), and incomplete tasks. In the original setup these came from a private JSON export (see the `daily-brief-export` skill); use whatever calendar/email/task connectors are available.
2. Compose the brief in two forms:
   - **Spoken form** — short, natural sentences suitable for text-to-speech, leading with the day's shape ("Three meetings, first at 10. Two emails need replies.").
   - **Written form** — a dated markdown log (`memory/YYYY-MM-DD-morning.md` in the original) with sections for calendar, email signal, tasks, and suggested first task.
3. Be selective: the brief is signal, not a dump. Two or three emails that actually need attention beat a list of twenty.

## Bundled resources

- `scripts/morning-brief.sh` — the original macOS cron wrapper (7:00 AM weekdays) that triggered the brief through the OpenClaw gateway and spoke it via Sonos. Machine-specific paths and tokens; keep as reference for re-automating.

Related skills: `evening-wrap`, `weekly-wrap`, `daily-brief-export`, `morning-music-alarm`.

> Source: OpenClaw agent "Bari" — `~/.openclaw/workspace/morning-brief.sh`.
