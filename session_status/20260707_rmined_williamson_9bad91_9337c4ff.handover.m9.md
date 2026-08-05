# Scribe handover - milestone 9 (~697K tokens)
# session: 20260707_rmined_williamson_9bad91_9337c4ff
# cwd: C:\claude_base\.claude\worktrees\determined-williamson-9bad91
# written: 2026-07-07 18:05:27 by deepseek-v4-pro

# X12B P2 HANDOVER - Primate-Ancestry Analysis Complete; Max Wants It Explained

---

## GOAL (in Max's own words)

"Measure each of the NPAs in terms of actual modern humans versus predecessors like monkeys and stuff, like other primates." Full genome, by NPA category, with proper statistics - specifically measuring whether the **new** (non-parental) allele in a child reverts toward the primate/ancient base, and testing that against a proper null so it's not the reference-allele tautology.

Max then asked me to explain the result in plain language because "I'm looking at the table, I understand nothing." I was mid-explanation when the session compacted.

---

## DECISIONS MADE + WHY

### 1. The "primate direction" is measured as: "is the new non-parental allele the ancestral base?"

For every non-parental allele (the letter in the child that is in neither parent), we check whether that letter matches the **EPO primate-ancestral genome** (chimpanzee/gorilla/orangutan/macaque consensus). If yes ? the new allele "reverted to the ancient/primate state." If no ? it's modern/derived.

This avoids the reference-allele tautology that earlier analysis fell into. The earlier crude method just asked "is the ALT allele ancestral?" - but the new non-parental allele isn't always the ALT (sometimes it's the REF). The correct detector (`catdrift3.py`) extracts the actual non-parental allele as `set(child_alleles) - set(parent_alleles)` and checks whether *that* base matches the primate-ancestral base.

### 2. The proper null is a scrambled-parent baseline (not all-genome baseline)

Comparing NPA reversion rate to the genome-wide average would be misleading because NPA sites aren't a random set - they're sites with at least one heterozygous parent (where a new allele can appear). So for each NPA site, we **scramble the parent assignments** (shuffle which two adults are the "parents" of which child), re-derive the "new" allele, and count whether it lands on the ancestral base. That gives the **chance expectation** for *these same sites* - how often a random assignment of parents to children would produce an ancient-looking new allele.

This cancels out any composition bias in the site set and any reference-allele tautology.

### 3. Analysis split by NPA category, but only DOCHAN categories matter for direction

The five categories are:
- **both-hom**: child homozygous for an allele neither parent carries (DOCHAN homozygous)
- **both-het**: child heterozygous for an allele neither parent carries (DOCHAN heterozygous)
- not_from_father, not_from_mother, other: by definition these have no allele absent from *both* parents, so "what base is the new allele?" is undefined for the direction question

Only both-hom and both-het carry a genuinely new (non-parental) allele whose direction we can measure.

### 4. Computed genome-wide (all 23 chromosomes) streaming 1000G VCFs on AWS

The box (`i-00c83a0af889f8bf1`, `c7i.8xlarge`, us-east-1) streamed all 22 autosomal + X chromosome VCFs through `catdrift3.py` in parallel (32 cores, resumable via `.done` marker files). Each chromosome tallied: BASELINE site counts, REAL NPA counts by category?stratum?ancestral/derived, and NULL (scrambled-parent) counts. The per-trio loop + null pass made this slow (~3 hours genome-wide).

### 5. Statistics: Wilson 95% CI + two-proportion z-test + Bonferroni correction

For each category, real ancient-fraction compared to null ancient-fraction via a two-proportion z-test, with Wilson 95% confidence intervals. Bonferroni corrected across the 5 categories. Both DOCHAN categories are *below* the null at p?0 - i.e., the new alleles land on the primate base **less** often than chance, not more.

---

## CURRENT STATE

### The genome-wide result (all 23 chromosomes, 4.22 million non-parental alleles):

| category | real ? primate% [95% CI] | null (chance)% [95% CI] | z | verdict |
|---|---|---|---|---|
| both-hom | 31.4% [31.1-31.7] | 36.7% [36.4-37.0] | ?35 | below chance |
| both-het | 12.5% [12.5-12.6] | 18.9% [18.8-18.9] | ?331 | below chance |
| overall (all categories with a new allele) | 13.0% | 21.9% | - | below chance |

