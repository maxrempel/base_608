# Scribe handover - milestone 3 (~244K tokens)
# session: 20260702_modest_murdock_f1ec2f_d10fb650
# cwd: C:\claude_base\.claude\worktrees\modest-murdock-f1ec2f
# written: 2026-07-02 12:43:07 by deepseek-v4-pro

# HANDOVER: Kristen Kenefick XG1 Genome Analysis (Session X5 / x1)

---

## GOAL (in Max's words)

"Looking for traces of alien manipulation but not at the expense of truth." Kristen Kenefick is an experiencer (UFO sighting ~2020, precognition, 5 children) who provided her 30x whole-genome sequencing data from Sequencing.com. She made specific claims about her genome: multiple X chromosomes, XX/XY chimerism (a Y chromosome appearing in her sample, ostensibly matching her son Oliver's Y), too much homozygosity, missing a parental contribution, and extra/missing gene copies. The project's true aim - the reason Max fought to get her raw reads - is to search for non-human sequence or engineered insertions through reference-free analysis of the raw FASTQ files.

---

## DECISIONS MADE + WHY

### 1. The "maternal-Y chimerism" was a panel artifact - NOT real male DNA
**Why:** Early analysis of Kristen's Sequencing.com genotype *panel* (~2,140 standardized Y SNP rsids) showed her matching Oliver's Y at ~99%, which was a 7-point gap above the unrelated-male floor (~92%). This looked like a biological miracle. But when the raw 30x BAM was analyzed on asto using mosdepth (MAPQ?20, genome-wide coverage), the Y chromosome showed **mean depth 0.41x vs autosomal ~39x (ratio 0.007)** - effectively zero. The male-specific Y region (MSY) was only ~7% covered. This **excludes any male cell line above ~1.5-2%** (the honest detection floor at 30x). The genotype panel's "calls" were most likely X-Y cross-mapping / array artifacts from paralogous regions. **x1 (the manager chat) independently converged on the same conclusion** - the team findings are aligned.

### 2. All five of Kristen's specific claims are now refuted by the raw BAM data
**Why:** The court-grade analysis used mosdepth (windowed MAPQ?20 depth), bcftools (biallelic PASS SNPs with allelic depths), and scipy for statistical tests. Each claim was measured against probabilistic expectations:
- Multiple X: X depth = 0.98? autosome, exactly two X
- XX/XY chimerism: Y depth effectively zero (see above)
- Too much homozygosity: het/hom ratio 1.76, 2.67M heterozygous sites (normal outbred)
- Missing a parent: inbreeding coefficient F_roh = 0.0017 (two unrelated parents)
- Extra/missing gene copies: 64 gains / 69 losses - ordinary burden for a human genome

### 3. Raw reads (FASTQ/BAM) are the essential data - VCFs are blind to novel insertions
**Why:** A variant call file (VCF) only lists differences from the reference genome (GRCh38). Fully novel sequence - the alien-insertion classes Max defined - would either fail to map or get soft-clipped and dropped by the caller. The raw FASTQ (and BAM that retains unmapped reads) are where the actual search lives. Kristen's BAM was confirmed to **retain unmapped reads**, so her raw-FASTQ realignment wasn't necessary for the first pass.

### 4. asto (astolfodebian, Liz's guest box) is the compute node; Centauri (Max's Windows server) is the storage
**Why:** Centauri has 16TB but only bare Python (no samtools/bcftools). asto has 16 cores, 31GB RAM, 982GB free, and we installed samtools 1.19.2, bcftools 1.19, mosdepth 0.3.8, numpy/scipy, and kraken2 2.1.3 into an ubuntu distrobox there. Data is transferred directly Centauri?asto over Tailscale (no laptop relay). Guest rules: footprint ?480GB, keep ?23% free, compute only.

### 5. Letters to Kristen are DRAFT-ONLY, sent only on Max's explicit "send"
**Why:** The experiencer-honesty rule: report observations/counts only, draw NO unfounded conclusions, NEVER say "normal / nothing alarming" (she's hunting an anomaly, and that framing reads as dismissal). Kristen is described as "talented but unbalanced - thrives on facts from Gemini, has no common sense in genetics, paranoid/delusional." Letters are in Anna's voice (Anna, Max's virtual AI assistant), sent from anna@maxrempel.com (auto-BCC max.rempel2@gmail.com). Max's own personal replies go from max@dnaresonance.org.

### 6. The three alien-manipulation evidence classes (Max's framework)
1. A long insertion in a child absent in both parents ? needs a **trio** (child + both biological parents)
2. Same insertions recurring across independent experiencer families, absent in the general population ? needs **multiple families' full sequences**
3. Artificial/CRISPR-like sequence tags ? needs **full individual sequences** with reference-free assembly

### 7. No letter was sent to Kristen about genome findings yet - the reads-based classification must finish first
**Why:** Max explicitly said: "the only updates on analysis I ask must be from raw reads. I had a lot of trouble convincing her to give me password and download reads. The whole argument was that without reads we can't say anything. So if you have no news from reads, that's bad." A draft was softened and held; the letter will go only after the non-human read classification completes.

### 8. Clean-tissue collection is impractical and unnecessary for the first pass
**Why:** Consumer WGS services take saliva, which concentrates leukocyte-borne microchimeric cells. Clean alternatives (skin fibroblasts, hair follicles, tape stripping) need a lab Max doesn't have. But the male admixture is Kristen's son Oliver's *known* genome (subtractable), and any germline alien insert would sit at ~50% VAF (far above the ~5% contamination floor). So the saliva raw reads can do the first search; clean tissue is only needed as a confirmatory step if a candidate appears.

---

## CURRENT STATE

### Downloads (Centauri D: drive, `D:\genomics\kenefick\`):
- **Kristen:** **100% complete** - 2 raw FASTQ (26.8GB + 26.75GB), BAM (34.07GB), snp-indel VCF (197MB), CNV/SV/MITO VCFs, 2 AncestryDNA chip files. Total ~88GB.
- **Oliver:** **~54% complete** - 2 raw FASTQ (~44.1GB each) still downloading as Windows Scheduled Tasks (dl_oliver_f1/f2). File 1 was at ~41%, file 2 at ~27% as of last check. Slow OCI?residential link, ~0.6-0.9 MB/s. Oliver has NO BAM (only FASTQ + variant VCFs + chip).
- **Twins (Genome 3 & 4):** chip data only. No WGS - dropped (no funding). Kristen may eventually WGS them herself.

### Analysis completed (all committed to `C:\claude_base\projects\XG1\kenefick\`):
- **Court-grade report**: `kristen_claims_report_v01_tomemex.md` - all five claims measured with detection limits, probabilistic framing, allele-balance distribution, and reconciliation with the earlier "maternal-Y" headline.
- **Analysis script**: `scripts/kristen_analyze.py`
- **Unmapped read characterization**: `scripts/kristen_unmapped_char.py` - 8.54M unmapped reads are full-length (150bp), clean (0% adapter, 0.05% low-complexity), human-like GC (mean 0.436). NOT library junk - reads that simply don't align to GRCh38.
- **Status report**: `kristen_kenefick_status_report_20260701_v01_tomemex.md`

### Analysis in flight:
- **kraken2 classification** of Kristen's 8.54M unmapped reads on asto: the 16GB PlusPFP reference library was downloading, then it classifies all reads. ~10-20 min total. This will give the "what are the non-matching reads?" answer - the last substantive piece before the letter to Kristen.

### Canonical project tree (resolved):
Previously branched between `genomics/kenefick/` (this session) and `projects/XG1/kenefick/` (x1's canonical root). **All files consolidated to `projects/XG1/kenefick/`** - committed and pushed (commit 1576abf6 and later). Structure:
```
projects/XG1/kenefick/
??? kristen_claims_report_v01_tomemex.md
??? kristen_kenefick_status_report_20260701_v01_tomemex.md
??? kristen_rawread_findings_v01_tomemex.md
??? kristen_stats_v01.json
??? kristen_depth_v2.txt
??? kristen_hom_roh_v01.txt
??? kristen_unmapped_char.txt
??? X3_BRIEFING_START_HERE.md
??? scripts/
?   ??? kristen_analyze.py
?   ??? kristen_unmapped_char.py
?   ??? kristen_kraken.sh
??? analysis/
?   ??? x3_maternalY_results_v01.txt
?   ??? x3_maternalY_AD.md
??? kristen/
?   ??? KK_indel.txt
?   ??? reply_send.py, reply_send_02.py, reply_send_03.py
?   ??? fastq_link_send.py
?   ??? consent_send.py
?   ??? drive_share_request_send.py
?   ??? y_report_send.py
?   ??? results_reply_send.py
??? oliver/
?   ??? OK_snpindel.txt
??? raw_vcf/
    ??? kristen_wgs/  (Kristen's 189MB gVCF)
    ??? oliver_wgs/   (Oliver's 194MB VCF)
    ??? [SV/CNV/MITO copies]
```

### Consent:
Full trio consent locked: Kristen's adult self-consent + parental consent for Oliver (minor under 18) - both received 2026-06-27. Recorded in D1 database row 41.

### Letters sent to Kristen (this case):
1. **reply_send_02.py** - Y-test results + request for raw VCFs/full WGS
2. **y_report_send.py** - Y-chromosome findings (microchimerism, 3 alien-evidence reasons)
3. **consent_send.py** - two consent emails (Kristen adult + Oliver parental)
4. **results_reply_send.py** - bare VCF/TXT + SV/CNV/MITO counts
5. **reply_send_03.py** - 6-answer science reply (cells-forever, Y-chain, microchimerism, 30x sensitivity, XXY caution, two-slippage-repeat dismissal)
6. **fastq_link_send.py** - FASTQ share-link instructions (later moot; she gave Max her login instead)
7. **send_kristen.py** - download receipt (~88GB report)

### Max's own letters:
- Personal Zoom offer (sent from max@dnaresonance.org)
- FASTQ download-instructions draft (ChatGPT-generated, heavily edited, ultimately sent as Anna-voice `fastq_link_send.py`)

---

## EXACT NEXT STEP

1. **Check kraken2 classification on asto** - it was launched with the 16GB PlusPFP library downloading. Read `/home/rempel/genomics/_analysis/kristen_kraken.log` and `/home/rempel/genomics/_analysis/kristen_kraken_report.txt` for the per-read taxonomic assignments. The key output: proportions of human-missing / microbial / truly unidentifiable reads.

2. **If classification is done:** update `kristen_claims_report_v01_tomemex.md` with the non-human classification (section 7), commit+push, then draft the Anna-voice letter to Kristen around real raw-read findings - observations/counts only, no "normal" framing, no promises, acknowledge what we can't yet resolve, and steer her to the trio + Oliver's data as the next real step.

3. **Continue monitoring Oliver's FASTQ downloads** on Centauri (`D:\genomics\kenefick\oliver\dl_ofq1.log` / `dl_ofq2.log`) to DONE_EXITCODE_0. When both finish, verify final sizes (~44.1GB each) and report to Max. Oliver's data is the prerequisite for the trio analysis.

4. **After Oliver's data lands:** run the same BAM-level analysis on Oliver (samtools flagstat/coverage on his FASTQ since he has no BAM), then the mother-son trio comparison for non-inherited variants.

---

## OPEN QUESTIONS AWAITING MAX

1. **Non-human classification method:** you authorized kraken2 implicitly (I was told to "work autonomously," and I explained it and proceeded). The job should be done by now. Confirm satisfied with the approach.

2. **Letter to Kristen:** the reads-based letter draft is ready to rewrite once classification finishes. How much detail do you want her to see about the null results on her five claims? The experiencer rule says "observations/counts only, no reassurance" - but five refutations at once is a lot. Do you want the letter to focus on the non-human pile (the part she actually wants to hear about) and soft-pedal the rest?

3. **Oliver analysis plan:** once his FASTQ finishes, the BAM-level pipeline is identical to Kristen's. Should I run it autonomously, or wait for your go?

4. **Parents/ex-husband trios:** Kristen's parents were willing to participate; the ex-husband's data would be the key to ruling out microchimerism definitively. Has there been any movement on getting their samples sequenced?

---

## KEY PATHS, IDs, COMMANDS

### Access:
- **Centauri:** `ssh -i C:\Users\maxre\.ssh\sol_key maxre@192.168.1.176` (LAN IPv4 only)
- **asto:** `ssh -i C:\Users\maxre\.ssh\bitwarden_ed25519 rempel@astolfodebian.tail251d88.ts.net` (Tailscale)
- **asto distrobox:** `distrobox enter ubuntu -- bash -lc '...'`
- **Pine worktree:** `C:\claude_base\.claude\worktrees\modest-murdock-f1ec2f`
- **Gmail (Kristen's address):** kristentheartist@gmail.com
- **Outbound mail:** anna@maxrempel.com (Anna/Rempel voice); max.rempel2@gmail.com auto-BCC'd

### Data locations on Centauri (`D:\genomics\kenefick\`):
- **Kristen (complete):** `kristen\KristenKenefick-SQ76JY63-30x-WGS-Sequencing_com-04-14-26.1.fq.gz` (26.8GB), `.2.fq.gz` (26.75GB), `.bam` (34.07GB), `.snp-indel.genome.vcf.gz` (197MB), `.cnv.vcf.gz`, `.sv.vcf.gz`, `.mito.vcf.gz`, `KristenKenefick-AncestryDNA.1.txt`, `.2.txt`
- **Oliver (in progress):** `oliver\OliverKenefick-SQA666N3-30x-WGS-Sequencing_com-05-22-26.1.fq.gz`, `.2.fq.gz` (~44.1GB each, downloading), `.snp-indel.genome.vcf.gz` (194MB), `.cnv.vcf.gz`, `.sv.vcf.gz`, `AncestryDNA4.txt`
- **Twins (chip only):** `twins\AncestryDNA17.txt` (Genome3), `Genome4-AncestryDNA.txt` (Genome4)
- **Download logs:** `oliver\dl_ofq1.log`, `dl_ofq2.log`

### Data locations on asto (`/home/rempel/genomics/`):
- **Kristen BAM:** `kenefick/kristen/*.bam` (34.07GB, indexed)
- **Kristen VCFs:** `kenefick/kristen/*snp-indel*.vcf.gz` + `.tbi`
- **Stage A outputs:** `_analysis/kristen_flagstat.txt`, `_analysis/kristen_idxstats.txt`, `_analysis/kristen_coverage.txt`, `_analysis/kristen_unmapped.bam`, `_analysis/kristen_unmapped_flagstat.txt`
- **MOSDEPTH output:** `_analysis/kristen_mosdepth/*`
- **Extracted SNP table:** `_analysis/kristen_snps_biallelic.tsv.gz` (4,126,577 SNPs)
- **Analysis stats:** `_analysis/kristen_stats_v01.json`
- **Kraken pipeline:** `genomics/kristen_kraken.sh`, output `_analysis/kristen_kraken.log`, `_analysis/kristen_kraken_report.txt`

### Canonical project files (Pine, committed to git):
- **Report (the load-bearing doc):** `C:\claude_base\projects\XG1\kenefick\kristen_claims_report_v01_tomemex.md`
- **Analysis script:** `C:\claude_base\projects\XG1\kenefick\scripts\kristen_analyze.py`
- **Kraken script:** `C:\claude_base\projects\XG1\kenefick\scripts\kristen_kraken.sh`
- **All prior letters/scripts:** `C:\claude_base\projects\XG1\kenefick\kristen\*.py`
- **Bcast
