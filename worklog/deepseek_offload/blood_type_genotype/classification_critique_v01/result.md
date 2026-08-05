### Critical Corrections

1. **MNS S/s mapping is fundamentally wrong** – rs7683365 is a C/T SNP (plus strand), not A/G. Mapping A=S and G=s is incorrect and will systematically misclassify S/s phenotype. This must be corrected to C=S, T=s (or the reverse if strand complementation is intended). Without this fix, all MNS results are unreliable.

2. **RhD proxy mapping may be inverted or uninterpretable** – rs590787 is used as a biallelic SNP (GG = RhD-negative, AG/AA = positive), but the common RHD deletion produces a null allele, not a G. In homozygous deletion, the SNP probe would fail (no call), not produce GG. The mapping assumes G is the deletion-linked allele, but this is not standard and may lead to false negatives/positives. The ancestry-dependent warning is insufficient without clarifying the actual array behavior.

3. **ABO fallback O proxy (rs
