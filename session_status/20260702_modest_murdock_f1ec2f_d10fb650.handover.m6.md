# Scribe handover - milestone 6 (~454K tokens)
# session: 20260702_modest_murdock_f1ec2f_d10fb650
# cwd: C:\claude_base\.claude\worktrees\modest-murdock-f1ec2f
# written: 2026-07-02 15:56:59 by deepseek-v4-pro

## Handover: Kristen Kenefick genome analysis (microchimerism + anomaly hunt)

---

### Goal (in Max's words)

Investigate Kristen's five genomic anomaly claims (multiple X, sex chimerism, homozygosity, missing-parent, extra/missing gene copies) using her full 30? whole-genome sequencing data, and determine whether the trace of male DNA in her saliva sample is a son's fetal microchimerism or something else. The overarching remit: "looking for traces of alien manipulation, but not at the expense of truth."

---

### Decisions + Why

1. **Raw reads (FASTQ/BAM) are the whole point.** Max clarified mid?session that processed VCFs are structurally blind to alien insertions, so the analysis must run on the aligned BAM and the raw FASTQ - not on the small variant calls. All claims were re?assessed directly from the reads.

2. **Compute on asto, not Pine.** A Liz?owned guest Linux box (astolfodebian) with 16 cores, 31?GB RAM, 982?GB free was used for all heavy computation. Kristen's 34?GB BAM and VCFs were transferred Centauri?asto over Tailscale. samtools/bcftools/mosdepth installed inside a distrobox (`ubuntu` container). CPU capped to ~50% (8 of 16 cores).

3. **Microchimerism number corrected from 5?9% to ~0.3%.** The earlier letter to Kristen (Anna?voice, sent from anna@maxrempel.com) estimated 5?9% male cells. The proper analysis showed this was inflated by three stacked errors:
   - Averaging only the *covered* spots of single?copy Y genes, ignoring the mostly?empty gene bodies.
   - X?gametolog cross?mapping onto the Y genes in a female background.
   - Kristen's own FAIL?filtered heterozygous sites leaking into the autosomal Oliver?specific test.
   The clean marker is SRY (single?copy, no X counterpart): 0.04? vs autosome ~30? ? f ? 0.3%. Genome?wide autosomal aggregate (C3) gave 0.26% allele fraction ? f ? 0.38%, uniform across all autosomes.

4. **Unmapped reads = oral microbiome.** Kraken2 with the PlusPFP database classified Kristen's 8.5?M unmapped reads: 45% ordinary mouth bacteria (*Streptococcus mitis* etc.), 54% unclassified (reference?gaps + unknown microbes). No anomaly.

5. **Which son? Cannot be pinned with this data.** The Y chromosome proves the source is a male child of the ex?husband's paternal line (Y?haplotype matches Oliver at 98.7%), but all full brothers share an identical Y. Autosomes could distinguish *Oliver specifically* via rare/private alleles - the full?power C4 test (running) addresses that. However, at a ~0.3% fraction the precision is marginal, and truly *de?novo* alleles need her parents. The defensible conclusion is "one or more of her sons by Oliver's father."

6. **Coordination with X7A.** Max instructed: "talk to X7A." X7A assigned the microchimerism analysis task, and later an "email?02" spec (amateur?friendly, term?to?plain?English, exclusion?step table). X5 ran the analysis and will deliver the email draft to X7A for review - both chats use the `bcast` team board `x`.

---

### Current state

**Downloads**
- **Kristen:** complete - 2 FASTQ (~27?GB each), 34?GB BAM, all VCFs, two chip files. BAM + VCFs are on asto; FASTQs on Centauri.
- **Oliver:** his 2 FASTQ (~44?GB each) were downloading to Centauri via Windows task scheduler. Last known: file1 41%, file2 27%, ~16h ETA (should finish mid?day today). His snp?indel VCF (194?MB) and chip file are on Centauri and asto. He has **no BAM**.
- **Twins:** chip files only (AncestryDNA). Whole?genome dropped (no funding).

