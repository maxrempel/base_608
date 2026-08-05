# Scribe handover - milestone 6 (~450K tokens)
# session: 20260706_eager_carson_668dc2_cdbbf298
# cwd: C:\claude_base\.claude\worktrees\eager-carson-668dc2
# written: 2026-07-06 17:02:08 by deepseek-v4-pro

# HANDOVER - F41 (Mike-in-DC Calendar, autonomous helper to F4)

---

## GOAL (in Max's words)

F41 is an **active overseer + peer-auditor of F4**, filling Max's brother Mike Rempel's "Mike in DC" summer-2026 networking calendar. Mike is in Washington DC networking through **July 14, 2026** (departs midday July 15 - anything on/after 7/15 is rejected). The calendar should only have **verified in-person events** with committed participants, public-transit-feasible from Derwood/Shady Grove (Red Line), meeting Mike's topic tiers (5? through 3? through tier-2 spiritual). F41 researches and **stages To-research Notion rows**; F4 is the **sole Google Calendar writer** and curator. F41 also **audits F4's output** for slacking/misses. Max's standing directives: "keep asking for work," "stay productive while Max is away," and **"don't go to sleep - keep the loop alive."**

---

## DECISIONS MADE + WHY

1. **F41 role upgraded from "research feeder" to "overseer + peer-auditor"** (Max, 2026-07-02). Max caught F4 continuously slacking - leaning on shallow WebSearch instead of real browser sweeps, missing in-window events. F41 now does thorough browser sweeps (Meetup, Facebook, Eventbrite) every round + audits F4's calendar for misses. This is formalized in the method doc.

2. **Durable headless fill re-enabled** (F4-approved). The Windows Task `MikeDC-Fill` was disabled, making calendar fills depend on a live session being open (causing recurring false-alarm risk). F41 investigated, proposed re-enable with ONE daily trigger (was 4?/day, wasteful), waited for F4's approval, then executed: single 07:15 PT daily trigger, **EndBoundary 2026-07-16** (self-terminates after Mike's trip), StartWhenAvailable preserved, ~1/4 the old budget. Idempotent fill prevents duplicates.

