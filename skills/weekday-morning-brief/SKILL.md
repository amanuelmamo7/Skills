---
name: weekday-morning-brief
description: Weekday 8am morning brief: calendar, important emails, US/UK/Japan markets, news headlines, action items (routine from schedule.json), and a system-health rollup (Sefer logs, brief freshness, delivery queue).
---

Generate Amanuel's morning brief for today. Use bash `date` if you need to confirm the current date.

Structure the brief in SIX short sections, in this order:

**1. Today's calendar** — List meetings/events for today in chronological order. For each: time (with timezone if it varies), title, attendees if small (<6), and location/video link if present. Flag any back-to-back blocks or conflicts. If the day is light, say so plainly.
- Use Google Calendar (`mcp__37f0f02d-3f31-4fcf-a33f-f7a71ce519c2__list_events` on the primary calendar, time range = start to end of today in local time).
- If no calendar connector is available, write "No calendar connector connected" and continue.

**2. Important unread emails** — Surface unread threads from the last ~24 hours that look like they need attention: direct messages to Amanuel, threads where he's been @-mentioned or asked a question, anything from recurring senders he replies to, and anything time-sensitive (today's meeting changes, deadlines, approvals requested).
- FIRST read the VIP list at `/Users/amanuelmamo/Documents/Claude/Projects/Computer efficiency/Daily Brief/vip-senders.md` (bash cat on the mounted folder path, or Desktop Commander read_file). It has manual sections AND an auto-generated block (from his Sent folder) — treat all of them as VIPs. Any unread thread from a VIP sender/domain is surfaced FIRST and overrides the category/label exclusions below.
- Use Gmail (`mcp__1e1bdb1c-a80f-4946-8365-97b8fde459f8__search_threads`) with query: `is:unread newer_than:1d -in:draft -category:promotions -category:social`
- IMPORTANT: Do NOT add `-category:updates` — the Updates tab contains his good newsletters (Market Briefs, DealBook, AP MorningWire, Above the Law). Those are handled separately in section 4.
- For each surfaced email: sender, subject, one-line summary of what they want, and why it matters. Cap at ~5 unless there are clearly more needing attention.
- DRAFT REPLIES: for up to 3 surfaced emails that ask Amanuel a question or clearly need a response, check `list_drafts` for an existing draft on that thread; if none, create a reply draft with `create_draft` — 2–5 sentences, plain and direct in Amanuel's voice, no filler, sign off "Amanuel". NEVER send; drafts only. Mark those items "📝 draft ready" in the brief. Skip drafting for pure-FYI emails, newsletters, and automated senders.
- DEADLINE CAPTURE: if a surfaced email states an explicit deadline or dated obligation within the next 60 days ("respond by July 15", "payment due Aug 1", hearing/filing dates, RSVP-by dates), create an ALL-DAY calendar event on that date via `create_event`: title `DEADLINE: <short description>`, description = sender + subject + email link. Before creating, `list_events` for that date and skip if an event with the same title already exists. Cap at 3 new deadline events per run; note each as "📅 calendarized" in the brief. Only capture explicit dates — never infer or guess a deadline.
- EXCLUDE: package tracking (USPSInformeddelivery, packageconcierge, amazon shipment/auto-confirm), Google security alerts (no-reply@accounts.google.com), Coursera badge/completion (no-reply@t.mail.coursera.org), LinkedIn job/message notifications (jobs-noreply@linkedin.com, messages-noreply@linkedin.com), scholarship/CC offer spam (fastweb.com, bankofamerica@emcom, no-reply@business.amazon.com), YouTube/Crunchyroll notifications, and Seattle-specific sources (googlealerts-noreply@google.com which is set to Seattle, newsletter@em.king5.com which is Seattle local TV) — these are noise, not action items.
- Also exclude any thread already labeled `Newsletters`, `Promotions`, `Jobs`, `Shipping & Mail`, `Account & Security`, or `Potential Scam` (unless the sender is a VIP).
- EXCLUDE job postings that ask for 3+ years of experience (or any seniority requirement above entry-level — e.g. "senior", "mid-level", "X+ years required", "Associate" attorney roles which conventionally require 3+ YOE). This applies to individual job-match emails (Indeed, GoInhouse, etc.) as well as digests — if a digest's surfaced roles all require 3+ YOE, drop the whole email. Only surface entry-level / 0–2 YOE roles. When experience requirement isn't visible in the snippet, use `get_thread` (FULL_CONTENT) to check the body before surfacing.

