---
name: commercial-contract-review
description: First-pass review of a commercial agreement (vendor, SaaS, NDA, services, license) against a playbook — producing a ranked issue table with clause quotes and pincites, position-vs-playbook comparison, fallback positions, and escalation flags, wrapped in an executive summary. Use when the user uploads or pastes a contract for review, asks "what's wrong with this agreement," wants redline priorities, or asks whether terms are market. Differentiator: materiality-ranked output with every finding quoted from the actual text — never a generic clause checklist.
---

# Commercial Contract Review

A structured first pass that a supervising attorney can trust and check: every issue anchored to quoted text, ranked by materiality, compared against a stated position, with the escalations flagged.

> Born from: transactional review practice — the recurring failure of AI contract review is unranked checklist output with paraphrased (sometimes invented) clause content. Built with `skill-distiller`.

## Boundary card

**Hard lines** — this skill never:
- States a finding without quoting the operative clause text with a section pincite (a paraphrase can't be checked; a quote can — this is the evidence-of-execution rule applied to contract text).
- Recommends signing, refusing, or terminating — output is analysis support for attorney decision, labeled work product (`references/legal-house-rules.md`, rule 8).
- Negotiates, marks up, or sends anything externally. It drafts positions; humans negotiate.
- Invents playbook positions. No playbook provided → apply stated market-norm defaults and label every such judgment `[default — no playbook]`.

**Judgment vs. determinism:** issue spotting, materiality ranking, and fallback framing are judgment. The issue-table structure, quote-and-pincite requirement, and escalation flag criteria are fixed.

## Workflow

1. **Intake (state-check).** Confirm: which side the user is on (paper matters — the same cap reads differently to vendor and customer), deal context (value, term, criticality), governing law, and whether a playbook exists. Missing side or context → ask; missing playbook → proceed with flagged defaults.
2. **Read the whole agreement before writing anything.** Note the defined terms that shift risk (Affiliates, Losses, Confidential Information) — clause-level review with wrong definitions produces confident nonsense.
3. **Sweep the risk-bearing clauses**, per the checklist in `assets/contract-review-template.md`: term/renewal/termination, fees and payment, indemnities, limitation of liability (cap, exclusions, carve-outs), IP ownership and license scope, confidentiality, data protection/security, warranties/disclaimers, insurance, assignment/change of control, dispute resolution and governing law, notice, and the definitions feeding each.
4. **Build the issue table.** For each finding: clause + pincite, quoted operative language, what the playbook (or flagged default) says, materiality rating (exposure × probability, per rule 5), proposed fallback position, and an escalation flag where the deviation exceeds stated authority or the exposure is uncapped.
5. **Write the executive summary last**: three to five sentences a business stakeholder can act on — the two or three issues that matter, the overall risk posture, what needs escalation.
6. **Close** with open questions (missing exhibits, facts only the business team knows), what would change the analysis, and the Sources footer (document version reviewed, playbook version applied).

## Validation loop

Before delivering: verify every quote appears verbatim in the source document; confirm every issue has a materiality rating and every `[default — no playbook]` label survived; check that the summary mentions nothing the table doesn't support.

## Bundled resources

- `assets/contract-review-template.md` — clause checklist + issue-table format.
- `references/legal-house-rules.md` — the eight rules; read before writing.

Related skills: `legal-research-memo` (when enforceability of a clause needs authority), `regulatory-change-analysis` (when a clause implicates a regulatory regime).

## What would make this skill wrong

If the user adopts a formal CLM playbook format, intake should parse it rather than ask. If reviews are consistently one clause type (e.g., all NDAs), a specialized variant will outperform this general sweep. If quoted text ever fails verbatim verification, the extraction step — not the analysis — is where to look.
