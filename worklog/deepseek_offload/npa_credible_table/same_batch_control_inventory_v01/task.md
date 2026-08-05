Review this deidentified inventory for the next NPA falsification unit. Do not invent data.

Goal: determine whether an accepted same-platform/same-batch public trio control set exists beyond two PJL controls, and recommend the smallest defensible next step.

Evidence:
- Frozen connected-locus pilot: 24 signal regions, 72 aggregate rows.
- Signal child: callable depth >=20 in 20/24 rows; strict connected-locus pass 0/5; alt-bearing 24/24; both strands 20/24; median alt MAPQ 23; batch signature differs from both controls.
- PJL control A HG02495: callable 24/24; strict pass 1/5; alt-bearing 14/24; both strands 9/24; median alt MAPQ 19; batch signature differs from signal.
- PJL control B HG02605: callable 18/24; strict pass 0/5; alt-bearing 7/24; both strands 2/24; median alt MAPQ 2; batch signature differs from signal.
- Candidate table lists 3 primary PJL sex-2 controls (HG02495, HG02605, HG02653) and 7 alternates (HG02659, HG02662, HG02692, HG02726, HG02776, HG02785, HG02788).
- Accepted deployment family manifest has 61 data rows but only three targeted complete families: PK16/HG02683, BB23/HG02280, PR26/HG01087. Source-recovery manifest has 9 lines and only those same three families' role files. No accepted CRAM/CRAI handoff or same-batch read-group manifest is recorded for the remaining candidate controls. HG02653 is unavailable and must not be treated as zero.
- Public sources use GRCh38 full analysis set plus decoy HLA and Illumina. Existing read-group signatures show shared Illumina platform but distinct flowcell/library signatures; exact same-batch matching is not established.

Return a compact recommendation with: (1) whether exact same-batch controls exist, (2) the narrowest result-producing bypass, (3) predeclared control selection and denominators, (4) falsification criteria, and (5) what cannot be concluded. Keep phenotype sealed.
