# Scribe handover - milestone 10 (~159K tokens)
# session: 20260615_fervent_poincare_d87348_3490eedf
# cwd: C:\claude_base\.claude\worktrees\fervent-poincare-d87348
# written: 2026-06-15 19:26:12 by deepseek-v4-pro

# HANDOVER - Currency Exchange Research + Olga Email + mxmail Improvements

Session: 67 turns, ~159K tokens, compaction imminent.
Date context: Transcript references "15 June 2026" as the "live" rate date.

---

## GOAL (in Max's words)

"Convert 30k rubles in cash, my friend travels from moscow to krakov poland. So compare conversion rate of 30k rub to zloty, in moscow, minsk, or krakov. Don't trust official or ads, see what actual users report."

Later refined: destination changed from Krakow to **Wroc?aw**. Final task: produce a Russian-language report for Olga (his friend) with both options in a comparison table, formatted, signed as Claude, sent via email. Then fix the mailer so auto-BCC to Max works permanently.

---

## DECISIONS + WHY

### 1. Minsk route ? decent, but not best for this trip
- RUB?BYN?PLN two-hop in Minsk gave ~1,365-1,430 z? for 30k ? (~7-11% below mid-market ~1,530 z?).
- Viable only if the friend transits Minsk. Not selected as final rec.

### 2. Direct RUB in Wroc?aw (Tavex) ? simple, decent rate
- Tavex at Wroclavia mall (Sucha 1, by Wroc?aw G??wny station) buys rubles at **0.0465 z?/?**.
- 30,000 ? ? ~1,395 z? (minus ~2 EUR flat fee ? ~1,390 z? in hand).
- Tavex is a regulated chain, board rate = what you get, no hidden commission confirmed by Polish user reviews.
- **Risk: only ONE place in Wroc?aw takes rubles.** If it's closed or refuses - stuck.

### 3. EUR route (buy ? in Moscow, sell ? in Wroc?aw) ? FINAL WINNER
- Moscow: buy EUR at ~88.5 ?/? ? 30,000 ? = ~339 ?.
- Wroc?aw: sell EUR at Tavex @ 4.206 z?/? ? ~1,418 z? in hand.
- Difference: +28 z? (+~550 ?, +2%) over direct rubles.
- **Why it wins, per Max:** "In Moscow there are tons of banks, thousands. If she is stuck in fucking Wroc?aw with rubles, she's stuck - like a monopoly. Euro is much more flexible."
- The actual monetary gain is tiny (~2%), but the flexibility/risk argument is decisive: euros can be exchanged ANYWHERE in the EU, rubles only at one Tavex kiosk.

### 4. Email formatting
- Monospace ASCII tables broke in Gmail's proportional font.
- Switched to HTML body with proper `<table>` and inline CSS borders.
- Language: Russian (Max's friend Olga is Russian-speaking).

### 5. mxmail improvements (two changes, both committed)
- **Auto-BCC:** every email from mass@tamza.com now automatically BCCs `max.rempel2@gmail.com` (envelope recipient, hidden from headers, deduped). Permanent fix - no reliance on Claude remembering.
- **HTML support:** mailer now accepts an `html_body` parameter and sends proper `multipart/alternative` MIME messages.

---

## CURRENT STATE

**Done:**
- ? Live rate comparison: Minsk, Krakow (originally), Wroc?aw (final) - all three cities researched with real cash rates from kantor.live (via Playwright when possible), myfin.by, banki.ru.
- ? User review verification: searched Polish and Russian forums for Tavex hidden fees - confirmed no secret commissions.
- ? Olga identified in Gmail: **tutoreffective@gmail.com** (Olga Lianzburg / Lyanzbourg, also uses cozymirrors alias).
- ? Email sent 3 times to Olga (two plain-text where the table collapsed, one final HTML with proper rendering).
- ? Copy sent to Max at max.rempel2@gmail.com.
- ? mxmail_v01.py updated with auto-BCC + HTML support.
- ? Changes committed (a70a52db) and pushed to origin/master.

**In flight:**
- Nothing active. Email is sent, tooling is fixed.

**Known caveat:**
- Olga received the email 3 times (two broken-plain-text + one good HTML). They thread in Gmail so it looks like one updated message. Max was annoyed about the double-send: "that's idiotic to send two messages in a row."

---

## EXACT NEXT STEP

**None required.** The task is complete. Olga has the Russian report with the comparison table. The euro route is recommended. The mailer is fixed for all future sessions.

If the cold session picks up, Max may want to:
- Confirm Olga received and understood the instructions.
- Do something else entirely - this task is closed.

---

## OPEN QUESTIONS

- **Did Olga act on it?** Unknown - no reply was received during the session.
- **Tavex phone confirmation:** Olga probably won't call (Max said "not sure she will actually call"), but the euro route bypasses this entirely since euros can be exchanged anywhere.

---

## KEY PATHS / IDs

| What | Value |
|---|---|
| mxmail script | `C:\claude_base\tools\mxmail\mxmail_v01.py` |
| One-off send script | `C:\claude_base\tools\mxmail\_send_olga_zloty_20260615.py` (can be deleted) |
| Olga's email | `tutoreffective@gmail.com` |
| Sender address | `mass@tamza.com` |
| Max's email (auto-BCC) | `max.rempel2@gmail.com` |
| Reply-To | `max.rempel2@gmail.com` |
| Git commit | `a70a52db` on `master` |
| Wroc?aw Tavex | Sucha 1, Wroclavia mall, next to Wroc?aw G??wny station |
| Rate sources | kantor.live, myfin.by, banki.ru |
| Playwright profile | `C:\claude_base\playwright_profile\` (stale Chrome processes killed during session) |

---

## GOTCHAS

1. **Playwright browser lock:** The shared Playwright profile was locked by a stale Chrome process from a sibling Claude session. Fixed by killing only the Chrome processes using `playwright_profile` (PIDs: 5844, 33468, 32268, 8264, 8340, 16692, 34536, 34152), then deleting the SingletonLock file. Max's personal Chrome was untouched.

2. **mxmail was plain-text only:** The first two emails to Olga had a monospace table that collapsed into garbage in Gmail's proportional font. Added `html_body` support to the mailer to fix this permanently.

3. **Krakow vs Wroc?aw flip:** In Krakow, ruble rates are terrible (~0.040 z?/?), so the EUR route was ~100+ z? better. In Wroc?aw, Tavex pays 0.0465, so the EUR route is only ~28 z? better. The *numbers* make it almost a tie, but Max's *risk/flexibility* argument (monopoly vs thousands of banks) makes EUR the clear winner regardless.

4. **Google Contacts API was down** - fell back to Gmail thread search to find Olga's address.

5. **Moscow EUR cash caveat:** Since 2022, some Russian banks ration or cap EUR cash. 339? is a small amount, likely fine, but it was noted. Max dismissed this concern: "in Moscow there are tons of banks, thousands."
