#!/bin/bash
# Morning music alarm — Family Room Sonos
# Rewritten 2026-06-04: curl-only SOAP (no `sonos` CLI).
# WHY: the sonos binary is ad-hoc signed; macOS Local Network privacy
# silently denies it (EHOSTUNREACH) when spawned by launchd. Apple-signed
# curl/ping/nc are exempt — verified 2026-06-04 via launchd-context probe.
# BEHAVIOR: picks a RANDOM playable Sonos favorite each morning, enables
# shuffle mode, sets volume, plays. Retries next favorite on failure.

IP="192.168.1.XXX"            # your speaker's LAN IP
BASE="http://$IP:1400"
VOLUME="40"
LOG="$HOME/.assistant/logs/cron-$(date +%Y-%m-%d)-morning-music.log"
mkdir -p "$(dirname "$LOG")"
log(){ echo "$(date): $*" >> "$LOG"; }

echo "----" >> "$LOG"
log "starting morning music (curl-only)"

# --- network wait: WiFi may not be associated yet after wake (max 3 min) ---
WAITED=0
until ping -c 1 -W 1000 "$IP" &>/dev/null; do
  WAITED=$((WAITED + 5))
  if [ "$WAITED" -ge 180 ]; then
    log "ERROR — speaker not pingable after 3 min, aborting"
    exit 1
  fi
  sleep 5
done
log "network ready (waited ${WAITED}s)"

# --- SOAP helper: soap <path> <service> <action> <args-xml> ---
soap() {
  curl -s -m 10 "$BASE$1" \
    -H "SOAPACTION: \"urn:schemas-upnp-org:service:$2:1#$3\"" \
    -H 'Content-Type: text/xml; charset="utf-8"' \
    --data "<?xml version=\"1.0\" encoding=\"utf-8\"?><s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\"><s:Body><u:$3 xmlns:u=\"urn:schemas-upnp-org:service:$2:1\">$4</u:$3></s:Body></s:Envelope>"
}
AVT="/MediaRenderer/AVTransport/Control"
RC="/MediaRenderer/RenderingControl/Control"
CD="/MediaServer/ContentDirectory/Control"

# --- speaker UID (needed for queue-based playback of container favorites) ---
UID_RINCON=$(curl -s -m 10 "$BASE/xml/device_description.xml" | sed -n 's/.*<UDN>uuid:\(RINCON_[A-Za-z0-9]*\).*/\1/p' | head -1)
if [ -z "$UID_RINCON" ]; then
  log "ERROR — could not read speaker UID from device description"
  exit 1
fi

# --- browse favorites (FV:2), parse + shuffle playable ones ---
BROWSE_XML=$(soap "$CD" ContentDirectory Browse '<ObjectID>FV:2</ObjectID><BrowseFlag>BrowseDirectChildren</BrowseFlag><Filter>*</Filter><StartingIndex>0</StartingIndex><RequestedCount>100</RequestedCount><SortCriteria></SortCriteria>')

# python3 used ONLY for XML parsing (no network) — emits records:
# title \x1f res \x1f resMD, separated by \x1e, pre-shuffled.
CANDIDATES=$(printf '%s' "$BROWSE_XML" | /usr/bin/python3 -c "
import sys, html, re, random
raw = sys.stdin.read()
m = re.search(r'<Result>(.*?)</Result>', raw, re.S)
if not m: sys.exit(0)
didl = html.unescape(m.group(1))
recs = []
for it in re.findall(r'<item.*?</item>', didl, re.S):
    t  = re.search(r'<dc:title>(.*?)</dc:title>', it, re.S)
    r  = re.search(r'<res[^>]*>(.*?)</res>', it, re.S)
    md = re.search(r'<r:resMD>(.*?)</r:resMD>', it, re.S)
    if t and r and r.group(1).strip():
        recs.append((t.group(1), r.group(1), md.group(1) if md else ''))
random.shuffle(recs)
sys.stdout.write('\x1e'.join('\x1f'.join(x) for x in recs))
")

if [ -z "$CANDIDATES" ]; then
  log "ERROR — no playable favorites found in Sonos favorites (FV:2). Add favorites in the Sonos app."
  exit 1
fi

# --- set volume once ---
soap "$RC" RenderingControl SetVolume "<InstanceID>0</InstanceID><Channel>Master</Channel><DesiredVolume>$VOLUME</DesiredVolume>" >/dev/null
log "volume set to $VOLUME"

# --- try favorites in shuffled order (max 3) ---
TRIES=0
SUCCESS=false
IFS=$'\x1e'
for REC in $CANDIDATES; do
  TRIES=$((TRIES + 1))
  [ "$TRIES" -gt 3 ] && break
  TITLE=$(printf '%s' "$REC" | awk -F $'\x1f' '{print $1}')
  RES=$(printf '%s' "$REC" | awk -F $'\x1f' '{print $2}')
  RESMD=$(printf '%s' "$REC" | awk -F $'\x1f' '{print $3}')
  log "attempt $TRIES: $TITLE"

  case "$RES" in
    x-rincon-cpcontainer:*)
      # Container favorite (e.g. Spotify playlist): load via queue
      soap "$AVT" AVTransport RemoveAllTracksFromQueue "<InstanceID>0</InstanceID>" >/dev/null
      ADD=$(soap "$AVT" AVTransport AddURIToQueue "<InstanceID>0</InstanceID><EnqueuedURI>$RES</EnqueuedURI><EnqueuedURIMetaData>$RESMD</EnqueuedURIMetaData><DesiredFirstTrackNumberEnqueued>0</DesiredFirstTrackNumberEnqueued><EnqueueAsNext>0</EnqueueAsNext>")
      if printf '%s' "$ADD" | grep -q "errorCode"; then
        log "  queue add failed: $(printf '%s' "$ADD" | grep -o '<errorCode>[0-9]*</errorCode>')"
        continue
      fi
      soap "$AVT" AVTransport SetAVTransportURI "<InstanceID>0</InstanceID><CurrentURI>x-rincon-queue:${UID_RINCON}#0</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>" >/dev/null
      soap "$AVT" AVTransport SetPlayMode "<InstanceID>0</InstanceID><NewPlayMode>SHUFFLE</NewPlayMode>" >/dev/null
      ;;
    *)
      # Stream/station favorite: set transport URI directly
      SETURI=$(soap "$AVT" AVTransport SetAVTransportURI "<InstanceID>0</InstanceID><CurrentURI>$RES</CurrentURI><CurrentURIMetaData>$RESMD</CurrentURIMetaData>")
      if printf '%s' "$SETURI" | grep -q "errorCode"; then
        log "  set-uri failed: $(printf '%s' "$SETURI" | grep -o '<errorCode>[0-9]*</errorCode>')"
        continue
      fi
      ;;
  esac

  soap "$AVT" AVTransport Play "<InstanceID>0</InstanceID><Speed>1</Speed>" >/dev/null
  sleep 3
  STATE=$(soap "$AVT" AVTransport GetTransportInfo "<InstanceID>0</InstanceID>" | grep -o '<CurrentTransportState>[A-Z_]*</CurrentTransportState>' | sed 's/<[^>]*>//g')
  if [ "$STATE" = "PLAYING" ] || [ "$STATE" = "TRANSITIONING" ]; then
    log "SUCCESS — playing: $TITLE (state: $STATE)"
    SUCCESS=true
    break
  fi
  log "  did not start (state: ${STATE:-unknown}), trying next favorite"
done
unset IFS

if [ "$SUCCESS" = false ]; then
  log "ERROR — no favorite would play after $TRIES attempt(s)"
  exit 1
fi

log "done"
