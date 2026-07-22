---
name: authority-synthesis
description: Turn a pile of cases into a usable rule — chart authorities per element (facts that mattered, holding, reasoning, comparison to the client's case), synthesize implicit rules from consistent outcomes, reconcile seemingly inconsistent decisions, and write tight case illustrations that prove the rule. Use when multiple opinions bear on one question, when the user asks "what's the rule from these cases," wants cases charted or compared, needs a synthesized rule stated, or when legal-research-memo's discussion section needs its authority layer built. Differentiator: the method between "found the cases" and "stated the rule" — research skills find authority; this skill makes it speak with one voice.
---

# Authority Synthesis

Courts rarely hand you the rule in one sentence. The rule usually lives across several opinions — sometimes stated, often implied by what courts consistently do. This skill is the disciplined path from a set of cases to a rule you can apply: chart, synthesize, illustrate.

> Born from: the observable gap in AI legal output between citing cases and actually deriving a rule from them — synthesis is where thin research becomes analysis. Method is standard legal-writing doctrine, expressed originally. Built with `skill-distiller`.

## Boundary card

**Hard lines** — this skill never:
- Charts a case it hasn't read this session. A chart row is a Tier 1 artifact by definition (`references/legal-house-rules.md`, rule 2) — headnote-only or memory-recalled cases don't get rows; they get a `[not yet read]` parking list.
- Passes a synthesized rule off as a quoted one. Explicit rules are quoted with pincites; synthesized rules are stated in the skill's own words and labeled `[synthesized from: <case list>]` — the reader must be able to tell which they're getting, because a synthesized rule is a claim about the cases, checkable only if labeled.
- Smooths over genuine conflict. If the cases actually disagree, the output is a split (with which line is better supported and why), not a fake harmony.

**Judgment vs. determinism:** what the operative variable is across cases, and whether consistency is real, are judgment. The chart columns, the illustration parts, and the labeling rules are fixed.

## Workflow

1. **Scope the set.** Governing jurisdiction's binding authority first; persuasive authority only where binding law runs out (and marked as persuasive). Note the question each case is in the set to answer — a case can be authority for one element and noise for another.
2. **Chart every case read**, using `assets/case-chart-template.md`. Per case: citation + court + year, posture, the facts that mattered to the outcome (not all facts — the ones the reasoning turned on), holding on the relevant question, the reasoning's operative logic, and the comparison to the client's facts (similar / distinguishable / neutral, with the specific fact that makes it so). For element-level work, chart per element, not per case.
3. **Extract the rule.**
   - **Explicit** — a court stated it: quote it, pincite it, check the later cases still follow it.
   - **Implicit** — no one stated it, but outcomes are consistent: identify the variable that separates the outcomes (what was present in the granted cases and absent in the denied ones?), state the resulting rule expressly in your own words, and label it `[synthesized]` with the supporting case list. Stating a synthesized rule plainly feels bold and is correct — an unstated pattern isn't usable; a stated one is checkable.
   - **Seemingly inconsistent** — before declaring conflict, test whether a distinguishing variable reconciles the cases (different postures, different element in play, different facts on the operative variable). If reconciliation works, the reconciling variable *is* the rule. If not, report the split honestly.
4. **Write case illustrations** for the load-bearing cases only — the ones that prove or clarify a rule the reader might doubt. Four parts, in order: the legal proposition the case stands for (one sentence), the facts the outcome turned on, the holding, the reasoning — and nothing else. An illustration with facts the later comparison never uses is carrying dead weight; cut to what the analogy will need.
5. **Deliver** the synthesis block: rule statements (each quoted-or-labeled), the chart, illustrations ordered by legal principle (not chronology), and the parking list of authorities not yet read.

## Validation loop

Before delivering: every chart row traces to a case read this session with a pincite; every rule statement is either quoted or `[synthesized]`-labeled with its case list; every illustration's facts reappear in some comparison downstream or get cut; genuine splits are reported as splits.

## Bundled resources

- `assets/case-chart-template.md` — chart, synthesized-rule block, and illustration block formats.
- `references/legal-house-rules.md` — the eight rules; the tier system governs every row.

Related skills: feeds `legal-research-memo` (this builds the discussion section's authority layer) and `contract-dispute-analysis` (contested-node rules). Use `legal-writing-editor` on the prose output.

## What would make this skill wrong

If a citator integration lands, step 3's "check the later cases still follow it" should defer to it. If charts are consistently built from more cases than the analysis uses, the scoping step is too loose — charting is expensive attention; spend it on cases that can change the answer. If a synthesized rule is ever contradicted by a case already in the chart, the consistency test in step 3 was skipped, not wrong — tighten the loop.
