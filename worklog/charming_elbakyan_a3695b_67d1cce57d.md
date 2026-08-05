
## [2026-07-01 21:49] ? 18e027ca
- DID: Fired + presented sc11 spot1 v4 reels: J3102 (restructured simple English) and J3103 (Chinese trial). Both done, merge_hash=spd8ff62c3f575, still=sc11_arr02_v39.png, arr=20. Worker crash class fixed earlier (resilient makedirs, pushed 8e3fe7f).
- STATE: Awaiting Max review of J3102 vs J3103. Checking: line-1 gets spoken by Ishtab, points Anna-then-Gunther, calmer nodding, Ishtab age/likeness, chairs slide.
- NEXT: Iterate from whichever version Max prefers. Do NOT fire more until he reviews. If Ishtab likeness still off, may need to regenerate source still sc11_arr02_v39.png.

## [2026-07-04 14:43] ? 18e027ca
- DID: sc11 spot1 (intro, merge spd8ff62c3f575, L0-L1) FINAL keeper = reel J3105 (Chinese-prompt v6): open-palm gesture, ladies arrive to table, hands off chair backs, eyes on speaker not camera. Approved by Max. Moving to spot2 (AI-shutdown, merge sp0421c7fa34a3, idx2-9) blocked: its merged audio is NOT built (only spot1 merge_*.mp3 exists in lines_20260630_001255_R0merge; audio_resolver returns no match for sp0421c7fa34a3).
- STATE: PAUSED per Max. Do NOT run sass/Fish TTS. Max says voices already exist per-line and merged spots just RE-GLUE automatically (like spot1 did) via in-system tool (he suspects libup / merge-glue), NO regeneration, NO custom scripts. Max is assigning a HELPER session to research the correct in-system audio-gluing path.
- NEXT: Wait for helper's finding on how merged audio gets glued in-system. Then build spot2 audio that way (free re-glue) and fire spot2 reel with fire_merge_lipsie(sp0421c7fa34a3, still sc11_arr02_v39.png or a distinct arr02 still, scene sc11_arr02, arr id 22). Reuse the proven Chinese v6 prompt structure. Still sc11_arr02 = the AI-shutdown table shot.
- LESSON: Do not run sass to (re)build merged audio for a spot; merges re-glue existing per-line audio in-system automatically. Fish TTS regeneration is wrong + costs money.

## [2026-07-04 16:34] ? 18e027ca
- DID: sc11 spot1 DONE+kept=J3105. sc11 spot2 (merge sp0421c7fa34a3, L2-9, still sc11_arr02_v23.png arr20): D03B built all 19 sc11 merged-audio files (no TTS) via sass merge-pass path. Fired spot2 reels: J3115 Chinese (rejected: duck-nodding, all-simultaneous). Switched to ENGLISH + hard one-speaker-at-a-time: J3116 names, J3117 bare digits, J3118 'Person One..Four'. All 3 presented for comparison.
- STATE: Awaiting Max review of J3116/J3117/J3118. Core problem: model animates everyone simultaneously (all nod on every Yes). Fallback Max named = SPLIT spot2 into separate single-speaker reels if one-at-a-time still fails.
- NEXT: If Max approves one: keep it, move to next sc11 spot. If still synchronized: split spot2 into per-turn single-speaker reels. Coordinate w/ D03B before any libup spine-collapse (still pending for sc11). Flag: sp3b8bd67b216c=15.96s over ~15s cap.
- LESSON: wan2.6-i2v-flash tends to animate ALL faces simultaneously on multi-turn reels (everyone nods together on each line); numbered 'only one moves' rule is the mitigation being tested; per-turn split is the fallback.

## [2026-07-04 22:39] ? a5643670
- DID: sc11 spot2 (merge sp0421c7fa34a3, 8 lines Anna/Derek x3/Werner) FAILS on every merged-reel attempt: J3115 zh, J3116 en names, J3117 en digits, J3118 en 'Person One', J3125 ru, J3138 zh, J3139 zh+numbered v60, J3147 zh+numbered v62. All duck-nod / can't localize speaker. ROOT CAUSE agreed w/ Max: WAN can't tell whose turn it is when one audio track carries all voices; ALSO too many lines overloads it (spot1 worked at 2 lines).
- STATE: DECISION (Max): split spot2 into SHORT 2-line sub-reels (spot1 length), keep all 4 people onscreen reacting. Max is manually dividing the lines now + will have a helper build the short sub-merges. My suggested split: 2a Anna 'The AI shutdown'+Derek 'Yes'; 2b Anna 'All three countries'+Derek 'Yes'; 2c Anna 'At the same time'+Derek 'Yes'; 2d Anna 'By coincidence?'+Werner 'Suspicion is infectious'.
- NEXT: HOLDING for Max's line division / new short merge_hashes. When short merges registered+audio glued (concat existing per-line voices per chunk, D03B method), fire each as its own reel via fire_merge_lipsie with numbered-image + short Chinese prompt (spot1 recipe). Numbered stills exist: sc11_arr02_v62_numbered.png (L-R 1Ishtab 2Werner 3Derek 4Anna).
- LESSON: wan2.6-i2v multi-speaker reel: keep merges SHORT (~2 lines/~4s). Long 8-line merges overload it -> all faces animate at once. Spot1 (2 lines) worked; 8-line spot2 never did across 8 tries/3 languages/numbered heads.

