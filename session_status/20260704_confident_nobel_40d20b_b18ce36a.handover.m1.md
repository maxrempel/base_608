# Scribe handover - milestone 1 (~129K tokens)
# session: 20260704_confident_nobel_40d20b_b18ce36a
# cwd: C:\claude_base\.claude\worktrees\confident-nobel-40d20b
# written: 2026-07-04 16:45:05 by deepseek-v4-pro

# HANDOVER - D04B: Storyboard Reel-Open Slowness Investigation

---

## GOAL (Max's words)

"When I click on a reel in storyboard, it takes like 10 seconds for it to open. In the past, it was opening immediately. Probably there is a bug. Something is happening in the background which shouldn't be happening."

---

## DECISIONS + WHY

1. **Diagnosed the 10s delay as Cloudflare D1 cold starts, not a code bug.** The storyboard's database layer is configured with `mode = d1`, meaning every database query goes over the internet to a Cloudflare D1 worker. When the worker is idle for a bit, the next query incurs a 4-5 second cold-start penalty. A reel click triggers roughly 4-5 database calls in sequence, so hitting even one or two cold ones lands at ~10 seconds.

2. **Ruled out single slow D1 queries.** A warm D1 query completes in ~150ms. A single query is not the problem - it's the stacking effect of multiple calls multiplied by cold starts.

3. **Ruled out the thumbnail/video serving path as the primary cause of the 10s delay.** The `/thumb_by_job` endpoint serves the full 7.4MB video file (not an actual thumbnail), but individual HTTP requests to it are fast (~0.4s). This is a secondary performance issue (bandwidth waste on the board's initial load), not the 10s click-to-open blocker.

4. **Identified the actual click path.** The reel click invokes `MomaPopup.open(jobId)` in `storyboard_editor_v3.html`, which calls the runner API at `localhost:8779/api/job/<jid>`. That endpoint is where the cold-start D1 queries pile up.

5. **Intentionally did NOT flip any configuration.** The fix was left as a decision for Max because switching from `mode = d1` to `mode = sqlite` would change data locality - the local SQLite copy could diverge from the shared D1 database if other machines or cloud workers are writing to it. The assistant wanted Max to confirm whether shared-cloud or local-only is acceptable before making the change.

---

## CURRENT STATE

- The root cause is **confirmed**: Cloudflare D1 worker cold starts.
- The server stack (slideshow server on port 8790, combo runner on port 8779) is ThreadingHTTPServer-based with Range support.
- The database config lives in `moma_db.py` and currently has `mode = d1`.
- Raw D1 query timing was measured: warm ~150ms, cold 4.0-5.1s.
- `/api/job/<jid>` call times vary from ~0.5s to 5s, consistent with cold-start pattern.
- No background process was saturating D1 - the variance is idle-time dependent.
- No code has been changed. No config has been changed.

---

## EXACT NEXT STEP

**Ask Max: Should the database mode go back to local (`sqlite`) or stay cloud (`d1`)?**

- **If local (`sqlite`):** Flip `mode = 'sqlite'` in the moma_db config. Reel-opens go back to instant. Risk: local DB diverges from cloud if other instances write to D1.
- **If cloud (`d1`) must stay:** Implement a keep-warm mechanism (periodic ping) plus connection reuse so cold-start penalty stops hitting the user. More engineering work, but preserves shared-database integrity.

Once Max answers, implement the chosen path and verify with repeated timed reel-open tests.

---

## OPEN QUESTIONS (awaiting Max)

- Is the D1 cloud database being shared across multiple machines or cloud workers right now? Or is this Pine machine the only writer/reader?
- Can the storyboard safely run off a local SQLite copy, or must it stay synced with the cloud D1 instance?

---

## KEY PATHS, FILES, AND IDS

| What | Path / Value |
|---|---|
| Storyboard editor (UI) | `C:\moma\sc10\sound_assembly\code\storyboard_editor_v3.html` |
| Slideshow server | `C:\moma\sc10\sound_assembly\code\slideshow_server_v01.py` (port 8790) |
| Combo runner (reel-open API) | `C:\moma\sc10\combo_runner\code\` (port 8779) |
| DB layer (mode config) | `moma_db.py` (in combo_runner/code) |
| DB mode line | `mode = d1` - this is the one-line change target |
| Thumbnail endpoint returns full video | `/thumb_by_job/<job_id>` ? 7.4MB, not a real thumbnail |
| Test job ID used | 3118 |

---

## GOTCHAS

- **The `/thumb_by_job` endpoint is a bandwidth bomb.** It serves the full video (7.4MB) when it should serve a small thumbnail. This makes the storyboard's initial grid load heavy. It is a separate, smaller issue from the 10s reel-click delay, but should be addressed afterward.
- **The one-line fix (`mode = d1` ? `mode = sqlite`) is trivial but has data-consistency implications.** Do not flip it unilaterally - Max must confirm whether cloud sharing is in play.
- **The D1 cold start is a Cloudflare platform behavior, not a code bug.** The worker goes idle and the next invocation pays a 4-5s wake-up tax. Keep-warm strategies (a ping every 30-60s) are the standard mitigation if cloud must stay.
