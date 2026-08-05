# VERBATIM user (Max) log - session dc210eba-7be1-4d4b-9c54-8235bf745b02
# cwd: C:\claude_base\.claude\worktrees\recursing-jemison-10c3c5
# Every line Max typed, saved verbatim, so it survives compaction.
# Recover specs / investigate trouble by reading this file.


## [2026-07-07 00:11:01] turn 85
F40 email-watch loop cycle. Steps:
1. Compute Mike's ET hour H: `PYTHONUTF8=1 python -c "from datetime import datetime; import zoneinfo; print(datetime.now(zoneinfo.ZoneInfo('America/New_York')).hour)"`
2. (A) MIKE inbox â€” MUST use the semantic-mail venv python (plain python fails with ModuleNotFoundError google.auth):
   `cd C:/claude_base/tools/mike_dc_calendar && PYTHONUTF8=1 C:/Users/maxre/semantic-mail/.venv/Scripts/python.exe mike_inbox.py sync`
   On a genuinely NEW Mike id (not on ALREADY-HANDLED list), force-wake f4: `python C:/claude_base/branch_bulletin/bcast.py wake --name f4 "new Mike email respond fast"`. Else stay silent.
3. (B) NON-Mike sweep:
   `PYTHONUTF8=1 C:/Users/maxre/semantic-mail/.venv/Scripts/python.exe C:/claude_base/tools/gmail_grab/gmail_grab.py search "(to:anna@maxrempel.com OR to:mass@tamza.com) newer_than:1d -from:healthchecks.io" 15`
   For any INTERESTING new non-Mike correspondent needing reply/decision NOT already handled â€” summarize to Max and force-wake f4. Ignore Meetup/newsletter/promo (e.g. xAI product newsletters).
4. Re-arm: NIGHT (H>=22 or H<7) -> ScheduleWakeup(3600); DAY (7-21) -> ScheduleWakeup(1800), with this same prompt.
HARD RULE: F40 NEVER auto-replies; f4/Anna is sole email answerer + calendar/Notion writer.
On "go sleep": run `PYTHONUTF8=1 python C:/claude_base/tools/timer_decel/timer_decel.py off` and stop re-arming.
ALREADY-HANDLED (do NOT re-wake f4 for these ids even if mike_inbox lists them UNHANDLED; only wake for a genuinely NEW Mike message id): 6/30 15:44; 7/1 12:09; 7/1 12:10; 7/1 13:50 x2; plus the 3 Mike msgs that arrived over 7/2-7/5 (already handled, 167 total mirrored, 0 unhandled). NON-Mike: marzieh razavizadeh REMINDER 7/6 already flagged+f4 woken; Kristen K 'inversion question' 7/5 is X-team/genomics lane not f4; xAI 'Voice Agent Builder' 7/7 = promo ignored; do not re-flag unless brand-new.
