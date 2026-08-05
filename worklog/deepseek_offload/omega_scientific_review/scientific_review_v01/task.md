Task: Draft a concise scientific-review structure for the XG1 OMEGA/Omun comparison using only deidentified aggregate endpoints.

Privacy: Do not include coordinates, read IDs, alignments, participant identities, or private sequence. Use only S1/S2/S3 labels and public-control aggregate labels.

Definitions:
- OMEGA/Omun endpoint: clean, two-sided, deduplicated autosomal OMEGA insertion-locus detector endpoint that is database-novel or known-rare below 0.001, normalized by D10 callable autosomal bases.
- Right-anchor overhang is a detector feature, not biological insertion length.
- Technical read-support attrition is not truth validation and does not revise burden.

Current endpoint facts:
- 20 balanced public controls, four each AFR/AMR/EAS/EUR/SAS, all cultured samples. Total 3,751 Omun person-loci = 3,468 novel + 283 known-rare. Individual counts 143-224. Mean count 187.55, median 184. Rates 53.6989-84.0128/Gb, mean 70.3220, median 69.0031. Callable D10 denominators span only 0.2489 percent.
- S1: 155 Omun = 140 novel + 15 rare; callable D10 2,663,784,865; rate 58.1879/Gb; technical starts2 pass 64/155. Only one of 20 controls has rate <= S1.
- S2: 3 Omun = 3 novel + 0 rare; callable D10 2,664,221,029; rate 1.12603/Gb; starts2 pass 1/3. Zero of 20 controls have rate <= S2.
- S3: 1 Omun = 1 novel + 0 rare; callable D10 2,664,016,901; rate 0.3754/Gb; starts2 pass 1/1. Zero of 20 controls have rate <= S3.
- S2 and S3 are not culture-matched to cultured controls. The focal-versus-cultured contrast is exploratory and culture/platform confounded.

Current validation/sensitivity facts:
- GIAB known insertion length reconstruction panel: 0/32 exact, 30/32 unresolved, 2/32 false exact. Therefore biological insertion length is unavailable.
- Positive/simple controls: synthetic 100 bp spanning control reconstructs; 5,000 bp control is unresolved despite eligible alignments.
- OMEGA retained-assembly sensitivity: 3 accepted real loci + 3 nearby shams gave 1/3 locus-window recovery, 1/3 expected terminal junction class, 0/3 exact coordinate plus both complete payload proxies, shams 0/3.
- Mapper diagnostic: two missed real controls contained exact source contigs and accepted two-anchor mappings, but fresh full-reference mapping extended into payload and reduced opposite overhang below the unchanged 30 bp gate before parser candidate formation. Low observed counts can therefore reflect mapper-dependent sensitivity.
- Final two-anchor local refinement recovered 0/3 real loci, 0/3 exact, 0/3 shams. No retained contig bridged both 800 bp flanks, consistent with separate terminal half-contigs rather than biological absence.
- S1 right-overhang 300-499 detector feature: 19 raw band loci, 4 pass stringent starts2/span gate. Seven control persons have raw band counts 2-6 and stringent band passes mostly 0, one control has 1. At starts3/4/5 the band disappears in both S1 and controls. This is a threshold-fragile detector-feature hypothesis, not insertion length.
- S1 all-Omun technical pass 64/155 = 41.3%, within seven-control range 32.0-41.9%, so no general S1 read-quality excess.
- Manta targeted calls reuse same reads/alignments and are computational corroboration only, not independent validation.

Ask:
Return a compact review outline in plain scientific language with:
1. Main biological question.
2. Strongest current evidence.
3. Null or weakened results.
4. Evidence of absence versus absence of evidence.
5. Exact blockers/gaps.
6. Falsification tests already done.
7. Three highest-value next analyses.

Do not make participant identity claims. Do not claim biological depletion, enrichment, or absence.
