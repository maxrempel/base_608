# OMEGA GRCh37 v02 manager-verification note

Last edited: 2026-08-03 by Codex (GPT-5.6 SOL)

Draft a concise, privacy-safe engineering verification note from these frozen aggregate facts. Maximum 800 words. Do not invent claims or propose threshold tuning.

Assets:
- Corrected runtime contract commit 83c7ac1f independently verified.
- hs37d5 compressed/decompressed/FAI exact registered hashes; BAM SQ order matched 86/86.
- Numeric hg19 genomicSuperDups-derived BED exact registered hash and 39,747 rows.
- No GIAB Tier1 detector mask and no third clean BED; clean-region remains local low-MAPQ fraction <=40%.
- Immutable wrapper binds frozen omega_junction_v02.py SHA e42c5a68..., with unchanged discovery scripts and thresholds.

Exposed regressions only:
- Synthetic: 100-bp exact 1/1; corrected 5,000-bp remains unresolved; no false exact.
- Old exposed GIAB32: v01 candidate 22/32, accepted 7/32. v02 candidate 22/32, accepted 9/32. v02 made 2 exact-length calls, 0 correct and 2 false exact. No retained prespecified exact-junction coordinate tolerance, so exact junction was not scored.
- Protected exposed 3-real/3-sham panel: both v01 and v02 recovered 1/3 locus windows, 1/3 junction classes, 0/3 exact coordinate-plus-payload, and 0/3 sham windows.
- Repeated exposed coded smoke: PAF, v02 hit table, and payload hashes identical across two independent runs.
- First two service attempts were killed by systemd-oomd because MemoryHigh was below the mapper working set. Per-locus checkpoints preserved 22 units. The scoped 13/14 GiB retry completed the remaining units with zero restarts, 11.2 GiB peak, zero swap, and no storage/kernel faults.

Boundary:
- These are exposed engineering controls, not the sealed 96-row v02.1 blind panel.
- False exact length calls mean length claims remain prohibited.
- Exact reconstruction remains unvalidated.
- No biological claim, no correction factor, no threshold/code repair.
- Stop for manager verification before opening or executing the sealed 96-row panel.

Return: opening decision, compact evidence table in Markdown, interpretation, immutable identities/checksum note, resource incident/repair note, and explicit stop/next authorization required.
