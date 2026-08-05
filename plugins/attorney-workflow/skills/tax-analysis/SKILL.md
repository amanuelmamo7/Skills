---
name: tax-analysis
description: Analyze US federal income tax questions through the four-stage individual framework — gross income and exclusions, deductions (business, capital recovery, mixed-purpose), timing and accounting methods, and attribution (who is the taxpayer) — plus a state-and-local overlay for nexus and constitutional constraints. Reads the actual Internal Revenue Code at runtime via a bundled section-to-page index, so every Code citation is quoted from the statute, never recalled. Use when the user asks any tax question — "is this income," "can I deduct this," "how is this gain taxed," "when is this recognized," "who pays tax on this," "can the state tax this" — or wants a tax memo, issue-spot, or Code section explained. Differentiator: Code-first with runtime verification; analysis support for a tax professional, never tax advice or return preparation.
---

# Tax Analysis

Tax questions decompose into a fixed sequence — is it income, is it deductible, when, and to whom — and almost every hard question is a fight about which stage it lives in. This skill walks that sequence with the Code itself open.

> Born from: a complete federal individual income tax course framework (outline, case briefs, and SALT constitutional materials) authored in study, plus the verification-tier discipline of the attorney-workflow family applied to the one domain where an invented citation is most tempting: statutory text everyone half-remembers. Built with `skill-distiller`.

## Boundary card

**Hard lines** — this skill never:
- Gives tax advice, prepares or reviews a return, or computes a specific liability for filing. Output is analysis support for review by a tax professional, work-product labeled (`references/legal-house-rules.md`, rule 8). Tax adds a reason the rule exists: penalty exposure turns on authority levels, and only a professional weighs that for a real taxpayer.
- Quotes the Code from memory. The bundled index (`assets/irc-page-index.tsv`) locates any section in the taxpayer's copy of the IRC PDF; the skill Reads the actual text and quotes with a pincite (Tier 1), or labels the proposition `[UNVERIFIED]`. Everyone "knows" what §162 says; the subsections are where answers live.
- States a dollar threshold, bracket, phase-out, or inflation-adjusted amount as current without a currency check. The bundled Code is a snapshot (Release Point 119-102, August 2026); inflation adjustments live in annual Revenue Procedures, not the Code text — flag every such number with its as-of source or mark it stale.
- Treats federal analysis as answering a state question. SALT is a separate overlay with its own constitutional gates (`references/salt-framework.md`); say which regime each conclusion belongs to.

**Judgment vs. determinism:** issue characterization, analogy to case law, and calibration are judgment. The four-stage sequence, the Code-reading protocol, and the currency flags are fixed.

## The Code-reading protocol (run before analysis)

1. Locate the taxpayer's IRC PDF. Default expectation: a local copy configured by the user (ask once and remember for the session if not found). No PDF available → proceed on the framework but mark every statutory proposition `[UNVERIFIED — Code not available this session]`.
2. For each section the analysis needs: look up its page in `assets/irc-page-index.tsv` (1,896 sections mapped, format: `section<TAB>pdf-page<TAB>title`), Read that page range of the PDF, and quote the operative language with section and subsection pincites.
3. Note the Release Point printed on the page — that is the snapshot's currency marker. Anything the question dates after it, verify externally.

## The sequence

**Stage 1 — Gross income.** Start from §61's sweep (accessions to wealth, clearly realized, complete dominion — the *Glenshaw Glass* gloss) and the economic-income frame (consumption + change in net worth; source irrelevant; imputed income the notable gap). Property dispositions run through §1001: amount realized minus adjusted basis (§1012 cost; §1016 adjustments), with debt in the amount realized whether recourse or not (*Crane*/*Tufts*), and discharge of indebtedness as income (*Kirby Lumber*) subject to the contested-liability limit (*Zarin*). Then the exclusions, each a statutory island with elements: gifts (§102 — donor's detached and disinterested generosity under *Duberstein*; carryover basis §1015; stepped-up basis at death §1014), life insurance (§101), fringe benefits (§132; §119 meals-and-lodging with its convenience-of-the-employer elements), prizes taxable (§74), qualified scholarships (§117), damages (§104 — physical injury excluded, punitive and standalone-emotional not; allocate mixed settlements by the nature of the claim, *Amos*), municipal bond interest (§103).

