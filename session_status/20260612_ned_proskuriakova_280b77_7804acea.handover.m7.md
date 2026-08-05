# Scribe handover - milestone 7 (~106K tokens)
# session: 20260612_ned_proskuriakova_280b77_7804acea
# cwd: C:\claude_base\.claude\worktrees\determined-proskuriakova-280b77
# written: 2026-06-12 10:37:44 by claude-opus-4-8

# HANDOVER - Telegram Assistant Build

## GOAL (in Max's words)
Max asked: *"I ponder if you could start reading and sending messages on Discord, fb messenger, telegram as my assistant. Most likely from my account or from assistant account."* He wants Claude to act as his AI assistant across messaging platforms - reading and writing messages for him. We started with Telegram. His operating model: *"We discuss, you propose, I approve, you send."* He explicitly wants this to be a **reusable tool any session here can call**, not a one-off.

## DECISIONS + WHY
- **Platform order: Telegram first.** Easiest, stable, Max already had bots there. Discord is doable as a bot account (acting as his personal account violates ToS ? ban risk). FB Messenger is the hard one - Meta has no real personal-DM API; unofficial tools get accounts banned. Only Pages work there. Telegram was the fast win.
- **Identity = Path B: Max's REAL account (@maxrempel), via Telethon (user API), not a bot.** Max explicitly chose B. Reason: a bot can only talk to people who message it first and can't read existing DMs or write to his contacts. Path B gives true "writing for me" access to his actual chats. Accepted small, low ban risk for personal use.
- **Draft?approve?send gate is mandatory and real.** Default Claude set and Max endorsed: Claude DRAFTS, Max approves with "send," nothing auto-sends to real people. This was implemented as an actual enforced gate in code, not just a promise.
- **Secrets stored in protected ssh folder, NOT in the worktree or any code dir.** Keeps credentials out of version-controlled/throwaway locations.

## CURRENT STATE - DONE
- Telethon installed and working.
- Registered a Telegram API app at my.telegram.org (platform: Desktop) via the Playwright browser tool. Max entered the my.telegram.org login code himself ("play safe").
- API keys captured and saved to the protected ssh folder (not displayed).
- Built the helper tool `tg.py` with subcommands: `login`, `code <code>`, `list <n>`, `read <chat_id> <n>`, `whoami`, `send`.
- Completed CLI login as **Max (@maxrempel)** - first code (55966) expired on timing; re-requested; second code (29922) succeeded. Session file written to the ssh folder.
- Hardened and **verified** the send gate: `send` with no staged draft correctly refuses. `whoami` confirms identity.
- Wrote README and logged two worklog entries documenting architecture + completion.
- Proved read access: listed chats (saw Olga, the ??? ????? chat, monitor bots) and read the Olga Foshchan conversation.

## CURRENT STATE - IN FLIGHT (paused)
Claude read Max's chat with **Olga Foshchan** (chat_id `564759209`). The conversation is in Russian; Max sent the LAST message (2026-06-07), so technically nothing is awaiting a reply. Olga's one open question was the average price for the dog-from-Ukraine service. Claude proposed (did NOT stage, did NOT send) a Russian follow-up roughly meaning: *"Olya, I'll ask Oleg the exact price and let you know. Meanwhile you can message him directly if it's easier."* Max replied **"good enough, taking a break. halt."**

## EXACT NEXT STEP
Nothing is queued to send. When Max returns, either: stage the proposed Olga reply as a draft on his go-ahead, or move to a different chat, or proceed to **Discord** (his stated next candidate platform - bot account recommended). Do not send anything without explicit "send."

## OPEN QUESTIONS AWAITING MAX
- Whether to actually send (or revise) the proposed Olga reply.
- Whether to do Discord next (and confirm bot-account approach vs. his personal account).
- FB Messenger remains flagged as not practically doable for personal DMs - undecided.

## KEY PATHS / IDS
- Tool: `C:/claude_base/tools/tg_assistant/tg.py`
- README: `C:/claude_base/tools/tg_assistant/README_tomemex.md`
- API keys file: `C:/Users/maxre/Nextcloud/zSyncMain/ssh/telegram_userapi_maxasst_20260612.txt`
- Telethon session file: in `C:/Users/maxre/Nextcloud/zSyncMain/ssh/` (protected folder)
- Pre-existing assistant bot (Path A, unused): `t.me/Clawy_33_44_bot`, token at `C:/Users/maxre/Nextcloud/zSyncMain/ssh/telegram_bot_clawy_33_44_20260524.txt`
- Account: Max, **@maxrempel**, phone **+15857051400**
- Telegram API app name registered as "MaxAssistant" (device label visible under Telegram ? Settings ? Devices)
- Olga Foshchan chat_id: `564759209`
- cwd: `C:\claude_base\.claude\worktrees\determined-proskuriakova-280b77`
- Worklog script: `C:/claude_base/compaction_kb/scripts/worklog.py`

## GOTCHAS / DEAD ENDS
- **Login codes expire fast** - request and enter immediately; first attempt (55966) died on timing. If session is lost, re-run `login` then `code <fresh>` quickly.
- **There are TWO separate codes** in setup: one for my.telegram.org web login, a second for the Telethon CLI login. Don't confuse them.
- A bare `tg.py telegram` / grep across worktrees produces noise - query the ssh creds folder directly instead.
- The send gate is enforced in code and tested; rely on it, but still treat "send" as the only trigger.
- To revoke Claude's access: Telegram ? Settings ? Devices ? terminate "MaxAssistant".
- FB Messenger personal DMs: ruled out as impractical/ban-prone. Discord-as-personal-account: ruled out (ToS/ban) - use a bot account.
- Drafting style for Max's Russian chats: match his existing tone (informal, first-name, e.g. "???").
