---
name: launchagent-scheduling
description: Conventions for scheduling recurring agent jobs on macOS — when to use LaunchAgents vs crontab vs session-scoped schedulers, a CRONS.md manifest as source of truth, and surviving sleep/reboot. Use when setting up, auditing, or debugging scheduled jobs on a Mac that must fire reliably.
---

# LaunchAgent Scheduling for Agent Jobs

Recurring agent jobs on macOS need a scheduler that actually fires on a laptop that sleeps. This skill covers choosing the mechanism, documenting it in a manifest, and the conventions that keep it debuggable.

## Choosing the mechanism

**LaunchAgents (`~/Library/LaunchAgents/`) — the production default on macOS.**
- Survive sleep/wake cycles; cron does NOT fire after clamshell sleep. This is the decisive reason.
- Use for anything the user relies on daily (briefs, heartbeats, market jobs).
- Pair with a scheduled wake (`pmset repeat wake MTWRFSU 06:55:00`) slightly before the earliest job so the machine is awake to run it.

**crontab — acceptable for servers, a liability on laptops.** If you inherit cron entries, migrating to LaunchAgents is usually the right call; if a runbook installs cron entries as a first pass, plan the LaunchAgent migration. Either way, exactly one mechanism should own a given job — after migrating, empty the crontab by design so nobody wonders which copy fires.

**Session-scoped schedulers (an agent framework's built-in cron/timer tool) — never for production jobs.** They die when the session ends. Fine for one-shot reminders ("in 20 minutes") within a live session.

**Heartbeat vs. dedicated job:** batch flexible-timing periodic checks (inbox + calendar + notifications) into a single heartbeat job with a rotation file, rather than many tiny jobs. Use a dedicated scheduled job when exact timing matters, the task needs isolation from session history, or output should deliver straight to a channel.

## The manifest: CRONS.md as source of truth

Keep one `CRONS.md` per workspace declaring every recurring job. Include:

1. A header stating the mechanism and the invariant, e.g. "All jobs run as LaunchAgents (crontab is empty by design)."
2. Quick-reference commands:
   - Check loaded: `launchctl list | grep -E "com\.(agent1|agent2)\."`
   - Load: `launchctl load ~/Library/LaunchAgents/<label>.plist`
3. **The jobs table:** Job | Schedule | LaunchAgent Label | Script path.
4. **What each job does** — a short prose section per job (what it fetches, what it writes, what it delivers).
5. **Log paths table** — every script logs to its own file (e.g. `/tmp/<agent>-<job>.log`). First debugging move when a job seems dead: `tail` the log.
6. **Lessons/notes section** — quirks you learned the hard way, dated.

The manifest exists so a fresh session (or a health check) can verify reality against intent: count `launchctl list` entries, compare to the table, alert on drift.

## Job script conventions

- Each job is a small bash script that does one thing — typically POSTing a templated prompt to the agent gateway's hook endpoint with the agent id in the payload.
- **Secrets never live in script source.** Scripts read the auth token from the config file at runtime (e.g. `jq -r '.hooks.token' <config>`) and fail loudly if it's missing. Know which token the endpoint expects — webhook token vs. gateway admin token confusion is a classic silent 401.
- `set -euo pipefail` at the top; append stdout/stderr to the job's log file.
- Naming: labels `com.<agent>.<job>`, scripts `<job>.sh` in the agent's workspace, logs `/tmp/<agent>-<job>.log`.
- Confirm the host timezone (`date`) before choosing schedule hours.

## Install / change procedure

1. Back up current state first: `crontab -l > /tmp/crontab-backup-<stamp>.txt` and copy any plist you're replacing.
2. Preserve and merge — never overwrite the whole crontab or someone else's LaunchAgents; verify pre-existing entries survived by diffing against the backup.
3. Load the plist, then verify: `launchctl list | grep <label>`.
4. Dry-run the script manually once and check its log plus its expected output artifact.
5. Update `CRONS.md` in the same change. Manifest drift is how ghost jobs happen.

## Health check (run at session startup or daily)

- `launchctl list | grep -E "com\.<prefix>\."` — count entries, compare against the manifest's expected count.
- If any are missing, reload from `~/Library/LaunchAgents/<label>.plist` and alert the user.
- If a job seems to have stopped: `tail /tmp/<agent>-*.log` before anything else.

## Gotchas

- **launchd parents the process, not Terminal:** macOS folder permissions (Privacy & Security) must grant the daemonized process access to any protected folders the scripts touch — a script that works in your terminal can still fail under launchd.
- `~/Documents`, `~/Desktop`, `~/Downloads` are TCC-protected; keep agent workspaces outside them.
- Async hook endpoints return success immediately; the real output lands minutes later. Verify with patience.
- Requires `jq` (or equivalent) on PATH for token extraction — check in preconditions.
