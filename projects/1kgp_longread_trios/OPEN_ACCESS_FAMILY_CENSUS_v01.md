# OPEN ACCESS FAMILY CENSUS v01

---
name: Open-access long-read family census v01
description: Saturated census of publicly downloadable human families with long-read WGS (complete families only). Built by Q38 census branch from 4 detached search agents (repositories, literature, consortia, saturation) plus direct API verification against ENA, NCBI, SRA, AWS S3, GIAB FTP, and GitHub.
type: project
last_edited: 2026-08-06 by Codex (Q38 branch)
status: v01 complete for verified families; Agent D saturation sweep (NGDC/Korea/Japan/India/2026 preprints) pending and will be merged as v02 if it adds families
---

# TLDR

32 unique open-access complete families (35 complete trios) have long-read WGS data publicly downloadable today. This is up from the 13 trios in FAMILY_MANIFEST_v01. Four additions beyond the known 13: GIAB Ashkenazi trio, GIAB Chinese trio, T2T-CQ Chinese Quartet, PAN027/WashU pedigree. The biggest new finding: the Platinum Pedigree (CEPH 1463, Porubsky et al. Nature 2025) is OPEN, not dbGaP-controlled as previously assumed; 23 of its 28 members have reads, assemblies, and variant calls on AWS Open Data and ENA, adding 15 new family units (17 trios) including two that overlap the Vienna CEU trios.

# 1. Headline counts

| Metric | Count |
|---|---|
| Unique open-access complete families | 32 |
| Complete trios across them | 35 |
| Families with de novo assemblies available for download | 18 (all members) + 1 partial (GIAB Ashkenazi: HG002 only) |
| Families with reads only (no assemblies) | 13 (6 Vienna trios, GIAB Chinese trio, GIAB parents HG003/HG004 counted within Ashkenazi trio) |
| Families from non-cultured primary material only | 0 (see section 5; Platinum Pedigree and PAN027 are closest: HiFi from blood) |

Max's remembered number 17 is explained: 13 manifest trios + 2 GIAB trios + T2T-CQ quartet + PAN027 pedigree = 17. The census then grew to 32 when Platinum Pedigree was found to be open access.

# 2. Family unit list (unique families, deduplicated across datasets)

F = family unit ID. Father/mother/child order where known. Overlapping dataset coverage noted.

## Group I: 1000 Genomes Project resources (13 families, all EBV LCL material)

| F | Population | Father | Mother | Child | Datasets | Assemblies |
|---|---|---|---|---|---|---|
| F01 | CHS | HG00512 | HG00513 | HG00514 | HGSVC3 | Verkko GCA_964198245 / GCA_964198275 / GCA_964659605 (v2; v1 corrupt) |
| F02 | YRI | NA19239 | NA19238 | NA19240 | HGSVC3 | Verkko GCA_964198345 / GCA_964198565 / GCA_964199255 |
| F03 | PUR | HG00731 | HG00732 | HG00733 | HGSVC3 (+child HG00733 also in HPRC_PLUS) | Verkko GCA_964199225 / GCA_964198225 / GCA_964198175 |
| F04 | ESN | HG03370 | HG03369 | HG03371 | LRSC ONT; child HG03371 also has HGSVC3 near-T2T assembly | LRSC ASSEMBLIES dir; child: HGSVC3 Verkko |
| F05 | CHS | HG00704 | HG00705 | HG00706 | LRSC ONT | LRSC ASSEMBLIES dir |
| F06 | KHV | HG02026 | HG02025 | HG02024 | LRSC ONT | LRSC ASSEMBLIES dir |
| F07 | GWD | HG02613 | HG02614 | HG02615 | LRSC ONT | LRSC ASSEMBLIES dir |
| F08 | CEU | NA12891 | NA12892 | NA12878 | Vienna ONT + Platinum Pedigree + GIAB (NA12878 = HG001) | Platinum Pedigree near-T2T (all 3 members) |
| F09 | CEU | NA12889 | NA12890 | NA12877 | Vienna ONT + Platinum Pedigree | Platinum Pedigree near-T2T (all 3 members) |
| F10 | YRI | NA19128 | NA19127 | NA19129 | Vienna ONT | none (reads only) |
| F11 | CLM | HG01256 | HG01257 | HG01258 | Vienna ONT | none |
| F12 | ASW | NA19818 | NA19819 | NA19828 | Vienna ONT | none |
| F13 | CHS | HG00418 | HG00419 | HG00420 | Vienna ONT | none |

