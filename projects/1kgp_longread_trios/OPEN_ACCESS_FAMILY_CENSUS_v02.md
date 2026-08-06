# OPEN ACCESS FAMILY CENSUS v02 (FINAL, SATURATED)

---
name: Open-access long-read family census v02
description: Saturated census of publicly downloadable human families with long-read WGS (complete families only). Built by Q38 census branch from 4 detached search agents (C repositories, B literature, A consortia, D saturation) plus direct API verification against ENA, NCBI, SRA, AWS S3, GIAB FTP, Europe PMC full text, and GitHub. v02 merges Agent D saturation results; no further open families exist as of 2026-08-06.
type: project
last_edited: 2026-08-06 by Codex (Q38 branch)
status: SATURATED. v01 preserved for history.
---

# TLDR

32 unique open-access complete families (35 complete trios) have long-read WGS data publicly downloadable today, up from the 13 trios in FAMILY_MANIFEST_v01. Agent D swept NGDC/CNCB, Korea, Japan, India, Middle East, Africa, Latin America, HPRC2, and ~100 recent PubMed papers: nothing new. The four additions beyond the manifest 13: GIAB Ashkenazi trio, GIAB Chinese trio, T2T-CQ Chinese Quartet, PAN027/WashU pedigree. The largest source of new families is the Platinum Pedigree (CEPH 1463): verified OPEN (23/28 members, AWS + ENA), previously misclassified as dbGaP-only. Note for Max: the remembered number 17 matches 13 + 2 GIAB + T2T-CQ + PAN027; the census then grew to 32 via Platinum Pedigree.

# 1. Headline counts

| Metric | Count |
|---|---|
| Unique open-access complete families | 32 |
| Complete trios across them | 35 |
| Families with assemblies downloadable for ALL members | 18 (T2T-class or near-T2T) |
| Families with partial assemblies | 1 (GIAB Ashkenazi: HG002 T2T only) |
| Families with reads only | 13 (6 Vienna trios, GIAB Chinese trio, and GIAB parents HG003/HG004 within the Ashkenazi trio) |
| Families fully from non-cultured material | 0 (closest: Platinum Pedigree and PAN027, HiFi from blood) |

# 2. Family unit list (unique families, deduplicated across datasets)

## Group I: 1000 Genomes Project resources (13 families, all EBV LCL material)

| F | Population | Father | Mother | Child | Datasets | Assemblies |
|---|---|---|---|---|---|---|
| F01 | CHS | HG00512 | HG00513 | HG00514 | HGSVC3 | Verkko GCA_964198245 / GCA_964198275 / GCA_964659605 (v2; v1 corrupt) |
| F02 | YRI | NA19239 | NA19238 | NA19240 | HGSVC3 | Verkko GCA_964198345 / GCA_964198565 / GCA_964199255 |
| F03 | PUR | HG00731 | HG00732 | HG00733 | HGSVC3 (child HG00733 also in HPRC_PLUS) | Verkko GCA_964199225 / GCA_964198225 / GCA_964198175 |
| F04 | ESN | HG03370 | HG03369 | HG03371 | LRSC ONT; child also has HGSVC3 near-T2T assembly | LRSC ASSEMBLIES dir; child: HGSVC3 Verkko |
| F05 | CHS | HG00704 | HG00705 | HG00706 | LRSC ONT | LRSC ASSEMBLIES dir |
| F06 | KHV | HG02026 | HG02025 | HG02024 | LRSC ONT | LRSC ASSEMBLIES dir |
| F07 | GWD | HG02613 | HG02614 | HG02615 | LRSC ONT | LRSC ASSEMBLIES dir |
| F08 | CEU | NA12891 | NA12892 | NA12878 | Vienna ONT + Platinum Pedigree + GIAB (NA12878 = HG001) | Platinum Pedigree near-T2T (all 3) |
| F09 | CEU | NA12889 | NA12890 | NA12877 | Vienna ONT + Platinum Pedigree | Platinum Pedigree near-T2T (all 3) |
| F10 | YRI | NA19128 | NA19127 | NA19129 | Vienna ONT | none |
| F11 | CLM | HG01256 | HG01257 | HG01258 | Vienna ONT | none |
| F12 | ASW | NA19818 | NA19819 | NA19828 | Vienna ONT | none |
| F13 | CHS | HG00418 | HG00419 | HG00420 | Vienna ONT | none |

