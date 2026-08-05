# Scribe handover - milestone 12 (~180K tokens)
# session: 20260617_sweet_kepler_a528fd_d0a8f775
# cwd: C:\claude_base\.claude\worktrees\sweet-kepler-a528fd
# written: 2026-06-17 11:45:47 by deepseek-v4-pro

# HANDOVER - Mike DC Calendar Autopilot & Email Loop

---

## GOAL (in Max's words)

Max asked me to:
1. **Investigate** whether Mike's DC calendar was properly filled and QC its quality - suspected a rogue agent.
2. **Fix** whatever was broken: housekeeping, refill, Notion sync, autopilot mechanism.
3. **Start a direct email conversation with Mike** (from mass@tamza.com) to ask what topics/platforms he actually wants, then poll his replies on a flexible cadence and bake his preferences into the autopilot permanently.

Mike's verbatim feedback (relayed by Max):
> *"Make it search through all events, not just tech, it keeps only giving me tech. And to put in more open hearings from House and Senate and prioritize most think tank events. Also, if there is anything for complete certain, that is 21 plus then likely don't add."*

---

## DECISIONS MADE + WHY

### Root cause of the dead calendar
The prior autopilot used a `ScheduleWakeup` cron set to every 6 hours - but crons are **per-session** and silently do not fire across sessions. The session that created it ended, the cron went dormant, and the calendar froze at **Jun 7** for 10 days. **Decision:** Replace the broken 6h cron with a **daily self-wake** (the `wakeup.py add --every daily` mechanism) that re-fires in whatever session is live. This kind of timer actually works across compactions.

