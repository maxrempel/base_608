# Scribe handover - milestone 4 (~68K tokens)
# session: 20260612_ned_proskuriakova_280b77_7804acea
# cwd: C:\claude_base\.claude\worktrees\determined-proskuriakova-280b77
# written: 2026-06-12 08:10:39 by claude-opus-4-8

# HANDOVER - Telegram AI Assistant Setup

## GOAL (in Max's words)
Max wants to know if Claude could "start reading and sending messages on Discord, fb messenger, telegram as my assistant." He's open to operating "from my account or from assistant account - both would be useful." After discussion he agreed to start with Telegram, confirming: "So you will be Max's AI assistant on telegram writing for me? Great. Do that."

So the immediate, approved scope is: **set Claude up to read and send messages on Telegram, acting as Max's AI assistant.**

## DECISIONS + WHY
- **Start with Telegram first** - it was assessed as the fastest, most stable win. Max already has bots there, and Telegram supports both bot accounts and personal-account access via the user API.
- **Discord deferred** - doable, but recommended as a **bot/assistant identity only**. Acting as Max's personal Discord account violates their terms and risks a ban.
- **FB Messenger deferred / likely not viable** - Meta has no real API for personal DMs. Unofficial tools tend to get accounts banned quickly. Realistically only works for a Facebook *Page*, not personal chats. This was flagged as the hard one.
- The platforms differ significantly, so the agreed approach is to handle them **one at a time**, Telegram first.

## CURRENT STATE
- Only conversation has happened - no setup work, no tool calls, no files created or modified yet.
- Max has just given the green light to begin the Telegram setup.
- A key decision point is still unresolved: **bot account vs. Max's personal account** for Telegram. Both were offered as possible; Max has not explicitly chosen which one to use. His phrasing "writing for me" leans toward acting on his behalf, but this needs confirmation before proceeding.

## EXACT NEXT STEP
Begin the Telegram setup. Before writing any integration, **confirm with Max which identity to use**:
1. A **Telegram bot** (clean, supported, separate assistant identity), or
2. Max's **own Telegram account** (via the Telegram user/client API, so messages appear as him).

Once that's decided, gather the needed credentials/access:
- If bot: a bot token from BotFather.
- If personal account: Telegram API ID + API hash (from my.telegram.org) and a login session.

Then scope what "assistant" means in practice - read-only first, or read + send; which chats; how much autonomy in sending vs. drafting for approval.

## OPEN QUESTIONS (awaiting Max)
- Bot account or his personal account for Telegram?
- Should the assistant **send autonomously**, or **draft messages for Max to approve** first?
- Which chats/contacts is it allowed to operate in?
- Does he already have a specific existing bot he wants to reuse (he mentioned already having bots on Telegram)?

## KEY PATHS / IDS
- Working directory: `C:\claude_base\.claude\worktrees\determined-proskuriakova-280b77`
- No tokens, API IDs, bot names, or files established yet.
- BotFather (for bot token) and my.telegram.org (for personal API credentials) are the relevant external sources once the identity choice is made.

## GOTCHAS / RULED OUT
- **Discord as personal account = ban risk** - use a bot identity there. Don't attempt personal-account automation.
- **FB Messenger personal DMs = effectively a dead end** - no official API; unofficial tools risk account bans. Only a Facebook Page is realistic. Don't burn time here unless Max explicitly insists.
- For Telegram, personal-account access requires the **user API (API ID/hash + session login)**, which is different and more involved than a simple bot token - pick the path before building.
- Max said he already has bots on Telegram, so check for reusable existing setup before creating anything new.
