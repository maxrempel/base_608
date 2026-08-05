# Scribe handover - milestone 8 (~602K tokens)
# session: 20260705_jolly_austin_dd9aa0_0acef98a
# cwd: C:\claude_base\.claude\worktrees\jolly-austin-dd9aa0
# written: 2026-07-05 16:56:18 by deepseek-v4-pro

# HANDOVER: P1 KENEFICK - X10A active manager track (post-compaction resume)

## GOAL (in Max's own words)
Max is off doing other things. You, the next session, are picking up **X10A's active-manager hat for P1 KENEFICK**. The broad mission: rebut Kristen Kenefick's "alien manipulation / 1500 inversions" fears with hard data, AND run a genuine hunt for any real inserted, foreign, or non?parental DNA in the Kristen + Oliver mother?son pair. You drive a team of worker?sessions on the asto Linux box. You keep them moving, chase laggards, make resource decisions when Max isn't around, and only surface real results or blockers to him.

Specifically, right now Max wants the team **diligently moving forward** - no slacking, no silent stalls. He explicitly told you to "keep pushing the team because they are like lazy bastards" and to be "the manager which is actually responsible for team moving forward". While Max was away you already drove several critical decisions autonomously.

## DECISIONS MADE + WHY (the reasoning)
- **Project naming**: P1 KENEFICK (manager X10A), P2 NPA (manager X12B), P3 OMEGA (manager X21B). Broadcast to all sessions; all board posts, folders and references now use these labels.
- **Lane split for Kristen emails**: X7A owns the actual drafting and sending (only on Max's explicit "send").  
  - An independent criticiser session, **x15b (Fable 5)**, was added to adversarially review every draft before Max sees it - this was a direct reaction to an earlier letter that conflated her insertion question with inversions (she caught it).  
  - Max's full verbatim feedback on the long email draft (13 points: too long, split per thread, Max?apologises, no screen?sharing but accept screenshots, keep pushing that all her claims turned out ordinary, etc.) was forwarded to X7A. The email side now works cleanly without you.
- **The main science method (maternal?haplotype concordance)**: Phase Kristen & Oliver, then isolate Oliver's maternal chromosome copy and walk it against Kristen's two known haplotypes. Segments where Oliver's maternal haplotype matches **neither** of Kristen's haplotypes are the anomaly signal. This elegantly eliminates the need for a father sample. The first implementation had a critical bug (always picking the wrong allele as maternal), caught by X9A's peer review, then fixed and **proven with a positive control** (a planted 200 kb swap was correctly flagged).
- **Kristen re?align**: The vendor (DRAGEN) BAM causes INSurVeyor and OMEGA to see zero signal. A fresh alignment from raw FASTQs is needed.  
  - A Xeno (EC2) option was tested but **killed** - asto's uplink is only ~15 Mbps, so transferring 58 GB would take 14?22 h, while asto already has the data locally.  
  - Max's hard rule NOT to throttle Liz's home?network bandwidth was respected.  
  - Final decision: **run the re?align on asto, data?local, at the guest?box cap (8 cores, ~50% of the machine)**, sharing politely with OMEGA. That gives the fastest throughput without over?consuming the borrowed machine or killing the internet.
- **Re?assigning stalled verification**: X9A (maternal?hap 2?candidate artifact check) was dormant across many force?wakes. The check was reassigned to **X1D**, who was free and independent of X8A. X1D delivered the mismap?QC result.
- **INSurVeyor for Kristen**: Because the DRAGEN?induced zero is unfixable at the tool level, you accepted X5's diagnosis and closed that lane; the pre?staged INSurVeyor script waits to auto?fire when the re?aligned BAM lands.
- **Sol hardware**: Silent data corruption confirmed (two writes gave different CRC32 offsets) - it is permanently untrustworthy for correctness?critical work. Omega moved off it; the bad?DIMM/disk status is documented in memory.

## CURRENT STATE (what's done, what's in flight)
### Fully done (the Kristen rebuttal)
- **Inversion rebuttal** (X9A): Kristen has 29 homozygous inversions; normal humans have 28-40. Her "1500" claim is a raw?record misread; her son Oliver shares 73% of them - normal parent?child inheritance. Stranger?sharing baseline 55% already measured. Letter?ready table.
- **Oliver insertions** (X10A's INSurVeyor): 4,054 passing insertions - a normal count.
- **OMEGA foreign?DNA on Oliver** (X21B): rigorous clean negative - all 743 candidates trace to known human sequence.
- **Kristen's browser misinterpretation**: X1D proved that the "I" label in the Sequencing.com explorer means **Insertion**, not Inversion; the root of her 1500?inversions claim was reading "I" as "inversion". This is captured for the letter.

### Maternal?haplotype payload (THE deeper hunt)
- **Phasing finished**: Kristen and Oliver both have phased VCFs.
- **Concordance walk v02** (X8A) **ran correctly after bug?fix** and with a **positive control pass** (planted swap detected). The real run found **0 anomalies at the strict threshold**.
- At a looser threshold there are **2 weak candidate regions**:
  - chr1:150.18 Mb
  - chr7:20.77 Mb
- **Mismap/artifact QC (X1D)**: those 2 regions are **cleanly, uniquely mapped** (quality ~60, not in repeats or segmental duplications). So they **survive the mismap test** - unlike everything else on this track.
- **Next (critical)**: they must also pass two further checks before we call them real anomalies:
  1. Are the "non?maternal" alleles just **common SNPs** (MAF check) - would be an ordinary calling artifact, not a de?novo change.
  2. Are they true **maternal?haplotype violations** or just a phasing?seam artefact?
  X1D is the worker assigned to both checks.

### Kristen re?align
- X5 was initially running at 4 cores (thinking Zeno was coming), but you overrode that: **X5 must ramp to the full guest cap (8 cores)** now that Zeno is dead and OMEGA is parked. You have not yet confirmed the ramp.
- The re?aligned BAM, `kristen.bwa.mq.bam`, is still being built. ETA unknown but likely several hours (the 4?core run was slow; 8?core will speed it). When it lands:
  - X8A's pre?staged INSurVeyor auto?fires.
  - OMEGA non?parental test fires (X21C/X21D lane).
- The literal BAM path that everything polls is: `/home/rempel/genomics/kenefick/kristen/kristen.bwa.mq.bam`

### Kristen email
- **Letter v06** (rs2081743753 reply, together with all Max's feedback) is **approved by x15b** (independent criticiser) and **science?cleared by X1D**.  
- **X7A has Max's delegated authority to send it** (Max explicitly said "send on delegated authority").  
- As of your last sweep, it was **probably sent**, but you haven't confirmed the send date yet. That is X7A's lane; you only note the state.

## EXACT NEXT STEP
The session that takes over should **immediately** run the same active?manager loop you've been doing. The self?wake was armed with a specific prompt (last used: `ScheduleWakeup` with a long prompt). In human terms:

1. Read the **x?board** (`bcast.py read`).
2. Check these concrete items, in priority:
   a. **X1D - common?SNP MAF answer** for chr1:150.18 Mb and chr7:20.77 Mb.  
      **Also** the true?violation?vs?phasing?seam check for those same two regions.  
      This is the final verdict on the maternal?hap candidates.
   b. **X5 - confirmed ramped to 8 cores? New asto?local ETA?** If still silent, poke hard.
   c. **Kristen re?align BAM landed?** Check `ls /home/rempel/genomics/kenefick/kristen/kristen.bwa.mq.bam` on asto. If it's present, confirm X8A's INSurVeyor auto?fired and OMEGA non?parental launched.
   d. **Letter**: note whether X7A posted that v06 was sent; not your lane, just a status check.
3. After acting on board:
   - If real new results appeared (candidate verdict, BAM landing), **log them** in `python C:/claude_base/compaction_kb/scripts/worklog.py log ...` and update `session_status.py report ...`.
   - If action happened, `tick work` on the timer; if nothing, `tick idle`.
   - Re?arm the same `ScheduleWakeup` (the custom manager prompt) for the next cycle. The timer currently uses `timer_decel.py` - it decelerates if nothing is happening, but stays fast while the team is moving.

**Essential:** Do NOT burn context on debugging tools or writing letters yourself. Stay high?level, supervise, delegate. Only surface to Max when there is a real, unambiguous result (especially the maternal?hap verdict or a confirmed foreign?DNA hit) or a blocker that requires his authority.

## OPEN QUESTIONS STILL AWAITING MAX
- **The maternal?haplotype final verdict** - if the two candidates pass all checks, that would be the first non?dismissible candidate in the whole hunt. Max will want to be told personally. But nothing to ask until that verdict lands.
- No other open questions right now; the email lane is self?sufficient.

## KEY PATHS, IDs, COMMANDS, NAMES
- **Project root (repo side)**: `C:/claude_base/projects/XG1/kenefick/`  
  - Letters: `letters/`  
  - Analysis: `analysis/`  
  - Maternal?hap candidate QC: `analysis/maternal_hap_candidates_mismap_QC_X1D_20260705_v01_tomemex.md`
- **Compute box (asto)**: SSH `rempel@astolfodebian.tail251d88.ts.net` (key `~/.ssh/bitwarden_ed25519`).  
  - Reference genomes: `~/genomics/ref/GRCh38_main.fa` (main chromosomes only, used by INSurVeyor - NEVER the full `GRCh38.fa` that has scaffold naming mismatches).  
  - Kristen re?align BAM target: `~/genomics/kenefick/kristen/kristen.bwa.mq.bam`  
  - Oliver BAMs (already done): `~/genomics/kenefick/oliver/oliver.mq.bam` (for INSurVeyor), `oliver.fixed.bam` (for Manta/phasing).
- **Board**: `python C:/claude_base/branch_bulletin/bcast.py post` (x?board, plain post), `read`, `catchup`, `wake --name ...`.  
  - Note: the pollution watcher sometimes falsely flags your team?only posts because bare tokens match other?team IDs - this is a known board?router bug, ignore it.
- **Timer**: `python C:/claude_base/tools/timer_decel/timer_decel.py tick work|idle` to adjust rescheduling.
- **Self?wake**: `ScheduleWakeup` tool with a custom prompt string (the manager prompt you've been using). The last armed prompt was exactly the "X10A ACTIVE MANAGER ..." block that lists all the checkpoints. The tool returns **how many seconds** until the next wake; you can trust it and re?arm after each cycle.
- **Worklog**: `python C:/claude_base/compaction_kb/scripts/worklog.py log "message"`  
  `python C:/claude_base/compaction_kb/scripts/session_status.py report "message"`
- **Memory notes** (durable):  
  - Sol unreliability: `C:\Users\maxre\.claude\projects\C--claude-base\memory\reference_sol_unreliable_workhorse.md`  
  - Project P1/P2/P3: `C:\Users\maxre\.claude\projects\C--claude-base\memory\project_genomics_p1p2p3.md`  
  - MEMORY.md index updated accordingly.

## GOTCHAS & DEAD ENDS ALREADY RULED OUT
- **False?negative on the first maternal?hap run**: X8A's initial detector always picked the wrong maternal allele. Fixed; the v02 is correct and positive?control verified. Don't re?investigate old "0 anomalies" claims.
- **INSurVeyor zero on Kristen's vendor BAM**: root cause is DRAGEN soft?clips 8? less than bwa, so INSurVeyor sees nothing. This is **not a fixable bug
