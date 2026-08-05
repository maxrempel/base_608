# Scribe handover - milestone 5 (~376K tokens)
# session: 20260714_claude_base_92fbfc9d
# cwd: C:\claude_base
# written: 2026-07-14 08:31:18 by deepseek-v4-pro

# HANDOVER - Bowater 23andMe Trio Download + NPA Analysis

---

## GOAL (Max's words)

Download the Bowater family 23andMe raw data (child Lottie, mother Julie, father Roger). Then run the full non-parental allele (NPA) analysis on the trio and fit it into the existing ~7-family study so results are comparable. Draft a letter to Lottie with findings. The larger context: searching for traces of alien genetic manipulation - not medical diagnosis.

---

## DECISIONS + WHY

1. **Bitwarden 2FA via CLI, not browser extension.** The browser launched without a logged-in Bitwarden because only one session can hold the shared Bitwarden profile at a time (there's a lock). A config edit was attempted and reverted - it wasn't the cause. The real fix: pull 2FA codes from the command line with `bw get totp <item-id>`. This works regardless of browser profile contention and is now documented in the shared logins file. Max accepted CLI workaround; no profile-pool built.

2. **Re-implemented the lost NPA scanner.** The original `L473v1_...NPA_Scanner` script from January was ephemeral (never committed). The method was reconstructed from the output files in the old analysis folder. The new scanner produces identical-formatted output with three categories: DOCHAN (both child alleles non-parental - strongest), HETEROPOP (het child, one non-parental allele), HOMOPOP (homozygous child, parents lack copies). Same logic, same output TSV columns.

3. **23andMe data replaces MyHeritage for Bowater.** The old MyHeritage Bowater run (994 NPAs) was ~96% platform noise - low coverage caused false non-parental calls. The 23andMe re-test is the canonical data. The old MyHeritage Bowater folder still exists for reference.

4. **50kb proximity window for cross-family NPA clustering** - chosen by Max. NPAs from different families within 50kb of each other would count as a shared hotspot.

5. **Genes left OUT of Lottie's letter per Max's steer.** The gene connections (MAF?autism, CTNNA3?autism, CAPN14?EDS) were researched and verified but Max chose to present a sober, honest message without naming genes. The letter leads with MyHeritage noise explanation, the 23andMe limitation (only reads known human markers), and the WGS next step.

6. **Canonical folder survived disk cleaning.** Max said files may have been lost to disk cleaning; the canonical folder lives on Nextcloud and was intact.
   
---

## CURRENT STATE

**Downloads - COMPLETE:**
- All three Bowater 23andMe raw genotype files are in the canonical folder:
  `C:\Users\maxre\Nextcloud\xg1_data\xg1_fams\20260614_bowater_trio_23andme\`
  - Lottie: `genome_Lottie_Bowater_v5_Full_20260614135707.zip` (from June)
  - Roger (father): `genome_Roger_BowaterLottiesFatherupdated_v5_Full_20260614135900.zip` (downloaded Jul 10)
  - Julie (mother): downloaded later when ready email came, verified 17MB genotype
  - `README_status_tomemex.md` - status doc in the folder

**NPA Analysis - COMPLETE:**
- Scanner: `C:\claude_base\projects\XG1\xp2_npa\npa_scanner_bowater23_v01.py`
- Results: `C:\Users\maxre\Nextcloud\xg1_data\xp2_analysis\260713_NPA_Bowater_23andme_trio\npa_results_bowater_23andme\`
  - `bowater23_npa_dochan.txt` - 0 DOCHAN
  - `bowater23_npa_heteropop.txt` - 7 HETEROPOP
  - `bowater23_npa_homopop.txt` - 31 HOMOPOP
  - **Total: 38 NPAs, 0.0063% of ~601,900 tested positions, 99.994% Mendelian**
- Full report: `REPORT_bowater_23andme_NPA_v01_tomemex.md` in the analysis folder

**Cross-family sharing - COMPLETE:**
- Script: `C:\claude_base\projects\XG1\xp2_npa\npa_cross_family_v01.py`
- Result: Zero genuine cross-family NPA sharing among clean 23andMe families
- 79 of 80 shared positions are MyHeritage-only artifacts
- One position (chr2:31,454,665) shows NPA in Lottie on BOTH platforms (23andMe + MyHeritage) - same person, two chips agree

**Proximity/Cluster analysis (50kb window) - COMPLETE:**
- Scripts: `npa_proximity_clusters_v01.py` + `npa_proximity_permutation_v01.py`
- Permutation test: Bowater cross-family proximity is chance (p=0.46, observed 6 near vs expected 5.4)
- Three loci show Lottie same-person cross-platform agreement within 50kb:
  - chr2:31.45Mb ? CAPN14
  - chr16:79.6Mb ? MAF  
  - chr20:59.6Mb ? gene desert
- One NPA cluster in clean data: chr10:68.08Mb, 3 NPAs in 9kb ? CTNNA3
- All committed and pushed to master

**Gene-connection research - DONE:**
- Lottie's full profile read: autistic, Ehlers-Danlos (hypermobility), fibromyalgia, narcolepsy, PoTS, immunocompromised. Father Roger autistic, whole maternal side autistic.
- MAF ? autism (Aym?-Gripp syndrome features include ASD, intellectual disability)
- CTNNA3 ? autism (GWAS + CNV studies link loss to ASD)
- CAPN14 ? eosinophilic esophagitis, 8-fold association with hypermobile EDS
- Sources verified: NCBI GeneReviews, J Neurodev Disord, JACI

**Email to Lottie - DRAFTED, NOT SENT:**
- First email (data-downloaded confirmation) was sent from Anna, CC'd Max
- Results letter is drafted but **HAS NOT BEEN SENT**
- Max caught a false statement: Claude wrote "most of it is likely the last of the residual noise" - this was editorializing with no evidence. Max challenged it.
- **The truth:** 38 NPAs is on the HIGH side (double the cleanest family), not reassuringly low. No evidence it's noise; array data cannot distinguish real from artifact.
- Revised paragraph proposed, letter still awaiting Max's final approval
- Disclaimer about alien-genetics research (not medical diagnosis) added per Max's request
- Gene names left out per Max's steer

**Infrastructure:**
- 2FA for 23andMe: Bitwarden item `7772765a-6e05-44ab-9955-b3fa0142a736` ("UK bowater lottie 23andme.com"), user max@tamza.com
- CLI 2FA method documented in `C:\Users\maxre\Nextcloud\zSyncMain\ssh\shared_logins_frequent.txt`
- Bitwarden session token lives at `C:/Users/maxre/Nextcloud/zSyncMain/ssh/bw_session.txt`
- Telegram bot: @MMMMonitorMaxBot, chat id 1395850773
- Bowater reminder task was DELETED (trio complete)
- Browser lock: released, no Playwright instance held

**Collaboration:**
- This session is X31B (auto-renamed to X31Bb/X31Bbb due to duplicate check-in collisions - id drift fixed with `whoami x31b`)
- Room P5 created for collaboration with x32 branch
- Room P2 has ~600-trio WGS NPA data (different platform, rates not directly comparable to array)
- P2 was asked for per-trio NPA count for the Lottie letter but hasn't replied yet

---

## EXACT NEXT STEP

1. **Max must approve the final Lottie letter.** The current draft is held - it needs the noise-claim sentence replaced with the honest version ("38 is on the higher side, we cannot tell if technical or real, that's why WGS is next"). Once Max says "send," fire it from Anna to depresstival@gmail.com (reply-to + CC Max).

2. **Optional: gene-set enrichment test.** Was discussed but not yet run - are Lottie's 38 candidates enriched in autism/connective-tissue genes above random expectation? This would test whether the gene convergence (MAF, CTNNA3, CAPN14 landing in her actual conditions) is real or chance. Max didn't explicitly greenlight this.

3. **Wait for the WGS funding step** - Max mentioned $379/person + ~$100 shipping, possibly checking UK pricing. No immediate action needed.

---

## OPEN QUESTIONS AWAITING MAX

1. **Send the letter?** As-is with the corrected noise paragraph? Or further edits?
2. **Add gene connections?** Max kept them out; does he want them in after all?
3. **Run the enrichment test?** To quantify whether the convergence on autism/EDS genes is above chance.
4. **P2's per-trio NPA number?** Still waiting for that data for the "how unusual is 38" estimate.

---

## KEY PATHS + IDs

| What | Path/ID |
|---|---|
| Bowater 23andMe files | `C:\Users\maxre\Nextcloud\xg1_data\xg1_fams\20260614_bowater_trio_23andme\` |
| NPA results (new) | `C:\Users\maxre\Nextcloud\xg1_data\xp2_analysis\260713_NPA_Bowater_23andme_trio\` |
| Old 7-family analysis | `C:\Users\maxre\Nextcloud\xg1_data\xp2_analysis\260124_NPA_7fam_11children\` |
| NPA scanner script | `C:\claude_base\projects\XG1\xp2_npa\npa_scanner_bowater23_v01.py` |
| Cross-family script | `C:\claude_base\projects\XG1\xp2_npa\npa_cross_family_v01.py` |
| Proximity script | `C:\claude_base\projects\XG1\xp2_npa\npa_proximity_clusters_v01.py` |
| Permutation script | `C:\claude_base\projects\XG1\xp2_npa\npa_proximity_permutation_v01.py` |
| Report | `260713_NPA_Bowater_23andme_trio\REPORT_bowater_23andme_NPA_v01_tomemex.md` |
| Bitwarden 23andMe TOTP item | `7772765a-6e05-44ab-9955-b3fa0142a736` |
| Bitwarden session token | `C:/Users/maxre/Nextcloud/zSyncMain/ssh/bw_session.txt` |
| Shared logins file | `C:\Users\maxre\Nextcloud\zSyncMain\ssh\shared_logins_frequent.txt` |
| 23andMe account | max@tamza.com |
| Lottie email | depresstival@gmail.com |
| Telegram bot | @MMMMonitorMaxBot, chat 1395850773 |
| Mxmail sender | `C:\claude_base\tools\mxmail\mxmail_v01.py` |
| Room P5 | x31b + x32 collaboration |
| Room P2 | ~600-trio WGS NPA data |
| Lottie's profile | Notion "Experience Profile v2" + XG1 database record |
| Lottie's conditions | autistic, EDS hypermobility, fibromyalgia, narcolepsy, PoTS, immunocompromised |

---

## GOTCHAS

1. **The NPA scanner is a re-implementation, not the original.** The original Jan script was lost. The new one faithfully reproduces the logic and output format (verified against old results), but it's not byte-identical. Any future comparison work should note this.

2. **"Residual noise" claim was false - Max caught it.** The 38 NPAs are on the **high** side (~2? the cleanest family), not reassuringly low. There's zero evidence they're noise vs. real. Array data genuinely cannot distinguish. Do not editorialize about "likely noise" in any output.

3. **MyHeritage Bowater data is NOT usable for fine NPA work.** The 994 NPAs were ~96% low-coverage artifacts. Only the 23andMe data is valid. The old MyHeritage folder should not be accidentally re-analyzed.

4. **Bitwarden browser profile contention is NOT fixed.** The root cause (single shared logged-in profile) remains. The CLI workaround works for 2FA codes but not for browser autofill. If a session needs actual Bitwarden browser interaction, it may fail silently if another session holds the profile.

5. **Session ID drift.** x31b auto-renamed to x31Bb/x31Bbb due to duplicate check-ins. The worktree's identity was re-claimed with `bcast.py whoami x31b`. The science files are safe; the id confusion is cosmetic. x32 is the new collaborating branch working in room P5.

6. **P2's 600-trio data is WGS, not array.** NPA rates from P2 are NOT directly comparable to Bowater's array results. Any "how unusual is 38" estimate must account for platform differences.

7. **The letter has NOT been sent.** Max was mid-review when he challenged the noise claim. The revised version awaits his approval. Do not send without explicit
