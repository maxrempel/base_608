
## [2026-06-07 14:40] ? ????????
- DID: DEPLOYED catalog to live: 1371 -> 26430 rows. Backup saved (archive/data_live_backup_...1371rows.json), deploy_catalog.py + rollback_catalog.py written. Verified LIVE URL serves 26430 rows, 0 malformed links
- STATE: Catalog LIVE at tamza.com/kartoteka, 19.3x. Fully reversible via rollback_catalog.py. Channel desc-DB crawl still running (a14c5ed8)
- NEXT: Watch for dead-link feedback; rollback ready; pending housekeeping = leftover worktrees agent-a152f918+agent-a9bce83d; channel-DB crawl will inform a future liveness pass

## [2026-06-08 11:15] ? ????????
- DID: C3 ran c5's two read-only lanes on the monthly-pipeline candidate. LANE A: independently re-derived G4/I1 for all 18 recent (>2025-12-06) tabs from source xlsx - exactly 4 suspect (03-01,05-16,05-30,06-06), match hidden log; 2026-05-23 has g4 real + i1=240 so correctly NOT hidden (no over-hide); no affected tab missed. Descriptions for the 4 are EMPTY (0 timecodes) so desc-ground-truth genuinely cannot cross-check - in-sheet marker is the only offline truth. LANE B: data 26283 = legacy 26046 + recent 237 exact; 0 dates in both layers; 0 merge dup/drop; frozen base BYTE-IDENTICAL to live<=cutoff (0/0 diff). b0 off-by-1 RESOLVED = benign: fresh parser found 371 recent vs old 370 (+1 recovered row), not a seam dup.
- STATE: Both lanes DONE, findings ready to post to c5. Read-only, touched nothing.
- NEXT: Post report to c5; await next assignment; keep 240s timer.
