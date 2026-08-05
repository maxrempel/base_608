# Scribe handover - milestone 3 (~246K tokens)
# session: 20260721_claude_base_1ed1e25b
# cwd: C:\claude_base
# written: 2026-07-21 00:10:28 by deepseek-v4-pro

# HANDOVER - Nadali Video Project

---

## GOAL (in Max's words)

Max is building the final, polished version of the "Nadali" video - Anna narrating Max's UEI launch talk on alien hybrids/starseed genetics (delivered Saturday July 11, 2026). The current task cluster: **replace the title and credit cards with a new background image** (`starseed_four_children_DNA.png` - four starseed children with a DNA helix), keep text off faces (place in lower torso band with a soft cloud behind for legibility), update credits to include Claude Code desktop app and production tools (Music by Suno, Images by OpenAI, Video by Wan), note the UEI launch date on the title card, and keep the music bed.

---

## DECISIONS + WHY

1. **select2 music folder chosen** - Max curated exactly 5 Suno tracks into `C:\Users\maxre\Nextcloud\suno_music_catalog\audio\select2`. These are his picks.

2. **Music layering spec** - Loudnorm all tracks, chop the big ones (~300s each) into 4 pieces used once, repeat the short/medium ones so every track gets roughly equal airtime (each ~215-320s out of the 1245s total). Randomly shuffled with crossfade joins (~1.5s fades). Music mixed at 25% of voice volume (measured ~9-10 dB under voice, peaks at -1.3 dB). 3s fade-out at end. This was Max's explicit recipe.

3. **starseed_four_children_DNA.png as card background** - Max provided this image. It's 1620?1080, cropped to 1920?1080 by taking a center strip. Faces occupy the upper portion; text placed only in the lower torso band. A soft white cloud oval is rendered behind the text block so letters remain legible against the busy background. Max was emphatic: no text over faces.

4. **New credits** - Title card subtitle now includes "A Max Rempel talk ? July 11, 2026" (UEI launch date). Credit card now reads: "by Max Rempel & Claude Code desktop app" followed by "Music by Suno ? Images by OpenAI ? Video by Wan" - Max dictated these.

5. **Rebuild strategy** - Rather than re-encoding the whole video from scratch each time, the workflow is: rebuild base v08 body with new cards (via `finalpass_v08.py`, which overlays the site/email lower-thirds on v07 and concatenates title+body+credit), then re-lay the music bed on top (via `music_bed_v09.py` logic, which mixes the pre-built music bed at -12 dB gain under the voice track). This keeps music and video assembly decoupled.

---

## CURRENT STATE

**v10 render is IN PROGRESS** - `remix_v10.py` was launched (last action in the session). This script:
1. Re-runs `finalpass_v08.py` to produce a fresh base video with the new title card (`card_title.png` with starseed image) and new credit card (`card_credit.png` with updated tool credits).
2. Re-runs the music layering step to mix the same music bed under the new base.
3. Output: presumably `nadali_uei_full_video_v10_music.mp4` (but check the exact filename - the script was `remix_v10.py`, output name not explicitly confirmed in transcript).

**Confirmed complete:**
- `nadali_uei_full_video_v08.mp4` - 313 MB, 1244.9s. Final cut with old navy-gradient cards. Verified live at maxrempel.com/temp4.
- `nadali_uei_full_video_v09_music.mp4` - 318 MB, 1244.9s. v08 + music bed. Also live at maxrempel.com/temp4. Music levels verified (no clipping, 25% of voice).
- New title card: `C:\Users\maxre\Videos\max talks\uei_max_talk_20260711\overlay_mockup\card_title.png` - 1920?1080, starseed children background, text "Check for Alien Genes in Your DNA / A Max Rempel talk ? July 11, 2026" in lower band with cloud.
- New credit card: `C:\Users\maxre\Videos\max talks\uei_max_talk_20260711\overlay_mockup\card_credit.png` - 1920?1080, same background, text "by Max Rempel & Claude Code desktop app / Music by Suno ? Images by OpenAI ? Video by Wan" in lower band with cloud.
- Both cards visually QC'd - faces fully clear, text legible, no overlap.

---

## EXACT NEXT STEP

