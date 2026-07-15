---
name: daily-job-search-crawl
description: Daily 8:30 AM CT job-search crawl: fetch saved searches, score postings, write to Pending Review, auto-promote high-fit.
---

You are running Amanuel's daily job-search crawl. Each run starts with no memory — follow these steps exactly.

**Time budget: 120 minutes** (read live value from Automation Config → "Time budget (minutes)").

**Geography:** Dallas, TX (DFW metro: Dallas, Fort Worth, Plano, Addison, Frisco, Irving, Arlington) OR Remote-US. Austin and Houston are OUT of scope.

**Scope:** firm-side transactional roles at boutique / mid-size firms (≤200 lawyers, DFW preferred) — corporate, finance, M&A, EC/VC associate. Legal-AI vendor SME / Legal Domain Expert / Legal Engineer (JD-track) roles when SWE is NOT required.

**Hard exclusion (NO SWE):** drop legal-tech / legal-AI roles requiring software engineering, MS/PhD in CS, X+ years coding, "engineer required" (SWE meaning), "developer role," ML engineering, full-stack, or DevOps. KEEP roles where technical fluency is optional/a plus/nice-to-have. Count drops as `filtered_swe`.

## 1. Bootstrap context

Read in order:
- /Users/amanuelmamo/Documents/Claude/Memory/CLAUDE.md
- /Users/amanuelmamo/Documents/iCloud Documents/Amanuels stuff/Job Postings/job tracking/Job_Search_Automation.xlsx (Automation Config, Saved Searches, Target Companies, Site Access, Credentials)
- /Users/amanuelmamo/Documents/iCloud Documents/Amanuels stuff/Job Postings/job tracking/Job_Tracker.xlsx sheet "Job Tracker" — dedup set.

Job_Tracker schema (no Status column): Date Added, Fit Score, Employer, Job Title, Location/Remote, Job Type, Pay Range, Date Posted, Application Deadline, Date Applied, Posting URL, Description, Qualifications, Notes, Fit Notes.

## 2. Crawl Saved Searches

For each row in Saved Searches:
1. Skip if Site in Excluded sites.
2. CADENCE CHECK: read the Cadence column.
   - `Daily` — crawl every run
   - `Weekly (Mon)` — crawl ONLY on Mondays
   - `Monthly` — crawl ONLY on the 1st
   - `Paused` — never crawl
   If Cadence doesn't match today, skip. Don't count as error.
3. Fetch search URL:
   - web_fetch for no-login sites
   - Chrome MCP for LinkedIn / Law.com / GoInHouse / NALP / PDC / ABA / GoBigLaw / Otta / WTTJ / **Google Jobs**
   - Law360: Google site:law360.com/jobs via WebSearch.
   - **Google Jobs (added 2026-06-30):** URLs hit Google's `&ibp=htl;jobs` widget. Use Chrome MCP to render. Widget shows ~10 listings per query with source labels (LinkedIn/Indeed/employer-direct/etc.). Extract: title, company, location, source/posted-time, per-listing apply URL. Many listings deep-link to LinkedIn/Indeed — let dedup handle overlap. VALUE = direct-from-employer posts that bypass aggregators.
4. Extract individual posting URLs.

## 2b. Crawl Target Companies

For each row where Priority ≠ "Paused":
1. Fetch Careers URL (Chrome MCP for SPAs).
2. Scan listings for titles matching "Target role types" in Automation Config.
3. SKIP non-matching titles (corp-securities, pure litigation, IP prosecution, paralegal, 5+yr stated minimums).
4. For each match, feed URL through Step 3.
5. Update row: Last Checked=today, Last Found=count.
6. If URL fails: leave Last Found blank, append failure to Notes with date, also write to Needs Manual Review with Failure Reason=`target_failed (<reason>)`.

Currently Paused (do not retry): Icertis, Ironclad, HubSpot, Evisort, Litera, Lexion.

## 3. For each posting URL

1. Skip if URL in dedup set.
2. Skip if Employer + Title + Location match existing Job_Tracker row.
3. Fetch posting page.

3a. EXPAND COLLAPSED SECTIONS (Chrome MCP only):
javascript_tool:
document.querySelectorAll('button[aria-expanded="false"], .show-more-less-text__button, .show-more-less-html__button, [data-testid="more-text-button"], .jobs-description__footer-button').forEach(b => { try { b.click(); } catch(e){} });
Wait 500ms. Extract BOTH get_page_text AND document.body.innerText. Concatenate.

