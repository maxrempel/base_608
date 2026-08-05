# Scribe handover - milestone 7 (~108K tokens)
# session: 20260617_agitated_austin_f89ae3_aa23f003
# cwd: C:\claude_base\.claude\worktrees\agitated-austin-f89ae3
# written: 2026-06-17 08:36:30 by deepseek-v4-pro

## HANDOVER - COLD SESSION START

### GOAL (in Max's words)
`Update global2 - low CPU and low memory chrons go on dax. , high drive capacity jobs go on lak, only if needed. Sol might come back, so once it is back, more goes on sol, since lak is needed for high responsibility long term funcitons such as nextcloud. Cent is less valuable - some things can go on sol. If needed, another computer Lis's is avialble. we probably will offload Lak's work to Liz's comp, to reduce wear. Lak is needed for nextcloud and other things. For genomics high cpu and memory jobs, we witilll either restore sol or spin an aws VM. termporarily.`

(The session originally aimed to set up a 20?minute mass@tamza inbox check, then duplicate it to "Clawy" for phone access. The user redirected at the end to fix deployment rules in global2, which will decide where the mail?check job itself should live.)

---

### DECISIONS MADE + WHY
1. **mass@tamza periodic check**  
   - Built `mass_check_v01.py` (IMAP reader, read?only, filters out Healthchecks.io noise, returns digest).  
   - Scheduled via the `wakeup.py` long?term timer (your tool) at a 20?minute interval.  
   - Why 20 min: you asked for it after initially thinking hourly.  
   - Key constraint: the wakeup timer only fires when a session is alive in the same worktree; it can survive sleep, but not a killed session.

2. **Clawy duplication (mail on phone) - NOT YET DONE**  
   - Clawy is an OpenClaw agent on **Sol** (192.168.1.113) with a Telegram plugin - that's how you use it from the phone.  
   - The idea was to replicate the check there, but Sol is unreliable (bad RAM, frequently freezes).  
   - I proposed an alternative: run the mail check as a cron on **Lak** (reliable, always?on) and push the digest to the same Telegram channel (so phone gets it).  
   - That discussion was interrupted before a decision. The new deployment rules you just gave may change the answer (Dax might be better for cron jobs now).

3. **Instruction gap: "context homework" rule**  
   - You were frustrated that I didn't know about Clawy and didn't automatically search Memex.  
   - After refinement, we settled on a rule for `global2.md` (autoloaded instructions):  

     > **IF A COMMAND IMPLIES CONTEXT YOU DON'T KNOW - DO HOMEWORK BEFORE ASKING**  
     > Max often gives commands assuming Claude knows the context. If context is implied and you don't know it:  
     > (1) check the autoloaded instructions - they hold short descriptions + paths pointing to fuller files that are *referenced but not themselves autoloaded*; if a description matches, open that file.  
     > (2) If not found, search Memex - the semantic database that auto-ingests all memories and all session reports.  
     > (3) If still not found, ask Max. Never ask without doing this basic homework first.  
   - This was written to `global2.md` and you gave a "perfect" on the wording. *One caveat*: the edit may have clobbered a previous imperfect version I'd inserted earlier, but the final committed version should be the correct one (verify).

---

### CURRENT STATE
- **mass_check tool**: exists at `C:\claude_base\tools\mass_check\mass_check_v01.py`, with an IMAP read?only method, tested live (101 messages, mostly noise). It uses IMAP credentials from `C:\Users\maxre\Nextcloud\zSyncMain\ssh/` (the file named something like `mxroute_creds`).  
- **Wake timer**: currently set to **every 20 minutes** (`wakeup.py add --in 20 minutes`, job ID `a963c9c8`). It fires the check and prints the digest to the terminal.  
- **Clawy duplication**: completely open. No code on Sol or Lak. The Telegram push idea is drafted but nothing built.  
- **Instruction fix**: committed and pushed to `global2.md` (autoloaded from Nextcloud). The new "context homework" rule is present.  
- **Deployment rules for jobs**: **Not yet updated**. Your final directive to add the server?assignment logic to `global2` is the immediate next step.

---

### EXACT NEXT STEP
1. **Edit `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md`** (or the canonical autoloaded version you use). Add your deployment rules as a new section - probably right after the context?homework rule, or in the system?roles section.  
   - Write verbatim: low CPU/memory cron jobs ? **Dax**; high drive?capacity jobs ? **Lak** (only if needed); Sol will return and then more goes there; Cent is less valuable; Liska's computer available; Lak is for high?responsibility long?term (Nextcloud); genomics high CPU/memory ? either Sol (when restored) or an AWS VM temporarily.  
2. **Re?evaluate the mass mail?check job**: now that Dax is the home for low?intensity cron, the 20?min check should be moved from the laptop's session?dependent timer to a **cron on Dax**. Decide whether to keep the terminal?output approach or pivot to a Telegram push (for phone access) - that's for you to choose.  
3. **If you want phone access**, the Telegram push via Lak (or Dax) can be built - likely just a cron that runs a Python script to check mail and send a message to your existing Telegram bot. That script can reuse `mass_check_v01.py`'s IMAP logic.

---

### OPEN QUESTIONS (awaiting Max)
- **Where exactly should the periodic mail check live now?** Dax? Keep it on the laptop for now?  
- **Do you still want the phone?accessible version** (Telegram push), or was that just a passing thought?  
- **Is the "context homework" rule in global2 satisfactory** as written, or do you want the trigger refined further (the "instead of producing it from training" bit you found "not a good formula" earlier)?  
- **What is the canonical location of global2.md** - is it the Nextcloud path I wrote to, or another copy that auto?loads?

---

### KEY PATHS / IDs
- IMAP reader: `C:\claude_base\tools\mass_check\mass_check_v01.py`  
- Its doc: `C:\claude_base\tools\mass_check\mass_check_v01_tomemex.md`  
- IMAP creds: `C:\Users\maxre\Nextcloud\zSyncMain\ssh/` (look for mxroute file with `MASS_USER`, `MASS_PASS`)  
- Wake listener: `C:\claude_base\tools\wake_listener\wakeup.py`  
- Autoloaded instructions: `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md`  
- Memex search tool: `mcp__memex__memex_search` (MCP tool available)  
- Clawy KB (if needed): `/home/maxre/Nextcloud/00_clawy_kb/`

---

### GOTCHAS / DEAD ENDS
- **Worktree confusion**: you found it amusing I used the term "worktree" - note that I now use "session directory" for clarity. No functional difference.  
- **Memex didn't return Clawy on first search** - I killed the search because you stopped me. Later, a second search (the assistant did) returned the definition. So Memex works, but may need exact queries.  
- **The initial attempt to add the context rule** was botched (I wrote a poor formula, you stopped it). The refined version is in global2, but verify the file hasn't been corrupted by the interrupted edit.  
- **Sol is explicitly unreliable** - I warned about it. The "restore Sol" statement in your new rules implies you're planning to fix it, but for now, don't depend on Sol for any scheduled actions.  
- **Lak is flagged as precious** - nextcloud and other high-responsibility tasks. In the new rules, high?drive?capacity jobs "go on Lak, only if needed." So a light mail check likely doesn't qualify; it belongs on Dax.

**Start here for the cold session:** open `global2.md` and write in those deployment rules verbatim, then decide where the mail check should actually run.
