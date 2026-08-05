# Scribe handover - milestone 8 (~121K tokens)
# session: 20260612_vigilant_carson_ffce68_be212fff
# cwd: C:\claude_base\.claude\worktrees\vigilant-carson-ffce68
# written: 2026-06-12 15:52:19 by claude-opus-4-8

# HANDOVER - Watchlog rename (aborted & fully reverted)

## GOAL (in Max's words)
The pasted task was: "Rename the folder `C:\claude_base\compaction_kb` to `C:\claude_base\watchlog`, and update every reference to it." It was framed as a housekeeping rename of the "Watchlog" session watch+log system, deferred from an earlier near-compaction session because it touches LIVE hook wiring and had to be done all-at-once.

**But Max changed course mid-execution.** He said "wait wait. undo what you did," then confirmed it was a **mis-paste** - that task was NOT what he actually wanted right now. The rename has been fully undone. As of the last message, Max has not yet stated his real goal; he only commented on a leftover backup file.

## DECISIONS + WHY
- **Did the rename in the main checkout `C:\claude_base` (master), not the worktree** - because that's the live physical path the hooks and verification actually use.
- **Backed up settings.json before editing** - it's the live hook wiring; breaking it kills the survival hooks silently.
- **When undoing, chose a clean inverse-rename commit instead of `git revert`** - because a Stop-hook autocommit (`ebbaf562`) had already swept the rename into a pushed commit *bundled with hundreds of other sessions' uncommitted files*. A plain revert would have destroyed those other sessions' work. The inverse rename touched only the folder paths.
- **Unstaged runtime `.gauge_state/*.json` files** during the revert commit so the commit was purely the 16 inverse renames, nothing else.
- **Keep the backup file** - Max's last message: "i think backup is not heavy. Let's keep." So `settings.json.bak_watchlog_rename_20260612` stays. Do NOT delete it.

## CURRENT STATE - everything is back to original
- **Folder:** back to `C:\claude_base\compaction_kb`, original layout, scripts directly inside (not nested).
- **settings.json:** restored from backup; all hooks + statusline point at `compaction_kb`; valid JSON; `ctx_gauge.py` confirmed runs fine.
- **Git/master:** inverse-rename commit `defd5f92` made and **pushed** to origin/master. `origin/master..master` is empty (in sync). Other sessions' work preserved.
- **Backup file kept** (Max's decision).
- The rename is **NOT done** and should not be resumed unless Max explicitly asks again.

## EXACT NEXT STEP
Wait for Max to state what he actually wants to do. His real goal is still unknown - the only thing settled is "keep the backup file." Ask him, or act on whatever he says next. Do not re-attempt the rename.

## OPEN QUESTIONS
- What did Max actually intend to do (the mis-paste replaced his real request)? Still unanswered.

## KEY PATHS / IDS
- Folder (current, correct): `C:\claude_base\compaction_kb`
- Live hook config: `C:\Users\maxre\.claude\settings.json`
- Kept backup: `C:\Users\maxre\.claude\settings.json.bak_watchlog_rename_20260612`
- Repo: `github.com/maxrempel/claude_base`, branch `master`
- Revert commit: `defd5f92` (pushed)
- Autocommit that swept the rename in: `ebbaf562` (15:46, misleading message)
- Worktree cwd: `C:\claude_base\vigilant-carson-ffce68`

## GOTCHAS (already learned the hard way)
- **A Stop-hook autocommit fires and pushes** - it will sweep your staged changes into a pushed commit bundled with other sessions' dirty work. Anything staged when a turn ends can get committed. Stage narrowly and assume autocommit may fire.
- **Live hooks recreate hardcoded paths.** During the reverse `git mv`, a hook recreated `compaction_kb/.gauge_state`, so the directory already existed and git nested the moved content *inside* it. Watch for this; flatten manually if it recurs (the fix used a temp dir `__tmp_wl_flatten`).
- **settings.json is edited by other live sessions concurrently** - it changed between read and edit, and a 5th reference (statusLine, line ~59) appeared that wasn't there originally. Re-read before editing.
- **Main checkout is extremely dirty** (~446 files from other sessions). NEVER `git add -A` broadly or commit/revert without scoping to exact paths. Output dirs `worklog/`, `session_status/`, `user_verbatim/` are siblings under `C:\claude_base`, not inside the folder - leave them alone.
