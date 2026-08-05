# Scribe handover - milestone 4 (~300K tokens)
# session: 20260728_gifted_dhawan_44d94e_dde74d7f
# cwd: C:\claude_base\.claude\worktrees\gifted-dhawan-44d94e
# written: 2026-07-28 10:33:21 by deepseek-v4-pro

GOAL (Max's own words, verbatim)
> "Okay, so drifting happens because of LLM. You just forget. So you need to create a fixed part of the prompt and script it... How can you prevent idiotic LLM from drifting from a developed prompt?"  
> "In any way, redo the two finger one. ... I prohibit you from stopping when you got a clear order. Go ahead and implement. Work safely and autonomously, ignore the compaction. I expect you to fix the semantics, fix the database, and produce the next five reels, the ones which are available. Go ahead, work autonomously. See you in a long. of time."

Also standing: produce all 112 spots of Telepathy Lesson 1 through the full MoMA pipeline, no shortcuts. Budget ceiling was $4 for the first piece; now the whole lesson is much larger, cost per reel is ~$0.25 (from the actual api_expenses ledger). Max reviews each batch and may junk reels; only fill junk gaps, never re-render approved or held?good reels.

DECISIONS MADE AND WHY
- Prompt is split into a locked permanent block and a variable gesture body. The permanent part (candlelight, "completely alone, no other people appear," forward gaze, gentle push?in) NEVER changes; a drift?guard in the render worker rejects any reel whose prompt is missing any mandatory clause. This stops the LLM from silently swapping candlelight for lamplight or dropping the "no other people" sentence.
- The gesture system was rebuilt from a keyword?table picker (which produced a victory sign on a death line) to a semantic meaning?annotated catalog. Each gesture now carries a meaning label (e.g. prayer?palms?45? = mortality/reverence; open?palm = offering/receiving). Reel gestures are assigned by reading the sentence and choosing the gesture whose meaning fits - no keyword triggers. This fixes the two-finger / dying mistake and eliminates random "broad" or looping gestures.
- `table_low.png` is banned permanently as a source image (it shortens Anna). It was junked in MoMA and excised from all future fire scripts.
- The render worker (`combo_wan26au_worker.py`) was hardened: a shared no?overwrite guard archives old renders before writing a new one; the prompt?lock guard aborts a job before spending money if mandatory clauses are missing; and a post?render step auto?sets the storyboard spine pick (only for empty spots, never clobbers an approved pick).
- Reels are now fired through the sanctioned `fire_job()` path (the database now blocks raw UPDATEs by non?authorised programs), and an empty storyboard spot auto?seeds the first non?junk reel that renders for that spot (via `storyboard_spot_order`). No manual spine?poking needed.
- This session (h01) claims spots 67?71 on a shared REEL REGISTRY board so siblings (like H03) don't collide.

CURRENT STATE (what is done, what is in flight)
- 112 total lesson1 spots.
- Spots 1?56: mix of approved, done, junk, and held. Max has been reviewing and junking bad ones directly in the Storyboard. The assistant does NOT alter approved or held?good reels; only junked spots get re?filled.
- Spots 57?66 (10 scripted reels with the per?sentence gesture timelines) were rendered overnight. Max reviewed them in the morning and flagged the dying?line spot (spot62) for a wrong gesture (two?fingers). That spot was immediately re?rendered with the correct prayer?palms?45? gesture and is now done (job 3581). The other nine of that batch are as Max last saw them; he has NOT explicitly approved all of them yet, but he called them "nothing disastrous." He needs to final?review them on the board before we re?fill anything from that range.
- Spots 67?71 (5 semantic reels) have been FIRED with the meaning?chosen gesture catalog. At the last check they were rendering (jobs 3583?3587). They should by now be "done" unless the queue is long; verify with a quick DB query on those job IDs.
- The spot62 re?render (job 3581) and the 5 semantic reels all use the locked candlelight permanent header, and the semantic gesturing for 67?71 is stored in `gesture_assignments_v01.json`.
- Remaining held/placeholder spots: spots 72?111 (~40 spots). These are untouched, all stat held, no video. They are the bulk of remaining work but MUST NOT be fired until Max rules on the sibling standard divergence (see OPEN QUESTION).
- A sibling session H03 is also making reels for Lesson1 but with a different prompt standard (older header, freehand gestures). H03 has paused and is asking which standard to use. That conflict is the critical blocker.
- The render worker is alive, the babysitter script watches it and can relaunch if it dies.

EXACT NEXT STEP (for the cold session)
1. Do NOT fire any more reels (no spots beyond 71) until Max answers the open question about the unified prompt/gesture standard.
2. Confirm the status of the 5 semantic reels (spots 67?71): query jobs 3583?3587. If any are still queued/running, wait for them to finish; if any "error", re?fire that single spot using `fire_lesson1_semantic_v11_h01.py` (which creates a fresh queued row with the same meaning?chosen gesture assignment, candlelight header, table_low banned). All go through the sanctioned `fire_job()` path.
3. Once 67?71 are all done, present them to Max - he hasn't seen them yet. The presentation method that works: serve the Nextcloud output_lipsies folder over HTTP (port 8899) and open `http://127.0.0.1:8899/_lesson1_review.html` in Chrome.
4. Present the open question to Max (below) and wait for his decision before continuing.
5. Keep the worker alive (babysitter). Do not kill the worker; if it needs a code reload, relaunch a fresh hidden process, never quit the running one.

OPEN QUESTION AWAITING MAX
- H03 (a sibling session) is using a different reel prompt standard - the older "lamplight, static camera" header with freehand gesture text. My reels use the locked candlelight + gentle push?in header and the semantic gesture catalog. This creates two different looks in the same lesson, which Max explicitly wants to avoid. H03 has paused and is waiting for Max to decide: do we unify everyone on the candlelight header + semantic catalog (recommended), or some other standard? The answer determines whether H03 can keep their reels or must redo them, and whether we fill the remaining ~40 spots with one consistent look.

KEY PATHS AND IDS
- Lesson1 project tag: `lesson1` ? MoMA scene rank **305**, arrangement_id **42**.
- Source stills folder: `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\telepathy_tapes\tape1select_output\`  
  Valid neutral stills (table_low banned): v2_front, v2_left, v2_right, v2_profile_l, cam_left, cam_right, cam_up, cam_down, table_profile_r, table_high, zoom_in, zoom_out.
- Locked permanent prompt block (candlelight header): stored in `fire_lesson1_semantic_v11_h01.py` `LOCKED_HEADER` and enforced by `prompt_lock.py` + `scene_locks.json`.
- Semantic gesture catalog: `gesture_catalog/gesture_catalog_v02.json` (42 gestures, all annotated with meaning). Picker/composer: `gesture_catalog/gesture_script_v02.py`. Assignment file for spots 67?71: `gesture_catalog/gesture_assignments_v01.json`.
- Fire scripts:  
  `fire_lesson1_semantic_v11_h01.py` - fires via `fire_job()`, uses semantic catalog, replaces held rows with fresh queued rows for uncovered lines.  
  `fire_lesson1_scripted_v10_h01.py` - the previous per?sentence timeline version (used for spots 57?66, now superseded by semantic).
- Render worker: `combo_wan26au_worker.py` (in `sc10/combo_runner/code`). PID file: `local_state/wan26au_worker_pid.txt`. State file: `wan26au_worker_state.json`. Log: `.../combo_runner/data/wan26au_worker.log`.  
- Storyboard display: served by `sc10/sound_assembly/code/slideshow_server_v01.py`; pages `storyboard_editor_v2.html` / `_v3.html`. Placement table: `storyboard_spot_order(scene=305, spot_key=manifest_idx, position=1, job_id=<lid>)`. Empty spots auto?seed the first non?junk reel for that spot.
- Expense ledger: `api_expenses` table (inside the D1 database, querable via `moma_db.connect_db()`).
- Reel output folder: `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\scenes\scene10_images\combo_runner\data\output_lipsies\`  
  Archive subfolder there holds overwrite?guarded old versions.
- Handover / work log file: `C:\claude_base\compaction_kb\scripts\worklog.py log "..."` (records durable state for any session).
- Bulletin board for sibling coordination: `python C:/claude_base/branch_bulletin/bcast.py dm <name> "..."` and `post --announce`.

GOTCHAS / DEAD ENDS TO AVOID
- **NEVER change the lighting.** The locked header = "warm candlelight." Any substitution ("lamplight", "flickering candlelight") ages Anna and sharpens the background; the drift?guard will abort, but do not even try.
- **Never zoom out** (pull back camera) - it makes the model invent extra people. Only gentle push?in or hold allowed.
- **Never put "Anna" or any proper name in the prompt** - it gets stamped as on?screen text.
- **Held ? approved.** Held = a placeholder job with NO video yet. When filling gaps, target lines that have NO approved/done reel, not just any held job. Do not re?render approved or held?good reels.
- **Storyboard placement uses `storyboard_spot_order`, not `line_current_clip`.** A new reel lands on the board when the spot is empty (no existing row in that table). If a stale row points at an old junk reel, the new reel won't appear - delete that stale row and let auto?seed replace it.
- **Never kill the render worker to reload code.** The worker is a singleton; stopping it leaves queued jobs stuck. Instead, launch a fresh hidden process (`pythonw.exe combo_wan26au_worker.py`, workdir `C:\moma\sc10\combo_runner\code`, hidden) and let the old one finish - or signal it gracefully via the state file if absolutely necessary.
- **table_low.png is banned** - it shortens Anna. All fire scripts skip it; the job for that still (3393) is junked. There are 8 held reels that originally pointed at table_low; their source_image was already swapped to good stills (held, not rendered yet - safe).
- **Use the sanctioned `fire_job()` call** to create new lipsie rows; the database now blocks raw UPDATEs from non?authorised programs. The fire script `fire_lesson1_semantic_v11_h01.py` is the correct template: it computes the prompt via `gesture_script_v02`, picks a good still, and calls `moma_db.fire_job()` with `job_type='lipsie'`, `scene_id='lesson1'`, `lipsync_tool='wan26flau'`, `arrangement_id=42`, `birth_line_hash=<line hash from manifest>`, `source_image=<full path to still
