# Scribe handover - milestone 6 (~460K tokens)
# session: 20260618_pedantic_mendel_0bee59_2609da4a
# cwd: C:\claude_base\.claude\worktrees\pedantic-mendel-0bee59
# written: 2026-06-18 08:07:55 by deepseek-v4-pro

# Scribe Handover - Tamza Pipeline (B26juniorconnector session)

---

## GOAL (Max's own words, in order of emphasis)

1. **Publish newly-identified NONH songs to the live site** - the project is reaching its end point (clean DB + live catalog). Songs that are confidently identified should go live. Unknowns stay held.
2. **KILL ALL CANON TITLES.** Song identity = **FIRST SUNG LINE ONLY.** No names, no announced titles, no matched canon songs. Everything verified by a smart LLM (DS4-nonflash minimum), spot-checked by the manager (me/B26). This is the cardinal rule that older sessions knew and newer ones forgot.
3. **NONH ? human timecoder handover** - pick the oldest good not-human-done video, build a handover table in the exact Excel format of the human team's "????? ?? ?????.xlsx", double-check it, hand to the timecoders. Repeat weekly.
4. **Manage B27** - B27 does the hard lifting (LLM reading transcripts to extract verified first sung lines). I (B26/B26juniorconnector) stay as manager/connector: coordinate owners, set priorities, spot-check, don't do the heavy implementation myself.
5. **Drive tasks to completion overnight** while Max sleeps. Keep autonomous timers running on critical-path owners.

---

## DECISIONS MADE + WHY

### 1. Go-Live Gate: 3-path OR logic (Max refined)
- **Path A:** Confident song-text match (~12-20% of segments)
- **Path B:** Clear spoken intro ("this is my song" / names composer-poet)
- **Path C:** Intro names a performer that matches the clean performer DB (most expansive path - uses performer attribution even when the song itself is unknown)
- **Fail all 3 ? held**
- A segment passes ANY one path = publishable.
- **Max later OVERRODE:** Path A is unsafe for old/fringe videos (famous-song drift). Performer-introduced (B/C) is safe. Then Max went further: KILL ALL TITLES entirely - song identity is first sung line only, not matched titles.

### 2. Safety stance: data-safe, reversible
- Never deploy without backup of the live catalog first
- Keep the held/unknown set stored on disk
- `publish_catalog.py` has `--dry-run` and reversibility built in - use `--dry-run` for homework before any live action
- Publish b15merger stalled overnight: b15merger disarmed its timer (per "idle sessions disarm" order), so manager (B26) couldn't wake it. **Live-publish did NOT happen overnight.** Parked for Max's morning.

### 3. Song identification: titles killed, first-lines-only
- The old mechanical matcher (char-ngram + fuzzy) produced famous-song drift - it would hear an announcer say "????????" and tag a famous Okudzhava song that wasn't actually sung.
- **Max's hard correction:** No canon titles anywhere. Song identity = verified **first sung line**, extracted by a smart LLM actually READING the transcript. No blind Python matching.
- Titles stripped from the handover tool, b15merger's gate, everything.
- The famous-song drift is worst in old/fringe videos where Tamza sings obscure songs.

### 4. LLM must READ the data - no blind mechanical pipelines
- "Only one Margarita in DB" - deciding who's a distinct person needs an LLM to actually reason about the data, not a Python name-collapse.
- This applies to performer identity, song clustering, everything.
- The principle was lost between older sessions and the current team.

