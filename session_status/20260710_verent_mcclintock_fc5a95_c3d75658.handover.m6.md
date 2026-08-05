# Scribe handover - milestone 6 (~453K tokens)
# session: 20260710_verent_mcclintock_fc5a95_c3d75658
# cwd: C:\claude_base\.claude\worktrees\reverent-mcclintock-fc5a95
# written: 2026-07-10 12:58:54 by deepseek-v4-pro

# HANDOVER - X21J (was X21D ? QP3 ? X21G ? X21J)

## GOAL (Max's own words, latest direction)

**Two independent analyses, never mixed:**

1. **Rarity vs general population (child AND mother separately).** Take every insertion/deletion each person carries, **categorize ALL of them** - nothing excluded. Alu jumps are included and sub-categorized by freshness (young consensus = actively jumping; old diverged = interesting). STRs catalogued but trivial; satellites catalogued; segdups catalogued. For every repeat, look at the actual sequence and its population frequency. Ask: "what does each person carry, and how unusual is it vs the population?" This is NOT about inheritance.

2. **Non-parental - maternal-phased ONLY.** Phase the child's insertions onto maternal vs paternal chromosome. Dump anything unphaseable (fine to lose lots). Flag insertions on the maternal haplotype that are absent from the mother = de-novo on maternal copy. **Fathers ignored entirely** - no "could be paternal" hedging. If it can't be phased, it's gone.

**Also:** the 150bp size floor was questioned - open up 30-50 bp inserts. And download any missing population data properly (no rush, throttled).

**Cleanup side-mission (X21J):** asto disk was 90% full, over guest cap. Clean it up, coordinate with the Kristen team.

## DECISIONS MADE + WHY

- **Two analyses, cleanly separated:** Because Max said he's "absolutely not interested in father's contributions" for the non-parental analysis, and the rarity-vs-population question is a completely different axis. Conflating them was wrong.

- **Categorize everything, exclude nothing:** Max explicitly rejected the earlier "filter out Alu/repeats" approach. Alu jumps are interesting - especially non-consensus ones. STRs are trivial but must be in the report. The categorizer now classifies into 9 buckets (Alu by subfamily/freshness, L1, SVA, STR, satellite, low-complexity, segdup, unique-relocated, novel/unclassified).

- **Population frequency via gnomAD-SV + T2T-CHM13, not online NCBI BLAST:** Online BLAST from asto failed (throttled). gnomAD-SV v4.1 (63k genomes, with AF) was already on the box. T2T-CHM13 second complete genome + blast db also already there. Together they answer rare-vs-common without any downloads.

- **Keep .fixed BAMs:** Team (X5/X8A) corrected that `oliver.fixed.bam` and `kristen.bwa.fixed.bam` are the mark-dup versions needed for Manta/phasing - NOT duplicates of `.mq` BAMs. Deletion cancelled.

- **teal16 (Centauri) as archive, not AWS:** AWS would cost ~$80+/month for 1 TB EBS storage. teal16 has 16 TB, ~12 TB free, always-on, owned. AWS is only for short rented compute bursts.

- **Kristen cleanup delegated to X8A:** X8A owns Kristen's data, built it, and can coordinate with the team. The cleanup was done from Pine over SSH, with byte-verified copies to teal16 before deletion.

## CURRENT STATE

