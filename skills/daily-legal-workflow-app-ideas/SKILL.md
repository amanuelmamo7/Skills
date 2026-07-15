---
name: daily-legal-workflow-app-ideas
description: Daily legal-tech research + brainstorm: scan AI-for-lawyers articles, LinkedIn, and GitHub, then generate app ideas for in-house counsel teams and law firm practice groups
---

This task has two phases each morning: (1) research the current legal-AI landscape, then (2) use what you found to generate fresh application ideas. Deliver everything in the Cowork chat.

=== PHASE 0: LOAD RUN MEMORY ===
Read `/Users/amanuelmamo/Documents/Claude/Scheduled/daily-legal-workflow-app-ideas/ideas-log.md` if it exists (Desktop Commander read_file, or bash). It lists idea names already generated on previous runs. Your unique ideas today must NOT repeat or lightly rebrand anything on that list.

=== PHASE 1: RESEARCH ===
Scan for what's new and notable in AI use by lawyers. Use web search and web fetch. RECENCY RULE: restrict searches to the last 7–14 days where the search tool supports it, and prefer sources with an explicit publication date; state the date next to each cited item. Cover these sources:

1. Articles / news — search for recent (last 1-2 weeks) articles on AI use by lawyers and in legal practice. Good sources: Artificial Lawyer, Above the Law, Legaltech News / Law.com, ABA Journal, Reuters Legal, Bloomberg Law. Note concrete developments: new tools, adoption trends, ethics/regulatory updates, notable firm or in-house deployments.

2. LinkedIn — search for recent LinkedIn posts/discussions from legal-tech voices and practitioners about AI in legal work (e.g., search "legal AI" / "AI lawyers" LinkedIn, and well-known commentators). If specific posts aren't directly fetchable, summarize the themes and sentiment you can find via search results, and note this is search-derived rather than full post text.

3. GitHub — search GitHub for popular/trending legal-AI applications and repos (e.g., search terms like "legal AI", "contract analysis", "legal LLM", "law"). Identify a few notable repos by stars/activity, what they do, and recent momentum. Skip repos already discussed in the last 7 runs per ideas-log.md unless something material changed.

Capture sources with dates and URLs as you go. If a particular source can't be fetched, note it and move on — don't get blocked. Do NOT report on MCP connectors needing authorization — that's noise; just use web search.

=== PHASE 2: IDEAS (informed by Phase 1) ===
Using the research above as grounding and inspiration, generate application ideas to improve legal workflows for two distinct audiences:

(i) In-house counsel teams — e.g., contract lifecycle management, legal intake/triage, matter management, compliance tracking, outside-counsel/vendor management, knowledge management, board/governance support.

(ii) Practice groups at a law firm (litigation, M&A, IP, real estate, etc.) — e.g., document drafting/review, e-discovery, time/billing, client collaboration, precedent/brief banks, deadline/docket management, intra-group knowledge sharing.

Ideas can take any of these forms, and a good mix is welcome:
- Echoing an existing application or category that's working well (it's fine to name an established tool/approach), then
- Offering a refined branch-off or new angle on it, or
- Discussing what NOT to do — pitfalls, failed patterns, or over-hyped approaches to avoid and why.

HARD REQUIREMENT: every run must include at least THREE genuinely unique/creative application ideas that are not just rehashes of existing tools — net-new concepts or non-obvious combinations — AND not on the ideas-log.md list.

SOURCING REQUIREMENT: for each application idea (or at minimum each of the three unique ones), point to a source — from Phase 1 or a fresh search — that backs an argument in favor of that application's value-add (e.g., an adoption stat, a pain-point study, a market trend, a practitioner quote, or a comparable tool's traction). Include the source link inline.

For each idea include: a short name; the specific pain point/workflow it targets; how it would work (key features); who would use it; the supporting source and the value-add argument it backs; and, where relevant, how it connects to a Phase 1 trend or tool. Favor practical, buildable ideas that meaningfully leverage AI/LLMs. Push for day-to-day novelty.

=== PHASE 3: SAVE RUN MEMORY ===
Append one line to `/Users/amanuelmamo/Documents/Claude/Scheduled/daily-legal-workflow-app-ideas/ideas-log.md` (create it if missing) in the format: `YYYY-MM-DD: <idea name 1>; <idea name 2>; ... | repos: <repo names discussed>`. Use Desktop Commander write/edit or bash append. Keep the log append-only.

=== OUTPUT FORMAT (in Cowork chat) ===
Structure the response in two clearly headed sections:
- "What's happening in legal AI" — a concise, skimmable research digest (bulleted themes from articles, LinkedIn, and GitHub), with linked sources and dates.
- "App ideas" — split by the two audiences. Clearly flag which ideas are the unique/creative ones (at least three). Mark any "what not to do" notes. End with a single "Wildcard" idea that's more ambitious or unconventional.

Keep it concise and skimmable — a sharp morning briefing, not an exhaustive report. Always include source links for both the research digest and the value-add arguments.
