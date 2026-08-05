# Scribe handover - milestone 1 (~142K tokens)
# session: 20260701_etermined_greider_50df14_6380f3c0
# cwd: C:\moma\.claude\worktrees\determined-greider-50df14
# written: 2026-07-01 12:19:30 by deepseek-v4-pro

# D57 HANDOVER: sc11-arr02 group scene - interior backdrop correction

---

## GOAL (Max's words, captured across the session)

"Use p1189 as the interior backdrop. White chairs, smaller table, four chairs symmetrically around the table. Werner and Derek seated, Anna and Ishtab standing behind chairs because they just came in. Four cups of tea, pastries, napkins. Insist on symmetrical position of chairs around the table - only four chairs, not all have to be visible. Portraits must be obeyed, faithful face similarity preserved."

Later after seeing the disaster v37: "s3087 was very good, I only disliked the background. Now it's all disaster - you screwed up something else besides the interior ref. The prompt changed and they're looking at the camera."

Then: "p1184" (presumably the correct interior, or a correction to the plate number).

---

## DECISIONS MADE + WHY

### What worked (s3087 = v35, job 3087)
- **Prompt**: A softer "inspired by refs 2, 3, and 4" approach, not rigid "EXACTLY from ref 2 / UNCHANGED."
- **12 refs**: Height ref + interior ref (p1189) + s3027 + s3041 (both style refs) + 8 portraits (4 faces + 4 bodies).
- **Derek body**: `derek_pose_05_table_forward.png` (seated at table, no visible boots, beret on).
- **Seating**: Anna LEFT standing, Ishtab between Anna+Werner standing, Werner MIDDLE seated, Derek RIGHT seated.
- Max declared s3087 "very good" - only disliked the background.

### What broke v37 (job 3089)
- Same refs as v36 except ref 2 swapped to p1189 (`titan_station_v04_artnouveau_legs_a.png`).
- **But the prompt was rewritten** from the s3087 original - D57 wrote a new, more rigid prompt that overspecified ("12/3/6/9 o'clock", "NO BOOTS", "EXACTLY from ref 2").
- Result: characters looking at camera, variable chairs, lost all the good composition from s3087.

### Key insight
The prompt text matters hugely. s3087's prompt was Max's original wording. D57's rewrites in v36/v37 introduced rigidity that broke the scene. **Stick to s3087's exact prompt, only swap the interior ref.**

### p1189 / p1184 confusion
- p1189 in the DB = `titan_station_v04_artnouveau_legs_a.png` - appears to be a **space station exterior** (kazarian_episode/ships/space/). D57 was confused because Max called it "the interior."
- p1184 in the DB = `shuttle_v149a_biggerpod_smallerppl_a.png` - also appears exterior (interiors/shuttle/). 
- Max said "I don't know where from did you take 1189. That's the correct one, the interior. It was lost, I guess, but now it is the correct one. p1184." - **Unresolved: what image does Max actually mean?** p1189 was already in s3087 (the "very good" one), and p1184 is also an exterior when looked up.

---

## CURRENT STATE

- s3087 (v35, job 3087) = the baseline "very good" image. Its prompt and ref list are known and preserved in the DB.
- v37 (job 3089) = disaster, discarded.
- D57 was mid-investigation when the session ended. Last action: looked up p1184 and reported it's also an exterior (`shuttle_v149a_biggerpod_smallerppl_a.png`), then asked Max to clarify.

---

## EXACT NEXT STEP

1. **Resolve the p1189/p1184 question with Max.** p1189 is already in s3087's refs. If Max wants a DIFFERENT interior, which plate ID? p1184 looks like a shuttle exterior too - need Max to confirm or provide the correct plate.

2. **Once the correct interior ref is identified:** take s3087's exact prompt and ref list, swap ONLY the interior ref (ref 2), change NOTHING else in the prompt text, and fire.

3. **Do not rewrite the prompt.** s3087's prompt is the golden reference.

---

## OPEN QUESTIONS FOR MAX

