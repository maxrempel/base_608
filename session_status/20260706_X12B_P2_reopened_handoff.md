# X12B P2 HANDOFF - REOPENED + CALIBRATED (2026-07-06). DO NOT CLOSE P2 NEGATIVE.

## STATE
Max rejected the 108,606->45->0 filtering funnel as signal-HIDING. Reopened P2 calibrated.
Key results (all committed, outputs/real/P2_REOPENED_calibrated_findings_v01.md):
- Read test OVERTURNED the old "dropout artifact": recurrent loci ARE genuinely non-parental
  (parents 0 alt reads) but MOSAIC (child VAF~0.25). Calibrated vs all 3202 samples = mix of
  site-noise / polymorphism / culture-mosaic.
- DIRECTIONAL null (noise-immune probe): chr21 bulk ancFrac real 0.243 vs scram 0.232 (+0.011,
  flat); chr22 clean-recurrent-residual GLOBAL real 0.087 vs scram 0.127 (derived-biased) = NO
  archaic-reversion excess on the pilot.
- No coherent 5% subpopulation on shared-loci (carriers differ per locus, overlap at chance).

## THE ONE DECISIVE TEST STILL OWED (blocked by infra, has a known fix)
PER-CHILD directional TAIL test = does a ~5% high-reversion SUBGROUP hide under the flat global?
X12F's direction_tail_test_v01.py is VALIDATED (recovers a planted 10% subgroup, p=1e-76). It needs
a per_child.tsv with columns: child_id, n_anc_calls, n_ancestral, n_refder, n_refder_rev.
BLOCKER + FIX: my per-child extractor used 1020 RANDOM per-locus pysam fetches on the 28GB remote
chr22 VCF -> the https handle CORRUPTS ("Illegal seek") after ~30 loci. FIX (proven: chr21 bulk
streamed 392k sites fine sequentially): use ONE SEQUENTIAL fetch over a range and filter to the
target positions - do NOT do random per-locus seeks. i.e. `for rec in vf.fetch("chr22", minpos,
maxpos): if rec.pos in target_set: ...` accumulate per-child ancestral-vs-derived on X12F's
chr22_clean_residual_positions.tsv (1020 loci). Ancestral base from
~/xg1/anc/homo_sapiens_ancestor_GRCh38/homo_sapiens_ancestor_22.fa (uppercase ACGT only).
Then: python scripts/direction_tail_test_v01.py --per-child <tsv> --stratum der.

## BOX (AWS)
i-00c83a0af889f8bf1, us-east-1, STOPPED (restart to continue). ec2-user@<new IP>, key
C:/Users/maxre/Nextcloud/zSyncMain/ssh/xg1_aws.pem. Has pysam (pip --user), g1k.ped at ~/xg1/g1k.ped,
ancestral FASTAs at ~/xg1/anc/. Only 9.8G free (CANNOT download 28GB VCF; no bcftools/tabix - dnf
lacks it). VCF url pattern: https://1000genomes.s3.amazonaws.com/1000G_2504_high_coverage/working/
20201028_3202_raw_GT_with_annot/20201028_CCDG_14151_B01_GRM_WGS_2020-08-05_chr{N}.recalibrated_variants.vcf.gz
Scripts left on box: ~/nulltest.py (permutation+direction), ~/perchild.py (per-child, needs the
sequential-fetch fix), ~/recur_readtest.py, ~/calib.py, ~/subpop.py.

## NEXT (calibrated, never-close)
1. Finish per-child tail test with the sequential-fetch fix (above) -> Max's confound-immune verdict.
2. Scale directional + recurrence-excess null GENOME-WIDE (pilot was chr21+chr22 only).
3. PER-PERSON BURDEN test: are outlier children (HG02650 6.7sigma etc) candidate hybrid INDIVIDUALS
   (elevated real-mosaic-nonparental burden vs permutation null) - NOT "bad samples" (I dismissed
   them circularly). Needs reads (box/VCF).
4. Consider a bigger-disk box or bcftools install so VCFs can be pulled local = reliable + fast.

