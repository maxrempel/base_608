---
name: Controlled-access long-read family census v01
description: Formal census of complete human families with long-read WGS that sit behind approval gates (controlled access), as a complement to the open census (OPEN_ACCESS_FAMILY_CENSUS_v04). Every entry records family scale, platform, repository accession, gate type, our application status, and how the study was found. Built from Q38 census waves 1-3 verification plus the FAMDAC v01 research pass.
type: project
last_edited: 2026-08-06 by Codex (Q38 census wave-3 takeover session, DeepSeek)
status: v01, first formalized version. Cross-references FAMDAC_registry_v01_tomemex.md (application state) and CONTROLLED_ACCESS_CANDIDATES_v01_tomemex.md (ranked strategy). No application state changed in this session.
---

# CONTROLLED-ACCESS LONG-READ FAMILY CENSUS v01

## TLDR

"Controlled access" is the standard term for studies that require approval:
the metadata (title, sample list, platform) is public, but the reads or
alignments are released only after an application approved by a data access
committee (DAC). This database is the census of such studies that contain
COMPLETE families (father + mother + child, or larger) with long-read whole
genomes. As of 2026-08-06 it holds 15 verified or near-verified controlled
long-read complete-family studies, plus 3 reported-but-unverified and several
excluded categories. The largest complete-trio sets: Asian Pan-Genome 160
trios (accession unverified), ToMMo 111 trios (struck from our plan by Max),
REACH autism 63 families, SSC/Noyes 42 families, duoNovo 38 trios + 2 quads,
Tibetan 35 trios. Our application state for each study is tracked in
FAMDAC_registry_v01_tomemex.md; nothing new was filed by this session.

## 1. What this database is

- It is the mirror image of OPEN_ACCESS_FAMILY_CENSUS_v04.md (32 open
  families / 34 trios): same subject, but the data requires an application.
- The counting unit is the STUDY, because approval is granted per study (per
  dbGaP dataset, EGA dataset, GSA-Human study, or portal collection), not per
  family. Each entry also carries the number of complete families/trios it
  holds where known.
- "How found" is a required field on every entry so the closed-access census
  session can reproduce or extend the search without re-reading this session.
- Application mechanics (entities, eRA accounts, held approvals, blockers such
  as the missing IRB) live in `C:\XG1\famdac\FAMDAC_registry_v01_tomemex.md`.
  This census records WHICH studies exist; FAMDAC records what we have done
  about them.

## 2. Registry of controlled long-read complete-family studies

### Verified or near-verified (waves 1-3, live checks or full text)

**duoNovo / GREGoR Pediatrics Mendelian Genomics (AJHG 2026)**
- Scale: 38 complete trios + 2 quads (122 individuals). Platform: PacBio Revio
  HiFi. Repository: dbGaP phs003047, hosted on AnVIL.
- Gate: dbGaP data-access request with institutional sign-off.
- Ours: FAMDAC top target; draft DAR written, NOT submitted.
- How found: wave-3 Europe PMC full text (PMC12987547) plus the official
  GREGoR page; counts and accession read from paper and registry.

**Noyes 2026 Nature Communications (Eichler lab, SSC autism)**
- Scale: 42 families (31 quads + 11 trios, 157 individuals). Platform: HiFi
  primary. Repository: SFARI Base SFARI_DS0000104 + NIMH Data Archive
  Collection 3780.
- Gate: SFARI Researcher Distribution Agreement + NDA account.
- Ours: DRRF registered in SFARI Base, status UNCONFIRMED (FAMDAC section 4).
- How found: wave-2/3 full-text verification (cached noyes_fulltext.xml).
  Resolves the v01 question "does SFARI redistribute long-read BAMs": yes.

**REACH autism long-read cohort (Cell Genomics 2026)**
- Scale: 63 families / 267 individuals. Platform: PacBio HiFi + ONT.
  Repository: NIMH Data Archive, DOI 10.15154/qpjh-dk51.
- Gate: NDA.
- Ours: none.
- How found: wave-3 Europe PMC full text (PMC13174233). Resolves the v01
  unknown "dbGaP accession for the 2026 Cell Genomics autism paper": it is not
  dbGaP; it is the NIMH Data Archive.

**Autism methylome quartets (Science Advances 2026)**
- Scale: 31 ASD quartets (124 individuals), Chinese cohort. Platform: PacBio
  HiFi, phased methylomes. Repository: CNCB OMIX004763.
- Gate: application to OMIX; their wording: "academic researchers can apply for
  access".
- Ours: none.
- How found: wave-3 full text (PMC13274601) + OMIX record.

