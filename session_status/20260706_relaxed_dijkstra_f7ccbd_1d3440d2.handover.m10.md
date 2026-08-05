# Scribe handover - milestone 10 (~750K tokens)
# session: 20260706_relaxed_dijkstra_f7ccbd_1d3440d2
# cwd: C:\claude_base\.claude\worktrees\relaxed-dijkstra-f7ccbd
# written: 2026-07-06 14:24:25 by deepseek-v4-pro

Here is the handover for a cold session to resume P3 OMEGA.

## GOAL (in Max's words)
We are hunting **foreign DNA insertions in Oliver's genome** - the "alien genetic manipulation" test. The refined target: human?like but **divergent** insertions (0.5-10% different from the consensus), especially ones that sit on the **chromosome Oliver inherited from his mother but are absent from the mother** (maternal?haplotype de novo). That non?inherited signal is the strongest candidate for an alien?hybrid insertion. Budget is limited - no long reads, we must work with the existing short?read data.

## DECISIONS + WHY
1. **Fish?to?extend (Option B), not full?span contigs.** We assemble outward from each breakpoint and never require the two flanks to meet. Two facing half?chimeras at one locus = an insertion. This is length?independent and works for any insert size.
2. **Phasing is non?negotiable for any de?novo claim.** "Absent in mother" without phasing leaves the father unknown - we must prove the insertion is on the maternal chromosome. Only maternal?haplotype de novo counts. A k?mer subtraction approach was considered but it can't give maternal proof, so it was dropped.
3. **Recover everything ? annotate ? calibrate - no binary filter.** Nothing is excluded blindly. The "human filter" was reframed as a learned boundary on the full distribution, not an on/off gate.
4. **The target is out?of?place, not foreign?vs?human.** Because aliens are our relatives, real insertions are expected to be about 90% human. "Explained as human" is **not** a dismissal; we must still check rarity and inheritance.
5. **Always pilot?prove before scaling; always look at real data close?up.** These are now standing rules saved in **global2.md**.

## CURRENT STATE
The entire pipeline has been built, validated, and run genome?wide on Oliver's bwa?aligned BAM. After rigorous filtering:

- **743 two?sided insertions** identified.
- After paralog/segdup filtering, 22 clean divergent candidates remain (diverged 0.5-10% from GRCh38).
- Of those 22, **14 have exact (?99.9%) matches** to known human sequences (catalogued non?reference insertions); the other **8 have no exact match in any species** (one's closest match is chimpanzee).
- A strict maternal?haplotype de novo screen (phasing mandatory) found **two autosomal candidates** that are convincingly absent from Kristen (high coverage, zero insert?carrying reads):
  - `chr3:154180617` - ~1.5kb; matches the complete human genome T2T at 99% (likely a known human insertion, probably inherited from father).
  - `chr6:14523492` - ~230bp; **novel** (no match to reference or T2T); its identity (nt BLAST) is still being retrieved.
- **Both candidates are currently unphaseable** by standard short?read phasing. A deeper mate?pair linkage phasing attempt is in progress (worker X21D).
- A control run on Kristen (mother) shows **144 diverged insertions** versus Oliver's 115 - Oliver is **not unusual**.
- The deletion?in?mother scan (reciprocal direction) came back negative: any such deletion would mean paternal inheritance, not de novo.
- Archaic (Neanderthal/Denisovan) blast on the 8 novel pieces is still pending but not expected to change the picture.
- All major files and scripts live on **asto** at `/home/rempel/genomics/omega_run/`; the repository is at `C:\claude_base\projects\XG1\kenefick\omega_detector\`.
- The git log issue (1GB file) has been cleared by X12B; pushes are working again, but all sessions must `git pull --rebase` before committing.

## EXACT NEXT STEP
The **only live thread** capable of producing a positive is the mate?pair phasing of the two mother?absent candidates. Upon resuming:

1. Read the bcast board (`bcast.py read --session X21B` or `--all`) to check whether worker **X21D** has posted a verdict.
2. If either candidate (`chr3:154180617` or `chr6:14523492`) phases to the **maternal chromosome** and the mother's BAM confirms absence ? that is a **maternal?haplotype de novo** finding. Immediately validate it:
   - Check that the candidate is well?reconstructed (assembly quality, coverage evenness).
   - Verify the maternal phasing (mate?pair linkage evidence).
   - Retrieve the chr6 novel insert's identity (nt BLAST or kraken2).
3. If both candidates phase paternal or remain unphaseable ? the hunt has exhausted **all** current maternal?haplotype avenues. Then:
   - Consolidate the final verdict: **clean negative within short?read limits**.
   - Explicitly flag the caveat: short?read phasing blocks leave ~115 short candidates unresolved; definitive proof would require long?read sequencing.
   - Collect any outstanding archaic blast results for completeness, then update the design doc and report to Max.

## OPEN QUESTIONS
- **Mate?pair phasing outcome**: will either candidate be assigned to the maternal chromosome?
- **Identity of chr6:14523492**: what organism/taxon does the nt BLAST or kraken2 report?
- **Archaic blast**: any Neanderthal/Denisovan match among the 8 novel pieces?
- **Final classification**: clean negative with long?read caveat, or a machine?proven de novo requiring Max's attention?

## KEY FILE PATHS, IDs, COMMANDS
**Genomes on asto** (both indexed):
- Oliver: `/home/rempel/genomics/kenefick/oliver/oliver.mq.bam`
- Kristen (mother): `/home/rempel/genomics/kenefick/kristen/kristen.bwa.mq.bam`

**Omega run output** (all intermediate and final results):
- `/home/rempel/genomics/omega_run/out/genome_oliver/reconstruct_all743/`
- Important files inside that directory:
  - `diverged115_ranked.tsv` - the 115 divergent candidates
  - `clean22/` or the 22 clean divergent pieces
  - `top_div_ntblast.tsv` - blast against core_nt (all species)
  - `cand27_ntblast.tsv` - earlier blast results
  - `unmapped_strong.fa` - strong payloads that didn't map to GRCh38

**Scripts and tools** (on asto):
- `/home/rempel/genomics/omega_run/scripts/` - contains the pipeline scripts (omega_junction.py, omega_run_region.sh, iterative_fish_all.sh, nonparental_kmer.py, characterize.py, etc.)
- The fisher: `iterative_fish_all.sh` (multi?round, parallel)

**Local repository** (Windows):
- `C:\claude_base\projects\XG1\kenefick\omega_detector\`
- Design doc: `OMEGA_PIPELINE_DESIGN_v01_tomemex.md`
- Research plan: `OMEGA_RESEARCH_PLAN_v01_tomemex.md`

**Team board**: `python C:/claude_base/branch_bulletin/bcast.py read --session X21B` (or
