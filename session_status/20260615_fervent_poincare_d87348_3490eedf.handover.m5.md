# Scribe handover - milestone 5 (~81K tokens)
# session: 20260615_fervent_poincare_d87348_3490eedf
# cwd: C:\claude_base\.claude\worktrees\fervent-poincare-d87348
# written: 2026-06-15 14:33:08 by deepseek-v4-pro

# HANDOVER - Scribe's record

**GOAL (in Max's words)**  
Convert 30,000 Russian rubles in cash to Polish zloty (PLN). A friend travels from Moscow to Krakow, Poland. Compare actual user?reported cash exchange rates in Moscow, Minsk, and Krakow. Do NOT trust official/ads; real users often face hidden fees and spreads ~20%. "also use plwrt to double check".

**DECISIONS MADE + WHY**  
- **Krakow:** Only 4 kantors accept RUB. Best posted rate on kantor.live was 0.040 PLN/RUB (mid?market ?0.051). That's ~22% loss, giving ~1,200 z? for 30k?. Confirmed "crazy 20%" expectation.  
- **Moscow:** (Dismissed) Polish zloty is scarce post?sanctions; rates are terrible or the currency simply unavailable. No realistic cash route.  
- **Minsk:** Researched via myfin.by. Two hops: RUB?BYN?PLN. RUB cash rates near mid?market (Belarus trades rubles easily). Cross?rate estimate ~1,365 z? for 30k?, about 11% loss. **Winner.**  
- Preferred source: real board aggregators (kantor.live, myfin.by) - not official bank quotes.

**CURRENT STATE**  
- Assistant has fetched and crunched numbers for Krakow and Minsk.  
- User prompted: "also use plwrt to double check".  
- The assistant has NOT yet responded to that last prompt. No search or request has been made for "plwrt".  
- The concrete Minsk bank/address list (requested earlier) is still pending - user didn't answer the offer yet.

**EXACT NEXT STEP**  
1. Identify what "plwrt" means. Likely a user?specific shorthand for a website or service (maybe pln?wart.pl, walutomat.pl, pl.rate.am, or a Telegram bot). If unclear, ask the user to clarify, or try common Russian?language exchange?monitoring tools that track real?world cash rates (e.g., bestchange, rates.am, profit.by, or "pln warto??" search).  
2. Search "plwrt" explicitly in the tool set; if nothing found, clarify with Max.  
3. Re?compute the 30k? ? PLN numbers from the plwrt data and compare to the earlier Minsk/Krakow findings. Confirm (or correct) the earlier conclusion.  
4. If the friend's route indeed passes through Minsk (e.g., train/bus from Moscow to Krakow via Minsk), prepare a shortlist of best Minsk exchange points with addresses and real?time rates from the same aggregator.

**OPEN QUESTIONS AWAITING MAX**  
- What exactly is "plwrt"? (A specific site, bot, or channel he expects?)  
- Does the friend actually transit Minsk? (If not, Minsk advice is irrelevant - only Krakow matters; confirm route to avoid wasted work.)  
- Is there a time constraint for the trip (rates change daily; the handover handoff may be stale by then)?  
- Should we also check Brest (border city) or other Belarus towns on the way?

**KEY PATHS / IDs / COMMANDS**  
- Tool used: ToolSearch, WebSearch, WebFetch.  
- Key URLs:  
  - `https://kantor.live/en/kantory/krakow/RUB` - Krakow RUB rates.  
  - `https://myfin.by/currency/minsk` - Minsk RUB cash buy/sell.  
  - `https://myfin.by/currency/pln` - Minsk PLN buy/sell (needed for cross rate).  
- Rates as of session time (approximate):  
  - Mid?market RUB/PLN ~0.051 PLN per ?.  
  - Krakow kantor: ~0.040 PLN/? ? 30k? = ~1,200 z?.  
  - Minsk RUB?BYN near 0.035 (in BYN, then BYN?PLN ~1.30 -> ~1,365 z? for 30k?). Exact numbers: from myfin, RUB buy in Minsk ~3.50 BYN per 100 RUB, PLN sell ~1.30 BYN/PLN (give or take).  
- No file paths saved; all information from online fetches.

**GOTCHAS & DEAD ENDS RULED OUT**  
- **GOTCHA 1:** Online converters or Google spot rates are useless for cash - reality is ~20% spread in Krakow. Already confirmed.  
- **GOTCHA 2:** RUB cash is ultra?illiquid in Poland; only 4 kantors in Krakow list it, and the spread is huge. Don't rely on Warsaw or other Polish cities either.  
- **GOTCHA 3:** Minsk requires a visa/transit OK for the friend; if the friend can't enter Belarus, only Krakow is feasible. This wasn't confirmed yet.  
- **Dead end:** Moscow?side conversion to PLN directly - ruled out, no need to revisit.  
- **Dead end:** Using official Russian bank rates - ruled out, they don't reflect street cash availability.  
- **Potential dead end:** If "plwrt" turns out to be a Russian aggregator that lists only Moscow rates, it won't give Minsk or Krakow data. The search should be adapted.
