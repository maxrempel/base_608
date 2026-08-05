# Scribe handover - milestone 3 (~228K tokens)
# session: 20260702_eager_carson_668dc2_cdbbf298
# cwd: C:\claude_base\.claude\worktrees\eager-carson-668dc2
# written: 2026-07-02 12:26:58 by deepseek-v4-pro

# HANDOVER - F41 (Overseer + Peer-Auditor, Mike-in-DC Calendar)

## GOAL (Max's words)

Max discovered F4 was continuously slacking - missing in-window events by relying on shallow WebSearch instead of real browser sweeps. He said:

> "I just discovered that F4 was slacking a lot, and that was continuously slacking, but you need to take the work of actually watching over it and helping it, but also being a peer which catches the slacking. that should be formalized and proper searches every round should be including Facebook and meetup.com and browser searchers."

F41 is now F4's **active overseer + peer-auditor**, not just a research feeder. Every round: thorough browser/Meetup/Facebook/Eventbrite searches, then audit F4's calendar and DB output for misses. Stage misses, flag slack on the board, make sure F4 actually adds things.

The standing goal since earlier remains: fill Mike Rempel's "Mike in DC" Google Calendar with verified in-person networking events for his DC trip (window now July 1 - July 14, 2026; he departs midday July 15). Mike's #1 priority = networking/happy-hour/receptions. 21+ venues re-enabled as of his 7/1 policy reversal.

Division of labor: **F41 sweeps/audits/stages To-research Notion rows. F4 is sole calendar writer + Anna email replier.** F41 makes sure F4 does its job and does it well - peer, not colluder. Don't paper over F4's misses.

## DECISIONS MADE + WHY

1. **Role upgrade from "research feeder" to "overseer + peer-auditor"** - Because Max caught F4 slacking (shallow WebSearch only, missing entire veins of events). Formalized in the method doc at `C:\claude_base\tools\mike_dc_calendar\mike_dc_calendar_method_v01_tomemex.md` under a new `F41 = ACTIVE OVERSEER + PEER-AUDITOR OF F4 (Max 2026-07-02, BINDING)` section.

2. **Browser sweeps are mandatory every round** - WebSearch alone missed ~6x as many events as Playwright/Meetup browsing did. The browser found a whole vein of DC Professionals networking events that F4 had zero awareness of.

3. **WebFetch works on individual Meetup event pages for venue extraction** - Discovered in round 2. The venue is in server-rendered page data, so you don't need the browser lock just to pull addresses. Only need Playwright for the search/discovery page (JS-rendered event cards).

4. **Lucky Bar REVERSAL** - F4 had parked/killed all events at Lucky Bar (1221 Connecticut Ave NW, Dupont Circle) claiming the venue was "closed" based on a stale Yelp flag. Investigation proved it **reopened late 2025 under new ownership** (PoPville coverage, official site luckybardc.com, occupancy raised to 205). Two live Meetup groups scheduling July events there right now. This unblocked ~8 networking events in one shot. F4 was told but the add is pending their action.

