# MSSNG database access application draft v02

Last edited: 2026-08-01 by Codex (GPT-5.6 SOL)

Status: DRAFT ONLY. Nothing has been submitted or sent. The institutional identity, ethics basis, and cloud-only security plan have now been resolved from source records. Max must review the exact application and legal agreement before submission or signature.

## Researcher

- Name: Max Myakishev-Rempel, Ph.D.
- Institution: TRANSPOSON
- Title: Chief Executive Officer and Principal Investigator
- Address: 6294 Caminito Del Oeste, San Diego, California 92111-6829, United States
- Email: mrempel@transposon.org [confirm against the portal account before submission]

## Research team

Max Myakishev-Rempel only for the initial application. Any later person who will access MSSNG must be added and must complete the required agreement.

## Title of research project

Validating De Novo Mutational Spectra and Non-Reference Insertions in Autism Whole-Genome Trios and Multiplex Families

Word count: 15

## Lay description of project

Autism has strong genetic contributions, but many questions remain about how new mutations arise and whether their patterns differ among family members. We will analyze whole-genome sequences from autism trios and multiplex families. We will ask whether autistic children differ from their unaffected relatives in the types of spontaneous, or de novo, single-letter DNA changes they carry and in carefully supported DNA insertions that are absent from the standard human reference genome. We will use predefined quality rules, positive controls, contamination screening, and independent computational checks before treating a candidate as credible. Results will be reported for groups, not identifiable individuals. This is a test of specific hypotheses, not an attempt to confirm a predetermined conclusion. The study may clarify mutation patterns in autism while also improving methods for finding difficult genomic changes in family sequencing data.

Word count: 137

## Research question and specific aims

Research question: In MSSNG autism whole-genome trios and multiplex families, do autistic probands differ from unaffected relatives in rigorously validated germline de novo single-nucleotide and short insertion/deletion spectra or in high-confidence non-reference insertions?

Aim 1 will identify stringent de novo single-nucleotide variants and short insertions or deletions using family-aware calling and read-level quality filters. We will evaluate mutation burden, substitution spectrum, genomic context, and a predefined mutation-direction statistic relative to inferred ancestral primate alleles. Comparisons will account for parental age, ancestry, sex, sequencing platform and batch, coverage, callable genome, and relatedness. Autism status will not be used during variant calling or quality classification.

Aim 2 will identify candidate non-reference insertions and unmapped or partially mapped sequences. The workflow will be calibrated with known positive controls and synthetic spike-ins where appropriate. Candidates will require contamination screening, junction or local-assembly reconstruction, independent read support, and checks against human repeat, microbial, viral, and vector databases. Unresolved sequences will remain unresolved rather than being assigned a speculative origin.

Aim 3 will distinguish likely germline events from mosaicism, sequencing damage, sample mix-up, mapping artifacts, low-complexity regions, and contamination. Only candidates surviving predefined validation will enter proband-versus-relative comparisons of burden, spectrum, and genomic context. Analyses will use aggregate family-aware statistics, correction for multiple testing, sensitivity analyses, and no exploratory phenotype fishing.

The methods were piloted in 602 trios from the 1000 Genomes Project. Those exploratory analyses produced a modest aggregate mutation-direction statistic, while apparent recurrent hotspots disappeared after artifact filtering. The insertion detector has not yet passed exact-reconstruction controls. MSSNG therefore provides a falsifiable replication and calibration study, not confirmation of prior interpretations.

References: Yuen et al., Nature Neuroscience 2017, doi:10.1038/nn.4524; Trost et al., Cell 2022, doi:10.1016/j.cell.2022.10.009; Werling et al., Nature Genetics 2018, doi:10.1038/s41588-018-0107-y.

Word count: 288

## Feasibility

Max Myakishev-Rempel, Ph.D., is a molecular geneticist with wet-laboratory and computational genomics experience, more than 4,500 citations, and an h-index of 21. He earned his Ph.D. at the Institute of Gene Biology in Moscow and held research positions at the Medical College of Virginia, the National Cancer Institute, and the University of Rochester. His experience includes human genetics, single-nucleotide variation, transposable elements, gene regulation, whole-genome analysis, family-aware variant review, and reproducible computational pipelines.

The project will begin entirely within the approved MSSNG cloud environment. The workflow will be version-controlled, logged, staged through small pilots, benchmarked with positive controls, and designed to resume without repeating completed work. Sample identifiers and record-level results will remain inside the approved environment. Only aggregate, disclosure-reviewed results will leave it. No participant re-identification, outside linkage, or redistribution is planned.

Selected publications:

