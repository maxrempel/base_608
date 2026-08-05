PRELIMINARY - NOT PEER REVIEWED - DO NOT CITE AS VALIDATED BIOLOGY

# Archaic Revival: The HOMEWARD Statistic and a Preliminary, Null-Dependent Excess of Ancestral-State Matches in 1000 Genomes Child-Nonparental SNV Calls

Max Myakishev-Rempel
Independent researcher
Draft for author review; correspondence details pending

## Abstract

Single-nucleotide variants that appear only in a child and not in either parent are often interpreted as candidate de novo mutations, but many arise from somatic mosaicism, cell-line immortalization, or technical artifacts. This preprint introduces the HOMEWARD statistic—the observed fraction of child-nonparental calls in which the alternate allele matches the inferred ancestral base at a drifted site, minus the fraction expected under a declared mutational null. We apply the statistic to 3,042,677 permissive child-nonparental autosomal SNV calls from 602 high-coverage 1000 Genomes trios, restricting to private, pipeline-heterozygous, locally complex sites that carry an Ensembl EPO-inferred ancestral state. Among 5,779 drifted rows in that primary slice, the observed RETURN fraction is 61.93%, compared with 57.74% expected from a pooled trinucleotide null (z approximately +8.4). A high-confidence EPO subset gives 61.64% vs. 57.85% (z +7.9), and the non-CpG subset gives 50.49% vs. 43.33% (z +8.5). In a balanced variant-allele-fraction (VAF 0.35–0.65) subset the excess weakens to +1.40 percentage points (z about 1.8). The signal is strongly dependent on the choice of null model; an older scrambled-parent null applied to a different call set yields a deficit. Conventional explanations—including lymphoblastoid somatic variation, incomplete mapping filters, null mismatch across genomic partitions, ancestral-state mispolarization, and multinucleotide events—are not ruled out. The work makes no claim of validated biology; it formalizes a reproducible computation and timestamps the pattern in a public LCL-derived catalog while recording a detailed falsification record and a prioritized next-test gate.

## Plain-language summary

When a child carries a DNA letter that neither parent carries, one natural explanation is a new mutation that occurred in the egg or sperm. However, such changes can also arise after fertilization, in the immortalized blood cells used for sequencing, or from data-handling quirks. This preprint looks at a specific feature of those rare child-only DNA variants: whether they tend to recreate the DNA letter that was present at that position millions of years ago in our common ancestor with other primates. In a set of 602 family genomes from the 1000 Genomes Project, child-only variants that pass lenient filters show a modest but statistically clear excess of recreated ancestral letters. The excess is much weaker in a subset of variants with a balanced number of reads supporting each letter, and it could be explained by known technical and biological confounders. The study does not claim to have discovered a new biological phenomenon; instead it publicly records the pattern, defines a metric (the HOMEWARD statistic), and lays out specific steps that would need to be taken before drawing any firm conclusion. The data and statistical code are not yet released, and the author has not reviewed this draft.

## Introduction

The cataloging of rare and private genetic variation from large trio-sequencing consortia has provided a rich resource for studying the mutational processes that operate in the human germline and soma. One prominent signal reported early in the 1000 Genomes era was a tendency for human polymorphisms to recreate the ancestral CpG dinucleotide (Li and Chen 2011), attributed primarily to the high mutability of methylated CpG sites.

More recently, several studies have noted that child-nonparental single-nucleotide calls in LCL-derived genomes from public repositories contain an appreciable fraction of low-VAF variants that likely represent somatic mutations acquired during cell-line immortalization and propagation (Caballero and Koren 2023; Ng et al. 2022). Distinguishing genuine germline de novo mutations from somatic or technical artifacts remains a considerable challenge.

This preprint approaches the question from a different angle. Instead of attempting to purify a set of true germline mutations, we condition on a lenient call catalog and ask whether, among well-measured sites where the current human population has drifted away from the inferred mammalian ancestor, the child-nonparental calls preferentially return to the ancestral state. This would be expected if the variants were enriched for neutral somatic mutations that follow a conventional mutational spectrum, but it could also be produced by more exotic processes or by biases in the data pipeline.

