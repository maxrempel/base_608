# Scribe handover - milestone 2 (~178K tokens)
# session: 20260727_gifted_dhawan_44d94e_dde74d7f
# cwd: C:\claude_base\.claude\worktrees\gifted-dhawan-44d94e
# written: 2026-07-27 12:41:00 by deepseek-v4-pro

# Handover for the Cold Session - Telepathy Lesson 1 Lipsync Reels (Iteration 3)

## GOAL (Max's words)
Max saw the second batch of 8 reels (spots 19-26). He liked the overall quality and the removal of third?person framing. However:

- Hand gestures were monotonous - he wants **Pleiadian?style gestures**, varied across clips.
- He junked **"six of the previous reels"** (from the batch before the new 8) and wants them redone **first**, then reviewed, then later he will redo the rejected ones from the new batch.
- He kept spots 19, 21, 23, 25 from the new eight; the other four (20, 22, 24, 26) will be redone later.
- He wants kind, warm delivery; eyes forward, not tracking camera; camera pans / zooms alternating.

## DECISIONS MADE AND WHY

### 1. Batch ordering
Max said: *"Do six first. Do the new ones first. Let's review them. And then after I review the new ones, let's go back and redo the old ones. I'm doing smaller steps just because we're still improving the method."*
Interpretation: Redo the junked reels (the "six") immediately, review them, then afterwards redo the rejected ones from the new eight.  
We are **waiting on Max to clarify** whether it is exactly six or whether the assistant should just redo all eight junked reels (spots 11-18) that the DB shows as junked.

### 2. Handling the "six" vs eight junked reels
The assistant queried MoMA and found **eight** junked lipsie jobs for Lesson 1 - transcripts spots 11 through 18.  
The assistant recommended redoing all eight, so nothing is left behind. Max's answer is pending.

### 3. New motion prompt
Based on Max's feedback and web research on Pleiadian channeling gestures, the assistant crafted a new motion prompt to be used for all subsequent reels:

- Eyes stay forward, soft focus ahead, never tracking the camera.
- Camera physically moves: alternating pan, zoom in, zoom out, zoom in across the batch.
- Gestures: flowing open?palm channeler?style - heart?center, offering palms, slow arcs, blooming fingers.  
  Each clip will explicitly describe a **different gesture** so they never repeat.
- Hands lift off the table; no static resting.
- Delivery: kind, warm, gentle, heavy weighting on kindness.

The exact Wan prompt text will be inserted into the fire script; it is ready.

### 4. Still image situation
Max deleted **two source images** before the second batch because they were inconsistent:
- One with an empty table (table should be covered with candles).
- One with an incorrect curtain.

The remaining stills in `tape1select_output` are the only ones available for new lipsync jobs.  
The junked spots 11-18 originally pointed at specific source images. If any of those images were the deleted ones, those assignments must be replaced with valid stills.

The assistant already ran a directory listing of the remaining PNGs; the session log contains that output (not reproduced here). A cold session can re?run the listing:  
`Get-ChildItem "C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\telepathy_tapes\tape1select_output" -Filter *.png`

### 5. MoMA status of earlier work
- First batch (spots 1-10): fully rendered and approved by Max in the prior session.
- Second batch (spots 19-26): rendered, reviewed by Max. Approved: 19, 21, 23, 25. To redo later: 20, 22, 24, 26.
- Junked batch (spots 11-18): currently status 'error' or 'junked'? The assistant observed them as junked; likely they are in state that a requeue script can turn into 'queued'.

## CURRENT STATE
- **Audio side is solid** - Anna's TTS for all spots exists; `audio_resolver` is fixed and committed.
- **Worker is running** - `combo_wan26au_worker.py` is active, restart not needed.
- **No reels are currently rendering** - the second batch is done, the junked ones are not yet re?queued.
- **The new motion prompt is ready** but not yet written into a fire script.
- **Awaiting Max's answer** on the "six" vs eight question.

## EXACT NEXT STEP (when Max replies)

1. **Confirm with Max** whether to redo all eight junked spots (11-18) or only six specific ones.  
   If Max picks six, identify exactly which spots (maybe he will enumerate them).  
   If he says "yes, all eight", proceed as below.

2. **Create (or adapt) a fire script** for the junked spots:
   - Use `SCENE_TAG = "lesson1"`, `ARRANGEMENT_ID = 42`, `lipsync_tool='wan26flau'`.
   - For each spot (11-18) retrieve the `birth_line_hash` from the existing audio run manifest (`lines_20260726/manifest.json`) and vocal line text.
   - Assign a source image from the remaining stills.  
     If a spot's original source image still exists and was not deleted, re?use it; otherwise pick another still, ensuring variety.
   - Embed the new motion prompt (one prompt per
