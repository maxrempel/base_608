# Scribe handover - milestone 8 (~602K tokens)
# session: 20260622_loving_bell_d1fb51_6e1df7d2
# cwd: C:\claude_base\.claude\worktrees\loving-bell-d1fb51
# written: 2026-06-22 10:51:08 by deepseek-v4-pro

# HANDOVER - Semantic Gmail Search (E10?E12)

## GOAL (Max's words)
Build a way for Claude to semantically search Max's Gmail - find old emails by meaning, not keywords. Must work on **Claude Code (laptop), Claude web, and Claude Android app**. Privacy is explicitly NOT a concern ("fuck privacy"); the only worry is Google not closing the account. Must include PDF/DOCX attachment contents in the search, and keep a full archive of every email + attachment.

---

## DECISIONS MADE + WHY

1. **Rejected all off-the-shelf tools** (Zemail, Context Link, Shortwave, Missive, Gmelius, retrieveIT) - they were either unproven, laptop-only, or standalone apps that don't feed Claude. The phone requirement killed everything local.

2. **Built our own pipeline** using `semantic-mail` (yahorbarkouski) as base, heavily rewritten:
   - **Embeddings:** OpenAI `text-embedding-3-small` (cheap, fast, cloud-based - privacy doesn't matter).
   - **Vector store:** Cloudflare Vectorize (index `max-emails`, 1536-dim cosine, separate from Memex's `claude-memory`/`babel` so Gmail junk never touches Memex).
   - **Archive:** Every `.eml` + all attachments saved to teal16 (Centauri D:\, 12.9 TB free, path `D:\mail_archive\`).
   - **Attachments:** PDF and DOCX text extracted and indexed; images saved but not embedded.
   - **Pipeline host:** asto (AstolfoDebian, always-on Debian box, Liz's old PC) - replaced Pine because Pine is a laptop that sleeps. Pine now only runs searches (which just query Cloudflare).
   - **Self-healing:** Watchdog cron on asto (`@reboot` + every 15 min) relaunches the driver if it dies. `loginctl enable-linger` enabled so processes survive SSH logout.

3. **Two query paths built:**
   - **Claude Code (laptop):** E11 built the `semanticgmail` skill that calls `search_cf.py` directly against Cloudflare.
   - **Web + Android:** E10 deployed a Cloudflare Worker (`gmail-mcp-search.max-rempel2.workers.dev`) as a remote MCP connector. You add its URL once in claude.ai ? Settings ? Connectors, and it syncs to Android.

4. **Indexing method:** Month-by-month, most-recent-first, resumable via a `chunks_done_full.txt` checkpoint file. Each month: fetch Gmail API ? extract body + attachments ? embed ? upsert to Cloudflare ? move `.eml`+attachments to teal16 ? delete local stage. One long-email truncation bug fixed (emails >8192 tokens were killing whole batches).

5. **Budget:** Using OpenAI embeddings. Roughly a few dollars for the full 505k emails (already spent). Cloudflare Workers + Vectorize within free tier.

---

## CURRENT STATE

- ? **Full backfill COMPLETE** - 503,209 of ~505,000 emails indexed (99.6%), all ~270 months from June 2026 back to 2004. Logged as "FULL-ARCHIVE v02 DONE" 2026-06-22 13:30.
- ? **Cloudflare Worker deployed and live** - confirmed responding to MCP `initialize` handshake.
- ? **Max added the connector URL** to claude.ai (just done - the last user action in the transcript).
- ? **Freshness/incremental sync** - NOT yet set up. New incoming mail won't auto-appear in the index.
- ? **Lak backup** of the rebuild-source (teal16 archive) - requested but not done yet.

---

## EXACT NEXT STEP - Max's question: "what command to tell cl chat to actually use it?"

The connector Max just added auto-discovers its tools. The Worker exposes a tool called **`search_gmail`**. Once the connector is saved in claude.ai, Claude on web and Android should automatically know about it.

**Max should just ask naturally** - something like:

> *"Search my Gmail for the Expedia flight confirmation from 2023"*

or

> *"Find any email about the rental agreement with the Paris address"*

Claude will invoke `search_gmail` automatically. No special command syntax needed.

If it doesn't work (Claude says it can't search or doesn't know about the tool), the likely issue is that claude.ai's connector flow expects a different transport (e.g. streaming MCP, or OAuth even when not needed). That's the gap to debug next - but try the natural query first.

For **Claude Code specifically**, the existing `semanticgmail` skill (E11's wrapper) is already in the skill list and can be used with the same natural-language queries.

---

## OPEN QUESTIONS

1. **Does the connector actually show the `search_gmail` tool in claude.ai?** If the natural query above doesn't trigger it, we need to harden the Worker's transport to match claude.ai's connector expectations.
2. **Freshness** - does Max want a daily incremental sync so new mail stays current? (Asto already has the pipeline; just needs a cron job.)
3. **Lak backup** - still pending. Teal16 already holds the rebuild source; Lak would be a secondary mirror.

---

## KEY PATHS, IDs, COMMANDS

| Thing | Value |
|---|---|
| **Cloudflare Worker (connector URL)** | `https://gmail-mcp-search.max-rempel2.workers.dev/mcp/Beyfo7uPMsE7yGuyIWCsbNfPZ_4uz-ho` |
| **Cloudflare account** | `e4dc2224d6baa721873dca77dc6f057d` |
| **Vectorize index** | `max-emails` (1536-dim, cosine) |
| **CF API token** | `zSyncMain\ssh\cloudflare_vectorize_token_20260304.txt` |
| **Code (on Pine)** | `C:\claude_base\tools\semantic_mail\` |
| **Worker source** | `C:\claude_base\tools\semantic_mail\gmail_mcp_worker\src\index.js` |
| **Search helper (local)** | `C:\claude_base\tools\semantic_mail\search_cf.py` |
| **Vectorize helper** | `C:\claude_base\tools\semantic_mail\cf_vectorize.py` |
| **Archive driver** | `C:\claude_base\tools\semantic_mail\full_archive_driver.py` |
| **Archive index worker** | `C:\claude_base\tools\semantic_mail\archive_index.py` |
| **Method doc** | `C:\claude_base\tools\semantic_mail\semantic_mail_method_v02_tomemex.md` |
| **Archive on teal16** | `D:\mail_archive\` (Centauri, 192.168.1.176, ssh key `~/.ssh/sol_key`) |
| **Asto SSH** | `rempel@astolfodebian.tail251d88.ts.net` (key `~/.ssh/bitwarden_ed25519`) |
| **Asto pipeline dir** | `~/semantic-mail/` (inside ubuntu distrobox container) |
| **Asto watchdog** | `~/semantic_mail_tools/watchdog.sh` + cron (`@reboot` + `*/15 * * * *`) |
| **Google OAuth client** | `zSyncMain\ssh\google_contacts_oauth_20260522.json` (project `stalwart-coast-240620`) |
| **OpenAI key** | `zSyncMain\ssh\openai_api_key_20260216.txt` |
| **Gmail account** | `max.rempel2@gmail.com` (read-only scope) |
| **Git repo** | `C:\claude_base` - pushed to master |
| **Bot name** | E10 (was the engine builder), E12 (new branch taking over the connector work) |

---

## GOTCHAS / DEAD ENDS ALREADY RULED OUT

- **Zemail, Context Link, ragmail, semantic-mail (stock):** All rejected - either unproven, laptop-only, or wrong shape for a 505k mailbox.
- **IMAP:** Not dead, but password-IMAP is. Gmail API + Takeout (both OAuth) are the correct modern methods.
- **Pine as pipeline host:** Laptop sleeps - causes silent multi-hour pauses. Migrated to asto.
- **asto container dying on SSH logout:** Root cause was `Linger=no` - systemd killed the user session and container. Fixed with `loginctl enable-linger`.
- **`nohup` not detaching inside distrobox:** Replaced with `setsid` for true detachment.
- **Backup JSONL clobbered on teal16:** `_vectors` was a file, not a directory - each month overwrote the last. Fixed by making it a directory.
- **Long emails killing batches:** OpenAI embedding API rejects >8192 tokens per input. Patched the embedder to truncate with tiktoken + fall back to per-item on batch failure.
- **Duplicate messages:** These are a known bug in the Claude Code app. Added to `global2.md` - treat them as app bugs, not fresh requests. Don't re-execute.
- **Report in years, not months** - Max asked for this explicitly (e.g. "back to 2019, ~7 years done").
- **Gmail index is SEPARATE from Memex** - `max-emails` is its own index. Gmail bulk never touches Memex's `claude-memory`/`babel`.
- **Google account safety:** All access is via official OAuth with read-only scope (`gmail.readonly`) - cannot send or delete. Zero account-closure risk.

---

## TO INVOKE THE SEARCH NOW

Max just needs to ask Claude naturally in any chat (web, Android, or Claude Code):

> *"Search my Gmail for [whatever I'm looking for]"*

The MCP connector on web/Android exposes `search_gmail`; the `semanticgmail` skill handles Claude Code. No special command needed - Claude discovers the tool automatically from the connector.
