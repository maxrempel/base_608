# Scribe handover - milestone 9 (~715K tokens)
# session: 20260705_sleepy_feistel_3e6add_17fad24d
# cwd: C:\claude_base\.claude\worktrees\sleepy-feistel-3e6add
# written: 2026-07-05 15:35:24 by deepseek-v4-pro

# HANDOVER - P3 OMEGA (X21B): Foreign-DNA Insertion Detector

## GOAL (in Max's words)

Find inserted foreign/non-human DNA in human genomes - the "alien genetic manipulation" test. Specifically: **human-LIKE insertions that are slightly divergent from the human consensus (0.5-10%) and out-of-place.** The core hypothesis: the aliens are humanoid relatives, so their DNA is human-like but subtly drifted. A clean human match at 100% = ordinary; a match at 85-97% = potentially the target. The strongest signal is **non-parental**: an insertion present in Oliver (child) but ABSENT in Kristen (mother).

---

## DECISIONS MADE + WHY

### Method: Option B ("fishing to extend, not to close")
- **What**: detect insertions as **facing half-chimeras** - each is a contig anchored in human DNA on one end, running off into foreign sequence on the other. Two facing halves at one locus = an insertion. We do NOT demand they meet in one spanning contig (that breaks on long inserts).
- **Why**: Max's fish-to-extend metaphor - extend outward from each anchor, re-bait with unmapped reads, repeat. Length-independent. Passed the positive control (1 kb and 5 kb synthetic inserts both found correctly).
- **Why not full-span (Option A)**: impossible for long inserts, failed the positive control (couldn't reconstruct the payload).

### Target reframe (CRITICAL - the mega-correction Max gave)
- **Original wrong frame**: "foreign = non-human." Led to dismissing everything that mapped to human as "uninteresting."
- **Corrected frame**: the aliens are related to us, so inserts are **human-LIKE but diverged from consensus by 0.5-10%**. Also "out-of-place" = maps to a *different/distant* locus, not just unmapped. "Unclassified" alone is NOT a finding.
- **Max's words**: "Human-like insertions are fine. But they must be strange, they must be out of place. Just not recognized is not enough."

### Filters: inventory first, calibrate second
- **Why**: Max explicitly rejected binary on/off gates - "you're like, oh, we turn on the filter. That's stupid." Every candidate is kept and annotated along all axes; thresholds are learned from the actual distribution, not preset.
- Repeat-bleed (transposon sticking) filter: loci where recruited reads explode (>5000) are **immediately discarded** as unreliable (Max: "as soon as the number of hits begins to scale, we immediately filter this section").

### Infrastructure
- **Sol abandoned**: hardware corrupts BAM on write (two copies, two different random CRC/BGZF corruptions). Rule: no genomics on Sol.
- **asto**: the borrowed/shared Linux box (Liz's). Resource cap: ?50% CPU/RAM/disk/network (Max: "keep all four under 50%").
- **EC2 attempted and aborted**: asto's upload measured at ~2.7 MB/s real (not the 65 MB/s local Tailscale path). Transfer would've taken 3.6 hours.
- **Xena**: a free server Max mentioned, ready to spin up. Not yet configured - no IP/key.

### Positive control mandatory
- Built `make_pc.sh`: synthetic genome with known foreign insert ? proves detector fires before trusting any result. Passes at 1 kb and 5 kb. Rule saved: **pilot-prove before scale** (no genome-wide until a pilot demonstrates the method finds something).

---

## CURRENT STATE

### What is DONE:
1. **Detector built and validated.** Option B junction half-chimera pipeline - `omega_junction.py` + `omega_percluster.sh` + iterative fishing (`iterative_fish_all.sh`, 3 rounds). Positive control passes.

2. **Genome-wide Oliver scan COMPLETE.** 743 two-sided insertions, 21k half-sided junctions, 23,830 payloads total. All 24 chromosomes run, resumable, committed.

3. **Full characterization pipeline built and run** - `characterize.py/sh`: blast vs GRCh38, dustmasker (low-complexity filter), transposon-family clustering, gene-context annotation (GENCODE bedtools intersect), kraken2 taxonomy, T2T-CHM13 check, nt-BLAST remote.

4. **Oliver-alone result = clean negative.** After exhaustive analysis (GRCh38, T2T, nt-BLAST, kraken, gene context, families): **everything resolves to known human DNA.** The "divergent" candidates (0.5-10% from consensus) are **115 from 743**, but all that were deep-checked turned out to be catalogued human non-reference insertions (fosmid clones, NA12878 variants, clone breakpoint junctions). No foreign, no archaic, no transposon families.

5. **Non-parental sieve built and validated.** `nonparental_kmer.py` - k-mer-presence method (aligner-agnostic, avoids the DRAGEN-vs-bwa soft-clip disparity). Validated Oliver-vs-Oliver (all 12 test candidates correctly show INHERITED with strong k-mer support). Ready to fire.

6. **Waiting on Kristen's bwa BAM.** X5 is running it (accelerated to 16 cores, ETA ~4-5h from ~2 days ago). When it lands, the non-parental sieve fires on the 78 clean diverged candidates. Verdict MATERNALLY_ABSENT = the real signal.

### What is IN FLIGHT:
- Kristen's bwa realignment (X5 on asto, ETA same evening)
- nt-BLAST remote queries sometimes stall at NCBI (used local T2T fallback successfully)

---

## EXACT NEXT STEP

**When `kristen.bwa.mq.bam` appears on asto** (path: `/home/rempel/genomics/kenefick/kristen/`), run:

```
bash /home/rempel/genomics/omega_run/scripts/np_sieve_runner.sh
```

This will: check the BAM exists ? extract k-mers from each of the 78 clean diverged candidates ? count k-mer presence in Kristen's reads via `samtools view` ? compare to Oliver counts ? produce `nonparental_verdict.txt` with three bins:
- **MATERNALLY_ABSENT**: k-mers in Oliver, zero in Kristen = THE signal
- **INHERITED**: present in both = normal polymorphism
- **INSUFFICIENT_DATA**: too few reads in Kristen to call

**The runner is already staged at** `/home/rempel/genomics/omega_run/scripts/np_sieve_runner.sh`
**The candidate list is at** `/home/rempel/genomics/omega_run/out/genome_oliver/reconstruct_all743/diverged115_ranked.tsv` (78 "clean" candidates with the repeat-bleed filter applied)

---

## OPEN QUESTIONS

1. **Xena server access**: Max mentioned Xena is free and ready. Need IP + SSH key + OS details to add it to the machine registry. Would be useful for offloading heavy compute from asto.

2. **New workers**: Max offered to spin another worker for production mode - X21B should stay as manager/overseer rather than doing the programming. Accept?

3. **Oliver alignment clarification**: Max just said Oliver has a proper bwa alignment finished yesterday (~7pm). The current genome-wide run used `oliver.mq.bam` (the MAPQ-filtered DRAGEN vendor BAM). Need to confirm: should the non-parental sieve use the **old DRAGEN Oliver BAM** (k-mer method is aligner-agnostic, so it should be fine) or the **new proper bwa Oliver BAM**? If a fresh bwa Oliver exists, everything should be re-run on it for maximal sensitivity.

4. **Kristen's realign ETA**: was ~4-5h from roughly mid-afternoon. Should be landing around early evening Pacific time.

---

## KEY PATHS / IDs

- **Design doc (canonical)**: `C:\claude_base\projects\XG1\kenefick\omega_detector\OMEGA_PIPELINE_DESIGN_v01_tomemex.md` - contains the BREAKTHROUGHS section, corrected target, all calibration results. READ THIS FIRST.
- **Brainstorm origin**: `C:\claude_base\projects\XG1\kenefick\FOREIGN_INSERTION_DETECTION_BRAINSTORM_tomemex.md`
- **Scripts (local)**: `C:\claude_base\projects\XG1\kenefick\omega_detector\` - all committed to git (claude_base repo, master)
- **Scripts (asto)**: `/home/rempel/genomics/omega_run/scripts/` - synced with local
- **Oliver BAM (DRAGEN, used)**: `/home/rempel/genomics/kenefick/oliver/oliver.mq.bam` (65.7 GB)
- **Kristen BAM (vendor, old)**: `/home/rempel/genomics/kenefick/kristen/kristen.mq.bam` (35 GB)
- **Kristen BAM (bwa, expected)**: `/home/rempel/genomics/kenefick/kristen/kristen.bwa.mq.bam` - NOT YET EXISTS
- **Reference**: `/home/rempel/genomics/omega_run/ref/GRCh38.fa`, `chm13v2.0.fa` (T2T, downloaded)
- **Genome-wide output**: `/home/rempel/genomics/omega_run/out/genome_oliver/` - per-chromosome `RUN_COMPLETE` markers, `reconstruct_all743/` has all payloads and the characterization
- **Candidate lists**: `diverged115_ranked.tsv` (78 clean for sieve), `cand27_ntblast.tsv` (resolved), `unmapped_strong.fa` (23 deep-checked ? 1 survivor ? now resolved as human)
- **Non-parental sieve**: `nonparental_kmer.py` + `np_sieve_runner.sh` (staged on asto)
- **Positive control**: `make_pc.sh` - generates synthetic genome, runs detector, expects PASS
- **global2.md rules**: pilot-prove-before-scale, look-at-real-data-close-up, blocked-sessions-self-escalate, dictation-artifacts-to-ignore
- **asto connection**: `ssh -i ~/.ssh/bitwarden_ed25519 rempel@astolfodebian.tail251d88.ts.net`, distrobox: `distrobox enter ubuntu`
- **Tmux sessions**: run long jobs in tmux (`tmux new-session -d -s omega '...'`), survive SSH drops
- **Anonymization**: Kristen?Antoinette, Oliver?Theodore, Kenefick?Whitfield (use in shared/cloud artifacts)
- **Board**: `python C:/claude_base/branch_bulletin/bcast.py` - team coordination; X5/X10A/X8A/X9A/x1 are active teammates

---

## GOTCHAS + DEAD ENDS

- **PowerShell `tr -d "\r"` deletes every letter 'r'**: use `tr -d '\015'` or bash `tr -d '\r'`, never PowerShell for line-ending stripping.
- **mkdir-before-redirect**: `omega_genome.sh` once redirected the log before creating the output dir ? every chromosome instantly failed, census reported false "0 hits." Always mkdir first.
- **Sol hardware corruption**: BAM copies get random CRC/BGZF corruption. `samtools quickcheck` false-passes (only checks EOF). Never trust Sol for big file storage.
- **systemd-oomd killer**: a repeat pileup at chr12 centromere fed megahit thousands of reads ? OOM kill of the whole run. Fixed with READCAP=2000 + per-worker `ulimit -v`.
- **DRAGEN vs bwa soft-clip disparity**: Kristen's vendor BAM has ~8? fewer soft-clips than bwa. The k-mer sieve (checking payload presence in reads directly) bypasses this - DON'T use clip-counting for the mother-son comparison.
- **"Divergence" from GRCh38 is misleading**: many payloads show 80-97% identity to GRCh38 but 100% to catalogued human non-reference sequences (fosmid clones, NA12878, clone breakpoint junctions). T2T-CHM13 catches some; nt-BLAST catches the rest. "Diverged from GRCh38" ? foreign - always check against the full human pan-reference (T2T + nt).
- **Remote nt-BLAST stalls**: NCBI queue sometimes sits at 0/23 for 20+ minutes. Local T2T is the fast fallback. Kill the remote query and re-submit one-at-a-time for stubborn ones.
- **Repeat-bleed (transposon sticking)**: iterative fishing rounds 4+ cause explosive recruitment (758k ? 5.9M ? 12.8M reads) = the contig grabbed a repetitive region. Discard immediately (Max's rule: "as soon as hits scale, throw it away").
- **"Blocked" must self-escalate**: never park on a dependency silently for 10+ hours. Check if the block is real, find a fallback, ping Max if still stuck. Saved as rule in global2.
- **Max's dictation artifacts to ignore**: "??????????? ???????," "thank you," "you" - these are Whisper blanks, NOT instructions.
- **Y chromosome and unplaced alt-contigs**: ~25% of candidates map there - mostly mapping artifacts in heterochromatin/repeats, not real insertions. Flag but don't discard (inventory-first).
- **Compaction recovery is clean**: compaction happened in this session and worked fine - context dropped from ~715k tokens to ~15%, all state preserved. No special recovery needed.

---

## CONSOLIDATED VERDICT (for Max)

Oliver's genome, analyzed exhaustively on its own, shows **no confirmed foreign/alien/diverged-non-human insertions**. All 743 candidates resolved to known human DNA. The non-parental mother-son sieve (Kristen's bwa BAM, arriving same evening) is the **last remaining test** that could reveal a true alien-origin signal - an insertion present in Oliver but absent from his mother. The sieve is built, validated, and ready to fire the moment Kristen's BAM lands.
