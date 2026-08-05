# VERBATIM user (Max) log - session 4f3f6a59-a6ed-4958-81fa-7874a46b36c1
# cwd: C:\claude_base\.claude\worktrees\priceless-snyder-07082c
# Every line Max typed, saved verbatim, so it survives compaction.
# Recover specs / investigate trouble by reading this file.


## [2026-07-26 14:03:35] turn 1
<task-notification>
<task-id>ae2b74cbc01d6c8e5</task-id>
<tool-use-id>toolu_01GZ9A5u7Kcwfr8aRhWGWsAS</tool-use-id>
<output-file>C:\Users\maxre\AppData\Local\Temp\claude\C--claude-base--claude-worktrees-priceless-snyder-07082c\4f3f6a59-a6ed-4958-81fa-7874a46b36c1\tasks\ae2b74cbc01d6c8e5.output</output-file>
<status>completed</status>
<summary>Agent "Read Taygeta setup docs" finished</summary>
<note>A task-notification fires each time this agent stops with no live background children of its own. The user can send it another message and resume it, so the same task-id may notify more than once.</note>
<result>Based on my thorough search of the documentation, I can now provide you with a comprehensive report:

---

## Taygeta GPU Box Video Generation Status (192.168.1.142)

**ComfyUI:** INSTALLED and PROVEN WORKING. Runs headless at `~/ComfyUI/` with venv `~/ComfyUI/venv` using torch 2.11.0+cu128. Started via: `~/ComfyUI/venv/bin/python main.py --listen 127.0.0.1 --port 8188`. API endpoint: http://127.0.0.1:8188. Log output: `~/setup/logs/comfyui.log`.

**Wan 2.2 S2V (Speech-to-Video) Lipsync:** INSTALLED and PROVEN WORKING end-to-end. Tested successfully: h264 480x480 49 frames at 3.06s, ~15s per step, uses ~13GB of the available 16GB VRAM on RTX 5060 Ti.

**Model Files (all in ~/ComfyUI/models/):** All INSTALLED and verified:
- `diffusion_models/wan2.2_s2v_14B_fp8_scaled.safetensors` (15.3GB)
- `text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors` (6.3GB)
- `audio_encoders/wav2vec2_large_english_fp16.safetensors` (0.6GB)
- `vae/wan_2.1_vae.safetensors` (0.25GB)

Models migrated to green24 (`/mnt/green24/comfyui/downloads/models_v01`) via migration script, symlinked back into ComfyUI folder.

**Clip Length Limits:** Single WanSoundImageToVideo pass limited to ~5s. For longer renders (target 15s), use WanSoundImageExtend to chain 3 sections sequentially with audio slicing.

**Invocation Path:** Fire script at `~/setup/scripts/s2v_fire.py`. Method: (1) place portrait in `~/ComfyUI/input/portrait.jpg` + audio in `~/ComfyUI/input/speech.wav`, (2) run the fire script, (3) poll `http://127.0.0.1:8188/history/&lt;prompt_id&gt;` for completion, (4) retrieve mp4 from `~/ComfyUI/output/`.

**Key Docs:**
- Full method: `C:\claude_base\tools\taygeta_s2v\s2v_video_method_v01_tomemex.md`
- Model migration script: `C:\claude_base\tools\taygeta_housekeeper\migrate_comfy_models_v01.sh`
- Model source note: Comfy-Org/Wan_2.2_ComfyUI_Repackaged on HuggingFace

**MoMA Integration:** PLANNED, not yet built. Blueprint exists for a `combo_s2v_local_worker.py` that would claim jobs tagged `lipsync_tool='s2vlocal'`, push still+voice to taygeta via SSH, POST to ComfyUI, poll, and pull output back into MoMA's pipeline.</result>
<usage><subagent_tokens>63511</subagent_tokens><tool_uses>41</tool_uses><duration_ms>133697</duration_ms></usage>
</task-notification>

## [2026-07-26 14:08:33] turn 2
Let's now focus on the traditional method. We just recently produced audio for another piece which was... Anna was introducing my presentation, so it was me, Anna and I were alternating. So everything worked and we did it through API with Alibaba. Let's focus on that. So make a plan and let's look at it.

## [2026-07-26 14:10:11] turn 3
<task-notification>
<task-id>ae59c391998735683</task-id>
<tool-use-id>toolu_01GBRt3ZeoRPHVXVNZBK2yxV</tool-use-id>
<output-file>C:\Users\maxre\AppData\Local\Temp\claude\C--claude-base--claude-worktrees-priceless-snyder-07082c\4f3f6a59-a6ed-4958-81fa-7874a46b36c1\tasks\ae59c391998735683.output</output-file>
<status>completed</status>
<summary>Agent "Research Nadali audio+video method" finished</summary>
<note>A task-notification fires each time this agent stops with no live background children of its own. The user can send it another message and resume it, so the same task-id may notify more than once.</note>
<result>Perfect. Now I have all the information I need. Let me compile my findings:

Based on my thorough exploration of the MoMA codebase and nadali project files, here is what produced the nadali project:

## Speech Audio (Anna's Narration)

