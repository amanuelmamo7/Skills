#!/bin/bash
# memory-maintenance.sh
# Sunday-morning memory housekeeping. Bari reads the past week's raw daily
# logs and distills durable insights into MEMORY.md so context survives even
# if individual daily logs get pruned later.
#
# Schedule (crontab):
#   0 9 * * 0 /Users/amanuelmamo/.openclaw/workspace/memory-maintenance.sh
#
# Logs to ~/.openclaw/workspace/logs/cron-YYYY-MM-DD-memory-maintenance.log

set -u

WORKSPACE="/Users/amanuelmamo/.openclaw/workspace"
CONFIG="$HOME/.openclaw/openclaw.json"
LOG="$HOME/.openclaw/workspace/logs/cron-$(date +%Y-%m-%d)-memory-maintenance.log"
mkdir -p "$(dirname "$LOG")"
GATEWAY_URL="http://127.0.0.1:18789/hooks/agent"

echo "----" >> "$LOG"
echo "$(date): memory-maintenance triggered" >> "$LOG"

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
Weekly memory maintenance.

FIRST — write a resume-protocol breadcrumb.
Before any other action, append this exact line to today's daily log
($WORKSPACE/memory/$(date +%Y-%m-%d).md), creating the file if it doesn't exist:
  [intent] memory maintenance — curating week's raw logs into MEMORY.md, ~180s, output MEMORY.md + USER.md updates
If this turn dies mid-task (this run reads many files and reasons over
them — high risk of long silent stretches), the next session reads that
line and resumes per AGENTS.md §Resume Protocol. Only proceed after the
breadcrumb is on disk.

1. Read the last 7 days of $WORKSPACE/memory/YYYY-MM-DD.md raw logs.
2. Read the last 1-2 weeks of $WORKSPACE/memory/*-wrap.md weekly wraps if
   present.
3. Read the current $WORKSPACE/MEMORY.md so you don't duplicate what's
   already curated.
4. Identify what's worth promoting from raw logs into long-term memory:
   - New durable facts about Amanuel's preferences, projects, or context
   - Lessons learned that should not be re-learned
   - Patterns you noticed (e.g., "Amanuel consistently underestimates X")
   - Project-specific notes that belong in memory/project_<name>.md (create
     new project files when appropriate)
   - Style/communication preferences he expressed
5. UPDATE $WORKSPACE/MEMORY.md by:
   - Adding new entries under appropriate sections (About Amanuel, Feedback
     & Style, Projects & Context, etc.)
   - Linking to new project files in memory/ if you created any
   - Pruning entries that are now stale or have been superseded
   - Keeping MEMORY.md scannable — index-like, links to detail files, not a
     wall of text
6. UPDATE $WORKSPACE/USER.md if you learned anything durable about him this
   week that wasn't there before (new preferences, new context, new
   working agreements).
7. Append a one-line summary of what you promoted to memory/YYYY-MM-DD.md
   (today's date) so the trail of curation work is visible.

Be conservative — only promote things that are genuinely durable. If
something might be a one-time situation, leave it in the daily log and
revisit next week.

Do not delete raw daily logs. Daily logs are append-only; MEMORY.md is the
curated layer on top.

Internal action only — do not send messages to channels. Do not deliver
the response to Telegram or any other channel. The result of this run is
the updated memory files on disk; nothing needs to be sent anywhere.
EOF

PAYLOAD=$("$JQ" -n --arg msg "$PROMPT" '{message: $msg, deliver: "none"}')

HTTP=$(curl -sS -o /tmp/bari-memory-response.json -w "%{http_code}" \
  -X POST "$GATEWAY_URL" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  --max-time 30 \
  -d "$PAYLOAD")

echo "$(date): gateway responded HTTP $HTTP" >> "$LOG"

if [ "$HTTP" != "200" ] && [ "$HTTP" != "202" ]; then
  echo "$(date): ERROR — non-success response. See /tmp/bari-memory-response.json" >> "$LOG"
  exit 1
fi

echo "$(date): done" >> "$LOG"
exit 0
