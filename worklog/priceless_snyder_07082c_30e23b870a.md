
## [2026-07-26 14:20] ? 4f3f6a59
- DID: Telepathy Lesson 1: verified real lipsync cost from MoMA api_expenses ledger (255 jobs, $63.15, = $0.025/sec = $1.50/min, NOT the $0.25/5s the code comment claims). Renamed Notion Training Tape -> Lesson. Cut opening into 10 pilot spots (~12s each, ~2 min, ~$3-4).
- STATE: Beat list written to scratchpad lesson1_beats_v01.txt. Researching exact Nadali MoMA commands (sass Fish Audio recipe + fire_job lipsie wan26flau fields).
- NEXT: Run Anna audio for the 10 spots, measure durations, PRESENT the audio clips to Max, then fire lipsie jobs through MoMA after he approves. Everything through MoMA, no shortcuts.

## [2026-07-26 14:52] ? 4f3f6a59
- DID: Telepathy Lesson 1: fired and rendered all 10 Anna narration lipsie reels through the standard MoMA lane (jobs 3403-3412, wan26flau, arrangement 42). Found and fixed a real audio_resolver bug: a named project tag ending in a digit (lesson1) was misread as film scene 1, killing every reel. Renamed scene 11 from 'Tape 1Select' to 'lesson1'. Corrected a wrong lipsync cost comment. Committed + pushed as e480e83.
- STATE: All 10 reels DONE and saved to output_lipsies as lesson1_lipsie_v34xx_wan26flau.mp4. Actual cost 2.175 dollars from MoMA's own api_expenses ledger, inside Max's 4 dollar pilot ceiling. Audio stage was already approved by Max.
- NEXT: Present the 10 reels to Max for review. Then surface four open items: the duplicate 'Telepathy Training Tape Outline' Notion page (branching risk), scene 10 / arrangement 41 still named 'Tape 1', whose voice speaks the first-person parts 2 and 3 of the script, and the 'as this tape ends' wording that should now say lesson.
- LESSON: audio_resolver._scene_num used a loose digit search, so ANY named project tag containing a number was silently treated as a numbered film scene. Fixed to full-match. Watch for the same loose-regex class of bug elsewhere in MoMA's tag handling.

## [2026-07-26 21:23] ? 4f3f6a59
- DID: Put lesson1 spots 11-34 on MoMA spine as 'held' lipsie jobs (3417-3440); rebuilt 34-spot audio run; committed+pushed moma d1e0ce5. Named projects live on spine as lipsie jobs only (nadali has 0 script_lines); do NOT write script_lines under integer scene 11 = movie Scene 11.
- STATE: Max says the STORYBOARD (localhost:8790 slideshow_server_v01.py) is BROKEN for lesson1. Root cause: that server only serves NUMBERED movie scenes - ?scene= takes an integer rank and queries script_lines WHERE scene=int + jobs scene_id LIKE 'scNN%'. It has NO path for named projects (scene_id='lesson1'/'nadali'), so lesson1 does not display. Reels ARE rendered (output_lipsies/lesson1_lipsie_v3403..3412). NOT a data problem - a viewer problem.
- NEXT: Fix slideshow_server_v01.py (C:/moma/sc10/sound_assembly/code) to serve named-project scenes: accept ?scene=lesson1 (string), and for a named tag build the spot list from jobs WHERE scene_id=tag AND job_type='lipsie' (order by label/spot number), text from vocal_line, video from output_file in OUTPUT_LIPSIES, audio from lines_20260726/manifest.json. Check how nadali was ever viewed - there may already be a named-project viewer/port. Do NOT raw-ffmpeg assemble - Max explicitly rejected that twice; he wants the storyboard itself fixed.
- LESSON: Max means the storyboard VIEWER when he says storyboard, not a stitched file. Named projects need viewer support, not workarounds.

