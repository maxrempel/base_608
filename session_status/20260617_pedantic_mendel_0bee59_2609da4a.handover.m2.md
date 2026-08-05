# Scribe handover - milestone 2 (~173K tokens)
# session: 20260617_pedantic_mendel_0bee59_2609da4a
# cwd: C:\claude_base\.claude\worktrees\pedantic-mendel-0bee59
# written: 2026-06-17 21:12:42 by deepseek-v4-pro

# HANDOVER - B26juniorconnector (Tamza Pipeline, Session 1)

---

## GOAL (Max's words, transcribed)

Max brought me (B26juniorconnector) in as a junior connector/poker on the whole Tamza picture. Explicit instructions:

1. **Register** as B26juniorconnector on the branch bulletin board.
2. **Understand whole-picture status** - read the existing handover, the full board history, learn where everything stands.
3. **Poke the team** - not a builder yet. Relay Max's decisions, ask owners to propose plans, let them design and decide individually and collectively. Grow into a qualified manager but don't rush.
4. **Relay the go-live rule**: newly identified songs go live; unknowns don't. Refined later: a segment goes live if it passes ANY of three paths: (A) confident song-text match, (B) clear spoken intro ("this is my song" / names composer-poet), (C) the intro's performer name matches the clean performer DB. Fails all three = held.
5. **Hands-on task**: pick the oldest good not-human-done NONH video, double-check its draft, annotate it, and hand it to the human timecoders. Repeat weekly.
6. **Manage B27**: develop a task for B27worker, run it by the owners, then steer B27.
7. **Push live**: tell the owners to push ready things live now (collective decision call).
8. **Weekly handover**: repeat a handover doc once per week.

---

## DECISIONS MADE + WHY

### 1. Go-live gate: 3-path OR rule
- **Original rule**: "identified songs go live, unknowns hold."
- **Max refined**: if the spoken intro clearly names the song/performer/authors, it also goes live - even without a song-text match. Path C added: match intro performer name against the existing clean performer database.
- **Rationale**: The ~88% UNKNOWN rate from text-matching alone is too conservative. Many segments have accurate spoken intros with performer names that ARE in the performer DB. Path C unlocks a lot more publishable content without sacrificing accuracy.
- **Decision mechanism**: relayed to b15merger, b7i, b10, b15A. b15merger accepted and is coding path C. Owners are designing the mechanism collectively - I stayed out of the build.

### 2. B27's task: archive cleanup
- **Chosen task**: the archive cleanup pass - the literal root cause of branching in this project. Flagged by B25handoverer and b23 as needed, but nobody owned it.
- **Rationale**: genuinely needed, cleanly scoped, and properly coordination-gated (run plan past owners before execution).
- **Status**: assigned to B27 with a coordination gate. Owners being poked affirmatively.

### 3. Push-live collective decision
- **What**: Max ordered "push live the ready things." I turned that into a collective readiness round: asked b7i, b15merger, b10, b15A, b9, b27 to each declare what they still need before push.
- **Rationale**: I'm junior - I don't decide the push threshold alone. Collective ownership.

### 4. Timecoder handover table format
- **Approach**: reverse-engineered the human team's column format from `output/data.json` (the existing human-catalog export): performer, song, authors, first_line, date, event, timecode, play_url.
- **Built a reusable tool** (`nonh_handover.py`) that (a) picks the oldest good NONH video by joining upload dates from `channel_inventory.json` with draft quality from the annotator drafts, and (b) emits a TSV table in the human-sheet column order.
- **First pick**: `pX_1m8DlMbA` (2020-03-30, "?????? ?? ???????????? ?????", 47 segments, 10 identified). The table is built at `timecoder_handover/tables/handover_2020-03-30_pX_1m8DlMbA.tsv`.
- **Gotcha uncovered**: several "first lines" in the drafts are actually spoken-intro bleed, not sung lines. Boundary is imperfect - exactly what human timecoders fix.

### 5. Handover review for B25handoverer
- Reviewed B25's START-HERE handover from a cold-reader perspective. Asked B25 to add the publish policy to it. Provided 5 specific notes (what worked, what needed adding).

---

## CURRENT STATE

### Pipeline overall (~90% done)
- 691 NONH videos: captions fetched, songs split by spoken-intro boundaries, frozen reference of 994 known songs built, every segment matched as KNOWN or UNKNOWN.
- Match results: ~12-20% confidently identified, ~88% UNKNOWN (by design - precision kept high).
- Human catalog re-timed and ready to publish.
- Website (voting, login, playlists) live.
- **Blocker**: 93 videos have no captions - need speech-to-text on Sol. Sol is off-limits while RAM tests run.

### Go-live gate in flight
- b15merger is building the 3-path OR gate.
- Spoken-intro fields (performer/author/title) need to "flow through" into the resolved store - b15merger and b7nonhtimes need to agree who wires that. I've nudged them.
- Paths A (song-text match) and B (clear spoken intro) data already exists. Path C (performer name match) being coded.

### B27 task: archive cleanup
- Assigned, coordination gate posted. Awaiting owner feedback before B27 executes.

### Push-live collective readiness
- Posted as a decision call. Awaiting each owner's "what I still need" response.

### Timecoder handover tool
- Reusable picker+table built: `nonh_handover.py` with `pick` and `table` subcommands.
- First video picked: `pX_1m8DlMbA` (2020-03-30).
- Table file: `timecoder_handover/tables/handover_2020-03-30_pX_1m8DlMbA.tsv` (47 rows).
- Not yet handed to timecoders - waiting on format confirmation.

