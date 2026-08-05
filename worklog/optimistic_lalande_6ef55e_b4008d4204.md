
## [2026-06-26 15:08] X4 59ea3219
- DID: X4 on Kenefick case: analyzed Kristen's SV(Manta 6497)/CNV(Canvas 133 PASS)/MITO(242) raw VCFs (sample SQ76JY63, GRCh38.p13)
- STATE: Findings: no class-1 giant insertion (max INS 979bp=Manta cap, 24 ins>=500bp, 0>=1kb); normal SV/CNV landscape; chrY ABSENT from SV file (female-mode pipeline) + sex chroms absent from CNV so they can't confirm/deny Y-chimerism; mtDNA=single clean maternal lineage (9 mid-het all D-loop homopolymer artifact). Scripts in project root.
- NEXT: Report to x1 done; x3 owns snp-indel maternal-Y headline
- LESSON: Sequencing.com SV/CNV pipeline excludes sex chromosomes in female-labeled samples - sex-chr chimerism CANNOT be checked via their SV/CNV VCFs, only via depth on the snp-indel WGS
