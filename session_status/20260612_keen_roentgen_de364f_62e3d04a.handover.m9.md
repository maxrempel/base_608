# Scribe handover - milestone 9 (~139K tokens)
# session: 20260612_keen_roentgen_de364f_62e3d04a
# cwd: C:\claude_base\.claude\worktrees\keen-roentgen-de364f
# written: 2026-06-12 15:09:14 by claude-opus-4-8

# HANDOVER - Session Survival Tooling

## GOAL (in Max's words)

Two completed tasks from earlier, plus one new task now in flight:

**Earlier (done):** *"We have an agent that summarizes things for the chat... update the docs describing the system. Hooks etc. Next, i want everything that i said in the session to be saved verbatim and the session should know where to look it up - because otherwise after compaction my words are lost."* Two reasons given: (1) preserve specs defined before a compaction, (2) help investigate troubles.

**New task (just requested, NOT yet started):** *"i have little clue - what is the size of the context and % to compaction. If compaction is 100%, where are we. Make automatically the sessions report their context every 10% or so."*

So: Max wants a session to automatically surface its own context usage as a percentage toward compaction, reporting roughly every 10% of progress.

## DECISIONS + WHY

- **Reuse existing transcript/keying machinery** rather than build fresh. The compaction system already reads session transcripts and keys per-session files; the verbatim tool was built on the same pattern, and the new context-reporting task should follow suit.
- **Stage only specific files for git, never `-A`.** The `C:\claude_base` repo carries heavy unrelated dirty state from other parallel sessions. All commits must add named files explicitly.
- **Edits land in main checkout, not the worktree.** Work happens in worktree `keen-roentgen-de364f` but file edits went to `C:\claude_base`, so commits are made from there.
- **Compaction is understood as a fixed threshold:** it triggers near ~169K tokens and wipes ~94% of context. This is the anchor for any "% to compaction" math the new task needs.

## CURRENT STATE

**Tasks 1 & 2 are fully complete, committed, and pushed** (commit `368cfd46` on master):

- **Task 1** - `compaction_kb/SYSTEM_OVERVIEW_tomemex.md` written: one authoritative map of all hooks (4 UserPromptSubmit, 1 pre-tool, 1 stop) and which agent does what. The stale status block in the old HANDOVER doc was pointed at it.
- **Task 2** - `user_verbatim.py` built and wired as the 4th UserPromptSubmit hook. It appends Max's exact text to a per-session file, and after a compaction auto-injects a pointer telling the session where to read the saved specs. Backfill, live capture, read, and compaction-pointer all tested working. A pointer was added to `global2.md` so every cold session knows the verbatim log exists.
- settings.json was backed up before editing and validated as valid JSON afterward (4 UserPromptSubmit hooks confirmed).
- A worklog milestone was logged.

**Task 3 (context %-reporting) has NOT been started.** No code, no design, no investigation yet.

## EXACT NEXT STEP

Begin Task 3. Before writing anything, investigate how a running session can know its own current token/context size - this is the crux. The hook scripts already read the transcript, so the likely approach is to estimate context size from the transcript and compute a percentage against the ~169K compaction threshold, then emit a report when the session crosses each ~10% band (tracking the last-reported band per-session so it fires once per band, not every message). Model this on the existing hook pattern in `session_status.py` / `user_verbatim.py`.

## OPEN QUESTIONS (awaiting Max)

- None explicitly pending, but the mechanism for a session to read its *own live* token count is the unresolved technical question - confirm whether transcript-size estimation is acceptable as the proxy, or whether a more exact source exists.

## KEY PATHS / IDS / COMMANDS

- Worktree cwd: `C:\claude_base\.claude\worktrees\keen-roentgen-de364f`
- Main checkout (commit from here): `C:\claude_base`
- Settings: `C:\Users\maxre\.claude\settings.json` (backup: `...settings.json.bak_20260612_verbatim`)
- New tool: `C:\claude_base\compaction_kb\scripts\user_verbatim.py` (modes: `backfill --cwd <path>`, `--hook` via stdin JSON)
- Existing models to copy: `compaction_kb\scripts\session_status.py`, `compaction_kb\scripts\worklog.py`
- Docs: `compaction_kb\SYSTEM_OVERVIEW_tomemex.md`, `compaction_kb\HANDOVER_AND_STATUS_v01_tomemex.md`
- Verbatim output dir: `C:\claude_base\user_verbatim\` (e.g. `20260612_keen_roentgen_de364f_62e3d04a.verbatim.md`)
- Auto-loaded global: `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md`
- Worklog command: `python C:/claude_base/compaction_kb/scripts/worklog.py log "..."`
- Last commit: `368cfd46`

## SYSTEM CONTEXT (the three jobs, for reference)

1. **Scribe** = summarizer agent (full Opus), writes handovers at token milestones. Alive, not dropped.
2. **Adviser** = safety watcher (invoke with `a'`), plus a mechanical death-spiral blocker and a bcast watcher for colliding branches.
3. **Compaction tracking** = measurement solved (~169K trigger, ~94% wipe); mitigations are the work-log and the new verbatim log. Scribe + Adviser together are called "THE WATCH."

## GOTCHAS / DEAD ENDS

- `/tmp` is NOT available in this Bash environment - use Windows-side temp files for any stdin/JSON testing.
- `echo` with JSON mangles backslashes in Windows paths (caused a JSON parse failure that silently fell back to cwd). Pipe test JSON via `python -c` writing to a file, not via `echo`.
- NEVER `git add -A` here - the repo is dirty from other sessions. Stage named files only.
- Current real token usage ~139K; compaction wipes near ~169K. This session is itself close to the threshold - proceed efficiently.
