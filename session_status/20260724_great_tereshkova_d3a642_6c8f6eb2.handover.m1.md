# Scribe handover - milestone 1 (~119K tokens)
# session: 20260724_great_tereshkova_d3a642_6c8f6eb2
# cwd: C:\claude_base\.claude\worktrees\great-tereshkova-d3a642
# written: 2026-07-24 11:24:29 by deepseek-v4-pro

# HANDOVER: DeepSeek Token-Offloading Strategy

---

## GOAL (in Max's own words)

Max is burning through weekly token limits on multiple platforms (Claude cloud desktop, Codex cloud desktop) in 3-4 days, even while trying to conserve. He's paying the maximum $200/month plan on each. He wants to offload substantial thinking to DeepSeek to stretch his token budgets, but when he told Codex to use DeepSeek, "it just didn't - it can't figure out how to do that." He's asking for a concrete, researched plan for how to route heavy thinking to DeepSeek in a way that actually fits into his production workflow.

---

## DECISIONS + WHY

1. **Recognized the core mismatch:** The DeepSeek tool that already exists on Pine (`headless_deepseek/provider.py`) only activates for fully *unattended background jobs*, not for interactive foreground chat. So the expensive token burn is happening in the main chat session regardless of that tool existing, because there's no automatic handoff mechanism.

2. **Identified the real gap:** The heavy reasoning work has to physically *leave* the foreground session, run as a separate DeepSeek job, and return a compressed answer. Codex failed to set this up because there's no automatic switch - someone has to explicitly wire each heavy task for handoff. This explains why "use DeepSeek" as an instruction to Codex did nothing.

3. **Posed a clarifying question (unanswered):** Asked whether Max wants a full research dive into a concrete auto-routing plan, or just the short version of the 2-3 known approaches now. This is the open fork in the conversation.

---

## CURRENT STATE

- The session has only just begun (turn 3). Two tool calls were made:
  1. `ls` on `C:/claude_base/tools/headless_deepseek/` - directory exists but likely had no immediate output shown beyond confirming existence.
  2. Read the `README.md` at that path - confirmed the tool's architecture and its limitation (background-only).

- No research has been done yet. No plan has been drafted. No code has been written or modified.

---

## EXACT NEXT STEP

**Wait for Max's answer to the open question:**

> Does he want a full, researched concrete plan (with architecture, wiring, and production integration details for auto-routing heavy thinking to DeepSeek), or does he want the short version now (just the 2-3 known approaches summarized)?

Once he answers, the session should either:
- **If "full research":** Investigate online how people actually route foreground reasoning to cheaper models (DeepSeek via API, OpenRouter, LiteLLM proxy patterns, custom middleware, etc.), then produce a concrete implementation plan tailored to his Pine/Codex/Claude setup.
- **If "short version":** Deliver the 2-3 methods immediately without further research.

---

## OPEN QUESTIONS (awaiting Max)

1. Full researched plan vs. short summary - which does he want?

---

## KEY PATHS / IDS

- **DeepSeek tool directory:** `C:/claude_base/tools/headless_deepseek/`
- **Provider script:** `C:/claude_base/tools/headless_deepseek/provider.py`
- **README:** `C:/claude_base/tools/headless_deepseek/README.md`
- **Working directory:** `C:\claude_base\.claude\worktrees\great-tereshkova-d3a642`
- **Context window note:** ~119K real tokens used so far, summaries kick in near ~840K on a 1M window.

---

## GOTCHAS

- **The existing DeepSeek tool is NOT the solution** - it's background-jobs-only by design. Telling Codex or Claude "use DeepSeek" will fail silently because there's no foreground handoff path wired.
- **Codex already tried and failed** to figure this out on its own. Any solution will require explicit wiring by someone who understands the architecture, not just a prompt instruction.
- **Multiple platforms are all burning tokens simultaneously** - Max mentioned Claude cloud desktop, Codex cloud desktop, and possibly others. The solution likely needs to work across environments, not just one.
- **The session is early** - nothing has been built, decided, or ruled out yet beyond identifying that the existing tool doesn't solve the foreground problem.
