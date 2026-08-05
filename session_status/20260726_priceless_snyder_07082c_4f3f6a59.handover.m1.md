# Scribe handover - milestone 1 (~135K tokens)
# session: 20260726_priceless_snyder_07082c_4f3f6a59
# cwd: C:\claude_base\.claude\worktrees\priceless-snyder-07082c
# written: 2026-07-26 14:04:01 by deepseek-v4-pro

# HANDOVER - Telepathy Training Tape 1: Audio & Video (Taygeta Lipsync)

---

## GOAL (Max's own words)

"Develop the script in Notion divided by 15-second pieces and produce an audio." The source is a Notion page currently called **"Training Tape"** - Max wants it renamed to **"Training Lesson 1"** or **"Telepathy Training Tape 1"**. Before splitting, Max redirected: first **research Taygeta's setup for video** to see if the old API-style limits still apply. Specifically: can we do video? Do we have lipsync? Max investigates in parallel.

The handover from the prior session (MOMA, objective-feynman) adds crucial context: the **visuals are already done** - 15 approved Anna night-kitchen-table frames in the D1 scene "Tape 1Select" (MOMA jobs 3381-3402, fired at 2048x1152 true 16:9). Output files live at `...\ai_images\kazarian_episode\telepathy_tapes\tape1select_output\`. No slideshow assembled yet, no audio yet. The audio needs to be **Anna's voice clone via Fish TTS**, force-aligned through the sound assembler (`sass_prep` then `sass` in `sc10/sound_assembly/code/`). Every sass run burns Fish Audio balance - no budget guard exists.

---

## DECISIONS + WHY

1. **Wan 2.2 S2V (speech-to-video lipsync) IS installed and real on Taygeta.** Full stack confirmed: 14B S2V model, wav2vec2 audio encoder, umt5 text encoder, Wan VAE. A fire script (`~/setup/scripts/s2v_fire.py`) queues jobs to the ComfyUI API. This is not planned/aspirational - it exists on the box.

2. **Only one test clip has ever been produced:** July 16, 480?480, 16fps, 49 frames = 3.06 seconds. Nothing longer or higher-res has ever been run. ComfyUI is NOT currently running on Taygeta (only the dictation server is up).

3. **The 15-second split is still the right approach**, but for a different reason than before. Originally it was an API hard cap. Now: clip length is just a workflow parameter - no hard limit exists. BUT 15 seconds remains the natural unit: one image + one audio chunk per render, small enough to finish and re-do when wrong. Wan does longer clips via chunking/stitching, which is more machinery than we've built.

4. **Real limits are unknown:** 16GB VRAM and render time. No measurements exist for actual frame sizes (source is 2048?1152, so render size would likely be 832?480 or similar). Without timing data we can't plan.

---

## CURRENT STATE

**Done:**
- Full investigation of Taygeta's S2V/lipsync capability - confirmed present, functional, but untested at scale.
- Taygeta box spec confirmed: Ubuntu 24.04, NVIDIA RTX A4000 (16GB VRAM), dictation server running, ComfyUI NOT running.
- Key paths inventoried on Taygeta (see below).
- Hard API limits confirmed absent - clip length is a workflow number.

**Not done:**
- The Notion script has NOT been fetched or split into 15-second pieces.
- No audio produced.
- No timing test run on Taygeta to measure seconds-of-video per minute-of-GPU.
- ComfyUI is not started.
- "Training Tape" has not been renamed to "Training Lesson 1."

**In flight:** Nothing active. Max is investigating in parallel (presumably on the Notion side).

---

## EXACT NEXT STEP

Claude proposed two options at session end - Max hasn't chosen yet:

- **Option A:** Start ComfyUI on Taygeta, fire a real render at actual frame size, time it. This gives us the seconds-of-video-per-minute-of-GPU number we need to plan anything downstream.
- **Option B:** Go get the Notion script and do the 15-second split now, deferring the timing test.

Max, which first?

---

## OPEN QUESTIONS (awaiting Max)

1. Does Max want the timing test first, or the script split first?
2. What is the exact Notion page name/URL for "Training Tape 1" / "Training Lesson 1"?
3. Confirm rename: "Training Tape" ? "Training Lesson 1" or "Telepathy Training Tape 1"?
4. Is the handover from objective-feynman accurate about the narration text location? (It said "ask Max where it lives - it's the Telepathy Tape 1 narration, not the Kazarian movie script.")
5. The handover noted one junked angle: v2_room (job 3401) - unpredictable gaze. Skip unless Max asks. Confirm?
6. Render resolution target? Source is 2048?1152 but Wan's only test was 480?480. What output size do we want?

---

## KEY PATHS / IDS

**Taygeta (192.168.1.142):**
- SSH key: `~/.ssh/sol_key`
- User: `maxre`
- Wan S2V model: `/mnt/green24/Wan2.2-S2V-14B/`
- Audio encoder (wav2vec2): `~/ComfyUI/models/audio_encoders/wav2vec2-large-xlsr-53-english/`
- Text encoder (umt5): `~/ComfyUI/models/text_encoders/umt5-xxl/`
- S2V fire script: `~/setup/scripts/s2v_fire.py`
- S2V test outputs: `/mnt/green24/s2v_tests/` (one sample: 480?480, 49 frames, 3.06s from July 16)
- Wan VAE: `~/ComfyUI/models/vae/wan_2.1_vae.safetensors`

**Local / MOMA (cwd: `C:\claude_base\.claude\worktrees\priceless-snyder-07082c`):**
- Image outputs: `...\ai_images\kazarian_episode\telepathy_tapes\tape1select_output\`
- MOMA D1 scene: "Tape 1Select", jobs 3381-3402
- Sound assembler: `sc10/sound_assembly/code/` (uses `sass_prep` then `sass`, burns Fish Audio credits)
- Voice: Anna voice clone via Fish TTS

---

## GOTCHAS

- **ComfyUI is not running on Taygeta right now.** Must start it before any render.
- **No budget guard on Fish Audio** - every sass run burns credits. Be intentional.
- **16GB VRAM only** (RTX A4000) - Wan 2.2 S2V is a 14B model. Unknown if it fits comfortably at target resolution.
- **The only test clip was 3 seconds at 480?480.** Scaling to 15 seconds at higher resolution is completely uncharacterized territory.
- **Wan does chunking/stitching for longer clips** - more complex pipeline than single-shot. We haven't built that.
- **Session rules:** all through MOMA system, never self-approve, commit+push to master after working edits, write for the ear in plain ASCII, Max drives approval in the GUI.
- **Job 3401 (v2_room angle) was junked** for unpredictable gaze - skip it.
