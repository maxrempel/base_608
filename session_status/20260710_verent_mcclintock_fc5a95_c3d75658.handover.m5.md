# Scribe handover - milestone 5 (~406K tokens)
# session: 20260710_verent_mcclintock_fc5a95_c3d75658
# cwd: C:\claude_base\.claude\worktrees\reverent-mcclintock-fc5a95
# written: 2026-07-10 11:51:07 by deepseek-v4-pro

# HANDOVER - OMEGA Insertion Detection, Session X21G (fka X21D / QP3)

---

## GOAL (Max's own words, final reframe)

Two **completely separate** analyses. Never conflate them:

**Analysis 1 - "Rarity vs the general population"** (child AND mother, independently). Catalog **every** insertion/deletion each person carries - exclude nothing. Categorize them (STR/tandem, satellite, Alu, L1, SVA, segdup, novel). For Alu: classify freshness (consensus/young = actively jumping; diverged = interesting old). For EVERY repeat: look at its actual sequence and its population frequency. Ask: which inserts are rare or unknown in the general population? This is about each genome's unusualness, not about inheritance.

**Analysis 2 - "Non-parental / maternal-phased ONLY"** (child only). Phase the child's insertions onto the maternal haplotype. **Dump anything unphaseable** - it's fine to lose lots of data. Among those phased to maternal: flag any absent from the mother = de-novo on the maternal copy. **Fathers ignored entirely.** No "could be paternal" hedging.

Max: *"Alu insertions should be also catalogued - don't exclude them. Include everything, but categorize. Repeats are trivial but catalogued. ALU jumps should be categorized: how fresh, consensus vs diverged, and the actual sequence. If non-consensus, catalog properly."*

---

## DECISIONS MADE + WHY

1. **The old filter (paralog-discard, 150bp floor, 700?16 harsh cut) was wrong.** Max's reframe: a human sequence copied from elsewhere in the genome into a new spot with its own mutations IS the target. Paralog doesn't mean artifact - resolve cleanly with diagnostic markers instead of discarding.

2. **Read-level junction examination is the ground truth**, not blast identity alone. An insertion is real only if reads at the locus show the soft-clip/dangling signature. The batch classifier found 17 of 47 "relocations" had no real junction (assembly artifacts). This QC step is mandatory.

3. **"Son homozygous" = common inherited, NOT alien.** A de-novo/alien insertion would be heterozygous in the son and absent from the mother. This error was caught live - the top-2 candidates were homozygous, making them uninteresting under either analysis.

4. **gnomAD-SV v4.1 needs "chr" prefix** on contig names. Without it, every pysam fetch threw "invalid contig" silently, making all 47 appear absent. Fixed.

5. **gnomAD-SV is blind to segdup/repeat regions** - 33 of 47 insertions fall in areas gnomAD can't call, so T2T-CHM13 second-genome presence check was needed as the resolver.

6. **The 150bp floor excluded a real signal class.** Dropping to 30-50bp on chr22 found the first "not-from-mother" candidates (chr22:21682594 and chr22:20232722) that the main pipeline missed. Max wanted this from the start, and it paid off.

7. **Alu classification uses Dfam-consensus identity.** Young Alu (AluYb8, AluYa5, AluY) at high identity to consensus = still capable of jumping. Non-consensus Alu (AluS, AluJ, diverged AluY) = old, embedded, carried along in segdups - catalogued separately per Max's instruction.

8. **Mother payloads exist but haven't been categorized.** Her reconstruct_all743 output has 1,407 pieces (vs Oliver's 1,107). She hasn't been run through the new categorizer yet.

9. **Small-insertion (30-50bp) pilot on chr22 worked.** 395 events, 24 clusters. Two de-novo-shaped candidates (son-has, mother-clean), one satellite artifact. Not yet scaled genome-wide.

10. **Classified 33/47 insertions as present in T2T-CHM13** = common polymorphisms, not rare. The remaining 14 are in gnomAD-blind regions. The chr12:30348820 candidate is absent from both reference genomes but inherited (mother has identical sequence).

---

## CURRENT STATE - WHAT IS DONE