### Autopilot architecture
A single daily wakeup (09:00) that re-wakes the live session, runs the full fill for the next 5 days, and self-terminates after **Jul 31** (Mike's trip end). The wake carries all of Mike's standing preferences baked into its prompt message so every run obeys them without manual re-telling.

### Mike's four standing preferences (now permanent rules)
1. **Balance all 9 topics, de-weight tech** - the calendar was skewing heavily startup/tech; the autopilot now actively balances across Effective Altruism/AI-safety, foreign policy, economics, tech, academic, activism/civic, ecology, culture, and AI policy.
2. **More open House + Senate hearings** - sweeps congress.gov each run.
3. **Prioritize think-tank events** - CSIS, Brookings, AEI, Carnegie, Wilson, Cato, Heritage, Hudson ranked high.
4. **Skip 21+/age-restricted events** - reading this as Mike being under 21 / unable to enter bar venues. **This interpretation was sent to Mike for confirmation but he hasn't replied yet.**

### Email polling cadence
You specified: baseline **60 minutes** while Mike is away ? when he replies, accelerate to **7 min ? 7 min ? 20 min**, then settle back to 60 min if quiet. Any new reply resets the ladder to the top.

### Notion DB sync strategy
Calendar is the source of truth; each daily run backfills the Notion "Mike DC Events" DB. The agent creates rows with Format=In-person, verified-date noted, dedupes against existing rows by date. The two HacDC rows on different dates (Jun 25, Jul 9) were correctly left as-is.

---

## CURRENT STATE

### Calendar (live)
- **2 duplicate pairs removed** (Civic Tech DC Project Night x2 on Jun 24; Jesse Wegman P&P x2 on Jun 24).
- **5 new events added** for Jun 17-22 (Incorruptible AI governance walk in Tysons, CROWDFUEL founders networking in McLean, HacDC hardware hacking night, Joanna Stern AI author talk at P&P, Phill Branch author talk at P&P). All verified in-person, with registration links, transit from Shady Grove, dress code, street address, and `notificationLevel=NONE`.
- **4 events added per Mike's rules** (by agent): 3 open Senate hearings + 1 CSIS panel - no tech, none 21+.
- Total: ~97-99 events Jun 17-Jul 28, all topics represented including EA.

### Autopilot
- **Daily wake armed:** ID `44823c93`, fires every 86400s at 09:00, carries Mike's full four preferences in the message body. Self-terminates after Jul 31.
- **Method doc updated:** `C:\claude_base\tools\mike_dc_calendar\mike_dc_calendar_method_v01_tomemex.md` - broken-cron lesson recorded, new daily self-wake mechanism documented, Mike's standing preferences codified. Committed + pushed.

### Notion DB
- In sync: all 5 new events created as rows, 0 failures, correct dedup.

### Email thread with Mike
- **Opening email sent** from mass@tamza.com to mikerempel3@gmail.com (Bcc'd to Max). It explained the current 9-topic sweep and asked what he wants changed.
- **Acknowledgment email sent** after Max relayed Mike's preferences - confirmed all four changes, asked for clarification on the "21+" meaning.
- **Mike has NOT replied directly** to the email thread (his prefs came through Max). No new messages from Mike in the mass@tamza.com inbox as of the last poll.
- **Poll loop armed:** baseline 60 min. Next fire will re-check.

### Git
- Method doc committed + pushed to master.
- `mass_inbox_poll.py` committed + pushed.

---

## EXACT NEXT STEP

The poll loop will fire next at its scheduled 60-min interval. When it fires, the prompt tells the cold session exactly what to do:

**If Mike has a NEW reply:**
1. Read it.
2. Send a warm assistant-voice reply via `mxmail_v01.send_mail` (to mikerempel3@gmail.com, auto-bccs Max).
3. Apply any new concrete preferences to:
   - The daily wake message (cancel `44823c93`, re-arm with updated prefs).
   - The method doc `C:\claude_base\tools\mike_dc_calendar\mike_dc_calendar_method_v01_tomemex.md`.
4. Re-arm the poll at 420s (7 min), laddering to 420s ? 1200s ? 3600s.

**If NO new reply:**
Re-arm at 3600s (60 min). Nothing else needed.

**Stop the loop entirely only if Max says to stop.**

The daily autopilot fires independently at 09:00 - it will run the full 5-day fill sweep with Mike's prefs baked in, no manual trigger needed.

---

## OPEN QUESTIONS AWAITING MIKE

1. **"21+" clarification:** Max and I interpreted this as age-restricted venues (Mike being under 21 / can't enter bars). Mike was asked in the second email to correct this if he meant something else (e.g., events with a 21-person cap, or something else entirely). He has not confirmed. The rule is active but soft - don't hard-enforce until he replies.

---

## KEY PATHS, IDs, COMMANDS

| What | Path / ID |
|---|---|
| Worktree | `C:\claude_base\.claude\worktrees\sweet-kepler-a528fd` |
| Method doc | `C:\claude_base\tools\mike_dc_calendar\mike_dc_calendar_method_v01_tomemex.md` |
| MX mail module | `C:\claude_base\tools\mxmail\mxmail_v01.py` (function: `send_mail`) |
| Inbox poll script | `C:\claude_base\tools\mxmail\mass_inbox_poll.py` |
| Wake listener | `C:\claude_base\tools\wake_listener\wakeup.py` |
| Worklog | `C:\claude_base\compaction_kb\scripts\worklog.py` |
| Session status | `C:\claude_base\compaction_kb\scripts\session_status.py` |
| Daily wake ID | **`44823c93`** (09:00, every 86400s, Mike's full prefs, expires after Jul 31) |
| Mike's email | `mikerempel3@gmail.com` |
| Sending address | `mass@tamza.com` |
| Poll --from filter | `--from mikerempel3@gmail.com --since "17-Jun-2026"` |

### Poll command (copy-paste ready)
```
python C:/claude_base/tools/mxmail/mass_inbox_poll.py --from mikerempel3@gmail.com --since "17-Jun-2026"
```

### Send-mail pattern (in Python)
```python
import sys; sys.path.insert(0, r"C:\claude_base\tools\mxmail")
from mxmail_v01 import send_mail
send_mail(to_email="mikerempel3@gmail.com", subject="Re: ...", body="...")
# Auto-Bcc's Max; no extra CC needed
```

### Wake management
```bash
python C:/claude_base/tools/wake_listener/wakeup.py list          # check armed wakes
python C:/claude_base/tools/wake_listener/wakeup.py cancel <id>   # remove old
python C:/claude_base/tools/wake_listener/wakeup.py add --at "2026-06-18 09:00" --every daily --msg "..."  # arm new
```

---

## GOTCHAS & DEAD ENDS

1. **Do NOT use ScheduleWakeup crons for long-term recurring work.** Crons are session-scoped and silently die when the creating session ends. The fix is `wakeup.py add --every daily`, which uses a durable timer that re-wakes whichever session is live. This was the root cause of the 10-day calendar freeze.

2. **Do NOT use Online/invite-only/press-only events.** The calendar gets ONLY verified in-person, public-attendable events. Online or restricted events are logged in the Notion DB with a rejection reason but never placed on the calendar. Mike is in DC physically and needs events he can walk into.

3. **notificationLevel must be NONE** on all calendar creates/updates. Mike and Oksana share the calendar; spamming them with notifications is forbidden.

4. **Every event carries:** registration link, transit from Shady Grove (Mike's Metro station), dress code, physical street address.

5. **The 5-day rolling window** means each daily run fills the next 5 days only. DC orgs publish ~2-4 weeks out, so daily re-sweeps catch newly published events. Events beyond the window are left stale until they roll into range.

6. **EA/AI-safety lane can legitimately return nothing** in a given 5-day window - that's saturation, not a miss. Don't force-add weak events to fill a quota.

7. **The poll loop prompt is self-replicating.** Each time ScheduleWakeup fires, it wakes the session with the full poll-loop instructions. The cold session should execute the poll, decide (reply vs. no reply), send email if needed, re-arm at the correct cadence rung, and pass the same prompt forward. Don't alter the prompt structure unless Max says to.

8. **Mike's prefs are in the waking message of wake `44823c93`.** If you need to change his prefs, cancel that wake and re-arm with the updated message - do NOT try to edit a wake in-place (there's no edit command).

9. **The "21+" rule is unconfirmed.** Don't hard-enforce it as a database constraint until Mike replies. Currently it's a soft filter in the autopilot prompt.

10. **Git always push after doc changes.** The method doc is in `C:\claude_base` (master). Any edits must be committed and pushed. The `mass_inbox_poll.py` is also tracked there.
