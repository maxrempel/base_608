# Task: scientific critique of genotype-derived blood-group classification

Act as a skeptical blood-group genetics reviewer. Review the deidentified
method and result below. Identify incorrect allele mappings, strand mistakes,
overconfident calls, missing validation, inheritance logic weaknesses, and
wording that could be mistaken for clinical typing. Return a compact prioritized
list: critical corrections, useful improvements, and safe interpretation.

## Input scope

- 28 consumer genotype exports representing 25 people in 7 families.
- Five people are documented designated self-reported Starseed participants.
- Two additional families have no proven designated-participant identity and
  are excluded from the Starseed-only count.
- One family has duplicate 23andMe and MyHeritage exports.
- Private identities and raw genotypes are intentionally omitted here.

## ABO method

The caller uses a four-tag allele-count panel:

- rs507666 A = A1 allele
- rs8176704 A = A2 allele
- rs8176746 T = B allele
- rs687289 G = O allele; rs505922 T is a fallback O proxy

The four allele counts must all be present and sum to exactly two. The common
O1 deletion rs8176719 is then used as a consistency check: D is counted as O1.
rs41302905 T can explain an observed non-O1 O allele. Incomplete or
non-reconciling panels are unresolved. A causal/tag conflict is retained but
downgraded to low confidence.

## Other systems

- RhD: rs590787, normalized to plus-strand A/G; GG is called
  RhD-negative proxy and AG/AA RhD-positive proxy. It is explicitly described
  as proxy-only because RHD deletion/copy number and variant alleles are not
  directly measured and accuracy is ancestry dependent.
- Kell K/k: rs8176058 A=K, G=k.
- Kell Kp(a/b): rs8176059 A=Kp(a), G=Kp(b).
- Kidd: rs1058396 G=Jk(a), A=Jk(b).
- Duffy: rs12075 G=Fy(a), A=Fy(b); rs2814778 C is the erythroid-null
  promoter allele. Homozygous rs12075 AA plus rs2814778 CC is called predicted
  Fy(a)-/Fy(b)-; heterozygous null promoter is left phase-unresolved.
- MNS S/s: rs7683365 plus-strand A=S, G=s.
- RHCE E/e: rs609320 plus-strand G=E, C=e.
- Diego: rs2285644 plus-strand A=Di(a), G=Di(b).
- Lutheran: rs28399653 A=Lu(a), G=Lu(b).
- FUT2: rs601338 A/A predicted nonsecretor, A/G or G/G predicted secretor.

Consumer genotypes are normalized to an expected plus-strand allele alphabet.
They are complemented only when the observed allele alphabet cannot be valid
for that marker.

## Validation

- ABO parent-child transmission is checked wherever both parents and child
  resolve.
- All testable transmissions reconcile; one trio is not testable because ABO
  is unresolved.
- Duplicate-platform people agree on shared interpreted blood-group systems.
- Missing calls remain unresolved rather than imputed.

## Deidentified Starseed-only result

- Five designated participants.
- ABO resolved in four: A=3, O=1, B=0, AB=0; fifth unresolved.
- Of the four ABO calls: one is high research confidence, two moderate tag
  panel calls, and one low-confidence A call due to tag/O1-deletion discordance.
- RhD proxy available for two, both positive; three unresolved.
- Therefore the small incomplete dataset does not support an O-negative
  enrichment hypothesis. It also cannot estimate prevalence precisely.

These are research predictions only, not clinical or transfusion-safe types.
