# Long-read family trios behind approval gates - candidate list v01

Date: 2026-08-05 (v01, Claude Opus 5); extended 2026-08-06 by the Q38 census
wave-3 session (DeepSeek Codex). Status: RESEARCH, no applications filed.
Companion to FAMILY_MANIFEST_v01.md (open trios) and
OPEN_ACCESS_FAMILY_CENSUS_v04.md (open families). The v01 application strategy
is preserved below; the new registry section adds every controlled-access
family study verified in census waves 1-3, each with a comment on how it was
found.

Terminology: "controlled access" is the standard name for studies that require
approval. The metadata (study title, sample list, platform) is public, but the
reads or alignments are released only after an application approved by a data
access committee (DAC), abbreviated DAC. The European Genome-phenome Archive
(EGA) also calls this "registered access". Open access, by contrast, means
anyone can download without any application.

## Question asked

Max: we have the open long-read trios; which CONTROLLED-ACCESS trio collections are
worth applying to, and which are easiest to get approved? Autism preferred, any
family data acceptable.

## Headline answer

Open data worldwide gives about 5 complete long-read trios (GIAB 2, HGSVC 3).
Our existing manifest of 13 counts medium-coverage ONT trios as well. Everything
larger is gated, and every gate is institutional: the legal counterparty is an
INSTITUTION, not a person. So the real question is not "which dataset" but
"which entity signs for us".

## Verified registry of controlled-access long-read family studies (waves 1-3, updated 2026-08-06)

External registries to search when looking for such studies: dbGaP (NIH),
EGA (EBI), GSA-Human (NGDC/CNCB, China), NIMH Data Archive, SFARI Base,
AnVIL, CNCB OMIX, and JGA (Japan). No single cross-database registry exists;
each repository is its own searchable registry, and this document is the
consolidated family-focused list. Every entry below carries a "How found"
comment so the closed-access census session can reproduce the search.

### Verified with live checks or full text (waves 2-3)

**duoNovo / GREGoR Pediatrics Mendelian Genomics (AJHG 2026)** - 38 complete
trios + 2 quads (122 individuals), PacBio Revio HiFi. dbGaP phs003047, hosted
on AnVIL. Gate: dbGaP data-access request + institutional sign-off.
How found: wave-3 Europe PMC full text (PMC12987547) plus the official GREGoR
page; counts and accession read from the paper and registry.

**Noyes 2026 Nature Communications (Eichler lab, SSC autism families)** - 42
families (31 quads + 11 trios, 157 individuals), HiFi primary. SFARI Base
SFARI_DS0000104 + NIMH Data Archive Collection 3780. Gate: SFARI Researcher
Distribution Agreement + NDA. How found: wave-2/3 full-text verification
(cached noyes_fulltext.xml). Resolves the v01 unknown "does SFARI redistribute
long-read BAMs": yes.

**REACH autism long-read cohort (Cell Genomics 2026)** - 63 families / 267
individuals, PacBio HiFi + ONT. NIMH Data Archive, DOI 10.15154/qpjh-dk51.
Gate: NDA. How found: wave-3 Europe PMC full text (PMC13174233). Resolves the
v01 unknown "dbGaP accession for the 2026 Cell Genomics autism paper": it is
not dbGaP; it is the NIMH Data Archive.

**Autism methylome quartets (Science Advances 2026)** - 31 ASD quartets (124
individuals), PacBio HiFi, phased methylomes, Chinese cohort. CNCB OMIX004763.
Gate: application to OMIX, wording "academic researchers can apply for access".
How found: wave-3 full text (PMC13274601) + OMIX record.

**Quartet PGT reference materials (BMC Genomics 2026)** - 13 quartets, ONT
PromethION. GSA-Human HRA009786, DAC HDAC005180. Gate: GSA-Human controlled
mode. How found: wave-3 full text (PMC12990502) + live GSA page check.

**Tibetan near-complete pangenome (bioRxiv 2025)** - 35 trios / 105
individuals, 70 near-complete phased assemblies, HiFi + UL-ONT + short reads
from blood. BioProject PRJCA043737 across GSA-Human/GWH/GVM, controlled via
KIZ-CAS DAC. Largest controlled family resource found. How found: wave-2 agent
G regional sweep + live BioProject and portal checks; the wave-2 session
corrected a wrong accession in the agent report.

**Asian Pan-Genome (Wu et al. 2026 bioRxiv)** - 160 trios. GSA-Human
HGV000009, controlled. How found: wave-2 agent G; accession as reported by the
agent, not yet independently re-verified.

**Emirati T2T pangenome** - EGA EGAS50000001232, controlled; reported trio
count is inconsistent across sources, unverified. How found: wave-2 agent G.

