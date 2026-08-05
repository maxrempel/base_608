# Scribe handover - milestone 2 (~167K tokens)
# session: 20260727_spiring_albattani_d796c6_bfb8f7a0
# cwd: C:\claude_base\.claude\worktrees\inspiring-albattani-d796c6
# written: 2026-07-27 11:57:13 by deepseek-v4-pro

# HANDOVER - Telepathy Lesson 1: Anna Reels (Audio Done, Lipsync Done, 10 Spots Rendered)

---

## GOAL (Max's own words)

"Develop the script in Notion divided by 15-second pieces and produce an audio. [...] Produce the reels. Properly do that through MoMA. There should be like a full MoMA workflow. Where everything is going through MoMA and deviations and shortcuts are not permitted."

Take the approved Telepathy Lesson 1 narration from Notion, split it into spoken "spots" roughly 12-15 seconds each, voice it in Anna's cloned voice via Fish Audio, then produce lipsynced video reels through the MoMA pipeline using Alibaba DashScope Wan 2.6 i2v-flash. Pilot first: ten spots off the opening, about $4 budget ceiling. Eventually switch to the local Taygeta GPU box once that lipsync pipeline is fixed.

---

## DECISIONS MADE + WHY

1. **15-second ceiling is real, and it is Alibaba's limit, not ours.** The DashScope Wan 2.6 i2v-flash API hard-caps at 15 seconds, and the MoMA worker (`combo_wan26au_worker.py`) enforces `DURATION_MAX=15`. Max half-remembered this from the Nadali project and was right. The local Taygeta S2V pipeline has no such cap but is not yet wired into MoMA.

2. **Stick to the proven Alibaba/Fish cloud lane for this pilot.** Max considered switching to Taygeta immediately but the local S2V pipeline is hand-driven, not MoMA-integrated, and has only ever produced one 3-second test clip. He decided: spend ~$4 on the cloud pilot now, switch to Taygeta once fixed.

3. **Pricing: read MoMA's own expense ledger, never a vendor page or a code comment.** Max pushed back twice on my pricing estimates. The correct answer came from the `api_expenses` D1 table: **$0.025 per second** of finished lipsync video. The code comment in `combo_wan26au_worker.py` saying "$0.25 per 5s" was wrong (off by double) - it was written by a prior session from memory, not verified. I fixed the comment.

4. **The unit is a "spot" - one authored block = one clip.** Max settled on the word "spot" after trying "steals", "arrangements", "scenes". One spot = one image + one audio chunk + one lipsync reel. The recipe does NOT re-chunk the authored blocks; each SPOT block in the libretto maps verbatim to one wav and one reel.

5. **Images are randomly alternated, interchangeable.** Max: "We just randomly alternate the images. They're all interchangeable. It's just different angles. Just to chop things." The 10 spots rotate across the 14 distinct approved kitchen-table frames.

6. **Scene 11 / arrangement 42 renamed from "Tape 1Select" to "lesson1".** The prior name had a space and mismatched the `lesson1_production` audio folder. Rather than branching the project across two scene tags, I renamed the scene, the arrangement, and all 22 image job rows in D1 to `lesson1`. This keeps one tag for stills, audio, and reels.

7. **Token discipline: delegate reading to cheap models.** Max said the weekly limit gets eaten in four days. Rule adopted: phrase delegations as retrieval to Haiku/Sonnet, never as verdicts to Opus. Well-specified building goes to Sonnet. Only deciding and talking to Max stays in the main session.

8. **Voice question for parts 2 and 3 is still open (see below).**

---

## CURRENT STATE - WHAT IS DONE

**Audio (DONE, APPROVED by Max):**
- Libretto written: `C:\moma\sc10\sound_assembly\librettos\telepathy_lesson1_v01.md` - 10 SPOT blocks from the opening of Lesson 1, sourced from Notion page `3a60316f-5560-811c-9bc2-e787bfec70ab`.
- Recipe script: `C:\moma\sc10\sound_assembly\code\sass_recipe_anna_lesson_v01.py` - adapted from the UEI recipe, no re-chunking, pre-flight duration guard, `--dry-run` flag.
- Anna's voice rendered: run `anna_lesson1_v01_20260726_142639` in `C:\Users\maxre\OneDrive\Music\rehearsals\anna_lesson1\`, mirrored flat to `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\sound\lesson1_production`.
- 10 clips, 72 seconds total, min 5.2s, max 8.6s, avg 7.2s. All comfortably under 15s.
- Voice: Anna clone #22, Fish Audio s2-pro, reference id `da5554ea7be8458f9560e0a2d90553e3`, temperature 0.85, top_p 0.80, tone tag "[warm, calm, curious]".
- Max listened and approved.

