
## [2026-06-08 11:59] D2 7faee3c9
- DID: D2 (firing) on MOMA line-merge. Joined bcast as D2; ACKed D1's contract; read project_wan26flau_lane.md and found the merged-lipsie firing recipe is ALREADY PROVEN (job 2713, 2026-06-03, Max 'it worked perfectly'): wan26flau lipsyncs turn-taking from ONE concat MP3 + prompt naming who speaks 1st/2nd + L/R. Exp scripts: sc10/combo_runner/code/_merge_fire_exp.py + _fire_mergeexp.py (manifest-injection hack). Posted firing plan + boundary + open Q to board.
- STATE: BLOCKED on input, not on me. Waiting: (1) D1 to confirm merged unit will expose ordered (speaker,text,member_line_hash); (2) Max for speaker L/R screen-position source; (3) Max doit22 before building the first-class merged-audio-lipsie helper (doc says ask first). No live edits authorized. Design+dict committed/pushed. ~90pct tokens, compaction imminent but durable state is on board + committed docs + session_status.
- NEXT: On doit22: build first-class merged-audio lipsie fire path = generalize _merge_fire_exp/_fire_mergeexp into a reusable helper that consumes D1's merge_hash+ordered members+still, builds alternating-speaker description (who 1st/2nd + L/R + slow/antiglamour tail per wan26flau doc), fire_job lipsie engine=wan2.6-i2v-flash + lipsync_tool=wan26flau. Re-read project_wan26flau_lane.md first.
- LESSON: wan26flash CAN do multi-speaker turn-taking in ONE clip from a single concatenated MP3; control is words-only (who speaks 1st/2nd + L/R), no speed slider.

## [2026-06-08 12:22] D2 7faee3c9
- DID: D2 firing design brainstormed with Max: merged unit = 'just a line with its own hash'. D1's real sass manifest entry keyed by merge_hash means firing with birth_line_hash=merge_hash auto-resolves audio (no 2713 synthetic-hash hack). Trigger decided: A=from chat. fire_merge_lipsie prep doc pushed.
- STATE: Build BLOCKED on Max doit22. One open Q: speaker L/R source (1=read from still, 2=Max says per fire; my lean=2).
- NEXT: On doit22+L/R answer: build fire_merge_lipsie(merge_hash,members,still,positions,scene,arr) reusable helper in combo_runner/code; generalize 2-person prompt to N turns; fire one test clip.

## [2026-06-08 12:45] D2 7faee3c9
- DID: D2 firing BUILT+pushed (cb6d0fc): audio_resolver v04 reads merges.json (Tier 0 by merge_hash); fire_merge_lipsie.py helper (verifies merged audio resolves, raises no-fallback, fires wan26flau + flips lipsync_tool). Validated on real 2713 audio: merge_hash resolves merge_<hash>.mp3, non-merge lines unaffected. Prompt = Max-approved verbatim-lines+emotion+style, composed in chat by looking at rendered still.
- STATE: All built+validated EXCEPT the final paid wan26flau fire, which needs ONE real [[MERGE]] sass run (merges.json) from D1 + Max go. D1 shipped sass merges.json (part1); libup spine-collapse pending.
- NEXT: When D1 emits a real merges.json: get merge_hash+scene+still, look at still for L/R, compose+get-Max-approve prompt, call fire_merge_lipsie(), watch job to done, present clip.

## [2026-06-08 15:50] D2 7faee3c9
- DID: Merged-lipsie firing LIVE-PROVEN (job 2714) + ran smile-intensity experiment on sc9 161-162 merge (jobs 2716-2720); 2720 chosen acceptable. Committed firing-doc LIVE-PROVEN status + smile lesson (master 59c5055, latest push).
- STATE: D2 firing side complete & proven. Smile size NOT controllable in wan26flau; best=closed-mouth+slow-onset (2720). Spend ~.25. STANDBY (b0 set end-of-session). Worker churn from multi-worktree sessions is pre-existing, low priority.
- NEXT: Hold for Max direction or D1 Part-3. Do NOT auto-approve 2720; Max picks spine take in storyboard. Keep self-wake armed.
- LESSON: wan26flau smile intensity can't be tamed by prompt (size words/negatives/onset all fail); closed-mouth + slow onset is the best acceptable lever. Don't re-burn money chasing it.

## [2026-06-09 12:28] D2 7faee3c9
- DID: Nod fix manual track: gave Max the 'never coming to rest' prompt clause; he tested it on the grandfather/1945 line, reports it helped just a bit
- STATE: STANDBY (team asleep). Prompt-only levers near ceiling for both smile and nod in wan26flau (Chinese tool, weak prompt adherence)
- NEXT: Move nod fix to deterministic audio-pad-then-trim + freeze-hold last clean frame; width normalization at assembly still open

## [2026-06-09 14:22] D2 7faee3c9
- DID: Quiet STANDBY ticks. Noted D1 merged libup v12 (5bfde9c): folding a merge now auto-junks superseded per-line lipsies + clears them from line_current_clip, storyboard hides them
- STATE: STANDBY (whole team asleep, b5). D2 firing side idle; nod fix (audio-pad-then-trim) and width normalization both await Max's go
- NEXT: On wake: offer to add tail_phrase auto-append+trim option to fire_merge_lipsie for the nod fix; decide width master resolution at assembly
