# Scribe handover - milestone 2 (~166K tokens)
# session: 20260630_magical_lovelace_c8f08d_5282bce9
# cwd: C:\moma\.claude\worktrees\magical-lovelace-c8f08d
# written: 2026-06-30 00:08:35 by deepseek-v4-pro

# MoMA Session D56 - Handover

---

## GOAL (Max's words)

"In MoMA images, the refresh is too slow. Consider how to speed it up and do implement. Check in as D56."

---

## DECISIONS + WHY

**1. Diagnosed the bottleneck by direct measurement rather than guessing.**
Ran timed HTTP calls from localhost to each endpoint. Found the four endpoints (jobs, plates, stats, canons) were being called sequentially in the frontend, each taking 2-4 seconds because every `conn.execute()` in the Python server is a separate HTTP round trip to Cloudflare D1 (~0.5s latency each, from San Diego). Total refresh wall-time: ~10 seconds.

**2. Chose parallelization over payload shrinking.**
The 4 MB `/api/jobs` payload is the floor (~2s of the remaining 3s), but scene-scoping it was judged too risky - it would touch hard-ruled client-side pile/scene-boundary filtering logic. Parallelizing the independent reads was safer, simpler, and still delivered a 3x speedup.

**3. Parallelized in two layers: frontend and backend.**
- **Frontend** (`runner_core.js`): wrapped the four `api()` calls in `Promise.all` so they fire simultaneously - the browser waits for the slowest single call instead of stacking all four.
- **Backend per-endpoint** (`combo_gui.py`): introduced a `_parallel_select(queries)` helper using `ThreadPoolExecutor` so each endpoint's internal D1 queries (e.g., jobs + script_lines + line_current_clip + clip_edits) run concurrently. Stateless D1 connections make this safe.
- **Stats collapse**: `get_stats()` previously made 4 separate COUNT queries. Collapsed into 1 SQL query using conditional grouping (`SUM(CASE WHEN ... THEN 1 ELSE 0 END)`).

**4. Avoided changing the Cloudflare Worker.**
The worker's `/api/batch` endpoint only returns `{ok, count}`, not rows. A worker redeploy to return batch query results was avoided - add complexity, risk, and deployment surface.

**5. Committed directly to master.**
Per HARD RULE #1: Max only sees merged master. Two files changed, single commit (0659373), pushed.

---

## CURRENT STATE

**Done:**
- `_parallel_select()` helper added to `combo_gui.py` (just before `get_jobs`).
- `get_jobs()` rewritten to fire its 4 internal D1 queries in parallel.
- `get_stats()` collapsed from 4 COUNT queries to 1.
- `/api/plates` handler parallelized (2 queries ? 1 `_parallel_select` call).
- `runner_core.js` `loadAll()` rewritten so the four endpoint fetches run via `Promise.all`.
- Server was restarted via `/api/restart` POST and confirmed back up.
- Timing measured live: **9.6s ? 3.1s (3.1x faster)**.
- Committed and pushed to `master` as commit `0659373` with message "D56 speed up image-grid Refresh ~3x (parallel reads)".
- Posted status to bcast board as D56.
- Syntax check passed on `combo_gui.py` (`ast.parse` OK).

**Not done:**
- No frontend cache-layer changes.
- No D1 worker changes.
- No payload shrinking (the ~4 MB `/api/jobs` full-table download remains as the ~2s floor).

---

## EXACT NEXT STEP

Max needs to **hard-reload the imager page** (F5 / Ctrl+F5) so the browser picks up the new `runner_core.js`, then hit the Refresh button and confirm it feels snappier. The new code is already live on the server - the watcher auto-restarted and the push to master is complete.

No further code changes are planned for D56 unless Max reports an issue or wants the jobs-payload shrinking tackled as a follow-up.

---

## OPEN QUESTIONS

None awaiting Max for D56. One future follow-up documented:
- **Shrinking the /api/jobs payload** (4 MB, takes ~2s). Would require scene-scoping the SQL query, which touches the orphan filter (`job_type != 'image' OR arrangement_id IS NOT NULL OR scene_id LIKE 'sc%'`) and the client-side pile/scene-boundary filtering. Left as a separate task with higher risk.

---

## KEY PATHS / IDs

| What | Path |
|---|---|
| Repo | `C:\moma` (GitHub: `maxrempel/moma`, branch `master`) |
| Python server (edited) | `C:\moma\sc10\combo_runner\code\combo_gui.py` |
| Frontend runner (edited) | `C:\moma\sc10\combo_runner\code\runner_core.js` |
| DB abstraction (read, not edited) | `C:\moma\sc10\combo_runner\code\moma_db.py` |
| Cloudflare Worker (read, not edited) | `C:\moma\sc10\combo_runner\code\moma_db_worker.js` |
| Server port | 8779 (combo_gui) |
| D1 HTTP endpoint | `https://moma-db-api.max-rempel2.workers.dev` |
| Commit | `0659373` on master |
| Session ID on bcast | D56 ("? D56") |
| bcast script | `C:\claude_base\branch_bulletin\bcast.py` |

---

## GOTCHAS

- **The watcher reloader may be flaky.** The file mtimes showed the old code was still live even after edits. Forcing a restart via `POST /api/restart` resolved it. If Max reports no improvement, first check whether the watcher actually picked up the changes (hit `/api/restart` manually).
- **The 4 MB jobs payload is still the floor.** If Max asks "why is it still 3 seconds?", explain that the remaining time is the single slowest call (jobs) downloading the full table from D1. The parallelization already squeezed out all the other waiting, so further gains require shrinking that payload.
- **Do NOT edit `moma_db.py` casually.** It has `_check_plate_eval_safety` and `_check_merge_ops_canonical_path` guards that protect against dangerous operations. The `_parallel_select` helper was added to `combo_gui.py` instead to keep the DB abstraction layer untouched.
- **The worktree at `C:\moma\.claude\worktrees\magical-lovelace-c8f08d` was NOT used.** All edits landed in the main checkout at `C:\moma`. The worktree was a red herring from a prior session setup.
- **Only two files were committed.** Other modified/untracked files in the working directory belong to other sessions. Used `git add` explicitly on just `combo_gui.py` and `runner_core.js`.
