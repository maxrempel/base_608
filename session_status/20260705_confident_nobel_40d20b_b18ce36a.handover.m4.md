# Scribe handover - milestone 4 (~300K tokens)
# session: 20260705_confident_nobel_40d20b_b18ce36a
# cwd: C:\claude_base\.claude\worktrees\confident-nobel-40d20b
# written: 2026-07-05 00:05:45 by deepseek-v4-pro

# HANDOVER - D04B Session: Storyboard Reel-Open Slowness, Drag Behavior, Scene Filter Leak

---

## GOAL (in Max's words, translated)

1. **"Investigate why it takes so long to play a reel in storyboard. When I click on a reel, it takes like 10 seconds for it to open. Probably there is a bug there."** - D04B checked in.

2. **"When I move a reel from the spine to the pile, it prompts me to junk it - correct. When I move an image from the spine to the pile, it should just move it because the image is not attached to lines and can be reusable."** - Bug fix requested.

3. **"Reels from the previous scene (sc09) keep showing up in Scene 11 view. This is a disaster. The filter should work clearly."** - Scene filter leak in ReelMaker/Imager.

4. **"Same problem, the filter went crazy, I got lots of junk, old junk."** - After fix #3, Max still saw old-junk behavior, this time in the Imager.

---

## DECISIONS MADE + WHY

### Fix 1: Reel-Open Slowness (12s ? ~1.5s)

**Diagnosis journey (Max pushed back twice - rightly - before we got the real answer):**
- First theory: cloud D1 database slow. Measured: single D1 query = ~0.15-0.3s warm, ~4-5s cold. Plausible but incomplete.
- Measured actual reel-open API sequence: 4 calls (`/api/job`, poll, reel membership, script lines) = consistently ~12s total.
- Compared standalone D1 vs through-server: same query 0.09s standalone vs 2-3s through server - proving the cost was inside the server process, not the database itself.
- **Real root cause:** `moma_db.py`'s `D1ConnectionProxy.execute()` used `urllib.request.urlopen` for every single query - opening a fresh TCP+TLS connection to Cloudflare each time. The `/api/job` handler also opened two separate DB connections redundantly. One reel-click = ~a dozen fresh internet round-trips.

**Why this fix (keep-alive session + single connection):**
- Added a module-level shared `requests.Session` in `moma_db.py` - all D1 HTTP calls reuse one warm TCP+TLS connection. The session is lazy-created on first use.
- Changed `/api/job` in `combo_gui.py` to reuse the same `conn` instead of opening a second `connect_db()`.
- **Result verified:** reel-open dropped from ~12s to ~1.5-1.9s (measured live after restart, across 3 different reels).
- **Files changed:** `sc10/combo_runner/code/moma_db.py`, `sc10/combo_runner/code/combo_gui.py`. Committed + pushed to master.

### Fix 2: Spine-to-Pile Drag Behavior

**What was needed:** Branch on the dragged card's `category`. A **still** (image) should just un-pin and return to the pile (reusable). A **reel** (lipsie/clip) should keep the "Junk J###?" confirmation dialog.

**Implementation in `wirePileDrop` (storyboard_editor_v3.html):**
- Before the junk confirm, check `data.category`. If it's a still: call `detachSlot()` to un-pin the card back to the pile, push history immediately, and `return` (skip the junk flow entirely).
- If it's a reel: exact same old behavior - `confirm()` junk prompt, then junk + unlink if confirmed.
- Moved `pushHistory()` inside each branch so a cancelled reel-drag doesn't leave a no-op undo entry.
- **File changed:** `sc10/sound_assembly/code/storyboard_editor_v3.html`. Committed + pushed. No server restart needed (HTML served from disk).

### Fix 3: Scene Filter Leak (sc09 reels in Scene 11 view)

**Diagnosis:**
- Server filter was proven correct: querying `/api/jobs` with Scene 11's 21 real arrangement ids returned **only** Scene 11 jobs, zero sc09 leak. The server was never the problem.
- **Real root cause:** `arrangement_picker.js` broadcast its scene selection (`arrangementchanged` event + `localStorage` write) exactly once - on boot and on user change. It never re-asserted. If anything later clobbered `moma_arrangement_filter_ids` to empty `[]` (the search box does this, and load races can too), nothing ever restored it. The display silently went to "show all scenes" while still showing "ALL Scene 11" in the dropdown.
- Irony: `runner_core.js` already had a NO-OP guard expecting a 2s "heartbeat" from the picker - but the picker never sent one. The guard existed, the heartbeat didn't.