Download paths for these 13: see FAMILY_MANIFEST_v01.md (unchanged; HGSVC3 FTP root, s3://1000g-ont, 1KG_ONT_VIENNA FTP/ENA PRJEB89727).

## Group II: GIAB reference trios (2 families, open FTP and S3, no DAC)

| F | Population | Father | Mother | Child | Data | Assemblies |
|---|---|---|---|---|---|---|
| F14 | Ashkenazi Jewish | HG003 (NA24149) | HG004 (NA24143) | HG002 (NA24385) | PacBio HiFi (Revio + SequelII CCS) + ONT ultralong, all 3 members | HG002: T2T diploid v2.7 (GIAB FTP data/AshkenazimTrio/analysis/T2T-HG002-XY-v2.7/); HG003/HG004: none public (reads only) |
| F15 | Han Chinese (PGP) | HG006 (NA24694, huCA017E) | HG007 (NA24695, hu38168) | HG005 (NA24631) | PacBio HiFi/CCS + ONT ultralong, all 3 members | none public (reads only) |

Access: https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/data/AshkenazimTrio/ and .../ChineseTrio/ ; AWS s3://giab ; index github.com/genome-in-a-bottle/giab_data_indexes. Verified 2026-08-06: GIAB Chinese trio is Personal Genome Project material and is NOT the same family as HGSVC3/1KGP Chinese trio HG00512/513/514 (different individuals; PGP donor IDs confirm). No double count.

## Group III: T2T reference families (2 families)

| F | Structure | Members | Data | Assemblies |
|---|---|---|---|---|
| F16 | T2T-CQ Chinese Quartet: father + mother + monozygotic twin sons (2 trios within) | sample IDs pending Agent D | ONT ultralong + PacBio HiFi | T2T haplotype-resolved diploid assemblies for all 4 members at NGDC GWH. Verified so far: maternal GWHFQEY00000000.1, paternal GWHFQEX00000000.1; twin accessions pending Agent D |
| F17 | PAN027 / WashU pedigree: grandmother + grandfather + daughter (+ granddaughter; her father is outside the pedigree) | HG06803 (PAN010, grandmother), HG06804 (PAN011, grandfather), HG06807 (PAN027, daughter), HG06808 (PAN028, granddaughter) | HiFi from BLOOD (raw, 5mC, DeepConsensus), ONT ultrlong + duplex + adaptive sampling + poreC from LCL, Illumina blood+LCL, Element Aviti, Omni-C; SRA study SRP320775 | T2T phased diploid assemblies for ALL 4 members, open at https://public.gi.ucsc.edu/~mcechova/pedigree/assemblies/ (v1.0, v1.1, v1.2, v1.3.1 panpatch); HG06807 also at NCBI: GCA_046332035.2 (pat hap) + GCA_046332005.3 (mat hap), BioProjects PRJNA1198676/PRJNA1198675 |

F16 source: Wang B et al. 2025, Genomics Proteomics Bioinformatics, DOI 10.1093/gpbjnl/qzaf118, PMC13075991. Raw reads: GSA-Human HRA010594 (NGDC/CNCB); access mechanics pending Agent D.
F17 sources: Cechova M et al. 2025 preprint DOI 10.64898/2025.12.14.693655 (paper: "Complete genomes of a multi-generational pedigree..."); Dong S et al. 2026 centromere companion DOI 10.64898/2026.02.14.705860 (same family, not a second family). Code: github.com/biomonika/washu-pedigree. Sample registry links: HG06807 in HPRC year-1 BioProject PRJNA701308; HG06803/HG06804/HG06808 in HPRC PLUS BioProject PRJNA731524. Complete trio in this family: HG06803 + HG06804 + HG06807.

## Group IV: Platinum Pedigree / CEPH-Utah family 1463 (15 new family units; 2 overlap F08/F09)

Source: Porubsky D et al. 2025 Nature, "Human de novo mutation rates from a four-generation pedigree reference", DOI 10.1038/s41586-025-08922-2, PMC12240836. Consortium: Platinum Pedigree (T2T consortium + E.E.E. lab). Verified open 2026-08-06 by direct bucket and ENA listing (previous Agent C rejection as dbGaP-only was WRONG: dbGaP phs003793.v1.p1 holds only the 5 non-consented members plus whole-family variant calls).

Open members (23 of 28), all with assemblies in s3://platinum-pedigree-data/assemblies/<ID>/ and data in s3://platinum-pedigree-data/data/ ; ENA BioProject PRJEB86317 (23 samples confirmed); GitHub index github.com/Platinum-Pedigree-Consortium/Platinum-Pedigree-Datasets:
- G1 grandparents: NA12889, NA12890 (parents of NA12877); NA12891, NA12892 (parents of NA12878)
- G2: NA12877, NA12878 (NA12878 = GIAB HG001)
- G3 (children of NA12877 x NA12878, open): NA12879, NA12881, NA12882, NA12885, NA12886; plus G3 spouses 200080 (male), 200100 (female)
- G4 (open): 200081, 200082, 200084, 200085, 200086, 200087 (branch of NA12879 x 200080); 200101, 200102, 200104, 200106 (branch of NA12886 x 200100)
- NOT open (dbGaP only): G3 NA12883, NA12884, NA12887; G4 200103, 200105

G3 parents of G4 branches confirmed from paper text (the two G3 individuals with sequenced children: NA12879 and NA12886).

Data: PacBio HiFi + Illumina + Element from BLOOD-derived DNA (G2-G4); ONT ultralong + Strand-seq from LCLs (G1-G3); assemblies built with LCL UL-ONT and polished with blood HiFi. Near-T2T phased diploid assemblies for all 23 open members; variant truth sets v1.1/v1.2 for NA12878 (Kronenberg et al. 2025 Nat Methods).

Complete trios fully inside the open set (17):

| Trio | Father | Mother | Child | New family? |
|---|---|---|---|---|
| PP01 | NA12889 | NA12890 | NA12877 | no (= F09, Vienna trio) |
| PP02 | NA12891 | NA12892 | NA12878 | no (= F08, Vienna trio) |
| PP03 | NA12877 | NA12878 | NA12879 | yes = F18 |
| PP04 | NA12877 | NA12878 | NA12881 | yes = F19 |
| PP05 | NA12877 | NA12878 | NA12882 | yes = F20 |
| PP06 | NA12877 | NA12878 | NA12885 | yes = F21 |
| PP07 | NA12877 | NA12878 | NA12886 | yes = F22 |
| PP08 | 200080 | NA12879 | 200081 | yes = F23 |
| PP09 | 200080 | NA12879 | 200082 | yes = F24 |
| PP10 | 200080 | NA12879 | 200084 | yes = F25 |
| PP11 | 200080 | NA12879 | 200085 | yes = F26 |
| PP12 | 200080 | NA12879 | 200086 | yes = F27 |
| PP13 | 200080 | NA12879 | 200087 | yes = F28 |
| PP14 | NA12886 | 200100 | 200101 | yes = F29 |
| PP15 | NA12886 | 200100 | 200102 | yes = F30 |
| PP16 | NA12886 | 200100 | 200104 | yes = F31 |
| PP17 | NA12886 | 200100 | 200106 | yes = F32 |

# 3. Quality ranking for the download branch (assemblies first)

Tier 1 - T2T-class phased diploid assemblies for every member (download these first):
1. F16 T2T-CQ Quartet (4 members, GWH, NGDC) - verify GSA-Human mechanics first
2. F17 PAN027 (4 members, UCSC public hosting + NCBI) - HiFi from blood; best non-cultured representation
3. Platinum Pedigree 23 members (AWS S3 + ENA) - near-T2T; HiFi from blood; largest single resource
4. F01-F03 HGSVC3 trios (Verkko, ENA PRJEB76276) - provenance-rich, benchmarked

Tier 2 - good assemblies, ONT-only input:
5. F04-F07 LRSC trios (s3://1000g-ont PROCESSED_DATA/ASSEMBLIES/; F04 child also has HGSVC3 Verkko)

Tier 3 - T2T assembly for one member only:
6. F14 GIAB Ashkenazi (HG002 T2T v2.7; HG003/HG004 reads only)

Tier 4 - reads only, assemble later if needed:
7. F08-F13 Vienna trios (F08/F09 upgrade to Platinum Pedigree assemblies instead)
8. F15 GIAB Chinese trio (HiFi + UL ONT reads; no public assemblies anywhere)

Estimated assembly-only download volume: roughly 250-350 GB total (23 Platinum Pedigree + 9 HGSVC3 + 4 T2T-CQ + 4 PAN027 + 12 LRSC + 1 HG002, diploid FASTAs ~6 GB each).

# 4. Access verification evidence (all checked live 2026-08-06)

- Platinum Pedigree: s3://platinum-pedigree-data/ lists assemblies/ for all 23 open members; ENA PRJEB86317 returns exactly those 23 samples; paper data availability section names AWS + ENA for open members and dbGaP phs003793.v1.p1 for the 5 others.
- PAN027: NCBI Assembly esummary confirms GCA_046332035.2 (PAN027_pat_v1.1, released 2026-07-22, UCSC Genomics Institute, isolate HG06807, coverage 259x) and GCA_046332005.3 chain (PAN027_mat); washu-pedigree README lists SRP320775 accessions for all 4 members and direct UCSC FASTA URLs for v1.0-v1.3.1 assemblies; Dong et al. 2026 full text confirms pedigree structure and LCL origin.
- GIAB: FTP listing confirms AshkenazimTrio and ChineseTrio directories with HG005_NA24631_son / HG006_NA24694-huCA017E_father / HG007_NA24695-hu38168_mother naming (PGP origin, distinct from HGSVC3 HG00512-514); T2T-HG002-XY-v2.7 present in analysis folder.
- HGSVC3: cached accession table confirms HG00512/513/514 HiFi 31-68x + ONT 61-81x and assembly GCAs; HG00512 has one ONT run flagged contaminant (exclude).
- T2T-CQ: paper verified by Agent B via Europe PMC full text; twin assembly accessions and GSA-Human download mechanics still pending Agent D.

# 5. Cultured vs non-cultured material (for the parent thread's priority)

No open-access family is fully non-cultured. Every family uses EBV-transformed lymphoblastoid cell lines for at least part of its data:
- Platinum Pedigree: HiFi, Illumina, Element from blood (non-cultured); UL-ONT and Strand-seq from LCL; assemblies are LCL-ONT based, blood-HiFi polished. Best available option.
- PAN027: HiFi from blood; ONT, Hi-C, Element from LCL; assemblies polished with blood HiFi.
- T2T-CQ: material unverified (likely LCL; Agent D checking).
- All 1KGP/HGSVC/LRSC/Vienna/GIAB families: LCL throughout.
This matches the parent thread's earlier conclusion: fully non-cultured complete families exist only behind controlled access (e.g., MSSNG blood-derived).

# 6. Open items (Agent D / Banach, qwen3.7-plus, running)

1. T2T-CQ: all four member assembly accessions at GWH (twins missing), sample IDs, and whether GSA-Human HRA010594 raw reads need registration.
2. Zhou H et al. 2026 (JGG, DOI 10.1016/j.jgg.2026.03.011, three-generation Chinese family, methylation): data availability verdict.
3. Final sweep: NGDC GSA/GWH other families, KPGP Korea, Japan, GenomeIndia, Middle East, H3Africa open subsets, 2025-2026 preprints.
If Agent D confirms new open families, they are added as v02; if nothing new, v01 stands as saturated.

# 7. Verified dead ends (do not re-search)

- Controlled: Ivashchenko 2026 (10 PacBio trios, EGA EGAS00001008250); Negi 2025 (41 families, likely dbGaP); Werren 2026 (20 clinical families); Platinum Pedigree non-consented 5 members (dbGaP phs003793.v1.p1); all clinical rare-disease trio LRS studies examined.
- No families: HPRC year-1 and HPRC_PLUS (unrelated individuals by design, though PAN027 members and HG00733 live there as individuals); HGSVC3 recount (exactly 3 trios); All of Us, TOPMed, UK Biobank, deCODE, Estonian Biocentre, H3Africa (restricted); Korean Cho 2024 (3 unrelated individuals); Chinese pangenome Niu 2022 (32 unrelated); GenomeAsia (short-read); IGSR collections (nothing beyond the 3 known).