## UPDATE (later 2026-07-06): GENOME-WIDE directional run LAUNCHED (the powered subgroup test)
chr22 pilot per-child test was UNDERPOWERED (mean 1.04 clean-stratum sites/child, 0 kids >=20).
So launched the SAME single-pass streamer GENOME-WIDE to accumulate ~22x sites.
- Box i-00c83a0af889f8bf1 us-east-1 (RUNNING), IP /tmp/boxip.txt (100.54.119.100 at launch).
- Driver: ~/gw_run.sh (PID 4911), 6-way parallel over chr1..22, RESUMABLE (per-chrom ~/gw/chrN.done,
  final ~/gw/ALLDONE). Positions: ~/gw/pos_chrN.tsv (split from recurrent_maskfree_v01.tsv, 27,078 loci).
  Output per chrom: ~/gw/arch_chrN.per_child.tsv. ETA ~1hr from ~18:20.
COLLECT WHEN ~/gw/ALLDONE (or 22 .done markers):
1. scp ec2-user@<IP>:~/gw/arch_chr*.per_child.tsv to outputs/real/gw/.
2. MERGE per child_id (sum columns n_npa,n_anc_calls,n_ancestral,n_refder,n_refder_rev across chroms)
   -> outputs/real/gw_merged.per_child.tsv (same header as chr22 per_child).
3. python scripts/direction_tail_test_v01.py --per-child outputs/real/gw_merged.per_child.tsv --stratum der (+ --stratum all).
4. VERDICT: n_high >> null_max (p<Bonferroni), ~2-10% of kids = archaic-reversion SUBGROUP trace
   (noise cant fake) -> REPORT MAX LOUD + name top-tail kids for close-look + cross-post team.
   Else within-null = calibrated no-subgroup GENOME-WIDE (honest, now POWERED - the real answer).
   Watch: is n_refder/child now >=20 (powered)? If still low, clean stratum is just rare -> report
   that limit honestly.
5. commit + board post + STOP box (aws ec2 stop-instances i-00c83a0af889f8bf1 --region us-east-1).

## CORRECTION (X12F): ref=DER stratum is TAUTOLOGICAL (NP allele always = ALT -> DER-reversion is a
## fixed SITE property, not per-person). Genome-wide does NOT fix that. The VALID powered subgroup
## test = per-child GLOBAL reversion (--stratum all: n_anc_calls/n_ancestral, which the gw run DOES
## emit, ~220/child genome-wide = powered) vs a SCRAMBLED-PARENT permutation null (X12F adding
## --permute to direction_tail_test). COLLECTION step 4 becomes:
##   python scripts/direction_tail_test_v01.py --per-child outputs/real/gw_merged.per_child.tsv --stratum all --permute
## Look for a ~5% tail of children whose global reversion EXCEEDS their own scrambled-parent null.
## (Cohort-level real<scram already = derived-biased/no-excess on chr21+chr22; the subgroup test asks
## if a minority bucks it.) DER stratum = ignore (tautological).

## FOLLOW-UP TOOL (X12F): permute_direction_v01.py = definitive non-tautological subgroup test
(real + scrambled-parent per-child reversion + z, one stream). DEFINITIVE workflow:
  per chrom: aws s3 cp <chrN.vcf.gz> - --region us-east-1 | python scripts/permute_direction_v01.py \
    --vcf - --ped <g1k.ped> --use-aa-field --permute 20 --out outputs/real/permdir_chrN.tsv --chrom-label chrN
  merge across chroms (X12F writing merge helper: sum real counts, pool scram per-perm) -> permdir_merged.tsv
  then: python scripts/direction_tail_test_v01.py --per-child permdir_merged.tsv --permute
  = UNDERPOWERED / SIGNAL-SHAPED(~5% tail beats own scrambled null, z>3) / NO-SUBGROUP.
FIRST-PASS (cheaper, uses the archaic gw run already done): direction_tail_test --stratum all (binomial
null) on gw_merged.per_child.tsv - powered per-child global-reversion subgroup read; permdir = clean confirm.
Note --use-aa-field needs the VCF AA INFO field; if the recalibrated VCF lacks AA in header (chr22 did),
pass --ancestral <chrN ancestral fa> instead (fastas on box ~/xg1/anc/...).

