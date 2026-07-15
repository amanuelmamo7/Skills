#!/bin/bash
# heartbeat.sh
# Fires a heartbeat to Bari every 2 hours during waking time. Bari processes
# the heartbeat per HEARTBEAT.md (rotating through email / calendar / cron
# health / mentions) and decides whether to interrupt or stay quiet.
#
# Schedule (crontab):
#   0 9,11,13,15,17,19 * * 1-5 /Users/amanuelmamo/.openclaw/workspace/heartbeat.sh
#
# Logs to ~/.openclaw/workspace/logs/cron-YYYY-MM-DD-heartbeat.log

set -u

WORKSPACE="/Users/amanuelmamo/.openclaw/workspace"
CONFIG="$HOME/.openclaw/openclaw.json"
LOG="$HOME/.openclaw/workspace/logs/cron-$(date +%Y-%m-%d)-heartbeat.log"
mkdir -p "$(dirname "$LOG")"
GATEWAY_URL="http://127.0.0.1:18789/hooks/agent"

echo "----" >> "$LOG"
echo "$(date): heartbeat triggered" >> "$LOG"

if ! command -v jq >/dev/null 2>&1; then
  JQ="/opt/homebrew/bin/jq"
  if [ ! -x "$JQ" ]; then
    echo "$(date): ERROR — jq not found. Install with: brew install jq" >> "$LOG"
    exit 1
  fi
else
  JQ=$(command -v jq)
fi

TOKEN=$("$JQ" -r '.hooks.token // empty' "$CONFIG" 2>>"$LOG")
if [ -z "$TOKEN" ] || [ "$TOKEN" = "null" ]; then
  echo "$(date): ERROR — could not extract hooks.token from $CONFIG" >> "$LOG"
  exit 1
fi

read -r -d '' PROMPT <<EOF
HEARTBEAT.

FIRST — write a resume-protocol breadcrumb.
Before doing the rotation check below, append this exact line to today's
daily log ($WORKSPACE/memory/$(date +%Y-%m-%d).md), creating the file if
it doesn't exist:
  [intent] heartbeat — rotating per HEARTBEAT.md, ~15s, may alert via say
This is light overhead but it makes the heartbeat trail visible to any
resume session per AGENTS.md §Resume Protocol. Skip the breadcrumb only
if you are *certain* you will immediately reply HEARTBEAT_OK with no
side effects.

Follow the rotation defined in HEARTBEAT.md. Read memory/heartbeat-state.json
to see what you checked last, pick the next item in the rotation, and run
that check.

Rules of engagement:

- If everything is normal and nothing needs Amanuel's attention, reply with
  HEARTBEAT_OK and update memory/heartbeat-state.json with the timestamp of
  this check. Do not message any channel. Do not say anything aloud.

- If something IS worth surfacing (urgent email from an important contact,
  calendar event starting in under 2 hours and not previously surfaced,
  morning jazz cron missing, gateway/Tailscale health degraded, anything
  genuinely time-sensitive), then:
    1. Write the finding to memory/heartbeat-state.json under "lastAlert"
       with a short description and timestamp.
    2. Speak a one-sentence headline via the \`say\` command so Amanuel
       hears it if nearby. Example: "Heads up — meeting with Sam at 3 PM
       starts in 90 minutes."
    3. Also append a one-line entry to today's memory/YYYY-MM-DD.md log so
       there's a written trail.

- Respect Amanuel's quiet hours (22:00–08:00 CDT). If the current local
  time is in that window, only react to genuinely urgent items; otherwise
  silently update state and exit.

- Be conservative about interruption. Erring toward "stay quiet" is the
  correct default. Don't surface routine traffic, newsletters, automated
  notifications, or low-stakes items.

Internal action only — do not send messages to channels. Do not deliver
the response to Telegram or any other channel. If something is worth
surfacing, the \`say\` command + memory file IS the surfacing — that's
the channel-free path. The hook is not a notification pipe.
EOF

PAYLOAD=$("$JQ" -n --arg msg "$PROMPT" '{agentId: "main", message: $msg}')

HTTP=$(curl -sS -o /tmp/bari-heartbeat-response.json -w "%{http_code}" \
  -X POST "$GATEWAY_URL" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  --max-time 30 \
  -d "$PAYLOAD")

echo "$(date): gateway responded HTTP $HTTP" >> "$LOG"

if [ "$HTTP" != "200" ] && [ "$HTTP" != "202" ]; then
  echo "$(date): ERROR — non-success response. See /tmp/bari-heartbeat-response.json" >> "$LOG"
  exit 1
fi

echo "$(date): done" >> "$LOG"
exit 0
