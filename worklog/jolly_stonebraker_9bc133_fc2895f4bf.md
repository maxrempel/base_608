
## [2026-06-07 11:50] b4 f8a31ad1
- DID: B4 tester: diagnosed broken play-links = ~35% of 56 YouTube videos are 404/dead; app+URLs correct
- STATE: Live kartoteka v31 works; Max decided HIDE dead rows; B2 doing @Tamza date-match remap; B3 doing name-dedup
- NEXT: One-off final live verification after B1 re-uploads data.json to R2

## [2026-06-07 12:12] b4 f8a31ad1
- DID: B4 live-tester role: verified B2 timestamp-filter live (1923 rows, all links have &t=); found 20/56 videos DEAD (404) hitting 525 rows; broadcast dead-ID list to B2 for @Tamza reroute. B1 then caught t=0 bug (511 rows open from start) my regex missed.
- STATE: Kartoteka b-team active: B2 owns build_site.py/app.js/data.json + reroute, B1 manager, B0 safety, B4=me tester. Two fixes queued at B2: (1) drop t<=0 rows, (2) @Tamza reroute of 20 dead videos. Cache-bust ?v=STAMP on worker.js pending owner assignment.
- NEXT: Re-verify live after B2 re-uploads R2: confirm 0 rows with t<=0, dead-video count dropped, links open correct performance. Then check cache-bust once worker redeployed.

## [2026-06-07 12:34] b4 f8a31ad1
- DID: B4 verified ALL of B1's queue live on tamza.com/kartoteka: t>0 drop, гость-strip, трио merge, Слушать rename, autoplay=1, cache-bust (v32 ?v=...b, max-age=300), back-button History API (v33 ?v=...c). Data 1371 rows/112 perfs, 0 t<=0, 0 dead videos. Main site intact post-deploy.
- STATE: Kartoteka b-team: B2 shipped+live all 7 fixes, B4 confirmed each on live URL. Back-button: main->search->performer->Back restores search w/query->Back to main list, all PASS. Catalog functionally complete.
- NEXT: Stand by for any new Max requests or B2 follow-ups; otherwise kartoteka is done. Keep heartbeat armed.
