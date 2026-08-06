# Agent B: Literature Sweep Report
## Open-Access Complete-Family Long-Read WGS Studies (2016-2026)

**Date:** 2026-08-06  
**Agent:** B (literature sweep)  
**Scope:** PubMed eutils, Europe PMC full-text, NCBI Assembly/BioProject  
**Queries run:** 7 PubMed queries (long-read + family/trio/pedigree + assembly/SV/methylation/T2T/multi-generational), Europe PMC full-text extraction for key papers, NCBI BioProject/Assembly searches

---

## NEW OPEN-ACCESS COMPLETE-FAMILY DATASETS FOUND

### 1. T2T-CQ: Chinese Quartet (T2T diploid assemblies of a family of four)

| Field | Value |
|-------|-------|
| **First author** | Wang Bo |
| **Year** | 2025 |
| **Journal** | Genomics, Proteomics & Bioinformatics |
| **DOI** | 10.1093/gpbjnl/qzaf118 |
| **PMID** | 41298323 |
| **PMCID** | PMC13075991 |
| **Family structure** | Quartet: father + mother + monozygotic twin sons (4 individuals, 1 complete trio + 1 MZ co-proband) |
| **Technology** | ONT ultralong + PacBio HiFi (high coverage) |
| **Assemblies** | T2T haplotype-phased diploid assemblies for all 4 members. Maternal: GWHFQEY00000000.1; Paternal: GWHFQEX00000000.1 |
| **Raw data** | GSA-Human: HRA010594 (NGDC/CNCB, publicly accessible at ngdc.cncb.ac.cn/gsa-human) |
| **Assembly data** | Genome Warehouse (GWH) at NGDC/CNCB: ngdc.cncb.ac.cn/gwh |
| **Sample material** | UNVERIFIED (likely EBV-transformed LCLs from the Quartet reference panel) |
| **Open access confirmed** | YES - raw reads + assemblies both publicly downloadable |
| **Notes** | Part of the Chinese Quartet reference material project. Updated higher-quality T2T assembly of the original CQ resource. GCI scores 77.76 (maternal) / 76.41 (paternal), QV > 66, CRAQ > 99.6. Novel 13-mer higher-order repeat patterns on chr17 identified. |

### 2. PAN027 / WashU Pedigree (T2T assemblies of a 3-generation African American family)

| Field | Value |
|-------|-------|
| **First author** | Cechova M (co-first with Potapova TA, Rechtsteiner A, Hickey G, et al.) |
| **Year** | 2025 (bioRxiv preprint, posted 2025-12-14) |
| **DOI** | 10.64898/2025.12.14.693655 |
| **PMID** | 41473289 |
| **PMCID** | PMC12746033 |
| **Family structure** | 4 individuals spanning 3 generations (African American, admixed ancestry). Contains at least one complete trio (father + mother + child). |
| **Technology** | ONT + PacBio HiFi (Verkko + hifiasm assemblies) |
| **Assemblies** | T2T diploid assemblies: paternal GCA_046332035.1, maternal GCA_046332005.1; BioSample SAMN33621959 |
| **Raw data** | AWS bucket accessible via GitHub: github.com/biomonika/HPP/tree/main/T2T-Pedigree-project |
| **Code** | github.com/biomonika/washu-pedigree |
| **Sample material** | UNVERIFIED (likely blood-derived; EBV-transformed LCLs possible) |
| **Open access confirmed** | YES - assemblies at NCBI GenBank, reads via AWS, code on GitHub |
| **Notes** | Parent-of-origin assigned chromosome-level assemblies. Revealed recombination breakpoints in acrocentric/subtelomeric regions. Complete rDNA array for paternal chr14. Also described in a companion centromere paper (Dong S et al. 2026, PMID 41756947, same family). |

### 3. Dong et al. 2026 (same PAN027 family, centromere focus)

