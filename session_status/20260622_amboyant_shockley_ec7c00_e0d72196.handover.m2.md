# Scribe handover - milestone 2 (~164K tokens)
# session: 20260622_amboyant_shockley_ec7c00_e0d72196
# cwd: C:\moma\.claude\worktrees\flamboyant-shockley-ec7c00
# written: 2026-06-22 12:49:37 by deepseek-v4-pro

# HANDOVER - F4 / Mike DC Calendar Takeover

---

## GOAL (Max's words, verbatim)

1. **"G4 - check in as F4, start learning about mike's cal updates."**
2. **"Take over form F1 the updates of mikes calendar. The reason that you have 5x context size due to updated [model]."**
3. **"Updates from F4 on pine and emiails are based on calendar and in centauri."**
4. **"Both F4 and centauri should be checking email"**
5. **"15mt"** - set a 15-minute decel self-wake timer.

The take-over is real: **F4 on the Pine worktree (flamboyant-shockley) owns the Mike-DC calendar fill/update job.** The Centauri worktree runs digest email generation *from* the calendar but does its own fills on its own schedule. F4 and Centauri both share the duty of polling Mike's inbound email.

---

## DECISIONS + WHY

### Structural (job architecture)

- **Two-store model maintained:** Notion DB = everything researched (including declined). Google Calendar "Mike in DC" = only verified-in-person events Mike can walk into. Sync is manual every run. *Reason: this is the established method doc; no deviation needed.*

- **EA = #1 priority topic** - gets a dedicated search pass every run. Tech is de-weighted. 21+/receptions/young-pro events are kept. *Reason: Mike's standing preferences from the method doc.*

- **Email read-only on Pine:** F4 polls Mike's inbox but does NOT auto-ack. Centauri owns the auto-reply. *Reason: running the full watcher on both Pine and Centauri would double-reply to Mike. A read-only poll script (`_f4_mailcheck.py`) was written so F4 can detect new requests without stepping on Centauri's replies.*

- **Notion backfill uses raw API token, not MCP tools.** The Notion MCP tools (`notion-query-database-view`, `notion-query-data-sources`) are plan-gated and refused to run. The raw API path via `zSyncMain\ssh\notion_internal_token_20260319.txt` works and was used for both reading existing rows and writing new ones. *Reason: plan gate blocked the tools; existing `_db_dump.py` and `_db_backfill.py` helpers in the calendar folder already used the raw token path.*

- **7 events created, notificationLevel=NONE on all.** Every event includes REGISTRATION link, COMMUTE from Shady Grove/Derwood, DRESS CODE, and street address. *Reason: required fields per method doc.*

### Dedup / gap detection

- **Friday Jun 26 was NOT the gap - Saturday Jun 27 was.** The first `list_events` query (Jun 22-26) hit the 50-event page cap and cut off before reaching Friday's 5 existing events, making Friday look nearly empty. A narrow re-query (Jun 26-28) revealed the truth: Friday had 5 events already (NatGeo grand opening, Print-O-Rama, Jazz in the Garden, 2 P&P author talks). Saturday had zero. *Reason: the 50-event cap masked reality; dedup caught it before duplicates were created.*

- **2 P&P talks the research agent "found" for Friday already existed on the calendar - NOT created again.** *Reason: hard rule in method doc to dedup before writing.*

### Declined / not added

- Healthcare/Pharma mixer, DC Tech Mixer (de-weighted by standing pref), Habesha niche event - declined as low-value padding. *Reason: method doc says "saturation is normal (0-3 events/run), don't pad."*
- Think-tank/hearing searches returned honest saturation; congress.gov, Heritage, and AEI bot-block with HTTP 403. No events manufactured. *Reason: rules forbid inventing hits.*

---

## CURRENT STATE

### Done (closed out)