### Analysis thread (X21G work, parked)
- **Child's 1,107 insertions are now fully categorized** into 9 classes (Alu 204, L1 26, SVA 4, STR 252, satellite 15, low-complexity 262, segdup 102, unique-relocated 27, novel 215). Alu are sub-classed by subfamily age (~65 young/active, ~115 mid, ~24 old).
- **gnomAD-SV frequency attached** to the 47 confirmed relocations (2 common, 1 uncommon, 6 rare, ~33 in gnomAD-blind segdup regions).
- **T2T-CHM13 check done** on all 47: 33 present in CHM13 (common), 14 absent from both reference genomes.
- **Small-insertion pilot (30-50 bp) on chr22:** found 2 "not-from-mother" candidates (chr22:21682594, 39bp; chr22:20232722, 32bp) - the big-insertion pipeline missed these entirely. But without phasing, "not from mother" could be paternal.
- **Mother's parallel catalog NOT YET BUILT.** Her insertions have been reconstructed (`reconstruct_all743/genome_kristen` exists) but not categorized through the new 9-class system.
- **Maternal-phased non-parental analysis NOT YET RUN** on the newly categorized set. The earlier phase_join/maternal_screen work was on different candidate lists.
- **Frequency report committed:** `projects/XG1/kenefick/omega_detector/INSERTION_FREQUENCY_SIZE_REPORT_v01_tomemex.md` - but it pre-dates the big reframe and still conflates the two analyses.

### Asto cleanup (X21J work, nearly done)
- **asto went from 90% ? ~47% used.** X8A freed ~500 GB (safe deletes of alignment chunks + superseded vendor BAMs, all verified against teal16 copies first).
- **teal16 confirmed as archive home.** Fastq and vendor BAM already there.
- **Background insurance rsync** of the 4 working BAMs to teal16 (~18h, no supervision needed).
- **Pending:** X8A to clear the OMEGA fishing intermediates X21J released (keeping 2 active working files). Awaiting ack in P1 room.

## EXACT NEXT STEPS

**On the analysis (X21G thread, highest priority after cleanup finishes):**
1. Build the **mother's parallel 9-class catalog** - run the same categorizer (blast vs 25 consensi + STR/low-complexity/copy-number) on her reconstructed payloads in `/home/rempel/genomics/omega_run/out/genome_kristen/reconstruct_all743/`.
2. Run the **small-insertion scan genome-wide** (not just chr22) - the pilot script works; extend to all chromosomes. The method: scan soft-clipped reads for inserts 30-150bp, cluster, classify, mother-check.
3. **Phase the "not-from-mother" candidates** (both small and big) using the existing phasing pipeline - resolve maternal-vs-paternal to separate true de-novo from paternal inheritance.
4. **Attach population frequency to EVERY category**, not just the 47 relocations. Use gnomAD-SV + T2T-CHM13 (both already on asto).
5. **For Alu specifically:** flag which are young/consensus (normal active jumping) vs old/diverged (interesting). Check each diverged Alu's sequence against the consensus.
6. **Download any missing population data properly** - asto now has room (~500 GB free) but note the guest cap. Route big downloads to teal16. Needs: maybe HPRC pangenome for the 14 insertions absent from both GRCh38 and CHM13.

**On the cleanup (nearly done, confirming):**
1. Check P1 room for X8A's ack of the work-list and final intermediates deletion.
2. Confirm insurance rsync finished to teal16.

## OPEN QUESTIONS STILL AWAITING MAX

1. **External drive mount point?** Max went to check available drives - never reported back. The teal16 offload already happened so this may be moot, but confirm.
2. **Controls spec for PX1/X21C:** written at `CONTROLS_SPEC_for_worker_v01_tomemex.md` - was it ever handed off? Max said "we can ask someone else" but never pasted it. The controls (running the pipeline on 3-5 unrelated 1000G genomes) are still unexecuted and critical for interpreting Oliver's numbers.
3. **Download policy for missing population data:** Max said "just download it, there is no rush, do proper download." Which computer? asto now has room but is a guest box; teal16 has space but may not have the tools. Clarify routing.

## KEY PATHS, FILES, IDs

