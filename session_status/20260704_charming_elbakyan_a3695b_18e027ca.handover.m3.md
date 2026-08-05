# Scribe handover - milestone 3 (~226K tokens)
# session: 20260704_charming_elbakyan_a3695b_18e027ca
# cwd: C:\moma\.claude\worktrees\charming-elbakyan-a3695b
# written: 2026-07-04 17:35:38 by deepseek-v4-pro

# HANDOVER: sc11 Reel Firing - Spot 1 Done, Spot 2 Iterating

---

## GOAL (Max's words)

Max is iteratively firing merged talking-clip reels (wan26flau, DashScope wan2.6-i2v-flash) for every storyboard spot in **Scene 11 ("Service Desk & Crisis Briefing")**, using the canonical Gesturing Protocol from `project_wan26flau_lane.md`.

**Spot 1 (intro, L00-L01): DONE AND KEPT.**
Reel J3105 = the keeper. Chinese-prompt v6. Ishtab (~70, wrinkled, red robes, jade beads) introduces Anna to Gunther & Derek. Men rise as ladies approach; chairs slide back; Ishtab gestures with open palm toward Anna then Gunther; everyone looks at the speaker (not camera); no bird-nodding; anti-glamour matte-skin clause.

**Spot 2 (Q&A, L02-L09): IN PROGRESS - 9th iteration just fired.**
Anna asks across the table about the AI shutdown. Derek (green alien) answers "Yes" three times. Werner closes: "Suspicion is infectious." The model merges 8 rapid turns across faces - multiple "Yes" responders, last line mis-assigned to the wrong person. Chinese prompts work better; nicknames + numbers being tested now.

---

## DECISIONS MADE + WHY

1. **Chinese prompts beat English for this model.** Spot 1 started in English (J3097-J3099), improved when restructured to simple sections, then got *much* better in Chinese (J3103 onward). Spot 2's English variants (J3116-J3121) all showed synchronous nodding/mis-assigned speakers, but Chinese v7 (J3122) showed notable improvement - only 2 people saying "Yes" instead of 3, and "Suspicion is infectious" trending toward Werner not Derek. **Chinese is the working language for prompt control in wan2.6-i2v-flash.**

2. **"Person One" word+digit format for speaker identification.** Max directed: use "Person" as a word and "1" as a digit ("Person 1"), not spelled out, not bare digits. In Chinese: ?1??, etc.

3. **Nicknames + numbers together (v8).** Max's theory: combine position number with a visual descriptor so the model can bind turns to the right face. Current v8: ?1?? (red-haired girl on left), ?2?? (old lady in red), ?3?? (old man in white shirt), ?4?? (green alien).

4. **Spot 2 is NOT being split yet.** Max rejected giving up; the model has been improving across iterations (3 responders ? 2 ? trending toward 1). Spot 1 already proved multi-speaker works in this model - spot 2's difficulty is the dense 8-turn rapid alternation, not a hard wall.

5. **Anti-glamour formula (proven from s2530):** "Soft haze filter on faces. Matte skin, not glossy. No specular highlights on skin. Diffused light. Real pores, no makeup. Calm, unhurried, documentary, film grain." This is a required tail clause on every prompt.

6. **Chair movement clause (proven from J3099):** "As each man stands, his chair slides back behind him, pushed away by his legs - the chairs move with the men; legs never pass through the chairs." This works and should be kept if the scene calls for standing.

7. **"No repeated nodding" / "do not nod like birds" (proven from spot 1).** Chinese: ??????. Works but must be stated explicitly.

8. **"Nobody looks at the camera" (proven from spot 1).** Chinese: ??????????. Works with repetition; eyes stay on speaker/Anna.

9. **D03B is the research helper.** It discovered all sc11 per-line voices exist (2026-05-10 sound dir) and built all merged audio by running the documented sass merge-pass canonical path (not a new tool - re-glued existing voices, zero TTS spend). It's standing by for the next task.