1. **7 Google Calendar events created** on "Mike in DC" (all returned confirmed IDs):
   - `48kc64v6ouhb0ssve8glb6mt5o` - Smithsonian Folklife Festival (Fri) Jun 26 11:00-17:30
   - `oe96c3aep6mjtqnbjdcu6v27s8` - Capital Conversations Panel + Networking Reception, Jun 26 18:00-20:00, The Madison Hotel
   - `ht317vbshh5p49qj3lhl4bb8es` - Smithsonian Folklife Festival (Sat) Jun 27 11:00-17:30
   - `fcf6540tjmh27hrl03tk5r54mg` - P&P: Aggie Blum Thompson book talk, Jun 27 17:00-18:00
   - `6mujn6urop93nt8804rgo43ds8` - P&P Union Market: Dara Levan book talk, Jun 27 18:00-19:00
   - `aslrkdb8db34ci3dvqf914il58` - [EA] EA DC Animal Welfare Meetup, Jun 25 18:00-20:00, Workshop House
   - `22usirimr6oh2b0bo5tore035k` - [EA] EA DC AI Meetup @ Dacha Beer Garden, Jun 30 18:00-20:00

2. **All 7 backfilled to Notion DB** (5 new pages created, 2 existing pages updated with Format field filled in). **Zero errors, write verified.** Backfill script: `C:\claude_base\tools\mike_dc_calendar\_f4_backfill_20260622.py` (one-shot, can be deleted or reused as template).

3. **Healthchecks heartbeat pinged:** `https://hc-ping.com/cd162bbb-59b9-4736-aee3-3ccd4740736b` returned OK.

4. **Timer armed at 15-minute decel:** `timer_decel.py set 15` printed `DELAY_SECONDS=` and a `ScheduleWakeup` was armed with prompt `<<autonomous-loop-dynamic>>`.

5. **Email check done (read-only):** 3 Mike messages in inbox, newest Jun 21 22:52. No new requests beyond the already-handled "wants Friday events" signal.

6. **Worklog entry written** to `C:\claude_base\worklog\flamboyant_shockley_ec7c00_ee5970c306.md`.

### In flight / pending from the task

- **Email threading fix** - Mike's Jun 21 signal noted email threading is still broken; needs stored Message-ID chain + dateless subject "Your DC options." NOT yet addressed. This was mentioned in the method doc as a live signal but no work was done on it during this session.

### Recurring checklist for next autonomous tick

- Poll Mike's inbox (read-only via `_f4_mailcheck.py` or equivalent)
- Roll the 5-day window forward (today was Jun 22 ? window advances to Jun 23-28)
- Research new day (Jun 28, Sunday) that enters the window
- Dedup against existing calendar + Notion DB before writing
- Backfill all researched events (added AND declined) to Notion DB
- Healthchecks heartbeat ping at end of fill
- Re-arm ScheduleWakeup with `<<autonomous-loop-dynamic>>`

---

## EXACT NEXT STEP

The autonomous loop tick at the end of the transcript fired (this is a timer wakeup). The loop instructions say:

> *If a Monitor is armed (check TaskList), keep delaySeconds at 1200-1800s - the Monitor is the wake signal and this is only the fallback heartbeat.*

The next concrete step when the timer fires:
1. **Read new Mike email** - `python C:\claude_base\tools\mike_dc_calendar\_f4_mailcheck.py`
2. **Advance the 5-day window** - today is now ~Jun 22-23; research and fill Jun 28 (Sunday) as it enters the window.
3. **Re-arm the timer** by calling ScheduleWakeup with `<<autonomous-loop-dynamic>>` at the end of the turn.

If there's genuinely no new mail and no gaps in the calendar window, say so in one line and stop.

---

## OPEN QUESTIONS

- **Email threading:** Mike wants a fixed Message-ID chain + dateless subject "Your DC options." Is F4 (Pine) supposed to fix this, or is it Centauri's job (since Centauri sends the digest emails)? The method doc records it as a live signal but doesn't assign ownership.
- **Monitor status:** The loop instructions reference checking TaskList for a Monitor. No Monitor was armed in this session; only the decel timer was set. The autonomous check should treat the timer wakeup as the primary signal.

---

## KEY PATHS & IDs

