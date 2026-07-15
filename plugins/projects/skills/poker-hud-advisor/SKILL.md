---
name: poker-hud-advisor
description: Real-time poker table advice layer for a HUD — builds a compact prompt from parsed game state (hero cards, board, pot, stacks) plus per-player session stats (VPIP/PFR/3B/AF/CB/WTSD over hands observed), and queries a fast Claude model with a strict latency budget, falling back from SDK streaming to the claude CLI. Use when working on the poker HUD project, poker hand analysis with player stats, or any build-an-LLM-advisor-into-a-live-loop problem where latency and crash-safety dominate.
---

# Poker HUD Advisor

The Claude analysis layer of a live poker HUD: turn OCR'd game state + tracked player statistics into one short piece of mid-hand advice, fast, without ever crashing the capture loop.

## Design (the constraints that shaped it)

- **Latency budget** — mid-hand advice is worthless late: use a fast model (Haiku-class), stream via the Anthropic SDK when `ANTHROPIC_API_KEY` is set (sub-second first token), fall back to the authenticated `claude` CLI otherwise, hard timeout ~25s.
- **Never raise** — `analyze()` returns an error string instead of throwing, so the HUD input thread can't be killed by an advice query.
- **None-safe formatting** — a fresh session has no stats yet; every stat formats as "—" rather than crashing the prompt build.
- **State reconciliation** — the frame at query time often lacks cards (partial OCR); fall back to what the session tracker remembered for the current hand.
- **Stat line per player** — `{hands}h | VPIP x% PFR x% 3B x% AF x.x CB x% FCB x% WTSD x%` gives the model exploitable reads in one line.

## How to use

1. `scripts/advisor.py` is the working implementation; it depends on sibling modules `parser.py` (GameState, state_summary) and `stats.py` (SessionTracker) from the poker-hud project at `~/.openclaw/workspace/poker-hud/`.
2. The design patterns (latency-tiered model choice, never-raise wrapper, None-safe stats, OCR state fallback) transfer to any live-loop LLM advisor.

## Bundled resources

- `scripts/advisor.py` — the advisor module (analysis layer only; capture/parse/stats live in the project folder).

> Source: `~/.openclaw/workspace/poker-hud/advisor.py`.
