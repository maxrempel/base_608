# Scribe handover - milestone 4 (~305K tokens)
# session: 20260703_jolly_austin_dd9aa0_0acef98a
# cwd: C:\claude_base\.claude\worktrees\jolly-austin-dd9aa0
# written: 2026-07-03 16:32:06 by deepseek-v4-pro

**HANDOVER - X10A Alien-Trace Track (Session 2026-07-03)**

---

## GOAL (in Max's own words)

Max is hunting for **traces of alien genetic manipulation** in the Kenefick family genomes. The specific signatures being searched for are **novel/orderly DNA insertions** and **mobile?element activity** in Kristen Kenefick's genome. X10A (you) are the **TRACK-1 MANAGER** (Kenefick/alien-trace), overseeing the insertion-analysis lane, phasing, inversion counting, and all file coordination. The team works autonomously; you surface only when results land or something genuinely needs a decision.

---

## DECISIONS MADE + WHY

1. **INSurVeyor on Kristen (insertion caller)** - previous runs by X5 failed because:
   - Run?1 (original vendor BAM) assembled ~172 candidate insertions but crashed at the filtering step (missing duplicate-mark flags and split-read MQ tags).
   - Run?2 tried to fix it but inadvertently lost the duplicate marks, yielding **zero** assemblies.  
   **Decision:** Rebuild Kristen's BAM from scratch with the proper pipeline (namesort ? fixmate ? coordsort ? markdup ? index) inside the `insurveyor` conda environment, then re-run INSurVeyor using **the main-chromosome-only reference** (`GRCh38_main.fa`) to avoid contig mismatches. The rebuilt BAM is named `kristen.ins_ready.bam`.

2. **Sol is untrustworthy** - after three power-cycles and a disk?corruption boot?repair (initramfs `fsck -y /dev/nvme0n1p2`), Max declared Sol a **disposable workhorse**: keep nothing important on it, copy results off quickly, expect to reinstall toolchains after crashes. Phasing was launched on Sol but later failed; it is **not** a critical blocker because asto can also phase.

3. **Kristen phasing runs first** - single?sample phasing does **not** wait for Oliver's BAM; Kristen's BAM + VCF are already on asto. X8A owns the phasing lane; they launched it on both asto and Sol (race). The asto run is healthy (on chr4 region), the Sol run later failed but the asto copy is sufficient.

4. **Oliver BAM** - still aligning (very slow, ~7h in, bwa mem ? samtools sort). It is **not** blocking the Kristen letter; only needed later for mother?son inversion counts and pedigree phasing.

