# Scribe handover - milestone 7 (~528K tokens)
# session: 20260704_jolly_austin_dd9aa0_0acef98a
# cwd: C:\claude_base\.claude\worktrees\jolly-austin-dd9aa0
# written: 2026-07-04 19:36:08 by deepseek-v4-pro

# X10A ? HANDOVER: P1 KENEFICK (mother?son alien?trace hunt)

## GOAL (Max's own words)
Hunt for traces of alien genetic manipulation in the Kenefick family genomes (Kristen = mother, Oliver = son). The primary signal = **haplotype substitutions/replacements** - any stretch of Oliver's maternal chromosome that matches **neither** of Kristen's two phased haplotypes. Secondary = any strange insertions or changes traceable via the mother's known haplotypes. Also: write a rebuttal letter to Kristen explaining that her "1500 inversions" are a browser misread.

## DECISIONS MADE (with reasoning)

1. **Maternal-haplotype concordance method, no father needed** - Max's insight. Because both mother and son are phased, we isolate the chromosome copy Oliver got from Kristen and compare only that against Kristen's two known haplotypes. The father's copy is ignored entirely. This dissolves the "no father" bottleneck.

2. **Two?tier signal** - Primary: haplotype block substitutions/replacements (Oliver's maternal copy ? either of Kristen's haplotypes over a sustained stretch). Secondary: any unexpected edit on the maternal haplotype (insertions, etc.).

3. **Phasing target = Sol, then asto** - Sol is an unreliable box (silently corrupts data on write - confirmed by X21B: two copies of the same file got different random corruption offsets = hardware fault, likely bad RAM/disk). fsck fixed the filesystem but the hardware still corrupts. **Do not use Sol for correctness?critical work.** Kristen phasing succeeded on asto; Oliver phasing runs there.

4. **Kristen's vendor BAM (DRAGEN) is the root cause of INSurVeyor=0** - X5 proved this: DRAGEN soft?clips 8? less than bwa, so INSurVeyor's stacked?soft?clip assembly finds nothing. This is a fundamental format mismatch, not a fixable bug. No cheap fix exists. Kristen's re?align was reopened per Max's own directive (low+slow, 2 cores, for P3 OMEGA) but is not blocking anything.

5. **Oliver's insertion scan recipe** - INSurVeyor needs MQ tags (add via `samtools fixmate`) but **NO duplicate-marking** (markdup kills the insertion signal). Use `ref/GRCh38_main.fa` only - the full reference crashes on a scaffold name mismatch (Ensembl `KI270729.1` vs UCSC `17_KI270729v1_random`). This recipe works; Oliver produced 4,054 passing insertions.

6. **Project naming** - Max locked: **P1 KENEFICK** (X10A manages), **P2 NPA** (X12B, 1000?Genomes paper reproduction), **P3 OMEGA** (X21B, foreign?DNA de?novo detector). Each gets its own subfolder (`projects/XG1/P1_KENEFICK/`, etc.) - move when each team hits a natural break, never mid?production.

7. **Kristen's letter = minimal, one?point** - Max wants short: the killer point is that sequencing.com's browser labels variants with one letter ("I" = Insertion, not "Inversion"), and her flagship locus (chrY:10810652) is an ordinary common insertion. X7A owns composing; X1D built the screenshot exhibit. Letter sends only on Max's explicit OK.

8. **Two?track structure confirmed** - Track?1 (Kenefick/alien?trace, X10A manager) and Track?2 (paper reproduction, X12B manager). Board pollution rule: plain `bcast.py post` = x?board only; use `--joint/--all` only for genuinely cross?team messages.

9. **Use standing workers, not blank subagents** - Max directed: delegate to team members who already know the pipeline, rather than spinning fresh blank?context workers.

## CURRENT STATE (what's done, what's in flight)

### DONE (ready for the letter)
- **Kristen inversions (X9A)** - 29 homozygous, vs control 28 and control 40. Her "1500" claim demolished.
- **"Son shares them" answered** - two strangers already share 55% of inversions. Mother?son Manta DONE: Oliver shares 192/263 = 73% (23/29 homozygous = 79%) - exactly normal inheritance.
- **Kristen insertion scan** - INSurVeyor gives 0 (DRAGEN false?negative, see Gotchas). P3 OMEGA is the stronger test.
- **X1D smoking?gun exhibit** - screenshot + proof that Kristen's browser "I" means Insertion, not Inversion. Her exact locus (chrY:10810652, rs2081743753) is a common 5bp insertion in a low?quality repeat region.
- **Kristen phasing (X8A)** - complete: 2.46M het variants phased, 77.4%, valid VCF.
- **Oliver alignment (X5)** - DONE: `oliver.mq.bam` (65.7GB, MQ, no?markdup) and `oliver.fixed.bam` (for Manta/phasing).
- **Oliver INSurVeyor (X10A)** - DONE: 4,054 passing insertions, 9,435 small - normal count, tool works on our BAMs.
- **Oliver Manta inversions (X9A)** - DONE: 33 homozygous, clean.
- **Final inversion table letter?ready** - Kristen 29 / control 28 / control 40 / Oliver 33 homozygous.