### 5. Session management overnight
- AWAKE + autonomous: b7nonhtimes (ASR) and b15merger (publish). b9 stays awake for full 2842-vid backup (Max's order).
- ASLEEP: everyone else.
- B26 holds the 4-min watch, widens to 20-min when stable.

### 6. B27 priority
- B27 got two tasks: (a) the critical-path first-line extraction from all NONH segments, (b) a rules-gap doc from B25handoverer.
- B26 set PRIORITY 1 = first-lines (publish-blocking). Rules-gap is secondary/rerouted.
- B27 went silent for ~25+ min of repeated pings; no output file found. B26 produced a small gold-standard first-line sample as a target to unblock.

---

## CURRENT STATE (what's done, what's in flight)

### DONE
- **Handover tool** (`nonh_handover.py`): picks oldest good NONH video, joins upload dates from `channel_inventory.json` (no YouTube hit needed), builds a table in the exact 11-column human Excel format matching "????? ?? ?????.xlsx" (per-concert tabs, performer-grouped, timecodes as &t= links).
- **First handover table:** video `pX_1m8DlMbA` (2020-03-30, "?????? ?? ???????????? ?????"), 31 performer turns, 47 segments.
- **Multi-pass LLM QC on that table:** two passes found only 2/10 matched song titles trustworthy; 8 drift cases flagged "?????????". Root cause documented: matcher locked onto announcer naming the author, not the sung lyric.
- **Titles killed** in the handover tool and b15merger's gate (titles-free split v02: 6997 publishable / 68 truly-unknown, but awaits b27's verified first-lines before the numbers are real).
- **7 cardinal rules enshrined** by b29 into a method doc + START-HERE handover - pushed.
- **HUM remap catalog = ALREADY LIVE** (verified via `publish_catalog.py --dry-run`: "NO CHANGE since last publish"). No deploy needed for the human-side re-timing.
- **All 93 caption-disabled videos now on teal16** (b9 finished the last pulls, 0 walls).
- **ASR running healthy on Sol:** Sol ASR (PID 52723 on Sol CPU, `transcribe_v02.py`) grinding through all 93. b7nonhtimes drains batches to Pine ? segments ? identifies autonomously. Pipeline validated end-to-end: noisy ASR still yields reliable performer attribution (intros transcribe clean), garbled song lyrics stay "verify", English/silent videos correctly fall to honest-unknown.
- **Video backup (b9):** full 2842-video Tamza backup continuing autonomously on Lak.
- **B27's archive cleanup plan** ready (55 scripts + 2 data files, grep-verified zero live imports, reversible) - waiting for owner sign-off (b9 approved, b15M needed for `_batch_aligner_v01.py` doc conflict). Parked for Max's morning signoff.

