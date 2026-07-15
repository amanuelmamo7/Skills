---
name: macro-readthrough
description: Produce a monthly macro readthrough of a data release or the month that just ended — CPI/PCE/NFP/GDP/FOMC prints vs. consensus, decomposition beneath the headline (shelter vs. ex-shelter, supercore, payrolls vs. wages), second-order asset moves (2Y/10Y/2s10s, DXY, gold, equities, Fed funds futures), and what it means for the inflation/growth/Fed regime. Use whenever the user asks about a CPI/PCE/jobs/GDP print, "what did the Fed data mean," monthly macro recap, or whether markets reacted correctly to an economic release.
---

# Macro Readthrough

Analyze an economic data release (or a full month of them) the way a rates desk would: the print vs. consensus, what's underneath the headline, whether the market's reaction was justified, and what it means for the policy regime.

## How to use

1. Read `references/analysis-rules.md` — state the prior (consensus and positioning) before the print; every number carries units and an as-of date.
2. Fetch the actual releases live (FRED/BLS/BEA): headline + core, MoM and YoY, subcomponents, plus the curve (2Y/5Y/10Y/30Y, 2s10s), breakevens, DXY, gold, and Fed funds futures pricing before/after.
3. Fill `assets/macro-readthrough-template.md`: the print in one sentence → prior/consensus → the print table → what's underneath the headline (decompose: for CPI shelter vs. ex-shelter, core goods vs. services, supercore; for NFP payrolls vs. unemployment vs. wages vs. participation) → second-order effects table with a justified? column → regime implications with probabilities from futures → what's priced in → what would change my mind → sources.

## Bundled resources

- `assets/macro-readthrough-template.md` — the exact output template.
- `references/analysis-rules.md` — house analysis rules.
- `references/original-agent-prompt.txt` — original OpenClaw (Sefer) monthly cron prompt, including the JSON digest format for a dashboard Macro panel.
- `scripts/macro-readthrough.sh` — original macOS cron wrapper (machine-specific; reference only).

> Source: OpenClaw agent "Sefer" — `~/.openclaw/workspace-sefer/`.
