# Consortia & Pangenome Report: Open-Access Long-Read Family Datasets

**Agent:** A (Consortia scope)
**Date:** 2026-08-06
**Scope:** HPRC, HGSVC3 full recount, HGSVC2, GIAB, All of Us, TOPMed, UK Biobank, deCODE, Estonian Biocentre, IGSR data collections, Korean/Chinese/GenomeAsia/H3Africa projects

---

## NEW CANDIDATES FOUND

### 1. GIAB Ashkenazi Trio (HG002 / HG003 / HG004)

- **Resource name:** Genome in a Bottle (GIAB) Ashkenazi Trio
- **Paper/DOI:** Zook et al. 2016 Nat Biotechnol (10.1038/nbt.3440); T2T-HG002 in Liao et al. 2023 Nature (10.1038/s41586-023-05896-x)
- **Number of complete long-read families:** 1 trio (3 individuals)
- **Technology + coverage:**
  - HG002: PacBio HiFi (Revio, SequelII CCS 11kb/15kb/20kb), ONT ultralong (Promethion, Cornell ONT)
  - HG003: PacBio HiFi (Revio, CCS 15kb/20kb), ONT ultralong (Promethion)
  - HG004: PacBio HiFi (Revio, CCS 15kb/20kb/21kb), ONT ultralong (Promethion)
- **De novo assemblies:** HG002 has a T2T diploid assembly (v1.1, T2T Consortium collaboration). HG003/HG004 assemblies not confirmed at T2T-level.
- **Sample material:** Coriell cell lines (LCLs). Coriell IDs: NA24385 (HG002/son), NA24149 (HG003/father), NA24143 (HG004/mother).
- **Access URLs:**
  - https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/data/AshkenazimTrio/
  - AWS S3: s3://giab
  - GitHub index: https://github.com/genome-in-a-bottle/giab_data_indexes
- **Open-access evidence:** Direct FTP and S3 download. No DAC, no registration, no data-access agreement. NCBI FTP with no embargo.
- **Relationship to HGSVC3:** HG002/HG003/HG004 are NOT in HGSVC3 (verified via ENA PRJEB76276/PRJEB83624 sample list). Separate GIAB reference samples from the Personal Genome Project.
- **Relationship to HPRC:** HG002 appears in HPRC_PLUS directory on HPRC S3 bucket, but HPRC_PLUS is an extension set, not a family collection.

### 2. GIAB Chinese Trio (HG005 / HG006 / HG007)

- **Resource name:** Genome in a Bottle (GIAB) Han Chinese Trio
- **Paper/DOI:** Zook et al. 2016 Nat Biotechnol (10.1038/nbt.3440); same consortium as Ashkenazi trio
- **Number of complete long-read families:** 1 trio (3 individuals)
- **Technology + coverage:**
  - HG005: PacBio CCS (SequelII 11kb, 15kb/20kb chemistry2), ONT ultralong (Promethion)
  - HG006: PacBio HiFi (Google, CCS 15kb/20kb), ONT ultralong (Promethion)
  - HG007: PacBio HiFi (Google, CCS 15kb/20kb), ONT ultralong (Promethion)
- **De novo assemblies:** Not confirmed as T2T-level; may have draft assemblies.
- **Sample material:** Coriell cell lines (LCLs). Coriell IDs: NA24631 (HG005/son), NA24694 (HG006/father), NA24695 (HG007/mother). PGP IDs: huCA017E (father), hu38168 (mother).
- **Access URLs:**
  - https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/data/ChineseTrio/
  - AWS S3: s3://giab
- **Open-access evidence:** Direct FTP and S3 download. No DAC, no registration. Consent from Personal Genome Project for commercial redistribution.
- **Relationship to HGSVC3:** HG005/HG006/HG007 are NOT in HGSVC3.
- **Relationship to HPRC:** HG005 appears in HPRC_PLUS directory.

---

## VERIFIED: NO NEW COMPLETE LONG-READ FAMILIES

### HPRC (Human Pangenome Reference Consortium)

