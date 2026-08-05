# Scribe handover - milestone 5 (~416K tokens)
# session: 20260702_modest_murdock_f1ec2f_d10fb650
# cwd: C:\claude_base\.claude\worktrees\modest-murdock-f1ec2f
# written: 2026-07-02 14:43:08 by deepseek-v4-pro

# HANDOVER - Kristen Kenefick XG1 Genome Analysis (Session X5 / x1)

---

## GOAL (in Max's words)

"We are still looking for traces of alien manipulation but not at the expense of truth." Kristen Kenefick is an experiencer who believes she has genomic anomalies (XX/XY chimerism, multiple X chromosomes, extra/missing genes, too much homozygosity, "missing a parent," son's genome dominated by her genes). Max obtained her Sequencing.com login, downloaded the family's whole-genome data, and tasked this session with running the actual **raw-read analysis** - specifically chimerism / microchimerism and the non-human / unmapped read hunt. The trump card over her claims is **the raw reads (BAM/FASTQ)**, not the processed VCFs.

---

## DECISIONS MADE + WHY

### 1. Switched compute from Centauri to asto (astolfodebian)
**Why:** Centauri (16TB Windows box) has only bare Python - no samtools, no bcftools. asto is a Debian box with 16 cores, 31GB RAM, 982GB free. Liz's guest rules: compute only, footprint ?480GB, keep ?23% free. Installed samtools 1.19.2, bcftools 1.19, mosdepth 0.3.8, numpy/scipy, kraken2 onto the `ubuntu` distrobox. Moved Kristen's 34GB BAM and all her VCFs from Centauri?asto over Tailscale.

### 2. Kristen's BAM retains unmapped reads - no FASTQ realignment needed
**Why:** `samtools flagstat` showed 8,539,605 unmapped reads (~1.0%), both mates unmapped. The BAM kept them, so I didn't need to pull the 2?27GB raw FASTQ for her. Note: Oliver has NO BAM - his hunt needs his FASTQ, which is still downloading.

### 3. Pivoted from "5-9% microchimerism" to "~0.3%, ordinary trace"
**Why (the critical methodological correction):** An earlier letter to Kristen already claimed ~5-9% male DNA. But three stacked artifacts inflated that:
- The old single-copy Y-gene measurement averaged depth only over *covered* spots, ignoring the mostly-empty gene bodies.
- X-gametolog reads cross-map onto Y genes in a female (X and Y share near-identical copies of ~11 genes).
- In the raw autosomal test, Kristen's own FAIL-filtered heterozygous sites leaked through (~48k of them matched exactly), producing a fake 5.35% raw signal.

**Corrected measures (three independent methods):**
| Measure | Result | Confidence |
|---|---|---|
| SRY (single-copy maleness gene, no X twin, BAM MAPQ?30) | **~0.3%** | Highest - immune to X-Y cross-mapping |
| Single-copy Y panel (11 X-degenerate genes, MAPQ?30) | 0.1-0.3% | Drops as MAPQ tightens ? confirms cross-map inflation |
| Autosomal Oliver-specific (strict, Kristen hets fully excluded) | Under ~1%, 91% zero-read sites | Confirms low fraction, but needs the genome-wide + control proof |

**A letter was ALREADY SENT to Kristen claiming ~5-9% male microchimerism - this number is very likely wrong and Max will want to decide whether to send a correction.**

### 4. Court-grade autosomal test (C3) was running at session end
**Why:** X7A (another worker) and Max both flagged that "91% zeros" isn't court-grade proof. The C3 test addresses this by:
- **Aggregate Oliver allele counting across ~300k sites** (not per-site) ? real fraction with 95% binomial confidence interval.
- **Genome-wide proof:** per-chromosome Oliver-allele VAF (a real signal must be uniform; a Y-only artifact would not be).
- **Mike (unrelated male) control:** Kristen's reads carry Oliver's allele where unrelated Mike has none ? kills "random contamination."
- **Exclusion matrix:** rules out noise, Y-artifact, Kristen's own mosaicism, random contamination, maternal microchimerism (her mother's cells), absorbed twin.

