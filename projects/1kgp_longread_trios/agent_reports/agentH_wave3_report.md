# Agent H: Wave 3 Report - Saturation Re-Verification and One Census Correction

**Date:** 2026-08-06
**Agent:** H (wave-3, direct verification, DeepSeek Codex session on branch codex/q38-longread-census)
**Task:** Verify every remaining wave-2/3 lead, run fresh saturation searches across literature and repositories, and update the census to v04 with any qualifying families.

## Summary

- New open-access complete long-read families found: **0**
- Wave-3 verdict: no new open families; several large controlled resources documented as near-misses.
- **Census correction:** T2T-CQ (F16) is REMOVED from the counted census. The GPB paper methods and live GSA-Human records show the parents (LCL7/LCL8) have short-read Illumina only, so this is not a complete long-read family.
- Census v04 headline: **32 unique open-access complete families / 34 complete trios** (was 33/36 in v03).
- bioRxiv full texts remained 429-rate-limited all session; CQ-chrY and Kramer/McCombie stay UNRESOLVED.

---

## Methods

- Europe PMC full-text XML for PMC-indexed papers (Mozilla user agent; works for PMC releases, not preprint PPR IDs).
- ENA portal API study-title sweeps (field-qualified terms such as `study_title="trio"`).
- NCBI E-utilities: SRA esearch/esummary and `efetch rettype=runinfo` for platform verification.
- NGDC BIG Search API (`https://ngdc.cncb.ac.cn/search/api/specific?db=hra&q=...`) for GSA-Human record discovery.
- GSA-Human AJAX endpoints (`/gsa-human/ajaxb/indinstudy` and `/runinstudy`) for per-study sample and platform verification.
- Live GVM page checks for Chinese/NGDC deposits.
- bioRxiv full text: HTTP 429 (rate-limited) on every attempt, including both DOI prefixes (10.1101 and 10.64898) for the new CQ-chrY preprint.

---

## Verified leads

### 1. duoNovo, Pediatrics Mendelian Genomics (AJHG 2026) - CONTROLLED NEAR-MISS

| Field | Value |
|---|---|
| Paper | duoNovo, American Journal of Human Genetics 2026, DOI 10.1016/j.ajhg.2026.02.006, PMC12987547 |
| Scale | 122 individuals from 38 trios + 2 quads |
| Platform | PacBio Revio HiFi |
| Center | Pediatrics Mendelian Genomics Research Center (GREGoR consortium) |
| Access | **CONTROLLED** - deposited via GREGoR on AnVIL/dbGaP, dbGaP phs003047 |
| Verdict | Does NOT count. Recorded as a near-miss with exact counts and phs003047. |

### 2. Noyes 2026 Nature Communications (Eichler lab) - ALREADY KNOWN CONTROLLED

- Confirmed the already-known controlled resource: SFARI Base SFARI_DS0000104 + NIMH Data Archive Collection 3780, 42 families (31 quads + 11 trios). Full text re-verified from cached XML.
- Already in census v03 section 7. Dead end, no new information.

### 3. Zhou H 2026 JGG three-generation Chinese family - UNRESOLVED, NOT COUNTED

| Field | Value |
|---|---|
| Paper | Journal of Genetics and Genomics 2026, DOI 10.1016/j.jgg.2026.03.011, PMID 41905586 |
| Family | 7 members: F0 grandparents, F1 parents, F2 proband (CN1) + sibling |
| Data | High-depth ONT + PacBio HiFi from blood; proband-specific T2T assembly |
| License | CC BY 4.0 (confirmed via Elsevier metadata), but full text unreachable: ScienceDirect 403 from every route; journal site hosts abstract only; Elsevier API returns metadata only |
| Accessions | NONE found in PubMed, Europe PMC, BIG Search NGDC endpoint, GSA search, GWH advanced search, CNSA, or NCBI |
| Verdict | UNRESOLVED and NOT counted. Even if opened, the assembly is proband-only (1 member), so this would count at best as a reads-only family. Suggested route: ask the corresponding authors (Kwok-Wing Tsui, CUHK; Jue Ruan, AGIS/CAAS) for the data accessions; requires Max's approval to send. |

### 4. PRJNA477862 (1000 Genomes harmonization) - DEAD END, SHORT-READ

- Verified via SRA runinfo: 24 runs, ALL Illumina HiSeq X Ten. 8 short-read trios from the 1000 Genomes / pipeline-harmonization dataset.
- Not long-read. Dead end for this census.

### 5. Quartet PGT reference materials (BMC Genomics 2026) - CONTROLLED DEAD END

| Field | Value |
|---|---|
| Paper | BMC Genomics 2026, DOI 10.1186/s12864-026-12556-7, PMC12990502 |
| Scale | 13 quartets |
| Platform | ONT PromethION |
| Access | **CONTROLLED** - GSA-Human HRA009786, DAC HDAC005180 (verified on the live GSA page) |
| Verdict | Dead end. |

### 6. Autism methylome quartets (Science Advances 2026) - APPLICATION-GATED DEAD END

