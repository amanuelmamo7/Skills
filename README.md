# Skills

Curated skills library — reviewed, pinned, and indexed. Skills I write myself and skills pulled from other repos that have passed the [intake checklist](docs/INTAKE.md).

**How this repo works**

- Every skill is a folder in [`skills/`](skills/) with a `SKILL.md` (plus optional `assets/`, `references/`, `scripts/`).
- [`index.json`](index.json) is the source of truth: every skill, its buckets, provenance, review status, and the relationships between skills. The tables below are generated from it.
- [`manifest.json`](manifest.json) is the provenance ledger for third-party skills — each pinned to the exact commit reviewed. Updates are diff-reviews, never blind re-pulls.
- [`.claude-plugin/`](.claude-plugin/) makes this repo installable in Claude Code: `/plugin marketplace add amanuelmamo7/Skills`
- Nothing here updates automatically. A skill enters or changes only after human review.
- A [weekly drift audit](.github/workflows/drift-audit.yml) compares every pinned commit against upstream and opens an issue when a vendored skill changed — run it manually anytime with `python3 tools/drift_audit.py`.
- [`graph.html`](graph.html) is an interactive view of the knowledge graph — open it in a browser.
- After ANY change to index.json, run `python3 tools/build.py` to regenerate plugins, README tables, and the graph.

## Installing

Add the marketplace once, then install only the buckets you need:

```
/plugin marketplace add amanuelmamo7/Skills
/plugin install personal-assistant@amanuel-skills
/plugin install attorney-workflow@amanuel-skills
```

Available plugins: `skills-library` (everything), `general`, `web-application`, `attorney-workflow`, `market-analysis`, `personal-assistant`, `projects`, `agent-infrastructure`.

Bucket plugins under [`plugins/`](plugins/) are **generated** from index.json by [`tools/build_plugins.py`](tools/build_plugins.py) — never edit them by hand. After adding or re-bucketing a skill, run `python3 tools/build_plugins.py` and commit the result.

## Buckets

<!-- GENERATED-BUCKETS:START (run tools/build_readme.py — do not edit by hand) -->
Buckets are metadata, not folders — a skill can live in more than one.

| Bucket | Skills | Status |
|---|---:|---|
| personal-assistant | 15 | active |
| web-application | 9 | active |
| market-analysis | 8 | active |
| agent-infrastructure | 5 | active |
| general | 5 | active |
| projects | 1 | active |
| attorney-workflow | 1 | active |

### personal-assistant (from Bari + Cowork, plus reviewed third-party)

| Skill | Use it for |
|---|---|
| [`morning-brief`](skills/morning-brief/SKILL.md) | Daily start-of-day brief: calendar, filtered email signal, tasks |
| [`evening-wrap`](skills/evening-wrap/SKILL.md) | End-of-workday wrap: tomorrow's calendar, honest review of today |
| [`weekly-wrap`](skills/weekly-wrap/SKILL.md) | Friday synthesis of the week's logs: themes, time allocation |
| [`memory-maintenance`](skills/memory-maintenance/SKILL.md) | Weekly distillation of raw logs into durable long-term memory |
| [`assistant-heartbeat`](skills/assistant-heartbeat/SKILL.md) | Periodic rotating check (email/calendar/cron health) |
| [`meeting-reminder`](skills/meeting-reminder/SKILL.md) | Deterministic no-LLM voice reminders 20 minutes before meetings |
| [`morning-music-alarm`](skills/morning-music-alarm/SKILL.md) | Sonos wake-up music via curl-only SOAP |
| [`daily-brief-export`](skills/daily-brief-export/SKILL.md) | Token-protected JSON endpoint exporting calendar/email/tasks |
| [`daily-job-search-crawl`](skills/daily-job-search-crawl/SKILL.md) | Daily job-search crawl: saved searches, scoring, auto-promote, Monday follow-ups |
| [`weekday-morning-brief`](skills/weekday-morning-brief/SKILL.md) | Weekday 8am brief: calendar, VIP email + reply drafts, markets, system health |
| [`weekly-system-self-audit`](skills/weekly-system-self-audit/SKILL.md) | Sunday audit: Sefer cadence, delivery health, Cowork crons, VIP auto-refresh |
| [`internal-comms`](skills/internal-comms/SKILL.md) | Status reports, leadership updates, and newsletters in repeatable formats (Anthropic) |
| [`audio-transcriber`](skills/audio-transcriber/SKILL.md) | Local Whisper transcription of meetings/audio to structured markdown — ⚠ see manifest |
| [`time-ledger`](skills/time-ledger/SKILL.md) | Natural-language time tracking into user's own Notion DB |
| [`privacy-mask`](skills/privacy-mask/SKILL.md) | PII/secret redaction in screenshots via OCR — ⚠ see manifest |

### web-application (third-party, from Agentic Awesome Skills — pinned `5e31f23`)

