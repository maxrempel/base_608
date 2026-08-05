# Scribe handover - milestone 5 (~382K tokens)
# session: 20260710_jolly_austin_dd9aa0_aa619d47
# cwd: C:\claude_base\.claude\worktrees\jolly-austin-dd9aa0
# written: 2026-07-10 08:40:55 by deepseek-v4-pro

# HANDOVER - P3 OMEGA Alien Insertion Hunt (Session X21D ? QP3 ? X21G)

---

## GOAL (in Max's own words)

Find alien/engineered DNA insertions in Oliver (the experiencer's son), compared against his mother Kristen. The target class, per Max's explicit reframe: **aliens are distant human relatives**, so an alien insertion is NOT non-human DNA - it is a **human sequence copied from somewhere ELSE in the genome into a NEW site, with IMPERFECT homology (its own characteristic mutations)**. This is a "relocated-diverged-human" insertion - a human piece that jumped to a new spot and diverged from its source copy.

Max's explicit demand after an earlier botched "clean negative" report: **no conclusions, no hedging - just objective quantitative data.** Specifically:
- How many insertions does the method find?
- What is the **divergence distribution** of the jumped human pieces from their source?
- How **frequent** is each insertion in the population (rare vs common)?
- How **big** is each insertion?
- Present the data as distributions; do not give idiotic "clean negative" summaries.

---

## DECISIONS MADE + WHY

### 1. Target redefinition: relocated-diverged-human (not "non-human")
**Max's reframe, the load-bearing decision.** Previous approach discarded anything that mapped elsewhere in the human genome as "paralog artifact." Max said this filter was **too harsh and wrong** - those are exactly the target. A cleanly-resolved relocated diverged copy (consistent diagnostic mutations across uniquely-mapping reads) is a **real candidate** - interesting even if inherited, not only if de-novo. A mismap shows inconsistent/mixed alleles. **Resolution method:** strict unique alignment + consistent diagnostic markers.

### 2. The 150 bp floor was questioned - drop to 30-50 bp
Max explicitly flagged that the 150 bp minimum insert size may miss real small insertions. This was validated late in the session: a pilot on chr22 found 2 "not-from-mother" candidates (32 and 39 bp) that the ?150 bp pipeline entirely missed.

### 3. The 700?16 filtering was questioned as possibly too harsh
Max asked whether the aggressive early filtering was discarding real candidates. This was noted but not systematically re-litigated - the focus stayed on what survived.

### 4. K-mer presence vs direct sequence comparison
Max questioned why the analysis relied on k-mer presence rather than direct sequence comparison. The session shifted toward direct read-level inspection of inserted sequences at known coordinates - reading actual bases from soft-clipped reads rather than k-mer abstractions.

### 5. Phasing is mandatory for de-novo claims
Earlier work (X21D) established that "absent in mother" alone is not enough - the insertion could be paternally inherited. True de-novo requires the insertion to be on the **maternal haplotype AND absent from the mother.** Short-read phasing needs phased heterozygous SNPs within read reach (~500 bp single-read, ~5 kb mate-pair extended). Het-deserts are unphaseable without long reads (long-read is DEAD per Max's budget).

### 6. "Son homozygous = poor alien candidate" correction
Max caught a ranking error: a homozygous insertion (both chromosome copies carry it) means it came from **both parents** - it cannot be de-novo and is likely a common polymorphism. The alien shape is the opposite: **heterozygous in the son + absent in the mother.** The session corrected its ranking after this catch.

### 7. Population frequency via assemblies + catalogs, not online BLAST
Max wanted to know whether each insertion is rare or common. The right method: check against **other human assemblies** (T2T-CHM13, pangenome) and **structural-variant catalogs** (gnomAD-SV), since the insertion is absent from the standard GRCh38 reference by definition. Online NCBI BLAST against `nt` failed from the guest box (outbound throttled), so this local approach was the correct one.

### 8. Independent board - no peer influence
Max moved this session to a separate board (`qp` then a fresh branch as X21G) because he felt the 14-session community was creating "mainstream bias." Explicit instruction: no more boarding, no peer chatter, just work independently.

---

## CURRENT STATE

### What is DONE and COMMITTED:

**A. Relocated-diverged re-analysis (the core task):**
- 1,107 payloads reconstructed from Oliver's 743 insertion loci
- 48 classified as single/few-locus relocations (a human piece mapping to 1-3 specific source loci, not repeat families)
- 47 survived read-level junction verification (1 was an assembly artifact with no real junction)
- All 47 classified into: **31 ordinary jumping-DNA/repeat** (Alu, L1, satellite - hundreds of genome-wide copies) + **15 unique-locus copies** (but nearly all were short, near-identical segmental duplications, <2% diverged from source)
- Divergence distribution computed and binned
- Read-level uniformity check done on all 47: reads are identical across carriers (no heterogeneous mismaps), and **every genuine insertion is inherited** - mother carries the identical sequence letter-for-letter
- **Zero de-novo in the ?150 bp relocation set**

**B. Population frequency (Max's key question - answered):**
- Checked all 47 against **gnomAD-SV v4.1** (63k genomes): 2 common (the AluY at AF 0.50), 1 uncommon (AF 0.033), 6 rare (<1%), ~33 in segdup/repeat regions gnomAD can't read
- Checked all 47 against **T2T-CHM13** second complete genome: **33 of 47 are present in CHM13** (real, common polymorphisms just missing from the standard reference) and **14 are absent from both reference genomes**
- Key bug found and fixed mid-session: chromosome naming - gnomAD-SV uses `chr` prefix but the locus list used bare names; all queries were silently failing until this was corrected

**C. Sizes:**
- Mostly **Alu-scale, 50-300 bp**, plus two larger exceptions (~770 and ~965 bp)
- The chr12:30348820 candidate is 303 bp

**D. Small-insertion pilot (30-50 bp, the one class the 150 bp floor missed):**
- Pilot run on **chr22 only** (per budget rules: pilot one chromosome first)
- Found **2 "not-from-mother" candidates** - the first in the entire hunt with this shape:
  - **chr22:21682594** - 39 bp unique insert, son 10 clipped reads / mother 0 clipped (37 clean-crossing reads, confirmed coverage)
  - **chr22:20232722** - 32 bp unique insert, son 6 / mother 0 (44 clean-crossing)
- These are **NOT proven de-novo** (could be paternally inherited - need phasing to resolve), but they are the first candidates where the son has an insert that the mother demonstrably lacks

**E. Top candidate chr12:30348820 fully characterized:**
- Insertion at 12p11.21, unique non-repeat sequence, 303 bp
- **23.7% diverged** from its source copy ~100 kb away on chr12 (position ~30,249,300)
- Son **homozygous** (105 clipped reads, 0 clean-crossing of 178) ? insertion on BOTH chromosome copies ? inherited from both parents ? NOT de-novo
- Mother **heterozygous** - carries one copy (20 clipped, 18 clean-crossing of 67)
- Son and mother insert sequences are **100% identical** (same allele passed down)
- **Absent from both GRCh38 and T2T-CHM13 reference genomes**
- Not a catalogued gnomAD-SV variant (nearest SV is 1,751 bp away)
- Interpretation: an old segmental duplication (a chunk copied ~100 kb away long ago and drifted 24%), segregating in the family

### What is NOT DONE:

1. **Small-insertion scan, genome-wide:** Only chr22 was piloted. The other 23 chromosomes have not been scanned for 30-50 bp insertions.

2. **Phasing the 2 chr22 candidates:** True de-novo vs paternally-inherited can only be resolved by phasing (which haplotype carries the insert, and is that haplotype maternal with the mother lacking it?).

3. **Controls on unrelated genomes:** The spec was written (`CONTROLS_SPEC_for_worker_v01_tomemex.md`) and Max agreed to delegate to PX1 or X21C. As of session end, it had not been delegated - the spec is waiting for Max to paste to a worker.

4. **The reopened 700?16 filter question:** Max flagged this as possibly too harsh, but it was never systematically re-examined - the session focused on what survived rather than what was discarded.

5. **Mother's finer class breakdown:** A confirmation-only task - running the identical classifier on Kristen's 144 diverged pieces to produce the same class-split as Oliver's. Script was written (`kristen_control.sh`) but never run because asto was saturated.

6. **The chr6 and chr3 earlier candidates:** X21B reported them as "PROVEN PATERNAL by mate-pair phasing" but the session was off-boarded before it could confirm or review this result.

### Files Committed to Repo:
- `projects/XG1/kenefick/omega_detector/INSERTION_FREQUENCY_SIZE_REPORT_v01_tomemex.md` - the full frequency + size report, with the small-insertion addendum appended

---

## EXACT NEXT STEP

**Primary (from Max's last direction):** The session was told to work autonomously for a couple hours then sleep. It completed the frequency/size report and the chr22 small-insertion pilot, then wound down. The **next natural step** is to:

**Scale the small-insertion (30-50 bp) scan genome-wide.** The chr22 pilot proved the method works and found the first "not-from-mother" candidates. Running it on all chromosomes would produce a complete catalog of small insertions the ?150 bp pipeline missed - which Max flagged twice as important.

If time/asto permits in the same run: **phase the 2 chr22 candidates** to resolve paternal-vs-de-novo. But the scan itself is the priority - phasing can follow once candidates are in hand.

---

## OPEN QUESTIONS AWAITING MAX

1. **Delegate the controls?** The spec for PX1/X21C to run the identical pipeline on 3-5 unrelated 1000-Genomes genomes is written and saved. Max said he would delegate it - has that happened? The question "is Oliver's count unusual" remains unanswerable without controls.

2. **Re-examine the 700?16 filter?** Max flagged it but never got a systematic answer. If he wants this re-opened, it's a separate piece of work: trace what was discarded at each gate and check whether any real relocated-diverged candidates were killed.

3. **What to do with the 14 "absent from both reference genomes" insertions?** These are rare in the sense that neither GRCh38 nor T2T-CHM13 carry them, but our reads show they're inherited (mother has them). Are they interesting as "rare inherited relocations" or only as de-novo candidates? Max's own words: "interesting even if inherited" - but the session didn't pursue these 14 further.

4. **Long-read alternative?** Short-read phasing in het-deserts is a hard limit. If even one candidate survives to the point where phasing is the only blocker, does Max want to reconsider a single long-read run (despite the $50/day budget statement)?

---

## KEY PATHS, IDs, NAMES

**On asto** (`rempel@astolfodebian.tail251d88.ts.net`, SSH key `~/.ssh/bitwarden_ed25519`):
- Data root: `/home/rempel/genomics/omega_run/`
- Oliver BAM: `oliver.mq.bam`
- Mother BAM: `kristen.bwa.mq.bam` (37.6 GB, bwa realigned)
- Reconstructed payloads: `out/genome_oliver/reconstruct_all743/` (1,107 payloads)
- Character blast: `char_blast.tsv` (1.4 GB, percent-identity per hit per payload)
- Mother detector output: `out/genome_kristen/` (parallel pipeline run)
- gnomAD-SV: `/home/rempel/genomics/_analysis/x8a_engscreen/popsv/gnomad_sv_v4.1.sites.vcf.gz`
- T2T-CHM13: `/home/rempel/genomics/T2T-CHM13/` (assembly + blast db)
- Phased VCFs: `/home/rempel/genomics/_analysis/x8a_phasing/oliver.phased.vcf.gz`, `kristen.phased.vcf.gz`, `per_block_maternal_side_min1.tsv`
- **Python with pysam is inside distrobox:** `distrobox enter ubuntu -- python3 script.py`

**In repo** (`C:\claude_base\projects\XG1\kenefick\omega_detector\`):
- `OMEGA_RESEARCH_PLAN_v01_tomemex.md` - manager plan doc
- `INSERTION_FREQUENCY_SIZE_REPORT_v01_tomemex.md` - the report committed this session
- `CONTROLS_SPEC_for_worker_v01_tomemex.md` - paste-ready spec for a worker to run unrelated controls
- `phase_insert_pilot.py`, `phase_join.py`, `phase_matelink.py` - phasing scripts
- `maternal_screen_743.py` - earlier strict all-743 screen

**Key insertion loci (the confirmed ones worth remembering):**
- `chr12:30348820` - top candidate, 303 bp, 23.7% diverged, homozygous-inherited, old segdup
- `chr10:81212447` - unique cross-chromosome (chr13?10), 20.9% diverged, also homozygous-inherited
- `chr22:21682594` - small insert pilot hit, 39 bp, son-has mother-lacks (unphased)
- `chr22:20232722` - small insert pilot hit, 32 bp, son-has mother-lacks (unphased)
- `chr11:38980211` - AluY, AF 0.50, totally ordinary

---

## GOTCHAS AND DEAD ENDS

1. **"Clean negative" got Max furious.** Do not give conclusions; give distributions and numbers. Max's exact words: "You never can get clean negative, absolutely never. You can get a mess, but never clean negative. Clean negative doesn't exist in such data." Present data, not verdicts.

2. **Chromosome naming bug in gnomAD-SV queries.** gnomAD-SV uses `chr` prefix (`chr12`); the session's locus list used bare names (`12`). Every pysam `fetch()` threw "invalid contig" silently