Fish Audio produced Anna's narration via the s2-pro TTS model. The script is **sass_recipe_anna_uei.py** at C:\moma\sc10\sound_assembly\code\sass_recipe_anna_uei.py. The recipe invokes Fish via HTTP POST to https://api.fish.audio/v1/tts with parameters including: voice reference ID da5554ea7be8458f9560e0a2d90553e3 (Anna clone #22), temperature 0.85, top_p 0.80, and a prepended tone tag "[warm, calm, curious]". Output format is WAV at 44.1kHz. The recipe is NOT integrated into MoMA's standard job queueâ€”it runs standalone, chunking Anna's libretto into &lt;=15-second clips to fit the video avatar maker's hard limit. The canonical versioned runs are stored at C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\sound\nadali_production\lines_YYYYMMDD\ (most recent is lines_20260718). Fish Audio cost was not explicitly logged per clip but the service enforces HTTP 402 when balance runs out.

## Video/Lipsync

Alibaba DashScope's **wan2.6-i2v-flash** model produced the video lip-sync. The worker is **combo_wan26au_worker.py** at C:\moma\sc10\combo_runner\code\combo_wan26au_worker.py, invoked via the standard MoMA job queue with job_type='lipsie' and lipsync_tool='wan26flau'. The worker submits to DashScope's async endpoint at POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis with model wan2.6-i2v-flash, 720P resolution, and audio duration between 3 and 15 seconds. Cost is documented at line 23 as approximately $0.25 per 5-second clip at the flash tier.

## Duration Limits and Chunking

The API's hard ceiling is **15 seconds maximum clip duration** (DURATION_MAX = 15 in combo_wan26au_worker.py line 55). The minimum is 3 seconds. The worker pads short audio clips with configurable silence buffers (default 0.5 seconds on each side) via FFmpeg to meet the minimum, then caps total duration to 15 seconds. No explicit 15-second chunking logic exists in nadali itselfâ€”the clips were pre-split by sass_recipe_anna_uei.py using sentence-aware logic that targets ~12 seconds per clip (TARGET_S = 12.0) to stay well under the 15-second limit. Anna's manifest shows one clip exceeded 15 seconds (anna_003_intro_c.wav at 15.0s, flagged "OVER15" in the manifest), indicating the recipe's safety margin occasionally fails on edge cases.

## Output Files

Nadali's Anna narration audio resides at C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\sound\nadali_production\ with two timestamped line-cut runs: lines_20260715 and lines_20260718 (the latter reflecting updated text from D42b). Each contains 28+ wav files per manifest.json, plus per-line metadata. The lipsync video reels (animated stills with synced video) are output by combo_wan26au_worker to C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\combo_runner\data\output_lipsies\ as files like nadali_lipsie_v{job_id}_wan26flau.mp4, with job metadata (duration, audio file, prompt, silence buffer) stored in the jobs database.

SURE of: TTS provider (Fish Audio), model (s2-pro), video API (DashScope wan2.6-i2v-flash), worker name (combo_wan26au_worker), 15-second limit, $0.25 per clip cost, output directories, manifest structure.

INFERRING: exact per-clip Fish Audio cost (not explicitly recorded; HTTP 402 on zero balance is the only brake).</result>
<usage><subagent_tokens>70196</subagent_tokens><tool_uses>33</tool_uses><duration_ms>77179</duration_ms></usage>
</task-notification>

## [2026-07-26 14:10:37] turn 4
So, we just randomly alternate the images. They're all interchangeable. It's just different angles. Just to chop things. Yeah, yeah. We renamed tapes to lessons. Training tapes to telepathy lessons.

## [2026-07-26 14:16:28] turn 5
<task-notification>
<task-id>a58ece7e13ef1f18c</task-id>
<tool-use-id>toolu_01LFXjQGqwvokpaUxznk56EF</tool-use-id>
<output-file>C:\Users\maxre\AppData\Local\Temp\claude\C--claude-base--claude-worktrees-priceless-snyder-07082c\4f3f6a59-a6ed-4958-81fa-7874a46b36c1\tasks\a58ece7e13ef1f18c.output</output-file>
<status>completed</status>
<summary>Agent "Find MoMA lipsync cost logs" finished</summary>
<note>A task-notification fires each time this agent stops with no live background children of its own. The user can send it another message and resume it, so the same task-id may notify more than once.</note>
<result>Excellent! Now I have comprehensive real data. Let me compile the final findings:

## Summary

I've found where actual DashScope Wan 2.6 lipsync (lipsie) job costs are recorded. Here are the REAL NUMBERS:

### Cost Recording Location
**Database:** Cloudflare D1 (cloud database)
**Table:** `api_expenses`
**Query file:** `C:\moma\sc10\combo_runner\code\expense_log.py` (lines 136-161) - records costs to D1
**Worker code:** `C:\moma\sc10\combo_runner\code\combo_wan26au_worker.py` (lines 465-470) - calls expense_log.record()
**Log file:** `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\scenes\scene10_images\combo_runner\data\wan26au_worker.log`

### Actual Billing Data (from D1 database)
- **Total lipsie jobs billed:** 255 jobs
- **Total dollars spent:** $63.15 USD
- **Dollars per second:** $0.025 per second (consistent rate for wan2.6-i2v-flash "flash tier")
- **Average cost per job:** $0.2476