- **Year-1 release (47 individuals, Liao et al. 2023 Nature):** All 47 samples are unrelated individuals. No parent-offspring pairs. Verified by checking S3 bucket working/HPRC/ directory listing (398 sample directories, all unique individuals). The 47 diploid assemblies are from unrelated donors selected for diversity.
- **HPRC_PLUS (24 additional samples):** Includes HG002, HG005, HG00733, and other individuals. No additional complete families. These are supplementary assemblies, not a family collection.
- **Year-2 and later releases:** No published evidence of family trios with long reads for all members. HPRC strategy has been to sequence unrelated individuals for pangenome diversity, not families.
- **Conclusion:** HPRC contributes NO complete long-read families. Parents were sequenced with Illumina only for some year-1 samples (for phasing validation), but no trio has long reads for all three members.

### HGSVC3 Full Recount

- **ENA studies:** PRJEB76276 and PRJEB83624
- **Total unique samples:** 65 (confirmed from ENA portal API)
- **Complete trios with long reads:** Exactly 3, matching the already-known list:
  1. HG00512 (father) / HG00513 (mother) / HG00514 (child)
  2. NA19238 (father) / NA19239 (mother) / NA19240 (child)
  3. HG00731 (father) / HG00732 (mother) / HG00733 (child)
- **HG03371:** Child with an assembly, but parents not in HGSVC3.
- **HG02059:** Present in HGSVC3, but parents HG02060/HG02061 are NOT in HGSVC3.
- **HG002/HG003/HG004:** NOT in HGSVC3 (confirmed).
- **HG00619/HG00620/HG00621:** NOT in HGSVC3 (confirmed). HG00621 is a 1kGP child with parents HG00619/HG00620 in the 1kGP pedigree, but none are in HGSVC3.
- **Other parent-offspring pairs checked:** HG02086, HG02107, HG00622, HG00623 - none form complete trios in HGSVC3.

### HGSVC2 / Older HGSVC Releases

- **Search result:** No separate HGSVC2 long-read family data found. HGSVC3 supersedes earlier releases. The original HGSVC (now called HGSVC2) had Illumina data for trios, not long-read WGS for complete families.
- **Conclusion:** No additional complete long-read families beyond HGSVC3.

### All of Us Long-Read Pilot

- **Search result:** No published paper describing a long-read pilot with complete families and open-access data. All of Us Research Program data is accessed through the Researcher Workbench with data-use agreements. Not open access.
- **Conclusion:** DEAD END. Restricted access; no evidence of complete family long-read sets publicly downloadable.

### TOPMed Long-Read

- **Search result:** TOPMed is primarily short-read. Any long-read pilot data would be through dbGaP with controlled access. No open-access complete family long-read datasets found.
- **Conclusion:** DEAD END. dbGaP controlled access.

### UK Biobank Long-Read Pilots

- **Search result:** UK Biobank has initiated long-read sequencing (e.g., ONT) but data access requires application through the UK Biobank Access Management System. Not open access. No complete family trios publicly downloadable.
- **Conclusion:** DEAD END. Application-required access.

### deCODE Iceland Long-Read

- **Search result:** deCODE has long-read data on Icelandic families, but all data is restricted under deCODE's governance and Icelandic data protection law. Not publicly downloadable.
- **Conclusion:** DEAD END. Restricted access.

### Estonian Biocentre Long-Read

- **Search result:** No published open-access long-read family dataset from the Estonian Biocentre found. Estonian Genome Center data is typically accessed through controlled mechanisms.
- **Conclusion:** DEAD END. No open-access evidence.

### IGSR Data Collections

- **Checked:** https://www.internationalgenome.org/data-portal/data-collection
- **1000 Genomes-related long-read collections:** The three already-known collections (HGSVC3, 1kGP-LRSC, 1KG_ONT_VIENNA) are the only long-read family collections under IGSR/1kGP.
- **Conclusion:** No additional long-read family collections beyond the three already known.

