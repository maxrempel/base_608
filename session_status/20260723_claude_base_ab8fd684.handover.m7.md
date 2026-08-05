# Scribe handover - milestone 7 (~578K tokens)
# session: 20260723_claude_base_ab8fd684
# cwd: C:\claude_base
# written: 2026-07-23 13:14:49 by deepseek-v4-pro

# HANDOVER - Liz German Student Visa, diplo.de Application (npa_main / expatriob)

---

## GOAL (in Max's words)
Get Liz (Samuel Myakishev-Rempel) a German student visa. The preferred university order is **Hannover, then Dortmund, then TH K?ln**. Right now only TH K?ln has issued an official admission letter - it was downloaded mid-session and is a genuine, signed, unconditional Zulassungsbescheid. The application is nearly complete on the German Consular Services Portal and needs final documents + Liz's review before submission.

---

## DECISIONS MADE + WHY

**1. Visa route: National student visa (regular), Los Angeles consulate.**
- Schengen visa-free entry is not available - Liz already used ~79 of her 90 Schengen days (entered May 11, flies Paris?LA July 28). No overstay, but Plan B is dead.
- LA is the correct consulate because Liz returns to/lives in San Diego (family home). New York was only for her RIT co-op, now finished.
- Started as an applicant visa (Studienbewerbervisum) because no official admission letter existed yet. Switched to regular student visa once the TH K?ln Zulassungsbescheid was downloaded.

**2. Health insurance: TK (Techniker Krankenkasse) statutory - but NOT set up yet.**
- Compared all options: rejected MAWISTA and other cheap private plans because taking one forces an **irrevocable exemption** from public insurance for Liz's entire master's (~2 years). Not worth saving ~?110/month.
- Among public insurers (all cover the same care by law, ~?144-150/month), TK wins on English app, 24/7 English hotline, remote pre-arrival enrollment, EU EHIC card, and Expatrio integration.
- TK is portable across universities - switching from K?ln to Hannover loses nothing.
- TK student rate for Liz (23, no children): ~?146/month, first payment only due at enrollment (~October), not now.

**3. What IS needed now for the visa: a cheap incoming/bridge policy.**
- The portal's exact requirement: "If you will be insured with a statutory insurance, submit the confirmation of the statutory insurance as well as a so-called incoming insurance. This should usually be valid for three months."
- Kaiser Southern California does NOT qualify (US domestic, no German coverage, reimburse-only for emergencies abroad).
- DR-WALTER Provisit Student was chosen as the bridge - but see the GOTCHAS section below for a price discrepancy that is STILL OPEN.

**4. Outbound mail: CC vs BCC rule saved.**
- K?ln + Hannover admission-request emails went out with Max on CC by mistake (cannot unsend). Dortmund was sent correctly with BCC.
- New rule in global_AGENT_RULES.md: CC only when all recipients should see each other; BCC for keeping Max in the loop on mail to third parties.

**5. Placeholders are banned.**
- Max was clear: never leave a guessed value in a form. Blank is better. Phone, entry date, and intended city placeholders were all cleared and replaced with real values from Liz's application files or Max's explicit answers.
- Only real data now on the form. Three values flagged for Liz to confirm when she reviews: phone (858-431-6888 from her uni-assist applications), entry date (15.09.2026), place of birth field ("Baltimore" - comma rejected by portal validator).

**6. Family Bitwarden collection for shared logins.**
- diplo.de portal credentials saved to "rempel family" org ? "rempel passwords collection" so Liz has access.
- Password: Studien-Portal-Liz-2026! (humanized, easy to type).

---

## CURRENT STATE

**Portal application (digital.diplo.de):**
- Login: emm@transposon.org / Studien-Portal-Liz-2026! (in Bitwarden family collection)
- 2FA: 6-digit code emailed to max.rempel2@gmail.com each login
- Process name: "Liz Student Applicant Visa" (now regular student visa after the switch)
- Reference: AP/463/230726/000000604
- **Entry form: FULFILLED** - switched to "Yes, already admitted" path, all qualifying questions answered
- **VIDEX form: 7/7 sections complete**
- **Documents: 7 required, 0 uploaded yet** - this is the remaining work

