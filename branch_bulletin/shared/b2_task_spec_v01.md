# b2 Task Spec v01 - Context & Compaction Calibration KB

Author: b2 (Claude Opus, worktree youthful-heyrovsky-b2c7a0), 2026-06-06.
Coordinated by b1 over the branch board. Owner/decider: Max.

## The problem (in Max's words)
We do NOT currently know two things:
1. At what transcript/JSON size does a compaction actually fire?
2. What is the consequence of a compaction? (usually severe memory loss)

So we cannot tune how we spend context per task. The fix is to MEASURE:
build a knowledge base (a set of log files) that accumulates real numbers
across many sessions, so b1/b2/future sessions can read it, learn the real
threshold, and optimize token spend.

This is a DATA-COLLECTION + CALIBRATION system, not a fancy logger.

## Two reinforcing threads (kept in one branch, b2, for now)
- Thread 1 - compaction damage: detect compactions, measure the size at which
  they fire, and measure how much memory is lost (severity).
- Thread 2 - universal work log: get every session to keep a dated work
  journal OUTSIDE its context. This is the mitigation for Thread 1: a log that
  survives a compaction is what lets a session/branch recover. Thread-1
  experiments drive the design of Thread-2, so we do NOT split them.

b1 decision (2026-06-06): keep both threads in b2; spin b3 only when b2's own
context-fill metric says b2 is heavy.

## What we learned from the first look (baseline)
Transcript files live at:
`C:\Users\maxre\.claude\projects\<PROJECT>\<session-uuid>.jsonl`
where <PROJECT> = the cwd with `: \ / . _` all replaced by `-`.
(e.g. cwd `C:\claude_base\.claude\worktrees\youthful-heyrovsky-b2c7a0`
  -> `C--claude-base--claude-worktrees-youthful-heyrovsky-b2c7a0`).

Key facts:
- The .jsonl is APPEND-ONLY full history. It does NOT shrink on compaction.
  So a compaction appears as a MARKER LINE, and the gold calibration number
  is the transcript size (bytes / est tokens) just BEFORE that marker.
- Line types seen so far: user, assistant, system(subtype=stop_hook_summary),
  attachment, queue-operation, last-prompt, ai-title, custom-title.
- No compaction has happened in any current session yet, so the exact
  compaction marker string is still UNKNOWN. The tracker must therefore log
  any unknown system subtype so we capture the real marker the first time.
- Rough sizing: ~bytes/4 = est tokens (overcounts; refine by summing message
  text only). b2's own transcript at baseline: ~448 KB, 245 lines, ~112K est tk.

## Components (build order)
1. ctx_track.py  - given a transcript (or auto-detect from cwd), report:
   bytes, lines, est tokens, compaction count, bytes-since-last-compaction.
   Append one record per run to logs/ctx_log.jsonl. On a NEWLY detected
   compaction, write an event (size-before = calibration gold, compression
   ratio) to kb/compaction_events.jsonl and ALERT/broadcast.
2. Compaction detector - candidate markers: isCompactSummary==true,
   type=="summary", subtype contains "compact", message text contains
   "This session is being continued" / "compacted" / "context low".
   Plus: log unknown system subtypes for discovery.
3. Severity meter - when a compaction fires: pre-size vs post-summary size =
   compression ratio; archive the pre-compaction tail so "lost" memory is
   recoverable, not gone.
4. Pre-compaction handover - when a branch nears the limit, save current
   thinking to a handover file BEFORE the loss.
5. Broadcast - warn siblings when a compaction happens ("b1 compacted at X,
   re-confirm before trusting it").
6. Universal work log (Thread 2) - hook-enforced dated journal for every
   session; survives compaction; speeds catch-up / migration to new sessions.

## Metrics natural to a session (the things we log each tick)
- transcript bytes, line count (turns), est tokens, % of window (once we know
  the window), tool-call count, compaction count, wall-clock age,
  bytes-since-last-compaction.

## Output locations
- Tool: `C:\claude_base\compaction_kb\scripts\`
- Per-tick logs: `C:\claude_base\compaction_kb\logs\ctx_log.jsonl`
- Compaction event KB: `C:\claude_base\compaction_kb\kb\compaction_events.jsonl`
- This spec + shared notes: `C:\claude_base\branch_bulletin\shared\`

## Safety / working rules (from Max + b1)
- No irreversible actions without Max. Commit work to git. If blocked, post a
  question to the board and WAIT - do not thrash. STOP word = "halt b2".
- No silent fallbacks; honest errors. Version + date everything; no "final".

## Status
- v01: spec written; baseline captured; tracker tool next.
