---
name: weekly-deep-dive
description: Run the weekly gainers aggregation — read a week's daily gainers-tracking files, score which names' moves held vs. faded, select the most "justified" names for deep-dive treatment, and write the weekly tracking file that feeds monthly/quarterly aggregation and the catalyst-pattern library. Use when the user asks for a weekly market review of tracked gainers, "which of this week's movers held up," or wants the weekly selection pass over daily tracking files.
---

# Weekly Gainers Deep-Dive & Aggregation

The weekly layer of the gainers-tracking system: aggregate five daily tracking files, mark each name continued / faded / fully retraced, select the strongest candidates, and produce deep-dives on the selected names.

## How to use

1. Read `references/analysis-rules.md` for the house rules.
2. Read the week's daily gainers tracking files (YAML block per name — see the `post-market-brief` skill's `gainers-tracking-schema.md` for the schema, including the weekly file format).
3. For each name: fetch the week-end price, compute the total 5-day move, and classify end-of-week status (`continued | faded | retraced_full`). Note whether the original verdict (justified/overshoot) was borne out — this is the calibration loop.
4. Select ~10 names whose catalysts held for the weekly file; flag the strongest for full deep-dive treatment using the `stock-deep-dive` skill's template.
5. Feed any pattern with ≥3 repeat occurrences into the catalyst-pattern library.

## Bundled resources

- `references/analysis-rules.md` — house analysis rules.
- `references/original-agent-prompt.txt` — original OpenClaw (Sefer) weekly cron prompt.
- `scripts/weekly-deep-dive.sh` — original macOS cron wrapper (machine-specific; reference only).

Related skills: `post-market-brief` (produces the daily files this consumes), `stock-deep-dive` (the per-name deep-dive format).

> Source: OpenClaw agent "Sefer" — `~/.openclaw/workspace-sefer/`.
