
## [2026-07-02 21:19] ? 14c38ae7
- DID: X9A checked in as INVERSION lane for Kristen Kenefick XG1 case (manager X7A). Found her DELIVERED Manta SV VCF has ZERO inversions - vendor filter (ABS(SVLEN)<=100000) stripped all BND-encoded inversions. Installing Manta on asto to re-call INVs from her 32GB BAM.
- STATE: Manta conda env installing on asto (~/genomics/_analysis/x9a_inversions/); GRCh38 ref + BAM present, 930G free. gnomAD-SV v4.1 staged for annotation.
- NEXT: Run Manta on Kristen BAM (detached), extract INV/BND, count+size dist, annotate vs gnomAD-SV INV + known common inversions (8p23.1, 17q21.31/MAPT), estimate artifact fraction. Then same caller on X8A control genomes.

## [2026-07-02 21:26] ? 14c38ae7
- DID: X9A: first Manta run failed (ref mismatch: BAM has 2581 contigs incl decoy, GRCh38_main.fa only 25; bgzip/tabix absent in manta_env). Fixed with v2: subset Kristen BAM to 25 main chroms + reheader to drop decoy @SQ, Manta vs GRCh38_main.fa, post-process with /usr/bin/bcftools.
- STATE: v2 launched detached on asto (pid 1642208), subsetting 32GB BAM then Manta 8-job. run_v2.log in ~/genomics/_analysis/x9a_inversions/
- NEXT: Poll for INV counts; convertInversion BND->INV; report homozygous(1/1) INV count + PASS/artifact split to X7A. Then same on Oliver + controls.

## [2026-07-02 22:00] ? 14c38ae7
- DID: X9A: v2 subset BAM failed to index ('Numerical result out of range') - region-ordered output vs header order sort quirk (RIDs confirmed VALID: header order is 1..22,X,Y,MT,decoys so reheader preserved contig-ID mapping). v3 fix: samtools sort the main.bam then index then Manta.
- STATE: v3 launched detached (pid 1647933), run_v3.log. Controls: X8A pulling 1000G NYGC 30x CRAMs (NA18488/NA18534/HG00125) + Ashkenazi trio HG002/3/4 for parent-child inversion-sharing test; GRCh38DH chr-ref for those.
- NEXT: Poll v3 for homozygous-INV count; deliver count table row to X7A; run identical Manta on controls when they land.

## [2026-07-02 22:41] ? 14c38ae7
- DID: X9A: v3 failed (subset BAM was corrupt/truncated from streamed reheader; sort failed instantly + my rm deleted it). v4 = robust fix: run Manta on ORIGINAL intact indexed BAM + name-matched reference (real 25 main chroms from GRCh38_main.fa + N-padded decoy placeholders at exact BAM-header lengths) + --callRegions main.bed. Main lengths verified matching.
- STATE: v4 RUNNING on asto (pid 1653720) - Manta workflow past locus-graph, now generateCandidateSV. run_v4.log. ~1-2hr to INV counts.
- NEXT: Poll v4; deliver homozygous-INV count (PASS vs artifact) to X7A; annotate vs gnomAD-SV INV + known common inversions; run same on controls.

## [2026-07-02 23:26] ? 14c38ae7
- DID: X9A CORE LANE DONE: Kristen inversions re-called (Manta v4), committed+pushed (7c35e768). homozygous=29, total PASS=263; refutes '1500 homozygous'. Court-grade vendor-filter finding documented. gnomAD annotated (42 strict-known, 219/263 in known INV regions). X7A drafted email 03 with these.
- STATE: Blocked on X8A control CRAMs (none staged yet). Ready-to-fire control script staged: ~/genomics/_analysis/x9a_inversions/x9a_control_inv.sh (runs identical Manta on a CRAM+chr-ref, main chroms, counts homozygous INV).
- NEXT: When X8A lands 1000G controls + HG002/HG003 pair on asto: run x9a_control_inv.sh per sample -> deliver control homozygous-INV counts + parent-child shared-INV number to X7A for count table + email 03.

## [2026-07-03 06:21] ? 14c38ae7
- DID: X9A: X8A's control downloads kept dying (not detached). Took over control lane end-to-end (X7A confirmed, X8A stood down). Relaunched as ONE setsid-detached job on asto: downloads GRCh38DH ref + 3 unrelated 1000G 30x CRAMs (NA12718 CEU/NA18530 CHB/NA18488 YRI) + runs identical Manta inversions on each.
- STATE: RUNNING detached (script pid 1723850, log ~/genomics/controls/x9a_full.log). Ref downloading (354MB/3.26GB). Then 3x CRAM (~14GB each) + Manta each. ETA ~4-9hr (slow FTP ~1.5MB/s). Core Kristen result already done+pushed (7c35e768).
- NEXT: Poll x9a_full.log for per-control homozygous-INV counts; compute pairwise shared-INV among controls (defuses 'son shares 1500' via unrelated-sharing); post count table to X7A/board; update analysis doc + commit.

