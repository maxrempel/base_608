
## [2026-06-12 09:11] ? 7804acea
- DID: Decided Telegram-assistant architecture: act as Max's REAL account via Telethon (path B), reusable tool any session calls, flow = read->draft->Max approves->send
- STATE: Have bot tokens in ssh; NO user-account session yet. Blocked on Max's phone number + SMS login code to register my.telegram.org app + Telethon login
- NEXT: Get phone+code from Max, get api_id/api_hash, build C:/claude_base/tools/tg_assistant/ (read/list/send), store session in zSyncMain/ssh

## [2026-06-12 10:32] ? 7804acea
- DID: Built+logged-in Telegram assistant tool: Claude now acts as Max's REAL account @maxrempel via Telethon. Tool C:/claude_base/tools/tg_assistant/tg.py (read/list/draft/send), draft->approve->send gate enforced (send refuses w/o staged draft), every send audited
- STATE: LIVE. Logged in OK, can read real chats. Session+api creds in zSyncMain/ssh (not worktree). NOT sent anything yet
- NEXT: Use draft->send flow when Max wants to reply. Later: FB Messenger (hard, Meta locked), Discord (bot identity). Revoke via Telegram Settings>Devices
