Task: Draft a concise executable OMEGA/Omun calibration specification from deidentified aggregate evidence.

Privacy and scope:
- Do not include participant identities, private coordinates, read IDs, alignments, or sequences.
- Do not propose launching production. This is a specification only.
- Use S1/S2/S3 labels only.

Current endpoint context:
- Omun means clean, deduplicated, two-sided autosomal OMEGA detector loci that are database-novel or known-rare below 0.001, normalized by D10 callable autosomal bases.
- 20 cultured public controls complete: four each AFR/AMR/EAS/EUR/SAS; 143-224 Omun per person; 53.6989-84.0128/Gb; total 3,751 Omun = 3,468 novel + 283 rare.
- S1: 155 Omun, 58.1879/Gb. S2: 3 Omun, 1.12603/Gb. S3: 1 Omun, 0.3754/Gb.
- S2/S3 low endpoints are exploratory and culture/platform confounded. No biological depletion or absence claim.

Existing sensitivity evidence:
- GIAB known-length panel: 32 real insertions, 8 each in length bands 300-499, 500-999, 1,000-4,999, >=5,000 bp. Result 0/32 exact, 30 unresolved, 2 false exact.
- Synthetic 100 bp spanning control reconstructs exactly.
- Corrected 5,000 bp positive control is unresolved despite six eligible alignments.
- Retained-assembly sensitivity: 3 accepted real loci plus 3 nearby shams gave 1/3 locus-window recovery, 1/3 expected terminal junction class, 0/3 exact coordinate plus both complete payload proxies, shams 0/3.
- Mapper diagnostic: two missed real controls contained exact source contigs and accepted two-anchor mappings, but fresh full-reference mapping extended into payload and reduced opposite overhang below unchanged 30 bp gate before parser candidate formation.
- Final two-anchor local refinement recovered 0/3 real, 0/3 exact, 0/3 shams.
- No retained contig bridged both 800 bp flanks.
- Right-anchor overhang is a detector feature, not insertion length.
- Technical read-support attrition is quality attrition, not truth validation.

Draft needed:
1. An executable calibration matrix across insertion sizes, repeat/mappability contexts, overhang structures, exact-junction truth, and shams.
2. Predefined outputs: sensitivity, specificity, false exact rate, locus-window recovery, terminal-junction class recovery, exact-junction recovery, complete-payload proxy recovery, mapper-boundary attrition, technical read-support attrition, callable-denominator checks.
3. Acceptance criteria sufficient to reopen biological interpretation, with fail-closed rules.
4. The smallest scientifically valid uncultured or blood-derived control comparison to distinguish culture/platform from participant biology using available or obtainable data.
5. Production needs routed to XG1 Variant Discovery Manager.

Keep concise and practical.
