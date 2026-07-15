---
name: company-thesis
description: Build a structured investment thesis on a company — what's priced in (implied earnings path, reverse-DCF sketch, consensus, comp-set multiples), a mechanical decomposition of what's actually driving the stock, bull and bear cases with sources, base rates, cyclical-vs-secular call, catalysts, and explicit falsifiers. Use whenever the user asks "what do you think of <company/ticker>," wants a bull/bear breakdown, asks what's priced into a stock, or wants a company analyzed as an investment.
---

# Company Thesis

A full-company analytical thesis: not "is the stock good," but *what is priced in, what is actually happening, and what would change the answer*.

## How to use

1. Read `references/analysis-rules.md`. Conviction calibration matters — "I think" / "the data suggests" / "I'd lean" / "no view," never bluffing. No buy/sell language; model what's priced in instead.
2. Fetch live: current price and market cap (timestamped), consensus estimates, peer multiples, latest filings.
3. Fill `assets/company-thesis-template.md`: one-line take → prior → what's priced in (implied earnings path at the current multiple, reverse-DCF sketch with stated WACC/terminal assumptions, consensus range, comp-set discount/premium) → decomposition table of the actual move (multiple vs. earnings vs. share count vs. FX vs. sector beta vs. idiosyncratic, in bps) → bull case and bear case (three to five tight claims, each with a fact and source) → base rate from historical analogs → cyclical or secular, explicit call → catalysts next 90 days with dates → what would change my mind (specific metric levels that invalidate each case) → trend verdict block → sources with timestamps.

## Bundled resources

- `assets/company-thesis-template.md` — the exact output template.
- `references/analysis-rules.md` — house analysis rules.

Related skills: `stock-deep-dive` (for decomposing a violent single move), `trend-justification` (for sector/theme-level moves).

> Source: OpenClaw agent "Sefer" — `~/.openclaw/workspace-sefer/templates/company-thesis.md`.
