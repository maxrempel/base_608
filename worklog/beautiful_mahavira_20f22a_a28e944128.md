
## [2026-06-19 18:26] d31 9bc1c7f0
- DID: D31: fixed empty SPOT 1 in storyboard v2. Cause: L0-3 were pinned to J585(L0-2)+J2826(L3), both rejected by v2.28 membership filter; correct greeting reel 2774 (membership 0-3) was pinned nowhere. Re-pinned line_current_clip L0-3->2774. Discovered /api/storyboard/assign also rewrites jobs.line_hash (v31, lines 1388-1405) - my repin corrupted 2774.line_hash, restored to birth m8df5135e0702c in D1.
- STATE: Spot1 verified rendering 2774 in browser. Data fix only (D1, live). No git commit needed for the data fix.
- NEXT: Coordinate on board re removing the jobs.line_hash rewrite from assign endpoint (D21's systemic complaint). Watch for other beats with same wrong-pin issue.
- LESSON: /api/storyboard/assign rewrites jobs.line_hash+vocal_line on every call (slideshow_server v31, lines 1388-1405) - calling it N times for one merged reel corrupts that reel's identity to the last line. Pin merged reels by writing line_current_clip directly, or fix the endpoint.

## [2026-06-19 19:22] d31 9bc1c7f0
- DID: Fixed spot11 (sc10 idx30-32) twice: first it was pinned to wrong old clip J490, then to half-rendered J2846. Re-pinned to approved in-map reel J2795 both times.
- STATE: spot11 now shows J2795 (approved, in membership map). v40 assign-corruption fix is live+verified.
- NEXT: Systemic fix needed: freshly re-fired merged reels must land in D21's membership map with a merge synth birth hash, or their spot drops until map regenerates. Bcast sent asking who fired 2846 + map-generator owner.

## [2026-06-20 09:33] d31 9bc1c7f0
- DID: Max ordered: wake relevant team, set 4mt autonomous, fix spot-drop bug e2e with testing. Woke D21/D30recoder/D24fixer/D26 via bcast wake (D24fixer force-woken, rest queued). Built e2e audit harness (worktree/_d31_audit_spots.py, HTTP-only) - found 15/33 broken spots, all 'pinned reel not in membership map'.
- STATE: Autonomous coordinator for the fix. Root cause: D21's hand-maintained membership map is stale; v2 hides any merged-spot reel not in map. Fix plan posted to bcast: D21 auto-derive map from D1; D30recoder v2 shows only approved+in-map; then re-pin spots; d31 runs audit gate (target BROKEN=0) + browser e2e.
- NEXT: On each 4mt wake: re-run _d31_audit_spots.py; when D21 regenerates map, re-pin the 15 broken spots to intended reels; when BROKEN=0 do playwright browser verify of /storyboard2; report to Max only when fully green.
- LESSON: The membership map being a hand-maintained JSON instead of D1-derived is the structural defect causing all the recurring spot drops.
