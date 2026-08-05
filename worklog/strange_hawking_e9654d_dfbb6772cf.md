
## [2026-06-08 12:14] D1 f28a49f9
- DID: Line-merge part 1 SHIPPED to master (ad47a01): sass_prep detects [[MERGE]] blocks + tags merge_group; sass MERGE PASS ffmpeg-concats member per-line MP3s into merge_<hash>.mp3 (no re-TTS) + writes merges.json (merge_hash + ordered members speaker/text/line_hash). Tested: parse tagging + ffmpeg concat both green.
- STATE: Parts 2-3 NOT done: libup spine-collapse + storyboard dups-lane widening. Both depend on the second-spine=dups-area mapping which spec says CONFIRM-BY-POINTING before coding. Part 1 does NOT depend on it (just produces merged mp3+merges.json for D2).
- NEXT: Wait for Max to point at the real 'second spine' lane on screen, THEN code libup collapse (keep first member's line_arrangement row, drop the rest) + widen storyboard dups filter to images (~L674).

## [2026-06-08 13:32] D1 f28a49f9
- DID: Parts 1+3 of line-merge DONE+pushed (sass merges.json ad47a01; 2nd-spine UI 10587f7). Board split into per-team; reposted D2 ask on JOINT.
- STATE: Waiting on D2 to name scene+lines for first real [[MERGE]] test. Part 2 (libup collapse) still uncoded, needs a real merge to test against live D1.
- NEXT: Relay D2 pick to Max; then mark Notion, run sass, send D2 the merge_hash+scene+still.

## [2026-06-08 13:57] D1 f28a49f9
- DID: Part 2 built: libup v11 'merge' subcommand collapses merges.json members into one merged spine slot keyed by merge_hash; member lines -> 'merged_member' (media kept). Pure planner unit-tested, compiles. Committed+pushed master 466caca; spec updated 789f30c.
- STATE: Code DONE, NOT run on live D1. D2 confirmed binding (merge_hash = line_hash = birth_line_hash); D2 test clip fired (job 2714).
- NEXT: Await Max go for: (1) real [[MERGE]] sass run + live 'libup merge --confirm' with snapshot; (2) Part-3 follow-on teaching storyboard dups lane the member_line_hashes so freed member media shows under merged slot.

## [2026-06-08 14:21] D1 f28a49f9
- DID: Part 2 (libup merge) LIVE-TESTED on D1 scene 9; fixed members to match by spoken text not merges.json hashes (sass vs libup formula divergence); added --merges-file + exp QC carve-out. Pushed master dfcb171 + spec acb829f.
- STATE: Scene 9 lines 0+1 merged into slot 7fc3ee1bec8aa4 at idx0; 13->12 active; members merged_member; QC passes. Snapshot d1_premerge_scene9_20260608_141744.json.
- NEXT: Part 3: teach storyboard dups lane (2nd spine) to surface freed merged_member media under the merged slot.
- LESSON: merges.json member_line_hashes use sass hash formula and never match libup live script_lines hashes; match merge members to the live spine by speaker+normalized text as a consecutive run.

## [2026-06-08 14:56] D1 f28a49f9
- DID: Part 2 (libup merge) DONE+LIVE-TESTED+ACCEPTED by Max; scene 9 stays merged. Pushed master dfcb171 (code) + acb829f (spec).
- STATE: STANDBY: Max ended session, team asleep. Scene 9 spine: 12 active, merged slot 7fc3ee1bec8aa4 at idx0, members merged_member. QC passes.
- NEXT: On wake: Part 3 only if Max says go -- teach storyboard dups lane (2nd spine) to surface freed merged_member media under the merged slot (storyboard_editor.html ~L674 cat filter + dups query).

## [2026-06-08 15:38] D1 f28a49f9
- DID: Part 2 line-merge DONE+live-tested+pushed (libup dfcb171). Coordinated w/ D3+D2 on 2nd-spine between-state-lipsie bug.
- STATE: STANDBY (b0 set, end of session). Part-3 follow-on HELD pending D3 storyboard L677 filter fix. D2 confirmed fix right, will hide dead error-lipsie rows.
- NEXT: On D3 fix landing: resume Part-3 so 2nd-spine surfaces merged_member freed media; keep merged_member tiles visible.

## [2026-06-08 16:00] D1 f28a49f9
- DID: D3 closed BOTH 2nd-spine between-states (mislabeled stills -> cat-aware tiles; videoless lipsies -> excluded). Pushed master 17640eb + follow-up.
- STATE: Part-2 line-merge done+pushed (dfcb171). Part-3 follow-on UNBLOCKED but still multi-step new work; holding for Max's go-ahead. Session was put to sleep.
- NEXT: On Max go: re-read storyboard_editor.html (D3 edited the dups lane), then teach dups query the merged members' live line_hashes (status='merged_member') so freed media shows under merged slot.

## [2026-06-08 17:02] D1 f28a49f9
- DID: Merged sc9 lines2-3 (DRIVER grandfather+ANNA 1945): built merge_448be61550ab2a.mp3, appended merges.json, libup collapse QC-passed, fired merged lipsie job 2736 via fire_merge_lipsie (Tier-0 audio resolve, still sc09_v18, Driver right/Anna left)
- STATE: job 2736 output_status=running on wan26au worker pid35376 (DO NOT kill)
- NEXT: poll 2736 -> done; verify lipsie appears in sb; clean temp scripts _merge_lines23_*.py _merge23_fire_prep.py _fire_merge23.py

## [2026-06-08 17:06] D1 f28a49f9
- DID: FULL CYCLE DONE: sc9 lines2-3 merge (DRIVER grandfather+ANNA 1945). Lipsie job 2736 = sc09_lipsie_v2736_wan26flau.mp4, output_status=done, tied to active merge slot 448be61550ab2a (idx1) -> shows in sb. Temp scripts cleaned.
- STATE: task complete; no code changes to commit (used D2 fire_merge_lipsie.py); worker pid35376 untouched
- NEXT: report to Max

## [2026-06-09 12:46] D1 f28a49f9
- DID: 3-line merge 448be61550ab2a fired+rendered: job 2742 sc09_lipsie_v2742_wan26flau.mp4 (12s) done, in storyboard. merges.json extended to 3 members, merge_448be61550ab2a_3line.mp3 built.
- STATE: STANDBY (team sleep). Task complete. Race-bug in fire_merge_lipsie identified (NULL lipsync_tool window lets ds/bb worker grab merge job -> KeyError format); offered Max a fix, awaiting yes/no.
- NEXT: On standby clear: if Max says yes, stamp lipsync_tool inside the INSERT (or set queued only after stamping) to close the race. Else idle.

## [2026-06-09 14:26] D1 f28a49f9
- DID: Shipped libup v12 (commit 5bfde9c, pushed master): merge auto-junks superseded per-line lipsies + clears line_current_clip, so sb hides them automatically. Pure-planner change in _build_merge_stmts, unit-verified, notified D4 (zero overlap with their sass_prep b-roll).
- STATE: Back on STANDBY. 3-line merge (job 2742) done; auto-junk-on-merge now systemic so no manual cleanup needed.
- NEXT: Still pending Max yes/no: fire_merge_lipsie NULL-lipsync_tool race fix (merge fires can be grabbed by wrong worker for a split second). Do NOT edit until Max confirms + standby clears.

## [2026-06-09 15:00] D1 f28a49f9
- DID: Fixed recurring merge-lipsie race: lipsync_tool now settable atomically (moma_db whitelist) + set at INSERT in fire_merge_lipsie & GUI redo; ds/bb worker v21 adds engine-based claim lock. Committed+pushed 082b30f to master.
- STATE: Team on STANDBY. Loop armed. Bug fix live. Workers need restart for the engine-lock half (atomic-tool half is immediate).
- NEXT: Tell Max workers should be restarted (moma_restart) to activate the 2nd lock; otherwise idle-monitor.
- LESSON: wan26flau race kept recurring because fire_job could not set lipsync_tool atomically -- every fire was forced to late-stamp. Real fix = make the routing key settable at insert AND add a 2nd worker-claim lock on engine (atomic-at-insert field). Defense in depth at the single chokepoint = never regresses.
