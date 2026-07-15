---
name: post-market-brief
description: Produce an end-of-day market wrap — index and sector closes, top S&P movers with attribution, anomaly detection (>2σ moves without a catalyst), after-hours earnings, tomorrow's setup — plus a structured daily gainers-tracking file for small/mid-cap movers with catalyst verification and return decomposition. Use whenever the user asks for a market wrap, post-market brief, "how did markets close," daily gainers analysis, or wants today's movers decomposed and logged for later pattern analysis.
---

# Post-Market Brief & Gainers Wrap

Two deliverables after the US close: a readable **daily wrap** and a machine-parseable **gainers tracking file** that feeds weekly/monthly/quarterly aggregation and a catalyst-pattern library.

## How to use

1. Read `references/analysis-rules.md` — the eight house rules apply (decompose returns, name the comp set, units + as-of dates, falsifiers, no recommendations).
2. Fetch closes live: SPY/QQQ/IWM/DIA/VIX, all eleven sector ETFs, top S&P movers, after-hours earnings prints.
3. Fill `assets/post-market-template.md` for the wrap. Flag anomalies: any move > 2σ vs. its 60-day realized vol without an obvious catalyst — show the volatility math.
4. For the gainers wrap, follow `assets/gainers-tracking-schema.md` exactly: one YAML block per name (catalyst category, verification tier 1–4 with confidence, return decomposition summing to ~100%, verdict justified/overshoot/undershoot/unclear, falsifiers, watch list) followed by 200–300 words of free-form analysis. Apply the exceptional small-cap gate (≥100% move, ≥$50M dollar volume, verified catalyst, not pre-revenue biotech).
5. If a catalyst-pattern library exists (`gainers-patterns.md`), reference matching patterns by name.

## Bundled resources

- `assets/post-market-template.md` — the wrap template.
- `assets/gainers-tracking-schema.md` — full YAML schema for daily/weekly/monthly/quarterly tracking files and the catalyst-pattern library; read it before writing any tracking file.
- `references/analysis-rules.md` — house analysis rules.
- `references/original-agent-prompt.txt` — the original OpenClaw (Sefer) cron prompt with Telegram/JSON-digest output variants.
- `scripts/post-market-brief.sh` — original macOS cron wrapper (machine-specific; reference only).

> Source: OpenClaw agent "Sefer" — `~/.openclaw/workspace-sefer/`.
