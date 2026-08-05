# Scribe handover - milestone 2 (~166K tokens)
# session: 20260630_eat_proskuriakova_e24186_7761affe
# cwd: C:\moma\.claude\worktrees\great-proskuriakova-e24186
# written: 2026-06-30 18:03:57 by deepseek-v4-pro

# Handover - D75: Storyboard PILE Scene-Boundary Leak Fix

## GOAL (Max's words)
"The storyboard, for some reason, it has images that don't belong to that scene, so the images only starting from 2000-something are relevant, and previous ones are from the previous scene. For some reason, they leaked into the new scene, so they should follow the filter."

Bug: sc11 PILE view showed old images J222-J1284 (from sc09/sc10) alongside the correct J2967+ images.

## ROOT CAUSE
The client-side `imgInScene()` filter in `storyboard_editor_v2.html` had a broken regex for the "arrless fallback" branch - images with `arrangement_id == null` whose `scene_id` didn't match the regex `/^sc0*(\d+)_/` would fall through to `return true` (include). Two failure modes:

1. **`sc09`** - bare scene_id with no trailing `_` ? regex failed ? included
2. **`sc_walk_*`, `sc_window_*`, `sc_door_*`, `sc_B1_*`, `sc_resume_*`** - no digits at all ? regex failed ? included

All leaked images were legacy sc09/sc10 content with `arrangement_id=null` (pre-standardization, before `fire_job` auto-stamped arrangement_ids).

## DECISIONS & REASONING
- **Server-side filtering was rejected** - `/api/approved_images` serves ALL images system-wide by design; the filter belongs client-side in the storyboard editor.
- **Regex tightened instead of replaced** - kept the `sc`-prefix convention but made the digit match non-optional and the `_` optional (`(?:_|$)`). Added an explicit exclusion clause: any `sc`-prefixed scene_id that doesn't affirmatively match the current `sceneRank` is excluded. Truly untagged (non-`sc`) scene_ids still fall through inclusively as a safety net.
- **Live D1 query used for verification**, not the stale local backup. Confirmed via `/api/arrangements` HTTP endpoint that `scene_rank` comes from a JOIN with `scenes` table (it is NOT a column in `arrangements` directly).

## FIX APPLIED
**File:** `C:/moma/sc10/sound_assembly/code/storyboard_editor_v2.html`
**Function:** `imgInScene()` (was lines 973-986, marked "v2.56 D-58")
**New code (v2.57 D75):**

```javascript
function imgInScene(im){
  if(ST.arrIds && ST.arrIds.indexOf(im.arrangement_id) !== -1) return true;
  if(im.arrangement_id == null){
    const sid = String(im.scene_id||'');
    const mThis = sid.match(/^sc0*(\d+)(?:_|$)/);
    if(mThis) return +mThis[1] === +ST.sceneRank;
    if(/^sc[_\d]/i.test(sid)) return false;
    return true;
  }
  return false;
}
```

Logic:
- Arr-tagged images: include if `arrangement_id` is in `ST.arrIds` (scene-matched arrangements).
- Arrless images: extract scene number from `scene_id`; if it matches `sc0*(\d+)` optionally followed by `_` or end-of-string, include only if the number equals current `sceneRank`. If it's `sc`-prefixed but didn't match the digit pattern (e.g. `sc_walk_*`), **exclude**. If it's truly untagged (no `sc` prefix), include (safety fallback).

## CURRENT STATE
- **Fix committed & pushed** to master: commit `c3a9d36`
- Branch: `great-proskuriakova-e24186` (worktree at `C:\moma\.claude\worktrees\great-proskuriakova-e24186`)
- **Awaits Max verification** - refresh the storyboard tab in Chrome and confirm J222-J1284 are gone from sc11 PILE; only J2967+ should remain.

## EXACT NEXT STEP
Max refreshes the storyboard editor tab and verifies the sc11 PILE no longer shows leaked old-scene images. If it works, D75 is closed. If not, re-examine.

## OPEN QUESTIONS
None. The bug is diagnosed, fixed, pushed.

## KEY PATHS & IDs
- **Storyboard editor:** `C:/moma/sc10/sound_assembly/code/storyboard_editor_v2.html`
- **Server:** `C:/moma/sc10/sound_assembly/code/slideshow_server_v01.py` (port 8790)
- **Live API:** `/api/approved_images` (all images), `/api/arrangements` (with scene_rank via JOIN)
- **D1 backup (stale):** `C:/moma/sc10/d1_backups/current/d1_20260630_174210.json`
- **Diagnostic script (throwaway):** `C:/moma/sc10/combo_runner/code/_d75_check.py`
- **Correct scene 11 arrangement IDs:** 8, 20, 21
- **Leaked image job ranges:** J222-J1284 (sc09/sc10 legacy)
- **Correct scene 11 job ranges:** J2967+

## GOTCHAS & DEAD ENDS RULED OUT
- **`scene_rank` is NOT a direct column** in the `arrangements` table - it comes from `JOIN scenes`. Querying `SELECT scene_rank FROM arrangements` fails. Use the `/api/arrangements` endpoint or JOIN properly.
- **Local sqlite is stale** - always use live D1 for authoritative data.
- **Unicode in D1 backups** - must specify `encoding='utf-8'` when reading JSON backups.
- **The `_` after digits was mandatory** in the old regex - that single character caused both failure modes. Making it optional (`(?:_|$)`) and adding the exclusion clause closed both holes.
- **Do NOT add server-side filtering** to `/api/approved_images` - it's intentionally global; the storyboard editor filters client-side per its active scene context.

## SESSION SIGNATURE
? D75 - Diego, Dormand, date.
