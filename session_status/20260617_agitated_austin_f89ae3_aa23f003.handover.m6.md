# Scribe handover - milestone 6 (~90K tokens)
# session: 20260617_agitated_austin_f89ae3_aa23f003
# cwd: C:\claude_base\.claude\worktrees\agitated-austin-f89ae3
# written: 2026-06-17 08:11:50 by deepseek-v4-pro

# HANDOVER: Mass@Tamza Periodic Inbox Check

---

## GOAL (in Max's words)
"Setup periodic email check of the mass@t mailbox, so you come to me with news. Right now it is minimal, but once it is in place, we will expand. We now have long term wake up timer, that's exactly what is needed, say every hour." - later revised to 20-minute intervals.

---

## DECISIONS + WHY

1. **Built a new IMAP reader** (`mass_check_v01.py`) rather than extending `mxmail`. Reason: `mxmail` (at `tools/mxmail/`) is SMTP-only - it can send but has no IMAP fetch capability. Building a separate read-only tool was cleaner than bolting IMAP into a send tool.

2. **Read-only IMAP - no side effects.** The script connects via IMAP, searches unseen messages, but does NOT mark them read or delete anything. Keeps the inbox pristine.

3. **Filtering out noise.** The script skips known noise senders: Healthchecks.io status pings and marketing cruft that currently dominate the inbox (101 messages in 7 days, mostly junk).

4. **Credential source:** `C:\Users\maxre\Nextcloud\zSyncMain\ssh\` - IMAP creds for mass@tamza were found here alongside the existing SMTP creds used by `mxmail`.

5. **Wakeup tool used:** The `wakeup.py` script at `tools/wake_listener/` - this is the long-term wakeup timer Max mentioned creating the day before. It supports `--in`, `--every`, `--msg`, and `hourly`/`daily`/`weekly` intervals.

6. **Interval change: hourly ? 20 minutes.** The hourly wake (ID `966aafb9`) was cancelled and replaced with a 20-minute recurring wake. Reader window narrowed to ~24 minutes (matching the cadence) to avoid repeating messages.

---

## CURRENT STATE

### What's built and working:
- **`C:\claude_base\tools\mass_check\mass_check_v01.py`** - IMAP inbox reader, tested live. Connects to mass@tamza, fetches recent unseen messages, filters noise, prints plain-English summaries.
- **`C:\claude_base\tools\mass_check\mass_check_v01_tomemex.md`** - Method doc for the tool.
- **Recurring wake scheduled:** 20-minute interval, message triggers `mass_check_v01.py`. First fire was ~08:31. Cancelled old hourly wake (ID `966aafb9`).
- **Committed and pushed** - everything is in git.

### What's NOT done / limitations:
- The wakeup only fires while a **session is alive in this worktree**. It cannot wake a sleeping machine or fire across reboots.
- OS-level scheduler (Task Scheduler) has NOT been set up - this is purely within Claude Code's wakeup infrastructure.

---

## EXACT NEXT STEP

**Nothing pending** from the transcript - the system is live and running at 20-minute intervals. The last exchange was Max noting that the laptop goes to sleep, and Claude acknowledged the limitation (session must be alive).

If a cold session picks this up:

1. **Check if the wake is still active:**
   ```
   python C:/claude_base/tools/wake_listener/wakeup.py list
   ```
2. **Test the reader manually:**
   ```
   cd C:/claude_base/tools/mass_check && PYTHONIOENCODING=utf-8 python mass_check_v01.py --hours 1
   ```
3. **If Max wants true unattended operation:** discuss OS-level scheduling (Windows Task Scheduler) to complement the in-session wakeup, potentially with a companion script that fires `mass_check_v01.py` on a cron-like schedule regardless of whether a Claude session is alive.

---

## OPEN QUESTIONS (awaiting Max)

1. **Sleep resilience:** Max said: "I use this laptop, but put it asleep when not used. The tool is resistant to that." - he's pointing out that the laptop sleeps and wants assurance the tool handles it. The answer: the wakeup timer fires *while the session is alive*, but if the machine sleeps, the session pauses too. True cross-sleep coverage needs an OS-level scheduled task. This was acknowledged but not yet resolved to Max's satisfaction.

2. **Expansion:** Max said "once it is in place, we will expand." What expansion? Better filtering? Alerts for specific senders/subjects? Auto-replies? This was left open-ended.

3. **What "news" means:** Currently the tool surfaces anything that isn't Healthchecks.io or known marketing. Max hasn't yet defined what specific content or senders he cares about.

---

## KEY PATHS, IDS, COMMANDS

| What | Path/Value |
|---|---|
| IMAP reader script | `C:\claude_base\tools\mass_check\mass_check_v01.py` |
| Method doc | `C:\claude_base\tools\mass_check\mass_check_v01_tomemex.md` |
| Wakeup tool | `C:\claude_base\tools\wake_listener\wakeup.py` |
| Wakeup method doc | `C:\claude_base\tools\wake_listener\wakeup_method_v01_tomemex.md` |
| SMTP send tool (not used here) | `C:\claude_base\tools\mxmail\mxmail_v01.py` |
| IMAP creds location | `C:\Users\maxre\Nextcloud\zSyncMain\ssh\` (contains mxroute IMAP creds for mass@tamza) |
| Mailbox | mass@tamza (IMAP via mxroute) |
| Cancelled wake ID | `966aafb9` |
| Current interval | 20 minutes |
| Wake message payload | Runs: `PYTHONIOENCODING=utf-8 python C:/claude_base/tools/mass_check/mass_check_v01.py --hours 0.4` |
| Worktree | `C:\claude_base\.claude\worktrees\agitated-austin-f89ae3` |

---

## GOTCHAS + DEAD ENDS RULED OUT

1. **mxmail can't read** - it's SMTP-only. Don't try to extend it for IMAP; the separate `mass_check` tool is the right pattern.

2. **IMAP credentials exist** - found at the Nextcloud ssh folder alongside SMTP creds. No need to hunt further.

3. **Python encoding** - must set `PYTHONIOENCODING=utf-8` or output can garble on Windows.

4. **Window sizing matters** - with a 20-minute interval, the `--hours 0.4` (~24 min) gives just enough overlap to catch everything without excessive duplicates. If the interval changes, the window should adjust proportionally.

5. **Tool is read-only by design** - doesn't mark messages seen, doesn't delete, doesn't move. If future expansion needs "mark as read" or "archive after processing," that's a deliberate change to make, not a bug.

6. **Wakeup tool is session-bound** - this is NOT a system service. Machine sleep pauses it. The user seems to expect it tolerates sleep (perhaps they think the timer compensates on wake), but that needs clarification.
