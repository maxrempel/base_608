# Scribe handover - milestone 9 (~677K tokens)
# session: 20260703_inspiring_almeida_cc66dc_3dba762b
# cwd: C:\claude_base\.claude\worktrees\inspiring-almeida-cc66dc
# written: 2026-07-03 12:50:18 by deepseek-v4-pro

# HANDOVER - Tamza Song Pipeline (b29, previously B26juniorconnector)

---

## GOAL (in Max's words)

The project is reaching its end point: a clean database of indexed songs, plus recognized songs going live. Newly identified songs from not-yet-human-indexed (NONH) videos should go live where the identification is confident; unknowns should not. Also: pick the oldest good NONH video, annotate it for human timecoders, and repeat weekly.

Later refined: **identity = first sung line only** - no canon titles, no announced names. Every first line must be verified by a smart LLM (Opus or DS4 non-flash minimum) that actually reads the sung text. Spot-checked by the human manager.

---

## DECISIONS MADE + WHY

### 1. Go-live gate: 3 OR-paths
**Decision:** A segment goes live if it passes ANY of: (A) confident song-text match to a known cluster, (B) clear spoken intro naming the song, or (C) performer named in the intro matches the performer DB. Fails all 3 = held.
**Why:** Pure cluster-match only catches ~12-20% confidently; paths B and C (exploiting rich spoken intros and the clean performer roster) unlock many more segments for live publishing. This is a big multiplier on what goes live.

### 2. Kill all titles - identity is first sung line only
**Decision:** No "????????" (title) anywhere. Song identity = the first sung line, read from the actual audio transcript by a smart LLM. No canon titles, no mechanical matcher-guesses.
**Why:** The mechanical matcher suffered "famous-song drift" - it locked onto the announcer naming a famous author ("????????") and grabbed a famous song, ignoring what was actually sung. Canon titles are unreliable; human-typed titles are sloppy/missing. The real first sung line (with smart verification) is the only honest identity.

### 3. Full-text clustering + DeepSeek FLASH for first-line reconstruction
**Decision:** Cluster songs by their full sung lyric text (already exists as the "canon"), then reconstruct the true first line from each cluster using DeepSeek FLASH (cheap, ~$0.19 for the whole catalog). Opus spot-checks for fabrication. Online headless workers only for the ~20% of songs where DeepSeek is uncertain (fringe/unindexed songs).
**Why:** First lines in the existing data are often garbled (ASR junk, spoken prefixes like "??? ???", author announcements stuck in front). Full-text clustering groups all performances of one song; then a smart reader extracts the real opening from the clustered lyrics. Pilot proved this works with zero fabrication on 60 test songs.

### 4. Publish the recognized performances live, always
**Decision:** Max's rule is "always" - publish recognized performances to the live site. The only safety requirement: back up the live catalog first, keep the held/unknown set on disk, and keep a reversible rollback path. Wrong guessed titles aren't dangerous (humans correct them later); losing data IS dangerous.
**Why:** Withholding ready work frustrates the user; the catalog already has a reversible deploy mechanism (`publish_catalog.py` with `--dry-run` + backup). The NONH publish was parked for 2 weeks because b15merger went silent - this should never happen again under "always."

