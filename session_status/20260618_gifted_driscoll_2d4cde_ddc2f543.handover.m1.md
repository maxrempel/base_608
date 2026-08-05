# Scribe handover - milestone 1 (~143K tokens)
# session: 20260618_gifted_driscoll_2d4cde_ddc2f543
# cwd: C:\moma\.claude\worktrees\gifted-driscoll-2d4cde
# written: 2026-06-18 17:49:37 by deepseek-v4-pro

# HANDOVER - MOMA Storyboard Filter (D26)

---

## GOAL (Max's words)
Only images with **2 ladies, standard style** should show in the storyboard pile. No junk, no blank slides, no corridors, no windows, no single-face shots, no clips from other scenes leaking in. The filtering must work end-to-end, tested live.

---

## DECISIONS + WHY

1. **Filename-regex blocklist is dead.**
   The team (3 prior chats) implemented a hide filter in `storyboard_editor.html` line ~645 that blocks filenames matching patterns: `bg_`, `extrap`, `station`, `window_looking`, etc. This is whack-a-mole - every new junk type needs a new pattern. Worse, it produces false positives: `sc05_window_twoshot` is a **good** 2-ladies image but contains "window"; `bg_corridor` is junk and also contains a location word. Same keywords, opposite verdicts. Filename heuristics cannot solve this.

2. **The data carries clean semantic tags.**
   The `/api/approved_images` response includes two reliable fields:
   - `role`: `"shot"` (1162 images) vs `"plate"` (894 images)
   - `mood`: includes `"broll"` for b-roll/background junk
   These are already populated. Filtering on them is the correct long-term fix.

3. **D22 retagged 78 genuine sc10 2-ladies stills into arr6.**
   The 78 arr6 images are the curated good ones. The pile currently mixes all arrangements (arr2 through arr7), including clips and lipsies from arrs 2/3/4/5/7, plus leaked sc05/sc07/sc08 files.

4. **Blank tiles come from plates with empty filenames.**
   IDs 1378, 1379, 1380, 1390 are plates with no filename - they render as the blank slides Max sees.

---

## CURRENT STATE

- **Server:** Slideshow server running on port 8790, serving the main checkout commit `647761d` ("fix: hide backgrounds in storyboard pile").
- **Code:** `c:/moma/sc10/sound_assembly/code/storyboard_editor.html` - filter exists at line ~645, uses filename-regex blocklist.
- **Filter behavior NOW (after Max's attempt to tighten it):** Only **1 image** survives filtering. This is far too aggressive - the filter is eating the good 2-ladies images Max wants to keep.
- **D26's earlier Playwright session:** Closed. Lock released. D26 inspected live data, confirmed the `role`/`mood` fields exist, confirmed the filename approach is hopeless, and proposed switching to `role=plate` + `mood=broll` filtering. But that hasn't been implemented yet - Max simply applied "proper filtering" (unclear exactly what) and wound up with 1 result.
- **Open browser:** Max has Firefox showing the storyboard. D26's Playwright was a separate Chromium instance (now closed).

---

## EXACT NEXT STEP

1. **Read the current filter logic** in `storyboard_editor.html` to understand what "proper filtering" Max just applied (it's over-filtering to 1 image).

2. **Analyze that 1 surviving image** - what is it? Is it actually a 2-ladies standard-style image? This tells us whether the filtering direction is right but threshold wrong, or completely wrong.

3. **Identify what SHOULD survive.** The 78 arr6 images (D22's curated set) are the likely gold-standard set. Cross-reference: which of those 78 have `role=shot` and NOT `mood=broll`? That should yield the correct keep-list.

4. **Rewrite the filter** to use data fields instead of filenames:
   - Hide: `role === "plate"` OR `mood === "broll"`
   - Keep: everything else
   - OR switch to an allowlist: only show images where arrangement index = 6.

5. **Test live** on `http://localhost:8790/storyboard` - verify multiple 2-ladies images appear, no blanks, no corridors, no single-face shots, no clip leaks from other scenes.

6. **Commit** the fix to master once verified.

---

## OPEN QUESTIONS (awaiting Max)

- What exact "proper filtering" was applied that resulted in only 1 image? (Did Max edit the HTML file, or apply a browser-side filter, or change something else?)
- Does Max want ALL arr6 images (78 stills) or a strict subset of those?
- Are there arr6 images that are NOT 2-ladies standard style and should also be excluded?
- Should the filter be an allowlist (only arr6) or a blocklist (hide plates + broll)?

---

## KEY PATHS, IDs, COMMANDS

| What | Path/Value |
|---|---|
| Storyboard HTML | `c:/moma/sc10/sound_assembly/code/storyboard_editor.html` |
| Filter logic location | Line ~645, function likely `getBinImages` or `loadSceneArrIds` |
| Storyboard URL | `http://localhost:8790/storyboard` |
| API endpoint | `/api/approved_images` |
| Server port | 8790 (slideshow_server) |
| Server script | `sc10/moma_restart.py` |
| Master commit with filter | `647761d` ("fix: hide backgrounds in storyboard pile") |
| D22's curated set | arr6 = 78 stills, retagged as genuine sc10 images |
| Blank-slide plate IDs | 1378, 1379, 1380, 1390 (empty filenames) |
| Data field: role | `"shot"` vs `"plate"` (1162 shots, 894 plates) |
| Data field: mood | includes `"broll"` for junk |
| Scene arrangements in pile | arr2 through arr7 (all 6 mixed together) |

---

## GOTCHAS + DEAD ENDS ALREADY RULED OUT

- **Filename blocklist cannot work.** It silently miscategorizes images (e.g., `sc05_window_twoshot` blocked for "window", `bg_corridor` missed by some patterns). Any approach that inspects filenames to decide keep/hide is a dead end.
- **Scenes are leaking cross-scene.** sc05, sc07, sc08 files appear in the scene-10 pile. This may be a data ingestion issue upstream, not just a display filter problem.
- **Playwright runs a separate Chromium.** If Max is testing in Firefox, D26's Playwright tests use a different browser - results must be verified in the actual user-facing browser.
- **The server is live on the main checkout.** Edits to `storyboard_editor.html` must be committed or the server restarted to take effect. The current running code is at commit `647761d`.
- **3 prior chats failed** on this same issue because they kept extending the filename regex instead of using the data fields.
