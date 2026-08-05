# Scribe handover - milestone 7 (~107K tokens)
# session: 20260615_fervent_poincare_d87348_3490eedf
# cwd: C:\claude_base\.claude\worktrees\fervent-poincare-d87348
# written: 2026-06-15 14:43:11 by deepseek-v4-pro

# HANDOVER - RUB?PLN Cash Exchange for Wroc?aw Trip

---

## GOAL (Max's words)
Convert 30,000 rubles cash. Friend travels Moscow ? Wroc?aw, Poland. Give **two final options** (euro route vs direct Tavex rubles), compared in **actual money difference (rubles + %)** , with all caveats and comments. Output a **long text report ready to paste into Telegram**.

---

## DECISIONS MADE + WHY

1. **Moscow ? zloty directly: ruled out.** Zloty is exotic/scarce in Russia post-sanctions. Banks rarely stock PLN cash. Not worth checking.

2. **Krakow as destination: ruled out.** User changed destination to Wroc?aw mid-session.

3. **Minsk two-hop (RUB?BYN?PLN): deprioritized.** It was competitive (~1,365-1,430 z?) but the Wroc?aw Tavex rate changed the calculus. Not in the final two options.

4. **Euro route (Moscow RUB?EUR, Wroc?aw EUR?PLN):** Chosen as Option A. Buy euros at Alfa-Bank Moscow (~88.5 ?/?), sell euros at Tavex Wroc?aw (~4.206 z?/?). Result: ~1,426 z?. The spread is small because euros trade near mid-market in Poland.

5. **Direct rubles at Tavex Wroc?aw:** Chosen as Option B. Tavex (Sucha 1, Wroclavia mall, next to Wroc?aw G??wny station) buys rubles at **0.0465 z?/?** - far better than Krakow's 0.040-0.044. Result: ~1,395 z?. **This is the recommended option** - simplest, only ~30 z? worse than the euro detour, and avoids Moscow euro-cash risk.

6. **Hidden fees fear:** Investigated Polish and Russian user reviews. Polish kantors quote **NET rates** - the spread IS the fee, nothing added on top. Tavex has a flat ~2?/transaction but that's negligible (~8.5 z?). Board rate 0.0465 is genuinely what lands in hand. The "20% hidden fee" the user feared is actually a *bad displayed rate* at tourist kantors (like Krakow's 0.040), not a secret surcharge.

7. **Playwright browser locked:** Stale Chrome processes from a prior session were using the playwright_profile. Killed 8 specific Chrome PIDs (5844, 33468, 32268, 8264, 8340, 16692, 34536, 34152) via taskkill, removed SingletonLock, then used Playwright live to verify Wroc?aw rates on kantor.live.

8. **Sources verified live or via WebFetch:** kantor.live (Polish kantor aggregator), banki.ru (Moscow cash EUR), myfin.by + select.by (Minsk rates).

---

## CURRENT STATE

The numbers are fully gathered and verified. Both options are defined. What's **NOT yet done**: the final Telegram-ready long text report with the side-by-side comparison in rubles and percentages. The session ended mid-task - the assistant was about to write it.

---

## EXACT NEXT STEP

**Produce the Telegram-pasteable long text report** containing:

- Intro: what this is (30k RUB ? PLN, Moscow ? Wroc?aw)
- Fair mid-market baseline (~1,530 z? for reference)
- **Option A - Euro route:** step-by-step (Alfa-Bank Moscow: buy ? at ~88.5 ?/? ? 339?, then Tavex Wroc?aw: sell ? at 4.206 z?/? ? ~1,426 z?). Include the caveat about Moscow euro cash availability.
- **Option B - Direct rubles at Tavex Wroc?aw:** step-by-step (Tavex Sucha 1, Wroclavia mall, 0.0465 z?/? ? ~1,395 z?). Include phone-call recommendation.
- **Comparison table or bullet:** difference in actual z?oty, equivalent rubles lost, and percentage loss vs mid-market.
- All caveats: Moscow euro rationing risk, Polish kantor net-rate explanation, Tavex ~2? flat fee, confirmation call.
- Recommendation: Option B (direct rubles) unless the friend already holds euros.

---

## OPEN QUESTIONS AWAITING THE USER

- None explicit. The user simply wants the Telegram text. However, the assistant previously flagged that **Tavex should be phoned** to confirm (a) they still accept RUB cash that day, and (b) the 0.0465 rate applies to a ~30k amount (some kantors degrade rate below a threshold). The friend "probably won't call," so this should be mentioned as a low-effort insurance step in the report.

---

## KEY PATHS, IDs, NAMES

| What | Value |
|------|-------|
| **Tavex Wroc?aw branch** | Sucha 1, Wroclavia shopping centre (next to Wroc?aw G??wny station) |
| **Tavex RUB buy rate** | 0.0465 z?/? (live, via kantor.live) |
| **Tavex EUR buy rate** | 4.206 z?/? (live, via kantor.live) |
| **Alfa-Bank Moscow EUR sell** | ~88.5 ?/? (via banki.ru) |
| **Fair mid-market RUB?PLN** | ~0.051, so 30k? ? 1,530 z? |
| **Rate sources** | kantor.live/en/kantory/wroclaw/RUB, kantor.live/en/kantory/wroclaw/EUR, banki.ru/products/currency/cash/eur/moskva/ |
| **Playwright profile** | C:/claude_base/playwright_profile/ (cleaned up after stale lock) |
| **cwd** | C:\claude_base\.claude\worktrees\fervent-poincare-d87348 |

---

## GOTCHAS + DEAD ENDS

- **Krakow is a dead end** - only 4 kantors take rubles, rate ~0.040, InternetowyKantor suspended RUB entirely. Irrelevant after destination change.
- **Moscow direct RUB?PLN is a dead end** - PLN cash scarcely available post-sanctions.
- **Playwright shared profile lock** - if browser navigation fails with "Browser is already in use," check for stale chrome.exe processes using playwright_profile (via `Get-CimInstance` or tasklist), taskkill them, delete `SingletonLock` file. Do NOT kill the user's personal Chrome.
- **Polish kantor rates are NET** - spread is the fee. No hidden surcharge. The scary "20%" is just a bad buy rate, not a line-item fee.
- **Tavex flat fee** - ~2? per transaction, negligible (~8.5 z? on this exchange).
- **Moscow euro cash caveat** - since 2022, banks sometimes cap euro cash sales or add commission. 339? is small enough to usually be fine, but this must be flagged in the report.
