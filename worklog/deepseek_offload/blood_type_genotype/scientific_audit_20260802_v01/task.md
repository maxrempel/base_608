Act as a critical genomics methods reviewer. Draft a concise, dated, deidentified PRELIMINARY scientific audit report in Markdown for an XG1 consumer-genotype blood-type project. Do not invent evidence. Use the facts below and explicitly distinguish tested, callable, inferred, and unresolved. Focus on method validity and the smallest useful next analysis.

Verified project evidence:
- 28 consumer genotype exports, 25 unique people, seven family groups. Five explicitly designated self-reported Starseed participants are the focal set. Relatives are not counted as additional focal observations.
- Focal callability:
  * focal 1, 23andMe: all 8 primary markers, all 4 tag markers, O1 deletion DI, predicted A1/O -> A, high research confidence.
  * focal 2, derived 23andMe CSV: 3/8 primary, 2/4 tag markers, unresolved.
  * focal 3, MyHeritage: 6/8 primary, 4/4 tags, O1 deletion absent, predicted A1/O -> A, moderate tag-based confidence.
  * focal 4, MyHeritage: 6/8 primary, 4/4 tags, O1 deletion absent, predicted O/O -> O, moderate tag-based confidence.
  * focal 5, 23andMe plus MyHeritage: 23andMe has 8/8 and 4/4, MyHeritage 6/8 and 4/4. Both tag sets predict A1/O -> A. The 23andMe O1 deletion is II, conflicting with the single O tag count, so this is low confidence. The duplicate array confirms tag reproducibility but not the causal deletion conflict.
- Broad focal ABO endpoint: 3 A, 1 O, 1 unresolved. Strict endpoint excluding low-confidence focal 5: 2 A, 1 O, one low-confidence excluded, one unresolved.
- No clinical ABO or RhD record was found for any focal participant. No red-cell antigen was measured.
- rs590787 exists in only two focal people; both are AG. It is ancestry-dependent proxy evidence only. None of the 28 arrays directly measures whole-RHD deletion, RHD copy number, weak D, partial D, RHD pseudogene, RHD-RHCE hybrid alleles, or comprehensive structural variation. Therefore RHD genotype and RhD positive/negative phenotype are unresolved for all five. Missing rs590787 must not become positive or negative.
- Primary marker build audit: all observed source coordinates match Ensembl GRCh37 exactly, with zero mismatches. Present/match counts: rs8176719 16/16 at chr9:136132909; rs8176746 25/25 at 9:136131322; rs41302905 28/28 at 9:136131316; rs687289 25/25 at 9:136137106; rs505922 25/25 at 9:136149229; rs507666 25/25 at 9:136149399; rs8176704 28/28 at 9:136135552; rs590787 13/13 at 1:25629943. Ensembl GRCh38 mappings are respectively 9:133257522, 9:133255935, 9:133255929, 9:133261703, 9:133273813, 9:133273983, 9:133260148, 1:25303452. All are plus-strand. Calls are keyed by rsID, so the GRCh37 source versus GRCh38 reference shift does not itself change extracted genotypes, but the prior audit documented only GRCh38 allele orientation and did not explicitly show source-coordinate build concordance.
- ABO method: four tag variants rs507666(A1), rs8176704(A2), rs8176746(B), rs687289(O). It counts unphased tag alleles and requires the counts to sum to two. rs8176719 O1 deletion and rs41302905 O2 are consistency checks when available. rs505922 is a fallback O proxy. The algorithm does not perform statistical phasing or full ABO haplotyping.
- Published context: the four-tag method has been used in phased/imputed cohorts. A 2024 systematic review/All of Us validation says phasing and imputation/haplotype structure are required for accurate ABO alleles; tag-SNP linkage varies by ancestry. O-tag median r2 with rs8176719 was about 0.443 in AFR, 0.869 in EUR, 0.946 in EAS; some tag methods mistyped up to 58% in particular settings. Therefore the current labels are research tag-derived predictions, not definitive ABO diplotypes or phenotypes.
- Allele gaps: rare ABO alleles, cis/trans ambiguity, recombinant alleles, weak A/B alleles, O alleles other than the explicitly checked O1/O2, Bombay/para-Bombay mechanisms, and structural alleles are not excluded. The inventory included some extra markers, but the endpoint classifier does not comprehensively genotype these states.
- Validation: all 155 testable parent-child marker transmissions were Mendelian-consistent. All 13 shared interpreted markers agreed between independent 23andMe/MyHeritage exports for three members of one family. These checks support file identity and marker reproducibility but do not validate phenotype accuracy or rare-allele completeness. Six classifier unit checks plus eight v02/v03 invariant tests passed. All completion marker output hashes and path-valued input hashes verified; two label-valued v01 input hashes separately matched the protected focal-call and marker-inventory files.
- Control: official 1000 Genomes Phase 3 Illumina Omni array reference, 1693 eligible controls. The exact same four-tag classifier resolved 1555 and left 138 unresolved (8.15%). Unresolved attrition by superpopulation: AFR 109/339=32.15%, AMR 13/268=4.85%, EAS 3/490=0.61%, EUR 13/493=2.64%, SAS 0/103=0%. 125/138 unresolved controls had all four tags but nonreconciling tag patterns. Thus apparent absence/callability is ancestry-dependent and the callable subset is selected.
- Control callable frequencies: ALL A 475/1555=30.547%, B 19.228%, AB 5.531%, O 44.695%. AFR callable n=230, AMR 255, EAS 487, EUR 480, SAS 103. Focal ancestry is not established and focal consumer arrays are not exact Omni platform matches.
- Quantitative result: broad A vs non-A 3/4 vs 475/1555, RR 2.4553, conditional OR 6.8119 with exact 95% CI 0.5454 to 358.4086, Fisher two-sided P=0.08851. Strict 2/3 vs 475/1555, RR 2.1825, OR 4.5424, exact CI 0.2359 to 268.5235, P=0.22365. Broad and strict O comparisons are nonsignificant. Across 24 unmatched exploratory rows, isolated nominal P<0.05 superpopulation rows are not claims and were not corrected for multiple testing.
- No Rh-negative or O-negative frequency analysis is possible from these arrays.

