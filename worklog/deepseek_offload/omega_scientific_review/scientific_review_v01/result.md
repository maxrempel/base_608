**Compact Scientific-Review Outline: XG1 OMEGA/Omun Comparison**  
*(Deidentified aggregate endpoints only; S1/S2/S3 = focal samples; public-control aggregates = 20 balanced cultured controls)*

---

**1. Main biological question**  
Does the focal sample set show a lower burden of clean, two-sided, deduplicated autosomal OMEGA insertion-locus detector endpoints (database-novel or known-rare <0.001, normalized by D10 callable autosomal bases) compared with public cultured controls, after accounting for technical and platform limitations?

**2. Strongest current evidence**  
- Control distribution is tight and well characterized: 20 individuals, 143–224 Omun person-loci (mean 187.55, median 184; rates 53.70–84.01/Gb, mean 70.32/Gb, median 69.00/Gb).  
- S1 rate = 58.19/Gb (155 Omun; 140 novel + 15 rare); only 1 of 20 controls has a rate at or below S1.  
- S2 = 1.13/Gb (3 Omun, all novel); 0/20 controls at or below this rate.  
- S3 = 0.375/Gb (1 Omun, novel); 0/20 controls at or below this rate.  
- All three focal rates are below the control mean and median; S2 and S3 are far below the full control range.  
- S1 overall read-support pass rate (64/155 = 41.3%) is within the seven-control range (32.0–41.9%), so S1’s low burden is not explained by a general excess of low-quality Omun calls.

**3. Null or weakened results**  
- S2 and S3 are not culture-matched to cultured controls; the focal-versus-cultured contrast is exploratory and confounded by culture/platform.  
- S1 is culture-comparable but only modestly low: its rate is within the lower tail of controls, not outside the observed range.  
- The S1 right-overhang 300–499 detector feature is a threshold-fragile hypothesis, not biological insertion length; it disappears at higher stringency (starts3/4/5) in both S1 and controls, and stringent passes are mostly 0 in controls (one control has 1).  
- Manta targeted calls reuse the same reads/alignments, so they provide computational corroboration only, not independent validation.  
- Body of evidence cannot support a claim of biological depletion, enrichment, or absence; all observations are detector-endpoint counts with technical caveats.

**4. Evidence of absence versus absence of evidence**  
- Evidence of absence is **not established**: no retained contig bridged both 800 bp flanks in S1 validation, and final local refinement recovered 0/3 real loci, consistent with separate terminal half-contigs rather than biological absence.  
- Absence of evidence is substantial: biological insertion length is unavailable (GIAB reconstruction panel: 0/32 exact, 30/32 unresolved, 2/32 false exact; 5,000 bp synthetic control unresolved despite eligible alignments).  
- Low observed counts can reflect mapper-dependent sensitivity: two missed real controls contained exact source contigs and accepted two-anchor mappings, but fresh full-reference mapping extended into payload and reduced opposite overhang below the unchanged 30 bp gate before parser candidate formation.  
- Therefore the focal low counts are currently best interpreted as detector/mapper/pipeline attrition, not as demonstrated biological absence.

**5. Exact blockers/gaps**  
- No independent validation of any focal Omun locus (assembly-based or otherwise).  
- Biological insertion length cannot be reconstructed (0/32 exact in GIAB panel; 30/32 unresolved).  
- Mapper sensitivity is variable and can suppress otherwise real loci before candidate formation, so the endpoint denominator is not validated as sensitivity-equivalent across samples.  
- Culture/platform mismatch for S2/S3 versus cultured controls.  
- Right-anchor overhang is a detector feature, not a biological insertion-size measurement.  
- Technical read-support attrition is not truth validation and cannot be used to revise burden.

**6. Falsification tests already done**  
- Control-rate comparison: tested whether focal rates fall outside the control distribution; S1 does not (1/20 controls at or below), S2/S3 do (0/20), but S2/S3 are confounded.  
- Read-quality test: S1 Omun technical pass rate versus seven-control range; no general excess.  
- Detector-feature threshold test: right-overhang 300–499 band at starts2/span gate disappears at starts3/4/5 in both S1 and controls.  
- Positive/simple control reconstruction: 100 bp synthetic control reconstructs; 5,000 bp control does not, showing length-dependent resolution failure.  
- OMEGA retained-assembly sensitivity test: 3 accepted real loci + 3 nearby shams yielded only 1/3 locus-window recovery, 1/3 expected terminal junction class, 0/3 exact coordinate plus both complete payload proxies; shams 0/3.  
- Mapper diagnostic: identified a concrete mechanism (payload extension reducing opposite overhang below gate) by which real loci are missed.  
- Local refinement: 0/3 real loci, 0/3 exact, 0/3 shams, indicating current assembly-based confirmation cannot distinguish real from sham.

**7. Three highest-value next analyses**  
1. **Sensitivity-calibrated rate comparison**: Apply the same mapper/parser pipeline to spike-in synthetic OMEGA-like insertions of varying payload lengths and flanking contexts in the focal and control samples, then compute detection-adjusted rates so that low counts can be interpreted with known sensitivity denominators.  
2. **Culture-matched reanalysis for S2/S3**: Obtain or generate non-cultured or matched-culture controls for S2/S3, or explicitly model culture/platform covariates, before any burden comparison is used for inference.  
3. **Long-read or hybrid assembly validation of the four focal Omun loci (S1:1–3, S2:3, S3:1) and matched control loci**: Use an orthogonal method that does not depend on the 30 bp overhang gate, to determine whether the low counts reflect true absence or mapper/pipeline dropout.