We formalize a simple metric, the HOMEWARD statistic, and compute it on a frozen set of permissive child-nonparental SNV calls from 602 trios in the expanded 1000 Genomes Project. We present the observed excess, show that its magnitude depends heavily on variant-allele fraction and on the choice of null model, and outline a series of tests that any biological interpretation would need to survive. The manuscript is a disclosure and methodological timestamp; it is not a claim of validated biology.

## Operational definitions

- **Ancestral base**: The Ensembl EPO-inferred ancestral base (EPO: Enredo-Pecan-Ortheus).
- **Private tier**: Cohort alternate-allele frequency (AF) below 0.0004, corresponding to at most two alternate copies among 3,202 samples; it does not require AF exactly zero.
- **Pipeline-heterozygous (pipeline-HET)**: Child variant-allele fraction (VAF) below 0.85 in the retained classifier; this label admits low-VAF calls.
- **Locally complex**: Not flagged by a custom 41-base-flank low-complexity heuristic. This is not a strict accessibility, mappability, repeat, or segmental-duplication mask.
- **Drifted**: Cohort consensus base differs from the EPO-inferred ancestral base at the site.
- **RETURN**: The child alternate allele equals the EPO-inferred ancestral base at a drifted site.
- **HOMEWARD statistic**: Observed RETURN fraction minus expected RETURN fraction under a declared null model; both fractions are reported explicitly.

## Methods

### Data sources and initial calls

High-coverage whole-genome sequence data for the expanded 1000 Genomes Project (Byrska-Bishop et al. 2022) were obtained from public repositories. A permissive autosomal child-nonparental SNV call set was generated for 602 trios using a lenient caller and minimal filtering. The primary working set contains 3,042,677 rows. A provenance note: a subsequent gentle 23-chromosome run from the same input produced 3,061,613 clean-parent carrier rows, of which only 1,577,147 fulfilled a retrospective threshold of at least six child alternate reads; the primary 3,042,677 set includes rows that would not meet that strict filter. All primary analyses use the larger permissive set.

### Ancestral-state and spectrum assignment

Each call was intersected with Ensembl EPO whole-genome primate alignments (Paten et al. 2008). Sites lacking an EPO label or labelled as ambiguous were removed, leaving 1,711,689 usable EPO labels out of the permissive set. Within those, 122,157 sites were classified as drifted (cohort consensus differing from the EPO base). For each call the local trinucleotide context (the mutated base and its immediate flanking bases) was recorded.

### Primary slice definition

The primary analysis slice was defined by three intersecting conditions: private tier, pipeline-HET, and locally complex (as defined above). Applied to the drifted EPO-labeled rows, this produced 5,779 calls.

### Null model construction

Two main null models were used.

1. **Pooled trinucleotide null**: The expected RETURN probability for each call was taken as the empirical RETURN probability among all 1,711,689 EPO-labeled rows, stratified by trinucleotide context and aggregated across all tiers.
2. **Scrambled-parent null**: An independent older call set of 4.22M child-nonparental rows was processed by randomly permuting the parental genotypes while preserving the joint frequency of child genotypes; the expected RETURN fraction was then derived from the rows that remained both-homozygous or both-heterozygous after scrambling.

For the primary slice, 200 simulation rounds of the pooled null gave an expected RETURN count of 3,336.9 with a standard deviation that placed the observed count 8.4 standard deviations above the mean.

### Additional sensitivity analyses

The same statistic was recomputed on subsets that enforced high-confidence EPO assignments (EPO posterior probability >0.95), non-CpG contexts, and a balanced-VAF (0.35–0.65) private complex subset. Chimp and gorilla EPO labels were also substituted to assess polarity sensitivity; no independent replication is implied because the same permissive call set was used.

### Synthetic and natural pilot checks

A synthetic engineering experiment was performed by spiking known variant sets into the data; 48/48 spike-in signals were detected, and 22/24 germline-like signal spikes passed a strict gate, while 0/240 no-spike controls passed. A natural strict pilot that required concordant evidence across two callers yielded 4 candidate site rows out of 205, collapsing to three local events in a single child; none could be validated as germline. Across all completed chromosomal chunks, 11 provisional events were noted. The family biology of the signal shows an odd/even sibling correlation of 0.08–0.10, and per-batch and per-callable-depth statistics are not yet available.

