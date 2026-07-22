---
name: legal-writing-editor
description: Four-pass editing gate for legal drafts — structure (explanation-of-law separated from application, everything explained actually applied and vice versa), flow (roadmaps, headings, topic sentences, transitions), sentences (one idea each, subjects near verbs, minimal passive and nominalization, consistent terminology), and mechanics (proofread, pincites present, defined terms consistent). Use when the user asks to edit, polish, tighten, or review a memo, letter, brief section, or any legal draft — and as the final pass on every attorney-workflow skill's output before delivery. Differentiator: edits style, flags substance — it never silently changes legal meaning.
---

# Legal Writing Editor

Editing legal writing is two different jobs pretending to be one: checking the *analysis architecture* (did the draft explain the law it applies and apply the law it explains?) and polishing the *prose*. This skill runs both as an ordered checklist — because an editing pass that starts with commas never gets to the missing counter-analysis.

> Born from: the recurring failure of single-pass editing — surface polish applied to structurally broken drafts — and the observation that architecture checks are mechanical enough to run as a deterministic list. Method is standard legal-editing doctrine, expressed originally. Built with `skill-distiller`.

## Boundary card

**Hard lines** — this skill never:
- Silently changes legal substance. Style edits (structure, flow, sentences, mechanics) are made; substantive problems (wrong rule, missing element, unsupported conclusion, absent counter-analysis) are **flagged with a note, not fixed** — substance belongs to the author and the house rules, not the editor (`references/legal-house-rules.md`, rule 8 by analogy: the editor supports, it doesn't opine).
- Introduces a citation, fact, or authority the draft didn't contain. Editing adds nothing to the record.
- "Improves" calibration language. "Likely" does not become "clearly"; hedges the author chose survive unless flagged as unsupported by the draft's own analysis.

**Judgment vs. determinism:** whether a flagged substance issue is real is judgment (the author's). The four passes, their order, and their checks are fixed — run all four, in order, every time.

## The four passes

**Pass 1 — Architecture (per legal argument).**
- Explanation of the law and application to the facts are separated, in that order — a paragraph doing both at once is doing neither well.
- Parity check, both directions: every rule or case explained is used in the application (unused explanation is excess — cut or flag); every rule or case relied on in the application was explained first (unexplained reliance is an omission — flag).
- Each case illustration is complete enough for the use its analogy makes of it — no comparison to facts the illustration never gave the reader.
- Conclusions appear where the reader needs them: up front for the argument, restated after the analysis. Flag conclusions that appear only at the end.
- Counter-analysis present where the question is genuinely contestable; flag its absence — don't write it.

**Pass 2 — Flow.**
- A roadmap opens multi-issue discussions; mini-roadmaps open multi-part arguments.
- Headings state points, not topics ("The notice was untimely" beats "Notice").
- Every paragraph opens with a topic sentence making one point; everything in the paragraph serves it.
- Transitions carry the logic between arguments — the reader should never wonder why a paragraph follows the last one.

**Pass 3 — Sentences.**
- One idea per sentence; split any sentence juggling more.
- Subject and verb close together; the actor of the sentence is its grammatical subject.
- Passive voice only where the actor is unknown or genuinely irrelevant.
- Un-nominalize: "decide," not "make a determination."
- One term per concept, everywhere — elegant variation is a defect in legal writing, because a new word implies a new referent. If the draft says "the Agreement," it never says "the contract."

**Pass 4 — Mechanics.**
- Proofread (spelling, grammar, dates, names, numbers — numbers against their provenance per house rule 6).
- Every citation present, formatted, and pincited; every quote verbatim against its source if the source is available, flagged `[quote unverified]` if not.
- Defined terms used as defined; cross-references resolve.

## Output

The edited draft, plus a change report in two lists: **edits made** (style — brief, grouped by pass) and **flags for the author** (substance — each with location and what's missing or wrong). A clean draft with an honest flag list beats a silently "fixed" one.

## Validation loop

Before delivering: confirm all four passes ran (the report shows findings-or-clean per pass); confirm no flag was resolved by editing; diff-check that no citation or fact was introduced.

## Bundled resources

- `assets/editing-checklist.md` — the four passes as a run-through checklist.
- `references/legal-house-rules.md` — the standards the edit enforces.

Related skills: terminal gate for `legal-research-memo`, `client-advice-letter`, `commercial-contract-review`, and `contract-dispute-analysis` outputs. `professional-proofreader` (general bucket) handles non-legal documents; this skill exists because legal drafts need the architecture passes it lacks.

## What would make this skill wrong

If authors routinely accept every substance flag without disagreement, the flag/fix boundary may be too conservative for this user — revisit whether obvious substance fixes should be offered as proposed diffs. If Pass 3 edits keep getting reverted, the style rules are fighting the author's voice — relax toward flagging. If a draft type keeps needing a check this list lacks, add the check; an editing checklist that never grows isn't being used honestly.
