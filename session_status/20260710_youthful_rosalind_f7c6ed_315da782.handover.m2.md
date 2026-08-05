# Scribe handover - milestone 2 (~153K tokens)
# session: 20260710_youthful_rosalind_f7c6ed_315da782
# cwd: C:\claude_base\.claude\worktrees\youthful-rosalind-f7c6ed
# written: 2026-07-10 14:39:29 by deepseek-v4-pro

## Handover: XG2 IONS Grant Proposal - July 10 session

### GOAL (Max's words)

Write a grant proposal for the IONS (Institute of Noetic Sciences) prize on consciousness-related UFO research. $100,000, first deadline **July 22**. The sequence is:

1. **Get the ChatGPT chat** (analysis already underway)
2. **Get data** (details to be pinned down once we see the chat)
3. **Finish the grant proposal letter**
4. **Invite three additional advisers** - the "Rose cold-heart" person (dictation garbled), the Stanford UFO researcher (almost certainly Garry Nolan), and Richard Dolan.

The work lives in the **XG2** subfolder (already created).

---

### DECISIONS MADE & WHY

- **XG2 folder created** at the start, per explicit request. This is the project home.
- **Email search** confirmed advisers already in the loop (Baranova, Krippner, Strieber, Steinfeld, Lamb). No need to re-send invites to them; they're done.
- **ChatGPT extraction tool** chosen: the `chatgpt_export` skill from `C:\Users\maxre\.claude\skills\chatgpt_export`. It's the robust method (injects JS into a share-link page to read the full conversation from in-memory React Router state). Dead ends documented in the skill file: DOM scrolling fails, curl-based extraction fails.
- **Share-link minting** is necessary because the given URL is a private `/c/` link. The skill doc says to use the logged-in Playwright browser to mint a share link via the backend API, then download the public share link with the CLI tool.
- **Playwright browser issue**: the session's Playwright browser is using an **isolated profile** (the persistently logged-in profile is held by another active session). Bitwarden extension is present but needs user to unlock and log in manually. The login won't persist, but it's fine for this one mint-and-download operation.

---

### CURRENT STATE

- **XG2 folder** exists, with a plan note saved:  
  `C:\claude_base\.claude\worktrees\youthful-rosalind-f7c6ed\XG2\PLAN_note_20260710_v01.md`  
  (Lists the order above, and flags the two unconfirmed adviser names.)
- **Email search** already completed: IONS prize details and adviser conversations from July 9 are identified.
- **ChatGPT export is blocked** waiting for Max to log into ChatGPT in the Playwright Chromium browser. The OpenAI login page (`https://auth.openai.com/log-in`) is open, ready for credentials. Bitwarden is in the toolbar.
- **The private chat URL** we need to export:  
  `https://chatgpt.com/c/6a4fcbd5-e69c-83ea-8f69-af9bec2edc7e`

---

### EXACT NEXT STEP

1. Max logs in to ChatGPT **in the existing Playwright Chromium window** (the one that shows "Welcome back"). He unlocks Bitwarden and fills credentials. He then tells Claude "in" (or "done").
2. Claude immediately:
   - Uses `browser_evaluate` to mint a share link (via the backend API: get bearer token, POST share create, PATCH to publish).  
   - Downloads the resulting `chatgpt.com/share/<id>` to a Markdown file (likely `XG2/chat_analysis.md`) using `chatgpt_export.py`.
   - Confirms the file size/chars and reports the successful grab.
3. After that, we proceed to **read/analyse the chat** (or mine it, but not inhale it all at once) and identify what "data" is needed to finish the grant letter.

---

### OPEN QUESTIONS (awaiting Max)

- **Who is "a Rose cold-heart"?** Dictation garbled this. Probably someone's name. Clarify so we can put it in the plan.
- **Is the Stanford researcher Garry Nolan?** He's the famous Stanford UFO researcher; confirm.
- **What specific data do you want to get?** (This will likely become clear once we have the ChatGPT analysis; but flag it now.)
- **Do you still want the proposal draft and adviser tracker in XG2, or just the plan note for now?** The original question "where do we start?" is still pending.

---

### KEY PATHS, IDs & COMMANDS

| What | Path / ID |
|------|-----------|
| XG2 folder | `C:\claude_base\.claude\worktrees\youthful-rosalind-f7c6ed\XG2` |
| Plan note | `.../XG2/PLAN_note_20260710_v01.md` |
| ChatGPT private chat | `https://chatgpt.com/c/6a4fcbd5-e69c-83ea-8f69-af9bec2edc7e` |
| Export CLI script | `C:/claude_base/tools/chatgpt_export/chatgpt_export.py` |
| Extractor JS | `C:/claude_base/tools/chatgpt_export/extractor.js` |
| Notion upload script | `C:/claude_base/tools/chatgpt_export/chatgpt_to_notion.py` |
| Notion internal token | `zSyncMain/ssh/notion_internal_token_20260319.txt` (for future uploads) |
| Bitwarden setup doc | `C:/claude_base/tools/playwright_bitwarden/bitwarden_persistent_setup_v01_tomemex.md` |
| Playwright launcher | `C:/claude_base/tools/playwright_bitwarden/pw_mcp_launch.py` |
| Project-level config | `C:/Users/maxre/.claude.json` (top-level `mcpServers.playwright` uses the launcher; the worktree's config overrides may be absent) |
| IONS prize first deadline | **July 22** |

---

### GOTCHAS & DEAD ENDS (do not repeat)

- **Never DOM-scroll the ChatGPT page** - virtualisation drops assistant messages. (Already known from `chatgpt_export` skill doc.)
- **Do not run extractor.js directly on the private `/c/` page** - it returns NOTFOUND; the share link must exist first.
- **The current Playwright browser is a throwaway profile.** Login in it will not persist. That's fine for this one export, but future exports may again need a manual login or the shared profile.
- **Bitwarden is present but not unlocked to Max's vault.** He must unlock it himself in that browser window; Claude cannot automate that step.