**Quartet PGT reference materials (BMC Genomics 2026)**
- Scale: 13 quartets. Platform: ONT PromethION. Repository: GSA-Human
  HRA009786, DAC HDAC005180.
- Gate: GSA-Human controlled mode (free account + DAC approval).
- Ours: none.
- How found: wave-3 full text (PMC12990502) + live GSA page check.

**Tibetan near-complete pangenome (bioRxiv 2025)**
- Scale: 35 trios / 105 individuals, 70 near-complete phased assemblies.
  Platform: HiFi + ultralong ONT + short reads, all from blood. Repository:
  BioProject PRJCA043737 across GSA-Human/GWH/GVM, controlled via KIZ-CAS DAC.
- Gate: GSA-Human DAC. Largest controlled family resource found.
- Ours: none.
- How found: wave-2 agent G regional sweep + live BioProject and portal
  checks; the session corrected a wrong accession from the agent report.

**Ghorbani et al. 2025 Nature Genetics**
- Scale: 6 Middle Eastern family trios (Sudan, Jordan, Syria, Qatar,
  Afghanistan). Platform: PacBio HiFi about 38x. Repository: dbGaP
  phs003917.v1.p1.
- Gate: dbGaP.
- Ours: none.
- How found: wave-2 agent E + PMC12081309 full text.

**Ivashchenko 2026**
- Scale: 10 PacBio trios. Repository: EGA EGAS00001008250.
- Gate: EGA DAC.
- Ours: none.
- How found: wave-1/2 repository mining.

**KCNC2 autism family**
- Scale: 5 members (father, mother, 3 children). Platform: PacBio HiFi.
  Repository: dbGaP phs002698.
- Gate: dbGaP.
- Ours: none.
- How found: wave-2 agent F, verified via SRA runinfo.

**EGA intellectual-disability trios**
- Scale: 6 complete trios + 1 singleton proband (19 samples, 1.53 TB).
  Platform: PacBio Sequel II HiFi 30x, whole blood. Repository:
  EGAD00001009109 / study EGAS00001006479 / DAC EGAC00001002803.
- Gate: EGA DAC; policy restricts to "research institutions for academic
  purposes".
- Ours: accounts exist, NO request filed (FAMDAC).
- How found: v01 research pass + FAMDAC deep verification (Kucuk et al.,
  Genome Medicine 2023, PMC10169305, and the same-lab cohort papers).

**ToMMo / Tohoku Medical Megabank**
- Scale: 111 complete trios. Platform: ONT PromethION. Repository: direct
  email request (jmorp@omics.megabank.tohoku.ac.jp).
- Gate: human application process, about 2-week turnaround.
- Ours: STRUCK from the plan by Max ("Japan never gives away the data"); kept
  for the record only.
- How found: v01 research pass.

