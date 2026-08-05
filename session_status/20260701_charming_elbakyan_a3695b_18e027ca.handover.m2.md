# Scribe handover - milestone 2 (~166K tokens)
# session: 20260701_charming_elbakyan_a3695b_18e027ca
# cwd: C:\moma\.claude\worktrees\charming-elbakyan-a3695b
# written: 2026-07-01 13:04:59 by deepseek-v4-pro

# HANDOVER - sc11 spot1 merged reel (J3097)

---

## GOAL (Max's words)
> "Okay, make a reel from that. sc11 spot1 L00-L01 lh=e3d6d39b36f10a spine=J3091"

Translate: fire a **merged wan26flau talking-clip** for Scene 11, storyboard spot 1, covering lines **L00 (Ishtab) + L01 (Werner/Gunther)**, using spine still **J3091**, from the `/storyboard2` URI.

---

## DECISIONS MADE + WHY

1. **lh=e3d6d39b36f10a is a line_hash, not a merge_hash.** The storyboard UI shows the anchor line's hash. The real merge_hash is `spd8ff62c3f575` ("lines0-1", 14.45s merged audio). This was discovered by querying `script_lines` then cross-referencing `merges.json`. Using the wrong hash would fail silently.

2. **Pixel-checked the still before writing the prompt.** Viewed `sc11_arr02_v39.png` directly: Anna (far left, red hair, white cloak), Ishtab (standing, left-of-center, red robes + jade beads), Werner/Gunther (seated, center-right, balding, light shirt), Derek (far right, green reptilian, black beret). This grounded the positional instructions in the prompt.

3. **Prompt follows THE GESTURING PROTOCOL** from `project_wan26flau_lane.md`:
   - Positions defined first (scene-setting sentence).
   - Numbered speaking-order list with verbatim quotes + one hand-gesture cue each.
   - Exclusivity clause ("ONLY the one speaking moves their lips").
   - Antiglamour tail ("Real skin, no makeup, film grain, documentary").
   - No smile/grin words.

4. **Fired via `fire_merge_lipsie.py`** - the sanctioned path for already-registered merges (per HARD RULE #0). This auto-spine-pins all member lines via `line_current_clip`.

---

## CURRENT STATE

- **Reel J3097 is DONE and rendered.** Status `completed` in D1. Output file exists:
  `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\scenes\scene10_images\combo_runner\data\output_lipsies\sc11_arr02_lipsie_v3097_wan26flau.mp4` (7.2MB).
- **Spine-pinned** to L00 and L01 in the storyboard.
- **Worker is alive** - pid 9984, auto-recovered from a transient Nextcloud crash.
- **Resilience fix committed + pushed:** `combo_wan26au_worker.py` now has a retry helper (`_makedirs_resilient`) around the two bare `os.makedirs` calls that were dying on transient Nextcloud placeholder errors (WinError -2145452027). Loads on next worker restart.

---

## EXACT NEXT STEP

**Max reviews the reel.** Point him at:
```
http://localhost:8779/lipser?ids=3097&title=sc11%20spot1%20L00-L01%20-%20Ishtab%20intro%2C%20Gunther%20welcomes%20-%20from%20spine%20v39
```

If he wants adjustments (motion, timing, gestures, expression), the prompt is recorded verbatim (see below) and can be tweaked. A junk-and-refire cycle is standard: junk J3097, adjust the prompt, fire a new one via `fire_merge_lipsie`.

---

## OPEN QUESTIONS

None pending from Max. The command was executed fully. Any follow-up depends on his review of the reel.

---

## KEY PATHS & IDS

| What | Value |
|---|---|
| **Reel job ID** | J3097 |
| **Spine still** | J3091 ? `sc11_arr02_v39.png` |
| **Merge hash** | `spd8ff62c3f575` |
| **Line hash (L00 anchor)** | `e3d6d39b36f10a` |
| **Scene / arrangement** | sc11 (scene_id=11), arr02 (arrangement_id=20) |
| **Merged audio** | `merge_spd8ff62c3f575.mp3` (14.45s) |
| **Canonical lane doc** | `C:/Users/maxre/.claude/projects/C--moma/memory/project_wan26flau_lane.md` |
| **Staging bible** | `C:\moma\memos\kazarian_staging_bible_tomemex.md` |
| **Fire function** | `C:\moma\sc10\combo_runner\code\fire_merge_lipsie.py` ? `fire_merge_lipsie()` |
| **Worker** | `C:\moma\sc10\combo_runner\code\combo_wan26au_worker.py` |
| **Worker pid** | 9984 (live) |
| **Output stills dir** | `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\scenes\scene10_images\combo_runner\data\output_stills\` |
| **Output lipsies dir** | `...\combo_runner\data\output_lipsies\` |
| **Git (moma)** | `C:\moma` - resilience fix committed on master |

---

## VERBATIM PROMPT (fired to wan26flau)

> Four people around a small round tea table in a bright room, a planet visible in the window behind.
>
> Speaking order:
> 1. The elder woman in red patterned robes and jade beads (standing, left of center) says: "Gentlemen, here is Anna. Anna, this is Gunther and Derek from the service desk." - she gestures warmly, an open presenting hand introducing them.
> 2. The balding man in the light shirt (seated, center-right) answers: "Ishtab's favorite troublemaker, all grown up. Welcome to the kitchen. We have a few things cooking here. You've arrived at an interesting moment." - relaxed, an easy open-handed welcoming gesture.
>
> At each moment ONLY the one speaking moves their lips; the others listen calmly with small nods. Only their hands move; no objects appear.
>
> Warm and friendly, but calm and unhurried. Real skin, no makeup, film grain, documentary.

---

## GOTCHAS & DEAD ENDS

- **Do NOT confuse `lh=` (line_hash) with `merge_hash`.** The storyboard URI gives the anchor line's hash. Always resolve the real merge_hash from `merges.json` or `merge_ops` before firing. The merge `e3d6d39b36f10a` does NOT exist; `spd8ff62c3f575` does.

- **D1 is SELECT-only at the query endpoint.** No PRAGMA, no table_info. Use `SELECT * ... LIMIT 1` and read `.keys()` to discover schema.

- **`script_lines` uses `scene` (int: 9/10/11) and `idx`** - not `scene_id`.

- **The wan26au worker dies on transient Nextcloud placeholder errors** (WinError -2145452027) when `os.makedirs` hits a dehydrated cloud folder. The retry fix (`_makedirs_resilient` with 3 retries, 2s backoff, touching the parent dir to force materialization) is in place but only activates on the NEXT worker restart - the current live worker (pid 9984) predates the fix.

- **Arrangement 20 = sc11-arr02** (briefing at table). Arrangement 8 = sc11-arr01 (introduction). Verify arrangement matches the still's content before firing - wrong arrangement = wrong scene context in the prompt.

- **Prior reel J3039 from still v27 was junked** - this is why a fresh fire from v39 was correct (not a duplicate).
