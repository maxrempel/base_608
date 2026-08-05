# Scribe handover - milestone 9 (~140K tokens)
# session: 20260615_elegant_lewin_cab1b0_c1c9c667
# cwd: C:\claude_base\.claude\worktrees\elegant-lewin-cab1b0
# written: 2026-06-15 23:39:35 by deepseek-v4-pro

# HANDOVER - b15B (song-timing mapper, "b" team)

---

## GOAL (in Max's own words)

Build the annotator/mapper that produces timecoder drafts - given a video's song boundaries, match each segment against the frequent-song canon and emit: timing, song identity (first sung line), composer/poet (as "X or Y?" when ambiguous), performer candidates. Everything with question marks where uncertain. **Imperfect is fine.** Then pilot it, spot-check the real data, do many rounds of eyeballing + optimization, and scale ~4? each round.

Overarching marching orders: "you know the drill now. you guys are all smart - need to coordinate and optimize."

---

## DECISIONS MADE + WHY

1. **Mapper should consume b7's boundaries, not the DeepSeek segmenter.**
   - Measured across all 7 cached pilot videos (260 ground-truth songs): b7 boundaries hit **90% recall**, DeepSeek seg_phase1 hit **73%**. The worst DeepSeek videos flip hard with b7 (43?97%, 67?98%, 68?93%).
   - Tuning the DeepSeek splitter is wasting time on a 73% ceiling when b7 already gives 90%. The mapper's input should be b7's `song_timing.json`.

2. **QC/spot-check partner role chosen to avoid collision with b15M.**
   - b15M is actively producing the annotator draft (not lazy). Their `draft_PtfcXsg_Ad8` already existed in the annotator dir. To avoid clobbering, b15B wrote read-only QC scripts with distinct filenames.

3. **Multi-video benchmark, not single-video.**
   - Max hammered this: pilot ? eyeball ? optimize, not blind scaling. b15B initially only checked one video; course-corrected to use all 7 cached pilots (`seg_phase1_*.json`) matching against their ground-truth `song_timing.json` entries.

4. **Segmentation recall is the bottleneck, not identification quality.**
   - Pilot QC on PtfcXsg_Ad8: 56 DeepSeek segments vs 81 ground-truth songs = 25 songs simply missing. 27 ground-truth song-starts had no matching segment boundary. 8 consecutive segments all got "Vladimir Vysotsky" (intro-propagation bug). A song never split out can never be correctly named.

5. **Git worktree is shared - do not touch siblings' unstaged files.**
   - Several commits were pushed with `git add -f` (since `_work/` is gitignored) while leaving siblings' in-progress files untouched.

---

## CURRENT STATE

### Completed and pushed
- **annotate_video_v01.py** - scaffold annotator, validated on sample video `5llciuQw7S8` (commit `fc211f0c`, master)
- **qc_pilot_b15B.py** - QC report on b15M's PtfcXsg_Ad8 draft, identifying the segmentation-recall bottleneck and the Vysotsky propagation bug
- **recall_bench_b15B.py** - measures DeepSeek segmentation recall across all 7 cached pilots
- **b7_vs_ds_recall_b15B.py** - head-to-head b7 boundaries vs DeepSeek on the same 7 videos (commit `abe98bf0`, master)

### Broadcast board state
- b15B posted the 90% vs 73% finding to b15M and asked: should I help B15A with ending-tolerant cluster-matching, or stay on the mapper feeding b7 boundaries?
- b15M has not yet responded.

### Autonomous loop
- Timer armed (dynamic pacing, 1200-1800s). Next tick will re-check the board for b15M's reply.

---

## EXACT NEXT STEP

**On wake or next session**, check the branch bulletin board for b15M's response:
```bash
python C:/claude_base/branch_bulletin/bcast.py catchup
```

If b15M has responded, follow orders. If silent, the unresolved fork is:

