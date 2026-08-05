# Scribe handover - milestone 4 (~302K tokens)
# session: 20260619_gifted_driscoll_2d4cde_ddc2f543
# cwd: C:\moma\.claude\worktrees\gifted-driscoll-2d4cde
# written: 2026-06-19 08:04:18 by deepseek-v4-pro

# HANDOVER - D26 (gifted-driscoll-2d4cde worktree)

---

## GOAL (Max's own words)

Max joined as D26, furious about 3 chats failing to fix a simple issue. Two tasks emerged:

1. **Pile filter** - only the good "2 ladies" standard-style images should show in the storyboard pile, not corridors/windows/single-faces/blanks.

2. **Spine UX** (the main task D26 implemented) - four precise asks:
   - When a new lipsie is done, it should land in the 1st spine, pushing the older one to the 2nd spine. (Only for lipsies with "done" or "approved" status.)
   - All lipsies per merg should have big numbers in order of their making, so Max can remember the last 2 without opening and rating each.
   - Older takes must NOT be discarded - sometimes new ones are worse and Max needs to revert.
   - The 2nd spine should be expandable to stretch lipsies horizontally.

Max also named the result-of-a-merge: **"merg"** (noun). D26 added it to the user dictionary.

---

## DECISIONS MADE + WHY

### Pile filter diagnosis (handed to D24)

- **Root cause found:** The team's filter used a filename-regex blocklist (`bg_|extrap|station|window_looking|...`). This is whack-a-mole - `sc05_window_twoshot` is a good 2-ladies shot containing "window", while `bg_corridor` is junk containing a location word. Filenames lie, so the filter kept swinging 166 ? 1.
- **Bonus bug found:** sc05/sc07/sc08 clips were leaking into the sc10 pile via the arrangement?scene mapping.
- **Stable fix identified:** Use the `role` field (shot vs plate) already in the data. D24 retagged backgrounds as `role=plate`, which hid them. This resolved ~90% of Max's complaint.
- **D26's restraint:** When 5 leftover images appeared to be background stragglers (filename-fooled again), D26 handed the list to D24 instead of mutating data. D24 pixel-read them - all were genuine Anna+Ishtab two-shots. The pile is fully correct; no further action needed.
- **Lesson saved:** "Pixels, not filenames" - stored in project memory (`C:\Users\maxre\.claude\projects\C--moma\memory\feedback_pixels_not_filenames.md` and indexed in MEMORY.md).

### Spine implementation (Phase 1 - v51, shipped to master)

- **Making-order signal:** No `created_at` field exists, but `job_id` is an autoincrement integer - higher job_id = made later. Used `job_id` ascending order within each merg to assign ordinals (1 = oldest, highest number = newest).
- **Ordinal display:** Big number overlaid on each 1st-spine slot tile; smaller number on each 2nd-spine take.
- **Expandable 2nd spine:** Click the `2ND SPINE [+]` label toggles expanded class - thumbs stretch from 64px to 146px wide; label flips to `[-]`. Pure CSS + a module-level `Set` tracking which mergs are expanded.

### Spine implementation (Phase 2 - v52, shipped to master)

- **First attempt discarded:** D26 initially built a load-time "always pick newest" auto-promote that writes to the DB. Dry-run on live data revealed **all 31 existing picks were `spine_pinned=1`** - the assign flow pins everything. The auto-promote would be completely inert, and a pure "always newest on load" rule would override Max's deliberate reverts to older takes. D26 reverted the code entirely before pushing.
- **Correct rebuilt design:** The auto-promote only fires for lipsies that are **genuinely new since the storyboard page was opened**. On load, a `freshBaseline` Set captures all existing job_ids. During the 60s refresh cycle, any lipsie NOT in that baseline (i.e., created after the page opened) gets auto-landed on spine1. Existing picks - including deliberate reverts to older takes - are never touched.
- **Why this respects Max's reverts:** If Max reverts from a bad new take back to an older good one, the older one stays. The bad new one was already in the baseline, so no auto-promote fires. Only genuinely new arrivals get pushed.
- **The function:** `autoLandNewLipsies()` - checks `role=shot`, `status=done/approved`, `!freshBaseline.has(job_id)`, `!state.spine_pinned[lh]`. If all pass, calls `assignTake(lh, job_id)` which writes to D1 and updates the DOM.

---

## CURRENT STATE

**Shipped and live on master (b5a4ffa):**
- `storyboard_editor.html` v52, served by slideshow_server on port 8790
- Phase 1 (v51): Big making-order ordinals + expandable 2nd spine
- Phase 2 (v52): Fresh lipsie auto-land in 1st spine (session-scoped - only lipsies arriving after page-open)
- Dictionary: "merg" noun added and committed to claude_base

