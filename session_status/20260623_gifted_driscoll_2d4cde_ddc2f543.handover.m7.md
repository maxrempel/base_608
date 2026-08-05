# Scribe handover - milestone 7 (~538K tokens)
# session: 20260623_gifted_driscoll_2d4cde_ddc2f543
# cwd: C:\moma\.claude\worktrees\gifted-driscoll-2d4cde
# written: 2026-06-23 17:51:36 by deepseek-v4-pro

# HANDOVER - MoMA Session: D26 (gifted-driscoll-2d4cde worktree)

---

## GOAL (in Max's own words)
Fix the **player grabbing a wrong/idiotic reel at image-only spots** (spot 10 onward). When a storyboard spot has only a still image (no reel), the player should **play the static image with sound from the line audio** - not hunt for some unrelated reel. The player must follow the storyboard spine picks and nothing else.

---

## DECISIONS MADE + WHY

**1. Spine UX (v51-v52, SHIPPED)**
- **Big making-order numbers per merg** - using `job_id` (autoincrement) as the making-order signal since no `created_at` field exists. Higher job_id = newer.
- **Expandable 2nd spine** - per-row click toggle on `2ND SPINE [+]` label, CSS stretches thumbnails from 64px to 146px. Session-only (persists only in `EXPANDED_SPINES` Set, not across reload).
- **Fresh-reel auto-land** - only promotes reels genuinely new *since storyboard opened* (captures a `KNOWN_JOB_IDS` baseline at load). Reverts to older takes are never overridden. Deliberate design choice: in-session freshness, NOT load-time "always newest" (which would shuffle Max's deliberate reverts).

**2. Term "merg" (noun)**
- Max named the result of merging multiple spine lines into one lipsie a "merg." Added to user dictionary and moma language map.

**3. Merged reels have UNSTABLE identity (ROOT CAUSE of J2829 not landing)**
- Every merg render gets a fresh synthetic `line_hash`. So J2805 (mc368bd08f68b3) and J2829 (d2170f51095058) are the same merg covering lines 10-16 but have different hashes. Hash-matching can't recognize a merg redo.
- D21 + D30recoder designed the fix: stable spot-id by line-range, D21 stamps membership at fire time, D30recoder ran a one-shot repair. D31 verified 33/33 spots green.

**4. Popup star fix**
- CSS bug: `.jp-stars-left` was `flex-direction: row`, collapsing LIP and FIT star rows side-by-side into one. Fixed to `column`.
- Permanent cache-buster (`?v=Date.now()`) added to popup.css `<link>` in both `storyboard_editor.html` and `mixboard.html` so future CSS fixes land without hard-refresh.

**5. Pile-junk diagnosis (not fixed by D26 - D24/D30recoder's lane)**
- Original complaint: filename-based blacklist/whitelist filter swings 166 ? 1 because filenames lie. `sc05_window_twoshot` = good, `bg_corridor` = junk, both contain location words.
- Solution was role retag (D24/D30recoder pixel-verified) + robust scene boundary (v61). D26 explicitly stayed hands-off the data per HARD RULE in MEMORY.md.

**6. `restart_moma` v17**
- Snapshots active Chrome tab via DevTools port 9222 before killing Chrome, saves to `data/last_moma_tab.txt`, restores focus after relaunch. Fail-silent - if anything goes wrong, Chrome's default tab set is the fallback.

**7. "PLAY THIS" button fixed (v2.40)**
- Was calling `openInRunner()` (popup). Now opens mixboard player at the spot's `start_lh` with `target='moma_player'` so repeated clicks reuse same tab.

---

## CURRENT STATE

| Item | Status | Owner |
|------|--------|-------|
| Spine v51/v52 | Shipped on master (b5a4ffa) | D26 |
| Popup star rows | Shipped (ffa090f) + cache-buster (c6669a6) | D26 |
| restart_moma v17 | Shipped (cce5808) | D26 |
| Pile junk | Resolved (D24/D30recoder role retag + v61) | D24fixer/D30recoder |
| Spot-drop / reel landing | Fixed (v2.32/2.33 + auto-derive, all 33 spots green per d31) | D21/D30recoder/d31 |
| Player wrong-reel after idx 16 | Fix reportedly landed (mixboard v50/v51 membership-aware) | E12/D30recoder |
| **Player wrong-reel at image spots (10+)** | **IN FLIGHT - D26 investigating, waked D44 + D30recoder/D24fixer/d31/D32, 4-min self-check armed** | **NOT YET FIXED** |

---

## EXACT NEXT STEP

**Fix the mixboard player so it handles image-only spine picks correctly.**

The data diagnosis is done: spots 10-14 (idx 28-37) are pinned to still images (J444, J445, J446, J448, J452 - all PNGs, no video). The player must detect `!hasVideo` on the spine pick and fall back to displaying the pinned still image + playing the line audio - not hunting for some reel by `line_hash` that happens to match the individual line but isn't the spine pick.

The likely code path is in `mixboard.html` around the per-line picker (`allItems` filter) or the advance/pool-fetch logic. The membership-aware fix (v50/v51) may have introduced a `hasVideo` guard that drops legitimate still picks.

**Who to fix:** E12 (was D30recoder) or D44 - both were waked via the bcast board. D26 armed a 4-minute self-check timer; if no fix push by then, D26 planned to take `mixboard.html` and fix it directly.

**D26's 4-min timer has expired by now** (this handover is written after that). Check the board to see if a fix was pushed. If not, dive into `sc10/sound_assembly/code/mixboard.html`.

---

## OPEN QUESTIONS (awaiting Max)
None - Max's last instruction was to fix the player at image spots. No forks pending his decision.

---

## KEY PATHS / IDs / COMMANDS

| What | Path/Value |
|------|------------|
| Worktree | `C:\moma\.claude\worktrees\gifted-driscoll-2d4cde` |
| Main checkout | `C:\moma` (master, pushes to origin) |
| Storyboard HTML | `sc10/sound_assembly/code/storyboard_editor.html` (v1), `storyboard_editor_v2.html` (v2.40, D30recoder's rebuild) |
| Mixboard/Player HTML | `sc10/sound_assembly/code/mixboard.html` |
| Popup JS/CSS | `sc10/shared_ui/popup.js`, `sc10/shared_ui/popup.css` |
| restart script | `sc10/moma_restart.py` |
| Live server port | 8790 (slideshow_server), 8779 (combo GUI) |
| Board tool | `python C:/claude_base/branch_bulletin/bcast.py` (read/post/wake) |
| Branch bulletin wake | `--active 24` wakes all D-numbers active in last 24h; `--name D##` wakes specific |
| Spot 10 data | idx 28-37, pinned to J444-J452 (stills, no video), `line_hash` individual per line |
| Membership map | `sc10/combo_runner/local_state/d24_scratch/` (D30recoder/D21's merg data) |
| User dictionary | `C:/claude_base/user_dictionary_tomemex.md` ("merg" added) |
| Project memory | `C:\Users\maxre\.claude\projects\C--moma\memory\MEMORY.md` (HARD RULE about pile filters) |
| Feedback memory | `C:\Users\maxre\.claude\projects\C--moma\memory\feedback_pixels_not_filenames.md` |

---

## GOTCHAS / DEAD ENDS RULED OUT

1. **Filename-based filtering is banned.** D24fixer added a HARD RULE in MEMORY.md after the over-shrink swing. Curate by reclassifying data (role/arr/mood), never by inventing filename-regex filters. D26 fell into this trap himself (flagged 5 real two-shots as "backgrounds" based on filenames - caught by D24's pixel-verification before any damage).

2. **Merged reels have UNSTABLE line_hash.** Every render gets a fresh synthetic hash. Hash-matching alone can never place a merg redo. The fix requires stable spot identity (line-range based) stamped at fire time in the API endpoint itself - not in the caller (Max's principle: MoMA is API-based, fool-proof).

3. **All spine picks are spine_pinned=1 by default** - the assign flow pins everything. A load-time "always pick newest" rule would ignore Max's deliberate reverts. D26's Phase 2 design (in-session freshness baseline) specifically avoids this.

4. **Popup.css was cached browser-side.** Even after the server served the fix, browsers held the old CSS. The permanent cache-buster (`?v=Date.now()`) prevents this forever - but for *this one session boundary*, Max may need a Ctrl+Shift+R one more time.

5. **Don't collide on shared files.** `storyboard_editor_v2.html` is owned by D30recoder; `mixboard.html` by E12/D30recoder; `slideshow_server` by D24fixer/d31. Always bcast-post before editing, and wake the owner if they're active.

6. **Playwright browser lock.** Only one session can hold the Playwright browser at a time (port 9222 conflict). Close it promptly with `mcp__playwright__browser_close` after use. The live servers (8790, 8779) serve files from the main checkout fresh on each request - no restart needed for HTML/CSS changes, but Python server changes need a restart.
