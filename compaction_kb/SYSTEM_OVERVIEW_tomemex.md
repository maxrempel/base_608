# WATCHLOG - the session watch + log system (bird's-eye overview)

NAME (Max, 2026-06-12): the system is called **WATCHLOG** - it WATCHES (safety:
Scribe, Adviser, death-spiral blocker) and LOGS (survival: work-log, verbatim,
breadcrumb, compaction tracking). The code/doc folder STAYS physically named
`compaction_kb` - Max decided NOT to rename it (2026-06-12: "no renaming messes
things up, compaction_kb is good enough"). The folder name carries the live hook
paths in settings.json; the WATCHLOG name lives only in the docs/conversation. Do
NOT attempt a folder rename.

Last updated 2026-06-12 by Claude Opus 4.8. Plain ASCII only.
This is the SINGLE map of every hook + background agent that protects a Claude
Code session on Pine. When you ask "what is the structure - is there a summarizer,
a safety watcher, a compaction tracker?", THIS is the answer. Detailed per-piece
docs are linked at the bottom; this doc is the index + the truth about what is
actually WIRED right now.

## THE ONE-LINE ANSWER

Nothing was dropped. There are THREE jobs, done by agents/hooks that all hang off
`~/.claude/settings.json`:
  1. SUMMARIZER  -> "the Scribe" (writes handovers so a cold session can resume).
  2. SAFETY      -> "the Adviser" + the death-spiral blocker + the bcast watcher.
  3. COMPACTION  -> the measurement (solved) + the two MITIGATIONS that let a
                    session survive a compaction: the conscious work-log and the
                    new verbatim user-log.

## WHAT IS ACTUALLY WIRED (settings.json, Pine only)

settings.json is NOT in the Nextcloud sync, so all of this is Pine-only unless
re-added by hand on Sirius/Vega.

UserPromptSubmit (fires once per Max message, in this order):
  1. bcast.py read --hook
        Sibling-branch broadcast board. Lets parallel branches hear each other.
        (Coordination, not survival - included here for completeness.)
  2. worklog_reminder.py
        Nudges if the conscious work-log has gone >20 min stale. Fail-open.
  3. session_status.py --hook   == "THE WATCH"
        Detects ~15K-token milestones (~11 before the ~169K compaction cliff).
        On each new milestone: (a) writes a mechanical breadcrumb line; (b)
        launches a DETACHED, HIDDEN background runner (session_oversight.py) that
        calls full Opus TWICE - once as the SCRIBE, once as the ADVISER; (c)
        injects a short "status report due" nudge. Also: a prompt starting with
        "a'" or "adviser:" is answered SYNCHRONOUSLY by the Adviser in the same
        turn.
  4. user_verbatim.py --hook    == NEW 2026-06-12
        Appends Max's exact words to an on-disk per-session file so his specs +
        corrections survive a compaction. On the first turn AFTER a compaction it
        injects a one-line pointer to the resume command (below).
  5. ctx_gauge.py --hook        == NEW 2026-06-12
        Always-on one-line context readout: "~146K / 169K tokens | 86% to
        compaction [bar]". Prints every turn; flags each new 10% band crossing.
        No Opus, no nudge - just a gauge so Max always knows where the session is.

RESUME / CATCH-UP (not a hook - a command a cold session runs):
  resume.py - pulls ALL recovery sources together in one call (verbatim words +
  work-log + Scribe handover + breadcrumb), so a post-compaction session takes
  advantage of EVERYTHING, not just one log:
    python C:/claude_base/compaction_kb/scripts/resume.py

PreToolUse (fires before every tool call):
  - block_death_spiral.py
        The suicide-prevention hook. Blocks 5 known death patterns: repeat-the-
        same-Bash, empty-result streak, BashOutput poll loop, repeated back-to-
        back Read of the same file, and the parallel cancel-cascade. Fail-open.

Stop (fires when the model finishes a turn):
  - autocommit_rules.sh
        Auto-commits per the repo's rules.

NOT in settings.json (Windows Scheduled Tasks, hidden):
  - bcast watcher (branch_bulletin/watcher.py + safety_watcher.py), task
    "bcast_watcher", every 10 min: sweeps for two live sessions claiming the same
    branch id; nudges the board + a Telegram critical alarm. A SAFETY net for the
    multi-branch case.

## THE THREE JOBS, IN PLAIN TERMS

### 1. SUMMARIZER = THE SCRIBE  (alive, not dropped)
A calm full-Opus agent. At each token milestone it reads the WHOLE transcript and
writes a rich handover to `C:\claude_base\session_status\<stem>.handover.m<level>.md`.
Purpose: a cold session (post-compaction, or a fresh resume) reads the latest
handover and continues the exact work. It never interrupts. It is one of the two
halves of "THE WATCH". Personality file (edit to retune, no code change):
`compaction_kb\personalities\scribe.md`.

### 2. SAFETY = THE ADVISER + the death-spiral blocker + the bcast watcher
- THE ADVISER: a skeptical full-Opus agent, the other half of THE WATCH. Reads
  the chat and catches trouble (shortcuts, branching, death-spiral, drift, Max
  being ignored). It advises two audiences - the working session and Max. Silent
  on a clean session. Two-way: Max can ask it directly with an "a'" prompt and
  gets a synchronous answer. Personality: `compaction_kb\personalities\adviser.md`.
- THE DEATH-SPIRAL BLOCKER (block_death_spiral.py): mechanical PreToolUse guard,
  no Opus, just pattern-matching, blocks the 5 patterns above before they pile up
  thinking blocks and kill the session. Full doc:
  `tools\suicide_prevention\suicide_prevention_tomemex.md`.
- THE BCAST WATCHER: cron safety net for duplicate-branch collisions.

### 3. COMPACTION = measurement (solved) + mitigations
MEASUREMENT (answered, not an open question anymore):
  - harvest_compactions.py scans all transcripts for the native compact_boundary
    markers Claude Code writes, into kb/compaction_events.jsonl.
  - RESULT: auto-compaction fires at ~169K tokens (mean 168,999, very tight) and
    keeps only ~5.7% of context -> ~94% memory loss. Manual /compact fires
    earlier (~142K) and more variably.
  - ctx_track.py is the older per-turn byte/token estimator (superseded by the
    native markers, kept for history).
MITIGATIONS (this is the part that matters day-to-day):
  - worklog.py - the CONSCIOUS work-log. The SESSION decides what to record
    (DID / STATE / NEXT, optional LESSON). One append-only file per project at
    `C:\claude_base\worklog\<project-key>.md`. Survives compaction; future/parallel
    sessions read it to resume.
  - user_verbatim.py - NEW. The UNCONSCIOUS, automatic record of Max's exact
    words (see next section). The work-log is the model's digest; the verbatim log
    is Max's raw words. Belt and suspenders.

## THE VERBATIM USER-LOG (new 2026-06-12) - what + why + where

WHY: a compaction wipes ~94% of context, so after one the session has LOST the
specs Max dictated and the corrections he gave - and his exact wording is
intentional (paraphrase loses function). Two uses: (1) recover specs after a
compaction, (2) a faithful transcript of Max's side for investigating trouble.

WHAT: `compaction_kb\scripts\user_verbatim.py`, wired as the 4th UserPromptSubmit
hook. Every turn it appends Max's exact submitted text (the hook's stdin `prompt`
field - pure, pre-injection) to one file per session:
`C:\claude_base\user_verbatim\<day>_<tail>_<sid8>.verbatim.md`
(same stem scheme as session_status, so the two pair up by stem).