**Ghorbani et al. 2025 Nature Genetics** - 6 Middle Eastern family trios
(Sudan, Jordan, Syria, Qatar, Afghanistan), PacBio HiFi about 38x. dbGaP
phs003917.v1.p1. How found: wave-2 agent E + PMC12081309 full text.

**Ivashchenko 2026** - 10 PacBio trios. EGA EGAS00001008250. How found:
wave-1/2 repository mining.

**Down syndrome families (AJHG 2026)** - 8 families, chr21 centromeres only.
dbGaP phs003761.v1.p1. How found: wave-2 agent E + PMC13288774.

**IRUD Japanese trios (Journal of Human Genetics 2026)** - 12 clinical trios.
No PMC; likely controlled. How found: wave-2 agent E literature sweep.

**KCNC2 autism family** - 5 members (father, mother, 3 children), PacBio HiFi.
dbGaP phs002698. How found: wave-2 agent F, verified via SRA runinfo.

**Negi 2025** - 41 families, likely dbGaP. How found: wave-2 agent E.

**Werren 2026** - 20 clinical families. How found: wave-2 agent E.

**Central Asian Genomic Diversity (medRxiv 2025)** - 166 individuals, but
unrelated, no family structure. GVM000900 / BioProject PRJCA032194. Gate:
controlled via submitter email (Guanglinhescu@163.com), release date
2026-11-11. How found: wave-3 live GVM page check; resolves the census section
6 unknown.

**T2T-CQ Chinese Quartet raw reads** - twins only: ONT ultralong + Hi-C in
GSA-Human HRA010594, LCL5 ONT WGS in HRA003188. Parents (LCL7/LCL8) have
short-read Illumina only. Gate: GSA-Human DAC. How found: wave-3 live
GSA-Human AJAX checks (per-study sample and platform lists). This family is
removed from the open census (v04) because it is not complete on long reads.

### Recorded in the v01 research pass (Claude, 2026-08-05)

**MSSNG (Autism Speaks / DNAstack)** - about 63 complete long-read trios (243
individuals; 158 HiFi, 109 ONT). Cloud-only portal, Database Access Agreement
signed by researcher AND institution, DACO review. Best autism match. How
found: v01 research pass, counts from the MSSNG portal.

