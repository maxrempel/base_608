# Scribe handover - milestone 6 (~455K tokens)
# session: 20260704_jolly_austin_dd9aa0_0acef98a
# cwd: C:\claude_base\.claude\worktrees\jolly-austin-dd9aa0
# written: 2026-07-04 14:58:06 by deepseek-v4-pro

# HANDOVER - P1 KENEFICK (Alien Genetic Manipulation Hunt)

## GOAL (Max's words, verbatim gist)

Investigate traces of alien genetic manipulation in the Kenefick family genetic data - specifically, hunt for **non-parental insertions, haplotype substitutions/replacements**, and any "orderly" foreign DNA integrated into Kristen's or Oliver's genomes. The core deliverable is a **maternal-haplotype concordance scan**: once both Kristen and Oliver are phased, compare Oliver's maternal chromosome copy against Kristen's two known haplotypes. Any segment on the maternal copy that matches **neither** of Kristen's haplotypes = a substitution/replacement - the anomaly. The father's chromosomes are ignored entirely because phased maternal inheritance pins down what came from Kristen.

Secondary goal: rebut Kristen Kenefick's claim that she has "1500 homozygous inversions" and other anomalies. That rebuttal is essentially done via inversion counting.

---

## DECISIONS MADE + WHY

### 1. Project naming (Max-directed)
**P1 KENEFICK** (X10A manages) - mother-son alien-trace hunt, inversion rebuttal, maternal haplotype concordance.
**P2 NPA** (X12B manages) - Non-Parental Alleles, 1000-Genomes paper reproduction genome-wide.
**P3 OMEGA** (X21B manages) - de-novo foreign-DNA detector (chimeric human|FOREIGN|human contigs).
**INFRA x30b** - cross-project resilience toolkit.
**SHARED x1** - downloads/transfers across all projects.
*Reason: Max asked for numbered/nameable projects because "we have multiple projects, I'm lost."*

### 2. Maternal-haplotype concordance method (Max's key insight)
After phasing both Kristen and Oliver, identify which of Oliver's two haplotypes came from Kristen. Then compare ONLY that maternal copy against Kristen's genome. Any inserted/substituted DNA on the maternal haplotype absent from Kristen = a genuine signal. The father's haplotype is irrelevant - never looked at.
*Reason: Max corrected that we don't need a father sample; phasing solves the trio problem.*

### 3. Sol = UNTRUSTWORTHY, do not use for correctness-critical work
Sol (192.168.1.113) was recovered from disk corruption via `fsck -y /dev/nvme0n1p2` after repeated hard power-offs. But X21B later proved it **silently corrupts data on write** - two writes of the same file gave *different* random corruption offsets. The RAM/disk hardware is still bad despite the fsck fix. Do NOT run genomics or court-grade work on Sol. Use asto or Lak.
*Reason: Silent data corruption is worse than a crash - it produces wrong results with no error.*

### 4. Kristen insertion "clean negative" was a technical false-negative - re-align initially greenlit, then HELD
Oliver's INSurVeyor run found 35,417 assemblies + 9,435 small insertions (normal). Kristen's vendor BAM gave **zero** - same tool, same recipe. That's impossible for a 30x human genome. So the Kristen result is a false-negative caused by something in the vendor (DRAGEN/Sequencing.com) BAM, not biology.
- X10A initially greenlit a full Kristen bwa re-align (delegated to X5).
- Max pushed back: "why re-process if we can find the bug? Look at the actual data first."
- X10A held the re-align and started looking at the raw reads.
- **Finding so far: the reads ARE fine** - Kristen's vendor BAM has 3,457 soft-clips, split reads, SA tags - MORE clipping signal than Oliver's. The reads have exactly the fingerprints INSurVeyor needs.
- Comparing logs: Kristen's INSurVeyor log shows it categorizing **hundreds of tiny alt/random scaffolds** (Un_KI270302v1, Y_KI270740v1_random, etc.), while Oliver's log doesn't. The contig list difference in the BAM headers is the likely culprit.
- **The re-align is held.** Max wants the simple diagnostic fix found before burning ~15 hours on a re-alignment.

### 5. INSurVeyor working recipe (nailed down through 8+ iterations)
- BAM needs **MQ tags** (fixmate) but must **NOT be markdup'd** (markdup kills INSurVeyor's assembly)
- Reference = `ref/GRCh38_main.fa` (main chromosomes 1-22,X,Y,MT only, UCSC naming). Full `GRCh38.fa` crashes on Ensembl scaffold names (`KI270729.1` not in the BAM).
- Conda env `insurveyor`, samtools at `~/miniconda3/envs/xtea/bin/samtools`
- Command: `insurveyor.py <bam> <outdir> ref/GRCh38_main.fa --threads 6`, nice -15, detached via setsid + heredoc

