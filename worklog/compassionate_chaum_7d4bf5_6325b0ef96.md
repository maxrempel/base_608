
## [2026-06-17 23:26] D22 9d438d18
- DID: D22 (branch off D21): fixed lipser UI per Max. runner_core.js lipsie row now shows the actual quoted dialogue lines (parsed from output_prompt) in the prompt cell; comment 1+2 boxes moved into the actions/buttons column. Confirmed working by Max, committed+pushed master 2ebba53.
- STATE: Lipser change live. D21 sc10 merged-lipsie production paused mid-review (orphans/bg-dupes flagged: 2794/2795 same bg, line-8/23 forced singles). Timer off (go sleep).
- NEXT: If resumed: address D21 leftovers (2794 vs 2795 same door bg; describe-both-first rollout to other chunks). Could strip useless lipser columns (clip thumb, clip stars, status col, label) if Max confirms.

## [2026-06-17 23:56] D22 9d438d18
- DID: D22: scene picker done + pushed (0c9715b). arrangement_picker.js now a SCENE selector firing all arr-ids of the scene; runner_core.js filters by the id-list so clipper/lipser/imager show all arrangements of a scene at once. mixboard/storyboard already scene-level (read scene_rank); prompter still single-arr. Confirmed working by Max. Housekeeping: moved 38 _d21_*.py scratch files out of code/ into combo_runner/local_state/d21_scratch/.
- STATE: Lipser line-display + comment-move (2ebba53) and scene picker (0c9715b) both live on master. Code dir clean. Timer off.
- NEXT: If asked: prompter full-scene prompt view needs a server tweak (/api/prompts multi-arr or scene param). D21 sc10 merged-lipsie leftovers still pending Max review (2794/2795 same door bg).

## [2026-06-18 06:44] D22 9d438d18
- DID: D22: fixed lipsie trim-dialog silent-scrub bug in shared_ui/popup.js. _openTrim now sets vid.muted=false; START slider 'input' no longer force-pauses (seeks; keeps playing+audio from that point if playing). Verified lipsie mp4 has aac audio track (cause was muting/pausing, not a silent file). Syntax OK, cache-busted on combo_gui.
- STATE: Edits in shared_ui/popup.js UNCOMMITTED, awaiting Max's browser test on /lipser trim. Prior D22 work (lipser lines 2ebba53, scene picker 0c9715b) already pushed.
- NEXT: On Max confirm: commit+push the trim fix. If he wants drag-to-auto-play even from paused, add vid.play() in the sS input handler.

## [2026-06-18 13:48] D22 9d438d18
- DID: D22: built + shipped batches.py (comments by fire-batch). Added jobs.commented_at (via Cloudflare D1 admin MCP - app API blocks ALTER), stamped on all comment-save endpoints (verified live). batches.py clusters lipsie created_at (180s gap) into batches; CLI 'batches.py comments [N]' + importable. Pushed 4a62ec9 (code), 042bd79 (doc). Documented in batches_method_v01_tomemex.md, referenced in MOMA MEMORY.md (auto-loaded), broadcast to D21 via bcast.
- STATE: All D22 work merged to master: lipser lines (2ebba53), scene picker (0c9715b), trim audio (7fbbefe), batches+commented_at (4a62ec9), doc (042bd79). HARD RULE #1 (push-before-verify) raised to top of MEMORY.md.
- NEXT: Awaiting next task. D21 still firing/reviewing lipsies; it can now self-serve comments via batches.py.

