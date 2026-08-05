# Scribe handover - milestone 8 (~601K tokens)
# session: 20260713_recursing_jemison_10c3c5_69b9ca76
# cwd: C:\claude_base\.claude\worktrees\recursing-jemison-10c3c5
# written: 2026-07-13 08:08:31 by deepseek-v4-pro

# Handover - X7A (Kristen Kenefick writer), Session `recursing-jemison-10c3c5`

---

## GOAL (Max's words)
Respond to Kristen's latest claim - that her and Oliver's genomes show a "completely novel architecture" versus GRCh38, "thousands of novel germline variants," and a "large truncation in H3-3B" that "should never have survived meiosis." Max's directive: **do not assert; use controls**. Measure the same things on three unrelated genomes (NA12718, NA18530, NA18488) and put the numbers side by side. The argument is: if the strangers show the same, it's universal-human, not novel architecture. Draft only, never send without Max's explicit per-letter approval by name.

---

## WHAT'S DONE

**Sent (4 letters this session):**
- **Email 08** - Mendelian-dominance ("father barely inherited"): refuted with whole-chromosome 50-50 structure + obligate-paternal alleles + 99.9% Mendelian consistency scan. Stands behind the microchimerism finding. Kristen didn't fight it.
- **Email 09** - topics/map: listed all her open questions so nothing is lost, noted the 30X one comes first.
- **Email 10** - 30X microchimerism rebuttal: the full evidence chain (averaging across many loci, colander/??????? analogy, uniformity across 100 genome segments, son-specific rare variants, "common in ~half of women"). Firm: her conclusion that 30X can't detect it is wrong.
- **Email 11** - easy answers: corrected her misread of 99.9% (it was Mendelian consistency, NOT homozygosity - real homozygosity is ~2.6%, normal) and explained why only 2.2M positions were tested (the rest are identical in everyone).

