# Scribe handover - milestone 2 (~151K tokens)
# session: 20260705_objective_faraday_7e53f8_edcd05fb
# cwd: C:\claude_base\.claude\worktrees\objective-faraday-7e53f8
# written: 2026-07-05 12:52:06 by deepseek-v4-pro

# HANDOVER - Tamza Zoom Security + Participant List Automation

---

## GOAL (in Max's own words, composite)

Two linked objectives:

1. **Website update:** The Tamza Zoom link was attacked by hooligans/GB agents on July 4, 2026. The link is now secret and must only go to trusted people via the newsletter. The tamza.com website must stop showing the direct Zoom link publicly - replace "Enter from site" buttons with a message telling people to contact Max (+1-585-705-1400, WhatsApp/Telegram/SMS) or subscribe to admin@tamza.com to get the link.

2. **Automate trusted-participant distribution:** Pull Zoom participant history from the admin account (admin@tamza.com) to identify regulars, match them against existing contacts to get their email/phone, and build a system to auto-send them the rotating Zoom link each time it changes - so trusted people get the link without it being public.

---

## DECISIONS + WHY

- **"Don't solve the system problem"** - Max explicitly said the Bitwarden/profile concurrency bug belongs to another branch. This session should just get a working browser with Bitwarden and accomplish the task. Do not redesign the fleet.
- **Kill-all-and-relaunch approach** - All stale Playwright Chromium processes were killed and lockfiles cleared before relaunching. This worked: Bitwarden loaded in the fresh browser.
- **CLI password retrieval rejected** - Max wants the login done through the Bitwarden extension (the visual one in the browser), not by Claude fetching passwords from the CLI and typing them. This is a usability/preference decision, not a technical limitation.
- **English switch** - Max switched to English mid-session because speech recognition was mangling Russian words (especially "?????" ? "TMZ 8"). All subsequent instructions were given in English.

---

## CURRENT STATE (at interruption)

- **Playwright browser is LIVE** - Chromium PID 12880 running on the real persistent profile (`C:\claude_base\playwright_profile`), with both **Bitwarden and Grammarly extensions loaded and enabled**.
- **Browser is on** `https://zoom.us/signin` - ready for login.
- **All dead copies killed** before this launch - no contention.
- **The Bitwarden extension IS present but likely LOGGED OUT** (using `Profile 1` sub-folder, not `Default` where the vault login data lives). The vault data itself is intact and fresh (July 2) under `Default`, but the current browser session may not see it without login.
- **Zoom credentials:** In Bitwarden as "Tamza zoom 202206" - username `admin@tamza.com`, password retrievable from Bitwarden CLI (session key works: `3Q1LuTvallMTPux+...`).
- **The newsletter draft** (for July 6, 2026) is fully written, sitting in the chat transcript. It contains the new secret Zoom link (`873 4648 6242` / passcode `44`), the security announcement, and the upcoming schedule (July 4 concert, July 5 GPK).

---

## EXACT NEXT STEP

1. **Max logs into Zoom** via the live Playwright Chromium using Bitwarden (click Bitwarden icon ? unlock if needed ? fill "Tamza zoom 202206" ? complete sign-in, possibly including 2FA if enabled).
2. **Navigate to Reports:** Once logged in ? `zoom.us` ? Analytics & Reports ? Usage ? Meeting and Webinar History ? find the July 4 meeting ? click participant count ? Export CSV.
3. **Extract display names** of regular participants from the CSV.
4. **Match against Google Contacts** to recover email/phone/WhatsApp.
5. **Design a distribution method** (likely email via mxmail, since the newsletter already goes through admin@tamza.com) for the rotating link.
6. **Return to the website task** after the participant-list work - update tamza.com to hide direct Zoom links and show the "contact Max" instructions.

---

## OPEN QUESTIONS (awaiting Max)

- Should the auto-distribution list be **additional** to the existing newsletter subscribers, or a **replacement**?
- What's the preferred distribution channel - email (mxmail), WhatsApp, Telegram, all three?
- Is the website update (hiding the direct link) being done in the current branch, or is that a separate branch? The session started with website update but pivoted to the Zoom participant-list investigation before any code was written.
- Does the "Tamza zoom 202206" Bitwarden entry have 2FA? If so, Max will need to handle that during login.

---

## KEY PATHS / IDs / NAMES

- **Playwright persistent profile:** `C:\claude_base\playwright_profile`
- **Bitwarden extension ID:** `hcgcgmickjodmmlcbcjmgklhfadjbcec` (unpacked, from `C:\claude_base\tools\playwright_bitwarden\extensions\bitwarden`)
- **Bitwarden session key (live):** `3Q1LuTvallMTPux+V2rK2NippR44lr3txSZTNTTeCs3V5QD9ZqfnR7EOQrdXpi/31nCf7MOrQ2N1FIS9jmU95g==`
- **Bitwarden item name:** "Tamza zoom 202206" (username: `admin@tamza.com`)
- **New secret Zoom link:** `https://us06web.zoom.us/j/87346486242?pwd=PlqZJGDFsLIU8Xq4T0OEueN8ELokgB.1` - Meeting ID: 873 4648 6242, Passcode: 44
- **Max's contact for link requests:** +1 (585) 705-1400 (WhatsApp, Telegram, SMS, Messenger)
- **Newsletter subscription:** admin@tamza.com
- **Tamza YouTube:** youtube.com/@Tamza (recordings), youtube.com/@prostoproverka/streams (live)
- **Backup site:** pomoga.org
- **Playwright MCP config:** Lives in `.claude.json` at various levels, pins `executablePath` to `chromium-1224` under `ms-playwright`
- **Setup doc read:** `C:\claude_base\tools\playwright_bitwarden\bitwarden_persistent_setup_v01_tomemex.md`

---

## GOTCHAS

- **Profile sub-folder mismatch:** Bitwarden login data lives in `playwright_profile\Default`, but Playwright sometimes opens `playwright_profile\Profile 1` - making Bitwarden appear "logged out" even though the login is intact. Not yet systematically fixed; that fix belongs to the other branch.
- **Multi-session contention:** The `playwright_profile` is shared across ALL Claude Code sessions. Only ONE Chromium can use it at a time. If another session holds it, a new launch silently falls back to `--isolated` (empty throwaway profile with zero extensions) ? Max sees "no Bitwarden." The just-completed kill-all resolved it for now, but it will recur if multiple sessions run simultaneously.
- **Bitwarden toolbar icon may not be pinned** - even when the extension loads, Max may not see it in the toolbar (it hides under the puzzle-piece Extensions menu). This may have caused the "it's not there" vs. "it is there" dispute.
- **Speech recognition failure on "?????":** If Max speaks Russian, the recognizer mangles "?????" ? "TMZ 8" or similar. English input is more reliable for this session.
- **Zoom participant reports:** Only work if the meeting was on a Pro+ account and the user was the host. Guest participants (not logged into Zoom) will have no email in the report - only display name. This limits automatic contact matching.
- **The newsletter text references dates in 2026** (July 4-6, 2026) - these appear to be the actual content, not placeholder/draft dates. The "????????? ???????" project has raised $43,758 total.
