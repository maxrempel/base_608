# Scribe handover - milestone 5 (~375K tokens)
# session: 20260706_serene_bardeen_4aa03c_5840f1e2
# cwd: C:\claude_base\.claude\worktrees\serene-bardeen-4aa03c
# written: 2026-07-06 08:31:07 by deepseek-v4-pro

# Handover for b51c - Tamza Trusted List (contacts unification)

## User's explicit goal (in Max's words)
Build a **tightly controlled, verified database of Tamza regulars** by merging Zoom attendance records with Max's address book and mailing list. The database is the foundation for a secure distribution channel: a private Telegram channel where a rotating secret Zoom link (needed after the 4?July?2026 impersonator attack) is posted **only** to people Max has personally confirmed. Max's summary: "merge the contacts with Zoom recordings ... polish it using LLM ... present to me ... non?merging is much worse [than merging]."

## Key decisions made and why

- **Delivery channel: Telegram, not SMS.** Research showed Russia blocks *all* SMS carrying URLs as spam and an Aug?2025 law blocks business SMS. Since the secret is a URL, SMS to Russia is dead. A private Telegram channel (approve?to?join) was selected as the correct tool. No channel has been created yet - Max wants the database finished first.
- **Merge philosophy: bias toward merging.** Max explicitly said merging two different people is cheaper than failing to merge, so the matcher errs on the side of attaching a contact, but flags every guess.
- **Precision over recall for phones on a secret link.** Wrong phone is worse than none, so the matcher was systematically tightened: common first?names (Alexander, Vladimir, etc.) no longer act as surname anchors, patronymics don't anchor, and junk/note contacts (License #..., Regina Estimate 20230130, Nikolai Painter in Florida) are filtered out. This dropped many false attaches.
- **Two data sources for contact info.** Max's 5,700?contact address book (phones) and the Tamza mailing?list Google Sheet (decoded the full base64?encoded export to get names?email). Both are used in the join.
- **b51b owns Zoom dedup, b51c owns the JOIN.** b51b delivered a canonical list of 251 unique people (from 309 raw Zoom entries). b51c matches that list against contacts + email. The joint pipeline lives in `tools/tamza_trusted_list/`.

## Current state

The **v01 consolidation** is built, run, and pushed to the private master branch `maxrempel/claude_base` (commit b3437417). This is the output of a multi?iteration fuzzy?matching pipeline that includes:

- Normalisation of Latin?Cyrillic names
- Fuzzy digraph similarity
- Surname?anchored matching with careful guards against false first?name anchors
- Fallback to mailing?list email when contact book lacks a phone
- Merging of Zoom variants (e.g. ???/????? ???????????) under a single canonical person

**Numbers:**
- 251 real people (from b51b)
- 53 confident matches (green) - **no action needed**
- 100 best?guess matches (yellow) - **needs Max's eye**
- 98 honestly unmatched (red) - mostly first?name?only Zoom entries like "Vera", junk device names like "Zoom user" / "Samsung SM?A165F", and surnames not in Max's contacts
- 154 people now have a phone and/or email
- Of the top?100 real crowd, 72 are reachable

**Deliverable files (on disk, committed):**
- `C:/claude_base/tools/tamza_trusted_list/scripts/consolidate_v01.py` - main consolidation script (runs the join, produces CSV + HTML)
- `C:/claude_base/tools/tamza_trusted_list/scripts/email_index_v01.py` - helper that parsed the mailing?list Google Sheet
- `C:/claude_base/tools/tamza_trusted_list/scripts/join_v02_fuzzy.py` - fuzzy?join engine (the one you iterated heavily)
- `C:/claude_base/tools/tamza_trusted_list/data_work/consolidated_v01.csv` - the canonical output (251 rows, columns: canonical_name, sessions, cluster_key, contact_name, phone, email, confidence, basis, alt_candidates ...) - **gitignored, regenerates**
- `C:/claude_base/tools/tamza_trusted_list/reports/tamza_consolidated_v01.html` - review page, sorted by attendance, with green/yellow/red colouring and alternate candidates shown
- `C:/claude_base/tools/tamza_trusted_list/reports/curation_notes_v01.md` - the assistant's own?judgment verdict on all 48 meaningful yellow guesses (26 confirm, 2 fix, 13 drop?as?wrong, 7 unsure)
- `C:/claude_base/tools/tamza_trusted_list/reports/max_decisions_v01.md` - records Max's one decision so far (???? -> Ratnovskaya, not Zuser)

## Max's one answer recorded but not yet applied

Max answered only **one** of the pending questions:
- **???? (the Zoom entry) ? Ratnovskaya, NOT Zuser.** That means the previously guessed contact "????? ????" should be dropped, and ???? should be associated with the Ratnovskiy family (contact "Jane Ratnovsky"). This decision is written in `max_decisions_v01.md` but the consolidation script has not been re?run with this override yet.

