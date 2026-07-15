---
name: evening-wrap
description: Run an end-of-workday wrap — tomorrow's calendar, any unread email signal, an honest review of how today's priorities went, and one suggested first task for tomorrow, written to a dated log. Use when the user asks to wrap up the day, "what's tomorrow look like," end-of-day review, evening summary, or wants to close out the workday and set up the next one.
---

# Evening Wrap

The bookend to the morning brief: close today honestly, set up tomorrow concretely.

## How to use

1. Gather: tomorrow's calendar, today's remaining unread email signal, and today's morning brief or task list (to review what actually got done vs. planned).
2. Compose four sections:
   - **Tomorrow's calendar** — times, titles, anything needing prep tonight.
   - **Email signal** — only what needs action; ignore noise.
   - **How today went** — compare against the morning's stated priorities; be honest about what got punted, no spin.
   - **First task for tomorrow** — one concrete suggestion, chosen from what was punted or what tomorrow's calendar makes urgent.
3. Write to a dated log (`memory/YYYY-MM-DD-evening.md` in the original) and keep the delivered form short enough to be read aloud.

## Bundled resources

- `scripts/evening-wrap.sh` — the original macOS cron wrapper (6:00 PM weekdays) that triggered the wrap through the OpenClaw gateway. Machine-specific; reference for re-automating.

Related skills: `morning-brief`, `weekly-wrap`, `memory-maintenance`.

> Source: OpenClaw agent "Bari" — `~/.openclaw/workspace/evening-wrap.sh`.
