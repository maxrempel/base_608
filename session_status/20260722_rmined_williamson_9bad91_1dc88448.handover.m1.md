# Scribe handover - milestone 1 (~128K tokens)
# session: 20260722_rmined_williamson_9bad91_1dc88448
# cwd: C:\claude_base\.claude\worktrees\determined-williamson-9bad91
# written: 2026-07-22 14:42:31 by deepseek-v4-pro

# Handover: Better Claude Code Desktop That Uses Anthropic Max Plan

**GOAL (in Max's own words)**
"Did anyone make a better replacement for Claude Code desktop? Codex is so much better, but I like Claude's Opus. So the question is just a better desktop app that uses the same $200/month plan from Anthropic."

**DECISIONS + WHY**
The assistant searched online and narrowed the field to two options that can reuse the Max subscription (i.e., log in with your Anthropic account, not require a separate API key or provider subscription):
- **Official redesigned Claude Code desktop app** - now has multi?session, file editor, diff viewer, and "Routines" (per VentureBeat, June 2026).
- **OpenCode** - an open?source terminal?with?GUI frontend that claims to support login via your Claude subscription (OAuth) instead of an API key.

Reason: Almost every other well?known "better" desktop tool (Cursor, Aider, Cline, Devin, etc.) either requires its own subscription or an API key and cannot ride the Max plan's Opus quota. The Max?plan?login constraint eliminated them.

Assistant recommended trying **OpenCode** first because it may approximate the "Codex feel" while still delivering Opus through the subscription, but explicitly flagged uncertainty about whether OpenCode currently supports Max?plan OAuth for Opus without a hitch.

**CURRENT STATE**
The assistant delivered the TLDR with sources and ended with a question for Max:
> "Want me to look closer at whether it truly supports Max?plan OAuth for Opus right now?"
The session is paused awaiting Max's reply. No further actions taken, no files modified, no configuration changes.

**EXACT NEXT STEP**
Answer Max's pending question. The most useful next action is either:
- Perform a deep?dive search/verification of OpenCode's current Max?plan OAuth support for Opus, including any known issues or workarounds,
- or, if Max prefers, guide them to try the official redesigned Claude Code desktop app first (since it's guaranteed to work with the subscription) and then compare with OpenCode.

**OPEN QUESTIONS STILL AWAITING THE USER**
1. Does OpenCode genuinely work with Max?plan OAuth for Opus right now (mid?2026) without requiring an API key or separate billing?
2. Does Max want to pursue OpenCode, the official app, or both?
3. What specific aspects of "Codex's feel" does Max value most (UI responsiveness, project sidebar, diff view, etc.)? This could inform whether OpenCode or the official redesign is a better match.

**KEY PATHS / IDS / NAMES**
- **cwd**: `C:\claude_base\.claude\worktrees\determined-williamson-9bad91` (session workspace; not directly relevant to the query).
- No files were created or changed in this session.
- Relevant terms: "Claude Code desktop," "OpenCode," "Anthropic Max plan ($200/month)", "Opus", "Codex".
- Sources saved: VentureBeat article on the redesign (June 2026), Nimbalyst blog on Claude Code GUI tools (2026), SecurityBoulevard comparison of 8 alternatives (2026).

**GOTCHAS**
- The user's original message had a typo "antrhopic" - irrelevant.
- The big trap: Most "better desktop app" recommendations online will point to tools that need an API key, which would bill you per token **on top of** your Max plan - that is not what Max wants. The assistant already pre?filtered for subscription?login capability.
- The assistant's recommendation of OpenCode is provisional - if OpenCode's OAuth integration is broken or only supports Free/Pro plans, it's a dead end. That's the immediate unknown that needs closing.

**TL;DR for the next session**
Max wants a desktop app that feels like Codex but uses Opus through his existing $200/month Anthropic Max subscription. Two candidates emerged: the official revamped Claude Code desktop app (safe, works out of the box) and OpenCode (unverified OAuth support). The ball is in Max's court on whether to verify OpenCode's Max?plan OAuth support or just try the official app first.
