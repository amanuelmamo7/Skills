#!/bin/bash
# weekly-wrap.sh
# Friday-afternoon weekly synthesis. Bari reads the week's daily memory files
# and produces a themed summary with patterns, time allocation, course
# corrections, and an honest "what got punted" list.
#
# Schedule (crontab):
#   0 16 * * 5 /Users/amanuelmamo/.openclaw/workspace/weekly-wrap.sh
#
# Logs to ~/.openclaw/workspace/logs/cron-YYYY-MM-DD-weekly-wrap.log

set -u

WORKSPACE="/Users/amanuelmamo/.openclaw/workspace"
CONFIG="$HOME/.openclaw/openclaw.json"
LOG="$HOME/.openclaw/workspace/logs/cron-$(date +%Y-%m-%d)-weekly-wrap.log"
mkdir -p "$(dirname "$LOG")"
GATEWAY_URL="http://127.0.0.1:18789/hooks/agent"
DATE=$(date +%Y-%m-%d)
# ISO week number for the filename
WEEK=$(date +%G-W%V)

echo "----" >> "$LOG"
echo "$(date): weekly-wrap triggered for $WEEK" >> "$LOG"

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
Weekly wrap for ISO week $WEEK (ending Friday $DATE).

FIRST — write a resume-protocol breadcrumb.
Before any other action, append this exact line to today's daily log
($WORKSPACE/memory/$DATE.md), creating the file if it doesn't exist:
  [intent] weekly wrap — reading week's morning/evening logs and synthesizing, ~120s, output memory/$WEEK-wrap.md
If this turn dies mid-task, the next session reads that line and resumes
per AGENTS.md §Resume Protocol. Only proceed after the breadcrumb is on disk.

1. Read all $WORKSPACE/memory/*-morning.md and *-evening.md files from this
   week (Monday through Friday). Also skim the raw $WORKSPACE/memory/YYYY-MM-DD.md
   files for the same range.
2. Synthesize patterns. Look for:
   - Themes — what was the week actually about? Don't just list activities.
   - Where time went vs. where Amanuel said priorities were on Monday.
   - Things that kept slipping (appeared on multiple "tomorrow" lists without
     getting done).
   - One or two genuine wins worth naming.
   - Things he punted that probably should not stay punted.
3. WRITE the synthesis to:
   $WORKSPACE/memory/$WEEK-wrap.md

   Structure:
   # Weekly Wrap - $WEEK

   ## Theme of the week
   One paragraph. What was this week really about? Be honest, not flattering.

   ## Wins
   - 2-4 concrete things that landed.

   ## Slip list
   - Things that kept moving forward without happening. Why?

   ## Time allocation
   - Where did the hours actually go? (Be qualitative — you don't have
     timesheets, just inference from the daily logs.)

   ## Course correction for next week
   - 1-3 specific shifts. Concrete enough to act on Monday morning.

   ## One question worth thinking about over the weekend
   - Something that emerged from the pattern. Not a to-do — a thinking
     prompt.

4. After writing the file, speak the "Theme of the week" paragraph and the
   "Course correction" section via \`say\` so Amanuel hears the framing even
   if he doesn't open the file.

5. Add a note to MEMORY.md under "## Weekly wraps" linking to the new file.
   Create that section if it doesn't exist.

Internal action only — do not send messages to channels. Do not deliver
the response to Telegram or any other channel. The result of this run is
the audio + the file on disk; nothing needs to be sent anywhere.
EOF

PAYLOAD=$("$JQ" -n --arg msg "$PROMPT" '{message: $msg, deliver: "none"}')

HTTP=$(curl -sS -o /tmp/bari-weekly-response.json -w "%{http_code}" \
  -X POST "$GATEWAY_URL" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  --max-time 30 \
  -d "$PAYLOAD")

echo "$(date): gateway responded HTTP $HTTP" >> "$LOG"

if [ "$HTTP" != "200" ] && [ "$HTTP" != "202" ]; then
  echo "$(date): ERROR — non-success response. See /tmp/bari-weekly-response.json" >> "$LOG"
  exit 1
fi

echo "$(date): done" >> "$LOG"
exit 0
