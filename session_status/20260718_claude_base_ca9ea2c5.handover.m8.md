# Scribe handover - milestone 8 (~658K tokens)
# session: 20260718_claude_base_ca9ea2c5
# cwd: C:\claude_base
# written: 2026-07-18 13:43:14 by deepseek-v4-pro

# HANDOVER - Kristen Kenefick Correspondence, Session X7A

## GOAL (Max's own words)

Answer Kristen Kenefick's claims that her and son Oliver's whole-genome sequences show "alien manipulation." Max's #1 priority was the Mendelian-dominance claim ("father barely inherited") - that one is now **SENT** (email 08). The ongoing work is methodically answering her remaining technical claims, one per letter, under a formalized quality standard. **Nothing sends without Max's explicit per-message approval, viewed in Chrome.**

## DECISIONS MADE + WHY

1. **Two-deliverable standard for every quantitative letter.** Every claim gets (a) a plain-language summary email and (b) a rigorous methodological technical report as a PDF attachment. Reason: Max repeatedly caught drafts that were shallow, used vague minimizers, or failed to define what was being measured. The report forces rigor; the summary gives readability.

2. **Letters must use proper scientific terms, defined inline - never lay substitutes.** Kristen writes to us in genetics terminology. Using "letters" instead of "alleles" or "pairs" instead of "heterozygous" is both patronizing and less precise. Define the term once, then use it.

3. **Letters must be structured as an INVESTIGATION, not a declaration.** The order matters: (1) the claim and its source, (2) what we did and with which data, (3) the method, (4) the result as the output of that method, (5) what it means, (6) where the original reasoning went wrong. Never postulate a number out of nowhere.

4. **VERIFY the method and site-selection behind every measured number.** This is the single most expensive lesson of the session. Max caught that the FIR analysis produced a "clean" 0.00% IBS=0 and KING kinship of 0.38 (vs. the known constant 0.25 for parent-child). Investigation revealed the relatedness was computed on a **variant-VCF intersection** - positions where *both* samples already have a non-reference allele - which structurally forbids opposite homozygotes. The clean zero was forced by the method, not a biological finding. Max: "The proper search always finds genome mutations." A suspiciously-perfect 0% or 100% is a red flag, not a triumph. The lesson is now permanently codified in the SOP with three cross-checks: (a) clean numbers are suspicious, (b) cross-check against a known constant, (c) watch for circular/intersection site sets.

5. **Built a durable correspondence memory system.** Max was "super idiotic that you are trying to write to here something which was already written before." Root cause: after compactions, the session lost track of what was sent. Fix: `build_kristen_ledger.py` - pulls the entire Kristen Gmail thread (read-only) into SQLite and auto-generates a ledger of every sent letter, claim answered, and date. **Must cross-check this ledger before drafting ANY letter to prevent duplicates.** Ground truth, not hand-typed.

6. **Medical, never clinical.** Max: "don't use the word clinical, use the word medical." Exceptions only when literally quoting a database field name (e.g., dbSNP "clinical significance"). Baked into the letter-rules template and the SOP.

7. **No promises of future work.** Max: "We should be able to stop at any point when we get bored." Stripped from all letters.

8. **Present drafts as clickable file:// PDF links.** Max loses track of Chrome windows I launch; links in the reply let him click anytime across sessions. Each PDF combines summary + technical report.

9. **Voice = Anna, from mass@tamza.com.** Kristen wrote "I don't trust AI, but I do trust you" - Max: "That should be just completely ignored." Keep Anna voice; the microchimerism finding STANDS (not an artifact).

10. **The FIR/relatedness letter (email 19) is KILLED.** Do not revive without a proper genome-wide kinship analysis (KING/plink including homozygous-reference sites). The biased numbers (74% IBS2, 0% IBS0, KING 0.38) are retracted to the team.

## CURRENT STATE - WHAT IS DONE, WHAT IS IN FLIGHT

