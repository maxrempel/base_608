Draft a concise Markdown scientific report titled:
"PRELIMINARY blood-type genotype scientific audit, 2026-08-02".

Limit output to 7,000 characters. Do not include participant names or clinical claims. Use plain scientific language and compact tables.

Question: can current consumer genotype files test whether five self-reported Starseed focal participants have unusual ABO or RhD blood types?

Verified evidence:
- 28 genotype exports, 25 people, seven families; five designated focal participants.
- Focal ABO evidence:
  1) Focal 1, 23andMe: 8/8 primary markers, 4/4 tags, rs8176719 DI, provisional A1/O -> predicted A, high research confidence.
  2) Focal 2, derived 23andMe CSV: 3/8 primary, 2/4 tags, unresolved.
  3) Focal 3, MyHeritage: 6/8, 4/4 tags, rs8176719 absent from array, provisional A1/O -> predicted A, moderate tag-based confidence.
  4) Focal 4, MyHeritage: 6/8, 4/4 tags, rs8176719 absent, provisional O/O -> predicted O, moderate tag-based confidence.
  5) Focal 5, duplicate 23andMe+MyHeritage: tag pattern A1/O on both, but 23andMe rs8176719 II conflicts with the O tag; low confidence.
- Broad focal endpoint: 3 predicted A, 1 predicted O, 1 unresolved. Strict endpoint excluding focal 5: 2 A, 1 O, 1 excluded, 1 unresolved.
- No focal participant has a clinical ABO or Rh record in this project. Genotype prediction is not phenotype.
- RhD: rs590787 is present only for two focal participants, both AG, but this is an ancestry-dependent proxy. No file directly measures whole-RHD deletion, copy number, weak D, partial D, pseudogene, or RHD/RHCE hybrids. RhD is uncallable for all five. Missing rs590787 is missing, not positive/negative. O-negative/Rh-negative folklore was not tested.
- ABO method: four unphased tag SNPs (rs507666 A1, rs8176704 A2, rs8176746 B, rs687289 O), with rs8176719 O1 deletion and rs41302905 O2 as consistency checks, rs505922 fallback. This is a published research tag classifier, not phenotype validation. It does not phase haplotypes. Rare alleles, cis/trans ambiguity, recombinants, weak A/B, unusual O, Bombay/para-Bombay and structural alleles are not excluded.
- Build audit: all source coordinates match GRCh37 exactly. Marker/match counts: rs8176719 16/16; rs8176746 25/25; rs41302905 28/28; rs687289 25/25; rs505922 25/25; rs507666 25/25; rs8176704 28/28; rs590787 13/13. GRCh37 coordinates respectively: 9:136132909, 9:136131322, 9:136131316, 9:136137106, 9:136149229, 9:136149399, 9:136135552, 1:25629943. GRCh38: 9:133257522, 9:133255935, 9:133255929, 9:133261703, 9:133273813, 9:133273983, 9:133260148, 1:25303452. All plus strand. Extraction was by rsID, so build shift did not alter calls.
- Family/platform checks: 155/155 testable parent-child transmissions Mendelian consistent; 13/13 shared interpreted markers concordant across 23andMe/MyHeritage. These support file identity/reproducibility, not phenotype validation.
- Same-classifier 1000 Genomes Omni control: 1693 eligible, 1555 callable, 138 unresolved (8.15%). Unresolved by superpopulation: AFR 109/339 (32.15%), AMR 13/268 (4.85%), EAS 3/490 (0.61%), EUR 13/493 (2.64%), SAS 0/103. 125/138 unresolved had all four tags but nonreconciling patterns. Callable overall: A 475/1555, B 299, AB 86, O 695. Focal ancestry unknown and consumer platforms are not Omni-matched. Callable subset is selected, especially in AFR.
- Broad A-vs-non-A: 3/4 vs 475/1555, RR 2.4553, conditional OR 6.8119, exact 95% CI 0.5454-358.4086, Fisher two-sided p=.08851.
- Strict A-vs-non-A: 2/3 vs 475/1555, RR 2.1825, OR 4.5424, CI .2359-268.5235, p=.22365. O comparisons nonsignificant. No multiple-testing correction across 24 exploratory rows; no stable enrichment claim.
- Published 2024 ancestry audit reports phased/haplotype data are required for accurate ABO alleles and tag portability differs by ancestry; O-tag versus rs8176719 median r2 AFR .443, EUR .869, EAS .946, and some tag methods mistyped up to 58%.
- Tests: six classifier checks and eight invariant tests passed. Completion artifact hashes were verified.

Required structure:
1. Opening TLDR stating ABO partially callable, no stable enrichment, RhD uncallable.
2. What was tested.
3. Table of five focal callability/inferences.
4. Table covering build, phase, structural alleles, phenotype ambiguity, control attrition.
5. Control/effect-size table.
6. Exact safe conclusion, distinguishing absence of evidence, method limitation, and unresolved question.
7. Smallest useful zero-cost next analysis: use phased 1000 Genomes sequence around ABO to calibrate this four-tag classifier by superpopulation and produce confusion matrices/probabilistic confidence for focal tag patterns. In parallel solicit already-existing documented ABO/Rh records and record whether blood type and folklore exposure predated Starseed self-identification. Do not recommend buying whole genomes solely for blood type.

Use these references as clickable links: https://pmc.ncbi.nlm.nih.gov/articles/PMC7669452/ ; https://pmc.ncbi.nlm.nih.gov/articles/PMC11631141/ ; https://www.ncbi.nlm.nih.gov/books/NBK2269/ ; https://pmc.ncbi.nlm.nih.gov/articles/PMC7509869/
