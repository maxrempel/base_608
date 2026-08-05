# Scribe handover - milestone 2 (~151K tokens)
# session: 20260726_priceless_snyder_07082c_4f3f6a59
# cwd: C:\claude_base\.claude\worktrees\priceless-snyder-07082c
# written: 2026-07-26 14:11:09 by deepseek-v4-pro

# HANDOVER - Telepathy Training Tape 1 Audio + Video

## GOAL (Max's words)

"Develop the script in Notion divided by 15-second pieces and produce an audio. The source is in Notion, it's called Training Tape 1 or Training Lesson 1. Right now it's called Training Tape, but it should be renamed to Lesson."

After Claude discovered Taygeta has local lipsync but it's unproven at scale, Max redirected: "Let's now focus on the traditional method. We just recently produced audio for another piece... Anna was introducing my presentation... Everything worked and we did it through API with Alibaba. Let's focus on that."

So: produce the full audio+video for Telepathy Training **Lesson** 1 using the proven Alibaba DashScope pipeline - same as the Nadali/UEI talk.

## DECISIONS + WHY

**Lipsync method: Alibaba DashScope (wan2.6-i2v-flash), NOT Taygeta.**
Max explicitly chose the proven pipeline. Taygeta S2V works on paper (14B model installed, one 3-second test clip ever produced) but has no MoMA integration, no timing data at full resolution, and would need a new worker built. Alibaba worked end-to-end for Nadali. Decision is final for this project.

**15-second split target.**
The Alibaba API hard-caps at 15 seconds (DURATION_MAX = 15 in combo_wan26au_worker.py line 55). Minimum is 3 seconds. The Nadali recipe targeted 12 seconds per clip to stay safely under. This limit is not ours - it's DashScope's.

**Proposed approach: pilot first, then full render.**
Claude recommended (not yet approved by Max): do script split + Fish Audio first (cheap), then render 5 test beats through Alibaba (~$7) for approval before committing to the full ~$45-$135 pass. This protects budget since first passes are never final.

## CURRENT STATE

### What is DONE:
- Taygeta investigation complete: lipsync stack exists but is not the path forward
- Nadali pipeline research complete: full method documented
- Notion script located: three approved parts ("APPROVED - Telepathy Training Tape - Minutes 0 to 5", "Minutes 5 to 10", "Final Five Minutes") under the "Telepathy Training Tape Outline" page
- Script is ~2,800 words, already in short breath-length lines, meditative pace
- 15 approved Anna frames exist in D1 scene "Tape 1Select" (jobs 3381-3402) at 2048x1152 - but these are for the OLD workflow; whether they're reused for Alibaba lipsync is TBD
- Plan proposed in 5 steps (see below), awaiting Max's go-ahead

### What is NOT done:
- Notion pages NOT renamed from "Tape" to "Lesson" (Max asked; Claude held off pending stability)
- No script pulled from Notion yet
- No 15-second split produced
- No audio generated
- No Alibaba jobs fired
- No MoMA integration work done

