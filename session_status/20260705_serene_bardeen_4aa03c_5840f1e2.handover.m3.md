# Scribe handover - milestone 3 (~235K tokens)
# session: 20260705_serene_bardeen_4aa03c_5840f1e2
# cwd: C:\claude_base\.claude\worktrees\serene-bardeen-4aa03c
# written: 2026-07-05 16:33:51 by deepseek-v4-pro

# HANDOVER: Tamza Trusted Contact Database (b51c session)

## GOAL (in Max's words)

"Your main task is the database. Merge the contacts with Zoom recordings. Keep working on the database until we kind of polish it using LLM and optimizing it. Unclear questions where the matches are questionable, just present them to me so I can review."

**The wider mission:** After the Tamza Zoom club was attacked by impersonators on July 4, 2026, the Zoom link must be kept secret. Max wants a tightly controlled, verified list of regular participants so rotating secret links can be distributed to them automatically. The database of trusted people - with phone numbers - is the foundation for whatever distribution channel comes next (likely Telegram).

---

## DECISIONS MADE + WHY

### 1. SMS to Russia is dead - Telegram is the right distribution channel
A research agent checked 8+ SMS providers against the real regulatory landscape. Two blockers in Russia: an Aug 2025 anti-spam law that blocks all business SMS by default, and a separate policy that blocks any SMS containing a URL as spam. Since the Zoom link IS a URL, no provider can reach Russian phones reliably. Ukraine is "best-effort" with silent drops. Telegram is where the Russian-speaking club already lives - free, no carrier filtering, same behavior across all target countries. Any SMS should only be a fallback for the IL/DE/US minority, using Telnyx (cheapest international).

### 2. Telegram private channel with approve-to-join, NOT a bot with cold messaging
A bot can't cold-message people (they must press "Start" first). Driving Max's own Telegram account via Telethon to bulk-DM invites risks spam-bans and must be paced at a few dozen per day. The simplest model discussed: a private channel where Max approves join requests one-time after a human identity check (voice message, recognize the person). Max didn't commit to building this yet - wanted the database first.

### 3. Per-person unique invite links were discussed but set aside as too complex
Max called the unique-link-per-person + auto-status-dashboard idea "a little bit tricky." Simpler approach (private channel + manual approve) was tabled until the database is ready.

### 4. Phone numbers from Max's Google Contacts are the key identifier
Zoom participant reports give display names (sometimes just first names or Cyrillic). The contacts book (~5,700 entries) is the richest source of phone numbers, which are needed for any Telegram/SMS/WhatsApp reach. Email list is secondary enrichment.

### 5. Latin?Cyrillic transliteration is the hard join problem
Zoom shows "???????????" - contacts store "Lebedinskaya." A simple token match misses these entirely. The fuzzy matcher uses: transliterate everything to Latin, fold similar letters (y/i, z/s, k/c), strip diacritics, and require ?2 matched tokens (first name AND surname) with high similarity (?0.85) to auto-classify. This recovered dozens of real matches that the naive join missed.

### 6. Multi-person Zoom entries must never auto-match
Entries like "Irina Nejdanova & Iouri So" would pick up first-name tokens from entirely unrelated contacts. A guard was added: if the display name contains "&", ",", or " ? ", it's always demoted to REVIEW or UNRESOLVED.

### 7. Division of labor with b51b (parallel session)
b51b owns the Zoom participant list - they pulled 14 months of attendance, ranked by frequency, and are doing the dedup/merge (collapsing name variants like "???" / "????? ???????????" into one person). b51c owns the 3-source JOIN: take b51b's cleaned Zoom list + Max's contacts + the Tamza email list, and produce one unified trusted table. b51b's merges have NOT been folded in yet.

### 8. Short surnames (4 chars like ????, Levi, Gold) are handled, not dropped
Early versions required surname length ?5 to anchor a match, which wrongly excluded real people with short surnames. The final rule uses ?2 matched tokens across the full name, which inherently blocks single-first-name false matches without penalizing short surnames.

