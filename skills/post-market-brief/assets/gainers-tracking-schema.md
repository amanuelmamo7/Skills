# Gainers Tracking File Schema

Per-day tracking files for the post-market gainers wrap. Designed so weekly / monthly / quarterly aggregations can mechanically parse them and surface patterns.

**File locations:**
- Daily: `memory/gainers/YYYY-MM-DD.md`
- Weekly: `memory/gainers/YYYY-WW-tracking.md`
- Monthly: `memory/gainers/YYYY-MM-tracking.md`
- Quarterly: `memory/gainers/YYYY-QQ-tracking.md`
- Catalyst pattern library: `memory/gainers/gainers-patterns.md`
- Regime check (monthly): `memory/gainers/quarterly-regime-check.md`

---

## Daily file format

Markdown wrapper with a structured YAML block per name so future sessions can both read for context and parse for aggregation.

```markdown
# Gainers Tracking — YYYY-MM-DD

## Section 1: Primary names

### TICKER1
```yaml
ticker: TICKER1
name: Full Company Name
date: 2026-06-04
close_price: 23.60
percent_gain: 15.12
market_cap: 7.06e9          # in dollars
dollar_volume: 224.1e6      # in dollars
section: primary             # primary | exceptional
tier: B                       # A | B | C
catalyst_category: [agm_clean_pass, earnings_beat_residual]
catalyst_summary: "AGM clean pass + Q1 beat residual"
verification_tier: 1          # 1=primary source, 2=Google News headline, 3=archive.ph, 4=EDGAR EFTS
verification_confidence: 95   # %
return_decomposition:
  narrative_re_rating: 25
  fundamental_re_rating: 60
  multiple_expansion: 10
  low_float_amplification: 0
  short_squeeze_options_gamma: 0
  sector_beta: 5
  idiosyncratic: 0
prior: "ACA insurer in year 2 of profitability; catalysts expected to be earnings-cycle"
verdict: justified            # justified | overshoot | undershoot | unclear
verdict_conviction: medium    # low | medium | high
cyclical_or_secular: cyclical
flagged_for_weekly: false
flag_reason: null
comp_set: [HUM, CI, CVS, UNH]
historical_analogs: []
falsifiers:
  - "If Q2 guidance lowered, this re-rating breaks"
  - "If ACA enrollment data surprises down, thesis weakens"
watch_list:
  within_7_days: "FDA cycle decisions on related applications"
  within_30_days: "Q2 earnings preannouncement window"
  within_90_days: "Q2 earnings call + 2027 guidance"
sources:
  - { url: "https://...", fetched: "2026-06-04T22:09Z", tier: 1 }
```

[Free-form 200-300 word analysis follows the YAML block, matching the house rules]

### TICKER2
[same structure]

...

## Section 2: Exceptional small-cap movers

### TICKER_X
```yaml
ticker: TICKER_X
name: Full Company Name
date: 2026-06-04
close_price: ...
percent_gain: ...
market_cap: ...
dollar_volume: ...
section: exceptional
tier: A                       # exceptional names default to A consideration; downgrade if substance lacking
catalyst_category: [thematic_pr, lottery_ticket_pattern]
catalyst_summary: "..."
verification_tier: 2          # Google News headline confirmed catalyst exists
verification_confidence: 75   # %
verification_notes: "T1 PR Newswire bot-blocked. T2 Google News confirmed via multi-publisher headlines."
[rest of fields same]
exceptional_gate_criteria:
  move_pct_passed: true       # ≥100%
  dollar_volume_passed: true  # ≥$50M
  catalyst_verified: true     # via tier 2
  not_pre_revenue_biotech: true
  has_revenue_or_named_ip: true
```

[Free-form analysis]

## Metrics for the day

```yaml
filter_funnel:
  raw_universe_count: 50
  primary_filter_passed: 8
  primary_filter_dropped_count: 42
  primary_filter_drops_by_reason:
    mcap_below_floor: 18
    volume_below_floor: 12
    pre_revenue_biotech_excluded: 5
    other: 7
  exceptional_gate_candidates: 4
  exceptional_gate_passed: 1
  exceptional_gate_drops_by_feature:
    move_below_100pct: 2
    biotech_excluded: 1
    catalyst_unverifiable: 0