| Field | Value |
|-------|-------|
| **First author** | Dong S |
| **Year** | 2026 (bioRxiv preprint, posted 2026-02-17) |
| **DOI** | 10.64898/2026.02.14.705860 |
| **PMID** | 41756947 |
| **PMCID** | PMC12934683 |
| **Family structure** | Same 3-generation pedigree as Cechova et al. above (PAN027/WashU pedigree) |
| **Technology** | Long-read (ONT + HiFi) + long-read epigenomes from PBMCs, iPSCs, and neural progenitor cells |
| **Assemblies** | Fully phased T2T diploid assemblies (same as Cechova et al.) |
| **Open access confirmed** | YES - same dataset as Cechova et al. above |
| **Notes** | Companion paper focusing on centromere genetic/epigenetic dynamics across inheritance and cell-fate transitions. NOT a separate family; counts as the same dataset as #2. |

---

## MAJOR DATASET WITH UNCERTAIN DATA ACCESS

### 4. CEPH 1463 (four-generation, 28-member pedigree)

| Field | Value |
|-------|-------|
| **First author** | Porubsky D |
| **Year** | 2025 (Nature, published 2025-07) |
| **DOI** | 10.1038/s41586-025-08922-2 |
| **PMID** | 40269156 |
| **PMCID** | PMC12240836 |
| **Family structure** | 28 members, 4 generations (G1-G4). Multiple complete trios embedded within the pedigree. |
| **Technology** | Five complementary technologies: PacBio HiFi, ONT, Strand-seq, Bionano, and short-read Illumina |
| **Assemblies** | Near-T2T phased diploid assemblies for >95% of each genome across all 28 members |
| **Data access** | **UNVERIFIED** - Paper claims "most comprehensive, publicly available truth set" but no specific SRA/BioProject/ENA accession found in the full text. Multiple BioProjects exist for CEPH 1463 (IDs: 647458, 323611, 205701, etc.) but none specifically matched to the long-read data. Data may be distributed through HPRC/GIAB or may require dbGaP access for raw reads. |
| **Sample material** | Primary material and EBV-transformed LCLs (cell line artefacts discussed in paper) |
| **Notes** | Multiple follow-up papers use this same dataset: Sasani TA et al. 2026 (PMID 41959501, tandem repeat mutagenesis, PacBio HiFi); Gao S et al. 2026 (PMID 42527608, centromere variation, Nature). All share the same CEPH 1463 resource. **STATUS: UNVERIFIED - data access needs confirmation via HPRC portal or dbGaP.** |

---

## THREE-GENERATION FAMILY (DATA ACCESS UNCERTAIN)

### 5. Zhou H et al. 2026 (three-generation Chinese family, methylation focus)

| Field | Value |
|-------|-------|
| **First author** | Zhou H |
| **Year** | 2026 |
| **Journal** | Journal of Genetics and Genomics |
| **DOI** | 10.1016/j.jgg.2026.03.011 |
| **PMID** | 41905586 |
| **Family structure** | Three-generation healthy Chinese family (at least 3 individuals spanning 3 generations, likely at least 1 complete trio) |
| **Technology** | ONT + PacBio HiFi (high-depth), anchored to proband-specific T2T assembly |
| **Assemblies** | Proband-specific T2T genome assembly produced |
| **Data access** | **UNVERIFIED** - Not in Europe PMC (openAccess=N, inEPMC=N). Published by Elsevier. Full-text not available for data availability extraction. |
| **Notes** | Focus on haplotype-resolved DNA methylation inheritance. 23 high-confidence imprinting control regions mapped. |

---

## CONTROLLED-ACCESS / REJECTED STUDIES (Notable)

