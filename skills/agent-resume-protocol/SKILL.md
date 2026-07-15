---
name: agent-resume-protocol
description: Protocol for resuming work after an agent subprocess dies mid-task — detect "continue" signals, reconstruct state from breadcrumb logs, state your inference before acting — plus the habit of logging [intent] breadcrumbs before every slow operation. Use in any hook/cron-spawned agent where turns can be watchdog-killed.
---

# Agent Resume Protocol (with Breadcrumb Logging)

Each hook or cron invocation spawns a fresh subprocess with no memory of prior subprocesses except what reached disk. If a turn died mid-tool-call (a watchdog typically kills processes after ~180s of silent waiting on a slow fetch or another agent), in-flight state never persisted — only completed turns are in the log. This protocol makes recovery deterministic instead of guesswork.

## Part 1 — Breadcrumbs: leave them BEFORE slow operations

Before any tool call or multi-step work expected to take more than ~30 seconds (chained web fetches, slow bash, waiting on another agent's hook, multi-stage analysis), append one line to today's daily log (`memory/YYYY-MM-DD.md`) BEFORE firing the call:

```
[intent] <verb> <object> — expected duration <N>, expected output <where>
```

Example:

```
[intent] firing pre-market hook at sibling agent — expected ~6 min, expected output memory/2026-06-02-pre-market.md
```

If the subprocess dies mid-call, the next session reads this and knows exactly what was in flight. Cost: one tiny disk write. Benefit: resume becomes deterministic. For cron-fired turns, make the breadcrumb the very first action of the templated prompt; for ad-hoc work, apply it manually.

## Part 2 — Detect resume signals

Trigger the protocol when the user message is one of: "continue", "continue where you left off", "resume", "pick up where you stopped", "keep going", "go on" — AND the prior assistant turn either:

- ended mid-action without a closing summary, or
- was followed by a runtime error like `CLI produced no output for Ns and was terminated`, or
- references "running/testing/firing/verifying/fetching" without a result.

## Part 3 — Resume protocol (in order)

1. **Read today's conversation log** (e.g. `memory/conversations/YYYY-MM-DD-<channel>.md`), last ~10 entries. Identify the most recent task requested and the last visible step before the gap.
2. **Read today's daily log for `[intent]` breadcrumbs** (`memory/YYYY-MM-DD.md`). The last breadcrumb is usually the resume point.
3. **Reconstruct and STATE explicitly before acting.** Reply in exactly this shape:

   ```
   Resuming.
   Last task: <what the user asked for>
   Last visible completion: <what made it into the log>
   Where we stopped: <best inference, with confidence noted>
   Resuming from: <concrete next step>
   ```

   If genuinely uncertain (multiple plausible resume points, no clear in-flight task), ask ONE short clarifying question instead of guessing. Do NOT produce a generic status digest — that is the classic failure mode: told "continue," the agent summarizes recent activity instead of resuming the in-flight task.

4. **Proceed with the next step only** — not the whole task. Re-verify each subsequent step against disk state, not memory (the breadcrumb's expected output may or may not exist; check).

## Part 4 — Avoid getting killed in the first place

Synchronous silent waits are the main watchdog hazard. Prefer:

- **Polling loop with progress markers:** fire the slow op, poll the expected output path every ~10s, print a one-line status each cycle. Flowing stdout keeps the watchdog asleep, and the polling state is itself visible to any resume session.
- **Progress markers between chained fetches:** print `fetched X ✓` after each so stdout never goes silent for minutes.
- **Background invocation:** run long bash in the background and check on it later.
- **Sub-agent dispatch:** spawn independent heavy work rather than waiting in-line.

If you're about to wait silently, ask whether you can poll instead.

## Checklist

- [ ] Breadcrumb written before every >30s operation, including expected output path
- [ ] Resume signal detection covers both the phrase and evidence of a dead turn
- [ ] Reconstruction stated to the user before any action
- [ ] Uncertain inference → one clarifying question, never a status digest
- [ ] Resume executes the next step only, verifying against disk each step
