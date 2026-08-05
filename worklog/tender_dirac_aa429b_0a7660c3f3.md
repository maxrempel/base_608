
## [2026-06-17 15:33] ? cec4e446
- DID: D21 registered. sc10 arrangement work: merge per-arrangement lines into ONE multiperson lipsie. arr01 = greeting beat, lines 0-3 (ANNA L / ISHTAB R alternating). Built merged 14.75s audio, fired wan26flau lipsie job 2761 from two-shot still sc01_meet_twoshot_var01.png. Started wan26au worker (bg) to render.
- STATE: Job 2761 queued+rendering. Worker bg id bvzpmlwq5. Audio synth hash d21e83574970eb, run lines_20260617_1531_d21arr01. arrangement_id=2 (sc10-arr01).
- NEXT: Poll 2761 to done, present lipsie to Max. Then arr02 = next beat (lines 4-9?), same merge approach.

## [2026-06-17 15:45] ? cec4e446
- DID: D21 arr01 v2: fired two prompt variants of the 4-line merged greeting lipsie (same audio synth d21e83574970eb, same two-shot still). 2762=minimal (warm+smiles), 2763=expanded (every spoken phrase written in, attributed L/R, to fix random nods). Both rendered done.
- STATE: MOMA up (8779). Jobs 2761(v1),2762(min),2763(exp) all done in arrangement_id=2. Awaiting Max pick between min vs exp.
- NEXT: On Max pick, lock the winning prompt style, then fire arr02 (lines 4-9) same merge approach.

## [2026-06-17 16:05] ? cec4e446
- DID: D21 arr01 nod-fight: smiles cause laughter, listener bobs like penguins. Dropped smiles. Fired 4 new: 2765 statue (listener-frozen), 2766 locked-off, 2767 bracketA (past+future dialogue as prompt text), 2768 bracketB. Same audio/still/model. Noted: 4-line=15s cap is why audio can't be padded; bracket lines went into prompt text instead.
- STATE: All of 2761-2768 done in arrangement_id=2. wan26flau, flash model (same as working sc09). Awaiting Max pick of which kills the nods.
- NEXT: Lock winner, then arr02 lines 4-9. If prompts can't kill listener-nod, fall back to shorter 2-line merges (proven sc09 win was 2-line).

## [2026-06-17 18:13] ? cec4e446
- DID: D21 arr01: Max requires every prompt to INCLUDE the actual lines, labeled Left/Right, minimal, no boilerplate. Fired 2769 (left/right + lines) and 2770 (same but lines in quotation marks). Same 4-line merged audio (synth d21e83574970eb), Anna-left two-shot still 933, wan26flau.
- STATE: 2769,2770 done in arrangement_id=2. Prior 2761-2768 are earlier variants (smiles/stillness/bracket) Max rejected. Pairs script _d21_pairs.py prepped but NOT fired (2-line split fallback).
- NEXT: Get Max read on minimal-quoted 2770. If still wrong speakers/nods, try 2-line split (_d21_pairs.py).

## [2026-06-17 18:40] ? cec4e446
- DID: D21 arr01 approved (job 2774, formal-officials template). Then fired arr02/03/04 as chunked merged lipsies (<=15s each) with same template. Beat map from prior production: arr02=lines4-9, arr03=10-21, arr04=22-29. Split: arr02=[4,5][6,7][8][9]=2775-2778; arr03=[10-16][17-21]=2779-2780; arr04=[22][23][24-28][29]=2781-2784. Anna=Left(even idx), Ishtab=Right(odd). Fixed audio_resolver verify bug (needed dummy vocal_line).
- STATE: All 10 rendering in detached wan26au worker. Template prompt: formal officials, profile, eyes on each other, lines quoted Left/Right, minimal nods/grins. Saved 2 feedback memories (no verbatim refires; no blocking polls).
- NEXT: Watch 2775-2784 complete; Max reviews per arrangement. arr05 (lines 30-32) still to do. Scratch scripts _d21_*.py in code dir (uncommitted).