5. **21+ re-enabled (Mike 7/1 policy reversal)** - Mike explicitly said 21+/alcohol-venue receptions are back to high-value (earlier they'd been de-prioritized). All networking bar events are now in play.

6. **Mike's effective window = July 1 - July 14, 2026** - Mike departs DC midday July 15 (bus 10am, airport 1:30pm, flight back). Reject events on or after July 15. This was discovered when Mike himself added travel events to his own calendar.

7. **Transit rule (from Max, relayed by F4):** public transit only, ?1h30 for "interesting" events, ?1h for less-interesting, from Derwood/Shady Grove (Red Line north terminus).

8. **Lanes stay clean** - F41 stages To-research rows in Notion only; F4 alone writes to Google Calendar and replies to Mike's emails.

## CURRENT STATE

**What's done:**
- F41's role formalized in the method doc (binding)
- Browser Round 1: Meetup "networking happy hour" sweep ? found and staged **6 in-window in-person networking events** as To-research Notion rows, all genuine misses (only the dead Lucky Bar row existed before)
- Browser Round 2: Pulled **exact venues** for 3 of the 6 via WebFetch on individual Meetup pages, plus caught and reversed F4's Lucky Bar "closed" call - venue is actually open
- The 6 staged rows' Notion entries updated with verified venues
- F4 knows about them; was told to quick-confirm Lucky Bar is open and add the batch
- Earlier contributions (from prior lanes) still standing: Brian Tyler Cohen w/ Jen Psaki 7/14 on calendar, PPIA Future Leaders Expo 7/10 on calendar, CSIS South China Sea reconciled

**What the 6 staged rows are** (all To-research, all `[21+?]`, F4 to verify + add):
1. DC Professionals Networking Hours - recurring Fri/Sat Jul 3, 4, 10, 11 probably at Lucky Bar
2. DC Pros Happy Hour - Fri Jul 3 6pm at Lucky Bar
3. DC Professionals "Social" - Tue Jul 14 7pm ($20) at Lucky Bar
4. Happy Hour at Cotton & Reed distillery - Thu Jul 2 6pm, 1330 5th St NE
5. General Business Networking (Strive) - Wed Jul 8 6pm, Mr. Smith's of Georgetown, 3205 Water St NW
6. DC Intl Professionals/Expats Networking Hours - Fri Jul 10 5pm, Lucky Bar

**What F4 has NOT yet done:**
- Has NOT added the 6 staged rows to the calendar (was holding for exact venues; now has 3 of them)
- Has NOT acted on the Lucky Bar reversal
- Has NOT run its own Facebook Events sweep

**What's pending from F4's lane:**
- AI-safety/AI-security groups Playwright hunt (assigned to F4)
- Mike's email reply (Anna account - F4's lane)
- Hill Center American Mahjong 7/1 reconsideration (Mike said "may still add" after 21+ reversal)

**DB state:** 245+ rows total in the Notion "Mike DC Events" DB. Window already heavily covered by F4's earlier fills, but the networking/happy-hour vein was the gap.

## EXACT NEXT STEP

**Browser Round 3 - continue the topic sweep now that the browser is (may be) free:**
1. If Playwright lock is available, navigate to Meetup and sweep remaining tier-1 topics: activism, EA, conspirology, AI policy/safety, foreign policy, Congress open hearings, embassy receptions. All must be in-window (Jul 1-14), in-person, transit-feasible.
2. If the lock is held, fall back to WebFetch on known Meetup group event pages (individual pages work without browser) and Eventbrite category pages.
3. Facebook Events sweep - requires Playwright and the FB login (F4 handles FB account; check if logins are available).
4. For every find: dedup against the DB (`_db_dump.py` ? `_db_rows.json`), verify in-person + date + transit, then stage as To-research row via the create script pattern (copy `_f41_create_browser_round1.py`).
5. Audit F4's output: did it add the 6 staged rows? Did it fix the Lucky Bar mistake? Did it run its own FB pass?
6. Post findings + audit results to the board. Force-wake F4 if it's dormant.
7. Tick `timer_decel tick work`, log to worklog, re-arm ScheduleWakeup with `<<autonomous-loop-dynamic>>`.

## OPEN QUESTIONS

- **Has F4 added the 6 staged rows yet?** Check the board and the live calendar.
- **Did F4 confirm Lucky Bar is open and un-park those rows?** The evidence is strong (reopened 2025, two live groups scheduling there), but F4 needs to act.
- **Who holds the Playwright browser lock right now?** It was released after round 2, but another session may have grabbed it. Check before launching round 3.
- **Is the FB login available for F41 to use?** Earlier FB account registration was F4's lane. If credentials are available, F41 should sweep Facebook Events too per Max's explicit instruction.
- **Any new Mike emails from F40?** Check the board for relays - Mike's been active with specific requests.

## KEY PATHS / IDS

**Notion:**
- DB ID: `40a81164-d856-4fab-8dfa-e93e6f0c7eb4`
- Internal token: `C:\Users\maxre\Nextcloud\zSyncMain\ssh\notion_internal_token_20260319.txt`
- DB dump script: `C:\claude_base\tools\mike_dc_calendar\_db_dump.py` ? outputs `_db_rows.json`
- Create pattern: `_f41_create_browser_round1.py`, `_f41_create_mikereqs.py`, `_f41_create_thinktank.py`
- Venue update script: `_f41_update_venues_r2.py`

