# Scribe handover - milestone 2 (~207K tokens)
# session: 20260713_claude_base_92fbfc9d
# cwd: C:\claude_base
# written: 2026-07-13 12:25:50 by deepseek-v4-pro

# Handover: Bowater 23andMe DNA Data Downloads

## GOAL (in Max's words)
Download the 23andMe raw DNA data for the Bowater family: mother (Julie), father (Roger), and child (Lottie). All three profiles live under the single account `max@tamza.com`. The data should end up in the existing canonical folder, and when the pending requests complete, a recurring Telegram reminder will keep the work on track.

## DECISIONS + WHY
1. **2FA handled via Bitwarden CLI, not browser extension.**  
   The Playwright browser with Bitwarden extension is contending with other sessions for a single logged?in profile. Rather than fight that lock every time, I pulled the 6?digit TOTP straight from your vault using `bw get totp` (vault already unlocked, session token from `bw_session.txt`). That way no restart, no waiting on you - it just works. I documented this method in the 23andMe entry inside `shared_logins_frequent.txt` so any future session can replicate it instantly.

2. **Three different download states ? three different actions.**  
   - **Roger** had a ready?to?download file **today**. I extracted the pre?signed S3 URL from the browser and saved the zip.  
   - **Lottie** and **Julie** both needed to *request* the data (check a risk box and submit). That triggers a processing delay (a few days). 23andMe then emails a "ready" link. So for them: request submitted, waiting for the email.

3. **Canonical folder found and honoured.**  
   A stray download folder I created was discarded. The real location is `C:\Users\maxre\Nextcloud\xg1_data\xg1_fams\20260614_bowater_trio_23andme\` - it already contained Lottie's June file. Roger's freshly downloaded zip was moved into that same folder, keeping the trio together. A `README_status_tomemex.md` in that folder records the current state and the exact download steps for when the remaining files arrive.

4. **Recurring Telegram reminders to keep the ball rolling.**  
   A Python script (`bowater_reminder.py`) sends a Telegram message to `@MMMMonitorMaxBot`. A Windows Scheduled Task on **Pine** triggers it every 2 days starting **July 13, 9am**, with catch?up if the machine was off. The message tells you to check Gmail for the 23andMe "ready" emails. The task runs until you ask me to delete it.

## CURRENT STATE
- **Roger (father):** ? **Downloaded and verified** - `genome_Roger_BowaterLottiesFatherupdated_v5_Full_20260614135900.zip` (5.9?MB compressed, 17?MB extracted genotype file). Sitting in the canonical folder.
- **Lottie (child):** ?? **Old file present, new request pending.** The June file `genome_Lottie_Bowater_v5_Full_20260614135639.zip` is already in the folder. Today's request (submitted) may produce an updated copy; the email could be for an identical file or a newer export. When the "ready" email arrives, download the fresh version and overwrite or add it.
- **Julie (mother):** ? **Request submitted, waiting.** No file yet. The 23andMe "ready" email is expected within a few days. When it arrives, download her data into the canonical folder.
- **Status file** exists: `README_status_tomemex.md` in the canonical folder describes the three family members, what's done, and how to pull the remaining files.
- **Telegram reminder** active: Scheduled task `Bowater_Reminder` on Pine; first ping July?13, then every 2 days. Test message already sent (you should have seen one).

## EXACT NEXT STEP (when the 23andMe "ready" email arrives)
1. Check Gmail for the email(s) from 23andMe (subject likely includes "Raw Data Download", "Your data is ready").  
2. Open `README_status_tomemex.md` in the canonical folder for step?by?step browser commands. The short version:  
   - Log in to `you.23andme.com` as `max@tamza.com`. The password is in Bitwarden (item "UK bowater lottie 23andme.com").  
   - For the 2FA code, run:  
     `bw get totp 7772765a-6e05-44ab-9955-b3fa0142a736 --session $(cat "C:\Users\maxre\Nextcloud\zSyncMain\ssh\bw_session.txt" \| tr -d '\r\n')`  
   - Switch to the relevant profile (Julie or Lottie) via the "Switch Profile" dialog.  
   - Navigate to the "Raw Data Download" page. If the file is ready, the page will show a download button.  
   - Use the Playwright browser to extract the pre?signed S3 URL from the page, then download directly with PowerShell/curl (like we did for Roger). Save into the canonical folder.  
3. After Julie's file is saved, the trio is complete; you can tell me to cancel the `Bowater_Reminder` task.

## OPEN QUESTIONS
- Is the existing Lottie file (June) still current, or should the freshly requested one replace it? The new request may yield an identical copy or a diff-assume overwriting with the fresh download is safe.
- Julie's mother was "ready" today but only via the request flow (not an instant download). That's normal; nothing is stuck.

## KEY FILE PATHS, IDs, AND COMMANDS
- **23andMe account:** `max@tamza.com`
- **Bitwarden item:** "UK bowater lottie 23andme.com" (contains password and TOTP)
- **TOTP item UUID:** `7772765a-6e05-44ab-9955-b3fa0142a736`
- **Bitwarden session token file:** `C:\Users\maxre\Nextcloud\zSyncMain\ssh\bw_session.txt`
- **Canonical data folder:** `C:\Users\maxre\Nextcloud\xg1_data\xg1_fams\20260614_bowater_trio_23andme\`
- **Status file:** `README_status_tomemax.md` (written in that folder)
- **Reminder script:** `C:\claude_base\tools\bowater_reminder\bowater_reminder.py`
- **Reminder scheduled task:** `Bowater_Reminder` (on Pine)
- **Telegram bot:** `@MMMMonitorMaxBot` (chat id `1395850773`)

## GOTCHAS / DEAD ENDS RULED OUT
- **Do not** try to make the browser Bitwarden autofill work reliably across multiple sessions; it's a shared?profile bottleneck. Always use the CLI method for TOTP (and for password if needed). The CLI is already documented and tested today.
- **Do not** expect an immediate download button after submitting the request. The 23andMe page will say "processing" - the email is the real trigger. The file could be ready in 1-3 days.
- **Do not** leave the Playwright browser open; close it after each session to release the shared lock. (Today's session already closed the browser.)
- The pre?signed S3 download links from 23andMe expire. When you get the "ready" email, don't delay-grab the file as soon as you see the reminder.
- The stray download folder I originally made (`projects/XG1/bowater/raw_23andme_20260710`) was deleted after moving Roger's file to the canonical location. Nothing should be there now.
- The temporary config edit to `.claude.json` was reverted; the Playwright launcher path remains as before (global config already points to the Bitwarden?enabled launcher). The real cause of today's "no Bitwarden" was profile contention, not a config mispoint.