**Plain English:** when a child gets a new letter that neither parent carries, that letter is the ancient/primate version only 13% of the time, but random chance (scrambled parents) would give it 22% of the time. The new alleles drift *modern/derived*, not ancient. This holds for both DOCHAN categories, at overwhelming statistical significance.

### Files delivered and committed:

- **Main report**: `C:\claude_base\projects\XG1\kenefick\paper_repro\outputs\real\P2_primate_drift_bycategory_genomewide_v01.md`
- **Per-chromosome raw tallies**: `outputs/real/gd3/` (23 `.out` files - BASELINE, REAL, NULL lines per category?stratum)
- **GOAL document**: `outputs/real/GOAL_primate_ancestry_of_NPAs_v01_tomemex.md`
- **NPA catalog** (from earlier in session): `outputs/real/NPA_catalog_perSNP.tsv` (902,249 calls, 140,849 sites, with recurrence column) and `outputs/real/NPA_catalog_perRegion.tsv` (108,606 mislands)
- **Genome-wide per-trio NPA calls**: `genome_out/chr*/calls/*.tsv` and `genome_out/chr*/regions/*.tsv` (local)
- **Category-drift pilot** (chr21+22, earlier method): `outputs/real/catdrift_chr21_22_v01.tsv`
- **AWS box**: **STOPPED** (not terminated) - `i-00c83a0af889f8bf1`, us-east-1, IP in `/tmp/boxip.txt`, SSH key at `C:/Users/maxre/Nextcloud/zSyncMain/ssh/xg1_aws.pem`
- **The detector script**: `catdrift3.py` lives on the box at `~/catdrift3.py` and in temp at `/tmp/catdrift3.py` locally

### What Max actually asked for at the very end:

He said "I'm looking at the table, I understand nothing." I started explaining from the ground up: one DNA position, one family, what an NPA is, what "ancient vs modern" means for that one letter, and what the two percentages (real vs null) count. I was mid-explanation - I had asked "Does that first layer land?" and was about to explain the 13% vs 19% comparison when the session compacted.

---

## EXACT NEXT STEP

**Continue the plain-English explanation of the primate-drift result that Max asked for.** Structure it exactly like this, building up from concrete examples:

1. **One position, one family.** Pick a real example from the data: a specific child, a specific chromosome position, what letters mom/dad/child actually have, what the "new" letter is, and whether it matches the primate-ancestral base.

2. **What "13%" and "19%" count.** Explain that across all 4.2 million surprise letters genome-wide, 13% of the *real* ones matched the primate base, but if we scramble which adults are the parents (the null), that number would be 19%. So the real NPAs land on the primate base *less* than random chance.

3. **What the conclusion actually means.** This is the **background signature** from normal human genetics + sequencing noise in control families. It does NOT show aliens pushing us *away* from primates - it's just the ordinary baseline. A real alien "reversion to ancient" would show up as the opposite: experiencer NPAs landing on the primate base *more* than this 19% null, not less. This experiment sets the yardstick.

4. **The table, re-presented plainly.** Three rows (both-hom, both-het, overall), two numbers each (real ancestral%, null ancestral%), one verdict each. No jargon.

**Do NOT:** restart the box, re-run anything, re-open the catalog work, spin up teammates, or do any new analysis. The data is delivered - Max just needs it explained clearly.

---

## OPEN QUESTIONS AWAITING MAX

- **The gene-set for hotspot overlay** - Max mentioned autism/SFARI genes as a possible set to overlay his recurrent hotspots onto, but never confirmed which gene set. This was queued but not done.
- **Haplotype clustering by family and location** - also queued but not done; no gene set needed for this, just the catalog.
- **What next?** Max's primate-ancestry question is answered (for controls). If he wants the real ~5% subgroup test, that needs actual experiencer genomes - 1000G controls can't show it. He should steer next steps.

---

## KEY PATHS, FILES, AND IDs

### Local (C:/claude_base/projects/XG1/kenefick/paper_repro/):

