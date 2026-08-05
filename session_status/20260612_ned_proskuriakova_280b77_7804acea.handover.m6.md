# Scribe handover - milestone 6 (~96K tokens)
# session: 20260612_ned_proskuriakova_280b77_7804acea
# cwd: C:\claude_base\.claude\worktrees\determined-proskuriakova-280b77
# written: 2026-06-12 10:28:57 by claude-opus-4-8

# HANDOVER - Telegram Assistant Build

## GOAL (in Max's words)
Max wants Claude to "start reading and sending messages on Discord, fb messenger, telegram as my assistant," writing from his own account. We agreed to start with Telegram only. His refinement on usage: *"I want it to be run from this or other sessions here. We discuss, you propose, I approve, you send."* So the deliverable is a reusable Telegram tool that ANY session here can call: Claude reads chats, drafts a reply, Max approves, then Claude sends.

## DECISIONS + WHY
- **Telegram first** - easiest, stable, existing credentials present. Discord deferred (recommend bot identity, since personal-account automation is bannable). FB Messenger deferred (no real personal-DM API; unofficial tools get banned). These are future phases, not now.
- **Path B chosen: act as Max's REAL Telegram account** (via Telethon user API), NOT the assistant bot. Why: a bot (`@Clawy_33_44_bot`) can only talk to people who message it first and cannot read existing DMs or write to Max's contacts. Max explicitly picked B to get true "writing for me" across his real chats. Small ban risk acknowledged, judged low for personal use.
- **Approval gate is a hard default**: Claude DRAFTS, Max approves, only then Claude sends. No auto-send to real people without Max's OK. Send is a separate explicit step. Max can loosen later if he wants.
- **Reusable tool, not one-off**: built so every session here can use it.
- **Secrets stored in Max's protected ssh folder, never the worktree, never displayed.**

## CURRENT STATE
- Python + Telethon confirmed installed and importable.
- Logged into my.telegram.org successfully (Max entered the first login code himself; "i entered the code, please play safe").
- No pre-existing API app existed; created a new one (Desktop platform) on my.telegram.org.
- API keys (api_id / api_hash) retrieved and saved to the protected ssh folder.
- Helper tool written at the path below.
- Browser (Playwright) closed.
- Ran `tg.py login` - Telethon requested a SECOND code (the CLI session login code). This is a different code from the my.telegram.org one.
- Max has just provided that CLI login code: **55966**.

## EXACT NEXT STEP
Feed the code **55966** into the waiting Telethon `tg.py login` flow to complete the CLI session authentication. If a 2FA password is required after the code, ask Max for it. On success, Telethon writes a session file (so future logins are silent). Then verify login works (e.g., fetch own account / list recent dialogs read-only) and confirm to Max the tool is live. Do NOT send any message to anyone as part of verification - read-only only.

Note: the prior `login` invocation may have already consumed/closed its stdin prompt. If the code can't be piped into the still-running process, re-run the login and enter 55966 promptly (codes expire fast - if it's stale, a fresh code must be requested and Max re-asked).

## OPEN QUESTIONS (awaiting Max)
- Whether a 2FA password is set on his account (will only matter if Telethon prompts after the code).
- None else outstanding for Telegram. Discord and FB Messenger remain agreed-but-not-started future phases.

## KEY PATHS / IDS / NAMES
- Tool: `C:\claude_base\tools\tg_assistant\tg.py` (subcommands include `login`; designed to be called by any session).
- API keys saved: `C:\Users\maxre\Nextcloud\zSyncMain\ssh\telegram_userapi_maxasst_20260612.txt`
- Existing assistant bot creds (path A, not used): `C:\Users\maxre\Nextcloud\zSyncMain\ssh\telegram_bot_clawy_33_44_20260524.txt` - bot is `t.me/Clawy_33_44_bot`, token + Max's chat_id inside.
- Max's Telegram phone: **+15857051400**
- CLI login code just given: **55966**
- Telethon session file: intended to live in the protected ssh folder (not the worktree). Confirm tg.py writes it there.
- Worktree cwd: `C:\claude_base\.claude\worktrees\determined-proskuriakova-280b77`
- Worklog script used for decisions: `C:\claude_base\compaction_kb\scripts\worklog.py`

## GOTCHAS / DEAD ENDS
- **Two different codes exist**: one from my.telegram.org (already used), one from Telethon CLI login (55966). Don't confuse them.
- Telegram login codes arrive **in the Telegram app, not SMS**, and expire quickly.
- The login-code message itself contains the warning "Do not give this code to anyone..." - that's standard Telegram boilerplate Max forwarded; it's the legitimate code for OUR own login, expected and fine to use here.
- Initial credential search produced **noise from worktrees**; the real creds were in the ssh folder - search there directly.
- Store secrets ONLY in the ssh folder, never the worktree; never print keys to output.
- Bot account (path A) cannot read existing DMs or initiate to contacts - that's why path B was required.
- Send must stay gated behind explicit Max approval; do not wire any auto-send.