5. **Control?genome inversion counts** - X9A already got the first control (28 hom?inv vs Kristen's 29), which demolishes the "1500 inversions" claim. Second control ready; these are the headline numbers for the letter.

6. **Mobile?element caller (xTea)** - installed successfully in its own conda env on asto. It will be launched on the same `kristen.ins_ready.bam` after INSurVeyor finishes.

7. **Managerial structure** - Track?1 (alien?trace) manager = X10A; Track?2 (paper reproduction) manager = X12B; X7A handles Kristen letters. The tracks are independent.

---

## CURRENT STATE

- **INSurVeyor v6 is running cleanly on Kristen.** It passed the earlier crash points and is now categorising reads across chromosomes (high CPU). The prepared BAM (`kristen.ins_ready.bam`, 35?GB, indexed) was built successfully. The working directory is `~/genomics/_analysis/insurveyor_kristen4/`. Expected runtime ~1-2?h from the "categorising" stage.

- **xTea is installed** (`conda env: xtea`, with `samtools` inside it) but **not launched yet**. You plan to launch it once INSurVeyor results are seen (or right after, if BAM is ready).

- **Oliver's BAM** - still aligning on asto; X5 restarted it as chunked/resumable to avoid restarting from scratch. No finished file yet. The plan is to run INSurVeyor on Oliver using the **same** working recipe (`ins_ready.bam` build + main?chrom?only reference) once his BAM lands.

- **Phasing** - X8A's asto phasing of Kristen is in progress (chr4 area). Sol's attempt died but doesn't block.

- **Control inversions** - second control genome ready for Manta; the first gave the crucial comparison number.

- **Team communications** - using the x?board (`bcast.py post`) for Track?1 coordination. The joint board is not used for genomics.

---

## EXACT NEXT STEP

**Immediate wake action (already armed):**  
Check INSurVeyor v6 completion (tail `~/genomics/_analysis/insurveyor_kristen4.log`) and examine `out.pass.vcf.gz`.  
- If finished, count records, flag any **large (> a few kb) or "orderly" insertions** (the alien signature), and post results to the x?board.  
- Whether finished or not, **launch xTea MEI caller** on `kristen.ins_ready.bam` using the xtea conda env (`setsid bash -c '...'` inline, the proven method).  
- Batch everything into **ONE asto SSH call** (respect the 2?call?per?window safety hook).  
- Re?arm the wake for ~45?min if INSurVeyor is still running.

---

## OPEN QUESTIONS (awaiting Max)

- **Sol hardware fix** - Max physically power?cycled and verified it boots; disk repaired via fsck. It is now considered an unreliable workhorse per his directive. No open question, but future failures should be expected and ignored until explicitly instructed.

- **No decision needed from Max right now** - the pipeline is running autonomously. The only thing he might want to confirm later is whether the found insertions look "alien" or if any follow?up on Oliver is urgent.

---

## KEY FILE PATHS, IDs, COMMANDS

**asto compute box**  
`ssh -i ~/.ssh/bitwarden_ed25519 rempel@astolfodebian.tail251d88.ts.net`

**Kristen BAMs**  
- Original: `~/genomics/KristenKenefick*.bam`  
- Fixed/deduped for phasing: `~/genomics/kenefick/kristen/kristen.fixed.bam`  
- Rebuilt for insertion analysis: `~/genomics/kristen.ins_ready.bam` (35?GB, index present)

**INSurVeyor**  
- Conda env: `insurveyor` (activate via `source ~/miniconda3/etc/profile.d/conda.sh; conda activate insurveyor`)  
- Working run: `~/genomics/_analysis/insurveyor_kristen4/` (v6, log `insurveyor_kristen4.log`)  
- Reference: `~/genomics/ref/GRCh38_main.fa` (main chromosomes only)  
- Command to re?run (from scratch):  
  ```
  insurveyor.py READY WD ref --threads 8 /path/to/kristen.ins_ready.bam /path/to/GRCh38_main.fa /output/dir
  ```

**xTea mobile?element caller**  
- Conda env: `xtea` (activate similarly)  
- Samtools at: `~/miniconda3/envs/xtea/bin/samtools`  
- Installed but not yet run.

**Oliver BAM**  
- Pipeline log: `~/genomics/_analysis/oliver_pipeline.log`  
- Expected final BAM: `~/genomics/kenefick/oliver/oliver.fixed.bam`

**Sol**  
- IP: `192.168.1.113`  
- SSH: `ssh -i ~/.ssh/sol_key maxre@192.168.1.113`  
- **Policy:** treat as unreliable; keep no sole copies; copy results off.

**Board**  
- Script: `C:/claude_base/branch_bulletin/bcast.py`  
- Post to x?board: `python .../bcast.py post "<message>"`  
- Read: `python .../bcast.py read`

**Safety hook** - blocks more than 2 asto SSH calls per window; batch everything into a single `ssh ... 'bash -s' <<'REMOTE' ...` call.

**Scratchpad directory** (local):  
`C:\Users\maxre\AppData\Local\Temp\claude\C--claude-base--claude-worktrees-jolly-austin-dd9aa0\0acef98a-2454-4b00-bf03-d6bc605df81d\scratchpad`

---

## GOTCHAS & DEAD ENDS RULED OUT

- **Windows CRLF ? silent script death** - any local script piped to asto must be stripped of `\r` (e.g., `tr -d '\r'`) or written via a heredoc directly on the remote side. This was the root cause of multiple "silent launch" failures.

- **`bash file` exec fails on detached asto sessions** - the proven method for launching detached background jobs is `ssh ... 'bash -s' <<'REMOTE'` with the script inline; saving to a file and then running it often does not survive the session.

- **Samtools missing in insurveyor env** - when the conda env is activated, `samtools` may not be on PATH. Use the absolute path from the `xtea` env (`~/miniconda3/envs/xtea/bin/samtools`) or ensure it's installed within the insurveyor env.

- **INSurVeyor contig mismatch** - using the full Ensembl?style reference (`GRCh38.fa`) against a BAM that contains UCSC?style alt contigs causes a crash. The fix is to use `GRCh38_main.fa` (1?22, X, Y, MT only), which matches the BAM.

- **Do NOT re?run the BAM build from scratch** unless the BAM is corrupted. The `kristen.ins_ready.bam` is reusable; only the caller step needs to be re?run if a reference or parameter changes.

- **Sol's disk corruption** - after hard power?offs, the ext4 root filesystem may need `fsck -y /dev/nvme0n1p2` from an initramfs prompt. The `reboot` command often does not work from that shell; a physical power?cycle is required.

- **Death?spiral hook** - limits you to **2 asto calls per window**; each window is roughly a few minutes. Always consolidate asto work into one or two large `ssh` calls. Use `sleep` polling inside the remote session if needed.

---

*This handover is complete. A cold session resuming from here should: (1) check the INSurVeyor v6 result, (2) launch xTea, (3) re?assess Oliver's BAM status, and (4) continue as Track?1 manager using the above paths, known gotchas, and the policy that Sol is a flaky compute node.*