### 5. Rules-gap: 6 high-priority disaster-causers missing from autoload
**Decision:** Analyzed 77 harvested rules from 106 sessions against CLAUDE.md + global2.md. Found ~33 gaps, 6 that repeatedly cause disasters: (1) first-line-only identity + smart-LLM verify + kill titles, (2) always pass full untruncated text to the LLM, (3) pilot ? spot-check ? scale 4x, (4) never relaunch an alive worker, (5) cluster by full lyrics, (6) song start = end of prose intro.
**Why:** These rules were genuinely absent from the autoloaded instructions, which is why every new session re-derives them the hard way. Max needs to promote them to global2. (I did NOT edit the autoload files - Max's decision.)

### 6. Read the FULL transcript window, use [??????] markers
**Decision:** The concrete reading technique: slice the full transcript text inside each segment's time window, find the `[??????]` marker (where speech turns to song), and extract the text right after it as the first sung line. Never trust `seg_text_head` alone (it's mostly the host's announcement).
**Why:** The initial "half the matches are wrong" panic was a head-only artifact. Reading full windows with [??????] cues flips the assessment - many canon matches are actually correct (the refrain is genuinely sung). The matcher wasn't the whole disaster; nobody reading the full text was.

---

## CURRENT STATE (what is done, what is in flight)

### DONE (pushed to master, validated)
- **Handover tool** (`timecoder_handover/nonh_handover.py`): picks the oldest good NONH video, produces a handover table in the exact human Excel format (one sheet per concert, performer-grouped, 11 columns matching "????? ?? ?????.xlsx"). Titles column is BLANK (humans fill). Identity carried via first-line only. QC verdict column flagged.
- **Pilot handover** for video `pX_1m8DlMbA` (2020-03-30, "?????? ?? ???????????? ?????"): 31 performer turns, 2 confident songs, 13 Opus-verified first sung lines, rest honestly marked intro-only/unknown.
- **Verified first lines** stored in `timecoder_handover/verified/pX_1m8DlMbA.json` - the raw Opus reads with the [??????]-cue technique.
- **Method doc**: `HANDOVER_METHOD_v01_tomemex.md` enshrining all the rules (kill titles, smart-read, [??????] technique, online lookup for fringe songs, Opus spot-check).
- **Rules-gap analysis**: `max_rules_GAP_vs_autoload_v01.md` - 77 harvested rules mapped, 33 gaps, 6 high-priority flagged. Pushed.
- **DeepSeek reconstruction pilot**: 60 test songs passed QC (zero fabrication, no drift). Full ~986-song run was launched and is completing in the background - results write to `timecoder_handover/firstline_ds_out.json`.
- **Human-side catalog is already live** - the re-timing deploy happened (confirmed by `publish_catalog.py --dry-run`: "NO CHANGE since last publish").
- **ASR pipeline** (93 caption-disabled videos): verified healthy overnight - all 93 videos processed, transcripts produced on Sol, draining to segmentation + identification.

### IN FLIGHT
- **Full first-line reconstruction run**: ~986 songs being processed by DeepSeek FLASH. The script is `firstline_ds_v01.py`, cost is pennies (~$0.19 total), results file `firstline_ds_out.json`. This was launched in the background - it may be complete by the time you read this.
- **Live publish of recognized NONH performances**: b15merger was directed to publish (Max said "always"). The user confirmed GO. Status uncertain - b15merger previously went silent for 2 weeks. The publish candidate (8059 rows / 782 videos, titles-free) was built and ready.
- **Archive cleanup**: B27's plan is built but held for owner sign-off (reversible git moves, zero live-import collisions). The one conflict (`_batch_aligner_v01.py` doc-vs-reality) needs b15M to resolve.

### PARKED (needs Max's decision or a fresh run)
- **The 6 high-priority rules** still not promoted to global2.md - Max hasn't done this yet.
- **Weekly timecoder handover cadence** never resumed after the pilot - I was dormant for ~2 weeks.
- **"Because" fragmentation fix**: pilot proved the real-fix plan (full-text cluster + smart first-line + wire into search), but it hasn't been wired into the live search yet. That's the next run's job.

---

## EXACT NEXT STEP

1. **Check the DeepSeek run**: look at `C:\claude_base\tools\tamza_songs\pipeline\timecoder_handover\firstline_ds_out.json` - it should contain ~986 reconstructed first lines. Spot-check a sample (especially low-confidence ones) for fabrication.

2. **For the ~20% still uncertain** (confidence < 0.5 or honest-DS-unknown): spin headless online workers using the proven prompt from `FIRSTLINE_RECONSTRUCTION_HANDOFF_v01_tomemex.md` to look up the real first lines on bards.ru/pesni.net/etc. Some will stay unknown (fringe songs) - that's honest.

3. **Write back**: merge the corrected first lines into the cluster canon, then propagate to the live catalog (or the NONH candidate) so search returns all performances of each song.

4. **Wire into search**: make the site's search use the corrected first-line identity, not the human-typed title. This is the final step that fixes "search shows 2, but we sang it 5 times."

5. **Resume weekly handovers**: pick the next oldest good NONH video, run the Opus-read ? verified-first-line pipeline, produce the Excel table, hand to timecoders.

6. **Confirm publish**: if b15merger hasn't pushed the recognized NONH performances live yet, re-engage or do it yourself - the publish script is `publish_catalog.py`, it backs up first and has `--dry-run`.

---

## OPEN QUESTIONS (awaiting Max)

- **Promote the 6 high-priority rules to global2.md?** They're flagged in the gap doc - the session will keep forgetting them until they're autoloaded.
- **Which "Because" performances to group?** Max said Russian and English versions can be different trees - but the ~3 missing English "Because" performances are still unaccounted for. Need to run the smart-LLM song recognizer over the FULL transcript set (not just the partial set loaded here) to find them.
- **DeepSeek account balance**: topped up by Max this session; should be sufficient for the full run (~$0.19). But verify before any new runs.

---

## KEY PATHS, IDs, COMMANDS

### Files you will need
- **Catalog**: `C:\claude_base\tools\tamza_songs\pipeline\output\data.json` (26,283 rows, live catalog)
- **Canon (clusters)**: `C:\claude_base\tools\tamza_songs\pipeline\song_timing\from_scratch_idx\_work\merge_pilot\canon_flat.json` (~994 clusters)
- **DeepSeek script**: `C:\claude_base\tools\tamza_songs\pipeline\timecoder_handover\firstline_ds_v01.py`
- **DeepSeek output**: `C:\claude_base\tools\tamza_songs\pipeline\timecoder_handover\firstline_ds_out.json`
- **Handover tool**: `C:\claude_base\tools\tamza_songs\pipeline\timecoder_handover\nonh_handover.py`
- **Method doc**: `C:\claude_base\tools\tamza_songs\pipeline\timecoder_handover\HANDOVER_METHOD_v01_tomemex.md`
- **Reconstruction handoff**: `C:\claude_base\tools\tamza_songs\pipeline\timecoder_handover\FIRSTLINE_RECONSTRUCTION_HANDOFF_v01_tomemex.md`
- **Pilot verified lines**: `C:\claude_base\tools\tamza_songs\pipeline\timecoder_handover\verified\pX_1m8DlMbA.json`
- **Rules gap**: `C:\claude_base\tools\max_rules_harvest\max_rules_GAP_vs_autoload_v01.md`
- **Human Excel template**: `C:\Users\maxre\Downloads\????? ?? ?????.xlsx`
- **Channel inventory (upload dates)**: `C:\claude_base\tools\tamza_songs\output\channel_inventory.json`
- **Transcipts**: `C:\claude_base\tools\tamza_songs\pipeline\song_timing\transcripts\*.json`
- **Publish script**: `C:\claude_base\tools\tamza_songs\pipeline\scripts\publish_catalog.py`
- **Board**: invoke via `python C:/claude_base/branch_bulletin/bcast.py read`

### Key IDs
- Pilot video: `pX_1m8DlMbA` (2020-03-30, "?????? ?? ???????????? ?????")
- DeepSeek API key: `C:\claude_base\tools\tamza_songs\zSyncMain\ssh\deepseek_api_key_20260226.txt`
- DeepSeek model: `deepseek-chat` (the cheap/fast one)
- Sol (ASR machine): `192.168.1.113`, user `maxre`, key `~/.ssh/sol_key`
- teal16 (Centauri, video storage): `192.168.1.176`

### Key commands
```bash
# Run the handover tool
cd C:\claude_base\tools\tamza_songs\pipeline
python timecoder_handover/nonh_handover.py pick          # pick oldest good NONH video
python timecoder_handover/nonh_handover.py table <vid>   # produce handover table

# Run DeepSeek reconstruction (first --do it with a small test)
python timecoder_handover/firstline_ds_v01.py --n 30

# Publish (safe, backs up first)
cd scripts
python publish_catalog.py --dry-run    # preview only
python publish_catalog.py              # actual publish

# SSH Sol to check ASR
ssh -i ~/.ssh/sol_key maxre@192.168.1.113 "ps -eo pid,cmd | grep transcribe"
```

---

## GOTCHAS AND DEAD ENDS RULED OUT

### Critical gotchas (do NOT repeat)

1. **Never identify a song by title or announced author.** The matcher locks onto the host saying "????????" and grabs a famous Okudzhava song - even when a completely different song is being sung. This is the "famous-song drift" that caused all the wrong matches.

2. **`seg_text_head` is mostly the spoken intro, not the sung lyric.** The segmentation boundaries land on the announcer talking. You MUST read the FULL transcript window (time-sliced from the full transcript JSON, not the head snippet). The ASR inserts a `[??????]` marker where speech turns to song - the real first line sits right after it.

3. **Searching transcripts for text fails for English songs.** The Russian-tuned ASR garbles English into Cyrillic gibberish - so a text grep for "because" can't find the Beatles song even when it was sung. Only a smart LLM reading the audio/transcript can recognize songs through the garble.

4. **The shared worktree cwd-keying bug.** Both `bcast.py` (identity) and `worklog.py` (logs) key by current working directory. Cd-ing to `/c/claude_base` (the shared checkout) for git operations collides with other sessions' identities and splits worklogs across files. ALWAYS register from your OWN worktree and never cd to the shared dir when posting to the board or logging. This bit b29's identity (kept showing as c6) and split its worklog across 3 files.

5. **b15merger went silent overnight** - solo-owning a critical live-deploy task with no backup. Don't let one session block a publish. If an owner is unresponsive for >1 hour, park the task (logged) and surface to Max; don't cold-deploy something complex and live without the owner.

6. **Clustering exists but
