# Skills

Curated skills library — reviewed, pinned, and indexed. Skills I write myself and skills pulled from other repos that have passed the [intake checklist](docs/INTAKE.md).

**How this repo works**

- Every skill is a folder in [`skills/`](skills/) with a `SKILL.md` (plus optional `assets/`, `references/`, `scripts/`).
- [`index.json`](index.json) is the source of truth: every skill, its buckets, provenance, review status, and the relationships between skills. The tables below are generated from it.
- [`manifest.json`](manifest.json) is the provenance ledger for third-party skills — each pinned to the exact commit reviewed. Updates are diff-reviews, never blind re-pulls.
- [`.claude-plugin/`](.claude-plugin/) makes this repo installable in Claude Code: `/plugin marketplace add amanuelmamo7/Skills`
- Nothing here updates automatically. A skill enters or changes only after human review.

## Buckets

Buckets are metadata, not folders — a skill can live in more than one.

| Bucket | Skills | Status |
|---|---:|---|
| market-analysis | 8 | active |
| personal-assistant | 12 | active |
| attorney-workflow | 1 | growing |
| projects | 1 | active |
| general | 0 | reserved |
| web-application | 0 | reserved |

### market-analysis (from Sefer)

| Skill | Use it for |
|---|---|
| [`pre-market-brief`](skills/pre-market-brief/SKILL.md) | Morning market rundown: overnight tape, catalysts, earnings docket |
| [`post-market-brief`](skills/post-market-brief/SKILL.md) | End-of-day wrap + gainers tracking with catalyst verification |
| [`macro-readthrough`](skills/macro-readthrough/SKILL.md) | CPI/PCE/NFP/GDP/FOMC prints: what's under the headline |
| [`weekly-deep-dive`](skills/weekly-deep-dive/SKILL.md) | Weekly aggregation of daily gainers: what held, what faded |
| [`stock-deep-dive`](skills/stock-deep-dive/SKILL.md) | 12-section deep-dive on a single stock's big move |
| [`company-thesis`](skills/company-thesis/SKILL.md) | Full company thesis: what's priced in, bull/bear cases, catalysts |
| [`trend-justification`](skills/trend-justification/SKILL.md) | "Is this rally justified?" Observed/Implied/Actual/Gap framework |
| [`pointed-analysis`](skills/pointed-analysis/SKILL.md) | Sharp one-off market questions: direct answer, fetch log, falsifiers |

### personal-assistant (from Bari + Cowork)

| Skill | Use it for |
|---|---|
| [`weekday-morning-brief`](skills/weekday-morning-brief/SKILL.md) | Weekday 8am brief: calendar, VIP email + reply drafts, markets, system health |
| [`morning-brief`](skills/morning-brief/SKILL.md) | Bari original of the daily brief — superseded by `weekday-morning-brief` |
| [`evening-wrap`](skills/evening-wrap/SKILL.md) | End-of-workday wrap: tomorrow's calendar, honest review of today |
| [`weekly-wrap`](skills/weekly-wrap/SKILL.md) | Friday synthesis of the week's logs: themes, time allocation |
| [`memory-maintenance`](skills/memory-maintenance/SKILL.md) | Weekly distillation of raw logs into durable long-term memory |
| [`assistant-heartbeat`](skills/assistant-heartbeat/SKILL.md) | Periodic rotating check (email/calendar/cron health) |
| [`weekly-system-self-audit`](skills/weekly-system-self-audit/SKILL.md) | Sunday audit: Sefer cadence, delivery health, Cowork crons, VIP refresh |
| [`meeting-reminder`](skills/meeting-reminder/SKILL.md) | Deterministic no-LLM voice reminders 20 minutes before meetings |
| [`morning-music-alarm`](skills/morning-music-alarm/SKILL.md) | Sonos wake-up music via curl-only SOAP |
| [`daily-brief-export`](skills/daily-brief-export/SKILL.md) | Token-protected JSON endpoint exporting calendar/email/tasks |
| [`daily-job-search-crawl`](skills/daily-job-search-crawl/SKILL.md) | Daily job-search crawl: saved searches, scoring, auto-promote, follow-ups |

### attorney-workflow

| Skill | Use it for |
|---|---|
| [`daily-legal-workflow-app-ideas`](skills/daily-legal-workflow-app-ideas/SKILL.md) | Daily legal-AI research digest + app-idea brainstorm |

### projects

| Skill | Use it for |
|---|---|
| [`poker-hud-advisor`](skills/poker-hud-advisor/SKILL.md) | Real-time Claude advice layer for the poker HUD |

## Adding a skill

- **I wrote it:** drop the folder in `skills/`, add a node to `index.json`.
- **Pulled from GitHub:** run the [intake checklist](docs/INTAKE.md) first, then add to `manifest.json` (pinned commit) and `index.json`.

## Provenance

| Origin | What came from it |
|---|---|
| Sefer (`~/.openclaw/workspace-sefer`) | All 8 market-analysis skills |
| Bari (`~/.openclaw/workspace`) | 8 assistant skills + poker-hud-advisor |
| Cowork (`~/Documents/Claude/Scheduled`) | 4 scheduled-task skills |

Originals were copied, never moved. Scripts keep machine-specific paths as working references.

*Seeded 2026-07-15 from the AI Skills library (built 2026-07-14). Roadmap: Phase 1 complete; next is Phase 2 (first third-party intake) and Phase 3 (bucket-level plugins).*