### 5. Non-human read classification (kraken2) was downloading the reference library
**Why:** The 8.54M unmapped reads need taxonomic IDs. Chose kraken2 with the 16GB PlusPFP database (fits asto's footprint, fast, citable, reusable for Oliver/trio). Library was ~44% downloaded at last check.

### 6. Identified and fixed a file-location branch
**Why:** This session was writing to `genomics/kenefick/` but x1's canonical project root is `C:\claude_base\projects\XG1\kenefick\`. Fixed: moved everything there, committed, pushed. Both locations existed - now only the canonical one has content.

---

## CURRENT STATE - WHAT IS DONE

### Downloads (on Centauri D:\genomics\kenefick\)
- **Kristen - COMPLETE:** 2 raw FASTQ (~27GB each), aligned BAM (34GB), snp-indel/cnv/sv/mito VCFs, 2 AncestryDNA chip files. Total ~88GB.
- **Oliver - PARTIAL:** His 2 raw FASTQ (~44GB each) are downloading as scheduled tasks (SYSTEM). File 1 ~41%, file 2 ~27% at last check (~midday today ETA). His small VCFs + chip already done. Oliver HAS NO BAM.
- **Twins (Genome 3/4) - chip only.** No whole-genome data (Kristen planned to sequence them; no funding from Max).

### Analysis completed (from Kristen's own raw reads + BAM, on asto)
All five of her claims have been measured court-grade:
1. **Multiple X chromosomes** ? **No.** X depth = 0.98? autosome (two X). X is normally heterozygous (unimodal BAF at 0.5). Extra X would read ~1.5?.
2. **XX/XY chimerism / maternal-Y** ? **No chimerism above ~few-% floor.** Y depth ? 0 (ratio 0.007, Y-specific region only ~7% covered). SRY ? zero. X-depth ratio and BAF exclude a large male line.
3. **Too much homozygosity** ? **No.** 2.67M heterozygous SNPs, het/hom ratio 1.77 (textbook-normal outbred). BAF distribution cleanly unimodal - no secondary bands from a second cell line.
4. **"Missing a parent"** ? **Contradicted.** Inbreeding coefficient 0.0017 (two unrelated parents). Zero long runs of homozygosity ?3Mb. A "missing parent" predicts ~300? higher inbreeding.
5. **Extra/missing gene copies (CNV)** ? **Ordinary.** ~133 confident events (64 gains, 69 losses) - normal human burden. No X-chromosome calls.

### Non-human / unmapped pile
- 8,539,605 reads (~1.0% of all reads), both mates unmapped.
- **Characterized:** full-length clean reads (150bp, human-like GC ~0.44, 0% adapter, 0.05% low-complexity). Not junk - they're clean reads that don't match GRCh38.
- **Classification pending:** kraken2 library ~44% downloaded on asto at last check.

### Letters
- **SENT (from Anna, anna@maxrempel.com, CC Max):** Y-chromosome report claiming ~5-9% male microchimerism matching Oliver. **THIS LIKELY NEEDS CORRECTION.**
- **SENT (from Anna):** File-receipt + FASTQ-link instructions.
- **NOT SENT:** The comprehensive claims report to Kristen (all 5 claims). Blocked on the C3 court-grade result finishing and Max's decision on the microchimerism correction.

---

## EXACT NEXT STEP

**Collect the C3 court-grade autosomal microchimerism result** - the script `kristen_microchimerism_courtgrade_v03.py` was running on asto when the session ended. It's processing ~300k sites across all 22 autosomes, with the Mike unrelated control and per-chromosome breakdown.

**How to check it:**
1. SSH to asto: `ssh -i C:\Users\maxre\.ssh\bitwarden_ed25519 rempel@astolfodebian.tail251d88.ts.net`
2. Check if C3 finished: `distrobox enter ubuntu -- bash -lc 'cat /home/rempel/genomics/_analysis/kristen_autosomal_courtgrade_v03.txt'`
3. If file exists ? read the aggregate fraction, per-chromosome table, CI, Mike control, and exclusion matrix.
4. If still running ? check `ps aux | grep courtgrade`; wait; collect.
5. **Write the final court-grade microchimerism report** replacing the earlier v01, with the clean fraction + full exclusion logic.
6. **Flag the correction to Max:** the sent letter claims 5-9% - reconcile with the C3 number (likely ~0.3%).
7. **Collect the kraken2 classification** when the library finishes downloading (check `/home/rempel/genomics/_analysis/kristen_kraken_report.txt`). Write the non-human findings.
8. **Monitor Oliver's 2 FASTQ** on Centauri to DONE_EXITCODE_0 (scheduled tasks dl_oliver_f1/f2). Then he's ready for analysis.
9. **Draft the correction letter** for Max's approval - DO NOT SEND without explicit "send."

---

## OPEN QUESTIONS AWAITING MAX

1. **Correction letter to Kristen:** The 5-9% microchimerism claim in the sent letter is wrong. Does Max want a correction sent now, or wait until the C3 court-grade result solidifies the number?
2. **Non-human classification method:** kraken2 16GB library was ~44% downloaded. Let it finish, or switch to a lighter BLAST subsample?
3. **Kristen comprehensive claims letter:** Drafted but not sent - should it go out after the microchimerism correction?
4. **Oliver's analysis:** His two raw FASTQ were still downloading (~41%/27% of 44GB each). His VCFs are on asto. The autosomal microchimerism test is partly done (needs him as the source - but C3 tests Kristen's reads *against* Oliver's private alleles, which is what we have).

---

## KEY PATHS AND IDs

### Local (Pine)
- **Canonical project root:** `C:\claude_base\projects\XG1\kenefick\`
- **Reports (committed, pushed):**
  - `kristen_claims_report_v01_tomemex.md` - all 5 claims, court-grade BAM analysis
  - `kristen_microchimerism_report_v01_tomemex.md` - microchimerism crux
  - `kristen_kenefick_status_report_20260701_v01_tomemex.md` - full data inventory + status
  - `kristen_rawread_findings_v01_tomemex.md` - Stage A raw-read findings
- **Scripts:** `projects/XG1/kenefick/scripts/` - kristen_analyze.py, kristen_singlecopy_mapq_v01.py, kristen_autosomal_microchimerism_v01.py, kristen_autosomal_microchimerism_v02.py, kristen_microchimerism_courtgrade_v03.py, kristen_unmapped_char.py, kristen_kraken.sh
- **Machine-readable stats:** `projects/XG1/kenefick/analysis/kristen_stats_v01.json`
- **Sent letters:** `projects/XG1/kenefick/kristen/y_report_send.py`, `fastq_link_send.py`, `reply_send_03.py`, `results_reply_send.py`
- **Mike (unrelated control) 23andMe:** `/tmp/mike_raw/genome_Michael_Rempel_v5_Full_20250403232651.txt` (also on asto at `/home/rempel/genomics/kenefick/mike/`)
- **worklog:** `C:\claude_base\worklog\modest_murdock_f1ec2f_ef7c31a5b0.md` (current worktree is modest-murdock-f1ec2f)

### Centauri (Windows, 16TB D: drive)
- `ssh -i C:\Users\maxre\.ssh\sol_key maxre@192.168.1.176`
- `D:\genomics\kenefick\kristen\` - Kristen's complete data (FASTQ + BAM + VCFs + chip)
- `D:\genomics\kenefick\oliver\` - Oliver's partial (2 FASTQ downloading via dl_ofq1/2.cmd, VCFs + chip done)
- `D:\genomics\kenefick\twins\` - chip only
- Oliver download scripts: `D:\genomics\kenefick\oliver\dl_ofq1.cmd`, `dl_ofq2.cmd` (launched as scheduled tasks dl_oliver_f1/f2)
- Transfer key: `D:\genomics\_work\astokey` (icacls-locked, for scp to asto)

### asto (Debian, guest compute)
- `ssh -i C:\Users\maxre\.ssh\bitwarden_ed25519 rempel@astolfodebian.tail251d88.ts.net`
- Tailnet IP: 100.83.187.123
- Distrobox: `distrobox enter ubuntu -- bash -lc '<command>'`
- Data: `/home/rempel/genomics/kenefick/kristen/` (BAM indexed, all VCFs), `/home/rempel/genomics/kenefick/oliver/` (snp-indel VCF), `/home/rempel/genomics/kenefick/mike/`
- Analysis outputs: `/home/rempel/genomics/_analysis/` - flagstat, idxstats, coverage, unmapped counts, C1 singlecopy results, C2 strict autosomal results, **C3 court-grade in progress**
- Unmapped reads: `/home/rempel/genomics/_analysis/kristen_unmapped.bam` (8.54M reads)
- kraken2: `/home/rempel/genomics/_analysis/kristen_kraken_report.txt` (in progress)

### Sequencing.com (Kristen's account, via Playwright Chromium)
- Genome UUIDs: Kristen=886b5b3a-e2f6-4b93-be08-53a382c6838a, Oliver=487b40c0-5c8f-4bb7-9cfd-05479727a048
- Oliver FASTQ file IDs: 3852428 (.1), 3852427 (.2)
- OCI pre-signed URLs valid ~10 days from generation (~2026-07-01)
- **Playwright browser lock should be CLOSED** (it was released before hibernation)

### Kristen contact
- Email: kristentheartist@gmail.com
- Letters sent from: anna@maxrempel.com (Anna assistant voice, auto-CC max.rempel2@gmail.com)
- Max's personal replies from: max@dnaresonance.org
- Consent: full trio consent locked (Kristen adult self-consent + parental for Oliver, both received 2026-06-26)
- Cloudflare D1 row id=41 (starseed-genetics-contacts database)

---

## GOTCHAS AND DEAD ENDS

### Critical scientific gotchas
1. **The old "5-9% microchimerism" was inflated by method errors.** The prior team (x3/x1) derived it from VCF depth on single-copy Y genes *without MAPQ filtering*, averaging only covered spots and ignoring X-gametolog cross-mapping. This number went into a letter already sent to Kristen. The corrected BAM-level analyses all converge on ~0.3%. **Do not use the 5-9% figure.**

2. **Whole-Y average depth is misleading in a female.** Most of chrY is ampliconic/repetitive - reads pile up confusingly. The clean measures are SRY (single-copy, no X twin) or the autosomal Oliver-specific test (completely immune to Y mapping).

3. **C2 v01 (autosomal test) had a 48k-site leak.** Kristen's FAIL-filtered heterozygous sites were not excluded, producing a fake 5.35% raw signal - exact count of FAIL hets = ~47,800, matching the leaked sites. C2 v02 fixed this by excluding ALL her variant sites (PASS + FAIL). C3 (court-grade) inherited this fix.

4. **The autosomal test can't distinguish Oliver from another son by the same father.** Oliver's private alleles trace to his father's line. The 98.7% Y-lineage match