## [2026-06-17 20:44] ? cec4e446
- DID: D21 path fix: scene already assembled along a path (per-line picks). Locations: hall(0-9), corridor/window(11-23), alcove(24-27), door(28-32). arr02 (4-9) kept on greeting/hall still (2775-2778, location-correct). Junked wrong static arr03/04 (2779-2784). Refired arr03 on WINDOW two-shot sc05 (Ishtab-L/Anna-R, Earth drifting) = 2785-2786; arr04 on CORRIDOR-WALK two-shot B1 (Anna-L/Ishtab-R, walking) = 2787-2790. wan26flau.
- STATE: 2785-2790 rendering detached. Still no clean two-shot for alcove/door; arr04 placed on corridor-walk as best moving still. arr05 (30-32) not done.
- NEXT: Max reviews arr02/03/04. May need a doorway two-shot for the final beat. Walking-lipsie quality unproven.

## [2026-06-17 21:28] ? cec4e446
- DID: D21 FULL rearrangement fired: sc10 as ~4-line merged multiline lipsies, location-respecting, traced each chunk to source stills. KEY: when merging, each line's lipsie traces to its still; choose per chunk. For alcove/door (no standalone two-shot) extracted mid-frames from existing approved spine lipsies (all clean Anna-L/Ishtab-R two-shots) -> copied to OUTPUT_STILLS as d21_*_twoshot.png. Stills: hall=sc01_meet_twoshot(4-9), window=sc05_window_twoshot(10-23), alcove=frame(24-27), room=frame(28-32).
- STATE: Coverage all 33 lines: 0-3=2774(approved); 4-9=2775-2778; 10-21=2785,2786; 22=2791;23=2792; 24-27=2793; 28-29=2794; 30-32=2795. wan26flau, ANNA=Left except window(sc05)=ISHTAB-Left. Junked off-plan 2779-2784,2787-2790. 5mt timer armed.
- NEXT: On wake: check 2791-2795 renders done, present full scene per location, get Max read.

## [2026-06-17 21:35] ? cec4e446
- DID: D21 COMPLETE: sc10 fully rebuilt as ~4-line merged multiline lipsies, all 12 chunks rendered done. Alcove/door frame-extract worked (frames pulled from approved spine lipsies, all Anna-L/Ishtab-R). Full scene order: 2774,2775,2776,2777,2778,2785,2786,2791,2792,2793,2794,2795.
- STATE: All done in D1. Awaiting Max review. Scratch scripts _d21_*.py uncommitted in code dir. Timer loop ended (work complete).
- NEXT: Max reviews full scene; junk/approve per chunk; fix any with wrong nods/speakers; then assemble into spine. arr05 closing line 32 included in 2795.

## [2026-06-17 23:14] ? cec4e446
- DID: D21 sc10 settled into 11 arrangements (one merged lipsie each), all 33 lines, no overlaps. arr04(line8,14s) and arr08(line23,13s) are FORCED singles (each fills the 15s wan2.6 cap alone) - Max understood/accepted. Live jobs: arr01=2774(appr),arr02=2775,arr03=2776,arr04=2777,arr05=2778,arr06=2785,arr07=2797(17-22 merged),arr08=2792,arr09=2796(describe-both-first),arr10=2794,arr11=2795. describe-both-first prompt fixes speaker-swap (state names+positions before lines).
- STATE: OPEN: arr10(2794) & arr11(2795) share same door bg (both door_pan_left frame) - Max flagged wrong; proposed refiring arr11 on door_pan_right frame(685) for distinct bg, not yet done. Stills: hall=sc01, window=sc05, alcove/door=frames from approved spine lipsies.
- NEXT: Fix arr11 distinct bg; consider rolling describe-both-first across all; then assemble spine. Scratch _d21_*.py uncommitted.

## [2026-06-17 23:29] ? cec4e446
- DID: D21 FINAL redo fired (2802-2808) with consolidated recipe: walking corridor B1 for hall beats 6-9, window sc05 for 10-23, alcove frame for 24-27. describe-both-first + profile/eyes-on-each-other/never-camera + only-speaker-moves + monologue=one-speaker + NO smile/grin words + composed-throughout (kills end-smile) + auto silence pads (sb auto-fit to 15s cap). Max approved+kept: 2774(arr01),2775(4-5),2777(8 standing),2778(9 standing),2794(28-29),2795(30-32). Junked superseded tests 2796,2797,2799,2800,2801. Note: 2803/2804 are WALKING versions of 8/9 (Max approved standing 2777/2778 but asked for walking).
- STATE: 2802 rendering rest queued, worker alive. Max asleep; verifying all land then sleeping. Lessons saved: no grin/smile words, describe-both-first, variation-not-verbatim, dont-block-poll.
- NEXT: On wake verify 2802-2808 done; if any error refire. Then full approved scene = 2774,2775,(2802),(2803/2777),(2804/2778),2805,2806,2807,2808,2794,2795. Max picks walking vs standing for 8/9.