**Implementation:**
- **`arrangement_picker.js`:** The existing 2s poll loop now writes `moma_arrangement_filter_ids` + fires `arrangementchanged` on every tick - re-asserting the current selection. NO-OP guards in listeners prevent unnecessary reloads/blinks.
- **`prompter_core.js`:** Had no guard at all (would re-render on every 2s heartbeat). Added a guard: skip re-render if scene selection hasn't changed from last time.
- **`mixboard.html`:** Had a partial guard (skipped network but still repainted). Tightened to full NO-OP when nothing changed.
- **Files changed:** `sc10/combo_runner/code/arrangement_picker.js`, `sc10/prompter/code/prompter_core.js`, `sc10/sound_assembly/code/mixboard.html`. Committed + pushed.

**Live verification in Max's Chrome:** Opened a fresh ReelMaker tab - picker on "ALL Scene 11", all 30 visible rows = sc11, zero sc09. Deliberately clobbered the filter to `[]` - within 2s the picker's re-assert restored it to Scene 11's 21 ids. The empty-filter fetch did trigger (pulling the huge all-scenes table) but the display self-healed.

### Fix 4: Cache-Buster Missing arrangement_picker.js

**Why Max kept seeing "same problem" after every JS fix:**
- The runner page (`combo_gui.py`) computes an `assetver` cache-buster from the max mtime of `runner_core.js`, `runner_core.css`, `popup.js`, `popup.css` - but **`ARR_PICKER_JS` was never in that list**. The constant existed but was unused in the version calculation.
- So when the picker was edited, the served version number didn't change. The browser kept serving the **cached old picker** on normal reloads. Only Ctrl+Shift+R hard-reload bypassed it.
- This is why Max kept saying "it's still broken" - his tabs were running stale code.

**Fix:** Added `ARR_PICKER_JS` to the `assetver` max-mtime set in `combo_gui.py`. Restarted runner. Verified: version bumped, server now serves the new picker code with the re-assert, and both `/imager` and `/lipser` pages reference the new version.
- **File changed:** `sc10/combo_runner/code/combo_gui.py`. Committed + pushed.

### Imager "Lots of Junk" at End of Session

**Max's final complaint:** Opened Imager, saw lots of junk/old images under "ALL Scene 11." Thought it was another filter leak.

**Actual finding (not yet confirmed with Max):**
- Checked the database: images 3230-3241 are **genuinely Scene 11** (`bg_sc11_service_desk_room`, arrangement_id=8), freshly generated by the running worker. Not a cross-scene leak.
- Scene 11's arrangement 8 genuinely holds a big pile: **119 junked + 80 unreviewed + 29 approved** background-room images. That's real data, not a filter bug.
- The "active" photo filter in the client code correctly hides junked images - but with an empty or "show all" filter state, everything shows.
- Most likely: Max's Imager tab was still running the **old cached JavaScript** (cache-buster fix hadn't taken effect in that tab yet). One hard reload should fix it.

---

## CURRENT STATE

- **All 4 fixes committed and pushed to master.**
- **Runner server restarted** with new code (keep-alive sessions + corrected cache-buster).
- **The Imager/ReelMaker tabs in Max's Chrome** were likely still running stale cached JS at session end (cache-buster fix requires a fresh page load). Max needs to hard-reload (Ctrl+Shift+R) to get the new picker code.
- **The large pile of Scene 11 background-room images** is real data, not a leak. The filter should correctly hide junked ones with the new code loaded.

---

## EXACT NEXT STEP

1. **Max hard-reloads (Ctrl+Shift+R) the Imager and ReelMaker tabs** to pick up the cache-busted new picker JavaScript.
2. **Verify:** In ReelMaker under "ALL Scene 11", sc09 reels should NOT appear. In Imager under "ALL Scene 11" with "active" filter, junked images should be hidden.
3. **If the flood of Scene 11 background images is still overwhelming:** This is a data-volume problem (119 junk + 80 unreviewed = ~200 images in one arrangement), not a filter bug. Options: add bulk-junk UI, or narrow default view to a single arrangement. Max hasn't decided on this yet.

