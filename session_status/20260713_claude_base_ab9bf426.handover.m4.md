# Scribe handover - milestone 4 (~339K tokens)
# session: 20260713_claude_base_ab9bf426
# cwd: C:\claude_base
# written: 2026-07-13 18:46:44 by deepseek-v4-pro

# HANDOVER - Bowater Family 23andMe Download & NPA Analysis (X32 session)

## GOAL (in Max's own words)
"Download the 23andMe raw data for Lottie Bowater's family (mother Julie, father Roger). Then analyse for non?parental alleles (NPAs) exactly like the 5?7 other families already done. Look for all sorts of NPAs. Compare across families. Test proximity (50?kb windows). Brainstorm what moves the research forward - probably sequencing. Also send Lottie an email. Work autonomously."

---

## DECISIONS MADE + WHY
1. **23andMe login & 2FA** - The account is `max@tamza.com` (Max's own account, Lottie is a profile inside it). The session hit a 2FA prompt. Instead of fighting the Bitwarden browser?extension contention, we pulled the 6?digit code from the command line (`bw get totp`) using the already?unlocked vault session file. This avoids the "only one session gets the logged?in Bitwarden" problem permanently. The method was written into the shared?logins file so all future sessions can do the same. **No config change needed.**

2. **Data storage** - All raw zip files must go into the canonical folder already used for earlier Bowater work:  
   `Nextcloud\xg1_data\xg1_fams\20260614_bowater_trio_23andme\`  
   (A stray folder I accidentally created was deleted after moving Roger's file there.)

3. **NPA scanner** - The original L473 scanner script from the January analysis is **lost**. I re?implemented it faithfully from the output formats and the documented rules (DOCHAN, HETEROPOP, HOMOPOP), matching the existing 7?family analysis exactly. This re?implementation is the official scanner for the Bowater 23andMe trio and is committed as `npa_scanner_bowater23_v01.py`. The report plainly states it is a re?implementation.

4. **Proximity definition** - When Max later asked for cross?family proximity tests, we used a **50?kilobase** window (as he specified).

5. **Collaboration via P5 room** - After branching as X32, we used the "p5" broadcast room to share findings with the session drafting the Lottie letter and with X7A (who is working on Oliver WGS filtering). All discoveries were posted there in letter?ready form.

6. **Next research step** - The array work on NPAs has hit its ceiling (chip miscalls vs real events). The brainstorm concluded that **whole?genome sequencing** is the payoff. Near?term: finish Oliver's filtered WGS NPAs (mother?only trio, weaker). The highest?value step: sequence the Bowater trio (complete trio, both parents). No final decision made - needs Max's go?ahead.

---

## CURRENT STATE
### Data
- **Bowater trio** - fully downloaded and verified.  
  - Lottie (child) - already present from June.  
  - Roger (father) - downloaded Jul?10.  
  - Julie (mother) - downloaded later when the email arrived.  
  All three `.zip` files plus a `README_status_tomemex.md` are in the canonical folder (`Nextcloud\xg1_data\xg1_fams\20260614_bowater_trio_23andme\`).  
- **Telegram reminder** - Scheduled to nag every 2?days, but **deleted** after Julie's file was retrieved. No more nags.

### Lottie email
- **Sent** from Anna (`mass@tamza.com`), CC to Max, to `depresstival@gmail.com`.  
- Informs her the trio data is complete, thanks her, sets expectation that analysis comes later.  
- The drafted letter (with discoveries) is being worked on by another session in P5. The exact wording and caveats are that session's responsibility; it will be shown to Max before sending.

### Array?level NPA analysis (complete)
- **Scanner run**: 0 DOCHAN, 7 HETEROPOP, 31 HOMOPOP ? 38 NPAs out of 601?900 positions (0.0063% non?parental). Trio is genuinely Mendelian.
- **Cross?family exact?match sharing**: zero positions shared between Bowater 23andMe and any other family. The only overlap is Lottie's own old MyHeritage data at one position (chr2?31,454,665).  
- **50?kb proximity + permutation**: Bowater's NPAs fall near other families' NPAs at exactly the chance rate (p=0.46). No real hotspot signal.  
- **Clusters**: one tight cluster on chr10 (3 NPAs within 9?kb) that sits in the gene CTNNA3, a known CNV/deletion hotspot - likely a small parental deletion, not noise.  
- **Gene annotation**: Lottie's two strongest candidate?real NPAs (called on both 23andMe and MyHeritage) are in **CAPN14** (chr2) and **MAF** (chr16). The chr20 locus is gene?poor.  

All outputs are in `Nextcloud\xg1_data\xp2_analysis\260713_NPA_Bowater_23andme_trio\` with subfolders `proximity/`, and the scanner script + cross?family script + annotation script are committed and pushed to `master`.

### WGS / Oliver thread (in flight)
- **Oliver Kenefick** - only mother (Kristen) and son sequenced; father absent.  
- The needed "properly filtered real NPA list" from reads is **not on disk** yet.  
- X7A (P5 room) is building a corrected maternal?inference phaser (a 3?gate read?level filter).  
- My role (X32) agreed with X7A: once the filter runs, I will do the population?frequency annotation and cross?check the resulting Oliver NPAs against the array families.  
- The earlier alarm about deleted BAMs on asto was false; data is safe on the Centauri drive (backup till 16:00).

---

## EXACT NEXT STEP (cold session picks up here)
1. **Check the P5 room** (`python bcast.py room p5 --read`) for any update from X7A on whether the Oliver maternal?filter is ready to run.
2. **If ready:** run the filter (X7A may have already produced a list). Then:
   - Annotate Oliver's filtered NPAs with population allele frequency (gnomAD) to remove common paternal alleles.
   - Cross?compare the remaining rare/novel NPAs against the 38 Bowater candidates and the other array families (re?use the proximity+permutation pipeline already built).  
3. **If not ready:** while waiting, you can price out WGS for the Bowater trio (Nebula 30x, ~$200-300/sample), draft a brief plan for Max, and/or finish any polishing the Lottie letter session needs.

---

## OPEN QUESTIONS (still awaiting Max)
- Should we actually order/sequence the Bowater trio? (Max indicated it's the best family and the next logical step.)
- Does the letter?to?Lottie session need any further input from us? (Max must review that letter before it goes.)
- What to do about the Lottie MyHeritage data - keep it for cross?platform validation only, or discard? (Currently it's treated as a separate family entry "bowater_myheritage" in the cross?family analysis.)

---

## KEY PATHS / IDs / COMMANDS
- **Canonical data folder**  
  `C:\Users\maxre\Nextcloud\xg1_data\xg1_fams\20260614_bowater_trio_23andme\`  
- **NPA analysis outputs**  
  `C:\Users\maxre\Nextcloud\xg1_data\xp2_analysis\260713_NPA_Bowater_23andme_trio\`  
- **Scanner script**  
  `C:\claude_base\projects\XG1\xp2_npa\npa_scanner_bowater23_v01.py`  
- **Cross?family + proximity scripts**  
  `C:\claude_base\projects\XG1\xp2_npa\npa_cross_family_v01.py`  
  `C:\claude_base\projects\XG1\xp2_npa\npa_proximity_clusters_v01.py`  
  `C:\claude_base\projects\XG1\xp2_npa\annotate_loci_v01.py`  
- **23andMe login**  
  Email: `max@tamza.com`  
  TOTP secret id: `7772765a-6e05-44ab-9955-b3fa0142a736` (in Bitwarden, pulled via CLI)  
- **Bitwarden CLI session token**  
  `C:\Users\maxre\Nextcloud\zSyncMain\ssh\bw_session.txt`  
- **P5 coordination room**  
  `python C:\claude_base\branch_bulletin\bcast.py room p5 --read`  
- **Oliver/Kenefick WGS source**  
  `C:\claude_base\projects\XG1\kenefick\`  
  (intermediate BAMs on asto, backed up to Centauri until 16:00)

---

## GOTCHAS & DEAD ENDS RULED OUT
- **Lost scanner script** - The original L473 scanner is gone. The re?implementation is the new gold standard for this analysis; all future Bowater work should reference it, not assume a lost script exists.
- **Browser Bitwarden contention** - Do **not** try to open a Playwright browser expecting the Bitwarden extension to be logged in. Instead, pull TOTP codes (and the password) from the command line with `bw` using the session token in `bw_session.txt`. If the vault is locked, `bw unlock` will need the master password - but in most sessions the token file is valid.
- **Father?absent WGS** - Oliver has only mother and son. A simple "child minus mother" NPA list is useless (it's mostly the father's normal alleles). The proper procedure is the maternal?inference filter (check mother's reads + population frequency). That is what X7A is building. Do not bypass it.
- **Old MyHeritage Bowater data** - It was noisy (994 NPAs, ~96% platform noise). It is retained for cross?platform validation of Lottie's candidates only, not as a standalone NPA source. The cross?family script already distinguishes `bowater_23andme` from `bowater_myheritage`.
- **Duplicate folders** - I accidentally created a stray folder under `projects/XG1/bowater`; it was deleted. The only valid place for the trio data is the Nextcloud canonical folder.
- **The `.claude.json` edit** - I initially patched the worktree's Playwright config to point to the Bitwarden launcher, but later reverted it. That was unnecessary; the real cause was profile contention, not missing config. No persistent config change was needed.
