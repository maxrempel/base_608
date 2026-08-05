# Scribe handover - milestone 2 (~170K tokens)
# session: 20260626_strange_poitras_35a1c8_3cea7873
# cwd: C:\moma\.claude\worktrees\strange-poitras-35a1c8
# written: 2026-06-26 07:26:25 by deepseek-v4-pro

## HANDOVER - Mike-DC Calendar (F4 / Anna on Pine)

---

### GOAL (Max's words)
"Take over from F1 the updates of Mike's calendar." Run twice-daily (7am and 4pm Pacific) research-and-fill of Mike's "Mike in DC" Google Calendar. F4 = "Anna" = the **sole** session contacting Mike now - reads his email, replies concisely, fills the calendar. No unsolicited daily summaries/reminders. The fill must run **headless** (WebSearch/WebFetch only - never a browser, because a browser steals keyboard/dictation focus). Must wake up and **catch up missed runs** when the computer comes back on. Mike's standing topic requests: EA (#1), Buddhist social/meditation+dinner/temple events, HacDC hackerspace, CivicTech DC, Flamingo-color all Hearings + P&P talks, verify start times, flag outside-central-DC events by city tag.

---

### DECISIONS MADE + WHY

1. **Architecture split (Max-corrected):** Calendar fills = F4 on Pine. Email digests = Centauri. Then Max overrode it: Centauri sends NOTHING (Mike declined reminders). F4/Anna is now sole Mike contact - reads AND answers his email. Prompt enforces "reply only when Mike writes, no unsolicited mail."

2. **Windows Task Scheduler as the resilient layer:** `wakeup.py` recurring wakes only fire when an f4 chat is alive - that caused a ~41h heartbeat lapse (Jun22?24). Root cause: chat closed while Pine was on. Fix: Windows Task `MikeDC-Fill` with `StartWhenAvailable=ON` - fires with no chat open, catches up missed runs on boot. Proven: overnight 06:58 catch-up ran 454s, added 10 events. Backstop `wakeup.py` morning wake (2534a386) now cancelled; afternoon (55aecd1c) kept until 16:00 Task slot proves out today.

3. **Command-based gcal MCP (C16 built, commit c9e738bd):** The old account-level claude.ai desktop connector (41c7be2d) is invisible to `claude -p` headless. C16 built a stdio MCP at `C:/claude_base/tools/mcp-google-calendar/main.py` that loads headless, same tool names. Takes the newest `google_calendar_oauth_token_*.json` from the ssh folder at startup.

4. **OAuth token (minted this session):** `google_calendar_oauth_token_20260625.json` - refresh_token present, calendar scope. Minted via `_f4_gcal_oauth_bootstrap.py` (one-time browser consent, now done - no more browser). GCP prereqs cleared: consent screen already "In production," Calendar API enabled.

5. **Prompt piped via stdin, not argv:** Windows `.cmd` batch parsing truncates multi-line args at the first newline ? headless claude only saw the first line and asked "what should I do?" (20s exit, no fill). Fixed in `resilient_run.py`: `subprocess.run(..., input=prompt)`. Verified with BANANA test. Committed + pushed.

6. **HacDC/CivicTech dedup by group+date, not exact title:** Older suffix-format tags ("Open Hac (HacDC open night)") weren't matching the new prefix format ("(HacDC) Open Hac"). Prompt now says: treat same group + same date/time as duplicate, keep the prefix form Mike asked for.

7. **Task has 5 daily triggers - causing budget waste:** A redundant 07:15 run burned ~$5 reaching the budget cap doing nothing (the 06:58 catch-up already filled). Mike only needs 1 good fill/day. **Decision pending Max:** trim to 2 triggers/day?

---

### CURRENT STATE
- **Calendar:** 51 events on Mike-in-DC covering Jun 26-Jul 12. All Hearings + P&P Flamingo (colorId=4). 6 Buddhist events, 4 (HacDC) events, 2 EA events (Animal Welfare Jun25, Dacha AI Jun30). CivicTech currently empty for next 2 weeks.
- **Inbox:** Clean - all 4 recent Mike messages (CivicTech, HacDC, Buddhist request, "are you getting these") already actioned + replied to by the 06:58 Task fill.
- **Healthchecks:** heartbeat cd162bbb last pinged GREEN by the 06:58 fill.
- **Durable Task:** Registered as `MikeDC-Fill` with StartWhenAvailable. 5 daily triggers (07:15/10:15/13:15/16:15/18:45 PT) plus boot catch-up. The 06:58 catch-up proved the chain works; the 07:15 scheduled slot redundantly fired and hit the $5 budget cap (exit 1, no fill, $ wasted).
- **Backstops:** `wakeup.py` 2534a386 (morning) CANCELLED. 55aecd1c (afternoon 16:00) still armed - keep until the 16:00 Task slot proves out.
- **Centauri:** Force-woken to CANCEL the live digest sends `20463c74` + `1e13feca` (not the already-dead `54c968f1/20c3b82e` I originally named). Awaiting its confirm. Mike must get zero unsolicited mail.
- **Hourly daytime timer:** Re-armed for ~09:17 PT (lightweight in-chat check - reads inbox, verifies fill, no $5 spawn).

---

### EXACT NEXT STEP
1. On next hourly wake (~09:17 PT): read Mike's inbox (`python _f4_mailcheck.py 3`), reply ONLY if a new unanswered request exists.
2. Verify Centauri confirmed digest cancellation (fleetcomm read). If not confirmed before 16:00 PT, escalate.
3. Let the 16:00 Task slot fire and verify it succeeded. If yes: **cancel the afternoon backstop 55aecd1c** (single clean mechanism). If it fails: diagnose, keep backstop.
4. **Ask Max:** trim `MikeDC-Fill` Task from 5 triggers/day to 2 (morning + afternoon) to stop ~$15-20/day of wasted runs at $5/run. The boot catch-up already covers missed slots.
5. Drop the old `wakeup.py` backstops list entirely once the Task proves out on afternoon cycle.

---

### OPEN QUESTIONS AWAITING MAX
1. **Trim Task to 2 triggers/day?** The 5 daily slots waste ~$15-20/day on runs that hit the budget cap doing nothing (boot catch-up already covers the real fill). One good fill/day covers Mike.
2. **Notion dedup** - blank-Format Admiral row (page_id `37a0316f-5560-8152-8920-eb2a5977a1ce`) duplicates the In-person one (`36c0316f-5560-8152-8fbc-d8327f18051c`). Delete the blank one?
3. **Outside-DC events get their own calendar color?** Currently flagged by city suffix only (e.g. "(McLean)"). Mike might want visual grouping like the Flamingo trick.

---

### KEY PATHS / IDs

| What | Value |
|---|---|
| **f4 worktree** | `C:/moma/.claude/worktrees/flamboyant-shockley-ec7c00` |
| **Windows Task** | `MikeDC-Fill` (5 triggers, StartWhenAvailable) |
| **Runner** | `C:/claude_base/tools/resilient_job/resilient_run.py` (prompt via stdin, not argv) |
| **Registration** | `C:/claude_base/tools/resilient_job/register_resilient_job.ps1` |
| **Task logs** | `C:/claude_base/tools/resilient_job/logs/MikeDC-Fill_*.log` |
| **Fill prompt** | `C:/claude_base/tools/mike_dc_calendar/mike_dc_fill_prompt_v01.md` |
| **Method doc** | `C:/claude_base/tools/mike_dc_calendar/mike_dc_calendar_method_v01_tomemex.md` |
| **Inbox reader** | `C:/claude_base/tools/mike_dc_calendar/_f4_mailcheck.py` (read-only IMAP) |
| **OAuth bootstrap** | `C:/claude_base/tools/mike_dc_calendar/_f4_gcal_oauth_bootstrap.py` (one-time, already run) |
| **OAuth token** | `C:\Users\maxre\Nextcloud\zSyncMain\ssh\google_calendar_oauth_token_20260625.json` |
| **OAuth client** | `C:\Users\maxre\Nextcloud\zSyncMain\ssh\google_contacts_oauth_20260522.json` (project `stalwart-coast-240620`) |
| **gcal MCP** | `C:/claude_base/tools/mcp-google-calendar/main.py` (C16, commit c9e738bd) |
| **Google Calendar ID** | `2b474b69d0de11e0d46398895550d7b023a5fb58fd26da773e80c3cfea458e6b@group.calendar.google.com` (tz America/New_York) |
| **Notion DB** | `40a81164-d856-4fab-8dfa-e93e6f0c7eb4` |
| **Notion token** | `C:\Users\maxre\Nextcloud\zSyncMain\ssh\notion_internal_token_20260319.txt` |
| **Healthchecks** | `https://hc-ping.com/cd162bbb-59b9-4736-aee3-3ccd4740736b` |
| **mxmail** | `C:/claude_base/tools/mxmail/mxmail_v01.py` (sender: mass@tamza.com, auto-bcc max.rempel2@gmail.com, auto-signs "Anna") |
| **Mike's email** | `mikerempel3@gmail.com` ? writes to `mass@tamza.com` |
| **IMAP** | HOST `witcher.mxrouting.net:993`, USER `mass@tamza.com`, PW `M4ss-Tamza-Send-2026=Kq9w` |
| **wakeup.py backstops** | 2534a386 (CANCELLED), 55aecd1c (armed, @16:00 PT daily) |
| **Centauri digest wakes** | `20463c74` (morning) + `1e13feca` (evening) - need cancellation |
| **bcast** | `python C:/claude_base/branch_bulletin/bcast.py post --as f4 "..."` / `wake --name <id> --as f4 "..."` |
| **fleetcomm** | `python C:/claude_base/tools/fleetcomm/fleetcomm.py post "..." --session f4` |
| **worklog** | `python C:/claude_base/compaction_kb/scripts/worklog.py log "DID" "STATE" "NEXT"` |
| **gcal verify py** | Use `C:/claude_base/tools/mcp-google-contacts/.venv/Scripts/python.exe` (has google libs) |
| **Pine off-window** | ~7pm-7am Pacific |
| **Mike-in-DC calendar color rules** | Hearing + P&P = Flamingo (colorId=4); EA = various; outside-DC flagged by city suffix only |

---

### GOTCHAS
- **Never open a browser in headless fills** - the fill prompt now has a HARD RULE: research = WebSearch/WebFetch ONLY. All browser/GUI tools forbidden.
- **Never double-reply to Mike** - the headless fill already sends concise results replies. The in-chat hourly check must only reply if the inbox has a NEW unanswered message.
- **Task double-fires:** boot catch-up + scheduled slots can overlap. The 06:58 catch-up ran, then 07:15 scheduled slot redundantly fired and burned $5. The prompt/logic doesn't prevent this - it's a trigger-count problem, not a runner bug.
- **gcal MCP token caching:** The MCP resolves the token file ONCE at startup. A session started before the token landed caches `None`. Fresh processes (the Task) are fine.
- **Prompt truncation was fixed** but keep in mind: any new headless runner must pipe the prompt via stdin, never pass on argv under Windows `.cmd`.
- **Centauri digest cancellation** needs verification - wrong IDs (`54c968f1/20c3b82e`) were already cancelled; the live ones are `20463c74` + `1e13feca`. If Centauri doesn't confirm, Mike could get an unwanted digest at 16:00 PT today.
- **HacDC/CivicTech dedup** must match by group+date, not exact title - old suffix-format tags exist and won't match the new prefix format.
- **Suicide-prevention hook** blocks identical Bash command 3+ times. Vary the approach or read underlying files directly.
- **Signature:** Every reply leads with `?? f4 ?`. Be terse (Max: "I cannot read that much"). Don't ask permission - check state and act.