10. **No new tools were built for audio.** Max stopped the audio-glue-tool idea mid-flight - D03B found the in-system sass merge path and ran it instead. Spot 2's merge `sp0421c7fa34a3` resolves at 13.32s.

---

## CURRENT STATE

### Spot 1 - DONE AND KEPT
- **Keeper: J3105** (Chinese-prompt v6). Already spine-pinned as the current clip for L00-L01.
- Merge: `spd8ff62c3f575` (lines 0-1, 14.45s audio)
- Still: `sc11_arr02_v39.png` (arrangement 20, briefing at table)
- Arrangement: sc11_arr02 (id=20)
- Scene: 11

### Spot 2 - IN PROGRESS (9th iteration just fired)
- **J3123 (v8) - just fired, rendering.** Merge `sp0421c7fa34a3` (13.32s), still `sc11_arr02_v23.png`.
- Lines covered: L02-L09 (idx 2-9). A Q&A: Anna asks 3 short questions, Derek answers "Yes" ?3, Werner closes.
- Prior iterations J3115-J3122: progressive improvement from "everyone says Yes" (v1) ? 2 people (v7 Chinese-bare) ? v8 adds nicknames+numbers to reduce it further.
- The 8 rapid turns are the model's weak point. But Max sees progress.

### Infrastructure
- **Worker: alive (pid 9984), but running OLD code.** The makedirs resilience fix was committed + pushed but needs a worker restart to load. Not urgent - worker is alive and rendering fine.
- **D1 (Cloudflare):** live. Access via `from moma_db import D1Client; D1Client().query_sql(sql, params)` (returns list of dicts, SELECT only, no PRAGMA).
- **bcast board:** D03B acknowledged, standing by.

---

## EXACT NEXT STEP

**Poll J3123 (spot 2 v8, nicknames+numbers in Chinese) until done, then present it to Max with verbatim prompt.**

The poll loop:
```python
from moma_db import D1Client
r = D1Client().query_sql('SELECT output_status FROM jobs WHERE id=3123', [])
# wait for 'done'
```

Then build the picks-link:
```
http://localhost:8779/lipser?ids=3123&title=sc11%20spot2%20v8%20CHINESE%20nicknames%2Bnumbers
```

**Present with the verbatim prompt from the DB** (`SELECT output_prompt FROM jobs WHERE id=3123`). Max will watch and give the next tweak - either: (a) the two "Yes" responders have reduced to one (keeper), or (b) still 2+ people answering, iterate v9 (possibly stronger per-turn isolation), or (c) if progress plateaus, split into 2-3 shorter reels.

**Do NOT fire anything new until Max reviews J3123.** He is actively iterating.

---

## OPEN QUESTIONS (awaiting Max)

- Does J3123 (nicknames+numbers) reduce the "Yes" to only Derek/the green alien?
- Does "Suspicion is infectious" finally land only on Werner (Person 3)?
- What is the still/image for spot 3? Max said he'd find it.
- Is D03B needed for anything further, or does it stand by?

---

## KEY FILE PATHS + IDs

### Reels (IDs)
| ID | Spot | Description | Status |
|----|------|-------------|--------|
| J3105 | 1 | Chinese v6 - KEEPER | done, pinned |
| J3115 | 2 | v1 (Chinese, names) | done, rejected |
| J3116 | 2 | v2 (English, names) | done, rejected |
| J3117 | 2 | v3 (English, digits) | done, rejected |
| J3118 | 2 | v4 (English, "Person One") | done, rejected |
| J3120 | 2 | v5 (screenplay format) | done, rejected |
| J3121 | 2 | v6 (bare English, speaker only) | done, rejected |
| J3122 | 2 | v7 (bare Chinese) | done, partial - 2 Yes, Werner trending right |
| J3123 | 2 | v8 (Chinese nicknames+numbers) | **just fired, rendering** |

### Merge hashes
- Spot 1: `spd8ff62c3f575` (14.45s)
- Spot 2: `sp0421c7fa34a3` (13.32s)

