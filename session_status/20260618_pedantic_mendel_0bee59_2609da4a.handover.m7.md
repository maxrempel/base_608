# Scribe handover - milestone 7 (~528K tokens)
# session: 20260618_pedantic_mendel_0bee59_2609da4a
# cwd: C:\claude_base\.claude\worktrees\pedantic-mendel-0bee59
# written: 2026-06-18 14:07:10 by deepseek-v4-pro

# HANDOVER - Tamza Project: B26juniorconnector Session

---

## GOAL (in Max's words)

The project is nearing its end point: a clean database plus a live catalog. Newly identified songs from not-yet-human-indexed (NONH) videos should go live. Unknowns should not. B26's role: junior connector/poker on the whole picture, plus pick one oldest good NONH video, annotate it, double-check it, and hand it to human timecoders. Repeat a handover once per week. Eventually grow into a qualified manager but don't rush.

Overnight Max put B26 in charge: drive tasks to completion while Max slept, define who's needed, tell others to sleep.

---

## DECISIONS MADE + WHY

### Go-Live Policy (Max's 3-path gate)
Max ruled that a NONH segment can go live if ANY of three paths pass:
- **Path A**: confident song-text match against the known-song cluster list
- **Path B**: clear spoken intro naming the song ("this is my song" / names composer-poet)
- **Path C**: the intro names a performer, and that performer matches the clean performer DB

If a segment fails all three, it stays held. The reasoning: Paths B and C dramatically expand what can go live beyond the ~12-20% that match a canon song title, since the performer DB is already clean.

### The HARD correction - KILL ALL TITLES, FIRST SUNG LINES ONLY
Mid-session Max discovered the machine pipeline had drifted from the original principle. Identity = **first sung line only**, never a canon title or announced name. All first lines must be verified by a smart LLM (DeepSeek-4 non-flash minimum) and spot-checked by a human/Opus. The reasoning: the mechanical matcher was locking onto announcer intros ("????????") and substituting famous canon songs (the "famous-song drift" - heard "???????? ?????????" but tagged "??????? ????????? ?????????"). This made ~half the matched titles wrong. Old sessions knew these rules; new ones forgot them.

### Opus API prohibited without Max's explicit permission
A session burned $40 on Opus API calls where DeepSeek-4 non-flash would work. Max ordered: no Opus sub-agents via API, no direct Opus API calls for bulk work. The in-session Opus (subscription) is fine for spot-checks. Rule added to `global2.md`.

### Overnight Roster
Only three sessions stayed awake: B26 (manager, 4-min then 20-min watch), b7nonhtimes (ASR ? segmentation ? identification, autonomous), and b9 (full 2842-video backup). Everyone else told to sleep. b15merger was tasked with the publish but went unresponsive overnight.

### Archive Cleanup
B27 built a plan (55 scripts + 2 data files to archive, zero live-import collisions). Parked for Max's morning sign-off; no moves executed.

### Scaling Method for First-Line Extraction
After b27 went unresponsive, B26 proved the method on one video using an Opus reader sub-agent (later flagged as a rule violation - but the prompt/method itself is valid for DS4-nonflash). B27 was re-tasked to scale on DS4-nonflash with a faithful-to-transcript mandate. B26's gold-standard spot-check caught b27's sample reintroducing famous-song drift (polishing garbled heard text into canonical lyrics). Blocked scale until b27 produces a faithful redo.

---

## CURRENT STATE

### Done / In Place
- **Handover tool**: `timecoder_handover/nonh_handover.py` - picks oldest good NONH video, builds Excel-format table matching the human team's exact "????? ?? ?????.xlsx" format (performer-grouped, 11 columns). Committed and pushed to master.
- **First handover table**: for video `pX_1m8DlMbA` (2020-03-30 concert, 47 segments, 31 performer turns). Multi-pass LLM-vetted (2 passes), bad matches demoted to ?????????. File: `timecoder_handover/tables/handover_2020-03-30_pX_1m8DlMbA.tsv`
- **Gold-standard first-line sample**: verified first sung lines for pX_1m8DlMbA, faithful to transcript, no famous-song drift. File: `timecoder_handover/verified_first_lines_pX_1m8DlMbA.json`
- **QC verdicts**: `timecoder_handover/qc/pX_1m8DlMbA.json` (pass 2 - caught the announcer-intro drift pattern)
- **ASR Transcription on Sol**: 54/93 caption-disabled videos transcribed as of Max waking, healthy and progressing (process PID alive, steady ~3-8/hour depending on concert length). b7nonhtimes draining batches to segmentation.
- **ASR pipeline validated end-to-end**: noisy ASR still yields reliable performer attribution (intros transcribe clean), English/silent videos fall to honest unknown.
- **b15merger's titles-free gate**: reworked after the kill-titles directive. Produces 7839 publish-candidates (744 videos), consumes INTRO-ONLY honestly. Awaiting verified first-lines.
- **Cardinal Rules enshrined**: B25handoverer pushed v03 handover doc with the 7 rules. b29 wrote a method doc.
- **Opus API rule**: added to `global2.md` with the $40 explanation kept.
- **Wake system bug logged**: selective force-wake unreliable on idle/disarmed sessions, logged to `rule_inconsistencies_tomemex.md` and flagged to c6.
- **HUM remap catalog**: already live (confirmed via `publish_catalog.py --dry-run` - 26,283 rows, no change since last publish).
- **Nonh_asr_ready_on_teal16**: 82 initially, now all 93 caption-disabled videos on teal16.