**Stage 2 — Deductions.** Business expenses under §162 require *ordinary and necessary in carrying on* a trade or business — ordinary meaning customary in the industry (*Welch v. Helvering*), with §262's personal-expense bar on the other side and origin-of-the-claim (*Gilmore*) deciding which side a litigation cost falls on. Then the capital/expense line: capitalize what creates a separate asset or a benefit beyond the year (*INDOPCO*), recover it through depreciation (§§167–168) or amortization (§197 intangibles, 15 years regardless of actual life), and watch §1245 recapture convert prior depreciation back to ordinary income on sale. Mixed personal/business territory runs on its own tests: travel away from home in pursuit of business (*Flowers*; the sleep-or-rest rule of *Correll*; one-year assignment limits), meals beyond personal baseline (*Moss*), education that maintains skills versus qualifies for a new trade (Reg. §1.162-5), home office (§280A), interest (§163), losses (§165), bad debts with the dominant-motivation test (§166, *Generes*), and the public-policy bar (§280E).

**Stage 3 — Timing.** Accounting method first (§446: cash vs. accrual), then the doctrines that override it: constructive receipt (unfettered control — *Hornung*), claim of right (income when received under a claim of right even if repayable — *North American Oil*; §1341's relief computation on restoration), and the tax benefit rule (recovery of a previously deducted amount is income — §111).

**Stage 4 — Who is the taxpayer.** Assignment-of-income: earnings taxed to the earner regardless of anticipatory assignment (*Lucas v. Earl* — who controls the tree), property income to the owner of the property unless the interest itself is fully assigned (*Blair* vs. *Horst*), contingent attorney's fees included in the client's recovery (*Banks*). Then family attribution: children's service income to the child (§73), spousal transfers and divorce basis (§1041 — carryover basis makes low-basis property a real negotiation item), joint-return liability and innocent-spouse relief (§6015).

**SALT overlay.** When the question is whether a *state* can tax: run `references/salt-framework.md` — Due Process minimum contacts and the Commerce Clause four-part test of *Complete Auto* (substantial nexus, fair apportionment, nondiscrimination, fair relation), with the nexus line's evolution from physical presence (*Bellas Hess*, *Quill*) to economic nexus (*Wayfair*) — and keep the state-law question expressly separate from the federal one.

## Analysis discipline

Every stage applies the house rules: elements anchored to facts (*because / as evident by / demonstrating*), calibration explicit, and the tax-specific authority hierarchy stated per conclusion — Code → Treasury Regulations → administrative guidance (Revenue Rulings, Revenue Procedures; PLRs bind no one but signal the Service's view) → case law. Say which rung each conclusion rests on; a position resting on a PLR is calibrated differently than one resting on the statute. Output uses `assets/tax-memo-template.md`; short questions get the QP + brief answer + key authority without the full memo body.

## Bundled resources

- `assets/irc-page-index.tsv` — 1,896 IRC sections mapped to pages of the August 2026 (Release Point 119-102) Code PDF.
- `assets/tax-memo-template.md` — tax memo structure with the authority-hierarchy footer.
- `references/federal-tax-framework.md` — the four-stage doctrine map with section and case anchors.
- `references/salt-framework.md` — state-tax constitutional gates and the nexus timeline.
- `references/legal-house-rules.md` — the eight rules; the tier system governs every Code quote.

Related skills: `legal-research-memo` (the general-purpose research engine when a tax question needs case law beyond the framework's anchors), `authority-synthesis` (reconciling tax cases), `regulatory-change-analysis` (new tax legislation or regulations against a taxpayer's facts), `client-advice-letter` (translating for the client — with the tax-professional review gate intact).

## What would make this skill wrong

The Code snapshot ages: after the next major tax act, the page index needs regeneration against a new PDF (the indexing script pattern is one regex over pdftotext output — rebuild rather than patch). If questions are consistently entity-tax (partnerships, subchapter C/S) rather than individual, the framework needs those modules — the current sequence is individual-tax scoped and says so. And if a quoted "current" threshold is ever shown stale in use, the currency-flag discipline failed structurally — tighten the Rev. Proc. check from flag to mandatory lookup.
