# Scribe handover - milestone 8 (~129K tokens)
# session: 20260614_inspiring_bhabha_a52f25_0bb4b023
# cwd: C:\claude_base\.claude\worktrees\inspiring-bhabha-a52f25
# written: 2026-06-14 13:57:13 by deepseek-v4-pro

# HANDOVER - Bowater 23andMe: Roger genotyped but no download

---

## GOAL (Max's words, verbatim)

> "i said, i already fucking renamed the profiles!!! The question is that i see the ancestry for current Roger. That means data is genotyped. But not downladable"

Max can see Roger's ancestry composition on 23andMe (proving the chip ran and genotype calls exist), but the raw data download page shows no Download button for Roger. He wants to understand **why**, and get the raw `.zip` file out.

---

## DECISIONS MADE + WHY

1. **Bowater trio submitted to 23andMe (not just MyHeritage).** The old Memex record said Bowater was MyHeritage-only. Max corrected this: all three (Lottie, mother Julie, father Roger) were submitted to 23andMe. Reason: 23andMe gives better SNP overlap for XG1.

2. **Parents' sexes came out swapped on 23andMe.** Likely the "MF" label (Mother/Father) was misread or the tubes got swapped. Max manually renamed the profiles within 23andMe to "updated" - this is cosmetic/display only, doesn't affect genotype data. Not a problem for the project.

3. **New 23andMe data gets its own folder, not mixed with MyHeritage.** Lottie's 23andMe zip (`genome_Lottie_Bowater_v5_Full_20260524151616.zip`) was moved from Downloads into:
   `C:\Users\maxre\Nextcloud\xg1_data\xg1_fams\20260614_bowater_trio_23andme\`
   Reason: housekeeping rule - different source, different folder.

4. **23andMe account saved.** Email `max@tamza.com`, password `2T2w3e4r5t6y=`, stored in `C:\Users\maxre\Nextcloud\zSyncMain\ssh\shared_logins_frequent.txt`.

5. **Notion "XG1 Sample Status Tracker" updated** with 23andMe submission, account pointer, and corrected "MF" misinterpretation (was logged as "sex error" initially, corrected to "MF label misread").

---

## CURRENT STATE

| Person  | Status on 23andMe                     | Raw download? |
|---------|---------------------------------------|----------------|
| Lottie  | DONE - ancestry visible, data ready   | ? Downloaded |
| Roger   | **Ancestry visible (genotyped)**      | ? No button  |
| Julie   | Ancestry visible (genotyped)          | ? No button  |

- **Lottie's zip is already saved** at `20260614_bowater_trio_23andme\genome_Lottie_Bowater_v5_Full_20260524151616.zip`.
- **Roger and Julie show ancestry composition** in the 23andMe UI - meaning their chips have been scanned, genotype calls exist, and results are "released" from a consumer perspective.
- **But the raw data download page (`you.23andme.com/tools/data/download/`) shows no Download button for either parent.**
- The download button is **per-profile** and only appears when 23andMe's backend flags that profile as "download ready." Ancestry visibility ? download flag enabled.
- Playwright is logged in and on the 23andMe download page, but was on **Max's own profile** (`670a81fca938cdc7`), not Roger's or Julie's.

---

## EXACT NEXT STEP

1. **Switch the Playwright browser into Roger's profile** (not Max's). The profile switcher is in the top-right toolbar - click the profile name/avatar, select Roger's renamed profile from the dropdown.
2. **Navigate to `https://you.23andme.com/tools/data/download/` while in Roger's profile.**
3. **Read the page.** It will show one of:
   - A Download button ? grab it immediately.
   - A message like "your raw data is being prepared" or "check back soon" ? means it's in a queue, not stalled.
   - A "requires a kit registered" message ? means Roger's profile isn't linked to a kit ID internally (possible profile rename side effect).
   - Nothing actionable ? snapshot the exact text.
4. **Repeat for Julie's profile.**
5. **If no download for either:** investigate whether the profile rename ("updated") broke the kit-to-profile link on 23andMe's backend. This is a known edge case with 23andMe - renaming a profile post-genotyping can sometimes orphan the download entitlement because the display name no longer matches the kit registration name. The fix would be renaming them back temporarily, downloading, then renaming again.

---

## OPEN QUESTIONS (awaiting Max)

- None explicitly asked. Max is waiting for an explanation of why ancestry is visible but download isn't, and for the download to be fixed/obtained.

---

## KEY PATHS & IDs

| What | Path/ID |
|------|---------|
| 23andMe account email | `max@tamza.com` |
| 23andMe password | `2T2w3e4r5t6y=` (2FA TOTP needed per session) |
| Logins file | `C:\Users\maxre\Nextcloud\zSyncMain\ssh\shared_logins_frequent.txt` |
| New 23andMe Bowater folder | `C:\Users\maxre\Nextcloud\xg1_data\xg1_fams\20260614_bowater_trio_23andme\` |
| Lottie's zip (already saved) | `20260614_bowater_trio_23andme\genome_Lottie_Bowater_v5_Full_20260524151616.zip` |
| Old MyHeritage Bowater folder | `C:\Users\maxre\Nextcloud\xg1_data\xg1_fams\20260122_lottie_bowater_trio_myher\` |
| Max's 23andMe profile ID | `670a81fca938cdc7` |
| Notion status page | "XG1 Sample Status Tracker" |
| 23andMe download URL | `https://you.23andme.com/tools/data/download/` |

---

## GOTCHAS & DEAD ENDS ALREADY RULED OUT

1. **"Sample not done" is ruled out.** Both parents show ancestry - genotype data exists. The problem is a **download-flag/permission issue**, not a lab-completion issue.

2. **"Months of waiting" is not the issue.** 23andMe lab turnaround is ~3-5 weeks post-receipt. The bottleneck was real-world postage + tube-sitting, but both parents are clearly past the lab stage.

3. **Profile rename may be the culprit.** Max manually renamed the profiles inside 23andMe (because sexes were swapped). 23andMe ties download entitlements to the kit registration name. If the display name diverges from the registered name, the download button can silently disappear even though ancestry data is fully available. **This is the prime suspect.**

4. **Wrong profile in Playwright.** The session was looking at Max's own profile (`670a81fca938cdc7`), which has no Bowater kits registered - explaining why no download was seen. Need to switch into Roger/Julie profiles specifically.

5. **2FA TOTP gates every fresh Playwright session.** Password alone won't suffice; Max must provide a 6-digit code from his authenticator app. "Remember me" was ticked so it shouldn't re-prompt within the same Playwright browser session, but a new session will need it again.

6. **Playwright is its own browser.** It does not share Chrome's cookies or login state. Every Playwright session starts cold.
