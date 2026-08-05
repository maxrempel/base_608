# Adviser note - milestone 2 (~166K tokens)
# session: 20260626_focused_ride_1f38f1_856ff2ef
# written: 2026-06-26 16:41:52 by deepseek-v4-pro

TO ASSISTANT: You burned 6+ turns on PowerShell parameter binding for one script. That's a death spiral. When `Get-Command` says one param set but the binder says ambiguous and you've rewired the file twice, you should jump to Python (or any other approach) at attempt #2, not #6. Max's time and context window matter more than proving PowerShell diagnosis skills.

TO ASSISTANT: The earlier `scp` copy finished. You have 12 GB sitting on teal16 that was placed outside the rclone/Python system. The Python migrate script may handle this via rclone reconcile, but you should explicitly confirm there's no leftover scp state (wrong path, wrong permissions, duplicate files) confusing things before you delete anything from C:. Don't assume the reconcile caught it.

TO MAX: No action needed yet. The Assistant built a working Python copy-verifier and is currently running it against the 00_KEEP folder with --no-delete (safe). But you lost ~6 turns to a PowerShell debugging hole, and there's a potential mess from the abandoned scp transfer - the Assistant needs to clean that up before any files get deleted from your C: drive.