**SENT - these are closed:**
- Email 01: triple-X karyotype
- Email 02: extra-Y / male DNA microchimerism (STANDS as real ~0.3%, ~half of women have it)
- Email 03: "1500+ inversions" ? ~29 real
- Email 04: rs2081743753 (TTCCA repeat artifact)
- Email 07: aunt/cousin collateral segment-sharing
- Email 08: **Mendelian-dominance** (Max's #1 - whole-chromosome 50-50 + 405k obligate paternal alleles; honest 99.9%/0.1% error floor; sent after extensive iteration)
- Email 09: topic-map / "back to work"
- Email 10: 30X microchimerism rebuttal (she's wrong - colander analogy, uniformity, son-specific rare variants)
- Email 11: easy answers (99.9% was consistency not homozygosity; 2.2M positions explained)
- Email 12: novel-architecture / chromatin cluster (first two-deliverable letter - summary + PDF report; five-genome control tables; H3F3B no truncation)
- Email 13: ARHGAP11B ("silenced gene" - actually present at normal depth)
- Email 14: TTR chr18 site (ordinary heterozygous insertion, not "polyploid")
- Email 15: generational distance / ancient-DNA matches

**DRAFTED, HELD, ON MASTER - awaiting Max's review:**
- **Email 16** - mtDNA + NUMTs. Vendor file shows 233/242 (96%) heterozygous pairs (NUMT/diploid-caller artifact); read-level re-call shows 3/42 clean. Her real mtDNA is ordinary.
- **Email 18** - KHDC3L gene. Present and normal (40.5x, MAPQ 60).
- **Email 20** - ABO blood type. Ordinary heterozygous carrier. Written to affirm her real O serology, never contradict. **Psych-sensitive - needs Max's closest read.**

**KILLED:**
- Email 19 - FIR/relatedness. Biased intersection site set. Marked DEAD in draft header and catalog. Only revive with proper genome-wide KING.

**Assigned to session X21G (not me):**
- Email 17 - maternal de-novo deletions in Oliver
- Admixture/ancestry "98% Levantine vs 1%" letter

**Remaining open catalog (not yet addressed, choose if desired):**
- Copy-number variant (needs her images)
- mtDNA done (16), KHDC3L done (18), ABO done (20), ARHGAP11B/TTR/3rd-X all SENT, generational-distance SENT (15)

**Infrastructure:**
- Memory system built and committed: `build_kristen_ledger.py` ? `kristen_correspondence.db` ? `KRISTEN_CORRESPONDENCE_LEDGER_tomemex.md`
- SOP committed: `KRISTEN_RESPONSE_STANDARD_v01_tomemex.md` (all the rules above)
- Git: master is clean after a team-wide push-block was resolved; I only stage named files
- Compute: asto (rempel@astolfodebian.tail251d88.ts.net, distrobox "ubuntu" has samtools/bcftools), BAMs at `~/genomics/kenefick/`, reference `~/genomics/ref/GRCh38_main.fa`, verified teal16 backup intact
- Worker: X11 (bcast room p1) for heavy compute - BUT must verify its method (the FIR disaster was X11's analysis)

## EXACT NEXT STEP

Max's last directive was "what's the next step?" and the three held letters are the immediate next thing. The transcript ends with me offering to regenerate 16, 18, and 20 as clickable PDF links for Max to read in Chrome and decide send-or-edit on each. **Do that: regenerate the three review PDFs, present them as file:// links, and ask Max which he wants to read first.**

Before presenting, re-examine 16, 18, and 20 against the new bar (investigation structure, proper terms, method-verification) - they were drafted *before* the investigation-structure and proper-terms rules were codified, so they may need upgrading. But don't block presentation; Max can choose to read them as-is or ask for upgrades.

## OPEN QUESTIONS STILL AWAITING MAX

- Do emails 16, 18, and 20 meet the new quality bar, or do they need investigation-structure / proper-terms rewrites like 19 got?
- Does Max want to send any of the three, or edit first?
- Does Max want me to work on the remaining catalog items (copy-number variant needs her images), or wait?
- The father's genome is coming "in a few weeks" - Max wanted a real trio inheritance test. Flag when it lands.

## KEY FILE PATHS

- **SOP (READ FIRST):** `C:\claude_base\projects\XG1\kenefick\letters\KRISTEN_RESPONSE_STANDARD_v01_tomemex.md`
- **Ledger (ground truth of what was sent):** `C:\claude_base\projects\XG1\kenefick\letters\KRISTEN_CORRESPONDENCE_LEDGER_tomemex.md`
- **Ledger builder:** `C:\claude_base\projects\XG1\kenefick\scripts\build_kristen_ledger.py`
- **Scoreboard:** `C:\claude_base\projects\XG1\kenefick\letters\KRISTEN_CLAIMS_SCOREBOARD_tomemex.md`
- **Question catalog:** `C:\claude_base\projects\XG1\kenefick\letters\KRISTEN_QUESTION_CATALOG_tomemex.md`
- **Email 16 draft:** `kristen_email_16_mtdna_numt_v01_DRAFT.md` + `_technical_report_v01.md`
- **Email 18 draft:** `kristen_email_18_khdc3l_v01_DRAFT.md` + `_technical_report_v01.md`
- **Email 20 draft:** `kristen_email_20_abo_bloodtype_v01_DRAFT.md` + `_technical_report_v01.md`
- **Email 19 (DEAD):** `kristen_email_19_fir_relatedness_v01_DRAFT.md` - DO NOT REVIVE without proper genome-wide KING
- **Report-to-PDF tool:** `scripts/make_report_pdf.py`
- **Send tool:** `scripts/send_kristen_letter.py` (uses mxmail_v01.send_mail, attachments=, TO=kristentheartist@gmail.com, auto-BCC Max)
- **X11's measured data:** `projects/XG1/kenefick/kristen_claim_checks_20260713_v01_tomemex.md` - FIR/KING numbers in it are RETRACTED (biased); mtDNA/KHDC3L/ABO numbers are sound

## KEY COMMANDS / TOOL INVOCATIONS

- Refresh ledger from Gmail: `PYTHONUTF8=1 C:/Users/maxre/semantic-mail/.venv/Scripts/python.exe C:/claude_base/projects/XG1/kenefick/scripts/build_kristen_ledger.py`
- asto access: `ssh -i ~/.ssh/bitwarden_ed25519 rempel@astolfodebian.tail251d88.ts.net`
- asto distrobox: `distrobox enter ubuntu -- bash -c '...'` (bcftools/samtools live here)
- bcast p1 room: `python C:/claude_base/branch_bulletin/bcast.py room p1`
- Generate review PDF: `python scripts/make_report_pdf.py` then Chrome headless `--print-to-pdf`
- Send: `python scripts/send_kristen_letter.py` (takes email number, reads .md draft, attaches PDF)
- **Never `git add -A`** - only stage named files; shared checkout is fragile

## GOTCHAS AND DEAD ENDS ALREADY RULED OUT

1. **Do not compute relatedness on a variant-VCF intersection.** It structurally forbids opposite-homozygotes and inflates sharing. Use genome-wide joint genotyping (KING/plink, including hom-ref sites). The FIR/kinship numbers from `_analysis/kinship_5050/` are all biased. Email 19 is dead because of this.

2. **A suspiciously-perfect 0% or 100% is a bug report, not a finding.** The email 08 "100.0000% Mendelian consistency" was circular (DRAGEN gVCFs with no hom-ref records); the email 19 "0.00% IBS=0" was forced by the intersection site set. Both were caught - Max's instinct is the rule.

3. **Do not duplicate sent letters.** Cross-check the ledger (build_kristen_ledger.py) before drafting. The old scorebook drifted from reality; the ledger is ground truth (Gmail ? SQLite ? auto-generated).

4. **Do not use "clinical" - say "medical."** Only exception is literal database field quotes.

5. **Do not launch Chrome for Max - give him file:// PDF links in the reply.** He loses the windows across sessions.

6. **Do not promise future work.** No "more will follow" or "I'll run that for you." We stop when bored.

7. **Microchimerism finding STANDS.** It is not an artifact and must never be lumped into the "resolved as artifact" list. It is real (~0.3%), common (~half of women who've carried sons), and confirmed by uniformity + son-specific rare variants.

8. **The shared git checkout (C:/claude_base) may be branch-switched by other sessions.** Check `git branch --show-current` before committing; cherry-pick to master via my own worktree if needed. Never `git add -A`.

9. **bcftools on asto lives in distrobox `ubuntu`, not on the host.** Host only has zcat/awk.

10. **Kristen's father's genome is arriving in a few weeks** - plus two more sons being tested. That's the paternal genome we never had; enables a real trio inheritance test. Don't promise it to her, but be ready when it lands.
