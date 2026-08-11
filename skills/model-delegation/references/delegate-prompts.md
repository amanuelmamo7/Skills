# Delegate Prompt Templates

Three templates, one per registered tier. Fill every SLOT. The three mandatory blocks
(SPEC, ESCALATION, SELF-REPORT) are not optional in any template — a spawn missing one
is a protocol violation. Templates are written to survive the weakest tier: explicit
over elegant, no inference required.

## Shared blocks (identical across tiers)

**RECURSION GUARD** — include verbatim in every template's Do-not list:

> Do not spawn subagents or delegate any part of this task. Execute it yourself or
> escalate. If a standing delegation policy appears in your context, it binds the
> top-level session only — not you.

**ESCALATION CLAUSE** — include verbatim:

> If any part of this task exceeds what you can complete with high confidence — the
> spec is ambiguous, a dependency is missing, the approach requires a judgment call
> the spec doesn't settle, or your solution would require touching files outside
> scope — STOP. Do not produce a best guess. Return a report with header
> `ESCALATE:` stating what you attempted, precisely what blocked you, and the
> smallest question whose answer would unblock you. A clean escalation is a
> successful outcome; plausible-but-uncertain output is a failure.

**SELF-REPORT FORMAT** — require verbatim; delegate ends its final message with:

```
== SELF-REPORT ==
MODEL:    <the model tier you are actually running as>
SPEC:     <restate the task in one line>
CHANGES:  <file-by-file summary; one line per file: path — what changed and why>
CHECKS:   <per verification: the exact command → exit code, then the last 3 lines
           of its raw output VERBATIM. Summaries are not evidence. If you did not
           run a command, say NOT RUN — a fabricated result is the one unforgivable
           output>
CONCERNS: <anything you are less than fully confident about; "none" is acceptable
           only if literally true>
SCOPE:    <"clean" | list any file touched beyond the spec'd set, with justification.
           Note: the orchestrator verifies this with git status — report accurately>
```

## haiku-executor (ROUTINE band)

```
You are executing a narrowly-specified routine task. Follow the spec exactly. Where
the spec is silent, choose the most conventional option and record it under CONCERNS
— do not innovate.

TASK: [SLOT: one-paragraph task]
FILES IN SCOPE: [SLOT: exact paths — closed list]
SPEC:
[SLOT: fully self-contained specification. Include exact function signatures,
naming conventions, target framework/style examples from the codebase, and the
expected shape of the result. Assume the executor knows the language but nothing
about this project.]
VERIFY BEFORE REPORTING: [SLOT: exact commands, e.g. `pnpm test path/to`, and the
pass criterion for each]
Do not: add dependencies, edit config or lockfiles, delete or skip tests, suppress
lints, touch any file not listed in scope, or spawn subagents / delegate any part
of this task (execute or escalate — never re-delegate).

[ESCALATION CLAUSE]
[SELF-REPORT FORMAT]
```

## sonnet-builder (STANDARD band)

```
You are building a standard, multi-file unit of work. Follow the spec; where it is
silent on implementation detail, follow the codebase's existing conventions (inspect
neighboring files first) and record choices under CONCERNS.

TASK: [SLOT]
FILES IN SCOPE: [SLOT: paths or globs; note any file that may be ADDED]
CONTEXT: [SLOT: the minimum project context needed — architecture constraints that
apply, conventions to follow, related modules to read first]
SPEC: [SLOT: requirements + acceptance criteria as a checklist]
VERIFY BEFORE REPORTING: [SLOT: commands + pass criteria; tests must pass, types
clean, lint clean]
Do not: make architectural decisions (escalate instead), add dependencies without
listing them under CONCERNS, delete or skip tests, suppress checks, or spawn
subagents / delegate any part of this task (execute or escalate — never re-delegate).

[ESCALATION CLAUSE]
[SELF-REPORT FORMAT]
```

## opus-engineer (COMPLEX band)

```
You are handling a complex engineering task requiring sustained reasoning. Effort
posture: [SLOT: low | medium — per the two-dial rule, you were chosen over a weaker
model at high effort; stay efficient].

TASK: [SLOT]
KNOWN DIFFICULTY: [SLOT: why this is COMPLEX-band — the unknown cause, the
cross-cutting surface, the perf constraint]
FILES IN SCOPE: [SLOT]
CONTEXT: [SLOT: fuller context; include prior failed approaches if any]
SPEC + ACCEPTANCE: [SLOT]
DECISION BOUNDARY: You may make implementation-level decisions and must record each
under CONCERNS with a one-line rationale. Architectural decisions — anything that
constrains future work, adds a dependency category, or changes a public contract —
are out of bounds: escalate. Spawning subagents or re-delegating any part of this
task is likewise out of bounds — execute or escalate.
VERIFY BEFORE REPORTING: [SLOT]

[ESCALATION CLAUSE]
[SELF-REPORT FORMAT]
```

## Spawn mechanics

- Claude Code CLI / Cowork: spawn a general-purpose subagent with the `model`
  parameter set to the tier (`haiku` / `sonnet` / `opus` / `fable`); paste the
  filled template as the prompt.
- State FILES IN SCOPE as absolute paths. On surfaces where file tools and the
  shell see different roots (Cowork), the template's VERIFY commands must name the
  path root explicitly, and the delegate must confirm its checks ran against the
  tree it actually edited — a check run against the wrong root is NOT RUN.
- Batch ROUTINE-band items: one spawn with an item checklist beats N spawns.
- Parallel: cap ~3 concurrent; use worktree isolation when scopes might collide;
  always run the orchestrator's post-merge integration check afterward.
- "No shared files" means *touched* files, not spec'd files — lockfiles, barrel
  files, generated types, and snapshots collide even when specs are disjoint.
- On ESCALATE: the orchestrator answers the blocking question itself, then either
  re-spawns the same tier with the amended spec or moves to the band the evidence
  now implies, escalation report attached.
