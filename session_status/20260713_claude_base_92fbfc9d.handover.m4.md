# Scribe handover - milestone 4 (~302K tokens)
# session: 20260713_claude_base_92fbfc9d
# cwd: C:\claude_base
# written: 2026-07-13 16:09:08 by deepseek-v4-pro

# HANDOVER - X31B (NPA cross-family + Bowater trio analysis, P5 collaboration)

---

## GOAL (Max's words, from the session)

- Download the 23andMe raw data for the **Bowater trio** (Lottie Bowater, mother Julie, father Roger) - the "best family" because child + both parents are available.
- Run the same **non-parental allele (NPA) analysis** as the earlier 7-family study (the `260124_NPA_7fam_11children` analysis), fitting the Bowater 23andMe data into that framework so it's directly comparable.
- Test whether **NPAs are shared across families** (exact position overlaps), and then **proximity** - whether NPA positions fall within 50 kb of each other across families, plus any **clusters**.
- Set up **room P5** for collaboration with a new branch (`x32`) that will continue the comparison work. This session remains **X31B**. All findings are posted to P5 so x32 can pick up cleanly.

---

## DECISIONS MADE + WHY

1. **Canonical folder used for raw data:**  
   The existing folder was `Nextcloud\xg1_data\xg1_fams\20260614_bowater_trio_23andme\` (already contained Lottie's June file). A previous disk-cleaning wipe ("swiped" not "swapped") did **not** destroy it because the folder lives on Nextcloud. Roger's and Julie's files were saved into this exact folder, and a stray duplicate was deleted. *Reason: Max demanded the files go to the proper place, not a new stray folder.*

2. **23andMe login via Bitwarden CLI (not browser extension):**  
   The Playwright browser launched without a logged-in Bitwarden extension because only one session can hold the shared Bitwarden profile at a time. Instead of fighting profile contention, the 2FA code was pulled directly from the command line (`bw get totp`). This method was documented in the shared logins file (`shared_logins_frequent.txt`) so **all future sessions will use the CLI for 2FA** - no more getting stuck. Max explicitly accepted "CLI workaround is fine." *Reason: avoids browser profile lock contention and user interaction.*

3. **NPA scanner re-implemented faithfully:**  
   The original scanner script (`L473v1_...NPA_Scanner.py`) from the January analysis was **not found on disk** (lost in an ephemeral session). The classification logic (DOCHAN, HETEROPOP, HOMOPOP, Mendelian) and output format were completely reconstructed from the saved output files. The reimplementation was verified by comparing against the old MyHeritage Bowater run and cross-checking example positions. *Reason: must produce exactly comparable results.*

4. **Cross-family overlap test refined:**  
   The initial script mistakenly labeled the new Bowater-23andMe child as just "bowater" (colliding with the old MyHeritage Bowater). Fixed by mapping family names with platform suffixes (`bowater_23andme` vs `bowater_myheritage`). *Reason: correct identification of which data belongs to which platform.*

5. **Proximity window = 50 kb (as Max specified: "5-0 kilobases"):**  
   Tested whether any two families' NPAs fall within 50 kb of each other. Separated clean 23andMe families from noisy MyHeritage families. *Reason: Max's explicit distance threshold for counting a proximity hit.*

6. **Permutation test on proximity results:**  
   To answer "is this beyond chance?", Bowater's 38 NPA positions were repeatedly sampled from the background of all chip positions and tested for proximity to other families' NPAs. Observed 6 near, expected 5.4, p = 0.46. *Reason: rigor - don't mistake random coincidences for signal.*

7. **Room P5 created for x32 collaboration:**  
   X31B created room P5 and has posted status updates, results, and open tasks there. The new branch `x32` (or `x32d`) will pick up work from P5. X31B stays. *Reason: Max wants parallel work without collisions.*

---

## CURRENT STATE

### Raw data (all three files secured)
All files in canonical folder:  
`C:/Users/maxre/Nextcloud/xg1_data/xg1_fams/20260614_bowater_trio_23andme/`

- `genome_Lottie_Bowater...v5_Full_...zip` - already there since mid-June.
- `genome_Roger_BowaterLottiesFatherupdated_v5_Full_20260614135900.zip` - downloaded Jul 10, verified (17 MB uncompressed).
- `genome_Julie_BowaterLottiesMother_v5_Full_202607...zip` - downloaded later (Jul 13), verified (17 MB uncompressed).
- `README_status_tomemex.md` - status doc, updated to show all three obtained.

### 23andMe download status
- All three requests submitted and files obtained. No pending downloads. The Telegram reminder (`Bowater_Reminder` scheduled task) was **deleted** after Julie's file arrived.

### Email to Lottie
Sent via `mxmail` from Anna (mass@tamza.com, CC'd Max) to depresstival@gmail.com. Mail informed her all three files are in and analysis can proceed. No action needed from her.

### NPA analysis output
Analysis folder:  
`C:/Users/maxre/Nextcloud/xg1_data/xp2_analysis/260713_NPA_Bowater_23andme_trio/`

Contents:
- `npa_results_bowater_23andme/bowater23_npa_DOCHAN.tsv` - empty (0 DOCHAN)
- `npa_results_bowater_23andme/bowater23_npa_HETEROPOP.tsv` - 7 HETEROPOP positions
- `npa_results_bowater_23andme/bowater23_npa_HOMOPOP.tsv` - 31 HOMOPOP positions
- `01_master_npa_summary_updated.tsv` - all 12 children across 8 families, including the new Bowater 23andMe row
- `REPORT_bowater_23andme_NPA_v01_tomemex.md` - full report
- `proximity/` - proximity/cluster results (CSV)

Total: **38 NPAs** (0.0063% non-parental of 601,900 positions). Trio is 99.994% Mendelian. QC confirmed correct family labels (sex checks passed).

### Cross-family position-exact overlap test (answer to "share the NPAs")
- Bowater 23andMe's 38 NPAs share **zero** exact positions with any other family.
- Across all families, 80 positions are shared by 2+ families, but **79 are MyHeritage-only** (platform artifact hotspots). The one exception is Lottie herself at chr2:31,454,665 - flagged non-parental on **both** 23andMe and MyHeritage. That's a same-person cross-platform hit, not a cross-family hit.

### Proximity (50 kb) test
- Among only the clean 23andMe families: **0** hotspots where two different families have NPAs within 50 kb.
- The few cross-family proximities involving Bowater are with MyHeritage families (dense artifact background).
- Permutation test: observed 6/38 Bowater NPAs within 50 kb of any other family; expected 5.4; **p = 0.46** ? not significant.

### Within-person cross-platform loci (same person, two platforms)
These 3 loci have Lottie's 23andMe and MyHeritage NPAs within 50 kb of each other:
- chr2:31.45 Mb
- chr16:79.6 Mb
- chr20:59.6 Mb

These are the prime candidates for real non-parental alleles (two independent platforms agree), warranting gene annotation and eventual WGS confirmation.

### Clusters
One cluster in the clean 23andMe data: **chr10:68.08 Mb** - 3 NPAs within 9 kb. Possible small parental deletion or local array artifact.

### Scripts (committed + pushed, master)
- `C:\claude_base\projects\XG1\xp2_npa\npa_scanner_bowater23_v01.py` - re-implemented NPA scanner (trio mode, classifies DOCHAN/HETEROPOP/HOMOPOP)
- `C:\claude_base\projects\XG1\xp2_npa\npa_cross_family_v01.py` - cross-family exact-position overlap test
- `C:\claude_base\projects\XG1\xp2_npa\npa_proximity_clusters_v01.py` - proximity (50 kb) and cluster detection
- `C:\claude_base\projects\XG1\xp2_npa\npa_proximity_permutation_v01.py` - permutation test on proximity

### Misc infrastructure
- `C:\claude_base\tools\bowater_reminder\bowater_reminder.py` - Telegram reminder script (scheduled task deleted, script remains)
- `C:\Users\maxre\Nextcloud\zSyncMain\ssh\shared_logins_frequent.txt` - updated with 23andMe 2FA CLI method

---

## EXACT NEXT STEP

**Gene-annotate the 3 within-person cross-platform loci and the chr10 cluster.**  
Specifically:
- chr2:31.45 Mb (?50 kb): what genes?
- chr16:79.6 Mb (?50 kb): what genes?
- chr20:59.6 Mb (?50 kb): what genes?
- chr10:68.08 Mb (?10 kb): what genes?

This task was flagged in P5 as ready for either X31B or x32. The clone (x32) has not yet been created/entered the room - X31B can grab it, or wait for x32.

---

## OPEN QUESTIONS (awaiting Max)

- Does Max want **X31B to do the gene annotation now**, or will **x32 take it** from P5?
- When is the follow-up on the 30x whole-genome sequencing for the Bowater trio? (This was flagged in the report as the real next level - array can't resolve below the 38 candidates.)
- Should the 3 cross-platform loci be validated on a different platform before WGS, or is the dual-platform agreement (23andMe + MyHeritage) sufficient to prioritize them?

---

## KEY PATHS, IDs, NAMES

| What | Path/ID |
|---|---|
| **Raw data folder** | `C:/Users/maxre/Nextcloud/xg1_data/xg1_fams/20260614_bowater_trio_23andme/` |
| **NPA analysis output** | `C:/Users/maxre/Nextcloud/xg1_data/xp2_analysis/260713_NPA_Bowater_23andme_trio/` |
| **Earlier 7-family analysis (reference)** | `C:/Users/maxre/Nextcloud/xg1_data/xp2_analysis/260124_NPA_7fam_11children/` |
| **NPA scripts** | `C:\claude_base\projects\XG1\xp2_npa\` |
| **Bitwarden vault session** | `C:/Users/maxre/Nextcloud/zSyncMain/ssh/bw_session.txt` |
| **23andMe Bitwarden item** | UUID `7772765a-6e05-44ab-9955-b3fa0142a736`, username `max@tamza.com` |
| **23andMe account** | `max@tamza.com`, profiles: Max (no kit), Lottie, Julie, Roger |
| **Lottie's email** | `depresstival@gmail.com` |
| **Anna's sending address** | `mass@tamza.com` |
| **mxmail tool** | `C:\claude_base\tools\mxmail\mxmail_v01.py` |
| **Branch bulletin (room P5)** | `C:\claude_base\branch_bulletin\bcast.py`, command: `python bcast.py room p5 "message"` |
| **Worklog** | `C:\claude_base\compaction_kb\scripts\worklog.py` |

---

## GOTCHAS / DEAD ENDS RULED OUT

- **Disk-cleaning "swipe":** Max thought the canonical Bowater folder was lost. It was not - it lived on Nextcloud and was fully intact. Verified before downloading Julie's file.
- **Original NPA scanner lost:** The `L473v1_...NPA_Scanner.py` script from January no longer exists on disk. Attempted glob and grep; not found. Reimplemented from the output files, matching format exactly. The reimplementation is sound (verified by matching example positions from old runs).
- **Family name collision in cross-family test:** The original script labeled Bowater-23andMe and Bowater-MyHeritage both just "bowater", causing spurious hits. Fixed by appending platform suffix.
- **Bitwarden browser extension missing:** The Playwright session launched without a logged-in Bitwarden because another session already held the shared profile. This is expected behavior with single-profile lock. It is **not** a bug that needs fixing. The permanent workaround is CLI 2FA (`bw get totp`).
- **Unnecessary config edit reverted:** An early attempt to edit `.claude.json` to point to the Bitwarden launcher was later reverted when it became clear it wouldn't help - the global config already had the correct launcher, and the real issue was profile contention.
- **Stray download folder deleted:** A temporary folder `C:\claude_base\projects\XG1\bowater\raw_23andme_20260710` was created in error, then merged into the canonical folder and deleted.
- **Playwright lock:** The browser was properly closed after each download session. No dangling locks.