## Results

### Primary HOMEWARD excess

In the primary slice of 5,779 private, pipeline-HET, locally complex drifted rows, the observed RETURN count is 3,579 (61.93%). The pooled trinucleotide null expects 3,336.9 RETURN counts (57.74%), yielding a HOMEWARD excess of +242.1 rows (+4.19 percentage points; observed/expected ratio 1.073). Under the 200-simulation null distribution, this corresponds to a z-score of approximately +8.4.

High-confidence EPO subset (5,234 rows): 3,226 observed vs. 3,027.5 expected (+3.79 percentage points, z +7.9). Non-CpG-only subset (2,745 rows): 1,386 observed vs. 1,189.6 expected (+7.16 percentage points, z +8.5). Thus the signal is not driven solely by CpG hypermutability and is present in multiple data-quality cuts.

### Alternative primate bases

When the chimp EPO base is used as the ancestral anchor, 5,587 rows are available (mapping retained only 51.1% of 529,490 input rows) and the observed RETURN fraction is 63.14% vs. expected 60.39% (+2.75 points, z +5.8). For gorilla (14,552 rows) the fractions are 64.48% vs. 60.33% (+4.15 points, z +12.6). The differing mapping rates and magnitudes reflect correlated polarity sensitivity; they are not independent replications because the same underlying call catalog was employed.

### Impact of VAF

The primary slice has a mean child VAF of approximately 0.25. Restricting to calls with VAF between 0.35 and 0.65 leaves 2,301 rows. In this balanced-VAF subset the observed RETURN fraction is 59.80% (1,376 rows) vs. 58.40% expected (1,343.9), yielding a HOMEWARD excess of +1.40 percentage points (z about 1.8). Approximately 86.8% of the primary excess lies outside this subset. The excess therefore weakens considerably when low- and high-VAF tails are removed; it does not disappear.

### Null-model dependence

The main null above is learned from all 1,711,689 EPO-labeled rows (spanning all tiers) and applied to the privately filtered drifted slice. The anchored matched private-HET-complex background spectrum (523,711 rows) differs from the pooled trinucleotide spectrum. The weighted total-variation distance between private and pooled conditional trinucleotide spectra is 6.67%, and the maximum absolute shift in a single context’s target probability is 20.9 percentage points. This warns that null mismatch could be substantial, though the exact bias in the 5,779 drifted test rows is unknown because the full joint distributions were not retained.

An older, independent call set (4.22M calls, different endpoint and caller, scrambled-parent null) illustrates the definition dependence starkly: for ancestral alleles in both-homozygous rows the observed RETURN fraction is 31.39% vs. expected 36.66% (z −34.6); for both-heterozygous rows 12.54% vs. 18.94% (z −330.9); overall 12.99% vs. 21.85%. This is not a direct refutation of the primary signal, but it demonstrates that the direction and magnitude of the HOMEWARD statistic can flip entirely depending on the call set and null construction. Reconciliation on a single frozen set of rows is essential.

## Sensitivity and falsification record

The following internal consistency checks were performed:

- **Synthetic spike-in recovery**: Detection sensitivity for engineered signals is high (48/48).
- **Strict pilot candidate rate**: In a small pilot requiring multi-caller support, 4/205 site rows survived, none validated as germline.
- **Family correlation**: Sibling correlation (odd/even assignment) is near zero (r=0.08–0.10).

These checks neither confirm nor exclude a biological origin; they demonstrate that the permissive call set is noisy and that the observed HOMEWARD excess, while statistically robust under the pooled null, is sensitive to data-processing choices.

## Discussion

The observation that child-nonparental SNV calls in LCL-derived genomes preferentially match the EPO-inferred ancestral base when the population has drifted away is consistent with multiple conventional explanations:

