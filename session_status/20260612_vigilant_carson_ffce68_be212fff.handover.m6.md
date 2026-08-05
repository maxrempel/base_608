# Scribe handover - milestone 6 (~92K tokens)
# session: 20260612_vigilant_carson_ffce68_be212fff
# cwd: C:\claude_base\.claude\worktrees\vigilant-carson-ffce68
# written: 2026-06-12 15:47:13 by claude-opus-4-8

# HANDOVER - Watchlog Rename (PAUSED, UNDO REQUESTED)

## GOAL (in Max's words)
"Rename the folder `C:\claude_base\compaction_kb` to `C:\claude_base\watchlog`, and update every reference to it." This is a housekeeping rename of the "Watchlog" session watch+log system (Max named it 2026-06-12). It was deferred from a prior near-compaction session because it touches LIVE hook wiring and must be done all-at-once.

**BUT - the most recent instruction overrides the task: Max said "wait wait. undo what you did."** The immediate job now is to REVERSE the partial migration, not finish it. Do not proceed with the rename. Restore the prior state and confirm with Max before doing anything else.

## CURRENT STATE - what was actually changed (must be undone)
Two things were already mutated on the LIVE system before Max said stop:

1. **Folder physically renamed via `git mv`** in the main checkout `C:\claude_base` (branch master). `C:\claude_base\watchlog\` now exists; `C:\claude_base\compaction_kb\` is gone. The rename is staged in git but NOT committed.
2. **`C:\Users\maxre\.claude\settings.json` was edited** - all 5 live hook/statusline command paths were repointed from `compaction_kb/scripts/` to `watchlog/scripts/`. JSON was validated as parseable after the edit. A backup exists at `C:\Users\maxre\.claude\settings.json.bak_watchlog_rename_20260612`.

Nothing else was changed. The following were NOT touched: the scripts' own hardcoded `compaction_kb` paths, the in-folder docs, global2.md, mdindex.md, infra_map_tomemex.md. Nothing was committed or pushed.

## EXACT NEXT STEP (the undo)
Reverse both mutations so the system returns to its pre-session state:

1. **Restore settings.json** from the backup `settings.json.bak_watchlog_rename_20260612` (overwrite the edited file). Then validate it parses as JSON. This is the live hook wiring - get it back to pointing at `compaction_kb/scripts/` first, since the folder is about to move back too.
2. **Reverse the folder rename**: `git mv watchlog compaction_kb` in `C:\claude_base` (master). Confirm `compaction_kb\` exists again and `watchlog\` is gone, and that git status shows no staged rename remaining for this folder.
3. **Verify** `git status` shows the watchlog/compaction_kb rename is fully unstaged/reverted, and that no commit was made.

Then report back to Max that the undo is complete and the system is back to its original state - and wait. Do not re-attempt the rename unless Max explicitly says so.

## OPEN QUESTIONS (awaiting Max)
- Max has not said WHY he wants to stop/undo, or whether the rename is cancelled entirely vs. just paused for a different approach. Ask once the undo is confirmed clean.

## GOTCHAS / THINGS ALREADY LEARNED
- **settings.json is being written by other live sessions.** During the original edit it changed underneath us - a 5th reference (a `statusLine` entry pointing at the scripts dir) was added by another session between read and edit. Restoring from the static backup may therefore LOSE concurrent edits another session made after the backup was taken. Before blindly overwriting, diff the current settings.json against the backup to see if anything non-Watchlog changed; only the `compaction_kb`/`watchlog` script paths should differ. If other sessions added unrelated keys, hand-revert just the path strings instead of clobbering the whole file.
- **The main `C:\claude_base` checkout is extremely DIRTY** - ~446 uncommitted files from many other sessions. NEVER `git add -A` or commit broadly. Only the `git mv` for this folder was staged. The undo must likewise touch only the folder rename. Do not commit anything.
- **Backup file location:** `C:\Users\maxre\.claude\settings.json.bak_watchlog_rename_20260612` - after a successful undo, consider whether to delete it (ask Max).
- Historical/frozen matches under `session_status/*.handover` and `branch_bulletin/*` were intentionally left untouched - they are snapshots, not live refs. Not relevant to the undo.

## KEY PATHS / IDS
- Folder (current, needs reverting): `C:\claude_base\watchlog\` ? back to `C:\claude_base\compaction_kb\`
- Live hooks config: `C:\Users\maxre\.claude\settings.json`
- Backup: `C:\Users\maxre\.claude\settings.json.bak_watchlog_rename_20260612`
- Repo: `C:\claude_base`, git remote github.com/maxrempel/claude_base, branch master
- cwd of this session: `C:\claude_base\.claude\worktrees\vigilant-carson-ffce68` (note: rename work was done in the MAIN checkout `C:\claude_base`, not this worktree)
- JSON validation command pattern: run python with `import json; json.load(open(<path>))` and print a confirmation.

## CONTEXT FOR THE FUTURE RENAME (if Max revives it later - NOT now)
The original task list of references to update: settings.json (4-5 hook/statusline paths), hardcoded `compaction_kb` strings inside session_status.py, ctx_gauge.py (incl. `.gauge_state` STATE_DIR and printed pointer strings), user_verbatim.py, resume.py, worklog.py docstring, ctx_track.py, harvest_compactions.py; docs SYSTEM_OVERVIEW_tomemex.md, HANDOVER_AND_STATUS_v01_tomemex.md, the_watch_oversight_tomemex.md; plus `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md`, `C:\claude_base\mdindex.md`, and `C:\claude_base\infra_map_tomemex.md` if present. Cross-script refs using `os.path.dirname` are relative and fine. Sibling OUTPUT dirs (`worklog/`, `session_status/`, `user_verbatim/` under `C:\claude_base`) were to be LEFT as-is. None of this should be acted on until Max re-greenlights.
