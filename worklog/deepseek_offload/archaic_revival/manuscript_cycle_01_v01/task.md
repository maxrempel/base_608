# Draft cycle 1: evidence-locked Archaic Revival preprint

Last edited: 2026-08-03 by Codex (GPT-5.6 SOL)

Write a complete scientific manuscript draft in Markdown, approximately 3,000
to 4,500 words, for skeptical readers. It is a PRELIMINARY, NOT PEER REVIEWED
exploratory methods and data note. Output only the manuscript.

Working title concept: Archaic Revival. Use a scientifically explicit subtitle.
Draft for author Max Myakishev-Rempel, independent researcher. Mark authorship
responsibility and correspondence as pending author review. Do not identify an
AI system as an author. Include an AI-assistance disclosure in acknowledgments.

The paper timestamps the HOMEWARD statistic and a narrow observed pattern. It
must not claim discovery of back mutation, directed mutation, biological
restoration, a new evolutionary force, established germline reversion, or
independent chimp/gorilla replication.

Required structure: visible preliminary banner; title; author note; abstract;
plain-language summary; introduction; operational definitions; data and
methods; results; sensitivity and falsification results; discussion led by
conventional explanations; precise priority statement; limitations; preregistered
next tests; conclusion; data/code availability; ethics; competing interests;
funding; acknowledgments; references.

Evidence facts:

- 602 public high-coverage expanded 1000 Genomes trios, largely
  lymphoblastoid-cell-line-derived DNA.
- Permissive autosomal catalog: 3,042,677 child-nonparental SNV call rows,
  about 5,054 per child. Do not say all passed six child alternate reads.
- 1,711,689 rows had a usable Ensembl EPO ancestral label; 122,157 were
  drifted, meaning cohort consensus differed from inferred ancestor.
- Primary reported slice: cohort-ultrarare/private, pipeline-heterozygous,
  locally complex, 5,779 rows.
- RETURN means child alternate equals inferred ancestor.
- Primary pooled trinucleotide null: 3,579/5,779 RETURN =61.93%, versus
  3,336.9 expected=57.74%; excess 242.1 rows, +4.19 percentage points,
  observed/expected 1.073; model z about +8.4 from 200 simulations.
- High-confidence EPO: 3,226/5,234 vs 3,027.5, +3.79 points, z about +7.9.
- Non-CpG: 1,386/2,745 vs 1,189.6, +7.16 points, z about +8.5.
- Chimp polarity sensitivity: 3,527/5,587 vs 3,373.3, +2.75 points, z about
  +5.8. Gorilla: 9,383/14,552 vs 8,778.7, +4.15 points, z about +12.6.
  Both reuse same calls and overlap EPO inputs; label correlated outgroup
  sensitivity, not replication. Only 51.1% of chimp input rows mapped.

Critical corrections and falsification:

- Source reports conflict. A 23-chromosome gentle run produced 3,061,613
  clean-parent carrier rows; only 1,577,147 passed six child alternate reads.
  The 3,042,677 autosomal count matches the permissive carrier table. Exact
  input command/table/hash must be recovered before public release.
- Primary script learns its trinucleotide spectrum from all 1,711,689 calls
  across frequency, zygosity, and complexity, then applies it to the private
  heterozygous complex slice. This is a mismatched pooled null.
- Retained private-HET-complex anchored spectrum has 523,711 calls. Private
  versus pooled conditional trinucleotide spectra have weighted total variation
  6.67%, larger than the +4.19-point effect; maximum context target-probability
  shift is 20.9 points. The correctly matched result cannot be recomputed from
  retained sufficient rows.
- Conditioning on DRIFTED sites selects loci with a prior lineage
  substitution. Stable site/channel mutability, 7-mer context, methylation,
  replication, transcription, recombination, accessibility, chromatin, and
  mapping can make ordinary recurrence look like return.