1. **LCL somatic mutations**: Low-VAF calls (mean ~0.25) are enriched for cell-line somatic variants that may follow a mutational spectrum with an elevated rate of reversion to the ancestral state, particularly when conditioned on historical substitution.
2. **Mapping and representation biases**: Incomplete accessibility masking, local mappability variation, and reference-bias during alignment could create a false RETURN excess at drifted sites.
3. **Null transfer from pooled to private tier**: The observed weighted total-variation distance of 6.67% between private and pooled spectra implies that the pooled trinucleotide null is not perfectly tailored to the tested slice.
4. **Conditioning on historical substitution**: Requiring a drifted site enriches for positions that have already undergone a substitution along the human lineage, potentially enriching for locally elevated mutation rates that could recur.
5. **Ancestral-state mispolarization**: Errors in the EPO reconstruction, especially at rapidly evolving sites or in incomplete lineage sorting regions, could inflate RETURN counts.
6. **Multinucleotide event clustering**: Nearby mutations can create non-independent rows, inflating apparent signal strength.

Critically, the signal weakens substantially (to z ~1.8) in the balanced-VAF subset and has not been replicated in a validated germline trio dataset from primary tissue. The negative result from the older scrambled-parent null further underscores the fragility of the signal under changes in filter thresholds and null specification.

The HOMEWARD statistic as formalized here provides a convenient scalar summary, but it cannot on its own distinguish among the above confounders.

## Priority statement

Li and Chen (2011) previously reported an excess of recreated ancestral CpG dinucleotides in human polymorphisms. This preprint does not claim to have discovered the underlying pattern de novo. The priority claims are limited to (a) naming and formalizing the HOMEWARD statistic, (b) timestamping this exact null-dependent pattern and its associated falsification record in a specific public LCL-derived SNV call catalog, and (c) laying out a concrete next-test gate. A preprint serves to disclose and to establish timing; it does not confer validation (Vale and Hyman 2016).

## Limitations

- The primary call set is permissive and contains rows that would not pass a strict alternate-read threshold; an earlier 23-chromosome reprocessing suggests a substantial fraction would be eliminated.
- Null-model assignment relies on pooled trinucleotide frequencies that have not been matched on VAF, genomic background, or family structure.
- The analysis conditions on drifted sites, which inherently selects for a non-random subset of the genome.
- EPO ancestral-state calls contain errors; their uncertainty has not been propagated.
- Row independence is assumed but not verified; multinucleotide events and within-family clustering are not modeled.
- No validated primary-tissue germline trio replication exists.
- The exact computational workflow and intermediate hashes are not yet publicly archived, hindering exact reproduction.

## Next-test gate

The following steps are required before any substantive biological claim can be entertained:

1. Recover and hash the exact input rows and commands to enable faithful reproduction.
2. Apply matched-private anchored, site-specific Roulette (Seplyarskiy et al. 2023; Seplyarskiy et al. 2021), 7-mer (Aggarwala and Voight 2016), and scrambled-parent nulls to the same frozen rows.
3. Recompute the HOMEWARD statistic after imposing balanced VAF, strict accessibility mappability filters, and external population-frequency databases.
4. Collapse multinucleotide events, perform family- and chromosome-block bootstrap, use Poisson-binomial confidence intervals, and perform leave-one-family-out cross-validation.
5. Propagate full ancestral-state uncertainty using the EPO posterior distribution.
6. Replicate in a validated primary-tissue germline trio dataset where contamination and somatic mosaicism are rigorously controlled.

Until these steps are completed, the observed excess should be regarded as an unresolved, null-dependent pattern in a specific analytical pipeline.

## Conclusion

We report a preliminary null-dependent excess of ancestral-state matches in 1000 Genomes child-nonparental SNV calls: among private, pipeline-heterozygous, locally complex drifted sites the HOMEWARD statistic shows +4.19 percentage points (z ~8.4) under a pooled trinucleotide null. The excess weakens in a balanced-VAF subset to +1.40 points (z ~1.8) and is highly sensitive to null specification. All plausible conventional explanations remain viable. This preprint documents the pattern, supplies a formal metric, and publishes a detailed falsification record and next-test gate. No validated biological inference is drawn.

## Availability

The exact code and data hashes are not yet publicly deposited. The author intends to release them alongside all processing commands upon full documentation. In the interim, the raw 1000 Genomes data are available from the International Genome Sample Resource.

## Ethics

