# Scribe handover - milestone 8 (~121K tokens)
# session: 20260612_some_grothendieck_db17dd_15179594
# cwd: C:\claude_base\.claude\worktrees\awesome-grothendieck-db17dd
# written: 2026-06-12 09:43:11 by claude-opus-4-8

# HANDOVER - Liz/Samuel German MSc Applications

## GOAL (in Max's words)
Two intertwined goals this session:
1. Original: "Go figure out Liz's Samuel's applications" - Liz (Samuel Myakishev-Rempel) got results back from German Master's programs: two rejections, one acceptance from K?ln that requires committing within a week. Preferred university is Hannover. The question: "What's the strategy? Should Liz accept K?ln and then withdraw or not?"
2. Current/active: After updating the tracker DB, Max's final instruction is to NOT add a new pointer block to global2.md. Instead: **"many sessions before you did the applications for Liz on this computer and they had the system. Locate all proper md instructions."** - i.e., the infrastructure/instructions for this work already exist somewhere in the markdown system; find the existing proper md instructions rather than inventing a new one.

## DECISIONS + WHY
- **Strategy = accept K?ln now, withdraw later if Hannover comes through.** In Germany this is normal and penalty-free. Accepting is not binding like US deposits; no shared blacklist between universities; students routinely hold multiple offers. The K?ln email itself is explicitly labeled "Non-binding admission" - replying yes costs nothing, holds the seat, no fee yet. The only money at risk is the ~300 EUR Semesterbeitrag paid much later at enrollment, mostly refundable if de-registered before the semester starts.
- **Timing makes it even safer than first thought:** Hannover decides by END OF JUNE (not July-August as originally guessed). Confirmed by Hannover admissions officer Veronika Bonsch (email May 30). So Hannover's answer arrives within ~2 weeks of the K?ln reply deadline, before any K?ln fee is ever due.
- **Reply must come FROM the address Samuel applied with = emm@transposon.org.** This mailbox was set up specifically for these German applications and forwards into max.rempel2@gmail.com (which is why the offer appears in Max's Gmail). The Freiburg email had no visible To: address because it was BCC'd to all admitted applicants - normal, not a red flag.
- **Sending mechanism switched to Gmail alias.** The local mxmail tool can only send FROM mass@tamza.com / tamza.com mailboxes - it does NOT have emm@'s SMTP password loaded at the time of the test. So Max set up "Send mail as emm@transposon.org" as an alias in his own Gmail (Settings ? Accounts and Import ? Send mail as). Max confirmed he sent the test from his Gmail successfully.
- **Robot/signature safety:** Max insisted on a test letter first to verify Claude wouldn't put a wrong signature or mention being a robot. The mxmail auto-signature block ("Claude Opus 4.8, AI assistant") was suppressed; the real acceptance signs plainly as "Samuel Myakishev-Rempel."

## CURRENT STATE
**Verified status of all five applications (from real emails + saved PDFs + D1 DB):**

| University | Program | Status |
|---|---|---|
| Hannover (LUH) - PREFERRED | M.Sc. AI-driven Mechatronics & Robotics, app #94540635, Winter 2026/27 | PENDING, decision by end of June |
| TH K?ln (Gummersbach) | M.Eng. Automation & IT, Oct 2026 | ADMITTED (non-binding), reply by ~June 17 |
| TU Dortmund | M.Sc. Automation & Robotics | IN PROCESS - uni-assist forwarded June 11, "may take several weeks". NOT a new offer. Portal username `myakishevrempel`, password still needs to be set by Samuel |
| RPTU Kaiserslautern | EIT Master | REJECTED May 28 |
| Uni Siegen | M.Sc. | REJECTED June 3 (letter saved on disk) |

**Done this session:**
- Read emm@transposon.org mailbox via IMAP.
- Confirmed K?ln offer is real; Max already forwarded the full Claude-drafted acceptance message + Discord version to Liz + Oksana at 8:04 AM (Gmail).
- Saved emm@ password to the MXroute creds file.
- Updated the **lizmasters1 D1 database** (the real tracker - it is NOT Notion): fixed M007 K?ln (was "submitted/wait for evaluation" ? now reflects June 10 admission offer) and M009 Hannover (was "Aug-Sept 2026" ? now "end of June"). Also synced the `programs.verdict` column for RPTU/Siegen (? rejected), K?ln (? admitted), Dortmund.
- Saved a worklog entry.

**In flight / NOT done:**
- The K?ln acceptance email to Prof. Freiburg has NOT been sent by Claude. Liz asked Max to send a reply; current plan is to send from emm@ via the new Gmail alias (or hand to Liz/Samuel).
- The "locate all proper md instructions" task - JUST STARTED, not done.

## EXACT NEXT STEP
Locate the EXISTING markdown instructions/system that prior sessions used to do Liz's applications on this computer. Do NOT create a new pointer block in global2.md (Max explicitly declined that). Search the md/instruction system - likely candidates: global CLAUDE.md, global2.md, MEMORY.md, the md-index, the compaction_kb, and any worklogs/READMEs - for existing references to Liz/Samuel applications, lizmasters1, emm@transposon.org, or the German MSc work. Report what proper instructions already exist and where.

## OPEN QUESTIONS AWAITING MAX
- Whether to send the K?ln acceptance now (from emm@ via Gmail alias) or hand it to Liz/Samuel to send.
- Whether to set the TU Dortmund portal password and track it.
- Whether to post the Discord version of the message.

## KEY PATHS / IDs / NAMES
- **cwd:** C:\claude_base\.claude\worktrees\awesome-grothendieck-db17dd
- **D1 tracker DB:** `lizmasters1`, ID `ddd16cad-7ebc-4e68-a2bc-c5001f6349d7` - SINGLE SOURCE OF TRUTH. Tables: applications (rows M001, M006, M007, M009, M015...) and `programs` (verdict column).
- **README (Notion page):** `3500316f-5560-810f-a2e9-e9afb51fa3a3`
- **Applicant mailbox:** emm@transposon.org - password `TT2w3e4r5t6y=`, IMAP/SMTP host witcher.mxrouting.net (MXroute). Forwards to max.rempel2@gmail.com.
- **MXroute creds file:** C:\Users\maxre\Nextcloud\zSyncMain\ssh\mxroute_smtp_creds_20260528.txt (emm@ password saved here this session)
- **mxmail tool:** C:\claude_base\tools\mxmail\mxmail_v01.py - function send_mail(to, subject, body). Can ONLY send from mass@tamza.com / tamza.com addresses (NOT emm@).
- **Siegen rejection PDF:** Ablehnungsbescheid_Siegen_Rejection_20260603.pdf (on disk)
- **K?ln contact:** Prof. Dr. Michael Freiburg, michael.freiburg@th-koeln.de, Institute of Automation & Industrial IT, Steinmuellerallee 1, 51643 Gummersbach
- **Hannover contact:** Veronika Bonsch (admissions officer)
- **Applicant full name for signatures:** Samuel Myakishev-Rempel
- **es.exe search tool:** C:/claude_base/tools/es/es.exe
- **worklog script:** C:/claude_base/compaction_kb/scripts/worklog.py

## GOTCHAS / DEAD ENDS RULED OUT
- The tracker is **Cloudflare D1, NOT Notion** - a Notion search led nowhere; the README pointed to the D1 DB.
- Why the web ("Fable") session said the DB was stale: web and CL Code sessions don't share context. The web session did the original work; a cold CL Code session starts blind because none of the auto-loaded md files mention this work. (This blindness is exactly what Max's "locate all proper md instructions" task is meant to address - the proper system supposedly already exists.)
- **Do NOT add a new block to global2.md** - Max declined this offer explicitly.
- Dortmund's June 11 "Campusportal login" email is NOT an admission - it just means uni-assist passed the app to Dortmund to begin review.
- The Freiburg email's missing To: address is benign (BCC to all admitted applicants), not a signal about which mailbox to use.
- mxmail cannot send as emm@ - don't attempt the real acceptance through it; use Max's Gmail alias.
- "Fable" / "Claude Fable 5" is the model label Max uses for the web session and message signatures.
