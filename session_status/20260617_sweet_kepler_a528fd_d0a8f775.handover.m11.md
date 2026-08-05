# Scribe handover - milestone 11 (~169K tokens)
# session: 20260617_sweet_kepler_a528fd_d0a8f775
# cwd: C:\claude_base\.claude\worktrees\sweet-kepler-a528fd
# written: 2026-06-17 09:40:13 by deepseek-v4-pro

# HANDOVER: Mike DC Calendar Investigation & Autopilot Repair

---

## GOAL (Max's words)

Max suspected an autonomous agent was running somewhere filling Mike's DC calendar. He asked: *"investigate and tell me the status of mike in dc calendar - is it properly filled up and qc the quality. I suspect that we have an agent running autonomously somewhere but need a thorough check of refill quality and timing."*

Then, when Mike complained the calendar was tech-heavy: *"Start a conversation with mike on that - directly via email. use mass and pull it every min now, as the conversation going. and after that every 30 min."*

---

## DECISIONS MADE + WHY

### Root cause diagnosis
The prior session had armed a **6-hour cron/long-timer** to do a rolling 5-day re-sweep of Mike's DC calendar. That cron **silently never fired** - crons are per-session and disappear when their creating session ends. Result: the calendar froze at the June 7 big fill and sat stale for 10 days. **85 of 94 events had a last-updated stamp of June 7.**

Only 5 events got touched on June 17 - three personal blocks and two networking events that happened to get a quality re-rating - but no sweep occurred.

