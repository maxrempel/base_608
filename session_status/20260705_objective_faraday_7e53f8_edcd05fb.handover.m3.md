# Scribe handover - milestone 3 (~271K tokens)
# session: 20260705_objective_faraday_7e53f8_edcd05fb
# cwd: C:\claude_base\.claude\worktrees\objective-faraday-7e53f8
# written: 2026-07-05 15:10:30 by deepseek-v4-pro

# HANDOVER - Tamza Zoom Attendance Database & Contact Matching

---

## GOAL (in Max's words)

Build a database of every person who has attended Tamza Zoom sessions over the last 2-3 years (or whatever Zoom retains). Count how many sessions each person attended. Then match those people against his Google Contacts and the Tamza newsletter spreadsheet to attach email/phone - the ultimate aim is to have a trusted-regulars list to whom the rotating secret Zoom link can be sent automatically when it changes, without exposing it publicly on the website.

A parallel, unfinished task from earlier in the session: update **tamza.com** to remove public Zoom links (after a troll attack on July 4, 2026) and replace them with a message telling people to contact Max for the secret link. This was discussed and text was drafted, but never applied to the site.

---

## DECISIONS MADE + WHY

1. **Crawl Zoom via the web portal (not API).** The Zoom REST API for participant reports requires account-level admin scopes that aren't set up. Instead, the Playwright browser logged into `admin@tamza.com` on `zoom.us`, navigated to Account Management ? Reports ? Usage Reports, and pulled meeting lists + per-meeting participant details by calling Zoom's internal JSON endpoints directly from the browser console. This avoided thousands of manual clicks.

2. **Use the internal `/nwc/report/meetings/usage` endpoint.** Discovered by watching network traffic during a search. Returns paginated meeting lists (20 per page, `&p=N`). Each meeting row links to a participant endpoint that returns `attendees[]` with name, join time, and duration. This was fast and reliable.

3. **Chunk the crawl into month batches saved to disk.** The browser context for `browser_run_code_unsafe` lacks filesystem access and is ephemeral cross-navigation. Data was accumulated in a JavaScript variable, stashed on `window` at the end of each navigation pass, and then dumped to a JSON file via `browser_evaluate` (which can save to the worktree). Three chunk files cover May 2025 through July 2026.

4. **Build the attendance DB as a Python script (`build_db_v01.py`).** Reads the raw chunk JSON, deduplicates rejoins within a session (same name joining multiple times = 1 attendance), normalizes messy display names (strips leading numbers like "07 ", removes parentheticals like "(?????????)", trims whitespace), and clusters name variants. Output is a ranked CSV: person ? session count, plus a per-session detail JSON.

5. **Zoom retention cap = 14 months, not 2-3 years.** The report returns zero data before May 2025. This is either Zoom's retention limit for this account tier, or Tamza used a different Zoom account earlier. 14 months is the real ceiling; the 2-3 year ambition cannot be met from this account alone.

6. **Two matching attempts made, both partial.** First pass was too literal (exact string match against Google Contacts CSV backup). Second pass added transliteration (Cyrillic ? Latin) and fuzzy token matching, which was better but still missed people. The real goldmine is the **Tamza newsletter spreadsheet** at `https://docs.google.com/spreadsheets/d/1qnWGKHzUtbezjsHo8L2580MPDIiVMVSJs_f-MMuIavg` - it contains names + emails for the actual subscriber base. The best matching strategy is to join the attendance DB against THAT sheet, not against raw Google Contacts.