### 6. Safety hook workaround for asto SSH calls
The death-spiral hook limits to 2 asto SSH calls per window. Workaround: use heredoc (`ssh asto 'bash -s' <<'REMOTE' ... REMOTE`) for Linux-native line endings. Do NOT use Windows scratchpad files piped to ssh (CRLF corrupts filenames). Batch everything into single calls.

---

## CURRENT STATE

**DONE (P1 KENEFICK):**
- All downloads complete (x1)
- Kristen inversion count: 29 homozygous PASS - normal (healthy controls: 28 and 40). Her "1500" claim demolished ?
- Kristen phasing: complete (2.46M variants, 77.4% phased) ?
- Two unrelated strangers share 55% of inversions - answers "but my son shares them" without Oliver ?
- Oliver genome alignment: **complete** - oliver.mq.bam (65.7GB, MQ tags, no markdup) + oliver.fixed.bam (for Manta/phasing) ?
- Oliver INSurVeyor: running clean, found 35,417 assemblies + 9,435 small insertions (normal), final remapping stage in progress
- Sol status: documented as unreliable/hardware-corrupting in memory files ?
- Project naming broadcast to all sessions ?

**IN FLIGHT:**
- Oliver INSurVeyor final result - waiting for out.pass.vcf.gz record counts, flag large/orderly insertions
- **Kristen vendor-BAM false-negative investigation** - X10A was mid-diagnosis, comparing INSurVeyor logs between Kristen (vendor BAM, 0 results) and Oliver (self-built BAM, thousands). Found: Kristen's BAM has normal read clipping, but her log shows INSurVeyor categorizing hundreds of alt scaffolds. This contig-list difference is the likely bug. X21B also had a data finding about this - X10A was called to read it when the session was interrupted.
- X8A pedigree phasing + maternal-hap concordance - needs to launch on oliver.fixed.bam (was being nudged)
- X9A mother-son Manta shared-INV comparison - needs to launch (was being nudged)
- X21B's P3 OMEGA detector on Kristen - also affected by the vendor-BAM false-negative issue
- X5 has Kristen raw fastq files staged (per x1 inventory) - ready IF re-align is needed, but on hold pending diagnostic

**NOT STARTED / WAITING:**
- pedigree phase (mother=Kristen, father=0) on Oliver
- maternal-haplotype concordance walk - THE deliverable, gated on pedigree phase

---

## EXACT NEXT STEP

1. **Read X21B's latest board post** - they posted a data finding about the Kristen vendor-BAM issue that may crack the false-negative diagnosis. This was the last thing X10A was about to do.

2. **Finish diagnosing why Kristen's vendor BAM gives zero INSurVeyor results** despite having normal soft-clip/split-read signal. The contig-list difference (vendor BAM has hundreds of alt/random scaffolds that Oliver's BAM doesn't) is the prime suspect. Compare Kristen vs Oliver INSurVeyor logs around the "Categorizing" stage. The fix is likely a simple filter or contig-whitelist, NOT a full re-alignment.

3. **Check Oliver INSurVeyor final result** - out.pass.vcf.gz + small_ins.vcf.gz record counts, flag any large (>1kb) or orderly/structured insertions.