- `outputs/real/P2_primate_drift_bycategory_genomewide_v01.md` - **the main result report**
- `outputs/real/gd3/` - 23 per-chromosome `.out` files (raw tallies)
- `outputs/real/GOAL_primate_ancestry_of_NPAs_v01_tomemex.md` - goal document
- `outputs/real/NPA_catalog_perSNP.tsv` - 902k NPA calls, one row per SNP
- `outputs/real/NPA_catalog_perRegion.tsv` - 108k mislands
- `outputs/real/catdrift_chr21_22_v01.tsv` - earlier pilot (chr21+22 only)
- `genome_out/chr*/calls/*.tsv` + `genome_out/chr*/regions/*.tsv` - per-trio per-chromosome NPA output
- `scripts/npa_detector.py` - the core NPA detector (validated, correct)
- `/tmp/catdrift3.py` (or on box at `~/catdrift3.py`) - the corrected primate-direction tally script

### AWS:

- **Instance**: `i-00c83a0af889f8bf1`, us-east-1, **STOPPED** (kept ~$5/mo disk - do NOT terminate)
- **SSH key**: `C:/Users/maxre/Nextcloud/zSyncMain/ssh/xg1_aws.pem`
- **IP**: stored in `/tmp/boxip.txt` (rotates on stop/start - re-query with `aws ec2 describe-instances` if needed)
- **SG**: `sg-0651e79bde1c34bd0` (must add current IP to inbound SSH rule if box restarted)
- **On-box data**: `~/gd3/` (the 23 `.out` files and `.done` markers), `~/catdrift3.py`, `~/xg1/anc/homo_sapiens_ancestor_GRCh38/` (primate ancestral FASTA), `~/xg1/g1k.ped`
- **VCFs streamed from**: `s3://1000genomes/1000G_2504_high_coverage/working/20201028_3202_raw_GT_with_annot/...recalibrated_variants.vcf.gz` (in-region S3, free/fast)

### Handoff files:

- `C:/claude_base/session_status/20260706_X12B_P2_reopened_handoff.md` - the full handoff from the reopened P2 phase (contains the complete genome-wide recipe + all state)

---

## GOTCHAS AND DEAD ENDS

1. **The reference-allele tautology.** Earlier runs wrongly assumed the "new" non-parental allele is always the ALT. It's not - for both-hom cases the new allele can be the REF. This made early numbers misleading (looked like 80%+ modern, which was just "ALT is usually modern"). The corrected `catdrift3.py` extracts the actual non-parental allele with `set(child) - set(parents)` and checks its ancestral status directly. The chr22 validation run confirmed this correction reproduces earlier validated numbers.

2. **Single-parent categories (not_from_father, not_from_mother, other) have no direction to measure.** These categories mean the child has an allele the named parent lacks *but the other parent could have it*. There is no allele absent from *both* parents, so "what is the new allele?" is undefined. Only both-hom and both-het (the DOCHAN categories) carry a genuine surprise letter whose direction can be measured. If Max asks about those categories, that's the honest answer.

3. **This is the control baseline, not the alien signal.** The analysis ran on 1000-Genomes controls - ordinary families, no experiencers. A ~5% genuine alien signal would be diluted ~20-to-1 and swamped by the ordinary background. So the finding "NPAs drift modern, below chance" is exactly what normal human genetics + sequencing noise produce. It neither supports nor refutes the alien hypothesis - it sets the null yardstick. The real test needs experiencer genomes compared against this baseline.

4. **Remote VCF streaming is fragile.** The per-child direction test (X12F's `archaic_annotate.py`) failed repeatedly due to random-seek corruption on 28GB remote VCFs - seeking backward in a gzip stream over HTTP doesn't work. The solution that succeeded: single-pass streaming (`aws s3 cp - | python3 detector.py --vcf -`), no random access. The corrected `catdrift3.py` uses exactly this approach. Per X12F's later note, a `--positions` pre-filter piped through `bcftools` would be even faster for targeted loci.

5. **The box is stopped, not terminated.** Max explicitly asked to keep it. Restarting requires re-adding the current IP to the security group before SSH works.

6. **The 222-hotspot Manhattan graph, the all-602 trio validation, and the NPA-type histogram were all delivered earlier in the session** and are committed. Max was satisfied with those.

7. **X11B/X12F are the sibling workers on P2.** X11B does concordance/artifact attribution; X12F does archaic-direction and read-pileup. Both have posted results during this session. Max explicitly told me to work solo and not wake them (conserving weekly limits). The handoff should note they exist but should NOT be nudged unless Max orders it.
