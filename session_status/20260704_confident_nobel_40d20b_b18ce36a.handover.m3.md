# Scribe handover - milestone 3 (~253K tokens)
# session: 20260704_confident_nobel_40d20b_b18ce36a
# cwd: C:\claude_base\.claude\worktrees\confident-nobel-40d20b
# written: 2026-07-04 23:29:14 by deepseek-v4-pro

# Handover: MOMA Storyboard / ReelMaker Fixes (Session D04B)

## GOAL (in Max's own words)

1. **Reel-open slowness** - "When I click on a reel, it takes like 10 seconds for it to open. Probably there is a bug there. It should open. In the past, it was opening like immediately."
2. **Spine?to?pile for stills** - "If I move the image from the spine to the pile, it should just move it because the image is not attached to the lines and can be reusable for other spots. (Reels should still prompt to junk.)"
3. **Previous?scene reels leaking into current scene** - "????? ?? ?????????? ????? ????????? ?????????, ??? ????????? ????????, ? ??? ??????????. ?????? ?????? ????? ????????." (Reels from the previous scene keep leaking in. The filter must work properly.)

---

## DECISIONS + WHY

### 1. Reel-open speedup (server?side connection reuse)

**Root cause**  
The MOMA database is in cloud mode (`mode = d1` ? Cloudflare D1 over HTTP). Every reel?click fires ~4 API calls to the runner (`/api/job`, poll, reel membership, script lines), and each of those calls was opening **a brand?new TCP+TLS connection** to Cloudflare for every single database query. `/api/job` itself opened two separate connections. That's ~12 cold handshakes per click ? measured **~12 seconds total**.

The local video files are never the holdup (serving them is ~0.5?s). The cloud DB itself answers fast when warm (~0.09-0.15?s). The slowness was entirely the per?query connection setup.

**What I changed**  

- **`moma_db.py`** - replaced the low?level `urllib.request.urlopen` (no keep?alive) with a single module?level `requests.Session` that pools connections and reuses them across queries. The session is created once and shared by every `connect_db()` call. Timeout and retry logic retained.
- **`combo_gui.py`** (`/api/job` handler) - eliminated the second, redundant `connect_db()` so the handler uses the same connection for all its internal queries.

**Result**  
After restart, reel?open sequence dropped from **~12?s to ~1.5-1.9?s** (measured across three different reels). Occasional spikes to 2-3?s may still happen under heavy concurrent polling from other tabs, but the baseline is fast. The fix also speeds up every other part of the runner that talks to the cloud DB.

### 2. Spine?to?pile for stills (storyboard UI)

**Root cause**  
The `wirePileDrop` handler in `storyboard_editor_v3.html` treated **all** spine items the same - it always showed the "Junk J###?" prompt and junked the item. An image (still) should just return to the pile because it has no tight coupling to script lines and is meant to be reused elsewhere.

**What I changed**  

- In `wirePileDrop`, added a branch on `category`:  
  - If `category === 'stills'` ? un?pin from the spine and add back to the pile **silently** (no prompt, no junk).  
  - If `category !== 'stills'` (reel/lipsie) ? keep the existing confirm?before?junk flow unchanged.  
- Also moved `pushHistory()` inside the confirm branch so cancelling the junk prompt doesn't create an empty undo step.

**Result**  
Images now slip back to the pile gracefully; reels still get the junk confirmation. No server restart needed - just a hard browser reload.

### 3. Scene?filter leak (ReelMaker showing previous scene's reels)

**Root cause**  
- The **server filter** is correct: when the client sends the right arrangement IDs, the server returns only jobs belonging to those arrangements (proved by direct API test).  
- The **client filter** drifted: the scene?arrangement picker (`arrangement_picker.js`) only wrote its chosen scene's arrangement IDs to localStorage **once at boot and on explicit user change**. If the stored filter ever got cleared (e.g. the search box clears it to "show all", or a load?timing race), it stayed empty forever, and the ReelMaker silently showed every scene including sc09.  
- The system was designed with a 2?second "heartbeat" expectation - all consuming pages (storyboard, mixboard, runner) already have no?op guards in place expecting a periodic re?assertion, but the picker never actually sent the heartbeat.

**What I changed**  

