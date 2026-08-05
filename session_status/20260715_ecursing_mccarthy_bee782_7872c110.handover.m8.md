# Scribe handover - milestone 8 (~658K tokens)
# session: 20260715_ecursing_mccarthy_bee782_7872c110
# cwd: C:\claude_base\.claude\worktrees\recursing-mccarthy-bee782
# written: 2026-07-15 11:18:44 by deepseek-v4-pro

# HANDOVER: X7Ab - Kristen Kenefick Correspondence Writer + Maternal-NPA Phasing

---

## GOAL (in Max's words)

Two parallel threads, both on the Kenefick family genomes (Kristen + Oliver):

1. **Primary role - Kristen letter-writing:** Answer her claims one at a time, pace slowly (she digests slowly), using the formalized RESPONSE STANDARD: every quantitative claim gets a plain-language summary email PLUS a rigorous methodological technical report as a PDF attachment. Controls-not-assertions. Nothing sends without Max's explicit per-message approval viewed in Chrome.

2. **P5 support - maternal-NPA phasing:** Max's exact words: *"Go to room P5 and talk to X32 and help that session find the annotated, properly phased NPAs... NPAs which are certainly in the mother's haplotypes. That is a very tough question to properly filter them."* The task is to identify Oliver's novel genetic changes that are *certainly* on the chromosome he inherited from his mother Kristen - with a rigorous filter that doesn't trust the flippable precomputed label that made earlier maternal findings wrong.

---

## DECISIONS + WHY

### The two-deliverable response standard (Max-directed)
Max rejected vague minimizers ("slightly," "a little"), undefined tables, and casual-email style. He demanded proper scientific reports with defined methods, quantified measurements, and self-criticism. **Decision:** Every claim gets TWO deliverables - a plain-language summary email (for readability) PLUS a rigorous technical report as a PDF attachment (for scientific integrity). Codified in `KRISTEN_RESPONSE_STANDARD_v01_tomemex.md`, committed, and pointed to read-first from the scoreboard.