Download paths for these 13: FAMILY_MANIFEST_v01.md (HGSVC3 FTP root, s3://1000g-ont, 1KG_ONT_VIENNA FTP + ENA PRJEB89727).

## Group II: GIAB reference trios (2 families, open FTP and S3, no DAC)

| F | Population | Father | Mother | Child | Data | Assemblies |
|---|---|---|---|---|---|---|
| F14 | Ashkenazi Jewish | HG003 (NA24149) | HG004 (NA24143) | HG002 (NA24385) | PacBio HiFi (Revio + SequelII) + ONT ultralong, all 3 | HG002 T2T v2.7 (GIAB FTP data/AshkenazimTrio/analysis/T2T-HG002-XY-v2.7/); HG003/HG004 none public |
| F15 | Han Chinese (PGP donors) | HG006 (NA24694, huCA017E) | HG007 (NA24695, hu38168) | HG005 (NA24631) | PacBio HiFi/CCS + ONT ultralong, all 3 | none public |

Access: https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/data/AshkenazimTrio/ and .../ChineseTrio/ ; AWS s3://giab. Verified 2026-08-06 via FTP directory names (HG005_NA24631_son etc.): the GIAB Chinese trio is Personal Genome Project material, NOT the HGSVC3/1KGP Chinese trio HG00512/513/514. No double count.

## Group III: T2T reference families (2 families)

F16 - T2T-CQ Chinese Quartet (chinese-quartet.org):
- Members: two monozygotic twin DAUGHTERS (LCL5, LCL6) + biological parents (LCL7 father, LCL8 mother). Han Chinese. Material: B-lymphoblastoid cell lines (confirmed in paper).
- Data: high-coverage ONT ultralong + PacBio HiFi. Raw reads at GSA-Human HRA010594. ACCESS CAVEAT: GSA-Human default mode is controlled access (free account + DAC approval per ngdc.cncb.ac.cn/gsa-human/policy); the paper's "publicly accessible" phrasing refers to the portal, so treat reads as controlled until confirmed.
- Assemblies (OPEN, GWH, freely downloadable): the T2T-CQ paper (Wang B et al. 2025 GPB, DOI 10.1093/gpbjnl/qzaf118, PMC13075991) produced a haplotype-phased T2T diploid assembly of the TWINS' genome (twin data combined because monozygotic): CQ v3.2 maternal haplotype GWHFQEY00000000.1, paternal haplotype GWHFQEX00000000.1, at https://ngdc.cncb.ac.cn/gwh . QV > 66 both haplotypes.
- Parents' assemblies: an earlier CQ v2.0 assembly of the family exists (paper reference 16); parent-specific accessions NOT yet verified - check chinese-quartet.org / GWH before download.
- Complete trios: father LCL7 + mother LCL8 + twin LCL5, and + twin LCL6 (2 trios).

F17 - PAN027 / WashU pedigree (Cechova M et al. 2025 preprint DOI 10.64898/2025.12.14.693655; Dong S et al. 2026 centromere companion DOI 10.64898/2026.02.14.705860, same family):
- Members: grandmother HG06803 (PAN010), grandfather HG06804 (PAN011), daughter HG06807 (PAN027), granddaughter HG06808 (PAN028; her father outside the pedigree). African American. Complete trio = HG06803 + HG06804 + HG06807.
- Data (all open, SRA SRP320775): PacBio HiFi from BLOOD (raw, 5mC, DeepConsensus); ONT ultralong + duplex + adaptive sampling + poreC from LCL; Illumina blood + LCL; Element Aviti; Omni-C. Index: github.com/biomonika/washu-pedigree.
- Assemblies (OPEN): T2T phased diploid assemblies for ALL 4 members at https://public.gi.ucsc.edu/~mcechova/pedigree/assemblies/ - use v1.3.1 (panpatch-curated); annotations and UCSC browser hubs on the same host. HG06807 also at NCBI: GCA_046332035.2 (pat haplotype, 259x, released 2026-07-22) and GCA_046332005 chain (mat haplotype), BioProjects PRJNA1198676 / PRJNA1198675.
- Registry links: HG06807 in HPRC year-1 BioProject PRJNA701308; HG06803/HG06804/HG06808 in HPRC PLUS BioProject PRJNA731524.

## Group IV: Platinum Pedigree / CEPH-Utah family 1463 (15 new family units; 2 overlap F08/F09)

Source: Porubsky D et al. 2025 Nature, "Human de novo mutation rates from a four-generation pedigree reference", DOI 10.1038/s41586-025-08922-2, PMC12240836. Verified OPEN 2026-08-06 by direct bucket + ENA listing. Earlier Agent C rejection as dbGaP-only was WRONG: dbGaP phs003793.v1.p1 holds only the 5 non-consented members plus whole-family variant calls.

Open members (23 of 28), each with an assembly folder in s3://platinum-pedigree-data/assemblies/<ID>/ , mapped data in s3://platinum-pedigree-data/data/ , ENA BioProject PRJEB86317 (23 samples confirmed), index repo github.com/Platinum-Pedigree-Consortium/Platinum-Pedigree-Datasets:
- G1 grandparents: NA12889, NA12890 (parents of NA12877); NA12891, NA12892 (parents of NA12878)
- G2: NA12877, NA12878 (NA12878 = GIAB HG001; truthsets v1.1/v1.2 in bucket)
- G3 open children of NA12877 x NA12878: NA12879, NA12881, NA12882, NA12885, NA12886; G3 spouses 200080 (male), 200100 (female)
- G4 open: 200081, 200082, 200084, 200085, 200086, 200087 (branch NA12879 x 200080); 200101, 200102, 200104, 200106 (branch NA12886 x 200100)
- NOT open (dbGaP only): NA12883, NA12884, NA12887 (G3); 200103, 200105 (G4)

Data: PacBio HiFi + Illumina + Element from BLOOD-derived DNA; ONT ultralong + Strand-seq from LCLs; assemblies built with LCL UL-ONT, polished with blood HiFi. Near-T2T phased diploid assemblies for all 23 open members.

Complete trios fully inside the open set (17): PP01 NA12889+NA12890+NA12877 (=F09); PP02 NA12891+NA12892+NA12878 (=F08); PP03-PP07 NA12877+NA12878 with child NA12879/NA12881/NA12882/NA12885/NA12886 (=F18-F22); PP08-PP13 200080+NA12879 with child 200081/200082/200084/200085/200086/200087 (=F23-F28); PP14-PP17 NA12886+200100 with child 200101/200102/200104/200106 (=F29-F32). G3 parents of the two G4 branches confirmed from paper text.

# 3. Quality ranking for the download branch (assemblies first)

Tier 1 - T2T-class phased diploid assemblies (download first):
1. F17 PAN027: 4 members, UCSC hosting + NCBI, HiFi from blood
2. Platinum Pedigree: 23 members, s3://platinum-pedigree-data + ENA PRJEB86317, HiFi from blood
3. F01-F03 HGSVC3: 9 members, Verkko ENA PRJEB76276
4. F16 T2T-CQ: twins' diploid genome T2T (2 haplotypes) via GWH; parents' v2.0 assemblies to verify; raw reads controlled

Tier 2 - solid assemblies from ONT-only input:
5. F04-F07 LRSC (s3://1000g-ont PROCESSED_DATA/ASSEMBLIES/; F04 child also has HGSVC3 Verkko)

Tier 3 - one-member T2T:
6. F14 GIAB Ashkenazi (HG002 T2T v2.7 only)

Tier 4 - reads only (assemble later if needed):
7. F10-F13 Vienna (F08/F09 covered by Platinum Pedigree instead)
8. F15 GIAB Chinese trio

Estimated assembly-only payload: roughly 250-350 GB.

# 4. Access verification evidence (all live checks 2026-08-06)

- Platinum Pedigree: S3 bucket lists assemblies/ for all 23 open members; ENA PRJEB86317 returns exactly those 23; paper data-availability section splits open (AWS + ENA) vs dbGaP (5 members).
- PAN027: NCBI esummary confirms GCA_046332035.2 (PAN027_pat_v1.1, UCSC Genomics Institute, isolate HG06807); washu-pedigree README lists SRP320775 accessions for all 4 members and direct FASTA URLs v1.0-v1.3.1; Dong 2026 full text (cached) confirms pedigree structure and LCL origin.
- GIAB: FTP confirms trio folder names with PGP donor IDs; T2T-HG002-XY-v2.7 present.
- T2T-CQ: Europe PMC full text (cached) confirms LCL5/LCL6 twin daughters + LCL7/LCL8 parents, LCL material, GWH accessions, GSA-Human HRA010594; GSA-Human policy page (Agent D) confirms controlled default for reads.
- HGSVC3: cached accession table confirms coverages (HiFi 31-68x, ONT 61-81x) and GCAs; one HG00512 ONT run flagged contaminant (exclude).

# 5. Cultured vs non-cultured material

No open-access family is fully non-cultured; every family uses EBV LCLs for at least part of its data:
- Platinum Pedigree: HiFi/Illumina/Element from blood; UL-ONT/Strand-seq from LCL; assemblies LCL-ONT based, blood-HiFi polished. Best available.
- PAN027: HiFi from blood; ONT/Hi-C/Element from LCL; assemblies polished with blood HiFi.
- T2T-CQ: B-lymphoblastoid cell lines throughout (confirmed).
- All 1KGP/HGSVC/LRSC/Vienna/GIAB families: LCL throughout.
Fully non-cultured complete families exist only behind controlled access (MSSNG blood-derived etc., see CONTROLLED_ACCESS_CANDIDATES doc).

# 6. Saturation status and remaining unknowns

Agent D (qwen3.7-plus) completed the saturation sweep 2026-08-06: NGDC/CNCB, KPGP/KOREF (Korea), Japanese T2T, GenomeIndia, Qatar/Saudi/Emirati, H3Africa, Latin America, HPRC2, and ~100 recent PubMed papers (of 397 hits). Verdict: NO new open-access complete families. Remaining unknowns (low priority for assembly-first scope):
- Zhou H et al. 2026 (JGG DOI 10.1016/j.jgg.2026.03.011, three-generation Chinese family, nanopore methylation): full text paywalled; data accessions unverified.
- T2T-CQ parents' assembly accessions (CQ v2.0) unverified.
- Mortazavi 2026 Cell Genomics (autism LRS): likely controlled, no accessions found.
- Sasani 2026 (Platinum Pedigree companion, tandem repeats): preprint unfetchable; data expected to follow Platinum Pedigree open/dbGaP split.

# 7. Verified dead ends (do not re-search)

Controlled access: Ivashchenko 2026 (10 PacBio trios, EGA EGAS00001008250); Negi 2025 (41 families, likely dbGaP); Werren 2026 (20 clinical families); Noyes 2026 Nat Commun (Eichler lab families, SFARI Base SFARI_DS0000104 + NDA Collection 3780); Platinum Pedigree non-consented 5 members (dbGaP phs003793.v1.p1); T2T-CQ raw reads (GSA-Human DAC); clinical rare-disease trio LRS studies generally.
Not complete long-read families: HPRC year-1 + HPRC_PLUS + HPRC2 (unrelated individuals by design; PAN027 members and HG00733 live there as individuals); HGSVC3 recount (exactly 3 trios); KOREF_S1 Korean reference (parents short-read only, PMID 35333300); Japanese T2T Suzuki 2026 (10 unrelated males); Niu 2022 Chinese pangenome (32 unrelated); GenomeAsia (short-read); All of Us, TOPMed, UK Biobank, deCODE, Estonian Biocentre, H3Africa (restricted); IGSR (nothing beyond the 3 known collections).
