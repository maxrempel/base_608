---
name: Q38 download session notes v01
description: State of the open-access long-read trio downloader as of 2026-08-06: what exists on Green24, the checksum repair, bandwidth policy, and the extension queue from the saturated census v03.
type: project
last_edited: 2026-08-06 by Codex (DeepSeek takeover of Q38 download)
---

# Q38 download session notes v01 (takeover from Qwen session)

## What exists on Green24 (as of 2026-08-06 ~14:30 PDT)

Data root: `/mnt/green24/1kgp_longread_trios/` with `data/`, `state/`, `logs/`, `software/`.

| Family | Resource | Status | Files |
|---|---|---|---|
| 1_HG00514 | HGSVC3 | checksum repair | 6 files on disk, 3 verified |
| 2_NA19240 | HGSVC3 | checksum repair | 6 files on disk, 4 verified |
| 3_HG00733 | HGSVC3 | complete | 6/6 |
| 4_HG03371 | LRSC500 | complete | 6/6 |
| 5_HG00706 | LRSC500 | complete | 6/6 |
| 6_HG02024 | LRSC500 | complete | 6/6 |
| 7_HG02615 | LRSC500 | complete | 6/6 |

~85 GB on disk. Families 1-2 fail MD5 verification (byte sizes match; manifest checksums are wrong or files corrupt). Ground-truth checksums are being computed by streaming each file from EBI (background job, 2026-08-06).

## Checksum repair procedure

1. Stream each failing file from EBI, compute md5, compare with the local file's md5 (recorded in the download logs as "got").
2. If local md5 == server md5: the manifest md5 is wrong. Update `ASSEMBLY_MANIFEST_v01.tsv` md5 column AND the `expected_md5` field in `state/<family>.json`, then restart the family service; it verifies and completes.
3. If local md5 != server md5: quarantine the local file under `state/quarantine/` and re-download.
4. Never delete partials.

Known transient EBI behavior on 2026-08-06: plain GETs intermittently returned 404 (several minutes at a time). Retry with backoff; a ranged request after a wait usually succeeds. The downloader already retries HTTP errors (30 attempts, 30 s apart).

## Bandwidth policy (Max, 2026-08-06)

Home line measured 500 Mbps. Two concurrent family streams. `run_downloader_v01.sh` sets the per-family cap by hour: 15,000 KiB/s (daytime 07:00-23:00, total ~250 Mbps) and 21,000 KiB/s (nighttime, total ~350 Mbps). If the source serves slower, no extra limiting applies.

## Extension queue from census v03 (33 unique families / 36 trios)

Assembly-first additions to the manifest (beyond the original 13):

| Source | Members | Payload | Source of truth |
|---|---|---|---|
| Platinum Pedigree (F18-F32 + F08/F09 overlap) | 23 open | 120.5 GB (Verkko 11 members, hifiasm 12 members) | s3://platinum-pedigree-data/assemblies/<ID>/ |
| PAN027 / WashU (F17) | 4 (trio = 3) | 24.6 GB v1.3.1 | public.gi.ucsc.edu/~mcechova/pedigree/assemblies/v1.3.1/ |
| T2T-CQ (F16) | 4 | TBD (GWH) | GWHFQEY00000000.1 + GWHFQEX00000000.1 |
| APR trio (F33) | 3 | ~18 GB est | GenBank / mbru.ac.ae |
| HG002 T2T (F14) | 1 (child) | TBD | GIAB FTP / human-pangenomics S3 |
| Vienna reads (F08-F13) | 18 | ~162 GB | 1KG_ONT_VIENNA FTP + ENA PRJEB89727 |
| GIAB Chinese reads (F15) | 3 | deferred | GIAB FTP ChineseTrio |

## Machine facts

