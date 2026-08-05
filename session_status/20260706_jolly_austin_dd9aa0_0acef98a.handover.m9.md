# Scribe handover - milestone 9 (~677K tokens)
# session: 20260706_jolly_austin_dd9aa0_0acef98a
# cwd: C:\claude_base\.claude\worktrees\jolly-austin-dd9aa0
# written: 2026-07-06 00:16:15 by deepseek-v4-pro

# X10A HANDOVER - P1 KENEFICK (Alien-Trace Hunt)

## GOAL (Max's words)

Max put me (X10A) in charge of **P1 KENEFICK** - the mother-son (Kristen + Oliver) genetic investigation. Two objectives:

1. **Rebut Kristen's extraordinary claims** - she believes her genome shows "~1500 homozygous inversions" and signs of alien genetic manipulation. Every claim she's made needs to be checked against raw data and answered honestly.
2. **Hunt for real alien-trace signatures** - the deeper search: non-parental insertions, haplotype substitutions, foreign DNA integrated into the genome. The primary method Max designed: phase both genomes, isolate Oliver's maternal chromosome copy, and check whether it traces cleanly to Kristen's two known haplotypes. Any segment matching neither = a candidate anomaly.

Secondary: handle Kristen's email correspondence as diplomatic customer support. She's a distrustful customer who's been feeding us claims; we answer when she asks, gently correct her errors, and keep her engaged because her data + energy are fueling the research program.

---

## DECISIONS MADE + WHY

### Sol (Max's desktop, 192.168.1.113)
- **Discovered Sol silently corrupts data on write** - two copies of the same BAM gave two *different* random corruption offsets. The fsck disk repair fixed the filesystem, but the RAM/disk hardware still corrupts under load.
- **RULING: Sol is untrustworthy for any correctness-critical work.** Use asto (the borrowed compute box) or Lak instead. A memory note saved at `reference_sol_unreliable_workhorse.md` records this.
- Sol's old "bad RAM" label in `global2.md` was updated to reflect the current state.

### Kristen's vendor BAM (DRAGEN-aligned) vs re-align
- **The vendor BAM (from Sequencing.com, DRAGEN-aligned) produces false-negatives in INSurVeyor.** Root cause: DRAGEN soft-clips ~8x less than bwa-mem, so INSurVeyor's stacked-soft-clip assembly finds nothing. X5 diagnosed this with hard data.
- **The same vendor BAM also gives false-negatives in P3 OMEGA** (the foreign-DNA detector).
- **DECISION: Re-align Kristen's raw fastq ourselves using bwa-mem** (same method as Oliver). This serves BOTH P1 INSurVeyor AND P3 OMEGA - one re-align fixes two projects' false-negatives.
- The re-align runs on asto at the guest cap (~8 cores, ~50% of the box). A faster Zeno/EC2 path was tested but killed - shipping 58GB over asto's ~15Mbps uplink would take 14-22h (transfer-bound), so asto-local is the fastest compliant path (Liz's bandwidth throttle is a hard rule Max won't override).

### Project naming
- **P1 KENEFICK** - mother-son alien-trace hunt (X10A manages)
- **P2 NPA** - non-parental alleles / 1000-Genomes paper reproduction (X12B manages)
- **P3 OMEGA** - de-novo foreign-DNA detector, chimeric human|FOREIGN|human contigs (X21B manages)
- Saved to memory at `project_genomics_p1p2p3.md`

### Kristen correspondence
- **PLAN-ONLY mode** - NO emails sent to Kristen unless Max explicitly approves each specific email by name. X7A (the mailer) mistakenly sent 2 without approval; corrected, and the rule is now locked.
- **REACTIVE mode** - when Kristen asks a question, we answer and keep gently correcting; when she's quiet, we don't push.
- **Independent criticizer (x15b/Fable 5)** - reviews every draft adversarially before Max sees it, to catch conflation errors like the insertion/inversion mixup that went out in the earlier letter.
- **The earlier letter's centerpiece was WRONG** - we told Kristen she probably misread the browser's "I" (Insertion) as "Inversion." She replied: she KNEW it was an insertion, never claimed it was an inversion, and felt we "diverted" from her real question. X1D's "smoking gun" was us misreading her. The recovery letter (email_06) owns this error.
- **Trust-wobble** - Kristen is rattled by getting mail from 4+ different Max addresses, none from max@dnaresonance.org (the one she asked for). A trust-repair note (email_06) is drafted in Max's voice but REQUIRES Max's identity decision + he must send it from max@dnaresonance.org himself. All sends are held waiting for this.

