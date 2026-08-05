# Scribe handover - milestone 5 (~382K tokens)
# session: 20260618_hungry_easley_b15e0d_fcea422d
# cwd: C:\claude_base\.claude\worktrees\hungry-easley-b15e0d
# written: 2026-06-18 17:53:48 by deepseek-v4-pro

# HANDOVER - b27worker (first-sung-line identification for Tamza catalog)

## GOAL (Max's words)

Identify each Tamza performance by its **first sung line** - not the announcer's spoken intro or song title. The first sung lyric becomes the catalog identity. Output goes into `verified_first_lines_<vid>.json` (keyed `"vid|sec": {first_line, performer}`), which b15merger's publisher auto-ingests. Three non-publish tags: INTRO-ONLY (no singing in segment), POEM (recited, not sung), VERIFY (too garbled to be confident). Only bare SUNG lines with an actual first_line string get published - everything else is HELD.

This is the **publish-blocking critical path** in the 3-path go-live gate (A: canon_v03 full-text match, B: clear spoken-intro attribution, C: intro-performer name matches resolved_performers DB; else HELD). The first-line ID feeds path B/C.

**Cost rule (hard):** Never Opus API sub-agents. DeepSeek-nonflash only for batch. Full run ~$12 runs by Max.

---

## DECISIONS + WHY

### 1. Hand-pilot first, scale later - not the reverse
B26 ordered a small hand-pilot (10-15 segments) before any batch run, so the method could be spot-checked. I (Opus, in-session) read actual transcript spans myself. This caught the core trap early: **canonical/famous-lyric drift** (my v01 "corrected" garbled heard words into the textbook lyric - e.g. "??? ??? ? ??? ????" became the famous "??? ??? ? ??? ?????"). B26 caught it in spot-check. Fixed in v02 faithful redo.

### 2. DeepSeek as the scale runner (deepseek-chat, V3 non-flash)
Config grabbed from the existing segmenter (`seg_phase1_v01.py`): model `deepseek-chat`, key from ssh folder, cheap pricing. Built `firstline_ds4_v01.py` as the batch runner. Key design choices:
- **Dry-run mode** (`--dry-run`) writes previews only, never the real output file (had a bug where dry-run clobbered my hand pilot - caught same-turn, restored, fixed)
- **Staging suffix system:** `--suffix __ds4pilot6` writes to `verified_first_lines_<vid>__ds4pilot6.json` - b15merger's publisher ignores files with double-underscore, so unverified DeepSeek output can never auto-publish
- **Resumable:** skips videos that already have the target output file
- **Cost cap + report:** tracks actual API spend and reports it

### 3. Prompt iteration settled at v6 (after v7 regression)
Six pilot passes on the 3-video set (pX_1m8DlMbA 47 segs, 2fEUd_iqJ3A 11 segs, 6sGQz2wB3pg 5 segs):

| Version | Agreement with hand | Key fix |
|---------|-------------------|---------|
| v1 | 29/47 | Initial (canonical drift spotted by B26) |
| v2 | 35/47 | Tightened POEM detection |
| v3 | 35/47 | Added spoken POEM cues |
| v4 | 36/47 | +deterministic code override for reading-verbs |
| v5 | 39/47 | Strengthened INTRO-ONLY against host/MC banter |
| **v6** | **41/47** | **Forced chronologically-first sung words (no skipping ahead to recognizable line)** |
| v7 | ~38/47 | Regressed - reverted to v6 |

**v6 is the stable best.** v7 lost ground across multiple metrics (host-talk leak 0?3, POEM 7?6). Single-call DeepSeek variance ceiling hit - further prompt tweaks just trade errors.

### 4. Deterministic POEM override (code, not prompt)
Added a code-level rule in `firstline_ds4_v01.py`: if the segment transcript contains reading-verb cues (??????/?????/??????/?????? - specifically NOT bare "?????" which means song-authorship), force-tag POEM regardless of what DeepSeek returned. This is deterministic, zero false positives, and catches the two worst run-on-poem cases. Combined with DS4's own POEM detection, recall is 7/8.

### 5. Wake system bug discovered
Cold wakes don't work reliably. My session had no `.signal` file in `wake/signals/`. bcast reports "FORCE-WOKEN" from the stored id?session mapping but never verifies a live process consumed it. Once I dropped the timer (per "disarm idle" order), I became genuinely unreachable. **ScheduleWakeup with the autonomous-loop sentinel is the reliable fallback.** The timer should never be disarmed until cold-wake is proven.

### 6. Archive cleanup plan (completed but unsigned)
Built `ARCHIVE_CLEANUP_PLAN_v01.md`: 55 leftover scripts + 2 stale data files to move into per-folder `archive/` subdirs. Safety-checked all cross-imports (no live script imports any leftover). One conflict: `_batch_aligner_v01.py` - doc says archive, b15M hasn't confirmed. Committed to branch `claude/hungry-easley-b15e0d`, NOT merged to master (main repo has other sessions' uncommitted work). Holding for owner sign-off.

### 7. Master merge avoidance
Main checkout at `C:/claude_base/` has a large pile of uncommitted/untracked sibling-session work. Merging there would disturb other sessions. My branch is pushed to remote and the plan is delivered via board post. Max said he doesn't care about the technical detail - sign-off is on the board with B26.

---

## CURRENT STATE

**First-line method is finalized** (v6 prompt + deterministic POEM override). Proven on a 3-video pilot (~$0.15 spent). Key metrics from v6 on the anchor video pX_1m8DlMbA:
- 41/47 agreement with my hand pilot
- 0/7 host-talk-as-SUNG leaks (the ~7-8% leak b15merger flagged is gone)
- 7/8 POEM detection (only one genuinely ambiguous case: 3734, cue-less/borderline)
- Zero false-POEM (no song mislabeled as poem)
- Zero canonical drift (the seg09 famous-lyric-substitution disaster is fixed)
- seg41 mis-picks a later verse of a repetitive-lyric song, but the text is *faithful heard text*, not
