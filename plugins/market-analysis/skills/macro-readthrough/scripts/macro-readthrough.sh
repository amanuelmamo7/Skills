#!/bin/bash
# macro-readthrough.sh — Sefer's 1st-of-month macro readthrough
#
# Pattern: SYNCHRONOUS delivery. The old version forked delivery into a
# detached `( ... ) &` subshell and the main script exited immediately — cron
# reaped the subshell before it polled/delivered, so macro would never deliver
# to Telegram or the dashboard. Now we poll + deliver inline.
#
# Not using `set -e`: a failed delivery step is logged, not fatal.

set -uo pipefail

CONFIG="$HOME/.openclaw/openclaw.json"
WORKSPACE="$HOME/.openclaw/workspace-sefer"
MONTH=$(date -v-1m +%Y-%m)
LOG="$WORKSPACE/logs/cron-$(date +%Y-%m-%d)-macro-readthrough.log"
mkdir -p "$(dirname "$LOG")"

ts() { date -Iseconds; }
log() { echo "$(ts) $*" >> "$LOG"; }

log "===== macro-readthrough.sh start ($MONTH) ====="

TOKEN=$(jq -r '.hooks.token // empty' "$CONFIG" 2>>"$LOG")
BOT_TOKEN=$(jq -r '.channels.telegram.botToken // empty' "$CONFIG" 2>>"$LOG")
CHAT_ID="2076378504"

if [ -z "$TOKEN" ] || [ "$TOKEN" = "null" ]; then
  log "FATAL: hooks.token missing from $CONFIG"; exit 1
fi

PROMPT=$(cat "$WORKSPACE/prompts/macro-readthrough.txt")

# --- fire hook (returns immediately with runId; agent runs async) -----------
log "[1/4] submitting hook to gateway"
HOOK_RESPONSE=$(curl -sS --max-time 600 -X POST "http://127.0.0.1:18789/hooks/agent" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d "$(jq -nc --arg agent "sefer" --arg msg "$PROMPT" '{agentId:$agent, message:$msg, timeoutSeconds:1800}')" 2>>"$LOG")
log "[1/4] hook response: $HOOK_RESPONSE"

BRIEF="$WORKSPACE/memory/${MONTH}-macro.md"
TELEGRAM="$WORKSPACE/memory/${MONTH}-macro-telegram.txt"
DIGEST="$WORKSPACE/memory/${MONTH}-macro.json"

# --- poll for the brief (up to 40 min) -------------------------------------
log "[2/4] polling for $BRIEF (up to 40 minutes, 30s intervals)"
for i in $(seq 1 80); do [ -f "$BRIEF" ] && break; sleep 30; done
if [ ! -f "$BRIEF" ]; then
  log "[2/4] ERROR: macro brief never appeared after ~40min"
  GWERR=$(grep -o 'error="[^"]*' "/private/tmp/openclaw/openclaw-$(date +%Y-%m-%d).log" 2>/dev/null | tail -1 | head -c 200)
  curl -s --max-time 30 -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
    -d "chat_id=${CHAT_ID}" \
    --data-urlencode "text=Sefer macro-readthrough: brief not delivered — timed out. Gateway said: ${GWERR:-no error logged}. Log: $LOG" \
    >> "$LOG" 2>&1 || log "[2/4] WARN: failure-alert Telegram also failed"
  exit 1
fi
log "[2/4] brief landed ($(wc -l < "$BRIEF") lines)"

# --- settle: sidecars (telegram + JSON digest) land a few seconds after .md -
for i in $(seq 1 60); do [ -f "$DIGEST" ] && break; sleep 5; done

# --- 3/4 Telegram delivery -------------------------------------------------
if [ -f "$TELEGRAM" ]; then
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 30 -X POST \
    "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
    -d "chat_id=${CHAT_ID}" --data-urlencode "text=$(cat "$TELEGRAM")" 2>>"$LOG") || HTTP_CODE="curl-failed"
  log "[3/4] Telegram HTTP ${HTTP_CODE}"
else
  log "[3/4] SKIP: no telegram sidecar"
fi

# --- 4/4 Daily Brief dashboard POST ----------------------------------------
FINANCE_TOKEN_FILE="$WORKSPACE/secrets/finance-token"
if [ ! -f "$FINANCE_TOKEN_FILE" ]; then
  log "[4/4] SKIP: no finance token"
elif [ ! -f "$DIGEST" ]; then
  log "[4/4] SKIP: no JSON digest at $DIGEST"
elif ! jq empty "$DIGEST" 2>>"$LOG"; then
  log "[4/4] SKIP: digest is not valid JSON"
else
  FIN_TOKEN=$(tr -d ' \t\r\n' < "$FINANCE_TOKEN_FILE")
  TG_TXT=""; [ -f "$TELEGRAM" ] && TG_TXT=$(cat "$TELEGRAM")
  POST_BODY=$(jq -nc --arg cadence "macro" --arg md "$(cat "$BRIEF")" --arg telegram "$TG_TXT" \
    --slurpfile digest "$DIGEST" \
    '{cadence:$cadence, markdown:$md, telegram:$telegram, headline:($digest[0].headline // ""), sections:($digest[0].sections // [])}' 2>>"$LOG")
  if [ -z "$POST_BODY" ]; then
    log "[4/4] ERROR: failed to assemble POST body"
  else
    FIN_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 30 -X POST \
      "https://daily-brief-beta-neon.vercel.app/api/finance" \
      -H "Authorization: Bearer $FIN_TOKEN" -H "Content-Type: application/json" \
      -d "$POST_BODY" 2>>"$LOG") || FIN_CODE="curl-failed"
    log "[4/4] dashboard POST HTTP ${FIN_CODE}"
  fi
fi

log "===== macro-readthrough.sh complete ====="
