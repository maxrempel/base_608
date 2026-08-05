# Scribe handover - milestone 7 (~534K tokens)
# session: 20260712_recursing_jemison_10c3c5_69b9ca76
# cwd: C:\claude_base\.claude\worktrees\recursing-jemison-10c3c5
# written: 2026-07-12 21:21:50 by deepseek-v4-pro

# HANDOVER - X7A Kristen Kenefick Correspondence Writer

---

## GOAL (in Max's words)

Respond to Kristen's newest genetics claim - the "chromatin" cluster from her personal "Soul" thread - using **control-genome side-by-side tables** to refute it. Three sub-claims attacked: (A) her genome shows an "obvious shift from GRCh38 / completely novel architecture," (B) "thousands of novel germline variants" unique to her lineage, (C) "truncations throughout our genomes" including H3-3B. The refutation method is Max's controls-not-assertions principle: run the same count on three unrelated healthy controls (NA12718, NA18530, NA18488) and show her numbers are identical to everyone else's.

Max's standing rules unchanged: draft only, never send without his explicit per-message approval by name. Work autonomously - don't stop to ask questions, only halt for danger.

---

## DECISIONS + WHY

**Decision:** Refute the chromatin cluster entirely via control tables, not argument.
**Why:** Max's core principle - don't assert, show. Kristen says her genome is novel/different; put her numbers next to three strangers and let the table speak. She trusts data (or distrusts AI argument), so the table format lands harder.

**Decision:** Drop claim 3 ("should never have survived meiosis yet healthy") entirely.
**Why:** Max said it's too generic to address - it's a rhetorical kicker, not a testable genetics claim. Dropped.

**Decision:** Ignore the "I don't trust AI, but I trust you" voice-switch suggestion.
**Why:** Max said "completely ignored." All letters continue as Anna, from mass@tamza.com, per the established pipeline.

**Decision:** Ignore medical stuff (EEG, MRI, tinnitus, pineal) and the "father's genome coming" timing signal.
**Why:** Max said ignore both. Kristen explicitly said she doesn't want medical advice. The father's-genome news got no reply from Max either.

**Decision:** The data request went to X11 (a new worker Max spun up) rather than waiting for the sleeping team.
**Why:** asto is reachable; the data exists; I diagnosed the pipeline-mismatch problem myself and handed X11 a fully-scouted task so it doesn't rediscover anything.

**Decision:** The control VCFs in `_analysis/kinship_5050/controls/` are NOT comparable to Kristen/Oliver's VCFs - they were called by a different pipeline (bcftools recall, no dbSNP annotation, incomplete at ~0.9-1.1M SNPs vs the ~4.1M expected for WGS).
**Why I caught this:** I ran the counts myself on asto using awk on the raw VCFs. Kristen = 4.13M variants (60,320 novel, 1.46%), Oliver = 4.15M (64,765 novel, 1.56%). Controls = ~0.9-1.1M with zero PASS filter and no rsIDs - apples-to-oranges. X11 needs to re-run the controls through the same pipeline as Kristen/Oliver for a fair table.

---

## CURRENT STATE