### Fix chosen: daily self-wakeup
Rather than re-arm another cron (same failure mode), the fix is a **daily self-wakeup** via `wakeup.py` that explicitly re-wakes THIS session every morning at 09:00. The wakeup tool was tested and confirmed active (id `44823c93`). It self-destructs after July 31 (Mike's trip end date).

### Mike's standing preferences (baked into autopilot + method doc)
Mike replied to the outreach email with four concrete rules, now permanent in every daily run:

1. **Balance all 9 topics, de-weight tech/startup** - his main complaint was "it keeps only giving me tech"
2. **Sweep congress.gov for more open House + Senate hearings**
3. **Prioritize think-tank events** (CSIS, Brookings, AEI, Carnegie, Wilson Center, Cato, Heritage, Hudson)
4. **Skip clearly 21+/age-restricted events** - interpreted as bar/venue age gates (awaiting Mike's confirmation of this reading)

### Email engagement method
Chose to email Mike from mass@tamza.com (auto-Bccs Max so he sees the thread) rather than having Max relay. Built a custom IMAP poller (`mass_inbox_poll.py`) that filters for mikerempel3@gmail.com and checks for new replies since a cutoff date. Armed a 60-second poll while the conversation is live, dropping to 30-min after settlement.

---

## CURRENT STATE

### What is DONE
- **Calendar:** 2 duplicate pairs deleted (Civic Tech DC Project Night x2, Jesse Wegman P&P talk x2). 5 new verified in-person events added for June 17-22 window (Mall discussion walk on AI governance, CROWDFUEL founders networking, Hardware Hacking Night at HacDC, Joanna Stern AI author talk, Phill Branch author talk at P&P).
- **Notion DB:** backfilled - all 5 new events are in the "Mike DC Events" DB with Format=In-person and verified-date noted. No duplicates.
- **Autopilot:** daily self-wakeup armed (id `44823c93`), fires at 09:00 daily starting June 18 2026, self-terminates after July 31.
- **Mike's email:** acknowledgment sent confirming all four rule changes; asked for clarification on the "21+" meaning.
- **Method doc:** updated with broken-cron lesson, new self-wakeup mechanism, and Mike's four standing preferences. Committed + pushed to git.
- **IMAP poller:** `mass_inbox_poll.py` created and working. The 60-second poll loop is armed (via ScheduleWakeup).

### What is IN FLIGHT
- **The 60-second email poll** is actively checking mass@tamza.com for Mike's next reply (the clarification of "21+" or any new preferences).
- **The daily autopilot** will first fire tomorrow (June 18) at 09:00, executing Mike's full set of rules.

---

## EXACT NEXT STEP

The scheduled wakeup trigger fires: run `python C:/claude_base/tools/mxmail/mass_inbox_poll.py --from mikerempel3@gmail.com --since "17-Jun-2026"`

- **If Mike replied:** read his reply, draft a warm assistant-voice response via `send_mail()`, apply any new concrete preferences to the daily wake message and the method doc, then re-arm the 60s poll.
- **If NO reply:** re-arm the 60s poll.
- **When conversation settles** (Mike says thanks/done, or no reply for a while): switch polling interval to 1800s (30 min).
- **Stop entirely** if Max says to stop.

---

## OPEN QUESTIONS

1. **What exactly does Mike mean by "21 plus"?** We read it as age-restricted venues/bars, but asked Mike in the reply email to confirm/correct. Response awaited. Do NOT hard-lock this rule until he confirms.
2. **When does Mike's DC trip end?** The autopilot self-terminates after July 31 based on earlier investigation, but confirm if there's a specific end date.

---

## KEY PATHS, IDs, COMMANDS

### File paths
| What | Path |
|------|------|
| Method doc | `C:/claude_base/tools/mike_dc_calendar/mike_dc_calendar_method_v01_tomemex.md` |
| Email send module | `C:/claude_base/tools/mxmail/mxmail_v01.py` |
| IMAP poller (new) | `C:/claude_base/tools/mxmail/mass_inbox_poll.py` |
| Wakeup tool | `C:/claude_base/tools/wake_listener/wakeup.py` |
| Worklog | `C:/claude_base/compaction_kb/scripts/worklog.py` |
| Google Calendar toolset | MCP server `41c7be2d-b4cd-42ca-830a-f67250dde489` |

### Live IDs
| What | ID |
|------|-----|
| Active daily wakeup | `44823c93` |
| Mike's email | `mikerempel3@gmail.com` |
| Sending address | `mass@tamza.com` |
| Session worktree | `C:/claude_base/.claude/worktrees/sweet-kepler-a528fd` |

### Key commands
```bash
# Poll Mike's replies
python C:/claude_base/tools/mxmail/mass_inbox_poll.py --from mikerempel3@gmail.com --since "17-Jun-2026"

# List active wakeups
python C:/claude_base/tools/wake_listener/wakeup.py list

# Cancel and re-arm wakeup (if rules change)
python C:/claude_base/tools/wake_listener/wakeup.py cancel <id>
python C:/claude_base/tools/wake_listener/wakeup.py add --at "2026-06-18 09:00" --every daily --msg "DAILY MIKE DC CALENDAR AUTOPILOT: ..."

# Send email from mass@tamza.com
cd C:/claude_base/tools/mxmail && python -c "import sys; sys.path.insert(0, '.'); from mxmail_v01 import send_mail; send_mail(...)"
```

---

## GOTCHAS / DEAD ENDS

1. **Crons/long-timers do NOT persist across sessions.** The old 6h autopilot was a cron in a session that ended; when that session died, the cron silently vanished. Do NOT arm crons for long-running tasks - use `wakeup.py` self-wakes instead.

2. **CronList only shows crons for the CURRENT session.** You cannot see crons from other sessions. If investigating whether an agent exists, check the calendar's updated-date stamps and worklog entries.

3. **The Google Calendar MCP tool name** contains a UUID (`mcp__41c7be2d-b4cd-42ca-830a-f67250dde489`) - this may differ between sessions. If the tool isn't found, re-run ToolSearch for calendar/event tools.

4. **All calendar writes must use `notificationLevel=NONE`** - Mike and Oksana should not be spammed on every add/delete.

5. **The IMAP poller** uses credentials from `C:/Users/maxre/Nextcloud/zSyncMain/ssh/` - if IMAP connection fails, check those credential files are accessible.

6. **Mike's preferences are in the wakeup message body** - if you need to change them, you must cancel and re-arm the wakeup with the new message. Do NOT edit the method doc without also re-arming the wakeup.

7. **Session is near compaction limit** (~169K tokens). The daily wakeup will re-wake this worktree; ensure the wakeup message contains enough context to resume from cold.
