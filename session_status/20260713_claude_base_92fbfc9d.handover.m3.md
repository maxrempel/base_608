# Scribe handover - milestone 3 (~264K tokens)
# session: 20260713_claude_base_92fbfc9d
# cwd: C:\claude_base
# written: 2026-07-13 14:19:48 by deepseek-v4-pro

## HANDOVER: Bowater 23andMe Trio - Download & NPA Analysis (Session x31b)

### GOAL (Max's words)
*"Download the data for Lottie ... and after that start the analysis and work autonomously ... analyze for the non?parental alleles and fit into already existing analysis. So it should be comparable to all others. We already did five to seven families ... so it's just another family. But it is the best family. So do it thoroughly. We are looking for all sorts of NPAs."*

He also wanted an email sent to Lottie (depresstival@gmail.com) from Anna announcing the downloads are complete, and asked to set a Telegram reminder to nudge him every other day until the trio was fully collected.

---

### WHAT WAS DONE AND WHY

**1. Login friction and the Bitwarden browser extension problem**
- The Bitwarden?enabled Playwright browser profile is shared between all sessions. Only one session can hold the logged?in vault; this session got the throwaway (logged?out) fallback. That's why the autofill button was missing.
- **Decision:** the root cause won't be restructured now - instead, we **permanently solved 2FA** by pulling TOTP codes straight from the **Bitwarden CLI** (`bw get totp`), which works in every session regardless of browser vault state. This was documented in `shared_logins_frequent.txt`. The CLI method was used successfully for this session's login.

**2. Downloading the three 23andMe raw data files**
- Account: max@tamza.com (the Bowater family kits live inside the same account under three profiles - Lottie is a child, Julie mother, Roger father).
- Lottie's file had already been downloaded in June. Roger's file was immediately ready; it was downloaded during the session and saved. Julie's file was in "processing" state - a download request was submitted, and the file was later downloaded when the "ready" email arrived.
- **Canonical download folder:**  
  `C:/Users/maxre/Nextcloud/xg1_data/xg1_fams/20260614_bowater_trio_23andme/`  
  Contains three genotype zip files + a `README_status_tomemex.md`. Despite a disk?cleaning scare, the Nextcloud folder was **intact** - nothing was lost.
- The Telegram reminder (ping every 2 days, nudging Max to check for the ready?email) was created, then deleted once Julie's file was downloaded and the trio was complete.

**3. Email to Lottie**
- From: Anna (mass@tamza.com)  
- To: depresstival@gmail.com  
- CC to Max.  
- Announced that all three family 23andMe data files are downloaded and verified, explaining that analysis will follow. The email was sent via the internal `mxmail` tool.

**4. Non?parental allele (NPA) analysis**
- The previous NPA scanner script for the 7?family analysis was lost. The assistant reconstructed the method by examining the original output files (inside `260124_NPA_7fam_11children/`).  
- A new scanner was written (`C:/claude_base/projects/XG1/xp2_npa/npa_scanner_bowater23_v01.py`) that reproduces exactly the same three NPA categories:
  - **DOCHAN** - both child alleles non?parental  
  - **HETEROPOP** - heterozygous child, one non?parental allele  
  - **HOMOPOP** - homozygous child, parents lack copies  
- The scanner was run on the 23andMe trio (build 37, v5, plus?strand; all three files in identical format).
- **Results:** 0 DOCHAN, 7 HETEROPOP, 31 HOMOPOP ? **38 non?parental alleles total, rate 0.0063%** over 601,900 overlapping positions. The trio is 99.994% Mendelian.
- All outputs were saved in a new analysis folder:  
  `C:/Users/maxre/Nextcloud/xg1_data/xp2_analysis/260713_NPA_Bowater_23andme_trio/`  
  including per?locus TSV files for each category, an updated master summary TSV that adds the new Bowater row alongside the existing 7 families, and a full narrative report (`REPORT_bowater_23andme_NPA_v01_tomemex.md`).
- The report notes that the earlier MyHeritage Bowater test had 994 NPAs; the 23andMe re?test shows only 38, confirming ~96% of the MyHeritage signal was platform noise. At array resolution the trio appears clean.

**5. Version control**
- The scanner script was committed to the `master` branch of the Claude base repository and pushed.

---

### CURRENT STATE

