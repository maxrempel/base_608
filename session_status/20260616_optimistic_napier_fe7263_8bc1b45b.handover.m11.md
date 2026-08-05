# Scribe handover - milestone 11 (~169K tokens)
# session: 20260616_optimistic_napier_fe7263_8bc1b45b
# cwd: C:\claude_base\.claude\worktrees\optimistic-napier-fe7263
# written: 2026-06-16 07:50:12 by deepseek-v4-pro

# HANDOVER - B7f "freshmap" (ex-B7, song starts owner)

## GOAL (Max's words)
"All videos are transcribed by youtube. Lets split - one version of you will finish the remap of indexed. That would be B7i indexed. Another will work on the new mapping. 'freshmap' B7f - that will be you, reregister."

You are **B7f "freshmap"** - your lane is the **unindexed/unmapped videos** (~1,049+ videos that were never fully timed). B7i inherits the already-running indexed-catalog remap. Both branches share the same tooling and methods.

---

## CONTEXT: What problem we were solving
Max reported songs start on the **first sung word**, chopping off the instrumental intro (5-20s of music between the host's prose and the first lyric). The fix: start = **end of preceding PROSE** (ANY non-sung speech: MC, author commentary, banter) so the intro is included. This is called the **prose-boundary rule** or "intro-included" timing.

---

## DECISIONS MADE + WHY

### 1. Prose-boundary rule (the validated method)
- **What**: Start = the timestamp right after the LAST word of ANY prose before the song. End = timestamp right before the FIRST word of ANY prose after the song.
- **Why**: Max dictated this (multiple iterations): "????? ? ???????????? - ?????? ????... ????? ????? - ????????", "?????? ?????? ???? ????????", "?????? ? ??????? ????? ?????????? ????? ?????". Validated 10/10 on Max's own songs, then 3 waves of 5 = 15 QC'd.
- **Implementation**: Russian prompt v2 in `map_core.py` `_build_prompt()`, with ??????? ?????? (prose/verse split), ????????? ??????? (quatrain end-prediction), ?????? ?? ???????????.

### 2. Model choice: deepseek-chat (cheap, non-reasoning)
- **What**: Switched from `deepseek-v4-flash` (reasoning model, ~$0.004/song, ~$95 full catalog) to `deepseek-chat` (plain V3-series, ~$0.0005/song, ~$12 full catalog).
- **Why**: Max's order: "oh shit - too expensive. Keep experimenting until you get to 30 usd for everything. Use sampling." Tested deepseek-chat+sampling vs flash on 12 validated Max songs: same start accuracy (8/12 dead-on), ~7x cheaper.
- **Grok was considered** but deepseek-chat already nailed the $30 budget, so Grok was never wired (another chat was registering it, not done yet).

### 3. 300s window cap + sampling
- **What**: Bound the transcript window fed to the AI to 300 seconds past the song's curated start, and sample every 2nd caption when the window is >40 lines.
- **Why**: A free offline scan (`analyze_windows.py`) revealed sparse-marker concerts produce 1,295-caption windows costing ~50x a normal song. The cap kills those outliers at zero quality loss. Proven via experiment.

### 4. Pipeline migrated OFF Sol
- **What**: `publish_catalog.py` no longer scp's the timing store from Sol; it reads from Pine's local `_work/song_timing.json`.
- **Why**: Sol has bad RAM (b11 diagnosed: kernel GPF under memory stress). Max said "the plan was to migrate off sol." It's unreliable for this pipeline.

### 5. Two-store architecture with overlay
- **What**: Base store `_work/song_timing.json` (all songs, what the remap rewrites) + Max overlay `_work/song_timing_max_v2.json` (Max's own 670 songs, prose-boundary validated, WINS on key collision).
- **Why**: The overlay was b6's work, already proven correct on Max's songs. Baked into `build_catalog.py` so the cron publisher always merges `{**base, **overlay}` - overlay wins. This prevents the auto-publisher from ever reverting Max's fix.

### 6. Atomic writes (cron-safe)
- **What**: `save_atomic()` writes to a temp file then `os.replace()` (atomic rename on Windows).
- **Why**: The publish cron reads the store every 3h. An atomic rename prevents torn reads. Confirmed by both b21 and me, and cleared by the safety watcher.

---

## CURRENT STATE

### Live on tamza.com
- **Max's own ~670 songs**: prose-boundary starts LIVE and DURABLE (overlay baked into the publish pipeline, can never be reverted by a cron run).
- **Rest of catalog (old songs)**: the indexed remap (B7i's lane) is in progress to fix them too. At last check the remap was ~33% done (6,992/21,438), $3.77 spent, then laptop slept. Relaunched as PID 5656, now resumed.

### The remap (B7i inherits this)
- **Script**: `C:\claude_base\tools\tamza_songs\pipeline\song_timing\map_all_v2.py`
- **Running**: PID 5656 (PowerShell Start-Process, window hidden), `$env:PYTHONIOENCODING='utf-8'`
- **Progress log**: `_work/map_all_v2.log`
- **State file**: `_work/map_all_v2_state.json` (keys already done, skips on resume)
- **Config**: `deepseek-chat`, TOKEN_BUDGETS=(2000,), 300s window cap, sampling every 2nd caption if >40 lines, hard cap --cap-usd 30
- **Spent**: ~$3.77 so far, on track ~$12 total
- **Resumable**: yes - if process dies, just run `python map_all_v2.py --cap-usd 30` again; it skips done keys
- **On finish**: run `python ../scripts/publish_catalog.py` (from pipeline/scripts/) to ship the new timings live through the proper guard+gating chain

### The auto-publisher (ongoing, independent)
- **Task**: `kartoteka_publish` (Windows Scheduled Task, every 3h at :15)
- **Runs**: `C:\Users\maxre\AppData\Local\Python\pythoncore-3.14-64\pythonw.exe C:\claude_base\tools\tamza_songs\pipeline\scripts\publish_catalog.py --log`
- **Log**: `pipeline/logs/publish.log`
- **Chain**: STORE ? BUILD (build_catalog.py, now merges overlay) ? GUARD (guard_starts.py) ? PAINT (manual_overrides.json) ? GATE (ROW_FLOOR=26000, END_FLOOR=20000) ? DEPLOY (data.json to R2)
- **No-op guard**: skips deploy if sha256 of candidate matches `.last_published_sha`

### Defect class (known, not yet fixed)
- **~274 catalog entries are pure SPEECH**, not songs (??????????, ???????, ??????????, ????, birthday greetings). These get mapped to wrong starts.
- **guard_starts.py** already reverts the worst ones (those that jump to the next song's slot). The residual (speech mapped to [??????] inside its own slot) is unfixed.
- **b21 has a flag script** (`qc_b21/flag_bad_starts_v02.py`) that identifies them. On remap finish, the handoff plan was: b21 hands b7 the residual queue, b7 nulls the bad starts so those entries keep the safe 120s player cap.

### Files that were NOT yet committed when the split happened
- `_work/map_all_v2.log`, `_work/map_all_v2_state.json` - runtime state, gitignored
- `_work/exp_cheap.py`, `_work/analyze_windows.py`, `_work/qc_starts.py` - investigation/QC throwaway scripts, not committed
- `_work/investigate_starts.py`, `_work/compare_v3_live.py`, `_work/investigate_v3.py`, `_work/verify_live_r2.py`, `_work/verify_live_starts.py` - earlier investigation scripts, not committed

---

## EXACT NEXT STEP (for B7f "freshmap")

1. **Re-register on the coordination board**: `python "C:/claude_base/branch_bulletin/bcast.py" whoami b7f` (NEVER cd before bcast - it mislabels the post). Post: "B7f freshmap registered - working on the unmapped/unindexed videos. B7i owns the indexed remap."

2. **Understand what "freshmap" means**: Max said "all videos are transcribed by youtube." So the unindexed videos HAVE auto-captions we can harvest. The task is to:
   - Get YouTube transcripts for the ~1,049 unindexed videos
   - Run the prose-boundary timing mapper on them
   - Feed the results into the catalog + store

3. **Find the unindexed video set**: b15's indexing team was working on ~1,049 unindexed videos. Their code is in `pipeline/song_timing/from_scratch_idx/`. Query them or read their state to get the video ID list.

4. **Transcript harvesting**: Use the same safe method from `timing_pipeline.py` - `youtube_transcript_api`, Russian captions, NEVER translate, polite random gaps. Or run on Sol (if it's stable - check with b11) to avoid hitting your home IP.

5. **Timing**: Use the validated prose-boundary method from `map_core.py` / `map_max_v2.py` (Russian prompt, deepseek-chat, 300s window cap, window sampling). Feed each video's transcript through the mapper, write results to the store.

6. **Publish**: The canonical path is `publish_catalog.py` (runs the full guarded chain). B7i's remap is also writing the same base store - coordinate via bcast to avoid concurrent writes (my `map_all_v2.py` does per-song atomic saves, so concurrent writes from different PIDs could interleave).

---

## OPEN QUESTIONS (for Max, when he engages)

? **Scope of "freshmap"**: "All videos are transcribed by youtube" - does this mean all ~1,049 unindexed videos have auto-captions we can fetch, or only the ones YouTube chose to caption? The old remap already skips 2,643 songs with "no cached transcript" - some may genuinely lack captions. Clarify whether to transcribe those from audio (Groq/Whisper, ~$6).

? **Destination**: Do the newly-timed songs go into the existing `_work/song_timing.json` base store (merging with B7i's remap), or a separate store/file that `build_catalog.py` also merges?

? **The relayed b15 ask**: "Max says your optimized boundary crunch must ALSO cover the ~1,049 UNINDEXED videos" - is this the same as "freshmap"? If so, b15's team may already have the video list and some pipeline code.

---

## KEY PATHS

### Local (Pine)
```
C:\claude_base\tools\tamza_songs\pipeline\song_timing\
  map_core.py              - core engine (_build_prompt has the Russian prose-boundary rule, _call_model wraps DeepSeek)
  map_max_v2.py             - Max-only mapper (writes song_timing_max_v2.json overlay)
  map_all_v2.py             - full-catalog remap (writes song_timing.json base store, NOW RUNNING as PID 5656 for B7i)
  guard_starts.py           - reverts collided/backloaded/preroll starts
  apply_overrides.py        - manual_overrides.json painter (last deploy step, wins over all)
  manual_overrides.json     - empty, for Max's hand-corrections
  timing_pipeline.py        - original transcript harvest + timing pipeline
  enrich_catalog.py         - folds store into data.json
  prompt_ru_v2_design_tomemex.md - the full Russian prompt design doc
  song_timing_full_remap_cheap_20260615_v01_tomemex.md - report/method doc
  _work/
    song_timing.json          - base store (21,481+ keys, being rewritten by map_all_v2.py)
    song_timing_max_v2.json   - Max v2 overlay (670 keys, WINS on collision)
    map_all_v2.log            - B7i remap progress log
    map_all_v2_state.json     - B7i remap state {done_keys, spent}
    transcripts/              - cached YouTube transcripts (107MB, gitignored)
    exp_cheap.py              - cost experiment script (throwaway)
    analyze_windows.py        - free window/cost scanner (throwaway)
    qc_starts.py              - start QC reviewer (throwaway)

C:\claude_base\tools\tamza_songs\pipeline\scripts\
  publish_catalog.py        - canonical publisher (STORE?BUILD?GUARD?PAINT?GATE?DEPLOY), migrated OFF Sol, cron task kartoteka_publish
  build_catalog.py          - deterministic catalog builder (EDITED: now merges overlay)
  deploy_catalog.py         - R2 uploader (ONLY takes a file path as arg, NO flags - my accident!)

C:\claude_base\tools\tamza_songs\pipeline\
  output\data.json          - local build artifact
  logs\publish.log          - cron publish log
  archive\                   - live backups (data_live_backup_<ts>_<rows>rows.json)
```

### Remote (Sol, unreliable - mostly retired from this pipeline)
```
maxre@192.168.1.113 ~/song_timing/
  timing_pipeline.py        - original harvest+p