## [2026-06-17 23:35] ? cec4e446
- DID: D21 night: 2802 (walk 6-7) Max verdict 'good walk but WRONG SPEAKER ASSIGNMENT' -> describe-both-first does NOT fully fix speaker swap; wan2.6 likely assigns mouths by audio timing not L/R labels. OPEN PROBLEM for morning. 2803 done, 2804 running, 2805-2808 queued (same recipe, may share speaker issue). Walking + no-smile + composed recipe otherwise good per Max.
- STATE: Merged lipsies use synthetic line_hashes so they DON'T show under moma per-line arrangement view (some arrangements look empty) - Max says propagation 'not sure needed', leaving it. Max asleep.
- NEXT: MORNING: solve speaker-assignment (wan ignores L/R labels in merged clips) - maybe order-of-mention, or fewer speakers per clip, or accept 2-line max. Then re-roll. Verify 2804-2808 landed.

## [2026-06-17 23:59] ? cec4e446
- DID: D21 COMPLETE: sc10 fully rebuilt as 11 merged multiline lipsies, ALL approved. Final map: arr01=2774(0-3),arr02=2775(4-5),arr03=2810(6-7),arr04=2812(8),arr05=2811(9),arr06=2805(10-16),arr07=2806(17-22),arr08=2807(23),arr09=2808(24-27),arr10=2794(28-29),arr11=2795(30-32). Recipe that worked: describe-both-first + speak-ORDER (left speaks first then right) fixes speaker swap; walking corridor B1 for hall beats 6-9 with NEUTRAL hand phrasing (frozen AND robotic both came from over-directing arms); window sc05 for 10-23; alcove/door frames from spine lipsies; NO smile/grin words; composed throughout; auto silence pads to 15s cap.
- STATE: All approved except 2812 just rendered (proven recipe, awaiting Max morning nod). Merged lipsies use synthetic line_hashes so DON'T show in moma per-line arrangement view - Max said propagation 'not sure needed', left undone. Scratch _d21_*.py uncommitted in code dir.
- NEXT: MORNING: Max nods 2812; optionally wire merged lipsies into arrangement spine if he wants them visible in moma UI. Scene otherwise done.

