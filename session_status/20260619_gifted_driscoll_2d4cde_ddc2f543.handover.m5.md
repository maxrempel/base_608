# Scribe handover - milestone 5 (~391K tokens)
# session: 20260619_gifted_driscoll_2d4cde_ddc2f543
# cwd: C:\moma\.claude\worktrees\gifted-driscoll-2d4cde
# written: 2026-06-19 19:18:11 by deepseek-v4-pro

# HANDOVER - D26 session (gifted-driscoll-2d4cde, 213 turns)

## MAX'S GOALS (in his own words)

1. **Pile filtering:** Only 2-ladies stills (standard style) should show in the sc10 storyboard pile. No corridors, windows, blanks, single faces.
2. **Spine UX:** New reels auto-land in 1st spine pushing older to 2nd; big making-order numbers; expandable 2nd spine; older reels never discarded.
3. **Star rating popup:** Stars in the Lipsy Edit/Preview/Universal Viewer popup must be two separate clickable rows (LIP + FIT), not collapsed into one unclickable row.
4. **"merg" terminology:** Saved.

---

## WHAT WAS DONE

### A) Spine UX - SHIPPED (v52 on master, b5a4ffa)
File: `sc10/sound_assembly/code/storyboard_editor.html`

- **Big making-order numbers:** Every reel in a merg gets an ordinal (1=oldest, ascending job_id = making order). Shown on both 1st-spine pick and 2nd-spine duplicates.
- **Expandable 2nd spine:** Click `2ND SPINE [+]` to stretch duplicate thumbnails horizontally; click `[-]` to shrink. Per-row, in-session only.
- **Auto-land fresh reels:** When a genuinely new reel (not seen at storyboard open) arrives via the 60s refresh, it lands in the 1st spine and the old pick shifts to the 2nd spine.
- **"merg"** added to user dictionary + project language map.

### B) Star popup CSS - SHIPPED (ffa090f) BUT MAX SAYS NOT FIXED
File: `sc10/shared_ui/popup.css` (line 69)

Changed `.jp-stars-left` from `flex-direction: row` to `flex-direction: column`. This makes the LIP and FIT star rows stack vertically instead of sitting side-by-side on one line.

**Max's feedback at transcript end: "i don't see them fixed"** - so this needs further investigation.

### C) Pile filtering - BROKEN AGAIN, OWNED BY D24fixer/D30recoder
- D24's role retag fixed the pile (19 stills, correct content) earlier in session.
- v56 removed the scene-narrowing filter, and now **439 role=shot images** from all scenes (sc01, sc02, sc03, sc05, B1, etc.) leak into sc10's pile.
- A HARD RULE in MEMORY.md (by D24fixer) forbids adding pile filters - reclassification is the approved fix path.
- D24fixer has a proposed fix using arrangement IDs, needs Max's OK.
- D30recoder (formerly D24) owns the original pixel-verified classification context.

