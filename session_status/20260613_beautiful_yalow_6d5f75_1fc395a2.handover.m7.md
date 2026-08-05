# Scribe handover - milestone 7 (~119K tokens)
# session: 20260613_beautiful_yalow_6d5f75_1fc395a2
# cwd: C:\claude_base\.claude\worktrees\beautiful-yalow-6d5f75
# written: 2026-06-13 13:24:35 by claude-opus-4-8

# HANDOVER - XG1 Starseed Forms Workflow

## GOAL (in Max's words)
"Got new google forms entree. locate starseed forms workflow and update database and tell me what is new." Then, after the investigation: "check email and investigate - can't be" (Max was certain a new entry existed). Finally: "hm... use your mass email to ask them questions as assistant."

## DECISIONS + WHY
- **Root-cause found:** The old workflow only read ONE of Max's XG1 forms (the "simple" form's response sheet). Max actually runs several XG1 forms - a short one, a big detailed questionnaire, and a subscriber/newsletter list. Anyone submitting via a different form was invisible to the DB sync. This was treated as a real bug, not a one-off miss.
- **Fix applied:** Workflow now uses Gmail "new form response" notification emails as the MASTER trigger (every form emails Max on submission), then cross-checks EVERY response sheet against the DB, matching by name OR email. Rationale: no single sheet can be a blind spot anymore.
- **Subscribers kept separate (for now):** Newsletter email-only signups (Barry Zusa, Stacey, Alex, etc.) were deliberately NOT imported as contacts, because they are subscribers, not experiencer registrations. This is the standing OPEN QUESTION.

## CURRENT STATE - DONE
- Investigated inbox; confirmed registrants arrive via 3+ different XG1 forms.
- Found the buried victim: **Abdurasul Otadjanov** (Dilara Abdieva's husband) filled the detailed questionnaire back in 2024, was never added - sat missing ~2 years.
- Inserted Abdurasul into the DB as **id 39**; verified the row landed correctly.
- Edited the workflow method doc (multiple edits: the blind-spot warning, the recipe, and the state sections).
- Committed and pushed the workflow fix to git.

## CURRENT STATE - IN FLIGHT
- Max's latest instruction is NEW and not yet started: he wants to use the **mass email tool** to email some group of people **as the assistant** to "ask them questions."

## EXACT NEXT STEP
Clarify and execute Max's mass-email request. Before sending, confirm:
1. **Who** is the audience - the registrants? the subscribers? a specific subset (e.g. people with incomplete form data)?
2. **What questions** does he want asked?
This connects to the open subscribers question - he may want to email subscribers to qualify them as experiencers. Load the mass-email MCP tool, draft the message in the assistant's voice, and show Max for approval before sending.

## OPEN QUESTIONS (awaiting Max)
- Should the subscribers-form people (Barry Zusa, Stacey, Alex, etc.) be added as contacts, or kept separate as subscribers only? (Asked, not yet answered.)
- Who exactly should the mass email go to, and what questions?

## KEY PATHS / IDS / NAMES
- Workflow doc: `C:\claude_base\tools\xg1_starseed_forms\xg1_starseed_forms_method_v01_tomemex.md`
- Repo root for commits: `C:\claude_base` (git committed from `/c/claude_base`)
- Worktree cwd: `C:\claude_base\.claude\worktrees\beautiful-yalow-6d5f75`
- DB: Cloudflare D1, queried via the d1_database_query MCP tool.
- Newly inserted contact: **Abdurasul Otadjanov = id 39**.
- The 14 already-synced registrants (from the simple form): Lottie Bowater, Suzanne Matteson, Jyoti Paramjyoti, Ann Carter, KarenMarie Gensheimer, Zuzanna Vee, Young Brinson, Doug Kohl, Jordan Maxwell, Stanislav Kernc, Jesse Sayranian, Jose Garcia, Anya Krupski, Anthony George (newest, 6/12). Plus one test row.
- MCP tools used: Google Drive (read_file_content, search_files), Cloudflare D1 (d1_database_query), Gmail (search_threads). Mass email tool NOT yet loaded - load via ToolSearch next.

## GOTCHAS / DEAD ENDS RULED OUT
- The "new entry" Max expected was NOT in the simple form's live sheet - that's why the first read showed nothing new. Don't re-investigate the simple sheet; the real answer was the multi-form blind spot, now fixed.
- There are THREE+ separate XG1 forms. Always check all response sheets, not just the simple one. The Gmail notification emails are the reliable master trigger.
- Subscribers list is a DIFFERENT category from experiencer registrations - don't conflate them when emailing or importing.
- Abdurasul is already inserted (id 39) - do not re-add him.