1. **Check if the v10 render finished.** Look in `C:\Users\maxre\Videos\max talks\uei_max_talk_20260711\` for the output file and any log from `remix_v10.py`.
2. **QC the v10 video frames** - grab frames at the title card (t=1.5s), the credit card (near end, ~1241s), and spot-check the music bed level hasn't shifted.
3. **Publish to maxrempel.com/temp4** - update `temp4_index.html` to point to the new file, upload to R2 bucket `maxrempel-papers` under prefix `temp4/`, delete old video object, verify link.
4. **Email Max** if he's still expecting the final link.

---

## OPEN QUESTIONS

- Does Max want any further tweaks to the music level (currently 25%)?
- Does the starseed image cropping work for him, or does he want a different placement?
- The v10 output filename is not locked - `remix_v10.py` generates it. Confirm the name before publishing.
- v09 is currently live at temp4; v10 should replace it.

---

## KEY PATHS / IDs

**Video project root:**
`C:\Users\maxre\Videos\max talks\uei_max_talk_20260711\`

**Key files:**
- `nadali_uei_full_video_v08.mp4` - base final cut (no music)
- `nadali_uei_full_video_v09_music.mp4` - v08 + music bed
- `nadali_uei_full_video_v07.mp4` - pre-card assembly (raw build)
- `v04_clean.mp4` - cleaned talk (retakes + asides cut)
- `finalpass_v08.py` - builds base video (title+body+credit with overlays)
- `music_bed_v09.py` - builds music bed + mixes under voice
- `remix_v10.py` - orchestrates both steps for v10
- `make_cards_v10.py` - generates title and credit cards from starseed image
- `NADALI_FINAL_PLAN.md` - durable plan document

**Card assets:**
- `overlay_mockup/card_title.png` - new title card (starseed bg)
- `overlay_mockup/card_credit.png` - new credit card (starseed bg)
- `overlay_mockup/overlay_website.png` - lower-third for starseedgenetics.com
- `overlay_mockup/overlay_email.png` - lower-third for anna@maxrempel.com

**Music:**
- `C:\Users\maxre\Nextcloud\suno_music_catalog\audio\select2\` - 5 hand-picked tracks
- Full catalog: `C:\Users\maxre\Nextcloud\suno_music_catalog\audio\` (119 tracks)

**Background image for cards:**
- `C:\Users\maxre\Downloads\starseed_four_children_DNA.png` (1620?1080)

**R2 / Hosting:**
- Bucket: `maxrempel-papers`
- Prefix: `temp4/`
- Endpoint: `https://e4dc2224d6baa721873dca77dc6f057d.r2.cloudflarestorage.com`
- Creds in: `C:\Users\maxre\Videos\max talks\uei_max_talk_20260711\publish_temp2.py` (access key / secret key pattern)
- Live URL: `https://maxrempel.com/temp4`
- Worker route handles `/tempN` via `C:\claude_base\sites\maxrempel-site\src\index.js`

**MoMA scene:** `nadali` (named scene, under sc10 combo_runner)

**Anna reel jobs:** 3299-3337 in MoMA DB

---

## GOTCHAS

- **Do NOT circumvent MoMA** - Max was emphatic. All image/video asset creation goes through `fire_job`. The music overlay and card work is post-production outside MoMA's scope, but don't invent new image generation paths.
- **concat FILTER, not concat demuxer** - audio/video drift (0.02-0.06s per segment) was fixed by using the concat filter (`-filter_complex concat=n:v=1:a=1`) instead of the demuxer. Any new assembly must use the filter.
- **Overlay window shifting** - When a title card is prepended (+3.5s), the overlay windows (`enable='between(t,S,E)'`) shift by exactly 3.5s. `finalpass_v08.py` already accounts for this; don't double-shift.
- **Silent reels bug in MoMA** - `jobs.engine` defaults to `'wan22'` in the DB, which caused silent lipsie clips. A guardrail was added in `moma_db.py`: if job_type is 'lipsie' and engine is None/''/'wan22', force it to the lipsync_tool or 'wan26flau'. Don't remove that guardrail.
- **imagegen skill disabled** - `SKILL.md` was renamed to `SKILL.md.DISABLED_20260716` at `C:\Users\maxre\AppData\Roaming\Claude\local-agent-mode-sessions\skills-plugin\54cf6fb1.../skills/imagegen/` because it was hijacking MoMA's image path. Keep it disabled.
- **trimming2 for sentence snaps** - Chapter cuts use `trimmer2` (at `C:\claude_base\tools\trimmer2\trimmer2.py`) to snap to Deepgram sentence boundaries. Do not cut mid-word.
- **R2 credentials** are in `publish_temp2.py` - access key and secret key hardcoded. Deepgram key at `zSyncMain\ssh\deepgram_key_20260515.txt`.
