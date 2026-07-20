# Heartbeat Rotation & Announce Policy

The reference policy for a periodic assistant heartbeat. The design goal: the assistant checks in regularly, but the user hears from it rarely — and never twice about the same thing.

## Rotation (2–4 checks per day)

Each heartbeat checks a different slice, tracked in a small state file so slices don't repeat back-to-back:

1. **Scheduler health** (startup + once daily) — verify every scheduled job/agent the stack depends on is actually loaded (e.g. `launchctl list` on macOS, `systemctl list-timers` on Linux). If any are missing, reload and alert.
2. **Unread email** (2x daily, skip quiet hours) — flag only what's urgent or from important contacts.
3. **Calendar** (2x daily) — surface events starting within 2 hours if not recently reminded.
4. **Infrastructure health** (1x daily) — gateway/daemon status checks; alert if down.

## Announce policy — deterministic, no judgment calls

When something is worth surfacing, pick the channel by RULE, not vibe:

**Voice** — ONLY during waking hours, one sentence ≤20 words, and ONLY for:
1. An email that is BOTH time-sensitive today (meeting change, deadline today, approval blocking someone) AND from a sender on the maintained VIP list (or clearly a real person writing directly to the user).
2. A system failure needing action from the user today (e.g. auth expired, scheduled job down).
3. NOT meeting reminders — if a deterministic meeting-reminder daemon exists (see the `meeting-reminder` skill), it owns the "starting in <20 minutes" announcement. The heartbeat surfaces events 1–2h out via the quiet channel only.

**Quiet channel** (chat/messaging) — everything else worth flagging but not urgent-now: interesting emails, tomorrow's deadlines, FYIs, weekly items.

**Silence** — newsletters, job digests, promos, shipping notices, security notices, anything already covered in the morning brief.

## Dedup rule

Before announcing, check the state file's `announced` map (key = event id or message id, value = date). Never announce the same item twice. Add every announcement to the map; prune entries older than 2 days.

**If unsure whether an item qualifies for voice, it doesn't — use the quiet channel.**
