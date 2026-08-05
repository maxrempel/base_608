# Adviser note - milestone 6 (~92K tokens)
# session: 20260612_vigilant_carson_ffce68_be212fff
# written: 2026-06-12 15:47:22 by claude-opus-4-8

TO ASSISTANT:
Undo means undo, in the right order. The repo is half-migrated but NOT broken, so be careful not to make it worse. Steps: (1) Restore settings.json from the backup (settings.json.bak_watchlog_rename_20260612) NOT by re-editing -- but first note that another session added a statusLine since your backup, so a raw restore will lose that addition. Safer: edit settings.json to revert the 5 watchlog/scripts paths back to compaction_kb/scripts, preserving the new statusLine, then re-validate JSON. (2) git mv watchlog compaction_kb to reverse the folder rename. (3) Confirm git status shows only the rename reversed and no stray staging. (4) Re-validate settings.json parses and confirm the path now points at a folder that exists. Report back the exact state before doing anything else. Do not commit, do not push.

TO MAX:
You said "undo" -- heads up on one wrinkle: while the session held settings.json, ANOTHER live session added a statusLine entry to it. A naive restore-from-backup would clobber that. The assistant should hand-revert the paths instead of overwriting the file. Also worth deciding: do you want a clean full undo, or just to pause? The work so far was actually careful (backup taken, JSON validated, dirty repo respected, caught the 5th ref). Nothing is broken right now. If you only meant "stop," a full undo may be wasted churn -- clarify.
