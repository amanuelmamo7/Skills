#!/bin/bash
# morning-brief.sh
# Triggers Bari's daily brief at 7:00 AM weekdays.
# (1) Speaks the brief aloud via Sonos (Family Room speaker).
# (2) Writes a text version to memory/YYYY-MM-DD-morning.md for skim-later.
#
# Schedule (crontab):
#   0 7 * * 1-5 /Users/amanuelmamo/.openclaw/workspace/morning-brief.sh
#
# Logs to ~/.openclaw/workspace/logs/cron-YYYY-MM-DD-morning-brief.log

set -u

WORKSPACE="/Users/amanuelmamo/.openclaw/workspace"
CONFIG="$HOME/.openclaw/openclaw.json"
LOG="$HOME/.openclaw/workspace/logs/cron-$(date +%Y-%m-%d)-morning-brief.log"
mkdir -p "$(dirname "$LOG")"
GATEWAY_URL="http://127.0.0.1:18789/hooks/agent"
DATE=$(date +%Y-%m-%d)

echo "----" >> "$LOG"
echo "$(date): morning-brief triggered" >> "$LOG"

# Need jq for safe JSON token extraction and payload construction.
if ! command -v jq >/dev/null 2>&1; then
  JQ="/opt/homebrew/bin/jq"
  if [ ! -x "$JQ" ]; then
    echo "$(date): ERROR — jq not found. Install with: brew install jq" >> "$LOG"
    exit 1
  fi
else
  JQ=$(command -v jq)
fi

# Pull tokens from openclaw.json so we never hard-code secrets.
TOKEN=$("$JQ" -r '.hooks.token // empty' "$CONFIG" 2>>"$LOG")
if [ -z "$TOKEN" ] || [ "$TOKEN" = "null" ]; then
  echo "$(date): ERROR — could not extract hooks.token from $CONFIG" >> "$LOG"
  exit 1
fi

BARI_TOKEN=$(cat "$HOME/.openclaw/workspace/secrets/bari-token.txt" 2>/dev/null | tr -d '[:space:]')
if [ -z "$BARI_TOKEN" ]; then
  echo "$(date): ERROR — could not read bari-token.txt" >> "$LOG"
  exit 1
fi

# Compose the prompt Bari will receive via the gateway webhook.
read -r -d '' PROMPT <<EOF
Run the daily morning brief.

FIRST — write a resume-protocol breadcrumb.
Before any other action, append this exact line to today's daily log
($WORKSPACE/memory/$DATE.md), creating the file if it doesn't exist:
  [intent] morning brief — fetching Daily Brief, ~60s, output memory/$DATE-morning.md
If this turn dies mid-task, the next session reads that line and resumes
per AGENTS.md §Resume Protocol. Only proceed after the breadcrumb is on disk.

DATA SOURCES — verify by calling, not by reading memory notes:

1. Call the Daily Brief Bari endpoint FIRST, before consulting any project
   memory file about what auth works:
     URL: https://daily-brief-beta-neon.vercel.app/api/progress?bari=1
     Header: x-bari-token: $BARI_TOKEN
   This single call returns calendar + tasks + unread email in one payload.
   If that call fails, run a fresh investigation (test other header styles,
   other routes) — do NOT silently fall back to "data unavailable." A 401
   means the auth pattern changed; figure it out in this run.

2. Markets and weather: call those endpoints (or public sources) directly.
   Weather location: Dallas, TX (not Chicago — same timezone, wrong city).

3. News: any reasonable public source is fine.

DELIVERY:

4. Speak the brief aloud through the Sonos "Family Room" speaker using this
   exact sequence of bash commands (run them, do not skip):

   a. Generate the audio file:
        say -o /tmp/morning-brief.aiff "<brief text here>"
        ffmpeg -i /tmp/morning-brief.aiff -acodec libmp3lame -q:a 4 /tmp/morning-brief.mp3 -y -loglevel error

   b. Get the Mac's LAN IP and start a temporary HTTP server:
        LAN_IP=\$(ipconfig getifaddr en0 || ipconfig getifaddr en1)
        python3 -m http.server 18766 --bind 0.0.0.0 --directory /tmp &
        HTTP_PID=\$!
        sleep 1

   c. Play on Sonos, wait for it to finish, then clean up:
        sonos volume set --name "Family Room" 55
        sonos play-uri --name "Family Room" "http://\${LAN_IP}:18766/morning-brief.mp3"
        sleep 120
        kill \$HTTP_PID 2>/dev/null

   Keep the spoken text under ~90 seconds — highest-signal items only.
   When addressing Amanuel by name in the spoken text, use the phonetic
   spelling "uh-manual" so macOS `say` pronounces it correctly.

5. Write the same brief in text form to
   $WORKSPACE/memory/$DATE-morning.md
   with this structure:
     # Morning Brief - $DATE
     ## Calendar
     ## Unread Email (signal only)
     ## Tasks
     ## Markets / Weather
     ## Top 3 Priorities for Today
6. Append a one-line entry to memory/$DATE.md if it exists, otherwise create
   it: "morning brief delivered at \$(date +%H:%M)".

Internal action only — do not send messages to channels. Do not deliver
the response to Telegram or any other channel. The result of this run is
the audio + the file on disk; nothing needs to be sent anywhere.
EOF

# Build the JSON payload safely via jq so quotes and newlines escape correctly.
PAYLOAD=$("$JQ" -n --arg msg "$PROMPT" '{agentId: "main", message: $msg}')

# Fire-and-forget POST to the gateway webhook.
HTTP=$(curl -sS -o /tmp/bari-morning-response.json -w "%{http_code}" \
  -X POST "$GATEWAY_URL" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  --max-time 30 \
  -d "$PAYLOAD")

echo "$(date): gateway responded HTTP $HTTP" >> "$LOG"

if [ "$HTTP" != "200" ] && [ "$HTTP" != "202" ]; then
  echo "$(date): ERROR — non-success response. See /tmp/bari-morning-response.json" >> "$LOG"
  exit 1
fi

echo "$(date): done" >> "$LOG"
exit 0
