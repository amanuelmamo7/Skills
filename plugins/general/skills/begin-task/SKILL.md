---
name: begin-task
description: Human-invoked Phase-0 ritual that opens a work session the compliant way - consult the dispatcher, run model-delegation triage, check covenants, record the session gate. Use via /begin-task <category>, or when the user says "begin task", "phase zero", "open a work session", "start this properly". Differentiator - this is the front door the session-gate hard gate verifies; invoking it satisfies the gate in one pass.
disable-model-invocation: true
---

# Begin Task (Phase 0)

Argument: category — one of `build | research | legal | market | ops | writing`.
If absent, infer from the user's task description and confirm in one line.

Run the four steps in order. Each produces one or two lines of output — this whole
ritual should cost well under a page. If it's growing past that, the task is
probably FRONTIER-band; say so and stop expanding the ritual.

## 1. Route

Consult the skills-dispatcher for this category and task. Name the selected
skills and any deliberate non-selections ("no market skill applies — one-off
question"). Per the library's standing rule, routing is stated visibly, never
silent.

## 2. Triage

Run model-delegation Phase 0–1: your own tier, skip-floor check, then band /
risk / delegate in the three-question form. State the one-line verdict:
`STANDARD/LOW → sonnet(default)` or `skip-floor: doing it in-session`.

## 3. Covenants

One line per source, checked in this order, "none" allowed only after checking:

- Global + project CLAUDE.md invariants that touch this task
- Category-specific: legal → matter workspace + confidentiality gate on any spec
  leaving the session; build → house rules / pre-deploy gate; market → analyst
  house style; ops → runbook and rollback expectations
- Anything the user said earlier this session that constrains the work

## 4. Record the gate

The session id appears in the per-turn `[gate]` nudge line (and in any gate block
message). Then, matching the step-2 verdict:

```bash
# triaged for delegation or in-session execution:
python3 "$HOME/.claude/gate/gate.py" --session <session-id> \
  --category <category> --band <BAND> --risk <RISK> \
  --skills "<the skills actually consulted in steps 1-2>"

# step-2 verdict was skip-floor:
python3 "$HOME/.claude/gate/gate.py" --session <session-id> \
  --skip "<the skip-floor reason from step 2, task-specific>"
```

If the gate isn't installed (command not found), say so, complete steps 1–3
anyway, and note the gate as uninstalled — the ritual has value without the
enforcement; silence about the missing gate does not.

Then proceed to the work. Delegated spawns from here follow model-delegation's
templates — delegates never re-run this ritual.