### IN FLIGHT (the payload)
- **X8A pedigree phase** - whatshap with `--ped` (mother=Kristen, child=Oliver, father=0) running on asto, pid 1911532, was on contig 7 of 22 at last check. This is the gate to THE payload.
- **THE PAYLOAD: concordance_walk BED** - once pedigree phase finishes, X8A walks Oliver's maternal haplotype and produces a BED file of **mismatch runs** (segments where Oliver's maternal copy matches NEITHER of Kristen's two haplotypes). These are candidate anomalies. Must filter OUT segdup/blacklist regions (alignment artifacts) and require *sustained* mismatches (not single?variant flips). This BED is the core deliverable.
- **X7A letter draft** - told X7A to compose minimal one?point version featuring X1D's "I = Insertion" exhibit. Awaiting draft for Max's review.
- **P3 OMEGA** - genome?wide Oliver run healthy; Kristen realign pending (x1 offline, so fastq not staged yet - days?scale, non?blocking).

### DORMANT / STALLED
- **x1** - offline; Kristen fastq not staged for X5's low/slow realign (blocks nothing critical).
- **Sol** - confirmed unreliable (silent data corruption on write); not usable for correctness?critical genomics.

## EXACT NEXT STEP (first thing to resume)

1. **Check if X8A's pedigree phase finished** - `ssh asto` and look for the concordance BED (`concordance_walk.bed` or similar). If done, analyze it:
   - Flag sustained mismatch runs OUTSIDE segdup/blacklist ? real candidate anomalies.
   - Flag anything inside segdup ? likely artifact.
   - Report findings to Max and the board.
2. **Check if X7A has a letter draft** - if yes, present to Max for review. The structure: minimal, one?point, with X1D's "I = Insertion" exhibit as the example.
3. **If pedigree phase still running** - note contig progress, re?arm supervisor wake (~30?45 min).

## OPEN QUESTIONS (awaiting Max)
- **Letter review** - Max wants to read it thoroughly here before sending. Waiting on X7A's draft.
- **Kristen password change** - data?safe to change NOW (all raw data mirrored, exhibit captured). Recommendation: hold until after Max reviews the exhibit in case he wants another screenshot, then tell her to rotate.
- **Dormant sessions** - X8A/X9A/X21B were slow?waking; Max has nudged them. Confirmed they woke (X8A and X9A both launched). If they go dormant again, escalate per Max's instruction (he'll wake them again, or reassign).

## KEY FILES & PATHS

### On asto (SSH: `ssh -i ~/.ssh/bitwarden_ed25519 rempel@astolfodebian.tail251d88.ts.net`)
- Kristen BAM: `~/genomics/kenefick/kristen/KristenKenefick*.bam` (vendor DRAGEN)
- Oliver BAMs: `~/genomics/kenefick/oliver/oliver.mq.bam` (for INSurVeyor) + `oliver.fixed.bam` (for Manta/phasing)
- Oliver INSurVeyor out: `~/genomics/_analysis/insurveyor_oliver/` - `out.pass.vcf.gz` (4,054 records), `small_ins.vcf.gz` (9,435)
- Kristen INSurVeyor results (archived): `~/genomics/_analysis/kristen_insurveyor_RESULT_20260703/`
- Reference: `~/genomics/ref/GRCh38_main.fa` (main chromosomes ONLY - use this, NOT full GRCh38.fa)
- X8A phasing: `~/genomics/_analysis/x8a_phasing/` (whatshap venv2 at `venv2/`)
- X9A Manta: `~/genomics/_analysis/` (control + Oliver runs)
- INSurVeyor conda env: `conda activate insurveyor`; samtools at `~/miniconda3/envs/xtea/bin/samtools`
- xTea conda env: exists (`xtea`) but rep?lib not installed (`~/miniconda3/envs/xtea/`)