## [2026-06-18 08:02] ? cec4e446
- DID: D21 sc10 COMPLETE + APPROVED: all 11 merged-multiline arrangements approved by Max. 2774(0-3),2775(4-5),2810(6-7 excellent),2812(8 perfect),2811(9 great),2805(10-16),2806(17-22),2807(23 good),2808(24-27 good),2794(28-29),2795(30-32). I mistakenly reset all to 'done' (thought auto-approve bug) - was Max's real approvals, RESTORED to approved. Worker only writes 'done'; my scripts never write approved (only-Max-approves intact).
- STATE: Scene done. PUNCH-LIST for next round (Max said HOLD): (1) DISTINCT still per lipsie - every beat different starting image, walk=different corridor parts (saved as feedback_distinct_still_per_lipsie). (2) arr11/2795: turn toward room behind them + better portrait/canon adherence + faces to back. (3) arr07/2806: Anna more relaxed/analytical/warm. (4) minor: 2775 last-half-sec smile, 2805 artistic.
- NEXT: Next round: rebuild with distinct per-beat stills (pull each line's own spine still or distinct clip frames) + the per-clip notes. Recipe locked: describe-both-first+speak-order, no smile words, walking neutral hands, window=at window, pads, 15s cap.

## [2026-06-19 14:39] D21 cec4e446
- DID: D21 sc10 bg-distinctness + hands: KEY INSIGHT - bent/frozen hands come from the SOURCE STILL's hand pose (wan freezes it), not the prompt; neutral wording already correct. Fix = use full-quality character source stills with relaxed hands (NOT frame extraction = quality loss). Fired 2833 (arr03 6-7 on sc_walk2_B) + 2834 (arr04 8 on B1_885), keyed to CANONICAL merge ids (mda9e627562064, m5abb6078c06d6) by building merged audio into a manifest keyed to the canon id -> resolves audio AND groups in spine -> auto-promote on approval, old->2nd spine.
- STATE: Good full-quality walking two-shots: 885 B1, sc_walk2_A(J483,arr02=2828), sc_walk2_B. arr05(line9) SHORT a 4th distinct corridor walking still. sc10_07_corridor_walk_wide=backs-turned unusable. All 11 arrs otherwise have distinct-bg candidates.
- NEXT: Get arr05 4th still (Max places or I generate); then refire arr05 same canonical-id method. Review 2833/2834. Recipe locked: full-quality still + neutral hands + speak-order + no smile.

## [2026-06-19 17:39] D21 cec4e446
- DID: D21 spine auto-land FIXED + shipped. Root cause: merged reels weren't pinning their member lines in line_current_clip (the storyboard state.assigned source), so they orphaned. FIX pushed 21562f7: fire_merge_lipsie now upserts line_current_clip for every member line at fire time (API-enforced, fool-proof, fail-open). D30recoder ran one-shot repair (34 pins/12 beats) from my membership map (local_state/d21_merge_membership_20260619_172144.json). D26 auto-promote=belt-only. Max: 'Terrific, thank you.'
- STATE: All sc10 reels healed in spine. D30 contract: prefer POST 8790/api/storyboard/assign {line_hash,job_id,pinned:1} over direct SQL (equivalent table; switch if demotion semantics needed). My SQL sets spine_pinned=0 (auto, not manual-pin).
- NEXT: Resume sc10 reel production: arr05 still needs a 4th distinct corridor walking still (Max places or I generate). Going forward route merged fires through fire_merge_lipsie (needs merges.json) OR replicate the pin. Recipe locked: full-quality still + neutral hands + speak-order + no smile + walking-already.

## [2026-06-19 18:50] D21 cec4e446
- DID: D21 sc10 reels + spine restore coordination. Made NEW per-spot reels from Max's placed images: L4-5=2835(c483), L6-7=2836(sc_walk_extrap3_05), L23=2837(sc_walk2_orig_B), L30-31=2838(sc_door_pan_right_B), L28-29=2839(fix_alcove_B). All fired keyed to first-member line_hash + pinned via line_current_clip. ISSUE: D30's repair/canonicalization REWRITES jobs.line_hash of fresh reels to a member's single hash (2838 line_hash->L31 'Indeed' though audio=merged 30-31, birth=L30 intact) - flagged D30 to stop. ISSUE2: D31's v2.28 membership filter HIDES reels lacking a registered membership entry -> my 5 newest went invisible ('lost'). Posted full current spine to D30/D31 to register+pin.
- STATE: CURRENT INTENDED SPINE: 0-3=2774,4-5=2835,6-7=2836,8=2812,9=2815,10-16=2829,17-22=2817,23=2837,24-27=2808,28-29=2839,30-31=2838,32=2795(needs own reel later). Reels pin via line_current_clip; D30/D31 own membership store+filter. fire_merge_lipsie now auto-pins (pushed 21562f7) but my manual fires bypass it (no merges.json). Context ~89%, near refresh.
- NEXT: Confirm D30/D31 registered the 5 new reels' membership + spine shows whole. L32 needs its own reel (split from 30-32). Going forward: register membership for each manual reel OR route via fire_merge_lipsie. Recipe: full-quality placed still + neutral hands + speak-order + no smile.

## [2026-06-23 14:50] D21 cec4e446
- DID: DIRECTIVE CHANGE (Max via D24fixer 2026-06-23): NO MANUAL PINS - PROHIBITED. Spine must AUTO-MATCH: a reel fills a spot ONLY if the reel's member lines EXACTLY equal the spot's lines (whole text, no deviation), derived from sass merges.json. My whole line_current_clip pin approach is now WRONG and must be undone. Max wants D21 to ship the auto-derive membership from D1/sass merges.json and drive spot-fill end-to-end via auto-match (not pins).
- STATE: PLAN for auto-match: (1) sass must produce merges.json for sc10's current [[MERGE]] spot structure (D30 said missing). (2) Reels MUST be fired via fire_merge_lipsie with birth_line_hash = the spot's merge_hash (canonical). (3) Storyboard matches reel.birth_line_hash==spot.merge_hash exact, newest wins, NO pins. (4) My manual reels 2835/2836/2837/2839/2846 used non-canonical hashes -> re-fire via fire_merge_lipsie once sc10 merges.json exists. Owners: D21 fire side, D30/D26 storyboard match side, D1/sass merges.json.
- NEXT: FRESH D21 WINDOW should drive this (this session 93% ctx). Re-register bcast whoami D21, read this log, coordinate w/ D30/D31/D26. Current reels all rendered+correct audio; only the SHOWING (auto-match) needs the merge_hash keying. Undo stray pins per Max.
