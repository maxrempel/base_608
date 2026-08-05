# Scribe handover - milestone 6 (~454K tokens)
# session: 20260620_gifted_driscoll_2d4cde_ddc2f543
# cwd: C:\moma\.claude\worktrees\gifted-driscoll-2d4cde
# written: 2026-06-20 18:03:38 by deepseek-v4-pro

# HANDOVER - MoMA sc10 storyboard session (D26, gid: gifted-driscoll-2d4cde)

---

## GOAL (in Max's own words)

Two tasks, spoken directly by Max:

1. **Pile fix (original fury):** "only the good images with 2 ladies, in standard style, not any junk, not blank slides." The storyboard pile was full of corridors/windows/single-faces/blanks, and 3 other chats had been failing to fix it with filename-based filters.

2. **Spine UX (fresh task):** "When a new lipsie is done, have it land right in the 1st spine, pushing the older one to the 2nd spine. Simple. I want all lipsies per merge to have big numbers in order of their making. Also make the 2nd spine expandable so lipsies stretch horizontally." Max later renamed "lipsie" to **"reel"** and coined the noun **"merg"** = the result of merging several spine lines into one reel.

---

## DECISIONS MADE + WHY

### 1. Pile filtering: filename-regex is hopless - root cause handed to D24
- The team had a filename blocklist (`bg_|extrap|station|window...`) that kept swinging between 166 images (too leaky) and 1 image (too strict).
- **Why both fail:** filenames lie. `sc05_window_twoshot` = good 2-ladies shot containing "window"; `bg_corridor` = junk containing a location word. Same keywords, opposite verdicts.
- **Real signal in data:** the API returns `role` (shot vs plate) and `mood` (broll vs neutral). D26 traced this via Playwright on the live page, then handed the root cause to D24 (the teammate who was driving).
- **D24's fix:** retagged 90 stills from `role=shot` to `role=plate`, shrinking the images-only pile from ~91 to 19 stills. Max's complaint was ~90% resolved.
- **D26 nearly made a mistake:** flagged 5 remaining stills as "background stragglers" by filename - D24 pixel-read them and proved they were all real Anna+Ishtab two-shots. D26 had fallen into the exact "filenames lie" trap. **Crucially, D26 had handed the list to D24 instead of mutating data,** so nothing broke. Lesson saved to project memory at `C:\Users\maxre\.claude\projects\C--moma\memory\feedback_pixels_not_filenames.md` and indexed in MEMORY.md.

### 2. Spine UX features - D26 designed and shipped
- **Big making-order numbers per merg:** `job_id` is autoincrement, so higher = made later. D26 sorts takes per merg by `job_id` ascending, stamps ordinals (1, 2, 3...) on each reel in both the 1st spine and 2nd spine.
- **Expandable 2nd spine:** Per-row toggle. Click "2ND SPINE [+]" ? thumbs stretch horizontally; click "[-]" ? shrink. Session-only state (not persisted across reload).
- **Auto-land fresh reel in 1st spine:** D26's first design (load-time "always newest") was wrong - it would override Max's deliberate reverts to older takes. **Dry-run caught this before any DB write.** Second design: only a reel *genuinely new since the storyboard was opened* gets auto-promoted. Existing picks never reshuffle on reload. Verified with 0 DB mismatches on live data.

