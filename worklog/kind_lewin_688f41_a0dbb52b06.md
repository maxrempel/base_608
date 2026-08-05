
## [2026-06-16 16:01] ? 50c19667
- DID: Resumed post-compaction. b7nonhtimes chose drop path _work/seg_nonh/<vid>.json (NOT my old nonh_boundaries proposal) - 11 drafts landed, schema {segments:[{start_sec,end_sec,start_hms,end_hms,performer,author,title,confidence}]}. Built _batch_nonh_v01.py (reuses aligner_v01.match_segment vs canon_v03; reads seg_nonh boundaries+inline DS attribution; pulls transcript text per window). Pilot -WuKx7lbhJE EYEBALLED=PASS (9 KNOWN all plausible, clean score gap, NEW? carry intro performer+author+title). Scaling --all -> drafts_nonh_v01/.
- STATE: NONH identifier built+piloted+passing; batch over 11 landed drafts running (bg); board posted.
- NEXT: When batch done: read _INDEX.txt totals, eyeball 1 more draft, commit _batch_nonh_v01.py to master, report to Max. As more seg_nonh drafts land (608 more coming) re-run --all. Confirm with b15merger the join of drafts_nonh_v01 + resolved_songs_v01.

## [2026-06-16 16:10] ? 50c19667
- DID: NONH identifier batch DONE + SHIPPED to master 6bc85475. 34 videos, 646 segs, 130 KNOWN/516 NEW?, 0 err. KNOWN align median 88; near-threshold 4/6 correct, 2 soft-FP on vocalise. Committed _batch_nonh_v01.py. Posted board, reported Max.
- STATE: NONH identification live + on master; drafts in drafts_nonh_v01/. Waiting on b7nonhtimes for ~608 more seg_nonh drafts.
- NEXT: Re-run 'python _batch_nonh_v01.py --all' as drafts land (idempotent, overwrites). Optional polish: skip wordless-vocalise segments (la-la/na-na) to kill the ~1.5% soft-FP. Coordinate b15merger join of drafts_nonh_v01 + resolved_songs_v01.

## [2026-06-16 16:10] ? 50c19667
- DID: Autonomous tick: seg_nonh grew 34->181 drafts. Re-running _batch_nonh_v01.py --all over all 181 (bg b4sp33b1m) to extend coverage per Max 'catch them as they appear'.
- STATE: NONH identifier re-running over 181 drafts; tool on master 6bc85475.
- NEXT: On batch done: read drafts_nonh_v01/_INDEX.txt totals, report KNOWN/NEW to Max if he's back. Keep re-running --all as seg_nonh approaches 786. Optional: vocalise-skip polish.

## [2026-06-16 16:47] ? 50c19667
- DID: NONH identifier --all over 181 drafts DONE: 1985 segs, 495 KNOWN/1 MAYBE/1489 NEW?, 0 err. ~25% catalog-match rate, consistent with 34-vid run. Tool on master 6bc85475, drafts in drafts_nonh_v01/.
- STATE: 181 NONH concerts auto-indexed; waiting on b7nonhtimes for remaining (~786 target).
- NEXT: Re-run 'python _batch_nonh_v01.py --all' as seg_nonh count grows toward 786. Optional vocalise-skip polish (~1.5% soft-FP). b15merger join drafts_nonh_v01 + resolved_songs_v01.

## [2026-06-16 18:35] ? 50c19667
- DID: Autonomous tick: seg_nonh jumped 181->512 (b7nonhtimes big batch). Re-running _batch_nonh_v01.py --all over 512 (bg buezkzrkl).
- STATE: NONH identifier re-running over 512 drafts; tool on master 6bc85475, output drafts_nonh_v01/.
- NEXT: On batch done: read drafts_nonh_v01/_INDEX.txt TOTAL line, report KNOWN/NEW. Keep re-running --all toward 786 target.

## [2026-06-17 14:39] ? 50c19667
- DID: Re-ran NONH identifier across all 691 timed videos (was stale at 34); batch b2nphkwr9 in progress, 527/691 drafts written
- STATE: 691 seg_nonh boundary drafts now exist, all have transcripts; identifier catching up; Max said named-inventory not needed (summary is enough)
- NEXT: Verify _INDEX TOTAL when batch finishes; keep re-running as more boundary drafts land toward ~786

## [2026-06-17 16:29] ? 50c19667
- DID: NONH identifier caught up: all 691 timed videos mapped (was stale at 34)
- STATE: TOTAL videos=691 segments=6969 KNOWN=1411 MAYBE=12 NEW?=5546, 0 errors; identifier now current with timing stage
- NEXT: Re-run on each tick as boundary drafts climb toward ~786; timing stage (b7nonhtimes) is the remaining bottleneck

## [2026-06-18 02:22] ? 50c19667
- DID: Re-ran identifier on 697 timed videos (6 new landed overnight)
- STATE: TOTAL videos=697 segments=7065 KNOWN=1421 MAYBE=12 NEW?=5632, 0 err; identifier current
- NEXT: Keep re-running each tick as boundary drafts climb toward ~786

## [2026-06-18 14:13] ? 50c19667
- DID: Re-ran identifier on 744 timed videos (47 new landed)
- STATE: TOTAL videos=744 segments=7910 KNOWN=1577 MAYBE=14 NEW?=6319, 0 err; identifier current
- NEXT: Keep re-running each tick as boundary drafts climb toward ~786

## [2026-06-18 17:11] ? 50c19667
- DID: Re-ran identifier on 772 timed videos (28 new landed)
- STATE: TOTAL videos=772 segments=8381 KNOWN=1684 MAYBE=15 NEW?=6682, 0 err; identifier current
- NEXT: Keep re-running each tick as boundary drafts climb toward ~786

## [2026-06-18 20:07] ? 50c19667
- DID: Re-ran identifier on 782 timed videos (10 new landed)
- STATE: TOTAL videos=782 segments=8693 KNOWN=1764 MAYBE=16 NEW?=6913, 0 err; identifier current, near ~786 target
- NEXT: Keep re-running each tick until timing stage finishes (~786)