**GA4K - Genomic Answers for Kids (Children's Mercy Kansas City)** - 75 PacBio
HiFi parent-offspring trios. dbGaP phs002206 on AnVIL. Needs eRA Commons,
Signing Official, institutional certification. How found: v01 research pass.

**GREGoR consortium (NHGRI rare disease)** - dbGaP phs003047. 4,366 families,
59% trio-or-larger; the verified long-read subset is the duoNovo 38 trios + 2
quads (wave-3). How found: v01 research pass + wave-3 duoNovo verification.

**EGA intellectual-disability trios** - EGAD00001009109 / study
EGAS00001006479 / DAC EGAC00001002803. 6 complete trios + 1 proband, 30x HiFi,
about 1.5 TB. Named DAC, case-by-case, restricted to research institutions.
How found: v01 research pass.

**UDN - dbGaP phs001232** - 68 ONT individuals, mostly duos, not trio-rich.
How found: v01 research pass.

**Genomics England ONT rare-disease pilot** - 315 participants, analysis only
inside their firewall, GeCIP membership required; no download. How found: v01
research pass.

**ToMMo / Tohoku Medical Megabank** - 111 complete trios, ONT PromethION, the
largest complete long-read trio set found. Direct email request
(jmorp@omics.megabank.tohoku.ac.jp). STRUCK from the plan by Max ("Japan never
gives away the data"), kept only for the record. How found: v01 research pass.

**All of Us** - long-read participants but population-recruited, not family;
trios unlikely; institutional DURA required. How found: v01 research pass.

### General category

Clinical rare-disease trio long-read studies, as a class, are almost always
controlled (dbGaP, EGA, GSA-Human, or hospital DAC). Any newly published
clinical trio paper should be assumed controlled until its data-availability
statement is read.

### v01 unknowns now resolved

- SFARI Base long-read BAM redistribution: VERIFIED yes (Noyes 2026,
  SFARI_DS0000104 + NDA Collection 3780).
- Cell Genomics 2026 autism paper accession: NIMH Data Archive DOI
  10.15154/qpjh-dk51 (not dbGaP).
- GREGoR long-read complete-trio count: duoNovo = 38 trios + 2 quads (122
  individuals, Revio HiFi).
- HPRC Release 2 parent long reads: still none (HPRC2 is unrelated individuals;
  HPRC design keeps parents short-read only).

## Ranked candidates - easiest approval first

1. ToMMo / Tohoku Medical Megabank three-generation cohort (Japan)
   111 complete trios, ONT PromethION R9.4.1, ~22x, N50 25.8 kb. Largest complete
   long-read trio set found anywhere. Access = direct email request to a named
   group (jmorp@omics.megabank.tohoku.ac.jp), ~2 week turnaround, after our own
   ethics approval. Human process, not a portal. BEST VALUE PER UNIT OF EFFORT.

2. EGA - PacBio HiFi intellectual-disability trios
   EGAD00001009109 / study EGAS00001006479 / DAC EGAC00001002803.
   6 complete trios + 1 proband, 30x HiFi, ~1.5 TB. Small named DAC, decides
   case by case. Wording restricts to "research institutions for academic
   purposes". Fast and human compared with dbGaP. Nearest thing to autism-adjacent
   (neurodevelopmental) with a tractable gate.

3. MSSNG (Autism Speaks / DNAstack) - the best AUTISM match
   ~63 complete long-read trios (243 individuals; 158 HiFi, 109 ONT).
   Cloud-only portal, Database Access Agreement signed by researcher AND
   affiliated institution, DACO review. Free portal, we pay cloud compute.

4. GA4K - Genomic Answers for Kids, Children's Mercy Kansas City
   75 PacBio HiFi parent-offspring trios, pediatric rare disease.
   dbGaP phs002206, hosted on AnVIL. Needs eRA Commons + Signing Official +
   Institutional Certification.

5. GREGoR consortium (NHGRI rare disease)
   dbGaP phs003047. 4,366 families, 59% trio-or-larger; long-read subset size
   UNVERIFIED. Same dbGaP gate.

6. SFARI Base (SSC / SPARK) - autism
   Published SSC long-read work exists: 42 families, 157 individuals (31 quads,
   11 trios), HiFi primary. Whether SFARI Base actually redistributes those long-read
   BAMs is UNVERIFIED - the preprint has no data-availability statement.
   Requires SFARI Researcher Distribution Agreement with a named Signing Official.

7. UDN - dbGaP phs001232. 68 ONT individuals, only 11 unaffected relatives.
   Duos, not trio-rich. Low value.

8. Genomics England ONT rare-disease pilot - 315 participants, analysis only inside
   their UK firewall, GeCIP membership required. Hardest; no download. Skip.

9. All of Us - 2,700+ long-read participants but population, not family-recruited.
   Trios unlikely. Institutional DURA required. Skip for family work.

10. dbGaP autism studies (ASC phs000298, AGP phs000267) - short-read only. No.

## The single blocker, stated plainly

dbGaP is the strictest: it wants an eRA Commons account, a Signing Official at an
NIH-recognised institution, AND a PI at professor / senior-scientist rank.
SFARI, MSSNG, All of Us and Genomics England all make the institution the legal
party. So candidates 3-6 are unreachable as a private individual.

Two routes exist:
 - Sign as a legal research entity of our own. TRANSPOSON is already registered
   in SAM.gov; a research entity with a genuine research purpose can act as the
   institution and supply its own Signing Official. This is how independent labs
   get dbGaP and SFARI access. NOT verified against a published policy page -
   treat as plausible, not certain.
 - Add ourselves as an approved user under an affiliated PI who submits the DAR.

Candidates 1 and 2 (ToMMo, EGA) are the ones where a small serious entity plus a
clear scientific rationale has the best chance without a university behind it.

## Suggested order of attack

REVISED 2026-08-05 after Max: "Japan never gives away the data." ToMMo is struck
from the plan despite its 111 trios - his judgement, not a data problem.

Working order:
 1. EGA intellectual-disability DAC (6 trios) - rehearsal application, cheapest
    yes to obtain, proves our signing entity can pass a DAC.
 2. MSSNG (63 autism long-read trios) - the actual target, approached with an
    EGA approval already on the record.
 3. GA4K (75 pediatric HiFi trios) - largest family count, heaviest dbGaP
    paperwork, attempt last.

## Explicitly unverified

- Whether SFARI Base distributes long-read BAMs at all.
- Complete-trio counts inside GREGoR's long-read subset and Genomics England's 315.
- Whether HPRC Release 2 added long reads for any PARENTS (Release 1 design gave
  parents Illumina only, so HPRC is long-read children, short-read parents).
- Approval turnaround for MSSNG, SFARI, EGA, Genomics England.
- dbGaP accession for the 2026 Cell Genomics autism long-read paper (publisher 403).

## Note on method

Max asked to route this through DeepSeek workers to save tokens. The DeepSeek
offload runner has no internet access, so it cannot do live web research. This
pass used cheap in-session research subagents instead; the expensive session only
ranked and decided. DeepSeek is the right tool for drafting the actual application
letters once we choose targets.