## DEFINITIVE PIPELINE COMPLETE (X12F, validated - merge==single-pass, max|dz|=0). USE THIS:
Per chrom (CRITICAL: identical --permute 20 --seed 13 on EVERY chrom so scrambles pool):
  aws s3 cp <chrN.vcf.gz> - --region us-east-1 | python scripts/permute_direction_v01.py \
    --vcf - --ped <g1k.ped> --use-aa-field --permute 20 --seed 13 --out permdir_chrN.tsv --chrom-label chrN
  (if VCF lacks AA header, use --ancestral ~/xg1/anc/homo_sapiens_ancestor_GRCh38/homo_sapiens_ancestor_N.fa)
Then: python scripts/merge_permdir_v01.py --out permdir_merged.tsv permdir_chr*.tsv
Then: python scripts/direction_tail_test_v01.py --per-child permdir_merged.tsv --permute  = SUBGROUP VERDICT
  (UNDERPOWERED / SIGNAL-SHAPED ~5% tail beats own scrambled null z>3 / NO-SUBGROUP).
This is the whole remaining job - a fresh session can drive it start-to-finish on the box.

## MAX'S ACTUAL AGENDA (2026-07-06 pm, live-steered) - THIS is the real work, drop the per-child ancestry machinery:
Max wants NPAs CATALOGED then analyzed by HIS hypotheses (aggregate/descriptive, not significance-hunting):
1. CATALOG the NPAs: per-SNP + per-region tables from genome_out (local), + population(ped) + recurrence(#distinct kids per chrom:pos). [outputs/real/NPA_catalog_perSNP.tsv + perRegion.tsv]
2. ANCIENT vs MODERN DRIFT **BY CATEGORY** (both_hom/both_het=DOCHAN, not_from_father, not_from_mother, other): aggregate ancient(ancestral):modern(derived) per category, in the ref=DER bias-CLEAN stratum (ref=ANC is bias-inflated-to-modern). RAW result chr21-22 = ~90% modern BUT that's ~tautological (NPA allele=ALT=non-ref=modern) + reference-mapping bias -> the CLEAN by-category number is the real test. Script: ~/catdrift.py on box (STDIN iterate `for rec in vf:` NOT fetch; streams aws s3 cp - | catdrift.py chrN <ancestral fa>). Running chr20/21/22.
3. HOTSPOTS reproducible in a SMALL % of population, genome-wide (paper hotspots extended) -> then OVERLAY onto a GENE SET (Max said "autistic" = autism/neuro genes? CONFIRM which set - SFARI?). Use exact_payload_gate.tsv / recurrence data (already have recurrence per site).
4. HAPLOTYPES where NPAs CLUSTER: cluster by FAMILY and by LOCATION (genomic). From the catalog.
Reference-bias caveat applies to anything ancestral/modern. NO per-child significance / population-subgroup machinery (Max found that confusing + off-target). Aggregate + descriptive + catalog.

## LIVE JOB STATE (2026-07-06 ~21:40, X12B context ~80% -> handing off):
- Box i-00c83a0af889f8bf1 us-east-1 RUNNING, IP in /tmp/boxip.txt (44.223.76.117).
- CATEGORY-DRIFT jobs running: ~/catdrift.py on chr20/21/22 (aws s3 cp - | catdrift.py chrN <anc.fa>),
  outputs ~/catdrift_chr{20,21,22}.out, ~15-20min from 21:40 (Python parse of 3202-sample lines is slow).
  COLLECT: cat the 3 .out (category x refanc/refder x ancient/modern/ancient_frac), merge, report the
  ref=DER clean-stratum ancient:modern PER CATEGORY to Max. Then STOP box.
- NPA CATALOG (task 2) not built yet - LOCAL from genome_out (no box). Script per agenda.
- Raw drift so far (chr21-22 pooled, all NPA): ~90% modern/~10% ancient, but tautological+refbias;
  by-category clean-stratum is the real number (pending above).