## Exact next step (the very first thing to do when Max returns)

1. **Apply Max's one decision to the consolidated list.** Edit the mapping in `consolidated_v01.py` (or a post?processing override) so that the canonical person "????" gets contact `Jane Ratnovsky` (phone/email from contacts), not ?????. Re?run `consolidate_v01.py` to regenerate the CSV and HTML.
2. **Continue presenting the remaining 9 questions to Max in batches of 3**, as agreed. The full list is under Open Questions below.
3. Once all questions are answered, lock in the merges, re?run the consolidation, and commit the final "locked" version.

After the database is finalised, Max's next intention is to create the Telegram channel and invite mechanism. (He mentioned building an invitee database in a parallel session; we would then need to connect that to the trusted list.)

## Open questions still awaiting Max (the 9 pending merges)

Present in batches of 3 - Max said he can only handle 3 at a time.

**Batch A (start here):**
- **Roland Kolxeli** = typo of **Roland Kolhely** (#1 regular)? Merge them? (yes/no)
- **????? ???????-?????????** = the same person as **Irina Barabash**, or a different Irina?
- **Vita Levi** = **Vitalia Levinson**? (yes/no)

**Batch B (next after):**
- **????? ????????** = your contact "Yulia Tikhonova"? (relative, or wrong?)
- **Julia Reshko** = your contact "Iryna Reshko" (sister/relative)?
- **???? ??????** - is he part of the Shapiro family (???? ??????) or a different person?

**Batch C (final):**
- **"Posidim u Kostra" (??????? ? ??????)** - is that **Kostya Shvebs** hosting, or just an event, not a person?
- **"borec"** - a nickname; do you know who it is, or should we drop it?
- **Junk device names** - **"Mila's iPhone", "vnk", "???????????", "Zoom user", "Samsung SM?A165F"** - OK to drop all such entries from the person list? (These are genuinely not real people.)

## Key file paths and IDs

- **Workspace root** - `C:\claude_base\tools\tamza_trusted_list\`
- **Main script** - `C:\claude_base\tools\tamza_trusted_list\scripts\consolidate_v01.py`
- **Input data**:
  - Contacts backup: `C:\Users\maxre\Nextcloud\zSyncMain\contacts_backup\contacts_20260528.csv` (~5,700 rows)
  - Zoom attendance (from b51b): `C:\claude_base\projects\tamza_zoom_attendance\output\attendance_ranked_v01.csv` (309 entries)
  - Zoom canonical dedup: `C:\claude_base\projects\tamza_zoom_attendance\output\zoom_canonical.csv` (251 people)
  - Mailing?list email index: `C:\claude_base\tools\tamza_trusted_list\data_raw\email_index.csv`
- **Output (gitignored)**:
  - `C:\claude_base\tools\tamza_trusted_list\data_work\consolidated_v01.csv`
  - `C:\claude_base\tools\tamza_trusted_list\reports\tamza_consolidated_v01.html`
- **Curation & decisions**:
  - `C:\claude_base\tools\tamza_trusted_list\reports\curation_notes_v01.md`
  - `C:\claude_base\tools\tamza_trusted_list\reports\max_decisions_v01.md`
- **Branch bulletin board** - `C:\claude_base\branch_bulletin\bcast.py` (use `python bcast.py read` / `post`)
- **Timer** - `C:\claude_base\tools\timer_decel\timer_decel.py` (use `python timer_decel.py tick work|idle` when working autonomously; a `ScheduleWakeup` often automates this)
- **Worklog** - `C:\claude_base\compaction_kb\scripts\worklog.py` (the assistant logged progress)
- **Repo** - private `maxrempel/claude_base`, current branch `master` (pushed all work)
- **Bitwarden session** - saved at `C:\Users\maxre\Nextcloud\zSyncMain\ssh\bw_session.txt` (but the Zoom login part was interrupted and not completed; the contact merge does not need Zoom credentials, only b51b's data)

## Gotchas and dead ends already ruled out

- **SMS to Russia is impossible for this task.** Russia blocks all SMS containing URLs as spam. No provider can circumvent this - the block is carrier?side, not the sender.
- **Telegram bot cold?DM is blocked.** A bot cannot message a user who hasn't pressed Start; therefore the distribution must be via a private channel where Max approves each join, or via Max's own Telegram account sending invites paced slowly. The project selected the private?channel approach.
- **The fuzzy matcher had several false?positive patterns that were systematically removed:**
  - Long common first names (Alexander, Vladimir, Nikolai) acting as false surname anchors ? fixed by requiring a real surname match, not just a long token.
  - Patronymics (Borisovich) falsely matching to unrelated people ? filtered out.
  - Junk/business contacts (License #..., "Regina Estimate 20230130", "Nikolai Painter in Florida") polluting attaches ? junk?contact black
