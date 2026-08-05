Draft a concise scientific feasibility memo, maximum 4,500 characters, for a read-only inventory of RHD structural-variant analysis. Do not claim phenotype or participant RhD status. Do not recommend wet-lab work. No chain-of-thought.

Manager gate: OMEGA calibration and NPA natural-specificity have priority. No depth, CNV, breakpoint, or alignment-scale job may launch until explicit release after their clean checkpoint. This memo must report feasibility and blockers only.

Verified participant inputs:
- S1: restricted coordinate-sorted GRCh38 BAM on Asto, 65,698,837,511 bytes, BAI present, samtools quickcheck clean, MGI read groups, numeric contigs with chr1 length 248,956,422. Existing chr22 estimate is about 80x. Retained BAM SHA256 5e11c0750a051c6b44b34b560cd00c8e1d7b08a3e36952d3d4eea923988129c9.
- S1-related: restricted coordinate-sorted GRCh38 BAM on Asto, 37,612,556,572 bytes, BAI present, quickcheck clean, MGI, numeric contigs, vendor label 30x. No retained authoritative full-file checksum was located in the bounded inventory.
- S2: restricted indexed GRCh38 CRAM on Taygeta Green24, exact documented size 226,627,001,526 bytes; v03 acceptance marker SHA256 993f37ffedd8f0a7fe050bb7ed6f9f7ae76e29d6b2776f18f13deff3e4e8e14d; 22/22 indexed probes passed.
- S3: restricted indexed GRCh38 CRAM on Centauri, queryable only by the verified encrypted direct route; integrity marker SHA256 96ad123ca475bbe4a340a4bcc57cd646883f60dbcf80786bafcab351785ecd97; all 22 autosomes previously passed indexed use.
- S1 and S1-related are family-related and not independent.

Public local inputs:
- Asto has 13 indexed official IGSR high-coverage CRAMs, GRCh38, Illumina NovaSeq; a representative header and quickcheck passed. They are technical controls but no independently established sample-level RHD deletion/copy-number truth is currently linked. Do not substitute Erythrogene/RBCeq computational predictions for authoritative truth.
- GIAB HG002 30x GRCh37 source is documented remotely but not local, reference-mismatched, and no authoritative RHD status is linked.

Local tools:
- Asto: samtools 1.19.2 and bcftools in PATH.
- Manta environment exists at a documented conda path and has previously run targeted windows.
- Previous Delly 1.2.6 VCF outputs exist for S1 and S1-related, but Delly is not in current PATH and exact runtime provenance has not been re-established.
- mosdepth, CNVkit, GRIDSS, Sniffles, and RHtyper were not found in current PATH.

Reference facts, GRCh38:
- upstream Rhesus box 1:25,258,884-25,268,025;
- RHD 1:25,272,486-25,330,445;
- downstream Rhesus box 1:25,329,026-25,338,354;
- RHCE 1:25,362,249-25,430,203.
- ClinVar common whole-RHD deletion is NC_000001.11:g.(25258851_25268086)_(25329003_25338415)del. High RHD/RHCE and Rhesus-box homology makes naive depth or generic SV calls unsafe.

Design after release:
1) Freeze input/checksum/build/tool manifests and use a 230 kb indexed window 1:25,230,000-25,460,000.
2) Compute both all-read and MAPQ>=20 depth in RHD, RHCE, Rhesus boxes, paralog-specific exonic/unique positions, and 20 single-copy autosomal controls matched for GC and mappability. Normalize RHD to RHCE and control depth; do not freeze copy thresholds until truth controls pass.
3) Inspect split reads, soft clips, insert-size/orientation outliers and discordant pairs around both Rhesus boxes and hybrid-box junction; run targeted Manta and independently summarize pre-existing Delly calls. Same-read agreement is computational corroboration, not independent truth.
4) Add RHtyper only in a pinned environment, using coverage plus variants/hybrid logic. Report structural genotype categories with uncertainty, never phenotype.
5) Calibration requires at minimum one independently verified conventional two-copy sample, one heterozygous deletion, and one homozygous whole-RHD deletion on GRCh38 short-read WGS, plus no-event genomic windows and process controls. Current local public CRAMs lack these truth labels.
6) Pilot order after manager release: truth controls first; only if expected separation and false-positive gates pass, run S1 and S1-related; S2/S3 later under their owners.

Resource estimate after release: indexed depth/feature extraction approximately 1 CPU, under 2 GiB, under 15 minutes per sample; published RHtyper mean about 3.4 minutes/sample but budget 10 minutes; targeted Manta roughly 1-2 CPUs, 4-6 GiB, 10-30 minutes/sample. These are planning bounds, not measured local runtime.

Required conclusion: technically feasible, scientifically blocked before calling by missing authoritative known-status controls, missing pinned RHtyper/Delly provenance, absent S1-related checksum, and manager release. No pilot was run.
