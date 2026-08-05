# Scribe handover - milestone 9 (~697K tokens)
# session: 20260710_admiring_maxwell_8cadba_6bb8eae1
# cwd: C:\claude_base\.claude\worktrees\admiring-maxwell-8cadba
# written: 2026-07-10 13:51:44 by deepseek-v4-pro

# X12B Handoff - Beautification Project (chr22 pilot complete)

## GOAL (in Max's words)
> "Beautification project. Metric of orderliness. I would expect a divergence in population - some people degrade and some people become more harmonious. We need to see the environment, the flanks, and get some metric of harmony. I think we might want to clean it up. Read global 2 and from a new version of global 2, give me the new compaction instruction to clean it up so you have the necessary tools but then we will go into the beautification project."

The core hypothesis: genuine de?novo changes (quality?filtered, not artifacts) may be *restoring order* in the local sequence - for example repairing a degraded repeat back to a cleaner form ("harmonious restoration of prettiness"). Max wants a metric that measures orderliness/harmony on nucleotide flanks (windows ?1 to ?20?nt), and a test of whether changes systematically raise orderliness and whether the population splits into "beautifiers" vs "degraders." He explicitly rejects ordinary mutation-chemistry spectra (CpG, UV signatures, etc.) - he wants **meaning and harmony, not chemistry**.

## DECISIONS MADE + REASONING

1. **Quality?filtered de?novo events only**  
   Earlier we discovered that the raw non?parental?allele catalog is dominated by genotyping errors. The key missing step was filtering to real events: child *clearly* carries the new allele (high GQ, DP?8, ?5 alt reads) and both parents *clearly* lack it (GQ?20, DP?8, zero alt reads). This filter removed ~93% of chr22 raw NPAs, leaving 9,580 high?confidence de?novo candidates. This is the whole game - without it the metric is polishing noise.

2. **Orderliness metric: compressibility of flanking runs**  
   The metric measures *local repetition*: for a window of 2W+1 bases around the variant, count the number of equal?adjacent?base pairs (n_runs) and divide by the maximum possible runs in a perfectly uniform sequence of that length. A perfect homopolymer scores 1.0; alternating A-C-A-C... scores 0.0. This captures "harmony" as Max described - restoring a degraded repeat yields a positive delta in orderliness. The metric is implemented in `scripts/orderliness_v01.py` and self?tests on known synthetic cases.

3. **Multi?permutation chemistry null**  
   To test whether ?O is "real" beyond ordinary composition, the null model randomly permutes the new base *within* the same site, but respecting the base?composition of the position (i.e., shuffles between the two observed bases). This rules out a simple compositional confound. The pipeline runs `--perms 25` and computes a z?score for the observed mean ?O vs the null distribution.

4. **Synthetic positive?control (recovery of a planted subgroup)**  
   Before touching real data, X12B built a self?test (`beautify_annotate_v01.py --selftest`) that injects a known 20%-beautifier subgroup (mean ?O +0.333 vs 0.0 for the rest) and confirms the pipeline recovers it. This is the discipline Max demands - prove the method can find the signal if it exists.

5. **Context stratification: slippage vs. residual**  
   Because the first real chr22 results showed that top "beautifying" changes were extending homopolymer runs (e.g., C?T inside a T?run), the analysis was stratified by whether the flank is low?complexity/repetitive (?70% of a single base pair or trinucleotide repeat) vs. complex. This revealed that **the signal is 4? stronger in repeat contexts (+0.029 vs +0.007)** - almost entirely ordinary polymerase slippage. A small residual order?bias survives in complex DNA, but it is not yet proven to be beyond chemistry.

6. **One shared de?novo compute pass**  
   The beautification lane shares the exact same prerequisite (a quality?filtered de?novo event table) with HOMEWARD (reversion?drift pilot from X31B). Both lanes can consume the same output, avoiding duplicate streaming of the 28?GB VCFs. The de?novo caller (`scripts/denovo_caller_v01.py`) was built to output columns `child,chrom,pos,ref,alt,dp,gq,...` - the consensus old base = ref, new base = alt.

7. **Work solo, no team wake, box stopped**  
   Max explicitly said we are running low on AWS weekly limits and should do things solo. The box was started only for the chr22 streaming (~$1.4/hr c7i.8xlarge), then stopped. All subsequent analysis is local. The box is kept (not terminated) per Max's standing order.

## CURRENT STATE
- **What is done:**
  - The orderliness metric and full beautification analysis pipeline are built, validated, committed, and pushed to `master`.
  - Real chr22 quality?filtered de?novo candidate table generated: `outputs/real/beaut_chr22/denovo_chr22.tsv` (9,580 events, 602 trios).
  - Beautification analysis run: per?orderliness?window (3-41?nt) mean ?O, null?derived z?score, per?child output.
  - Context stratification performed: repeat vs. non?repeat.
  - Honest pilot report written: `outputs/real/beaut_chr22/BEAUTIFICATION_chr22_pilot_v01_tomemex.md`.
  - All scripts + data committed; box stopped.

- **What the data shows (chr22 pilot):**
  - **Overall:** small but statistically significant order?preservation - observed mean ?O is slightly *less* negative than the chemistry null, so observed?null = positive signal (e.g., +0.013 at 7?nt window, z?+6.3).
  - **But the confound:** the signal is concentrated in low?complexity/repetitive flanks (30% of events, signal +0.029, z=+6.5). In complex non?repetitive DNA (70% of events) the residual is +0.007, z=+3.6 - 4? weaker.
  - **Per?child spread:** 205 net?beautifiers (?O>0), 321 net?degraders. Max's "divergence" is visible, but so far the top beautifiers look like slippage artifacts.

