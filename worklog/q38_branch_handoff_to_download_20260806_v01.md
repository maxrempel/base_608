# Q38 branch handoff to the download session
Last edited: 2026-08-06 by Codex Q38 branch (open-access long-read family census).

This branch (thread "Q38 long-read families download open access", worktree
C:\base_608\worktrees\q38-longread-census, git branch codex/q38-longread-census)
saturates the open-access long-read FAMILY list via detached search agents.
The download session should proceed with the SATURATED census (32 unique open-access families, 35 trios) in OPEN_ACCESS_FAMILY_CENSUS_v01.md (committed on codex/q38-longread-census, also pushed to origin); the original verified 13 trios are in
C:\base_608\projects\1kgp_longread_trios\ (same content as
C:\claude_base\projects\1kgp_longread_trios\).

## Verified facts for the download session (2026-08-06)

1. CULTURE STATUS: all three open resources used EBV-transformed lymphoblastoid
   cell lines from Coriell. Vienna paper (PMC12350158) and HGSVC3 paper
   (PMC12350169, DOI 10.1038/s41586-025-09140-6) state this in Methods; LRSC
   paper (PMC11610458) uses Coriell NHGRI repository samples. There is NO
   non-cultured complete family in the current open set. Non-cultured family
   genomes live in controlled-access sets (MSSNG blood-derived, EGA DAC, GA4K),
   tracked in CONTROLLED_ACCESS_CANDIDATES_v01_tomemex.md.

2. ASSEMBLY-ONLY SCOPE (Max instruction 2026-08-06): download de novo
   assemblies first, not reads.
   - HGSVC3: Verkko assemblies ENA PRJEB76276 (use v2 accessions;
     GCA_964198545 v1 for HG00512 is corrupt per manifest), optional hifiasm
     PRJEB83624. Accessions table cached: C:\base_608\_tmp\q38\hgsvc3_accessions.tsv
   - LRSC (S3 1000g-ont): assemblies exist for all 12 samples under
     PROCESSED_DATA/ASSEMBLIES/NAPU_PIPELINE_FASTAS/<ID>/ (hapdup_dual_1/2 +
     hapdup_phased_1/2 fasta); FLYE and R10_HIFIASM subdirs cover subsets.
     Vienna (1KG_ONT_VIENNA) has NO de novo assemblies (only hg38/t2t CRAM +
     GAF + variant releases) - Vienna families get assemblies only if reads are
     later assembled locally.
   - Total assembly-only payload estimate: tens of GB (FASTA), far smaller than
     the full read set; fits Green24 comfortably.

3. This branch will deliver OPEN_ACCESS_FAMILY_CENSUS_v01.md with any
   additional open-access families found; merge via codex/q38-longread-census.

## Census v01 results (appended 2026-08-06)

OPEN_ACCESS_FAMILY_CENSUS_v01.md is committed (25d1a71) and pushed on
codex/q38-longread-census. Headline: 32 unique open-access complete families,
35 complete trios. The 13 manifest trios stand; additions:

4. PLATINUM PEDIGREE / CEPH 1463 (Porubsky et al. 2025 Nature,
   DOI 10.1038/s41586-025-08922-2): VERIFIED OPEN (earlier agent rejection was
   wrong). 23 of 28 members open with reads + near-T2T assemblies + truthsets:
   AWS s3://platinum-pedigree-data/ (assemblies/, data/, variants/,
   truthset_v1.1+v1.2) and ENA PRJEB86317. dbGaP phs003793.v1.p1 holds only 5
   non-consented members (NA12883, NA12884, NA12887, 200103, 200105).
   Adds 15 new family units (17 trios; PP01/PP02 overlap Vienna trios F08/F09).
   HiFi/Illumina/Element from BLOOD; UL-ONT/Strand-seq from LCL. Best
   non-cultured representation available in open access. Index repo:
   github.com/Platinum-Pedigree-Consortium/Platinum-Pedigree-Datasets.

5. GIAB Ashkenazi trio HG002/HG003/HG004 (HG002 T2T v2.7 assembly; HG003/004
   reads only) and GIAB Chinese trio HG005/HG006/HG007 (reads only). Open FTP:
   .../giab/data/AshkenazimTrio/ and .../ChineseTrio/ ; s3://giab. Verified the
   GIAB Chinese trio is PGP material, NOT HGSVC3's HG00512/513/514 (no double
   count).

