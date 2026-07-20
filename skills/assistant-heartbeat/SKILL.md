---
name: assistant-heartbeat
description: Run a periodic assistant heartbeat check — rotate through email, calendar, cron-job health, and mentions on a schedule, decide whether anything justifies interrupting the user, and stay silent otherwise. Use when building or running a proactive background assistant that checks in every couple of hours, or when the user asks for a "heartbeat," periodic check-in routine, or an interrupt-only-when-it-matters monitoring loop.
---

# Assistant Heartbeat

The proactive loop for a background assistant: check a rotation of sources every couple of hours during waking time, and interrupt **only** when something clears the bar. The hard part is staying quiet.

## How to use

1. Read `references/heartbeat-policy.md` — the original rotation and announce policy. The core design:
   - **Rotation**: each heartbeat checks a different slice (unread email signal → upcoming calendar → cron/automation health → mentions), tracked in a small state file so slices don't repeat back-to-back.
   - **Interrupt bar**: a timed event soon, an email that clearly needs a same-day reply, or a broken automation. Everything else is logged, not announced.
   - **Quiet hours** and deduplication: never announce the same item twice; never announce outside waking hours.
2. On each heartbeat: read the state file, check the current rotation slice, decide interrupt-or-silent, update state, append a one-line trail to the daily log.
3. If nothing needs attention, the correct output is effectively nothing ("HEARTBEAT_OK" in the original protocol).

## Bundled resources

- `references/heartbeat-policy.md` — the original HEARTBEAT.md rotation/announce policy.

Related skills: `meeting-reminder` (owns voice announcements for meetings — the heartbeat must not duplicate it).

> Adapted from the author's personal assistant stack.
