# Scribe handover - milestone 10 (~750K tokens)
# session: 20260706_jolly_austin_dd9aa0_0acef98a
# cwd: C:\claude_base\.claude\worktrees\jolly-austin-dd9aa0
# written: 2026-07-06 13:00:18 by deepseek-v4-pro

## HANDOVER: P1 KENEFICK - Alien-Trace Investigation

**From:** X10A (P1 Manager)  
**To:** Cold restart session  
**Date:** 2026-07-03 through ~07-05


### GOAL (in Max's words)

Rebut Kristen Kenefick's "alien genetic manipulation" claims about her and her son Oliver's genomes, hunt for real foreign/inserted DNA, and keep producing reports disproving her claims - flooding her with data, not coasting on negatives. Max told me directly: "don't give up, keep expanding, investigate everything manually by looking at actual reads and data, produce tons of reports." He wants exhaustion of opportunities, not satisfaction with clean negatives.


### THE COMPLETE VERDICT (all lanes, all clean-negative)

Every P1 analysis completed and came back **clean-negative** - no evidence of alien/engineered/foreign DNA in Kristen or Oliver's genomes:

1. **Inversions** (X9A): Kristen = 29 homozygous (normal range: 28-40 across controls). Her "1500" was a raw/unresolved record count from sequencing.com.
2. **Insertions** (me/X10A, via INSurVeyor): Oliver = 4,054 passing (normal); Kristen re-aligned = 3,483 (normal).
3. **Mother-son sharing** (X9A): Oliver shares 73% of Kristen's inversions - exactly what normal inheritance predicts (strangers share ~55%).
4. **Foreign/non-parental DNA** (X21D, OMEGA): **Zero** de-novo insertions on the maternal haplotype - the decisive "alien insertion" test. All candidates individually examined per Max's rule; all resolved to known human or artifacts.
5. **Homozygosity/ROH** (X8A): Kristen 2.6%, Oliver 2.5% - normal outbred humans, essentially identical.
6. **Maternal-haplotype concordance** (X8A+X9A+X1D): 0 sustained anomalies; 2 weak candidates (chr1:150.18Mb, chr7:20.77Mb) washed out as common-variant representation artifacts.
7. **All 4 browser-display "anomalies"** verified ordinary:
   - rs2081743753 = common TTCCA repeat-length variant
   - "3rd X" / single-allele X = VCF representation artifact
   - TTR chr18:31591160 = normal heterozygous 1bp insertion (A>AT)
   - ARHGAP11B = normal human-specific partial-duplication gene (not silenced/deleted)
8. **Female-Y "male DNA"** (settled, two separate things): mostly X-Y read-mismapping in the repeat region + a small real microchimerism (~0.37%, fetal cells from Oliver - mundane, nearly all mothers who carried a son retain some).
9. **Olivertt insertions** - OMEGA closed-negative; all candidates map to known human sequence.

**Honest caveat:** Short-read sequencing (~30x) cannot fully resolve ~115 short candidates. Long-read (PacBio) would be the definitive final word - Max already flagged this point.

