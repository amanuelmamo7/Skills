# Skill Skeleton — start every distilled skill from this

```markdown
---
name: <kebab-case, matches folder name exactly>
description: <WHAT it does> + <WHEN to use it, with the trigger phrases a real user would type> + <DIFFERENTIATOR vs. related skills>. Never summarize the how.
---

# <Skill Title>

<One paragraph: the job this skill does and the lesson it encodes.>

> Born from: <the incident / repeated correction / workflow that motivated this skill>, <date>.

## Boundary card

**Hard lines** — this skill never:
- <constraint stated as a design rule, not a disclaimer — with its reason>

**Judgment vs. determinism:**
- In code (deterministic): <steps where variation is a bug — and why>
- In prose (judgment): <steps that genuinely need a model>

**Interrupt bar** (delete if the skill never runs proactively):
- Surface to the user only when: <rule, not vibe>
- Everything else: <logged where / silent>
- Dedup: <state file path + key scheme>

## Workflow

<Numbered atomic steps. Strictness scaled to fragility. For each step that matters:>

1. <Action.> Verify: <the artifact that proves this step ran — log line, file, response body>.
2. <Action.> On failure: <what failure looks like → what to do — retry / skip / halt>.
3. <If only a human can do this step:> HALT FOR USER — print exactly: `<command>`, then wait.

<Destructive writes: write to `<file>.proposed`, show the diff, apply only on approval.>

<State-check before action: "First verify <setup> exists: <command>. If not, <setup steps>.">

## Output format

<The exact template the output must fill, with a slot for every required element —
including a `Sources & timestamps` footer if the skill touches live data.>

## Run memory (delete if single-shot)

Read `<log file>` at start; append one line at end: `<YYYY-MM-DD>: <what happened>`.
Append-only — never rewrite.

## What would make this skill wrong

- <The specific observation that means this skill is outdated and must be revised — an API change, a schedule change, the user overriding the same behavior twice.>
```