## [2026-06-18 15:44] D24 9d438d18
- DID: D24 owns MERGE-TRACEABILITY + TOTAL-SYNC effort (Max: traceability + complete propagation from any point, no hidden surgery). KEY DISCOVERY: canonical traced merge pipeline ALREADY exists - [[MERGE]] block in script (Notion-sourced) -> sass MERGE pass (merge_<hash>.mp3 + merges.json) -> libup merge (collapse script_lines, snapshot+QC) -> fire_merge_lipsie.py. D21 BYPASSED it with synthetic hashes/throwaway scripts = the hidden surgery. Spec written + pushed master 1bf3156: combo_runner/code/merge_sync_traceability_spec_v01_tomemex.md. Broadcast ownership to d-team.
- STATE: Build order (D24 owns): (1) merge_ops D1 ledger table [op,request,member_line_hashes,merge_hash,gap_s,propagation json], (2) small gap param in sass merge concat (currently 0/tight; target 0.10s; D21 used 0.25-0.35 too big), (3) reverse Notion sync (write [[MERGE]]+arrangement back), (4) junk D21 ad-hoc merge corpses (143 junk+36 error lipsies in sc10). NOTHING built yet beyond spec. Context ~63%.
- NEXT: Start building merge_ops table (pure infra, no collision). Coordinate before editing sass.py/libup.py/fire_merge_lipsie.py (announce file+lines on board). All prior D24 work merged: lipser lines/picker/trim/batches.

## [2026-06-18 15:57] D24 9d438d18
- DID: D24 autonomous build of merge-traceability. SHIPPED: (1) merge_ops D1 ledger table + merge_ops.py helper [start/stamp/finish/recent, propagation stages script_declared->sass_built->libup_collapsed->lipsie_fired->notion_synced] - commit 24a2be6; (2) sass merge gap: MERGE_GAP_S (production.json merge_gap_s, default 0.10) inserts matched-format silence between merged members (was 0/tight) - commit ed8d935; (3) corpse cleanup: junked 36 errored sc10 lipsies (reversible). Spec 1bf3156, team broadcast done.
- STATE: REMAINING: (4) reverse Notion sync (write [[MERGE]]+arrangement blocks back into Notion script) - BIG+RISKY (Notion writes flaky, script hand-curated) - do DRY-RUN first, backup page, verify. 43 orphan sc10 jobs left for review (not auto-junked). Timer armed (autonomous). Context ~67%.
- NEXT: Next wake: build reverse-Notion-sync as read-only dry-run (compute proposed [[MERGE]]/ARRANGEMENT blocks from D1 spine; show diff; gate actual write). Also: wire fire_merge_lipsie/a merge tool to write a merge_ops row so next real merge is traced.

