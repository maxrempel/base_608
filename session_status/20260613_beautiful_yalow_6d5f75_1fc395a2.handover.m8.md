# Scribe handover - milestone 8 (~120K tokens)
# session: 20260613_beautiful_yalow_6d5f75_1fc395a2
# cwd: C:\claude_base\.claude\worktrees\beautiful-yalow-6d5f75
# written: 2026-06-13 13:25:20 by claude-opus-4-8

# HANDOVER - XG1 Starseed Forms Workflow + Registrant Outreach

## GOAL (in Max's words)
"Got new google forms entree. locate starseed forms workflow and update database and tell me what is new." - Then, after the workflow fix: "use your mass email to ask them questions as assistant." Most recently, when asked which registrants to email, Max replied: **"the ones that didn't tell much. ahah"** - meaning send the questions only to registrants whose form submissions were thin/incomplete (not the ones who already gave full detail).

## DECISIONS + WHY
- **Switched the workflow's master trigger from one sheet to Gmail form-notification emails.** Reason: the old recipe only read the "simple" XG1 form's response sheet. Max actually has multiple XG1 forms (a short/simple one, a big detailed questionnaire, and a subscriber/newsletter list). Anyone using a different form was invisible to the DB sync. Every form emails Max a "new form response" notification, so those emails are now the reliable master trigger - then check every response sheet against the DB, matching by name OR email.
- **Added the missing person found by this investigation.** Abdurasul Otadjanov (Dilara Abdieva's husband) had filled the detailed questionnaire back in 2024 and was never added - sat missing ~2 years. Inserted as DB **id 39**.
- **Kept the subscribers form OUT of the contacts import (for now).** Reason: newsletter email-only signups (Barry Zusa, Stacey, Alex, etc.) are a different category from experiencer registrations. Flagged as an open question rather than auto-importing.
- **Treating mass email as a one-way, confirm-before-fire action.** Claude proposed who/what and waited for explicit "go" rather than sending blind.

## CURRENT STATE
- Workflow doc edited and **committed/pushed** (git commit made in C:\claude_base). The fix to the single-sheet blind spot is done.
- Abdurasul Otadjanov inserted as id 39 and verified in the DB.
- Mass email is **NOT yet sent.** Claude had proposed sending 3 questions to all 14 registrants from mass@tamza.com. Max then narrowed the target: only the registrants "that didn't tell much" - i.e. those with sparse/incomplete submissions.

## EXACT NEXT STEP
Identify which registrants gave thin/incomplete answers (vs. those who already provided full detail), then send the assistant-voice email with the trio/DNA questions to that subset only. You will likely need to re-read the response sheets to judge who "didn't tell much." Confirm the final recipient list with Max before sending (one-way action). The 3 proposed questions:
1. Can you provide a complete trio - yourself + both biological parents - all willing to sign consent? If a parent is deceased/unavailable, say who's missing.
2. Are you willing to give a saliva DNA sample (we mail a kit)?
3. Do you already have raw DNA data (23andMe / AncestryDNA) you could share?

## OPEN QUESTIONS (awaiting Max)
- Exactly which registrants count as "didn't tell much" - confirm the subset before sending.
- Should the subscribers-form people (Barry Zusa, Stacey, Alex, etc.) be added as contacts too, or kept separate as just subscribers? (Still unanswered.)
- Whether to include the 3 detailed-form people (Dilara, Abdurasul, Alison) in the outreach.
- The 3 questions as-is, or different ones Max has in mind.

## KEY PATHS / IDS / NAMES
- Workflow doc: `C:\claude_base\tools\xg1_starseed_forms\xg1_starseed_forms_method_v01_tomemex.md`
- Repo root for commits: `C:\claude_base`
- Mass email sender: **mass@tamza.com** (assistant voice + auto-signature)
- DB: Cloudflare D1 (queried via d1_database_query MCP)
- New row added: **id 39 = Abdurasul Otadjanov** (Dilara Abdieva's husband)
- 14 experiencer registrants currently in DB: Lottie Bowater, Suzanne Matteson, Jyoti Paramjyoti, Ann Carter, KarenMarie Gensheimer, Zuzanna Vee, Young Brinson, Doug Kohl, Jordan Maxwell, Stanislav Kernc, Jesse Sayranian, Jose Garcia, Anya Krupski, Anthony George.
- Detailed-form people: Dilara, Abdurasul, Alison.
- MCP tools in use: Google Drive (read_file_content, search_files), Cloudflare D1 (d1_database_query), Gmail (search_threads). Load via ToolSearch.

## GOTCHAS / DEAD ENDS RULED OUT
- The "new entry" Max expected was NOT in the live simple-form sheet - that sheet's newest was still Anthony George (6/12), already in the DB. The real issue was the multi-form blind spot, not a fresh submission to the monitored sheet.
- Do NOT trust a single response sheet as the source of truth - there are 3+ XG1 forms. Use the Gmail form-notification emails as the trigger and cross-check every sheet.
- Match registrants by name OR email when reconciling against the DB (people may differ slightly across forms).
- Subscribers form ? experiencer registrations - don't auto-merge them.
- Max's "ahah" is amused agreement, not a new instruction; the actionable content is "the ones that didn't tell much."
