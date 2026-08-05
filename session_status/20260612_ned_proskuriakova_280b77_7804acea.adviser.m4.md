# Adviser note - milestone 4 (~68K tokens)
# session: 20260612_ned_proskuriakova_280b77_7804acea
# written: 2026-06-12 08:10:46 by claude-opus-4-8

TO MAX:
Before this goes further, decide the identity question deliberately. "Writing for me" on Telegram as YOUR own account means the Assistant sends messages to real people impersonating you. That has real-world consequences (reputation, trust, account safety). A separate assistant/bot identity is the safer default. Tell the Assistant which one you actually want.

TO ASSISTANT:
Do not start building anything yet. "Do that" is too vague to act on safely. Before any code or API setup, nail down:
1. Identity - bot account vs Max's personal user account (very different setup, risk, and ethics). Do not silently pick the personal-account route.
2. Scope - read-only first, or auto-send? Auto-replying to humans as Max without review is a big step; default to drafts-for-approval.
3. Credentials - what bot token / API id Max has, and where they live.

Ask these three, get explicit answers, then proceed one channel (Telegram) at a time. No tool calls until identity and send-vs-draft are confirmed.
