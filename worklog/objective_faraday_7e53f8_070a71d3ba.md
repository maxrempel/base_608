
## [2026-07-05 15:09] ? edcd05fb
- DID: Built Tamza Zoom attendance DB: crawled 14 months (May2025-Jul2026) of Zoom usage reports via admin@tamza.com login, pulled participant lists per meeting, aggregated 126 real sessions / 309 people ranked by attendance. Output CSV at projects/tamza_zoom_attendance/output/attendance_ranked_v01.csv
- STATE: Zoom report only goes back to May 2025 (no 2-3yr data). DB v01 has some near-dup clusters to merge (Regina Perl+Regina, Movshits, Natalya Grinbaum). Playwright login was via CLI password (Bitwarden extension logged-out - separate fix branch owns that).
- NEXT: Merge duplicate clusters, then LEFT-JOIN emails from the рассылка Google Sheet (id 1qnWGKHzUtbezjsHo8L2580MPDIiVMVSJs_f-MMuIavg) + contacts to attach reach info; goal = auto-send secret Zoom link to regulars

## [2026-07-06 09:32] ? edcd05fb
- DID: Max expanded scope: LIFETIME merge of all sources, include only performers with >=5 lifetime performances. Found performances DB = Tamza catalog output/data.json (26283 rows, 2020-2026). Extracted 382 performers >=5, linked Zoom attendance (150 matched). Spine at output/spine_perf_ge5_plus_zoom_v01.csv. Handed to b51c for contact/email attach.
- STATE: Performer full-Cyrillic names resolve most Zoom ambiguity (Vera=Вера Павлова etc). b51c owns final contact enrichment. A few zoom matches are first-name false-positives (flagged via match_score).
- NEXT: b51c attaches email(mailing 842)+phone(contacts) onto 382-row spine, ranks by performances_lifetime, ships final table. Then Max reviews.