- Taygeta 1 (CyberPowerPC) is the live download host; Green24 mounted at /mnt/green24, ~21 TB free. Taygeta 2 (Dell) arrives 2026-08-07 night; 3-day migration window. Everything durable lives on Green24; this repo is the GitHub backup.
- Live software checkout on Taygeta: `/home/maxre/1kgp_longread_trios/` (NOT a git repo; this folder is the canonical copy).
- Report auto-refreshes every 3 hours via Windows scheduled task `Q38DownloadReportRefresh` (hidden) -> `C:\base_608\xg1\download_families_60806\REPORT.md`.

## Update 2026-08-06 evening (DeepSeek takeover, active session)

### Families 1-7: COMPLETE and verified

The 5 corrupt HGSVC3 files (HG00512.hap2, HG00513.hap2, HG00514.hap2, NA19239.hap1, NA19240.hap1) were quarantined under `state/quarantine/` with `.gzip-invalid-truncated.*` names. The downloader was patched to re-download on failed verification, and all of families 1-3 (HGSVC3) and 4-7 (LRSC500) are now complete: 6/6 files each, ~85 GB total. PROGRESS.md under `state/` is the live table.

### Root cause of the pp_200080 / pp_200100 restart loop: FIXED

Platinum Pedigree files K1463_200080_*.fasta.gz and K1463_200100_*.fasta.gz are gzip-compressed. The verify() structure check read raw bytes, so every valid .gz file looked like "not a complete FASTA" (first byte = gzip magic 0x1f), the downloader quarantined it, re-downloaded, failed again, forever. Downloads were never corrupt; the check was wrong for compressed files.

Fix (assembly_downloader_v01.py): new `fa_structure_ok()` decompresses .gz files (validates CRC + first byte `>` + last byte newline); plain FASTA keeps the fast path. Verified on Taygeta: valid gz -> True, truncated gz -> False, plain fa -> True. Deployed to live checkout `/home/maxre/1kgp_longread_trios/software/`, Green24 mirror, and this repo. Services restarted; pp_200080 complete, pp_200100 finished 1/2 and re-downloading file 2 with the fixed verifier.

### Resumable download watcher (Max request)

New Windows scheduled task `Q38DownloadWatch` (hidden, every 30 minutes, survives session and machine restarts) runs `C:\base_608\xg1\download_families_60806\watch_downloads.ps1`. It SSHes to Taygeta via the Asto jump, snapshots PROGRESS.md + active services + anomalies (failed/verify_failed families) + disk, stores `watch_state.json`, and appends to `watch_alerts.log` on: new anomalies, anomalies cleared, newly completed families, or a downloading family with identical byte counts for 2 consecutive cycles (60 min stall). On an event it also refreshes REPORT.md. First run 2026-08-06 20:32 PDT; it correctly reported the 18 completed units and the pp_200100 anomaly that is now clearing.

### Queue position

Assembly phase: 18 of 33 family units complete (all 7 original trios + 11 Platinum units). Remaining: pp_200100 (finishing), pp_NA12877/78/79/81/82/85/86/89/90/91/92 (Platinum Verkko members), then pan027_HG06803/04/07/08. Supervisor auto-advances 3 concurrent families. After all assemblies, the supervisor switches to the Vienna aligned-reads manifest (8-13). Bandwidth policy as reported: day 7000 KiB/s per family x 3 = ~168 Mbps total; night 9000 KiB/s per family.

### Watch cadence (Max, 2026-08-06 20:40 PDT)

- Session wakes armed via wakeup skill: recurring every 20 min (id 383ef0ac, first 21:00 PDT) to check progress and push the queue; one-time wake at 23:35 PDT (id 81fc36d7) to switch the session cadence to every 45 min.
- Windows task Q38DownloadWatch runs every 20 min until 23:36 PDT, when one-time task Q38DownloadWatchCadence45 re-creates it with 45 min and removes itself (script `switch_watch_cadence.ps1`).
- Live state: 3 families at full concurrency (pp_NA12877/78/79), rest queued; supervisor auto-advances.

