# Scribe handover - milestone 3 (~234K tokens)
# session: 20260617_tender_dirac_aa429b_cec4e446
# cwd: C:\moma\.claude\worktrees\tender-dirac-aa429b
# written: 2026-06-17 18:48:29 by deepseek-v4-pro

# HANDOVER - D21: sc10 Arrangements (Lipsie Production)

---

## GOAL (Max's actual words)

"Register D21, we are starting to work on next arrangement - the first arrangement of sc10. Review everything, suggest how to merge or split - per arrangement. Most likely all 4 or so lines together in one actual scene, how to call it - one lipsie, multiperson. Actually go ahead, make a prompt and produce a lipsie. And then for the next arrangement, same thing."

Later clarified: every prompt **MUST** include the actual spoken lines, labeled with Left/Right speaker. Atmosphere = "formal meeting of officials," mutual gaze, minimal nods, royal postures.

**But final user message - the live grenade:** *"fuck, they must be moving along the path"* - the characters are NOT walking; the still/action may be fundamentally wrong for the scene.

---

## DECISIONS MADE + REASONING

### 1. Merge vs Split Decision
- **arr01 (lines 0-3):** Originally tried as ONE merged 4-turn lipsie (14.75s). This mostly worked after many prompt iterations but nod behavior was erratic and the long duration gave the model too much idle time to invent movements.
- **arr02-04 fired as CHUNKED ?15s clips:** Forced by the 15s clip cap. arr02 split [4+5], [6+7], [8], [9]; arr03 split [10-16], [17-21]; arr04 split [22], [23], [24-28], [29] - 10 clips total for the three arrangements.
- **Rationale:** The existing DB arrangement containers (id3=arr02 lines 4-9, id4=arr03 lines 10-21, id5=arr04 lines 22-29) from prior production work defined the beat boundaries. The splits were mechanical (audio length > 15s ? split into ?15s chunks).

