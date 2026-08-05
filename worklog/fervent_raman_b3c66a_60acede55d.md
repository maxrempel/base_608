
## [2026-06-19 11:26] ? d7337ba9
- DID: Set up persistent Bitwarden ext in Playwright MCP (profile+config+arg patch, doc committed); created Notion DNA Vibe Meetings DB under DNA Vibe Essentials w/ today's row (Perry hosting, 15 attendees)
- STATE: Bitwarden live after CC restart; Playwright lock released; meeting transcripts link is in an email from Tony@dnavibe -- use Gmail connector not Playwright
- NEXT: Find Tony's email w/ transcripts link, pull transcripts into the meeting notes

## [2026-06-19 11:42] ? d7337ba9
- DID: Wired Bitwarden+Grammarly to persist in Playwright MCP (load-extension flags in pw_mcp_config.json, persistent profile C:\claude_base\playwright_profile, patched .claude.json for C:\moma + worktree). Verified both service workers load. Built Notion DNA Vibe Meetings DB w/ today's row. Found read.ai transcripts shared by Tony to max@dnavibe (behind login).
- STATE: Playwright lock released (browser closed). Extensions need CC RESTART to appear in MCP browser.
- NEXT: After restart: Max logs into BW (maxrempel@icloud.com)+Grammarly once; logins persist. Optional: pull read.ai transcripts into Notion meetings DB.

## [2026-06-19 12:53] ? d7337ba9
- DID: Set up fast Playwright Chromium (NOT chrome) with persistent profile + Bitwarden+Grammarly extensions; fixed Chrome-137 load-extension block (use Chromium) and Grammarly OAuth (pinned official ID via manifest key). Verified BW login persists across restarts, Grammarly login works. Added global2 rule + session report (both pushed). Built Notion DNA Vibe Meetings DB w/ today's row.
- STATE: DONE: extensions work+persist; configs pushed. MCP picks up Chromium+ext after next CC RESTART. read.ai transcripts located but not yet pulled into Notion.
- NEXT: After CC restart: pull read.ai weekly-huddle transcripts into DNA Vibe Meetings DB (try mcp__readai connector, else magic-link via Gmail connector).