- **"p1189 is already in s3087 - is p1184 a different image you want swapped in? When I look up p1184, it shows a shuttle exterior, not an interior room. Which plate number has the interior backdrop you want?"**
- Also worth asking: "s3087 was 'very good' except the background - if p1189 was already the interior ref in s3087, what specifically about the background didn't you like?"

---

## KEY PATHS, IDs, COMMANDS

### Image IDs & files
| Reference | Job ID | File |
|-----------|--------|------|
| s3027 (v19) | job 3027 | `sc11_arr02_v19.png` |
| s3041 (v31) | job 3041 | `sc11_arr02_v31.png` |
| s3087 (v35, THE GOOD ONE) | job 3087 | `sc11_arr02_v35.png` |
| v34 (disaster) | job 3086 | `sc11_arr02_v34.png` |
| v36 (pretty good, wrong interior) | job 3088 | `sc11_arr02_v36.png` |
| v37 (disaster) | job 3089 | `sc11_arr02_v37.png` |

### Plate IDs in question
| Plate | File |
|-------|------|
| p1189 | `titan_station_v04_artnouveau_legs_a.png` (ships/space - exterior) |
| p1184 | `shuttle_v149a_biggerpod_smallerppl_a.png` (interiors/shuttle - exterior) |

### Canonical portrait refs used across all fires
- Anna face + body, Ishtab face + body, Werner face + body, Derek face + body
- Derek body switched from `derek_pose_01_console_front.png` (bad, boots visible) to `derek_pose_05_table_forward.png` (good, seated at table)

### Key paths
- Workspace: `C:\moma\.claude\worktrees\determined-greider-50df14`
- Combo runner code: `C:/moma/sc10/combo_runner/code/`
- DB module: `moma_db.py` (D1Client class)
- Output stills: `C:/Users/maxre/Nextcloud/ai_images/kazarian_episode/scenes/scene10_images/combo_runner/data/output_stills/`
- Kazarian root: `C:/Users/maxre/Nextcloud/ai_images/kazarian_episode/`

### How D57 fires images
- `fire_image(prompt, ref_bytes_list=[...], concept_arrangement=None, output_prefix='sc11_arr02')` 
- Takes a list of ref PNG file paths, builds a concept strip, sends to OpenAI image API.
- Auto-downscales refs to speed up upload (24 MB ? ~1.4 MB typically).
- Registers result via `fire_job(conn, ...)` into the D1 database.

### How to query the DB
```python
from moma_db import D1Client
d1 = D1Client()
d1.query_sql("SELECT id, input_prompt, plate_recipe FROM jobs WHERE id=3087")
```

---

## GOTCHAS

1. **p1189 and p1184 both resolve to exteriors in the DB**, yet Max calls them "the interior." Do not assume the DB lookup is wrong - but do not proceed until Max clarifies. He may be referencing images by a naming convention or view that differs from what the file contents show.

2. **Never rewrite the prompt when Max says "just swap the interior ref."** s3087's prompt is the golden copy. D57's rewrite in v37 introduced "EXACTLY," "UNCHANGED," "12/3/6/9 o'clock," and other overspecifications that caused the model to produce characters staring at the camera and erratic chair counts.

3. **The formula that works**: 12 refs (height + interior + s3027 + s3041 + 8 portraits). Dropping s3027 or s3041 (going to 11 refs) produced inferior results.

4. **Derek's body ref matters.** `derek_pose_01_console_front.png` shows boots and a console pose - wrong for a seated tea scene. `derek_pose_05_table_forward.png` works.

5. **The imager viewer** is at `http://localhost:8779/imager?ids=<job_id>&title=...` for presenting results.

6. **Fire detached** with `nohup python -u <script>.py > <log>.txt 2>&1 &` - the Windows equivalent works but needs `python -u` for unbuffered output. Monitor with `grep -q "Result:"` polling loop.

7. **Clean up temp scripts** after use (`_d57_fire*.py`, `_d57_fire*_log.txt`).
