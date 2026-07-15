#!/bin/bash
# evening-wrap.sh
# End-of-workday wrap. Runs at 18:00 on weekdays.
# Bari assembles: what's on tomorrow's calendar, any unread email signal,
# how today's priorities went, and one suggested first task for tomorrow.
# Written to memory/YYYY-MM-DD-evening.md and also spoken if user is around.
#
# Schedule (crontab):
#   0 18 * * 1-5 /Users/amanuelmamo/.openclaw/workspace/evening-wrap.sh
#
# Logs to ~/.openclaw/workspace/logs/cron-YYYY-MM-DD-evening-wrap.log

set -u

WORKSPACE="/Users/amanuelmamo/.openclaw/workspace"
CONFIG="$HOME/.openclaw/openclaw.json"
LOG="$HOME/.openclaw/workspace/logs/cron-$(date +%Y-%m-%d)-evening-wrap.log"
mkdir -p "$(dirname "$LOG")"
GATEWAY_URL="http://127.0.0.1:18789/hooks/agent"
DATE=$(date +%Y-%m-%d)
TOMORROW=$(date -v+1d +%Y-%m-%d 2>/dev/null || date -d "tomorrow" +%Y-%m-%d)

echo "----" >> "$LOG"
echo "$(date): evening-wrap triggered" >> "$LOG"

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

BARI_TOKEN=$(cat "$HOME/.openclaw/workspace/secrets/bari-token.txt" 2>/dev/null | tr -d '[:space:]')
if [ -z "$BARI_TOKEN" ]; then
  echo "$(date): ERROR — could not read bari-token.txt" >> "$LOG"
  exit 1
fi

read -r -d '' PROMPT <<EOF
End-of-workday wrap for $DATE.

FIRST — write a resume-protocol breadcrumb.
Before any other action, append this exact line to today's daily log
($WORKSPACE/memory/$DATE.md), creating the file if it doesn't exist:
  [intent] evening wrap — synthesizing today + tomorrow's data, ~90s, output memory/$DATE-evening.md
If this turn dies mid-task, the next session reads that line and resumes
per AGENTS.md §Resume Protocol. Only proceed after the breadcrumb is on disk.

1. Read $WORKSPACE/memory/$DATE-morning.md (if it exists) to see what the
   morning brief flagged as today's Top 3 Priorities.
2. Check today's $WORKSPACE/memory/$DATE.md (raw daily log, if present) for
   any notable events or decisions Amanuel logged.
3. Fetch fresh data — verify by calling, not by reading memory notes:
   - Call: https://daily-brief-beta-neon.vercel.app/api/progress?bari=1&days=2
     (days=2 returns today + tomorrow's calendar in one payload — filter
     events whose start date is $TOMORROW for the look-ahead)
   - Header: x-bari-token: $BARI_TOKEN
   - This returns calendar + tasks + emails in one payload.
   - You need:
     • Tomorrow's calendar ($TOMORROW)
     • Any high-signal unread email since this morning
     • Any open tasks at or past their due date
   - If the call fails, run a fresh investigation in this turn — do NOT
     silently write "data unavailable" by trusting old notes.
3b. StreamSmart progress sync (keeps the Daily Brief hero ring honest).
   Read from /Users/amanuelmamo/dev/StreamEZ:
   - CHANGELOG.md — the newest "### <title> (YYYY-MM-DD)" heading = latest activity.
   - The status header (first ~10 lines) of each of: docs/WORKSTREAM_A.md,
     docs/WORKSTREAM_B_PRIME.md, docs/WORKSTREAM_C.md, docs/WORKSTREAM_D.md,
     docs/WORKSTREAM_E.md.
   - MASTER_PLAN.md build sequence only if a status header is ambiguous.
   Score progress with this FIXED rubric — same formula every night, so the
   ring never jitters from judgment drift (total 100):
   - Foundations (Phase 0 + Slice 0, both closed): 10 pts.
   - Workstreams A, B-prime, C, D, E: 15 pts each. Closed/complete = full 15.
     In-progress = 15 x (sub-steps DONE / sub-steps listed) — e.g. header says
     "E.0-E.7 DONE" and steps run E.0-E.8, that's 15 x 8/9.
   - Soft-launch polish (MASTER_PLAN weeks 19-20: v1 UI polish, beta invites):
     up to 15 pts, awarded ONLY on explicit CHANGELOG evidence.
   Count explicit blockers (a doc literally saying blocked/waiting-on) — else 0.
   Then POST exactly one update:
     curl -s -X POST https://daily-brief-beta-neon.vercel.app/api/progress \
       -H "x-bari-token: \$(cat $WORKSPACE/secrets/bari-token.txt)" \
       -H "Content-Type: application/json" \
       -d '{"streamsmart":{"tasksDone":<score>,"tasksTotal":100,"milestone":"<current in-progress workstream + next step>","latestActivity":"<newest changelog title (date)>","blockers":<n>}}'
   Confirm the response is {"ok":true...}. If the repo is unreadable or the
   POST fails, note it in the wrap and move on — never invent a score.

4. Synthesize a short wrap with this structure, and WRITE IT to
   $WORKSPACE/memory/$DATE-evening.md
   (add a "## StreamSmart" line with the score, milestone, and latest ship):

   # Evening Wrap - $DATE

   ## How today went
   - For each of the morning's Top 3 Priorities, say (Done / In Progress /
     Not Started / Unclear) based on what you can verify. If you can't tell,
     say so honestly rather than guessing.

   ## Tomorrow's setup
   - Top calendar events ($TOMORROW), with time blocks visible.
   - Any unread email worth seeing tonight (signal only — skip newsletters).
   - Overdue tasks.

   ## Suggested first task for tomorrow
   - One specific thing, chosen to get momentum, not to be heroic.

   ## Question for Amanuel
   - One short question only if there's something genuinely unclear you'd
     want him to clarify before tomorrow. Skip if nothing.

5. After writing the file, speak ONLY the "Tomorrow's setup" and "Suggested
   first task" sections via \`say\` so Amanuel hears the future-facing part
   even if he's not at his computer.

Internal action only — do not send messages to channels. Do not deliver
the response to Telegram or any other channel. The result of this run is
the audio + the file on disk; nothing needs to be sent anywhere.
EOF

PAYLOAD=$("$JQ" -n --arg msg "$PROMPT" '{message: $msg, deliver: "none"}')

HTTP=$(curl -sS -o /tmp/bari-evening-response.json -w "%{http_code}" \
  -X POST "$GATEWAY_URL" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  --max-time 30 \
  -d "$PAYLOAD")

echo "$(date): gateway responded HTTP $HTTP" >> "$LOG"

if [ "$HTTP" != "200" ] && [ "$HTTP" != "202" ]; then
  echo "$(date): ERROR — non-success response. See /tmp/bari-evening-response.json" >> "$LOG"
  exit 1
fi

echo "$(date): done" >> "$LOG"
exit 0
