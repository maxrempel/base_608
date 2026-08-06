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

## Second pass (same day, ~14:17 PDT): stop fighting the app's own titler

Max reported new sessions still not renamed and worried the watcher was
project-scoped. Investigation showed two real issues:

1. The Codex desktop app (v0.146.0-alpha.3.1) auto-names active sessions with
   informative titles and stamps its own lowercase model tags ("ds ...",
   "deepseek ...", "qw ..."). The old labeler did not recognize those and
   double-stamped them ("[DS] ds Adding a prefix to a session name,
   model-prefix"), and it could overwrite the app's better names with raw
   first messages (it built from the DB title instead of the newest display
   index entry).
2. Threads whose first message was dictation-style ("Okay, name yourself
   Typer2 ...") kept raw first-message titles because the app's one-shot
   titler gave up on them.

Fix in label_threads.py:
- Build from the newest display index entry, falling back to the DB title.
- Recognize the app's native bare tags and normalize to the standard
  "[TAG] " form; strip nested tags ("[DS] ds X" -> "[DS] X").
- Shorten raw dictation-style titles from the first user message
  ("Okay, name yourself Typer2 and here is the task. We start i..." ->
  "[DS] Name yourself Typer2 and here is the task.").
- Preserve the app's informative titles, only fixing the tag format.

Verified 14:17 PDT: 9 double/mismatched tags normalized (backup
run_20260806-141721), current session now "[DS] Adding a prefix to a session
name, model-prefix", 0 untagged / 0 double-tagged out of 224 threads, watcher
run is a clean no-op. The watcher covers every project: it reads the global
Codex thread database, and the new xg1 downloads session was tagged from the
start. Committed to both repos (claude_base 42434488 + follow-up, base_608
3661b96 + follow-up).

## Third pass (same day, ~14:22 PDT): no-churn fix

The first normalization pass churned: 21 threads whose cleaned title already
equalled their display were still planned (backup per run), and the raw-title
shortener was about to rewrite weeks-old GPT-era names. Two fixes:

- Raw-title shortening is limited to threads created in the last 7 days; old
  names are left alone.
- `build_plan` now skips entries where the new title equals both the DB title
  and the display index entry, and when only the DB lags behind a correct
  index title it syncs the DB without appending another index line. Result:
  one final apply synced 79 DB titles (backup run_20260806-142241), pending
  dropped to 0, and the hidden watcher run is a true no-op with no new
  backup.

Final state 14:22 PDT: 224 threads, 0 untagged, 0 double-tagged, watcher
quiet. The app's own titler may still rename active sessions later (its
lowercase-tagged titles are normalized by the next 5-minute sweep).
