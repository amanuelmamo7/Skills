---
name: skill-distiller
description: Create new agent skills by distilling operational lessons — incidents, post-mortems, repeated corrections, hard-won workflows — into governed, falsifiable SKILL.md packages. A guardrails-first alternative to generic skill authoring: every skill must cite the evidence that motivated it, draw its boundaries before its workflow, and ship with a staleness falsifier. Use whenever the user says "make this a skill," "turn this lesson into a skill," "add this to my skill library," wants a post-mortem or debugging session captured as reusable process, or asks to review a drafted skill for boundary and verification gaps.
---

# Skill Distiller

A skill is a distilled lesson. The best ones are not brainstormed — they are extracted from evidence: an incident that cost an afternoon, a correction the user had to make twice, a workflow whose unfun parts kept getting skipped. This skill encodes the distillation process, and it differs from generic skill-authoring in one core commitment: **the guardrails are designed before the workflow, and the evidence is named before either.**

## Phase 0 — The evidence gate

A skill is warranted when you can point at one of these:

- **An incident or post-mortem** — something broke, the diagnosis is written down, and the failure could recur.
- **A repeated correction** — the user has fixed the same behavior twice. Twice is a pattern; once is noise.
- **Re-prompting fatigue** — the same multi-step instructions keep getting re-typed across sessions.
- **Skipped discipline** — free-form output keeps omitting the unfun parts (the sources footer, the falsifier section, the verification step). Templates enforce structurally what prose skips.

A skill is NOT warranted for style preferences (that's a system prompt), things the model already knows (don't re-teach), or a capability used once. If you cannot name the motivating evidence in one sentence, the skill is speculative — say so and ask whether to proceed anyway.

**Output of this phase:** a one-paragraph lesson statement plus a provenance line — `Born from: <incident / correction / workflow>, <date>`. This line ships in the final SKILL.md. A skill that can't cite its lesson can't be trusted to encode it.

## Phase 1 — Draw the boundary card (before the workflow)

Writing the workflow first and bolting on caveats later produces happy-path skills. Draw the boundaries first, using `assets/skill-template.md`:

1. **Hard lines** — what this skill must never do, stated once, structurally. A hard line is a design constraint, not a disclaimer ("no buy/sell directives, even when asked directly" beats "this is not financial advice").
2. **Judgment vs. determinism split** — for each part of the job, decide: does this need a model, or a script? Time-critical, fragile, or consistency-critical steps go in code with the reasoning documented ("announce exactly once" is a script property, not a prompt property). Judgment calls stay in prose. Reserve the LLM for what actually requires one.
3. **The interrupt bar** — if the skill runs proactively or on a schedule: what clears the bar for bothering the user, by rule not vibe? Everything else is logged or silent. Deduplicate by state file, never by memory.
4. **Degrees of freedom** — match instruction strictness to fragility: loose heuristics where many approaches are valid, exact numbered steps where a wrong move is costly. Numbered atomic steps buy resumability for free.
5. **Failure modes** — for every step that can fail, what does failure look like and what happens next? Include halt-for-user gates for steps only a human can do: print exactly what to run, mark paused, wait. Never silently pretend success.
6. **The staleness falsifier** — every skill ends with `## What would make this skill wrong`: the specific observation (an API change, a schedule change, a repeated user override) that means the skill is outdated and must be revised, not re-run. Skills rot; a skill that names its own expiry conditions gets fixed instead of quietly misfiring.

## Phase 2 — Draft the body

- **Template over prose.** If the output has required elements, give it a template with a slot for each — a slot for the prior, a slot for the sources footer, a slot for the falsifier. Structure enforces what prose skips.
- **State-check before action.** Verify setup exists before using it; branch to setup instructions if not.
- **Evidence of execution, not presence of instructions.** "The instruction is in the skill" is not evidence it ran — the log line, the file on disk, the checkable artifact is. For each step that matters, name the artifact that proves it happened, and have the skill check it.
- **Destructive writes go through a proposed-diff gate.** Write to `<file>.proposed`, show the diff, apply on approval. Reversible until the moment of commit.
- **Run memory is append-only.** If the skill runs repeatedly and must not repeat itself, give it an append-only log it reads at start and appends to at end — never rewrites.
- **Explain why, not just what.** Every constraint in the body should carry its reason in-line. Models follow understood rules better than bare imperatives, and future maintainers can tell load-bearing rules from incidental ones.

## Phase 3 — The routing contract and library fit

- **Description = what + when + differentiator.** It is the only thing the agent sees before deciding to load the skill; if the skill doesn't trigger, the description is wrong, not the body. Include the trigger phrases a real user would type. Describe what and when — never summarize the how, or the agent will follow the summary and skip the body.
- **Check the library before shipping.** Does this overlap an existing skill? If so, write the disambiguation down ("prefer X for interactive use; this skill is the scheduled pipeline") — in both skills or in the library's routing index if one exists.
- **Declare dependencies and risk.** If the skill needs a CLI, an endpoint, a credential, or another skill, list them. If it runs commands, acts unattended, or delegates trust to external code, label it prominently so a library index can surface the flag.

## Phase 4 — Verify like an operator

1. **Trigger test** — describe the target task naturally, without naming the skill. If it doesn't fire, fix the description.
2. **Execution test** — invoke it explicitly on the original motivating case. The skill must beat the from-scratch baseline on the very lesson it distills, or it isn't carrying the lesson.
3. **Adversarial pass** — ask (or have a second model ask): what input breaks this? What edge case does the boundary card miss? Patch the gaps that are real; resist patching hypotheticals into bloat.
4. **Split your confidence.** Confidence that the skill triggers correctly and confidence that it produces the right output are independent quantities — report both, and name what evidence would raise the lower one.
5. **Ship v1, log the rest.** Version the skill, record deferred improvements in a follow-up register (what / why-not-now / what-would-trigger-doing-it), and let real usage — not speculation — drive v1.1.

## Bundled resources

- `assets/skill-template.md` — the skeleton every distilled skill starts from, boundary card included.
- `references/distillation-checklist.md` — the full pre-ship checklist; run it before calling any skill done.

## Lineage

This process synthesizes three sources: Anthropic's skill-creator methodology (test-with/without baselines, description-as-trigger, generalize-don't-overfit), community skill-authoring guides (progressive disclosure, routing contracts, degrees of freedom), and the operational lessons of running scheduled agents in production — where the patterns above (verify-before-trust, halt-for-user, proposed-diff gates, evidence-of-execution, split confidence) were each learned the expensive way.

## What would make this skill wrong

If your agent platform gains first-class skill-testing infrastructure with baseline comparison built in, Phase 4 should defer to it. If a library grows past the point where manual overlap-checking works, Phase 3 needs a registry tool, not a checklist. And if you find yourself distilling skills nobody invokes twice, the evidence gate is being skipped — return to Phase 0.
