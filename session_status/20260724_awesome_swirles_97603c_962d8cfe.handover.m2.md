# Scribe handover - milestone 2 (~168K tokens)
# session: 20260724_awesome_swirles_97603c_962d8cfe
# cwd: C:\moma\.claude\worktrees\awesome-swirles-97603c
# written: 2026-07-24 22:41:08 by deepseek-v4-pro

# HANDOVER - Session: Compaction Threshold, Token Bloat Investigation, Agent Rules Update

## GOAL (in Max's words)

1. "Increase the default compaction trigger from 175 to 230,000 tokens. Set it as default in the settings." - DONE.
2. "Which is way above my default instructions that are loaded by default... go and search, maybe there is some inflation of instructions that just suddenly happened." - INVESTIGATED, root cause identified.
3. "The story with Codex is that I migrated to Codex, it swallowed its plan much faster than needed so I am now running parallel Codex and Claude... So that agent rules should be, I guess, updated strongly, basically we are running them in parallel and probably they want to communicate between each other. So review it thoroughly and remove all nonsense and outdated stuff." - DONE (reframe pass), one bloated block flagged but not yet trimmed.

## DECISIONS MADE + WHY

### Compaction Threshold
- **Key used:** `autoCompactWindow` (not `autoCompactEnabled`, which is just the on/off toggle).
- **Value:** 230000 (within schema range 100000-1000000).
- **File:** `C:\Users\maxre\.claude\settings.json` (user/global scope - applies as default across all sessions).
- **Method:** Read existing file first, then merged with Edit. The old value was **180,000** (Max remembered it as 175K). Now 230,000. Other keys (e.g. `"model": "opus"`) preserved.

### Token Bloat Investigation
- **Finding:** Rule files total ~66K tokens - roughly what Max always remembered as ~70K. The instructions did NOT actually double.
- **The extra ~60K pushing sessions to ~130K:** MCP connector tool schemas and baked-in instruction blocks. Specifically: google-calendar, google-contacts (~25 tools alone), Notion, Gmail, Google Drive, Memex (?2 instances), Babel, playwright, claude-in-chrome, computer-use, lakarian-python, pine-python, scheduled-tasks, dialog-trainer, mcp-registry, readai. The big hitters: claude-in-chrome and computer-use each inject multi-paragraph instruction manuals into the prompt.
- **global2.md is NOT to be removed.** Its header says "FROZEN LEGACY FILE - do not add new rules here" but that only means new rules go in the shared file. The content is current and load-bearing (~30K tokens). Claude initially suggested dropping global2, then retracted that when Max pushed back. Keep loading it.

### Agent Rules File Update
- **File edited:** `C:\Users\maxre\Nextcloud\claude_md_synced\global_AGENT_RULES.md`
- Four surgical edits made:
  1. Added a top note: Claude and Codex run as parallel co-equal peers, each burns its weekly limit in 3-4 days, so neither is primary/legacy.
  2. Rewrote "migrating away from Claude, build Codex-first" ? "neither is being retired; build tooling both agents can run."
  3. Changed "Codex is Max's primary agent" ? "co-equal agents that both read this file."
  4. Added a short "Two agents in parallel - coordination" section: coordinate through shared files, git history, work-logs; check what the other did before big work; leave a handoff when pausing.
- **No safety rules were deleted.** One safety block was identified as bloated - a giant internet-throttling/bandwidth paragraph (Watcher 3, Verigen, Lakarian link). It reads like a Codex session dumped a full method doc into the rules. Left untouched pending Max's decision.
- The original file had been written under the assumption "Codex replaces Claude" - that was the outdated framing now corrected.

## CURRENT STATE

### Done
- Compaction threshold raised from 180K to 230K in `C:\Users\maxre\.claude\settings.json` (global default).
- `global_AGENT_RULES.md` reframed from "Codex-primary" to "parallel co-equal agents."
- Token bloat root cause identified: MCP connector pile, not rule file inflation.
- Rule files measured and accounted for - the ~70K baseline is normal.

### In Flight / Not Yet Done
- The bloated internet-throttling paragraph in `global_AGENT_RULES.md` was flagged but not yet trimmed.
- No MCP servers have been disconnected.
- No further optimization has been applied to reduce the ~130K session startup cost.

## EXACT NEXT STEP

Claude offered to produce a **full MCP connector inventory** - every connected server, one line of what it does, plus a rough estimate of how many tokens it costs the prompt - so Max can decide what to disconnect. This is the most immediate pending action.

Before that inventory is done: Max should also confirm or deny whether a "Codex becomes primary agent" migration was ever approved (the file was written as if it was, but Max didn't recognize global_AGENT_RULES.md and called it "super weird"). That answer affects whether further rules cleanup is needed beyond the reframe already done.

## OPEN QUESTIONS AWAITING MAX

1. **Does the "Codex migration" ring a bell?** The shared rules file was created/edited today under the assumption Max is moving to Codex as primary. If that never happened (or happened differently), the file may need more rework than the surgical fixes already applied.

2. **Want a full MCP connector inventory?** Claude offered to enumerate every connected MCP server with rough token cost so Max can choose what to disconnect.

3. **Shrink the bloated internet-throttling safety block?** The giant paragraph (Watcher 3, Verigen, Lakarian link) in `global_AGENT_RULES.md` is flagged for trimming - reads like a method doc dump, not a compact rule.

4. **Which MCP servers are truly needed per-session vs. on-demand?** Specifically: pine-python and lakarian-python were retired on Claude Desktop back in July as redundant with plain SSH, but are still wired into Claude Code. dialog-trainer and mcp-registry are also suspect.

## KEY FILE PATHS

| File | Role |
|------|------|
| `C:\Users\maxre\.claude\settings.json` | Global user settings - now contains `"autoCompactWindow": 230000` |
| `C:\Users\maxre\Nextcloud\claude_md_synced\global_AGENT_RULES.md` | Shared Claude+Codex rules (~10K tokens) - just reframed to parallel-agent reality |
| `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md` | "Frozen" legacy rules (~30K tokens) - still load-bearing, do NOT remove |
| `C:\Users\maxre\Nextcloud\claude_md_synced\global_CLAUDE.md` | Claude-only global rules (~6K tokens) |
| `C:\Users\maxre\Nextcloud\claude_md_synced\max_profile_tomemex.md` | Max's profile (~1K tokens) |
| `C:\moma\.claude\worktrees\awesome-swirles-97603c` | Current working directory (worktree) |

## GOTCHAS & RULED-OUT DEAD ENDS

- **The "175" was actually 180,000** in the settings file already. Not a problem, just a note.
- **global2 is NOT "outdated."** The "FROZEN LEGACY" header only means don't add new rules to it - the content is current. Do not propose removing it again.
- **The ~130K startup is mostly MCP connectors, not instructions.** The rule-file doubling theory was dead wrong - rules are still ~70K. The extra is tool schemas and baked-in connector instruction manuals (claude-in-chrome, computer-use, etc.).
- **Some MCP servers are zombie connections:** pine-python and lakarian-python were retired on Claude Desktop in July but live on in Claude Code.
- **Settings watcher caveat:** If a new settings file is created mid-session, the watcher may not pick it up until `/hooks` is opened or the session is restarted. The compaction change went into an existing file, so this should not apply here.
- **Always merge, never replace** when editing settings.json. This was followed correctly.
- **`autoCompactWindow` is the correct key** - not `autoCompactEnabled` (that's just the boolean toggle, not the threshold value).
- **dialog-trainer and mcp-registry** are of unclear origin and purpose - worth investigating before keeping connected.