### Fully delivered:
- **Read-level examination of all 47 relocations**: 30 have real junctions (13 het-inherited, 11 homozygous-inherited, 6 heterogeneous/mismap), 17 are assembly artifacts, **0 de-novo, 0 son-differs-from-mother**.
- **Population frequency via gnomAD-SV v4.1** (63k genomes) for the 15 that land in callable regions.
- **T2T-CHM13 second-genome presence** for all 47: 33 present (common), 14 absent (rare or unresolved).
- **Payload sizes**: mostly Alu-scale 50-300 bp; two large ~770-965 bp.
- **Categorizer built and run on Oliver's 1,107 insertions** (9 classes, see below).
- **Alu freshness analysis** on Oliver: 204 Alu split by subfamily age/consensus-divergence.
- **chr22 small-insertion pilot**: 2 candidates (chr22:21682594, chr22:20232722), mother confirmed clean.
- **Controls spec written** for delegation to PX1/X21C (`CONTROLS_SPEC_for_worker_v01_tomemex.md`).

### Oliver's 1,107 insertions categorized:
| class | count |
|---|---|
| Low-complexity | 262 |
| STR / tandem-repeat expansion | 252 |
| **Unclassified / novel** (no repeat family, low copy) | 215 |
| **Alu** | 204 |
| Segdup / multicopy | 102 |
| **Unique relocated** | 27 |
| LINE / L1 | 26 |
| Satellite | 15 |
| SVA | 4 |

### Alu subfamily breakdown (Oliver):
- **Young/active** (~65): AluYb8 (~36), AluYa5 (~19), AluY (~10) - high consensus identity, capable of jumping
- **Mid-age** (~115): AluSc (~55), other AluS - old copies, not actively jumping
- **Old/dead** (~24): AluJ - ancient, completely fixed

### Not done yet (the gap):
- **Mother's catalog**: her 1,407 payloads need the identical categorizer run.
- **Population frequency attached to all classes** for both individuals - gnomAD-SV checked for 15 relocations but not for the full 1,107/1,407 sets.
- **Analysis 2 (non-parental maternal-phased)**: the phasing pipeline exists (from earlier X8A outputs), but hasn't been applied under the new framework with the full categorized set.
- **Small-insertion scaled genome-wide**: pilot on chr22 only.

---

## EXACT NEXT STEP

**Run the categorizer on the mother's 1,407 payloads first** - this gives the parallel catalog Max demanded (Analysis 1 for mother, independent of the child). The script (`categorize.py`) and Dfam consensi blast DB already exist on asto. The mother's payload fasta and blast TSV are at:
- `/home/rempel/genomics/omega_run/out/genome_kristen/reconstruct_all743/`