The work uses publicly available, de-identified human genomic data collected under informed consent by the 1000 Genomes Project. No new human subjects research was conducted.

## Competing interests

The author declares no competing interests.

## Funding

No external funding was received for this work.

## Acknowledgments

This draft was produced with AI-assisted literature triage and language editing. Scientific responsibility remains solely with the author after final review; the author has not yet reviewed or endorsed this draft version. The 1000 Genomes Project and the Ensembl team are thanked for making data and annotations openly available.

## References

1.  Li M, Chen SS. The tendency to recreate ancestral CG dinucleotides in the human genome. BMC Evolutionary Biology. 2011;11:3. https://doi.org/10.1186/1471-2148-11-3
2.  Jiang C, Zhao Z. Mutational spectrum in the recent human genome inferred by single nucleotide polymorphisms. Genomics. 2006;88(3):263–272. https://doi.org/10.1016/j.ygeno.2006.06.003
3.  Mathieson I, Reich D. Differences in the rare variant spectrum among human populations. PLOS Genetics. 2017;13(2):e1006581. https://doi.org/10.1371/journal.pgen.1006581
4.  Byrska-Bishop M et al. High-coverage whole-genome sequencing of the expanded 1000 Genomes Project cohort including 602 trios. Cell. 2022;185(18):3426–3440.e19. https://doi.org/10.1016/j.cell.2022.08.004
5.  Ng JK et al. de novo variant calling identifies cancer mutation signatures in the 1000 Genomes Project. Human Mutation. 2022;43(12):1979–1993. https://doi.org/10.1002/humu.24455
6.  Caballero M, Koren A. The landscape of somatic mutations in lymphoblastoid cell lines. Cell Genomics. 2023;3(6):100305. https://doi.org/10.1016/j.xgen.2023.100305
7.  Conrad DF et al. Variation in genome-wide mutation rates within and between human families. Nature Genetics. 2011;43(7):712–714. https://doi.org/10.1038/ng.862
8.  Jonsson H et al. Parental influence on human germline de novo mutations in 1,548 trios from Iceland. Nature. 2017;549(7673):519–522. https://doi.org/10.1038/nature24018
9.  Francioli LC et al. Genome-wide patterns and properties of de novo mutations in humans. Nature Genetics. 2015;47(7):822–826. https://doi.org/10.1038/ng.3292
10. Aggarwala V, Voight BF. An expanded sequence context model broadly explains variability in polymorphism levels across the human genome. Nature Genetics. 2016;48(4):349–355. https://doi.org/10.1038/ng.3511
11. Seplyarskiy V et al. A mutation rate model at the basepair resolution identifies the mutagenic effect of polymerase III transcription. Nature Genetics. 2023;55(12):2152–2163. https://doi.org/10.1038/s41588-023-01562-0
12. Seplyarskiy VB et al. Population sequencing data reveal a compendium of mutational processes in the human germ line. Science. 2021;373(6558):1030–1035. https://doi.org/10.1126/science.aba7408
13. Hernandez RD, Williamson SH, Bustamante CD. Context dependence, ancestral misidentification, and spurious signatures of natural selection. Molecular Biology and Evolution. 2007;24(8):1792–1800. https://doi.org/10.1093/molbev/msm108
14. Keightley PD, Jackson BC. Inferring the Probability of the Derived versus the Ancestral Allelic State at a Polymorphic Site. Genetics. 2018;209(3):897–906. https://doi.org/10.1534/genetics.118.301120
15. Paten B et al. Genome-wide nucleotide-level mammalian ancestor reconstruction. Genome Research. 2008;18(11):1829–1843. https://doi.org/10.1101/gr.076521.108
16. Harris K, Nielsen R. Error-prone polymerase activity causes multinucleotide mutations in humans. Genome Research. 2014;24(9):1445–1454. https://doi.org/10.1101/gr.170696.113
17. Besenbacher S et al. Multi-nucleotide de novo Mutations in Humans. PLOS Genetics. 2016;12(11):e1006315. https://doi.org/10.1371/journal.pgen.1006315
18. Vale RD, Hyman AA. Priority of discovery in the life sciences. eLife. 2016;5:e16931. https://doi.org/10.7554/eLife.16931
