# Scribe handover - milestone 11 (~166K tokens)
# session: 20260615_competent_solomon_47fe23_c1b091fe
# cwd: C:\claude_base\.claude\worktrees\competent-solomon-47fe23
# written: 2026-06-15 17:15:41 by deepseek-v4-pro

# Handover: B15 - Canonical Consensus Song-Text DB (Tamza Archive)

---

## GOAL (Max's words)

Build the **canonical database of consensi** - a clean, deduplicated song-text reference for the Tamza concert archive. The job evolved through several corrections and is now crystal-clear:

- **Scope-locked by Max:** B15 does ONLY the canon consensus DB. b6 and b7 own song start/end timing. B15 is entirely OUT of timing.
- **Full-text merge, not first-line matching.** The earlier first-line sliding-window approach was declared wrong and is dead. The correct strategy: cluster performances into songs by full-text similarity (never by title), collapse multiple noisy performances of the same song into one consensus text, and build a clean database that Phase 2 can match against.
- **Pilot then scale.** Experiment with various clustering approaches on small samples, validate against human ground truth (queue.json), then scale the winning method.
- **Most recent instruction (end of transcript):** BEFORE spending time or money on wholesale retranscription, first sample the transcripts thoroughly and estimate how bad they really are. Maybe they can be QC'd and only a few re-transcribed. The $40 transcription budget and local-Whisper-on-Sol plan are paused until this assessment is done.

---

## DECISIONS + WHY

1. **Strategy pivot - first-line ? segment-then-full-text.** Max: "stupid - it is not the correct strategy. Assuming the transcript is 50% garbage the correct strategy is to walk through the whole thing and separate semantically with DS." A tiny transient first line is too fragile in noisy ASR; a full song-text block survives garbling.

2. **Scope lock - B15 = canon DB only.** After reading the board and seeing b6/b7's shared-file clobber mess (three conflicting rule-versions all writing to `song_timing.json`), Max explicitly reassigned timing to b6/b7 and restricted B15 to the consensus text DB. Logged and posted on the board.

3. **Titles are TOTAL JUNK for merging.** Max's verdict after seeing the QC results. The existing corpus (`song_corpus_v01.json`) groups performances by `title_norm`, which wrongly merges distinct songs sharing generic titles (????????????, ???????, etc.). Any rebuild must cluster by full-text similarity, never title.

4. **DeepSeek = semantics only, never timing.** LLMs can't reliably track time points. When DeepSeek is used (for segment labelling, performer/author capture), it must not be asked for timestamps.

5. **QC every LLM step.** Standing mandate: Opus independently re-does the same task on a sample and compares. For assembly steps, spot-check SOURCE vs RESULT, not just row counts. Max caught that the corpus was assembled without any source-vs-result check - confirmed as QC debt.

6. **Transcription budget: $40, must work with Russian, 4 weeks ok, slow acceptable.** Local faster-whisper large-v3 on Sol = $0, fits all constraints. But Max's last instruction puts this on hold - first assess whether retranscription is even needed.

7. **"Deterministic" - banned.** Max objected to both the word and the approach (a hand-built timing guesser using duration arithmetic to recover missed songs). Dropped entirely; timing is b6/b7's job anyway.

---

## CURRENT STATE

**What's done and pushed to master:**

- **Consensus corpus built** (`_work/song_corpus_v01.json`, 91MB, gitignored): 13,670 songs, 21,218 performances, 3,057 with multi-performance consensus. Built from noisy transcripts grouped by title_norm (WRONG - titles are junk for merging, per Max).
- **First-line matching experiments** (v01-v04, ds_confirm_pilot v01-v02): ALL NOW SUPERSEDED by the strategy pivot. Valuable only as dead ends documented in the algorithm plan doc.
- **DeepSeek Phase-1 segmentation tested** on one video (PtfcXsg_Ad8, 81-song marathon): 96% boundary precision, 93% performer-name accuracy, 67% recall (misses songs in dense stretches). Output at `_work/seg_phase1_PtfcXsg_Ad8.json`.
- **Corpus QC done** (`corpus_qc_v01.py`): Confirmed Max's prediction - the corpus has real problems. Only 3,070 of 13,670 songs have multi-perf consensus; some consensus texts are ASR garbage (Okudzhava romance contains "beyonce/russian/tusya"); title-based grouping merges different songs.
- **Algorithm plan doc saved**: `from_scratch_ALGORITHM_PLAN_v01_tomemex.md` - the authoritative spec. Contains the full two-phase architecture, the QC mandate, the titles-are-junk lesson, and all the dead ends.
- **QC scorer for segmentation**: `seg_score_v01.py` - matches DeepSeek segments against queue.json ground truth.
- **faster-whisper installation on Sol was in progress** when Max diverted to this branch's new task. Partially installed in `~/whisper_env/` on Sol (192.168.1.113, key at `~/.ssh/sol_key`). NVIDIA driver 535, Quadro P400 2GB VRAM, ffmpeg present.