### 2. Prompt Template Locked (after ~14 fires)
- **The winner (2774):** Formal officials, kept in profile, eyes locked on each other (NOT the camera), minimal nods/grins, lines labeled **Left:** / **Right:** with quotation marks. Two-shot still `sc01_meet_twoshot_var01.png` (Anna = red hair, white cloak on LEFT; Ishtab = elder, red robes on RIGHT).
- **What got killed:**
  - "Smiles" / "warm" ? produces random bursts of laughter and stupid nodding (wan2.6-i2v-flash can't do subtle emotional direction).
  - Bracket text (extra dialogue wrapping the real lines) ? scrambles speaker attribution (model swaps Left/Right).
  - "Royal bearing" / grand wording ? model spawns Earth planet in background.
  - Prompts WITHOUT the spoken lines ? user rejected immediately ("this fucking is wrong").
  - Any prompt that lets characters face the camera ? they look at the camera instead of each other (wrong, like addressing a third party).
- **Model:** `wan2.6-i2v-flash`, `prompt_extend=off` (no auto-beautify). Same model as sc09 pod clips. The regression vs sc09 is purely duration: sc09 wins were 2-line ~3s clips; a 4-turn 15s clip gives too much idle time.

### 3. Behavioral Rules Saved
- **No verbatim re-fires:** When Max gives a prompt, he wants a VARIATION, not his exact words fired again (wasted 30?).
- **Never block on polling:** Fire-and-detach; the MOMA worker renders in the background. Stay responsive; don't `sleep` waiting.
- Saved to `C:\Users\maxre\.claude\projects\C--moma\memory\feedback_variation_not_verbatim.md` and `feedback_dont_block_poll.md`, cross-linked in MEMORY.md.

### 4. Audio Resolver Gotcha
- The `audio_resolver.py` verify call requires a `vocal_line` parameter; omitting it causes the resolver to bail before hash matching. Fixed in the fire script but caused a false verify failure on first run.

---

## CURRENT STATE

### DONE:
- **arr01 APPROVED:** Job 2774, 4-line merged multiperson lipsie. Formal-officials template locked.
- **arr02-04 FIRED and RENDERING (detached):** 10 jobs (2775-2784), using the locked template. Awaiting completion (~15 min from fire time) and Max's review.
- **Two-shot still locked:** `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\scenes\scene10_images\combo_runner\data\approved_stills\sc01_meet_twoshot_var01.png` - Anna LEFT, Ishtab RIGHT.

### IN FLIGHT (unreviewed):
| Arrangement | Lines | Jobs | Link |
|---|---|---|---|
| arr02 | 4-9 | 2775, 2776, 2777, 2778 | `/lipser?ids=2775,2776,2777,2778` |
| arr03 | 10-21 | 2779, 2780 | `/lipser?ids=2779,2780` |
| arr04 | 22-29 | 2781, 2782, 2783, 2784 | `/lipser?ids=2781,2782,2783,2784` |

### NOT YET TOUCHED:
- **arr05** (lines 30-32) - not fired, awaiting Max's read on arr02-04 quality first.

---

## EXACT NEXT STEP

**The BIG one first:** Resolve Max's final complaint - *"they must be moving along the path."* The two-shot still shows Anna and Ishtab standing in a domed room facing each other. If the scene actually requires them to be WALKING along a path (traveling together, approaching a destination), the current still and prompt template are fundamentally wrong. Before reviewing arr02-04, need to:

1. **Clarify with Max:** Is the scene supposed to have them walking/moving along a path? If yes, an entirely different still (or video-in video-out approach) is needed - the two-shot `sc01_meet_twoshot_var01.png` won't work.
2. **If path-walking is confirmed:** Need new still(s) showing them on a path, likely in profile or from behind, moving through environment. The entire prompt template shifts from "facing each other in a domed room" to "walking side by side along a path, talking."
3. **Then review arr02-04** (the 10 fired clips) - Max will approve or junk per arrangement. Given the "moving along the path" issue, he may want to scrap them and redo with a walking still.

**If Max is satisfied with the domed-room standing setup:** Check which of jobs 2775-2784 have finished rendering, present them for review, then fire arr05.

---

## OPEN QUESTIONS AWAITING MAX

1. **"Moving along the path"** - what does this mean? Are Anna and Ishtab supposed to be walking during this conversation? If so, the current two-shot still and all 2774-2784 renders are on the wrong visual.
2. **arr01 (2774) truly approved?** Max said "the first one is acceptable" - this could mean "good enough to template from" or "actually approved as final." Need explicit confirmation.
3. **arr02-04 line content fit:** The DB-defined beat boundaries (arr02=4-9, arr03=10-21, arr04=22-29) came from prior production. Does Max still agree with those boundaries, or should beats be redrawn now that he's seen the material?

---

## KEY PATHS, IDs, COMMANDS

### Still Image (the ONLY approved two-shot):
```
C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\scenes\scene10_images\combo_runner\data\approved_stills\sc01_meet_twoshot_var01.png
```
- Anna = red hair, white cloak, **LEFT**
- Ishtab = elder, red robes, **RIGHT**

### D1 Database (query sc10 state):
```python
from moma_db import D1Client
d1 = D1Client()
# sc10 lines
d1.query_sql("SELECT * FROM vocal_lines WHERE scene='sc10' ORDER BY line_index")
# arrangements
d1.query_sql("SELECT * FROM arrangements WHERE scene='sc10'")
# arrangement_line_map
d1.query_sql("SELECT a.arrangement_name, alm.line_index, vl.text FROM arrangement_line_map alm JOIN arrangements a ON a.id=alm.arrangement_id JOIN vocal_lines vl ON vl.id=alm.vocal_line_id WHERE a.scene='sc10' ORDER BY a.id, alm.position")
```

### Fire Pattern (locked template used for 2775-2784):
```python
# Key parameters:
# - still_png_path = sc01_meet_twoshot_var01.png (Anna LEFT, Ishtab RIGHT)
# - correct_speaker_left = True (speaker on LEFT says line first)
# - merged_audio_path = temp merge of per-line MP3s (pydub concatenation + silence_buffer=0)
# - silence_buffer = 0 (to fit the 15s cap)
# - wan_i2v_still = base64 of the still
# - wan_i2v_prompt = template + lines labeled Left:/Right: in quotation marks
```

### Locked Prompt Template (verbatim, used in 2774 ? arr02-04):
```
The speakers keep looking at each other.
Left: "[ANNA'S LINE]"
Right: "[ISHTAB'S LINE]"
Left: "[ANNA'S LINE]"
Right: "[ISHTAB'S LINE]"
The speakers keep looking at each other. Minimalistic nods. Royal postures. Minimal grins; the atmosphere is of a formal meeting of the officials.
```
(For single-line clips, just one Left: or Right: line; for longer merges, all lines in order.)

### MOMA UI (review):
- Base: `http://localhost:8779/lipser?ids=...`
- MOMA stack started via: `cmd //c start_moma.bat` from `C:\moma\sc10\`

### Saved Behavioral Rules:
```
C:\Users\maxre\.claude\projects\C--moma\memory\feedback_variation_not_verbatim.md
C:\Users\maxre\.claude\projects\C--moma\memory\feedback_dont_block_poll.md
C:\Users\maxre\.claude\projects\C--moma\memory\MEMORY.md  (cross-references both)
```

### Worklog:
```
python C:/claude_base/compaction_kb/scripts/worklog.py log "message"
python C:/claude_base/compaction_kb/scripts/worklog.py read
```

---

## GOTCHAS AND DEAD ENDS

| Gotcha | Detail |
|---|---|
| **"Smiles" kills the clip** | Any emotion adjective (smiles, warm, gentle smiles) ? wan2.6 produces random laughter bursts and idiotic head-nodding. DO NOT USE. |
| **Bracket text scrambles speakers** | Adding extra dialogue lines before/after the real ones ? model swaps Left/Right attribution. DO NOT USE. |
| **Facing camera = wrong** | "Royal bearing" / any wording that opens posture ? characters face the camera like addressing a third party. They must stay in profile, eyes locked on each other. |
| **Grand wording spawns objects** | "Royal bearing" or grandiose descriptors ? model invents things (Earth planet appeared in 2772). Keep language grounded. |
| **15s clip cap is hard** | Audio > 15s gets clamped. Merged clips must keep `silence_buffer=0` and total audio ? 15s. |
| **Audio resolver needs `vocal_line` param** | When verifying audio merges via `audio_resolver.py`, must include `vocal_line` parameter or resolver bails before hash matching. |
| **wan26au worker is a poll loop** | Runs serially, ~90s per clip. Must be alive in background (MOMA's `start_moma.bat` launches it). Check via `Test-NetConnection localhost -Port 8779`. |
| **Never block on polls** | Max explicitly said "don't hang when I talk to you, just run the detached." Fire-and-respond; the worker renders independently. |
| **Never re-fire verbatim** | When Max gives a descriptive prompt, he wants a VARIATION - not his exact words fired as-is (costs 30? per wasted fire). |
| **Even lines = Anna (Left), Odd lines = Ishtab (Right)** | The line_index parity maps to speaker position for this two-hander. |
| **The "path" issue is unresolved** | Max's final words indicate the arrangement may need characters WALKING, not standing. This could invalidate all 2774-2784 work if the scene context is fundamentally wrong. |

---

## SESSION SUMMARY (for cold resumption)

D21 produced ~15 lipsie fires across arr01 to lock a prompt template (formal officials, profile gaze, lines labeled L/R). Then fired 10 chunked clips for arr02-04 (jobs 2775-2784) using that template. **Max's last words were that characters must be moving along a path** - this is unresolved and may require scrapping the domed-room two-shot approach entirely. The next session must first clarify the "path" requirement, then review whatever of 2775-2784 has rendered, then either continue or pivot to a walking-based still/prompt.
