---
name: agent-install-runbook
description: Method for one agent to autonomously install a sibling agent (or any risky multi-step system change) using atomic checkpointed steps, halt-for-user gates, structured status lines, and a tested rollback. Use when writing or executing a runbook where an agent modifies shared config, schedulers, or installs another agent.
---

# Agent Install Runbook Pattern

When one agent installs a sibling agent — or performs any multi-step change to shared infrastructure — improvisation is the enemy. Write the runbook first; the executing agent follows it mechanically.

## Operating mode (put this at the top of every runbook)

1. **Atomic steps.** Each numbered step is one transaction: run its `action`, then run its `verify`. If verify fails, write FAIL to the checkpoint and STOP. Never proceed past a failed verify.
2. **Checkpoint after every step.** Maintain a JSON checkpoint file in the target workspace: `{"step": N, "status": "ok"|"fail"|"halted-for-user"|"complete", "note": "...", "ts": "..."}`. On resume, read it and start at step N+1.
3. **Structured reporting.** After each step emit exactly one line: `STEP <N> <ok|fail|halted-for-user> — <note>`. End the run with a summary block listing all step outcomes.
4. **Verify live, not from memory.** Every verify is a real command on the host — never a recollection of how it usually works.
5. **HALT-FOR-USER gates** mark steps the agent cannot do autonomously. At those, write `halted-for-user` to the checkpoint, print exactly what the user must do (copy-pasteable commands) plus the resume phrase, and STOP.
6. **No improvisation.** If a verify fails in a way the runbook doesn't anticipate, halt rather than guess.

## Runbook skeleton

- **Step -1 — Hard preconditions.** A table of check / command / required-result rows (service up, credentials loaded, source files readable). Any failure → halt at step 0.
- **Step 0 — Initialize checkpoint** file; verify by reading it back.
- **Step 1 — Backup everything you will touch** (config files, crontab, plists) with a shared timestamp stamp saved to a stamp file. Verify backups exist and are non-empty. No backup, no proceeding.
- **Middle steps — the actual install:** move workspace into place, write scripts/prompts, set permissions. Each with an explicit verify (file-exists tests, `echo "manifest OK"` style assertions).
- **Config-change step — propose, don't apply.** Write the new config to a `.proposed` sibling file and show the diff. Never edit the live config directly.
- **HALT-FOR-USER gate — apply config and restart the service.** If applying requires restarting the process that hosts the executing agent, the agent must not do it (it would kill itself mid-task). Print the exact commands for the user, plus the abort path ("if the diff looks wrong, `rm` the .proposed file and tell me").
- **Resume step — smoke test.** After the user resumes, verify the service is back and the new agent responds: send it a message demanding an exact sentinel reply ("Respond with exactly: <AGENT> ALIVE") and grep for it.
- **Scheduling step.** Append (never overwrite) scheduler entries; verify the new entries exist AND diff against the backup to prove pre-existing entries were preserved.
- **Final step — end-to-end dry run.** Fire one real job and verify multiple independent conditions (no auth errors in the log, output file exists, expected footer present, non-trivial size). All pass = install complete.

## Final summary block

On completion, emit a structured summary: what was installed and where, what was backed up and where, the first output produced, open items only the user can do (e.g. "populate the secrets file with API keys"), and the next scheduled run. On failure, list the failing step, the verify output, and point to rollback.

## Rollback section (mandatory)

A single copy-pasteable block that restores the pre-install state: restore config from the stamped backup, restore the scheduler from its backup, restart the service. Leave the new workspace in place for re-attempt unless abandoning.

## Resume protocol (mandatory)

If restarted mid-install: read the checkpoint file; print "Resuming from step N+1"; do not redo completed steps; if the checkpoint is missing, start from step 0.

## Don't-do list (tailor per runbook)

- Do not edit live shared config directly — only via the `.proposed` pattern.
- Do not restart the service hosting yourself.
- Do not invent step numbers beyond those defined.
- Do not write into OS-protected directories the agent can't reliably access.
- Do not delete staging/source material until the copy-into-place step has verified.

## Kickoff prompt for the executing agent

Pair the runbook with a short kickoff message the user pastes to the executing agent, restating the operating rules (halt on first verify failure, maintain the checkpoint, print the halt block verbatim at the gate, emit STEP lines, end with the summary) and granting explicit scoped approval ("you may modify <config> via the .proposed pattern only"). Also prepare a one-line resume phrase ("resume <name> install") and a status-query phrase ("what step are you at? read the checkpoint and report").

## Hard-won gotchas to encode in your runbooks

- Distinguish similarly-named credentials (e.g. a webhook token vs. a gateway admin token) and make error messages name the right one.
- Async job systems return success immediately; the real output lands later — verify with patience windows, not instant checks.
- Cosmetic errors exist (e.g. a delivery-status quirk that logs `error` alongside a successful output file) — document them so the executor doesn't halt on noise.
