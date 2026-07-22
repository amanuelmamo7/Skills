---
name: client-advice-letter
description: Translate legal analysis into a client-facing advice letter or email — plain-English answer up front, facts-as-understood inviting correction, honest calibration that survives translation, options with practical tradeoffs, concrete next steps, and a confidentiality note. Use when the user asks to draft a letter or email to a client, explain an analysis to a business team or non-lawyer, or turn a memo into something the client can act on. Differentiator: everything else in the attorney-workflow family is internal work product — this is the outward-facing translation layer, drafted for attorney review and signature, never sent by the skill.
---

# Client Advice Letter

A memo convinces a lawyer; a client letter helps a person decide. Same analysis, different job: the letter must be understandable without legal training, honest about uncertainty without hiding behind it, and organized around what the client should *do*.

> Born from: the translation gap at the end of every analysis — internal work product that never becomes a decision-useful communication is analysis wasted. Structure is standard client-letter practice, expressed originally. Built with `skill-distiller`.

## Boundary card

**Hard lines** — this skill never:
- Sends anything. It drafts for a named attorney's review and signature — the letter is the attorney's advice, not the skill's (`references/legal-house-rules.md`, rule 8: the skill drafts; a human attorney sends). The draft header carries `DRAFT — FOR ATTORNEY REVIEW BEFORE SENDING`.
- Lets calibration die in translation. "Unsettled — reasonable arguments both ways" does not become "you should be fine." The plain-English version of a hedge is a plainer hedge, not confidence. Overpromising to a client is the failure mode this hard line exists for.
- States facts as true that came from the client. Facts are presented as *our understanding, please correct* — because the analysis rests on them, and the letter should say so.
- Buries the answer. The client's question and the short answer appear in the opening — a letter the client must read twice to find the point has failed.

**Judgment vs. determinism:** what the options are and how tradeoffs weigh is judgment. The letter structure, the calibration-preservation rule, and the review-before-send gate are fixed.

## Structure (from `assets/client-letter-template.md`)

1. **Opening** — the question the client asked, restated plainly, and the short answer with its honest qualifier. Two to four sentences.
2. **Facts as we understand them** — only the facts the analysis rests on, with an explicit invitation to correct anything wrong or incomplete, and a note that the answer could change if the facts do.
3. **The analysis, translated** — plain business English; no citations unless the client asked for them; every unavoidable term of art defined in the sentence that first uses it. Explain *why* the answer is what it is in terms of the client's situation, not doctrine for its own sake.
4. **Options** — each realistic path with its practical tradeoffs (cost, time, risk, relationship). No option without a tradeoff; a tradeoff-free option list is advocacy wearing an options costume.
5. **Next steps** — concrete: who does what by when, including what the client needs to send or decide, and what the attorney will do on receipt.
6. **Closing + confidentiality** — invitation to call with questions; a note that the letter is confidential legal communication and shouldn't be forwarded without talking to the attorney first (forwarding can waive privilege — say so in plain terms).

**Email variant:** same content discipline, tighter — short answer in the first lines, headers only if the email runs long, and the stop-and-think rule: nothing goes in the draft the attorney wouldn't want quoted back later.

## Validation loop

Before delivering the draft: no unexplained term of art survives; the facts section invites correction; every option has a tradeoff; the opening contains the answer; the calibration in the letter matches the calibration in the underlying analysis (compare them directly); the draft header and confidentiality note are present.

## Bundled resources

- `assets/client-letter-template.md` — letter and email skeletons.
- `references/legal-house-rules.md` — the eight rules; rule 8 and the confidentiality discipline govern this skill most directly.

Related skills: consumes `legal-research-memo`, `commercial-contract-review`, or `regulatory-change-analysis` output as the underlying analysis; run `legal-writing-editor` on the draft before it goes to the attorney.

## What would make this skill wrong

If clients are consistently sophisticated (in-house counsel writing to other lawyers), the no-citations default inverts. If the attorney keeps deleting the options section in favor of a single recommendation, this user's practice wants advice letters, not options letters — adjust the structure, keeping the calibration rule. If a draft is ever sent without attorney review, the gate failed structurally — move the review flag from the header into the delivery workflow itself.