**Pile complaint:** Resolved - D24's role retag fixed it; all remaining images verified as genuine two-shots.

**No open PRs, no CI, no merge conflicts.** Work is complete.

---

## EXACT NEXT STEP (Max's returning question)

The question: **"why then l2829 didn't land on spine1"**

This is the **known design gap** D26 explicitly flagged when shipping. Answer:

- l2829 almost certainly **already existed when Max opened the storyboard page**. The `freshBaseline` Set captured it at load time, so `autoLandNewLipsies()` treats it as pre-existing - even if it was just made minutes before the page was opened.
- The auto-promote only fires for lipsies that arrive **during** an open session (caught on the 60s refresh), not lipsies made while the storyboard was closed.
- D26's exact message to Max at handoff: *"One small gap: a lipsie made while the storyboard is closed won't auto-land when you reopen (it's treated as already-there). Say the word and I'll make that survive reopens too."*

**If Max wants this gap closed:** The fix is to change the baseline from "job_ids at page load" to "the highest job_id that was already picked for each line_hash at page load" - or to a server-side timestamp. Max needs to say "go" - D26 intentionally left it pending because it changes the semantics (could auto-promote a lipsie made during a closed window, which Max might not want if he hasn't seen it yet).

---

## OPEN QUESTIONS AWAITING MAX

1. **Auto-land across reopens:** Should a lipsie made while the storyboard is closed auto-land when Max reopens? (D26 offered to build this - needs Max's decision.)

2. **Any other junk still showing?** The pile is resolved per D24's pixel-read, but Max should confirm on his Firefox.

---

## KEY PATHS AND IDS

| What | Where |
|------|-------|
| Storyboard editor | `C:\moma\sc10\sound_assembly\code\storyboard_editor.html` (v52) |
| Slideshow server | `C:\moma\sc10\sound_assembly\code\slideshow_server.py` (port 8790) |
| Live storyboard URL | `http://localhost:8790/storyboard` |
| Approved images API | `http://localhost:8790/api/approved_images` |
| Master HEAD | `b5a4ffa` on `origin/master` |
| Worktree | `C:\moma\.claude\worktrees\gifted-driscoll-2d4cde` |
| User dictionary | `C:\claude_base\user_dictionary_tomemex.md` |
| Project language map | `C:\moma\.claude\worktrees\gifted-driscoll-2d4cde\memos\moma_system_map_tomemex.md` |
| Project memory | `C:\Users\maxre\.claude\projects\C--moma\memory\` |
| Board (`bcast`) | `python "C:/claude_base/branch_bulletin/bcast.py"` |

Key code locations in `storyboard_editor.html`:
- **Line ~964:** `freshBaseline` Set declaration
- **Line ~969:** Baseline capture during loader (`freshBaseline.add(job_id)`)
- **Line ~975:** `autoLandNewLipsies()` function
- **Line ~1000:** Call site in loader (after `state.assigned` built)
- **Line ~2829 area:** Where Max saw the missed auto-promote (likely inside the merg rendering loop where ordinals are computed and the spine pick is resolved)

---

## GOTCHAS AND DEAD ENDS

- **Filename-based filtering is hopeless.** The data has clean `role` (shot/plate) and `mood` fields. Any future junk filtering must use those, never filenames. D26 fell into this trap himself when classifying 5 genuine two-shots as "backgrounds" - the filenames lied. **Pixels, not filenames.**
- **The first Phase 2 design (load-time always-newest) was discarded** after a live-data dry-run showed it would be inert (all picks already pinned) and would override Max's deliberate reverts if unpinned. Do not resurrect that approach.
- **The mixboard's auto-resort was removed 2026-05-28** - the storyboard is the sole owner of the spine pick. No fight between the two. (mixboard.html:604.)
- **The server serves HTML fresh from disk** - no restart needed after edits. Just merge to master and reload the page.
- **Playwright lock:** D26 held the Playwright browser lock during testing and always released it (`browser_close`). If testing again, the same pattern: open, test, close.
- **Claude base dict was left uncommitted** by D26 initially - caught and fixed on a later autonomous tick. Check that if doing documentation work.
- **D24 owns `storyboard_editor.html` for pile filtering** - coordinate if touching the pile/filter section. D26 had clearance for the spine section specifically.
- **D25 owns `slideshow_server`** - coordinate if touching assignment/server logic. D26 didn't need to touch it for the spine features (all display + autoLand was client-side).