| Field | Value |
|---|---|
| Paper | Science Advances 2026, DOI 10.1126/sciadv.aee4069, PMC13274601 |
| Scale | 31 ASD quartets (124 individuals), Chinese cohort |
| Platform | PacBio HiFi, phased methylomes |
| Access | **CONTROLLED** - OMIX004763, application-gated (their wording: "Academic researchers can apply for access") |
| Verdict | Dead end. |

### 7. Long-read autism, 63 families (Cell Genomics 2026) - CONTROLLED DEAD END

| Field | Value |
|---|---|
| Paper | Cell Genomics 2026, DOI 10.1016/j.xgen.2026.101186, PMC13174233 |
| Scale | 267 individuals / 63 families, REACH cohort |
| Platform | PacBio HiFi + ONT |
| Access | **CONTROLLED** - aligned BAMs/VCFs at NIMH Data Archive, DOI 10.15154/qpjh-dk51 |
| Verdict | Dead end. |

### 8. Paternal age effect (HGG Advances 2026) - DEAD END, SHORT-READ

- PMC12934291. Short-read Illumina only. Dead end.

### 9. Central Asian Genomic Diversity GVM000900 (medRxiv 2025) - RESOLVED DEAD END

| Field | Value |
|---|---|
| Paper | medRxiv 2025.08.26.25334450 |
| Scale | 166 individuals, BioProject PRJCA032194 |
| Access | **CONTROLLED** - via submitter email (Guanglinhescu@163.com); release date listed 2026-11-11; reads controlled |
| Family structure | Unrelated individuals, no family structure |
| Verdict | Resolves the census section 6 unknown -> dead end. |

### 10. CQ-chrY preprint (bioRxiv 2026) - ANNOUNCED, NOT DEPOSITED

| Field | Value |
|---|---|
| Paper | bioRxiv DOI 10.64898/2026.04.13.718326 |
| Content | Chinese Quartet FATHER's chrY T2T (CQ-chrY, 61.88 Mb, ONT + HiFi + Hi-C) |
| Verification | bioRxiv 429-blocked all session; Europe PMC has abstract only; no NCBI assembly record found; GitHub repo BoWangXJTU/T2T-CQ contains scripts only, no data files |
| Verdict | Announced, accession unverified. Keep as a T2T-CQ companion pending, NOT a new family. The father's chrY T2T would not by itself make the Quartet a long-read family, and its raw reads are controlled anyway. |

---

## MAJOR CORRECTION: T2T-CQ (F16) removed from the census

Wave-3 resolved the long-standing "parents' assemblies unverified" unknown, and the answer disqualifies the family:

1. **Paper methods (PMC13075991, Wang B et al. 2025 GPB, DOI 10.1093/gpbjnl/qzaf118):** "Parental datasets, consisting of Illumina PCR-free paired-end sequences, were obtained from LCL7 (father) and LCL8 (mother)." The long-read ONT ultralong + HiFi data in the T2T paper is the TWINS' data.
2. **GSA-Human live checks (2026-08-06):**
   - HRA010594 (T2T paper): 2 individuals only - LCL5, LCL6. 28 runs: ONT ultralong (PromethION) + Hi-C (MGISEQ-2000) for the twins. CONTROLLED.
   - HRA003188 (CQ v2.0-era): LCL5 only, 9 ONT PromethION WGS runs (2019).
   - HRA001859 (original Quartet multi-omics): all four members present, but 2,042 runs are all short-read platforms (WGBS, miRNA-Seq, RNA-Seq, etc.) - no WGS-strategy runs, no long reads.
3. **NCBI SRA:** LCL7/LCL8 searches return only false positives (e.g., a plant 16S metagenome study with an unrelated library named "LCL3_3"). No Chinese Quartet parent long-read WGS.
4. **Assembly interpretation:** CQ v2.0 and CQ v3.2 are BOTH the twins' diploid genome assemblies (two haplotypes), not parent assemblies. The open GWH accessions GWHFQEY00000000.1 (maternal haplotype) and GWHFQEX00000000.1 (paternal haplotype) are the twins' combined genome.

**Consequence:** the parents have no long-read WGS anywhere findable, so T2T-CQ is not a complete long-read family. It was counted as F16 (2 trios) in v01-v03; it is now removed.

**Counts after removal:** 33 - 1 = **32 families**; 36 - 2 = **34 trios**.

---

## Verdict and census impact

- Wave-3 found **zero new open-access complete long-read families**.
- One prior family (T2T-CQ, F16) was removed after direct repository verification, so the census DECREASED from 33/36 to 32/34.
- All other wave-3 leads are verified controlled (duoNovo/GREGoR, Quartet PGT, autism methylome, REACH 63-family autism), short-read only (PRJNA477862, paternal-age study), or unresolved-but-not-counted (Zhou 2026, CQ-chrY, Kramer/McCombie).
- New working method recorded for future waves: GSA-Human per-study AJAX endpoints (`/gsa-human/ajaxb/indinstudy`, `/runinstudy`) and the BIG Search API (`/search/api/specific?db=hra`) give exact sample lists and platforms, which is the only reliable way to distinguish family-wide long-read data from proband-only long reads.
