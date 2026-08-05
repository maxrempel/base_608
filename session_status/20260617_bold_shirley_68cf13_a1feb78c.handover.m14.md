# Scribe handover - milestone 14 (~222K tokens)
# session: 20260617_bold_shirley_68cf13_a1feb78c
# cwd: C:\claude_base\.claude\worktrees\bold-shirley-68cf13
# written: 2026-06-17 13:21:22 by deepseek-v4-pro

# HANDOVER - Starseed Genetics Letter System Build (Session: bold-shirley-68cf13)

---

## GOAL (Max's words, from the session)

1. **Add a rule to global2.md**: When a session is retired/waiting, it must report rule inconsistencies, housekeeping issues, folder/machine structure problems - including all autoloaded files. Log to `rule_inconsistencies_tomemex.md`. Also note that "obvious exceptions" shouldn't be reported - Max overrides rules when needed, because Claude is fuzzy/guessing like a human mind, not a deterministic Python program.

2. **Respond to Gav's Gmail**: Gav (prospekt221@gmail.com) is an experiencer who saw tabloid coverage about Max's DNA insert finding. He wants Max's RAW DNA file to compare against his own on GEDmatch. Max said: review the starseed project in Memex, review the site, read past replies in Gmail, then think about what to reply.

3. **Build a starseedgenetics letter-answering system**: Subfolder, rules/method doc, templates, and collect all past replies for reference.

4. **Last question**: "how many letters did you find?" (already answered - 5 public correspondents).

---

## DECISIONS MADE + WHY

### global2 rule addition
- **Where**: Added new section to `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md`
- **Log file name**: Max originally said `rule_inconsistensies_to_memex.md`, but Claude changed it to `rule_inconsistencies_tomemex.md` because the Memex auto-scanner requires the `_tomemex` suffix. **Max was notified and did not object.**
- **Created**: Empty log file at `C:\claude_base\rule_inconsistencies_tomemex.md`

### Gav's request - the scientific dead end
- Reviewed Memex: `Project Starseed Genetics - A Crowdsourced Hunt...` (the research proposal) and `starseedgenetics.com`
- **Key finding**: Comparing Gav's DNA to Max's on GEDmatch would ONLY show human relatedness (are they cousins). It CANNOT detect alien inserts. The actual method requires a family trio (mother + father + adult child) with long-read sequencing to find sequences present in the child but absent from both parents.
- **Decision**: Do NOT share Max's raw DNA file. Instead, redirect Gav to the proper method - his own family trio, start with 23andMe, register via the site.

