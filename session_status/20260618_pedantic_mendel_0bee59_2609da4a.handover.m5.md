# Scribe handover - milestone 5 (~376K tokens)
# session: 20260618_pedantic_mendel_0bee59_2609da4a
# cwd: C:\claude_base\.claude\worktrees\pedantic-mendel-0bee59
# written: 2026-06-18 06:25:02 by deepseek-v4-pro

# HANDOVER - Tamza Song Pipeline (B26juniorconnector, end of overnight shift)

---

## GOAL (Max's words)

Finish the Tamza song-indexing project. The end state is a clean database plus a live website. **Newly-identified songs should go live.** Unknowns should not. The project is ~90% done; drive the remaining deploys to completion safely (don't lose/break data), coordinate the team, and produce a weekly handover for human timecoders - starting with one oldest good not-human-done video, annotated, double-checked, and delivered.

---

## DECISIONS MADE (and WHY)

### Go-live policy - 3 OR-paths
A segment goes live if it passes ANY of:
- **(A) Confident song-text match** - the lyrics match a known song in the 994-song reference
- **(B) Clear spoken intro** - the performer says "this is my song" or names the composer/poet explicitly
- **(C) Performer-name match** - the spoken intro names a performer who exists in the clean performer DB

**Why:** Path A alone catches only ~12-20% of segments (Max's machine keeps precision high). Path B and C unlock many more segments where the song is unknown but the performer is confident - the performer DB is already clean and deduplicated.

### Path A is unreliable on old/fringe videos - do NOT publish as truth
**Why:** Two independent LLM reviews found the matcher drifts to famous songs (~half wrong on an old 2020 concert). The announcer often names the author/composer in the intro, and the matcher locks onto that instead of the actual sung lyric. **Performers, by contrast, are reliable** (intros transcribe clean even from noisy ASR).

### Human-side catalog is ALREADY live
Ran `publish_catalog.py --dry-run` - verified the live catalog already matches the candidate (26,283 songs, 22,051 timed ends match the live SHA). That "push live" order is already done. The remaining go-live work is the NONH gate for newly-identified songs.

### Publish safety rule
Publishing is safe as long as you **back up the live catalog before deploy**, **keep the held/unknown set stored on disk**, and **keep rollback ready** (the publisher is gated and reversible). Wrong machine-guessed titles aren't dangerous - they're drafts humans correct. The only real hazard is clobbering existing human data.

### Archive cleanup
B27 produced a plan (`ARCHIVE_CLEANUP_PLAN_v01.md`) - 55 scripts + 2 data files to archive, **zero live-import collisions** (grep-verified), 4 unlisted files flagged for owner decision. One doc/reality conflict: `_batch_aligner_v01.py` (documentation says one thing, reality another). b15M owns that. **No moves executed** - awaiting collective sign-off per Max's "main decisions go through the collective" rule.

### ASR QC requirement
Every transcript must go through "many LLM-QC passes" before segmentation and identification. b7nonhtimes has the pipeline validated end-to-end: noisy ASR ? reliable performer attribution (intros clean), garbled lyrics stay "verify", English/silent vids correctly fall to honest-unknown.

---

## CURRENT STATE

### Done
- **Human-side re-timed catalog** - already live on the website
- **Performer de-duplication** - live
- **Website** (voting, login, playlists) - live
- **Machine indexing pipeline** (captions, song-splitting, 994-song reference, matching, reconciled DB) - complete for all videos that had captions
- **Handover tool** (`nonh_handover.py`) - picks oldest good NONH video, builds table in the EXACT human Excel format (read from the real `????? ?? ?????.xlsx`, mirrors all 11 columns, performer-grouped). **LLM-QC'd twice**, drift cases flagged "?????????" (verify), committed+pushed to master.
- **First handover table** - video `pX_1m8DlMbA` (2020-03-30, "?????? ?? ???????????? ?????", 47 songs). Only 2 of ~10 matches trustworthy; 8 marked verify.
- **ASR input staging** - all 93 caption-disabled videos are on teal16 (b9 finished the pulls overnight, 0 walls)

### In Flight
- **ASR on Sol** - transcribing the 93 caption-disabled videos. **54/93 done** (~past halfway), process alive and healthy (PID check confirmed). CPU-only, ~7-9 min/video, resumable (detached process). b7nonhtimes drains batches to Pine ? segments ? identifies autonomously. ETA: completing through the morning, then repeated LLM-QC passes on transcripts.
- **Video backup** (b9) - full 2842-video Tamza channel backup grinding on Lak, on its own timer.

### PARKED (needs Max's decision or re-engagement)
- **NONH live-publish** - did NOT happen overnight. b15merger (sole owner of the go-live gate code and the live-patch) went unresponsive despite multiple force-wakes over ~several hours. I parked it rather than risk a cold complex live deploy that could break the "don't lose data" rule. The gate is built/being built but not deployed.
- **Archive cleanup** - B27's plan ready, awaiting owner sign-off (b15M, b15merger, b15A, b7nonhtimes)
- **`_batch_aligner_v01.py` doc conflict** - b15M owns resolution

---

## EXACT NEXT STEP

1. **Decide on b15merger/b15merger** - re-engage the existing session, or hand the live-publish to a fresh session. The publish is the single biggest outstanding item. The publisher script (`pipeline/scripts/publish_catalog.py`) is clean, gated, and reversible (`--dry-run` for preview). All that's needed is someone to run it with the 3-path gate data, backing up live first.
2. If a fresh session takes it: read the handover doc at `TAMZA_HANDOVER_START_HERE_v01_tomemex.md`, consult the board, run `--dry-run` first, confirm the gate's output, then publish with backup.
3. Keep watching ASR until completion ? LLM-QC passes ? segmentation ? identification ? feed into the publish gate.
4. Sign off (or delegate) the archive cleanup plan so B27 can execute the reversible git moves.
5. Next weekly handover: pick the next-oldest good NONH video, same tool, same QC process.

---

## OPEN QUESTIONS FOR MAX

1. **b15merger went unresponsive overnight** - do you want me to wake them again, or hand the publish to a fresh session (or b7i, who owns the live deploy normally)?
2. **Archive cleanup sign-off** - B27's plan is ready and safe. Give the green light?
3. **Path A (song-match) threshold** - you said you'd tune the 3 thresholds in the morning. Given the confirmed drift, should Path A be demoted to "publish performer only, title = verify" by default on old videos, or do you want to set a stricter confidence bar?
4. **Handover table format** - I matched the exact columns from your Excel. Is the TSV drop-in acceptable, or do you want me to generate `.xlsx` tabs directly?

---

## KEY PATHS AND IDS

| What | Path/Command |
|---|---|
| Pipeline root | `C:\claude_base\tools\tamza_songs\pipeline\` |
| Handover doc (START HERE) | `pipeline/TAMZA_HANDOVER_START_HERE_v01_tomemex.md` |
| Workflow map | `pipeline/CURRENT_WORKFLOW_v01_tomemex.md` |
| Handover tool | `pipeline/timecoder_handover/nonh_handover.py` |
| First table (TSV) | `pipeline/timecoder_handover/tables/handover_2020-03-30_pX_1m8DlMbA.tsv` |
| QC verdicts | `pipeline/timecoder_handover/qc/pX_1m8DlMbA.json` |
| Human Excel | `C:\Users\maxre\Downloads\????? ?? ?????.xlsx` |
| Channel inventory (dates) | `output/channel_inventory.json` (935 videos, has upload_date) |
| Nonh caption-disabled list | `pipeline/song_timing/_work/nonh_caption_disabled_ids.txt` (93 ids) |
| ASR-ready on teal16 | `pipeline/song_timing/_work/nonh_asr_ready_on_teal16.txt` (82 ids) |
| Publish script | `pipeline/scripts/publish_catalog.py` (supports `--dry-run`) |
| Board (read/post/wake) | `python "C:/claude_base/branch_bulletin/bcast.py" read/post/wake` |
| Worklog | `python C:/claude_base/compaction_kb/scripts/worklog.py log "msg"` |
| B27 archive plan | `ARCHIVE_CLEANUP_PLAN_v01.md` (on B27's branch) |
| Session ID | B26juniorconnector (junior connector/poker on the whole picture) |
| ASR process on Sol | `ssh -i ~/.ssh/sol_key maxre@192.168.1.113` - `pgrep -fc '[t]ranscribe_v02'` |
| ASR output on Sol | `~/nonh_transcribe/out/` |
| ASR input on teal16 | `ssh -i ~/.ssh/sol_key maxre@192.168.1.176` - videos in `~/tamza/tamza_nonh/` |
| Oldest good NONH video | `pX_1m8DlMbA` (2020-03-30, 47 songs, 10 machine-identified) |
| Known song reference | 994 songs in the reference DB |

---

## GOTCHAS AND DEAD ENDS

- **Famous-song drift:** The matcher on old/fringe NONH videos drifts to famous songs - ~half of the "KNOWN" labels are wrong. Root cause: the announcer names the author/composer in the spoken intro, and the matcher locks onto that rather than the sung lyric. **Performers remain reliable** even from noisy ASR.
- **b15merger is unresponsive** - started the go-live gate build but never reported completion. Do NOT attempt a cold solo deploy of the live-publish; the gate logic lives in that session.
- **Human catalog IS already live** - verified via `publish_catalog.py --dry-run`. Don't re-push what's already deployed.
- **"First line" bleed:** In machine drafts, many "first line" cells contain the spoken intro text, not the sung lyric (boundary error). Flagged in the handover table tool's warning.
- **ASR is CPU-only on Sol** - no GPU acceleration. ~7-9 min per video, resumable (detached process). The process name is `transcribe_v02.py`; use bracket pattern `[t]ranscribe_v02` with pgrep to avoid matching grep itself.
- **Shell glob trap:** `ls *.json` in the ASR out dir can return 0 even when files exist (glob expands before SSH). Use `ls -la` or `find` instead.
- **Don't hit YouTube for metadata** - use `output/channel_inventory.json` (has upload_date, title, id for all 935 videos). YouTube is rate-limited and ytdow is busy.
- **Publisher is gated:** `publish_catalog.py` has a `--dry-run`, backs up live catalog before deploy, and is rollback-capable. The "don't lose data" rule is enforced by the tool itself -
