---
name: proactive-announce-policy
description: Deterministic routing policy for a proactive assistant deciding whether a finding goes to voice, a chat channel, or stays silent — plus a state-file dedup pattern so nothing is announced twice. Use when building heartbeat/monitoring loops that surface emails, calendar events, or system alerts to a user.
---

# Proactive Announce Policy

When a background check (heartbeat, cron, monitor) finds something worth surfacing, pick the channel by RULE, not vibe. Judgment calls drift; rules don't.

## The three-tier routing rule

**Voice channel** (spoken announcement) — highest interruption cost, so gate hard. ONLY during waking hours (e.g. 08:00-22:00 local), one sentence of 20 words or fewer, and ONLY for:

1. A message that is BOTH time-sensitive today (meeting change, deadline today, approval blocking someone) AND from a sender on the maintained VIP list — or clearly a real person writing directly to the user.
2. A system failure needing action from the user today (auth expired, scheduler down).
3. Anything else another deterministic job doesn't already own. If a dedicated scheduled job owns a category (e.g. a meeting-reminder agent owns "starts in <20 minutes" announcements), do NOT duplicate it — route your version to the chat channel instead.

**Chat channel** (async message) — everything worth flagging but not urgent-now: interesting emails, tomorrow's deadlines, events 1-2 hours out, FYIs, weekly items.

**Silence** — newsletters, job digests, promos, shipping notifications, security notices, anything already covered by a scheduled brief the user will read anyway.

**Tie-breaker rule:** if unsure whether an item qualifies for voice, it doesn't — use the chat channel. Voice false-positives erode trust in the whole system.

## Dedup via state file

Never announce the same item twice. Maintain a JSON state file (e.g. `memory/heartbeat-state.json`) with an `announced` map:

```json
{
  "announced": {
    "<event-id-or-message-id>": "2026-07-15",
    "<another-id>": "2026-07-14"
  },
  "last_checks": { "email": "2026-07-15T14:02:00Z", "calendar": "2026-07-15T13:30:00Z" }
}
```

Procedure on every check cycle:

1. Before announcing anything, look up its stable id (message id, event id, alert fingerprint) in the `announced` map. If present — skip, regardless of channel.
2. After every announcement (voice OR chat), write the id and today's date into the map immediately, before moving on.
3. Prune entries older than 2 days each cycle so the file stays small.
4. Track per-category last-check timestamps in the same file so overlapping runs can skip categories checked within the last ~30 minutes.

## Quiet hours

Define an explicit quiet window (e.g. 22:00-08:00): no voice ever; hold non-urgent chat pings until morning unless genuinely urgent. Encode the window in the policy file, not in your head.

## Writing the policy down

Keep the policy in a checked-in file (e.g. `HEARTBEAT.md`) with:

- The rotation of checks and their frequency (email 2x daily, calendar 2x daily, scheduler health at startup + daily, gateway health 1x daily)
- The three-tier routing rule with the exact qualifying conditions
- The path to the VIP list the voice tier depends on
- The dedup rule and state-file path

The point of a written deterministic policy: any session — including a fresh one with no memory — makes identical routing decisions.

## Anti-patterns

- Announcing on "feels important" without matching a written rule.
- Voice announcements longer than one sentence.
- Re-announcing after a restart because dedup state lived in memory instead of on disk.
- Two jobs owning the same announcement category (leads to double alerts — assign each category one owner).
- Letting the announced map grow unbounded — prune every cycle.