**What's been sent/emailed:**
- Three admission-request emails (K?ln, Hannover, Dortmund) - all sent from emm@transposon.org
- TH K?ln replied: Prof. Freiburg said the official admission letter might be on the portal - Max downloaded it during the session
- Anna letter to Oksana and Liz explaining the applicant-visa logic - sent, but has one minor inaccuracy (said "book appointment, bring documents later" - real LA flow is submit-online-first). Max said NOT to send a correction yet; will handle after submission.

**TH K?ln admission letter:**
- Downloaded and saved: `TH_Koln_Letter_of_Admission_Zulassungsbescheid_20260612.pdf` in `C:\Users\maxre\Nextcloud\2026 Applications as senior undergrad\modified\uni-assist\th koln automation it submission 20260427\`
- Dated 12.06.2026, signed, stamped, verification number, unconditional admission to Automation & IT Master (English-taught), Winter 2026/27.

**Expatrio blocked account:**
- Funded (blocked-account-only; TK is NOT bundled).
- ~?11,904 parked - covers the financial-proof requirement.

**Hannover/Dortmund:**
- No official admission letters yet. Emails sent. Still Liz's preferred choices.

---

## EXACT NEXT STEP

**1. Resolve the DR-WALTER vs Care Concept insurance question (URGENT, was mid-discussion at session end).**

The session ended with a price bomb: DR-WALTER Provisit Student is actually **?79/month, so ~?237 for 3 months**, not the ~?50/month / ~?100-130 total originally estimated. The assistant flagged this as a DANGER and recommended switching to **Care Concept Incoming Basic** (~?30-45/month, ~?90-135 total). Max had said "proceed" and gave the card (ending X6391) *before* this discrepancy was discovered. **The user has NOT yet answered the "DR-WALTER at ?237 or Care Concept at ~?100?" question.** That is the very first thing to ask.

**2. Purchase the chosen policy, get the insurance PDF, upload it as document #6.**

**3. Upload the remaining 6 documents to the portal:**
- Passport scan (on file: `Passport Scan 2026-04-04.pdf`)
- Proof of admission (TH K?ln Zulassungsbescheid - on file)
- CV (on file)
- Intention-to-study letter (a short free-text statement - likely adaptable from her motivation letters on file)
- Proof of livelihood (Expatrio blocked-account confirmation - needs to be located or requested)
- Proof of residence in LA consular district (something showing Liz lives in San Diego - e.g. a utility bill, bank statement, or similar)

**4. Let Liz review everything, then submit. Do NOT submit without Liz's explicit approval - it is her legal declaration.**

**5. After submission:** the portal pre-checks the application and, if complete, sends an individualized appointment-booking link. Slots are typically ~2 weeks out. She then attends in person in LA with originals, fingerprints, and pays the ~?75 visa fee.

---

## OPEN QUESTIONS AWAITING MAX

1. **Which incoming insurance?** DR-WALTER Provisit Student at ~?237 total (TK-partner bridge, clean handoff) vs Care Concept Incoming Basic at ~?90-135 total (cheapest, still consulate-accepted). The card is ending X6391.

2. **Residence proof for LA consulate:** What document proves Liz lives at 6294 Caminito Del Oeste, San Diego, CA 92111? (Bank statement, driver's license, utility bill?)

3. **Expatrio blocked-account confirmation PDF:** Is it on file somewhere under the applications folder, or does it need to be downloaded from the Expatrio dashboard?

4. **Intention-to-study letter:** Liz may want to write this herself, or the assistant can draft one from her existing motivation letters - Max's call.

5. **The Anna correction letter to Oksana/Liz** - deferred until after submission.

---

## KEY PATHS, IDs, NAMES

| What | Value |
|---|---|
| Portal | https://digital.diplo.de |
| Login | emm@transposon.org |
| Password | Studien-Portal-Liz-2026! (Bitwarden, rempel family collection) |
| Process reference | AP/463/230726/000000604 |
| Process group ID | 8fb71e4c-2c91-40ac-8462-b27c2c39d08c |
| App ID | 92dad7d0-b380-5564-bcd3-1f346542d00a |
| Liz legal name | Samuel Maximovich Myakishev-Rempel |
| Passport # | A29748001 (issued 12 Nov 2023, expires 11 Nov 2033, US Dept of State) |
| DOB / Place | 11 Nov 2002 / Baltimore, Maryland (portal: "Baltimore" only - comma rejected) |
| Address | 6294 Caminito Del Oeste, San Diego, CA 92111 |
| Phone (Liz) | 858-431-6888 ? entered as 0018584316888 (portal rejects "+") |
| Email (joint) | emm@transposon.org |
| TH K?ln admission letter | `TH_Koln_Letter_of_Admission_Zulassungsbescheid_20260612.pdf` |
| Application data doc | `visa_diplo_application_data_v01.md` (in the same folder) |
| Master system doc | `LIZ_APPLICATIONS_SYSTEM_tomemex.md` |
| Agent rules | `C:\Users\maxre\Nextcloud\claude_md_synced\global_AGENT_RULES.md` |
| Liz's card | Ends in X6391 |
| Intended entry | 15.09.2026 |
| Intended end | 15.09.2027 |
| Intended city | Gummersbach (TH K?ln Campus Gummersbach), postal 51643 |
| Reference (section 6) | TH K?ln, Prof. Michael Freiburg, Steinm?llerallee 1, 51643 Gummersbach, phone 0049226181960 |

**7 VIDEX sections filled:**
1. Representation - "for myself"
2. Personal - full name, DOB, place of birth, parents (Max & Oksana), US national, single, student
3. Contact - San Diego address, Liz's phone, emm@transposon.org
4. Identification - passport A29748001, ordinary, US Dept of State
5. Travel - study purpose, single visa ?12 months, 15.09.2026-15.09.2027
6. Reference - TH K?ln, educational establishment (Prof. Freiburg contact)
7. Means of support - Expatrio blocked account, Gummersbach intended stay, no scholarship, no health insurance yet, prior Germany stay = Yes

---

## GOTCHAS AND DEAD ENDS

- **DR-WALTER price discrepancy:** Assistant estimated ~?50/month; real price is ?79/month (~?237 for 3 months). DO NOT proceed with the purchase until Max confirms which policy he wants. This is the #1 open item.

- **Portal phone field rejects "+":** Use `00` prefix (e.g. `0018584316888`). Plus sign triggers an invalid-state validator. Plain digits are fine.

- **Portal place-of-birth field rejects commas:** "Baltimore, Maryland" is invalid. Use just "Baltimore" - Country of birth is already "United States" in a separate dropdown, so the city alone is enough.

- **Portal deep-links bounce to /login:** The SPA uses Keycloak SSO. Always navigate by clicking through the UI: `/groups` ? Open process ? Open application ? Fill out form. Do not try direct URLs to `/apps/...` or `/form/...`.

- **2FA delivery lag:** The 6-digit confirmation codes go to max.rempel2@gmail.com (NOT the emm inbox). Sometimes delivery lags 5-10 minutes. Check the email thread from `noreply@digital.diplo.de`; use "Send code again" if a code expires (20-min validity).

- **OTP box JS quirk:** When filling the 6 individual digit boxes, filling all 6 doesn't always enable the "Continue" button. The fix is to Backspace and retype the last digit - this triggers the JS handler.

- **Cookie banner blocks clicks:** On the application/process pages, a cookie consent banner can overlay the "Open process" button. Click "Deny" first.

- **Custom comboboxes, not native `<select>`:** Country, sex, marital status, nationality, occupation fields are custom React components. Click to open the dropdown,
