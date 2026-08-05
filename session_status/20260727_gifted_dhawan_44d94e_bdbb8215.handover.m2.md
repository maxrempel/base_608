# Scribe handover - milestone 2 (~167K tokens)
# session: 20260727_gifted_dhawan_44d94e_bdbb8215
# cwd: C:\claude_base\.claude\worktrees\gifted-dhawan-44d94e
# written: 2026-07-27 11:57:36 by deepseek-v4-pro

# HANDOVER - Telepathy Lesson 1: Pilot Reels Complete, Script Parts 2-3 Remain

---

## GOAL (in Max's words)

Max: "Proceed with the spots. Properly do that through MoMA. There should be like a full MoMA workflow. Where everything is going through MoMA and deviations and shortcuts are not permitted."

Produce the Telepathy Lesson 1 video - Anna narrating to the trainee - in roughly-15-second "spots," each one still image plus lipsynced audio. Audio through Fish Audio (Anna clone #22), lipsync through Alibaba DashScope wan2.6-i2v-flash, everything fired as MoMA jobs. Eventual endgame: switch to local Taygeta GPU rendering once it is fixed, but the cloud lane is the production lane for now.

---

## DECISIONS MADE AND WHY

### Pricing method: read our own ledger, not vendor pages
Max pushed back hard on my first two price estimates ($45 from a code comment, $77 from a web search). He said: "I think it would be nicer if you just went into MoMA and MoMA has the pricing, it logs the price, the expenses." The real answer came from the `api_expenses` D1 table: **$0.025 per second of finished lipsync video**. 255 prior jobs, $63.15 total, unambiguously consistent across all durations. The code comment in combo_wan26au_worker.py line 23 saying "~$0.25 per 5s" was wrong (off by double) - it has since been corrected.

### Pilot first, full lesson later
Max: "Let's spend maybe $4 for now and do the first piece. And then, by that time, I think we'll fix the TIGETA video maker and then we'll switch to that." The pilot is 10 spots from the opening of the script, ~72 seconds of narration, ~$2.18 actual billed cost.

### One spot = one image = one lipsync reel, hand-authored not auto-chunked
Max chose "spot" as the unit. The UEI/Nadali recipe auto-chunks free-flowing prose into ~12-second pieces. For this lesson, the spots are hand-authored in the libretto - one SPOT block is one clip verbatim, no re-chunking. This required a new TTS recipe (`sass_recipe_anna_lesson_v01.py`) rather than reusing the UEI one, because the UEI parser only accepts INTRO/INTERMISSION/CONCLUSION titles and would have destroyed the authored split.

### Scene rename: "Tape 1Select" ? "lesson1"
The approved stills lived under scene_id='Tape 1Select' (scene 11, arrangement 42, 22 image jobs). The new audio mirror was `lesson1_production`. Rather than split one project across two scene tags (the branching Max hates), I renamed scene 11, arrangement 42, and all 22 image job rows from 'Tape 1Select' to 'lesson1' in the D1 database. Scene 10 ('Tape 1', the wider unselected pool of 43 images) was deliberately left alone.

### Image rotation: random, interchangeable
Max: "we just randomly alternate the images. They're all interchangeable. It's just different angles. Just to chop things." The 10 spots were assigned different stills from the 14 approved kitchen-table frames. Exact assignments are in the job list below.

### Token discipline
Max: "when it is rational to offload to cheaper models, please do that... Let's learn the art of saving the tokens." Rule adopted: send file hunting and mechanical building to Sonnet/Haiku, keep judgment in the main session. Phrase delegations as retrieval ("print every command that mentions fish audio"), never as verdict ("is this the right recipe").

---

## CURRENT STATE - WHAT IS DONE

### Audio stage: DONE and approved
- Libretto: `C:\moma\sc10\sound_assembly\librettos\telepathy_lesson1_v01.md` - 10 SPOT blocks
- TTS recipe: `C:\moma\sc10\sound_assembly\code\sass_recipe_anna_lesson_v01.py`
- Run: `C:\Users\maxre\OneDrive\Music\rehearsals\anna_lesson1\anna_lesson1_v01_20260726_142639`
- Mirror: `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\sound\lesson1_production\`
- 10 wav files, 72 seconds total, all under 15s ceiling (min 5.2s, max 8.6s, avg 7.2s)
- Max listened and approved: "okay now produce the lip the reels"

### Lipsync reels: DONE, reviewed, and approved
- Audio run built: `...\sound\lesson1_production\lines_20260726\manifest.json`
- Build script: `C:\moma\sc10\combo_runner\code\build_lesson1_audio_run_v01.py`
- Fire script: `C:\moma\sc10\combo_runner\code\fire_lesson1_reels_v01.py`
- 10 MoMA lipsie jobs fired: **3403-3412**, all status='done'
- All saved to: `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\scenes\scene10_images\combo_runner\data\output_lipsies\lesson1_lipsie_v{3403..3412}_wan26flau.mp4`
- Arrangement 42, scene_id='lesson1'
- **Actual cost: $2.18** (from api_expenses ledger)
- Max reviewed: "I looked at the videos and they look pretty, the reels."

Job-to-image map:

| Job | Spot | Image | Duration |
|-----|------|-------|----------|
| 3403 | 01 | zoom_in.png | 7.43s |
| 3404 | 02 | cam_left.png | 6.64s |
| 3405 | 03 | v2_front.png | 5.67s |
| 3406 | 04 | table_profile_r.png | 8.64s |
| 3407 | 05 | cam_right.png | 8.41s |
| 3408 | 06 | v2_left.png | 5.20s |
| 3409 | 07 | zoom_out.png | 6.27s |
| 3410 | 08 | cam_up.png | 8.54s |
| 3411 | 09 | v2_right.png | 7.29s |
| 3412 | 10 | table_low.png | 7.48s |

Motion prompt for all: "A woman sits at a kitchen table at night, speaking calmly and directly to the camera. Natural subtle head movement and blinking, gentle breathing, warm lamplight. Static camera, no zoom, no cuts."

### Infrastructure: bug fixed, committed, pushed
- **audio_resolver.py v05** - three edits. The old `_scene_num()` did a loose `re.search(r"\d+")` that grabbed the first digit run from any tag, so "lesson1" was misread as film scene 1. Fixed to a full-match regex that only treats a tag as a numbered scene when the whole string is a number (optionally 'scene'-prefixed). The named-tag fallback branch also dropped its no-digits test (a Nadali-era assumption - 'nadali' has no digits, but 'lesson1' does). This fix makes lesson2, lesson3, etc. work out of the box.
- **combo_wan26au_worker.py** - line 23 cost comment fixed from "$0.25 per 5s" to "$0.025/sec (~$0.125 per 5s, ~$1.50/min)".
- Commit pushed to master on the C:\moma repo. All five files included: audio_resolver.py, combo_wan26au_worker.py, build_lesson1_audio_run_v01.py, fire_lesson1_reels_v01.py, sass_recipe_anna_lesson_v01.py, telepathy_lesson1_v01.md.

---

## EXACT NEXT STEP

Max approved the pilot reels. The natural next step is to proceed with the remaining script. Parts 2 and 3 ("Minutes 5-10" and "Final Five Minutes") are the remaining ~13 minutes of the 15-minute lesson. The pipeline is proven end to end. However, one decision is needed first (see Open Questions below) - whose voice speaks parts 2 and 3, because they are written in first person with personal anecdotes.

What to do after that decision:
1. Pull Notion pages `3a60316f-5560-81e1-894c-ce3c6681d973` (Minutes 5-10) and `3a60316f-5560-812d-bb40-cd3e3d288c54` (Final Five Minutes) into the libretto as additional SPOT blocks.
2. Run the TTS recipe for those spots.
3. Present the audio to Max for approval.
4. Fire the lipsie jobs through MoMA.
5. Fix the "as this tape ends" wording in the Final Five Minutes text (should be "lesson").
6. Finish the remaining Notion renames (see below).

---

## OPEN QUESTIONS STILL AWAITING MAX

### 1. First-person voice - Anna or Max?
Parts 2 and 3 of the script contain lines like "I remember sitting quietly with a small group once" and "I once spent time with a group of people." The question I raised: is Anna speaking these as her own, or should they be rewritten as Max's voice? This was the last thing I asked before the session ended. Max responded about reviewing the reels but did not answer this question.

### 2. Duplicate Notion page
There are TWO pages both titled "Telepathy Training Tape Outline": IDs `3a60316f-5560-8188-853f-de48b6654b83` and `3a60316f-5560-8167-bba3-eb50eaef92db`. Max's #1 disaster rule is branching from duplicate versions. This must be surfaced explicitly - do not silently resolve it.

### 3. Remaining Notion renames
Max said "We renamed tapes to lessons. Training tapes to telepathy lessons." Done: the three APPROVED Lesson 1 script pages. Still to rename:
- "Telepathy Training Tape Outline" (both copies - see #2 above)
- "Telepathy Training Tapes - Registry of Ideas and Instructions" (`3a60316f-5560-81cb-816e-d9ad61bca8a1`)
- "APPROVED - Telepathy Training Tape 2 - Minutes 0-5" (`3a80316f-5560-81ad-a023-e17bdc46ff4e`)

### 4. Scene 10 / arrangement 41 still named 'Tape 1'
Scene 11 was renamed to 'lesson1'. Scene 10 ('Tape 1', 43 images, the wider unselected pool from which the 14 approved frames were drawn) was deliberately left alone. Max may want it renamed or archived.

### 5. "So as this tape ends" wording
In the Final Five Minutes text, this line should be "So as this lesson ends" to match the rename.

---

## KEY PATHS, IDS, AND COMMANDS

### Paths
- **Script libretto:** `C:\moma\sc10\sound_assembly\librettos\telepathy_lesson1_v01.md`
- **TTS recipe:** `C:\moma\sc10\sound_assembly\code\sass_recipe_anna_lesson_v01.py`
- **Audio mirror:** `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\sound\lesson1_production\`
- **Audio run:** `...\sound\lesson1_production\lines_20260726\manifest.json`
- **Build script:** `C:\moma\sc10\combo_runner\code\build_lesson1_audio_run_v01.py`
- **Fire script:** `C:\moma\sc10\combo_runner\code\fire_lesson1_reels_v01.py`
- **Approved stills:** `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\telepathy_tapes\tape1select_output\` (14 distinct PNGs)
- **Lipsync output:** `...\scene10_images\combo_runner\data\output_lipsies\lesson1_lipsie_v{job}_wan26flau.mp4`
- **Worker log:** `...\scene10_images\combo_runner\data\wan26au_worker.log`
- **Worker pid file:** `C:\moma\sc10\combo_runner\local_state\wan26au_worker_pid.txt` (OFF Nextcloud)
- **Anna voice key:** `C:\Users\maxre\Nextcloud\zSyncMain\ssh\fishaudio_api_key_20260226.txt`
- **DashScope key:** `C:\Users\maxre\Nextcloud\zSyncMain\ssh\dashscope_beijing_api_key_20260329.txt`
- **D1 auth:** `C:\Users\maxre\Nextcloud\zSyncMain\ssh\moma_d1_auth_20260409.txt`

### MoMA IDs
- **Scene:** id=11, name='lesson1'
- **Arrangement:** id=42, name='lesson1'
- **Pilot lipsie jobs:** 3403-3412 (all done)
- **Approved still jobs:** 3381,3382,3383,3384,3385,3386,3387,3388,3393,3396,3397,3398,3399,3400,3402 (15 approved out of 22)

### Notion page IDs
- Minutes 0-5 (pilot source): `3a60316f-5560-811c-9bc2-e787bfec70ab`
- Minutes 5-10: `3a60316f-5560-81e1-894c-ce3c6681d973`
- Final Five Minutes: `3a60316f-5560-812d-bb40-cd3e3d288c54`
- Duplicate outlines: `3a60316f-5560-8188-853f-de48b6654b83` and `3a60316f-5560-8167-bba3-eb50eaef92db`
- Registry page: `3a60316f-5560-81cb-816e-d9ad61bca8a1`
- Tape 2 page: `3a80316f-5560-81ad-a023-e17bdc46ff4e`

### Anna voice parameters
- Clone: reference_id `da5554ea7be8458f9560e0a2d90553e3` (clone #22)
- Model: s2-pro, 44100 Hz wav
- Temperature: 0.85, top_p: 0.80
- Tone tag prepended: `[warm, calm, curious]`

### Pricing
- **$0.025 per second** of lipsync video (Alibaba DashScope wan2.6-i2v-flash, 720P)
- **$1.50 per minute** of finished video
- 15-minute lesson ? ~$25 including silence padding and whole-second billing
- Fish Audio TTS is pennies by comparison; the lipsync is essentially all the cost

---

## GOTCHAS AND DEAD ENDS ALREADY RULED OUT

### The audio_resolver named-tag-with-digit bug - FIXED
**Do not reintroduce.** The old `_scene_num()` did a loose `re.search(r"\d+")` that grabbed the first digit run from any tag, so "lesson1" was misread as film scene 1 and the resolver looked for a nonexistent `scene1_production` folder. The named-tag fallback branch also had a `not any(ch.isdigit