---

## OPEN QUESTIONS (awaiting Max)

1. **After hard-reload:** Does the Imager still show "old junk"? If yes, which job IDs? I can verify whether they're real Scene 11 data or a true cross-scene leak.
2. **Scene 11 arrangement 8 has ~200 images.** Is that expected/intentional, or should old background-room generations be cleaned up? Max may want a bulk-action or tighter arrangement filtering.

---

## KEY PATHS, FILES, AND IDS

| What | Path |
|---|---|
| D1 connection proxy (keep-alive fix) | `C:\moma\sc10\combo_runner\code\moma_db.py` |
| Runner server (double-connect fix + cache-buster) | `C:\moma\sc10\combo_runner\code\combo_gui.py` |
| Arrangement picker (re-assert fix) | `C:\moma\sc10\combo_runner\code\arrangement_picker.js` |
| Storyboard editor (spine?pile fix) | `C:\moma\sc10\sound_assembly\code\storyboard_editor_v3.html` |
| Prompter core (guard added) | `C:\moma\sc10\prompter\code\prompter_core.js` |
| Mixboard (guard tightened) | `C:\moma\sc10\sound_assembly\code\mixboard.html` |
| Git repo | `C:\moma` (branch: master) |
| D1 worker URL | `https://moma-db-worker.maxwarnock.workers.dev` |
| Config mode | `mode = d1` in config (cloud database) |
| Runner port | `localhost:8779` |
| Storyboard port | `localhost:8790` |
| Scene 11 = scenes.id=3 (21 arrangements) | Scene 9 = scenes.id=2 (1 arrangement, id=1) |
| Leaking jobs investigated | 2742, 2741, 2737 (all arrangement_id=1, sc09) |
| Imager jobs at end | 3230-3241 (arrangement_id=8, sc11, bg_sc11_service_desk_room) |

---

## GOTCHAS AND DEAD ENDS

### Gotchas (things that will trip up future work)

1. **Cache-buster must include every JS file that pages load.** If a fix edits a JS file not in the `assetver` set, browsers keep serving stale code on normal reloads. The list is in `combo_gui.py`'s page handler - if you add new scripts to the HTML, add them there too.
2. **The picker's 2s re-assert now fires `arrangementchanged` continuously.** Any new listener for that event MUST have a NO-OP guard (compare to last-known selection, skip if unchanged) or it'll repaint/reload every 2 seconds. Existing listeners (ReelMaker, Imager, storyboard v2/v3, mixboard, prompter) are all guarded now.
3. **The `requests.Session` in `moma_db.py` is module-level and lazy-created.** It's safe across threads (the session object is thread-safe for HTTP). If the session ever goes stale, `del _d1_session` and the next query creates a fresh one. The fallback to `urllib` is still present if `requests` isn't available.
4. **The spine-to-pile still check uses `data.category`.** This is set in the card-render code. If the category attribute name changes or isn't set on the dragged element, the check silently falls through to the reel path. Confirm the attribute is reliably `"still"` for images.
5. **The runner restart tool (`moma_restart.py`) is windowless and restores the active tab.** It restarts the MOMA servers + render workers. It's safe but kills in-flight renders.

### Dead Ends (approaches that were ruled out)

1. **"Just flip `mode = d1` to `mode = sqlite`"** - Ruled out because the cloud database is shared across machines/workers, and Max didn't confirm this machine is isolated. Would cause data divergence.
2. **"The D1 database itself is slow"** - Proven false. Direct D1 queries from a standalone process are ~0.09s. The cost was in the reconnection, not the query execution.
3. **"The server filter is broken and letting sc09 through"** - Proven false. Direct HTTP test with Scene 11's real arrangement ids returned zero sc09 jobs. The filter logic is correct.
4. **"The images Max saw at the end are a cross-scene leak"** - Data shows they're genuinely Scene 11 (bg_sc11_service_desk_room, arrangement 8). Not a leak. It's a volume problem in that arrangement's pile.
5. **"The picker fix didn't work because the heartbeat doesn't fire"** - Verified live in Chrome: the picker does re-assert every 2s, and it does self-heal a clobbered filter. The problem was Max's tabs running old cached JS (the cache-buster omission).
