# Scribe handover - milestone 2 (~166K tokens)
# session: 20260725_laughing_taussig_f0a4bf_4ee52300
# cwd: C:\claude_base\.claude\worktrees\laughing-taussig-f0a4bf
# written: 2026-07-25 15:55:33 by deepseek-v4-pro

# HANDOVER - Token Budget, Cheap Model Routing, Measurement System

---

## GOAL (Max's words)

> "Figure out, compare searching line and we need to reduce the token usage. So let's try starting from DeepSeek as a major worker to do the work or maybe not. Maybe whatever native Claude native worker is to do the dirty work, the bulk, so to save the tokens. Searching line, what's the best practice in terms of tokens and money? I have $200 a month plan and I need to not run out of the tokens every week. So maybe Claude's native simpler, faster, less expensive model would work for dirty work. Search online and implement and set up the measurement system."

Translation: Max burns through his $200/month Claude plan in ~3-4 days. Wants to know whether DeepSeek or Claude-native cheap models (Haiku/Sonnet) is the right answer, and wants measurement built so he can see if it's working.

---

## DECISIONS MADE + WHY

### 1. DeepSeek is NOT the fix for the weekly allowance
DeepSeek costs are paid per-token out of pocket (tracked by `ds_ledger`), not from the Claude plan. It helps the wallet but does zero to relieve the rolling 5-hour/weekly Claude allowance windows. The only thing that stretches the Claude allowance is cheaper Claude models (Haiku, Sonnet) and smaller per-message context.

### 2. Built Claude-native cheap-model sub-agents (grunt + mule)
Claude Code supports `model:` frontmatter on sub-agents - resolved per-invocation, no env var needed. Created two:
- **grunt** (Haiku): bulk reading, grepping, listing, extracting, checking presence, summarizing verbose output. Returns SHORT answers, no file dumps.
- **mule** (Sonnet): well-spec'd hands-on work - writing scripts, mechanical refactors, format conversion, wiring scheduled tasks.

The main Opus session keeps judgment and conversation with Max. Delegation is for volume, not decisions.

### 3. Built measurement on ccusage, not an API
`ccusage` (npm) reads local Claude Code + Codex JSONL session logs on this machine - no API key, nothing leaves the machine. It supports `--json`, per-model breakdowns, cache create/read splits. `snapshot.py` shells out to it, buckets by model family, writes JSON for a dashboard.

### 4. Did NOT touch global2.md for trimming yet
global2.md is 117KB (~30k tokens) of the 55k-token always-loaded preamble - the single biggest lever for reducing per-message cost. But it's Max's rule file. Asked him for a decision; awaiting answer.

### 5. Measurement KPIs chosen
- **cheap-model share** of Claude token work (the goal metric - should move off 0.0%)
- **preamble tokens** per session (~55,028 baseline)
- **cache-read share** (>90% - mostly re-reading conversation history)
- **$/day vs plan $6.67/day** (13x at baseline)

### 6. Hidden scheduled task via PowerShell, not schtasks
Git Bash mangles `schtasks /Create`. Used PowerShell `Register-ScheduledTask` with `pythonw.exe` (no console window). Runs every 2 hours.

---

## CURRENT STATE