## [2026-07-04 23:46] ? a5643670
- DID: sc11 spot2 diagnosis CONFIRMED by Max: unique long lines (Anna Qs, Werner 'Suspicion is infectious') localize to ONE speaker fine even in merged reels; the three DEREK 'Yes' beats make ALL THREE speak+nod synchronously ('like clones'). Root cause: 'Yes' too short (~0.3s) for audio-localization + 'yes'=agreement triggers group-nod prior. Shortening (2a/2b) and numbered stills + EN/RU/ZH prompts all failed on the Yes beats. Reels fired this session incl short splits: 3154/3155 zh, 3156/3157 ru screenplay, 3158/3159 ru 'Человек N говорит'.
- STATE: PROPOSED FIX to Max: per-line micro-reels, each fed ONLY one speaker's voice (single-member merge), then stitch/sequence. Max skeptical it's feasible; I offered a 1-clip PROOF (Derek-only 'Yes', ~/usr/bin/bash.30). AWAITING his 'давай'.
- NEXT: On go: register Derek's 'Yes' as 1-member merge (D03B glue method: copy the single per-line Derek mp3 as merge_<hash>.mp3 + merges.json), fire 1 micro-reel on numbered v62 still, prompt 'только Человек 3 говорит, у остальных рот закрыт, никто не кивает'. If proof works, do all 8 lines + stitch (storyboard spine already sequences per-line reels).
- LESSON: wan2.6-i2v: short generic agreement words ('Yes') can't be localized to one speaker in a multi-voice track -> all mouths say it in sync. Long unique lines localize fine. Fix = one-voice-per-clip, not prompt wording.

## [2026-07-05 22:45] ? a5643670
- DID: BREAKTHROUGH confirmed: TWO-SHOT (2 faces) solves the 'Yes' clone bug. Saved memory feedback_twoshot_for_short_yes.md + MEMORY.md pointer. Max re-split sc11 spot2 into: spot2=6 lines Anna/Derek (merge sp5bb675ba211a 9.3s), spot3=2 lines Anna/Werner (merge sp314845dac658 3.9s) - D03B registered+glued both. Max placed stills in storyboard: spot2=v95 (Anna+Derek two-shot, job3256), spot3=v70 (4-person group, job3146), read via storyboard_spot_order table + pixel-check. Fired J3261 (spot2 6-line v95) + J3262 (spot3 2-line v70). Both done, presented.
- STATE: Awaiting Max review of J3261 + J3262. spot1 keeper=J3105. Earlier two-shot proof J3260 (spot2a 4-line on v94) worked+approved.
- NEXT: If J3261/J3262 approved: sc11 arr02 (spots1-3) done as reels; move to next sc11 spot per storyboard. Keep using TWO-SHOT per speaking-pair for any short/'Yes' exchanges. Coordinate w/ D03B on remaining sc11 merges + pending libup spine-collapse + Notion [[MERGE]].

## [2026-07-05 22:51] ? a5643670
- DID: sc11-arr02 COMPLETE: Max APPROVED all three reels - spot1=J3105, spot2=J3261 (6-line Anna/Derek two-shot v95), spot3=J3262 (2-line Anna/Werner group v70). The multi-day 'Yes' clone battle is won via TWO-SHOT framing. Rule saved to memory.
- STATE: sc11-arr02 done. No git changes this session (reels are D1 data, auto-spine-pinned; only memory file added, Nextcloud-synced).
- NEXT: Next: continue sc11 remaining spots (many more merges already registered: lines21-31, 60-69, 80-84 etc). Use TWO-SHOT for any short/'Yes'/repeated-word exchanges. Coordinate w/ D03B on pending libup spine-collapse + Notion [[MERGE]] for sc11 before mutating spine.