### IN FLIGHT (need action/awaiting)
- **b27: LLM-verified first sung line extraction** for all NONH segments - this is the CRITICAL PATH blocking the live-publish. B27 has been silent despite 2 pings. No output file found on disk. B26 posted a gold-standard sample (pX_1m8DlMbA, 6 segments) as a method demo + target.
- **b15merger: titles-free live-publish gate** - b15merger is back online (wasn't stalled, just had disarmed timer overnight per idle-sessions policy). Produced a dry-run split but it still carried titles. Re-tasked to consume b27's verified first-lines when they land.
- **ASR on Sol** - still grinding. Was at 54/93 last known count. Progressive, resumable. b7nonhtimes draining to local `song_timing/transcripts/<vid>.json` as transcripts accumulate.
- **Handover doc v03** - pushed with tonight's additions.

---

## EXACT NEXT STEP

1. **Get b27 to deliver the LLM-verified first-sung-line extraction.** This is the single publish-blocking item. The gold-standard sample is posted on the board for b27 to match. If b27 remains unresponsive, Max may need to assign a fresh session or have B26 (Opus) do the pilot video directly.
2. **Once first-lines land ? b15merger's gate consumes them ? publish the titles-free catalog** (data-safe: backup live first, reversible rollback).
3. **Max to sign off on archive cleanup** (B27's plan, the `_batch_aligner` doc conflict with b15M).
4. **Continue the 5-min autonomous watch** (Max set 5mt cadence).

---

## OPEN QUESTIONS AWAITING MAX

1. **Live-publish:** b15merger went silent overnight (timer disarmed). It's back now. Does Max want B26 to re-engage b15merger for the publish, or hand to a fresh session?
2. **B27 first-lines:** B27 has been unresponsive on the critical path. Does Max want to reassign, wait longer, or have B26 (Opus) do the pilot video directly?
3. **Archive cleanup sign-off:** Ready, reversible, parked. Sign off?
4. **Should B26 (Opus) directly read the transcript data** for the pilot video to prove the first-line method, or keep delegating to B27?

---

## KEY PATHS / IDs / COMMANDS

| Item | Path / ID |
|------|-----------|
| **Handover tool** | `C:\claude_base\tools\tamza_songs\pipeline\timecoder_handover\nonh_handover.py` |
| **First handover table** | `C:\claude_base\tools\tamza_songs\pipeline\timecoder_handover\tables\handover_2020-03-30_pX_1m8DlMbA.tsv` |
| **Gold-standard first-line sample** | Posted to bcast board (video `pX_1m8DlMbA`, 6 segments) |
| **QC verdicts** | `C:\claude_base\tools\tamza_songs\pipeline\timecoder_handover\qc\pX_1m8DlMbA.json` |
| **Human Excel reference** | `C:\Users\maxre\Downloads\????? ?? ?????.xlsx` (one sheet per concert, 11 columns) |
| **Channel inventory (upload dates)** | `C:\claude_base\tools\tamza_songs\output\channel_inventory.json` |
| **ASR transcripts** | Sol: `~/nonh_transcribe/out/` ? local: `song_timing/transcripts/<vid>.json` |
| **Publish catalog script** | `C:\claude_base\tools\tamza_songs\pipeline\scripts\publish_catalog.py` (safe `--dry-run`, reversible) |
| **Board/bcast** | `python "C:/claude_base/branch_bulletin/bcast.py" read` |
| **Worklog** | `python C:/claude_base/compaction_kb/scripts/worklog.py log "..."` |
| **Owner IDs for wake** | b7nonhtimes (ASR+seg), b15merger (publish gate+live push), b27 (first-lines LLM work), b9 (backup), b15M (archive signoff) |
| **Selected video** | `pX_1m8DlMbA` (2020-03-30, 47 segments, 10 originally identified - now stripped to first-lines-only) |

---

## GOTCHAS / DEAD ENDS RULED OUT

1. **Famous-song drift is THE gotcha.** The mechanical matcher (char-ngram + fuzzy align) produces WRONG titles because it hears the announcer name an author/composer and grabs that person's most famous song. Do not use matched canon titles as truth. Symptom: announcer says "????????" ? matcher grabs "??????? ????????? ?????????" even though the performer is singing a different song entirely.

2. **Announcer intro bleed.** Many segments' "first lines" in the drafts are actually spoken intro/chatter, not the sung lyric. The LLM must strip the intro to find the real first sung line.

3. **b15merger's timer disarmed overnight.** Per the "idle sessions disarm their timers" policy, b15merger didn't receive any of the repeated wake calls overnight. It wasn't ignoring them - the wake mechanism literally couldn't land. This is why the live-publish didn't happen. The fix: Max pings the session directly.

4. **No Opus read the transcript.** The entire song identification chain was done by mechanical matchers - zero intelligent reading. This is the root failure. Fix: LLM must actually read the heard text and reason about what song it is.

5. **Titles killed everywhere.** Don't reintroduce canon titles. The handover tool now strips them, b15merger's gate strips them, and B27's first-line extraction should produce only verified first sung lines.

6. **"Only one Margarita in DB" / performer identity.** Name-collapsing in Python is blind. Performer identity merging (deciding which "?????????" is the same person across different videos) requires an LLM to reason about context. This hasn't been done yet.

7. **The cardinal rules were lost between sessions.** Older sessions knew "first-lines-only, LLM-reads-the-data, no titles." The current team drifted into blind mechanical pipelines. b29 just enshrined them into a method doc - but every new session needs to pick them up from START-HERE.

8. **The HUM remap catalog is already live** - don't re-deploy it. `publish_catalog.py --dry-run` says "NO CHANGE since last publish." The remaining publish work is the NONH gate only.

9. **Do NOT hit YouTube for metadata.** `channel_inventory.json` (935 videos) has upload_date and title for every video - use it instead of yt-dlp. Hit YouTube only for the actual video downloads/backup.
