## Completion Audit & Prioritized Next Actions

### 1. Completeness Decision

The requested “thorough blood type classification for all genotyped Starseeds” is **complete to the limit of the available consumer-genotype data** for the four individuals with resolved ABO calls. For the fifth Starseed, ABO remains unresolved. RhD classification is incomplete for three of five individuals because no proxy SNP (rs590787) is available; for the two with proxy, the result is non‑diagnostic (ancestry‑dependent, not clinical). Extended blood‑group markers are reported where directly assayed. The classification cannot be made more thorough without additional samples, clinical serology, or orthogonal molecular methods (e.g., RHD deletion typing).

### 2. Missing Deterministic Validation (Performable Now)

- **Strand/orientation check** for every blood‑group SNP used (rs507666, rs8176704, rs8176746, rs687289, rs8176719, rs41302905, rs590787) against the reference genome (GRCh38). Consumer arrays may report on either strand; verify all genotypes are in the same orientation and forward‑strand convention.
- **Mendelian consistency scan** on all 28 samples across every called blood‑group variant (not only the 155 transmissions already reconciled). Confirm zero errors in the remaining untested parent‑child pairs (e.g., for the focal Starseed without ABO, check if any informative transmission can infer missing call).
- **Deterministic classifier re‑run** using the verified strand‑corrected genotype table to ensure all six tests still pass.
- **Duplicate consistency** for the 23andMe/MyHeritage trio: confirm that all 13 shared markers are in the same genomic build and strand orientation; if not, resolve.

### 3. Overclaim, Risks, and Issues

- **RhD risk**: The proxy rs590787 is a non‑coding SNP with variable linkage to the *RHD* deletion across populations. Its positive predictive value for RhD‑positive is high only in European ancestry; in other ancestries it can produce false positives/negatives. The current description (“ancestry‑dependent proxy evidence”) is correct but must be reiterated for every focal report. **No clinical RhD call should be made.**
- **ABO risk**: The fifth Starseed has unresolved ABO. If any family member has a known ABO (from other data), the inheritance pattern could infer the missing call, but the Notion audit found no usable clinical values. Do not impute.
- **Extended marker limitations**: Kell, Duffy, MNS, etc., are reported only for directly assayed variants. Rare alleles (e.g., Kp(a/b), Fy(x), MNS hybrid GP.Mur) may be missed. System coverage should be explicitly documented as partial.
- **Family‑inheritance**: The reconciled 155 transmissions do not guarantee no error in the untested pairs. A single Mendelian inconsistency would invalidate calls for that marker.
- **No ancestry or identity information is used or invented** – this is correct and must be maintained.

### 4. Must‑Do vs. Optional Future

**Must‑do (immediate, from existing data)**:
- Complete strand/orientation audit for all blood‑group SNPs.
- Extend Mendelian consistency check to all untested parent‑child pairs.
- Re‑run deterministic classifiers after strand/orientation correction.
- Document that the fifth Starseed’s ABO is unresolved and that RhD interpretations are proxy‑only.

**Optional future (requires new samples or clinical data)**:
- Obtain serological ABO/RhD typing for all five Starseeds.
- Perform RHD deletion‑specific genotyping (e.g., PCR or WGS) for definitive RhD.
- Sequence full coding regions for extended systems to detect rare alleles.
- Expand sample set to fill missing parental genotypes for inference.

### 5. Short Acceptance Checklist

- [ ] All blood‑group SNPs verified on forward strand (GRCh38).
- [ ] All parent‑child Mendelian transmissions consistent (no errors).
- [ ] Deterministic classifier tests pass after strand correction.
- [ ] Duplicate sample agreement confirmed with same build/orientation.
- [ ] ABO called for 4/5 Starseeds; fifth explicitly marked unresolved.
- [ ] RhD proxy calls (rs590787) provided only with ancestry‑dependency disclaimer.
- [ ] Extended markers reported only where directly assayed, with coverage limitations noted.
- [ ] No clinical ABO or RhD values used from participant profiles.
- [ ] No participant‑level results or identities included in deliverables.
