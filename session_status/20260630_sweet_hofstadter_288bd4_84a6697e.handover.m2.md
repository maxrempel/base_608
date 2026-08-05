# Scribe handover - milestone 2 (~166K tokens)
# session: 20260630_sweet_hofstadter_288bd4_84a6697e
# cwd: C:\moma\.claude\worktrees\sweet-hofstadter-288bd4
# written: 2026-06-30 00:20:06 by deepseek-v4-pro

# HANDOVER - Popup Libretto Lines Fix

## GOAL (Max's words)
"I don't see you failed to fix image lines in the pop-up. Implement, please."
- Show libretto lines in the image popup (`jp-vocal-lines` div). The images belong to arrangements; only the arrangement's lines should appear (not the whole scene). Sc11 has two arrangements: arr01 (2 people, greeting/intro), arr02 (4 people seated, the crisis briefing).

## DECISIONS + WHY
1. **My first fix was WRONG (rejected by Max):** I modified `_getVocalLines()` in popup.js to fall back to the full `/api/script_lines` endpoint, bridging `scene_id="sc11_arr02"` ? script `scene="11"`. This dumped all 85 lines of scene 11. Max: "you gave me the whole scene, which is a mistake. It should be only whatever the image is produced for the arrangement."
2. **The real data model:** There's a `line_arrangement` table in D1 (mapping specific script line ranges to arrangements). It's populated for scene 10 but **completely empty for sc11** - nobody registered which lines belong to arr01 vs arr02.
3. **Ownership:** Max identified that session D53 owns the line-splitting + Notion sync work that would populate `line_arrangement`. He said: "Talk to D53, it will wake it up. It should feed proper arrangements."
4. **The code fix needs to be redone:** my commit pushed a wrong approach. The correct popup fix should read `line_arrangement` (per arrangement_id on the image) rather than falling back to the whole scene.

## CURRENT STATE
- **Wrong fix committed + pushed to master** (commit message: "popup: show libretto lines for any scene via live script_lines fallback"). This needs rollback or replacement.
- **popup.js** now prefetches `/api/script_lines` into `scriptLinesCache` and `_getVocalLines` has a fallback that returns the full scene's lines keyed by extracted scene number.
- **No API endpoint exposes `line_arrangement`** - none found via grep. One would need to be created or the popup would query it directly.
- **`line_arrangement` table exists** in D1 with these columns (inferred): links arrangement IDs to script line ranges. Populated for scene10, empty for sc11.
- **D53 broadcast was started but interrupted by user** before the `bcast.py wake` command completed.

## EXACT NEXT STEP
1. **Revert or rewrite the wrong popup.js fix.** The current code shows all scene lines - replace with logic that reads `line_arrangement` scoped to the image's `arrangement_id`.
2. **Choose data path:** Either create a new API endpoint for line_arrangement (cleaner, server-side) or have the popup fetch from a new query parameter on an existing endpoint.
3. **Wake D53 properly** (see OPEN QUESTIONS) to get sc11 lines registered into `line_arrangement`.
4. After both code + data are right, commit + push, then ask Max to hard-refresh and verify on J3032 / J3031 popups.

## OPEN QUESTIONS (awaiting Max)
- How does D53 wake? The `bcast.py` command `python "C:/claude_base/branch_bulletin/bcast.py" wake --name D53 "..."` - what's the correct protocol? Does it spawn a new session, or does Max need to manually open D53?
- What are the exact line ranges for sc11 arr01 vs arr02? D53 should know this (it owns the splits).

## KEY PATHS / IDS
- **Worktree:** `C:\moma\.claude\worktrees\sweet-hofstadter-288bd4` (branch `claude/sweet-hofstadter-288bd4`)
- **Main checkout:** `C:\moma` (on `master`, received the bad commit)
- **popup.js:** `C:\moma\sc10\shared_ui\popup.js`
- **popup.css:** `C:\moma\sc10\shared_ui\popup.css` (`.jp-vocal-lines`, `.jp-vl-current`, `.jp-vl-other` - lines ~111-113)
- **combo_gui.py:** `C:\moma\sc10\combo_runner\code\combo_gui.py` (lines 452: `VOCAL_LINES` dict, 2054: `/api/vocal_lines`, 2057: `/api/script_lines`)
- **D1 tables:** `line_arrangement`, `script_lines`, `arrangements`, `jobs`
- **Sc11 arrangements:** sc11-arr01 (14 images, 2 people), sc11-arr02 (30 images, 4 people), sc11-heights (19 images)
- **Images to verify:** J3032 (4? approved, arr02), J3031, J3030
- **D53 data:** The session that splits lines by arrangement and syncs to both Notion and D1 `line_arrangement`

## GOTCHAS
- **Wrong fix is live on master** - the popup currently shows all 85 sc11 lines instead of arrangement-scoped ~5 lines. Must be rolled back or overwritten.
- **`line_arrangement` table is empty for sc11** - even with correct popup code, no lines will show until D53 populates it.
- **popup.js is a static asset** - server-side caching may require a hard refresh (or server restart) after edit.
- **Worktree vs main checkout confusion:** shell cwd resets every Bash call. Always `cd /c/moma/...` explicitly. The previous commit landed on main checkout because that's where the edit accidentally wrote.
- **`es.exe` does not exist** - file searches via Everything CLI fail silently (the binary isn't there). Use Glob instead.
- **SCENE_ID vs scene column mismatch:** image `scene_id = "sc11_arr02"` but `script_lines.scene = "11"` (bare number). Any bridging logic must handle this.
- **Max's standing intents:** "don't ask, keep firing", pingpong/terse replies, answer questions directly (don't fire images when asked a question).