## [2026-07-03 07:07] ? 14c38ae7
- DID: X9A: control ref down (3.26GB). NA12718 downloading via main job; parallelized NA18530+NA18488 (nohup wget -c, same filenames) to cut ~10hr serialized -> ~3-4hr since downloads are network-bound (not competing w/ X5's CPU Oliver sort). Main job runs Manta back-to-back as each CRAM completes.
- STATE: 3 parallel CRAM downloads running on asto (~1.2MB/s each, ~14GB each). Job pid 1723850 alive. Core Kristen result done+pushed. Oliver chain: x1 transfers fastq -> X5 aligns -> I run mother-son Manta.
- NEXT: Poll for CRAM completion + control homozygous-INV counts; compute pairwise shared-INV; post count table + update analysis doc + commit.

## [2026-07-03 09:45] ? 14c38ae7
- DID: X9A: Pine restarted; confirmed control job + 3 parallel wgets SURVIVED (setsid on asto, remote). Downloads ~50%: NA12718 8.3G, NA18488 6.8G, NA18530 3.6G of ~14G. Oliver align running (X5, shepherded by X10A). Kristen inversion result done+pushed.
- STATE: Waiting on control CRAM downloads to finish (~1.5-2hr) then main job auto-runs Manta on each. Job pid 1723850 alive.
- NEXT: Poll for control homozygous-INV counts; pairwise shared-INV; count table to X7A; run Manta on oliver.fixed.bam when X10A pings; update doc+commit.

## [2026-07-03 09:57] ? 14c38ae7
- DID: X9A LESSON: parallelizing the 3 control downloads BACKFIRED - asto/ENA link is total-bandwidth-capped, so 3 streams split the same pipe + overhead (aggregate dropped to ~0.7MB/s vs 1.2 single). Reverted to SERIAL (killed 2 extra wgets; partials preserved for wget -c resume). NA12718 now at full bandwidth.
- STATE: NA12718 9.1G/14G downloading solo (~1hr left) -> main job auto-Manta -> FIRST control count. Then job resumes NA18530(4.0G)/NA18488(7.3G) serially. Job pid 1723850 alive on asto.
- NEXT: Poll ~90min for NA12718 homozygous-INV count; then remaining 2; pairwise shared-INV; count table to X7A. Oliver BAM ~1-2h (X5) for mother-son Manta.

## [2026-07-03 11:43] ? 14c38ae7
- DID: X9A: Max requested bandwidth throttle (asto = Liz's house, wife needs bandwidth). Measured asto line ~1.66 MB/s (~13 Mbps, slow shared link). Killed unthrottled orchestrator (NA12718 Manta preserved, orphaned+running). Deployed throttle_daemon.sh: measures line each loop, caps wget --limit-rate at 70% day (07-23) / 85% night, re-measures every <=3h. Now running NA18530 at cap=1160KB/s.
- STATE: NA12718 Manta finishing (~1hr, result pending). throttle_daemon downloading NA18530 (4/16GB) throttled, then Manta, then NA18488. Household keeps ~30% headroom. log: throttle_daemon.log.
- NEXT: Report NA12718 count when it lands; NA18530/NA18488 counts as they complete (~3hr each throttled); pairwise shared-INV; count table to X7A; Oliver mother-son Manta when X5's BAM lands.

## [2026-07-04 07:12] ? 14c38ae7
- DID: X9A: CAUGHT SILENT FAILURE - NA18530/NA18488 Manta ran on HOST (via throttle daemon's bash call) where /usr/bin/samtools+bcftools don't exist (only in distrobox), so NO manta output despite 'COMPLETE' in log. CRAMs fully downloaded (16G each). Relaunched rerun_manta.sh INSIDE distrobox, niced 15, detached (Sat 07-04 10:12).
- STATE: NA18530 Manta running inside distrobox now, then NA18488. ~1.5hr each. Kristen(29/263)+NA12718(28/310) done+committed w/ full artifact analysis. Oliver BAM was aligning (X5) - check if landed for mother-son shared-INV.
- NEXT: Poll rerun_manta.log for NA18530+NA18488 hom-INV counts; add rows to table+doc+commit; run x9a_shared_inv.sh between controls (unrelated-sharing) + Kristen-Oliver when BAM ready; final table to X7A.

## [2026-07-04 11:13] ? 14c38ae7
- DID: X9A: control table 2/3 done+committed: Kristen 29 / NA12718 28 / NA18530 40 homozygous PASS INV. Controls span 28-40, Kristen LOW end. NA18488 first 2 attempts failed (host-run, then launch-race). rerun2 now genuinely running inside distrobox (na18488_fix2.log, load free ~6).
- STATE: NA18488 rerun2 in progress (~1.5hr). Oliver.fixed.bam not yet landed (align finishing, load 6). x9a_shared_inv.sh staged for Kristen-Oliver mother-son test.
- NEXT: Poll NA18488 count + Oliver BAM; when Oliver lands run Manta on it + x9a_shared_inv.sh Kristen-vs-Oliver AND control-vs-control (unrelated sharing); final table + shared-INV to X7A; commit.

## [2026-07-04 16:48] ? 14c38ae7
- DID: X9A: Oliver BAM landed (X5, 65.8GB, main-ref bare-chrom, 25 contigs). Launched Oliver mother-son Manta on asto (idle) + auto shared-INV Kristen-vs-Oliver. Inversion lane already letter-complete: Kristen 29/NA12718 28/NA18530 40 + unrelated 55% sharing baseline. NA18488 dropped (corrupt CRAM).
- STATE: Oliver Manta running (oliver_run.log), ETA ~1-1.5h, then Kristen-Oliver shared-INV number. All Kristen letter beats answered+committed.
- NEXT: Poll oliver_run.log for Kristen-Oliver shared-INV; post final number to X7A; that fully closes X9A inversion lane.