### Open items (from handoff)

- T2T-CQ (F16): GWH API returns nulls; try the GWH browse page / download.cncb.ac.cn path, verify parents' v2.0 accessions.
- APR trio (F33): map APR-F/M/S to aprNNN IDs via paper Supplementary Table 1 (Europe PMC 41467_2025_61645_MOESM2_ESM.xlsx).
- HG002 T2T (F14): human-pangenomics S3 path is a delete-marker; find current T2T-HG002 v2.7/v1.x FASTAs.
- Vienna reads: get exact sizes for the 5 members missing from vienna_manifest_full.tsv from the FTP listing.
- Migration prep: confirm all durable state on Green24 + GitHub before Taygeta 1 return; recheck Green24 USB speed on Taygeta 2 (aim 5000M/10000M).

## Update 2026-08-07 morning (after Pine slept ~7 hours)

- Overnight the queue finished the whole assembly phase (all 34 units) and auto-advanced to the aligned-reads phase. Reads are the HGSVC3 20250307 HiFi T2T BAM alignments for all 13 read-families (r1-r13), ~3.4 TB total, from EBI. Census v04 (32 families / 34 trios, T2T-CQ removed) is in the sibling census branch; REPORT.md updated.
- r1 and r2 ran overnight at EBI-limited speed (~1.5 MB/s per family, ~40 GB each in 7.5 h). PROGRESS.md showed stale byte counts during long files, so the watcher logged false STALLED alerts at 00:21. Root cause: the downloader only persisted state when a file finished.
- Fixes deployed and committed:
  - downloader now persists downloaded_bytes every 60 s during transfer, so PROGRESS.md and the report show live bytes (verified: PROGRESS now matches du).
  - resume_aligned MAX_ACTIVE raised 2 -> 4; r1-r5 are now downloading concurrently (r4 had failed to auto-start, started manually). Watch task already on 45-min cadence (OS switch ran 23:36); session wake 27779eae now 45-min recurring (20-min wake 383ef0ac cancelled).
- ETA for the 3.4 TB reads at current EBI speeds: several days. Concurrency is capped by the 250 Mbps day policy at 4 families on paper; actual usage stays near 60-100 Mbps because EBI is the bottleneck.

## Incident 2026-08-07 afternoon: Green24 USB re-enumeration (resolved)

At ~15:46 PDT the downloads stopped with I/O errors. Root cause: the Green24 USB drive re-enumerated on the USB bus and its device letter changed from /dev/sdi to /dev/sdj, so the old mount at /mnt/green24 (still pointing at sdi) went stale. All reads/writes returned "Input/output error", the downloader services crashed with OSError Errno 5, hit their restart limits (StartLimitBurst), and went failed. The data itself was never lost.

Recovery (with Taygeta sudo password from Bitwarden "Taygeta administrator login", never printed):
1. Stopped the supervisor to stop retry churn against the dead mount.
2. `sudo umount /mnt/green24`, then `sudo mount /mnt/green24` (reads fstab, which uses UUID=7B5F-D16C and uid=1000,gid=1000,umask=022). A plain `mount -U` without fstab options mounted as root and caused PermissionError on the state lock files; the second mount fixed ownership (state dir now maxre:maxre, write OK).
3. `systemctl --user reset-failed kgp-aligned-dl-v01@r1..r9` then started r1-r5 (r6-r9 came back too); all 9 read families active and resuming partials via HTTP Range.
4. Partial files resumed normally; EBI-truncated files (r4/r5 had verify_failed) are re-downloaded by the downloader's quarantine loop.

Hardening notes for migration: fstab already uses UUID + nofail, so a reboot auto-mounts correctly; the failure mode is a mid-run USB re-enumeration, which no mount option prevents. A udev/systemd automount rule for /mnt/green24 by UUID would make this self-healing on Taygeta 2. Keep the watcher's "watch failed" alert as the tripwire.