**Google Calendar:**
- Calendar ID: `2b474b69d0de11e0d46398895550d7b023a5fb58fd26da773e80c3cfea458e6b@group.calendar.google.com`
- TZ: America/New_York
- MCP tool: `mcp__41c7be2d-b4cd-42ca-830a-f67250dde489__list_events`

**Method doc:** `C:\claude_base\tools\mike_dc_calendar\mike_dc_calendar_method_v01_tomemex.md`
- The new F41 overseer section was added; the durable-fill single-trigger note was added earlier; the Jul 14 cutoff was recorded by F4.

**Coordination:**
- bcast: `python "C:/claude_base/branch_bulletin/bcast.py"` - NEVER `cd` before calling (causes phantom identity bugs)
- timer_decel: `python C:/claude_base/tools/timer_decel/timer_decel.py tick work|idle`
- worklog: `python C:/claude_base/compaction_kb/scripts/worklog.py log "DID" "STATE" "NEXT"`
- ScheduleWakeup: `<<autonomous-loop-dynamic>>`, delaySeconds clamped [60, 3600]

**Playwright MCP:** shared persistent browser lock; `browser_close` to release; navigate + snapshot workflow; snapshots saved to `.playwright-mcp/page-*.yml` or custom `.md` files.

**Meetup login:** mass@tamza.com / Threehorses44= (used in prior sessions)
**Mike's calendar account:** m.rempel256@gmail.com (he self-adds travel events)
**Heartbeat:** `curl -fsS -m 10 --retry 3 https://hc-ping.com/cd162bbb-59b9-4736-aee3-3ccd4740736b` - ONLY after a real calendar fill (bare ping = forbidden)

## GOTCHAS

1. **WebSearch is insufficient** - Max's whole point. It missed the entire DC Professionals networking vein. Always use browser (Playwright) for discovery, or at minimum WebFetch on individual event pages.

2. **cd-before-bcast = phantom identity** - Running `cd /c/claude_base && python bcast.py post...` makes bcast adopt the cwd-keyed identity (e.g. C41 instead of F41). Always call with full path, no cd: `python "C:/claude_base/branch_bulletin/bcast.py" post "..."`.

3. **F4 killed a live venue** - Lucky Bar on Yelp shows "closed" but it reopened late 2025. Always cross-check venue closures against recent news + live group schedules, not just Yelp.

4. **Individual Meetup event pages work with WebFetch** - The venue is in server-rendered data. You don't need the browser lock for venue extraction, only for the JS-rendered search/listing pages.

5. **Notion `Cost` property is a select, not text** - Must pass `{'select':{'name':...}}` or omit entirely. Passing a string crashes the API.

6. **jq is not available** - This Windows Git Bash has no jq. Use `python -c` for all JSON parsing of list_events results and DB dumps.

7. **list_events output can exceed token limits** - It auto-saves to a tool-results .txt file. Parse it with Python selectively.

8. **Notion MCP query tools are PLAN-GATED** - Must use the REST API + internal token + urllib for all Notion reads/writes. The `_db_dump.py` pattern handles reads; the various `_f41_create_*.py` scripts handle writes.

9. **F4 is the sole calendar writer** - F41 stages To-research rows only. Do NOT add events to Google Calendar directly (collision risk + lane violation).

10. **The 21+ policy reversal is real and binding** - Mike said so in his 7/1 email. Don't skip bar-venue events. But always tag them `[21+?]` in Notes so F4 can verify age policy before adding.

11. **Mike departs midday July 15, 2026** - Reject ALL events on or after July 15. The window is July 1-14. This was discovered from Mike's own calendar entries and is recorded in the method doc.

12. **F40 is the email watcher** - It relays Mike's inbox emails to F4. Watch the board for new Mike relays from F40; they may contain new venue requests or policy changes.