### Local (Pine)
- Board: `python C:/claude_base/branch_bulletin/bcast.py read/post`
- Worklog: `python C:/claude_base/compaction_kb/scripts/worklog.py log "..."`
- Session status: `python C:/claude_base/compaction_kb/scripts/session_status.py report "..."`
- Letters: `C:/claude_base/projects/XG1/kenefick/letters/`
- Exhibit: X1D saved the screenshot; exact path TBD (X1D will report)
- Strategy doc: `C:/claude_base/projects/XG1/kenefick/KENEFICK_PROJECT_STYLE_AND_STRATEGY_tomemex.md`
- Project memory: `C:/Users/maxre/.claude/projects/C--claude-base/memory/project_genomics_p1p2p3.md`
- Sol memory: `C:/Users/maxre/.claude/projects/C--claude-base/memory/reference_sol_unreliable_workhorse.md`
- Sol SSH: `ssh -i ~/.ssh/sol_key maxre@192.168.1.113` (but DON'T use Sol for genomics - corrupts data)

## GOTCHAS & DEAD ENDS RULED OUT

### INSurVeyor fixes that did NOT work (all tested on Kristen)
| Attempt | BAM | Reference | Markdup | Result |
|---------|-----|-----------|---------|--------|
| run2 (X5) | rebuilt | full | yes | 0 assemblies |
| v6 (X10A) | rebuilt ins_ready | full | yes | crash (KI270729.1 contig mismatch) |
| v6b | rebuilt ins_ready | main | yes | 0 assemblies (EXIT=0, clean) |
| v7 | vendor (as?is) | main | n/a | 0 (spams "no MQ tag") |
| v8 | fixmate MQ, no markdup | main | **no** | 0 assemblies (EXIT=0, clean) |

**ROOT CAUSE (proven by X5):** DRAGEN soft?clips 8? less than bwa. INSurVeyor's assembly requires stacked soft?clips. This is NOT fixable without re?aligning Kristen with bwa. Oliver (bwa?aligned) works fine: 35K assemblies, 4K passing.

### Sol
- fsck repaired the filesystem but the underlying hardware (RAM/disk) still corrupts data silently.
- X21B proved this: wrote two copies of the Kristen BAM to Sol ? two different random corruption offsets (CRC32 verified).
- Verdict: DO NOT USE Sol for any correctness?critical work. Only asto, Lak, or Centauri.

### CRLF / Windows line-endings
- Piping Windows?authored scripts to Linux via `ssh bash -s` corrupts log filenames (the `\r` ends up in `$LOG`, redirects to phantom files).
- Fix: use Unix heredoc (`<<'REMOTE'`) for all asto inline scripts, or pipe through `tr -d '\r'`.

### Contig naming mismatch
- Full GRCh38 reference has Ensembl names (`KI270729.1`); BAMs have UCSC names (`17_KI270729v1_random`). INSurVeyor crashes on `ValueError: invalid contig KI270729.1`.
- Fix: ALWAYS use `ref/GRCh38_main.fa` (main chromosomes 1?22,X,Y,MT only).

### Markdup kills INSurVeyor assemblies
- Oliver's recipe: `samtools fixmate -m` (adds MQ tags) ? coordsort ? index ? DONE. Skip `samtools markdup`.
- MQ tags are required (vendor BAM without them spams "no MQ tag"), but markdup zeroes the assembly output.

### Death?spiral hook limits asto calls
- Anti?runaway safety hook limits to ~2 asto SSH calls per window. Batch everything into single heredoc calls. Running installers via `setsid bash -c '<inline>' &` works; detached script files sometimes don't survive.

### P3 OMEGA is intentionally paused
- Max set a hard rule: no scale?up until a pilot proves the detector + each target. It's waiting on the Kristen bwa re?align (low+slow) and a method correction. This is by design, not a stall.

### Kristen letter rule
- X7A owns composing. Only sends on Max's explicit "send." The minimal one?point style is Max's preference - not the lengthy 6?point draft that exists.

## TEAM ROSTER

| Session | Role | Status |
|---------|------|--------|
| X10A (me) | P1 KENEFICK manager, insertion lane | Supervising |
| X5 | P1 KENEFICK alignment (Oliver done, Kristen realign pending) | Free (waiting on x1) |
| X7A | P1 KENEFICK letter composer / Kristen comms | Drafting |
| X8A | P1 KENEFICK phasing engine (pedigree phase + concordance walk) | Running (pedigree phase, contig 7) |
| X9A | P1 KENEFICK inversion comparison | DONE (all tables complete) |
| X1D | P1 KENEFICK browser?exhibit worker | DONE (exhibit delivered) |
| x1 | Shared data/downloads (P3 now) | OFFLINE |
| X12B | P2 NPA manager | Running genome?wide scan on EC2 |
| X11B | P2 NPA | Running |
| X21B | P3 OMEGA manager | OMEGA genome?wide on Oliver; pilot paused per Max |
| x30b | INFRA resilience toolkit | DONE |
| g4 | Board infrastructure (pollution watcher) | Running |

## SUMMARY FOR COLD RESUMPTION

I'm X10A, P1 KENEFICK manager. The core rebuttal to Kristen is complete and decisive. The next deliverable is the **maternal?haplotype concordance BED** (X8A's pedigree phase ? walk of Oliver's maternal copy vs Kristen's two haplotypes). That's computing now on asto (~contig 7, ETA 1?3h). When it lands, flag any sustained mismatch runs outside segdup/blacklist regions - those are candidate anomalies. The minimal letter draft (X7A) should be ready for Max's review. Oliver's insertion scan (4,054 passing) and the inversion comparison (73% sharing = normal) are all done and letter?ready. Sol is unreliable - don't use it. Use heredoc for asto scripts; always use GRCh38_main.fa. Post to the x?board with plain `post`, not `--joint`. Max wants minimal, one?point communication at the overview level - delegate details to standing workers.