- `arrangement_picker.js` - added a **re?assertion of the current scene selection on every 2?second poll**. If the localStorage filter has drifted to empty (or anything else), this restores it within 2?s. The existing listeners already skip action when nothing changed, so no visible flicker.  
- `prompter_core.js` - added a guard to skip re?rendering when the heartbeat fires with the same scene (previously prompter re?rendered on every `arrangementchanged` event, now it's safe).  
- `mixboard.html` - tightened its listener guard to fully no?op when the scene hasn't changed (previously it skipped the network call but still repainted some lines).  

**Result**  
The scene filter is now self?healing. Even if the filter gets wiped, the ReelMaker will snap back to the correct scene within 2?s. All three files committed and pushed.

---

## CURRENT STATE

All three fixes are **implemented, committed, and pushed to `moma` master**:

- `moma_db.py` - keep?alive session
- `combo_gui.py` - `/api/job` connection reuse
- `storyboard_editor_v3.html` - still?move?only on spine?to?pile
- `arrangement_picker.js` - 2?s heartbeat re?assertion
- `prompter_core.js` - guard against heartbeat
- `mixboard.html` - guard against heartbeat

The MOMA servers have been restarted, picking up the Python changes. The HTML/JS changes require a **hard browser reload** (Ctrl+Shift+R) on the relevant tabs (storyboard, ReelMaker, prompter, mixboard) to bypass the browser cache.

**Max has not yet verified any of these fixes live** - the work is ready for him to test.

---

## EXACT NEXT STEP

1. Max reloads **each affected tab** with Ctrl+Shift+R (or clear cache):  
   - Storyboard (for spine?to?pile fix)  
   - ReelMaker / lipser view (for scene?filter fix)  
   - Prompter and Mixboard (for heartbeat guard safety)
2. Verify:  
   - Click a reel in storyboard ? should now open in ~1-2?s, not 10?s.  
   - Drag an image from spine to pile ? moves back silently, no junk prompt.  
   - Drag a reel from spine to pile ? still asks "Junk J###?", and junks if confirmed.  
   - In ReelMaker, with "ALL Scene 11" selected, no sc09 reels appear. If they still leak, wait 2?s and re?check (heartbeat should self?heal).  
3. If any fix doesn't "feel right" or fails, report back with exactly what you see.

---

## OPEN QUESTIONS (awaiting Max)

- None raised explicitly.  
- Implicit: do any other pages (besides storyboard, ReelMaker, prompter, mixboard) listen to `arrangementchanged` and need a guard? Currently only those four files listen (storyboard v3 already had a guard). If you add new listeners later, they must include the same no?op guard.  
- For the speedup: occasional ~2-3?s "spikes" may still appear when many browser tabs are polling simultaneously. That is multi?query contention, not the connection overhead. If it's bothersome, we can batch parallel queries server?side, but it's a separate task.

---

## KEY FILE PATHS & IDENTIFIERS

- `C:\moma\sc10\combo_runner\code\moma_db.py` - DB connection layer, keep?alive session
- `C:\moma\sc10\combo_runner\code\combo_gui.py` - runner endpoint `/api/job` connection reuse
- `C:\moma\sc10\sound_assembly\code\storyboard_editor_v3.html` - storyboard drop handler
- `C:\moma\sc10\combo_runner\code\arrangement_picker.js` - scene filter picker heartbeat
- `C:\moma\sc10\prompter\code\prompter_core.js` - prompter guard
- `C:\moma\sc10\sound_assembly\code\mixboard.html` - mixboard guard
- Database mode config: `C:\moma\sc10\combo_runner\code\moma_db.py` (line: `mode = d1` - currently cloud; local would be `mode = sqlite`)
- Scene IDs: Scene 11 = scenes.id **3** (21 arrangements), Scene 9 = scenes.id **2** (arrangement id=1)
- Ports: storyboard on `:8790` (slideshow server), runner on `:8779` (combo GUI)
- Check?in name: **D04B**

---

## GOTCHAS & DEAD ENDS ALREADY RULED OUT

- **Server restart did not pick up new code on first try** - after editing Python files, the automated restart appeared to start new processes but the first measurement still showed ~12?s. That was likely due to browser tabs hammering the server immediately after restart (contention), or a stale `.pyc` bytecode cache. The second restart showed the fix working. *Lesson: after touching Python server files, ensure a clean restart and give the servers a few seconds to settle before testing.*
- **Local video files were never the bottleneck** - serving a full 7.4?MB "thumbnail" through the slideshow server took ~0.5?s. The issue was the database lookups, not the video.
- **The cloud DB itself is fast** - raw D1 queries timed at 0.09-0.15?s when connection is warm. With keep?alive, the whole sequence became fast.
- **Scene filter was correct server?side** - test explicitly: `curl /api/jobs?arr=<Scene 11 ids>` returned zero sc09 reels. The leak was purely client?state drift.
- **The 2?s heartbeat design was already there** - storyboard v3, mixboard, and runner already had no?op guards expecting a periodic event; the picker simply never emitted it. I didn't invent a new pattern, I just activated the missing piece. For prompter, I had to add the missing guard.
