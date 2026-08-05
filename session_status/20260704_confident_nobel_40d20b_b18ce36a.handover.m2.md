# Scribe handover - milestone 2 (~182K tokens)
# session: 20260704_confident_nobel_40d20b_b18ce36a
# cwd: C:\claude_base\.claude\worktrees\confident-nobel-40d20b
# written: 2026-07-04 17:36:33 by deepseek-v4-pro

# HANDOVER - D04B: Storyboard Reel-Open Slowness Fix

## GOAL (in Max's words)
"When I click on a reel in storyboard, it takes like 10 seconds for it to open. Probably there is a bug there. It should open immediately like it used to. Something is happening in the background which shouldn't be happening."

## DECISIONS + WHY

1. **Initial diagnosis was wrong twice.** First I blamed D1 cloud-latency cold-starts (4-5s per query). Max pushed back: "The file is local. Database is only a link to the file." Then I proposed connection-reuse as the fix. Max pushed back again: "I don't buy it. I think it's just a theory." Both pushes were correct - I had to actually measure and prove before acting.

2. **Measured the real cost, not guessed.** The click fires 4 API calls (job details, job poll, reel membership, script lines). Each call was taking 2-4.5s, totaling ~12s per click. Serving the actual local media file was only ~0.5s. The problem was entirely in the index lookups.

3. **Root cause: no HTTP keep-alive.** `moma_db.py` used `urllib.request.urlopen` for every D1 cloud query - this opens a fresh TCP+TLS connection each time, paying a full handshake per query. `/api/job` in `combo_gui.py` also opened two separate fresh connections per request. A reel-click cascaded into ~a dozen fresh internet round-trips.

4. **Fix accepted after validated proof.** Max said "Absolutely, yes, perfect, that makes sense" only after I tested the exact reel-open sequence against both the library-level fix and the running servers, showing the measurement wasn't a theory.

5. **Why requests.Session:** `requests` 2.32.5 was already available. It pools connections with keep-alive built in. A shared global `requests.Session()` in `moma_db.py` means every D1 query across all server threads reuses warm connections. The `/api/job` double-connect was also merged to use the same single `connect_db()` call instead of opening a second connection.

## CURRENT STATE

- **Fix is live.** The servers were restarted and are running the new code.
- **Performance:** Reel-open dropped from a rock-solid ~12s to ~1.5-1.9s total (each of the 4 calls is ~0.3-0.6s). Verified across three different reels.
- **Code committed and pushed** to moma master:
  - `moma_db.py`: replaced `urllib.urlopen` with a shared `requests.Session()` for keep-alive; added fallback to urllib if requests is unavailable.
  - `combo_gui.py`: eliminated the second redundant `connect_db()` in `/api/job` handler.
- **Debug instrumentation removed.** Temporary timing probe log (`d1_timing_probe.log`) and `print` statements were stripped before final commit.
- **Work-log entry written.**

## EXACT NEXT STEP

Click reels in the storyboard and confirm it feels fast. If any reel still takes more than ~2 seconds, report it - the occasional spike happens under heavy browser-tab polling load but the baseline should be fast. If drag persists, the next place to investigate is the multi-query endpoints (contention from simultaneous browser requests saturating the connection pool).

## OPEN QUESTIONS

None - the fix is complete and verified.

## KEY PATHS / IDS

- **Storyboard server:** `C:\moma\sc10\sound_assembly\code\slideshow_server_v01.py` (port 8790)
- **Runner server (where the fix is):** `C:\moma\sc10\combo_runner\code\combo_gui.py` (port 8779)
- **D1 connection library (where the fix is):** `C:\moma\sc10\combo_runner\code\moma_db.py`
- **Restart tool:** `C:\moma\sc10\moma_restart.py`
- **Start script:** `C:\moma\sc10\start_moma.bat`
- **Test reel IDs used:** 3118, 3105
- **Git remote:** origin, branch: master
- **`requests` version:** 2.32.5

## GOTCHAS

1. **Measuring immediately after restart gives misleading results.** After a server restart, the browser tabs reconnect and all hammer the server at once - transient contention made calls look like 2-3s even though the D1 layer itself was fast (~0.09s). Let things settle for a few seconds before measuring.

2. **The urllib `urlopen` per-query pattern is saturating.** If the fix only halved the cost, it's because the cost wasn't just the handshake - it was also connection-pool exhaustion under concurrent load. The shared `Session` fixes both.

3. **Don't use Playwright if another session holds the browser lock.** It silently hangs. Use curl/python against the localhost endpoints directly - same fidelity, no lock contention.

4. **The "thumbnail" endpoint serves full 7.4MB files.** That's a separate, unfixed issue - it makes the storyboard's initial board-load heavy but wasn't the reel-open blocker. Max didn't ask about it, so I didn't touch it.

5. **Fallback path in moma_db is important.** If `requests` is somehow missing, it falls back to urllib - no breakage, just slower again. The import is inside a try/except.
