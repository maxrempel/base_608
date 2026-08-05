# Scribe handover - milestone 5 (~75K tokens)
# session: 20260612_ned_proskuriakova_280b77_7804acea
# cwd: C:\claude_base\.claude\worktrees\determined-proskuriakova-280b77
# written: 2026-06-12 09:11:25 by claude-opus-4-8

# HANDOVER - Telegram Assistant Setup for Max

## GOAL (in Max's words)
Max wants Claude to "start reading and sending messages on Discord, fb messenger, telegram as my assistant" - from his own account or an assistant account, "both would be useful." The chosen starting point is **Telegram, acting as Max's real personal account** ("B").

His operating model, stated explicitly: *"I want it to be run from this or other sessions here. We discuss, you propose, I approve, you send."* So the workflow must be: discuss ? Claude drafts/proposes ? Max approves ? Claude sends. Nothing auto-sends to real people without his OK.

## DECISIONS + WHY
- **Telegram first** - easiest win; credentials already partly exist; stable API. Discord and FB Messenger deferred.
- **Discord deferred** - doable only as a bot account (acting as personal account violates ToS, risks ban).
- **FB Messenger deferred** - hardest; no real personal-DM API, unofficial tools risk account bans. Only works for a Facebook Page, not personal chats.
- **Option B chosen (real account, not bot)** - Max wants to read his actual existing DMs and write to his contacts as himself. A Telegram *bot* can't do this: a bot can only talk to people who message it first, and cannot read existing DMs. So the real-account user API (e.g. Telethon-style login) is required.
- **Approval gate is mandatory** - Claude drafts; Max approves each message before it sends as him. This is the confirmed default, reinforced by Max's last message.

## CURRENT STATE
- Searched local system for existing Telegram credentials.
- **Found** an existing assistant bot: `@Clawy_33_44_bot` with its token and Max's chat_id saved on disk (see KEY PATHS). This is the Option-A bot - NOT what Max ultimately chose.
- **No real-account login exists yet.** No my.telegram.org app registered, no API ID/hash, no user session file.
- The setup for Option B has NOT been started. We are blocked at the login step.

## EXACT NEXT STEP
Resolve a tension introduced by Max's last message before doing anything else:

Max wants the assistant "run from this or other sessions here" - i.e. persistent, usable across sessions, not a one-off. The standard Option-B login normally needs a one-time interactive SMS/app login code from his phone (and 2FA password if set). The next action is to **propose a concrete login + session-persistence plan**: register an app at my.telegram.org to get an API ID/hash, perform the one-time phone-code login to create a saved user session file that future sessions can reuse (so the code is only needed once), then store that session securely alongside the other ssh creds.

Then ask Max for the two things needed to execute: his **Telegram phone number**, and confirmation he's **at his phone to grab the one-time login code** (plus 2FA password if he has one set).

## OPEN QUESTIONS AWAITING MAX
- His Telegram **phone number**.
- Is he at his phone now to grab the login code?
- Does he have a **2FA password** set on Telegram?
- Confirmation that a one-time interactive login (to create a reusable session) is acceptable, given he wants it runnable from any session here.

## KEY PATHS / IDS
- Existing bot creds file: `C:/Users/maxre/Nextcloud/zSyncMain/ssh/telegram_bot_clawy_33_44_20260524.txt`
- Bot: `t.me/Clawy_33_44_bot` (token + Max's chat_id stored in that file)
- Creds/secrets directory generally: `C:/Users/maxre/Nextcloud/zSyncMain/ssh/`
- Search tool used: `C:/claude_base/tools/es/es.exe` (Everything search)
- cwd: `C:\claude_base\.claude\worktrees\determined-proskuriakova-280b77`

## GOTCHAS
- The `es.exe` search produced **noise from worktree copies** - filter results; the real creds live in the Nextcloud `ssh` folder.
- The found bot (`@Clawy_33_44_bot`) is Option A and does **not** satisfy Max's goal - don't mistakenly build on it as if it were the answer. It can still be useful for a public "Max's assistant" people message directly.
- Acting as Max's real account carries a small ban risk (low for normal personal use) - already accepted by Max implicitly by choosing B.
- The approval-before-send rule is firm. Do not wire up any auto-send to real contacts.
- Don't ask Max to re-decide Telegram-vs-others or A-vs-B; those are settled (Telegram, B). Pick up at the login/session plan.
