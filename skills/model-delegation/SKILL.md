---
name: model-delegation
description: Task-model congruity routing — get expensive-model oversight without expensive-model execution. Use at the start of any multi-step or multi-file task, when the user says "triage this", "delegate this", "use a cheaper model", "have haiku/sonnet do it", "parallelize this", "this is burning tokens", or asks which model should handle something. Differentiator - routes work across model tiers within a session; agent-self-scheduling schedules unattended runs (never this skill's job); concise-planning plans steps, this skill decides who executes them.
---

# Model Delegation

Orchestrator tokens are the most expensive in the stack. The point of this skill:
spend them on judgment (assessment, review), not execution.

## Phase 0 — State check (once per session)

1. **Determine your own tier.** The ladder and the savings math assume the
   orchestrator is the top tier. If you are not (e.g. a Sonnet session), the ratios
   shrink, same-tier delegation saves nothing, and the escalation ladder's top rung
   is a `fable` subagent — not you.
2. **Confirm the spawn mechanism**: subagent with a `model` parameter (or an agent
   definition with pinned `model:` frontmatter). If neither exists on this surface,
   stop — this skill does not apply.
3. Current relative pricing (verify against the platform docs' models overview if
   precision matters; see the falsifiers section if these look stale):
   Haiku 1× · Sonnet 2× · Opus 5× · Fable 10×, input and output alike.

## Skip-floor — check FIRST, before any assessment

Execute directly in-session (no triage) when ANY of:

- Under ~3 steps or ~50 lines of expected output
- Conversational or informational
- **The spec would be longer than the diff.** Writing a fully-self-contained spec is
  orchestrator *output* — the expensive half. If specifying the task costs more than
  the change itself, do it yourself.
- HIGH-risk (defined below) AND expected diff over ~200 lines — mandatory full-diff
  review would approach the cost of doing the work, making delegation strictly worse
- The user assigned the work to you by name

Note the deliberate asymmetry: very large tasks are NOT kept in-session by size —
break them into delegable units instead. Only spec-heavier-than-diff and
oversized-HIGH-risk work stays home.

## Phase 1 — Assessment (structurally bounded)

Answer exactly three one-line questions — if you are writing paragraphs, you have
left the assessment phase:

1. **Band?** TRIVIAL / ROUTINE / STANDARD / COMPLEX / FRONTIER
2. **Risk?** HIGH if it touches security, auth, payments/money movement,
   client/matter/personal data, architecture, or irreversible operations. Else LOW.
3. **Self-contained spec possible?** If genuinely no — the task is inseparable from
   this conversation — keep it. Do not use this as a reflex; most tasks spec out.

| Band | Typical work | Delegate | Effort |
|---|---|---|---|
| TRIVIAL | rename, format, one-file edit | (skip-floor — just do it) | — |
| ROUTINE | boilerplate, CRUD, tests for existing code, docstrings, data reshaping | haiku | default |
| STANDARD | multi-file feature, contained refactor, standard integration, drafts | sonnet | default |
| COMPLEX | cross-cutting refactor, unknown-cause debugging, perf work | opus | low→med |
| FRONTIER | architecture, novel algorithms, long-horizon agentic chains | orchestrator (or `fable` subagent if orchestrator is a lower tier) | — |

**Two-dial rule** for borderline bands: prefer the stronger model at lower effort
over the weaker model at maximum effort (per Anthropic's own guidance that effort is
often a better lever than switching models).

**KEEP list — never delegate the task itself:** security-sensitive logic, credential
handling, client/matter data processing, architecture decisions, work the user
assigned to you personally.

**Stated explicitly, because the asymmetry is load-bearing:** HIGH-risk is *wider*
than KEEP. Auth flows, payment-adjacent code, and irreversible operations MAY be
delegated when band-appropriate — HIGH risk changes the *review* (Phase 3), not the
router. If that posture is ever wrong for a domain, add it to KEEP.

**Confidentiality gate on the spec itself:** the spec you write travels into the
delegate's transcript. Scrub client names, matter identifiers, secrets, and `.env`
values before spawning — delegating a clean task with a dirty spec is a KEEP-list
violation by the back door. This gate becomes an egress question if non-Claude
delegates are ever wired in.

## Delegate registry

| Delegate | Status | Invocation | Band ceiling | Notes |
|---|---|---|---|---|
| haiku | registered | subagent `model: haiku` | ROUTINE | weakest tier — specs fully explicit; it will not infer |
| sonnet | registered | subagent `model: sonnet` | STANDARD | default workhorse |
| opus | registered | subagent `model: opus` | COMPLEX | low→med effort first |
| fable | registered | subagent `model: fable` | FRONTIER | use when orchestrator is a lower tier; else redundant |
| hermes / gpt via openclaw | declared | MCP-wrapped — not wired | TBD | deferred: RAM + wiring; tracked in the library's deferred-work register |
| local (ollama) | declared | MCP-wrapped — not wired | TBD | deferred: RAM-gated; same register |

Registering a delegate = one row (capability ceiling + invocation) + a data-egress
note if it leaves the machine. The rubric never changes.

## Phase 2 — Delegation

Read `references/delegate-prompts.md` before the first spawn of a session. Every
spawn carries three mandatory blocks: self-contained spec, escalation clause,
self-report format. Additionally:

- **Recursion guard:** delegates execute; they never re-triage or sub-spawn. The
  templates state this; do not remove it. The standing policy (if installed) binds
  the top-level session only.
- **Batch the ROUTINE band.** Five docstring fixes are ONE haiku spawn with a
  five-item checklist, not five spawns — every spawn re-pays the context tax.
- **Parallel spawns:** independent scopes only, cap ~3 concurrent, and remember
  "independent" means *touched* files, not spec'd files — lockfiles, barrel files,
  generated types, and snapshots are shared even when specs are disjoint. Use
  worktree isolation where the surface offers it. After ANY parallel batch, run the
  integration verification below — N green self-reports say nothing about the
  merged tree.
- **Surface note (Cowork):** file tools and the shell may see different roots.
  Templates must state absolute paths and require the delegate to confirm its
  verification commands ran against the tree it actually edited.

## Phase 3 — Evaluation (verify → fix → re-verify, tiered by risk)

**Deterministic gate — run yourself on EVERY delegated output, both risk tiers
(~50 tokens, non-negotiable):**

```bash
git status --porcelain            # falsifies SCOPE: "clean"
git diff -- <spec'd paths> | grep -nE '@ts-ignore|eslint-disable|\.skip\(|it\.only|xit\(|# type: ignore'
```

Then check the self-report: MODEL field matches the tier you requested (misroutes
are otherwise invisible); CHECKS contains verbatim command output tails and exit
codes, not summaries. A well-formatted report is not evidence — the raw output tail
is.

**LOW risk:** deterministic gate + self-report scan. Accept on pass.

**HIGH risk:** deterministic gate + orchestrator reads the full diff itself. Never
delegated — that would put the 1× model in judgment over the work that justified
10× oversight.

**Post-parallel integration check:** after merging any parallel batch, re-run the
project's own verification (tests/typecheck) on the combined tree before accepting
any member of the batch.

**Fix loop:** return to the SAME delegate with enumerated fixes — max 2 rounds. If
the surface can't resume a delegate with context intact, the re-spawn must carry the
original spec + the prior self-report + the fix list. Then:

- **Escalate to the band the evidence now implies** — not mechanically one rung. Two
  haiku failures on "ROUTINE" work usually means the band was wrong, not the model.
- **Re-examine the spec before re-spawning.** Repeated failure across tiers is
  better evidence of an underspecified spec than a weak model.
- **Global abort:** cumulative rounds ≥ 4 across all tiers → stop delegating, do it
  in-session, and log the misclassification.

**Never accept, regardless of tier** (the deterministic gate enforces this):
deleted/skipped tests, suppressed checks or lint rules, out-of-scope edits.

## Audit line

Close every delegated task with observables only — no estimated percentages:

```
delegation: STANDARD/LOW → sonnet(default) | rounds: 1 | gate: clean | escalations: 0
```

Session-level accounting: run the explain-usage skill if installed; otherwise note
orchestrator-vs-delegate turn counts manually.

## Failure modes

| Symptom | Action |
|---|---|
| Output plausible but wrong after 2 rounds | escalate to the evidence-implied band; never a 3rd same-tier round |
| Delegate fired its escalation clause | orchestrator answers the blocking question, then re-spawns or absorbs; log it |
| Delegate stalled or returned empty | likely blocked on a permission prompt — check before assuming incompetence; re-spawn with pre-approved tools or absorb |
| Assessment producing paragraphs | structural bound violated — answer the three questions or skip-floor it |
| Orchestrator did ROUTINE work 3+ consecutive turns | red flag, any single trigger fires: triage NOW |
| MODEL field ≠ requested tier | misroute — treat output as untiered; re-spawn correctly |

## Standing-policy install

Only on explicit user request: read `references/policy-block.md` and follow its
proposed-diff procedure (never a blind append). It includes the idempotency check,
the top-level-only binding, and removal instructions.

## What would make this skill wrong

- Tier price ratios move materially, or a tier lands above the current top — Phase 0
  ratios and the FRONTIER row rot first
- The effort parameter's semantics change — the two-dial rule inherits its meaning
  from current docs
- Spawn mechanics change (model param renamed/removed, worktree isolation semantics)
- Two consecutive audits show delegation costing more than in-session execution —
  the skip-floor thresholds are miscalibrated; recalibrate before trusting the rubric
- A delegate tier gains the ability to sub-spawn by default — the recursion guard
  becomes load-bearing and must move from template text to enforcement

---

Pattern provenance: task-type→model mapping seeded by autonomous-agent-patterns §1.2
(this library) and substantially extended (band ceilings, effort dial, registry,
evaluation gate are original); tier positioning and effort guidance from Anthropic's
model docs; band structure, OR-trigger discipline, and checklist shape adapted
(rewritten, not copied) from reviewed community rubrics.
