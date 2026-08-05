# Scribe handover - milestone 4 (~303K tokens)
# session: 20260705_serene_bardeen_4aa03c_5840f1e2
# cwd: C:\claude_base\.claude\worktrees\serene-bardeen-4aa03c
# written: 2026-07-05 17:06:55 by deepseek-v4-pro

# HANDOVER - Tamza Trusted-List Database Build (b51c)

---

## GOAL (in Max's words)

Max needs a **tightly controlled, verified list of trusted Tamza regulars** to distribute a rotating secret Zoom link. The Tamza club was attacked by impersonators ("agents of GB") on July 4, 2026 - people joining Zoom with fake names and cameras off, pretending to be real members. The link must now be secret and sent only to verified people. Max wants to **merge his address book, email mailing list, and actual Zoom participant history into one curated database** - flagging ambiguous name-matches for his review, but aggressively merging where reasonable. The final list should be ~100 real people (50 regulars + ~50 guests).

---

## DECISIONS MADE + WHY

### 1. SMS is dead for Russia - Telegram is the delivery channel
- **Finding:** Russia's Aug 2025 anti-spam law blocks all A2P (business) SMS, AND Russia specifically blocks any SMS containing a URL as spam. The message IS a URL. No US provider can bypass this.
- **Ukraine:** works "best-effort" but with silent drops. Israel/Germany/US: fine.
- **Decision:** Primary delivery = **Telegram** (private channel or bot with approved list). SMS fallback (Telnyx) only for IL/DE/US stragglers not on Telegram.
- **Cost:** Telegram = free. SMS backup = a few dollars/month for ~50-80 messages.

### 2. Private Telegram Channel with approve-to-join (not a bot, not a group)
- **Why not a bot:** a bot can't cold-message; every person must tap "Start" first. This is manageable but adds friction.
- **Why not a group:** impersonators could join.
- **Chosen design:** One private channel, approve-to-join ON. The channel membership IS the verified list. Max (or co-orgs) verify a person once (voice message, recognition), send them the invite link, approve them - done forever. Link rotates? Post once in the channel, all members see it.
- **Reality accepted:** any trusted member could forward the link. No technical fix for that.

### 3. Database consolidation strategy: merge-biased
- **Max's directive:** "Merging two different people is not a big deal. Non-merging is much worse. Give me your best version of preferred mergers."
- **Approach:** Fuzzy surname-anchored matching with phonetic folding for Latin?Cyrillic. When in doubt, attach a best-guess contact and flag it yellow for review - never leave a regular unmatched when there's a plausible candidate.

### 4. Precision over recall for the secret list
- **Key realization (from close-look review):** a wrong phone number is worse than none for a secret link. Common first names (?????????, Vladimir, Nikolai, Irene, ?????) were falsely matching different people - these are now filtered out and the entries show as honestly "unmatched" rather than wrong-attached.

### 5. Sources used: 3-way join
- **Primary anchor:** b51b's 309-person ranked Zoom attendance list (14 months of meetings)
- **Phones + emails from:** Max's Google Contacts export (~5,700 contacts, file from 2026-05-28)
- **Emails additionally from:** Tamza mailing list Google Sheet (decoded from base64 export - 842 emails, 311 name?email pairs recovered)
- **Division of labor with b51b:** b51b owns Zoom deduplication (309 entries ? 251 real people); b51c owns the cross-source join and contact attachment.

---

## CURRENT STATE

**251 real people in the database**, sorted by Zoom attendance. Each person has:

| Category | Count | Meaning |
|---|---|---|
| **Confident (green)** | 54 | High-confidence match with phone/email - surname + first name both match. Ready to invite. |
| **Best-guess (yellow)** | 100 | Plausible match but flagged - needs Max's review. Shows alternate candidates and match basis (surname vs first-name). |
| **Unmatched (red)** | 97 | No contact found - mostly first-name-only Zoom entries ("Vera", "Inna", "Svetlana"), junk names ("Samsung SM-A165F", "Zoom user"), or people genuinely not in Max's contacts/email list. |

- **154 of 251 have a phone or email** (61% coverage)
- **Of the top-100 attenders, 72 are reachable** (72% coverage)
- **Work is committed and pushed to master** on the private repo
- **Coordinated with b51b** via branch bulletin board; they know about my email index

---

## EXACT NEXT STEP

**Max reviews the yellow "best-guess" entries** in the HTML report and corrects them. The report is at:

```
C:\claude_base\tools\tamza_trusted_list\reports\tamza_consolidated_v01.html
```

It's a light-theme page with three sections (CONFIDENT / REVIEW / UNMATCHED), sorted by attendance. Each yellow row shows:
- Zoom display name
- Sessions attended
- The best-guess contact (name, phone, email)
- Alternate candidates found
- Match basis (surname vs first-name)

**After Max's review**, the corrections get folded back in, producing a clean trusted list. Then:
1. Create the private Telegram channel (not done yet - deliberately held until Max approves the list)
2. Generate invite links per person
3. Deliver invites through existing contacts
4. Post the first secret Zoom link