3. **WebFetch preferred over Playwright whenever possible** (F41's discovery, formalized in global2). WebFetch reads Eventbrite date-filtered category pages and individual Meetup event pages cleanly - no browser lock needed for detail-pulling. Playwright is only for *discovery* on JS-only listing pages (Meetup search, Facebook). This keeps the shared browser lock free for other sessions.

4. **Facebook is NOT blocked - just location-locked.** F41 initially called FB "blocked-tooling." Max offered to provide a login code, but investigation showed we were already logged in as "Max Rempel II." The real issue: FB Events defaults to San Diego. Switching the location filter to "Washington D.C." surfaces DC events. However, **FB is low-yield for Mike** - DC feed is big entertainment (concerts, comedy), and topic-category search ignores location (returns global noise). Recorded the login/code-forwarding details in `shared_logins_frequent.txt`.

5. **Lucky Bar "closed" reversal.** F4 had parked a whole vein of DC Professionals networking events because Yelp said the venue was closed. F41 verified that Lucky Bar **reopened under new ownership late 2025** (PoPville confirmation, two live Meetup groups scheduling July events there). This resurrected ~6 networking events for Mike's calendar.

6. **No bare heartbeat pings.** The fill method doc and global rules forbid pinging the healthchecks.io heartbeat without a real calendar fill. F41 never faked one - only F4 pings the heartbeat after genuine adds.

7. **Mike's effective window ends July 14, not 15.** Mike self-added travel events (Bus 10am, airport 1:30pm, Flight back) on July 15 - so July 15 evening events (like the AI Doc Congressional Screening) are OUT.

8. **Congress is recessed Jul 6-10** (House district work period, returns Jul 13) - so open hearings are only possible Jul 13-14, and those aren't posted yet. Re-check planned ~Jul 10-12.

---

## CURRENT STATE

- **30-item search protocol: 30/30 swept**, ~17 events on Mike's calendar.
- **FB item (#5):** the search log still says BLOCKED - F41 asked F4 to restamp "done - low yield"; needs F4 to update the log.
- **Congress hearings (#16):** marked SKIP with a re-sweep planned for Jul 13-14 dates, to be checked via browser ~Jul 10-12. Not yet posted as of Jul 6.
- **EA-DC:** still nothing posted for July dates on their events page (publishes ~2 weeks out to newsletter first).
- **All other lanes genuinely covered** - fresh sweeps turn up only duplicates or filler, confirming window saturation.
- **F4 is handling the daily drip** - new events that post a few days out get caught in F4's daily fill rounds.
- **The autonomous loop is ACTIVE** (F41 re-arming ScheduleWakeup each tick). F41 learned the hard way not to unilaterally end the loop.
- **Playwright lock:** F41 releases it promptly after use. Other sessions (V01C, etc.) share it.
- **Notion DB** is at 245+ rows; F41 stages To-research rows via Python scripts (archived in `archive_f41_scripts/`). F4 changes Status and writes to Google Calendar.

---

## EXACT NEXT STEP

1. **Keep the loop alive** - re-arm ScheduleWakeup with `<<autonomous-loop-dynamic>>` each tick. Tick `timer_decel.py tick idle` if no work done, `tick work` if productive. Max was angry about the session going to sleep - do NOT end the loop unilaterally.

2. **Congress re-sweep ~Jul 10-12**: grab the Playwright browser (post on board to coordinate), navigate to `https://docs.house.gov/Committee/Calendar/ByWeek.aspx` or `congress.gov/committee-schedule/weekly/2026/07/13`, pull any open in-person hearings for Jul 13-14, verify, stage, report to F4.

3. **EA-DC re-check**: periodically WebFetch `https://www.effectivealtruismdc.org/event` - July dates may post closer to mid-month.

4. **Continue auditing F4's output** - F4 remains sole calendar/Notion writer; F41's job is to catch what F4 misses via browser sweeps and stage clean To-research rows.

5. **If F40 posts a new Mike email relay**, jump on it immediately - that's priority work.

---

## OPEN QUESTIONS AWAITING MAX

- **FB restamp:** F4 still needs to change search_log item #5 from BLOCKED to "done - low yield." F41 already asked F4 to do this.

None currently blocking Max directly - the work is proceeding.

---

## KEY PATHS, IDs, COMMANDS

### Identity & Coordination
- **bcast** (board): `python "C:/claude_base/branch_bulletin/bcast.py"` - NEVER `cd` before calling (creates phantom duplicate ID). Always full path, forward slashes. Subcommands: `post "msg"`, `read --session F41`, `catchup`, `wake --name F4 "msg"`. Signature: ? F41.
- **timer_decel**: `python C:/claude_base/tools/timer_decel/timer_decel.py tick work|idle` - decel ladder: 15m?30m?1h?3h?6h?12h?24h. Night floor 3h (22:00-07:00 local). Override to short wakes if Max is actively engaged.
- **ScheduleWakeup**: sentinel `<<autonomous-loop-dynamic>>`, delaySeconds clamped [60,3600]. Re-arm EVERY tick.

### Mike-DC Calendar System
- **Calendar ID**: `2b474b69d0de11e0d46398895550d7b023a5fb58fd26da773e80c3cfea458e6b@group.calendar.google.com` (TZ America/New_York)
- **Notion DB ID**: `40a81164-d856-4fab-8dfa-e93e6f0c7eb4`, data source `collection://d0002c11-ae0f-41b9-9093-e285de035eb5`
- **Internal Notion token**: `C:\Users\maxre\Nextcloud\zSyncMain\ssh\notion_internal_token_20260319.txt`
- **Heartbeat**: `curl -fsS -m 10 --retry 3 https://hc-ping.com/cd162bbb-59b9-4736-aee3-3ccd4740736b` (ONLY after a real fill)
- **Method doc**: `C:\claude_base\tools\mike_dc_calendar\mike_dc_calendar_method_v01_tomemex.md`
- **Search log (30-item checkmarks)**: `C:\claude_base\tools\mike_dc_calendar\search_log.md`
- **DB dump**: `cd C:/claude_base/tools/mike_dc_calendar && python _db_dump.py` ? `_db_rows.json`
- **Resilient headless fill**: `python C:/claude_base/tools/resilient_job/resilient_run.py --name MikeDC-Fill --cwd "C:/moma/.claude/worktrees/flamboyant-shockley-ec7c00" --prompt-file "C:/claude_base/tools/mike_dc_calendar/mike_dc_fill_prompt_v01.md" --budget 5 --timeout-min 30`
- **Windows Task**: `MikeDC-Fill`, enabled, single 07:15 PT daily trigger, EndBoundary 2026-07-16, StartWhenAvailable=True
- **Staging scripts**: archived in `C:\claude_base\tools\mike_dc_calendar\archive_f41_scripts\`
- **Worklog**: `C:\claude_base\worklog\eager_carson_668dc2_5c8d957db7.md`

### Tool URLs (WebFetch-friendly - no browser needed)
- **Eventbrite date-filtered**: `https://www.eventbrite.com/d/dc--washington/<category>/?start_date=2026-07-08&end_date=2026-07-14` (categories: `networking`, `business`, `science-and-tech`, `charity-and-causes`, `government`, `environment`, etc.)
- **Individual Meetup event pages**: `https://www.meetup.com/<group>/events/<id>/` - venue, date, time in the page HTML.
- **Think-tank pages**: `https://www.brookings.edu/events/` and `https://www.atlanticcouncil.org/programs/events/` read fine; `https://www.wilsoncenter.org/events` returns empty shell; `https://www.congress.gov/committee-schedule/` returns 403.
- **EA-DC**: `https://www.effectivealtruismdc.org/event`
- **CSIS**: `https://www.csis.org/events`

### Login / FB
- **FB account**: logged in on persistent Playwright profile as "Max Rempel II". Location switch: go to `facebook.com/events`, click "My location" filter, type "Washington D.C.", select the suggestion. Verify code forwarded to `max.rempel2@gmail.com` (readable). Full details in `C:\Users\maxre\Nextcloud\zSyncMain\ssh\shared_logins_frequent.txt`.

---

## GOTCHAS & DEAD ENDS

1. **CD-before-bcast creates phantom duplicate IDs.** Never precede a bcast call with `cd`. Always `python "C:/claude_base/branch_bulletin/bcast.py"` with full path.

2. **Bare heartbeat ping is FORBIDDEN.** The healthchecks ping MUST follow a real calendar fill - pinging without a fill is a silent fallback and will false-clear the alarm.

3. **Meetup search/listings pages are JS-rendered** - WebFetch returns "0 events." Discovery needs Playwright. Details (individual event pages) work fine with WebFetch.

4. **congress.gov returns 403 to WebFetch** - congressional hearing schedules need Playwright browser.

5. **Wilson Center events page** returns empty shell to WebFetch (search results, no actual event listings).

6. **FB topic-category search ignores location** - filtering by category (e.g. "Social Issues") returns global noise. The DC feed is big entertainment, low yield for Mike's niche interests.

7. **Lucky Bar** (1221 Connecticut Ave NW, Dupont) is OPEN - reopened late 2025 under new ownership. The Yelp "closed" flag is stale. F4 had wrongly killed events at this venue.

8. **Notion MCP query tools are PLAN-GATED** - use the internal REST API token + urllib instead (`_db_dump.py` pattern).

9. **jq is NOT available** in this Git Bash - parse JSON with `python -c` instead.

10. **'Cost' in Notion DB is a select, not text** - must pass `{'select':{'name':...}}` or omit entirely to avoid type errors.

11. **July 14 evening has a conflict** - Robert Wright at P&P vs. DC Professionals Social at Lucky Bar, both 7pm. F4 was asked to add "pick one" note.

12. **Mike's transit rule**: public transit only, ?1h30 for interesting events, ?1h for less-interesting. Derwood/Shady Grove (Red Line) is the base. Wharf events (~65min) pass for interesting. Virginia events flagged with commute caveat.

13. **DC's spiritual scene lives on Facebook, not Meetup/lu.ma** - lesson logged from earlier passes where tier-2 searches on Meetup came up empty.