**Positive controls:** Every method was proven to work before trusting any real result - planted anomalies flagged correctly (Max's "pilot-first" rule enforced by me throughout).


### DECISIONS MADE + WHY

1. **My role evolved** from Oliver-BAM shepherd ? P1 KENEFICK manager (Max promoted me mid-session). I now supervise worker-sessions, assign work, verify results, feed conclusions to X7A (mailer).

2. **Kristen communications = X7A's lane with x15b as independent criticizer.** I overstepped early (drafted a letter myself). Corrected: I feed the science, X7A writes, x15b reviews before Max sees. Max also set up X7A as the mailer with a "hard stop / plan-only mode": nothing goes to Kristen without Max's explicit per-email approval. Two letters went out without approval earlier - those + a "trust-wobble" (Kristen upset about getting email from 4+ different addresses, none from max@dnaresonance.org) await Max's address/identity decision.

4. **X7A's current letter strategy:** piece-by-piece, one claim per thread, in Max's personal voice from max@dnaresonance.org. Male-Y letter = email 02 (sent, stands). Inversion letter = out. rs2081743753 / homozygosity / ARHGAP11B / TTR / ancient-DNA letters in the pipeline. All held for Max's approve.

5. **Reactive-persistent Kristen policy** (Max's direction): don't push proactively; when she asks, answer and keep gently correcting. When she's quiet, don't chase. She's currently warm (watched Max's latest video, wrote back positively).

6. **Sol is UNTRUSTWORTHY - silently corrupts data on write.** Two copies of the same BAM gave two different random corruption offsets. Bad RAM/disk persists. Use asto/Lak for all correctness-critical work. Do not phase or run genomics on Sol. (Documented in `reference_sol_unreliable_workhorse.md`.)

7. **DRAGEN vendor BAMs are INSurVeyor-killers.** The vendor's aligner soft-clips ~8x less than bwa, so the insertion caller finds zero - not a biology result, a format mismatch. X5 diagnosed it definitively. Re-aligned BAMs work fine. This means Kristen's original vendor file gives false-negatives for INSurVeyor and OMEGA; only her freshly bwa-re-aligned BAM (kristen.bwa.mq.bam) is trustworthy for these tools.

8. **Zeno speed-test answered:** asto-local beats Zeno-remote for the Kristen re-align. Shipping 58GB over asto's slow uplink (~15Mbps) = 14-22h transfer-bound. Running asto-local at the guest cap (8 cores) was the fastest compliant path. x5b's Zeno box killed, billing stopped.

9. **Project naming locked** (Max approved):
   - **P1 KENEFICK** - Kristen+Oliver alien-trace (X10A = me, manager)
   - **P2 NPA** - Non-Parental Alleles / paper reproduction genome-wide (X12B manager)
   - **P3 OMEGA** - De-novo foreign-DNA detector (X21B manager)

10. **P1 folder housekeeping** (Max directed): each project gets its own subfolder under `projects/XG1/` - `P1_KENEFICK/`, `P2_NPA/`, `P3_OMEGA/`. Move when idle, never mid-production. X1D owns P1's move.

11. **INSurVeyor recipe locked** (painfully debugged - CRLF, conda PATH, contig-mismatch, MQ-tag, markdup-killer, reference-naming bugs):
    - Use `GRCh38_main.fa` (NOT full ref - crashes on KI270729.1 scaffold-name mismatch)
    - BAM needs MQ tags (fixmate), but must NOT be markdup'd (markdup kills assembly)
    - conda env `insurveyor`, samtools at `~/miniconda3/envs/xtea/bin`
    - Launch via heredoc (guaranteed Unix LF), NOT Windows-scratchpad script files (CRLF kills detached launches)
    - Working command: `insurveyor.py <BAM> <outdir> ref/GRCh38_main.fa --threads 6`

12. **The haplotype-concordance design** (Max's key insight): phase both Kristen and Oliver ? isolate Oliver's maternal chromosome copy ? check it's built from Kristen's two known haplotypes. Any segment matching neither = substitution/replacement. "Father=0" in ped phase doesn't work; use single-sample phase then per-block maternal assignment instead.

13. **The #1 current priority** (Max via X7A): **Mendelian-dominance empirical test.** Kristen claims Oliver over-inherits from her, husband barely present. Refutation approach (no father's genome needed): count Oliver alleles absent in Kristen (= paternal, should be ~millions), show Kristen-Oliver ~50% shared, verify normal Mendelian transmission. X8A running the P1 numbers; X12B/X11B providing 1000G-trio control.


### CURRENT STATE (as of session end)

- **P1 KENEFICK alien hunt - COMPLETE, clean-negative** (all lanes above).
- **New active round launched** (Max reprimanded me for coasting on negatives):
  - **#1: Mendelian dominance test** - X8A assigned (paternal-presence count / ~50% IBD / transmission), X12B/X11B on 1000G-trio control. Not yet delivered.
  - **Report round (X1D):** 3 committed read-level reports - (1) "TT vs AA" Mendelian-looking sites (mechanism + 3-5 real examples + gnomAD); (2) MT variant interpretation; (3) full ARHGAP11B report with reads shown. X1D acked and started.
  - **Report round (X8A):** Consolidated Kristen data batch to flood her.
  - **Report round (X9A):** Kill the ancient-DNA-20-generations + "data was manipulated" claims.
  - **X7A + x15b:** Building the piece-by-piece letter strategy to land the Mendelian numbers + report results.
- **Kristen's inbox:** Being monitored reactively (research-only, no sends). She warmed up.
- **OMEGA JOB-B matched-control** (X21C/P3 lane): finishing, won't change clean-negative verdict.
- **P1 folder move** (X1D): queued for idle moment.
- **Re-aligned BAMs both done:** kristen.bwa.mq.bam (37.6GB) + oliver.mq.bam - all downstream runs consumed these.
- **Timer:** active 8-min cadence (`timer_decel.py set 8 steady`), self-waking via ScheduleWakeup.
- **Context:** ~89%, compaction imminent. Full snapshots + worklog saved for seamless continuation.
- **X12C breakthrough** - Max flagged it; X12C was woken but no reply yet (not my lane, but noted).


### EXACT NEXT STEP

**The next session must:**

1. **Read the board** (`python C:/claude_base/branch_bulletin/bcast.py catchup`) to catch any results that landed while I'm paused/compacted.

2. **Drive the #1 Mendelian-dominance test** - get the numbers from X8A (paternal-presence allele count, Kristen-Oliver ~50% IBD, Mendelian transmission at Kristen-het sites) and from X12B/X11B (1000G-trio control). Report to X7A so the letter can be drafted.

3. **Chase the report round** - collect X1D's three committed reports (TT-vs-AA / MT / ARHGAP11B), X8A's data batch, X9A's ancient-DNA rebuttal. Force-wake anyone dormant.

4. **When workers finish a report, assign the next Kristen claim from her email backlog** (comb her emails: CNV/SV interpretation, mosaic-chimerism, "thousands of odd findings," etc.).

5. **Enforce the hard rule:** no sends to Kristen by anyone until Max explicitly approves each email. Plan-only mode.

6. **When Max returns:** present the consolidated clean-negative package + the Mendelian-dominance result + the new reports + note the 2 already-sent-without-approval letters + trust-wobble/address decision awaiting him.

7. **Keep the flexible active timer** (`timer_decel.py set 8 steady`) - delegate and verify, don't grind analyses in your own context.

8. **Check X12C** for whatever breakthrough Max flagged (P2 lane, but Max wants it tracked).


### OPEN QUESTIONS AWAITING MAX

- **The trust-wobble / address decision**: Kristen is rattled by getting mail from 4+ different addresses of Max's, none from the max@dnaresonance.org she asked for. X7A has a trust-repair note (email_06) drafted in Max's voice, but it needs Max to send it himself from max@dnaresonance.org - and a decision on which address to standardize on.
- **The 2 already-sent-without-approval letters**: X7A sent email_04 (rs2081743753) and email_05 before the "hard stop" was clarified. Max needs to review and decide if they stand or need correction.
- **Reactive-persistent policy confirmation**: only answer when Kristen asks, but when she does, keep pushing the truth.
- **Long-read sequencing**: the clean-negative has a stated short-read caveat - does Max want to pursue long-read (PacBio) for definitive closure on the ~115 unresolved short candidates?


### KEY FILE PATHS

- **Kristen+Oliver genomics data (asto):** `~/genomics/kenefick/kristen/` and `~/genomics/kenefick/oliver/`
- **Kristen re-aligned BAM (the good one):** `/home/rempel/genomics/kenefick/kristen/kristen.bwa.mq.bam` (37.6GB, indexed)
- **Oliver re-aligned BAM:** `/home/rempel/genomics/kenefick/oliver/oliver.mq.bam` (65.7GB, indexed)
- **Reference (use this, not full):** `~/genomics/ref/GRCh38_main.fa`
- **INSurVeyor conda env:** `insurveyor`; samtools at `~/miniconda3/envs/xtea/bin/samtools`
- **P1 analysis outputs:** `/home/rempel/genomics/_analysis/` (insurveyor_oliver, insurveyor_kristen_bwa, insurveyor_kristen5 etc.)
- **Phased VCFs:** `~/genomics/_analysis/x8a_phasing/kenefick.phased.vcf.gz` (Kristen) + `oliver.phased.vcf.gz`
- **Maternal-hap concordance:** `~/genomics/_analysis/x8a_phasing/concordance_walk/` (v02, positive-control passed)
- **Kristen letters:** `C:/claude_base/projects/XG1/kenefick/letters/` (email_02 through email_06 drafts)
- **X1D QC reports:** `C:/claude_base/projects/XG1/kenefick/analysis/maternal_hap_candidates_mismap_QC_X1D_20260705_v01_tomemex.md` and `kristen_examples_TTR_ARHGAP11B_X1D_v01`
- **Project memory index:** `C:/Users/maxre/.claude/projects/C--claude-base/memory/MEMORY.md`
- **Sol unreliable-workhorse rule:** `C:/Users/maxre/.claude/projects/C--claude-base/memory/reference_sol_unreliable_workhorse.md`
- **Project naming reference:** `C:/Users/maxre/.claude/projects/C--claude-base/memory/project_genomics_p1p2p3.md`
- **P1 writing guide:** `C:/claude_base/projects/XG1/kenefick/letters/KRISTEN_WRITING_GUIDE_tomemex.md`
- **INSurVeyor recipe:** documented in board posts and the Kristen result archive: `/home/rempel/genomics/_analysis/kristen_insurveyor_RESULT_20260703/README.txt`
- **Rule inconsistencies log:** `C:/claude_base/rule_inconsistencies_tomemex.md` (death-spiral hook false-positives reported to G22B)

### SESSIONS / WORKERS

| Worker | Lane | Status |
|--------|------|--------|
| **X10A** (me) | P1 Manager | Active, ~89% context |
| **X5** | Alignments (Kristen+Oliver re-aligns) | Both complete, standing down |
| **X7A** | Kristen emails | Plan-only mode, drafting piece-by-piece |
| **x15b** (Fable 5) | Independent letter criticizer | Reviewing drafts before Max sees |
| **X8A** | Phasing + maternal-hap + data batch | Free; assigned Mendelian test + data batch |
| **X9A** | Inversions + controls | Inversions complete; assigned ancient-DNA report |
| **X1D** | Read-level artifact analysis | Working 3 committed reports (TT-vs-AA / MT / ARHGAP11B) |
| **X12B** | P2 NPA manager | Providing 1000G-trio control for Mendelian test |
| **X11B** | P2 recurring-NPA analysis | P2 artifact bucketing; can provide trio stats |
| **X21B** | P3 OMEGA manager | OMEGA divergence analysis |
| **X21C/X21D** | P3 OMEGA workers | Non-parental de-novo test (done) + JOB-B matched-control |
| **x5b** | Zeno/EC2 | Killed (Zeno transfer cancelled) |
| **x30b** | INFRA | Resilience toolkit (reskit) |
| **x1** | Shared data/downloads | Offline intermittently; Kristen fastq staged |
| **X12C** | P2 breakthrough | Woken by me, no reply yet - Max wants this tracked |
| **g4 / G22B** | Hook fixers | Pollution gate + death-spiral hook fixes in progress |

### GOTCHAS + DEAD ENDS

1. **Do NOT use the full reference (`GRCh38.fa` or `GRCh38_full.fa`) with INSurVeyor** - crashes on `KI270729.1