---

## CURRENT STATE

**What's built and working:**
- `C:/claude_base/tools/tamza_trusted_list/` - the workspace, committed and pushed to the private repo `maxrempel/claude_base` on master
- `scripts/join_v02_fuzzy.py` - the production-quality fuzzy join script. Reads b51b's 309-person ranked Zoom list (`C:/claude_base/projects/tamza_zoom_attendance/output/attendance_ranked_v01.csv`) and Max's contacts export (`C:/Users/maxre/Nextcloud/zSyncMain/contacts_backup/contacts_20260528.csv`), transliterates, fuzzy-matches, and outputs the merged table.
- Output: `data_work/trusted_join_v03.csv` - the merged master table with these columns: b51b's rank/sessions/Zoom-name, match decision (auto/review/none), matched contact name, phone, email, match score, and which tokens matched.
- Review page: `reports/tamza_trusted_review_v01.html` - a light-theme HTML page with three sections (READY / REVIEW / UNRESOLVED) for Max to visually scan. READY=72 auto-matched people (no action needed), REVIEW=107 ambiguous matches (Max picks the right person or marks as mismatch), UNRESOLVED=130 honest dead-ends.
- PII outputs (CSV with phone numbers) are gitignored. They regenerate from the scripts.
- `README.md` documents the whole pipeline.

**Numbers from the final run:**
- 309 Zoom regulars ingested (from b51b)
- 72 auto-matched - high confidence, phone/email attached
- 107 for Max's review - surname candidate found but ambiguous
- 130 unresolvable: 80 first-name-only Zoom entries (e.g. "Vera", "Inna"), 50 with a surname not found in Max's contacts
- **172 people now have a phone number** in the merged output

**What is NOT yet done:**
- b51b's "same person" merges have not been applied - duplicates like "???" and "????? ???????????" still appear as separate rows and should collapse into one
- The Tamza email list (Google Sheet) was partially read and is messy (bounce-tracking sheet, not a clean mailing list). The reader got truncated at letter "e". Full email enrichment is pending.
- No Telegram channel/bot has been created. Max said "proceed without actually registering the channel."
- Max has not reviewed the 107-person REVIEW list.

---

## EXACT NEXT STEP

**When Max returns:** he needs to review the 107 ambiguous matches in `tamza_trusted_review_v01.html`. For each one, confirm the right contact person or mark as false match. This is the human-in-the-loop polish step he asked for - the LLM got as far as it can, now the questionable cases need his personal knowledge.

**After review is done:** fold in b51b's dedup merges so duplicate name-variants collapse to one row per real person. Then re-run the join against the updated Zoom list.

**Then:** pull the full Tamza email Google Sheet (not truncated) and enrich the table with whatever email addresses the contacts book didn't have. Some regulars may be reachable by email but not phone.

**Final deliverable:** one clean, deduplicated table of verified regulars with at least one reachable contact method (phone or email), ready to be imported as the trusted recipient list for whatever distribution channel Max chooses.

---

## OPEN QUESTIONS STILL AWAITING MAX

1. **Telegram channel or bot?** The design discussion settled on "private channel + manual approve after voice verification" but Max never gave a final go-ahead. The bot-with-allowlist approach is also viable. This decision is needed before any distribution mechanism is built.

2. **What about people Max doesn't have phone numbers for?** ~130 people are in the UNRESOLVED bucket. Some are genuine regulars who just aren't saved in Max's contacts. Should we send them a message (email? existing Telegram group?) asking them to provide their contact info? Or leave them out and they'll notice they're not getting the secret link?

3. **The 107 REVIEW-list names** - Max needs to go through them. Many are probably correct matches; some are genuinely ambiguous (two people with the same uncommon name, or a name that exists for two different people in different countries).

4. **How often does the link rotate?** The newsletter says "we will regularly change it." The sending script needs to know the cadence.