1. Myakishev M, Polesskaya O, Kulichkova V, et al. PCR-based detection of Pol III-transcribed transposons and its application to the rodent model of ultraviolet response. Cell Stress Chaperones. 2008;13:111-116. doi:10.1007/s12192-008-0010-z.
2. Polesskaya O, Kananykhina E, Roy-Engel AM, et al. The role of Alu-derived RNAs in Alzheimer's and other neurodegenerative conditions. Medical Hypotheses. 2018;115:29-34. doi:10.1016/j.mehy.2018.03.008.
3. Polesskaya O, Guschin V, Kondratev N, et al. On possible role of DNA electrodynamics in chromatin regulation. Progress in Biophysics and Molecular Biology. 2018;134:50-54. doi:10.1016/j.pbiomolbio.2017.12.006.
4. Lueders KK, Hu S, McHugh L, Myakishev MV, Sirota LA, Hamer DH. Genetic and functional analysis of single nucleotide polymorphisms in CHRNB2. Nicotine & Tobacco Research. 2002;4:115-125. doi:10.1080/14622200110098419.
5. Vinson C, Myakishev M, Acharya A, et al. Classification of human B-ZIP proteins based on dimerization properties. Molecular and Cellular Biology. 2002;22:6321-6335. doi:10.1128/MCB.22.18.6321-6335.2002.
6. Tian X, Azpurua J, Hine C, et al. High-molecular-mass hyaluronan mediates the cancer resistance of the naked mole rat. Nature. 2013;499:346-349. doi:10.1038/nature12234.
7. Myakishev-Rempel M, Stadler I, Polesskaya O, et al. Red light modulates ultraviolet-induced gene expression in the epidermis of hairless mice. Photomedicine and Laser Surgery. 2015;33:498-503. doi:10.1089/pho.2015.3916.

## Use of data

- Perform all analysis in the cloud: Yes.
- Use the research portal for searching data: Yes.
- Download data: No, not initially.
- Country where research will be conducted: United States.
- Description of data proposed to be downloaded: Not applicable for the initial cloud-only phase. Any later download would require prior MSSNG approval and a verified compliant environment.

## Requested cohort and data

Family-based MSSNG participants, prioritizing complete autism trios and multiplex families with probands, both parents, and unaffected siblings or relatives where available. Requested data are approximately 30-fold whole-genome sequence data, aligned or read-level files needed for validation, existing variant files, pedigree structure, sequencing and quality-control metadata, and only the phenotype fields necessary to identify affected status and prespecified covariates.

## Data security safeguards

Proposed selection: Yes.

TRANSPOSON has documented a project-specific cloud-only security plan covering individual access, provider audit logging, endpoint protection, incident response, disclosure review, retention, and destruction. Only the named researcher will access data using an individual account. Raw and participant-level data will remain inside the MSSNG-approved cloud environment. No local download, removable-media storage, outside synchronization, re-identification, external linkage, or credential sharing is permitted. Windows Firewall and Microsoft Defender real-time protections are active on the intended workstation. Any later local download is prohibited until MSSNG gives written approval and TRANSPOSON verifies full-disk encryption and the additional local safeguards required by the agreement.

## Research ethics: foreseeable issues

Yes, genetic comparisons can create a risk of stigmatizing autistic people, families, or ancestry groups if results are overinterpreted. The project will use autism status only for prespecified group comparisons, treat ancestry as a statistical covariate rather than a biological hierarchy, suppress small or potentially identifying cells, avoid individual or family ranking, report negative and uncertain findings, and distinguish association from cause. Results will be described in respectful, non-essentialist language and will not be used for diagnosis or return of individual findings.

## Does TRANSPOSON require research ethics approval?

Proposed selection: No.

Proposed justification: TRANSPOSON does not require separate research ethics approval for this project because it is limited to secondary computational analysis of existing coded data collected under prior consent. The researcher will have no participant contact, access to the identity key, intervention, return of individual findings, re-identification attempt, or unapproved external linkage. All work remains subject to the MSSNG Database Access Agreement, Data Access Compliance Office review, consent restrictions, and TRANSPOSON's project-specific security and disclosure controls. If MSSNG or an applicable authority requires an independent exemption determination or review, it will be obtained before analysis begins.

## Database access agreement and public researcher listing

- Confirm all applicants have read and agreed to the agreement: Pending Max's review and signature.
- Confirm researcher names may be posted publicly: Pending Max's review.

## Institutional and submission details

- Current governing form: MSSNG Database Access Agreement version 2.2, United States.
- Institution legal name: TRANSPOSON.
- Institution address: 6294 Caminito Del Oeste, San Diego, California 92111-6829, United States.
- Researcher title: Chief Executive Officer and Principal Investigator.
- Initial research team: Max Myakishev-Rempel only.
- Institution official: Oksana Polesskaya, Ph.D., TRANSPOSON Signing Official, using opolessk@transposon.org. TRANSPOSON's existing controlled-data approval records consistently assign this role to her. Max remains the Chief Executive Officer and Principal Investigator.
- Ethics basis: documented in `transposon_mssng_ethics_basis_v01.md`.
- Security controls: documented in `transposon_mssng_data_security_plan_v01.md`.

Before submission, confirm only the portal email/account mapping and that the portal is serving the same version 2.2 United States agreement. The application requests aligned or read-level files needed for validation; exact CRAM or BAM availability may be confirmed by MSSNG during feasibility review and is not a filing blocker.

## Submission state

Nothing has been submitted, emailed, signed, or agreed to. Max must review and explicitly approve the exact completed application before submission.