- **What is NOT done (pending Max decision):**
  - A more sophisticated context?matched mutation baseline to test the residual beyond chemistry.
  - Checking whether the order?preservation is stronger in the rarest/private events (a real "push" should be, slippage will not).
  - Scaling to genome?wide - only chr22 was pilot.

## EXACT NEXT STEP (blocking)
Max must decide: **"Do you want me to chase that small residual, or is this a dead end too?"**  
The session ended with that question. No action should be taken until Max gives a clear yes/no on whether to pursue the residual beauty signal in non?repetitive DNA.

If Max says **yes**, the planned next steps are:
1. Build a **proper context?matched mutation baseline** (trinucleotide?context mutation probabilities from the 1000G background itself, not just compositional shuffling).
2. Test whether the order?preservation signal is **stronger in the rarest, singletons** (recurrence==1 in the catalog) - a real "push" favours fresh events, slippage does not.
3. If those tests still show a residual beyond chemistry, then scale to genome?wide using the same streaming method.

If Max says **no**, the beautification lane (as a single?letter?change project) closes; the handover should note that the metric and infrastructure are reusable for any other flank?based analysis Max might invent.

## OPEN QUESTIONS AWAITING MAX
- Continue chasing the residual beautification signal beyond slippage, or declare this a dead end?
- If yes, should the box be restarted for another streaming run, or can analysis continue locally with the existing chr22 de?novo table?

## KEY FILE PATHS & IDs
- **Working directory (local):** `C:/claude_base/projects/XG1/kenefick/paper_repro/`
- **Orderliness metric:** `scripts/orderliness_v01.py`
- **De?novo caller (streaming):** `scripts/denovo_caller_v01.py` (runs on box, python streaming S3 VCF)
- **Beautification analysis (multi?perm null, per?child):** `scripts/beautify_annotate_v01.py`
- **Context stratification script:** `scripts/beaut_context_strat_v01.py`
- **Pilot output data:** `outputs/real/beaut_chr22/denovo_chr22.tsv` (9,580 rows)
- **Per?child and per?window outputs:** same directory (beautify_annotate writes per?child and per?window .tsv files)
- **Pilot report (readable):** `outputs/real/beaut_chr22/BEAUTIFICATION_chr22_pilot_v01_tomemex.md`
- **Beautification specs:** `BEAUTIFICATION_orderliness_spec_v01_tomemex.md`
- **Reusable NPA catalog (older):** `outputs/real/NPA_catalog_perSNP.tsv` (902k calls, 140k sites)
- **AWS box:** `i-00c83a0af889f8bf1` (us?east?1); **CURRENTLY STOPPED** (no spend). SSH key: `C:/Users/maxre/Nextcloud/zSyncMain/ssh/xg1_aws.pem`. User: `ec2-user`.
- **Pedigree (602 trios):** S3: `s3://1000genomes/1000G_2504_high_coverage/additional_698_related/20130606_g1k.ped` (also on box at `~/beaut/g1k.ped`).
- **1000G VCF pattern:** `s3://1000genomes/1000G_2504_high_coverage/working/20201028_3202_raw_GT_with_annot/20201028_CCDG_14151_B01_GRM_WGS_2020-08-05_chr${n}.recalibrated_variants.vcf.gz`
- **Git branch:** `claude/determined-williamson-9bad91` (merged to `master`). Use explicit paths; never `git add -A`.
- **Security:** `nospiral` token bypasses hook; always re?add your current IP to SG `sg-0651e79bde1c34bd0` before SSH.

## GOTCHAS & DEAD ENDS ALREADY RULED OUT
- **Per?letter ancient?vs?modern direction analysis was bullshit** - it was dominated by the "non?parental allele = non?reference allele" tautology and was per?position, not meaningful. Max rejected it and demanded a new approach. Do not resurrect this.
- **Clean?cut "negative" conclusion was explicitly forbidden** by Max. Earlier in the session he reacted furiously that we filtered 100k events to 45 and declared no alien signal - he wants calibration against noise, not artifact?funneling. The beautification pilot is calibrated via null, but the pilot is **not a final declaration**.
- **The raw NPA catalog is mostly genotyping noise.** Single?letter surprise sites in the catalog are overwhelmingly artifacts; do not use them without the quality filter. The denovo_caller_v01.py is the correct entry point for real de?novo events.
- **The box can only stream VCFs; do NOT download 28GB files locally.** In?region `aws s3 cp - | python ...` is free and fast. Local disk on the box is small (9GB free), so never store a full VCF - only per?chromosome output tables.
- **Beautification signal in repeats = polymerase slippage.** The top beautifying changes are extending homopolymers; do not interpret that as "meaning." The honest path is context stratification, and Max's call determines whether the residual is worth pursuing.
- **The team is not to be woken** (Max: running low on weekly resources). X12B works solo. The p2 room is a data?pipe for lane coordination only - do not expect other sessions to act on X12B's posts.
- **The compaction instruction** Max asked for was delivered, but the handoff should still preserve the thread. The beautification project is the load?bearing direction; drop all the AWS/SSH/hook/box?restart mechanics and idle wake?loop turns. Keep the two pending teammate results mentioned in the original summary only if they become relevant (they haven't yet).