### Stills
- Spot 1: `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\scenes\scene10_images\combo_runner\data\output_stills\sc11_arr02_v39.png` (arr 20)
- Spot 2: `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\scenes\scene10_images\combo_runner\data\output_stills\sc11_arr02_v23.png` (arr 20)

### Canonical docs
- Gesturing Protocol: `C:/Users/maxre/.claude/projects/C--moma/memory/project_wan26flau_lane.md`
- Staging Bible: `C:\moma\memos\kazarian_staging_bible_tomemex.md`
- Firing function: `C:\moma\sc10\combo_runner\code\fire_merge_lipsie.py` (signature: `fire_merge_lipsie(merge_hash, still, prompt, scene_id, arrangement_id, *, source_job_id=None, note=None, conn=None, op_id=None)`)
- Worker: `C:\moma\sc10\combo_runner\code\combo_wan26au_worker.py` (pid 9984 alive, fix pushed but not loaded)

### Scene 11 script lines (from D1)
- Spot 1: L00 (Ishtab, line_hash `e3d6d39b36f10a`) + L01 (Werner) - "Gentlemen, here is Anna..." ? "Ishtab's favorite troublemaker..."
- Spot 2: L02-L09 (Anna/Derek/Werner) - "The AI shutdown." ? "Yes." ?3 ? "Suspicion is infectious."

### Characters (left?right in both stills)
- **Person 1: Anna** - young, red hair, white cloak
- **Person 2: Ishtab** - ~70, wrinkled, grey-black hair, red patterned robes, jade beads (speaks in spot 1, silent in spot 2)
- **Person 3: Werner/Gunther** - balding, light shirt (speaks closing line in both spots)
- **Person 4: Derek** - tall green reptilian, golden eyes, black beret ALWAYS on, dark SC uniform

---

## GOTCHAS + DEAD ENDS

1. **Do NOT fire a reel unless the merge's audio is confirmed to resolve.** Use `fire_merge_lipsie` which verifies this internally.

2. **Do NOT run TTS or Fish Audio.** Max explicitly stopped this: all voices already exist in `sound/scene11_production/lines_20260510_1714/`. Merged audio is built by D03B or the sass merge-pass (existing in-system path, no new tools).

3. **Nextcloud WinError -2145452027** - transient placeholder blip on `lipsync_temp` makedirs. Fixed with retry wrapper in `combo_wan26au_worker.py` (commit 8e3fe7f), but worker pid 9984 runs old code. Restart the worker to load the fix.

4. **The "rapid-turn smearing" problem** - wan2.6-i2v-flash handles 2-speaker slow alternation fine (spot 1 worked). 8 rapid short turns across 4 faces is harder. Splitting the spot into shorter 2-3 turn reels is the reliable fallback if further Chinese-prompt iterations plateau. Max hasn't authorized splitting yet.

5. **English prompts are a dead end for spot 2.** All English variants (v2 through v6) performed worse than Chinese. The winning spot 1 prompt was also Chinese. Future iterations should stay in Chinese unless Max explicitly calls for another language.

6. **Numbering format:** use `Person 1`, `Person 2` (word + digit) in English; `?1??`, `?2??` in Chinese. Max rejected bare digits and spelled-out numbers.

7. **Spoken lines in the Chinese prompt stay ENGLISH** - the merged audio track is English, so the dialogue quotes in the prompt must match the audio. Only the descriptive framing is Chinese.

8. **Always present the verbatim prompt** with the reel (HARD RULE). Build the picks-link: `http://localhost:8779/lipser?ids=<jobid>&title=<url-encoded description>`. Put the link first, then the quoted prompt.

9. **Do not hedge or give up.** Max explicitly called that out: spot 1 proved multi-speaker works. Iterate before suggesting splitting.

10. **bcast identity is ? D02A.** Check the board (`python C:/claude_base/branch_bulletin/bcast.py read`) before acting on any helper output. D03B is the assigned research helper.