### In Flight / Blocked
- **First-line extraction at scale (CRITICAL PATH)**: B27 owns it, produced a sample that failed B26's spot-check (polished toward famous canon instead of faithful to heard text). B27 was told to redo on DS4-nonflash with a faithful redo. This blocks the full NONH publish because b15merger's gate awaits verified first-lines.
- **NONH live-publish**: parked for Max's morning. b15merger went silent overnight (timer disarmed per idle-session rule). b15merger is now back and built the titles-free gate split but is still awaiting B27's first-lines.
- **2-min cap on radio (Max's complaint)**: ROOT CAUSE DIAGNOSED. Not a player bug. The radio player (`app.js:605-614`) plays full real length when `seg_end` exists; falls back to 2-min cap only when `seg_end` is missing. **4,232 of 26,283 catalog rows have no seg_end** - they were never time-mapped. Fix: push those untimed rows through the transcript?timing pipeline to produce real `seg_end` values, then republish. Routed to b7nonhtimes. Converges with "incomplete HUM videos ? NONH."
- **Incomplete HUM videos not in NONH**: Routed to b7nonhtimes. These are the ~4232 untimed rows.
- **Archive cleanup**: B27's plan ready, holding for Max's sign-off (b9 approved; b15M needed for one doc conflict - `_batch_aligner_v01.py` doc-vs-reality).
- **b7i (site deployer)**: unreachable - no armed listener. bcast wake queued but can't land. Work (republish after timing fix) may need RemoteTrigger or b7nonhtimes to absorb.
- **Video backup (b9)**: self-sustaining on Lak, full 2842 videos, all 93 priority done.

### Housekeeping / Infra
- Wake system has a structural bug: when idle sessions disarm their timers, `bcast wake` can't reach them. c6 fixed the lying "FORCE-WOKEN" stamp; now honest "queued" for dead sessions.
- The listener-free wake is `RemoteTrigger run` (claude.ai remote-trigger API) - spawns/runs a fresh agent server-side without needing a listener. B26 found this but hasn't used it yet.

---

## EXACT NEXT STEP

**Blocking publish**: B27 must produce a faithful redo of the first-line sample (faithful to the transcript heard text, don't polish into famous canon). B26 spot-checks it again. Once B26 approves, B27 scales on DS4-nonflash across all segments. Then b15merger's gate consumes them and produces the final publish split. Then publish (likely via b7nonhtimes since b7i is unreachable, or via RemoteTrigger).

**Radio 2-min cap**: b7nonhtimes needs to push the 4,232 untimed rows through the transcript?timing pipeline to produce real `seg_end` values.

**Archive cleanup**: awaiting Max's sign-off.

**Weekly handover**: B26 owes a recurring handover. The tool exists; the next video needs to be picked and processed with the new first-lines-only, titles-killed method.

---

## OPEN QUESTIONS AWAITING MAX

1. **Scaling fork for first-line extraction**: B26 asked whether to orchestrate sub-agents or hand to a worker/DS4 batch, and any budget cap. Max assigned it to B27 - but B27 is unreliable (wake system bug + silent). Does Max want a fresh worker spawned via RemoteTrigger for the DS4-nonflash bulk run?
2. **RemoteTrigger agents**: do they bill to the subscription (safe) or the disabled Opus API key? Max hasn't answered.
3. **Archive cleanup sign-off**: B27's plan ready, one conflict (`_batch_aligner_v01.py`) needs Max or b15M to decide.
4. **Should b7i's publish duties be reassigned** since b7i is unreachable (no armed listener)?
5. **Handover table format**: B26 asked whether to match the exact existing Google Sheet or run the column layout past the team - Max pointed to the Excel copy instead, but hasn't confirmed the exported format is final for the human team.

---

## KEY PATHS / IDS

- **Handover tool**: `C:\claude_base\tools\tamza_songs\pipeline\timecoder_handover\nonh_handover.py`
- **First handover table**: `tools/tamza_songs/pipeline/timecoder_handover/tables/handover_2020-03-30_pX_1m8DlMbA.tsv`
- **Gold-standard first lines**: `tools/tamza_songs/pipeline/timecoder_handover/verified_first_lines_pX_1m8DlMbA.json`
- **QC file**: `tools/tamza_songs/pipeline/timecoder_handover/qc/pX_1m8DlMbA.json`
- **Pilot video**: `pX_1m8DlMbA` (2020-03-30, "?????? ?? ???????????? ?????", 47 segments, 31 performer turns, 18 sung lines, 29 intro-only)
- **Human Excel reference**: `C:\Users\maxre\Downloads\????? ?? ?????.xlsx`
- **Live catalog**: `tools/tamza_songs/pipeline/output/data.json` (26,283 rows)
- **Publish script**: `tools/tamza_songs/pipeline/scripts/publish_catalog.py` (gated, reversible, `--dry-run` flag)
- **Channel inventory** (upload dates, no YT hit): `tools/tamza_songs/output/channel_inventory.json` (935 videos)
- **ASR state**: Sol at `192.168.1.113`, process `transcribe_v02.py`, output in `~/nonh_transcribe/out/`, ready list at `song_timing/_work/nonh_asr_ready_on_teal16.txt`
- **93 caption-disabled IDs**: `song_timing/_work/nonh_caption_disabled_ids.txt`
- **Board tool**: `python C:/claude_base/branch_bulletin/bcast.py` (read, post, wake, whoami, catchup)
- **Worklog**: `python C:/claude_base/compaction_kb/scripts/worklog.py log`
- **Global2**: `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md`
- **Inconsistencies log**: `C:/claude_base/rule_inconsistencies_tomemex.md`
- **Handover doc**: `C:\claude_base\tools\tamza_songs\pipeline\TAMZA_HANDOVER_START_HERE_v01_tomemex.md` (now v03)
- **Workflow map**: `C:\claude_base\tools\tamza_songs\pipeline\CURRENT_WORKFLOW_v01_tomemex.md`
- **Monthly update method**: `tools/tamza_songs/pipeline/method/monthly_update_method_v01_tomemex.md`
- **Segment drafts**: `song_timing/from_scratch_idx/_work/annotator/drafts_nonh_v01/`
- **Transcripts**: `song_timing/transcripts/<vid>.json`
- **Published commit**: `eb59a115` (handover QC passes + tool changes), `54ce78ed` (handover warning row)
- **bcast identities**: B26juniorconnector (manager), b15merger (gate/publish), b7nonhtimes (ASR/seg), b7i (site deploy), b9 (backup), b27 (worker, first-line extraction), c6 (wake-listener infra), B25handoverer (handover doc), b15A, b15M, b10, b29 (rules method doc)

---

## GOTCHAS AND DEAD ENDS

### Gotchas
- **Famous-song drift is the #1 data-quality trap.** The mechanical matcher hears the announcer name a famous author (????????) and grabs a famous song, even when a different song is sung or the segment is still intro chatter. The **LLM must read the actual heard lyric**, not names in the intro. Even DS4-nonflash can drift by polishing garbled text into the canonical version - spot-checking must catch this.
- **Opus API sub-agents are PROHIBITED without Max's explicit permission.** Use DS4-nonflash for bulk. In-session Opus (subscription) is free for spot-checks. Opus API key was disabled by Max.
- **Titles are dead.** Song identity = first sung line only. No canon titles. No announced names as identity. This must be in every handover and pipeline step.
- **bcast wake is listener-based** - it cannot reach a session whose listener is disarmed (idle sessions disarm their timers). The c6 stamp "FORCE-WOKEN" used to lie about this; now says "queued" honestly. For dead sessions, use `RemoteTrigger run` instead.
- **The HUM remap catalog IS already live** - the `--dry-run` showed no changes. The 2-min cap is NOT a stale publish; it's missing `seg_end` values for 4,232 untimed rows.
- **The human Excel format** is one sheet per concert, performer-grouped, columns: ? | ?????? | ??????????? | ???????? | ?????? | ?????? ?????? | ??????? ????? | ?????? | ??????? + ??????????? | ????-???? | ??????? ? ?????? ?????. The handover tool mirrors this exactly.
- **Performers are the reliable signal** - intros transcribe cleanly even from rough ASR, performer names match the DB well. Song titles are the unreliable part.
- **Margarita problem**: the DB has one "?????????" but there may be several different people. This needs an LLM to actually read and reason, not a Python name-collapse.

### Dead Ends / Ruled Out
- **Don't hit YouTube for video metadata** - upload dates are in `channel_inventory.json` (935 videos, pre-fetched, no YT hit needed).
- **Don't solo-deploy** - all live deploys go through collective sign-off and the gated/reversible `publish_catalog.py`. B26 correctly parked the publish when b15merger went silent overnight rather than risk a cold deploy.
- **Don't nag unresponsive sessions endlessly** - B26 settled into health-checks (read-only SSH) for ASR rather than repeated wakes. Archive moves held for sign-off.
- **90/93 not 82** - initially B26 counted 82 videos on teal16, but the full 93 arrived within an hour (b9 finished the last 11).
- **The "0 transcripts" count was a false alarm
