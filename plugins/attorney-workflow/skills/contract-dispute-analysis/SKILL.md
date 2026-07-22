---
name: contract-dispute-analysis
description: Analyze a contract dispute end-to-end through the sequential enforceability framework — what law governs (UCC Article 2 vs. common law, predominant-purpose for mixed transactions), whether a contract was formed, defenses, what the terms actually are (parol evidence, implied and gap-filler terms, conditions), breach, excuses, remedies, and alternative theories like promissory estoppel. Use when a dispute exists or is brewing over whether a contract exists, what it requires, or who breached — "do we have a contract," "are we bound," "did they breach," "what are we owed." Differentiator: post-signature dispute posture — for pre-signature review of draft terms, use commercial-contract-review instead.
---

# Contract Dispute Analysis

Contract disputes decompose into a fixed sequence of questions, each gating the next: no point analyzing breach before formation, or remedies before terms. This skill walks that sequence with element-level rigor applied only where the fight actually is.

> Born from: an element-by-element CIRAC analysis framework for UCC/common-law contract disputes, whose sequential structure this skill abstracts. Built with `skill-distiller`.

## Boundary card

**Hard lines** — this skill never:
- Concludes the client should sue, settle, or repudiate — output is dispute analysis for counsel, work-product labeled (rule 8, `references/legal-house-rules.md`).
- Treats the framework's rule statements as authority. Doctrinal rules and section cites (§2-102, §2-201, §1-303...) are scaffold; anything load-bearing to the conclusion gets verified at runtime and tier-labeled per rule 2. This skill is US-law scoped (UCC Article 2 / common law) — flag immediately if the dispute points elsewhere.
- Grinds every element at every node. Full element-by-element analysis is for **contested nodes only** — the exam-style discipline of proving all seven elements of offer for every communication is correct training and wrong practice. Uncontested nodes get one line and a cite.

**Judgment vs. determinism:** which nodes are contested, how facts map to elements, and calibration are judgment. The sequence itself, the CIRAC structure at contested nodes, and the evidence-anchoring formula are fixed.

## The sequence

Walk the stages in order; each stage's answer gates the next (stage 0 can run in parallel with 1 — forum and merits are separable questions). At every stage, state the conclusion first (CIRAC), and mark the stage **contested** or **uncontested** before deciding how deep to go.

0. **Forum and arbitrability.** Before what's decided: who decides. If an arbitration clause exists (or a statutory scheme channels the dispute), gate on: is this dispute within the clause's scope, is it carved out by statute or the agreement itself, and who rules on arbitrability. The pivotal technique: **characterization drives arbitrability** — the same facts framed as one claim type may be arbitrable and framed as another may be excluded, so state both characterizations and which the record better supports. Where authorities pull opposite directions, reconcile them by their operative variable (`authority-synthesis`). If the forum is uncontested, one line and move on.
1. **What law governs.** UCC Article 2 ("transactions in goods") vs. common law by default. Mixed goods/services → predominant-purpose analysis (contract language, nature of the supplier's business, relative value of goods vs. services; gravamen of the dispute as tiebreaker). Governing law changes the answers downstream — never skip this stage even when it seems obvious; say why it's uncontested.
2. **Was a contract formed.** Mutual assent (offer, acceptance — analyzed communication by communication when contested, under the objective theory) plus consideration (bargained-for legal detriment). Identify *which* communication was the offer and which the acceptance; when formation is contested, that identification is usually the whole fight.
3. **Defenses to enforcement.** Statute of frauds (with its exceptions — merchant confirmation, specially manufactured goods, admissions, part performance), capacity, duress, unconscionability, mistake — analyze the ones the facts raise, name the ones they don't.
4. **What are the terms.** Express terms via integration analysis: was there an integration → full or partial → what outside terms exist → oral/written, before/during/after formation → contradicting vs. adding vs. explaining → apply the governing parol evidence rule. Then implied terms (course of performance, course of dealing, usage of trade), statutory gap-fillers, court-supplied terms, and conditions — distinguishing express conditions (strict compliance) from constructive ones (substantial performance), and conditions from promises (breach liability attaches to promises, not failed conditions).
5. **Breach.** Which promised performance failed, measured against the terms established in stage 4 — material vs. minor at common law; the tender rules under Article 2.
6. **Excuses.** Impossibility/impracticability, frustration, waiver, failure of a condition precedent, the other side's prior material breach.
7. **Remedies.** Expectation as the default measure, with reliance, restitution, specific performance, and the Article 2 buyer/seller remedy structures as the facts warrant; note limitations (foreseeability, mitigation, certainty).
8. **Alternative theories.** If formation failed: promissory estoppel, quasi-contract/unjust enrichment, quantum meruit.

## Contested-node discipline

At each **contested** node: state the elements of the governing rule with a tier-labeled authority, then apply the evidence-anchoring formula from the house rules — each element is *present or absent on these facts because [fact], as evident by [record cite], demonstrating [inference]*. Every "because" must point at a real fact from the record; an element application without its evidencing fact is a conclusion wearing an analysis costume. At each **uncontested** node: one sentence, the rule cite, and why no one disputes it.

## Validation loop

Before delivering: every stage of the sequence is present (even if one line); every contested-node element application names its fact and record cite; every load-bearing rule statement carries a verification tier; the conclusion chain is gated correctly (nothing downstream of a failed gate except the stage-8 alternatives).

## Bundled resources

- `assets/dispute-analysis-template.md` — the staged worksheet with the contested-node block.
- `references/legal-house-rules.md` — the eight rules, including the evidence-anchoring application discipline.

Related skills: `commercial-contract-review` (pre-signature clause review — the other posture), `litigation-hold-and-triage` (when the dispute is heading to litigation, run both: this for the merits map, that for preservation and deadlines), `legal-research-memo` (when a stage turns on contested authority).

## What would make this skill wrong

If disputes are consistently non-US or non-goods (services, IP licenses, real estate), the stage-1 framework needs the corresponding regime rather than a UCC/common-law fork. If counsel repeatedly re-grinds nodes this skill marked uncontested, the contested-node triage is miscalibrated — loosen it. If the underlying doctrinal scaffold drifts from current law in a governing jurisdiction (e.g., a state's parol-evidence or SoF amendments), runtime verification should catch it — a scaffold rule surviving into a conclusion unverified means rule 2 failed.
