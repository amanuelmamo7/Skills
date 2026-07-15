---
name: vip-list-management
description: Maintain a VIP-senders list file that mixes manually curated entries with an auto-generated block, so announce policies and email triage can rank senders. Use when the user says "add X to VIPs" / "remove X", or when setting up sender-priority infrastructure for an assistant.
---

# VIP List Management

Maintain a single shared markdown file listing the senders who matter, consumed by announce policies, email triage, and briefing jobs. The file mixes hand-curated sections with a machine-regenerated block — the core discipline is never letting one clobber the other.

## File structure

One markdown file at a stable, shared path (e.g. a `vip-senders.md` inside the user's project or workspace directory — every consumer references the same path):

```markdown
# VIP Senders

## People (manual — voice-worthy)
jane@example.com — Jane Doe / direct manager
counsel@firm.example — outside counsel on active matter

## Domains / senders (manual — flag-only)
@importantclient.example — key client domain
billing@vendor.example — invoices need same-day review

<!-- AUTO-VIP START -->
frequent1@example.com — auto: 14 sent replies last 90d
frequent2@example.com — auto: 9 sent replies last 90d
<!-- AUTO-VIP END -->
```

Two manual tiers, deliberately distinct:

- **People (voice-worthy):** real humans whose time-sensitive email can justify the highest-interruption channel (voice announcement).
- **Domains / senders (flag-only):** worth flagging in chat/briefs but never worth a voice interrupt.

Entry format is one line each: `email-or-domain — name/why`. The "why" matters — a future session must understand the entry without asking.

## Handling user commands

**"Add X to VIPs":**
1. Decide tier: named human writing directly to the user → People section; a domain, role address, or "just flag these" → Domains/senders section. If ambiguous, ask which tier — the tiers drive different interruption levels.
2. Append one line in the entry format to the correct manual section.
3. Confirm in one line: "Added <email> to VIPs (<tier>)."

**"Remove X":**
1. Search the manual sections for the line; delete it.
2. If the entry only exists inside the auto block, tell the user it's auto-generated and will reappear on regeneration — offer to add an explicit exclusion convention instead (e.g. a `## Never-VIP` manual section your generator respects).

## The auto-generated block rule

**NEVER manually edit anything between `<!-- AUTO-VIP START -->` and `<!-- AUTO-VIP END -->`.** That block is regenerated on a schedule (e.g. weekly) by a job that mines the user's sent folder for frequently-replied-to correspondents. Manual edits there are silently destroyed on the next regeneration.

Corollaries:

- Manual additions always go outside the markers.
- The regeneration job must replace only the marked block, preserving everything else byte-for-byte.
- If the markers are missing or malformed, halt the regeneration and alert rather than rewriting the whole file.

## Consumers

Document (in the file header or the consuming policy files) who reads this list, so changes are made with eyes open. Typical consumers:

- **Announce policy:** voice-tier announcements require the sender to be in the People section (see a companion announce-policy skill if present).
- **Email triage / heartbeat checks:** flag messages from any listed sender or domain.
- **Daily briefs:** surface VIP threads above the fold.

## Hygiene

- Keep entries current: when the user's job or matters change, stale VIPs cause noisy voice interrupts — prune on request or during periodic memory maintenance.
- Never store anything but addresses/domains and a short reason. No message contents, no credentials.
- One file, one path. Duplicated VIP lists drift immediately.
