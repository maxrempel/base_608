# Scribe handover - milestone 1 (~96K tokens)
# session: 20260621_suspicious_leakey_ea2f52_6fa4eb29
# cwd: C:\claude_base\.claude\worktrees\suspicious-leakey-ea2f52
# written: 2026-06-21 18:00:21 by deepseek-v4-pro

# HANDOVER - Lekarstva Calendar Update Session

## GOAL (in Max's words)
Max wants to update the Lekarstva calendar on tamza with dates provided by Ira Barabash. The critical meta-instruction is: **do not fix anything**, only watch that Max doesn't mess things up himself ("?????? ?? ?????, ?????? ?????, ????? ? ??? ?? ??????????").

The calendar entries to add:
- **27 ????** - guest Leonid Vaksman, host Vita
- **4 ????** - NOT Lekarstva, it's Felix Krivizna's poetry
- **11 ????** - guest Vitaly Basenok, host Vita
- **18 ????** - guests: the Shapiro brothers, host Ed Prizant

There's also an earlier note from Ira: Uzlaner confirmed on August 1 that he can record, and she's waiting - Ira said "don't book him yet" ("???? ?? ?????????, ??????????").

## DECISIONS + WHY
No decisions have been made yet. The session was interrupted during discovery.

## CURRENT STATE
Claude ran preliminary discovery:
- Found a repository at `C:/claude_base/tamza/lekarstva_gosti/`
- Read a file `gosti_table_v01_20260513.md` - but this is a guest count/table, NOT the calendar
- Searched for `tamza_calendar` and `tamza ext:py` in the codebase but results weren't reviewed before interruption
- **No edits have been made to anything.**

The actual Lekarstva calendar location on tamza.com has NOT yet been identified.

## EXACT NEXT STEP
Max needs to:
1. Locate the actual Lekarstva calendar (not the guest statistics table)
2. Enter the four dates Ira specified
3. Ensure the July 4 entry is marked as poetry, not Lekarstva
4. Leave Uzlaner's slot open (Ira is still waiting on that)

## OPEN QUESTIONS
- Where is the actual calendar file? The `gosti_table_v01_20260513.md` was a guest count, not a schedule.
- Is the calendar on tamza.com (a website) or in a local file under the worktree?
- What format does the calendar use?

## KEY PATHS/IDS
- Worktree: `C:\claude_base\.claude\worktrees\suspicious-leakey-ea2f52`
- Lekarstva guest directory: `C:/claude_base/tamza/lekarstva_gosti/`
- Guest table (NOT calendar): `C:/claude_base/tamza/lekarstva_gosti/gosti_table_v01_20260513.md`
- Base repo: `C:\claude_base`
- Search tool: `C:/claude_base/tools/es/es.exe`

## GOTCHAS
- Max explicitly said **do not edit anything** - Claude's role is observation/oversight only, not proactive fixing.
- The guest statistics table (`gosti_table_v01_20260513.md`) is a dead end for calendar editing - it's a different document type.
- Uzlaner's slot is still unconfirmed per Ira's August 1 message - do not book it.
