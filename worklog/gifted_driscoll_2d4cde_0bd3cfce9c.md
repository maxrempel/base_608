
## [2026-06-18 17:50] D26 ddc2f543
- DID: D26 joined team; diagnosed sc10 storyboard PILE filter fight
- STATE: Root cause: filename-based filter can't separate good 2-ladies shots from junk (sc05_window_twoshot=good vs bg_corridor=junk both contain location words). D24 whitelist->1 img (reverted aac4809); blacklist 647761d->166 w/junk. Data has clean role(shot/plate)+mood(neutral/broll) but corridors are tagged shot+neutral so no filter isolates '2 ladies'.
- NEXT: Proposed: curate once (junk corridor/window/single junk in sc10, junk persists), then pile is clean. Awaiting Max OK to junk + show list.

## [2026-06-18 19:06] D26 ddc2f543
- DID: D26 Phase1 shipped: storyboard v51 2nd-spine making-order numbers + expandable lane
- STATE: Pushed master 3815e69, e2e verified live (ordinals 2778->1/2811->2/2815->3 correct; expand 64->146px; only favicon404). storyboard_editor.html is my lane (D24/D25 cleared). 'merg' noun added to dict+system map.
- NEXT: Phase 2: newest-lipsie auto-promote to 1st spine for unpinned lines; FIRST check mixboard auto-resort rule (slideshow_server/mixboard) so they don't fight over line_current_clip pick; respect spine_pinned; persist pinned:0.

## [2026-06-18 19:14] D26 ddc2f543
- DID: D26 Phase2 shipped: fresh lipsie auto-lands in 1st spine (storyboard v52)
- STATE: Pushed master b5a4ffa. e2e verified: 0 reshuffle on load (no DB corruption), baseline 86 lipsies, fresh-lipsie placement correct. First load-time design was INERT (all 31 picks pinned) + couldn't respect reverts -> discarded, rebuilt as in-session new-arrival detection (SEEN_LIPSIES set diff). All 4 of Max's asks done + 'merg' coined.
- NEXT: Optional Phase 3 if Max wants: persist a 'seen' marker so lipsies made while sb CLOSED also auto-land on reopen. Otherwise task complete.

## [2026-06-18 20:03] D26 ddc2f543
- DID: D26 autonomous: verified Max's original pile complaint is ~90% fixed by D24's role retag
- STATE: Images-only pile = 19 stills (was ~91); 5 bg stragglers still role=shot (J440,J650,J884,J885,J889) - handed to D24, did NOT mutate (Max's curation, away). J2707/J2708 sc10 imgs mis-filed in arr=1. My spine v52 done+pushed (b5a4ffa).
- NEXT: If Max wants: flip those 5 shot->plate + fix J2707/8 arrangement. Otherwise idle - all my established work shipped.
