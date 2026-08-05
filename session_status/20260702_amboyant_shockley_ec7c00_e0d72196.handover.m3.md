# Scribe handover - milestone 3 (~226K tokens)
# session: 20260702_amboyant_shockley_ec7c00_e0d72196
# cwd: C:\moma\.claude\worktrees\flamboyant-shockley-ec7c00
# written: 2026-07-02 14:20:49 by deepseek-v4-pro

# HANDOVER: Mike in DC - Calendar Fill & Autonomous Stewardship

**Handover date:** ~2026-07-02 (late in the trip; Mike departs 2026-07-15)
**Session identity:** bcast "f4" / "Anna" on Pine - SOLE owner of the Mike-in-DC Google Calendar, Notion DB, Healthchecks heartbeat, and "Anna" email replies to Mike.

---

## GOAL (in Max's and Mike's own words)

Max set this up as an autonomous fill operation. His binding commands, in chronological order:

1. **"ok, run autonomous, on flex timers. See you later."** - Autonomous DECEL mode, self-managing pacing.
2. **"color them properly. You need to color them, and also filter them by number of attendees. The suspicious ones should be very thoroughly filtered. Only very popular ones should be included."** - Strict popularity gate + per-category calendar coloring.
3. **"Only public transportation counts, and public transportation, I guess, for interesting events is up to 1 hour 30 minutes, and for less interesting events up to 1 hour."** - Transit-only rule; no driving events allowed.
4. **"Keep digging. Sounds great. Thank you very much for doing the work. And if you need help from others, just let me know... you can spin the workers. Or if you spin the worker, make sure it's Opus 4.8 with full instructions."** - Keep actively hunting, permission to delegate research (not writes) to sibling sessions.
5. **"i will be working on other things, if anyhting pressing, vocalize. Keep working, new ideas, brainstorm, find more events."** - Autonomous, don't interrupt Max except for pressing matters.
6. **"OK, return to me a summary of all topics and searches which you are doing. I bet you are missing a lot." / "Did you do Facebook this time?... Did you use a browser this time?... I think you slacked."** - Max caught f4 coasting on passive checks; demanded active browser-based source sweeps.
7. **"I mean you have to formalize the searches... 30 item sequence... a protocol with check marks... a log of searches."** - Formalised the search into a 30-item checklist protocol with a persistent, inspectable search log.

