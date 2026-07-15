---
name: investor-profile-template
description: Template for a USER.md financial-context profile that a markets-analysis agent reads before every analysis — time horizon, risk tolerance, liquidity, tax posture, watchlist, coverage universe, and delivery preferences. Use when setting up a new investing/markets agent or standardizing how it models its user.
---

# Investor Profile (USER.md) Template

Maintain one file that captures everything an analysis agent needs to know about its user's financial context. Every section below is structure; fill with the user's real values (the examples here are placeholders).

## Structure

### 1. Who they are (2-4 sentences)
Profession, financial sophistication, time constraints, how to pitch the register. Example: "Treat them as a numerate peer who doesn't live in markets day-to-day. Signal, not lectures."

### 2. How they want the agent to work (bullet list)
- Concise vs. thorough preference
- Whether to surface reasoning and priors before conclusions
- Surface assumptions before acting on them
- Act-then-explain vs. ask-first default
- Any hard rules (e.g., no buy/sell recommendations ever)

### 3. Financial profile table

| Field | Value |
|-------|-------|
| Time horizon | e.g. "Mixed: some names long-term (5-10 yr, secular trends), others medium-term (1-3 yr, earnings revisions + catalysts). Ask per analysis when ambiguous." |
| Risk tolerance | e.g. "Moderate, equity-heavy with macro hedges" — state the default tilt and which signals matter (rates / FX / commodities) |
| Liquidity needs | e.g. "None in next 12 months" — use an explicit TODO placeholder until confirmed |
| Tax posture | e.g. "US person, taxable account focus" — TODO until confirmed |
| Income geography | e.g. "US" |

Rule: when the agent runs an analysis, it tags which framing it used (long-term vs. medium-term) so the user can correct on the fly.

### 4. Watchlist table

```
TICKER  NAME              THESIS-IN-ONE-LINE      ADDED
AAAA    Example Corp      [TODO]                  YYYY-MM-DD
BBBB    Sample Inc        [TODO]                  YYYY-MM-DD
```

Keep a `[TODO]` thesis column until the user articulates one per name — the empty slot is a prompt to fill it.

### 5. Default coverage universe
Beyond the watchlist, list what every recurring brief covers, e.g.:
- **Indices:** broad-market, tech, small-cap, volatility index
- **Treasuries:** 2Y / 10Y / 30Y yields; 2s10s spread
- **FX & commodities:** dollar index, gold, crude, copper
- **Macro:** scheduled data releases that day (per an economic-calendar source)
- **Sectors:** the sector ETF complex for rotation signal

### 6. Sectors of interest
Explicit list, or a marked TODO with a stated default (e.g. "broad market with extra weight on financials, tech, and policy-sensitive sectors; adjust on instruction").

### 7. Holdings integration
State whether the agent reads from a holdings source. If shelved, say so and note what config goes here when enabled. Users can always share positions ad-hoc in a turn.

### 8. Things the user does NOT want (anti-preferences)
This section prevents drift. Examples of the genre:
- Day-trading takes dressed up as analysis
- Single-name pumping — every name comes with peers and the bear case
- Hot takes without falsifiers
- Generic commentary that could be written without the day's data
- Repeated compliance disclaimers (one per session)

### 9. Delivery preferences table

| Surface | Status |
|---------|--------|
| Chat channel | Always on |
| Written file in `memory/` | Always for scheduled briefs |
| Audio summary | On/off per brief type; length cap (e.g. < 90 seconds) |
| Messaging channel | Which briefs get pushed, any prefix convention |

### 10. On-demand commands
Document the exact trigger syntax the user can send (e.g. `deep-dive <TICKER> [date]`) and what template/depth each produces.

### 11. Update protocol
When anything here changes (new watchlist name, risk shift, sector focus), the agent proposes a diff and waits for the user's approval — never silently edits its own model of the user.

## Rules for using this file

- The profile is the agent's view of the user, not the user's diary. Keep it operational.
- Every TODO is visible debt: surface unfilled placeholders periodically rather than silently defaulting forever.
- Never store account numbers, position sizes, or credentials here; positions shared ad-hoc stay in the turn, not the profile, unless the user asks.
