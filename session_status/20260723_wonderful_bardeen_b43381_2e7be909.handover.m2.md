# Scribe handover - milestone 2 (~169K tokens)
# session: 20260723_wonderful_bardeen_b43381_2e7be909
# cwd: C:\claude_base\.claude\worktrees\wonderful-bardeen-b43381
# written: 2026-07-23 14:08:56 by deepseek-v4-pro

# HANDOVER - IONS Grant Deadline (Starseed Genetics / Strieber + Steinfeld)

## GOAL (in Max's words)
"Locate the deadline for the submission of the grant which I was planning to submit on Starseed Genetics with Striber and Alan Steinfeld."

The grant is for a project on **Starseed Genetics**, with **Whitley Strieber** and **Alan Steinfeld** listed as advisors/collaborators.

## WHAT WAS FOUND

The grant is the **IONS prize** - the **Institute of Noetic Sciences** award for consciousness-related UFO research. Prize value: **$100,000**.

### Deadlines
- **Stage 1 - Letter of Intent: July 22** (had just passed at time of search; session appeared to be on or about July 23)
- **Stage 2 - Full Proposal: September 7** (only if invited after LOI)

## DECISIONS + REASONING

1. **Searched broadly first** - Claude ran file system searches, Memex searches, and email searches in parallel because your initial phrasing ("Striber" not "Strieber," "Starseed Genetics" not a formal name) meant the exact grant name was unknown.

2. **Spelling variants handled on the fly** - "Striber" was corrected to "Strieber" during search; the system searched both variants across multiple tools (Memex, semantic mail, file system).

3. **Escalated to email deep search** - When file/Memex searches didn't immediately surface the deadline, Claude searched your semantic mail index for "grant proposal deadline" and "Strieber Steinfeld grant," plus ran Gmail thread searches via the MCP email tool.

4. **Found it in actual email threads** - The definitive answer came from pulling full Gmail threads (three threads were retrieved) that contained the IONS prize details. This is authoritative because it came from the actual correspondence, not a local file.

## CURRENT STATE

- **Done:** Grant identified (IONS prize, $100K), both deadlines confirmed (July 22 LOI, Sept 7 full proposal).
- **In flight / unresolved at session end:** Claude ended by flagging that the **July 22 LOI deadline had just passed** (by ~1 day at time of session). It is unknown whether you actually submitted the letter of intent. Claude offered to check whether the LOI went out or whether IONS might still accept a late one.

## EXACT NEXT STEP

1. **Determine LOI status** - Did you submit the July 22 letter of intent?
   - Check your sent email for anything to IONS around July 21-22.
   - Check IONS submission portal for confirmation.
2. **If LOI was submitted:** Next milestone is **September 7** - the full proposal deadline. All effort should pivot to preparing that.
3. **If LOI was missed:** Ask Claude to investigate whether IONS accepts late LOIs (check the email threads for contact person / flexibility language), and draft a quick outreach.

## OPEN QUESTIONS AWAITING MAX

- Did you actually submit the LOI by July 22?
- If not, do you want Claude to check whether IONS still accepts it and help draft a late-submission email?
- What is the actual project title as submitted (or planned)? "Starseed Genetics" may be a working name - the formal name may differ in the grant materials.

## KEY PATHS / IDS

- **Google Drive grant folder:** `/g/My Drive/00Main2026/xg project/advena grant proposal 50209/`
- **Broader project folder:** `/g/My Drive/00Main2026/xg project/`
- **Email search script:** `C:/claude_base/tools/semantic_mail/search_cf.py` (searches semantic mail index using Python venv at `C:/Users/maxre/semantic-mail/.venv`)
- **Enterprise Search index:** Indexed at `advena` (searched via ES at `/c/claude_base/tools/es/es.exe`)
- **MCP email tool:** Thread retrieval worked for Gmail searches on "IONS" and "grant" variants - this is the fastest path to re-find the original emails.

## GOTCHAS

- **"Striber" is a typo** - the collaborator is **Whitley Strieber**. File/Memex searches using "Striber" returned nothing; "Strieber" found matches. Always correct this.
- **"Starseed Genetics"** may not be the formal project name - it didn't return clean hits in file structures. The Google Drive folder is under `advena grant proposal 50209`, which may be the actual grant ID or project codename.
- **The LOI deadline was July 22** and the session ran on approximately July 23. If you didn't submit, this is a time-sensitive problem - every day counts for late-submission pleading or pivoting to the next opportunity.
- **The IONS prize is a two-stage process** - no full proposal can be submitted without passing the LOI stage. Confirming LOI status is the single blocking dependency for all further work.