### INSurVeyor recipe (nailed down through 8 failed runs)
- **Working recipe**: `insurveyor.py <bam> <outdir> ref/GRCh38_main.fa --threads 6`
- Key requirements: BAM must have MQ tags (fixmate adds them), **NO markdup** (markdup kills INSurVeyor's assembly engine), use **main-chromosome reference** (GRCh38_main.fa), NOT the full reference (contig name mismatch between UCSC-style BAM and Ensembl-style full ref causes crashes).
- samtools path: `~/miniconda3/envs/xtea/bin/samtools`
- conda env: `insurveyor`

### Maternal-haplotype payload (the concordance walk)
- **First version (v01) was a FALSE NEGATIVE** - X9A's peer review caught two bugs: the mat-allele assignment always picked allele 1 (ignoring which chromosome copy was maternal), and it compared at heterozygous sites instead of homozygous ones (so the detector couldn't fire).
- **v02: positive-control PASSED** (planted a 200kb synthetic swap - flagged cleanly, zero false positives). Max's pilot-first rule satisfied.
- **Real result: 0 sustained anomalies** at strict threshold; 2 weak candidates at a loose threshold (chr1:150.18Mb, chr7:20.77Mb). X1D verified both: cleanly mapped (MAPQ~60, no repeats/segdup), but the "violation" alleles are **common indels** - a representation-mismatch artifact, not de-novo. Both WASH OUT.
- Final verdict: **clean negative** on maternal-haplotype concordance.