### Paths
| What | Path |
|------|------|
| Worktree root | `C:\moma\.claude\worktrees\flamboyant-shockley-ec7c00` |
| Base tools | `C:\claude_base\tools\` |
| Calendar method doc | `C:\claude_base\tools\mike_dc_calendar\mike_dc_calendar_method_v01_tomemex.md` |
| DB dump helper | `C:\claude_base\tools\mike_dc_calendar\_db_dump.py` |
| DB backfill helper | `C:\claude_base\tools\mike_dc_calendar\_db_backfill.py` |
| F4's one-shot backfill | `C:\claude_base\tools\mike_dc_calendar\_f4_backfill_20260622.py` |
| F4's mail-check script | `C:\claude_base\tools\mike_dc_calendar\_f4_mailcheck.py` |
| Inbound watcher (Centauri) | `C:\claude_base\tools\mike_dc_calendar\mike_inbound_watch_v01.py` |
| Notion internal token | `zSyncMain\ssh\notion_internal_token_20260319.txt` |
| Worklog | `C:\claude_base\worklog\flamboyant_shockley_ec7c00_ee5970c306.md` |
| Session transcript | `C:\Users\maxre\.claude\projects\C--moma--claude-worktrees-flamboyant-shockley-ec7c00\e0d72196-9b8b-4140-8ae7-fcd65fa51dbd.jsonl` |

### IDs
| What | ID |
|------|-----|
| Notion "Mike DC Events" DB | `40a81164-d856-4fab-8dfa-e93e6f0c7eb4` |
| Notion data source | `collection://d0002c11-ae0f-41b9-9093-e285de035eb5` |
| Google Calendar "Mike in DC" | `2b474b69d0de11e0d46398895550d7b023a5fb58fd26da773e80c3cfea458e6b@group.calendar.google.com` |
| Healthchecks ping URL | `https://hc-ping.com/cd162bbb-59b9-4736-aee3-3ccd4740736b` |
| Google Calendar MCP prefix | `mcp__41c7be2d-b4cd-42ca-830a-f67250dde489__` |
| Notion MCP prefix | `mcp__56b90699-44a5-4951-add8-3e26a5a18809__` |
| bcast identity | ?? f4 |
| Tasklog command | `python C:/claude_base/tools/tasklog/tasklog.py set "..."` |
| Decel timer | `python C:/claude_base/tools/timer_decel/timer_decel.py set <N>` |

### Calendar event IDs (for deletion/modification)
- Folklife Fri: `48kc64v6ouhb0ssve8glb6mt5o`
- Capital Conversations: `oe96c3aep6mjtqnbjdcu6v27s8`
- Folklife Sat: `ht317vbshh5p49qj3lhl4bb8es`
- P&P Thompson: `fcf6540tjmh27hrl03tk5r54mg`
- P&P Levan: `6mujn6urop93nt8804rgo43ds8`
- EA Animal Welfare: `aslrkdb8db34ci3dvqf914il58`
- EA AI Dacha: `22usirimr6oh2b0bo5tore035k`

---

## GOTCHAS

1. **50-event page cap on `list_events`** - the Google Calendar MCP tool silently truncates at 50 events. This caused a false "Jun 26 empty" diagnosis on the first pass. **Always narrow queries to ?3-day windows** and validate that no events were clipped by checking whether the last event in the result is near the end of the window.

2. **Notion MCP tools are plan-gated** - `notion-query-database-view` and `notion-query-data-sources` return plan-gate errors. Don't waste time on them. Use the raw API token path via `_db_dump.py` (read) and `_db_backfill.py` (write) as templates. The token is in `zSyncMain\ssh\notion_internal_token_20260319.txt`.

3. **jq is not installed** - use `python -c` for JSON parsing, not jq.

4. **Email double-ack danger** - `mike_inbound_watch_v01.py` auto-replies to Mike. Running it from both Pine and Centauri would send duplicate replies. F4's `_f4_mailcheck.py` does read-only polling (no reply, no state mutation) to avoid this.

5. **Centauri owns the digest emails** - F4 on Pine should NOT generate or send digest emails. Calendar fill only.

6. **In-person verification is mandatory** - only add to Google Calendar if the event has been verified on the actual registration page. Online-only or invite-only events stay in Notion only.

7. **`notificationLevel=NONE` on all calendar creates** - Mike doesn't want Google
