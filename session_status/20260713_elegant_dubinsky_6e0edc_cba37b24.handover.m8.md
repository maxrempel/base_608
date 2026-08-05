# Scribe handover - milestone 8 (~658K tokens)
# session: 20260713_elegant_dubinsky_6e0edc_cba37b24
# cwd: C:\claude_base\.claude\worktrees\elegant-dubinsky-6e0edc
# written: 2026-07-13 14:33:00 by deepseek-v4-pro

# HANDOVER - Kristen Kenefick Letter Writing (X7A)

---

## GOAL (in Max's words)

Answer Kristen's open genetics claims systematically. No more polling for her replies - "You have tons more work." The queue of unanswered claims is sitting right there. Produce rigorous, two-deliverable responses (plain summary email + PDF technical report) under the formalized standard, with controls-not-assertions, every number defined and quantified. Nothing sends without Max's explicit per-message approval viewed in Chrome.

---

## DECISIONS MADE + WHY

**1. The Two-Deliverable Response Standard (Max's #1 directive)**
Every quantitative claim gets: (a) a plain-language summary email, and (b) a rigorous methodological PDF technical report (Objective / Samples / Methods / Results tables / Limitations / Conclusion). Created because Max was sick of vague, undefined, hand-wavy drafts. Codified in `KRISTEN_RESPONSE_STANDARD_v01_tomemex.md` and wired read-first into the scoreboard so future writers comply automatically.

**2. Controls-not-assertions with accessibility mask**
Don't assert Kristen is normal - prove it by running the identical pipeline on three unrelated control genomes (NA12718 European, NA18530 East Asian, NA18488 African), restricted to the 1000 Genomes strict-accessibility mask (excludes low-complexity/repetitive regions where short reads misbehave). The mask is critical: without it, Kristen looks artificially inflated because her BAMs lack decoy/ALT contigs.

**3. "medical" not "clinical" (Max's explicit instruction)**
"Clinical" is banned from Kristen correspondence. Fixed in the letter-rules template (which every new letter uses), the response standard's self-critique checklist, and email 12 templates. Exception: only when quoting a literal database field name (e.g., "ClinVar clinical significance") - never our own framing.

**4. ARHGAP11B and TTR - no external controls needed**
Max said "I don't think it's necessary" to run controls for ARHGAP11B and TTR. The "control" is built into her own data: the gene sits at normal depth alongside a single-copy reference region, or the notation is standard and the reads are cleanly mapped. So letters 13 and 14 were drafted without compute delegation.

**5. The correspondence memory system**
The old scoreboard drifted from reality - it listed "3rd X" as open when it was already answered in email 01. Max was pissed: "How is it possible that your summary of your emails is not saved?" So I built `build_kristen_ledger.py` - pulls the full Kristen Gmail thread (147 messages) via semantic-mail's auth, stores in SQLite, auto-writes a regenerable ledger (`KRISTEN_CORRESPONDENCE_LEDGER_tomemex.md`) that maps every outbound letter to the claim it answered. Because it's from Gmail, it can't drift. Wired read-first in the scoreboard. Committed to master.

**6. Killed the reply-polling timer**
Max explicitly: "What the fuck is happening? Why do you check for replies from Kristen? How does it matter? You have tons more work." Timer shut off (`timer_decel.py off`). Her reply gates nothing; the open queue is the work.

---

## CURRENT STATE

**SENT (emails 01-12, all from mass@tamza.com, BCC to Max):**
- 01: triple-X (karyotype + VCF notation) - SENT+CLOSED
- 02: extra-Y / male-DNA microchimerism (~0.3%) - STANDS as real (not artifact), Max satisfied
- 03: 1500+ inversions ? ~29 real, ~15-18 after dedup
- 04: rs2081743753 - common TTCCA repeat + mismapping artifact
- 05b/07: aunt/cousin segment-sharing dominance (collateral-relative variance)
- 06: trust-repair note - drafted, superseded when Max handled it personally
- 08: Mendelian-dominance ("father barely inherited") - 50-50 rule holds, 405,465 obligate-paternal alleles
- 09: topic map ("back to work")
- 10: 30X microchimerism - full argument (colander analogy, uniformity, son-specific, "~half of women")
- 11: easy answers (99.9% correction, 2.2M positions explanation)
- 12: novel-architecture / chromatin - summary + PDF technical report (5-genome SNV table, H3F3B coverage, novel-count confound excluded)

**DRAFTED - HELD FOR MAX'S REVIEW/APPROVAL (DO NOT SEND):**
- **Email 13** (`kristen_email_13_arhgap11b_v01_DRAFT.md` + `kristen_email_13_technical_report_v01.md`): ARHGAP11B gene - present at full normal depth, no deletion/silencing. The "one-third" is the gene's natural human structure (partial duplicate by design). Her own data shows normal coverage alongside a single-copy control region.
- **Email 14** (`kristen_email_14_ttr_chr18_v01_DRAFT.md` + `kristen_email_14_technical_report_v01.md`): Chromosome 18 TTR site - ordinary heterozygous one-letter insertion (A/AT), cleanly mapped, inherited by Oliver. Normal two-copy genetics, not "polyploid."
- **Email 15** (`kristen_email_15_generational_distance_v01_DRAFT.md` + `kristen_email_15_technical_report_v01.md`): Generational distance / ancient-DNA matches - explains "generational distance" is a similarity score (not generations), ancient matches are shared common ancestry, and her family numbers are ordinary parent/child and sibling values. Honestly flags this explains a third-party tool, not a new genome measurement.

**DELEGATED TO COMPUTE WORKER X11 (via p1 room) - 5 JOBS IN FLIGHT, NO RESULTS YET:**
- Kristin's mtDNA + NUMT count
- KHDC3L gene coverage/status
- ABO blood-type actual genotype
- Real fully-identical (FIR) fraction between Kristen and Oliver (rebuts her "impossible 70% FIR" claim)
- These compute on asto using Kristen's and control VCFs

**STANDING RULES:**
- Sending is fully paused (plan-only) until Max gives explicit per-message approval by name, viewed in Chrome
- Voice: Anna, from mass@tamza.com
- Goal stated: alien-genetic-trace detection - not medical, not diagnosis
- Microchimerism STANDS (real ~0.3% finding) - never lump into resolved-as-artifact list
- "clinical" ? "medical" everywhere
- No vague minimizers ("slightly," "a little") without the exact number
- No undefined tables - name the metric, give units, column headers
- Hunt confounds: a number that superficially supports Kristen is the #1 trap
- Self-critique >=2 passes before presenting to Max, re-scan prior-correction regressions
- No promises of future work - "We should be able to stop at any point when we get bored"

---

## EXACT NEXT STEP

The session ended with the question: **"Want me to open the four drafts in Chrome so you can read and approve them, or keep drafting while the worker computes?"** - Max hasn't answered. The cold session should:

1. Open drafts 13, 14, 15 in Chrome for Max to read (plus remember 13+14 had two earlier drafts from before the compaction - only 13/14/15 are newly drafted in this window)
   - Correction: there are 3 drafts waiting (13 ARHGAP11B, 14 TTR, 15 generational distance), plus the question catalog had them all listed
   - Wait - re-reading: emails 13/14 were drafted earlier in the pre-compaction window and then 15 was drafted post-compaction. All three are drafted and held.

2. Check whether X11 has returned results on the 5 delegated jobs (mtDNA, NUMTs, KHDC3L, ABO, FIR) - if yes, draft those next; if not, check the p1 room and nudge

3. Continue drafting from the open question catalog using the memory ledger as ground truth - the remaining unanswered ones are: mtDNA, NUMTs, KHDC3L, ABO/blood-type, ancient-DNA matches (email 15 covers the "generational distance" framing but the specific ancient-match files she sent may need a separate look), the copy-number variant she sent, and the low-priority ones

---

## OPEN QUESTIONS AWAITING MAX

- **Approve emails 13, 14, 15 for sending?** (ARHGAP11B, TTR, generational distance)
- **Prioritization of the remaining queue** - the 5 delegated jobs will produce results for mtDNA/NUMTs/KHDC3L/ABO/FIR; in what order after that?
- **Her father's genome arriving "in a few weeks"** - real trio inheritance test becomes possible then; revisit strategy?
- **The copy-number variant she sent by email** - triage or answer?

---

## KEY FILES AND PATHS

- **Canonical docs (read-first):**
  - `C:\claude_base\projects\XG1\kenefick\letters\KRISTEN_CLAIMS_SCOREBOARD_tomemex.md` - master claim tracker (READ FIRST on resume)
  - `C:\claude_base\projects\XG1\kenefick\letters\KRISTEN_RESPONSE_STANDARD_v01_tomemex.md` - the two-deliverable quality SOP
  - `C:\claude_base\projects\XG1\kenefick\letters\KRISTEN_QUESTION_CATALOG_tomemex.md` - Kristen's unanswered questions
  - `C:\claude_base\projects\XG1\kenefick\letters\KRISTEN_LETTER_RULES_tomemex.md` - x15b-maintained writing rules + disclaimer template ("medical" not "clinical")
  - `C:\claude_base\projects\XG1\kenefick\letters\KRISTEN_WRITING_GUIDE_tomemex.md` - psychology profile + numbered guide rules

- **Memory system:**
  - `C:\claude_base\projects\XG1\kenefick\scripts\build_kristen_ledger.py` - regenerates the correspondence DB from Gmail
  - `C:\claude_base\projects\XG1\kenefick\memory\kristen_correspondence.db` - SQLite DB (regenerable, gitignored)
  - `C:\claude_base\projects\XG1\kenefick\letters\KRISTEN_CORRESPONDENCE_LEDGER_tomemex.md` - auto-generated plain-English ledger
  - `C:\claude_base\projects\XG1\kenefick\memory\KRISTEN_MEMORY_SYSTEM_v01_tomemex.md` - method doc
  - Refresh command: `PYTHONUTF8=1 C:/Users/maxre/semantic-mail/.venv/Scripts/python.exe C:/claude_base/projects/XG1/kenefick/scripts/build_kristen_ledger.py`

- **Drafts held for Max (email 13-15):**
  - `C:\claude_base\projects\XG1\kenefick\letters\kristen_email_13_arhgap11b_v01_DRAFT.md`
  - `C:\claude_base\projects\XG1\kenefick\letters\kristen_email_13_technical_report_v01.md`
  - `C:\claude_base\projects\XG1\kenefick\letters\kristen_email_14_ttr_chr18_v01_DRAFT.md`
  - `C:\claude_base\projects\XG1\kenefick\letters\kristen_email_14_technical_report_v01.md`
  - `C:\claude_base\projects\XG1\kenefick\letters\kristen_email_15_generational_distance_v01_DRAFT.md`
  - `C:\claude_base\projects\XG1\kenefick\letters\kristen_email_15_technical_report_v01.md`

- **Infrastructure:**
  - Send pattern: create `send_email_NN_*.py` in `scripts/`, imports `mxmail_v01.send_mail`, from mass@tamza.com, auto-BCC max.rempel2, supports `attachments=[PDF_path]`
  - PDF generation: markdown lib ? HTML ? Chrome headless `--print-to-pdf`
  - asto: `ssh -i ~/.ssh/bitwarden_ed25519 rempel@astolfodebian.tail251d88.ts.net`
  - bcftools: inside distrobox `ubuntu`, not on asto host
  - bcast room: `p1` (Kenefick project coordination)
  - Scoreboard + catalog + ledger edited via the ledger refresh, not hand-updated

---

## GOTCHAS AND DEAD ENDS

- **Kristen/Oliver have decoy-less alignments** - their BAMs were aligned to primary assembly only (25 contigs, no decoy/ALT/HLA). This inflates their raw SNV count by ~7% because reads that belong on decoy/ALT sequences mismap onto primary chromosomes and keep high MAPQ (no competing location). Always use