### The proposed 5-step plan:
1. Pull all three script parts from Notion into one clean line file
2. Split into ~12-second beats (~75 beats for 15 minutes), honor sentence boundaries, never exceed 15 seconds; produce a readable list for Max to approve
3. Run Fish Audio (Anna clone #22, s2-pro, tone tag "[warm, calm, curious]") over every beat; measure durations, flag any over 15 seconds
4. Assign images to beats (15 frames for ~75 beats = ~5 beats per frame, grouped by topic - needs Max's eye)
5. Fire lipsie jobs through MoMA using combo_wan26au_worker.py (job_type='lipsie', lipsync_tool='wan26flau'), batch small, review

### Money estimate:
- Alibaba: ~$0.25 per 5 seconds ? ~$45 per full pass (900 seconds)
- Fish Audio: per-clip cost, not explicitly logged; HTTP 402 on zero balance is the only brake
- Realistic: 2-3 passes ? $100-$135 total

## EXACT NEXT STEP

**Max needs to answer two questions Claude asked at the end of the session:**
1. Pilot-first approach (5 beats / ~$7) - yes or no?
2. Rename Notion pages from "Tape" to "Lesson" - now or after the script work settles?

Once Max answers, Claude should immediately:
- If rename now: update the 3 approved pages + the outline page + the Tape 2 page via Notion API
- Pull all three script parts into a single file
- Begin the 12-second beat split

## OPEN QUESTIONS (awaiting Max)

1. Pilot-first or full send?
2. Rename now or later?
3. Do the 15 existing Anna frames get reused for the Alibaba videos, or does Alibaba generate its own starting frame? (In Nadali, the worker takes a still image + audio and generates the lipsynced video from that still - so the existing frames likely ARE the inputs. But the aspect ratio / resolution may differ from what Alibaba expects at 720P.)

## KEY PATHS AND IDs

### Script (Notion):
- Notion page: "Telepathy Training Tape Outline" (found via Notion search)
- Three sub-pages: "APPROVED - Telepathy Training Tape - Minutes 0 to 5", "Minutes 5 to 10", "Final Five Minutes"
- Also: a Tape 2 page started, and a registry/ideas page

### Audio pipeline (Fish ? Alibaba):
- Recipe script: `C:\moma\sc10\sound_assembly\code\sass_recipe_anna_uei.py`
- Fish API: POST https://api.fish.audio/v1/tts, model s2-pro
- Anna voice clone ID: `da5554ea7be8458f9560e0a2d90553e3` (clone #22)
- Tone tag prepended: "[warm, calm, curious]"
- Output: WAV 44.1kHz, chunked to ?15 seconds per `sass_prep` / `sass` pipeline
- Nadali reference output: `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\sound\nadali_production\lines_20260718\`

### Video pipeline (Alibaba DashScope):
- MoMA worker: `C:\moma\sc10\combo_runner\code\combo_wan26au_worker.py`
- Model: wan2.6-i2v-flash
- Endpoint: POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis
- Resolution: 720P
- Job type in MoMA: `lipsie` with `lipsync_tool='wan26flau'`
- Output directory: `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\combo_runner\data\output_lipsies\`
- Durations: min 3s, max 15s, worker pads short clips with 0.5s silence each side

### Existing visuals (may or may not be reused):
- D1 scene "Tape 1Select" - 15 Anna frames at 2048x1152
- Image files: `...\ai_images\kazarian_episode\telepathy_tapes\tape1select_output\`
- MOMA jobs 3381-3402

### Taygeta (the path NOT taken, but documented):
- Box: 192.168.1.142, user maxre, key ~/.ssh/sol_key
- ComfyUI at ~/ComfyUI/, port 8188, usually not running
- Wan 2.2 S2V 14B model at ~/ComfyUI/models/diffusion_models/wan2.2_s2v_14B_fp8_scaled.safetensors
- Fire script: ~/setup/scripts/s2v_fire.py
- S2V method doc: `C:\claude_base\tools\taygeta_s2v\s2v_video_method_v01_tomemex.md`
- MoMA local worker blueprint exists but not built

## GOTCHAS

1. **The 15-second limit is hard, from Alibaba.** Clip 16 seconds = rejected. The Nadali recipe targets 12 seconds for safety, and still had one clip hit exactly 15.0 flagged "OVER15." The split must be conservative.

2. **Fish Audio has no budget guard.** HTTP 402 is the only brake. No per-clip cost tally exists. Small per clip, but ~75 clips adds up.

3. **The existing 15 Anna frames were made for a different workflow** (slideshow, not lipsync video). Alibaba takes a still image as the starting frame and animates the mouth from the audio. So the frames are likely reusable as inputs - but 720P may require resizing from 2048x1152. This needs checking.

4. **Tape 1 = Lesson 1 rename touches multiple pages.** Max wanted this but it was deferred. If done mid-work, Notion links may shift. Better to do it before or after, not during.

5. **MoMA drives the Alibaba jobs.** Per Max's standing rule, everything goes through MoMA. The worker already exists and is proven. No new integration needed - just queue the jobs with the right tags.

6. **Taygeta was ruled out for NOW, not forever.** The box can do lipsync locally for free. The MoMA local worker just isn't built yet. If pilot costs run high, Max may want to revisit. Keep the Taygeta docs path handy.