**For the 97 unmatched:** Facebook/Messenger is the next channel to try. Many of these are people Max knows but whose contact info isn't in his address book under a recognizable name.

---

## OPEN QUESTIONS AWAITING MAX

1. **The yellow guesses need human ground truth.** Max knows these people. Examples: "?????? ???????" ? matched to "Marina Belkina" - is this correct? "?????? ??????? ????????" ? matched to "?????? ????????" - correct person?

2. **Facebook/Messenger for the ~97 unmatched.** Should b51c tackle scraping Facebook friends / Messenger contacts as an additional data source?

3. **The channel setup.** Does Max want to create the private Telegram channel now (even without final list), or wait until the list is fully curated?

4. **Co-organizers as approvers.** Should other orgs (?????? ????????-???????, ???? ??????, etc.) also have approve rights in the channel, or only Max?

---

## KEY FILE PATHS

| What | Path |
|---|---|
| **Consolidation script** | `C:\claude_base\tools\tamza_trusted_list\scripts\consolidate_v01.py` |
| **Email index builder** | `C:\claude_base\tools\tamza_trusted_list\scripts\email_index_v01.py` |
| **Fuzzy join (v02, still useful)** | `C:\claude_base\tools\tamza_trusted_list\scripts\join_v02_fuzzy.py` |
| **HTML review report** | `C:\claude_base\tools\tamza_trusted_list\reports\tamza_consolidated_v01.html` |
| **Consolidated CSV (working data)** | `C:\claude_base\tools\tamza_trusted_list\data_work\tamza_consolidated_v01.csv` |
| **Contacts backup (source)** | `C:\Users\maxre\Nextcloud\zSyncMain\contacts_backup\contacts_20260528.csv` |
| **b51b's dedup output** | `C:\claude_base\projects\tamza_zoom_attendance\output\zoom_canonical_v01.csv` |
| **b51b's ranked attendance** | `C:\claude_base\projects\tamza_zoom_attendance\output\attendance_ranked_v01.csv` |
| **Mailing list decoded** | `C:\claude_base\tools\tamza_trusted_list\data_raw\maillist_decoded.tsv` |
| **Email name?addr index** | `C:\claude_base\tools\tamza_trusted_list\data_work\email_name_to_addr.csv` |
| **Workspace root** | `C:\claude_base\tools\tamza_trusted_list\` |
| **Branch bulletin board** | `C:\claude_base\branch_bulletin\bcast.py` |

## KEY IDs & NAMES

- **Branch name:** b51c (Timmy)
- **Peer branch:** b51b (Jimmy) - owns Zoom dedup
- **Bitwarden entry:** "Tamza zoom 202206" - username admin@tamza.com (Zoom admin account)
- **Zoom meeting ID:** 873 4648 6242, passcode 44
- **Max's phone for contacts:** +1 (585) 705-1400
- **Tamza email:** admin@tamza.com
- **PayPal for meds:** pay@tamza.com
- **Tamza site:** tamza.com
- **Bitwarden session (may be stale):** `3Q1LuTvallMTPux+V2rK2NippR44lr3txSZTNTTeCs3V5QD9ZqfnR7EOQrdXpi/31nCf7MOrQ2N1FIS9jmU95g==`

---

## GOTCHAS & RULED-OUT APPROACHES

### Gotchas
1. **Latin?Cyrillic transliteration is the #1 matching problem.** "???????????" ? "Lebedinskaya" vs "Lebedinskaa" - the fuzzy matcher handles this but needs tuning per name.
2. **Common first names are NOT surname anchors.** ?????????, Vladimir, Nikolai, Irene, ?????, etc. - the filter blocks using a shared long first name as if it were a surname match. This is correct behavior.
3. **Multi-person Zoom display names** ("Irina Nejdanova & Iouri So") are never auto-matched - too risky to guess which person the contact matches.
4. **Junk contacts pollute matching.** "License #...", "Regina Estimate 20230130", "Nikolai Painter in Florida" - these are filtered out by the junk-contact detector.
5. **PII is gitignored.** The `data_work/` directory (containing phones and emails) is in `.gitignore`. Scripts regenerate outputs from source data. The repo is private, but this is still good hygiene.
6. **The email list required base64 decoding** - the Google Sheets MCP tool returned base64-encoded content, not plain text. The script handles this.

### Ruled Out
1. **SMS to Russia** - completely dead due to carrier-level URL blocking and Aug 2025 anti-spam law. No US provider can bypass it.
2. **SMS for the whole list** - researched Twilio, Telnyx, Plivo, Vonage, MessageBird. All blocked in Russia. Ukraine is "best-effort." Not viable as primary channel.
3. **WhatsApp API** - needs pre-approved templates, business account, opt-in. Too heavy for this use case.
4. **Facebook Messenger automation** - breaks ToS for personal accounts; effectively manual.
5. **Bot cold-messaging** - Telegram bots cannot initiate conversations; each user must press Start first.
6. **Bulk phone-number import into Telegram channel** - Telegram blocks this (privacy + anti-spam). People must join via invite link individually.
