
## [2026-06-24 22:39] D41 52d965f2
- DID: Shipped storyboard v2.46: replaced fragile client imgBeat watermark with real persisted timestamps (reel created_at vs image placed_at) for 1st-spine precedence.
- STATE: Committed+pushed master 1c9d54a; slideshow server restarted on 8790; placed_at+created_at verified live.
- NEXT: Await Max verify: make a reel -> should land on 1st spine; drag image to slot -> bumps reel to 2nd; drag image to 2nd spine -> stashes.

## [2026-06-25 15:11] D41 52d965f2
- DID: v2.48 left storyboard spine EMPTY (didn't migrate line_current_clip picks into new storyboard_spot_order table). v2.50 (7ba2543) adds load-time seed: empty spots seeded from legacy pick + matching reels, persisted.
- STATE: v2.50 pushed to master, slideshow_server already restarted on prior commit. Awaiting Max's verify after hard-refresh.
- NEXT: If still empty: check /api/storyboard_state_v2 spot_order growth after a /storyboard2 load (seed POSTs); also check assigned dict has entries (legacy source).

## [2026-06-25 18:32] D41 52d965f2
- DID: Shipped v2.51 (sparse positions, null sentinel - no auto-promote on p1 removal) and v2.54 (fresh reels land on p1 on every page load - fixed first-load baseline that swallowed unplaced reels)
- STATE: v2.54 live on master 803de8a; server serves fresh HTML each request, no restart needed
- NEXT: wait for Max to test new ellipses land on p1 after refresh