For web_fetch: HTML body is full.

4. Extract per Field Mapping from FULL text.

4a. EXTRACTION SANITY GATE + MANUAL REVIEW ROUTING:
If Description <200 chars OR Qualifications empty AND source is Chrome MCP, treat as extraction failure. Write to Needs Manual Review with Failure Reason=`extraction_failed (<short reason>)`. Increment counter. Same routing for target-company failures.

5. Hard filters (drop if any fail):

EXPIRATION (filtered_expired), STALE (filtered_stale / filtered_no_date_stale_prone), EXCLUDED EMPLOYERS, NO-SWE (filtered_swe), COMP FLOOR (filtered_comp), LOCATIONS (filtered_loc: DFW or Remote-US), EXPERIENCE (filtered_exp: 3+ yr minimum).

EXCEPTION for boutique firm transactional: mid-level (3-5yr) routes to Needs Manual Review with Failure Reason=`manual_review (boutique mid-level 3-5yr)` rather than silent drop.

## 4. Score surviving postings

Read latest 10 Job_Tracker rows for voice. Fit Score 1–10 + Fit Notes. Honest about gaps.

For boutique firm-side: 7-8 if firm is non-AmLaw-100 and DFW-based with junior-friendly framing. Note firm size in Fit Notes.
For legal-AI vendor SME/Domain-Expert: 7-8 if JD required, SWE not required, remote-US/DFW.
For DFW major employers (AT&T, Toyota North America, T-Mobile, Texas Instruments, AECOM, Match Group): junior-friendly framing is the key signal.

## 5. Write to Pending Review

ALWAYS use append_row_with_inherited_style.

## 6. Auto-promote high-fit rows

For Fit Score ≥ floor (default 7), append to Job_Tracker via Field Mapping. Date Added=today.

## 6b. Follow-through check (Mondays only)

On Mondays, after the crawl: scan Job_Tracker for rows where Date Applied is set and falls 7–21 days ago, and Notes does NOT already contain a response/rejection/interview note or a `followup:` tag. For each (cap 8, most recent first), produce a follow-through list: Employer, Title, days since applied, Posting URL, and a one-line suggested action ("send a brief status-inquiry note to the recruiter", "connection-request the hiring partner on LinkedIn", or "archive — posting closed" if the URL is dead; check with a quick fetch). Include this list in the run output AND in the Gmail digest (section "Follow-ups due"). Then append `followup: surfaced YYYY-MM-DD` to each row's Notes (append, never overwrite) so next Monday doesn't re-surface it unless another 14 days pass. Do NOT send any outreach yourself — surface only.

## 7. Log the run

Append ONE Run Log row via append_row_with_inherited_style:
- Run Timestamp, Trigger
- Source: comma-list (include "Google Jobs x3" if all 3 ran)
- Jobs Seen, Jobs New, Promoted, Errors
- Duration (s): ACTUAL elapsed seconds
- Notes: expired=N stale=N no_date_dropped=N comp=N loc=N exp=N excl=N swe=N extraction_failed=N target_companies_checked=N target_failed=N. Note "Cadence-skipped: N weekly sources" on non-Monday runs. Note "Google Jobs yield=N" so we can track contribution. On Mondays add "followups_surfaced=N".

## 8. Notify

If "Notify on new ≥ floor"=Yes and any cleared floor, Gmail digest to amanuelmamo7@gmail.com with Employer/Title/Location/Comp/Fit Score/URL. Apply "Jobs" label (Label_7). If Needs Manual Review picked up new rows, list at bottom. On Mondays include the "Follow-ups due" section from step 6b even if no new roles cleared the floor.

## Hard rules

- Never edit Job_Tracker schema — only append.
- Never delete from Pending Review or Needs Manual Review.
- Never auto-promote below floor.
- Honor Cadence column.
- Don't retry Paused Target Companies.
- If a credentialed site fails, log and move on.
- Never fill forms, click apply, or submit on Amanuel's behalf.
- ALWAYS use append_row_with_inherited_style.
- Notes appends for follow-ups must preserve existing Notes content.

Reference: /Users/amanuelmamo/Documents/Claude/Projects/Jobs/scheduled_task_prompt.md (source of truth) and style_helpers.py.
