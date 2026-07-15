---
name: memory-maintenance
description: Weekly memory housekeeping for a long-running assistant — read the past week's raw daily logs and distill durable insights (preferences, decisions, recurring context, corrections) into a curated long-term memory file so context survives log pruning. Use when the user asks to consolidate notes/memory, distill a week of logs, clean up an assistant's memory files, or run periodic knowledge-base maintenance.
---

# Memory Maintenance

Raw daily logs are append-only and noisy; long-term memory should be small and durable. This skill is the weekly distillation pass between them.

## How to use

1. Read the past week's raw daily logs and the current long-term memory file (`MEMORY.md` and `USER.md` in the original layout).
2. Extract only what's *durable*: stated preferences, decisions and their reasons, recurring people/projects and how they connect, corrections the user made, workflow changes that stuck. Skip anything that only mattered that day.
3. Merge into the long-term file — update or replace stale entries rather than appending duplicates. The file should stay readable end-to-end; if it's growing without bound, the curation is failing.
4. Note in the daily log that maintenance ran, so the next session can see it happened.

The discipline that makes this work: **distill, don't accumulate.** A memory file that doubles every month is a log, not a memory.

## Bundled resources

- `scripts/memory-maintenance.sh` — the original macOS cron wrapper (Sunday 9:00 AM) that triggered this pass through the OpenClaw gateway. Machine-specific; reference for re-automating.

Related skills: `weekly-wrap` (synthesis for the human), this skill (synthesis for the agent).

> Source: OpenClaw agent "Bari" — `~/.openclaw/workspace/memory-maintenance.sh`.