### Job Duration Breakdown (255 completed jobs)
| Duration | Job Count | Total Cost | Cost per Second |
|----------|-----------|-----------|-----------------|
| 3s | 28 | $2.10 | $0.70/s |
| 4s | 13 | $1.30 | $0.33/s |
| 5s | 16 | $2.00 | $0.40/s |
| 6s | 10 | $1.50 | $0.25/s |
| 7s | 15 | $2.62 | $0.38/s |
| 8s | 17 | $3.40 | $0.43/s |
| 9s | 5 | $1.12 | $0.13/s |
| 10s | 15 | $3.75 | $0.38/s |
| 11s | 11 | $3.02 | $0.28/s |
| 12s | 19 | $5.70 | $0.48/s |
| 13s | 19 | $6.18 | $0.48/s |
| 14s | 17 | $5.95 | $0.43/s |
| **15s** | **63** | **$23.62** | **$1.58/s** |

### Key Findings
1. **282 output files exist** in `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\scenes\scene10_images\combo_runner\data\output_lipsies` (named `*wan26flau*.mp4`)
2. **248 successful jobs logged** in the worker log file
3. **255 expense records** in D1 (some may be from retries or different runs)
4. **Cost estimation was accurate:** The code comment stating "~$0.25 per 5s 720P clip" (line 23 of combo_wan26au_worker.py) is confirmed by actual data showing $0.025/sec rate

### Database Query Path
The costs are accessible via D1 API at: `https://moma-db-api.max-rempel2.workers.dev` using auth from `C:\Users\maxre\Nextcloud\zSyncMain\ssh\moma_d1_auth_20260409.txt`</result>
<usage><subagent_tokens>85308</subagent_tokens><tool_uses>48</tool_uses><duration_ms>125755</duration_ms></usage>
</task-notification>

## [2026-07-26 14:18:28] turn 6
You know what? Let's start... I like the beginning. Let's spend maybe $4 for now and do the first piece. And then, by that time, I think we'll fix the TIGETA video maker and then we'll switch to that. I think that would be terrific. Proceed with the first, say, first several lines or whatever. Shouts, phrases. How do you call that? Arrangements, scenes. There is a word for that. Steals? No. Spots. Yeah, proceed with the spots. Properly do that through MoMA. There should be like a full MoMA workflow. Where everything is going through MoMA and deviations and shortcuts are not permitted. Okay. Let's go. Okay. Okay. Okay. Okay. Okay.

## [2026-07-26 14:20:27] turn 7
When they are ready, present them to me.

## [2026-07-26 14:22:02] turn 8
By the way, when you can, when it is rational to offload to cheaper models, please do that. So far I don't think it was smart to do the cheaper models, but if there is a production where a cheap model can do a part of the job, do that. Let's learn the art of saving the tokens, because otherwise we run out of tokens too fast per week. Weekly limits are too strict.

## [2026-07-26 14:22:24] turn 9
Yeah, we are... It looks like we will use up the weak resources in four days, so we need to offload a lot to the cheaper models.

## [2026-07-26 14:22:45] turn 10
So, what's the next step? Will you just vocalize when you need me?

## [2026-07-26 14:24:10] turn 11
<task-notification>
<task-id>a6baf34de9506bd1c</task-id>
<tool-use-id>toolu_01LP4wMgpkLvR61oKZH7hJ3S</tool-use-id>
<output-file>C:\Users\maxre\AppData\Local\Temp\claude\C--claude-base--claude-worktrees-priceless-snyder-07082c\4f3f6a59-a6ed-4958-81fa-7874a46b36c1\tasks\a6baf34de9506bd1c.output</output-file>
<status>completed</status>
<summary>Agent "Get exact MoMA Nadali audio+lipsie recipe" finished</summary>
<note>A task-notification fires each time this agent stops with no live background children of its own. The user can send it another message and resume it, so the same task-id may notify more than once.</note>
<result>## Summary

The Nadali chain is 4 scripts + 1 background worker. Everything is real and in `C:\moma` (main repo, not a worktree). Interpreter used by MoMA everywhere is `C:\Users\maxre\AppData\Local\Python\pythoncore-3.14-64\python.exe` (`pythonw.exe` for detached workers).

---

## 1. AUDIO â€” Fish Audio TTS

**Script:** `C:\moma\sc10\sound_assembly\code\sass_recipe_anna_uei.py`

**Command (no args at all â€” everything is hardcoded constants at the top of the file):**
```
cd C:\moma\sc10\sound_assembly\code
C:\Users\maxre\AppData\Local\Python\pythoncore-3.14-64\python.exe sass_recipe_anna_uei.py
```

**Input:** NOT a text file list, NOT a scene id. It is a **libretto markdown file** â€” `LIBRETTO` constant, line 47:
`C:\Users\maxre\Videos\max talks\uei_max_talk_20260711\anna_commentary_v09.md`
Format = blocks delimited by `==========` bars, with a title line `INTRO` / `INTERMISSION N` / `CONCLUSION`, then spoken text. `[square bracket]` tags are read by Fish as delivery direction, not spoken. The script chunks each block to â‰¤15 s (TARGET_S=12.0, HARD_S=15.0, CPS=17.0). To point it at a new script you **edit `LIBRETTO`** â€” there is no CLI flag.