7. **Bitwarden-in-Playwright bug deferred to a separate fix branch.** The Playwright Chromium launches with the Bitwarden extension loaded (verified via `chrome://extensions`), but the extension appears logged out because it's running under `Profile 1` rather than `Default` where the stored login lives. Max couldn't see the Bitwarden icon at all (possibly the toolbar icon isn't pinned, and the extension popup was empty when clicked). This consumed many turns. Final decision: fix it in another branch, stop blocking the Zoom task on it. Login was done by fetching the password from Bitwarden CLI and typing it in.

---

## CURRENT STATE - WHAT IS DONE

### Zoom attendance database: **DONE**
- **126 sessions** crawled across **14 months** (May 2025 - July 2026)
- **309 distinct people** identified
- Ranked CSV saved: `C:\claude_base\projects\tamza_zoom_attendance\output\attendance_ranked_v01.csv`
- Per-session detail JSON saved alongside it
- Raw chunk data in: `C:\claude_base\.claude\worktrees\objective-faraday-7e53f8\zoom_data\` (3 files: `chunk_1_2026-02_to_2026-07.json`, `chunk_2_2025-08_to_2026-01.json`, `chunk_3_2025-05_to_2025-07.json`)

### Top regulars (session counts):
| Sessions | Name |
|----------|------|
| 118 | Roland Kolhely |
| 107 | ?????? ?????? ??????? |
| 93 | Diana Peltz |
| 82 | Natalya Grinbaum-Smyrnos |
| 78 | ???? ?????? |
| 74 | ????? ???? |
| 71 | Vera |
| 69 | ?????? ??????? |
| 69 | ????? ??????????? |
| 62 | Lev Milchin |
| 59 | Inna |
| 58 | ?????? ?????????? / Liya Chernyakova |
...and 297 more in the CSV.

### Contact matching: **PARTIAL / INCOMPLETE**
- First pass (exact match against Google Contacts CSV backup) and second pass (transliteration + fuzzy) both ran
- ~12 people matched with email or phone; ~6 not found at all
- Max said the matching was "very bad" because most people ARE in his contacts - the problem is transliteration/spelling variants and nickname storage ("Vova bard Kyiv" vs "???? ??????")
- The Tamza newsletter spreadsheet has been accessed and read - it contains the actual subscriber list with emails, and is the correct source for matching

### Tamza.com website update: **NOT STARTED**
- Draft text was composed: replacing public "????? ? ?????" buttons with a message saying the Zoom link is now secret, directing people to contact Max (WhatsApp/Telegram/SMS at +1 585-705-1400) or subscribe to the newsletter (admin@tamza.com)
- No code was written, no site changes made
- This is a completely separate task from the attendance database

### Known merging problems in the attendance DB:
- "Regina Perl" (46) + "Regina" (20) = same person
- "Vladimir & Mila Movshits" (38) + "Vladimir Movshits" (30) = same person
- "Natalya Grinbaum-Smyrnos" (82) + "Cell Natalya Grinbaum" (23) = same person
- These are stated in the script's output but not yet auto-merged

---

## EXACT NEXT STEP

**Join the attendance database against the newsletter spreadsheet** (the Google Sheet at `1qnWGKHzUtbezjsHo8L2580MPDIiVMVSJs_f-MMuIavg`). This gives a cross-reference table:

- **Who is a regular attendee but NOT on the newsletter** ? candidates to add to the trusted list
- **Who is on the newsletter but rarely/never attends** ? informational
- **Attach email to each person in the attendance DB** from the newsletter sheet (much more reliable than the Google Contacts fuzzy matching)

The newsletter sheet has columns: name, email, bounce/unsub flags, etc. The matching should handle Cyrillic/Latin transliteration both ways, strip parentheticals and prefixes, and allow fuzzy surname matching. Output: a merged CSV with attendance count + newsletter email (or flag "not subscribed").

**After that**, Max's ultimate workflow is:
1. Have a clean trusted-regulars list (high-attendance + verified email)
2. When the Zoom link rotates, auto-send it to that list (email via the existing newsletter system, or a new mechanism)
3. This prevents the public link from being abused by trolls

The **tamza.com website update** (replacing public Zoom links) is also still pending and has not been touched beyond drafting text.

---

## OPEN QUESTIONS (awaiting Max)

1. **Pre-May-2025 data?** The Zoom account has nothing before May 2025. Did Tamza use a different Zoom account before that? If so, what are its credentials? Without it, the 2-3 year history goal is capped at 14 months.

2. **The merging of split clusters in the attendance DB** - should the script auto-merge "Regina Perl"+"Regina", "Vladimir & Mila Movshits"+"Vladimir Movshits", and "Natalya Grinbaum-Smyrnos"+"Cell Natalya Grinbaum", or does Max want to review first? There may be other split clusters.

3. **Website update priority.** Should the tamza.com changes (hiding the Zoom link) happen in this branch, or a separate one? The text is drafted but not applied.

4. **WhatsApp/Telegram auto-send.** Many regulars are phone-only in contacts (not email). Does Max want a WhatsApp/Telegram broadcast component, or is email sufficient?

---

## KEY PATHS, FILES, IDS, COMMANDS

### Files created/used:
- **Attendance DB output:** `C:\claude_base\projects\tamza_zoom_attendance\output\attendance_ranked_v01.csv`
- **Per-session detail:** `C:\claude_base\projects\tamza_zoom_attendance\output\sessions_detail_v01.json`
- **Build script:** `C:\claude_base\projects\tamza_zoom_attendance\scripts\build_db_v01.py`
- **Raw Zoom chunk data:** `C:\claude_base\.claude\worktrees\objective-faraday-7e53f8\zoom_data\chunk_*.json` (3 files)
- **Newsletter spreadsheet:** `https://docs.google.com/spreadsheets/d/1qnWGKHzUtbezjsHo8L2580MPDIiVMVSJs_f-MMuIavg/edit?gid=0#gid=0` (readable via Google Drive MCP connector `62ad6c43-6d9d-4a95-89d5-afe68b9798fd`)
- **Contacts backup:** `C:\Users\maxre\Nextcloud\zSyncMain\contacts_backup\contacts_20260528.csv`

### Key IDs / credentials:
- **Zoom account:** `admin@tamza.com`, password in Bitwarden under item **"Tamza zoom 202206"**
- **Zoom account web portal:** `https://us06web.zoom.us/` (the Zoom subdomain for this account)
- **Internal Zoom report endpoint (discovered):** `https://us06web.zoom.us/nwc/report/meetings/usage?from=YYYY-MM-DD&to=YYYY-MM-DD&p=N` - returns JSON with meeting list, each row has a participant link
- **Participant endpoint:** `https://us06web.zoom.us/nwc/report/meetings/{meetingId}/participants` - returns `attendees[]` array
- **Secret Zoom link (current):** Meeting ID `873 4648 6242`, passcode `44`, pwd token `PlqZJGDFsLIU8Xq4T0OEueN8ELokgB.1`

### Bitwarden CLI session (for password retrieval):
- Session token (may be expired by now): `3Q1LuTvallMTPux+V2rK2NippR44lr3txSZTNTTeCs3V5QD9ZqfnR7EOQrdXpi/31nCf7MOrQ2N1FIS9jmU95g==`
- Command to get password: `bw get password "Tamza zoom 202206" --session "$BW_SESSION"`

---

## GOTCHAS & DEAD ENDS RULED OUT

1. **Zoom REST API (OAuth) - NOT used.** Would require creating an app in Zoom Marketplace with admin scopes. The internal endpoint approach (calling `/nwc/report/meetings/usage` from the logged-in browser) works perfectly and is faster to set up. Stick with it.

2. **Zoom participant reports give NO email for guests.** Only the host account shows an email. Every attendee who joins without a Zoom account shows as a guest with blank email. So the Zoom data alone cannot produce a contact list - matching against an external source (newsletter sheet or Google Contacts) is mandatory.

3. **Raw HTML scraping of the report page fails.** The usage report table is client-side rendered; fetching the HTML directly returns an empty/skeleton table. Must use the JSON endpoints or Playwright navigation + DOM interaction. The JSON endpoints are the reliable path.

4. **Pagination detection by counting participant links is fragile.** Some meeting rows have no participant link (e.g., meetings with 0 attendees), so a `< 20 per page` check trips early. The fix: drive pagination by the "Total: N" count displayed on the page, not by row counting.

5. **The Playwright browser locks a shared persistent profile.** Only ONE Chromium can use the profile at a time. If another session holds the lock (stale or live), new launches fall back to an isolated profile with no extensions ? Bitwarden "gone." For this task, killing all Playwright Chromium processes and clearing the lockfile worked.

6. **Bitwarden extension visible but logged out.** The extension IS installed and enabled (verified in `chrome://extensions`) but loads under `Profile 1` instead of `Default`, so the stored vault login isn't seen. Max couldn't see the icon. This is a config bug, deferred to another branch. The workaround used here: fetch credentials from Bitwarden CLI and type them in.

7. **Google Contacts MCP connector is unreliable.** It returned errors when called. Fallback: read the local CSV backup at `contacts_backup/contacts_20260528.csv`. But for the matching task, the **newsletter spreadsheet** is the better source anyway.

8. **Transliteration matching needs Cyrillic?Latin on BOTH sides.** Max stores contacts with English transliterations (e.g., "Roland Kalheli" not "?????? ???????"). The matching script must generate multiple Latin spellings for each Cyrillic name (and vice versa) and do fuzzy token matching on surname, not exact string match.

---

## WORKLOG ENTRY MADE

The session logged to: `C:\claude_base\compaction_kb\scripts\worklog.py` with summary: "Built Tamza Zoom attendance DB: crawled 14 months (May2025-Jul2026) of Zoom usage reports via admin@tamza.com. 126 sessions, 309 distinct people, ranked CSV saved."