### Korean Genome Projects (KOREF etc.)

- **Korean long-read genomes:** Cho et al. 2024 NAR (10.1093/nar/gkae1294) generated ~20x HiFi long-read data from 3 Korean individuals with phased assemblies. However, these 3 individuals are NOT a family trio - they are unrelated individuals selected for high-quality reference genomes.
- **KOREF:** Short-read based reference genome. No long-read family data found.
- **Conclusion:** DEAD END for families. Individual Korean genomes exist but not as a complete family.

### Chinese Pangenome Projects

- **Niu et al. 2022 Cell (32 diploid assemblies):** This paper generated 32 phased diploid assemblies from unrelated Chinese individuals using a combination of technologies. No family trios - the samples were selected for diversity, not relatedness.
- **Later Chinese pangenome papers:** No published complete family long-read datasets with open access found.
- **Conclusion:** DEAD END for families. Individual diploid assemblies exist but not as complete families.

### GenomeAsia 100K

- **Search result:** GenomeAsia is primarily short-read (Illumina) for 100K individuals. No long-read family dataset found.
- **Conclusion:** DEAD END. Short-read project.

### H3Africa Long-Read Efforts

- **Search result:** No published open-access long-read family dataset from H3Africa found. H3Africa data is accessed through the H3Africa BIOS study via controlled access.
- **Conclusion:** DEAD END. No open-access evidence.

---

## SUMMARY TABLE

| Dataset | Complete LR Families | Open Access | Notes |
|---------|---------------------|-------------|-------|
| **GIAB Ashkenazi Trio** | 1 (HG002/003/004) | YES | NEW finding |
| **GIAB Chinese Trio** | 1 (HG005/006/007) | YES | NEW finding |
| HGSVC3 | 3 (already known) | YES | Confirmed, no additions |
| 1kGP-LRSC | 4 (already known) | YES | Not re-verified in this scope |
| 1KG_ONT_VIENNA | 6 (already known) | YES | Not re-verified in this scope |
| HPRC year-1 | 0 | N/A | Unrelated individuals |
| HPRC_PLUS | 0 | N/A | Supplementary assemblies |
| HGSVC2 | 0 | N/A | No LR family data |
| All of Us | 0 | NO | Restricted access |
| TOPMed | 0 | NO | dbGaP controlled |
| UK Biobank | 0 | NO | Application required |
| deCODE | 0 | NO | Restricted |
| Estonian Biocentre | 0 | NO | No OA evidence |
| Korean projects | 0 | N/A | Individuals, not families |
| Chinese pangenome | 0 | N/A | Unrelated individuals |
| GenomeAsia 100K | 0 | N/A | Short-read |
| H3Africa | 0 | NO | Controlled access |

---

## TOTAL NEW CANDIDATES FROM THIS AGENT

**2 new complete open-access long-read families:**
1. GIAB Ashkenazi Trio (HG002/HG003/HG004) - PacBio HiFi + ONT
2. GIAB Chinese Trio (HG005/HG006/HG007) - PacBio HiFi + ONT

**Combined with already-known datasets, the full census of open-access complete long-read families now includes:**
- 3 HGSVC3 trios
- 4 LRSC trios
- 6 Vienna trios
- 1 GIAB Ashkenazi trio (NEW)
- 1 GIAB Chinese trio (NEW)
- **Total: 15 complete open-access long-read families**

---

## DEAD ENDS (with evidence checked)

- **HPRC:** S3 bucket listing of 398 samples; all unrelated. No family structure.
- **HGSVC3 full recount:** ENA API returned 65 samples; only 3 known trios confirmed. HG002/003/004, HG00619/620/621, HG02060/61/59 not in HGSVC3.
- **All of Us, TOPMed, UK Biobank, deCODE, Estonian, H3Africa:** All restricted/controlled access. No open downloads.
- **Korean, Chinese pangenome, GenomeAsia:** Individual genomes or short-read; no complete families with long reads.
- **IGSR data collections:** No additional long-read family collections beyond the 3 already known.