**Voice/params:** `config/voices.json` â†’ `ANNA` = reference_id `da5554ea7be8458f9560e0a2d90553e3` (clone #22); model `s2-pro`; `temperature=0.85`, `top_p=0.80`, tone prefix `"[warm, calm, curious] "`, `format=wav`, `sample_rate=44100`. Key file: `C:\Users\maxre\Nextcloud\zSyncMain\ssh\fishaudio_api_key_20260226.txt`.

**Where it writes (two places):**
1. Canonical versioned run: `C:\Users\maxre\OneDrive\Music\rehearsals\anna_uei\&lt;run_tag&gt;\` where run_tag = `anna_uei_v09_20260716_144741` style. Contains `anna_NNN_&lt;tag&gt;_&lt;letter&gt;.wav`, `manifest.json`, `manifest.tsv`, `SOURCE.txt`.
2. Flat mirror (wiped + recopied each run): `C:\Users\maxre\Videos\max talks\uei_max_talk_20260711\anna_audio\`

Real prior runs on disk: `anna_uei_v08_20260716_121404`, `anna_uei_v09_20260716_131219`, `anna_uei_v09_20260716_144741` (34 wavs). `SOURCE.txt` of the last one confirms libretto v09, ANNA #22, s2-pro, temp 0.85 / top_p 0.8.

**Then, hand-off into MoMA (2 steps):**
- The wavs + `manifest.json` are copied flat into `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\sound\nadali_production\` (this is `paths.SOUND_WORK_DIR` + `nadali_production`, via `paths.scene_production_dir("nadali")`).
- Then: `C:\moma\sc10\combo_runner\code\build_nadali_audio_run.py` (no args) reads `nadali_production\manifest.json` and lays out a sass-format per-line run:
  `...\sound\nadali_production\lines_20260715\` (RUN_DIR constant â€” for the 7/18 rebuild this constant was edited to `lines_20260718`).
  It writes `manifest.json` with `line_hash = sha256("nadali|ANNA|{order}|{normalized_text}")[:14]`, plus `file`, `duration` (ffprobe), `char="ANNA"`, `text`, `order`, `tag`.

Live on disk now: `lines_20260715\` (28 lines) and `lines_20260718\` (34 lines + manifest.json, mtime 2026-07-18 00:11).

---

## 2. LIPSIE JOBS

**Entry point:** `fire_job` in `C:\moma\sc10\combo_runner\code\moma_db.py` line 674. It is a **Python function, not a CLI**:

```python
fire_job(conn, *, job_type, scene_id, source_image, **fields) -&gt; int   # new job id
```
`conn` comes from `with connect_db() as conn:`. `job_type` must be in `{'image','clip','lipsie'}`. Any kwarg outside the `_FIRE_JOB_COLS` whitelist (line 565) raises. Legal columns include: `scene_id, source_image, input_prompt, input_ref, input_status, input_file, output_prompt, output_status, output_file, attempts, rating, comment, output_comment, plate_recipe, label, vocal_line, engine, engine_params, line_hash, birth_line_hash, source_job_id, frame_speakers, audio_start, audio_end, lipsy_mask_side, lipsy_mask_x1, lipsy_mask_x2, clip_maker, prompt_id, arrangement_id, batch_id, hide_tile, job_type, lipsync_tool, created_at, updated_at`.

**The Nadali firing script:** `C:\moma\sc10\combo_runner\code\fire_nadali_reels.py`
```
cd C:\moma\sc10\combo_runner\code
C:\Users\maxre\AppData\Local\Python\pythoncore-3.14-64\python.exe fire_nadali_reels.py
```
No args â€” you edit the `REELS` list (`(manifest_order, still_filename)` tuples), `RUN_MANIFEST`, and `PROMPT` in the file.

**Exact field values for a wan26flau lipsie (from fire_nadali_reels.py, lines 81-87):**

| field | value |
|---|---|
| `job_type` | `'lipsie'` |
| `lipsync_tool` | `'wan26flau'` |
| `scene_id` | `'nadali'` (the scene TAG string, not the numeric id) |
| still-image field | **BOTH** `source_image=&lt;abs path to .png&gt;` and `input_file=&lt;same abs path&gt;` |
| audio field | **NOT a path.** `birth_line_hash=&lt;line_hash from lines_TS/manifest.json&gt;` â€” the worker resolves the wav via `audio_resolver.resolve_per_line_audio()`. `vocal_line='ANNA: &lt;text&gt;'` is the fallback matcher. |
| `output_status` | `'queued'` |
| `output_prompt` | the motion prompt string |
| `arrangement_id` | `40` (for `nadali-anna-presenter-20260715`) |
| `label` | `f"nadali_reel_{tag}_ord{order}"` |
| `hide_tile` | `0` |
| `engine` | **do not pass it.** `fire_job` auto-forces `engine = lipsync_tool` for lipsies (guardrail at moma_db.py:730) because the DB default `'wan22'` lets `combo_worker` steal the job and render a silent clip. This bit Nadali twice. |

Note: pass `birth_line_hash`, **not** `line_hash`. The merge-hash guard (moma_db.py:739) fires only on `line_hash` and would reject a nadali hash (no `script_lines` row).

**REAL fired job â€” id 3336 (from D1 backup `C:\moma\sc10\d1_backups\current\d1_20260726_141203.json`, table `jobs`):**
```
id                3336
job_type          lipsie
scene_id          nadali
lipsync_tool      wan26flau
engine            wan26flau
arrangement_id    40
label             nadali_reel_conclusion_ord33
birth_line_hash   9f1455a268dd27
source_image      C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\nadali\output\anna_meetingroom_presenter_v3.png
input_file        (same as source_image)
input_status      pending
output_status     done
vocal_line        ANNA: You are carrying this forward for people who cannot yet do it themselves...
output_file       nadali_lipsie_v3336_wan26flau.mp4
request_id        6131acf7-7a52-4023-b02e-f51b880947ee
created_at        2026-07-18 07:13:24   updated_at 2026-07-18 07:33:00
lipsync_params    {"model":"wan2.6-i2v-flash","mode":"image+audio","resolution":"720P",
                   "duration":13,"audio_duration":11.006,"audio_run":"lines_20260718",
                   "audio_file":"anna_033_conclusion_f.wav","silence_buffer":0.5, ...}
```
(`lipsync_params` is written BY the worker, not by the fire. Only exception: you may pre-set `{"silence_buffer": N}` before the worker claims the row.)

Nadali job id ranges: **3299-3327** (batches 1-4, 24 unchanged lines) and **3328-3337** (batch 5, the 10 D42b-changed lines). 39 lipsie jobs, 48 nadali jobs total.

---

## 3. WORKER

**Script:** `C:\moma\sc10\combo_runner\code\combo_wan26au_worker.py`
Model `wan2.6-i2v-flash`, 720P, DashScope. Claims: `job_type='lipsie' AND lipsync_tool='wan26flau' AND output_status='queued'`. ~$0.25 per 5 s clip.

**How it is started** â€” never by hand; by `C:\moma\sc10\moma_restart.py` (line 437), launched via `C:\moma\sc10\start_moma.bat`. The literal spawn is:
```
cwd = C:\moma\sc10\combo_runner\code
C:\Users\maxre\AppData\Local\Python\pythoncore-3.14-64\pythonw.exe combo_wan26au_worker.py
```
detached (`CREATE_NO_WINDOW|DETACHED_PROCESS`), stderr â†’ `&lt;DATA_DIR&gt;\crashlogs\combo_wan26au_worker.stderr.log`.
Normal operator action: run `C:\moma\sc10\start_moma.bat` (restarts the whole MoMA stack) â€” or just start the one worker with the command above if the rest is already up.

**Confirm it is running â€” singleton pid file:**
```
C:\moma\sc10\combo_runner\local_state\wan26au_worker_pid.txt
```
(deliberately OFF Nextcloud). Right now it contains `35900`, and `combo_wan26au_worker.py` is indeed live as pid 35900. If a second instance starts it logs `=== wan26au worker ABORT: already running (pid=NNN) ===` and exits.

**Logs / outputs:**
- Log: `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\scenes\scene10_images\combo_runner\data\wan26au_worker.log` (real lines: `LIPSIE wan26flau: job 3336 scene=nadali char/line='ANNA: ...'` â†’ `SAVED: nadali_lipsie_v3336_wan26flau.mp4 (6725KB)`)
- State: `...\combo_runner\data\wan26au_worker_state.json`
- Rendered MP4s: `...\scene10_images\combo_runner\data\output_lipsies\{scene_id}_lipsie_v{job_id}_wan26flau.mp4`
- API key: `C:\Users\maxre\Nextcloud\zSyncMain\ssh\dashscope_beijing_api_key_20260329.txt`

---

## 4. SCENE ROWS / "Tape 1Select"

Yes â€” there is a real `scenes` table in Cloudflare D1 (the sqlite file `combo_db.sqlite` is a STALE snapshot; never touch it â€” go through `moma_db.connect_db()` / `D1Client`). Schema: `id, name, notes, rank, created_at`. Sibling table `arrangements(id, scene_id, name, location, notes, rank, created_at)`.

Key rows:
- `scenes.id=9, name='nadali'`, created 2026-07-15 â†’ `arrangements.id=40, name='nadali-anna-presenter-20260715'`
- `scenes.id=10, name='Tape 1'` (contaminated, abandoned)
- **`scenes.id=11, name='Tape 1Select'`**, created 2026-07-25 22:27:41 â†’ **`arrangements.id=42, name='Tape 1Select'`**

Critically: `jobs.scene_id` for these projects stores the **scene NAME string**, i.e. literally `'Tape 1Select'` (with the space), not `11`. Same pattern as `'nadali'`.

**Jobs 3381-3402 = exactly the 22 Tape 1Select rows** (all `job_type='image'`, `arrangement_id=42`). Of those, **15 are `output_status='approved'`**: 3381, 3382, 3383, 3384, 3385, 3386, 3387, 3388, 3393, 3396, 3397, 3398, 3399, 3400, 3402. (The 7 junked: 3389, 3390, 3391, 3392, 3394, 3395, 3401.) Note 3381 and 3388 both point at the same `kitchen_night_v3.png`, so it is 14 distinct PNGs.

**Where the files physically live** â€” `output_file` is KAZARIAN_ROOT-relative:
- `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\telepathy_tapes\tape1select_output\` â†’ `zoom_in.png, zoom_out.png, cam_left.png, cam_right.png, cam_up.png, cam_down.png, table_low.png, table_profile_r.png, v2_front.png, v2_left.png, v2_right.png, v2_high.png, v2_profile_l.png` (+ the junked ones)
- plus `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\telepathy_tapes\tape1_output\kitchen_night_v3.png` (jobs 3381 &amp; 3388)

The scripts that created that scene: `C:\moma\sc10\combo_runner\code\fire_tape1select_variations.py` (creates scene+arrangement, moves job 3381 in, fires 6 camera variations), `fire_tape1select_table.py`, `fire_tape1select_table_redo.py`. All use `SCENE_NAME = ARR_NAME = SCENE_TAG = "Tape 1Select"`, `SIZE="2048x1152"`, refs = Anna face + Anna body + s3381.

Nadali's own stills live in `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\nadali\output\` (9 presenter PNGs + `_ref_anna_room_strip.png`), registered by `fire_nadali_anna.py`.

---

## 5. Method docs

- **`C:\Users\maxre\Videos\max talks\uei_max_talk_20260711\NADALI_FINAL_PLAN.md`** â€” the closest thing to an end-to-end doc for this exact deliverable: locked title/subtitle/credit, cut list, pipeline order, "Reels: kazarian_episode/scenes/scene10_images/combo_runner/data/output_lipsies/nadali_lipsie_v{job}_wan26flau.mp4", job ranges 3299-3327 / 3328-3337, run `lines_20260718`, assembler `assemble_nadali_video_v04.py`, and the shipped-v08 log.
- `C:\Users\maxre\Videos\max talks\uei_max_talk_20260711\README.txt` â€” talk-cleaning + Anna-commentary overview.
- The three script docstrings are the authoritative per-stage docs: `sass_recipe_anna_uei.py` (lines 1-37), `build_nadali_audio_run.py` (1-7), `fire_nadali_reels.py` (1-8).
- `C:\moma\sc10\combo_runner\code\combo_wan26au_worker.py` header (lines 1-33) documents the queue claim, audio padding and output naming.
- `C:\moma\memos\audio_resolver_v03_report_20260527_tomemex.md` and `C:\moma\memos\moma_system_map_tomemex.md` cover the wan26flau lane generally.

There is **no single README covering TTSâ†’lipsie end-to-end**; NADALI_FINAL_PLAN.md plus the three docstrings is the real documentation.

---

## The runnable recipe, in order

```
:: 1. TTS (edit LIBRETTO constant first)
cd C:\moma\sc10\sound_assembly\code
C:\Users\maxre\AppData\Local\Python\pythoncore-3.14-64\python.exe sass_recipe_anna_uei.py

:: 2. copy the run's *.wav + manifest.json flat into
::    C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\sound\&lt;TAG&gt;_production\

:: 3. build the per-line run (edit SCENE_TAG / SRC_DIR / RUN_DIR first)
cd C:\moma\sc10\combo_runner\code
C:\Users\maxre\AppData\Local\Python\pythoncore-3.14-64\python.exe build_nadali_audio_run.py

:: 4. make sure the worker is alive
type C:\moma\sc10\combo_runner\local_state\wan26au_worker_pid.txt
::    (if dead) C:\moma\sc10\start_moma.bat

:: 5. fire the reels (edit REELS / RUN_MANIFEST / STILL_DIR / PROMPT first)
cd C:\moma\sc10\combo_runner\code
C:\Users\maxre\AppData\Local\Python\pythoncore-3.14-64\python.exe fire_nadali_reels.py

:: 6. watch
::    ...scene10_images\combo_runner\data\wan26au_worker.log
::    output -&gt; ...combo_runner\data\output_lipsies\&lt;scene&gt;_lipsie_v&lt;job&gt;_wan26flau.mp4
```

Two gotchas to carry forward: (a) never pass `engine=` on a lipsie fire â€” let the guardrail set it; (b) for a Tape 1Select run you would need a `&lt;tag&gt;_production` audio folder whose name matches `jobs.scene_id` exactly (`scene_production_dir` would look for `Tape 1Select_production` â€” a space in the folder name), so a cleaner tag is worth choosing before you fire.</result>
<usage><subagent_tokens>111164</subagent_tokens><tool_uses>50</tool_uses><duration_ms>300923</duration_ms></usage>
</task-notification>

## [2026-07-26 14:26:33] turn 12
<task-notification>
<task-id>aaabc7331af9e0334</task-id>
<tool-use-id>toolu_01QpQMBsjRaQCwxWC118cnxe</tool-use-id>
<output-file>C:\Users\maxre\AppData\Local\Temp\claude\C--claude-base--claude-worktrees-priceless-snyder-07082c\4f3f6a59-a6ed-4958-81fa-7874a46b36c1\tasks\aaabc7331af9e0334.output</output-file>
<status>completed</status>
<summary>Agent "Write Anna lesson TTS recipe script" finished</summary>
<note>A task-notification fires each time this agent stops with no live background children of its own. The user can send it another message and resume it, so the same task-id may notify more than once.</note>
<result>Dry-run worked cleanly, no Fish Audio calls made, all 10 spots under the 15-second ceiling.

**What I changed:** I created `sass_recipe_anna_lesson_v01.py` as an adaptation of the UEI recipe, for the Telepathy Lessons project (original file untouched). It keeps all the original machinery â€” MOMA voice/production config loading, the Fish Audio synth-with-retry logic, ffprobe duration checking, versioned run-tag output folders, and the flat mirror copy. The key difference: the UEI recipe re-chunks free-flowing prose into sub-15-second pieces automatically; this new recipe does not, because in the lesson libretto each "SPOT NN" block is already hand-authored as exactly one clip. So I replaced the INTRO/INTERMISSION/CONCLUSION title parser with one that matches "SPOT NN", removed all the sentence-splitting/merging code, and added a pre-flight step that estimates each spot's duration from character count and aborts loudly (no Fish calls) if anything would exceed 15 seconds. I also added a `--dry-run` flag that runs only that pre-flight check. Output goes to `REHEARSALS_DIR/anna_lesson1/&lt;run_tag&gt;/` with filenames like `anna_001_spot01.wav`, and mirrors to the new `lesson1_production` sound folder. Manifest entries include order, tag, file, text, duration, and char as required.</result>
<usage><subagent_tokens>135834</subagent_tokens><tool_uses>6</tool_uses><duration_ms>63576</duration_ms></usage>
</task-notification>

## [2026-07-26 14:33:07] turn 13
okay now produce the lip the reels produce the reels reels

## [2026-07-26 14:33:22] turn 14
I expect them to end up in MoMA right? So it will be assembled in MoMA as normal

## [2026-07-26 14:52:32] turn 15
<task-notification>
<task-id>bbkkbcxxk</task-id>
<tool-use-id>toolu_016zA7gmFVycezkUzSN4hged</tool-use-id>
<output-file>C:\Users\maxre\AppData\Local\Temp\claude\C--claude-base--claude-worktrees-priceless-snyder-07082c\4f3f6a59-a6ed-4958-81fa-7874a46b36c1\tasks\bbkkbcxxk.output</output-file>
<status>completed</status>
<summary>Background command "Wait for all 10 reels to render" completed (exit code 0)</summary>
</task-notification>

## [2026-07-26 15:59:18] turn 16
Yeah, I just renamed training tape to Telepathy Lesson 1. And I looked at the videos and they look pretty, the reels.

## [2026-07-26 15:59:51] turn 17
No, I think it's good. I want to listen to how it sounds, but I think it's good.

## [2026-07-26 21:00:59] turn 18
you slacked and didn't properly populate the moma. There is no spots, nothing to fill in the spine! I prohibited circumventing moma!!!

## [2026-07-26 21:04:50] turn 19
I need to assemble the transcript in the storyboard. Update the db to fit.

## [2026-07-26 21:08:46] turn 20
<task-notification>
<task-id>afd186904815cf47f</task-id>
<tool-use-id>toolu_01ShAtutzU2HpV2pBhN8dMXm</tool-use-id>
<output-file>C:\Users\maxre\AppData\Local\Temp\claude\C--claude-base--claude-worktrees-priceless-snyder-07082c\4f3f6a59-a6ed-4958-81fa-7874a46b36c1\tasks\afd186904815cf47f.output</output-file>
<status>completed</status>
<summary>Agent "Find storyboard spine assembly for named projects" finished</summary>
<note>A task-notification fires each time this agent stops with no live background children of its own. The user can send it another message and resume it, so the same task-id may notify more than once.</note>
<result>Now I have a comprehensive understanding. Let me compile a concise summary with specific SQL references:

## Summary Report

Based on my analysis of the MoMA codebase, here are the concrete answers:

### 1. **Which file/server renders the storyboard spine, and what query does it run?**

**File:** `/c/moma/sc10/sound_assembly/code/slideshow_server_v01.py` (port 8790)

**Primary spine assembly query** (line 1454-1458 in `_load_timings()` and `/api/script_lines` endpoint at line 1449-1466):
```sql
SELECT line_hash, idx, char, text FROM script_lines 
WHERE scene=? AND status='active' ORDER BY idx
```

**For reel membership mapping** (`/api/reel_membership_sc10` endpoint at line 699-799):
- Pulls lipsies: `SELECT id, line_hash, vocal_line, output_status FROM jobs WHERE job_type='lipsie' AND scene_id LIKE ?`
- Maps line_hash â†’ script_lines.idx (line 725-730)
- Resolves merges via `merge_ops` table (line 748-758)

### 2. **For a named-tag project (scene_id='nadali' or 'lesson1'), what rows make a "spot" appear on the spine?**

**Answer:** Combination of three tables:

1. **`script_lines`** â€” The spine authority (PRIMARY SOURCE). Contains:
   - `line_hash` (primary key, e.g. '3d7f2a...')
   - `scene` (integer rank, e.g. 11 for lesson1's scene)
   - `idx` (line order: 0, 1, 2, ...)
   - `char` ('ANNA')
   - `text` (spoken words)
   - `status` ('active')

2. **`jobs`** with `job_type IN ('lipsie', 'image')` matching:
   - `scene_id = 'lesson1'` (named tag, NOT 'sc11')
   - `birth_line_hash` or `line_hash` matching a script_lines row
   - `output_status NOT IN ('error','running','pending','junk')`

3. **`line_current_clip`** (spotlight/1st spine pick):
   - `line_hash` (links to script_lines)
   - `job_id` (points to the chosen job for that line)

**For named projects specifically** (lesson1, nadali):
- Scene is NOT a numeric sc-scene (sc10, sc11); instead `scene_id` is a string tag
- Audio resolves via `latest_scene_lines_dir(scene_num)` â†’ `lines_*/manifest.json` (line 587-612)
- No scene_rank exists; uses `scene_production_dir()` to find the audio folder

### 3. **How is the transcript/line text shown on the spine?**

**Source:** `script_lines.text` (fetched directly in line 1449-1466)

**Overlaid with audio from:** `lines_*/manifest.json` matched by **(char, normalized_text)** tuple (line 596-610):
```python
key = ((char or '').upper(), _norm_text(text))
a = audio_by_key.get(key)  # file, duration, text_with_tags
```

**No usage of `jobs.vocal_line`** for the spine display â€” vocal_line is metadata only.

### 4. **To add 24 narration spots (spots 11..34, character ANNA, each with spoken text) to lesson1 spine:**

**Exact insert sequence (all required columns are minimal set):**

#### Step 1: Insert into `script_lines` (if not already present):
```sql
INSERT INTO script_lines (line_hash, scene, idx, char, text, norm_text, status, created_at, updated_at)
VALUES (?, 11, ?, 'ANNA', ?, ?, 'active', datetime('now','localtime'), datetime('now','localtime'))
```
- `line_hash`: compute as `hashlib.sha256(f"lesson1|ANNA|{idx}|{norm_text}".encode()).hexdigest()[:14]` (see build_lesson1_audio_run_v01.py:22-24)
- `scene`: 11 (lesson1's scene rank)
- `idx`: 10, 11, 12, ... 33 (for spots 11..34; 0-indexed)
- `char`: 'ANNA'
- `text`: the full spoken line with tone tags if any (e.g., "[warm] Welcome...")
- `norm_text`: alphanumeric-only lowercase (see slideshow_server line 120-123)

#### Step 2: Fire lipsie jobs (via moma_db.fire_job() â€” see fire_lesson1_reels_v01.py:103-115):
```python
fire_job(conn, 
    job_type='lipsie', 
    scene_id='lesson1',
    source_image=still_path,
    input_file=still_path,
    birth_line_hash=line_hash,  # NOT line_hash parameter (D44 guard)
    vocal_line='ANNA: &lt;text&gt;',
    output_prompt='...',
    lipsync_tool='wan26flau',
    arrangement_id=42,  # lesson1 arrangement
    label='lesson1_reel_spot11',
    output_status='queued')
```

#### Step 3: (If multi-arrangement scene) File into `line_arrangement`:
```sql
INSERT OR REPLACE INTO line_arrangement (line_hash, arrangement_id)
VALUES (?, 42)
```

#### Step 4: Audio resolution:
- Place MP3 files in `scene_production_dir(11)/lines_YYYYMMDD/` with `manifest.json`:
```json
[
  {"order": 11, "line_hash": "...", "char": "ANNA", "text": "...", "file": "spot_11.mp3", "duration": 2.5, "tag": "..."},
  ...
]
```

**Tables touched:**
- `script_lines` â€” spine rows (idx 10..33)
- `jobs` â€” lipsie image/audio pairs (scene_id='lesson1', birth_line_hash per line)
- `line_arrangement` â€” (line_hash, arrangement_id=42) for multi-arr scoping
- Filesystem: `sound_assembly/data/scene11_production/lines_YYYYMMDD/manifest.json` + MP3 files

**File references:**
- firepoint: `/c/moma/sc10/combo_runner/code/fire_lesson1_reels_v01.py:103-115`
- audio builder: `/c/moma/sc10/combo_runner/code/build_lesson1_audio_run_v01.py:36-57`
- DB queries: `/c/moma/sc10/sound_assembly/code/slideshow_server_v01.py:1449-1466, 1576-1666`</result>
<usage><subagent_tokens>93326</subagent_tokens><tool_uses>24</tool_uses><duration_ms>78643</duration_ms></usage>
</task-notification>

## [2026-07-26 21:21:00] turn 21
TLDR, I don't know. I want to see what was already produced, assembled. And did you update it so I can look at it?

## [2026-07-26 21:23:21] turn 22
No, no, no, I'm not asking to assemble, I'm asking to fix the storyboard. The storyboard is broken.

## [2026-07-26 21:24:28] turn 23
There is another session that's trying to fix the storyboard, so I don't know how you guys cooperate. I guess I will give you a new number. I will name it G. No, G is taken. K. I think K is available. So you will be K1.

## [2026-07-26 21:25:50] turn 24
<task-notification>
<summary>Stop hook feedback</summary>
</task-notification>
<system-reminder>
Stop hook blocking error from command "UserPromptSubmit": Direct message from K2: K2 here (storyboard/8790 owner). Diagnosed: my scene-picker root fix (named scen

</system-reminder>

## [2026-07-26 21:28:23] turn 25
Did you see the questions from K2? Do I need to push every time? Why can't you guys talk directly? Why do I need to help?

## [2026-07-26 21:31:00] turn 26
<task-notification>
<summary>Stop hook feedback</summary>
</task-notification>
<system-reminder>
Stop hook blocking error from command "UserPromptSubmit": Direct message from K2: Built + pushed (814960f). Storyboard now renders named projects server-side: _na

</system-reminder>
