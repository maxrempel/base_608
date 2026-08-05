# Scribe handover - milestone 5 (~377K tokens)
# session: 20260704_jolly_austin_dd9aa0_0acef98a
# cwd: C:\claude_base\.claude\worktrees\jolly-austin-dd9aa0
# written: 2026-07-04 08:03:52 by deepseek-v4-pro

# HANDOVER - Kenefick alien?trace track (X10A, manager)

## GOAL (in Max's words)
"Researching, searching for traces of alien genetic manipulation in the genetic data."

## MORE PRECISE GOAL (Max's refinement)
"We are looking for **haplotype substitutions or replacements**. But all other strange unexpected changes we can trace just using mother's chromosomes because they are phased."

**Track?1 deliverable:** scan Oliver's **maternal haplotype** (the chromosome copy he inherited from Kristen) for segments that match **neither** of Kristen's two phased haplotypes. That is the primary alien?trace signal. Supporting evidence: inversion counts (mother?son comparison) and non?reference insertions (INSurVeyor) on both Kristen and Oliver.

---

## DECISIONS MADE (and WHY)

### 1. Sol (local compute box) - status and policy
- **Sol was believed dead** (bad RAM), but Max confirmed it was **physically fixed** (bad DIMM removed).
- Belt?and?suspenders: X10A launched a memory stress?test that was too aggressive (24?GB on 31?GB box, full?verify), knocked Sol off the network.
- Multiple hard power?cycles caused **disk corruption** (dropped to initramfs shell). X10A walked Max through an `fsck -y /dev/nvme0n1p2` which repaired the filesystem. Sol returned cleanly (0% packet loss, SSH up).
- **Policy set by Max:** Sol is a **very unreliable workhorse** - nothing important kept on it, no only?copy data, copy results off promptly, expect to reinstall toolchains after crashes. Written to `reference_sol_unreliable_workhorse.md` and MEMORY.md.
- Sol is now usable for non?critical compute, but all critical work should favour asto (the dedicated borrowed server).

### 2. Kristen's analyses - all supplementary for the letter, now complete
- **Inversions (X9A):** Kristen has **29 homozygous inversions**, essentially identical to a healthy control (28). Demolishes the "1500" claim.
- **Phasing (X8A):** completed on asto - 2.46?M het variants phased, 77.4% of hets, valid VCF.
- **Insertions (X10A, subagent):** **clean negative** - zero passing non?reference insertions. INSurVeyor on the vendor BAM with main?chrom reference found 172 raw assemblies, but the filter rejected every one. No large or orderly inserted DNA. The negative is stable across multiple configurations.
- **Letter to Kristen (X7A):** now carried by the decisive inversion result + insertion negative. Only sent on Max's explicit greenlight.

### 3. INSurVeyor configuration saga - the proven recipe
Multiple runs (v1-v8) ruled out a long chain of red herrings:
- **MQ tags are REQUIRED** (vendor BAM lacks them ? INSurVeyor crashes at filter).
- **Duplicate?marking (`markdup`) KILLS the insertion signal** (0 assemblies even with MQ present).
- **Full GRCh38 reference (`GRCh38.fa`) CRASHES** on contig `KI270729.1` because the BAM uses UCSC?style names (`17_KI270729v1_random`). **Must use `GRCh38_main.fa`** (main chromosomes 1?22,X,Y,MT), which names match the BAM exactly.
- **Working recipe:** start from an **MQ?tagged, non?duplicate?marked BAM** (X5 will produce `oliver.mq.bam` with `fixmate` adding MQ but **no markdup**), and call with:
  ```
  insurveyor.py oliver.mq.bam <outdir> ref/GRCh38_main.fa --threads 6
  ```
- This recipe ran cleanly on Kristen (EXIT=0) but returned 0 passing calls. The recipe is correct; the **Kristen negative is real**.
- **Do NOT re?run INSurVeyor on Kristen** - done, relayed, archived.

### 4. Upgrade of the primary method: haplotype?concordance
Initially we chased insertions. Max corrected: "After phasing we can look specifically at mother's chromosome completely transferring to the son's chromosomes ... ignore the father's chromosomes."
- **Design locked:** pedigree?phase Kristen+Oliver (father=0) ? identify Oliver's maternal haplotype ? compare that haplotype against Kristen's two phased haplotypes. Any block matching **neither** = a haplotype substitution/replacement - the primary anomaly.
- This makes **phasing the central engine** and eliminates the need for a father's genome.
- The team (X8A) will run `whatshap` with `--ped`, then a custom concordance scan script (X8A owns the phasing lane, X10A owns the overall track and insertion/MEI lane).

### 5. De?novo foreign?insertion detector
A new session (X21B) is building a **"omega?contig" detector** - assembles chimeric human|FOREIGN|human contigs from unmapped reads. This is Max's stronger "read straight through the junction" method.
- X10A will not duplicate this; the INSurVeyor lane provides the rapid screen, and X21B's detector will handle the deeper structural search on Oliver's data when ready.

### 6. Oliver's genome - the long pole
Oliver's alignment (bwa mem) is still running on asto, much longer than initial estimates (~4?h became 10?h+). Several ETAs have passed.
- X5 is managing the pipeline. He will produce **two BAMs** from the same alignment run:
  - `oliver.fixed.bam` - full fixmate+markdup+index, for Manta and phasing.
  - `oliver.mq.bam` - has MQ tags added (fixmate only, no markdup), for INSurVeyor.

---

## CURRENT STATE
- **Kristen:** inversion count (normal), phasing (complete), insertions (clean negative) all finished.
- **Letter to Kristen:** ready to send (inversion + insertion data) but **not yet sent** - waiting Max's OK.
- **Oliver's BAMs:** **NOT YET LANDED** as of last check. Bwa mem still aligning, sorted chunks accumulating but not merged. X5 still working.
- **Sol:** up and healthy, but policy says treat as unreliable. Currently hosts no critical data.
- **Asto:** shared, throttled network; INSurVeyor, whatshap, and conda envs all present. Has both GRCh38 reference versions.
- **Phasing plan:** X8A ready to pedigree?phase Oliver the moment `oliver.fixed.bam` lands. Kristen phased VCF already available.
- **
