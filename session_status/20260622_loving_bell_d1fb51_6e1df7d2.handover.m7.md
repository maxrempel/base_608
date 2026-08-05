# Scribe handover - milestone 7 (~598K tokens)
# session: 20260622_loving_bell_d1fb51_6e1df7d2
# cwd: C:\claude_base\.claude\worktrees\loving-bell-d1fb51
# written: 2026-06-22 10:46:33 by deepseek-v4-pro

# Handover: Gmail Semantic Search ? Claude on Android via Cloudflare

## Goal (in Max's own words)
Connect Claude on the Android app (and web and Claude Code) to Cloudflare so Claude can semantically search his entire Gmail - find old emails by meaning, including content inside PDF and DOCX attachments. Separate from Memex; Gmail junk must not pollute Memex.

## Decisions made and why

1. **Cloudflare Vectorize as the index** - chosen because Memex already lives there, and a remote index is required for the Android app (Claude on mobile can't reach a local index). The Gmail index is a separate Vectorize index called `max-emails` (1536-dim, cosine). It lives alongside Memex's `claude-memory` and `babel` indexes but is completely independent - Gmail junk never touches Memex.

2. **Archive on teal16** - full `.eml` files plus every attachment (PDF, DOCX, images) saved to `D:\mail_archive` on teal16 (Centauri, label "16tbRaid", 12.9 TB free). Each month is a subdirectory; images are saved but not indexed. The archive is the permanent record; the Cloudflare index is the fast search layer.

3. **Pipeline runs on asto (AstolfoDebian)** - an always-on Debian box in the home server room, not the sleeping laptop. The pipeline is resumable month-by-month, most-recent-first. It stages each month locally, pushes vectors to Cloudflare, moves the archive to teal16 via SCP, then deletes the local stage so Pine (the laptop) never fills up.

4. **OpenAI embeddings (text-embedding-3-small)** - cheap, private enough (privacy was explicitly waived), and runs server-side so asto just sends API calls.

5. **Remote MCP Worker on Cloudflare** - a Cloudflare Worker (`gmail-mcp-search.max-rempel2.workers.dev`) exposes a `search_gmail` tool via the Remote MCP protocol. It embeds the query with OpenAI, queries the `max-emails` Vectorize index, and returns results. Adding its URL once in claude.ai ? Settings ? Connectors syncs it to the Android app automatically.

6. **Attachment text indexing** - PDF and DOCX text is extracted (pypdf, python-docx) and folded into the search index. Images are saved to disk but not embedded.

## Current state

- **Full backfill COMPLETE** - 503,209 of ~505,000 emails indexed (all 270 months, 2004-2026). The driver logged "FULL-ARCHIVE v02 DONE" on 2026-06-22 13:30.
- **Cloudflare Worker deployed and live-tested** - returns real semantic results (tested with flight confirmation queries).
- **Archive** - complete `.eml` + attachments on teal16 (`D:\mail_archive\{YYYY-MM}\`), with per-month `_vectors/` backup JSONL.
- **Search usable** - via the `semanticgmail` skill in Claude Code, and via the Worker.
- **asto is self-healing** - watchdog cron relaunches the driver every 15 min if it dies; `loginctl enable-linger` is on so processes survive SSH logout.
- **The one remaining user action: paste the connector URL into claude.ai.** That's the only manual step; once done, the Android app will see it.

## Exact next step for Max (or E12)

Max needs to do this once in a web browser on claude.ai:
1. **Settings ? Connectors ? Add custom connector**
2. Name it **"Gmail Search"**
3. Paste this URL:
   ```
   https://gmail-mcp-search.max-rempel2.workers.dev/mcp/Beyfo7uPMsE7yGuyIWCsbNfPZ_4uz-ho
   ```
4. Leave OAuth blank, Save. Claude will discover a `search_gmail` tool.
5. Then on the Android app: Settings ? Connectors ? enable "Gmail Search". It syncs automatically.

After that, Max can say *"search my Gmail for the Expedia flight confirmation"* from his phone.

## Open questions (awaiting Max)

1. **Incremental freshness** - the backfill is a snapshot. New incoming mail isn't automatically added. Max was asked if he wants a once-a-day refresh; no answer yet.
2. **Lak backup of the rebuild-source** - Max asked for this earlier; teal16 holds the archive, but Lak doesn't have a copy yet. Still pending.
3. **After the connector is added** - verify it works end-to-end from the Android app.

## Key file paths and IDs

- Cloudflare account ID: `e4dc2224d6baa721873dca77dc6f057d`
- Cloudflare Vectorize index: `max-emails` (1536-dim, cosine)
- Cloudflare Worker: `gmail-mcp-search` at `gmail-mcp-search.max-rempel2.workers.dev`
- Connector URL (includes secret): `https://gmail-mcp-search.max-rempel2.workers.dev/mcp/Beyfo7uPMsE7yGuyIWCsbNfPZ_4uz-ho`
- OpenAI API key: at `C:\Users\maxre\Nextcloud\zSyncMain\ssh\openai_api_key_20260216.txt`
- Cloudflare Vectorize token: at `C:\Users\maxre\Nextcloud\zSyncMain\ssh\cloudflare_vectorize_token_20260304.txt`
- Google OAuth client credentials: `C:\Users\maxre\Nextcloud\zSyncMain\ssh\google_contacts_oauth_20260522.json` (project `stalwart-coast-240620`, reused)
- Pipeline source code (committed to master on branch): `C:\claude_base\tools\semantic_mail\`
  - `cf_vectorize.py` - Cloudflare Vectorize helper (list, create, upsert, query, stats)
  - `archive_index.py` - the worker that fetches emails, extracts attachments, embeds, upserts to CF
  - `search_cf.py` - CLI search against CF (used by the `semanticgmail` skill)
  - `full_archive_driver.py` - the month-by-month driver with disk guard, teal16 SCP move
  - `gmail_mcp_worker/` - the Cloudflare Worker (wrangler.jsonc, src/index.js)
- asto details:
  - Host: `astolfodebian.tail251d88.ts.net`
  - User: `rempel`
  - SSH key: `~/.ssh/bitwarden_ed25519` (on Pine)
  - Container: `distrobox enter ubuntu`
  - Pipeline lives at `~/semantic-mail/` with an env file at `~/semantic-mail-env`
- teal16 (Centauri):
  - IP: `192.168.1.176`
  - User: `maxre`
  - SSH key: `~/.ssh/sol_key`
  - Archive path: `D:\mail_archive\{YYYY-MM}\`
- Pine is not involved anymore (pipeline moved off it, search just queries Cloudflare).
- Method doc: `C:\claude_base\tools\semantic_mail\semantic_mail_method_v02_tomemex.md`

## Gotchas and dead ends already ruled out

1. **Do NOT re-index** - the backfill is done. A re-sent message from Max earlier was a Claude Code app duplicate; we treat duplicates as bugs, not new requests.
2. **Do NOT use the body-only local Chroma index** - that was a temporary first pass on Pine, now deleted because it would fill Pine's disk and is superseded by Cloudflare.
3. **The batch-truncation bug** - originally, a single >8192-token email killed the whole embedding batch. Fixed by truncating each email with tiktoken before embedding.
4. **asto `Linger=no` was the root cause of repeated silent deaths** - without `loginctl enable-linger`, systemd killed the container and driver on SSH logout. Fixed.
5. **`nohup` inside `distrobox enter` doesn't truly detach** - the process dies when the entry session ends. Fixed by using `setsid` in the watchdog launch.
6. **The `_vectors` directory on teal16 was originally a file** - each month's backup JSONL was clobbering the previous month. Fixed by making it a directory and having the driver ensure it exists.
7. **Do NOT confuse `max-emails` with Memex indexes** - they share a Cloudflare account but are separate indexes. Gmail bulk will never pollute Memex.
8. **The Android app does NOT support local MCP** - only remote MCP (Cloudflare Worker) works. All local-only tools (Zemail, ragmail, semantic-mail CLI) were therefore dead ends.
9. **Context Link was over-sold** - it had no real user reviews and wasn't designed for huge mailbox indexing. Ruled out.
10. **IMAP is not dead** - only password-based IMAP died. OAuth IMAP still works, but the pipeline uses the Gmail API (OAuth) anyway. Google Takeout was considered but the live API incremental approach won.