6. T2T-CQ Chinese Quartet (Wang 2025 GPB, DOI 10.1093/gpbjnl/qzaf118):
   father + mother + MZ twin sons; T2T diploid assemblies for all 4 at NGDC GWH
   (maternal GWHFQEY00000000.1, paternal GWHFQEX00000000.1; twins pending);
   reads GSA-Human HRA010594 (access mechanics pending Agent D).

7. PAN027 / WashU pedigree (Cechova 2025 preprint
   DOI 10.64898/2025.12.14.693655; Dong 2026 companion): grandmother HG06803
   (PAN010) + grandfather HG06804 (PAN011) + daughter HG06807 (PAN027) +
   granddaughter HG06808 (PAN028). Complete trio = HG06803/HG06804/HG06807.
   T2T assemblies all 4 at public.gi.ucsc.edu/~mcechova/pedigree/assemblies/
   (use v1.3.1); reads SRA SRP320775; HiFi from blood. HG06807 also NCBI
   GCA_046332035.2 + GCA_046332005.3.

8. Download priority for assembly-first scope: (1) T2T-CQ + PAN027 + Platinum
   Pedigree + HGSVC3 (Tier 1 T2T-class), (2) LRSC assemblies, (3) HG002 T2T,
   (4) Vienna/GIAB-Chinese reads only if later needed. Estimated 250-350 GB for
   all assemblies. Agent D saturation sweep may add more families (v02).

## FINAL STATUS (appended 2026-08-06, commit 3f44e1b pushed)

Census is SATURATED: OPEN_ACCESS_FAMILY_CENSUS_v02.md on branch
codex/q38-longread-census. 32 unique open-access families, 35 trios. Agent D
confirmed no further open families (Korea KOREF_S1 parents short-read only;
Japan/India/Middle East/Africa/Latin America nothing; HPRC2 unrelated
individuals; Noyes 2026 Eichler families controlled via SFARI/NDA).

Download branch corrections for v02:
- T2T-CQ: twins are DAUGHTERS (LCL5/LCL6), parents LCL7/LCL8; the T2T assembly
  is the twins' combined diploid genome (GWHFQEY00000000.1 mat,
  GWHFQEX00000000.1 pat, open at GWH); raw reads GSA-Human HRA010594 are
  CONTROLLED (DAC) - assemblies-only scope unaffected. Parents' v2.0 assemblies:
  verify accessions at chinese-quartet.org/GWH before attempting.
