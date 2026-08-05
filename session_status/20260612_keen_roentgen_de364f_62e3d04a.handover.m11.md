# Scribe handover - milestone 11 (~165K tokens)
# session: 20260612_keen_roentgen_de364f_62e3d04a
# cwd: C:\claude_base\.claude\worktrees\keen-roentgen-de364f
# written: 2026-06-12 15:23:59 by claude-opus-4-8

# HANDOVER - Watchlog System Build

## GOAL (in Max's words)

Max gave a sequence of requests across the session:

1. *"What is the structure - there is a safety watcher and i think a summarizer? Or not? and a system that tracks the compactions? That's the first task - to update the docs describing the system. Hooks etc."*
2. *"i want everything that i said in the session to be saved verbatim and the session should know where to look it up - because otherwise after compaction my words are lost. I need them for two reasons - to preserve the specs i defined after compaction and 2. to help investigation of troubles."*
3. *"i have little clue - what is the size of the context and % to compaction. If compaction is 100%, where are we. Make automatically the sessions report their context every 10% or so."*
4. *"sessions should take advantage of all summarizes and logs"* (not just one recovery source).
5. Name the umbrella system ? Max chose *"ok watchlog system"*.

Delivery style Max expects: humanized before/after summaries, plain English, pingpong, TLDR with colored-circle markers, always commit+push.

## DECISIONS + WHY

- **System named WATCHLOG** - because it does two things: WATCH (safety oversight agents) + LOG (durable files that survive compaction). Max confirmed the name explicitly.
- **Verbatim capture uses the hook's stdin `prompt` field** as the pure source (captured pre-injection, so it's Max's raw text), with transcript-backfill as a best-effort fallback. Storage keyed the same way as session_status.
- **Context gauge built as a separate lightweight hook** (no Opus, no nudge). It reuses session_status's token-measurement method (input + cache tokens, 169K cliff constant) rather than inventing a parallel estimator - the Adviser warned against a second estimator. The % is explicitly labeled an estimate (compaction lands *near* ~169K, not exactly).
- **Gauge set to fire only on a new 10% band** (`BAND_ONLY = True`) - Max objected that "every turn" was spammy; his original spec was "every 10%."
- **Physical folder rename was DEFERRED**, not done. Reason: renaming `compaction_kb` ? `watchlog` touches the live hook wiring in settings.json plus many hardcoded paths; doing it half-finished at ~93% context (compaction imminent) was too risky. It was queued as a clean separate job via a spawned task.
- **Fail-open everywhere** - a broken hook must never wedge a session. UTF-8 stdout, ASCII-only output except sanctioned colored-circle markers.
- **Never `git add -A`** - the main checkout is dirty with other sessions' work; only specific files staged each commit.

## CURRENT STATE - all five tasks DONE, committed, pushed to master

The work is complete. Then a compaction fired. The post-compaction session correctly summarized that all five tasks were finished and asked Max whether to run the queued folder rename now or leave it as a separate fresh-session job.

**Max's last message: "what folder rename"** - he is asking what the folder rename refers to. He appears not to recall the deferred rename item. The cold session must answer this question plainly.

## EXACT NEXT STEP

**Answer Max's question "what folder rename" directly and briefly.** Explain: the system is now named *Watchlog*, but its folder on disk is still physically called `compaction_kb`. The only leftover task is to rename that folder (`C:\claude_base\compaction_kb` ? `C:\claude_base\watchlog`) and update every reference to it - most critically the 4-5 hook paths in `settings.json`, plus hardcoded paths in the scripts, docs, global2.md, and any index/infra-map files. This was deliberately deferred because it touches live hook wiring and was risky to do at the compaction edge. It is already queued as a separate spawned job. Then ask whether to run it now or leave it queued.

Do NOT auto-run the rename without Max's confirmation.

## OPEN QUESTIONS AWAITING MAX

- Whether to run the `compaction_kb` ? `watchlog` folder rename now, or leave it as the queued separate fresh-session job.
- (Standing flag, not blocking) The main `C:\claude_base` checkout is dirty with uncommitted work from other sessions - a housekeeping/branching cleanup worth doing before it bites.

## KEY PATHS / IDS

- Repo: `claude_base` (github.com/maxrempel/claude_base), branch **master**.
- This session's verbatim log: `C:\claude_base\user_verbatim\20260612_keen_roentgen_de364f_62e3d04a.verbatim.md`
- Full transcript jsonl: `C:\Users\maxre\.claude\projects\C--claude-base--claude-worktrees-keen-roentgen-de364f\62e3d04a-c11d-4173-82e3-7f74f32b99b9.jsonl`
- cwd (worktree): `C:\claude_base\.claude\worktrees\keen-roentgen-de364f`
- New scripts (all in `C:\claude_base\compaction_kb\scripts\`): `user_verbatim.py`, `ctx_gauge.py`, `resume.py`
- New doc: `C:\claude_base\compaction_kb\SYSTEM_OVERVIEW_tomemex.md` (titled "WATCHLOG - the session watch + log system")
- Edited docs: `compaction_kb\HANDOVER_AND_STATUS_v01_tomemex.md` (superseded-in-part note), `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md` (added VERBATIM USER-LOG section + WATCHLOG name pointer)
- Live hook wiring: `C:\Users\maxre\.claude\settings.json` (Pine-only, NOT in repo; backup at `.bak_20260612_verbatim`). Now has 5 UserPromptSubmit hooks: bcast read, worklog_reminder, session_status --hook, user_verbatim --hook, ctx_gauge --hook.
- Commands: `python compaction_kb/scripts/user_verbatim.py read|backfill|path|--hook`; `resume.py --cwd "<cwd>"`; `ctx_gauge.py`.
- Gauge constants: `COMPACT_CLIFF = 169000`, `BAR_W = 20`, `BAND_ONLY = True`, state dir `C:\claude_base\compaction_kb\.gauge_state`.

## ARCHITECTURE FACTS (for answering "what is the structure")

- **THE WATCH** = two full-Opus oversight agents: the **Scribe** (summarizer / handover writer - NOT dropped, it's alive) and the **Adviser** (skeptical safety watcher; answers `a'` / `adviser:` prompts synchronously). Driven by `session_status.py` at ~15K-token milestones via detached `session_oversight.py`.
- **Safety mechanics**: `block_death_spiral.py` (PreToolUse hook blocking 5 self-destructive patterns) + `bcast`/`branch_bulletin` watcher (sibling-branch collision coordination).
- **Compaction**: auto-fires ~169K tokens (mean ~168,999), keeps ~5.7% ? ~94% memory loss. Detected via native `compact_boundary` markers in the transcript jsonl.

## GOTCHAS / DEAD ENDS RULED OUT

- `echo '{...}'` in this bash mangles backslashes ? JSON parse fails ? tool falls back to wrong cwd. Use a Python-written Windows temp JSON file for hook tests, not echo.
- `/tmp` does not exist on this bash; use `C:\claude_base\_hk.json` for temp files.
- Never use `git add -A` - main checkout is dirty with other sessions' work; stage only your specific files.
- The gauge % is an estimate, not exact - present it as a fuel gauge.
- `settings.json` and `global2.md` live OUTSIDE the git repo (local Pine + Nextcloud respectively) - the folder rename must update both manually.
