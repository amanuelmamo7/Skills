---
name: trend-justification
description: Test whether a market trend or theme is justified — decompose the move into multiple re-rating vs. fundamentals vs. sector beta vs. macro vs. flows, write down the falsifiable claims that would have to be true, compare against what actually happened, and deliver an Observed/Implied/Actual/Gap verdict (justified, overshoot, undershoot, or unclear). Use whenever the user asks "is this rally/selloff justified," "why are <sector> stocks up," whether a theme (AI, rate cuts, small caps) has run too far, or any is-the-market-right question.
---

# Trend Justification

The core "is this move justified" framework, applied to a trend or theme rather than a single name. The punchline is always the gap between what would justify the move and what actually changed.

## How to use

1. Read `references/analysis-rules.md`. Rule 2 is the heart of this skill: frame the assessment as a hypothesis test — (a) what would have to be true for the move to be justified, (b) what would falsify it, (c) what you actually observe.
2. Quantify the observed move against a named comparison set ("up 12% vs. sector +8% vs. S&P +6%" — never a bare number).
3. Fill `assets/trend-justification-template.md`: the trend in one sentence → prior → observed move table → decomposition (multiple re-rating / fundamentals / sector beta / macro / flows / idiosyncratic) → what would have to be true (numbered, falsifiable) → what actually happened (same list, with data) → the gap block:

```
Observed:  <move>
Implied:   <what would justify>
Actual:    <what changed>
Gap:       <signed magnitude>
Verdict:   <justified | overshoot | undershoot | unclear>
Conviction: <low | medium | high>
```

4. Make the cyclical-vs-secular call explicitly — most "unjustified" moves are regime confusion. Close with base rates and falsifiers.

## Bundled resources

- `assets/trend-justification-template.md` — the exact output template.
- `references/analysis-rules.md` — house analysis rules, including the four-line framework.

Related skills: `company-thesis`, `stock-deep-dive`, `pointed-analysis`.

> Source: OpenClaw agent "Sefer" — `~/.openclaw/workspace-sefer/templates/trend-justification.md`.
