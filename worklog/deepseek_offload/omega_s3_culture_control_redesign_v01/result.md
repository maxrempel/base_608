1. **Reframing the present result**  
   The observed difference in Omun frequency between S3 and the balanced cultured cohort cannot be attributed to biology because culture status and sequencing platform are unresolved confounders. The comparison is a technical contrast, not a biological test.

2. **Culture as primary confounder – mechanisms**  
   - Clonal expansion or rearrangement in cell lines can create *de novo* structural variants or mobile-element insertions.  
   - Loss of heterozygosity or artefactual homozygosity alters apparent allele frequencies.  
   - DNA degradation, library preparation biases, and platform-specific error profiles (e.g., read length, GC bias) affect insertion detection.  
   - Bioinformatic mapping artefacts (e.g., overhang handling, anchor uncertainty) may differ between cultured and blood-derived DNA.  
   - Technical missingness patterns differ, especially at repetitive regions flanking Omun.

3. **Preservation of cultured cohort**  
   The balanced-20 cultured set is retained only as a technical reference for platform-specific artefact rates and as a sensitivity analysis for stability of Omun calls under different bioinformatic filters. It is not a valid comparator for biological inference.

4. **Minimum defensible control set**  
   - 20 unrelated, blood-derived or uncultured controls.  
   - Matched to S3 on: ancestry (genetic or self-reported), sex, sequencing platform (same technology, read length, coverage target ≥30x), and callable opportunity (same genomic regions, comparable median depth ±20%).  
   - Staged: Phase 1 – 5 such controls for initial comparison; Phase 2 – full 20.

5. **Staged design, rules, and tests**  
   - *Inclusion*: unrelated, blood/uncultured, matched ancestry/sex/platform/coverage, callable fraction >0.90.  
   - *Exclusion*: any cultured sample, low coverage (<20x), high missingness, ancestry mismatch.  
   - *Denominators*: total callable autosomal base pairs; Omun count per genome; Omun rate per Mbp.  
   - *Validation gates*: all candidate Omun in S3 or controls must be confirmed by orthogonal long-read or PCR.  
   - *Falsification tests*: (a) Compare Omun rate between cultured and uncultured controls – if significant, culture effect is demonstrated; (b) re-analyse S3 with the same bioinformatic pipeline as controls; (c) test for systematic differences in read-anchor overhang patterns.

6. **Conclusions before new controls**  
   Can conclude:  
   - A technical contrast exists between S3 and cultured references.  
   - No conclusion about Starseed biological status, enrichment, or depletion is warranted.  
   Cannot conclude:  
   - Any Omun frequency difference is biological or related to Starseed status.  
   - The current cohort provides evidence for or against any hypothesis about S3.

7. **Replacement language**  
   In reports: *“The Omun frequency in S3 (X per genome) differs from the cultured reference set (Y per genome). However, culture status and sequencing platform are primary confounders. This comparison is a technical observation and does not support biological inference about Starseed status.”*  
   In tables: **S3**: X; **Cultured controls (technical reference only)**: Y; **Note**: comparison confounded by culture – no biological conclusion.

8. **Acquisition routes (category level)**  
   - Existing biobanks with blood-derived whole-genome data (e.g., public datasets).  
   - Volunteer recruitment from populations matching S3’s ancestry/sex.  
   - Collaboration with sequencing projects that have uncultured controls from similar ancestry backgrounds.  
   - Do not assume availability or consent; these are potential avenues only.
