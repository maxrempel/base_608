# Scribe handover - milestone 6 (~92K tokens)
# session: 20260608_strange_hawking_e9654d_f28a49f9
# cwd: C:\moma\.claude\worktrees\strange-hawking-e9654d
# written: 2026-06-08 10:49:08 by claude-opus-4-8

# Handover - moma "Line Combining into a Single Lispie"

## GOAL (in Max's words)

"The task here is to implement line combining into a single lispie." Max discovered that **Wan26flash (Wan 2.6 flash) is capable of alternating speakers** - you put the instruction in the description field and it actually alternates the speakers (this succeeded at least once). So the working assumption is: we can now make scenes with an **unlimited number of lines** - normally 2-6 - where two or more speakers speak in turn, all rendered into a single audio file.

Max wants a **full cycle rework of the moma system to allow merging of lines.**

## DECISIONS + WHY

- **Merging is triggered by Max's command** to any new session, phrased loosely like "merge lines 2, 3, 4." The system must accept this informal command.
- **The merge must be "fool proof" in Notion**, using "some smart marks we need to invent" - e.g. marking that a run of lines (say lines 2-4) collapses into one MP3 file.
- **The SASS (the splitting/assembly script) needs rework:** it should still split the lines as usual, but then **assemble the combined run** into one unit. Name the assembled artifact something like `lines2-4`.
- **Pipeline flow:** the assembled combination is named (`lines2-4`) ? lifted to SB ? **replaces the current multiple lines via libup**.
- **The core principle / the real point of this rework:** sessions (LLMs) routinely *skip instructions*. So correctness must be **enforced programmatically, not just by a command in memory.** Max wants "programmatic control over sloppiness of LLM" - the format must be *forced* by code, not trusted to the model following written guidance.
- **Division of labor for the Notion edit:** the Notion script edit should be done **largely by hand by the LLM**, but possibly **assisted by a script template** - Max said "that would be cool," so the template idea is desirable but not mandatory. The goal: the script in Notion is **formally perfect**, and everything downstream is **propagated programmatically** from that perfect source.

## CURRENT STATE

- This is the very start of the work session - **no tool calls, no files read, no code written yet.** Max has just laid out the task verbally.
- The Wan26flash alternating-speakers capability has been **validated at least once** (proven possible, not yet productionized).
- Nothing about the merge mechanism, the "smart marks," the SASS rework, or the libup replacement has been implemented or inspected yet.

## EXACT NEXT STEP

Begin by **orienting in the actual moma codebase** before designing anything:
1. Locate and read the **SASS** script (the line splitter/assembler) to understand how lines are currently split and named.
2. Understand the existing **SB lift** and **libup** steps so the "replace multiple lines with one merged line" flow can hook in correctly.
3. Understand the current **Notion** representation of lines/scripts so the new "smart marks" can be designed to be programmatically parseable.

Then propose the design: (a) the Notion mark convention for "these N lines = one MP3," (b) how SASS detects the marks, splits, then assembles the run into `lines2-4`, (c) the lift-to-SB and libup-replace logic, and (d) the programmatic enforcement that prevents a sloppy session from producing the wrong format.

## OPEN QUESTIONS (awaiting Max)

- What exactly should the **"smart marks"** in Notion look like? Max wants us to *invent* them - needs a proposal and his sign-off.
- Should the **Notion edit use a script template**, or be done purely by hand by the LLM? Max likes the template idea ("that would be cool") but left it open.
- What is the precise final **naming convention** - is `lines2-4` literal, or just illustrative?
- What does "programmatic enforcement" concretely block/validate - at the SASS stage, the lift stage, or both?

## KEY PATHS / IDS / NAMES

- **cwd:** `C:\moma\.claude\worktrees\strange-hawking-e9654d`
- **SASS** - the script that splits lines and (newly) must assemble combined runs.
- **SB** - destination the assembled audio is "lifted" to.
- **libup** - the step that replaces the multiple original lines with the single merged line.
- **Notion** - source of truth for the formally-perfect script; edited largely by hand.
- **Wan26flash (Wan 2.6 flash)** - the model that alternates speakers via the description field.
- Artifact naming pattern: `lines2-4` (a merged run of lines 2 through 4 ? one MP3).

## GOTCHAS

- **Do not rely on memory-only instructions to enforce the format.** Max's central concern is that sessions skip instructions; the whole point is to make the correct format *impossible to get wrong programmatically*. Any design that "just tells the LLM to do it right" misses the goal.
- The Notion script is the **formally perfect source**; everything else is **propagated from it programmatically** - don't invert this.
- Typical scenes are 2-6 lines but the system should treat the line count as **unlimited**.
- Wan26flash alternating speakers has only succeeded **at least once** - treat reliability as not-yet-confirmed; the merge feature assumes it works but this assumption may need re-validation.