**Audio run build (DONE):**
- Script: `C:\moma\sc10\combo_runner\code\build_lesson1_audio_run_v01.py`
- Run folder: `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\sound\lesson1_production\lines_20260726\`
- 10 lines, manifest with `line_hash` values.

**Lipsync reels (DONE, rendered, in MoMA):**
- Firing script: `C:\moma\sc10\combo_runner\code\fire_lesson1_reels_v01.py` - rotates 14 distinct approved PNGs, fires as `job_type='lipsie'`, `lipsync_tool='wan26flau'`, `scene_id='lesson1'`, `arrangement_id=42`, no `engine=` passed (let the guardrail set it), `birth_line_hash` from the manifest.
- Jobs 3403-3412, all `output_status='done'`.
- Actual cost from `api_expenses`: **$2.18** (inside Max's $4 ceiling).
- Output MP4s in: `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\scenes\scene10_images\combo_runner\data\output_lipsies\lesson1_lipsie_v{3403-3412}_wan26flau.mp4`
- Max reviewed them: "they look pretty, the reels."

**Bug fixed - audio resolver named-tag-with-digits (DONE, committed):**
- `C:\moma\sc10\combo_runner\code\audio_resolver.py` - `_scene_num()` was using a loose `re.search(r"\d+")` that extracted "1" from "lesson1" and treated it as film scene 1. The named-tag fallback also rejected any tag containing a digit (a Nadali-era assumption - "nadali" has no digits). All 10 reels errored on the first attempt.
- Fixed: `_scene_num()` now uses `re.fullmatch()` so only purely-numeric (or "scene"-prefixed numeric) tags become numbered film scenes. The named-tag branch no longer rejects digits.
- Verified: `resolve 3403 -> {'ok': True, 'audio_path': '...anna_001_spot01.wav', 'duration': 7.43, 'match': 'line_hash'}`.

**Cost comment fixed (DONE, committed):**
- `combo_wan26au_worker.py` line 23: was `# Cost: ~$0.25 per 5s 720P clip (flash tier)`, now reads `# Cost: ~$0.025/s 720P clip (~$0.125 per 5s, ~$1.50/min) per api_expenses ledger`.

**Notion rename (partial):**
- The three "APPROVED - Telepathy Lesson 1" script pages renamed from "Training Tape" to "Lesson".
- Parent page "Telepathy Training Tape Outline" and sibling "Registry of Ideas and Instructions" NOT YET renamed.

**Commit:** All changes committed and pushed to master on the MOMA repo. Commit message references scale medium, includes the resolver fix, the cost-comment fix, the lesson1 libretto, recipe, build script, and fire script.

---

## EXACT NEXT STEP

Max has the 10 rendered reels and likes them. The immediate next thing he asked about is the voice for parts 2 and 3. The question I left him with:

> Parts two and three of the script are written in first person, with a personal memory in them - "I remember sitting quietly with a small group once." Anna is saying it. Should she keep speaking that as her own, or should I rewrite those to be voiced as yours?

He has not yet answered. That is the blocking question.

Once he answers, the next work is:
1. Produce Anna's audio for the remaining spots of Lesson 1 (parts 2 and 3, or however the script redivision lands).
2. Fire the lipsync reels for those spots.
3. Eventually assemble the full lesson video in MoMA.

---

## OPEN QUESTIONS AWAITING MAX

1. **Voice for parts 2 and 3 (active, blocking).** "I remember sitting quietly with a small group once..." - Anna's voice as her own, or rewritten to be Max's voice?

2. **Duplicate Notion page.** Two pages both titled "Telepathy Training Tape Outline": `3a60316f-5560-8188-853f-de48b6654b83` and `3a60316f-5560-8167-bba3-eb50eaef92db`. This is the branching Max warns about. Not resolved.

3. **"As this tape ends" wording.** The Final Five Minutes script says "So as this tape ends" - needs rewording to "lesson" after the rename.

4. **Scene 10 / arrangement 41 still named "Tape 1".** That is the wider unselected pool of 43 Anna images. Deliberately left alone, but worth flagging: it is the old name.

5. **Notion rename still incomplete.** "Telepathy Training Tape Outline" (both copies), "Registry of Ideas and Instructions", and "Tape 2" page not yet renamed to "Lesson".

6. **Taygeta local lipsync.** Max wants to switch to the local GPU box once it's fixed. The S2V stack is installed and proven (one 3s test clip), but the MoMA worker (`combo_s2v_local_worker.py`) has not been built. ComfyUI is not currently running on the box.

---

## KEY PATHS AND IDS

**MoMA repo:** `C:\moma` (main repo, NOT a worktree)

**Scene and arrangement:**
- Scene 11, name `lesson1` (renamed from "Tape 1Select"), created 2026-07-25
- Arrangement 42, name `lesson1`, scene_id 11