POST-COMPACTION POINTER: the hook counts the native compact_boundary markers in
the transcript; on the first turn after a NEW one appears it injects a one-line
note: "context was just compacted; read your verbatim log here". So a cold session
KNOWS where to look (Max's requirement).

COMMANDS:
  python C:/claude_base/compaction_kb/scripts/user_verbatim.py read       (this session's words)
  python ... user_verbatim.py backfill   (rebuild the file from the transcript - catches
                                          turns from before the hook existed, or repairs a lost file)
  python ... user_verbatim.py path       (print the file path)
Fails open everywhere.

## WHERE THE OUTPUTS LIVE (quick reference)
  C:\claude_base\session_status\        Scribe handovers, Adviser notes, breadcrumbs
  C:\claude_base\session_status\oversight.log   the Watch runner log (debug silent failures)
  C:\claude_base\worklog\               conscious per-project work-logs
  C:\claude_base\user_verbatim\         NEW - per-session verbatim record of Max's words
  C:\claude_base\compaction_kb\kb\compaction_events.jsonl   harvested compaction stats

## DETAILED DOCS (read these for any one piece)
  THE WATCH (Scribe + Adviser):   compaction_kb\the_watch_oversight_tomemex.md
  Measurement + work-log history: compaction_kb\HANDOVER_AND_STATUS_v01_tomemex.md
  Death-spiral blocker:           tools\suicide_prevention\suicide_prevention_tomemex.md
  Sibling broadcast + watcher:    branch_bulletin\README_tomemex.md
  Conscious work-log usage:       global2.md "CONSCIOUS WORK-LOG" section

## MACHINE NOTE
All settings.json hooks are Pine-only (that file is not synced). To enable on
Sirius/Vega, re-add the same UserPromptSubmit / PreToolUse / Stop commands there.
