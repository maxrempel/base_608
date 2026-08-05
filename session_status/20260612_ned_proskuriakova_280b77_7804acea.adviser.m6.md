# Adviser note - milestone 6 (~96K tokens)
# session: 20260612_ned_proskuriakova_280b77_7804acea
# written: 2026-06-12 10:29:08 by claude-opus-4-8

Max pasted the login code, but that code carries Telegram's own literal warning: "Do not give this code to anyone, even if they say they are from Telegram!" That warning exists because handing this code to a third party IS the account-takeover attack. Max authorized this himself, so it's not theft - but it's worth a beat.

TO MAX:
You just gave the Assistant full login control of your REAL Telegram account (all DMs, ability to message anyone as you). That's exactly what you asked for, so no foul - but understand the blast radius: the Telethon session file now living in your ssh folder = permanent logged-in access for any session here, no further code needed. If you ever want to revoke it, it's Telegram Settings > Devices > terminate session. Two things to confirm you actually want: (1) full account, not the safer bot, and (2) that the draft-then-approve gate is real and enforced, not just a promise in chat. If both are yes, you're fine.

TO ASSISTANT:
Mostly clean execution. Three corrections:
- The "I DRAFT, you approve before sending" rule is currently just words. Enforce it in the tool itself: send should require an explicit confirm flag / separate step, never auto-fire. Verify tg.py does this; if not, fix before anything goes live.
- Confirm the session string landed in the protected ssh folder and NOT in the worktree or any git-tracked path. State the exact file so Max can see it.
- Do a single sanity read (e.g. list recent dialogs) to prove login worked, then STOP and report. Do not start sending or batch-processing chats this session.