**GA4K / Genomic Answers for Kids (Children's Mercy Kansas City)**
- Scale: roughly 2,000 long-read genomes; complete-trio count UNVERIFIED (v01
  reported 75 HiFi trios). Platform: PacBio HiFi. Repository: dbGaP
  phs002206 on AnVIL. Consent code DS-PEDD-IRB (IRB approval required).
- Gate: dbGaP DAR + IRB.
- Ours: blocked on IRB (FAMDAC); nothing filed.
- How found: v01 research pass + FAMDAC verification.

**IRUD Japanese trios (Journal of Human Genetics 2026)**
- Scale: 12 clinical trios. Platform: long-read WGS. Repository: none found,
  no PMC; likely controlled.
- Gate: likely hospital/institutional DAC.
- Ours: none.
- How found: wave-2 agent E literature sweep.

**Negi 2025**
- Scale: 41 families. Repository: likely dbGaP (unconfirmed).
- Ours: none.
- How found: wave-2 agent E.

**Werren 2026**
- Scale: 20 clinical families. Repository: likely controlled (unconfirmed).
- Ours: none.
- How found: wave-2 agent E.

### Reported but NOT fully verified

**Asian Pan-Genome (Wu et al. 2026 bioRxiv)** - 160 trios, GSA-Human
HGV000009, controlled. Accession as reported by wave-2 agent G; not yet
independently re-verified.

**Emirati T2T pangenome** - EGA EGAS50000001232, controlled; reported trio
count inconsistent across sources.

**MSSNG (Autism Speaks / DNAstack)** - CONFLICTING RECORDS. The standard
release is verified short-read only (Illumina CRAM + VCF, 9,621 samples;
FAMDAC section 5C). The v01 candidates doc reports about 63 complete
long-read trios (243 individuals; 158 HiFi, 109 ONT). Treat the long-read arm
as UNVERIFIED until a portal or paper confirms it; do not count it in the
long-read census yet.

### Excluded (not complete long-read families)

- **Down syndrome families (AJHG 2026)**: dbGaP phs003761.v1.p1, chr21
  centromeres only, not whole genome.
- **Central Asian Genomic Diversity (medRxiv 2025)**: 166 individuals,
  unrelated; GVM000900 / PRJCA032194, controlled via submitter email, release
  2026-11-11.
- **T2T-CQ Chinese Quartet raw reads**: GSA-Human HRA010594/HRA003188, twins
  only; parents short-read Illumina only (wave-3 verified). Removed from the
  open census v04 for the same reason.
- **UDN**: dbGaP phs001232, 68 ONT individuals, mostly duos, not trios.
- **Genomics England ONT pilot**: 315 participants, analysis only inside their
  firewall, no download at all.
- **All of Us**: long-read participants but population-recruited, not family.
- **Short-read applications already held (FAMDAC)**: dbGaP ASC phs000298,
  ADHD phs003647, CHOP phs000199, PCGC phs001194 (about 1,800 trios). All
  short-read; out of this census's scope.

## 3. Counts (2026-08-06)

| Bucket | Count | Notes |
|---|---|---|
| Verified/near-verified controlled long-read complete-family studies | 15 | duoNovo, SSC/Noyes, REACH, autism methylome, Quartet PGT, Tibetan, Ghorbani, Ivashchenko, KCNC2, EGA ID, ToMMo, GA4K, IRUD, Negi, Werren |
| Reported, not fully verified | 3 | Asian Pan-Genome, Emirati T2T, MSSNG long-read arm |
| Excluded (not complete long-read families) | 7 | Down syndrome, Central Asian, T2T-CQ, UDN, GEL, All of Us, short-read held applications |
| Largest verified complete-trio sets | REACH 63 families; SSC 42; duoNovo 38 trios + 2 quads; Tibetan 35; autism methylome 31 quartets | ToMMo 111 and Asian Pan-Genome 160 larger but struck/unverified |

## 4. Gate types (what approval actually means)

- **dbGaP (NIH)**: data-access request (DAR) via eRA Commons; requires an
  institutional Signing Official and a PI account; some consent codes add an
  IRB requirement (e.g. GA4K DS-PEDD-IRB).
- **EGA (EBI)**: dataset-level DAC decides case by case; policy text may
  restrict applicants (e.g. "research institutions for academic purposes").
- **GSA-Human (NGDC/CNCB, China)**: controlled mode with DAC approval.
- **NIMH Data Archive (NDA)**: account plus study-specific access request.
- **SFARI Base**: Researcher Distribution Agreement signed with a Signing
  Official.
- **OMIX (CNCB)**: application through the portal, academic applicants.
- **Submitter email**: some Chinese projects are gated by emailing the submitter
  (e.g. Central Asian GVM000900).
- **Firewall-only**: Genomics England; no download exists.

## 5. Application status (cross-reference)

Nothing was filed or changed by this session. Live application state is in
`C:\XG1\famdac\FAMDAC_registry_v01_tomemex.md`: dbGaP project 42416 ACTIVE
(GRU only), project 42326 pending, EGA accounts exist with no request, GA4K
blocked on IRB, SFARI Base unconfirmed, MSSNG draft dated 2026-08-01.

## 6. How to keep this census alive

1. Update this file in the same task whenever a study's access state changes
   (approval granted, data released, accession found, study retracted).
2. Every new entry MUST carry a "How found" comment naming the search route
   and the verifying source (full-text PMC ID, live repository check, agent
   report).
3. Bump the version (v01 to v02) on material updates; keep prior versions
   alongside.
4. Search recipes that worked: Europe PMC fullTextXML for PMC papers; ENA
   portal API study-title sweeps; NCBI SRA runinfo via efetch for platform
   verification; GSA-Human AJAX endpoints (`/gsa-human/ajaxb/indinstudy` and
   `/runinstudy`) for per-study sample and platform lists; NGDC BIG Search API
   (`/search/api/specific?db=hra`); live GVM pages for Chinese deposits;
   dbGaP/EGA/NDA/OMIX/SFARI search pages for gate and consent codes.

## 7. Sources

- Q38 census waves 1-3 agent reports and OPEN_ACCESS_FAMILY_CENSUS_v04.md
  (this project folder).
- `C:\XG1\famdac\FAMDAC_registry_v01_tomemex.md` (application state).
- `CONTROLLED_ACCESS_CANDIDATES_v01_tomemex.md` (ranked application strategy).
- Full-text caches for wave-3 verifications under `C:\base_608\_tmp\q38\wave3\`.
