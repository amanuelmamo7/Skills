---
name: contract-anatomy
description: >-
  Repository of commercial-contract heading structures (19 contract types, ~300
  headings from real SEC/Justia exhibits) plus an interactive explorer/quiz game.
  Use this skill whenever the user asks about contract structure or anatomy —
  what sections a contract type contains, how two contract types differ or
  overlap, which clauses are boilerplate vs. signature, classifying an unknown
  agreement from its headings or table of contents, adding a new contract type
  to the repository, or updating/regenerating the contract game. Trigger even if
  the user just pastes a contract TOC and asks "what kind of agreement is this,"
  mentions "the contract game," "contract taxonomy," "heading repository," or
  wants a new agreement type "added" from a URL (SEC EDGAR, Justia, LawInsider).
---

# Contract Anatomy

A structural taxonomy of commercial contracts and a game built on it. The core
idea: every commercial contract shares a boilerplate spine (definitions →
risk-allocation stack → miscellaneous), and each type's identity lives in a
handful of signature clauses. Making that visible is the fastest way to teach
contract-type recognition.

## Bundled resources

- `references/contracts_taxonomy.json` — the repository. Per contract type:
  ordered headings with subheadings, a canonical concept key (`c`) shared
  across types so overlap is computable, and a tag: `u` (universal
  boilerplate), `s` (family-shared), `x` (signature/fingerprint). Sources
  cited per type.
- `assets/contract_anatomy.html` — single-file explorer + game (Explore,
  Compare, DNA similarity matrix, guess-the-contract quiz with behavioral
  engagement mechanics). Data is embedded; regenerate after taxonomy edits.
- `scripts/sync_data.py` — injects the taxonomy JSON into the HTML, updates
  header counts, and runs integrity checks. Run after any taxonomy change.

## Task: classify an unknown contract from its headings

Read `references/contracts_taxonomy.json`. Match the unknown TOC against each
type's signature (`x`) headings first — boilerplate matches carry almost no
signal since it appears everywhere. Report the best match, the tell headings
that drove it, and the runner-up. If nothing fits well, say so; the repository
covers 19 types, not all of law.

## Task: compare contract types / explain differences

Use the concept keys: headings sharing a `c` value are structurally the same
clause wearing different names. Jaccard similarity over concept sets is the
repository's similarity measure (the game's DNA matrix computes it live).
When explaining, lead with the signature clauses that separate the types, not
the shared boilerplate.

## Task: add a new contract type from a real agreement

This is the maintained method — follow it so new entries stay consistent:

1. **Source a real exemplar** — SEC EDGAR exhibits, Justia contracts, or
   LawInsider. Prefer filed agreements over templates. Fetch the page; large
   fetches get saved to a file — grep it rather than reading it whole. TOC
   extraction patterns that work: `\*\*[^*]{3,80}\*\*` (bold headings),
   `\| \*\*\d+\.?\*\* \| [^|]{3,80}` (TOC table rows),
   `ARTICLE [IVX]+[^\n]{0,80}`, `Section \d+\.\d+[^\n]{0,60}`.
2. **Decide: new type or update?** If the agreement's skeleton matches an
   existing type, merge missed headings into that entry instead of creating a
   near-duplicate. Create a new type only when the fingerprint is genuinely
   distinct (e.g., a share purchase agreement is not a goods purchase
   agreement).
3. **Write the entry** — keep the document's real heading order. Reuse
   existing concept keys wherever the clause is the same idea (check the JSON
   first); invent new keys only for genuinely new concepts. Tag honestly:
   `x` only for clauses that would identify the type on their own. Every type
   needs at least 2 `u` and 1 `x` headings or the quiz can't build clue
   ladders. Cite the source URL.
4. **Sync and verify** — run `python3 scripts/sync_data.py` from the skill
   root (or wherever the JSON and HTML live; the script takes paths as
   arguments). It validates the JSON, re-embeds it in the HTML, updates the
   "N contract types, M headings" header, and fails loudly on clue shortages.
5. **Sanity-check similarity** — the script prints each new type's nearest
   neighbors. A share purchase agreement landing closest to a merger
   agreement is right; landing closest to a lease means the concept keys are
   wrong.

## Task: update or restyle the game

The HTML is self-contained (no build step, no network). Game code sits after
the embedded `const DATA`. The engagement layer is deliberate and
evidence-based — career ladder and progress bars (goal-gradient), per-case
"tell" feedback (competence feedback), player-paced reveals and mode choice
(autonomy), uncracked-type chips (open loops), Daily Docket (fresh-start
effect), endscreen replaying the best call (peak–end rule), occasional
double-point rounds (variable stakes), lapse-friendly streak framing. Keep
those mechanisms intact when editing; they're documented in the in-game
"behavioral design notes" panel. Persistence uses localStorage with an
in-memory fallback — don't remove the fallback.

## Grading honesty

The taxonomy is a teaching model, not legal advice. Real agreements deviate:
covenant-lite loans drop the financial-covenants article, UK locked-box SPAs
drop indemnification, SOWs inherit almost everything from their MSA. When a
user's real contract deviates from the taxonomy, that's usually the
interesting finding — surface it rather than forcing the match.