**Completed earlier this session:**
- Email 08 (Mendelian-dominance, Max's #1 claim) - sent 2026-07-07 from mass@tamza.com. Refutes "father barely inherited" via whole-chromosome 50-50 + obligate paternal alleles. Clean, honest, Max-approved.
- Email 09 (topics/map + "back to work") - sent.
- Email 10 (30X microchimerism rebuttal, full argument: arithmetic, colander analogy, uniformity, son-specific rare variants, "common in ~half of women") - sent.
- Email 11 (easy answers: 99.9% homozygosity correction + 2.2M-positions explanation, no future-work promises) - sent.
- P1 project room created on bcast.py to keep main board quiet. Team moved: X10A, x15b, X8A, X9A, X1D, X5, X21D, X11, me.

**In flight - the chromatin letter (email 12):**
- Draft shell exists: `kristen_email_12_novel_architecture_v01_DRAFT.md`
- Kristen/Oliver columns filled with real numbers (computed by me on asto).
- Control columns marked PENDING X11.
- Three tables planned: A=total variants vs GRCh38, B=novel/rare variants (no-rsID), C=H3-3B truncation/loss (plus genome-wide truncation calls).
- A self-wake is armed (~30 min) to pick up X11's numbers, fill the blanks, and open the finished draft in Chrome.

**What X11 has been tasked with:**
- Re-call or harmonize the three controls through the same dbSNP-annotated pipeline as Kristen/Oliver (the `kinship_5050` files).
- Report: total PASS SNP count, novel (no-rsID) count + %, plus H3F3B (H3-3B) coverage/SV status for all five.
- Exact data location: `~/genomics/_analysis/kinship_5050/` on asto (rempel@astolfodebian.tail251d88.ts.net, key at `~/.ssh/bitwarden_ed25519`).

---

## EXACT NEXT STEP

1. **Check X11's reply** in the p1 room (`bcast.py room p1 --read`). If the three control numbers landed, fill the PENDING cells in the email 12 draft table, remove all PENDING markers, and open the finished draft in Chrome.
2. **Do NOT send anything.** Present the complete draft to Max with a TLDR: the table speaks for itself (all five genomes at ~4M variants / ~1.5% novel - universal human, no novel architecture).
3. If X11 hasn't replied yet, either wait for the self-wake or re-check the board. If X11 is stuck, run the control counts yourself on asto (bcftools is inside the distrobox container; `zcat | awk` on the host works for raw counts, but dbSNP annotation needs the distrobox pipeline).
4. Once the chromatin letter is approved and sent, the **next queued claims** from the question catalog: mtDNA, NUMTs, KHD3CL gene, 3rd-X multiallelic site, mosaicism/blood-type ABO, TTR chr18, ARHGAP11B. Scoreboard file tracks priority.

---

## OPEN QUESTIONS

| Question | Status |
|---|---|
| X11's control numbers for email 12 | PENDING - task dispatched, self-wake armed |
| Per-chromosome UPD/ROH scan (commissioned earlier) | May still be pending from X8A/X1D; not currently blocking anything |
| Kristen's reply to emails 09/10/11 | Not received yet as of last check - she started a new "chromatin" thread instead |
| Should x15b review email 12 before Max sees it? | Max said "don't bother" for the last Opus version of 08; unclear if this applies generally now |

---

## KEY PATHS / IDS

| What | Path/Value |
|---|---|
| Current active letter draft | `C:\claude_base\projects\XG1\kenefick\letters\kristen_email_12_novel_architecture_v01_DRAFT.md` |
| All drafts directory | `C:\claude_base\projects\XG1\kenefick\letters\` |
| Send scripts directory | `C:\claude_base\projects\XG1\kenefick\scripts\` |
| Question catalog | `C:\claude_base\projects\XG1\kenefick\letters\KRISTEN_QUESTION_CATALOG_tomemex.md` |
| Claims scoreboard (canonical tracker) | `C:\claude_base\projects\XG1\kenefick\letters\KRISTEN_CLAIMS_SCOREBOARD_tomemex.md` |
| Writing guide (x15b-maintained) | `C:\claude_base\projects\XG1\kenefick\letters\KRISTEN_WRITING_GUIDE_tomemex.md` |
| Control genome data on asto | `~/genomics/_analysis/kinship_5050/` (kristen.snps.vcf.gz, oliver.snps.vcf.gz, controls/{NA12718,NA18530,NA18488}.snps.vcf.gz) |
| asto SSH | `rempel@astolfodebian.tail251d88.ts.net` (key: `~/.ssh/bitwarden_ed25519`) |
| Board/room tool | `python C:/claude_base/branch_bulletin/bcast.py` |
| P1 room name | `p1` |
| Sender address | mass@tamza.com (auto-BCC to Max) |
| Kristen's email | kristentheartist@gmail.com |
| Max's dnaresonance address | dna@dnaresonance.org (personal track, not our letters) |
| Chrome launch pattern | `"/c/Program Files/Google/Chrome/Application/chrome.exe" "file:///C:/path/to/file.md"` (forward slashes) |

---

## GOTCHAS + DEAD ENDS

1. **Context was compacted at least once.** On resume, re-read `KRISTEN_CLAIMS_SCOREBOARD_tomemex.md` and `KRISTEN_QUESTION_CATALOG_tomemex.md` first - don't rebuild claim status from memory.

2. **The control VCF pipeline mismatch is a real, diagnosed problem.** The `kinship_5050/controls/` files were bcftools-recalled without dbSNP annotation and are incomplete (~1M records, not ~4M). A naive side-by-side count from those files would produce misleadingly low numbers and Kristen **will** notice and call it out. The controls MUST be re-run through the same pipeline. I already scouted: bcftools lives inside a distrobox container on asto, not on the host. X11 has the exact diagnostic posted to the p1 room.

3. **"Novel variant" = no-rsID in the ID column** works for Kristen/Oliver (their kinship VCFs are dbSNP-annotated) but NOT for the raw controls. The pipeline fix is necessary for Table B to be honest.

4. **Kristen hasn't replied to any of the four sent letters** (emails 08-11). She opened a new "chromatin" claim on her personal thread with Max instead. This is a pattern - she may not engage with refutations directly; she just moves to the next claim. Don't expect acknowledgment.

5. **The "three independent views" framing** Max caught as pretense in email 08. Don't pad one analysis into fake multiple views - it's one genotype comparison, two things you read off it.

6. **Never state a bare count without a denominator.** The 405,465 paternal-allele count got called "idiotic" twice by Max until the whole-chromosome 50-50 was made the real proof. Counts need context or they're meaningless.

7. **"Gene" vs "position"** - Kristen's data is SNP-level single-nucleotide positions, not whole genes. Don't say "copy of a gene" when you mean "DNA letter at a position." Max caught this once; it'll get caught again.

8. **"100.0000% / zero violations" statistics are a credibility trap.** Max personally discovered the fake 100.00% in email 08's first draft was circular (pre-filtered data). Always show the honest natural noise floor.

9. **The 52:48 paternal/maternal ratio** was cut because it's a technical artifact of the union-VCF method (not biological) and even X1D refused to quote it as clean. If a number makes *you* suspicious, it'll make Kristen suspicious. Drop it.

10. **Never promise future work.** "More will follow as I work through them" was caught and cut by Max. We can stop whenever we get bored; no commitments.

11. **Standing plan-only mode remains in effect.** Every Kristen letter requires Max's explicit named approval before sending. The board/room knows this.

12. **The microchimerism finding stands** as real and small (~0.3%, ordinary fetal microchimerism found in ~half of women who've carried sons). Do not lump it with resolved-as-artifact claims. It was email 02 and Max is personally satisfied with it.

13. **Medical matters are not our scope.** The project goal is finding traces of alien genetic manipulation, not clinical diagnosis. The disclaimer now states this explicitly.