### Microchimerism (female-Y question)
- **FINAL AGREED FRAMING**: TWO separate true things, both ordinary:
  1. The raw Y-read pileup Kristen sees in the browser is mostly X-Y mismapping (reads from elsewhere landing in the Y).
  2. Separately, a real ~0.37% fetal microchimerism IS present (Oliver's cells in Kristen's sample) - measured robustly via rare/private-allele enrichment (z~336), not raw Y-read counting. This is mundane biology (nearly every mother who's carried a son retains a few of his cells).
- The microchimerism finding STANDS - was never retracted.
- Email 02 (the microchimerism letter) is correct and shouldn't be walked back.

---

## CURRENT STATE (everything done vs pending)

### DONE - Rebuttal (all clean-negative)
- **Inversions**: Kristen = 29 homozygous (normal range 28-40; controls 28 and 40; Oliver 33). Her "1500" was likely the browser's raw unresolved record count. "Son shares them" = 73% (ordinary inheritance; strangers share 55%).
- **Insertions (Oliver)**: 4,054 passing (normal human count). Tool works fine on our bwa-aligned BAM.
- **Insertions (Kristen)**: vendor BAM gives false-negative due to DRAGEN soft-clip difference. Re-align pending.
- **Maternal-haplotype concordance**: clean negative (0 sustained anomalies after positive-control validation).
- **All 4 of Kristen's display/paralog claims verified ordinary**: rs2081743753 = common TTCCA repeat-length variant; TTR chr18 = het 1-base insertion (anchor-base misread); ARHGAP11B = normal human-specific partial duplication gene, present at normal depth, not silenced; "I" = Insertion not Inversion.
- **OMEGA Oliver (foreign-DNA)**: clean negative - 743 candidates all resolve to known human sequence.
- **OMEGA divergence angle**: closed-negative - the "diverged" inserts are lower-identity paralog fragments.

### IN FLIGHT - one remaining test
- **Kristen bwa re-align** (`kristen.bwa.mq.bam`): was at **9/12 chunks** at last check, ETA ~1-2h from session end (~12:45am PT). X5 auto-wakes the team when it lands.
- When the BAM lands, **two analyses auto-fire**:
  1. **X8A's INSurVeyor** on `kristen.bwa.mq.bam` - pre-staged, a polling script waits for the BAM and launches automatically (pid 2842829 on asto).
  2. **X21C/X21D OMEGA non-parental** - the decisive foreign-DNA test on Kristen.
- Both are expected to return **clean-negative** (consistent with everything else).

### PARKED
- **Kristen letters**: all held in plan-only mode. X7A has email_06 (trust-repair) drafted, x15b approved psychologically, but needs Max's identity decision + send from max@dnaresonance.org.
- **Two letters already sent without approval** (X7A corrected the process; Max aware).
- **TT-vs-AA and MT deferred claims**: need Kristen to provide exact coordinates (X7A to request when appropriate).

---

## EXACT NEXT STEP

1. **Wait for `kristen.bwa.mq.bam` to land** - X5 auto-wakes the team on completion. When it lands:
   - Confirm X8A's INSurVeyor auto-fired.
   - Confirm X21C/X21D OMEGA non-parental auto-fired.
   - Collect results (expect clean-negative) and consolidate the final P1 verdict.
2. **If Kristen sends a new question**, research the answer (do NOT send - plan only), hold the draft for Max's approval.
3. **When Max returns**: surface the trust-wobble (email_06 needs his identity decision + send from max@dnaresonance.org), the 2 already-sent letters, and the all-clean-negative science summary.

---

## OPEN QUESTIONS AWAITING MAX

1. **Trust-wobble / email_06**: Max needs to decide his identity approach and send the trust-repair note from max@dnaresonance.org himself. X7A holds the draft.
2. **The 2 already-sent letters**: Max should review and decide if any follow-up is needed.
3. **Kristen's password**: she can change it - all data is mirrored, screenshots captured. But Max didn't explicitly tell her; the window to tell her was after reviewing the exhibit.

---

## KEY PATHS, IDs, NAMES

### Files & paths (asto = `rempel@astolfodebian.tail251d88.ts.net`, SSH key `~/.ssh/bitwarden_ed25519`)
- **Oliver BAMs**: `~/genomics/kenefick/oliver/oliver.mq.bam` (MQ, no-markdup - for INSurVeyor) + `oliver.fixed.bam` (marked duplicates - for Manta/phasing)
- **Oliver phased VCF**: `~/genomics/_analysis/x8a_phasing/oliver.phased.vcf.gz` (180MB, single-sample phase)
- **Kristen vendor BAM**: `~/genomics/kenefick/kristen/KristenKenefick*.bam`
- **Kristen re-align target**: `~/genomics/kenefick/kristen/kristen.bwa.mq.bam` (in progress, 9/12 chunks)
- **Reference**: `~/genomics/ref/GRCh38_main.fa` (main chromosomes 1-22,X,Y,MT - use THIS, not the full ref)
- **INSurVeyor outdirs**: `~/genomics/_analysis/insurveyor_kristen6/` (v8, 0 assemblies - vendor BAM), `~/genomics/_analysis/insurveyor_oliver/` (4,054 passing), `~/genomics/_analysis/insurveyor_kristen4/` (v6)
- **Maternal-hap candidates**: chr1:150.18Mb, chr7:20.77Mb (both washed out as common-indel artifacts)
- **Concordance walk**: `~/genomics/_analysis/x8a_phasing/concordance_walk/`
- **Kristen INSurVeyor auto-fire script**: running detached on asto, pid 2842829, polls for `kristen.bwa.mq.bam`
- **Kristen letters**: `C:/claude_base/projects/XG1/kenefick/letters/` - key files: `kristen_email_03_inversions_v03_DRAFT.md` (the too-long one Max rejected), `kristen_email_04_rs2081743753_v03_DRAFT.md` (the detailed recovery draft)
- **Writing guide**: `KRISTEN_WRITING_GUIDE_tomemex.md` (x15b's psych profile + Max's strategic position)
- **X1D reports**: `kristen_examples_TTR_ARHGAP11B_X1D_v01` (committed 2c35c493)
- **X1D maternal-hap QC**: `maternal_hap_candidates_mismap_QC_X1D_20260705_v01_tomemex.md`
- **Saved result archive**: `~/genomics/_analysis/kristen_insurveyor_RESULT_20260703/`
- **Sol memory**: `C:\Users\maxre\.claude\projects\C--claude-base\memory\reference_sol_unreliable_workhorse.md`
- **Project naming**: `C:\Users\maxre\.claude\projects\C--claude-base\memory\project_genomics_p1p2p3.md`
- **MEMORY.md index**: `C:\Users\maxre\.claude\projects\C--claude-base\memory\MEMORY.md`
- **global2.md**: `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md` (Sol section updated)
- **Board**: `C:/claude_base/branch_bulletin/bcast.py` (plain `post` = x-team board; `--joint`/`--all` = global)
- **Timer**: `C:/claude_base/tools/timer_decel/timer_decel.py` (set 10, tick work|idle), currently decelerated to ~3600s fallback
- **Worklog**: `C:/claude_base/compaction_kb/scripts/worklog.py`
- **Session status**: `C:/claude_base/compaction_kb/scripts/session_status.py`

### Sessions / workers
- **X10A** = this session (P1 manager, alien-trace track)
- **X5** - genome builder (alignment, BAM production). Running the Kristen re-align on asto.
- **X7A** - emailer / Kristen comms (holds all sends pending Max approval)
- **X8A** - phasing engine (whatshap, pedigree phase, concordance walk). Pre-staged INSurVeyor auto-fire.
- **X9A** - inversions + control comparison (Manta). May be dormant; its maternal-hap verdict task was reassigned to X1D.
- **X1D** - read-level artifact analysis (browser exhibit, TTR/ARHGAP11B, maternal-hap candidate verification, female-Y read-level check)
- **x1** - downloads/transfers/mirroring (shared across projects; sometimes offline - was the blocker on Kristen re-align staging)
- **x15b / Fable 5** - independent letter criticizer (reviews every Kristen draft adversarially before Max sees it)
- **X12B** - P2 NPA manager (paper reproduction track)
- **X21B/X21C
