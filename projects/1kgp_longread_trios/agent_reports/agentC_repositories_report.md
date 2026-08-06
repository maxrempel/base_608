# Agent C: Direct Repository Mining Report
## Open-Access Human Family Long-Read WGS Census

**Date:** 2026-08-06
**Agent:** C (repository mining)
**Scope:** ENA, NCBI SRA, NCBI Assembly, DDBJ

---

## Summary

**NEW OPEN-ACCESS COMPLETE FAMILY DATASET FOUND:**

1. **GIAB Ashkenazim Trio (HG002/HG003/HG004) with PacBio HiFi**
   - Study Accession: PRJNA1028149
   - Complete family: YES (father HG003/NA24149, mother HG004/NA24143, son HG002/NA24385)
   - Technology: PacBio Sequel II (HiFi/CCS)
   - Coverage: ~30-40x per sample (one Revio SMRT Cell per sample)
   - Assemblies: Multiple available via GIAB consortium
   - Sample material: Coriell cell lines (EBV-transformed lymphoblastoid)
   - Open access: YES - public SRA runs
   - Public URLs:
     - SRA: https://www.ncbi.nlm.nih.gov/sra/SRP26402937
     - ENA: https://www.ebi.ac.uk/ena/browser/view/PRJNA1028149
   - First public: 2023-10-17
   - Paper: GIAB consortium; PacBio Revio dataset release
   - **UNVERIFIED:** Exact per-sample coverage from metadata alone

---

## Already Known Datasets (Confirmed in Repository Searches)

### 1. HGSVC3 Trios
- **Han Chinese Trio (HG00512/HG00513/HG00514)**
  - Study: PRJEB12236 (original 2015 PacBio RS II), also in HGSVC3 PRJEB76276/PRJEB83624
  - Status: Already known

- **Yoruban Trio Y117 (NA19238/NA19239/NA19240)**
  - Study: PRJNA288807 (original 2015 PacBio RS), also in HGSVC3
  - NA19240 also has Sequel II data (SRR11363956) and ONT data in HPRC PLUS
  - Status: Already known

- **HG00731/732/733 trio** - Part of HGSVC3. Already known.

### 2. 1kGP-LRSC
- Trios: HG03370/69/71, HG00704/05/06, HG02026/25/24, HG02613/14/15
- Status: Already known

### 3. 1KG_ONT_VIENNA
- ENA: PRJEB89727
- Includes NA12878 family (CEPH/Utah Pedigree 1463: NA12878/NA12891/NA12892)
- Status: Already known

---

## Investigated and Rejected

| Accession | Title | Reason for Rejection |
|-----------|-------|---------------------|
| PRJNA1167349, PRJNA1167350 | Platinum Pedigree Consortium Long-Read Sequencing | dbGaP controlled access. 4-generation CEPH-Utah family 1463 with 17+ members, PacBio Revio + ONT PromethION. Description explicitly states "Data available through dbGaP." |
| PRJNA701308, PRJNA731524 | HPRC Genome Sequencing / HPRC PLUS | Individual-based, not designed as family study. ~350 individuals including some from 1000G trios, but not a "complete family dataset." |
| PRJNA586841 | Simons Genome Diversity Project | Individuals only, no family relationships |
| PRJNA167318, PRJNA488321, PRJNA488322 | Simons Simplex Collection | Autism family studies, likely dbGaP-controlled, not confirmed long-read WGS |
| PRJNA230425, PRJNA230426 | Bulgarian schizophrenia trio sequencing | Likely short-read Illumina, not long-read WGS |
| PRJNA549351 | KOREF Korean reference genome | Individual reference genome, not family study |
| PRJDB10452, PRJDB19788 | Japanese reference genome projects | Individual reference genomes, not family studies |
| PRJNA1169852 | Long-read direct RNA sequencing of GIAB HG002/HG004/HG005 | RNA-seq (transcriptomic), NOT WGS. ONT dRNA-seq for Clair3-RNA variant caller. |
| PRJNA607914 | Ashkenazi Human Reference Genome | Investigated but no complete trio long-read WGS confirmed |

---

## Repository Search Methodology

### ENA Portal API Queries:
- tax_eq(9606) AND instrument_model="PromethION" -> multiple studies
- study_title="trio/family/pedigree" AND tax_eq(9606) -> limited results (API limitations)
- study_title="Ashkenazi/GIAB/NIST" AND tax_eq(9606) -> found PRJNA1028149
- study_title="Yoruban/CEPH/HPRC/pangenome" -> found known datasets
- study_title="HG002/HG003/HG004" -> confirmed individual projects
- study_title="long-read" AND trio/family -> found Platinum Pedigree

### NCBI SRA/eutils:
- "human trio nanopore" -> 44 results, mostly HPRC PLUS (NA19240) and GIAB RNA-seq
- "human family pacbio" -> 2649 results (broad, mostly unrelated)
- Specific BioProject queries for PRJNA730823, PRJNA1028149, etc.

---

## Key Findings

### New Open-Access Complete Family:
**GIAB Ashkenazim Trio (PRJNA1028149)** - 1 complete family
- Deliberate trio design (father + mother + child)
- All three members have PacBio HiFi WGS from Revio system
- Public SRA/ENA access, no controlled access required
- Part of NIST Genome in a Bottle reference material program
- The trio is widely used as a benchmark for variant calling

### Important Distinctions:
1. HPRC is NOT a family dataset - sequences individuals, not families by design
2. Platinum Pedigree has 17+ members with long-read data but is dbGaP-controlled
3. GIAB Ashkenazim trio (HG002/HG003/HG004) is DISTINCT from HGSVC3 trios
4. PRJNA1169852 has the same GIAB trio members but is RNA-seq, not WGS

---

## Final Count

**New open-access complete-family long-read WGS datasets found: 1**
- GIAB Ashkenazim Trio (PRJNA1028149): HG002/HG003/HG004, PacBio HiFi

**Already known (confirmed present in repositories):**
- HGSVC3: 3 trios (HG00512/513/514, NA19238/239/240, HG00731/732/733)
- 1kGP-LRSC: 4 trios
- 1KG_ONT_VIENNA: 6 trios including NA12878 family

**Total open-access complete families with long-read WGS: 14 trios**
(3 HGSVC3 + 4 1kGP-LRSC + 6 1KG_ONT_VIENNA + 1 GIAB Ashkenazim)
