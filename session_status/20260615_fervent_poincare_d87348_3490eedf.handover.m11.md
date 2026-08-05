# Scribe handover - milestone 11 (~165K tokens)
# session: 20260615_fervent_poincare_d87348_3490eedf
# cwd: C:\claude_base\.claude\worktrees\fervent-poincare-d87348
# written: 2026-06-15 19:45:31 by deepseek-v4-pro

# HANDOVER - RUB?PLN Exchange for Olga (Wroc?aw)

---

## GOAL (Max's words)
"Convert 30k rubles in cash, my friend travels from moscow to krakov poland [...] compare conversion rate [...] Don't trust official or ads, see what actual users report."

Later corrected: **Krakow ? Wroc?aw.** Friend = **Olga Lianzburg** (also goes by a G-name variant). Final ask: compare RUB?PLN rates, recommend the best route, send Olga a Russian email with tables.

Then: "search online and check if curr exchange in poland actually answers phone [...] the exchange places are afraid of robbers, they are small, i woudl be totally suprised they answer phone. Retract the stupid advice to call. send follow up email to olga."

---

## DECISIONS MADE + WHY

| # | Decision | Reasoning |
|---|----------|-----------|
| 1 | **Euro route is best** (RUB?EUR in Moscow, EUR?PLN in Wroc?aw). Yields ~1,418 z? net. | Moscow has thousands of banks for euro cash - trivial to buy. Euros are accepted everywhere in Poland; rubles are accepted by almost nobody = monopoly trap if she's stuck in Wroc?aw with rubles. |
| 2 | **Ruble route second** (Tavex Wroc?aw directly). Yields ~1,390 z? net. | Only ~28 z? worse, but she's locked into ONE kantor. If it's closed/refuses, she's stuck. Max: "If she is stuck in fucking w, she is stuck. like monopoly." |
| 3 | **Moscow ? Minsk ? Wroc?aw route dropped.** | When destination became Wroc?aw (not Krakow), Tavex Wroc?aw's ruble rate (0.0465) made the Minsk two-hop not worth the detour. |
| 4 | **Tavex as the Wroc?aw recommendation** (ul. Sucha 1, Wroclavia mall by Wroc?aw G??wny station). | Only kantor in Wroc?aw with a good published ruble buy rate. Large chain, regulated. The rate on the board IS the net rate - Polish kantors bake fees into the buy/sell spread, not on top. Flat ~2 EUR fee only. |
| 5 | **Phone-answering advice was wrong - retracted.** | Initial "call ahead" advice came from kantor-industry/marketing pages (centkantor.pl, dobrykantor.pl), NOT real users. User-complaint search found complaints about post office/pharmacies/DHL not answering, ZERO kantor-specific testimony. Max's reasoning: kantors are small, afraid of robbers, would never answer. Honest conclusion: assume they DON'T answer. |
| 6 | **mxmail auto-BCC baked into code** (mxmail_v01.py). | Every mass@tamza send now envelope-BCCs max.rempel2@gmail.com automatically - no Claude memory needed. |
| 7 | **HTML support added to mxmail.** | ASCII tables break in Gmail's proportional font. HTML with real `<table>` markup renders properly. |
| 8 | **Never re-send to external recipients for formatting fixes.** | Saved as feedback memory `feedback_no_respam_external.md`. Olga got 3 emails - 2 plain text (broken table) + 1 HTML (good). The re-send without Max's approval was a mistake. |

---

## CURRENT STATE

**Done:**
- Rates researched live via Playwright (kantor.live) + WebSearch + WebFetch for Moscow, Minsk, Krakow, Wroc?aw.
- Rates verified: Moscow EUR ~88.5 RUB/EUR, Wroc?aw Tavex RUB buy 0.0465, Wroc?aw Tavex EUR buy 4.206.
- Russian HTML email sent to **Olga at tutoreffective@gmail.com** (from mass@tamza.com, signed Claude).
- Auto-copy sent to max.rempel2@gmail.com (manual copy + now structural via auto-BCC).
- mxmail_v01.py upgraded (auto-BCC + HTML), committed + pushed to master (a70a52db).
- Phone-answering research done - admitted reliance on ads, found zero user confirmation.
- Max's instruction to retract the phone advice and send a follow-up email to Olga received.

