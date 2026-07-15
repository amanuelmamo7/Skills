#!/bin/bash
# pre-market-brief.sh — Sefer's 8 AM weekday pre-market brief
#
# Pattern: synchronous delivery (Approach B).
# - Submits the hook to fire Sefer (the agent).
# - Polls inline (no background subshell) for the brief file to appear.
# - Invokes `say` reading the audio sidecar.
# - POSTs the Telegram sidecar to the bot with HTTP code capture.
#
# Why synchronous: the previous version forked the delivery to a background
# subshell with `(...) &` and the subshell was reaped before the brief landed.
# Holds the cron slot for up to ~40 minutes worst case; ~4 min typical.
#
# Schedule: 0 8 * * 1-5 /Users/amanuelmamo/.openclaw/workspace-sefer/pre-market-brief.sh
# Log:      ~/.openclaw/workspace-sefer/logs/cron-YYYY-MM-DD-pre-market-brief.log
# Backup of prior version: pre-market-brief.sh.pre-sync-patch-<stamp>.bak

set -uo pipefail
# NOTE: not using `-e` so a failed delivery step is logged but doesn't abort
# subsequent steps. Each step checks its own exit status explicitly.

CONFIG="$HOME/.openclaw/openclaw.json"
WORKSPACE="$HOME/.openclaw/workspace-sefer"
DATE=$(date +%Y-%m-%d)
LOG="$WORKSPACE/logs/cron-${DATE}-pre-market-brief.log"
mkdir -p "$(dirname "$LOG")"

ts() { date -Iseconds; }
log() { echo "$(ts) $*" >> "$LOG"; }

log "===== pre-market-brief.sh start ====="

# --- credentials -----------------------------------------------------------
TOKEN=$(jq -r '.hooks.token // empty' "$CONFIG" 2>>"$LOG")
BOT_TOKEN=$(jq -r '.channels.telegram.botToken // empty' "$CONFIG" 2>>"$LOG")
CHAT_ID="2076378504"

if [ -z "$TOKEN" ] || [ "$TOKEN" = "null" ]; then
  log "FATAL: hooks.token missing from $CONFIG"
  exit 1
fi
if [ -z "$BOT_TOKEN" ] || [ "$BOT_TOKEN" = "null" ]; then
  log "FATAL: channels.telegram.botToken missing from $CONFIG"
  exit 1
fi

# --- prompt ----------------------------------------------------------------
PROMPT_FILE="$WORKSPACE/prompts/pre-market-brief.txt"
if [ ! -f "$PROMPT_FILE" ]; then
  log "FATAL: prompt file missing at $PROMPT_FILE"
  exit 1
fi
PROMPT=$(cat "$PROMPT_FILE")

# --- 1/4 fire hook ---------------------------------------------------------
log "[1/4] submitting hook to gateway"
HOOK_PAYLOAD=$(jq -nc --arg agent "sefer" --arg msg "$PROMPT" \
  '{agentId:$agent, message:$msg, timeoutSeconds:1800}')
HOOK_RESPONSE=$(curl -sS --max-time 600 -X POST "http://127.0.0.1:18789/hooks/agent" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "$HOOK_PAYLOAD" 2>>"$LOG") || {
  log "[1/4] FATAL: hook POST curl failed exit=$?"
  exit 1
}
log "[1/4] hook response: $HOOK_RESPONSE"

# --- 2/4 poll for brief file ----------------------------------------------
BRIEF="$WORKSPACE/memory/${DATE}-pre-market.md"
AUDIO="$WORKSPACE/memory/${DATE}-pre-market-audio.txt"
TELEGRAM="$WORKSPACE/memory/${DATE}-pre-market-telegram.txt"
DIGEST="$WORKSPACE/memory/${DATE}-pre-market.json"

log "[2/4] polling for $BRIEF (up to 40 minutes, 30s intervals)"
POLL_START=$(date +%s)
for i in $(seq 1 80); do
  [ -f "$BRIEF" ] && break
  sleep 30
done
POLL_ELAPSED=$(( $(date +%s) - POLL_START ))

if [ ! -f "$BRIEF" ]; then
  log "[2/4] ERROR: brief never appeared after ${POLL_ELAPSED}s"
  # Send failure alert (best-effort; may also fail)
  GWERR=$(grep -o 'error="[^"]*' "/private/tmp/openclaw/openclaw-$(date +%Y-%m-%d).log" 2>/dev/null | tail -1 | head -c 200)
  curl -s --max-time 30 -X POST \
    "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
    -d "chat_id=${CHAT_ID}" \
    --data-urlencode "text=Sefer pre-market: brief not delivered — timed out after ${POLL_ELAPSED}s. Gateway said: ${GWERR:-no error logged}. Log: $LOG" \
    >> "$LOG" 2>&1 || log "[2/4] WARN: failure-alert Telegram POST also failed"
  exit 1
fi
log "[2/4] brief landed after ${POLL_ELAPSED}s ($(wc -l < "$BRIEF") lines)"