**3. Markets snapshot** — Pull recent issues of Amanuel's finance newsletters and summarize. Query: `(from:hello@market.briefs.co OR from:nytdirect@nytimes.com OR from:morningwire@apnews.com) newer_than:2d`. For each issue, read the subject + snippet. Produce three concrete one-liners:
  - 🇺🇸 **US** — what's moving in Dow / S&P / Nasdaq / Fed / Treasuries
  - 🇬🇧 **UK & Europe** — FTSE / ECB / BoE / pound / euro
  - 🇯🇵 **Japan & Asia** — Nikkei / yen / BoJ / China / Hang Seng
  Name a specific company, index, or theme that's actually in the newsletter. If a region isn't covered today, say "Not in today's newsletters." Do NOT invent market data.
- FALLBACK: if no newsletter issue is less than 36 hours old (holiday weeks, delivery gaps), do ONE web search for "stock market today <region>" per uncovered region and clearly tag those lines `[web]` instead of leaving the section stale. Never mix invented numbers — only report what a source states.

**4. News headlines** — Pull last 48 hours of subject lines from: `(from:editor@levernews.com OR from:newsletters@abovethelaw.com OR from:morningwire@apnews.com OR from:breakingnews@nytimes.com) newer_than:2d`. List up to 5 headlines, each with source tag (e.g., `[Lever News]`, `[AP]`, `[Above the Law]`, `[NYT]`). Just headlines — no summaries. DO NOT include Seattle-specific Google Alerts or King5 (they're stale; he's in Dallas now). If nothing recent, skip the section.

**5. Needs attention today** — Synthesize across calendar + important emails: things Amanuel should actually do today. Prep needed before a meeting, replies owed before end of day, deadlines hitting today (including any `DEADLINE:` events on today's calendar), decisions pending. Pull from the data already gathered; do not invent items.
- His daily routine lives in `/Users/amanuelmamo/Documents/Claude/Projects/Computer efficiency/Daily Brief/schedule.json` — read it (bash `cat` on the mounted path, or Desktop Commander `read_file`) and use it as the single source of truth for his timeline. Respect the `condition` field (e.g. poker only on even-dated days). Flag if a calendar event conflicts with a routine block. If the file is unreadable, fall back to: 9am brief reading, 9:30 job hunt, 10:30 Coursera, 11:30 StreamSmart, 12:30 lunch, 1pm poker on even-dated days, 2pm gaming, 4pm Coursera, 6pm StreamSmart.
- If nothing clearly needs attention, say "Nothing flagged — looks like a clear day."

**6. System health** — One line per system, checked via Desktop Commander (or bash on the Mac paths if available). Keep it to 3–5 lines total:
- **Sefer (finance briefs):** read the newest 1–2 files matching `/Users/amanuelmamo/.openclaw/workspace-sefer/logs/cron-*.log` (Desktop Commander `list_directory` + `read_file`, tail ~15 lines). Report the last run's outcome. If a log contains `ERROR` or `FATAL`, also grep the last `error="` line from `/private/tmp/openclaw/openclaw-<today>.log` and report the reason in plain words (e.g. "401 auth — re-run `claude` login and restart gateway").
- **Brief freshness:** check the newest file dates in `/Users/amanuelmamo/.openclaw/workspace-sefer/memory/`. If the newest pre-market or post-market brief is older than 2 trading days, flag it prominently at the TOP of the whole brief, not just here.
- **Meeting reminders:** confirm `com.bari.meeting-reminder` appears in `launchctl list | grep meeting-reminder` (Desktop Commander start_process). If missing, flag: "reload with launchctl bootstrap gui/501 ~/Library/LaunchAgents/com.bari.meeting-reminder.plist".
- **Delivery queue:** count files in `/Users/amanuelmamo/.openclaw/delivery-queue/failed/` — if the count grew since yesterday (note the newest file date), flag it.
- If Desktop Commander is unavailable this run, write "Health check skipped — Desktop Commander not available" and move on. Do NOT report on MCP connectors that need authorization; that is noise.

**Formatting rules:**
- Lead with a one-line greeting and the day/date (e.g. "Good morning, Amanuel — Tuesday, May 19").
- Use compact bullet points within each section, not prose paragraphs.
- Bold the section headers exactly as above.
- Keep the whole brief skimmable — target under ~550 words total.
- Cite linkable items (calendar events, email threads) with markdown links where the connector provides URLs.
- If a connector call fails with an auth error, note the failure in the relevant section and move on — don't abort the whole brief.

Deliver the brief directly in chat. Do not create files.