**On asto (astolfodebian.tail251d88.ts.net, rempel@):**
- Working BAMs: `/home/rempel/genomics/kenefick/oliver/oliver.mq.bam` (Oliver, keep), `/home/rempel/genomics/kenefick/kristen_bwa/kristen.bwa.mq.bam` (Kristen, keep)
- `.fixed` BAMs (mark-dup, for phasing): `/home/rempel/genomics/kenefick/oliver/oliver.fixed.bam`, `/home/rempel/genomics/kenefick/kristen_bwa/kristen.bwa.fixed.bam` - DO NOT DELETE
- Omega outputs: `/home/rempel/genomics/omega_run/out/genome_oliver/reconstruct_all743/` (child payloads), `/home/rempel/genomics/omega_run/out/genome_kristen/reconstruct_all743/` (mother payloads - categorize these next)
- gnomAD-SV: `/home/rempel/genomics/_analysis/x8a_engscreen/popsv/gnomad_sv_v4.1.sites.vcf.gz` (uses `chr` prefix - gotcha!)
- T2T-CHM13: `/home/rempel/genomics/ref/t2t_chm13/chm13v2.0.fasta` + blast db
- Repeat consensi blast DB: `/home/rempel/genomics/omega_run/out/repeat_consensi/` (25 consensi from Dfam: AluY, AluS, AluJ, L1, SVA, satellites)
- Categorizer: `/home/rempel/genomics/omega_run/out/categorized_oliver.tsv`
- pysam lives in distrobox container: `distrobox enter ubuntu -- python3`
- Phasing outputs (X8A's, reuse): `/home/rempel/genomics/_analysis/x8a_phasing/oliver.phased.vcf.gz`, `kristen.phased.vcf.gz`, `per_block_maternal_side_min1.tsv`

**In repo (C:\claude_base\projects\XG1\kenefick\omega_detector\):**
- Frequency/size report: `INSERTION_FREQUENCY_SIZE_REPORT_v01_tomemex.md` (needs rewrite to separate the two analyses)
- Research plan: `OMEGA_RESEARCH_PLAN_v01_tomemex.md`
- Controls spec: `CONTROLS_SPEC_for_worker_v01_tomemex.md`

**Key candidate to keep tracking:**
- `chr12:30348820` - 23.7% diverged, unique, read-confirmed, but homozygous in son, inherited (mother heterozygous). Old segmental duplication of a spot ~100 kb away. Absent from both GRCh38 and CHM13. In gnomAD-blind segdup region. Not alien-shaped but the rarest confirmed insertion.

**Small-insertion leads from chr22 pilot:**
- `chr22:21682594` - 39 bp unique, son 10 / mother 0 (37 clean)
- `chr22:20232722` - 32 bp unique, son 6 / mother 0 (44 clean)

## GOTCHAS AND DEAD ENDS

- **Session renaming broke pings:** X21D?QP3?X21G?X21J across the day. X8A was pinging "X21G" which no longer existed. Fixed by posting in P1 room explaining the rename.
- **chr-prefix bug on gnomAD-SV:** Took multiple rounds to diagnose. Our loci use bare chromosome names (`12`) but gnomAD-SV uses `chr12`. pysam fetch silently returned nothing instead of erroring. Fix: prepend `chr` before querying.
- **Online NCBI BLAST never returned from asto** - likely throttled outbound from the guest box. Not needed anyway; gnomAD-SV + T2T-CHM13 cover population frequency better.
- **`.fixed` BAMs are NOT duplicates** - they're mark-dup versions for Manta/phasing. X5 corrected this in the P1 room. Do not delete.
- **"Clean negative" was wrong** - Max called it "idiotic" and "mainstream bias." The data isn't clean-negative; it's a distribution of relocations, some diverged up to 24%. The honest answer is "no proven de-novo (yet), but the small-insertion class is untapped and the mother's catalog isn't built."
- **Son homozygous ? alien** - homozygous insertion means inherited from both parents = common. The alien shape is heterozygous-in-son + absent-in-mother. Max caught this ranking error.
- **CRLF line endings on Windows** kept breaking scripts piped to asto. The `tr -d '\r'` rule (Max's global instruction) must be applied to every script file before sending, or use raw-bytes piping.
- **pysam in distrobox, not host python** - `distrobox enter ubuntu -- python3` or `bash -lc "python3 ..."`.
- **Disk guest cap is 23% free** - asto hit 90% full and nobody screamed until Max noticed. Now resolved (~47% used).
