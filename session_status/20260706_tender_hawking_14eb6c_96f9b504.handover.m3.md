# Scribe handover - milestone 3 (~227K tokens)
# session: 20260706_tender_hawking_14eb6c_96f9b504
# cwd: C:\claude_base\.claude\worktrees\tender-hawking-14eb6c
# written: 2026-07-06 16:00:46 by deepseek-v4-pro

# HANDOVER - Liz's German MSc Applications (as of Mon 2026-07-06)

## GOAL (Max's own words)
"Check out the status of Liz's applications." Later, when Dortmund emailed: "We just got an email from Dortmund. Dortmund." - Max wants the actual admission/rejection decision inside that portal.

## WHAT'S AT STAKE
Liz applied to 5 German MSc programs for Winter 2026/27. The top choice is **Hannover** (AI-driven Mechatronics & Robotics). The backup is **K?ln** (admitted, seat held). The wildcard is **Dortmund** (Automation & Robotics), which just posted a decision in its portal today - but we are locked out and can't read it.

---

## DECISIONS MADE + WHY
1. **K?ln seat = hold until Hannover decides.** Reasoning: K?ln is the only admit in hand (deadline Aug 31). Hannover is the preferred school. If Hannover says no, enroll at K?ln. If Hannover says yes, drop K?ln.
2. **Dortmund password reset via self-service.** Reasoning: Liz set the Dortmund portal password herself and it's not saved anywhere (not in the master doc, not in any file, not in Bitwarden known to us). The automated reset form works (we have her DOB: 2002-11-11, we can solve the captchas), **but the reset link in the email arrives corrupted** - token missing its `=` sign and sometimes a character.
3. **Stop fighting the corrupted reset link.** After two attempts (token `18c6be3...` burned by bad URL first try, token `Ga8133d...` immediately invalid on clean first use), Claude correctly identified this as a genuine technical transport-layer corruption, not something to brute-force. Browser was closed to release the Playwright lock.

## CURRENT STATE (as of Mon 2026-07-06, ~midday Berlin time)

| School | Status | Detail |
|---|---|---|
| **Hannover (LUH)** | ? PENDING | App #94540635, forwarded to admissions committee. Officer Bonsch said "end of June" but portal says end-July to mid-Sept. No decision posted in QIS portal (checked June 26). No new emails since May 31. |
| **TH K?ln (Gummersbach)** | ? ADMITTED | Official letter in hand. Enroll by Aug 31. Seat held as backup. |
| **TU Dortmund** | ? DECISION POSTED TODAY | Portal says status changed. Email arrived July 6 morning with "log in to see." **The admit/reject decision is invisible to us - locked out.** |
| RPTU Kaiserslautern | ? REJECTED | Incomplete (2 recommendation letters never submitted). |
| Siegen | ? REJECTED | Generic rejection. |

**No Hannover decision.** Portal (last checked June 26) shows: "Application received on time and has been processed. It is being forwarded to the admissions committee of your faculty for the decision." The portal's own timeline text says winter applicant letters go out **end of July to mid-September** - contradictory to what officer Bonsch told us ("end of June").

---

## EXACT NEXT STEP
**Get past the Dortmund portal lock to read the decision.** Three options, none yet chosen by Max:

1. **Liz clicks the reset link herself** and sets a new password (the link works in her own mail client - the corruption seems to be in the Gmail API read path or our URL construction). Then give us the password.
2. **Max OK's a Bitwarden unlock** to check if Liz saved the `myakishevrempel` Dortmund campusportal password in her vault.
3. **Max pastes the existing password** if he knows it or can get it from Liz.

Once unlocked, log into **https://www.campus.tu-dortmund.de** with username `myakishevrempel`, navigate to application status, and read whether it's an admit, reject, or document request.

After that: update `LIZ_APPLICATIONS_SYSTEM_tomemex.md` master pointer doc, update the live D1 database `application_tracker`, and report to Max for the Discord paste.

## OPEN QUESTIONS AWAITING MAX
- Which of the three unlock methods (above) does he want to pursue?
- Does he want a recurring self-wake to re-check Hannover portal every few days?
- The "today is much later" comment - Claude correctly pointed out it's still the same day. Max may be time-shifted or testing. Clarify when needed.

## KEY PATHS, IDs, CREDENTIALS

| Item | Value |
|---|---|
| Master pointer doc | `C:\Users\maxre\Nextcloud\2026 Applications as senior undergrad\LIZ_APPLICATIONS_SYSTEM_tomemex.md` |
| D1 database | `application_tracker` table (via MCP tool `d1_database_query`) |
| Hannover portal | `https://qis.verwaltung.uni-hannover.de` |
| Hannover login | Username: **94540635**, Token/PIN: **5D7F61DB** |
| Hannover applicant name shown | Samuel Myakishev-Rempel |
| Dortmund portal | `https://www.campus.tu-dortmund.de` |
| Dortmund username | **myakishevrempel** |
| Dortmund password | **UNKNOWN** - Liz set it herself, not recorded anywhere |
| Dortmund DOB | **2002-11-11** (Elizaveta Myakishev-Rempel, born Nov 11 2002) |
| Dortmund reset URL | `https://www.campus.tu-dortmund.de/passwort_setzen` |
| Email MCP tools | Two tools: `d1237438...` (search_threads/get_thread) and `4dbc6a76...` (search_gmail). Both access the Emm@ mailbox. |
| Playwright MCP | Browser automation - remember to `browser_close` to release the lock |

## GOTCHAS + DEAD ENDS ALREADY RULED OUT
1. **Dortmund reset link corruption.** The emailed reset link arrives with the `token=` parameter missing its `=`. Example: the raw email body shows `token18c6be3-c01f-4bdb-8ced-e511a` (missing the `=` after `token`). Manually inserting it and navigating doesn't work - the link is genuinely damaged in transit through the Gmail API fetch path, or the URL gets truncated. **Two tokens were burned** (first: `18c6be3...`, second: `Ga8133d...`). Do not generate a third reset without a new approach.
2. **Dortmund captcha is simple math.** First attempt: "24 plus 24" = 48. Second: "How many letters in WINED?" = 5. We can solve these.
3. **Hannover timeline conflict.** Officer Bonsch wrote "decisions by end of June" (May 30 email). The QIS portal's standard blurb says end-July to mid-September. "End of June" may have been aspirational - do not treat it as a broken promise, just a possible slip.
4. **Hannover portal navigation.** After login, click "Status Ihrer Bewerbung" ? then "Bearbeitungsstatus" to see the application processing status. The "Antr?ge" tab shows the application details.
5. **Browser lock discipline.** The MCP Playwright tool is shared/mutexed. Always `browser_close` when done with a portal session.
6. **Not a new day.** When Max said "today is much later" and "we just got an email from Dortmund," Claude correctly identified it was still the same Monday July 6, and the only recent Dortmund emails were the same-morning status-change notice plus the two password-reset emails *we ourselves generated*. The admit/reject decision is still unread.