**Email 12 - drafted, NOT sent, open in Chrome:**
- Answers the "novel architecture" / chromatin claim via side-by-side control tables.
- **Table A** - single-nucleotide variant (SNV) count vs GRCh38, restricted to the reliably-mappable genome across 5 chromosomes (chr1,2,20,21,22). Kristen 570,922; European control 569,425 (0.3% apart); Oliver 574,854; all within normal range. African control is 704,791 (ancestry-driven).
- **Table C** - H3F3B (H3-3B) read depth across the gene body. All five people fully covered (Kristen 40?, Oliver 84?, controls 32-39?). A real truncation would collapse coverage to near zero. It's the known H3.3 paralog artifact.
- **Novel-variant count (Table B) deliberately excluded** - X11 discovered it backfires: K/O show ~15? more "novel" variants naively, but 81% are shared between mother and son (real novelty wouldn't be). It's an artifact of their shared alignment lacking decoy/ALT contigs. Handled in prose instead.

**Team/infra:**
- Created dedicated **p1 room** (`bcast.py room p1`) to keep Kristen-project traffic off the main board. Members: X7A, X10A, X8A, X9A, X1D, X5, X21D, X11, x15b.
- X11 is the active compute worker for control-genome comparisons (on asto, accessible via Tailscale/SSH).
- asto cleanup completed by X8A (90% ? 47% disk).
- All letter sends use `mass@tamza.com` with auto-BCC to Max. Send scripts at `C:\claude_base\projects\XG1\kenefick\scripts\send_email_XX_*.py`.

---

## EXACT CURRENT STATE
Email 12 (`kristen_email_12_novel_architecture_v01_DRAFT.md`) is drafted with revised (scientifically precise) table definitions and **open in Chrome** - Max's last feedback on this file was that the definitions were imprecise ("DNA differences" is not sufficient, must be scientifically correct). The definitions have been updated to name SNVs and read depth explicitly. **Max has not yet responded to the revised version** - his last words were the demand for precise definitions, and the transcript ends with me reopening the revised file in Chrome. Nothing is approved. Nothing is sent.

---

## EXACT NEXT STEP
**Max needs to read the revised email_12 in Chrome and give feedback.** The letter is open in his browser. The immediate questions he'll likely have:
1. Are the table definitions now precise enough? (Current headers: "Single-nucleotide variants (vs GRCh38)" and "Mean read depth over the gene.")
2. Any other language to tighten or cut.
3. Once he approves: do NOT send autonomously - explicit per-message approval by name is standing rule.

---

## KEY PATHS
- **Email 12 draft:** `C:\claude_base\projects\XG1\kenefick\letters\kristen_email_12_novel_architecture_v01_DRAFT.md`
- **Claims scoreboard:** `C:\claude_base\projects\XG1\kenefick\letters\KRISTEN_CLAIMS_SCOREBOARD_tomemex.md`
- **Question catalog:** `C:\claude_base\projects\XG1\kenefick\letters\KRISTEN_QUESTION_CATALOG_tomemex.md`
- **X11's control-table report (committed):** `projects/XG1/kenefick/kristen_control_table_20260713_v01_tomemex.md`
- **X11's analysis workspace on asto:** `~/genomics/_analysis/x11_controltable/`
- **5-genome call set (kinship pipeline):** `~/genomics/_analysis/kinship_5050/` on asto - Kristen, Oliver, NA12718, NA18530, NA18488
- **Broadcast:** `C:\claude_base\branch_bulletin\bcast.py`
- **p1 room:** `bcast.py room p1 --read`
- **Send scripts (pattern):** `C:\claude_base\projects\XG1\kenefick\scripts\send_email_*.py`
- **Opens in Chrome via:** `"C:/Program Files/Google/Chrome/Application/chrome.exe" "file:///C:/claude_base/projects/XG1/kenefick/letters/..."`

---

## GOTCHAS & DEAD ENDS
1. **Plan-only mode is standing** - nothing sends until Max gives explicit per-message approval by name. This is a HARD RULE after earlier violations.
2. **The Sonnet hour** - Max discovered mid-session that the model had been downgraded to Sonnet, producing "super idiotic" logic for about an hour. The session is now on Opus. Always verify model identity on resume; if Sonnet, scream and refuse to continue (Max's standing rule).
3. **The novel-variant table backfires** - do NOT reinstate a side-by-side novel-variant count in email 12. Naively, Kristen/Oliver show ~15? more "novel" variants, which appears to support her claim. X11 proved it's an artifact: 81% of those novel sites are shared between mother and son (real germline novelty wouldn't be), caused by their shared alignment lacking decoy/ALT contigs. Handle in prose only.
4. **The raw-vs-masked genome count trap** - raw genome-wide SNV counts made Kristen look special because her/Oliver's BAMs lack decoy/ALT contigs, so artifact reads inflate the count. The fix (X11's) is to restrict to the reliably-callable genome mask, where they land dead center of normal. Never quote raw genome-wide counts for K/O.
5. **Table definitions must be precise** - "DNA differences" was rejected as too vague. The column must name and define the exact thing being counted (single-nucleotide variant, read depth, etc.) in scientifically correct terms, not simplified.
6. **Never promise future work** - "more will follow" was cut from email 11. We stop whenever Max wants.
7. **The microchimerism BAM** - numbers in email_10 came from a vendor BAM that X8A deleted during cleanup. The numbers are safe in the committed report; a re-run would need re-alignment (byte-verified backup on teal16). Not a current blocker.
8. **x15b has NOT reviewed the Opus versions** of emails 09-12. Max said "don't bother" for email_08, but this may matter for future letters.
9. **Kristen is getting her father sequenced** (raw data in a few weeks) plus two more sons - that's the paternal genome we never had. Real trio analysis becomes possible then.
10. **Chrome, not links** - Markdown file links don't work in Max's client. Always open .md files via Chrome with forward slashes.

---

## OPEN QUESTIONS (awaiting Max)
- Is the revised email_12 (with precise SNV/read-depth definitions) now acceptable?
- Does he want any other changes before approving email_12?
- Priority order for remaining unanswered claims: mtDNA, NUMTs, KHD3CL gene, blood-type ABO/mosaicism, 3rd-X/multiallelic, TTR chr18, ARHGAP11B, ancient matches, ancestry/kinship.