4. **Launch pedigree phase + maternal-hap concordance** on Oliver (nudge X8A, or do it directly if they haven't picked up).

5. **Launch mother-son Manta shared-INV** (nudge X9A, or do it directly).

6. Once Kristen vendor-BAM bug is understood and fixed, re-run INSurVeyor on Kristen's vendor BAM (with the fix) - OR if the fix requires a re-align after all, greenlight X5's bwa re-align.

---

## OPEN QUESTIONS

- **What is X21B's finding about the vendor BAM?** (the interrupted read)
- **Is the Kristen vendor-BAM false-negative fixable with a simple contig filter, or does it genuinely need a full re-align?** Max wants the simple fix found first.
- **Has X8A launched the pedigree phase on oliver.fixed.bam?** Last check: no process was running.
- **Has X9A launched mother-son Manta?** Last check: no process was running.

---

## KEY PATHS / IDs / COMMANDS

**Machines:**
- **asto**: `ssh -i ~/.ssh/bitwarden_ed25519 rempel@astolfodebian.tail251d88.ts.net` - the main compute box (borrowed, 16 cores, ~32GB). Where all genomics data lives.
- **Sol**: `ssh -i ~/.ssh/sol_key maxre@192.168.1.113` - Max's local box, **UNTRUSTWORTHY** (silently corrupts data). Do not use.
- **Lakarian (.199)**, **Centauri (.176)**, **Pine** - also on 192.168.1.x LAN.
- **OpenWRT router**: 192.168.1.1, root password `0y32dnkh40rj7hub1y`. DHCP leases via `ubus` HTTPS.

**Key file paths (on asto):**
- Kristen vendor BAM: `~/genomics/kenefick/kristen/KristenKenefick*.bam`
- Oliver BAMs: `~/genomics/kenefick/oliver/oliver.mq.bam` (MQ, no markdup) + `oliver.fixed.bam` (markdup)
- Kristen phased VCF: `~/genomics/_analysis/x8a_phasing/` (whatshap output)
- INSurVeyor working dirs:
  - Kristen: `~/genomics/_analysis/insurveyor_kristen*` (v1-v8, all 0 results; run1 has 172 raw assemblies saved at `/home/rempel/genomics/_analysis/kristen_insurveyor_RESULT_20260703/`)
  - Oliver: `~/genomics/_analysis/insurveyor_oliver/` (running, 35k+ assemblies)
- Reference: `~/genomics/ref/GRCh38_main.fa` (main chroms, UCSC names) - **use this, NOT GRCh38_full.fa**
- INSurVeyor conda env: `insurveyor`
- samtools: `~/miniconda3/envs/xtea/bin/samtools`
- xTea conda env: `xtea` (installed but no rep-lib - needs ~GB download for full run)
- whatshap venv: `~/genomics/_analysis/x8a_phasing/venv2/` (reinstalled by X10A, v2.8, confirmed working)

**Board (team communication):**
- `python C:/claude_base/branch_bulletin/bcast.py post "message"` - post to x-team board
- `python C:/claude_base/branch_bulletin/bcast.py read` - read the board
- Use plain `post` (NOT `--joint`/`--all`) for P1-internal traffic

**Memory files (survive compaction):**
- `C:\Users\maxre\.claude\projects\C--claude-base\memory\reference_sol_unreliable_workhorse.md` - Sol is untrustworthy, silently corrupts data
- `C:\Users\maxre\.claude\projects\C--claude-base\memory\project_genomics_p1p2p3.md` - project naming
- `C:\Users\maxre\.claude\projects\C--claude-base\memory\MEMORY.md` - index
- `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md` - updated Sol section (no longer says "BAD RAM", now says "BACK UP + healthy as of 2026-07-03" - **this is outdated given X21B's corruption finding; needs update**)

**WorkLog:** `python C:/claude_base/compaction_kb/scripts/worklog.py log "message"`
**Session status:** `python C:/claude_base/compaction_kb/scripts/session_status.py report "message"`

---

## GOTCHAS

- **Sol silently corrupts data.** Two identical file writes produced different random corruption. Do NOT trust Sol for any correctness-critical work. Use asto or Lak.
- **global2.md still says Sol is healthy** - X10A updated it after the fsck fix, but X21B's later corruption finding means it needs to be updated AGAIN to mark Sol as untrustworthy.
- **Do NOT use `GRCh38_full.fa`** (the Ensembl-scaffold reference). INSurVeyor crashes on contig name mismatches (`KI270729.1` in ref vs `17_KI270729v1_random` in BAM). Always use `ref/GRCh38_main.fa`.
- **Do NOT markdup BAMs for INSurVeyor.** Marking duplicates kills its assembly step (went from 172 raw assemblies to 0). Only add MQ tags via fixmate.
- **Vendor (DRAGEN) BAM from Sequencing.com gives false-negatives for INSurVeyor AND P3 OMEGA.** The reads look fine (soft-clips, split reads all present), but both tools find zero insertions. The contig list in the BAM header may be the issue - hundreds of tiny alt/random scaffolds that Oliver's self-built BAM doesn't have.
- **Windows line endings (CRLF) silently break scripts piped to Linux.** Always use heredoc (`<<'REMOTE'`) for inline commands to asto. Never pipe a Windows scratchpad file.
- **The safety hook limits asto SSH to 2 calls per window.** Batch everything into single heredoc calls. If rate-limited, wait for the cooldown (~4-5 min).
- **The death-spiral hook description in global2 says "fails open, never wedges"** but in practice it was blocking legitimate work - this inconsistency was logged to `C:/claude_base/rule_inconsistencies_tomemex.md`.
- **INSurVeyor's log is block-buffered** - output may not appear in the log file immediately. Use start-marker files (touch a marker at launch, check for it) to confirm a detached run actually started.
- **Kristen's INSurVeyor `assembly_succeeded.sv` from run1 (146KB, ~172 assemblies) was saved** at `/home/rempel/genomics/_analysis/kristen_insurveyor_RESULT_20260703/` - these are raw pre-filter assemblies, all filtered out by INSurVeyor's pass filter. Sizes 418-137