### Handover review
- B25handoverer aware of the publish-policy gap. Not yet updated.

---

## EXACT NEXT STEP (for the next session)

1. **Resolve the Google Sheet format question**: Max said the Google Sheet wasn't found but "you must have its copy in Excel." Search for an Excel copy of the human timecoders' sheet - likely a `.xlsx` file somewhere in the pipeline or project folders. Match the handover table columns exactly to that Excel's columns before handing off.

2. **Confirm the table format with the team**: post the TSV header/sample to b10 and b7nonhtimes, ask if it matches what they expect for a weekly handoff.

3. **Once format confirmed**: hand `pX_1m8DlMbA` table to the human timecoders (paste into their Sheet or send the TSV, whatever their workflow is).

4. **Monitor the 3 owner threads**:
   - b15merger's go-live gate build (path C coding).
   - The spoken-intro-fields flow-through agreement (b15merger ? b7nonhtimes).
   - Push-live readiness responses from each owner.

5. **Follow up on B27**: check if owners confirmed the archive cleanup plan, unblock B27 if stalled.

6. **Weekly handover doc**: produce the first recurring handover for the next session.

---

## OPEN QUESTIONS (awaiting Max or team)

1. **Google Sheet Excel copy** - where is it? Max says it exists locally. Need to find it to match the timecoder handover format exactly.

2. **Column format confirmation** - is the current TSV structure (date, event, start, start_sec, performer, song, authors, first_line, status, align, intro_title, play_url, heard) the right set of columns for the human timecoders, or does their existing sheet have different/additional columns?

3. **Go-live thresholds** - Max said he'd set the 3 thresholds (confidence scores for paths A/B/C) once b15merger has the gate ready. Not yet set.

4. **Sol RAM tests ETA** - when can speech-to-text resume for the 93 captionless videos? No answer yet.

---

## KEY FILES & PATHS

| What | Path |
|---|---|
| Bulletin board script | `C:/claude_base/branch_bulletin/bcast.py` |
| TAMZA handover (start here) | `C:/claude_base/tools/tamza_songs/pipeline/TAMZA_HANDOVER_START_HERE_v01_tomemex.md` |
| Workflow description | `C:/claude_base/tools/tamza_songs/pipeline/CURRENT_WORKFLOW_v01_tomemex.md` |
| Channel inventory (dates + titles) | `C:/claude_base/tools/tamza_songs/output/channel_inventory.json` |
| Human catalog export | `C:/claude_base/tools/tamza_songs/pipeline/output/data.json` |
| NONH draft for picked video | `C:/claude_base/tools/tamza_songs/pipeline/song_timing/from_scratch_idx/_work/annotator/drafts_nonh_v01/nonh_pX_1m8DlMbA.json` |
| Drafts index | `C:/claude_base/tools/tamza_songs/pipeline/song_timing/from_scratch_idx/_work/annotator/drafts_nonh_v01/_INDEX.txt` |
| Timecoder handover tool | `C:/claude_base/tools/tamza_songs/pipeline/timecoder_handover/nonh_handover.py` |
| Handover table (first output) | `C:/claude_base/tools/tamza_songs/pipeline/timecoder_handover/tables/handover_2020-03-30_pX_1m8DlMbA.tsv` |
| Worklog | `C:/claude_base/compaction_kb/scripts/worklog.py` |

---

## KEY IDs & NAMES

| Entity | Details |
|---|---|
| My board ID | `B26juniorconnector` |
| First picked video | `pX_1m8DlMbA` (2020-03-30, "?????? ?? ???????????? ?????", 47 segments) |
| Go-live gate owners | b15merger (build), b7i (publish), b10 (render), b15A |
| Worker I manage | B27 (B27worker) |
| Handover author | B25handoverer |
| Speech-to-text blocker | Sol machine (RAM tests) |
| NONH queue | `song_timing/queue.json` (691 videos) |
| Known-song reference | 994 songs frozen |

---

## GOTCHAS & DEAD ENDS RULED OUT

1. **No YouTube hits allowed**: channel dates came from `channel_inventory.json` (already on disk from b9's ytdow run), not from live YouTube API calls. The tool respects the block rules.

2. **Drafts have boundary bleed**: several "first_line" fields in the machine drafts are actually the tail of the spoken intro, not the first sung line. Humans must verify. Don't treat drafts as ground truth.

3. **channel_inventory.json is the master video list**: 935 videos total, has `id`, `upload_date`, and `title` (Russian date in title). No need to query YouTube.

4. **fetch_nonh_state.json has no dates**: it tracks processing state (downloaded, captioned, split, matched) but not upload dates. Dates must come from the inventory.

5. **Inline Python pattern flagged**: got several "hook" warnings for repeated inline `python -c` blocks. Switched to writing a proper reusable script (`nonh_handover.py`). Use scripts, not one-liners, going forward.

6. **Go-live is 3 OR-paths, not 1**: the original rule ("identified = go live") was refined twice. Path C (performer-name match from intro) is the big unlock. Don't revert to the simpler version.

7. **Spoken-intro fields need a flow-through agreement**: b15merger needs the intro perforer/author/title fields for paths B and C. b7nonhtimes may need to wire them through. This is a coordination point, not a build task - I need to nudge them to settle it.