# --- 2b settle: wait for trailing sidecars ---------------------------------
# Sefer writes the .md FIRST, then audio/telegram/json over the next 10-60s.
# Without this wait we race ahead and skip them all. The JSON digest is the
# last file Sefer writes, so once it exists the others are present too.
log "[2b/4] waiting up to 300s for sidecars (JSON digest last) to settle"
for i in $(seq 1 60); do [ -f "$DIGEST" ] && break; sleep 5; done
[ -f "$DIGEST" ] && log "[2b/4] sidecars settled" || log "[2b/4] WARN: JSON digest never arrived; proceeding (steps self-check)"

# --- 3/4 audio via macOS say -----------------------------------------------
if [ -f "$AUDIO" ]; then
  AUDIO_BYTES=$(wc -c < "$AUDIO" | tr -d ' ')
  log "[3/4] invoking /usr/bin/say (audio sidecar: ${AUDIO_BYTES} bytes)"
  if /usr/bin/say "$(cat "$AUDIO")" >> "$LOG" 2>&1; then
    log "[3/4] say returned exit 0"
  else
    SAY_RC=$?
    log "[3/4] WARN: say failed exit=${SAY_RC}"
  fi
else
  log "[3/4] SKIP: no audio sidecar at $AUDIO"
fi

# --- 4/4 Telegram delivery -------------------------------------------------
if [ -f "$TELEGRAM" ]; then
  TG_BYTES=$(wc -c < "$TELEGRAM" | tr -d ' ')
  log "[4/4] POSTing telegram sidecar (${TG_BYTES} bytes) to chat ${CHAT_ID}"
  TG_RESP_FILE=$(mktemp /tmp/sefer-tg-response.XXXXXX)
  HTTP_CODE=$(curl -s -o "$TG_RESP_FILE" -w "%{http_code}" --max-time 30 \
    -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
    -d "chat_id=${CHAT_ID}" \
    --data-urlencode "text=$(cat "$TELEGRAM")" 2>>"$LOG") || HTTP_CODE="curl-failed"
  TG_BODY=$(cat "$TG_RESP_FILE" 2>/dev/null | head -c 500)
  rm -f "$TG_RESP_FILE"
  log "[4/4] Telegram HTTP ${HTTP_CODE}: ${TG_BODY}"
  case "$HTTP_CODE" in
    200) log "[4/4] Telegram delivered OK" ;;
    *)   log "[4/4] WARN: Telegram non-200 (${HTTP_CODE})" ;;
  esac
else
  log "[4/4] SKIP: no telegram sidecar at $TELEGRAM"
fi

# --- 5/5 Daily Brief dashboard POST ----------------------------------------
# Best-effort: pushes the brief (full markdown + JSON digest + audio + telegram)
# to the Daily Brief web app so the Finance tab renders it. Never aborts the run.
FINANCE_URL="https://daily-brief-beta-neon.vercel.app/api/finance"
FINANCE_TOKEN_FILE="$WORKSPACE/secrets/finance-token"
if [ ! -f "$FINANCE_TOKEN_FILE" ]; then
  log "[5/5] SKIP: no finance token at $FINANCE_TOKEN_FILE"
elif [ ! -f "$DIGEST" ]; then
  log "[5/5] SKIP: no JSON digest at $DIGEST"
elif ! jq empty "$DIGEST" 2>>"$LOG"; then
  log "[5/5] SKIP: digest is not valid JSON ($DIGEST)"
else
  FIN_TOKEN=$(tr -d ' \t\r\n' < "$FINANCE_TOKEN_FILE")
  AUDIO_TXT=""; [ -f "$AUDIO" ] && AUDIO_TXT=$(cat "$AUDIO")
  TG_TXT="";    [ -f "$TELEGRAM" ] && TG_TXT=$(cat "$TELEGRAM")
  POST_BODY=$(jq -nc \
    --arg cadence "pre-market" \
    --arg md "$(cat "$BRIEF")" \
    --arg audio "$AUDIO_TXT" \
    --arg telegram "$TG_TXT" \
    --slurpfile digest "$DIGEST" \
    '{cadence:$cadence, markdown:$md, audio:$audio, telegram:$telegram,
      headline:($digest[0].headline // ""), sections:($digest[0].sections // [])}' 2>>"$LOG")
  if [ -z "$POST_BODY" ]; then
    log "[5/5] ERROR: failed to assemble POST body"
  else
    FIN_RESP_FILE=$(mktemp /tmp/sefer-finance.XXXXXX)
    FIN_CODE=$(curl -s -o "$FIN_RESP_FILE" -w "%{http_code}" --max-time 30 \
      -X POST "$FINANCE_URL" \
      -H "Authorization: Bearer $FIN_TOKEN" \
      -H "Content-Type: application/json" \
      -d "$POST_BODY" 2>>"$LOG") || FIN_CODE="curl-failed"
    FIN_BODY=$(head -c 300 "$FIN_RESP_FILE" 2>/dev/null); rm -f "$FIN_RESP_FILE"
    case "$FIN_CODE" in
      200) log "[5/5] dashboard POST OK: ${FIN_BODY}" ;;
      *)   log "[5/5] WARN: dashboard POST HTTP ${FIN_CODE}: ${FIN_BODY}" ;;
    esac
  fi
fi

log "===== pre-market-brief.sh complete ====="