- Platinum Pedigree: download via AWS CLI no-sign-request (s3
  ls --no-sign-request s3://platinum-pedigree-data/assemblies/) or HTTPS;
  23 member folders; use v-latest near-T2T assemblies; G4 members included.
- PAN027: use v1.3.1 FASTAs from public.gi.ucsc.edu/~mcechova/pedigree/assemblies/.
- Updated assembly payload estimate 250-350 GB; fits Green24 planning.

---

## WAVE-2 DELTA (appended 2026-08-06, census v03, commit c21421c on codex/q38-longread-census)

Max ordered a second online saturation wave with detached agents (qwen3.7-plus:
E literature ~700 papers, F repository metadata mining ENA/NCBI/SRA, G regional
SE/Central Asia + Middle East + Africa + Oceania + Latin America). Result:
33 unique open families now (was 32), 36 trios.

NEW OPEN FAMILY for the download queue (F33, assembly-first Tier 1):
- Arab Pangenome Reference trio: APR-F (father), APR-M (mother), APR-S (son).
  Nassir et al. 2025 Nat Commun, PMID 40707445, PMC12290100. Healthy trio,
  all data from peripheral blood (first fully non-cultured open family).
- Reads: SRA PRJNA1108179 (ENA-verified per-member PacBio pbAPR-* and ONT
  APR-* runs; Hi-C per paper).
- Assemblies: haplotype-phased, N50 ~124 Mb, all 3 members. GenBank BioProjects
  PRJNA1151091-PRJNA1151118 + PRJNA1152014-PRJNA1152091 (106 haplotype projects
  for 53 samples; e.g. GCA_050491585.1 = apr052.2 v1, biosample tissue=Blood).
  Direct FASTA portal: https://www.mbru.ac.ae/the-arab-pangenome-reference/
- Download note: assembly projects are named aprNNN.haplotype; map APR-F/M/S
  via Supplementary Table 1 before pulling (only the trio is needed, not the
  50 unrelated panel members).

## WAVE-3 DELTA (appended 2026-08-06, census v04, branch codex/q38-longread-census)

Wave-3 (direct verification by the DeepSeek takeover session, no subagents)
re-verified every open lead and found ZERO new open families. It also made one
correction, so the download queue changes:

1. CENSUS NOW 32 FAMILIES / 34 TRIOS (was 33/36 in v03). T2T-CQ (F16) is
   REMOVED: the parents (LCL7/LCL8) have short-read Illumina only. Verified in
   the GPB paper methods (PMC13075991: "Parental datasets, consisting of
   Illumina PCR-free paired-end sequences, were obtained from LCL7 (father) and
   LCL8 (mother)") and in live GSA-Human records: HRA010594 = LCL5+LCL6 only
   (ONT ultralong + Hi-C, controlled); HRA003188 = LCL5 only (ONT WGS);
   HRA001859 = all four members but all short-read multi-omics; NCBI SRA has no
   parent long reads. CQ v2.0 and CQ v3.2 are BOTH the twins' combined diploid
   genome (GWHFQEY00000000.1 mat / GWHFQEX00000000.1 pat, open at GWH) - there
   are no parent assemblies. DO NOT download T2T-CQ as a family; the twins-only
   T2T diploid remains open at GWH if the reference genome itself is wanted.

2. No new families join the download queue. Verified controlled near-misses
   (for the record, not downloadable): duoNovo/GREGoR AJHG 2026 (38 trios + 2
   quads, dbGaP phs003047); Quartet PGT BMC Genomics 2026 (13 quartets, ONT,
   GSA-Human HRA009786, DAC HDAC005180); autism methylome Sci Adv 2026 (31
   quartets, HiFi, OMIX004763 application-gated); REACH autism Cell Genomics
   2026 (63 families, HiFi+ONT, NIMH Data Archive DOI 10.15154/qpjh-dk51);
   Central Asian GVM000900 medRxiv 2025 (166 unrelated individuals, controlled,
   release 2026-11-11). Short-read-only dead ends: PRJNA477862 (8 trios, all
   Illumina HiSeq X Ten), paternal-age HGG Advances 2026.

3. CQ-chrY preprint (bioRxiv 10.64898/2026.04.13.718326) announces the Chinese
   Quartet father's chrY T2T (61.88 Mb, ONT + HiFi + Hi-C) but no public
   deposit was found; even if it appears, the Quartet stays excluded as a
   family (parents short-read only, twins' reads controlled). Assembly-only
   scope is unaffected.

4. Downloads are untouched and remain the other branch's duty. Updated
   assembly-first priority unchanged: PAN027, Platinum Pedigree, HGSVC3,
   LRSC, HG002 T2T, Vienna/GIAB-Chinese reads if later needed, plus F33 APR.
   Estimated payload remains roughly 250-350 GB.

Platinum Pedigree refinement: G1-G3 members have Verkko near-T2T assemblies;
G4 members (200081-200087, 200101-200106) have hifiasm diploid assemblies only
(verified in the S3 assemblies/ tree).

NOT added (wave-2 dead ends, full evidence in census v03 section 7):
- Tibetan pangenome 35 trios: real and large but CONTROLLED (GSA-Human DAC,
  KIZ CAS; correct BioProject PRJCA043737). Best candidate if Max ever does
  a controlled-access application.
- Asian Pan-Genome 160 trios: controlled (GSA-Human HGV000009, agent-reported).
- Emirati T2T pangenome: controlled (EGA EGAS50000001232).
- Korean Pangenome Project (Jang 2025 medRxiv): 40 individuals / 33 clinical
  families = proband-centric, not complete trios; claimed accession
  PRJNA1122054 does not exist in NCBI.
- 22q11.2 NA10382 trio: Coriell cell lines public, but no public reads or
  assemblies (SRA + ENA empty); only 22q11.2-region FASTAs on Zenodo.
- Zhou H 2026 three-generation Chinese family: UNRESOLVED, not counted
  (bot-blocked CC-BY full text, no OA copy anywhere, no deposit found;
  assembly is proband-only anyway). If Max wants it, ask corresponding
  authors Kwok-Wing Tsui (CUHK) / Jue Ruan (AGIS); needs his approval.
- Ghorbani 2025 (6 Middle Eastern trios, dbGaP phs003917), Down syndrome
  families (dbGaP phs003761, chr21 only), IRUD Japanese trios, MENA SV
  study, VN1K, cancer pedigrees (no deposit found).

Census file: projects/1kgp_longread_trios/OPEN_ACCESS_FAMILY_CENSUS_v03.md.
Wave-2 agent reports in projects/1kgp_longread_trios/agent_reports/
(agentE/F/G *_wave2.md). Payload estimate unchanged (250-350 GB); the APR
trio adds roughly 5-10 GB of assemblies.