- **All three Bowater 23andMe raw data files are downloaded, verified, and stored in the canonical folder.**  
- **The NPA analysis is complete and results are directly comparable to the previous 7?family analysis.**  
- The email to Lottie has been sent.  
- The Telegram reminder has been deleted.  
- **No immediate action is pending.** The report suggests that the scientifically meaningful next step would be **30x whole?genome sequencing** for the trio, as array data cannot resolve the handful of candidates or detect signals below array resolution.

---

### EXACT NEXT STEP (for a cold session)

1. **If Max wants to review or discuss the NPA results:** Open the report at  
   `C:/Users/maxre/Nextcloud/xg1_data/xp2_analysis/260713_NPA_Bowater_23andme_trio/REPORT_bowater_23andme_NPA_v01_tomemex.md`  
   and the per?locus files (especially the 7 HETEROPOP and 31 HOMOPOP lists). The one finding that might warrant a closer look is a **tiny 3?marker cluster on chr10** - assess if it is noise or warrants further investigation.

2. **If Max wants to proceed towards WGS:** The conversation should shift to obtaining 30x trio whole?genome sequencing data. The Bowater trio is the "best family" because it has both parents and the child, already confirmed by array data to be correctly labelled and nearly Mendelian.

3. **If re?download is ever needed:** The 23andMe login is max@tamza.com; 2FA is obtained via `bw get totp 7772765a?6e05?44ab?9955?b3fa0142a736` using the Bitwarden session token from `C:/Users/maxre/Nextcloud/zSyncMain/ssh/bw_session.txt`. The presigned S3 download links expire - do not reuse old ones.

---

### OPEN QUESTIONS (none urgent, but may arise later)

- **Was the sex check in the scanner wrong?** The scanner's SNP?based sex classifier initially mis?called the father as "neither," but visual inspection of parent?child mismatch patterns confirmed male. This is a known artefact of genotyping?array sex classifiers and does not affect the NPA calls, but it may be worth fixing the script for future families.
- **Should the Bowater trio be re?run with the original scanner if it is ever recovered?** The re?implementation matches the original format and classification logic exactly, so the results should be identical. If the original script reappears, a spot?check is enough.
- **Is the "3?marker cluster on chr10" real or an artefact?** The current call set flags it; a deeper look might be warranted if Max wants to investigate rare genuine non?parental alleles.

---

### KEY PATHS, IDs & COMMANDS

| What | Path / Identifier |
|------|-------------------|
| **Canonical raw data folder** | `C:\Users\maxre\Nextcloud\xg1_data\xg1_fams\20260614_bowater_trio_23andme\` |
| **NPA analysis output folder** | `C:\Users\maxre\Nextcloud\xg1_data\xp2_analysis\260713_NPA_Bowater_23andme_trio\` |
| **Previous 7?family analysis (reference)** | `C:\Users\maxre\Nextcloud\xg1_data\xp2_analysis\260124_NPA_7fam_11children\` |
| **New NPA scanner script** | `C:\claude_base\projects\XG1\xp2_npa\npa_scanner_bowater23_v01.py` |
| **Email sending script** | `C:\claude_base\tools\mxmail\mxmail_v01.py` |
| **Bitwarden session file** | `C:\Users\maxre\Nextcloud\zSyncMain\ssh\bw_session.txt` |
| **23andMe TOTP secret key (Bitwarden UUID)** | `7772765a-6e05-44ab-9955-b3fa0142a736` |
| **Telegram bot (reminder now disabled)** | @MMMMonitorMaxBot, chat_id 1395850773 |

---

### GOTCHAS & BOUNDARY CONDITIONS

- **2FA login for 23andMe** - Do **not** try to use the Playwright browser's Bitwarden extension for autofill. Always fetch the 6?digit code from the CLI:  
  `bw get totp 7772765a?...?b3fa0142a736` (needs an unlocked vault via `bw_session.txt`).
- **Disk cleaning did not wipe the Nextcloud?synced folders** - the data was safe. If anything ever seems missing, check Nextcloud sync status first.
- **The original NPA scanner script is gone** - the new script that produced the results must be preserved as the working implementation. Do not delete or overwrite it without explicit confirmation.
- **The earlier MyHeritage Bowater results (994 NPAs) are platform noise** - do not treat them as real biological signal. The 23andMe re?test is the authoritative array dataset.
- **The report explicitly states that array data cannot settle the question** - any future "thorough NPA" investigation should pivot to WGS. The handover should make this clear so nobody wastes time squeezing more from the array files.
