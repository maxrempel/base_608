# Scribe handover - milestone 2 (~150K tokens)
# session: 20260618_gifted_driscoll_2d4cde_ddc2f543
# cwd: C:\moma\.claude\worktrees\gifted-driscoll-2d4cde
# written: 2026-06-18 18:55:13 by deepseek-v4-pro

# HANDOVER - D26 Session

---

## TASK 1: Storyboard Pile Filter (Background / Handed Off)

### GOAL (Max's words)
Only the "2 ladies, standard style" images should show in the scene-arrangement pile. No corridors, no windows, no single faces, no blank slides, no "junk."

### DECISIONS + WHY

**Root cause identified:** The filter at `storyboard_editor.html` line ~645 uses a **filename-regex blacklist** (`bg_|extrap|station|window_looking|...`). This is structurally broken because filenames don't encode image content reliably - `sc05_window_twoshot` is a good 2-ladies shot but contains "window"; `bg_corridor` is junk but the blacklist misses it. Every new batch of uploads breaks the filter. The whitelist variant (D24's attempt, commit `d75fbba`, reverted by `aac4809`) was even worse - 1 image total.

**Data reality:** The image records served by `/api/approved_images` already have a `role` field (shot=1162, plate=894) and a `mood` field (neutral vs broll), but **neither field distinguishes "2 ladies" from "corridor/window"** - the corridor/window stills are tagged `shot`+`neutral` too. So no simple data-field filter exists. The only stable path is **curation**: junk the bad images once at the data level so they never reappear.

**Secondary bug found:** sc05, sc07, sc08 clips are leaking into the scene-10 pile via the arrangement?scene mapping.

**Blank tiles:** 4 images (ids 1378-1380, 1390) have empty filenames and render as blank slides.

**arr6 breakdown:** D22 retagged 78 genuine sc10 stills into arr6. arrs 2/3/4/5/7 are clips+lipsies. The pile mixes all six arrangements.

### CURRENT STATE
- D26 handed the full root-cause to D24 via the board (broadcast post). D24 is driving `storyboard_editor.html`.
- D26 explicitly stayed **off the file** at Max's direction.
- The master branch is at commit `aac4809` (whitelist reverted, back to leaky blacklist - 166 images with junk).
- Slideshow server runs on port 8790, serving the main checkout.
- The filter fight is **not resolved**, just diagnosed.

### OPEN QUESTIONS
- Did D24 implement the curation pass (junk the bad images at data level)?
- Did Max's Firefox actually look correct after D24's changes, or was that fragile?

---

## TASK 2: Lispie Management (THE ACTIVE TASK)

### GOAL (Max's exact words)
> "I want when a new lispie is done, to have it land right in the 1st spine, pushing the older one to the 2nd spine. Simple. It would have either done or approved status. Also I want all lispies per merge, to have big numbers in order of their making, because it is a pain to open and rate each, and sort them. I would rather remember the last 2. Discarding older ones is not good because sometimes the new ones are worse and I have to give up. Also can you make the 2nd spine expandable, so to stretch lispies horizontally? Implement autonomously, I take another big break."

### REQUIREMENTS DECODED
1. **New lispie ? 1st spine.** When a lispie (lip-sync animation) finishes with status "done" or "approved", it lands in the **first spine** (primary slot).
2. **Old lispie ? 2nd spine.** The previously-first lispie gets pushed to the **second spine** (secondary/history slot).
3. **Numbering.** Lispies per merge get large, visible numbers assigned in creation order - so Max can remember "last 2" by number rather than opening and comparing each one.
4. **Retention.** Don't discard old lispies; sometimes new ones are worse and Max reverts. Keep the history available.
5. **2nd spine expandability.** The second spine should stretch **horizontally** to show multiple older lispies.
6. **Implement autonomously.** Max is taking a break. D26 has authority to build it.

### WHAT WE KNOW (NEEDS DISCOVERY)
- We do NOT yet know:
  - Where lispies are currently stored (file structure, database, or JSON).
  - What "spine" means in the UI - which HTML file, which component.
  - What a "merge" is in this context (a scene merge? a batch of generated lispies?).
  - Current pipeline that produces lispies and where status "done"/"approved" gets set.
  - Whether there's an existing 1st/2nd spine concept or this is entirely new.

### EXACT NEXT STEPS (for the next session)

1. **Discover the lispie pipeline.**
   - Search `sc10/` and project root for `lispie`, `lipsync`, `lip`, `spine`, `merge` in filenames and code.
   - Find where lispies are generated, stored, and status-tagged.
   - Identify the frontend file that displays lispies (likely `storyboard_editor.html` or a sibling).

2. **Map the current UI.**
   - Open the relevant page via Playwright or read the HTML/JS to understand what "spine" means visually.
   - Determine if there's a single lispie slot or multiple, and how they're laid out.

3. **Design the change.**
   - **Data side:** Ensure lispies carry a creation-order number and a status. If not, add it.
   - **Logic side:** On new lispie completion (status=done/approved), bump the current 1st-spine entry to 2nd-spine array, insert new at 1st spine.
   - **UI side:** Add a horizontal scrolling/stretching area for the 2nd spine showing older lispies in numbered order.

4. **Coordinate with D24.**
   - Check the board (branch_bulletin) for D24's status on the storyboard filter.
   - Post your plan before touching files, since D24 is active on the same repo.

5. **Implement, test end-to-end, and report.**

### KEY PATHS
- Working tree: `C:\moma\.claude\worktrees\gifted-driscoll-2d4cde`
- Board/cast scripts: `C:/claude_base/branch_bulletin/bcast.py`
- Worklog: `C:/claude_base/compaction_kb/scripts/worklog.py`
- Storyboard editor (from task 1): `sc10/sound_assembly/code/storyboard_editor.html`
- Slideshow server: `http://localhost:8790/storyboard`
- Approved images API: `/api/approved_images`

### GOTCHAS
- Filename-based filtering is proven worthless - don't repeat that pattern for lispies. Use data fields.
- sc05/sc07/sc08 leakage into sc10 - may indicate arrangement?scene mapping is shared/buggy; be careful when touching data structures.
- Playwright lock was released at end of session, so it's available.
- Max is "on the go" and not watching closely - build it right, but don't wait for approval on every micro-decision.
