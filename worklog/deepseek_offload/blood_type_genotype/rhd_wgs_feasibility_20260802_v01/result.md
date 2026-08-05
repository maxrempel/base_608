# Feasibility Memo: Read-Only Inventory of RHD Structural-Variant Analysis

## Scope and status
This memo covers feasibility of a read-only bioinformatics inventory of RHD structural variants (SVs) for S1, S1-related, S2, and S3. No phenotype or participant RhD status is inferred or claimed. No wet-lab work is recommended. No depth, CNV, breakpoint, or alignment-scale job was launched; this is a planning and feasibility assessment only.

## Manager gate
OMEGA calibration and NPA natural-specificity analysis have priority. No depth, CNV, breakpoint, or alignment-scale job may begin until explicit release after their clean checkpoint. All plans below are contingent on that release.

## Verified inputs
- S1: 65,698,837,511-byte coordinate-sorted GRCh38 BAM on Asto, BAI present, `samtools quickcheck` clean, MGI read groups, numeric contigs with chr1 length 248,956,422; retained SHA256 `5e11c0750a051c6b44b34b560cd00c8e1d7b08a3e36952d3d4eea923988129c9`; existing chr22 estimate about 80x.
- S1-related: 37,612,556,572-byte coordinate-sorted GRCh38 BAM on Asto, BAI present, quickcheck clean, MGI, numeric contigs, vendor label 30x; no retained authoritative full-file checksum located in the bounded inventory.
- S2: 226,627,001,526-byte indexed GRCh38 CRAM on Taygeta Green24; v03 acceptance marker SHA256 `993f37ffedd8f0a7fe050bb7ed6f9f7ae76e29d6b2776f18f13deff3e4e8e14d`; 22/22 indexed probes passed.
- S3: indexed GRCh38 CRAM on Centauri, queryable only by the verified encrypted direct route; integrity marker SHA256 `96ad123ca475bbe4a340a4bcc57cd646883f60dbcf80786bafcab351785ecd97`; all 22 autosomes previously passed indexed use.
- S1 and S1-related are family-related and therefore not independent.

## Public local control inputs
- Asto has 13 indexed official IGSR high-coverage GRCh38 Illumina NovaSeq CRAMs; representative header and quickcheck passed. These may be technical controls, but no independently established sample-level RHD deletion/copy-number truth is linked.
- GIAB HG002 30x GRCh37 is documented remotely but not local; reference mismatch and no authoritative RHD status. It cannot substitute as a truth control.
- Erythrogene/RBCeq computational predictions are not authoritative truth and will not be used as ground truth.

## Tool availability
- Present on Asto PATH: `samtools` 1.19.2, `bcftools`.
- Manta exists at a documented conda path and has previously run targeted windows.
- Prior Delly 1.2.6 VCFs exist for S1 and S1-related, but Delly is not in current PATH and exact runtime provenance has not been re-established.
- Not found in current PATH: mosdepth, CNVkit, GRIDSS, Sniffles, RHtyper.

## Reference facts (GRCh38)
- Upstream Rhesus box: 1:25,258,884-25,268,025
- RHD: 1:25,272,486-25,330,445
- Downstream Rhesus box: 1:25,329,026-25,338,354
- RHCE: 1:25,362,249-25,430,203
- ClinVar common whole-RHD deletion: NC_000011.11:g.(25258851_25268086)_(25329003_25338415)del
- High RHD/RHCE and Rhesus-box homology makes naive depth or generic SV calls unsafe.

## Proposed design after release
1. Freeze input, checksum, build, and tool manifests; use an indexed 230 kb window 1:25,230,000-25,460,000.
2. Compute all-read and MAPQ>=20 depth in RHD, RHCE, Rhesus boxes, paralog-specific exonic/unique positions, and 20 single-copy autosomal controls matched for GC and mappability. Normalize RHD to RHCE and control depth. Do not freeze copy-number thresholds until truth controls pass.
3. Inspect split reads, soft clips, insert-size/orientation outliers, and discordant pairs around both Rhesus boxes and the hybrid-box junction; run targeted Manta and independently summarize pre-existing Delly calls. Same-read agreement is computational corroboration, not independent truth.
4. Add RHtyper only in a pinned environment, using coverage plus variants/hybrid logic. Report structural genotype categories with uncertainty, never phenotype.

## Calibration requirements and blocker
Calibration requires at minimum:
- One independently verified conventional two-copy sample,
- one heterozygous whole-RHD deletion,
- one homozygous whole-RHD deletion,
- all on GRCh38 short-read WGS,
- plus no-event genomic windows and process controls.

Current local public CRAMs lack these authoritative truth labels. This is a scientific blocker for calls: no threshold or genotype category can be calibrated safely. The same limitation applies to S2 and S3, as no linked authoritative RHD status is documented for those samples in the bounded inventory.

## Resource estimate after release
- Indexed depth/feature extraction: approximately 1 CPU, under 2 GiB, under 15 minutes per sample.
- Published RHtyper mean about 3.4 minutes/sample; budget 10 minutes/sample.
- Targeted Manta: roughly 1-2 CPUs, 4-6 GiB, 10-30 minutes/sample.
These are planning bounds, not measured local runtime.

## Pilot order after manager release
1. Truth controls first; only if expected separation and false-positive gates pass, proceed.
2. Run S1 and S1-related.
3. S2 and S3 later under their owners.

## Conclusion
Technically feasible: read-only operations, required tools, references, and compute bounds are sufficient.

Scientifically blocked before calling by:
- Missing authoritative known-status controls for GRCh38 short-read WGS;
- Missing pinned RHtyper environment and re-established Delly provenance;
- Absent authoritative checksum for S1-related;
- Manager release not yet granted.

No pilot was run.