**NOT DONE - the exact next step:**
- **Send Olga a follow-up email retracting the "call ahead" advice.** The original email said to phone Tavex to confirm ruble acceptance. Max says this is stupid - they're small/afraid of robbers/won't answer - so retract it.

---

## EXACT NEXT STEP

**Compose and send a SHORT follow-up in Russian to Olga (tutoreffective@gmail.com) retracting the phone-call advice.**

Content should:
- Say the earlier advice to call Tavex before arriving was wrong - these small exchange kiosks typically don't answer phones (afraid of robbers, understaffed).
- Just walk in. Tavex Wroclavia is in the mall by the station, reliable. Or better: bring euros for maximum flexibility.
- Keep it brief - she already has the full report; this is just a correction on one safety tip.
- **Do NOT re-send the full original report.** This is a standalone correction note.
- Signed Claude.

**CAUTION:** Olga already got 3 emails from the original send (2 plain + 1 HTML). This follow-up is explicitly requested by Max - it's a substantive correction, not a formatting redo - so it's appropriate. But if you're unsure whether he still wants this extra send after the earlier spam lesson, confirm with him before sending.

---

## OPEN QUESTIONS (still awaiting Max)

1. **Delete or keep `_send_olga_zloty_20260615.py`?** - Claude asked, Max hasn't answered.

---

## KEY PATHS / IDS

| What | Value |
|------|-------|
| **Olga's email** | tutoreffective@gmail.com |
| **Olga's Gmail alias** | cozymirrors (forwards to same inbox) |
| **Send-from mailbox** | mass@tamza.com (MXroute/witcher server) |
| **Reply-To** | max.rempel2@gmail.com |
| **Auto-BCC** | max.rempel2@gmail.com (wired in mxmail_v01.py) |
| **Mailer script** | `C:\claude_base\tools\mxmail\mxmail_v01.py` |
| **One-off send script** | `C:\claude_base\tools\mxmail\_send_olga_zloty_20260615.py` |
| **Feedback memory** | `C:\Users\maxre\.claude\projects\C--claude-base\memory\feedback_no_respam_external.md` |
| **Memory index** | `C:\Users\maxre\.claude\projects\C--claude-base\memory\MEMORY.md` |
| **Git commit** | a70a52db (mxmail upgrades, pushed to origin/master) |
| **Playwright profile** | `C:\claude_base\playwright_profile` (shared - kill stale chrome.exe filtered by 'playwright_profile' in CommandLine) |
| **Tavex Wroc?aw** | ul. Sucha 1, Wroclavia mall, by Wroc?aw G??wny station |
| **Rates (live 15 Jun 2026)** | Moscow EUR buy: ~88.5 RUB/EUR; Tavex Wroc?aw PLN buy: 0.0465 (RUB), 4.206 (EUR) |
| **Conversion math** | 30,000 RUB ? 339 EUR ? ~1,418 PLN (euro route, -2 EUR flat fee) |
| **Ruble-direct** | 30,000 RUB ? ~1,390 PLN (Tavex, -2 EUR flat fee) |
| **Delta** | Euro route wins by ~28 PLN (~550 RUB, ~2%) |

---

## GOTCHAS

1. **Shared Playwright profile locks.** If browser navigation fails with "already in use", kill only the Chrome processes whose CommandLine contains `playwright_profile` (PowerShell: `Get-CimInstance Win32_Process -Filter "Name='chrome.exe'" | Where-Object { $_.CommandLine -match 'playwright_profile' }`), then delete `SingletonLock`/`SingletonCookie`/`SingletonSocket` from `C:\claude_base\playwright_profile\`.

2. **Google Contacts API may be down.** Fallback: Gmail search_threads (MCP `d1237438-8996-485f-bbb2-aa5b2e7dda32__search_threads`) finds email addresses from past threads.

3. **Gmail MCP can only create DRAFTS, not send.** Must use mxmail SMTP for actual sending.

4. **ASCII tables break in Gmail.** Always use `html=` param with real `<table>` markup in mxmail.

5. **Max dislikes external re-sends.** If something needs fixing after the first send, send the fix ONLY to Max's copy unless he explicitly approves resending to the external recipient.

6. **Polish kantors don't answer phones** (Max's assessment, and no user evidence contradicts it). Don't advise calling them.

7. **Olga has already received 3 emails** from the original report - any follow-up must be a brief, clearly separate correction note, not a re-send of the original.
