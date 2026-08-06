# Continuous thread-label watcher (2026-08-06)

Problem: the Codex thread model labeler existed but only ran when a session
remembered the one-time manual command, so today's new tasks (including the
requesting session) were never stamped.

Solution: hidden scheduled task `CodexThreadLabelWatcher` runs
`label_threads.py apply --log` every 5 minutes under `pythonw.exe` (no console
window), logs to `C:\Users\maxre\.codex\logs\thread_label_watcher.log`, and
creates a backup + undo manifest for every real change. Idempotent no-op runs
write one log line.

Files (canonical copy committed in C:\claude_base, mirrored to C:\base_608):
- `tools/codex_backend/label_threads.py` (new `apply --log` quiet mode)
- `tools/codex_backend/install_thread_label_watcher.ps1`
- README updated in both repos; shared global rules updated (Nextcloud source
  + `~/.codex/AGENTS.md`) so sessions know labeling is automatic.

Verified 2026-08-06 13:18 PDT: installer ran, labeled the 3 untagged threads
(backup run_20260806-131832), task LastTaskResult 0, status shows 0 untagged
out of 228 threads. Reinstall anytime with:
`powershell -ExecutionPolicy Bypass -File C:\claude_base\tools\codex_backend\install_thread_label_watcher.ps1`
