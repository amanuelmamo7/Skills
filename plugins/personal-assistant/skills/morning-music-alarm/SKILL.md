---
name: morning-music-alarm
description: Wake-up music automation for Sonos speakers using raw SOAP over curl (no CLI dependency) — waits for the network after wake, picks a random playable Sonos favorite, enables shuffle, sets volume, and starts playback with retry on failure. Use when the user wants a music alarm, scheduled Sonos playback, "play music every morning," or needs to control Sonos from scripts/launchd where third-party binaries are blocked by macOS privacy rules.
---

# Morning Music Alarm (Sonos, curl-only)

A scheduled Sonos wake-up that survives the two things that kill naive versions: WiFi not yet associated after machine wake, and macOS Local Network privacy silently blocking ad-hoc-signed binaries under launchd.

## Design (the hard-won details)

- **curl-only SOAP** — the `sonos` CLI is ad-hoc signed, so launchd-spawned runs get EHOSTUNREACH from macOS Local Network privacy. Apple-signed `curl`/`ping` are exempt. All control is raw UPnP SOAP calls to the speaker on port 1400.
- **Network wait** — ping the speaker for up to 3 minutes before giving up (WiFi re-associates slowly after wake).
- **Random favorite + retry** — picks a random playable Sonos favorite each morning; if one fails to load, tries the next.
- **Queue-based playback** — container favorites (playlists/albums) are enqueued via the speaker UID, then shuffle is enabled and volume set before play.

## How to use

1. `scripts/morning-jazz.sh` is the working implementation. Adapt the constants at the top: speaker IP, volume, log path.
2. Schedule via launchd/cron for the wake time. The script is idempotent and logs each run.
3. The SOAP helper inside (`soap <path> <service> <action> <args-xml>`) is a reusable pattern for any Sonos control task — play/pause, volume, queue management — without any dependency beyond curl.

## Bundled resources

- `scripts/morning-jazz.sh` — the original, working macOS implementation (speaker IP hard-coded; adjust).

Related skills: `morning-brief` (the original stack played music, then delivered the spoken brief).

> Adapted from the author's personal assistant stack.
