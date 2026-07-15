---
name: pre-market-brief
description: Produce a structured pre-market brief for a trading day — overnight futures/rates/FX/commodities tape, Asia/Europe recap, today's catalysts with times and consensus, earnings docket, watchlist deltas, and the single most important thing to watch. Use whenever the user asks for a pre-market brief, morning market rundown, "what's moving overnight," "what matters in markets today," or wants to prepare before the US open.
---

# Pre-Market Brief

Generate a disciplined pre-market briefing before the US open. The output answers one question: *what is positioned to move today, and why?*

## How to use

1. Read `references/analysis-rules.md` first — the eight house rules (prior before evidence, decompose, name the comp set, units + as-of dates, end with falsifiers, no buy/sell recommendations) govern every line.
2. Fetch live data for every level quoted: S&P/Nasdaq/Russell futures, DXY, US 2Y/10Y, gold, WTI, VIX, plus Asia/Europe closes. Never quote a price from memory.
3. Fill `assets/pre-market-template.md` exactly — same sections, same tables.
4. Lead with "The day in one sentence." Close with "One thing to watch" (a specific level, data point, or catalyst) and a Sources & timestamps footer that also lists failed fetches.

## Structure (from the template)

The day in one sentence → Overnight tape table → Asia + Europe (two lines max) → Today's catalysts (time ET, consensus, why it matters) → Earnings docket (before open / after close) → Watchlist deltas → One thing to watch → Sources & timestamps.

## Bundled resources

- `assets/pre-market-template.md` — the exact output template.
- `references/analysis-rules.md` — the house analysis rules; read before writing.
- `references/original-agent-prompt.txt` — the original OpenClaw (Sefer) cron prompt, including Telegram-summary and JSON-digest output variants for dashboard integration.
- `scripts/pre-market-brief.sh` — the original macOS cron wrapper that triggered this brief via the OpenClaw gateway (machine-specific paths; reference only).

> Source: OpenClaw agent "Sefer" — `~/.openclaw/workspace-sefer/` (templates, prompts, cron scripts).
