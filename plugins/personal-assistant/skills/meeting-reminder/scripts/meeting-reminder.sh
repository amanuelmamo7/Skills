#!/bin/bash
# meeting-reminder.sh — deterministic voice reminders for upcoming meetings.
#
# Runs every 5 minutes via launchd (com.bari.meeting-reminder). NO LLM in the
# loop: fetches today's calendar from the Daily Brief bari export, and if a
# timed event starts within the next 20 minutes, announces it once via `say`.
# Dedup state lives in memory/meeting-reminder-state.json so an event is
# never announced twice. Quiet hours: silent before 08:00 and after 22:00.
#
# Built 2026-07-07 as part of the EA stack. Bari's heartbeat must NOT also
# voice-announce meetings (see HEARTBEAT.md announce policy) — this daemon
# owns that job.

set -u

WORKSPACE="$HOME/.openclaw/workspace"
STATE="$WORKSPACE/memory/meeting-reminder-state.json"
LOG="$WORKSPACE/logs/meeting-reminder.log"
mkdir -p "$WORKSPACE/memory" "$WORKSPACE/logs"

ts() { date -Iseconds; }
log() { echo "$(ts) $*" >> "$LOG"; }

# Keep the rolling log small.
if [ -f "$LOG" ] && [ "$(wc -c < "$LOG" | tr -d ' ')" -gt 200000 ]; then
  tail -c 50000 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"
fi

# Quiet hours: 22:00–08:00.
HOUR=$(date +%H)
if [ "$HOUR" -lt 8 ] || [ "$HOUR" -ge 22 ]; then exit 0; fi

JQ="/opt/homebrew/bin/jq"; command -v jq >/dev/null 2>&1 && JQ="$(command -v jq)"
[ -x "$JQ" ] || { log "FATAL: jq not found"; exit 1; }

BARI_TOKEN=$(tr -d '[:space:]' < "$WORKSPACE/secrets/bari-token.txt" 2>/dev/null || true)
[ -n "$BARI_TOKEN" ] || { log "FATAL: bari-token.txt missing/empty"; exit 1; }

RESP=$(curl -s --max-time 20 -H "x-bari-token: $BARI_TOKEN" \
  "https://daily-brief-beta-neon.vercel.app/api/progress?bari=1") || { log "WARN: fetch failed (network?)"; exit 0; }

echo "$RESP" | "$JQ" -e '.calendar' >/dev/null 2>&1 || {
  log "WARN: unexpected payload: $(echo "$RESP" | head -c 150)"; exit 0; }

[ -f "$STATE" ] || echo '{}' > "$STATE"
NOW=$(date +%s)
LEAD_MAX=1200  # announce when event starts within 20 minutes

# Timed events only (dateTime contains "T"; all-day events are bare dates).
echo "$RESP" | "$JQ" -c '.calendar[] | select((.time // "") | test("T"))' | while read -r EV; do
  START_RAW=$(echo "$EV" | "$JQ" -r '.time')
  TITLE=$(echo "$EV" | "$JQ" -r '.summary // "an untitled event"')
  # Parse the local wall-clock portion (offset in payload is local anyway).
  START=$(date -j -f "%Y-%m-%dT%H:%M:%S" "$(echo "$START_RAW" | cut -c1-19)" +%s 2>/dev/null) || continue
  DELTA=$(( START - NOW ))
  { [ "$DELTA" -gt 0 ] && [ "$DELTA" -le "$LEAD_MAX" ]; } || continue
  KEY=$(printf '%s|%s' "$START_RAW" "$TITLE" | /sbin/md5)
  ALREADY=$("$JQ" -r --arg k "$KEY" '.[$k] // empty' "$STATE")
  [ -n "$ALREADY" ] && continue
  MINS=$(( (DELTA + 59) / 60 ))
  log "announcing: \"$TITLE\" in ${MINS}m (start $START_RAW)"
  /usr/bin/say "Heads up — $TITLE starts in $MINS minutes." >> "$LOG" 2>&1
  "$JQ" --arg k "$KEY" --arg d "$(date +%Y-%m-%d)" '.[$k] = $d' "$STATE" > "$STATE.tmp" \
    && mv "$STATE.tmp" "$STATE"
done

# Prune dedup entries older than yesterday.
TODAY=$(date +%Y-%m-%d); YDAY=$(date -v-1d +%Y-%m-%d)
"$JQ" --arg t "$TODAY" --arg y "$YDAY" \
  'with_entries(select(.value == $t or .value == $y))' "$STATE" > "$STATE.tmp" \
  && mv "$STATE.tmp" "$STATE"
exit 0