- Strict VAF 0.35-0.65 PRIVATE complex sensitivity: 1,376/2,301 RETURN versus
  1,343.9 expected; 59.80% vs58.40%; +1.40 points; z about +1.8. About 86.8%
  of the primary excess lies outside this balanced subset. Main catalog mean
  VAF is about 0.25.
- A different older caller/endpoint/scrambled-parent null points oppositely:
  4.22 million NPA alleles; both-hom ancestral state 31.39% vs36.66%, z -34.6;
  both-het 12.54% vs18.94%, z -330.9; overall 12.99% vs21.85%. Not a direct
  refutation, but it makes the conclusion endpoint- and null-dependent.
- Synthetic engineering validation: 48/48 signals detected, 22/24
  germline-like spikes passed strict gate, 0/240 no-spike controls passed.
  This is not natural-catalog PPV.
- Natural strict pilot: 4/205 site rows passed, collapsing to 3 local events,
  all in one child; none proven biological germline de novo. Across completed
  chunks, 11 provisional events.
- Read review found somatic mosaics and segmental-duplication mis-mapping among
  apparent events. Complex sequence is not a full accessibility mask.
- Family spread is unresolved: odd/even r only 0.08-0.10; true batch and
  callable depth absent. Do not present family biology.

Novelty and context:

- Li & Chen 2011 already reported excess recreation of ancestral CpG
  dinucleotides; broad ancestral-recreation priority is unsafe.
- Safest priority: introduction of the HOMEWARD statistic and dated disclosure
  of this exact null-dependent pattern in specified LCL-derived public calls.
- Same cohort Ng et al. 2022 found 445,711 DNV calls, only 123/602 children
  under 100, some up to 11,219, with B-cell lymphoma signatures; they recommend
  primary tissue. Caballero & Koren 2023 document 885,655 LCL somatic mutations.
- Validated germline studies report about 60-70 SNVs per birth.

References to cite accurately:

Li & Chen 2011 DOI 10.1186/1471-2148-11-3.
Jiang & Zhao 2006 DOI 10.1016/j.ygeno.2006.06.003.
Mathieson & Reich 2017 DOI 10.1371/journal.pgen.1006581.
Byrska-Bishop et al. 2022 DOI 10.1016/j.cell.2022.08.004.
Ng et al. 2022 DOI 10.1002/humu.24455.
Caballero & Koren 2023 DOI 10.1016/j.xgen.2023.100305.
Conrad et al. 2011 DOI 10.1038/ng.862.
Jonsson et al. 2017 DOI 10.1038/nature24018.
Francioli et al. 2015 DOI 10.1038/ng.3292.
Aggarwala & Voight 2016 DOI 10.1038/ng.3511.
Seplyarskiy et al. 2023 DOI 10.1038/s41588-023-01562-0.
Seplyarskiy et al. 2021 DOI 10.1126/science.aba7408.
Hernandez et al. 2007 DOI 10.1093/molbev/msm108.
Keightley & Jackson 2018 DOI 10.1534/genetics.118.301120.
Paten et al. 2008 DOI 10.1101/gr.076521.108.
Harris & Nielsen 2014 DOI 10.1101/gr.170696.113.
Besenbacher et al. 2016 DOI 10.1371/journal.pgen.1006315.
Vale & Hyman 2016 DOI 10.7554/eLife.16931.

Required next-test gate:

1. Recover and hash exact primary rows and command.
2. Freeze same rows and compare matched-private anchored trinucleotide null,
   site-specific Roulette null, and scrambled-parent null.
3. Use analytic Poisson-binomial uncertainty, family/event cluster bootstrap,
   chromosome blocks, event collapse, and leave-one-family-out.
4. Apply strict accessibility and balanced genotype filters.
5. Replicate in validated primary-tissue germline trios.
6. Propagate ancestral-state uncertainty.

Tone: plain scientific English, skeptical, transparent, no sensationalism.
The abstract must contain both the primary +4.19-point result and the balanced
+1.40-point z1.8 result. State that posting timestamps disclosure, not
validation.
