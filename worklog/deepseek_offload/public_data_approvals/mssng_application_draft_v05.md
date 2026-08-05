# MSSNG database access application draft v05

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

De Novo Noncoding Variants Affecting Chromatin Regulation in Autism Families

Word count: 10

## Lay description of project

Autism has a strong genetic component, but most genetic studies have concentrated on the small portion of the genome that encodes proteins. The much larger noncoding genome contains regulatory elements that control when and where genes are active and how DNA is organized within the cell nucleus. We will study autism families to identify new, or de novo, noncoding variants present in a child but absent from both parents. We will test whether autistic children carry an excess of variants predicted to disrupt regulatory DNA, chromatin accessibility, enhancer-promoter communication, or other features of genome organization important during brain development. Comparisons with unaffected relatives will use stringent family-based quality controls. The study will identify credible regulatory candidates and affected biological pathways, while recognizing that computational evidence predicts function but does not by itself prove it.

Word count: 130

## Research question and specific aims

Research question: In MSSNG autism families, are autistic probands enriched for high-confidence de novo noncoding variants predicted to disrupt chromatin regulation or the control of neurodevelopmental gene expression, compared with unaffected relatives?

Aim 1 will identify germline de novo single-nucleotide variants and short insertions or deletions using pedigree-aware calling, read-level validation, and a consistently defined callable genome. Variant detection and quality classification will be performed without using autism status. Analyses will account for parental age, ancestry, sex, sequencing platform, batch, coverage, and relatedness.

Aim 2 will prioritize de novo variants in noncoding regulatory DNA using established reference annotations rather than external participant-level data. These annotations will include promoters, enhancers, chromatin-accessible regions, transcription-factor binding sites, insulators, and boundaries or contacts involved in three-dimensional genome organization. Neural and developmental annotations will be emphasized. Predicted effects will include altered regulatory motifs, enhancer-promoter relationships, chromatin accessibility, and regulation of nearby or contact-linked genes.

Aim 3 will test whether autistic probands differ from unaffected siblings or other unaffected relatives in the burden and predicted functional severity of these variants. Analyses will compare matched callable sequence, use family-aware statistical models, correct for multiple testing, and perform sensitivity analyses across annotation sets and technical strata. Results will be reported at aggregate level. Individual variants will be described as candidates whose function requires experimental validation, not as proven causes of autism.

This study is directly suited to whole-genome family data because de novo status requires both parents and most regulatory DNA lies outside exons. It builds on the researcher's experience in psychiatric genetics, transcription-factor biology, regulatory genomics, and chromatin structure.

References: Yuen et al., Nature Neuroscience 2017, doi:10.1038/nn.4524; Werling et al., Nature Genetics 2018, doi:10.1038/s41588-018-0107-y; Zhou et al., Nature Genetics 2019, doi:10.1038/s41588-019-0420-0.

Word count: 312

## Feasibility

Max Myakishev-Rempel, Ph.D., is a molecular geneticist with wet-laboratory and computational genomics experience, more than 4,500 citations, and an h-index of 21. He earned his Ph.D. at the Institute of Gene Biology in Moscow and held research positions at the Medical College of Virginia, the National Cancer Institute, and the University of Rochester. His experience includes psychiatric genetics, family-based linkage and association analysis, single-nucleotide variation, transcription-factor biology, promoter regulation, chromatin structure, whole-genome analysis, and reproducible computational pipelines.

The project requires complete individual-level whole-genome read data for family-aware calling and read-level validation. Approved CRAM alignments and their indexes will be downloaded to a secured TRANSPOSON-controlled compute and storage environment. The workflow will be version-controlled, logged, staged through small family pilots, benchmarked with positive controls, and designed to resume without repeating completed work. Access will be limited to approved personnel. No participant re-identification, outside linkage, or redistribution is planned.

Selected publications:

1. Straub RE, Jiang Y, MacLean CJ, Ma Y, Webb BT, Myakishev MV, et al. Genetic variation in the 6p22.3 gene DTNBP1, the human ortholog of the mouse dysbindin gene, is associated with schizophrenia. American Journal of Human Genetics. 2002;71:337-348. doi:10.1086/341750.
2. Straub RE, MacLean CJ, Martin RB, Ma Y, Myakishev MV, Harris-Kerr C, et al. A schizophrenia locus may be located in region 10p15-p11. American Journal of Medical Genetics. 1998;81:296-301.
3. Straub RE, Sullivan PF, Ma Y, Myakishev MV, Harris-Kerr C, et al. Susceptibility genes for nicotine dependence: a genome scan and followup in an independent sample suggest that regions on chromosomes 2, 4, 10, 16, 17 and 18 merit further study. Molecular Psychiatry. 1999;4:129-144. doi:10.1038/sj.mp.4000518.
4. Rozenberg JM, Shlyakhtenko A, Glass K, Rishi V, Myakishev MV, FitzGerald PC, Vinson C. All and only CpG containing sequences are enriched in promoters abundantly bound by RNA polymerase II in multiple tissues. BMC Genomics. 2008;9:67. doi:10.1186/1471-2164-9-67.
5. Vinson C, Myakishev M, Acharya A, Mir AA, Moll JR, Bonovich M. Classification of human B-ZIP proteins based on dimerization properties. Molecular and Cellular Biology. 2002;22:6321-6335. doi:10.1128/MCB.22.18.6321-6335.2002.

## Use of data

- Perform all analysis in the cloud: No.
- Use the research portal for cohort identification and authorized transfer: Yes.
- Download data: Yes.
- Country where research will be conducted: United States.
- Description of data proposed to be downloaded: Complete individual-level, whole-genome read files in CRAM format, with CRAI indexes, required reference files, pedigree relationships, sequencing and quality-control metadata, affection status, and the limited phenotype fields needed for prespecified covariates. Files must retain the available mapped, unmapped, supplementary, secondary, clipped, discordant, and chimeric read evidence needed for independent calling and local reconstruction. The initial transfer will include every sequenced member of at least 300 complete autism families, prioritizing trios with an autistic proband and both biological parents and including unaffected siblings where available. Permission is requested to expand the download to additional qualifying complete families as storage permits. Derived VCF files, consensus sequences, or assemblies alone are not acceptable substitutes for read-level data because the project requires independent calling and read-level validation across coding and noncoding regions.

## Requested cohort and data

Family-based MSSNG participants, prioritizing complete autism trios and multiplex families with probands, both biological parents, and unaffected siblings or relatives where available. The requested genomic data are the complete approximately 30-fold whole-genome CRAM files and indexes for each individual, retaining all available read-level evidence rather than a variant-only or assembly-only subset. The initial target is at least 300 complete families, with authorization to add further qualifying families as local capacity permits. Pedigree structure, sequencing and quality-control metadata, affection status, and only the phenotype fields required for prespecified covariates are also requested.

## Data security safeguards

Proposed selection: Pending verification of the designated TRANSPOSON download environment.

The project-specific security plan is being revised for local CRAM storage. Before checking Yes, TRANSPOSON will document and verify encrypted storage, physical access control, individual user access, non-user-deletable audit logging, malware and firewall protection, controlled backup, incident response, and auditable destruction. Removable-media storage, outside synchronization, re-identification, external linkage, redistribution, and credential sharing will be prohibited.

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
