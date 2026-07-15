# HEARTBEAT checks — rotate through these 2-4x per day

## 1. Scheduler Health (every session startup + once daily)
All jobs now run as LaunchAgents (crontab is empty by design).
Verify core agents are loaded:
`launchctl list | grep -E "com\.(bari|sefer)\."`
Expected: 11 entries (com.bari.morning-jazz, com.bari.morning-brief, com.bari.heartbeat, com.bari.evening-wrap, com.bari.weekly-wrap, com.bari.memory-maintenance, com.bari.meeting-reminder, com.sefer.pre-market-brief, com.sefer.post-market-brief, com.sefer.weekly-deep-dive, com.sefer.macro-readthrough).
If any are missing, reload from ~/Library/LaunchAgents/<label>.plist and alert Amanuel.

## 2. Unread Emails (2x daily, skip 22:00–08:00 CDT)
Flag anything urgent or from important contacts only.

## 3. Calendar (2x daily)
Surface events starting within 2 hours if not recently reminded.

## 4. Gateway Health (1x daily)
`openclaw status | grep -E "Gateway|Tailscale"` — alert if down or Tailscale serve is off.

# ANNOUNCE POLICY — deterministic, no judgment calls
When something is worth surfacing, pick the channel by RULE, not vibe:

**Voice (`say`)** — ONLY 08:00–22:00 CT, one sentence ≤20 words, and ONLY for:
1. ~~Calendar events starting soon~~ — NOT your job anymore: the `com.bari.meeting-reminder` LaunchAgent (every 5 min, deterministic) owns the "<20 minutes" voice announcement. You surface events 1–2h out via Telegram only.
2. An email that is BOTH time-sensitive today (meeting change, deadline today, approval blocking someone) AND from a sender on the VIP list at `/Users/amanuelmamo/Documents/Claude/Projects/Computer efficiency/Daily Brief/vip-senders.md` (or clearly a real person writing directly to Amanuel).
3. A system failure needing action from Amanuel today (e.g. auth expired, cron down).

**Telegram** — everything else worth flagging but not urgent-now: interesting emails, tomorrow's deadlines, FYIs, weekly items.

**Silence** — newsletters, job digests, promos, shipping, security notices, anything already covered in the 8am morning brief.

**Dedup rule:** before announcing, check `memory/heartbeat-state.json` → `announced` map (key = event id or message id, value = date). Never announce the same item twice. Add every announcement to the map; prune entries older than 2 days. If unsure whether an item qualifies for voice, it doesn't — use Telegram.

# State: memory/heartbeat-state.json