generation_metrics:
  time_minutes: 12
  word_count_total: 3200
  fetches_attempted: 47
  fetches_succeeded: 38
  verification_tier_hit_counts:
    tier_1: 5
    tier_2: 2
    tier_3: 1
    tier_4: 0
filter_calibration_note: "Filter cutoffs appropriate today. 1 borderline exclusion (ABVX) needs revenue-check fast-path."
regime_markers:
  russell_2000_vs_sp500: -0.4
  txse_news: "none observed"
  overflow_exceptional_count: 0     # # that would have qualified beyond the 2/day cap
```

## Sources & timestamps

[Full source list with URLs and timestamps]
```

---

## Weekly file format

Aggregates 5 daily files. Same YAML block structure per name but adds week-end status.

```yaml
ticker: TICKER1
appearances_this_week: 2          # days the name appeared on a daily list
days_appeared: [2026-06-02, 2026-06-04]
total_5d_move_pct: 28.3
end_of_week_price: 26.40
end_of_week_status: continued       # continued | faded | retraced_full
weekly_verdict: ...
selected_for_weekly_deep_dive: true # 1 of 10 most "justified" weekly picks
selection_reason: "Catalyst held; comp set continued to confirm thesis"
```

10 names selected per week from the funnel. Selection logic in `gainers-aggregation.md` (to be written).

---

## Monthly file format

Aggregates 4 weekly files. Same structure plus month-end status.

```yaml
ticker: TICKER1
weeks_selected: [W22, W23]
total_30d_move_pct: ...
end_of_month_status: ...
new_catalysts_in_month: [...]
selected_for_monthly_deep_dive: true # 10-15 names from 40 weekly survivors
```

---

## Quarterly file format

Aggregates 3 monthly files. 10-15 names from 30-45 monthly survivors.

```yaml
ticker: TICKER1
months_selected: [M5, M6]
total_90d_move_pct: ...
end_of_quarter_status: ...
catalyst_pattern_classification: lottery_ticket_faded | structural_re_rating_held | ...
selected_for_quarterly_wrap: true
```

---

## Catalyst pattern library format

`gainers-patterns.md` — only entries with ≥ 3 repeat occurrences across tracking files. Disciplined curation per the house rules.

```yaml
- pattern_id: lottery_ticket_thematic_pr_lowfloat
  pattern_name: "Lottery-ticket thematic PR on low-float micro-cap"
  observed_count: 5
  named_instances:
    - { ticker: STI, date: 2026-06-04, outcome: faded_60pct_in_3_weeks }
    - { ticker: DPRO, date: 2025-09-15, outcome: faded_72pct_in_4_weeks }
    - { ticker: CODA, date: 2021-04-22, outcome: faded_55pct_in_2_weeks }
    - { ticker: ..., date: ..., outcome: ... }
  structural_features:
    - market_cap_under_500m: true
    - thematic_pr_no_signed_deal: true
    - dollar_volume_over_50m: true
    - move_over_100pct: true
  typical_follow_through:
    fade_window_days_min: 14
    fade_window_days_max: 30
    fade_magnitude_pct_min: 50
    fade_magnitude_pct_max: 80
    rare_outcomes: "If named partner surfaces within 30 days, ~10% of cases re-rate higher; otherwise fade is near-certain"
  pre_market_recognition_signals:
    - "Same-day PR with thematic keyword cluster (e.g., SpaceX, AI, lunar, LEO)"
    - "No named counterparty in the PR"
    - "Market cap <$500M before the move"
    - "Low float (<50M shares public)"
  added: 2026-09-XX
  refreshed: 2026-09-XX
```

The agent reads this file at the top of every pre-market brief and references patterns when analyzing overnight movers. The goal: pattern-recognition in pre-market analysis, not after-the-fact narration in post-market.

---

## Schema discipline notes

- **YAML block per name, not per section.** Future weekly aggregation parses individual names regardless of which day's file they appear in.
- **All numeric fields normalized to base units** (dollars not "in millions" — use scientific notation like `7.06e9`).
- **Verification tier and confidence labeled per name.** Catalyst-library learns which tiers produced strongest signal over time.
- **Selection flags propagate up.** A name flagged for weekly deep-dive must be readable from a single grep across daily files.
- **Markdown body still required.** YAML is for aggregation; the markdown free-form analysis is for human (and future-session) reading.
