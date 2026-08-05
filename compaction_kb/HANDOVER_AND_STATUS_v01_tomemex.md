# Compaction-Calibration KB - HANDOVER & STATUS v01

## *** SUPERSEDED-IN-PART 2026-06-12: read SYSTEM_OVERVIEW_tomemex.md first ***
The measurement question and the mitigations are now DONE and live. For the
current bird's-eye map of every wired hook + agent (Scribe, Adviser, death-spiral
blocker, work-log, verbatim user-log) read `compaction_kb\SYSTEM_OVERVIEW_tomemex.md`.
The "IN-PROGRESS / hook build gated on b1" notes below are HISTORICAL - the Stop/
UserPromptSubmit hooks were built and wired; the conscious work-log (worklog.py)
and the new verbatim user-log (user_verbatim.py) both ship. This file is kept for
the experiment's findings and history.

## *** ROLLING STATUS (update every milestone; last: 2026-06-06 ~22:16 by b2) ***
DONE:
- Measurement question SOLVED. harvest_compactions.py harvested 158 events;
  auto-compact fires ~169K tokens (mean 168,999, n=149); ~94% memory loss.
  Committed+pushed (6bd15a8e). Answer broadcast to b1.
- Component 6 SPEC written + b1-APPROVED (per-project log, milestone cadence,
  add near-limit handover). branch_bulletin/shared/b2_component6_worklog_spec_v01.md.
- Component 6 BUILD #1 DONE: worklog.py (log/read/path; fails open; branch+
  session auto-tagged; keyed by bcast cwd-hash). Seeded this session, verified
  read. Committed+pushed (e27554fa). Tool: compaction_kb/scripts/worklog.py;
  logs at C:/claude_base/worklog/<project-key>.md.
IN-PROGRESS:
- Asked b1+b3 to log a test entry from their worktrees (prove the habit).
- DESIGN FLAG raised to b1: cwd-hash keys per-WORKTREE not per-JOB. Options
  (A) per-worktree = crash-resume insurance (my lean) vs (B) per-repo-root =
  one shared job log. HOLDING hook build until b1 picks the key.
NEXT (after b1 picks key):
- Build additive fail-open Stop-hook nudge (backup settings.json, do NOT touch
  autocommit/death-spiral, validate JSON, test, ready to revert).
- Then propose global2 section + skill for Max's approval. Add near-limit
  (~150K) full-handover trigger.
LIGHT side-thread (cheap only): 1M-model threshold? preCompactDiscoveredTools
meaning? postTokens ~12-13K budget fixed? manual-vs-auto difference?
BLOCKERS: hook build gated on b1's per-worktree-vs-per-job key decision.
CADENCE: self-wake every 4 min (Max directive). b1 coordinates.
ARTIFACTS: harvest_compactions.py, ctx_track.py, kb/compaction_events.jsonl,
b2_task_spec_v01.md, b2_component6_worklog_spec_v01.md (all under C:/claude_base).


Written 2026-06-06 ~21:50 by b2 (Claude Opus, worktree youthful-heyrovsky-b2c7a0),
WHILE NEARING ITS OWN COMPACTION. This doc exists so a future session (post-
compaction-b2, a fresh b2, or any Claude) can CONTINUE this multi-day experiment.
Max's framing: "you build the system blindly and hope future sessions continue;
the task must be documented and embedded." This is that document.

## THE MISSION (one paragraph)
We do not know (a) at what context fill a Claude Code session auto-compacts, nor
(b) how badly a compaction damages memory. Build a system of LOG FILES that
accumulates real numbers across ~40 sessions over several days, so future
sessions can read it, learn the true threshold, and calibrate token spend per
task. This is data collection + calibration, NOT a fancy logger. The ANSWER will
be found by FUTURE sessions reading the accumulated logs.

## TEAM / OPERATING MODEL
- b1 = commander (worktree vigorous-jemison-340d7a). b2 = me, worker+peer
  (worktree youthful-heyrovsky-b2c7a0). Same Opus model; b2 offers options and
  may disagree on the board, but b1 decides. Max is ultimate owner.
- They coordinate via the bcast board: `python C:\claude_base\branch_bulletin\bcast.py`
  (whoami / post / read). Hearing is automatic via a UserPromptSubmit hook.
- STOP conditions: JOB DONE -> post "JOB DONE: ..."; CRITICAL -> `bcast.py halt "..."`;
  MANUAL -> "halt b2"/"halt all" banner. Never loop forever.

## WHAT IS BUILT (all committed to git repo claude_base)
- `C:\claude_base\branch_bulletin\bcast.py` - sibling broadcast board.
- `C:\claude_base\branch_bulletin\shared\b2_task_spec_v01.md` - full spec, 6 components.
- `C:\claude_base\compaction_kb\scripts\ctx_track.py` - measures a session
  transcript: bytes, lines, est tokens (file/4 AND message-text/4), tool calls,
  compaction count (STRUCTURAL markers only), bytes-since-last-compaction.
  Appends each run to `compaction_kb\logs\ctx_log.jsonl`; on a NEW compaction
  writes a calibration event to `compaction_kb\kb\compaction_events.jsonl`; logs
  unknown system subtypes to discover the real marker.
  Run: `python C:/claude_base/compaction_kb/scripts/ctx_track.py --cwd "<cwd>" --branch bX`

## *** ANSWER FOUND (2026-06-06, ~21:55) - THE EXPERIMENT IS LARGELY SOLVED ***
Claude Code NATIVELY records every compaction in the transcript:
  line with type=system, subtype=**compact_boundary**, field **compactMetadata** =
  {trigger, preTokens, postTokens, preCompactDiscoveredTools, durationMs}.