### D) Auto-land bug for merged reels - IN PROGRESS by D21 + D30recoder
- 9 of 12 most recent reels did not auto-land. Root causes:
  - **Merg hash mismatch:** Re-renders of merged spots get different synthetic hashes, so hash-matching (my auto-land's method) can't recognize them.
  - **Closed-storyboard gap:** Reels made while storyboard was closed get absorbed into the SEEN baseline on reopen.
- D21 delivered the membership map (75 sc10 merged reels). D30recoder is writing a one-shot repair.
- Max's principle: fix must be **in the API endpoint** (not convention-based), so no future session can forget.

---

## CURRENT STATE - WHAT NEEDS ATTENTION NOW

### ? IMMEDIATE: Star popup still broken
Max says he doesn't see the fix. The CSS only addressed visual stacking. Two deeper issues found during Playwright testing but NOT addressed:

1. **`window._jpJob` / `window._jpJobId` are never set** in the popup open path. When a star is clicked, `_fitRate()` and `_lipRate()` reference these variables - they throw because the variables are undefined. The rating save to the DB likely fails silently.
2. Stars render with `onclick` handlers but the actual rating persistence was never confirmed end-to-end (Playwright tests had timing artifacts).

**File:** `sc10/shared_ui/popup.js` - the open function must set `window._jpJob` and `window._jpJobId` before the star HTML renders, and the `_lipRate`/`_fitRate` functions need to reference the correct job to persist ratings.

The CSS fix (ffa090f) made rows stack visually but the **click-to-save functionality** is almost certainly broken because the job context variables are unset.

### ? Pile is still full of junk
D24fixer and D30recoder are working on it but not yet shipped. Cross-scene productions leaking into sc10 storyboard.

### ? Auto-land for merg redos
D21 + D30recoder coordinating. One-shot repair + API-level fix needed. Not yet shipped.

---

## EXACT NEXT STEPS

### Step 1 (most urgent): Fix the star popup end-to-end
Max said "i don't see them fixed" - need to:
1. Open `sc10/shared_ui/popup.js`
2. Find where the reel popup open function builds the content (around line 1060+ or wherever the "simple" popup path is)
3. Set `window._jpJob` and `window._jpJobId` to the current reel's job object and job_id so `_lipRate`/`_fitRate` have the context they need to persist ratings
4. Test end-to-end: open any reel, click a star, verify the rating appears in the DB
5. The CSS fix (flex-direction: column) is already on master but verify it renders correctly

### Step 2: Check board for D24fixer/D30recoder pile fix
Read the broadcast board to see if D24fixer shipped the arrangement-based scene boundary fix. If so, reload storyboard and verify pile content.

### Step 3: Check D30recoder's one-shot repair for orphaned reels
The repair script should heal J2829 and other non-landed merg reels. Verify by checking if J2829 (or any recent approved reel) lands in its correct spine position.

---

## OPEN QUESTIONS FOR MAX

- The popup star fix is visually applied but the click-to-save path likely broken - do you see two star rows stacked, or are they still collapsed? If collapsed, browser cache might be holding the old CSS.
- D24fixer needs your OK to add a scene-boundary filter (arrangement-isolated pile) since it contradicts the HARD RULE they just wrote.

---

## KEY FILES

| File | What changed | Status |
|------|--------------|--------|
| `sc10/sound_assembly/code/storyboard_editor.html` | v52 spine UX (auto-land, ordinals, expandable 2nd spine) | Shipped |
| `sc10/shared_ui/popup.css` | flex-direction column fix for star rows | Shipped but insufficient |
| `sc10/shared_ui/popup.js` | Popup open + star rating logic | **Needs fix** - `_jpJob`/`_jpJobId` unset |
| `C:\claude_base\user_dictionary_tomemex.md` | "merg" entry | Committed + pushed |

## KEY IDs

- Master commit with spine UX: **b5a4ffa** (v52)
- Popup CSS fix: **ffa090f**
- Worktree: `gifted-driscoll-2d4cde` (synced to latest master)
- Non-landing reel: **J2829** (merged, covers lines 10-16, hash=d2170f51095058)
- D30recoder = formerly D24, owns classification context
- D24fixer = separate sibling, wrote HARD RULE, owns current pile filter
- D21 = owns reel creation / merge membership data

## GOTCHAS

1. **Filenames lie - never filter by filename.** The original pile filter whack-a-mole was caused by regex-matching filenames which have no reliable signal for good-vs-junk. Role tagging (shot/plate) is the correct approach.
2. **Merged reels get fresh hashes each render.** My auto-land matches by `line_hash` - works for single-line redos but merges get different hashes, so merg redos never auto-land. Needs line-range or stable merg-id matching.
3. **The HARD RULE in MEMORY.md blocks pile filter changes.** Any pile fix must go through D24fixer (rule author) or Max's explicit override.
4. **D26's Playwright lock was released** - no browser session held. Popup testing was done on 8779 (lipser) and 8790 (storyboard).
5. **Server serves files fresh from disk** (no restart needed) - the main checkout at C:\moma is what the 8790 server reads. My worktree merges to main checkout via `git -C /c/moma merge`.
6. **Window globals pattern:** `window._jpJob` and `window._jpJobId` are expected by the star-rating functions but may not be set in all popup open paths. This is the likely root cause of stars being unclickable.
