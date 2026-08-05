# Draft cycle 2: literature-corrected HOMEWARD preprint

Last edited: 2026-08-03 by Codex (GPT-5.6 SOL)

Produce one clean Markdown manuscript of 2,500 to 3,500 words. Output only the
manuscript, once. Use ASCII punctuation only. Do not include planning notes,
self-talk, duplicate text, or unverified bibliographic details.

Title:
Archaic Revival: The HOMEWARD Statistic and a Preliminary, Null-Dependent
Excess of Ancestral-State Matches in 1000 Genomes Child-Nonparental SNV Calls

Author line:
Max Myakishev-Rempel
Independent researcher
Draft for author review; correspondence details pending

Put PRELIMINARY - NOT PEER REVIEWED - DO NOT CITE AS VALIDATED BIOLOGY at the
top. Include abstract, plain-language summary, introduction, operational
definitions, methods, results, sensitivity/falsification, discussion,
priority statement, limitations, next tests, conclusion, availability, ethics,
competing interests, funding, acknowledgments, and references.

Never conclude that the signal is an artifact. The evidence shows an unresolved,
null-dependent pattern with plausible conventional explanations. Never call
the rows germline de novo mutations. Never say the effect disappeared; say it
weakened to z about 1.8 in the balanced-VAF subset. Never say the balanced
subset repaired the null mismatch. Never call chimp/gorilla independent
replications.

Exact definitions:

- EPO means Enredo-Pecan-Ortheus. Use "Ensembl EPO-inferred ancestral base."
- Private tier means cohort AF below 0.0004, approximately no more than two
  alternate copies among 3,202 samples; it does not mean AF exactly zero.
- Pipeline-heterozygous means child VAF below 0.85 in the retained classifier;
  this broad label admits low-VAF calls.
- Locally complex means not flagged by the custom 41-base-flank low-complexity
  heuristic. It is not a strict accessibility, mappability, repeat, or
  segmental-duplication mask.
- Drifted means cohort consensus differs from inferred ancestor.
- RETURN means child alternate equals inferred ancestor at a drifted site.
- HOMEWARD statistic is observed RETURN fraction minus expected RETURN
  fraction under a declared null, reported with both fractions.

Exact evidence:

- 602 high-coverage expanded 1000 Genomes public trios, largely LCL-derived.
- 3,042,677 permissive autosomal child-nonparental SNV call rows, about 5,054
  per child. Provenance contradiction: a gentle 23-chromosome run yielded
  3,061,613 clean-parent carrier rows, of which only 1,577,147 passed six child
  alternate reads. Do not claim the primary 3,042,677 all passed six reads.
- 1,711,689 usable EPO labels; 122,157 drifted rows.
- Primary slice 5,779 private, pipeline-HET, locally complex drifted rows:
  3,579 RETURN=61.93%, pooled trinucleotide expected 3,336.9=57.74%;
  +242.1 rows, +4.19 percentage points, O/E 1.073, z about +8.4 from 200
  simulations.
- High-confidence EPO: 3,226/5,234 vs3,027.5, +3.79 points, z +7.9.
- Non-CpG: 1,386/2,745 vs1,189.6, +7.16 points, z +8.5.
- Chimp: 3,527/5,587 vs3,373.3, +2.75 points, z +5.8.
- Gorilla: 9,383/14,552 vs8,778.7, +4.15 points, z +12.6.
  Same call dataset, correlated polarity sensitivity. Chimp mapping retained
  only 51.1% of 529,490 input rows; mapped/unmapped bias unresolved.
- Main null is learned from all 1,711,689 rows across tiers and applied to the
  primary slice. The retained matched private-HET-complex anchored spectrum has
  523,711 rows. Private versus pooled conditional trinucleotide spectra have
  weighted total-variation 6.67%; maximum context target-probability shift
  20.9 points. This comparison warns that null mismatch can be large, but it
  does not quantify the bias in the 5,779 drifted test rows because those
  sufficient statistics are not retained.
- Balanced VAF 0.35-0.65 private complex: 1,376/2,301=59.80% vs1,343.9=58.40%;
  +1.40 points; z +1.8 under retained null. About 86.8% of primary excess lies
  outside this subset. Main catalog mean VAF about 0.25.
- Older different endpoint/caller/scrambled-parent null: 4.22M calls; both-hom
  ancestral 31.39% vs36.66%, z -34.6; both-het 12.54% vs18.94%, z -330.9;
  overall12.99% vs21.85%. Not a direct refutation; it proves definition/null
  dependence must be reconciled on same frozen rows.