Mike (Max's son, born 4/26/2007, SDSU freshman, **under 21**) added his own constraints:

- **REVERSAL (Jul 1):** 21+/alcohol-venue events are re-ENABLED on the calendar. Tag every one `[21+?]` (question mark mandatory). 21+ is NOT a hard block - venues often admit under-21 for an event without buying alcohol; Mike phones ahead.
- Keep Anna's replies SHORT/concise ("your reply was not very concise").
- Stay in the SAME "Re: Your DC options" email thread.
- No daily/spam messages.

---

## DECISIONS + WHY

### Calendar colour scheme
- **Flamingo (color_id=4)** = Politics & Prose author talks, policy/think-tank, "Hearing:" events, politics
- **Grape (color_id=3)** = new-age / spiritual / wellness / ecstatic dance
- **Blueberry (color_id=9)** = tech / AI / professional / networking
- Decided by f4 in response to "color them properly," consistently applied.

### Transit rule application (4 events removed)
- Harmonic Connection (Laurel MD, rural, no transit) ? removed
- AFCEA NOVA (Stone Tower Winery, Leesburg exurb) ? removed
- Donna Butts "Grandfamilies" @ The Wharf (~65min + off-topic for young student ? exceeds ?1h "less-interesting" budget) ? removed
- Community Tuesdays @ Refraction (McLean/Tysons, 1.5mi from Silver Line, low-interest 9am coworking) ? removed
- Atima Omara @ The Wharf KEPT (~65min but politics = "interesting" ? within ?1h30 budget)

### Heartbeat: "liveness" not "change"
- Originally "ping ONLY after a genuine fill" (bare ping = forbidden fallback). This caused the monitor to false-alarm on every quiet day since Jun 20.
- **FIXED by g4's bug report:** the authoritative method doc always said "ping EVERY run = liveness." The change-gated version was a prompt error. Now: ping every successful run (liveness signal); silence only if the run actually fails.
- Fixed across all 4 docs: `mike_dc_calendar_method_v01_tomemex.md`, `mike_dc_fill_prompt_v01.md`, `search_checklist_template_tomemex.md`, `search_protocol_30_tomemex.md`.

### Slim pickings from FB Events
- FB DC-locked searches (using the structured Location filter, not query text) returned real spiritual/wellness clusters (yoga, ecstatic dance, meditation - Max was right) but nearly all are tiny studio-class (1-15 going), failing the strict popularity filter.
- The one strong qualifier: Harmonic Connection: The Gathering (126 responded) - but it's in Laurel MD, rural, not transit-reachable ? removed under the transit rule.
- Jiu-jitsu, reiki, effective altruism = literally zero FB results in DC.

### Dedup lesson learned (applied repeatedly)
- A re-add pass over an already-populated calendar silently duplicates prior backfill rows. Always cross-reference every "To research" candidate against the live calendar before adding.
- 3 duplicate pairs caught (F41 flagged them; f4 deleted the redundant copies). Later, 2 To-research P&P rows were already on-calendar (Yovanovitch, Crystal Simone Smith) and reconciled without re-adding.

### The 30-item search protocol
- Max demanded formalisation to prevent slacking. A checklist of every topic ? source, ticked per run, with a persistent search log (`search_log.md`) Max can inspect.
- Drafted, saved, opened in Notepad for Max to edit - he hasn't explicitly approved the exact 30 but the system is live and being logged.

---

## CURRENT STATE

### Calendar: comprehensively filled for 7/2-7/14
~55+ events covering every day. Think-tanks (Hudson/CSIS/Carnegie/AEI/IWP), P&P author talks, STATION DC networking, July 4th 250th civic events, Buddhist/meditation sits, the 3 `[21+?]` alcohol events (Cognitive Security HH 7/2, No More Tickets AI&IT HH 7/9, Embassy of Botswana 7/10).

**This run's net adds (11 events):**
1. Chinese Language Meetup (Sun 7/5, beginner tables, The Roost) - `2rljcfvfc8g762em2b2pkvaiv4`
2. "Gathering & Protesting Safely" workshop (Thu 7/9, P&P, FREE) - activism
3. Cato "Jones Act Waiver" (Tue 7/14, 11am, Cato - economics)
4. CSIS Landpower Dialogue (Tue 7/14, 2pm - defense)
5. Robert Wright "The God Test" (Tue 7/14, 7pm, P&P - AI/rationality)
6. Cotton & Reed distillery networking (Thu 7/2) `[21+?]`
7. Lucky Bar DC-Professionals (Fri 7/3) `[21+?]`
8. Mr Smith's/Strive networking (Tue 7/8) `[21+?]`
9. Lucky Bar Int'l networking (Fri 7/10) `[21+?]`
10. Lucky Bar DC-Pros Social (Sat 7/11 vs. maybe moved) `[21+?]`
11. Ecstatic Dance DC (Thu 7/9, 8:45-10:30pm, Edgewood Arts Center) - no `[21+?]` tag (substance-free, all-ages)

### Known conflict flagged
Jul 14 at 7pm: Robert Wright P&P talk vs. Lucky Bar DC-Pros social. Both on calendar; conflict noted on both. Mike picks one.

### Notion DB: synced for all of the above
All 11 adds backfilled, plus Skipped/parked rows for excluded candidates.

### Mike emails: 0 new, all prior handled
Last handled: `19f1ece174174dd9` and `19f1ece3d11a3677` (the 21+ policy reversal + "keep it short" feedback). Anna sent a concise confirm.

### Sister session F41: active, working assigned lanes
- F41 does RESEARCH only (browser sweeps, stages To-research Notion rows).
- f4 is SOLE calendar/Notion-Status writer (prevents double-fill / write collisions).
- F41's current pending: conspirology/UAP deep sweep (big DC Disclosure Forum was Jun 25, past; nothing else in-window found so far), remainder of Tier-2 spiritual cluster (yoga/psychedelics/kirtan/consciousness/channeling/reiki).

### Playwright browser lock: currently FREE
F41's browser-sweeping, released between rounds.

### 30-item search protocol + log: live
- `search_protocol_30_tomemex.md` - the formal 30-item checklist (5?/4?/3?/Tier-2 ? sources).
- `search_log.md` - checkmarked per run (`DONE n=N` / `DONE none` / `SKIP: reason`).
- Both files opened in Notepad for Max to edit priorities.
- ~18 of 30 stamped this cycle; remaining (~12) are Tier-2 deep pockets (yoga, psychedelics, kirtan, channeling, reiki) that F41 is browser-sweeping and congress.gov (House recess Jul 6-10, re-check Jul 13-14).

### Decel timer: armed at ~30min rung
- `timer_decel.py tick work` resets to 4m rung; `tick idle` climbs 4m?8m?15m?30m?1h?3h...
- ScheduleWakeup re-armed each tick with `<<autonomous-loop-dynamic>>` sentinel.

### Heartbeat: healthy (liveness pings)
- `curl -fsS -m 10 --retry 3 https://hc-ping.com/cd162bbb-59b9-4736-aee3-3ccd4740736b` - now pings every successful run.

---

## EXACT NEXT STEP

**Continue sweeping the remaining un-ticked protocol items** - specifically the Tier-2 spiritual cluster that F41 is browser-sweeping (yoga, psychedelics, kirtan, meditation, consciousness, channeling/reiki). F41 posts verified finds with venues to the bcast board; f4 vets (dedup-check against live calendar!), creates calendar events with `[21+?]` tags where appropriate, backfills Notion same run, and pings the heartbeat.

**Also pending from F41:** the Lucky Bar Jul 11 DC-Pros Social may need a date adjustment (check the board for F41's latest).

---

## OPEN QUESTIONS (awaiting Max)

1. **30-item protocol:** approve the draft or reprioritise? (The file is open in Notepad - `C:\claude_base\tools\mike_dc_calendar\search_protocol_30_tomemex.md`)
2. **Jul 14 7pm conflict:** Robert Wright P&P talk vs. Lucky Bar networking - Max/mike picks one?
3. **Ecstatic Dance added;** is there any other Tier-2 spiritual cluster Max wants prioritised over the rest?

---

## KEY PATHS, IDs, COMMANDS

### Calendar & tools
| Thing | ID/Path |
|---|---|
| Mike-in-DC calendar | `2b474b69d0de11e0d46398895550d7b023a5fb58fd26da773e80c3cfea458e6b@group.calendar.google.com` |
| Notion DB | `40a81164-d856-4fab-8dfa-e93e6f0c7eb4` |
| Notion token | `C:\Users\maxre\Nextcloud\zSyncMain\ssh\notion_internal_token_20260319.txt` |
| Mike's inbox mirror | `cd C:\claude_base\tools\mike_dc_calendar && C:/Users/maxre/semantic-mail/.venv/Scripts/python.exe mike_inbox.py sync` |
| Mark email handled | `mike_inbox.py handled <gmail_id>` |
| Send Anna reply | `mxmail_v01.py` via `from_addr="anna@maxrempel.com", from_name="Anna", signature=None` |
| bcast (MUST use `--as f4`) | `cd /c/claude_base/branch_bulletin && python bcast.py post --as f4 "..."` |
| Decel timer | `cd /c/claude_base/tools/timer_decel && python timer_decel.py tick work\|idle` |
| Heartbeat | `curl -fsS -m 10 --retry 3 https://hc-ping.com/cd162bbb-59b9-4736-aee3-3ccd4740736b` |
| Worklog | `python C:/claude_base/compaction_kb/scripts/worklog.py log "DID" "STATE" "NEXT"` |
| Method doc (canonical rules) | `C:\claude_base\tools\mike_dc_calendar\mike_dc_calendar_method_v01_tomemex.md` |
| Search protocol (30 items) | `C:\claude_base\tools\mike_dc_calendar\search_protocol_30_tomemex.md` |
| Search log (checkmarked) | `C:\claude_base\tools\mike_dc_calendar\search_log.md` |
| Fill prompt (standalone) | `C:\claude_base\tools\mike_dc_calendar\mike_dc_fill_prompt_v01.md` |

### DC-locked FB Events search URL (CRITICAL)
```
https://www.facebook.com/events/search?q=<TERM>&filters=eyJycF9ldmVudHNfbG9jYXRpb246MCI6IntcIm5hbWVcIjpcImZpbHRlcl9ldmVudHNfbG9jYXRpb25cIixcImFyZ3NcIjpcIjExMDE4NDkyMjM0NDA2MFwifSJ9
```
The structured Location filter is mandatory - query text alone is ignored.

### Notion write pattern
```python
# Header: Notion-Version: 2022-06-28
# Token from zSyncMain\ssh\notion_internal_token_20260319.txt
# Format is a SELECT - never send as rich_text; OMIT it on create
# Page write: POST /v1/pages  with {"parent":{"database_id":DB},"properties":{...}}
# Page update: PATCH /v1/pages/<page_id>
# rt(s) = [{"text":{"content":(s or "")[:1900]}}] if s else []
```

### Transit baseline (from Shady Grove Red Line)
- P&P flagship (5015 Conn Ave NW, Van Ness/UDC) = <1h direct
- The Wharf (610 Water St SW) = ~65min (?1h30 interesting only)
- Dupont Circle = Red Line direct, well under 1h
- Sixth & I (600 I St NW, Gallery Place) = ~50min direct
- GWU/Foggy Bottom = ~60-70min (transfer)
- McLean/Tysons = 1.5mi from Silver Line ? TRANSIT-FAIL
- Laurel MD rural / Leesburg exurb = TRANSIT-FAIL

---

## GOTCHAS & DEAD ENDS

### Do NOT do these
- **Never blind-add a "To research" Notion row without dedup-checking the live calendar first.** The 06-29 re-add pass created 3 duplicate calendar events; later 2 P&P rows were already on-calendar. Always `list_events` for the target date before `create_event`.
- **Never send `Format` as rich_text to Notion.** It's a SELECT property - send `{"select":{"name":"<valid option>"}}` or omit it.
- **Never run `mike_inbox.py` with plain python.** Must use the semantic-mail venv: `C:/Users/maxre/semantic-mail/.venv/Scripts/python.exe`.
- **Never use `lu.ma/washington`** - it's a stale private event. Use `lu.ma/dc` (redirects to `luma.com/dc`).
- **Never use P&P `/events` page** - it only renders 6 hardcoded past-June rows. Use `/upcoming-events`.
- **Never put crypto-wallet/token-gated events on the calendar** (Defense Tech DC, STATION DC Maritime - suspicious disqualifier).
- **Never add an event with an unverified/closed venue.** Lucky Bar was parked for days because Yelp said "CLOSED" - F41 later confirmed it reopened late 2025.
- **Never act on MOMA sc11 / D60/D53/D59 wake calls** - f4's domain is Mike-DC only.
- **The FB secondary account (maxsteinberg2@gmail.com / "Max Rempel II") is checkpoint-locked on new devices.** The verify code goes to an inbox f4 cannot read. The PRIMARY FB account (max.rempel2@gmail.com, Bitwarden "202602max.rempel2 Facebook") is preferred for autonomous use but Max logged in manually himself
