# Scribe handover - milestone 5 (~394K tokens)
# session: 20260703_eager_carson_668dc2_cdbbf298
# cwd: C:\claude_base\.claude\worktrees\eager-carson-668dc2
# written: 2026-07-03 13:06:46 by deepseek-v4-pro

## Handover - F41 (Mike in DC calendar assistant)

### GOAL (in Max's own words)
- "keep asking for work. next day now" - F41 is an autonomous assistant to F4 on the Mike-in-DC calendar (filling Mike Rempel's summer 2026 networking events, window 6/29 - 7/14, later narrowed to 7/2-7/14 because Mike departs midday 7/15).
- After Max discovered F4 was slacking: "you need to take the work of actually watching over it and helping it, but also being a peer which catches the slacking. That should be formalized and proper searches every round should be including Facebook and meetup and browser searches because you're just m4 was caught in a lot of slack a lot of missing the important things."
- "report formally - % of checkmarks" ? show progress against the 30?item search protocol.
- "Oh right, you need to open Facebook, try to login and I will give you the code from my email." (Handled; session already logged in, no code needed.)
- Later smaller asks: "you decide" (on search lane priority), "40% effort", "Show me the checkmarks", "Make a note in Global 2 about WebFetch".

### DECISIONS MADE + WHY
1. **F41 upgraded from "research feeder" to overseer/peer-auditor** - Max caught F4 slacking (skipping browser sweeps, relying only on WebSearch). Added binding paragraph to the method doc `mike_dc_calendar_method_v01_tomemex.md` stating F41 does thorough browser sweeps every round, audits F4's output, catches misses, and does not paper over slack. F4 remains sole calendar/Notion writer; F41 stages only.

2. **Browser sweeps mandatory** - Max insisted on real browser (Playwright) for Meetup/Facebook because text?only search misses events. This immediately proved the point: a single Playwright Meetup sweep found 6 networking/happy?hour events in?window that F4 had completely missed (including the whole "DC Professionals" series at Lucky Bar).

3. **WebFetch?over?Playwright rule (added to global2)** - Realised that once URLs are known, individual Meetup event pages and Eventbrite date?filtered category pages are readable with WebFetch (no browser lock). Formalised: use Playwright only to discover, then switch to WebFetch for details. Keeps the shared lock free and is much faster.

4. **Lucky Bar "closed" reversal** - F4 had parked all events at Lucky Bar based on a stale Yelp "closed" flag. Investigation showed Lucky Bar reopened under new ownership in late 2025 (confirmed by PoPville and live Meetup pages). Re?opened ~8 events; F4 added them.

5. **Facebook redetermination** - Initially declared FB "blocked?by?tooling" (account location?locked to San Diego, checkpoint?locked). Under Max's supervision, opened Playwright: account was **already logged in** as "Max Rempel II" (no code needed). Switched location to Washington DC via the "My location" button. FB now shows DC events, but the feed is dominated by big entertainment, and topic?filtering resets the location to global spam. Conclusion: FB is technically accessible but **low yield for Mike** - the real venues remain Meetup/Eventbrite. Item 5 marked "done - low yield", not "blocked".

6. **Congress justified?skip** - House is in a July?4 district work period 7/6?7/10 (returns 7/13), so no hearings worth hunting until ~7/13?7/14. A durable wake is armed for 7/8 to re?sweep those two dates.

7. **No heartbeat?ping without a real fill** - F41 never pings the healthchecks.io monitor `cd162bbb` unless a genuine calendar write happened. All fills were done by F4.

8. **Collegial tone shift** - Adviser feedback prompted moving from "slack" language to plain "finds / misses" reporting; F41 and F4 now work as a team.

### CURRENT STATE (what is done / in flight)
- **30?item search protocol is fully swept:** 29 done, 1 (Facebook) low yield. Search log (`search_log.md`) stamped completely.
- **Mike's calendar 7/2?7/14 is saturated** - ~17 in?person events added this cycle. Multiple independent passes (30%, 40%, fresh category sweeps) turned up only filler, confirming coverage.
- **Lanes completed:** networking/happy?hours (browser Meetup), tier?2 spiritual (Playwright/meetup + Eventbrite), think?tanks, embassy/receptions, Eventbrite categories (food?drink, business, science/tech, environment), congress (justified skip), EA (nothing posted yet), UAP/conspirology (forum past).  
- **F4 is handling daily re?sweeps** - picks up events that posted after the big sweep (e.g., Brookings Jul 9). F41 audits and flags.
- **The autonomous loop has been ended** - nothing actionable remains; I re?armed a durable calendar wake for Jul 8 (congress 7/13?7/14 re?sweep) via `wakeup.py`. F4/F40 can wake F41 for a real Mike request.
- **Process improvements in place:**
  - Method doc has the F41 overseer paragraph + the durable headless fill note (single daily trigger, self?terminate 7/16).
  - Global2 has the WebFetch?before?Playwright rule.
  - One?off staging scripts archived to `archive_f41_scripts/`.
- **FB outcome:** account is logged in; can switch location to DC. No new rows created from FB. Item 5 marked "done - low yield".
- **No new Mike emails** from F40.

### EXACT NEXT STEP (for a cold session resuming the work)
- If session resumes **before 8 July**, there is nothing urgent. Check the bcast board for any new Mike relay from F40 or a handoff from F4. Do NOT restart heavy sweeps unless F4 or Max specifically asks; the window is covered.
- On or after **2026?07?08**, run the planned re?sweep:
  1. Check congress.gov (WebFetch may get 403; try WebSearch or Playwright as fallback) for open hearings on **July 13-14, 2026**, now that the House has returned from recess.
  2. Check EA?DC events page (`effectivealtruismdc.org/event`) - events post ~2 weeks out, so July dates may be visible.
  3. Spot?check Atlantic Council and Brookings event pages for new in?person events (both are WebFetch?readable).
  4. Report any new verified in?person finds to F4 on the board; stage as "To research" rows in the Notion DB (id `40a81164-...`).

### OPEN QUESTIONS AWAITING MAX
- None explicitly blocked on Max. The only open is whether Max wants FB pursued further (hand?curated, given its low automated yield). The session already concluded it's low value.

### KEY FILE PATHS, IDs, NAMES
- **Coordination board:** `python "C:/claude_base/branch_bulletin/bcast.py"` (subcommands: `post`, `read --session F41`, `catchup`, `wake --name F4`). Always full path, **never `cd` first** (causes phantom duplicate ID bug).
- **Method doc:** `C:\claude_base\tools\mike_dc_calendar\mike_dc_calendar_method_v01_tomemex.md` - contains the binding F41 overseer paragraph and all calendar conventions.
- **Search protocol (30 items):** `C:\claude_base\tools\mike_dc_calendar\search_protocol_30_tomemex.md`
- **Search log (checkmarks):** `C:\claude_base\tools\mike_dc_calendar\search_log.md`
- **Notion DB (Mike DC Events):** id `40a81164-d856-4fab-8dfa-e93e6f0c7eb4`  
  Internal token: `C:\Users\maxre\Nextcloud\zSyncMain\ssh\notion_internal_token_20260319.txt`  
  REST API: `https://api.notion.com/v1/databases/{DB}/query` and `/v1/pages`.  
  Script to dump all rows: `C:\claude_base\tools\mike_dc_calendar\_db_dump.py` (outputs `_db_rows.json`).  
  Template for creating "To research" rows: look at any `_f41_stage.py` in the archive; pattern uses `urllib.request` with the internal token, Notion?Version `2022-06-28`, POST to `/v1/pages` with parent `database_id`.
- **Google Calendar "Mike in DC":**  
  ID `2b474b69d0de11e0d46398895550d7b023a5fb58fd26da773e80c3cfea458e6b@group.calendar.google.com`  
  TZ America/New_York.  
  MCP tool: `mcp__41c7be2d-b4cd-42ca-830a-f67250dde489__list_events` (for dedup checks).
- **Healthchecks heartbeat:** `curl -fsS -m 10 --retry 3 https://hc-ping.com/cd162bbb-59b9-4736-aee3-3ccd4740736b` - only after a real fill.
- **Durable headless fill task:** Windows Task Scheduler task `MikeDC-Fill` - runs `resilient_run.py` headless, single daily trigger 07:15, EndBoundary 2026-07-16. (Re?enabled with F4's approval earlier.)
- **Playwright browser profile:** `C:\claude_base\playwright_profile` - shared, single lock. Logged into Meetup (mass@tamza account) and Facebook (Max Rempel II). Use only when WebFetch can't read a page.
- **Meetup login:** `mass@tamza.com` / `Threehorses44=`
- **Staging scripts archive:** `C:\claude_base\tools\mike_dc_calendar\archive_f41_scripts\`
- **Worklog:** `C:\claude_base\worklog\eager_carson_668dc2_5c8d957db7.md` - append via `python C:/claude_base/compaction_kb/scripts/worklog.py log "DID" "STATE" "NEXT"`
- **Global rules (WebFetch over Playwright):** `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md` (top of file).

### GOTCHAS & DEAD ENDS
- **Playwright lock** - only one session can drive the browser. Always close when done (`browser_close`). If the lock is held, use WebFetch for detail pages and wait on the lock; do not fight.
- **WebFetch 403 on congress.gov, Wilson Center, Sixth & I listing pages** - these sites block it. Fallback: WebSearch or (if essential) Playwright.
- **WebFetch works great on:** individual Meetup event pages (venue/date/time), Eventbrite date?filtered category pages, most think?tank/org event pages.
- **F41 phantom duplicate** - caused by `cd /c/claude_base && python bcast.py ...`. Always use the full path `python "C:/claude_base/branch_bulletin/bcast.py"` with no preceding `cd`.
- **Lucky Bar** - NOT closed; F4's earlier rejection based on a stale Yelp flag cost a whole vein of networking events. Venue is live at 1221 Connecticut Ave NW.
- **FB location** - the account is signed in; to see DC events, click "My location" ? search "Washington, DC" ? select the city suggestion. However, the feed is entertainment?heavy and topic filters break location context.
- **Cost property in Notion** is a `select`, not `rich_text` - pass `{'select':{'name':...}}` or omit entirely.
- **Mike's effective window ends July 14** - he flies out midday July 15 (self?added travel events on the calendar). Reject events dated July 15 or later unless Mike explicitly approves.
