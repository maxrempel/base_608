# Scribe handover - milestone 4 (~309K tokens)
# session: 20260706_objective_faraday_7e53f8_edcd05fb
# cwd: C:\claude_base\.claude\worktrees\objective-faraday-7e53f8
# written: 2026-07-06 09:28:17 by deepseek-v4-pro

# HANDOVER - Tamza Zoom Attendance + Site Update Session

---

## GOAL (in Max's words)

Max has two intertwined goals:

1. **"???????? ???? ?????"** - update tamza.com to hide the Zoom link behind a contact-request wall, because on 4 July 2026 the club was attacked by hooligans (?????? ??) who joined with fake names/cameras-off and disrupted meetings. The secret link should only go to known, trusted people.

2. **Build a trusted regulars list** - pull Zoom attendance history, match names against Max's Google Contacts and the Tamza email-list spreadsheet, so that when the Zoom link rotates, it can be sent automatically to verified regulars (or at least produce a reviewable list of who's trusted and who's missing contact info).

---

## DECISIONS MADE + WHY

### 1. Site update: what to write instead of the direct Zoom link
- **Decision:** Replace every "????? ? ?????" button with a message saying the link is now secret due to the attack, and instruct people to contact Max Rempel (WhatsApp/Telegram/SMS, +1 585-705-1400) or subscribe via admin@tamza.com to get it.
- **Why:** Direct link on a public site is exactly how the attackers found it. The link must only circulate privately.
- **Status:** TEXT WAS DRAFTED BUT NEVER APPLIED TO THE SITE. The entire site-edit task got sidelined by the attendance-data rabbit hole.

### 2. Bitwarden in Playwright: accepted it's broken for now
- After ~5 rounds of Max insisting the Bitwarden icon is not visible in the Playwright Chromium, Claude accepted the user's reality (even though CLI checks showed the extension loaded). 
- **Decision:** Another branch will fix the Playwright/Bitwarden integration properly. For this session, Claude used the Bitwarden CLI to fetch the Zoom password directly.
- **Why:** Arguing about it was burning time. The CLI path unblocked the real work.

### 3. Zoom login method
- **Credentials:** "Tamza zoom 202206" entry in Bitwarden - username `admin@tamza.com`, password retrieved via `bw get password`.
- **Why:** The Bitwarden browser extension wasn't usable, so CLI was the only path.

### 4. Attendance crawl scope: 14 months, not 2-3 years
- **Decision:** Crawl everything available in the Zoom usage reports. It turned out to be May 2025 - July 2026 (14 months).
- **Why:** Zoom simply has no data before May 2025 for this account (either retention limit, or the club used a different Zoom account earlier). Max accepted this: "14 months is perfect. That's good enough."

### 5. Data architecture: crawl ? raw JSON ? ranked CSV ? dedup canonical list
- **Decision:** Three chunk files per ~6-month window, saved to the worktree's `zoom_data/` folder. Then a Python script builds a ranked attendance DB, then a dedup script merges surname-based variants into canonical people.
- **Why:** Resumable, inspectable at each stage, and the raw data is preserved if dedup logic needs re-running.

