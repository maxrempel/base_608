# Scribe handover - milestone 1 (~149K tokens)
# session: 20260617_tender_dirac_aa429b_cec4e446
# cwd: C:\moma\.claude\worktrees\tender-dirac-aa429b
# written: 2026-06-17 15:42:30 by deepseek-v4-pro

## HANDOVER: sc10 arrangement lipsie prompt iteration (D21)

### GOAL (Max's words)
> "nearly good. Describe positive emotions smiles and include every phrase in the prompt. Avoid excessive prompts. Currently, the nods are random. Hopefully if we include actual text, it will work better. Do two versions - minimal and expanded. prompts."

He wants a new lipsie for **sc10 arrangement?1 (lines?0?3)** that:
- explicitly mentions smiles / positive emotions
- embeds the actual spoken dialogue text (to tie mouth shapes to the words)
- comes in two prompt variants: **minimal** and **expanded**
- avoids "excessive" / noisy description

### DECISIONS MADE + WHY
1. **One?clip multiperson lipsie per arrangement.**
   - sc10 is an Anna?Ishtab two?hander. Max wants each arrangement merged into a single clip instead of per?line clips.
   - **Why:** better rhythm, natural back?and?forth without cuts.
2. **Two?shot still.**
   - Approved still `sc01_meet_twoshot_var01.png` (Anna left, red hair; Ishtab right, elder). Both characters clearly visible; avoids cropping issues.
   - **Why:** WAN2?1 needs a single image with both faces for a multi?person lip?sync.
3. **Merged audio** (14.75?s, all 4 lines, silence_buffer=0 to stay under 15?s cap).
   - Built from the exact MP3 lines 0?3, resolved by content hash from D1.
   - **Why:** avoid re?encoding and guarantee lip?sync alignment.
4. **First prompt** (used for job?2761) was:
   > *Two women talking in turn in a calm domed room. The red-haired woman on the left speaks first, looking at the elder; then the elder woman on the right answers, looking back; they alternate gently. Calm, minimal, barely-moving. Matte skin, real pores, no makeup. Soft pastel, muted saturation, film grain. Documentary, unretouched.*
   Result: Max says "nearly good" but nods are random and he believes actual text will help.
5. **Decision to be made now:** precise wording of the two new prompts.
   - Must include the **4 script lines verbatim** (or at least their full text) in the prompt so the model ties mouth movement to phonemes.
   - Must add description of **smiles / positive emotion** for the appropriate lines (the greeting is warm).
   - "Avoid excessive prompts" likely means keep the prompt focused on the action, not on arbitrary styling.

### CURRENT STATE
- **MOMA stack is up**, serving at `http://localhost:8779`.
- **Job?2761** (the first attempt) exists and is viewable in the UI.
- **Merged audio** at `C:\moma\sc10\combo_runner\data\merged_arr01_audio.mp3` (ready for re?use).
- **Two?shot still** at `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\scenes\scene10_images\combo_runner\data\approved_stills\sc01_meet_twoshot_var01.png`.
- **Script lines** (from D1, lines?id 0?3):
  | Line | Character | Text |
  |------|-----------|------|
  | 0    | ANNA      | I'm a historian, from the exterior research foundation. We study settlements like this - the ones that survived the years. |
  | 1    | ISHTAB    | You're the first outsider we've let in for a long time. |
  | 2    | ANNA      | I'm honored. And I know it can't have been an easy decision. |
  | 3    | ISHTAB    | Easier than you might think. The elders remember the old times. We know what it means to cut ourselves off entirely. |
- **Worker:** A fresh fire for the new prompts will be handled by the running wan26au worker (launched automatically by MOMA, listening on the job queue).

### EXACT NEXT STEP
1. **Craft two prompts** (minimal / expanded) that:
   - reference the still image ("Two women...")
   - list the dialogue lines with speaker tags
   - add "they smile warmly" or "positive, gentle smiles" where appropriate
   - keep the photographic/doco styling from the original prompt
2. **Fire two multi?person lipsie jobs** (using the same merged audio and still, just swapping the prompt). The proven fire pattern lives in `C:\moma\sc10\combo_runner\code\_fire_mergeexp.py` (imports `wan26_flauncher.fire_lipsie_multi_person`).
3. **Post both /lipser links** so Max can compare which prompt gives better mouth tracking and natural nodding.

### OPEN QUESTIONS AWAITING MAX
- Does "every phrase" mean literally pasting the 4 lines into the prompt, or a summary like "Anna says she's a historian; Ishtab replies..."? (We'll try literal inclusion first - it's what Wan2.1 understands best.)
- Should the smiles be described as a constant trait ("both women smile warmly throughout") or tied to specific lines?
- Does he want the model to stay on `wan26flau` (the current 14B FL non?emo t2v)? The earlier job used that model.

### KEY PATHS & IDs
- **D1 job record:** `jobs` table, job_id?2761 (existing), new jobs will get sequential ids.
- **Merged audio:** `C:\moma\sc10\combo_runner\data\merged_arr01_audio.mp3`
- **Still:** `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\scenes\scene10_images\combo_runner\data\approved_stills\sc01_meet_twoshot_var01.png`
- **Probe script** (for querying lines/stills): `C:\moma\sc10\combo_runner\code\_d21_probe.py`
- **Build audio script:** `C:\moma\sc10\combo_runner\code\_d21_build_arr01.py`
- **Fire script reference:** `C:\moma\sc10\combo_runner\code\_fire_mergeexp.py`
- **UI link for new lipser pick:** `http://localhost:8779/lipser?ids=<new_job_id>&title=...`

### GOTCHAS / DEAD ENDS
- **Prompt length limit:** Wan2.1?T2V accepts ~75 tokens in the prompt; if we dump all 4 lines verbatim we may exceed the effective token window. The "expanded" version will push that limit - may need truncation or summarisation if the model ignores later parts.
- **Nodding randomness:** The base model (non?emo) often adds head nods as idle motion. Embedding the exact dialogue may help, but the "minimal" version should still include the text because that's the main lever.
- **Speaker order:** Must always be Anna?left, Ishtab?right. The prompt describes left/right; the audio aligns with Anna/Ishtab in sequence.
- **Silence buffer:** Must stay at 0?s (the merged audio is already 14.75?s, cap is 15?s).
- **Model:** Ensure we call `fire_lipsie_multi_person(model="wan26flau")` unless Max explicitly asks for a different model.