Once both catalogs exist, attach population frequency per class, then pivot to Analysis 2 (maternal-phased non-parental check on the child's maternal haplotype).

The categorizer script is exactly the same - it just needs the mother's payload fasta and her blast TSV as input. It blasts each payload vs the 25 repeat consensi, computes identity (freshness), classifies into the 9 buckets.

---

## OPEN QUESTIONS AWAITING MAX

None explicitly - Max said "proceed autonomously" and "I will see you later." The instructions are clear: build both catalogs (child + mother), categorize everything (exclude nothing), attach population frequency, then do the maternal-phased non-parental analysis. If stuck, pop a question when Max checks in.

---

## KEY FILE PATHS & IDS

### Repo (local Windows):
- Report: `C:\claude_base\projects\XG1\kenefick\omega_detector\INSERTION_FREQUENCY_SIZE_REPORT_v01_tomemex.md`
- Controls spec: `C:\claude_base\projects\XG1\kenefick\omega_detector\CONTROLS_SPEC_for_worker_v01_tomemex.md`
- Current worktree: `C:\claude_base\.claude\worktrees\jolly-austin-dd9aa0` (scratchpad path)

### asto (compute box - astolfodebian.tail251d88.ts.net, rempel@, SSH key: `~/.ssh/bitwarden_ed25519`):
- Oliver BAM: `/home/rempel/genomics/kenefick/bam/oliver.mq.bam`
- Mother BAM: `/home/rempel/genomics/kenefick/bam/kristen.bwa.mq.bam`
- Oliver reconstruct: `/home/rempel/genomics/omega_run/out/genome_oliver/reconstruct_all743/`
  - Payload FASTA: `unique_payloads.fa` (1,107 sequences)
  - Blast TSV: `char_blast.tsv` (columns: qseqid, qlen, sseqid, slen, pident, length, ...)
- Mother reconstruct: `/home/rempel/genomics/omega_run/out/genome_kristen/reconstruct_all743/`
  - Same structure, 1,407 payloads
- Dfam consensi + blast DB: `/home/rempel/genomics/omega_run/out/repeat_consensi/`
  - 25 sequences: AluY ? AluS ? AluJ subfamilies, L1, SVA, satellites
- gnomAD-SV v4.1: `/home/rempel/genomics/_analysis/x8a_engscreen/popsv/gnomad_sv_v4.1.sites.vcf.gz` (needs `chr` prefix on contigs)
- T2T-CHM13 assembly + blast DB on asto (path from inventory, used for presence check)
- X8A phasing outputs (for Analysis 2 later):
  - Oliver phased VCF: `/home/rempel/genomics/_analysis/x8a_phasing/oliver.phased.vcf.gz`
  - Mother phased VCF: `/home/rempel/genomics/_analysis/x8a_phasing/kristen.phased.vcf.gz`
  - Maternal-side table: `/home/rempel/genomics/_analysis/x8a_phasing/per_block_maternal_side_min1.tsv`
- pysam lives in the `ubuntu` distrobox container: `distrobox enter ubuntu -- python3`
- Worklog: `python C:/claude_base/compaction_kb/scripts/worklog.py log "message"`

### Key genomic loci:
- **chr12:30348820** - rarest confirmed insertion (absent from both ref genomes, but mother carries identical copy = inherited)
- **chr22:21682594** - 39 bp, son 10 clips / mother 0 (37 clean reads), small-insertion candidate
- **chr22:20232722** - 32 bp, son 6 clips / mother 0 (44 clean reads), small-insertion candidate

---

## GOTCHAS & DEAD ENDS RULED OUT

1. **gnomAD-SV contig names require "chr" prefix.** The VCF uses `chr12` not `12`. Without the prefix, every pysam fetch or tabix query silently returns nothing. The bug was hidden for multiple runs before being caught.

2. **pysam lives in the distrobox ubuntu container**, not the host python. Always prefix with `distrobox enter ubuntu -- python3` or `distrobox enter ubuntu -- bash -lc '...'`.

3. **gnomAD-SV contains giant genome-scale records** (70-117 Mb, AF~0.5) that overlap everything. When fetching a small locus, filter to `SVTYPE == 'INS'` and small SVLEN, otherwise you get false "present" from megabase events.

4. **gnomAD-SV is blind to segdup/repeat regions.** If an insertion is in a segdup, gnomAD won't call it - "absent from gnomAD" does NOT mean rare. The T2T-CHM13 second-genome check is the resolver for these.

5. **"Absent in mother" with short-read data ? de-novo** without phasing proof. The chr22 candidates could be paternally inherited. Max explicitly said: if unphaseable, dump it - don't hedge about fathers.

6. **Online NCBI BLAST from asto is unreliable** - the guest box likely throttles outbound to NCBI. The job never returned after 10+ minutes. Don't rely on it; use local blast DBs instead.

7. **The Dfam API works** (tiny consensus downloads are fine on asto), but RepeatMasker is NOT installed. The custom Dfam-consensi blast approach (25 curated repeat families) was built as the alternative.

8. **asto disk is at 90% (130 GB free).** Large downloads (HPRC pangenome) must route to Centauri (teal16, ~12 TB free). Only small files (consensi, indices) go to asto.

9. **Worktrees get recycled** - the current one is `jolly-austin-dd9aa0`, not the earlier `reverent-mcclintock-fc5a95` or `confident-nobel-40d20b`. Scratchpad paths and temp files from earlier worktrees are gone. The report file in `projects/XG1/` persists.

10. **Dead end: de-novo in the ?150bp relocation set.** Every confirmed insertion with a real junction was shown to be inherited (mother carries the identical sequence, confirmed by read-level comparison). The only "not-from-mother" signals were in the small-insertion class (30-50bp) that the original pipeline excluded.

11. **The session ID changed twice** - X21D ? QP3 ? X21G (current branch name). The board/team name changed from 'omega' to 'qp'. Max
