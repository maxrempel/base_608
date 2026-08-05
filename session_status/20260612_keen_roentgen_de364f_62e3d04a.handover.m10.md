# Scribe handover - milestone 10 (~155K tokens)
# session: 20260612_keen_roentgen_de364f_62e3d04a
# cwd: C:\claude_base\.claude\worktrees\keen-roentgen-de364f
# written: 2026-06-12 15:12:47 by claude-opus-4-8

# HANDOVER - Session Survival System work

## GOAL (in Max's words)

Max kicked off with: *"We have an agent that summarizes things for the chat. I think. Or did we drop it?"* - he wanted clarity on the system structure (safety watcher, summarizer, compaction tracker, hooks). The first task: **update the docs describing the system**.

Then a concrete addition, his words: *"I want everything that I said in the session to be saved verbatim and the session should know where to look it up - because otherwise after compaction my words are lost."* Two stated reasons: (1) preserve the specs he defines, so they survive compaction; (2) help investigate troubles. He wanted a humanized before/after summary.

A follow-up task, his words: *"What is the size of the context and % to compaction. If compaction is 100%, where are we. Make automatically the sessions report their context every 10% or so."*

His latest message is **a naming brainstorm**, not a new build request. He's reacting to the assistant's prompt to name the umbrella system. He's tossing out: the functions are context, compaction, tracking, safety watch, logging - and floating names: *"watchlog? logger, logr? watcher and logger system?"*

## DECISIONS + WHY

- **Reuse existing machinery, don't reinvent.** The verbatim tool was built on the same transcript-reading/session-keying logic as `session_status.py`, so capture behaves consistently with the rest of the system.
- **Verbatim capture as a hook, not manual.** Wired as a 4th `UserPromptSubmit` hook so every user message is appended automatically - no reliance on the model remembering.
- **Post-compaction auto-pointer.** When a compaction is detected, the tool injects a note telling the fresh session where its specs live, because a cold session otherwise has no idea the log exists.
- **Context gauge every turn, not only at 10% bands.** It's one short line and directly answers Max's "where are we" question. A band-crossing marker still fires once per new 10% band. Max was explicitly offered the option to switch to 10%-only if he prefers.
- **Unified `resume.py`.** Rather than make a cold session hunt across four recovery sources (Scribe handover, work-log, verbatim log, breadcrumb), one command pulls them all together. The post-compaction pointer now sends sessions to `resume.py`.
- **Surgical git staging.** The repo has heavy unrelated dirty state from other sessions, so only the specific new/changed files were ever staged - never `git add -A`.

## CURRENT STATE

Both original tasks AND the context-gauge follow-up are **DONE, tested, committed, and pushed**. Nothing is in flight code-wise.

What exists now (the architecture, confirmed nothing was dropped):
- **The Scribe** = summarizer agent (full-Opus), writes handovers at token milestones. ALIVE.
- **The Adviser** = safety watcher (catches shortcuts/branching/drift; reachable via `a'`), plus a mechanical death-spiral blocker and a bcast watcher for colliding branches. ALIVE.
- Scribe + Adviser together = **"THE WATCH."**
- **Compaction tracking** - measurement is solved (compaction ~169K tokens, wipes ~94%). Mitigations: work-log + new verbatim log.

New this session:
- `user_verbatim.py` - 4th UserPromptSubmit hook, appends exact user text per session, auto-injects post-compaction pointer.
- `ctx_gauge.py` - 5th UserPromptSubmit hook, prints a one-line context gauge every turn + band-crossing marker.
- `resume.py` - unified recovery command pulling verbatim + work-log + Scribe handover + breadcrumb.
- `SYSTEM_OVERVIEW_tomemex.md` - the single authoritative architecture map (lists all hooks + which agent does what).
- Stale status block in the old HANDOVER doc was corrected; a pointer was added to `global2.md`.

## EXACT NEXT STEP

**Respond to Max's naming question - do NOT build anything.** He is choosing a name for the umbrella system. He's brainstorming around "watcher and logger" themes (watchlog / logger / logr). The assistant had previously offered BLACKBOX / LIFEBOAT / SENTINEL. Help him converge on a name. Once he picks one, the likely follow-on work is renaming the `compaction_kb` folder / docs to match - but wait for his decision first.

## OPEN QUESTIONS (awaiting Max)

1. **What to name the umbrella system?** (His current message.) He's leaning toward watcher/logger-flavored names.
2. Does he want the context gauge every turn (current) or only at 10%-band jumps? (Offered; not yet answered.)

## KEY PATHS / IDS / COMMANDS

- Working dir: `C:\claude_base\.claude\worktrees\keen-roentgen-de364f` (edits actually landed in main checkout `C:\claude_base`).
- Repo: `claude_base` ? github.com/maxrempel/claude_base, branch master.
- Scripts dir: `C:\claude_base\compaction_kb\scripts\` - `user_verbatim.py`, `ctx_gauge.py`, `resume.py`, `session_status.py`, `worklog.py`.
- Architecture doc: `C:\claude_base\compaction_kb\SYSTEM_OVERVIEW_tomemex.md`.
- Old handover doc (status fixed): `C:\claude_base\compaction_kb\HANDOVER_AND_STATUS_v01_tomemex.md`.
- This session's verbatim log: `C:\claude_base\user_verbatim\20260612_keen_roentgen_de364f_62e3d04a.verbatim.md`. Read with `user_verbatim.py read`.
- Hook wiring: `C:\Users\maxre\.claude\settings.json` (5 UserPromptSubmit hooks now). Backup at `settings.json.bak_20260612_verbatim`.
- Auto-loaded pointer: `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md`.
- Commits: first batch `368cfd46` (verbatim + overview); a second commit added resume.py + edits.
- Resume command: `python C:/claude_base/compaction_kb/scripts/resume.py --cwd "<session cwd>"`.

## GOTCHAS / DEAD ENDS RULED OUT

- **`/tmp` is not available** in this Bash environment - use a Windows-side temp file for stdin-fed hook tests.
- **`echo` mangles backslashes in JSON** - a test showed a wrong cwd because JSON failed to parse and fell back. Use `python -c` with raw strings to feed hook stdin, not `echo`.
- **Never `git add -A`** here - repo carries unrelated dirty state from other sessions; stage named files only.
- **Two artifacts live outside git by design:** `settings.json` (local to this machine) and `global2.md` (Nextcloud-synced).
- The compaction-pointer correctly fires ONLY on sessions that actually had a compaction - verified it does not false-fire on this worktree session.
- A synthetic test line was written then wiped via re-backfill, so the verbatim log is clean.
