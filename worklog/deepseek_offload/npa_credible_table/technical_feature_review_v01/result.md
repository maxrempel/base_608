## Critical Review

### Technical explanations gaining/losing support

- **Clustering (<1 kb span for 10/11) strongly supports a systematic technical artifact** – e.g., PCR duplication, mapping bias, or a single misaligned tandem duplication. This pattern is inconsistent with independent biological events and undermines the validity of the 11-event set as a whole.
- **Repeat/blacklist flag in only 1/11** initially suggests low contamination from known repetitive regions, but the high clustering rate implies an unannotated repetitive or low-complexity element may be driving the artifact. The flag is therefore insufficiently informative.
- **Representation not re-evaluated for 2/11** – these two events lack any manual or orthogonal check, weakening confidence and making them prime candidates for technical false positives.
- **Parent depth <20 for 3/11** increases the risk of low-coverage artifacts (e.g., failed Mendelian transmission call). This pattern is consistent with stochastic noise in shallow sequencing.
- **4 selected primary rows in background all non-empty for repeat/blacklist** – this indicates the filtering criteria for “primary” status are enriched for flagged sites, yet these are used as controls. This selection bias directly undermines any background comparison; the 4 selected primaries are not proxies for the 11 events.
- **8/201 background non-primary rows have flags** – a low fraction, suggesting that if background is intended to represent a neutral set, repeat/blacklist flags are relatively rare. The disparity with the 4/4 selected primary rows confirms a flawed control selection.

### Selection and denominator problems

- **Denominator for the 11 events is missing** – without the total number of candidate sites or the number of samples/regions screened, clustering proportion is uninterpretable. The 1-kb span likely contains an inflated rate of calls relative to the rest of the genome, but no background rate per kilobase is provided.
- **The 205-site background is not comparable** – annotation fields are incomplete, and the 4 selected primary rows are not independent controls. Using them as a denominator for enrichment testing would be circular.
- **Clustering itself invalidates simple count-based tests** – the 10/11 cluster violates the independence assumption required for binomial or Poisson models. Any statistical inference would need to treat the cluster as a single observation.

### Smallest phenotype-blind next local analysis

1. **For the 10 clustered events**: extract exact genomic coordinates, compute inter-event distances, and identify any shared sequence motif, homopolymer, or segmental duplication (e.g., via RepeatMasker or TRF). Also calculate strand bias (Fisher’s exact test) and allele balance in each sample. Compare these metrics to the 11th non-clustered event and to the 201 background non-primary rows (after completing annotation for the same fields).  
2. **Re-evaluate the 2 events not previously inspected** using the same technical metrics (read pileup, BAM visualization if available).  
3. **If clustering persists**, perform a permutation test: randomly shuffle the 11 events across the genome (conditioning on callable regions) and recompute the maximum cluster size. The empirical p-value will quantify whether the observed clustering is extreme relative to background expectation. This requires only the event coordinates and a callable-region mask—no phenotype data.

These steps will directly assess the dominant artifact hypothesis and provide a quantitative basis for either dismissing the 11-event set or proceeding with a corrected background model.