## [2026-07-26 21:24] ? 4f3f6a59
- DID: SYMPTOM REFINED
- STATE: Max: reels DO show in the storyboard but clicking PLAY does nothing for lesson1 reels. So the tiles render but the video play-back URL/handler is broken for named-project (lesson1) reels - the server likely serves the reel mp4 from a numbered-scene path and can't resolve output_file for scene_id='lesson1'.
- NEXT: In slideshow_server_v01.py find the play/video endpoint (how a tile's job_id maps to its mp4 URL). Reels are at OUTPUT_LIPSIES/lesson1_lipsie_v{id}_wan26flau.mp4. Make the play handler resolve output_file from OUTPUT_LIPSIES for named scenes. Test by clicking play on spot01.

## [2026-07-29 22:04] ? 408953dc
- DID: H06 processed all 53 of Max's reel review comments: built review_feedback subsystem in the prompter fork (ledger JSON + 18 consolidated rules + regenerable SQLite + method doc), wired 9 live rules into prompter.py as a LEARNED CONSTRAINTS block, removed zoom_out.png from the stills pool (R1), added ANTI_LOOP_LINE (R2). Fixed comment_extraction.py crashing on Russian comments.
- STATE: Fork commit 1b4539d pushed on branch prompter; master 9e66833 pushed. Dry-run verified across 9 spots: header intact, anti-loop present, no palm-up, no eye/eyebrow touch, no zoom-out, nothing fired, zero spend. 46 comment events marked processed by H06; 7 cross-lane (input-curation/render-drift) left fresh for their owner.
- NEXT: Awaiting Max on the 3 proposed new gestures (sphere/half-sphere, wide-spread twice-max, one-hand surrounding-condition) before wiring them; continue prompt development and process the next comment batch as it arrives.

## [2026-07-29 23:02] ? 408953dc
- DID: H06 delivered review_feedback subsystem (53 comments -> DB + 9 live rules wired into forked prompter, commit 1b4539d) and handed cross-cutting findings to H07 (9c3a17f). Verified my branch is NOT exposed to H07's eye-zone substring bug: _BODY_PART_WORDS excludes 'eye', gate matches MOTION not meaning, one_hand_present_look survives. comment_extraction Russian-crash fix on master 9e66833.
- STATE: Two prompter forks now exist: mine (prompter) + H07's (prompter2, newer 118-gesture system w/ automated loop). H07 REPORTS Max gave them overnight priority on comments + the newer system + wants my work folded into theirs via summaries -- but I have NOT heard this from Max directly. Cooperating fully, competing on nothing, firing nothing.
- NEXT: Ask Max ONE open question: keep developing on my prompter branch, or fold into prompter2 and switch to independent verifier of H07's outputs. Recommend the latter (non-duplicative, matches supervisor/verifier rule) IF he confirms H07 owns comments+newer system.

## [2026-07-30 09:05] ? 408953dc
- DID: H06 diagnosed the storyboard pin/second-spine disaster read-only (Codex owns fix). Wrote durable diagnostic C:/moma/sc10/sound_assembly/code/storyboard_pin_bug_diagnostic_H06_v01_tomemex.md (commit 0acaa71), posted board lead. Self-audit: my session never touched slideshow_server_v01.py or storyboard_editor_v4.html; my earlier duplicate reels aggravate but don't cause it.
- STATE: KEY FINDING: storyboard_spot_order_history ALREADY logs before/after+timestamp per reorder -> Max's lost pins likely RECOVERABLE. Trouble2=load sort L992 keys x['order'] None->0, likely ignores persisted storyboard_spot_order.position. Trouble1=_apply_spot_order DELETE+partial re-INSERT drops reels. Trouble3 ~80% exists.
- NEXT: Recovery-first: dump history table, restore last human after_json before auto-sort clobber. Coordinate w/ Codex; do NOT edit the storyboard code (collision). Await Max on prompter-vs-prompter2 ownership + whether to help recover.