Required audit judgments:
1. Say the original pipeline is reproducible and appropriately fail-closed for missingness/RhD, but the phrase "validated four-tag classifier" overstates phenotype validation in this exact unphased, ancestry-unknown setting. Recommend "published four-tag research classifier" and treat diplotype labels as provisional allele-tag reconstructions.
2. Explain why source build and strand are technically coherent, but build concordance does not solve tag portability, phasing, or structural-allele limitations.
3. Explain how control attrition can create apparent absence or shift frequencies, particularly AFR attrition.
4. Distinguish family consistency from independent biological replication.
5. State safe conclusion: no stable ABO enrichment; central Rh-negative/O-negative folklore hypothesis was not tested.
6. Smallest useful next analysis requiring no new wet-lab spending: download the small phased 1000 Genomes sequence region spanning ABO, directly call functional ABO variants/haplotypes, and cross-tab the existing four-tag calls against direct phased sequence by superpopulation. Use this to derive ancestry-specific confusion matrices and probabilistic confidence for each focal tag pattern. This calibrates the existing classifier but still does not determine focal RhD or replace serology.
7. Parallel zero-cost evidence: solicit existing documented ABO/Rh results (blood donor card, medical portal, prenatal/surgical record), recording whether blood type was known before Starseed self-identification and prior exposure to Rh-negative/Starseed claims. Keep undocumented self-report separate.

Format:
- Title must begin PRELIMINARY and include date 2026-08-02.
- Begin with question, most important result, and plain-language conclusion.
- Include tables: evidence scope; five focal callability rows; control attrition; audit findings; smallest next analysis.
- Define ABO and RhD plainly.
- Avoid participant names and exact private identifiers. Codes Focal 1-5 are acceptable.
- No em dashes.
- Include references with URLs for four-tag paper PMC7669452, All of Us ancestry audit PMC11631141, Ensembl variation REST, 1000 Genomes Omni source, RHD biology NCBI Bookshelf NBK2269, RHtyper PMC7509869.
- Return only the complete Markdown report.
