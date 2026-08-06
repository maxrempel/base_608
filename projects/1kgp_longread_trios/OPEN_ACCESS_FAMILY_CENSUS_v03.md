# OPEN ACCESS FAMILY CENSUS v03 (SATURATED AFTER WAVE-2)

---
name: Open-access long-read family census v03
description: Saturated census of publicly downloadable human families with long-read WGS (complete families only). Built by Q38 census branch from 4 wave-1 search agents (C repositories, B literature, A consortia, D saturation) and 3 wave-2 agents (E literature, F repositories, G regional) plus direct API verification against ENA, NCBI, SRA, AWS S3, GIAB FTP, Europe PMC full text, bioRxiv, NGDC GSA-Human/GWH, and GitHub. v03 adds one new verified open family (F33 APR trio, blood-derived) and resolves all wave-2 candidates.
type: project
last_edited: 2026-08-06 by Codex (Q38 branch, wave-2)
status: SATURATED after wave-2. v01 and v02 preserved for history.
---

# TLDR

33 unique open-access complete families (36 complete trios) have long-read WGS data publicly downloadable today, up from the 13 trios in FAMILY_MANIFEST_v01. Wave-2 (agents E/F/G: ~700 more papers, ENA/NCBI/GSA metadata mining, regional sweep of SE/Central Asia, Middle East, Africa, Oceania, Latin America) found exactly ONE new open family: F33, the Arab Pangenome Reference trio (UAE, healthy father-mother-son, PacBio HiFi + ONT ultralong + Hi-C, phased assemblies for all 3, all data from peripheral blood, the first fully non-cultured open family). Wave-2 also surfaced three large CONTROLLED resources (Tibetan 35 trios, Asian Pan-Genome 160 trios, Emirati T2T trios) and several dead ends (section 7). Zhou H 2026 (three-generation Chinese family) remains UNRESOLVED: full text is bot-blocked everywhere reachable, no public accession found, and it is not counted. The four v02-era additions beyond the manifest 13 stand: GIAB Ashkenazi trio, GIAB Chinese trio, T2T-CQ Chinese Quartet, PAN027/WashU pedigree; the Platinum Pedigree (CEPH 1463) remains the largest single source (23/28 members open). Note for Max: the remembered number 17 matches 13 + 2 GIAB + T2T-CQ + PAN027; the census then grew to 32 via Platinum Pedigree and to 33 via the APR trio.

# 1. Headline counts

| Metric | Count |
|---|---|
| Unique open-access complete families | 33 |
| Complete trios across them | 36 |
| Families with assemblies downloadable for ALL members | 19 (T2T-class, near-T2T, or chromosome-scale phased) |
| Families with partial assemblies | 1 (GIAB Ashkenazi: HG002 T2T only) |
| Families with reads only | 13 (6 Vienna trios, GIAB Chinese trio, and GIAB parents HG003/HG004 within the Ashkenazi trio) |
| Families fully from non-cultured material | 1 (F33 APR trio, all data from blood; next closest: Platinum Pedigree and PAN027, HiFi from blood) |

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

