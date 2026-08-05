# Scribe handover - milestone 9 (~675K tokens)
# session: 20260618_pedantic_mendel_0bee59_2609da4a
# cwd: C:\claude_base\.claude\worktrees\pedantic-mendel-0bee59
# written: 2026-06-18 18:45:56 by deepseek-v4-pro

# TAMZA HANDOVER - b26juniorconnector (manager/connector)

## GOAL (in Max's words)
The Tamza song-indexing project is near the end point: a **clean database + live catalog**. Newly identified songs from not-yet-human-indexed (NONH) videos should go live to the radio site; unknown/untrusted ones stay held. B26's role: junior connector/manager on the whole picture - poke owners, coordinate, don't build solo. Also own one hands-on task: pick the oldest good NONH video, annotate it, hand to the human timecoders, repeat weekly. Manage B27 worker.

## CORE PRINCIPLE (hard-won, do not forget)
**Song identity = FIRST SUNG LINE only.** Never names, never canonical titles. The first sung line must be verified by a smart LLM (DeepSeek-4 non-flash minimum) that **actually reads the transcript** - not a mechanical matcher. Opus spot-checks the output. Titles are killed everywhere. This rule was known by older sessions but got lost and caused a disaster (mechanical matching drifted to famous/canonical songs that weren't actually sung).

## DECISIONS MADE + WHY

1. **Go-live gate (3 OR-paths)**: A segment passes if (A) confident song-text match, OR (B) clear spoken intro naming the song, OR (C) performer name from intro matches the clean performer DB. Fails all three ? held. Rationale: path C lets us publish many performances with correct performer attribution even when the song itself is unknown.

2. **Handover table format**: Must match the EXACT human Excel format (`C:\Users\maxre\Downloads\????? ?? ?????.xlsx`) - one sheet per concert, columns: ? | ?????? | ??????????? | ???????? | ?????? | ?????? ?????? | ??????? ????? | ?????? | ??????? + ??????????? | ????-???? | ??????? ? ?????? ?????. Grouped by performer turn.

3. **Kill all titles**: After Max's correction, all canon titles stripped from handover + gate. Song identity = first sung line only, LLM-verified, hand-QC'd by B26.

4. **Opus API PROHIBITED** without Max's explicit permission - too expensive ($40 wasted where DS4-nonflash works). Added to global2 rules. Bulk LLM ? DS4-nonflash. B26's in-session Opus (subscription) is free for spot-checks only.

5. **Budget**: ~$3 USD for pilots/trials, ~$12 USD for the full Tamza first-line run. Cheap DeepSeek-4 batch, not Opus, not hand at scale.

6. **First-line method v6 ACCEPTED** as final: famous-song-drift disaster solved. After 6+ QC rounds (B26 hand-QC + b15merger LLM-QC, independent), v6 is the DS4 ceiling. v7/v8 regressed. Residual: on repetitive-lyric songs, the model occasionally grabs a later verse of the SAME song - still faithful, not a wrong song; humans fix the exact start during timecoding.

7. **Radio 2-min cap**: NOT a player bug. The app.js radio plays full length when `seg_end` exists, falls back to 120s cap only when it's missing. ~4,232 rows had no end-time. Free fixes recovered ~4,100 (stale data republished + next-start-guarded). Remaining: 54 videos need speech-to-text.

8. **Missing-transcript videos go via teal16 ASR**, NOT YouTube. The full video backup already downloads the video files to teal16; we run speech-to-text from those stored files - no second YouTube puller, no block risk.

9. **bcast team bug**: Case-sensitive team derivation. Capital "B26" = team "B", lowercase workers = team "b" ? cross-team routing chaos. Fixed by re-registering as lowercase `b26juniorconnector`. Reported to c6.

10. **Force-wake unreliability**: `bcast wake` can falsely claim "FORCE-WOKEN" when the target session is dead. c6 added proof-of-life check (now honestly says "queued"). For truly dead sessions, use `RemoteTrigger` (listener-free cold-spawn). When workers are idle/disarmed, Max must manually nudge their chat windows.

## CURRENT STATE

### DONE (deployed live)
- **+899 songs uncapped**: stale end-times recovered via republish. Live + byte-verified.
- **+3,201 songs uncapped**: next-start-derived ends, guarded against >30min fabrications. Live.
- **17 broken ends (negdur)**: removed from live.
- **~4,100 total songs now play full length in radio** (was capped at 2 min). Zero spend, all free fixes.

### METHOD PROVEN, AWAITING GO
- **First-line extraction**: v6 method accepted (faithful to heard words, zero canonical drift, poems detected, host-chatter filtered). QC complete (B26 hand + b15merger LLM, independent, converged). Pilot cost: ~$0.15.
- **Waiting on Max's one-word "go"** for the $12 full DS4 run across all 772 NONH videos.

### IN PROGRESS
- **ASR on Sol**: 93/93 caption-disabled videos transcribed overnight. Pipeline validated end-to-end (noisy ASR still yields reliable performer attribution; intros transcribe clean).
- **54 un-timed videos**: remaining from the ~4,232 originally untimed. Need speech-to-text from teal16 (their video files are already downloading via the big backup). b7nonhtimes + B30 own this.
- **b27 (worker)**: idling/offline. Holds the recipe for the $12 full first-line run when Max says go.
- **b15merger**: live, owns the live-publish gate. Deployed the free fixes.
- **b9**: big 2,842-video backup still running (self-sustaining on Lak).

### PARKED
- **Archive cleanup** (B27's plan): 55 dead scripts identified, zero live-import collisions. Ready, reversible git moves. Holding for owner sign-off (b15M for the `_batch_aligner_v01.py` doc/reality conflict).
- **NONH live-publish of recognized performances**: gate built (titles-free split: 6,997 publish / 68 truly-unknown), but blocked until first-lines are done (the $12 run).

### RULES ENSHRINED
- **global2.md**: Opus API prohibition (with $40 explanation).
- **START-HERE handover (v03+)**: 7 cardinal rules re-enshrined so new sessions don't drift.
- **Method doc**: b29 wrote a standalone method doc with the principles.

## EXACT NEXT STEP

**Get Max's "go" on the $12 full first-line run**, then:
1. b27 runs all 772 NONH videos through the DS4 v6 first-line method (~$12, within cap).
2. B26 hand-spot-checks the output.
3. b15merger ingests verified first-lines into the titles-free gate.
4. Publish recognized performances live (reversible, backup-first).

For the remaining radio cap: the 54 un-timed videos flow through teal16 ASR ? timing ? republish (already routed to b7nonhtimes/B30).

## OPEN QUESTIONS FOR MAX

1. **$12 GO**: Say "go" to run the faithful first-line method across all 772 videos. Method is proven, disaster solved, within your pre-approved cap.

2. **Wake the workers?** b27 and b7nonhtimes may be offline (their timers disarmed from idle). Need you to nudge their chat windows, or authorize RemoteTrigger cold-spawns.

## KEY PATHS / FILES

| What | Path |
|------|------|
| Pipeline root | `C:\claude_base\tools\tamza_songs\pipeline\` |
| Handover tool | `timecoder_handover/nonh_handover.py` (subcommands: pick, table) |
| Generated tables | `timecoder_handover/tables/handover_*.tsv` |
| QC verdicts | `timecoder_handover/qc/pX_1m8DlMbA.json` |
| Verified first lines (pilot) | `timecoder_handover/verified_first_lines_pX_1m8DlMbA.json` |
| b27's pilot samples | `timecoder_handover/firstline_SAMPLE_b27_*` |
| Human Excel | `C:\Users\maxre\Downloads\????? ?? ?????.xlsx` |
| Live catalog | `output/data.json` (26,283 rows) |
| Channel inventory (upload dates) | `../output/channel_inventory.json` (935 videos) |
| ASR transcripts (local) | `song_timing/transcripts/<vid>.json` |
| ASR transcripts (Sol) | `~/nonh_transcribe/out/<vid>.json` on 192.168.1.113 |
| Publish script | `scripts/publish_catalog.py` (gated, reversible, `--dry-run`) |
| Board tool | `C:\claude_base\branch_bulletin\bcast.py` |
| Global rules | `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md` |
| Rule inconsistencies | `C:\claude_base\rule_inconsistencies_tomemex.md` |
| START-HERE handover | `C:\claude_base\tools\tamza_songs\pipeline\TAMZA_HANDOVER_START_HERE_v01_tomemex.md` |
| 7 cardinal rules | `C:\claude_base\tools\tamza_songs\pipeline\method\CARDINAL_RULES_METHOD_v01.md` |
| Pilot video | `pX_1m8DlMbA` (2020-03-30, "?????? ?? ???????????? ?????", 47 segments) |

## WORKERS AND OWNERS

| ID | Role | Status |
|----|------|--------|
| b26juniorconnector | Junior manager/connector (you) | Active, watching |
| b27 | Worker (hard lifting: DS4 first-line extraction) | Intermittent, needs wake |
| b15merger | Live-publish gate owner | Active |
| b7nonhtimes | ASR + segmentation + timing | Intermittent |
| b9 | Video backup (2,842 videos) | Active, self-sustaining |
| b7i | Site publish (often unreachable) | Offline |
| B30 | Fresh 1M worker (untimed-rows timing) | Assigned, may need wake |
| c6 | bcast/wake infra owner | For comms bugs |
| c16 | New comms-infra owner | For routing issues |

## GOTCHAS / DEAD ENDS

1. **Mechanical matching drifts to famous songs** - the matcher hears the announcer name "????????" and grabs a famous Okudzhava song, ignoring what was actually sung. The fix is LLM reading the transcript, not mechanical n-gram matching
