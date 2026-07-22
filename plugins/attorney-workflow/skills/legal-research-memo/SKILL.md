---
name: legal-research-memo
description: Research a legal question and produce a verification-disciplined memo — question presented, calibrated brief answer, tiered authorities with pincites, mandatory strongest-contrary-authority section, and open questions. Use when the user asks a legal question needing authority ("can we...", "is it enforceable...", "what does the statute require..."), asks for a research memo, or needs existing legal analysis cite-checked. Differentiator: every citation carries a verification tier and unread authorities are labeled UNVERIFIED — the structural defense against fabricated cites.
---

# Legal Research Memo

Answer a legal question the way it will be checked: authority first, calibration explicit, contrary authority faced head-on.

> Born from: the fabricated-citation failure mode of legal AI, plus the verification-tier and falsifier disciplines proven in the market-analysis skill family. Built with `skill-distiller`.

## Boundary card

**Hard lines** — this skill never:
- Cites an authority it has not read this session without labeling it `[UNVERIFIED]` (rule 2 — the tier system exists because confident memory is exactly how fabricated cites happen).
- Presents the answer as legal advice or a final opinion — the memo is a first-pass draft for attorney review, labeled as work product (rule 8).
- Answers without naming the jurisdiction. If the user didn't specify, ask — or answer for a stated default and flag that the answer may not travel.

**Judgment vs. determinism:** research strategy, synthesis, and calibration are judgment. Citation formatting, the tier labels, and the memo structure are fixed by the template — no variation.

## Workflow

1. **Frame the question.** Restate it as a Question Presented in under/does/when form — *Under [governing law], does/is/can [legal consequence] when [the determinative facts]?* — with the determinative facts stated concretely, not as legal conclusions that assume the answer. One QP per issue; if the question is really three questions, split it and say so. State the facts assumed and unknown per `references/legal-house-rules.md` rule 1.
2. **State the prior.** What you'd expect the answer to be and why — doctrine, analogous rules, market understanding. The reader should see whether research confirmed or surprised.
3. **Research primary authority first.** Statutes and regulations before cases, cases before commentary. For each authority actually retrieved and read: quote the operative language with a pincite, note the court/agency and date, and check currency (later amendments, negative treatment, pending appeals — flag anything you cannot confirm as current).
4. **Assign verification tiers as you go.** Tier 1 = read directly this session. Tier 2 = specific secondary source confirmed. Tier 3 = `[UNVERIFIED]` — recalled, not checked. The evidence of execution for any Tier 1 claim is the quote + pincite in the memo; if you can't produce the quote, the tier drops.
5. **Hunt the contrary authority.** Mandatory, in the three-part counter-analysis shape: (a) state the strongest opposing argument fairly, as its best advocate would; (b) explain why the better reading rejects it — or concede that it may prevail and recalibrate; (c) return to the conclusion, adjusted for what the counter-analysis taught. If genuinely no contrary authority exists after looking, say what searches came back empty — an absence you searched for is a finding; an absence you assumed is a gap.
5a. **For statutory questions**, work the interpretation ladder in order: intrinsic evidence first (text and plain meaning → the provision in the context of the whole statute → textual canons), then extrinsic (interpreting cases, agency interpretations, legislative history, substantive canons) — and say which rung the answer rests on, because an answer resting on legislative history is weaker than one resting on text and should be calibrated accordingly.
6. **Write the memo** using `assets/research-memo-template.md`: QP → brief answer (a direct answer, the because-clause carrying the chief reason, and the chief caveat — calibrated: "clearly established / better reading / unsettled / cannot answer without X") → facts assumed → discussion → counter-analysis → open questions → what would change the analysis → Sources & citations footer with tiers and as-of dates.

## Validation loop

Before delivering: re-scan the memo for any legal proposition lacking a tier-labeled citation; verify every quote against the source text retrieved; confirm the contrary-authority section exists and is non-trivial. A memo failing any check is not done.

## Bundled resources

- `assets/research-memo-template.md` — the exact memo structure.
- `references/legal-house-rules.md` — the eight rules; read before writing.

Related skills: `authority-synthesis` builds the discussion section's rule layer when multiple cases bear on the question; feeds `commercial-contract-review` (clause enforceability) and `regulatory-change-analysis` (applicability); `client-advice-letter` translates the finished memo for the client; run `legal-writing-editor` before delivery. Use `efficient-web-research` for the retrieval layer.

## What would make this skill wrong

If the research environment gains a native citator (Shepard's/KeyCite-equivalent) integration, step 3's manual currency check should defer to it. If users are consistently attorneys asking for internal notes rather than memos, the template weight may need a "short-form answer" mode. If a Tier 3 label ever survives to a delivered memo without an explicit user waiver, the validation loop has failed — tighten it.
