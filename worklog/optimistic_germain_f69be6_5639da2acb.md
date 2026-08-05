
## [2026-06-24 14:15] ? 8ec57f54
- DID: Fixed sc10 spot9 'reel absent': junk reels 2783/2789 injected phantom 5-line span [24,25,26,27,28] into /api/reel_membership_sc10 via Sources A(seed)+C(vocal_line regex) which lacked junk filters. Added .startswith('junk') guard to both (commits 5951ffe + cf7bb20, on master). Restarted slideshow_server 8790 (PID 38040). VERIFIED live: spot9 now derives [24,25,26,27], filled by approved reel 2935 - exact auto-match, no pin. L28 ('Could you explain?') belongs to spot10 (L28-L29, merge sp109ddb58dbea).
- STATE: spot9 DONE+pushed+live. Max is branching+compacting. Next branch: full storyboard recheck (every spot + rebuilt code) for inelegance/inherited bugs.
- NEXT: After Max's new branch: recheck every spot end-to-end and audit storyboard code for inherited messiness. Coordinate 8790 restarts w/ D40 (owns slideshow_server).

## [2026-06-24 19:04] D53 8ec57f54
- DID: D53 storyboard merge-map unification: migrated 4 legacy 'm' merges into merge_ops via register_merge + rebound 24 sc10 reels onto canonical 'sp' merge_hash; stripped Sources A/B2/C from /api/reel_membership_sc10 leaving merge_ops alone (slideshow_server v41, committed+pushed master 3affb6c); bounced 8790; verified 8 spans live; cleaned _d53_ scratch; resolved a real two-session D53 id-collision (other was idle 13min, I kept D53).
- STATE: DONE - migration complete + live + verified + announced to team.
- NEXT: Nothing pending for D53. Storyboard now driven by single canonical ledger.
- LESSON: When stripping fallback map-sources, first migrate ALL legacy data into the canonical store and rebind dependents, then verify the live endpoint reproduces identical output BEFORE and AFTER the strip - the strip should be a no-op by construction.

## [2026-06-24 22:21] D53 8ec57f54
- DID: Built two-table merge ledger: merge_ops (live state) + merge_ops_events (append-only change-story, session-stamped). Backfilled 16 rows->40 sc10 events. Wrote merge_ledger_method_v01_tomemex.md + MEMORY.md ref.
- STATE: DONE+pushed master e97b4c7 (code) + 3d3041b (doc). Verified live on D1, idempotent backfill.
- NEXT: Idle/await Max. D53 storyboard audit + ledger elegance complete.
- LESSON: History belongs in an append-only events table, never crammed into a live-state JSON field (repeated supersede overwrote the audit trail pre-D53).

## [2026-06-25 18:32] D53 8ec57f54
- DID: Fixed scene-9 storyboard's two empty BROLL end spots (first=opening title card job2757, last=earth arrival job2758).
- STATE: DONE+VERIFIED. Fix live on origin/master (bundled into D41 commit 803de8a, file storyboard_editor_v2.html v2.53). Root cause: loadAll+quietPoll fetched /api/storyboard_state_v2 with NO scene param (got scene10 state for scene9), AND the v2.12 'drop all clips' filter removed BROLL picks (they are job_type=clip not reels). Fixed: scene-scoped state fetch + pick-membership keep for clips. Tested in real browser: 12 spots, 0 empty, persisted to D1 storyboard_spot_order.
- NEXT: Nothing pending. Max confirmed thanks. If issues recur, hard-refresh scene-9 tab; verify storyboard_spot_order has -1->[2757] and 10->[2758].