- **Option A**: Help B15A build the cluster-matching that tolerates ragged song endings (Max said this is the quality gap now - the song's *middle* carries enough signal; endings are noisy).
- **Option B**: Repoint the mapper to consume b7's `song_timing.json` boundaries and validate annotation quality against the 7 pilots.

**Lean toward whichever continues established work without inventing new scope.** The find-better-segmentation work is done (answer: use b7). The annotator draft quality work is now gated on either b15M's repointing or B15A's matching improvement.

---

## OPEN QUESTIONS (awaiting user or b15M)

1. **Mapper repointing**: Does b15M want the annotator to consume b7's `song_timing.json` instead of DeepSeek seg_phase1? (b15B recommended this.)
2. **B15A collaboration**: Should b15B jump into the ending-tolerant cluster-matching problem (Max's stated priority)?
3. **Unindexed videos (~1049)**: Board mentioned this open ask - not assigned to b15B yet, but relevant if b7 is already crunching all videos.

---

## KEY PATHS AND IDS

| What | Path |
|---|---|
| **Work root** | `C:/claude_base/tools/tamza_songs/pipeline/song_timing/from_scratch_idx/_work/` |
| **Annotator dir** | `.../_work/annotator/` |
| **Merge pilot dir** (canon + consensus) | `.../_work/merge_pilot/` |
| **Frequent-song canon** | `.../_work/merge_pilot/canon_frequent_v02_llmmerged.json` |
| **Consensus song DB** | `.../_work/merge_pilot/consensus_song_db_exactDedup.json` |
| **b7's song boundaries** | `song_timing.json` (keys: `vid:offset`, fields: `seg_start`/`seg_end` in seconds) |
| **DeepSeek segments** (7 cached pilots) | `seg_phase1_{videoId}.json` - each has `start`/`end`/`performer`/`author`/`title`/`confidence` |
| **b15M's draft** | `.../_work/annotator/draft_PtfcXsg_Ad8` - b15M is actively updating this |
| **b15B's QC + bench scripts** | `qc_pilot_b15B.py`, `recall_bench_b15B.py`, `b7_vs_ds_recall_b15B.py` |
| **Branch bulletin** | `python C:/claude_base/branch_bulletin/bcast.py` (post/catchup/whoami) |
| **Worklog** | `python C:/claude_base/compaction_kb/scripts/worklog.py log` |
| **Git repo** | `C:/claude_base` (master branch, shared worktree) |
| **Latest commit** | `abe98bf0` - bench + QC scripts |

### Video IDs for the 7-pilot bench (in recall order):
best: 0oNb4jOFf2g (97%), Sh11FXhH7rw (43%?97% w/ b7), PtfcXsg_Ad8 (67%?98%), UOA7OovhsC8, usdMyDhDUV0 (94%), gD_RmnDdKM0 (68%?93%), worst baseline was 43% on Sh11FXhH7rw.

---

## GOTCHAS

- **Canon join key**: canon `members` use offsets like `19450`; song_timing keys are `vid:offset`. They join correctly but look different. Segment text is NOT in the splitter output - need transcript for text-based matching.
- **Git: `_work/` is gitignored** - must use `git add -f` to commit scripts. Siblings' in-progress files exist in the shared worktree; never `git add .` or touch their changes.
- **b15M parallel work**: b15M is writing to `draft_PtfcXsg_Ad8` in the same annotator dir. b15B's own files use distinct names (`qc_*`, `recall_*`, `b7_vs_*`) to avoid collision.
- **Hook sensitivity**: repeated `cd ... && python` command patterns trigger the duplication hook. Use full absolute paths instead.
- **UTF-8 output**: must set `PYTHONIOENCODING=utf-8` for Cyrillic text to render.
- **Budget**: $15 was noted. Spending has been on reads/bench scripts - no API-heavy calls.
- **Segmentation segments have NO text field** - to match against canon by first-line text, the transcript (Whisper output or similar) is needed; the segments only carry `title`/`performer`/`author`/`confidence`.
- **The Vysotsky bug** (8 consecutive segments all "Vladimir Vysotsky") is intro-propagation - one correct identification near a host introduction snowballs across subsequent segments because the splitter misplaces boundaries and the matcher inherits the wrong context window.
