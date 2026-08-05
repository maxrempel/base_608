# Scribe handover - milestone 2 (~176K tokens)
# session: 20260801_priceless_snyder_07082c_e1b7b06f
# cwd: C:\claude_base\.claude\worktrees\priceless-snyder-07082c
# written: 2026-08-01 13:29:17 by deepseek-v4-pro

## Handover: MSSNG Data Access for Autism WGS Trios (Point + Omega NPA)

### GOAL (in Max's words)
"My recommendation: kick off MSSNG access now (the data is the long pole), and I can prep the pipeline alongside. Want me to start digging into MSSNG's access requirements - check what the application needs and whether we hit the same institutional/IRB questions - the same careful 'verify before applying' pass I did for SSC? Or would you rather I point at a different branch?"

(Translation: get whole?genome autism trios to replicate the 1000G point+omega NPA analysis. SSC is blocked - open MSSNG.)

### DECISIONS MADE + WHY
1. **MSSNG selected over other resources** - all three old dbGaP grants (project 42416) yielded only exome or SNP?array data, no whole?genome. EGA/MalariaGEN not autism. SSC (SFARI Base) best fit but institution "unconfirmed," so blocked. MSSNG independent, self?contained, no dbGaP federation.
2. **Verification?before?applying pass completed on MSSNG** - the assistant read the actual MSSNG access application form and Data Access Agreement. Three key checks:
   - **University affiliation?** Not required. The form explicitly says "if any" for institution; if unaffiliated, Researcher signs alone. Transposon/DRRF qualifies.
   - **Separate signing official (like SFARI's SBSO)?** No. If no institution, only Researcher signature.
   - **Local IRB/ethics approval?** Almost certainly waivable. Required only "if required by local laws," with a "No - provide justification" box. Standard justification: secondary analysis of de?identified, already?consented data.
3. **Filing under Transposon recommended** - per Max's standing rule (future filings from Transposon unless continuation of an earlier one).
4. **Application components identified** - title, lay summary, ~500?word research question with references, feasibility section with a 5+ publication list. Max clears the publication threshold easily (4,500 citations). No fee; data on Google Cloud (CRAM + BigQuery), compute paid by the researcher.

### CURRENT STATE
- The assistant finished digging into MSSNG requirements and confirmed **no institutional/IRB blockers** (unlike SSC).
- Assistant **offered to draft the full MSSNG application** (research question built around point + omega NPA replication on autism trios) - **draft only, not submit**, per the standing rule that no letters/registrations are finalized without Max's OK.
- The assistant is **waiting for Max's "go"** to start drafting.
- SSC remains parked on SFARI's reply (Oksana emailed Tisshawrn to confirm the institution; reply goes to Max's Gmail).

### EXACT NEXT STEP
**Max must approve the application draft.** Once Max says "Go," Claude will:
- Write the full application text (title, lay summary, research question, feasibility/publications) under Transposon.
- Hold it for Max's review and send/no?send decision.

If Max prefers a different branch (e.g., wait on SSC, explore another dataset, reconsider institutional affiliation approach), they should specify.

### OPEN QUESTIONS (awaiting Max)
- Any specific framing or emphasis for the research question? (e.g., de novo mutation rate, specific phenotypes, cohort subsets)
- Any preferred contact person/affiliation details for the application (Transposon as legal entity, etc.)?
- Does Max want the assistant to also note any Google Cloud setup steps alongside the application?

### KEY PATHS / IDs / DOCUMENTS
- **MSSNG portal:** https://research.mss.ng/
- **MSSNG application form (PDF):** fetched and read from the session's working directory (`C:\Users\maxre\.claude\projects\C--claude-base--claude-worktrees-adoring-grothendieck-7efff2\e1b7b06f-604e-4c8a-ab19-51c27b30572f\tool-results\webfetch-17842321` - file name likely `webfetch-17842321`).
- **DbGaP project 42416** - exhausted (no WGS studies).
- **SFARI SSC request** - staged, pending Oksana's institution confirmation email; watch Max's Gmail.
- **Worktree of the dead session:** `wizardly-perlman-b98acf`, transcript file `af0a7d77-0056-4444-a4f9-20ed4a728e.jsonl` (used for resurrection only).

### GOTCHAS / RULED OUT
- **SSC institution wall** (Signing Official requirement) is why we're not waiting on it; MSSNG has no such wall.
- **Old dbGaP grants** - triple?checked study by study; all exome or SNP?array, no WGS.
- **Any other autism WGS source** - none found with a simpler gate than MSSNG.
- **Standing rules reminder:** don't finalize anything without Max's OK; use Transposon for new filings; bw for 2FA; vocalize if Claude needs input.