### Done and verified working:
- `ccusage` installed globally (npm)
- `C:\claude_base\tools\token_budget\snapshot.py` - runs, produces baseline: **"claude 7d $608.18 ($86.88/day, plan is $6.67/day) cheap-model share 0.0% preamble 55028 tok"**
- `C:\claude_base\tools\token_budget\dashboard.html` - light theme, compact (~1.35 line-height per Max's preference), KPI cards + 21-day table + preamble size table + plain-English explanation
- Hidden scheduled task **"Max Token Budget Snapshot"** - State: Ready, runs `pythonw.exe snapshot.py` every 2 hours
- `C:\Users\maxre\.claude\agents\grunt.md` - Haiku bulk worker, frontmatter `model: haiku`
- `C:\Users\maxre\.claude\agents\mule.md` - Sonnet workhorse, frontmatter `model: sonnet`
- `C:\claude_base\tools\token_budget\README_tomemex.md` - documents baseline, KPIs, dashboard, gotchas
- New section added to `C:\Users\maxre\Nextcloud\claude_md_synced\global_AGENT_RULES.md` (under `## Token budget - hand bulk work to a cheap model (added 2026-07-25)`) - verbatim text shown to Max in report, awaits his recheck
- Matching shorter pointer added to `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md`
- All new files committed and pushed (only explicit paths, never `git add -A` per standing constraint for this shared dirty checkout)

### Smoking gun - the 13x diagnosis:
| Metric | Value |
|--------|-------|
| Claude $/day (7d avg) | $86.88 |
| Plan face value/day | $6.67 |
| Over-plan multiple | **~13x** |
| Cheap-model share | **0.0%** |
| Cache-read share | >90% |
| Preamble tokens | 55,028 |
| global2.md size | 117 KB (~30k tokens) |

### NOT yet verified:
- **Grunt/mule agents may not be visible in desktop Claude Code sessions.** The smoke test from this session (which runs on the desktop agent registry) could not see them. They live in `~/.claude/agents/` where CLI Claude Code reads them - should be available in a fresh session - but unconfirmed. **The dashboard's cheap-model share staying at 0.0% would be the canary.**

---

## EXACT NEXT STEP

**Max needs to answer the open question about trimming global2.md.** That's the blocking decision. Once he says yes/no, the next action is either:

If YES: Move the rarely-needed recipes out of global2.md into on-demand skill files, keeping only always-true core rules inline. This cuts the 30k-token standing cost of every session and every sub-agent invocation.

If NO: Move on to verifying cheap-model routing is actually working in real sessions (check dashboard after a day of real use).

Regardless of his answer, wait 24-48 hours and check `dashboard.html` to confirm cheap-model share moves off 0.0%. If it stays at zero, the grunt/mule agents aren't being picked up - need to debug desktop vs CLI agent resolution.

---

## OPEN QUESTIONS AWAITING MAX

1. **"Do you want me to trim global2.md?"** - 117KB of always-loaded preamble, ~30k of the 55k tokens. Move rarely-needed recipes to on-demand skills, keep always-true rules inline. Would substantially cut the standing cost of every session. His rules, his decision.

2. Implicit recheck: Max has a standing rule that any text written to persistent rules or memory must be shown to him verbatim. The new token-budget section in `global_AGENT_RULES.md` was shown in the TLDR report. Has not yet been acknowledged.

---

## KEY PATHS, IDS, COMMANDS

### Files created/modified:
```
C:\claude_base\tools\token_budget\snapshot.py          (measurement engine)
C:\claude_base\tools\token_budget\dashboard.html        (HTML dashboard)
C:\claude_base\tools\token_budget\README_tomemex.md     (documentation)
C:\Users\maxre\.claude\agents\grunt.md                  (Haiku sub-agent)
C:\Users\maxre\.claude\agents\mule.md                   (Sonnet sub-agent)
C:\Users\maxre\Nextcloud\claude_md_synced\global_AGENT_RULES.md  (EDITED - new token-budget section)
C:\Users\maxre\Nextcloud\claude_md_synced\global2.md              (EDITED - matching pointer)
```

### The preamble chain (always-loaded on every session + every sub-agent):
```
~\.claude\CLAUDE.md
Nextcloud\claude_md_synced\global2.md          ? 117KB, biggest single file
Nextcloud\claude_md_synced\global_AGENT_RULES.md
Nextcloud\claude_md_synced\max_profile_tomemex.md
C:\claude_base\user_dictionary_tomemex.md
C:\claude_base\CLAUDE.md
C:\claude_base\AGENTS.md
~\.claude\projects\C--claude-base\memory\MEMORY.md
```

### Scheduled task:
- Name: **"Max Token Budget Snapshot"**
- Runs: `pythonw.exe C:\claude_base\tools\token_budget\snapshot.py` every 2 hours
- Created via PowerShell `Register-ScheduledTask`, NOT schtasks (Git Bash mangles it)
- `pythonw.exe` at `C:\Users\maxre\AppData\Local\Python\pythoncore-3.14-64\pythonw.exe`

### Session log (pre-compaction full transcript reference):
```
C:\Users\maxre\.claude\projects\C--claude-base--claude-worktrees-laughing-taussig-f0a4bf\4ee52300-3599-41cb-b3d0-a87af126c1cd.jsonl
```

---

## GOTCHAS AND DEAD ENDS

1. **Desktop Claude Code vs CLI agent registry**: This session (desktop) couldn't see grunt/mule in smoke test. They're in the standard `~/.claude/agents/` path. May be a desktop-vs-CLI split. The dashboard is the ground truth - if cheap-share stays 0.0%, routing isn't happening.

2. **`git add -A` is forbidden** in this shared dirty checkout. Only explicitly named files. Commits must name exact paths.

3. **Never show Max code** without explicit permission. Plain English only. Plain ASCII, no emoji/arrows/checkmarks. Write for TTS (ear, not eye). TLDR at top and bottom.

4. **`subprocess.run` on Windows with `pythonw.exe`**: Must pass `creationflags=0x08000000` (CREATE_NO_WINDOW) to suppress console flash. Already done in snapshot.py.

5. **WebFetch gotchas**: docs.claude.com redirects to code.claude.com. Large fetched files get auto-persisted to tool-results files - grep those instead of re-reading.

6. **`~/.claude/settings.json` no longer pins `"model": "opus"`** even though global2 says it should. Not acted on - may be intentional or may need checking.

7. **DeepSeek offload tools already exist** at `C:/claude_base/tools/deepseek_offload/` and `C:/claude_base/tools/headless_deepseek/` - not touched in this session. Separate system tracking out-of-pocket costs.

8. **Non-interactive usage (Agent SDK, `claude -p`) draws from a separate monthly credit pool** since June 15 2026, not the interactive allowance. Relevant if Max uses headless Claude.
