# Scribe handover - milestone 1 (~94K tokens)
# session: 20260805_keen_swartz_9b1c30_e87c6bfb
# cwd: C:\claude_base\.claude\worktrees\keen-swartz-9b1c30
# written: 2026-08-05 08:35:15 by deepseek-v4-pro

**HANDOVER - DeepSeek Token?Saving Workers Recall Session**

**GOAL (in Max's words)**
> "In the past we were able to implement DeepSeek for saving tokens as workers. What do you know about it?"

Max wanted a summary of the existing DeepSeek offload/worker infrastructure - what was built, how it works, its current status, and any relevant context.

**DECISIONS + WHY**
No new decisions were made in this session. The assistant searched the codebase to recall the design rather than designer from memory, because the implementation is spread across multiple tool directories and worklogs. Everything described below is the *as?built* state, intended for cold?restart comprehension.

**CURRENT STATE (what was found and reported)**
- **Brokered offload runner** (`tools/deepseek_offload`) - The core token?saver.  
  *How it works:* You write a task packet as a plain file. Run the task runner. DeepSeek does the heavy reading/drafting with zero tools and no filesystem access. Only the thin `result.md` comes back into the expensive (Claude) session.  
  *Model choice:* Uses DeepSeek Flash by default; Pro reserved for "hard reasoning" only.  
  *Broker:* A hidden broker owns the API key, runs up to 4 jobs concurrently, fails closed (no fallback to paid models).  
  *Adoption:* ~37 projects have used it - OMEGA, RHD, Tamza, MoMA, Typer, monitors, etc.

- **Headless provider gate** (`tools/headless_deepseek`) - Pins any unattended agent process to DeepSeek V4?Pro (subagents get Flash) through DeepSeek's Anthropic?compatible endpoint.  
  *Safety:* If the API key is missing, the launch fails instead of silently falling back to a paid model.

- **Cost tracking** - Includes `deepseek_cost_projector` plus a spend dashboard with 20?minute balance snapshots, and a `token_budget` mechanism that measures the share of cheap?model work vs. expensive Claude work.

- **Routing hook** - A `PreToolUse` hook on the Agent tool that nudges toward grunt/mule/DeepSeek.  
  *Notable gotcha fixed today:* This hook was broken until today (the file was registered but missing), which silently blocked every subagent spawn on Pine. A sibling session fixed it this morning.

- **Philosophy baked in:** Judgment and dialogue stay with the expensive model; volume (reading, drafting, bulk processing) goes to DeepSeek or cheap subagents.

**EXACT NEXT STEP**
The session ended after the assistant delivered the summary. No further action was requested. The immediate next step is purely conversational: the user may ask follow?up questions, request a specific change, or give a new task. The assistant is ready to act on those.

**OPEN QUESTIONS (awaiting user)**
None explicitly from the assistant. The user has not yet indicated whether they need clarification, want to modify the implementation, or plan to use a specific part of the system.

**KEY PATHS / IDs / COMMANDS**
- `C:/claude_base/tools/deepseek_offload/` - Brokered offload runner (README, `enforce_offload.py`, etc.)
- `C:/claude_base/tools/headless_deepseek/` - Headless provider gate (README, scripts)
- `C:/claude_base/worklog/deepseek_offload/` - Historical worklogs (Git commit messages mention deepseek)
- `deepseek_cost_projector` and `token_budget` - Tracking tools, locations not fully enumerated but present in `tools/` and meta?config
- The routing hook fix was done in a sibling session; the exact commit/file not shown in this transcript but confirmed as repaired today.

**GOTCHAS ALREADY RULED OUT OR KNOWN**
- The routing hook silently blocking subagent spawns on Pine was a known issue; it was fixed today (morning) by a sibling session - no need to re?investigate.
- The API keys are managed by a hidden broker; manual key handling is not required.
- DeepSeek Flash is the default for brokered tasks; using Pro requires explicit override.
- The headless provider gate rejects launch if the key is missing; a cold session should not attempt to work around this - the failure is by design.