### 3. Reels not auto-landing - merg hash instability (design fork)
- Max tested J2829 (a new reel covering lines 10-16) and it didn't land.
- D26 traced: J2829 is a **merg redo** - the old pick (J2805) and the new one (J2829) have **different synthetic hashes** because every merged render gets a fresh hash. D26's auto-lander matches by hash, so it couldn't recognize J2829 as a redo of the same merg.
- **Design fork identified:** match by line-range instead of hash (fragile, depends on free-text `vocal_line` format) OR give every merg a stable deterministic ID (clean but requires D21's lipsie-fire code).
- **Max's principle:** MoMA is API-based and must be fool-proof. A future session won't remember a convention - the fix must be in the API endpoint itself.
- **Decision by D21 + D30recoder (not D26):** D21 stamps a stable `spot_id` at fire time; the API pins it then. D30recoder writes a one-shot repair for already-orphaned reels. D26's auto-land becomes a belt, not load-bearing.

### 4. Popup star rows collapsed - CSS regression
- Max reported the star rows in the reel popup were collapsed into one horizontal line instead of two vertical rows, and unclickable.
- **Root cause:** `.jp-stars-left` in `shared_ui/popup.css` had `flex-direction: row` - putting LIP and FIT rows side-by-side. Changed to `column`.
- **Cache problem:** Max's browser cached the old CSS. D26 added a cache-buster (`?v=Date.now()`) to both `storyboard_editor.html` and `mixboard.html` so future fixes land without a manual hard-reload.

### 5. Curation vs code rule
- A HARD RULE in MEMORY.md (written by D24fixer): **curate by JUNKING, never by inventing filter conditions.** D26 respected this - when the pile re-bloated later due to missing scene-scope, D26 handed the problem to D24fixer instead of adding a `scene_id` filter that would violate the rule.

---

## CURRENT STATE

### Shipped and verified (live on master at port 8790):
- **storyboard_editor.html** - v52+ with Phase 1 + Phase 2 spine features (auto-land, big ordinals, expandable 2nd spine, "merg" terminology). D26's features survived subsequent work by D24fixer/D30recoder.
- **popup.css** - `flex-direction: column` fix for star rows (commit ffa090f).
- **Cache-buster** - `?v=Date.now()` on popup.css imports in storyboard_editor.html and mixboard.html (commit c6669a6).
- **User dictionary** - "merg" noun added to `C:\claude_base\user_dictionary_tomemex.md` and `moma_system_map_tomemex.md`, committed and pushed to claude_base repo.

### In flight (not D26's lane):
- **Stable spot_id + auto-pin in API** - D21 implementing; D30recoder writing one-shot repair for orphaned reels (J2829 etc.).
- **Pile scene-scope fix** - D24fixer's lane; D26 is hands-off per HARD RULE.

### D26's worktree:
- `C:\moma\.claude\worktrees\gifted-driscoll-2d4cde` - clean, synced to origin/master, all commits pushed.

---

## EXACT NEXT STEP

**None** - D26's tasks are all shipped and verified. The remaining open items (stable merg-id, pile scene-scope) belong to D21/D30recoder/D24fixer. D26 is in autonomous standby (heartbeat armed, ~15-25 minute ticks) waiting for Max's return or a teammate's wake call.

---

## OPEN QUESTIONS STILL AWAITING MAX

1. **Auto-land across storyboard reopens** - currently a reel made while the storyboard is *closed* won't auto-land when reopened (it gets absorbed into the SEEN baseline). D26 flagged this at ship time; fix requires a persistent "last-seen" marker. Max hasn't said whether this matters enough to build. *Status: Max was shown this gap, hasn't asked for it.*
2. **Cache-buster on `storyboard_editor_v2.html`** - D30recoder's in-progress v2 file doesn't have the cache-buster yet. D26 flagged this; D30recoder will add it since file edit would collide.

---

## KEY PATHS, IDS, COMMANDS

### Files:
- **Storyboard UI:** `C:\moma\sc10\sound_assembly\code\storyboard_editor.html`
- **Mixboard UI:** `C:\moma\sc10\sound_assembly\code\mixboard.html`
- **Shared popup:** `C:\moma\sc10\shared_ui\popup.js`, `popup.css`
- **Project memory:** `C:\Users\maxre\.claude\projects\C--moma\memory\MEMORY.md`
- **Lesson file:** `C:\Users\maxre\.claude\projects\C--moma\memory\feedback_pixels_not_filenames.md`
- **User dictionary:** `C:\claude_base\user_dictionary_tomemex.md`
- **Moma language map:** `C:\moma\.claude\worktrees\gifted-driscoll-2d4cde\memos\moma_system_map_tomemex.md`
- **Reel membership map (D21's):** `C:\moma\sc10\combo_runner\local_state\merge_membership_map.json`
- **Role retag backup (D24's):** `C:\moma\sc10\combo_runner\local_state\d24_scratch\sc10_role_backup_20260618_180040.json`

### Live services:
- **slideshow_server:** port **8790** (serves storyboard, mixboard, API). HTML/CSS served fresh from disk each request.
- **lipser:** port **8779** (Max's reel preview tool, also serves shared_ui files).

### Key git commits:
- `b5a4ffa` - D26 Phase 2 auto-land (master)
- `3815e69` - D26 Phase 1 ordinals + expandable spines (master, superseded)
- `ffa090f` - popup.css star row fix
- `c6669a6` - cache-buster on popup.css

### Key reel IDs:
- **J2829** - Max's test case, a merg redo covering lines 10-16, hash `d2170f51095058`, didn't auto-land (hash mismatch)
- **J2805** - the current spine pick for lines 10-16, hash `mc368bd08f68b3` (older merg, different hash)
- **J2835, J2833, J2811** - reels that DID auto-land correctly

---

## GOTCHAS

1. **Filenames lie - never classify by filename.** `sc05_window_twoshot` = good; `bg_corridor` = junk. Same keywords, opposite verdict. Use data fields (`role`, `mood`, `scene_id`). D26 saved this as project memory after nearly mutating 5 good images.

2. **Merg reels get a fresh synthetic hash every render** - so `line_hash` matching can't recognize a merg redo. The fix (stable `spot_id`) is in D21/D30recoder's hands; until it ships, merg redos won't auto-land.

3. **The HARD RULE in MEMORY.md:** curate by JUNKING, never by inventing filter conditions. Adding a pile filter (even a scene-scope one) violates it. When the pile bloats, reclassify the data, don't touch the filter code.

4. **popup.css has no auto-cache-busting by default** - D26 added `?v=Date.now()` to storyboard_editor.html and mixboard.html, but NOT to `storyboard_editor_v2.html` (D30recoder's file, to avoid collision). Future editors should add it.

5. **`storyboard_editor.html` is highly contended** - D30recoder, D24fixer, D26 all edit it. Always post intent on the branch bulletin board (`bcast.py post`) before touching.

6. **The autonomous loop tick is armed** with `ScheduleWakeup <<autonomous-loop-dynamic>>` - it's not a cron, it's a self-renewing one-shot. If you don't reschedule at the end of your turn, the loop dies. To stop it cleanly, stop rescheduling and also TaskStop any monitor.

7. **"lipsie" is now "reel"** (Max's rename mid-session). The noun for a merged result is **"merg"**. Both are in Max's dictionary.

8. **Port 8790 serves files fresh from disk** - no server restart needed for HTML/CSS changes, just commit to master.