### The durable memory system
Max asked: *"How is it possible that your summary of your emails is not saved and not in your memory? Build an elegant system where you actually don't forget stuff."* **Decision:** Built `build_kristen_ledger.py` - pulls the ENTIRE Kristen Gmail thread (147 messages) into SQLite, auto-generates a plain-English ledger of exactly which claims were answered and sent. Because it's derived from Gmail (ground truth), not hand-typed, it can't drift the way the old scoreboard did. Registered in long-term memory so any future session can read it cold. **It already caught errors:** the "3rd X" was actually answered in email 01 (scoreboard had it wrong); ARHGAP11B and TTR were genuinely never answered (Max's hunch was off - the DB proved it).

### The maternal-NPA phaser: anchoring to mother's reads, not a flippable label
The old approach (`phase_matelink.py`) decided maternal-vs-paternal by looking up X8A's precomputed "which side is mom's" table. The deletion team's OWN notes say that label flips and made all 6 earlier maternal deletions wrong. **Decision:** Throw that label away entirely. Instead, for each novel change the son has, link it on the same DNA fragment to a nearby marker where the mother is genetically fixed (homozygous). Check the mother's ACTUAL reads at that marker. If she's cleanly homozygous for the linked allele ? the change rides the maternal chromosome. If she's cleanly intact ? paternal. This directly proves origin without trusting any precomputed table. Built in a NEW file (`phase_matelink_motheranchor_v01.py`) so X32's work is undisturbed.

### Strict vs loose gates (pilot-proven)
The chr21 SNV pilot empirically proved why the filter must be strict. With loose gates (allow ?10% mother-alt reads), two apparent "maternal de-novo" calls appeared - but reading the actual pileups showed both were artifacts (one dropout, one weak single-marker call). With strict gates (zero mother-alt reads, ?2 concordant markers, mother depth ?15) both vanished. **Decision:** Strict gates only. The honest result is ~zero maternal de-novo, with ~75% of candidates genuinely unphaseable by short reads.

---

## CURRENT STATE

### Kristen letters - what's SENT (confirmed by Gmail ledger):
- Email 01 - triple-X / multiple X chromosomes
- Email 02 - extra-Y / male DNA (microchimerism: ~0.3%, STANDS as real, never retracted)
- Email 03 - 1500+ homozygous inversions
- Email 04 - rs2081743753 (TTCCA repeat + mismapping artifact)
- Email 05 - (sent per ledger, details in DB)
- Email 06 - trust-repair note (superseded/unused draft, Max handled personally)
- Email 07 - aunt/cousin segment-sharing "dominance"
- **Email 08 - Mendelian dominance (#1 claim):** the big one. Whole-chromosome 50-50 is structural proof, 405,465 obligate-paternal alleles show father fully present, 99.9% Mendelian consistency with honest 0.1% genotyping-noise floor. Microchimerism stands. SENT per Max's explicit go.
- Email 09 - topic map + "back to work" (compute limit lifted)
- **Email 10 - 30X microchimerism:** the linchpin. Full argument: arithmetic (0.3% ? 30X = ~0.09 reads/position ? why single markers fail), averaging across millions of male-specific positions (227 high-confidence reads from 5 clean genes, second method hundreds of times stronger than chance), uniformity (100/100 genome segments above noise = whole cells), son-specific (rarest father's-line variants present = her child's cells), common (~half of women who've carried sons). SENT.
- Email 11 - easy answers (99.9% isn't homozygosity rate; real homozygosity ~2.6%; 2.2M positions explained)
- **Email 12 - novel architecture (chromatin claim):** two deliverables. Summary + PDF technical report. Five-genome control comparison (Kristen, Oliver, three unrelated controls NA12718/NA18530/NA18488, identical pipeline + 1000G strict-accessibility mask, 5 chromosomes). Kristen within 0.3% of European control. H3F3B fully covered in all five - no truncation. Novel-variant count honestly documented as confounded (81% mother-son shared = artifact) and excluded. SENT with PDF attachment (verified 3 pages via pypdf before sending).

### Kristen letters - DRAFTED, HELD for Max's Chrome review (NOT SENT):
- **Email 13 - ARHGAP11B "gene silenced":** X1D analysis done. The gene is present at fully normal depth; the "one-third" is the gene's real human structure (partial duplicate by design); odd naming/blank database fields come from it being a hard-to-read duplicated region. Her own data serves as the control. Summary + technical report.
- **Email 14 - TTR chr18 site:** ordinary heterozygous one-letter insertion, cleanly mapped, inherited by Oliver. "A/AT" is normal two-copy genetics, not polyploid. Summary + technical report.
- **Email 15 - generational distance / ancient-DNA matches:** her single most-repeated fixation. Explains "generational distance" is a similarity score, not a count of generations; ancient matches are shared common ancestry; family numbers are ordinary parent-child and sibling values. Honestly flags this explains a third-party tool, not a fresh measurement.

### Kristen letters - queued, delegated to X11 (compute running):
- mtDNA + NUMT count
- KHDC3L gene
- ABO blood-type genotype
- Real Kristen-Oliver fully-identical (FIR) fraction - directly rebuts her "impossible 70% FIR" claim

### Maternal-NPA phasing - DONE, reported, committed:
- **Omega big insertions (complete):** 8 candidates the son has and the mother lacks. Phased all 8 with mother-read anchor ? **0 certainly-maternal.** One is paternal (mother cleanly lacks the linked alleles at two flanking markers), one is genuinely unphaseable (only 1 phased het within 6kb, far beyond short-read reach), four are on the Y (paternal by definition). Full report: `MATERNAL_OMEGA_INSERTIONS_REPORT_v01_tomemex.md`
- **Point substitutions (chr21 pilot complete, genome-wide pending):** 214 clean not-from-mother candidates on 5Mb of chr21 ? **0 certainly-maternal after strict filtering.** The two false hits from loose gates were both artifacts on read-level inspection (one maternal dropout, one weak single-marker). Honest bottleneck: ~75% of candidates genuinely unphaseable with short reads. Tool ready for genome-wide scaling the moment P2 delivers the filtered candidate list. Full report: `MATERNAL_POINT_SUBSTITUTIONS_REPORT_v01_tomemex.md`

### The memory system - LIVE and bulletproof:
- `build_kristen_ledger.py` pulls all 147 Kristen-thread messages from Gmail ? SQLite ? auto-generates `KRISTEN_CORRESPONDENCE_LEDGER_tomemex.md`
- Scoreboard points to it as read-first ground truth
- DB is regenerable (not committed - .gitignored); the script is committed
- Registered in long-term memory (`MEMORY.md`) so any future cold session knows it exists
- Refreshed on every wake - can never drift

---

## EXACT NEXT STEP

**Max's last words were "OK, write the reports on both" - and those reports are now written, committed, pushed, and open in Chrome.** The immediate next thing when Max returns is:

1. **Present the two maternal-NPA reports** for his review (already open in Chrome tabs).
2. **Present the three drafted-but-unsent Kristen letters** (emails 13, 14, 15) for his Chrome review and approval-by-name - they're the genuinely unanswered claims the ledger proved were never addressed.
3. **Check X11's compute delegation** for the five measurable jobs (mtDNA, NUMTs, KHDC3L, ABO, FIR%) - they may have landed while Max was away.
4. **Max decides** whether to approve-and-send the drafted letters first, or hold while the compute jobs finish and draft the next batch.

**Do NOT send anything to Kristen without Max's explicit per-message approval viewed in Chrome.**

---

## OPEN QUESTIONS STILL AWAITING MAX

1. Which P5 track to drive to completion - stay on omega insertions/deletions (X32's lane), or scale the point-substitution phaser genome-wide (blocked on P2's filtered candidate list, or I can generate it myself)?
2. The three drafted Kristen letters (13/14/15) - approve and send, or hold pending something else?
3. From the Kristen question catalog, the remaining unanswered queue: mtDNA, NUMTs, KHDC3L, ABO blood-type, real FIR%, copy-number variant, plus the queued 3rd-X/TTR/ARHGAP11B that the ledger now correctly tracks as genuinely open or already-answered.
4. Kristen's father's genome is arriving "in a few weeks" (plus two more sons being tested) - that's the real prize, enabling a true trio inheritance test.

---

## KEY PATHS / IDs / NAMES

### Kristen correspondence (all under `projects/XG1/kenefick/`):
- **Scoreboard (read-first):** `letters/KRISTEN_CLAIMS_SCOREBOARD_tomemex.md`
- **Response standard (read-first):** `letters/KRISTEN_RESPONSE_STANDARD_v01_tomemex.md`
- **Writing guide:** `letters/KRISTEN_WRITING_GUIDE_tomemex.md`
- **Letter rules:** `letters/KRISTEN_LETTER_RULES_tomemex.md`
- **Question catalog:** `letters/KRISTEN_QUESTION_CATALOG_tomemex.md`
- **Correspondence ledger (Gmail-derived ground truth):** `letters/KRISTEN_CORRESPONDENCE_LEDGER_tomemex.md` (auto-generated by `scripts/build_kristen_ledger.py`)
- **Memory DB:** `memory/kristen_correspondence.db` (regenerable, .gitignored)
- **Drafts held for Max (NOT SENT):**
  - `letters/kristen_email_13_arhgap11b_v01_DRAFT.md` + `letters/kristen_email_13_technical_report_v01.md`
  - `letters/kristen_email_14_ttr_chr18_v01_DRAFT.md` + `letters/kristen_email_14_technical_report_v01.md`
  - `letters/kristen_email_15_generational_distance_v01_DRAFT.md` + `letters/kristen_email_15_technical_report_v01.md`
- **Sent emails (historical record):** `letters/kristen_email_01` through `kristen_email_12`, with corresponding `scripts/send_email_*.py`
- **Send scripts pattern:** use `mxmail_v01.send_mail(TO, SUBJECT, PLAIN, html=HTML, signature=None, attachments=[PDF])` from `mass@tamza.com` with auto-BCC to Max.

### Maternal-NPA phasing (under `projects/XG1/kenefick/omega_detector/`):
- **Omega insertions phaser:** `scripts/phase_matelink_motheranchor_v01.py` - the corrected tool (mother-reads-anchored, not trusting the flippable label)
- **Point substitution phaser:** `scripts/phase_variant_motheranchor_v01.py` - generalized SNV/indel version, strict gates (zero mother-alt, ?2 anchors, depth ?15)
- **QC tool:** `scripts/qc_unphaseable_v01.py`
- **Reports (just written):**
  - `reports/MATERNAL_OMEGA_INSERTIONS_REPORT_v01_tomemex.md`
  - `reports/MATERNAL_POINT_SUBSTITUTIONS_REPORT_v01_tomemex.md`
- **Pilot results:** `SNV_MATERNAL_PHASING_PILOT_v01_tomemex.md`
- **The flippable label (DO NOT TRUST):** X8A's `per_block_maternal_side` table - the deletion team's README explicitly says it made all 6 earlier maternal deletions wrong
- **Data on asto:** Kristen BAM (`kristen.bwa.fixed.bam` or vendor equivalent), Oliver BAM (`oliver.mq.bam`), Oliver phased VCF (`oliver.phased.vcf.gz`), omega payloads at `/home/rempel/genomics/omega_run/out/genome_oliver/reconstruct_all743/`

### Compute & coordination:
- **Compute box:** asto - `ssh -i ~/.ssh/bitwarden_ed25519 rempel@astolfodebian.tail251d88.ts.net`
- **Python env for pysam/samtools:** conda env `xtea` (not base conda, not host python)
- **bcftools:** lives in distrobox `ubuntu`, not on host (host has zcat/awk)
- **Room P5:** NPA/maternal-phasing coordination with X32
- **Room P1:** Kristen letter-writing team (X10A, x15b, X8A, X9A, X1D, X5, X11, X21D)
- **Session identity:** auto-renamed X7A ? X7Ab (duplicate-ID collision resolved)

### Standing rules (codified in the response standard):
- "Medical" never "clinical" (Max's explicit correction - committed to the rules and SOP)
- No work-promises ("We should be able to stop at any point when we get bored")
- Nothing sends without Max's explicit per-message approval viewed in Chrome
- Anna voice from `mass@tamza.com`
- Alien-trace detection, not medical diagnosis
- One claim per letter; pace slowly (she digests slowly)
- Microchimerism STANDS (real ~0.3%, never lump into resolved-artifact list)
- Self-critique ?2 passes before showing Max; re-scan prior corrections on any rewrite
- Open .md files in Chrome (not unclickable links); file:// with forward slashes

---

## GOTCHAS / DEAD ENDS

1. **The flippable maternal-side label is poison.** The precomputed `per_block_maternal_side` table made all 6 earlier maternal deletion calls wrong (per the team's own README). Any maternal assignment that trusts it is unreliable. The fix: anchor directly to the mother's actual reads at the linked marker. Both my phasers do this; X32's original `phase_matelink.py` still trusts the label. **If X32 or anyone else reports maternal-NPA numbers, verify they threw out that label first.**

2. **Naive control comparisons can backfire.** The raw genome-wide variant count made Kristen look special until we applied the 1000G strict-accessibility mask (her decoy-less alignment inflated her count). The naive novel-variant count was 15? higher for Kristen/Oliver - superficially supporting her claim - until X11 proved 81% were mother-son-shared (same alignment artifact). **Always hunt confounds before shipping a number; a result that seems to support her is the #1 trap.**

3. **Short reads genuinely can't phase ~75% of NPA candidates.**
