# Scribe handover - milestone 2 (~186K tokens)
# session: 20260725_objective_feynman_eb09d3_b5f68f00
# cwd: C:\moma\.claude\worktrees\objective-feynman-eb09d3
# written: 2026-07-25 13:02:43 by deepseek-v4-pro

## GOAL (Max's words)
- Fix Anna's body posture: she was tilted/twisted - she must face **fully forward**, body, head and eyes all facing the same direction, **straight upright**, no twist, like a presenter looking slightly off?axis to a camera that is shifted but the body is straight.
- Put her in front of a traditional **bookshelf with only books** (no candles).
- The telepathy training should feel like a **one?on?one protected therapy/training session**: Anna is seated *across from* the trainee (the camera/viewer), not alone in a room. Variants: kitchen table, backyard fire pit, armchair.

## DECISIONS + WHY
- **Feed Anna reference plates** into `fire_image()` via `ref_bytes_list`. This keeps her face and body consistent instead of generating a generic person. The two canonical plates used: `anna_approved_headshot_white_cloak_20260330.png` and `anna_approved_body_frontal_white_dress_20260330.png`.  
- **Create a dedicated scene/arrangement "Tape 1"** via `get_or_create_scene`/`get_or_create_arrangement` so all jobs land under a clean, non?movie grouping and do **not** pollute the existing arrangement 40.  
- **Straight?posture prompt** explicitly says "upright straight posture, torso and shoulders facing directly to camera, no twist, head facing same direction, a presenter standing and looking straight ahead."  
- **One?on?one composition** prompt: "Anna seated across from the viewer (the trainee), intimate protected therapy setting, camera = trainee's perspective, she is the only person visible, warm lighting."  
- All images fired through the **MoMA Image Maker pipeline** (`fire_job` + `fire_image`), quality **low**, size **1536?1024**, sequential (no parallel). No hand?rolled HTTP calls. Scripts committed to git.

## CURRENT STATE
Two new batch scripts have been written and run, producing 7 new images in **scene "Tape 1"** (arrangement "Tape 1"):

### 1. Presenter straight posture (4 images)
Script: `fire_tape1_presenter.py`  
Jobs: **3364, 3365, 3366, 3367**  
Each is Anna standing in front of a traditional bookshelf full of books, straight posture. Varied bookshelf framing.

### 2. One?on?one training setups (3 images)
Script: `fire_tape1_situations.py`  
Jobs: **3368** (kitchen table), **3369** (backyard fire pit), **3370** (armchair)  
Each shows Anna seated across from the trainee, only her visible, in a protected setting.

All images are displayed in the Image Maker at:  
`http://localhost:8779/imager?ids=3364,3365,3366,3367,3368,3369,3370&title=Tape+1+Anna+presenter+and+one-on-one+setups`

No user rating/approval has been set (Max must approve manually). No further rounds fired yet.

## EXACT NEXT STEP (what to do when the session resumes)
- **Max has not yet chosen** which one?on?one situation he prefers. The assistant's last message ended with "Look them over and tell me which situation feels right... Once you pick, I'll do a focused round of that one."  
- When the session resumes, **first check** if Max has left a new message (maybe in?between compactions) picking a situation.  
- If he hasn't responded yet, you should **re?present the link** and ask which one to focus on. The assistant hinted the **fire pit** as a top pick.  
- Once Max picks (fire pit / kitchen table / armchair), fire a new batch of 4?6 variations of that specific scenario, keeping Anna straight and across from the viewer, using the same MoMA pipeline and reference plates.

## OPEN QUESTIONS (awaiting Max)
- Which one?on?one setup does he want to develop further? (fire pit was suggested, but he hasn't confirmed.)
- Are the straight?posture bookshelf shots acceptable, or does he need further adjustments (e.g., tighter crop, different lighting, different bookshelf style)?
- Does he want any of the presenter images (straight posture, bookshelf) also turned into one?on?one setups, or should those remain as separate options?

## KEY PATHS / IDs / NAMES
- Scene & arrangement name: `"Tape 1"` (both, created in `fire_telepathy_backgrounds.py` and reused).
- Jobs for straight?posture presenters: **3364, 3365, 3366, 3367**
- Jobs for one?on?one situations: **3368, 3369, 3370**
- Canonical Anna reference plates (absolute, from env path):
  - Face/head: `characters/anna/anna_approved_headshot_white_cloak_20260330.png`
  - Body: `characters/anna/anna_approved_body_frontal_white_dress_20260330.png`
- Scripts (committed to git):
  - `C:\moma\sc10\combo_runner\code\fire_telepathy_backgrounds.py` (first batch of 6 backgrounds, no Anna)
  - `C:\moma\sc10\combo_runner\code\fire_tape1_presenter.py` (the 4 straight?posture bookshelf shots)
  - `C:\moma\sc10\combo_runner\code\fire_tape1_situations.py` (the 3 one?on?one setups)
- Template pattern (still the canonical reference for new scripts): `fire_mediakit_portrait.py` - use its get/create scene/arrangement flow, the prompt INSERT + fire_job + fire_image + done?UPDATE sequence.
- Bulk fire defaults: `paths.IMAGE_QUALITY` = `'low'`, size `1536x1024`, model `gpt-image-2`.

## GOTCHAS / RULED OUT
- **Never hand?roll API calls** - only `fire_job()` + `fire_image()`.  
- **Never parallelise** - OpenAI image endpoint breaks under concurrent calls; always sequential.  
- **Do NOT overwrite `scene_id` in the final UPDATE** - `fire_job()` already sets it to the TEXT scene tag; replacing it with a numeric id breaks scene/name filters.  
- Do **not** approve or rate images - only change `output_status` from `'pending'` to `'done'`.  
- Current arrangement ID for Tape 1 is **not** 40; it's the ID created for "Tape 1" scene, so all jobs are cleanly grouped. Do not accidentally fire into arrangement 40.  
- For the one?on?one setups, the prompt must **not** include a second person - Anna alone, facing camera, the trainee is implied by the POV.  
- The "bookshelf" prompt explicitly **removed candles** per Max's instruction.