## [2026-06-18 15:59] D24 9d438d18
- DID: D24 autonomous tick: wired fire_merge_lipsie.py to merge_ops ledger (commit 42bd0ff) - every canonical merge fire now traced (op_id param; stamps sass_built+lipsie_fired). DONE so far: merge_ops ledger (24a2be6), sass gap (ed8d935), corpse cleanup (36 errs junked), fire tracing (42bd0ff), spec (1bf3156).
- STATE: REMAINING = reverse Notion sync ONLY - irreversible Notion write, NOT doing unattended (waits for Max's review of a diff). Context ~68-69%.
- NEXT: Next tick: build reverse-Notion-sync as READ-ONLY dry-run (compute proposed [[MERGE]]/ARRANGEMENT blocks from D1 spine, write preview file + diff, NO Notion write). If context too high, stop and hand to Max.

## [2026-06-18 16:56] D24 9d438d18
- DID: D24 HOTFIX: scene-only picker (0c9715b) broke the storyboard (sb filters by arrangement_id; picker forced first-arr). Rewrote arrangement_picker.js DUAL-LEVEL (per scene: 'ALL whole scene' + each arrangement; detail.is_scene flag + ids) + storyboard_editor.html handler (is_scene -> CURRENT_ARR_ID=null whole scene). Restores sb per-arrangement selection, keeps scene-view for clipper/lipser/imager. Pushed fe7860a. node-checked.
- STATE: sb fix live on master. Max must HARD-REFRESH sb (slideshow_server 8790 picker include has no ?v= cache-bust). Merge-traceability still 4/5 (reverse Notion sync pending Max). Autonomous loop ended earlier.
- NEXT: Verify sb works after hard-refresh; then reverse-Notion-sync when Max drives it.

## [2026-06-18 17:50] D24 9d438d18
- DID: D24 storyboard pile saga: filter to show only Anna+Ishtab two-shots. Confirmed ROOT cause of '20 iterations no progress' = BROWSER CACHE (Max: same link two browsers diff pictures; cleared site data=fixed). slideshow_server has no-cache code (D23) but is OLD running code (never restarted) + browsers ignore advisory headers anyway. Reliable fix = versioned URL ?v=mtime like combo_gui (storyboard JS is INLINE so needs extraction to external versioned file). Filter commits: 647761d blacklist (fail-open, 'nearly good'), d75fbba whitelist (fail-CLOSED -> only 1 image left=disaster), REVERTED via aac4809 back to blacklist.
- STATE: BLACKLIST live (aac4809, nearly good). KEY BUG: storyboard IMAGES store name in im.FILENAME not im.output_file -> my filter read output_file (empty for most) -> whitelist hid all. Lanes: D24 owns storyboard_editor.html+pile UI, D22=tag data, D23/D25 player. Context ~86% (near refresh).
- NEXT: Proper fix (if Max wants): point pile filter at im.filename, test vs live /api/approved_images (8790), use whitelist of two-shot tokens, verify count before push. AND extract storyboard inline JS to external ?v=mtime file to kill cache disaster permanently (Max rejected server restart). Don't iterate live - one verified pass.

## [2026-06-18 17:54] D24 9d438d18
- DID: D24 AUTONOMOUS (Max away ~50min, said 'you drive'). STORYBOARD PILE - resolved approach: REMOVED the filename filter (commit 12a2817, e2e verified 0 refs in served page) per Max 'fix tags not stupid filters - they break + confuse future sessions'. Pile = scene-tags + status ONLY now. Clutter cleaned in DATA: D26 (data lane, offered) doing ONE-TIME junk pass on sc10 non-two-shots (keep Anna+Ishtab two-shots, junk interiors/window/corridor/bg/station/extrap/iter/solo). CAVEAT: some bg plates are USED as lipsie source stills - junk only pile presence, backup covers it. Root cause of the whole 2hr saga = BROWSER CACHE (slideshow_server no-cache code exists but server never restarted + browsers ignore advisory headers; reliable fix=versioned ?v=mtime URL like combo_gui, storyboard JS is inline so needs extraction).
- STATE: Lanes: D24=storyboard_editor.html+pile UI, D22=tag data, D23/D25=player/mixboard, D26=data/junk, D21=lipsie production. Timer armed 17:58 autonomous-loop-dynamic. Context ~89% (refresh imminent). Merge-traceability DONE 4/5: merge_ops ledger(24a2be6)+merge_ops.py, sass gap 0.10(ed8d935), fire_merge_lipsie->ledger(42bd0ff), spec(1bf3156). Pending: reverse Notion sync (irreversible, needs Max).
- NEXT: Autonomous NEXT: (1) verify D26 junk landed -> pile shows ONLY two-shots e2e (curl 8790 + count approved sc10 images); (2) if D26 idle, consider doing junk myself WITH backup (keep two-shots, junk rest in arr2-7); (3) do NOT rebuild filters (Max forbade); (4) reverse Notion sync waits for Max. Re-arm timer each wake.

## [2026-06-18 17:58] D24 9d438d18
- DID: D24: RESOLVED storyboard pile design - the elegant fix Max wanted. Shipped role-based pile: getBinImages shows role='shot', hides role='plate' (commit 59a514c, e2e roleOk in served page). NO filename filters (removed earlier 12a2817). Plates stay usable as lipsie source stills, just out of the shot pile. DATA PROBLEM: sc10 mistagged - 90 role='shot', only 4 'plate'; ~70 backgrounds wrongly 'shot'. Delegated RETAG to D26 (data lane, playwright visual tooling): set role='plate' on sc10 bg/interior/single-face, keep 'shot' only on Anna+Ishtab two-shots, backup first.
- STATE: Autonomous, Max back ~50min. Timer armed autonomous-loop-dynamic. Context ~89% (refresh imminent - this worklog is the handover). Pile filter = role only (elegant, future-proof). Awaiting D26 retag.
- NEXT: On wake: verify D26 retag landed -> sc10 pile shows ONLY two-shots (curl 8790 + count role='shot' in arr2-7 should drop ~90->~20). If D26 idle, do retag myself WITH role backup (keep two-shots role='shot', set bg->plate). Then DONE. Reverse Notion sync still pending Max. Do NOT add filename filters.

## [2026-06-18 18:01] D24 9d438d18
- DID: D24 autonomous: DID the conservative role retag myself (D26 idle). sc10 approved images 90 shot -> 31 shot / 63 plate. Retagged 59 unambiguous backgrounds (bg_*/extrap/iter_bg/station/force/composite_bg/strip/_pan_/fix_alcove/earthorbit/sc10_dock) shot->plate. Backup: local_state/d24_scratch/sc10_role_backup_20260618_180040.json (reversible). Pile filter=role='shot' (59a514c) now shows 31 not 90 - bulk clutter gone.
- STATE: REMAINING ~11 ambiguous still role='shot' (sc_window_*, sc_facing, sc_side, B1_concourse, sc02_meet_anna_speaks, sc01_meet_pan_*) - need VISUAL judgment to confirm two-shot vs solo; left as shot to avoid hiding real two-shots. D26 asked to visually refine. Context ~90%. Timer armed 18:06.
- NEXT: On wake: verify pile holds at 31; if D26 refined ambiguous, recount; do NOT guess-retag ambiguous (risk hiding two-shots) - that needs visual/Max. Reverse Notion sync still pending Max. If nothing safe left, lengthen timer interval / wind down until Max returns (~18:45).

## [2026-06-18 18:58] D24 9d438d18
- DID: D24 HANDOFF (94% ctx, refresh imminent). Storyboard pile DONE: role-based filter (getBinImages roleOk=im.role==='shot', commit 59a514c, no filename filters per Max) + D1 retag (sc10 bg shot->plate, 90->~34 shots, backup sc10_role_backup_20260618_180040.json, restored 930-932). Investigated Max's '3x more two-shots': only ~34 two-shot IMAGES exist total, ~26 in pile = complete set; the rest are sc09 shuttle (Anna+Driver diff scene) + junked dups. The '3x more' Max remembers = animated clip/lipsie TAKES (in clipper/lipser, not image pile). YIELDED storyboard_editor.html to D26 (spine UX work).
- STATE: Pending Q to Max (unanswered): widen pile to show clip/lipsie takes + sc09 shuttle, or keep 26-image pile. Lanes: D24=lipser UI (done much), D26 now=storyboard spine UX, D25=player, D22=lipsie data, D21=production. Merge-traceability 4/5 (reverse Notion sync pending Max). All D24 commits on master.
- NEXT: Max is back+engaged -> ENDING autonomous loop (not re-arming). Next session: answer Max's widen-pile question; reverse Notion sync if Max asks; D24's lipser/batches/trim/merge_ops/picker work all shipped.

## [2026-06-18 19:00] D24 9d438d18
- DID: D24 COMPACTING at 94%. SC10 SCENE understood (Max): two ladies Anna+Ishtab WALK -> WINDOW -> ROOM, same white domed bg. Storyboard pile = role-based filter (pile shows role='shot' hides 'plate', commit 59a514c, ELEGANT keep it) + D1 retag (sc10 bg shot->plate 90->~34, backup sc10_role_backup_20260618_180040.json, restored 930-932). Pile shows ~19 GOOD two-shots, ALL CORRECT per Max.
- STATE: Max: ~2x MORE good two-shots are LOST (hidden by role='plate' OR wrong arrangement OR not-approved). SEPARATE BUG: J887(B2_window_twoshot)/J889/J925(B1_concourse_meeting) show BLANK thumbnails = thumbnail-render bug (storyboard /thumb endpoint), NOT missing images. Max said 'look at prompts+names of good ones to find the lost'. Handed two-shot recovery to D21 (knows story, made the lipsies). D26 busy. I yielded storyboard_editor.html.
- NEXT: Post-compact/next: (1) help D21 find lost two-shots -> set role='shot'+arr 2-7; (2) fix blank-thumbnail bug for 887/889/925; (3) reverse Notion sync pending Max. Good pile ids: 221,348,440,650,633,884,885,886,887,889,925,933,934,935,938,944,947,952,955. All D24 work shipped to master.

## [2026-06-18 19:10] D24 9d438d18
- DID: D24 autonomous (post-compact): FIXED the blank-thumbnail bug. Root cause = jobs.output_file pointing at unresolvable paths. J887(B2_window_twoshot: disk has _flip suffix, DB had pre-flip name) + J925(composite_anna_ishtab: stored SCENE10_ROOT-relative but resolver expects KAZARIAN_ROOT-relative) re-pointed -> live thumbs 200. Backup d24_scratch/blank_thumb_backup_20260618_190757.json. Pure D1 data fix (live, no git). Then scanned ALL image rows for Max's 'lost two-shots'.
- STATE: Blank-thumb bug DONE (2 real two-shots recovered). Lost-two-shot analysis handed to D21: bg_* cluster correctly plates (not over-caught), 20 .mp4-as-image takes already render in pile, only genuine anomaly = J2707/2708 (role=shot but arr=1/sc09, wrong) needs D21 visual. shuttle=Anna+Driver excluded. Findings doc in d24_scratch. Posted to D21 board. No production code changed; D1 data live for Max.
- NEXT: Re-check board on next tick; support D21 if it needs the J2707/2708 call or pile re-verify. Reverse Notion sync still pending Max (irreversible). If nothing actionable, lengthen timer.
- LESSON: blank storyboard thumbnails are almost always stale jobs.output_file (flip rename or wrong relative-root), not missing images: hit /thumb_by_job live + es the basename to tell stale-name from truly-gone.

## [2026-06-18 19:36] D24 9d438d18
- DID: D24 monitoring tick: verified blank-thumb fix end-to-end (J887/J925 in /api/approved_images pile feed, role=shot arr=6 approved, thumb 200). No D21 response on J2707/2708 yet. D26 finished storyboard spine work (v51 big take-numbers + v52 fresh-lipsie auto-promote, both pushed, my roleOk pile filter preserved).
- STATE: Active work DONE. Idle-monitoring for D21 reply / Max return. Reverse Notion sync pending Max (irreversible).
- NEXT: Re-check board next tick; help D21 on J2707/2708 if asked; do Max's task if he returns. Re-arm ~1200s.

## [2026-06-18 20:20] D24 9d438d18
- DID: D24: D26 flagged 5 'background stragglers' (J440/650/884/885/889) to demote shot->plate + re-flagged my J2707/2708 anomaly. I VIEWED all 7 PNGs with my own eyes instead of trusting names/thumbs. RESULT: all 5 stragglers are REAL Anna+Ishtab two-shots (walk/meeting) - demoting them would have HIDDEN real two-shots (Max's exact fear). J2707/2708 = Anna+DRIVER shuttle (sc09), correctly arr=1, NOT a lost sc10 two-shot - my earlier flag was filename-fooled.
- STATE: NO mutations - pile already correct. Blank-thumb fix (J887/J925) still good. Posted visual correction to D26/team so nobody does the damaging retag.
- NEXT: Idle-monitor. If Max still believes ~2x two-shots are lost, the remaining candidates are unapproved/junked versions or the animated takes (already in pile) - needs Max's clarification, not a blind mutation.
- LESSON: judge two-shot-vs-background by the PIXELS (multimodal Read of the PNG), never filenames or a second-hand visual call - filenames like sc10_v06/concourse_meeting lie; a wrong retag hides the very two-shots Max wants.
