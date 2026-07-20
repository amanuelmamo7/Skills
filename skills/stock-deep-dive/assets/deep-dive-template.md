# Gainers Deep-Dive — <TICKER>

*Model: the 2026-06-04 STI analysis. Match its structure and rigor. ~1000-1500 words target unless the data clearly doesn't support that depth.*

Invocation: the user requests `deep-dive <TICKER>` (optionally with a date) for any name on a recent gainers tracking file (today, this week, this month, this quarter). Read the relevant tracking file, find the name's prior wrap if any, and produce a full reference-grade analysis.

---

## Header

```
<NAME> (<TICKER>) — +<%>% <Period> Move: Decomposed
As of: <ISO timestamp> · Source list: <count> primary + <count> secondary
```

## 1. Prior going in

2-4 sentences. What you'd expect to be true going in, before the data. Example pattern: "A micro-cap battery-materials company with patented graphene/silicon anode IP, no meaningful commercial revenue until May 2026, and an all-time chart that's down -95.52% — classic deep-value-trap profile. You'd expect any single-catalyst pop to be violent but fragile."

The prior frames whether the analysis confirms or surprises you. The reader should be able to tell which.

## 2. What Happened — The Catalyst

The specific PR, 8-K, filing, news, or event that triggered the move. Quote the headline. Name the source. Include the date and the specific content. Example: "This is a single press release doing all the work. Issued this morning, June 4: 'Solidion Technology Unveils Patented Extreme-Climate Battery Technology...' ... That's the whole release. No signed contract. No named partner. No revenue guidance."

If multiple catalysts, list in order of contribution.

## 3. Return Decomposition

Table with explicit % attribution per factor. Total should sum to ~100%.

| Component | Contribution | Reasoning |
|-----------|-------------|-----------|
| Narrative re-rating | ~X% | One line on the mechanism |
| Fundamental re-rating | ~X% | One line |
| Multiple expansion | ~X% | One line |
| Low-float / microstructure amplification | ~X% | One line |
| Short squeeze / options gamma | ~X% | One line |
| Sector beta | ~X% | One line |
| Idiosyncratic / one-off | ~X% | One line |

State the punchline: "This is a narrative multiple expansion on a stock that had nearly zero implied optionality priced in," or "This is largely a fundamental re-rating in response to a beat."

## 4. Why It Worked / The Mechanism

1-2 paragraphs on the structural lever. Why did this particular catalyst produce this magnitude of move? What makes the market susceptible to this narrative right now?

Example for STI: "The SpaceX IPO is arguably the single most anticipated liquidity event in private markets right now — any small-cap that can credibly stitch itself into that story gets speculative momentum. Retail traders and algo scanners both react to keyword clusters..."

## 5. What Could Be Happening Behind Closed Doors

Three named scenarios in **descending probability**. Each one paragraph. Probability-weighted by what the evidence supports.

1. **<Most likely scenario>** (~%%) — reasoning
2. **<Second-most-likely scenario>** (~%%) — reasoning
3. **<Tail scenario>** (~%%) — reasoning

State which scenario the evidence currently favors.

## 6. The Framework Test (apply "is the trend justified")

```
Observed:  <move> over <period>
Implied:   <metric> needs to <change by X> to justify
Actual:    <metric> actually changed by <Y>
Gap:       <signed magnitude>
Verdict:   <justified | overshoot | undershoot | unclear>
Conviction: <low | medium | high>
```

If implied/actual can't be computed numerically, state "qualitative only" and explain why.

## 7. Comparison Set

Two parts:

**Historical analogs** — specific named past spikes that followed the same pattern. Use ticker + date + outcome. Example: "DPRO (Draganfly drone-delivery pop, 2025), CODA (battery-company SpaceX-adjacent narrative, 2021), BLNK/WKHS during EV mania (2020-21). The setup is nearly identical — low float + hot theme + PR-trigger = violent spike, followed by 50–80% retracement within 2–4 weeks when the contract never materializes."

**Current peer compset** — named competitors / sector peers with current multiples for context. Example: "ASTS, RKLB, MNTS as space-pure-plays; LITE, COHR for the optical layer."

## 8. Institutional Angle

Who is buying and selling. Specifically distinguish:
- Institutional flow (mutual funds, pensions, long-only)
- Hedge fund positioning (short interest, pair-trade structure)
- Retail momentum flow
- Options gamma / dealer hedging
- Pre-positioned holders selling into strength

Use evidence: short interest data, options volume, block trade reporting, 13F lag, ETF flows. If you can't determine flow attribution, say so and name what would close the gap.

Example: "Almost certainly not institutional-driven. Institutional investors don't move micro-caps on press releases — they'd be selling into this strength if they held prior positions. The volume and price action is consistent with retail momentum flow + options gamma..."

## 9. What Would Change My Mind

Three specific falsifiers. Each one a concrete observation that would invalidate the current take.

- **<Falsifier 1>**: <specific event, level, filing, or print that would force a revision>
- **<Falsifier 2>**: <same>
- **<Falsifier 3>**: <same>

Example: "A named commercial agreement with SpaceX, a Starlink satellite manufacturer, Northrop, L3Harris, or a NASA prime contractor → move would be partially justified."

## 10. Watch List

Specific filings, events, releases with timeframes. The reader should know exactly what to monitor and when.

- **Within 7 days**: <thing to watch>
- **Within 30 days**: <thing to watch>
- **Within 90 days**: <thing to watch>

Example: "Watch the 8-K filings over the next 2 weeks. If they file a prospectus supplement or S-3 drawdown, that confirms scenario 2."

## 11. Bottom Line

One paragraph. Direct call: lottery-ticket / structural re-rating / sector beta / cyclical bounce / undecided. With reasoning.

No buy/sell recommendation per house rule 8. The verdict is analytical: this is a lottery-ticket pattern with X% expected fade within Y weeks if no commercial agreement surfaces. Not "I'd sell" — "the pattern historically retraces 50-80% within 2-4 weeks without a named partner."

## 12. Sources & timestamps

- <URL> — fetched <ISO timestamp>
- <URL> — fetched <ISO timestamp>
- <URL> — fetched <ISO timestamp>

Verification chain status per Tier:
- Tier 1 (primary source direct): <succeeded / failed>
- Tier 2 (Google News headlines, ≥70% rubric): <succeeded / failed / N/A>
- Tier 3 (archive.ph fallback): <succeeded / failed / N/A>
- Tier 4 (EDGAR EFTS): <succeeded / failed / N/A>

Fetches attempted but failed: <list, or "none">

---

## Compliance footer

This deep-dive is informational analysis produced by an automated research assistant, not personalized investment advice, and does not constitute a recommendation.