### 6. Branch split with B51C
- **Decision:** B51B (this session) owns **Zoom dedup and merge review**. B51C owns the **3-source join** (Zoom canonical list ? Tamza email spreadsheet ? Max's Google Contacts ? one enriched table with email/phone).
- **Why:** Parallelise the work. B51C can wire the join infrastructure against the current CSV while B51B refines the dedup with Max's manual review.

### 7. PII protection
- Files containing real names are gitignored in `projects/tamza_zoom_attendance/.gitignore`. A project README was written.

---

## CURRENT STATE

### ? DONE
- **Zoom attendance database built:** 126 sessions, 309 raw name-clusters, deduped to **251 canonical people**, ranked by session count, saved at `C:\claude_base\projects\tamza_zoom_attendance\output\`.
- **Top regulars identified:** Roland Kolhely (118 sessions), ?????? ??????? (107), Natalya Grinbaum (96), Diana Peltz (93), ???????? ?????? (80), ????? ???? (74), etc.
- **Confident surname-based merges applied** (e.g. "???? ??????" + "???????? ??????" + "?????? ?????? ????????" ? one person with 80 sessions).
- **Canonical deduped list + variant?person_key map** handed to B51C via bulletin board post (local disk, not committed - PII).
- **B51C has already produced a first-cut 3-source join** (72 auto-matches with phone/email attached, pushed to master at `tools/tamza_trusted_list/`). It posted results and is waiting for B51B's refined dedup keys.

### ?? IN FLIGHT (blocked on Max)
- **Merge review:** Claude generated a 2-tier review sheet (`merge_review_v02.html`):
  - **Tier A - Confident** (shared surname): ~15 merges, including Natalya Grinbaum variants, ?????? ???????, ???????? ??????, ?????? ???????, Vladimir & Mila Movshits (couple?), Max Gold, etc. One flagged ambiguity: ??????? ?????????? = ??????? ?????? (different surnames - probably NOT the same person).
  - **Tier B - Ambiguous first-name-only:** Vera (71 sessions), Inna (59), Svetlana (48), Regina (20), liya (19), victor (13), and ~10 more low-count ones. These need Max to say whether each is a single person (e.g. Vera = Vera Rechter, liya = Liya Chernyakova) or a mix of different people.

### ? NOT DONE
- **Tamza.com secret-link page edit** - the original task. Text was drafted in chat but never applied to any site files. Completely sidelined.
- **Year-long participant pull from other meetings** - only the main July 5 session was manually reviewed for contacts matching. The full 14-month crawl captured all raw data, but the contact-matching work (B51C's job) is based on the canonical list, not individual sessions.

---

## EXACT NEXT STEP

1. **IMMEDIATE (unblocks everything):** Max answers the merge-review questions:
   - Are **Vera (71), Inna (59), Svetlana (48), Regina (20), liya (19), victor (13)** each a single person? ("Yes all" or flag exceptions.)
   - Is **??????? ?????????? = ??????? ??????** the same person? (Different surnames - likely no.)
   - Should couples (Movshits, Rechter, Katsir) count as **one household entry** or two separate people?
   - Any other merges in Tier A that look wrong?

2. **After Max's answers:** B51B regenerates the canonical deduped list (v02) and hands it to B51C. B51C then produces the final enriched trusted list (name ? email/phone).

3. **Then, the forgotten task:** Apply the secret-link text to tamza.com (replace all "????? ? ?????" buttons). The drafted text is in the transcript - it's ready to go, just needs to be edited into the site files.

---

## OPEN QUESTIONS AWAITING MAX

1. **Merge review answers** (see above - Vera/Inna/Svetlana/Regina/liya/victor, ??????????/??????, couples).
2. **Where are the tamza.com site files?** The transcript never navigated to them. Are they in this repo, on a server, or in a separate project? (Claude needs a path or URL to edit.)
3. **The secret-link text** - is the draft from the chat acceptable as-is, or does Max want to wordsmith it before it goes live?

---

## KEY PATHS, IDs, NAMES

| What | Path / Value |
|---|---|
| **Attendance raw data (3 chunks)** | `C:\claude_base\.claude\worktrees\objective-faraday-7e53f8\zoom_data\chunk_*.json` |
| **Ranked CSV (309 raw)** | `C:\claude_base\projects\tamza_zoom_attendance\output\attendance_ranked_v01.csv` |
| **Canonical deduped CSV (251 people)** | `C:\claude_base\projects\tamza_zoom_attendance\output\canonical_people_v01.csv` |
| **Variant?person_key map** | `C:\claude_base\projects\tamza_zoom_attendance\output\variant_to_person_v01.csv` |
| **Merge review sheet** | `C:\claude_base\projects\tamza_zoom_attendance\output\merge_review_v02.html` |
| **Scripts** | `C:\claude_base\projects\tamza_zoom_attendance\scripts\` |
| **Project README** | `C:\claude_base\projects\tamza_zoom_attendance\README_tomemex.md` |
| **Tamza email spreadsheet** | `https://docs.google.com/spreadsheets/d/1qnWGKHzUtbezjsHo8L2580MPDIiVMVSJs_f-MMuIavg/edit` |
| **Contacts backup** | `C:\Users\maxre\Nextcloud\zSyncMain\contacts_backup\contacts_20260528.csv` |
| **Zoom account** | admin@tamza.com (Bitwarden entry: "Tamza zoom 202206") |
| **Current Zoom link (secret)** | Meeting ID 873 4648 6242, Passcode 44, pwd=PlqZJGDFsLIU8Xq4T0OEueN8ELokgB.1 |
| **Old Zoom link (compromised)** | Meeting ID 828 3716 6247, Passcode 145281 |
| **B51C's first-cut join output** | `tools/tamza_trusted_list/` (pushed to master) |
| **Bulletin board** | `C:\claude_base\branch_bulletin\bcast.py` |

---

## GOTCHAS & DEAD ENDS

1. **Bitwarden-in-Playwright is a known broken state.** The extension is installed but shows the "Log in / Create account" intro screen - it's logged out because the Playwright MCP opens `Profile 1` instead of `Default` where the vault login lives. Any session that needs the Bitwarden UI must either (a) fix the profile path, or (b) use the CLI. A separate branch is supposed to handle this. **Do not waste time re-litigating whether Bitwarden is "there" - Max sees no icon, that's the reality.**

2. **Zoom participant reports give NAMES but NOT emails for guests.** Only the host account (admin@tamza.com) shows an email in the CSV export. Everyone else joins as a guest with a blank email field. So the Zoom data alone cannot produce a contact list - it MUST be joined against the email spreadsheet and/or Google Contacts.

3. **Zoom display names are messy.** People appear as "07 Svetlana", "02 ????? ????", "Inna (?????????)", "Cell Natalya Grinbaum", "iPhone", "??????" etc. The dedup script strips numeric prefixes and parentheticals, but first-name-only entries (Vera, Inna, Svetlana, Regina) cannot be auto-merged - they're genuinely ambiguous and need a human to say "yes, that's always the same Vera."

4. **Zoom history goes back only to May 2025.** Crawling Feb-Apr 2025 returned zero meetings. This is either Zoom's retention policy or the club used a different account before May 2025. No workaround - 14 months is the ceiling.

5. **The original tamza.com site edit was NEVER done.** The entire session got absorbed by the attendance-data project. The drafted replacement text exists in the transcript but was never applied to any HTML/PHP files. A cold session resuming this handover must not forget that the site still has the old public Zoom link live.

6. **Profile-lock contention between Playwright sessions.** The persistent `playwright_profile` allows only one Chromium at a time. When multiple Claude sessions try to use Playwright, the second one gets bounced to an isolated (extension-less) profile. B51B released the lock after the crawl finished, so it's free now - but this will recur in any multi-session workflow. The proper fix (profile-copy per session, or auto-clear stale locks) belongs to the separate Bitwarden-fix branch.
