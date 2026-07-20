---
name: regulatory-change-analysis
description: Analyze a new or amended statute, regulation, or agency guidance for a specific organization — calibrated applicability determination, obligations table with effective dates and citations, gap analysis against current practice, and a ranked action list with owners and deadlines. Use when the user asks "does this new rule apply to us," "what do we need to do about <regulation>," needs a compliance gap assessment, or wants a regulatory development translated into concrete obligations. Differentiator: separates what the rule says (cited) from whether it applies (calibrated) from what to do (ranked) — the three questions generic summaries blur together.
---

# Regulatory Change Analysis

A regulatory development is three separate questions — what does it say, does it apply to us, and what do we do — and blurring them is how compliance work goes wrong. This skill keeps them separate and forces each to its own standard of proof.

> Born from: the daily legal-AI landscape research runs, where the recurring gap between "new rule announced" coverage and "here is what it obligates *this* organization to do by *when*" is the analysis nobody publishes. Built with `skill-distiller`.

## Boundary card

**Hard lines** — this skill never:
- Quotes an obligation without its citation and effective date (rule 6, `references/legal-house-rules.md` — a compliance deadline without provenance cannot be relied on or verified).
- Collapses applicability into a yes/no when it's genuinely conditional — the determination is calibrated (*clearly applies / likely applies / unsettled / clearly exempt*) with the conditions quoted (rule 4).
- Declares the organization compliant. It maps gaps; compliance sign-off is an attorney/compliance-officer judgment (rule 8).
- Analyzes from a summary alone when the primary text is retrievable. Secondary coverage is Tier 2 at best; the rule text is the rule.

**Judgment vs. determinism:** applicability reasoning and gap severity are judgment. The obligations-table structure, citation-per-row requirement, and the watch list (comment deadlines, effective dates, phase-ins) are fixed.

## Workflow

1. **Intake (state-check).** Confirm what changed (rule, amendment, guidance, enforcement action) and retrieve the primary text — verify the version and its status (proposed / final / effective / stayed). Confirm the organization profile: entity type, jurisdictions of operation, activities and thresholds that regulators key on (revenue, user counts, data volumes, sector). Missing profile facts that drive applicability → list as blocking open questions rather than assuming.
2. **State the prior.** What regime governed this area before, and what you'd expect the change to mean going in.
3. **What it says.** Summarize the operative provisions with pincites and effective/phase-in dates. Distinguish new obligations from restatements of existing law — the delta is the analysis.
4. **Does it apply.** Work the applicability conditions element by element against the organization profile, quoting each condition. Output the calibrated determination with the decisive conditions named — and for *unsettled*, what interpretation, guidance, or fact would resolve it.
5. **Gap analysis.** For each applicable obligation: current practice (from the user — never assumed), the gap, severity (exposure × probability of enforcement, per rule 5), and the remediation action with a candidate owner and deadline keyed to the effective date.
6. **Write it up** with `assets/reg-analysis-template.md`: executive summary → the change (cited) → applicability (calibrated) → obligations table → gap analysis → action list → watch list (comment periods, phase-in dates, expected guidance) → what would change the analysis → Sources & citations with tiers and as-of dates.

## Validation loop

Before delivering: every obligation row has a citation and an effective date; the applicability section quotes actual conditions rather than paraphrasing them; every gap row's "current practice" traces to something the user said, not an assumption; the watch list has dates, not vibes.

## Bundled resources

- `assets/reg-analysis-template.md` — the exact output structure.
- `references/legal-house-rules.md` — the eight rules; read before writing.

Related skills: `legal-research-memo` (when applicability turns on a contested interpretation), `commercial-contract-review` (when the change forces contract remediation — flowdown clauses, DPAs), `deferred-work-register` (for phase-in obligations deliberately scheduled later).

## What would make this skill wrong

If the organization adopts a GRC platform, the obligations and action tables should export to its schema rather than markdown. If the same regulatory regime is analyzed repeatedly, a regime-specific variant with a maintained obligations register beats re-deriving from scratch. If a "clearly applies" determination is later reversed by counsel more than once, the calibration bands need re-anchoring.