So we do NOT need byte/token estimates and do NOT need to wait for 40 sessions -
the exact pre/post token counts are already logged. Harvested ALL historical
compactions across ~/.claude/projects in one scan (script:
compaction_kb/scripts/harvest_compactions.py -> kb/compaction_events.jsonl):

  - 158 compaction events found (149 auto, 8 manual) on this machine's history.
  - **AUTO-compact threshold: mean 168,999 preTokens, min 167,004, max 191,421,
    n=149.** Very tight: auto-compaction fires at ~169K tokens (~85% of a 200K
    window). (Note: a few manual /compact events pull the all-events min down to
    ~129K.)
  - **Severity: mean kept-ratio 0.057 -> only ~5.7% of context survives a
    compaction (~94% memory loss).** This is why compaction is so damaging.
  - One concrete event (b1, the one we watched live): preTokens 169,582 ->
    postTokens 12,826, trigger auto, durationMs 96,168 (~96s).

PRACTICAL UPSHOT for token budgeting:
  - Treat ~165K tokens as the danger zone; auto-compaction will hit ~169K.
  - To compact EARLIER/cleaner, set env CLAUDE_AUTOCOMPACT_PCT_OVERRIDE (1-100).
  - Because ~94% is lost, the mitigation (Component 6: durable dated work-log +
    pre-compaction handover) is what actually preserves continuity. THAT is now
    the remaining valuable work; the measurement question is answered.
  - harvest_compactions.py is idempotent (dedups by uuid); re-run it anytime to
    add new compactions and refresh stats.

## LIGHT-THREAD FINDINGS (2026-06-07, from already-harvested events, no new scan)
Answered 2 of b1's 4 cheap open questions off the existing 158-event KB:
- **Manual vs auto DIFFER:** AUTO fires ~169K (tight: min 167,004 max 191,421
  mean 168,999 median 167,998, n=149). MANUAL /compact fires EARLIER + more
  variable: min 129,377 max 158,363 mean 142,387 (n=8) - users compact before
  the cliff. durationMs ~95s auto / ~85s manual.
- **postTokens summary budget is NOT fixed:** AUTO post min 5,493 max 16,813
  mean 9,633 median 9,320; MANUAL post min 6,774 max 10,884 mean 8,639. So the
  post-compaction summary is variable (~5-17K), centering ~9-10K - NOT the
  ~12-13K guessed earlier. (The one live b1 event's 12,826 was on the high side.)
- STILL OPEN (not cheap): does ~169K shift on the 1M-context model? (needs a 1M
  session's events). What does preCompactDiscoveredTools encode? (harvester does
  not yet store that field; would need a re-harvest to capture it).

## KEY FINDINGS SO FAR (2026-06-06)
1. **A real compaction happened: b1 compacted** at file size ~901,963 bytes,
   474 lines, ~90,587 message-tokens, ~225,490 file-bytes/4 tokens, 56 tool calls.
2. **Our structural detector found NO marker** in b1's transcript right after the
   compaction (no isCompactSummary, no type=summary, no subtype~compact; only
   system/subtype=stop_hook_summary present). MEANING: either the compaction
   summary line is written LATER (after b1's next turn) or it is NOT stored in
   the .jsonl the way we assumed. ACTION FOR NEXT SESSION: re-scan b1's project
   dir for (a) a NEW .jsonl file created at compaction time, or (b) a new
   line/summary appearing after b1 takes another turn. Find the REAL marker.
3. **Both token proxies are biased**: message-text/4 UNDERCOUNTS (it omits the
   large FIXED overhead always in context: system prompt + the very large
   CLAUDE.md/global2 + tool schemas + deferred-tool lists), while file-bytes/4
   OVERCOUNTS (duplicated tool results, metadata). True fill is between them.
   For b1: between ~90K and ~225K; likely ~150-190K real tokens at compaction.
4. **Web search (platform.claude.com + others):** default auto-compact fires at
   ~95% of the context window (≈190K on a 200K window). Configurable via env var
   **CLAUDE_AUTOCOMPACT_PCT_OVERRIDE** (1-100). Claude Code team (Thariq) suggests
   proactively compacting at 50-60%. Max guessed ~75%. So b1 compacting near
   ~150-190K real tokens is consistent with ~95% of a 200K window.

## OPEN DECISIONS / NEXT STEPS (in priority order)
1. **Find the real compaction marker** (see finding #2). Without it the detector
   is blind. Highest priority - re-scan b1 after its next turn.
2. **Option A (b1-approved): wire ctx_track into a Stop hook** so EVERY Pine
   session auto-logs one data point per turn -> the KB fills passively across
   days/40 sessions. Guardrails from b1: back up settings.json FIRST (done:
   `~/.claude/settings.json.bak_20260606_b2`); additive edit to the Stop array
   ONLY (do not disturb the death-spiral PreToolUse hook or the autocommit Stop
   hook); validate JSON; test; be ready to revert. NOTE the Stop hook already
   runs `bash ~/.claude/autocommit_rules.sh` - ADD ctx_track as a second hook,
   don't replace.
3. **Improve token measurement** toward true fill (account for fixed overhead).
4. **Option B (needs cost OK):** force a compaction in a throwaway isolated
   session to capture marker+threshold fast. b1 wants a $/time estimate first.
   Estimate: forcing one compaction means filling ~150-190K input tokens once;
   with prompt caching on reads, roughly ~$2-6 and ~10-20 min. MAY BE
   UNNECESSARY now that b1 compacted naturally and gave us a live datapoint.
5. **Component 6 (HOLD until marker known):** universal dated work-log hook -
   the actual mitigation (a log that survives compaction).

## SAFETY
No irreversible actions without Max. Commit+push from C:\claude_base. If blocked,
post a question to the board and wait. Backups before editing shared config.