| Skill | Use it for |
|---|---|
| [`form-cro`](skills/form-cro/SKILL.md) | Form conversion-rate optimization methodology |
| [`frontend-design`](skills/frontend-design/SKILL.md) | Design direction and visual quality guidance for web UI |
| [`frontend-developer`](skills/frontend-developer/SKILL.md) | Frontend engineering persona and capability catalog |
| [`nextjs-app-router-patterns`](skills/nextjs-app-router-patterns/SKILL.md) | Next.js App Router patterns and playbook |
| [`nextjs-best-practices`](skills/nextjs-best-practices/SKILL.md) | Next.js App Router principles and best practices |
| [`react-best-practices`](skills/react-best-practices/SKILL.md) | Vercel Engineering's React performance guide (47 rules) |
| [`seo-audit`](skills/seo-audit/SKILL.md) | Diagnostic-only SEO audit framework |
| [`shadcn`](skills/shadcn/SKILL.md) | shadcn/ui component workflows via the official CLI — ⚠ see manifest |
| [`tailwind-patterns`](skills/tailwind-patterns/SKILL.md) | Tailwind CSS v4 patterns and reference |

### market-analysis (from Sefer)

| Skill | Use it for |
|---|---|
| [`pre-market-brief`](skills/pre-market-brief/SKILL.md) | Morning market rundown: overnight tape, catalysts, earnings docket |
| [`post-market-brief`](skills/post-market-brief/SKILL.md) | End-of-day wrap + gainers tracking with catalyst verification |
| [`macro-readthrough`](skills/macro-readthrough/SKILL.md) | CPI/PCE/NFP/GDP/FOMC prints: what's under the headline |
| [`weekly-deep-dive`](skills/weekly-deep-dive/SKILL.md) | Weekly aggregation of daily gainers: what held, what faded |
| [`stock-deep-dive`](skills/stock-deep-dive/SKILL.md) | 12-section deep-dive on a single stock's big move |
| [`company-thesis`](skills/company-thesis/SKILL.md) | Full company thesis: what's priced in, bull/bear cases, catalysts |
| [`trend-justification`](skills/trend-justification/SKILL.md) | Is this rally justified? Observed/Implied/Actual/Gap framework |
| [`pointed-analysis`](skills/pointed-analysis/SKILL.md) | Sharp one-off market questions: direct answer, fetch log, falsifiers |

### agent-infrastructure (third-party, from Agentic Awesome Skills — pinned `5e31f23`)

| Skill | Use it for |
|---|---|
| [`ai-agents-architect`](skills/ai-agents-architect/SKILL.md) | Agent system design patterns and sharp edges |
| [`autonomous-agent-patterns`](skills/autonomous-agent-patterns/SKILL.md) | Autonomous agent design patterns: loops, permissions, sandboxing |
| [`agent-orchestration-improve-agent`](skills/agent-orchestration-improve-agent/SKILL.md) | Methodology for measuring and improving an agent's performance |
| [`agent-self-scheduling`](skills/agent-self-scheduling/SKILL.md) | Scheduling unattended recurring agent runs (cron + pre-approved tools) — ⚠ see manifest |
| [`agent-memory-mcp`](skills/agent-memory-mcp/SKILL.md) | Persistent agent memory via external MCP server (webzler/agentMemory) — ⚠ see manifest |

### general (third-party, from Agentic Awesome Skills — pinned `5e31f23`)

| Skill | Use it for |
|---|---|
| [`gemini-deep-research`](skills/gemini-deep-research/SKILL.md) | Autonomous multi-step research with cited reports via Gemini API |
| [`bulletmind`](skills/bulletmind/SKILL.md) | Any input into clean hierarchical bullet notes |
| [`professional-proofreader`](skills/professional-proofreader/SKILL.md) | Proofread and correct documents while preserving voice |
| [`research-prompt`](skills/research-prompt/SKILL.md) | Turns vague asks into one precise deep-research prompt |
| [`efficient-web-research`](skills/efficient-web-research/SKILL.md) | Token-efficient web research protocol |

### projects

| Skill | Use it for |
|---|---|
| [`poker-hud-advisor`](skills/poker-hud-advisor/SKILL.md) | Real-time Claude advice layer for the poker HUD |

### attorney-workflow

| Skill | Use it for |
|---|---|
| [`daily-legal-workflow-app-ideas`](skills/daily-legal-workflow-app-ideas/SKILL.md) | Daily legal-AI research digest + app-idea brainstorm with run-memory dedup |
<!-- GENERATED-BUCKETS:END -->

## Adding a skill

- **I wrote it:** drop the folder in `skills/`, add a node to `index.json`.
- **Pulled from GitHub:** run the [intake checklist](docs/INTAKE.md) first, then add to `manifest.json` (pinned commit) and `index.json`.

## Provenance

| Origin | What came from it |
|---|---|
| Sefer (`~/.openclaw/workspace-sefer`) | All 8 market-analysis skills |
| Bari (`~/.openclaw/workspace`) | 8 assistant skills + poker-hud-advisor |
| Cowork (`~/Documents/Claude/Scheduled`) | 4 scheduled-task skills |
| [Agentic Awesome Skills](https://github.com/sickn33/agentic-awesome-skills) @ `5e31f23` | 23 skills: 9 web-application, 5 agent-infrastructure, 5 general, 4 personal-assistant (intake 2026-07-15; 11 rejected — see manifest.json) |

Originals were copied, never moved. Scripts keep machine-specific paths as working references.

*Seeded 2026-07-15 from the AI Skills library (built 2026-07-14). Roadmap: Phases 1-2 complete (first third-party intake done); next is Phase 3 (bucket-level plugins).*
