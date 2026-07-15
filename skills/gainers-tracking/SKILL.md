---
name: gainers-tracking
description: Schema for tracking daily stock gainers in machine-parseable files that roll up into weekly, monthly, and quarterly aggregations plus a catalyst-pattern library. Use when building or maintaining a post-market gainers wrap pipeline that needs to learn repeating catalyst patterns over time.
---

# Gainers Tracking File Schema

Maintain per-day tracking files for a post-market gainers wrap, designed so weekly / monthly / quarterly aggregations can mechanically parse them and surface patterns.

**File locations (relative to your workspace memory directory):**
- Daily: `memory/gainers/YYYY-MM-DD.md`
- Weekly: `memory/gainers/YYYY-WW-tracking.md`
- Monthly: `memory/gainers/YYYY-MM-tracking.md`
- Quarterly: `memory/gainers/YYYY-QQ-tracking.md`
- Catalyst pattern library: `memory/gainers/gainers-patterns.md`
- Regime check (monthly): `memory/gainers/quarterly-regime-check.md`

## Daily file format

Markdown wrapper with a structured YAML block per name — readable for context, parseable for aggregation. Two sections: primary names, then exceptional small-cap movers.

```yaml
ticker: TICKER1
name: Full Company Name
date: 2026-06-04
close_price: 23.60
percent_gain: 15.12
market_cap: 7.06e9          # in dollars, base units
dollar_volume: 224.1e6      # in dollars
section: primary             # primary | exceptional
tier: B                      # A | B | C
catalyst_category: [agm_clean_pass, earnings_beat_residual]
catalyst_summary: "AGM clean pass + Q1 beat residual"
verification_tier: 1         # 1=primary source, 2=news headline, 3=archive, 4=regulatory full-text search
verification_confidence: 95  # %
return_decomposition:        # percentages, sum ~100
  narrative_re_rating: 25
  fundamental_re_rating: 60
  multiple_expansion: 10
  low_float_amplification: 0
  short_squeeze_options_gamma: 0
  sector_beta: 5
  idiosyncratic: 0
prior: "What you expected going in, and why"
verdict: justified           # justified | overshoot | undershoot | unclear
verdict_conviction: medium   # low | medium | high
cyclical_or_secular: cyclical
flagged_for_weekly: false
flag_reason: null
comp_set: [PEER1, PEER2, PEER3]
historical_analogs: []
falsifiers:
  - "If Q2 guidance lowered, this re-rating breaks"
watch_list:
  within_7_days: "..."
  within_30_days: "..."
  within_90_days: "..."
sources:
  - { url: "https://...", fetched: "2026-06-04T22:09Z", tier: 1 }
```

A free-form 200-300 word analysis follows each YAML block. Exceptional-section names add `verification_notes` and a gate block:

```yaml
exceptional_gate_criteria:
  move_pct_passed: true       # >=100%
  dollar_volume_passed: true  # >=$50M
  catalyst_verified: true
  not_pre_revenue_biotech: true
  has_revenue_or_named_ip: true
```

End every daily file with a metrics block:

```yaml
filter_funnel:
  raw_universe_count: 50
  primary_filter_passed: 8
  primary_filter_dropped_count: 42
  primary_filter_drops_by_reason: { mcap_below_floor: 18, volume_below_floor: 12, pre_revenue_biotech_excluded: 5, other: 7 }
  exceptional_gate_candidates: 4
  exceptional_gate_passed: 1
  exceptional_gate_drops_by_feature: { move_below_100pct: 2, biotech_excluded: 1, catalyst_unverifiable: 0 }
generation_metrics:
  time_minutes: 12
  word_count_total: 3200
  fetches_attempted: 47
  fetches_succeeded: 38
  verification_tier_hit_counts: { tier_1: 5, tier_2: 2, tier_3: 1, tier_4: 0 }
filter_calibration_note: "Were the cutoffs right today? Note borderline exclusions."
regime_markers:
  small_cap_vs_large_cap_spread: -0.4
  overflow_exceptional_count: 0   # names beyond the daily exceptional cap
```

Close with a full `Sources & timestamps` list.

## Weekly / monthly / quarterly rollups

Same YAML-block-per-name structure, each level adding status fields:

- **Weekly** (aggregates 5 dailies, select ~10 names): `appearances_this_week`, `days_appeared`, `total_5d_move_pct`, `end_of_week_price`, `end_of_week_status: continued | faded | retraced_full`, `weekly_verdict`, `selected_for_weekly_deep_dive`, `selection_reason`.
- **Monthly** (aggregates 4 weeklies, select 10-15 from ~40 survivors): `weeks_selected`, `total_30d_move_pct`, `end_of_month_status`, `new_catalysts_in_month`, `selected_for_monthly_deep_dive`.
- **Quarterly** (aggregates 3 monthlies, select 10-15): `months_selected`, `total_90d_move_pct`, `end_of_quarter_status`, `catalyst_pattern_classification` (e.g. `lottery_ticket_faded | structural_re_rating_held`), `selected_for_quarterly_wrap`.

## Catalyst pattern library format

`gainers-patterns.md` — admit only patterns with >= 3 repeat occurrences across tracking files. Curate with discipline.

```yaml
- pattern_id: lottery_ticket_thematic_pr_lowfloat
  pattern_name: "Lottery-ticket thematic PR on low-float micro-cap"
  observed_count: 5
  named_instances:
    - { ticker: XXXX, date: 2026-06-04, outcome: faded_60pct_in_3_weeks }
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
    rare_outcomes: "If a named partner surfaces within 30 days, ~10% re-rate higher; otherwise fade is near-certain"
  pre_market_recognition_signals:
    - "Same-day PR with thematic keyword cluster (AI, space, quantum...)"
    - "No named counterparty in the PR"
    - "Market cap <$500M before the move; low float"
  added: YYYY-MM-DD
  refreshed: YYYY-MM-DD
```

Read this file at the top of every pre-market brief and name matching patterns explicitly when analyzing overnight movers — that is the learning loop: prospective pattern recognition, not after-the-fact narration.

## Schema discipline rules

- **YAML block per name, not per section** — aggregation parses names regardless of which file they appear in.
- **All numeric fields in base units** (dollars, scientific notation like `7.06e9` — never "in millions").
- **Verification tier + confidence labeled per name** so the library learns which tiers produced signal.
- **Selection flags propagate up** — a weekly-flagged name must be findable with a single grep across daily files.
- **Markdown body still required** — YAML is for machines, prose is for readers.