Note on assembly methods by generation (verified 2026-08-06 in s3://platinum-pedigree-data): G1-G3 members have Verkko near-T2T assemblies; G4 members (200081-200087, 200101-200106) have hifiasm diploid assemblies only.

## Group V: Arab Pangenome Reference trio (1 family, added in v03)

F33 - APR trio (Nassir et al. 2025 Nature Communications, "A draft UAE-based Arab pangenome reference", PMID 40707445, DOI 10.1038/s41467-025-61645-w, full text PMC12290100 cached):
- Members: APR-F (father), APR-M (mother), APR-S (son). Healthy trio with no known rare or common chronic disease, enrolled among 53 Arab individuals (50 unrelated + this trio) residing in the UAE.
- Material: peripheral blood (8-10 ml per person); no LCL/EBV transformation anywhere in the paper. FIRST fully non-cultured open-access family.
- Data (all open): PacBio HiFi 35.27X (pbAPR-F/M/S, Revio + Sequel IIe) + ONT ultralong 54.22X (APR-F/M/S, PromethION) + Hi-C 65.46X, per the paper; per-member HiFi and UL-ONT runs verified in ENA. Reads: SRA PRJNA1108179 (metadata SRP509490).
- Assemblies (OPEN): haplotype-phased de novo assemblies for all 53 samples (106 haplotype projects), average N50 124.28 Mb (chromosome-scale, not T2T). GenBank BioProjects PRJNA1151091-PRJNA1151118 and PRJNA1152014-PRJNA1152091 (e.g. GCA_050491585.1 = apr052.2 v1, biosample tissue=Blood); all sample FASTAs plus pangenome files also at https://www.mbru.ac.ae/the-arab-pangenome-reference/ . Trio sample-name mapping to assembly projects must be resolved at download time (assemblies are named aprNNN.haplotype; Supplementary Table 1 maps IDs).
- Note: the other 50 samples are unrelated individuals (pangenome panel), not families.

# 3. Quality ranking for the download branch (assemblies first)

Tier 1 - T2T-class phased diploid assemblies (download first):
1. F17 PAN027: 4 members, UCSC hosting + NCBI, HiFi from blood
2. Platinum Pedigree: 23 members, s3://platinum-pedigree-data + ENA PRJEB86317, HiFi from blood
3. F01-F03 HGSVC3: 9 members, Verkko ENA PRJEB76276
4. F16 T2T-CQ: twins' diploid genome T2T (2 haplotypes) via GWH; parents' v2.0 assemblies to verify; raw reads controlled
5. F33 APR trio: 3 members, chromosome-scale phased assemblies (N50 ~124 Mb), GenBank + mbru.ac.ae direct FASTA; all data from blood (top pick for the non-cultured priority)

Tier 2 - solid assemblies from ONT-only input:
6. F04-F07 LRSC (s3://1000g-ont PROCESSED_DATA/ASSEMBLIES/; F04 child also has HGSVC3 Verkko)

Tier 3 - one-member T2T:
7. F14 GIAB Ashkenazi (HG002 T2T v2.7 only)

Tier 4 - reads only (assemble later if needed):
8. F10-F13 Vienna (F08/F09 covered by Platinum Pedigree instead)
9. F15 GIAB Chinese trio

Estimated assembly-only payload: roughly 250-350 GB.

# 4. Access verification evidence (all live checks 2026-08-06)

- Platinum Pedigree: S3 bucket lists assemblies/ for all 23 open members; ENA PRJEB86317 returns exactly those 23; paper data-availability section splits open (AWS + ENA) vs dbGaP (5 members).
- PAN027: NCBI esummary confirms GCA_046332035.2 (PAN027_pat_v1.1, UCSC Genomics Institute, isolate HG06807); washu-pedigree README lists SRP320775 accessions for all 4 members and direct FASTA URLs v1.0-v1.3.1; Dong 2026 full text (cached) confirms pedigree structure and LCL origin.
- GIAB: FTP confirms trio folder names with PGP donor IDs; T2T-HG002-XY-v2.7 present.
- T2T-CQ: Europe PMC full text (cached) confirms LCL5/LCL6 twin daughters + LCL7/LCL8 parents, LCL material, GWH accessions, GSA-Human HRA010594; GSA-Human policy page (Agent D) confirms controlled default for reads.
- HGSVC3: cached accession table confirms coverages (HiFi 31-68x, ONT 61-81x) and GCAs; one HG00512 ONT run flagged contaminant (exclude).
- F33 APR trio (2026-08-06, wave-2): PMC12290100 full text confirms 50 unrelated + 1 healthy trio, blood collection, HiFi+UL+Hi-C coverages, and the assembly accession ranges; ENA filereport for PRJNA1108179 returns per-member runs for APR-F/APR-M/APR-S (PacBio pbAPR-* and ONT APR-*, 2 runs each); NCBI esummary confirms indexed assemblies (GCA_050491585.1 apr052.2 v1; GCA_050492395.1 apr041.2 v1) with biosample tissue=Blood; Datasets API confirms isolation_source=blood.

# 5. Cultured vs non-cultured material

One open-access family is fully non-cultured as of v03:
- F33 APR trio: HiFi, UL-ONT, and Hi-C all from peripheral blood DNA; no LCL/EBV anywhere in the paper. Best match for the non-cultured priority.
Every other family uses EBV LCLs for at least part of its data:
- Platinum Pedigree: HiFi/Illumina/Element from blood; UL-ONT/Strand-seq from LCL; assemblies LCL-ONT based, blood-HiFi polished.
- PAN027: HiFi from blood; ONT/Hi-C/Element from LCL; assemblies polished with blood HiFi.
- T2T-CQ: B-lymphoblastoid cell lines throughout (confirmed).
- All 1KGP/HGSVC/LRSC/Vienna/GIAB families: LCL throughout.
Additional fully non-cultured (blood) complete families exist behind controlled access: Tibetan pangenome 35 trios (blood DNA, GSA-Human DAC), MSSNG blood-derived, etc.; see section 7 and the CONTROLLED_ACCESS_CANDIDATES doc.

# 6. Saturation status and remaining unknowns

Wave-1 (Agent D, qwen3.7-plus) swept NGDC/CNCB, KPGP/KOREF (Korea), Japanese T2T, GenomeIndia, Qatar/Saudi/Emirati, H3Africa, Latin America, HPRC2, and ~100 recent PubMed papers. Wave-2 (2026-08-06, agents E/F/G, qwen3.7-plus) added: ~700 more papers screened (E), ENA/NCBI/SRA metadata mining for family-labeled submissions 2022-2026 (F), and a regional sweep of SE Asia, Central Asia, Turkey/Iran, North Africa, Sub-Saharan Africa, Indigenous Oceania, Latin America, and 2025-2026 pangenome labs (G). Wave-2 verdict: exactly ONE new open family (F33 APR trio), verified end-to-end here; all other wave-2 candidates resolved as controlled, incomplete families, unrelated individuals, or unverifiable (section 7). Census is saturated for public knowledge as of 2026-08-06. Remaining unknowns (low priority for assembly-first scope):
- Zhou H et al. 2026 (JGG DOI 10.1016/j.jgg.2026.03.011, PMID 41905586, three-generation healthy Chinese family, high-depth ONT + HiFi, proband-specific T2T assembly): UNRESOLVED and NOT counted. Full text is CC-BY but unreachable: ScienceDirect Cloudflare captcha from every route tried (direct, curl, Playwright real-Chrome, r.jina.ai, Wayback 2026-07-02/07-31 captures are 403); no PMC/EPMC/DOAJ/OpenAlex/Semantic Scholar OA copy; no preprint; GSA-Human pending list (810 datasets) and NCBI SRA contain no matching deposit; GWH advanced-search backend returns HTTP 400 (broken) and its public API is ID-lookup only. Even if opened, the assembly is proband-only (1 member), so the family would count at best as reads-only. Suggested route if Max wants it: ask the corresponding authors (Kwok-Wing Tsui, CUHK; Jue Ruan, AGIS/CAAS) for the data accessions; requires Max's approval to send.
- T2T-CQ parents' assembly accessions (CQ v2.0) unverified.
- Mortazavi 2026 Cell Genomics (autism LRS): likely controlled, no accessions found.
- Sasani 2026 (Platinum Pedigree companion, tandem repeats): preprint unfetchable; data expected to follow Platinum Pedigree open/dbGaP split.
- Kramer/McCombie cancer pedigrees (bioRxiv 10.1101/2024.06.27.601096, PMID 39005350, 2 colorectal-cancer trios + 1 testicular-cancer quad, ONT PromethION): UNRESOLVED, not counted. No SRA/ENA deposit found by sample or study terms; no peer-reviewed publication since 2024; full text unreachable (bioRxiv rate-limited this session).
- Central Asian Genomic Diversity (agent G report: 166 individuals, PacBio HiFi, "GVM000900"): family structure and accession unverified; treated as unrelated individuals until proven otherwise.

# 7. Verified dead ends (do not re-search)

Controlled access: Ivashchenko 2026 (10 PacBio trios, EGA EGAS00001008250); Negi 2025 (41 families, likely dbGaP); Werren 2026 (20 clinical families); Noyes 2026 Nat Commun (Eichler lab families, SFARI Base SFARI_DS0000104 + NDA Collection 3780); Platinum Pedigree non-consented 5 members (dbGaP phs003793.v1.p1); T2T-CQ raw reads (GSA-Human DAC); clinical rare-disease trio LRS studies generally; Ghorbani et al. 2025 Nat Genet (PMC12081309, 6 Middle Eastern family trios - Sudan/Jordan/Syria/Qatar/Afghanistan - PacBio HiFi ~38x, dbGaP phs003917.v1.p1); Tibetan near-complete pangenome (bioRxiv 10.64898/2025.12.16.694547, 35 trios / 105 individuals, 70 near-complete phased assemblies, HiFi + UL-ONT + short-read from BLOOD, BioProject PRJCA043737 across GSA-Human/GWH/GVM, controlled via KIZ-CAS DAC - largest controlled family resource found); Asian Pan-Genome (Wu et al. 2026 bioRxiv, 160 trios, GSA-Human HGV000009, controlled; accession as reported by agent G, unverified); Emirati T2T pangenome (EGA EGAS50000001232, controlled; reported trio count inconsistent in source, unverified); Down syndrome families AJHG 2026 (dbGaP phs003761.v1.p1, chr21 centromeres only); IRUD Japanese trios J Hum Genet 2026 (12 clinical trios, no PMC, likely controlled); KCNC2 autism family (5 members, PacBio HiFi, dbGaP phs002698).
Not complete long-read families: HPRC year-1 + HPRC_PLUS + HPRC2 (unrelated individuals by design; PAN027 members and HG00733 live there as individuals); HGSVC3 recount (exactly 3 trios); KOREF_S1 Korean reference (parents short-read only, PMID 35333300); Korean Pangenome Project (Jang et al. 2025 medRxiv 10.1101/2025.07.08.25330875: 40 individuals from 33 previously undiagnosed rare-disease families, i.e. proband-centric, NOT complete trios; the agent-reported accession PRJNA1122054 does not exist in NCBI BioProject or SRA - verified 2026-08-06); Japanese T2T Suzuki 2026 (10 unrelated males); Niu 2022 Chinese pangenome (32 unrelated); GenomeAsia (short-read); All of Us, TOPMed, UK Biobank, deCODE, Estonian Biocentre, H3Africa (restricted); IGSR (nothing beyond the 3 known collections); 22q11.2 study Nat Commun 2025 (PMC12236504: NA10382/NA10383/NA10384 = Coriell GM10382-84, "publicly available" refers to the cell lines only - no trio reads or assemblies in SRA or ENA, clinical families in EGA, only 22q11.2-region FASTAs on Zenodo 10.5281/zenodo.15790793; agent E's "already known 1000G" label was wrong); MENA nanopore SV study (bioRxiv 10.64898/2026.02.20.26346743: 61 unrelated individuals, reanalysis of public UL-ONT data); VN1K Vietnamese pangenome (Nat Commun 2026, PMID 42486871: no family component; long reads used only for methylation); JaSaPaGe (9 Saudi + 10 Japanese, unrelated); G10K-VGP mHomSap3 trio (PRJNA1008626: son's PacBio reads open but parents never deposited - 1 of 3 members public; ONT clinical-readiness project PRJNA1334404 includes a trio but data not released).
