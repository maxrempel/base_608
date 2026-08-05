# Scribe handover - milestone 5 (~88K tokens)
# session: 20260617_agitated_austin_f89ae3_aa23f003
# cwd: C:\claude_base\.claude\worktrees\agitated-austin-f89ae3
# written: 2026-06-17 08:11:47 by deepseek-v4-pro

**GOAL** (in Max's own words)  
- Original: "setup periodic email check of the mass@t mailbox, so you come to me with news ... every hour."  
- Last request: **"Set it up for 20 min now. It must use the tool for waking up that is long term. We just created it yesteday, i forgot the name."**

**DECISIONS + WHY**  
1. **Built a new read?only IMAP digest (`mass_check_v01.py`)** because the existing `mxmail_v01.py` only sends; IMAP was required, and credentials for `mass@tamza` already existed.  
2. **Read?only mode** - the script opens the INBOX with `(READ-ONLY)` to avoid marking messages as seen, keeping the mailbox untouched for any other client.  
3. **Skip noise** - filters out Healthchecks.io monitoring pings and common marketing/deletable junk so only real human or transactional mails are surfaced.  
4. **Wake mechanism** - used the long?term wake?up tool (`C:\claude_base\tools\wake_listener\wakeup.py`) because the user explicitly wants a true background timer that wakes the session, not an in?process sleep loop.  
5. **Hourly schedule** was added with `wakeup.py add --in "1 hour" ...` after confirming `hourly` as a valid interval choice.  
6. **Now must switch to 20 minutes** - the user's last instruction trumps the earlier hourly, and they explicitly want the same long?term wake?up tool they just forgot the name of.

**CURRENT STATE**  
- The `mass_check` tool is tested against the real inbox (101 messages in 7?days), working correctly.  
- An **hourly** wake?up job is registered in the long?term timer's database. From the earlier run: the job ID was likely `1` and was scheduled to fire at ~09:05 (session time).  
- The **20?minute change has NOT been applied yet** - the assistant received the request but the transcript ends before any action.  
- The tool files are committed to the `agitated-austin-f89ae3` worktree and pushed.

**EXACT NEXT STEP (for a cold, resumed session)**  
1. **Remove the existing hourly wake?up job.**  
   - Command: `python C:/claude_base/tools/wake_listener/wakeup.py remove 1` (replace `1` with the actual job ID if different; first run `wakeup.py list` to confirm).  
2. **Add a new wake?up job that fires every 20?minutes.**  
   - First, check if the wake?up tool supports arbitrary intervals or only predefined choices (hourly/daily/weekly). The known choices from the source show `hourly, daily, weekly`. It may also accept raw `--every 20m` or `--every 1200` (seconds) - need to inspect `wakeup.py` help or source, or try `--in "20 minutes"` for a one?shot and then use a recurring flag.  
   - Likely correct syntax (to be confirmed):  
     `python C:/claude_base/tools/wake_listener/wakeup.py add --every "20 minutes" --msg "MASS@TAMZA 20MIN CHECK: ..."`  
     If `--every` only supports the three named intervals, you'll need to fall back to a **one?shot rescheduling trick** (chain the mass?check to re?add another one?shot 20?min later) or modify the wake?up code.  
   - The message must contain the exact invocation: `PYTHONIOENCODING=utf-8 python C:/claude_base/tools/mass_check/mass_check_v01.py --hours 1` (or whatever window you want). Do **not** include `--hours 168` for a short check; likely 1?hour is fine.  
3. **Verify** the job is in the list and note the next fire time.  
4. **Test** a manual trigger or wait for the first fire, then confirm the assistant reads and reports news.  
5. **Commit** any changes (if the wake?up command change is just a schedule update, no code changes needed - but you might want to document the new interval in the `mass_check_v01_tomemex.md` or a note).

**OPEN QUESTIONS (awaiting Max)**  
- Does the long?term timer support arbitrary minutely intervals, or must we implement a "re?schedule" loop? The user expects a 20?minute repeat, not an ad?hoc one?off. This will likely require checking `wakeup.py --help` and the source; if only named intervals, propose a fix or workaround.  
- What is the preferred window for inbox scanning (`--hours 1` is sensible; confirm).  
- Should the 20?minute check keep the same spam filter (skip Healthchecks) or expand? The user said "once it is in place, we will expand" - that expansion hasn't been defined.

**KEY PATHS & IDs**  
- Long?term wake?up tool: `C:\claude_base\tools\wake_listener\wakeup.py`  
- Mass?check script: `C:\claude_base\tools\mass_check\mass_check_v01.py`  
- Mass?check method doc: `C:\claude_base\tools\mass_check\mass_check_v01_tomemex.md`  
- IMAP credentials: `C:/Users/maxre/Nextcloud/zSyncMain/ssh/mxroute_creds` (or similar; the actual credential file is loaded by the script parsing `mass@tamza` credentials)  
- Git worktree: `C:\claude_base\.claude\worktrees\agitated-austin-f89ae3` (claude_base root)  
- Wake?up DB: stored internally by `wakeup.py` (likely SQLite in the same directory or user?specific location; inspect the source for path).

**GOTCHAS & DEAD ENDS ALREADY RULED OUT**  
- **Read?only needed** - already handled; do not change to a mode that marks seen.  
- **mxmail can't read** - ruled out, hence the new script.  
- **Session must be alive** - the wake?up timer fires only when a Claude session is running in this worktree; the user knows this. If they want fully unattended cross?machine, an OS scheduler is required. That is not a dead end but a known limitation.  
- **Spam filter is crude** - currently skips Healthchecks and some generic marketing. If inbox content changes a lot, the filter may need updates; user acknowledged it will be expanded later.  
- **Do NOT re?use the hourly job** - the explicit request is 20 min, so ensure you replace the old schedule, not just add a second one.