**Analysis complete (court?grade, all on asto)**
- **Ploidy / X chromosome:** two X (X mean depth 39.99?, ratio 0.98 vs autosome; heterozygous).
- **Y / chimerism:** no male Y above a ~2% floor. Y coverage 4.63% (PAR?only); SRY depth ~0.04? ? male fraction ~0.3%.
- **Homozygosity / runs of homozygosity:** 2.67?M het SNPs, het/hom ratio 1.77; essentially zero ROH ?3?Mb. Inbreeding coefficient 0.0017 ? two unrelated parents.
- **CNV:** 64 gains, 69 losses (confident Canvas calls) - ordinary burden.
- **Unmapped/non?human reads:** oral bacteria (kraken2), no anomaly.
- **Microchimerism (fraction + specificity):** 
  - Single?copy Y genes (MAPQ?30): ~0.1?0.3%
  - Autosomal aggregate (C3, 288k sites, genome?wide, per?chromosome uniform): cleaned VAF 0.264%, CI 0.261?0.267% ? f ? 0.38%
  - **Full?power C4 is still running on asto** (all ~809k Oliver?het / Kristen?homref autosomal sites, gnomAD allele?frequency?stratified, Mike unrelated control). It will give the definitive verdict on Oliver?specificity.

**Reports committed + pushed**
- `kristen_claims_report_v01_tomemex.md` (all 5 claims)
- `kristen_microchimerism_report_v01_tomemex.md` (microchimerism, exclusion matrix, C3 + C4 placeholder)
- all scripts and raw output under `projects/XG1/kenefick/` inside the `C:\claude_base` repo.

**Letter to Kristen**
- A **draft correction letter** exists: `kristen_correction_email_DRAFT_v01.md` (Anna voice, corrects the 5?9% to ~0.3%, explains oral bacteria, notes trio need). **Not yet sent.**
- X7A asked for a separate **email?02** (amateur?friendly, counts, exclusion table). X5 ack'd and will write it after C4 lands.

---

### Exact next step

1. **Collect C4 result from asto** ? lock the final microchimerism number.
2. **Write the full amateur?friendly email?02** per X7A's spec (include plain?English definitions, counts, logical steps, exclusion table, honest "which son" limit).
3. **Save email?02 as draft** under `letters/` in the canonical project tree. **Do NOT send.** Hand it to X7A via bcast and wake X7A.
4. **Report the final number to Max** and present the email draft for his review. (The simpler Anna?style correction draft is also available for his choice.)
5. If Oliver's downloads have finished, check them and plan his analysis - but Kristen's deliverable is the priority.

---

### Open questions (for Max)

- Which email draft does Max actually want sent? The existing Anna correction (simple, one?paragraph) or the fuller amateur?friendly version X7A specified? (Show both when ready.)
- Does Max want the microchimerism fraction stated as ~0.3% (anchor on SRY) or the autosomal aggregate 0.38%? (Both are consistent; SRY is cleaner.)
- Oliver's FASTQ downloads - have they finished? If not, does Max want a follow?up to re?check or wait?
- Any further analysis of Oliver's data beyond the microchimerism context? (e.g., testing his own ploidy, homozygosity, etc.)

---

### Key paths + IDs

| What | Path / ID |
|---|---|
| Project root (canonical) | `C:\claude_base\projects\XG1\kenefick\` |
| Court?grade microchimerism report | `.../kristen_microchimerism_report_v01_tomemex.md` |
| Broad claims report | `.../kristen_claims_report_v01_tomemex.md` |
| Current correction email draft | `.../kristen_correction_email_DRAFT_v01.md` |
| C4 full?power script | `.../scripts/kristen_microchimerism_courtgrade_v04.py` |
| C4 output (on asto when done) | `/home/rempel/genomics/_analysis/kristen_microchimerism_courtgrade_v04.txt` |
|