**The current pivot (end of transcript):** Max said "don't continue" the transcription path - another branch is doing that. B15 should instead **sample the transcripts thoroughly and estimate whether they are that bad that retranscription is needed at all. Maybe only a few need redoing.**

---

## EXACT NEXT STEP

**Sample the transcripts thoroughly.** Inspect a representative sample of the 452 local transcript files. For each sampled video, assess:

- Word error rate / garbled stretches vs. clean stretches
- How much English/hallucinated text appears in Russian content (the "beyonce/russian/tusya" problem)
- Whether the ASR is uniformly bad or mostly ok with specific failure modes
- How many videos have transcripts bad enough to warrant re-transcription, vs. how many are usable as-is

Build a quantitative report: what fraction of the archive actually needs redoing, and what fraction is good enough for full-text clustering and consensus-building. Output should directly answer "do we need the $40/4-week re-transcription or not?"

Then report back to Max. The full-text merge pilot (clustering performances by text similarity) is the natural next thing after the transcript-quality assessment.

---

## OPEN QUESTIONS (awaiting Max)

1. **Where are Max's clean lyrics?** He mentioned having them, but the file path was never given. Crucial for building a clean canon DB.
2. **Canon DB material source:** Even if transcripts are "good enough," a clean-lyrics canon (Max's lyrics + web-sourced) beats even perfect ASR. Does the clean-lyrics canon exist somewhere, or does it need building?
3. **Sol stability for long runs**: Sol has a failing RAM stick (kernel panic Jun 13, flagged untrustworthy). Is it safe for a 4-week transcription grind? The current task (transcript sampling) doesn't need Sol at all.
4. **Full-text merge approach preference**: Once transcripts are sampled, does Max want rapidfuzz threshold clustering, TF-IDF + cosine similarity, MinHash/LSH, or a hybrid? The instruction was "experiment, do various approaches" - this is authorized.

---

## KEY PATHS AND IDS

- **Project root:** `C:/claude_base/tools/tamza_songs/pipeline/song_timing/from_scratch_idx/`
- **Algorithm plan (AUTHORITATIVE):** `from_scratch_ALGORITHM_PLAN_v01_tomemex.md`
- **Existing corpus (flawed, title-grouped):** `_work/song_corpus_v01.json` (91MB, gitignored - `_work/` in .gitignore)
- **Ground truth:** `../queue.json` (parent dir - `C:/claude_base/tools/tamza_songs/pipeline/song_timing/queue.json`). Key fields per song row: `start` (seconds), `song` (curated name), `performer`, `first_line` (filled for 69% of rows), `date`.
- **Transcripts:** `../transcripts/<vid>.json` - each is a list of `{t: start_sec, d: duration_sec, x: text}`
- **DeepSeek API key:** `C:/Users/maxre/Nextcloud/zSyncMain/ssh/deepseek_api_key_20260226.txt` (36 bytes, verified present)
- **DeepSeek config:** model=`deepseek-chat`, base_url=`https://api.deepseek.com`, pricing $0.27/1M in, $1.10/1M out
- **Board script:** `C:/claude_base/branch_bulletin/bcast.py` (whoami=catchup=read=post)
- **Durable journal:** `C:/claude_base/compaction_kb/scripts/worklog.py log "message"`
- **Session snapshot:** `C:/claude_base/compaction_kb/scripts/session_status.py report "message"`
- **Sol SSH:** `maxre@192.168.1.113`, key `~/.ssh/sol_key`, faster-whisper partially installed in `~/whisper_env/`
- **Worklog file:** `C:\claude_base\worklog\claude_base_15c30882f7.md`
- **Git remote:** `origin master` - always merge before push, push when work is validated
- **Working directory for git:** `C:/claude_base` (NOT the worktree at `C:/claude_base/.claude/worktrees/focused-wilbur-d92388`)
- **My bcast identity:** b15 (but worktree sometimes shows "b14" in whoami output - message content says b15)

---

## GOTCHAS

1. **Titles are junk for merging** - never group by title. Only full-text similarity.
2. **Don't use "deterministic"** - Max hates the word and the approach (hand-built timing guesser).
3. **DeepSeek = semantics only, never timestamps** - LLMs can't track time.
4. **QC every LLM step** - Opus spot-checks independently. Non-negotiable.
5. **Don't touch b6/b7's files** - `data.json`, `
