# Adviser note - milestone 5 (~75K tokens)
# session: 20260612_ned_proskuriakova_280b77_7804acea
# written: 2026-06-12 09:11:36 by claude-opus-4-8

TO MAX:
You're about to hand a Claude session a full login to your *personal* Telegram account - SMS code and 2FA password included. That means this session (and "other sessions here") can read every private chat you have and message anyone as you. Three things to weigh before you paste any code:
- This uses an unofficial user-API login (Telethon-style). It carries a real, if low, ban risk on your main account.
- The session string it creates is a persistent credential - whoever can read that file/worktree can be you on Telegram indefinitely. Make sure it lands in your protected ssh creds folder, not loose in a worktree.
- "Run from this or other sessions" means no single audit point. Decide if you actually want every session here to have your identity, or one dedicated place.
The "I draft, you approve, you send" rule is good - hold the Assistant to it hard.

TO ASSISTANT:
Before requesting any SMS code, stop and pin down the plumbing Max just asked for. He wants this runnable across sessions with a discuss/propose/approve/send loop - that is an architecture decision you have NOT addressed. Specifically:
- Where does the session string get stored, and with what permissions? Propose the protected creds folder, not the worktree.
- How do "other sessions" invoke send without re-login? You need a small persistent helper/script, not a live login per session. Design that first.
- Make the approve-gate enforced, not just a verbal promise - no send path that bypasses Max's OK.
Propose this plan to Max and get his approval before you ever ask for the phone code. Don't trigger the login until the storage and approval mechanism are agreed.