5. **Who else besides Max can approve people / manage the list?** Co-organizers (Natasha Grinbaum-Smirnos, Sasha Noskov, Liya Chernyakova, etc.) might need access.

---

## KEY FILE PATHS AND IDS

| Purpose | Path |
|---|---|
| Workspace root | `C:/claude_base/tools/tamza_trusted_list/` |
| Main fuzzy join script | `C:/claude_base/tools/tamza_trusted_list/scripts/join_v02_fuzzy.py` |
| HTML report generator | `C:/claude_base/tools/tamza_trusted_list/scripts/make_report_v01.py` |
| Merged output CSV (PII-gitignored) | `C:/claude_base/tools/tamza_trusted_list/data_work/trusted_join_v03.csv` |
| Review page for Max | `C:/claude_base/tools/tamza_trusted_list/reports/tamza_trusted_review_v01.html` |
| b51b's Zoom attendance list (input) | `C:/claude_base/projects/tamza_zoom_attendance/output/attendance_ranked_v01.csv` |
| b51b's build script (normalization key) | `C:/claude_base/projects/tamza_zoom_attendance/scripts/build_db_v01.py` |
| Max's Google Contacts export | `C:/Users/maxre/Nextcloud/zSyncMain/contacts_backup/contacts_20260528.csv` |
| Branch bulletin board | `C:/claude_base/branch_bulletin/bcast.py` |
| Work log | `C:/claude_base/compaction_kb/scripts/worklog.py` |

**Key IDs:**
- b51c - this session (trusted database join)
- b51b - parallel session (Zoom participant dedup)
- Zoom account: "Tamza zoom 202206" in Bitwarden, username `admin@tamza.com`
- Secret Zoom link from newsletter: Meeting ID `873 4648 6242`, Passcode `44`, URL `https://us06web.zoom.us/j/87346486242?pwd=PlqZJGDFsLIU8Xq4T0OEueN8ELokgB.1`
- Max's contact number for link requests: +1 (585) 705-1400
- Tamza PayPal: `pay@tamza.com`
- Newsletter subscription: `admin@tamza.com`
- Tamza YouTube: `https://youtube.com/@Tamza`
- Live stream: `https://www.youtube.com/@prostoproverka/streams`

---

## GOTCHAS AND DEAD ENDS RULED OUT

**SMS-to-Russia is dead.** A thorough 8-provider comparison confirmed: Russia's Aug 2025 anti-spam law blocks all A2P SMS, and separately blocks any SMS containing a URL. Since the secret Zoom link IS a URL, no provider can deliver it to Russian phones. Do not revisit SMS as a primary channel - it only works for IL/DE/US, and even then only as a fallback.

**Simple name-matching misses real people.** The first attempt (exact token match) produced only 67 matches out of 309. The Latin?Cyrillic gap is real - "???????????" ? "lebedinskaa" (transliterated) ? "Lebedinskaya" (how Max saved the contact). The fuzzy matcher with digraph folding recovered these.

**Bots cannot cold-message on Telegram.** A Telegram bot can only message people who have pressed "Start" first. To reach people proactively, the only option is driving Max's own Telegram account via Telethon/MTProto - which is riskier (spam-ban) and must be paced.

**First-name-only Zoom entries are unresolvable.** About 80 of the 309 regulars only showed a first name on Zoom - "Vera," "Inna," "Svetlana," etc. Without a surname or other identifier, the join cannot disambiguate these from Max's many contacts sharing those first names. These are honest dead-ends that need human outreach (Max asking them directly for their full name or contact info).

**Multi-person Zoom names break auto-matching.** If two people share one Zoom display name ("Irina Nejdanova & Iouri So"), first-name tokens would match unrelated contacts. The guard that demotes any entry containing "&", ",", or " ? " to REVIEW fixed this.

**Short surnames must not be penalized.** Early versions required surname length ?5 to anchor a match, which killed matches for people like "????? ????" (surname = 4 chars). The final rule (?2 matched tokens, both first name and surname must match) handles short surnames correctly.

**The