**Approved Anna stills (14 distinct PNGs):**
- `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\telepathy_tapes\tape1select_output\` - zoom_in.png, zoom_out.png, cam_left.png, cam_right.png, cam_up.png, cam_down.png, table_low.png, table_profile_r.png, v2_front.png, v2_left.png, v2_right.png, v2_high.png, v2_profile_l.png
- Plus `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\telepathy_tapes\tape1_output\kitchen_night_v3.png` (used by two jobs)
- Jobs 3381-3402 (15 approved out of 22), all `arrangement_id=42`

**Audio:**
- Libretto: `C:\moma\sc10\sound_assembly\librettos\telepathy_lesson1_v01.md`
- Recipe: `C:\moma\sc10\sound_assembly\code\sass_recipe_anna_lesson_v01.py`
- Run: `C:\Users\maxre\OneDrive\Music\rehearsals\anna_lesson1\anna_lesson1_v01_20260726_142639\`
- Mirror: `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\sound\lesson1_production\`
- Per-line run: `...\lesson1_production\lines_20260726\`
- Build script: `C:\moma\sc10\combo_runner\code\build_lesson1_audio_run_v01.py`

**Lipsync:**
- Fire script: `C:\moma\sc10\combo_runner\code\fire_lesson1_reels_v01.py`
- Worker: `C:\moma\sc10\combo_runner\code\combo_wan26au_worker.py` (pid file: `C:\moma\sc10\combo_runner\local_state\wan26au_worker_pid.txt`)
- Log: `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\scenes\scene10_images\combo_runner\data\wan26au_worker.log`
- Output reels: `...\combo_runner\data\output_lipsies\lesson1_lipsie_v{3403-3412}_wan26flau.mp4`
- Reels database: Cloudflare D1, table `jobs`, table `api_expenses`

**Notion pages:**
- Lesson 1 Min 0-5: `3a60316f-5560-811c-9bc2-e787bfec70ab` (this produced the 10 pilot spots)
- Lesson 1 Min 5-10: `3a60316f-5560-81e1-894c-ce3c6681d973`
- Lesson 1 Final Five: `3a60316f-5560-812d-bb40-cd3d3e289c54`
- Parent (duplicate!): `3a60316f-5560-8188-853f-de48b6654b83` and `3a60316f-5560-8167-bba3-eb50eaef92db`

**Voice:**
- Anna clone #22, reference id `da5554ea7be8458f9560e0a2d90553e3`
- Fish Audio s2-pro, temp 0.85, top_p 0.80
- Key file: `C:\Users\maxre\Nextcloud\zSyncMain\ssh\fishaudio_api_key_20260226.txt`
- Alibaba key: `C:\Users\maxre\Nextcloud\zSyncMain\ssh\dashscope_beijing_api_key_20260329.txt`
- D1 auth: `C:\Users\maxre\Nextcloud\zSyncMain\ssh\moma_d1_auth_20260409.txt`

**Python interpreter (used everywhere):** `C:\Users\maxre\AppData\Local\Python\pythoncore-3.14-64\python.exe` (and `pythonw.exe` for detached workers)

---

## GOTCHAS AND DEAD ENDS RULED OUT

1. **Never pass `engine=` on a lipsie fire.** `fire_job` auto-forces `engine = lipsync_tool`. Passing `engine=` or relying on the DB default `'wan22'` lets `combo_worker` steal the job and render a silent clip. This bit the Nadali project twice. The lesson1 fire script does not pass `engine=`.

2. **Pass `birth_line_hash`, NOT `line_hash`.** The merge-hash guard in `moma_db.py` line 739 fires only on `line_hash` and would reject a lipsie hash (no `script_lines` row exists for it). Nadali and lesson1 both use `birth_line_hash`.

3. **Named project tags with digits now work.** The `_scene_num()` loose-regex bug was the root cause of all 10 reels failing on the first attempt. Fixed with `re.fullmatch()`. Tags like `lesson1`, `lesson2` etc. are now handled correctly. **But the worker must be restarted to pick up the patched `audio_resolver.py`** - the running process loads modules once at startup.

4. **Scene tag with a space = folder-name pain.** `paths.scene_production_dir()` derives the audio folder from the scene tag. A space in the tag (`"Tape 1Select"`) would produce a folder called `Tape 1Select_production` with a space in it. Lesson learned: use single-word tags like `lesson1`.

5. **`combo_db.sqlite` is stale.** Never touch it. Always go through `moma_db.connect_db()` / `D1Client`.

6. **The worker pid file is deliberately OFF Nextcloud.** `C:\moma\sc10\combo_runner\local_state\wan26au_worker_pid.txt` - if it were on Nextcloud, the VFS could leave the placeholder online-only, failing `open()` with Errno 22 and silently killing the worker's singleton check.

7. **No `output_error` column in the jobs table.** The D1 schema does not have it. Don't try to set it.

8. **The Nadali UEI recipe re-chunks blocks itself** - it would have destroyed the authored spot split. That is why a new recipe was written for the lessons rather than editing the UEI one.

9. **Wan 2.6 i2v-flash minimum audio is 3 seconds, padded with 0.5s silence each side.** The worker handles this automatically, but it adds ~1 second of billed time per clip.

10. **Taygeta ComfyUI is not running.** To use the local lipsync lane, you must start ComfyUI on the GPU box, build the MoMA worker, and time a real render at the target resolution.

11. **The Notion duplicate is live.** Two pages both named "Telepathy Training Tape Outline." Any rename or edit that hits only one of them creates divergence. Max must decide which is canonical.

12. **Fish Audio has no budget guard.** The
