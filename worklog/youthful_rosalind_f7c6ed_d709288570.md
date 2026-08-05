
## [2026-07-05 23:58] ? 4433a1f9
- DID: Built facer (per-image face box labeling in MoMA popup, D1 face_boxes) + facefreeze compositor (freeze non-speaking listeners per turn, feathered still crop over box, speech-envelope-anchored timeline). Integrated: 'freeze listeners' button on reel popups, /api/facefreeze endpoints, facefreeze_map table, startup ensure. Approved on sc11 spot4 (J3279).
- STATE: STATE: shipped+pushed to moma master; MOMA restarted clean; endpoints live and tested end-to-end.
- NEXT: NEXT: Max to hard-refresh MOMA tab for the button; run freeze-listeners on remaining sc11 spots; possible polish (idle breathing instead of hard freeze, gaze).

## [2026-07-06 16:15] ? 4433a1f9
- DID: facefreeze fully integrated into MoMA: 'silence face' panel on reel popups (pick person box + line + cushion + smooth), renders surgical freeze and registers a NEW lipsie job via fire_job into OUTPUT_LIPSIES. Report + user instruction written.
- STATE: STATE: shipped+pushed to moma master; MOMA restarted clean; end-to-end verified (new job 3289 created, /lipsie serves 200).
- NEXT: NEXT: Max hard-refresh MOMA tab to get the 'silence face' panel; use it on remaining leaks; problem2 (Derek gaze on Bias) = separate prompt-fix + rerender.

## [2026-07-10 14:48] ? ????????
- DID: XG2 IONS grant: made XG2 folder, saved plan note, found July 9 adviser emails, exported the 'IONS grant suitability' ChatGPT chat to XG2/IONS_grant_suitability_chatgpt_20260710.md (42k tokens) via share-link mint in Max's main Chrome
- STATE: Chat downloaded, not yet mined into proposal
- NEXT: Read the exported chat and continue the grant proposal draft; confirm adviser names (Garry Nolan? 'Rose cold heart'?)

## [2026-07-10 15:25] ? 41f36113
- DID: XG2 IONS grant: wrote 4 thorough drafts (REPORT honest data state, PROPOSAL LOI, BUDGET, invite LETTER to Dolan/Nolan/Coulthart) using real OMEGA/Kenefick analysis + ChatGPT plan. Committed to branch.
- STATE: Drafts done + committed (e33b8a85). Honest data = method built+pos-controlled, zero confirmed non-parental insertions, one live lead chr9:2226585 unphaseable w/o father+long reads. Flagged 'two families sequenced' overclaim.
- NEXT: Max reviews drafts; decide analysis-first vs polish LOI; resolve chr9 lead needs trio+long-read; confirm Ross Coulthart status

## [2026-07-10 15:55] ? 41f36113
- DID: SENT Vittorio Piantedosi follow-up email from anna@maxrempel.com (openly-AI Anna, signed DNA Resonance), bcc Max. Asks: which family member is each of 2 samples (H48ZYY71E/HYMQHR3VV), and can he provide the other 2 for a full trio.
- STATE: Email sent; awaiting Vittorio reply. Found the mystery flash drive = COSTELLA (SanDisk 1.82TB), Piantedosi family, 2 of 4 WGS samples (~1.17TB), 30x short-read TellMeGen. He never answered Feb-17 sample-ID question.
- NEXT: On reply: map sample IDs to people, pursue missing 2 samples; Piantedosi could be a 2nd sequenced family for the IONS grant.
