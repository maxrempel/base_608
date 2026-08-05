
## [2026-06-11 13:51] D16 923c6302
- DID: Built Retroactivity layer-1 assembly manifest in render_mixboard_video_v01.py (v07): on every render writes <out>.manifest.json freezing per-clip lineage (job_id, media_file, prompt_id, rating, birth_line_hash, audio, segment timing, encode params, git commit). Joined branch team as D16.
- STATE: Committed+pushed to branch claude/admiring-mahavira-6f8fc6 (0b4ba1d), NOT master - awaiting D4 merge window per team safety rule. Syntax+unit test green; no live render yet. Render file is a hot shared file (D12/D13/D15 area).
- NEXT: Wait for D4 ok to merge to master. Then optional: live-render verify, then layers 2 (episode lockbox) + 3 (swap-not-rerun) + trims/flips recording per memo addendum - all NOT started, need Max's go.

## [2026-06-11 16:00] D16 923c6302
- DID: Layer-1 assembly manifest DONE+on master (render_mixboard_video_v01.py v07, commit 0b4ba1d, live-render verified scene9). But it only captures job_id POINTERS, not the recipe - prompt_id=None on lipsies. Max wants FULL retroactivity per clip, not imitation. Building it now.
- STATE: render v07 on master writes <out>.manifest.json per render. Need to UPGRADE write_assembly_manifest to inline the FULL frozen recipe per clip by walking ancestry lipsie->source still->prompt. Servers 8779+8790 are UP. Scene9=12 lines run lines_20260603_1709_mergeexp. Worktree has moma_data_root.txt copied in (gitignored).
- NEXT: 1) Inspect a real lipsie job row (id 2720) ALL columns via D1Client to find link lipsie->source still + where prompt/mood-codes/params/ref-images are stored. 2) Inspect that still row for prompt_id->prompts table (text+mood+params). 3) Write recipe-resolver: job_id -> frozen full recipe (prompt verbatim, mood codes, params, ref image paths, audio). 4) Inline under manifest clip 'recipe' key. 5) Re-render scene9 verify. 6) Flip+trim are recorded NOWHERE = separate gap, flag it, cannot freeze what isnt stored. Use moma_db.D1Client. Do NOT ask Max permission - he authorized full build.

## [2026-06-11 16:02] D16 923c6302
- DID: SCHEMA SOLVED for full-recipe capture. Recipe is stored INLINE on jobs rows (prompt_id UNUSED/None). Chain: lipsie.source_job_id -> still(job_type=image).source_job_id=None(root). Also source_clip_id for clip ancestry.
- STATE: Confirmed via jobs 2720(lipsie)->2501(still). KEY COLUMNS to freeze per ancestry node: input_prompt+output_prompt (verbatim prompt w/ mood codes), plate_recipe (JSON w/ ref_paths = the exact reference images!), engine, engine_params, lipsync_tool, lipsync_params, clip_maker, vocal_line, notes (motion/wan prompt), source_image, input_file, output_file, audio_start, audio_end (audio trim pts!), lipsy_mask_side/x1/x2, frame_speakers, rating, label, batch_id, line_hash, birth_line_hash, source_job_id, source_clip_id, created_at, updated_at. NOTE: horizontal FLIP still has no column = remains unrecorded gap.
- NEXT: BUILD now in render_mixboard_video_v01.py: (1) add resolve_recipe(d1,job_id,cache) that walks source_job_id/source_clip_id up to depth 8, querying FULL row via moma_db.D1Client.query_sql('SELECT * FROM jobs WHERE id=?') per node (cache by id), parse plate_recipe JSON, freeze RECIPE_FIELDS list above. (2) in write_assembly_manifest add per-clip clip['recipe']={'resolved':bool,'ancestry':[nodes clip->root]}, wrapped per-clip try/except. (3) construct D1Client in main, pass in; if D1 down skip recipe gracefully. (4) bump VERSION v08. (5) re-render scene9, verify recipe.ancestry has input_prompt+plate_recipe.ref_paths. (6) commit+push master (Max waived gate, team asleep). render file imports moma_db OK (combo_runner/code on sys.path via paths hack line 51).

## [2026-06-11 16:50] D16 923c6302
- DID: ar1bkp DONE (lockbox arr1_scene9 79MB clips+mp4+manifest on GDrive). Going autonomous on: (2) trimtrack design, (3) on-demand backup package tool extracting components+db+inputs+prompts
- STATE: v08 recipe-in-manifest + episode_lockbox_v01 both merged to master. arr1 safe.
- NEXT: build arr_package_v01.py (task3), write trimtrack design memo (task2); only touch own files, NOT shared UI

## [2026-06-11 17:01] D16 923c6302
- DID: Housekeeping: documented 3 retroactivity tools in moma_system_map + moma_storage_map (bumped versions), wrote READMEs into G drive episode_lockbox & arr_packages, merged+pushed master f138ea8.
- STATE: All 3 Max tasks DONE+pushed: ar1bkp=episode_lockbox_v01 (arr1 frozen 79MB), arr_package_v01 (107MB), trimtrack design memo. Memos discoverable. Master synced.
- NEXT: Await Max: report 3 done; trimtrack impl held for go-ahead + clear combo_gui/mixboard window. Timer armed.

## [2026-06-11 17:33] D16 923c6302
- DID: Built trimtrack Phase-1 (capture): clip_edits table + record_flip/record_trim in moma_db.py, recorder hooks + /api/jobs flipped/trim_count in combo_gui.py, FLIP/TRIM badge in mixboard.html. Merged+pushed master 2ebe9db. Corrected stale design memo.
- STATE: All 3 named tasks (ar1bkp, trimtrack, on-demand package) done+pushed. trimtrack Phase-1 capture LIVE-tested on D1. Phase-2 (non-destructive render) NOT started.
- NEXT: Phase-2 needs Max's explicit OK (asked him; it touches the render engine = real fork, not autonomous-safe). Hold until he answers.

## [2026-06-12 08:14] D16 923c6302
- DID: Design settled: Max wants flips/trims baked clip-by-clip immediately (current behavior) + the new clip_edits data record. Phase-2 non-destructive-render SCRAPPED (wrong for his workflow).
- STATE: trimtrack final = capture-only, correct as built. All 3 tasks done+pushed master 260c494.
- NEXT: Now doing end-to-end QC: restore arr1 from backup into isolated area, verify intact.

## [2026-06-12 08:18] D16 923c6302
- DID: End-to-end QC of arr1 package PASSED. Restored full package to isolated scratch; all 12 media components present+ffprobe-valid (durs match manifest), 10 external refs all present, DB ancestry covers 12/12 clip job_ids, rebuilt-from-components duration 52.0s vs frozen 52.12s (match). Investigated 9 unpackaged image names: 7 intermediate generated stills (regenerable), 1 lipsie source_image (final clip packaged), 1 filename-in-prompt-text. NONE are real missing inputs.
- STATE: arr1 package proven self-sufficient + traceable. All tasks done+pushed. trimtrack capture-only final.
- NEXT: Await Max. Possible future: bundle deepest-ancestor source stills too (minor traceability nicety, not needed for restore).

## [2026-06-17 15:25] D16 923c6302
- DID: Max said 'stop timer, tms, status' - ending autonomous loop, no re-arm.
- STATE: All 3 tasks (ar1bkp, trimtrack, on-demand package) done+pushed master. arr1 end-to-end restore QC PASSED. trimtrack = capture-only final (flips/trims recorded as data + mixboard badge).
- NEXT: Idle/standby. Only open item: optional green Q - bundle deepest source stills into package (not needed for restore). Awaiting Max.
