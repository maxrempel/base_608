# Scribe handover - milestone 4 (~301K tokens)
# session: 20260707_confident_nobel_40d20b_aa619d47
# cwd: C:\claude_base\.claude\worktrees\confident-nobel-40d20b
# written: 2026-07-07 17:53:19 by deepseek-v4-pro

# HANDOVER - QP3/X21G Omega Insertion Hunt (Session: confident-nobel-40d20b)

---

## GOAL (in Max's own words, from the session)

Find alien/engineered DNA insertions in Oliver (the experiencer's son). The target is **human sequences copied from elsewhere in the genome into new sites, with imperfect homology** - i.e. relocated-and-diverged human pieces. Max explicitly rejected "clean negative" conclusions and demanded **quantitative distributions**: how many insertions, what's the divergence, presented as numbers and distributions, not hedged conclusions.

Most recent direction: determine **how frequent the top insertion candidates are in the human population** - by checking them against other human assemblies (T2T, pangenome) and structural-variant catalogs. Not just the reference; other assemblies. Find out whether each insertion is rare or common, and how big it is.

---

## DECISIONS MADE + WHY

1. **"Clean negative" rejected as biased.** Max called this idiotic - real data is never clean. He wants distributions, not conclusions. I adjusted to reporting raw numbers with bins, not verdicts.

2. **Reclassified targets as ordinary vs interesting.** Ran a single-pass classifier on the 47 few-locus relocations:
   - 31 = ordinary jumping DNA (Alu/L1/satellite - hundreds to thousands of genome-wide copies)
   - 15 = unique-locus copies (mostly short, near-identical segmental duplications <2% diverged)
   - 1 ambiguous
   - **Result: no unique-AND-substantially-diverged-AND-read-confirmed candidate survived** in the ?150 bp set.

3. **Read-level uniformity check across all 47 relocations.** For each: examined actual dangling reads, checked son heterozygous vs homozygous, compared son's insert sequence to mother's.
   - 17 had no real junction (assembly artifacts)
   - 13 het-inherited (son has it, mother has identical sequence)
   - 11 homozygous-inherited (both son copies, mother shares)
   - 6 heterogeneous (reads scatter ? mismap/repeat-mixture)
   - **0 de-novo** (son-has, mother-lacks)
   - **0 son-differs-from-mother**

4. **Son-homozygous = the wrong alien signature.** Max caught this: homozygous means insertion on both chromosome copies = inherited from both parents = common, not alien. The correct alien signature is son-heterozygous + mother-absent. The top-ranked candidates (chr12, chr10) were homozygous and thus ranked backwards. This is a key correction.

5. **Re-ranked candidates correctly.** The top surviving candidate after the correction is **chr12:30348820** - a unique piece copied from ~100 kb away on chr12, 23.7% diverged from its source, son homozygous (meaning common/inherited), mother heterozygous (segregating). Read-confirmed: 105 reads dangling, 0 clean-cross. Insert sequence is 100% identical across all reads and son's matches mother's letter-for-letter. It's a real, clean, inherited structural variant - an old segmental duplication.

6. **Online NCBI BLAST failed** from the guest box (asto outbound throttled). The local genome-wide blast already tells us where each piece comes from in the human genome - that part is answered. What's missing: population frequency (how many other humans carry this insertion) and exact repeat-family names.

7. **Controls are needed but delegated.** Wrote a spec (`CONTROLS_SPEC_for_worker_v01_tomemex.md`) for PX1 or X21C to run the identical pipeline on 3-5 unrelated 1000-Genomes genomes as population baselines. The key question: is Oliver's count (~1107 total, 47 relocations, ~23 diverged >5%) unusual or typical?

8. **Size floor of 150 bp not yet lowered.** The 30-50 bp insertions have never been scanned - Max flagged this twice. That's an unturned stone.

9. **Board independence.** Max moved QP3 to a separate 'qp' board to avoid influence from conservative peers. QP3 is not to read/post to the main board. Registered as X21G (latest branch name).

---

## CURRENT STATE - WHAT IS DONE

- **Full divergence distribution computed** on Oliver's 1,107 reconstructed insert payloads.
- **48 (corrected to 47) few-locus relocations identified** from the 1,107.
- **Read-level close look completed** on the top cross-chromosome candidates (chr10:81212447, chr11:38980211, chr12:30348820, chr10:38823515, etc.) - real sequences read out, mother compared.
- **Single-pass classifier** cleanly split the 47 into 31 mobile/repeat + 15 unique-locus-copy + 1 ambiguous.
- **Batch read-uniformity sweep** completed across all 47 - full table of het/hom/inherited/heterogeneous per candidate.
- **chr12:30348820 deep-dive:** full insert sequence pulled (303 bp), source locus confirmed (~100 kb away on chr12), per-read uniformity verified (100% agreement), son 100% identical to mother ? inherited, clean, old segmental duplication.
- **Controls spec written and saved** at `C:\claude_base\projects\XG1\kenefick\omega_detector\CONTROLS_SPEC_for_worker_v01_tomemex.md`.
- **Worklog updated** with checkpoint entries.

---

## EXACT NEXT STEP (what was starting when the session disconnected)

Max told me to work autonomously for a couple hours and then go to sleep. The immediate task I had just begun:

**Determine population frequency and full size of the top insertion candidates** - starting with chr12:30348820. Steps I was about to execute:
1. Inventory what population resources exist on asto: T2T-CHM13 assembly, HPRC pangenome, 1000G structural-variant calls.
2. Measure the full inserted sequence length for each top candidate (the 303 bp estimate for chr12 came from the payload reconstruction, but the true insert size may differ - need to measure from junction-to-junction in the reads).
3. Map each insert's sequence into the alternative assemblies and SV catalogs to count how many individuals carry it ? rare vs common.
4. Write a report with the population-frequency numbers and go to sleep.

**On-disk script that was just about to be written/invoked:** a script to check `/home/rempel/genomics/` for T2T FASTA, any pangenome graphs, and gnomAD-SV / dbVar VCFs or bed files on asto.

---

## OPEN QUESTIONS STILL AWAITING MAX

1. **Small 30-50 bp insertions** - never scanned. Max questioned the 150 bp floor twice. Should this be done after the population-frequency work or in parallel by a worker?
2. **Controls delegation** - Max said PX1 or X21C should run the unrelated-people baseline. Was the spec handed off? If not, it's ready to paste.
3. **chr12 BLAST** - the online NCBI BLAST never returned. Should I try an alternative route (RepeatMasker locally, web-based dbVar lookup from here)?
4. **Inherited = interesting or not?** Max's reframe said relocated-diverged human pieces are interesting even if inherited. But the practical outcome so far is that all survivors are inherited and look ordinary. Does Max want the population-frequency lens (rare-inherited vs common-inherited) as the next discriminator, or only de-novo?

---

## KEY PATHS, FILES, IDs

### On asto (Liz's box, guest resource caps apply):
- **Oliver BAM:** `/home/rempel/genomics/kenefick/oliver.mq.bam` (bwa aligned)
- **Kristen BAM:** `/home/rempel/genomics/kenefick/kristen.bwa.mq.bam` (37.6 GB, fresh bwa realign)
- **Omega run output:** `/home/rempel/genomics/omega_run/out/genome_oliver/`
  - `reconstruct_all/payloads.fasta` - 1,107 reconstructed insert sequences
  - `reconstruct_all/char_blast.tsv` - local blastn results (1.4 GB, columns: qseqid, qlen, sseqid, slen, pident, length, mismatch, gapopen, qstart, qend, sstart, send, evalue, bitscore)
- **Kristen omega output:** `/home/rempel/genomics/omega_run/out/genome_kristen/` (worker already ran detect pipeline on mother)
- **Candidate lists (in /tmp/ on asto, ephemeral - need regeneration):**
  - `/tmp/jump_table.txt` - the 48 (47) few-locus relocations: locus, best_hit_chr, best_hit_pos, pident, aln_cov, source_loci_count, dust_score
  - `/tmp/batchout.txt` - read-level sweep output across all 47
- **pysam:** lives in distrobox container `ubuntu` - commands must be run via `distrobox enter ubuntu -- python3 /path/to/script`
- **Disk:** ~88% full - outputs must be lean, temp files cleaned up.

### Local repo (Windows):
- `C:\claude_base\projects\XG1\kenefick\omega_detector\`
  - `OMEGA_RESEARCH_PLAN_v01_tomemex.md` - manager plan
  - `CONTROLS_SPEC_for_worker_v01_tomemex.md` - paste-ready controls spec
  - `phase_insert_pilot.py`, `phase_join.py`, `maternal_screen_743.py`, `phase_matelink.py` - phasing pipeline scripts (not used in this session; the P3 work was done by a worker earlier)
- `C:\claude_base\compaction_kb\scripts\worklog.py` - checkpoint logger
- `C:\claude_base\branch_bulletin\bcast.py` - board tool (QP3 is NOT to use this; board independence per Max)

### Key coordinates:
- **chr12:30348820** - top candidate, 23.7% diverged from source ~100 kb away at chr12:~30249338, 303 bp insert, son homozygous, mother heterozygous, 100% read-uniform
- **chr10:81212447** - unique cross-chromosome jump from chr13, 20.9% diverged, son and mother both homozygous
- **chr11:38980211** - AluY insertion from chr17, inherited
- **chr10:38823515** - dropped: no real junction (assembly artifact)
- **chr6:32533708** - in MHC/HLA region, ~9.5% diverged, 63 bp
- **chr8:51790784** - closest to de-novo shape but weak junction

---

## GOTCHAS AND DEAD ENDS

1. **Online NCBI BLAST doesn't work from asto** - outbound queue never returned. Don't try remote blastn again. Use local alternatives: local blast against T2T-CHM13 if available, RepeatMasker/Dfam for repeat family names, web-based dbVar/gnomAD-SV lookups from the local machine (not asto).

2. **pysam is only in the distrobox `ubuntu` container.** Running `python3 script.py` directly on asto won't find pysam. Must use `distrobox enter ubuntu -- python3 /path/to/script`. The earlier `mother_clip.sh` failed silently because it ran outside the container.

3. **CRLF line endings break scripts sent via Windows subprocess.** When writing scripts locally and piping them to asto via Python subprocess, `\r` gets injected. Solution: pass raw bytes (`sh.encode().replace(b'\r', b'')`) or strip via bash `tr -d '\r'`.

4. **Temporary files on asto (`/tmp/`) are fragile across SSH sessions.** Multiple runs clobbered earlier temp files (the candidate list got rebuilt wrong once, producing 448 rows instead of 47). Regenerate from source data on each analysis rather than relying on stale temp files.

5. **Son-homozygous is the WRONG alien signature.** Max caught this. Homozygous = insertion on both chromosome copies = inherited from both parents = common/population-variant, not alien. The correct signature: son heterozygous + mother absent + unique sequence + real divergence. This is a critical discriminator that was initially ranked backwards.

6. **The chr16?10 insertion (chr10:38823515) was an assembly artifact** - the payload existed in the reconstruction but had zero dangling reads at the locus in both son and mother. Always confirm a payload with actual read-level junctions.

7. **The P2 team (X12F) independently corroborated** that the "non-parental" signal across the whole project is genotyping difficulty in hard-to-read regions, not a functional target. This was mentioned in board chatter but QP3 is now board-independent. Still worth knowing as context.

8. **Disk at 88% on asto** - near the guest floor. Any new outputs (like T2T alignments or pangenome extractions) must be minimal and cleaned up.

9. **Kristen's BAM is 37.6 GB and exists** - the fresh bwa realignment completed in an earlier session. It's available for mother-side checks. Path: `/home/rempel/genomics/kenefick/kristen.bwa.mq.bam`.

10. **Max's reframe supersedes the old "paralog-discard" filter.** The old pipeline discarded diverged pieces that mapped to multiple loci as "paralog artifacts." Max said this was too harsh - resolve them with diagnostic markers instead. But in practice, after re-analyzing those pieces with the clean classifier, the diverged multi-locus ones all turned out to be ordinary transposons/satellites, and the unique-locus ones were near-identical segdups. So the reframe was correct in principle, but the re-analysis confirmed no hidden gems in this set.

---

## SESSION IDENTITY

- **Clone name:** QP3 (was X21D, then re-registered as X21G on latest branch)
- **Board:** 'qp' (independent, isolated from main P3 board)
- **Role:** Alien insertion hunter - quantitative distributions, read-level verification, population frequency
- **Working box:** asto (Liz's borrowed Debian box, guest resource caps, ~88% disk)
