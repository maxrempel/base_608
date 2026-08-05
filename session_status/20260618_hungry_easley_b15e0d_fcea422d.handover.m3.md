# Scribe handover - milestone 3 (~246K tokens)
# session: 20260618_hungry_easley_b15e0d_fcea422d
# cwd: C:\claude_base\.claude\worktrees\hungry-easley-b15e0d
# written: 2026-06-18 14:19:58 by deepseek-v4-pro

# HANDOVER - B27worker session (hungry-easley-b15e0d)

---

## GOAL (Max's words, from the board)
**"Verified first-SUNG-line" duty**: for every video segment in the Tamza pipeline, extract the actual first sung lyric (not the announcer's spoken intro, not the song title someone gave it). The identity of a performance = its first sung words. Tag talk-only segments as INTRO-ONLY, recited poems as POEM, too-garbled audio as VERIFY. Output goes into `timecoder_handover/verified_first_lines_<vid>.json` for b15merger to auto-ingest into the publisher.

The deeper product goal (per Max's radio complaint): the performer-facing radio should surface fresh, correctly-titled songs (not 2-min-capped, not mislabelled with announcer chatter).

---

## DECISIONS + WHY

1. **Faithful-to-heard, never canonical drift.** B26 corrected b27's v01 sample - it had silently "corrected" sung lines to the famous/poetry-book version of the lyric (e.g. writing "?????? ???????????" instead of the actually-sung "????? ???????????"). Rule locked in: transcribe what was SUNG, garbled and all, never substitute the textbook version. Root of the bug: the annotator pipeline originally ran Opus sub-agents with instructions that nudged toward "identify the song," which triggered the LLM's internal knowledge of the canonical poem. 

2. **No Opus API sub-agents - use DS4-nonflash for scale.** Max was furious about a prior $40 Opus API sub-agent bill for the first-line work. B26's standing order: the hand-pilot is done in-session (free), the full ~778-video run goes on DeepSeek non-flash, cost-capped at ~$12. Never spawn Opus sub-agents for this task.

3. **Autonomous self-wake (ScheduleWakeup ~240s) must stay armed.** A cold-wake bug was discovered: bcast reports "FORCE-WOKEN" but no actual signal file is consumed by a live listener. Root cause in c6's wake delivery. Until fixed, the reliable fallback is a 4-min self-wake timer that re-arms every cycle. Without it, b27 went completely dark for ~25 minutes because the peer-idle disarm rule killed its timer and cold-wake never delivered.

4. **Archive cleanup plan is built but NOT executed.** B26's original task for b27 was to produce an analysis-only plan (move nothing) flagging 55 stale scripts + 2 data files across the pipeline. Safety cross-check via import tracing proved no live script imports any leftover. Plan committed to b27's branch, not merged to master (main checkout has other sessions' uncommitted work - merging could disturb them). Sign-off stalled: b15M hasn't answered the `_batch_aligner_v01.py` keep-or-archive question.

5. **Schema for verified_first_lines JSON**: `"<vid>|<sec>": {"first_line": <string or null for INTRO-ONLY>, "performer": <string>}`. INTRO-ONLY segments get `first_line: null` and the announcer/performer name. POEM segments get the first recited line. VERIFY segments get a best-effort line with a VERIFY flag. The schema was reverse-engineered from B26's existing `verified_first_lines_pX_1m8DlMbA.json` (now backed up as obsolete).

---

## CURRENT STATE

### Done
- **Hand-pilot COMPLETE on pX_1m8DlMbA** (2020 concert, 47 segments). Output written to `timecoder_handover/verified_first_lines_pX_1m8DlMbA.json`. Breakdown: 28 sung, 8 recited poems, 4 too-garbled (VERIFY), 7 talk-only (INTRO-ONLY). The old file was backed up to `archive/obsolete_verified_first_lines_pX_1m8DlMbA.json`.
- **FAITHFUL v02 sample** (`firstline_SAMPLE_b27_pX_1m8DlMbA_v02_FAITHFUL.md`) posted to B26 for spot-check. Supersedes the canonical-drift v01.
- **Archive cleanup plan** (`ARCHIVE_CLEANUP_PLAN_v01.md`) built, committed, pushed to remote branch `claude/hungry-easley-b15e0d`. Not merged.
- **Wake bug diagnosed** - documented the false-positive "FORCE-WOKEN" signal; armed the autonomous 4-min timer as the reliable alternative.

### In Flight / Holding
- **B26's spot-check verdict** on the pX faithful pilot - this is THE gate before anything scales.
- **POEM/VERIFY tag handling** - waiting on b15merger to confirm how the publisher treats these (a poem must never appear as a song titled "POEM").
- **Archive plan sign-off** - stalled on b15M's silence about `_batch_aligner_v01.py`.

---

## EXACT NEXT STEP

1. **4-min timer fires** ? run `bcast.py read` to check for B26's spot-check verdict on the faithful first-line redo.
2. **If approved**: wire the DS4-nonflash scale run across all videos (never Opus API). Script should read each video's segments + transcript, extract the first SUNG line faithfully (full segment, not just the start), output per-video `verified_first_lines_<vid>.json` into `timecoder_handover/`.
3. **If not yet approved**: re-arm the 4-min timer and hold.

The hand-pilot method is proven self-contained - no external API needed for the in-session pilot. The scale script needs to replicate the same logic (skip spoken intros, stay faithful to garbled heard text, tag poems/talk-only/garbled) but callable on DS4.

---

## OPEN QUESTIONS (awaiting Max or board)

1. **B26's spot-check of the pX faithful pilot** - is the method approved?
2. **b15merger: how to handle POEM and VERIFY tags** in the publisher ingest? Does POEM get its own category, or is it excluded from the song radio? Does VERIFY block publishing until a human checks it?
3. **b15M: `_batch_aligner_v01.py`** - keep or archive? This is the one conflict flagged in the archive cleanup plan. b15M has not responded.
4. **Master merge for archive plan** - Max deferred (too technical). Plan stays on b27's branch until an owner merges it.

---

## KEY PATHS / IDs

| What | Path |
|------|------|
| **Session worktree** | `C:\claude_base\.claude\worktrees\hungry-easley-b15e0d` |
| **Session git branch** | `claude/hungry-easley-b15e0d` (pushed, not merged) |
| **Session bcast ID** | `fcea422d` - mapped as b27 in `state/b27_session.txt` |
| **Pipeline root** | `C:\claude_base\tools\tamza_songs\pipeline\` |
| **Verified first-lines output** | `.../pipeline/timecoder_handover/verified_first_lines_<vid>.json` |
| **pX pilot JSON (new, correct)** | `.../timecoder_handover/verified_first_lines_pX_1m8DlMbA.json` |
| **pX pilot backup (old, wrong)** | `.../timecoder_handover/archive/obsolete_verified_first_lines_pX_1m8DlMbA.json` |
| **FAITHFUL sample doc** | `.../timecoder_handover/firstline_SAMPLE_b27_pX_1m8DlMbA_v02_FAITHFUL.md` |
| **Archive cleanup plan** | `.../pipeline/ARCHIVE_CLEANUP_PLAN_v01.md` |
| **Span-extraction helper** | `.../pipeline/song_timing/from_scratch_idx/_work/annotator/_firstline_sample_b27.py` |
| **Transcripts (main checkout)** | `C:\claude_base\tools\tamza_songs\pipeline\song_timing\transcripts\` (1225 files) |
| **Segments (main checkout)** | `C:\claude_base\tools\tamza_songs\pipeline\song_timing\from_scratch_idx\_work\segments\` (772 files) |
| **Workflow doc** | `.../pipeline/CURRENT_WORKFLOW_v01_tomemex.md` |
| **Broadcast board** | `python C:\claude_base\branch_bulletin\bcast.py read` |
| **Worklog** | `python C:\claude_base\compaction_kb\scripts\worklog.py log "..."` |
| **Schema** | `"<vid>|<sec>": {"first_line": <string|null>, "performer": <string>}` - INTRO-ONLY has `first_line: null`, POEM has recited text, VERIFY has garbled best-effort |

---

## GOTCHAS

1. **Canonical drift is the #1 trap.** Never let the LLM substitute the famous/poetry-book lyric for what was actually sung. The heard text may be garbled, misremembered, or a variant - write it down as-is. This is the mistake the v01 sample made and the old pX JSON (B26's earlier Opus-subagent run) also had.

2. **Wake delivery is broken for cold sessions.** bcast reports "FORCE-WOKEN" but the signal file is never consumed by a live listener. The ONLY reliable path is the `ScheduleWakeup` self-wake timer (~240s, re-armed on every wake). Never disarm the timer on an idle worker - that's what caused b27's 25-min blackout.

3. **Do NOT merge to master from this worktree.** The main checkout at `C:\claude_base\tools\` has uncommitted/untracked sibling session work. Merging from the worktree could disturb other sessions' live state. Push to branch is fine; merge must be done from a clean state.

4. **No Opus API sub-agents - period.** Max lost $40 on this once already. The scale run goes on DeepSeek-nonflash. The hand-pilot is free (in-session Opus reading files). This prohibition should probably go into global2 rules.

5. **Cyrillic encoding trap.** Windows console is cp1252, not UTF-8. All Python reads/writes of transcripts/segments need `PYTHONIOENCODING=utf-8` or `PYTHONUTF8=1`, and debug output should go to a UTF-8 file (e.g. `/tmp/`), never to stdout in the console.

6. **Some segments are recited poems, not songs.** They need their own classification (POEM), not shoehorned into a song slot, or the radio will play a poetry recitation as a "song."

7. **The full run must read the ENTIRE segment transcript**, not just the first few lines. Some segments have long spoken intros (2+ minutes) before the singing starts. Scanning only the beginning produces false INTRO-ONLY labels.

8. **B26 is in charge of b27's tasking** - Max explicitly deferred technical decisions to B26 on the board. Don't take direct tasking from Max for this lane unless it comes through B26 or is clearly a new task.
