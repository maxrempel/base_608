
## [2026-07-02 08:17] ? 83a4cc61
- DID: D03A: /storyboard3 elegant lane live. New /api/sb_pool scopes server-side. v3 strips imgInScene + role filter. sc11 leak (exp01_no_bg) closed - verified 0 off-scope rows in sc9/10/11.
- STATE: server restarted with new endpoint; v3 route serves storyboard_editor_v3.html; v2 untouched and running parallel.
- NEXT: Max opens /storyboard3 to compare A/B; on issue reports, rip remaining flood-then-filter spots (quietPoll dedup, showCats).

## [2026-07-02 08:39] ? 83a4cc61
- DID: v3 sb_pool endpoint live with status alias; audit clean; server restarted; commit 4269061 pushed
- STATE: idle waiting Max A/B feedback on /storyboard3 vs /storyboard2
- NEXT: on feedback, address; else keep decel

## [2026-07-02 11:27] ? 83a4cc61
- DID: v3 storyboard hardening: title fix, /api/storyboard_state_v2 cross-scene guard (sc10 lipsies off sc11 spine), sb_pool excludes cancelled+empty-file (blank tiles), startup opens /storyboard3 tab
- STATE: all pushed to master (6673ed1); server restarted; Max A/B testing v3 live
- NEXT: await next Max issue on /storyboard3