| Study | PMID | Family | Tech | Reason for exclusion |
|-------|------|--------|------|---------------------|
| **Ivashchenko et al. 2026** - PacBio methylation episignatures | 41588467 | 10 trios (~30 individuals) | PacBio HiFi ~30x | **EGA controlled access** (EGAS00001008250). "Access is controlled and available upon request and approval by the data access committee." |
| **Negi et al. 2025** - Napu pipeline, rare disease | 39862869 | 41 families, 98 samples | ONT ~36x | **Likely controlled access** - No SRA BioProject found. Center for Mendelian Genomics / Broad Institute data typically in dbGaP. Clinical rare-disease cohort. |
| **Werren et al. 2026** - Clinical LR-GS reanalysis | 42050932 | 19 children + parents (20 families) | PacBio HiFi | **Clinical cohort** - Jackson Laboratory / Connecticut Children's. Data likely controlled access. |
| **Stacey et al. 2024** - Retinoblastoma parent-of-origin | 39724000 | 16 participants (7 familial + 9 de novo) | Targeted ONT long-read | **Targeted sequencing** (not WGS). Patent filed. Data likely restricted. |
| **Batlle-Maso et al. 2026** - Hereditary angioedema | 41896320 | 3-generation family | LR-WGS (ONT) + OGM | **Single rare-disease family** - clinical diagnostic study. Data access not stated as public. |
| **Rakwongkhachon et al. 2026** - BAFME epilepsy | 41874439 | 3 multigenerational families, 18 affected | Targeted adaptive sampling ONT | **Targeted sequencing** (not WGS). Focused on repeat expansion loci only. |
| **Cheung et al. 2023** - HiFi 5-base methylation, rare disease | 37248219 | Rare disease cohort | PacBio HiFi | **Likely controlled access** - clinical rare disease cohort. |
| **Khazeeva et al. 2022** - DeNovoCNN | 35713566 | WES trios (5616) + validation trios | WES + PacBio HiFi validation | **Not long-read WGS** - primarily short-read; PacBio only for validation of select variants. |

---

## ALREADY KNOWN (Not re-reported per instructions)

- HGSVC3 trios (HG00512/513/514, NA19239/238/240, HG00731/732/733)
- 1kGP-LRSC / s3 1000g-ont trios (HG03370/69/71, HG00704/05/06, HG02026/25/24, HG02613/14/15)
- 1KG_ONT_VIENNA (6 trios including NA12878 family)
- 1KGP high-coverage short-read cohort (not long-read)

---

## SUMMARY

### New open-access complete-family long-read WGS datasets found: 2 (plus 1 same-family companion paper)

1. **T2T-CQ Chinese Quartet** - 4 members (father + mother + MZ twin sons), ONT + HiFi, T2T assemblies, openly deposited at NGDC/CNCB (GSA-Human HRA010594, GWH assemblies)
2. **PAN027/WashU Pedigree** - 4 individuals, 3 generations, African American, ONT + HiFi, T2T assemblies (GCA_046332035.1 / GCA_046332005.1), openly on GitHub + AWS

### Major dataset with uncertain access: 1
3. **CEPH 1463** - 28 members, 4 generations, Nature 2025. Claims public availability but specific open-data repository not confirmed. Needs verification via HPRC/GIAB portals.

### Controlled-access dead ends:
- **Ivashchenko et al. 2026** - 10 PacBio HiFi trios, EGA controlled (EGAS00001008250)
- **Negi et al. 2025** - 41 rare-disease families, ONT, no public SRA found (likely dbGaP)
- **Werren et al. 2026** - 20 clinical families, PacBio HiFi, likely controlled
- Multiple single-family rare-disease studies with targeted or clinical data behind institutional access

### Key observation:
The open-access complete-family long-read WGS landscape is dominated by **reference genome projects** (T2T-CQ, PAN027, CEPH 1463) rather than clinical cohorts. Clinical rare-disease trio long-read studies are overwhelmingly controlled-access through dbGaP or EGA. No additional open-access population-scale family long-read datasets beyond the already-known HGSVC3, 1kGP-LRSC, and 1KG_ONT_VIENNA were found.
