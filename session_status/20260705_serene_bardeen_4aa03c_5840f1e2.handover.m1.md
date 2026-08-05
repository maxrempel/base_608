# Scribe handover - milestone 1 (~119K tokens)
# session: 20260705_serene_bardeen_4aa03c_5840f1e2
# cwd: C:\claude_base\.claude\worktrees\serene-bardeen-4aa03c
# written: 2026-07-05 13:48:04 by deepseek-v4-pro

# HANDOVER - Tamza Session (serene-bardeen-4aa03c)

---

## GOAL (in Max's words)

Two intertwined objectives emerged:

1. **Website update (tamza.com):** After a coordinated Zoom-bombing attack by "agents of GB" on July 4, the public Zoom link posted on the website must be removed or hidden. The link is now secret - only shared via the email newsletter to known people. The site's "????? ? ?????" (Join from site) buttons can no longer point directly to Zoom.

2. **Trusted-regulars auto-notification system:** Max wants to collect typical Zoom participants from past meeting reports, extract their contact info, and build an automated pipeline that sends the rotating secret link to those regulars directly - so trusted people who aren't on the newsletter still get the link.

This conversation was on a **branch from a branch** - a fresh task distinct from whatever was on the parent branch.

---

## DECISIONS MADE + WHY

| Decision | Reasoning |
|---|---|
| **Zoom link must NOT appear publicly on tamza.com** | The July 4 attack was serious enough to force a "secret mode." Posting it openly lets attackers grab it. |
| **Text replacement proposed instead of a password gate** | Simpler and more direct - users are told to contact Max (WhatsApp/Telegram/SMS) for the fresh link. |
| **Match Zoom participant names against Google Contacts** | Zoom reports only give display names + optional email (only if the person was logged into a Zoom account). Max already has a rich contact base; matching names ? email/phone is the bridge. |
| **Auto-send via email (mxmail) for now** | WhatsApp/Telegram auto-send is a separate, later channel. |
| **Use the Bitwarden entry "Tamza zoom 202206"** for Zoom login | That's the Zoom account for admin@tamza.com. Found via `bw list items --search tamza` in the ssh/tamza-related Bitwarden vault. |
| **Target Zoom web portal (zoom.us ? Reports), NOT the desktop app** | Only the web portal at zoom.us provides exportable participant CSV reports for hosts. |

---

## CURRENT STATE - WHAT IS DONE

**Website task:**
- Problem diagnosed and confirmed: secret Zoom link replaces the public one.
- Draft replacement text was proposed (Russian - telling people to contact Max at +1-585-705-1400 or subscribe to admin@tamza.com).
- **No code or site edits were made.** This is pure analysis so far.

**Zoom participant extraction task:**
- Bitwarden session established: `BW_SESSION=3Q1LuTvallMTPux+V2rK2NippR44lr3txSZTNTTeCs3V5QD9ZqfnR7EOQrdXpi/31nCf7MOrQ2N1FIS9jmU95g==`
- Bitwarden item found: **"Tamza zoom 202206"**, username **admin@tamza.com**
- Playwright browser opened, navigated to `https://zoom.us/account/report/user`, currently sitting at the Zoom sign-in page.
- The `bw get item "Tamza zoom 202206"` command was issued to retrieve the password but **was interrupted before completing** - the password was not yet extracted.

**What was NOT yet done:**
- Password not retrieved from Bitwarden output.
- Not logged into Zoom.
- No participant reports pulled yet.
- No matching against Google Contacts.
- The "tamza.com to update" work was not started.

---

## EXACT NEXT STEP

**Step 1 - Retrieve the Zoom password and log in:**
```bash
export BW_SESSION="3Q1LuTvallMTPux+V2rK2NippR44lr3txSZTNTTeCs3V5QD9ZqfnR7EOQrdXpi/31nCf7MOrQ2N1FIS9jmU95g=="
bw get item "Tamza zoom 202206" --session "$BW_SESSION"
```
Parse the JSON output for the password field (likely under `.login.password`).

**Step 2 - Log into Zoom via Playwright:**
- Fill the email field with `admin@tamza.com` on the current sign-in page.
- Click Next, then fill the password field, click Sign In.
- (If there's a 2FA prompt, Max will need to handle it.)

**Step 3 - Navigate to participant reports:**
- Go to: Analytics & Reports ? Meetings & Webinars ? Usage Reports ? Meeting and webinar history.
- Find the July 4 meeting (the one that was attacked) and any other recent meetings.
- Export participant CSV(s).

**Step 4 - Match names against Google Contacts** (once CSV is in hand).

**Step 5 - Website work (separate branch task, not yet started):**
- Locate the source for tamza.com (likely in a different worktree or repo).
- Replace "????? ? ?????" links with the contact-Max message (the draft text from the conversation).

---

## OPEN QUESTIONS (awaiting Max)

1. **Is the auto-notify list *additional* to the newsletter, or a *replacement*?** The newsletter already reaches trusted people via admin@tamza.com. Clarifying overlap matters for architecture.
2. **Which meetings to pull reports from?** Just July 4? All of 2024-2025? A specific date range?
3. **Where is the tamza.com source code?** Not yet located - no file operations were done on it in this session.
4. **What's the parent branch?** This is "a branch from a branch" - knowing the hierarchy matters for merges later.

---

## KEY PATHS, IDS, COMMANDS

| What | Value |
|---|---|
| **cwd (worktree root)** | `C:\claude_base\.claude\worktrees\serene-bardeen-4aa03c` |
| **Bitwarden session** | `3Q1LuTvallMTPux+V2rK2NippR44lr3txSZTNTTeCs3V5QD9ZqfnR7EOQrdXpi/31nCf7MOrQ2N1FIS9jmU95g==` |
| **Bitwarden item** | `Tamza zoom 202206` |
| **Zoom username** | `admin@tamza.com` |
| **Zoom account** | Pro-level (required for reports) |
| **New secret Zoom link** | `https://us06web.zoom.us/j/87346486242?pwd=PlqZJGDFsLIU8Xq4T0OEueN8ELokgB.1` |
| **Meeting ID** | `873 4648 6242` |
| **Passcode** | `44` |
| **Max's phone for contacts** | `+1 (585) 705-1400` |
| **Newsletter sub** | `admin@tamza.com` |
| **Bitwarden session file** | `C:/Users/maxre/Nextcloud/zSyncMain/ssh/bw_session.txt` |
| **Playwright** | Already connected via MCP (`mcp__playwright__browser_navigate`, `browser_snapshot`, `browser_take_screenshot`) |

---

## GOTCHAS & DEAD ENDS RULED OUT

- **Zoom desktop app is useless for this** - only the web portal (zoom.us) has the participant CSV export. ChatGPT confirmed this.
- **Free Zoom accounts don't get participant reports** - admin@tamza.com must be Pro or higher. Worth verifying the plan tier after login.
- **Guest participants (no Zoom account) leave no email in the report** - their rows will have display names only, with blank email. Matching those against Google Contacts is purely name-based (fuzzy).
- **Bitwarden session tokens expire** - the `BW_SESSION` above may be dead by the time this handover is read. The cold session should regenerate it: check `bw_session.txt` freshness or run `bw login` / `bw unlock`.
- **Speech recognition repeatedly misheard "Tamza"** - Max had to spell it T-A-M-Z-A. The Bitwarden search for "tamza" (not "zoom") was what found the right entry.
- **The website update is a SEPARATE worktree/branch** - don't confuse it with this Zoom-participant work. Max explicitly said "another task in this branch" after switching, so the website edits might belong to a different branch entirely.
