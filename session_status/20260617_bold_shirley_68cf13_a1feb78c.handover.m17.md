# Scribe handover - milestone 17 (~257K tokens)
# session: 20260617_bold_shirley_68cf13_a1feb78c
# cwd: C:\claude_base\.claude\worktrees\bold-shirley-68cf13
# written: 2026-06-17 13:22:29 by deepseek-v4-pro

# Scribe Handover - Starseed Genetics Letter Archive & Keyword Expansion

## GOAL (Max's words)
"Review letters, find good keywords and keep expanding the finds." He stated there should be around 15-30 threads, not just the 5-7 initially found and archived.

## DECISIONS MADE + WHY
- **Built a letter-handling system from scratch** because no rules doc existed before. Stored at `C:\claude_base\tools\starseedgenetics\`, committed to git.
  - `starseedgenetics_letters_method_v01_tomemex.md` - 8 rules, known correspondents, Gmail search keywords (initial set), template index.
  - Three templates: full experiencer reply, short trio/register, DNA-data-received.
  - `reference_past_replies/ARCHIVE_max_replies_to_public_v01.md` - collected all sent replies from known correspondents (Ethan Jones, Anthony George, Kasie Damico, Francis, Valentina, Anne-laure, and Gav as unanswered).
  - A pointer in `global2.md` so future sessions auto-discover this system.
- **Initial undercount acknowledged.** Claude's first search used only narrow experiencer/DNA terms and project mailboxes, but didn't paginate fully and wrongly dismissed UFO-community/fringe-science threads as "noise." Max corrected: far more threads exist (~15-30). Decision: broaden inclusion criteria - all correspondence that touches on the DNA/experiencer/starseed topic, even tangentially (e.g. MUFON video invites, "Science of Resonances," WiFi-sensing guy, fernanselva, etc.) should be archived.
- **Storage philosophy:** Text files (rules, templates, archives) go in the claude_base git repo. Raw DNA/genotyping data stays in Nextcloud (xg1_data) due to size and privacy.

## CURRENT STATE
- The letter system folder and initial archive exist and are committed/pushed to `master` on `github.com/maxrempel/claude_base`.
- The initial archive (`ARCHIVE_max_replies_to_public_v01.md`) contains **5 people's** threads, plus notes on Gav (unanswered) and the broader correspondents. That's far below Max's estimated 15-30.
- Valentina and Anne-laure were found later, bringing distinct correspondents to ~7, but still incomplete.
- The method doc includes an initial keyword list from Gmail searches, but Max is now questioning exactly which keywords were used and wants a full enumeration.

## EXACT NEXT STEP
1. **Enumerate all keywords used so far** in Gmail searches for this project. The transcript shows:
   - `starseed`
   - `xg1`
   - The project mailbox addresses: searches like `from:mass@tamza`, `to:mass@tamza`, `starseedgenetics.com` (mailbox for the site).
   - Possibly others Claude used before like "DNA insert", "experiencer", etc. Need to explicitly list them.
2. **Expand the search comprehensively** using:
   - All project mailboxes (`mass@tamza`, `contact@starseedgenetics.com`, any forwarding addresses, Gmail aliases).
   - Broad subjects: "DNA", "insert", "alien", "hybrid", "experiencer", "starseed", "XG1", "23andMe", "genetics project", "MUFON", "UFO", "contactee", "Rh-negative" (because of the Kasie Damico angle).
   - Known sender names and domains (protonmail, hotmail.fr, gmail.com, etc.).
   - Keyword combinations: the earlier search missed threads from people like Jay Albertson, franco.ivaldi, fernanselva, and others.
   - **Paginate fully** - the transcript shows Claude stopped after page 1 for several searches. Need to retrieve all pages.
3. **Collect all matching threads** - fetch the full thread content for every identified correspondent, not just the 7 already in the archive.
4. **Update the archive file** to include all newly found replies and correspondents, organized clearly.
5. **Update the method doc** (`starseedgenetics_letters_method_v01_tomemex.md`) with the complete, expanded keyword list so future sessions don't repeat this undercount.

## OPEN QUESTIONS (AWAITING MAX)
- **Inclusion threshold exactly how broad?** Should all UFO-community or fringe-science threads be included, or only those where Max actually replied with project information? (From Max's reaction, it seems "all" is the answer, but clarity is good.)
- **Are there other Gmail accounts or labels** that might contain relevant correspondence (e.g., Max might have forwarded some to another address, or used labels like "starseed")? The search so far used `search_threads` without label filtering.
- **Should the archive include only Max's sent replies**, or also the incoming original letters where Max hasn't replied yet?
- **Any other data sources** where past correspondence might live (e.g., Nextcloud email backups, WhatsApp, Telegram)? Claude only searched Gmail.

## KEY FILES & PATHS
- `C:\claude_base\tools\starseedgenetics\` - the entire letter system.
- `C:\claude_base\tools\starseedgenetics\starseedgenetics_letters_method_v01_tomemex.md` - method/rules doc (keyword list lives here).
- `C:\claude_base\tools\starseedgenetics\reference_past_replies\ARCHIVE_max_replies_to_public_v01.md` - current (incomplete) archive.
- `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md` - contains the pointer to the starseedgenetics folder for auto-discovery.
- Gmail MCP server: `mcp__d1237438-8996-485f-bbb2-aa5b2e7dda32` with tools `search_threads` and `get_thread`.
- Project mailboxes known: `mass@tamza`, possibly `contact@starseedgenetics.com`, plus Max's primary Gmail (the session is authenticated to his account).

## GOTCHAS / DEAD ENDS RULED OUT
- **Do NOT** share raw DNA files; the project doesn't work that way. Gav's request to compare DNA on GEDmatch is a dead end scientifically - it only shows human relatedness. The correct method needs a family trio. This is already in the method doc.
- **Avoid** narrow searches: using only `starseed` or `xg1` as keywords missed many correspondents. Project mailboxes and broader community terms are essential.
- **Paginate fully**: Claude stopped at page 1 for some searches in this session, which is why many threads were missed. A cold session must ensure it retrieves all pages of results for each search query.
- **The "noise" category** was too aggressively applied; many threads initially dismissed (journalists, newsletters) might contain conversations worth archiving. The default should be to include unless clearly irrelevant (e.g., automated newsletters with no personal exchange).
- **The archive file** is version 1, but the final archive should be renamed/updated with the full set before Max considers it done.