### The letter system build
- **No prior rules/templates doc existed** - this is brand new.
- **Subfolder created**: `C:\claude_base\tools\starseedgenetics\`
- **Method doc**: `starseedgenetics_letters_method_v01_tomemex.md` - 8 rules, Gmail search keywords, known correspondents list, template index, resources.
- **3 templates created**:
  1. `template_experiencer_reply_v01.md` - full Ethan Jones-style reply (warm, validates experience, reframes as "powers not damage," redirects to trio method)
  2. `template_register_trio_v01.md` - short Anthony George-style (practical, "start with 23andMe and register")
  3. `template_dna_data_received_v01.md` - acknowledgment template for when DNA data arrives
- **Reply archive**: All Max's past sent replies collected into `reference_past_replies/ARCHIVE_max_replies_to_public_v01.md`
- **global2 pointer added**: So future sessions auto-discover the system.
- **Repo decision**: Committed to claude_base repo (GitHub). Text only - raw DNA data stays in Nextcloud (xg1_data), not in git.

### The count
- **5 distinct public correspondents** found in Max's Gmail:
  1. **Ethan Jones** - experiencer in crisis (answered, long warm reply)
  2. **Anthony George** - DNA inquiry (answered, short practical script)
  3. **Kasie Damico** (originally called "Casey") - Rh-negative angle, offered to volunteer/help (answered, fundraising + outreach angle, NOT the trio script - distinct case)
  4. **Francis** - (answered)
  5. **Gav** (prospekt221@gmail.com) - **UNANSWERED**, the current open item

---

## CURRENT STATE

### Done
- ? global2 rule added + log file created
- ? Memex searched, starseedgenetics.com reviewed
- ? Max's past Gmail replies read and archived
- ? Letter system built: folder, method doc, 3 templates, reply archive
- ? global2 pointer added
- ? Committed + pushed to GitHub (`master`, commit `0024a9ef`)
- ? The count answered: 5 public letters

### In Flight / Not Yet Done
- ? **Gav's reply has NOT been drafted or sent.** The analysis is complete but the draft was never written.

---

## EXACT NEXT STEP

**Draft Gav's reply using the new template.** Max said "very good, read my past replies to others in gmail" and agreed with the approach of redirecting Gav to his own trio + the site. The draft should:
- Use Max's house style (Ethan Jones model but lighter tone since Gav is measured/scientific, not in crisis)
- Validate his experiencer background
- Gently explain why GEDmatch DNA comparison can't detect inserts (shows only human relatedness)
- Redirect to the real method: his own family trio, 23andMe, register at starseedgenetics.com
- Link starseedgenetics.com and published work
- **Send from**: mass@tamza or Max's Gmail (Max asked "Send from your Gmail as a reply, or via mass@tamza?" - this was never answered)

---

## OPEN QUESTIONS (awaiting Max)

1. **Gav's reply**: Draft now? Send from mass@tamza or from Max's Gmail as a reply to Gav's thread?
2. **Which specific paper/site link** to include in Gav's reply? Just starseedgenetics.com, or a specific publication?
3. **The inconsistency-reporting rule**: Max accepted the filename change (spelling fix + `_tomemex` suffix), but this was a unilateral change - worth flagging in the log file itself.

---

## KEY PATHS, IDs, NAMES

| Item | Path/ID |
|---|---|
| global2.md | `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md` |
| Inconsistency log | `C:\claude_base\rule_inconsistencies_tomemex.md` |
| Letters method doc | `C:\claude_base\tools\starseedgenetics\starseedgenetics_letters_method_v01_tomemex.md` |
| Template: experiencer | `C:\claude_base\tools\starseedgenetics\templates\template_experiencer_reply_v01.md` |
| Template: trio/register | `C:\claude_base\tools\starseedgenetics\templates\template_register_trio_v01.md` |
| Template: DNA received | `C:\claude_base\tools\starseedgenetics\templates\template_dna_data_received_v01.md` |
| Reply archive | `C:\claude_base\tools\starseedgenetics\reference_past_replies\ARCHIVE_max_replies_to_public_v01.md` |
| GitHub commit | `0024a9ef` on `master`, repo: `github.com/maxrempel/claude_base` |
| Starseed site | `https://starseedgenetics.com` |
| Memex proposal | "Project Starseed Genetics - A Crowdsourced Hunt..." |
| Gav's email | `prospekt221@gmail.com`, thread ID in Gmail tools |
| Ethan Jones thread | (fetched, in reply archive) |
| Anthony George thread | (fetched, in reply archive) |
| Kasie Damico thread | (fetched, in reply archive - Rh-negative, volunteer case, NOT trio) |
| Worklog | `C:/claude_base/compaction_kb/scripts/worklog.py` |

---

## GOTCHAS

1. **`_tomemex` suffix is REQUIRED** for Memex auto-ingestion. Max's original filename `rule_inconsistensies_to_memex.md` wouldn't work. Claude changed it. Max was told. Future sessions: don't "fix" it back.

2. **Kasie Damico ? "Casey."** Her angle is Rh-negative and volunteering, not the standard trio path. Her reply used a different template (fundraising/outreach). Don't mix her up with the experiencer-template correspondents.

3. **Raw DNA data stays in Nextcloud** (`xg1_data`), NOT in the git repo. The repo is text-only for rules/templates/archives. The large private files are elsewhere.

4. **The template folder exists at `C:\claude_base\tools\starseedgenetics\templates\`** - all 3 templates are v01. When editing for Gav, either edit inline in a draft or create a new template variant (v02) if diverging significantly.

5. **Gmail tool IDs**: The MCP server IDs for Gmail are `d1237438-8996-485f-bbb2-aa5b2e7dda32` (Gmail) and `876d399f-e171-42f5-a4dd-c5b1a0d2ca4a` (Memex). Use `search_threads` and `get_thread` on the Gmail server.