- Synthetic engineering: 48/48 signals detected; 22/24 germline-like spikes
  passed strict gate; 0/240 no-spike controls passed. Not natural PPV.
- Natural strict pilot: 4/205 site rows, collapsed to 3 local events, one child;
  none proven germline. 11 provisional events across completed chunks.
- Family biology unresolved: odd/even r 0.08-0.10; batch/callable depth missing.

Conventional explanations:

- LCL somatic mutations and low VAF.
- Mapping/representation and incomplete accessibility masking.
- Null transferred from pooled anchored calls to a narrower drifted slice.
- Conditioning on sites with a historical substitution, which enriches for
  recurrent mutability.
- Ancestral-state mispolarization.
- Multinucleotide event clustering and nonindependent rows.

Priority boundary:

Li and Chen 2011 already reported excess recreation of ancestral CpGs. Claim
priority only for naming/formalizing the HOMEWARD statistic and timestamping
this exact null-dependent pattern and falsification record in this public
LCL-derived call catalog. A preprint timestamps disclosure, not validation.

Next-test gate:

1 recover/hash exact rows and command;
2 apply matched-private anchored, site-specific Roulette, 7-mer, and
scrambled-parent nulls to same frozen rows;
3 balanced VAF plus strict accessibility and external frequency;
4 event collapse, family/chromosome block bootstrap, Poisson-binomial
uncertainty, leave-one-family-out;
5 propagate ancestral uncertainty;
6 replicate in validated primary-tissue germline trios.

References. Use these exact titles and DOI links. Do not invent authors,
pagination, volumes, or alternate titles beyond what is given:

1. Li M, Chen SS. The tendency to recreate ancestral CG dinucleotides in the
human genome. https://doi.org/10.1186/1471-2148-11-3
2. Jiang C, Zhao Z. Mutational spectrum in the recent human genome inferred by
single nucleotide polymorphisms. https://doi.org/10.1016/j.ygeno.2006.06.003
3. Mathieson I, Reich D. Differences in the rare variant spectrum among human
populations. https://doi.org/10.1371/journal.pgen.1006581
4. Byrska-Bishop M et al. High-coverage whole-genome sequencing of the expanded
1000 Genomes Project cohort including 602 trios.
https://doi.org/10.1016/j.cell.2022.08.004
5. Ng JK et al. de novo variant calling identifies cancer mutation signatures
in the 1000 Genomes Project. https://doi.org/10.1002/humu.24455
6. Caballero M, Koren A. The landscape of somatic mutations in lymphoblastoid
cell lines. https://doi.org/10.1016/j.xgen.2023.100305
7. Conrad DF et al. Variation in genome-wide mutation rates within and between
human families. https://doi.org/10.1038/ng.862
8. Jonsson H et al. Parental influence on human germline de novo mutations in
1,548 trios from Iceland. https://doi.org/10.1038/nature24018
9. Francioli LC et al. Genome-wide patterns and properties of de novo mutations
in humans. https://doi.org/10.1038/ng.3292
10. Aggarwala V, Voight BF. An expanded sequence context model broadly explains
variability in polymorphism levels across the human genome.
https://doi.org/10.1038/ng.3511
11. Seplyarskiy V et al. A mutation rate model at the basepair resolution
identifies the mutagenic effect of polymerase III transcription.
https://doi.org/10.1038/s41588-023-01562-0
12. Seplyarskiy VB et al. Population sequencing data reveal a compendium of
mutational processes in the human germ line.
https://doi.org/10.1126/science.aba7408
13. Hernandez RD, Williamson SH, Bustamante CD. Context dependence, ancestral
misidentification, and spurious signatures of natural selection.
https://doi.org/10.1093/molbev/msm108
14. Keightley PD, Jackson BC. Inferring the Probability of the Derived versus
the Ancestral Allelic State at a Polymorphic Site.
https://doi.org/10.1534/genetics.118.301120
15. Paten B et al. Genome-wide nucleotide-level mammalian ancestor
reconstruction. https://doi.org/10.1101/gr.076521.108
16. Harris K, Nielsen R. Error-prone polymerase activity causes multinucleotide
mutations in humans. https://doi.org/10.1101/gr.170696.113
17. Besenbacher S et al. Multi-nucleotide de novo Mutations in Humans.
https://doi.org/10.1371/journal.pgen.1006315
18. Vale RD, Hyman AA. Priority of discovery in the life sciences.
https://doi.org/10.7554/eLife.16931

Acknowledgment must say draft used AI-assisted literature triage and language
editing, but scientific responsibility remains with the author after review.
Do not claim the author already reviewed or endorsed this draft.
