
## [2026-07-12 21:12] ? 501244df
- DID: X11 in P1 room, took X7A control-table task (Tables A/B/C, 5 genomes on asto ~/genomics/_analysis/kinship_5050/)
- STATE: starting bcftools counts on asto
- NEXT: run A+B counts, assess C feasibility, post table in p1 room

## [2026-07-12 21:18] ? 501244df
- DID: X11 P1: found control VCFs NOT apples-to-apples (kinship-purpose: 5 chroms, SNP-only, bcftools-not-vendor, no dbSNP). Consulted X7A with fix plan. Launched chr22 identical-pipeline pilot on asto (re-call Kristen+Oliver, count controls same region).
- STATE: pilot running bg id b9xwb8x26; awaiting X7A scope pick (5-chrom vs genome-wide)
- NEXT: read pilot result, post chr22 apples-to-apples table to X7A, then scale per X7A decision; still need dbSNP for Table B, H3F3B coverage for Table C

## [2026-07-12 21:27] ? 501244df
- DID: X11 P1: Table C done (H3F3B fully covered in all 5 = truncation claim refuted). chr22 pilot A/B: with .mq(no-markdup) K/O ran high (K92k O93k vs controls 67-84k); root cause = mpileup skips marked dups in control CRAMs but counts them in no-markdup K/O BAMs. Re-running chr22 with .fixed(markdup) K/O BAMs to match.
- STATE: markdup pilot bg id bx8i1bnlh running
- NEXT: read markdup chr22 numbers; if K/O now in control range, scale to 5 chroms; interpret vs ancestry (NA18488=YRI highest control). dbSNP still needed for Table B novel.

## [2026-07-12 21:41] ? 501244df
- DID: X11 P1: BREAKTHROUGH - root cause of K/O variant excess = primary-only alignment (25 contigs, no decoy) vs control full-analysis-set (3366 contigs). Fixed cheaply with 1000G strict-accessibility mask: chr22 masked counts Kristen 32.8k/Oliver 34k land IN control range (CEU 31.7k, YRI 42.7k); K/O keep only 36pct of raw vs controls 47-51pct = artifact confined to unreliable regions. Table C (H3F3B) done+clean. Scaling mask method to 5 chroms.
- STATE: 5-chrom scale running bg id btg0144c0 (resumable, per-chrom .done)
- NEXT: read 5-chrom totals, write results report to projects/XG1/kenefick, post final Table A+C to X7A; dbSNP for Table B only if X7A wants it

## [2026-07-12 23:29] ? 501244df
- DID: X11 P1 control-table DELIVERED: Table A (5-chrom, mask) K/O match healthy controls within 0.3pct in callable genome; Table C H3F3B fully intact all 5; Table B novel confounded by decoy-artifact (81pct shared K/O), documented+omitted per X7A. Report committed+pushed to master: projects/XG1/kenefick/kristen_control_table_20260713_v01_tomemex.md (commit fd666128).
- STATE: deliverable complete; A+C refute all 3 claims; X7A reframing letter around mask finding
- NEXT: standby for X7A follow-ups (extend A to 22 autosomes, or expensive Table B re-align) - else task done

## [2026-07-13 16:22] ? 501244df
- DID: X11 P1: completed X32's 5 Kristen claim-checks. KILLER job5: FIR/HIR K-vs-O = 74.08% fully-identical, 100% share-ge-1, 0% opposite-hom = textbook mother-son, reproduces her 'impossible 70-75% FIR' exactly. mtDNA clean (3/42 het w/ MAPQ filter), KHDC3L normal (40.8x MAPQ59), ABO ordinary het. Committed projects/XG1/kenefick/kristen_claim_checks_20260713_v01 to master (b562007f). Flagged mtDNA reconcile w/ sibling's email-16 (their 96% unfiltered vs my 3 filtered = artifact-vs-truth).
- STATE: 5 jobs delivered+pushed+posted to X32; git was messy (dangling commit from concurrent shared-checkout, recovered+pushed clean, restored sibling branch)
- NEXT: standby for X32 letter feedback / follow-ups (exact ABO O-indel genotype or de-novo NUMT count available on request)
