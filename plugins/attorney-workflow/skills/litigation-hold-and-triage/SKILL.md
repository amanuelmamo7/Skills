---
name: litigation-hold-and-triage
description: Triage an incoming dispute (demand letter, complaint, credible threat) into a structured intake memo — claims, exposure range, critical deadlines, insurer-notice check — and draft the litigation-hold notice with custodian and source lists. Use when a demand letter or complaint arrives, the user says "we might get sued" or "should we put a hold in place," or preservation obligations need scoping. Differentiator: drafts and checklists only — the preservation-trigger call and every outbound notice remain with counsel, explicitly.
---

# Litigation Hold & Dispute Triage

When a dispute lands, two clocks start: the deadlines and the preservation duty. This skill structures the first response — the triage memo and the hold notice draft — without ever making the calls that belong to counsel.

> Born from: the observation that the highest-stakes early litigation failures are process failures (missed deadlines, late holds, spoliation) — exactly the class of problem checklists and deterministic structure prevent. Built with `skill-distiller`.

## Boundary card

**Hard lines** — this skill never:
- Concludes when the preservation duty attached — that is a legal judgment with spoliation consequences; the skill surfaces the trigger facts and drafts on the assumption counsel confirms (rule 8, `references/legal-house-rules.md`).
- Sends a hold notice, response, or acknowledgment to anyone. Drafts only; a named attorney issues them.
- Computes a limitations or response deadline as a conclusion. It flags candidate deadlines with the governing source quoted and marks each `[confirm with counsel — jurisdiction rules apply]` (deadline math varies by forum, service date, and tolling; a confident wrong date is worse than a flagged range).
- Assesses merits beyond a preliminary claims inventory — triage is exposure scoping, not case evaluation.

**Judgment vs. determinism:** claims characterization and exposure ranging are judgment. The triage checklist, hold-notice structure, custodian/source inventory, and acknowledgment tracking are fixed structure — this is a domain where variation is a bug.

## Workflow

1. **Intake the trigger.** What arrived (demand / complaint / threat / incident), when, how served, from whom. Quote the operative assertions with pincites to the document.
2. **Run the triage checklist** (`assets/dispute-triage-template.md`): claims inventory with elements sketched; parties and relationships; candidate deadlines (response due, service rules, limitations concerns — each quoted to source and flagged for counsel); insurance — does any policy plausibly cover, and is there a notice provision with its own clock (quote it); forum and governing law; immediate do-not-do list (no destruction, no unsupervised contact with adverse parties, route communications through counsel).
3. **Scope the hold.** Build the custodian list (who plausibly touched the matter — err broad, note the reasoning per name) and the source list (email, chat, shared drives, devices, SaaS systems, auto-deletion policies that need suspension — name the systems specifically).
4. **Draft the hold notice** (`assets/litigation-hold-notice-template.md`): plain-English scope, what to preserve, auto-deletion suspension instructions, no-selective-deletion warning, acknowledgment requirement, contact for questions. Written to be understood by non-lawyers.
5. **Deliver both drafts** with the escalation block on top: what counsel must decide (duty trigger, deadline confirmation, insurer notice) and by when.

## Validation loop

Before delivering: every deadline flagged `[confirm with counsel]`; every quoted assertion verified against the source document; custodian list cross-checked against every person named in the triage memo; auto-deletion systems section is specific, not generic.

## Bundled resources

- `assets/dispute-triage-template.md` — the intake memo structure.
- `assets/litigation-hold-notice-template.md` — the hold notice draft structure.
- `references/legal-house-rules.md` — the eight rules; read before writing.

Related skills: `legal-research-memo` (limitations or elements research), `commercial-contract-review` (when the dispute arises under a contract — pull the dispute-resolution and indemnity clauses first).

## What would make this skill wrong

If the organization adopts a legal-hold platform, the notice draft should target its format and the acknowledgment tracking should defer to it entirely. If counsel repeatedly overrides the custodian-list breadth in the same direction, recalibrate the default. If any draft is ever sent without attorney sign-off, the hard line failed structurally — add a distribution block that names the issuing attorney before any recipient list.
