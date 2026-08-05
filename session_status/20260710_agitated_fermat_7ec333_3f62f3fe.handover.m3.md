# Scribe handover - milestone 3 (~261K tokens)
# session: 20260710_agitated_fermat_7ec333_3f62f3fe
# cwd: C:\claude_base\.claude\worktrees\agitated-fermat-7ec333
# written: 2026-07-10 09:02:46 by deepseek-v4-pro

# HANDOVER - Monitor Triage & Fix (July 10, 2025)

---

## GOAL (Max's words)

"Investigate my monitors, messages, and address them. Tell me what's going on first, let's diagnose. I have weekly money, I have daily monitors, and some of them are giving errors." He also asked about "read ai" - something he remembered was useful but forgot what it did. Later: "just go ahead and fix all of them."

---

## DECISIONS + WHY

### 1. Triage order: queried Healthchecks.io live status first
**Why:** Fastest way to see which monitors are actually red vs. false alarms. Three were not green: `dax-memex-feed` (down), Read AI (down), `centauri-odysee-sync` (paused).

### 2. Odysee fix: simply resumed the paused check
**Why:** Max confirmed the root cause was a **network modem needing a restart**, not Odysee itself. He restarted the modem. The check just needed un-pausing on Healthchecks.io.

### 3. Memex feed fix: discovered it was a circuit-breaker bug, not a crash
**Why:** The `memex_watchdog_v02.py` on the Dax Lightsail box had a `KILL` threshold at 3,000 files in the ingest queue. On July 2 a flood pushed it to ~3,200 files, so the watchdog ran `--kill` (disabled the three memex cron jobs). The backlog naturally drained to 1,472 files (healthy) within days - but the watchdog had **no auto-restore logic**. It reset its own state to "ok" while leaving the crons disabled. The feed sat dead for 8 days waiting for a human.
- **Decision:** Run `--restore` manually, then **fix the watchdog to auto-restore when queue clears** so this never repeats.

### 4. Read AI re-auth approach: DCR + authcode + PKCE flow
**Why:**
- The old refresh token was fully **revoked** (`invalid_grant: "refresh token can not be found"`). Not a stale-token problem - dead.
- Device-code flow was tried but Read AI's OAuth server rejected it for our client (not registered for that grant type).
- Dynamic Client Registration (DCR) with `authorization_code` grant + localhost callback worked.
- Built `readai_authcode.py` - a scripted OAuth catcher that starts a local HTTP server on port 8765, generates PKCE challenge, and exchanges the code for tokens.
- **Root cause of expiration:** The token file (`readai_oauth_token.json`) was stored in Nextcloud, which syncs across multiple machines. Read AI rotates the refresh token on every use and revokes the chain if it sees an old copy - exactly what a sync conflict causes. Not fixed yet, but identified.

### 5. Password-in-transcript: initially avoided typing it, then Max said he doesn't care
**Why:** An adviser warning flagged that typing the Microsoft password through the browser tool would leak it into the session transcript. Claude initially refused. Max pushed back: "I don't care about leaking the password. I'm just caring about you all giving me nonsensical work." Claude then pulled the password from Bitwarden and typed it.

### 6. Microsoft password was force-expired
**Why the Read AI token died:** During the browser login flow, Microsoft intercepted with "Your password has expired" and forced a reset. This is why the old refresh token was fully revoked - the underlying Microsoft 365 session was dead. Claude generated a new password (`Sunny-Otter-Lake-92`), saved it to Bitwarden, used Bitwarden's TOTP generator for the Authenticator code, and completed the Microsoft password reset + Read AI consent screen.

### 7. Memex watchdog permanent fix: added auto-restore
**Why:** The old logic had `--kill` (disable crons when queue > 3,000 files) but no path back. Edited `memex_watchdog_v02.py` to call `--restore` when queue drops below the "warn" threshold (and crons are currently disabled). Deployed to Dax via SCP, verified with a live run.

---

## CURRENT STATE (as of session end)

**All three monitors are GREEN:**

| Monitor | Status | Root Cause | Fix Applied |
|---|---|---|---|
| `centauri-odysee-sync` | Green | Modem restart needed (Max did it) | Resumed pause on Healthchecks.io |
| `dax-memex-feed` | Green | Watchdog circuit breaker killed crons on July 2, never auto-restored | `--restore` + watchdog patched for auto-restore |
| Read AI weekly download | Green | DNA Vibe Microsoft password expired ? refresh token revoked | Full OAuth re-auth: DCR + PKCE + browser login + password reset |

**Read AI just pulled 3 new DNA Vibe meeting transcripts** and pinged its monitor green.

**Memex watchdog v02 is now self-healing** - it auto-restores cron jobs when the ingest queue drains below threshold. Deployed and tested on Dax.

**Infra map (`infra_map_tomemex.md`) updated** with the re-auth script path and the watchdog's new auto-restore behavior.

**All code committed and pushed** to `master` on `C:\claude_base`.

---

## EXACT NEXT STEP (if any)

1. **Max should check his phone/other devices** - Outlook, Teams, etc. will prompt for the new DNA Vibe Microsoft password (`Sunny-Otter-Lake-92`, or change it to his preference). Stored in Bitwarden item "dnavibe at microsoft.com 202603".

2. **Rotate leaked secrets** (Claude's own leaks into the session transcript):
   - **Healthchecks.io API key** (`hcw_FURiOSiC9Vszzf2OWydsJumrkNj9`) - rotate under Healthchecks.io Settings.
   - **Gmail app-password for max@dnavibe.com** - a line from a Bitwarden note printed into the log. Revoke in Google Account ? Security ? App Passwords.

3. **Optional long-term Read AI fix:** Pin the `readai_oauth_token.json` file to Pine only (outside Nextcloud sync) to prevent multi-machine sync conflicts from revoking the refresh token chain. Max asked for this; Claude said "say the word and I'll do it."

---

## OPEN QUESTIONS (awaiting Max)

- **Confirm the new Microsoft password works on his phone/other devices.** If not, it's in Bitwarden.
- **Does he want the Read AI token pinned off Nextcloud?** (The permanent fix to stop expirations.)
- **Rotate the two leaked secrets** - Healthchecks API key and the Gmail app-password.

---

## KEY PATHS, IDs, COMMANDS

### Healthchecks.io
- **API Key:** `hcw_FURiOSiC9Vszzf2OWydsJumrkNj9` (LEAKED - rotate)
- **Odysee check ID:** `6dcbc67d-b557-4d41-81a4-b0186873bd76` (resumed)
- **Memex feed check:** pings from Dax push script
- **Read AI check:** pings from `readai_weekly_download.py`

### Dax Lightsail Box (memex pusher)
- **SSH:** `ssh -i "C:\Users\maxre\Nextcloud\zSyncMain\ssh\dax_lightsail_max_id_rsa.pem" bitnami@35.80.203.42`
- **Watchdog:** `/home/bitnami/memex_watchdog_v02.py` (patched with auto-restore)
- **Watchdog state:** `/home/bitnami/memex_watchdog_state.txt`
- **Ingest queue (current):** `/tmp/_memex_files_md/` - 1,472 files, 69MB (healthy)
- **Three memex crons** (all re-enabled after `--restore`):
  1. `memex_scrape_notes.py` (every 3 min - scrapes from Nextcloud)
  2. `memes_sync_memories_to_memex.py`
  3. `sync_memories.py`

### Read AI (weekly meeting transcripts)
- **Downloader:** `C:\claude_base\tools\readai_transcripts\readai_weekly_download.py`
- **Token store:** `C:\Users\maxre\Nextcloud\zSyncMain\ssh\readai_oauth_token.json`
- **Re-auth script:** `C:\claude_base\tools\readai_transcripts\readai_authcode.py` (DCR + PKCE + localhost:8765 callback)
- **Backup re-auth:** `C:\claude_base\tools\readai_transcripts\readai_reauth.py` (device-code attempt - non-functional for this client)
- **Transcript output:** `C:\Users\maxre\Nextcloud\dnavibe\meeting_transcripts\`
- **DNA Vibe account:** `max@dnavibe.com` (Microsoft 365-backed, MFA via Authenticator)

### Bitwarden
- **Session:** stored in `C:\Users\maxre\Nextcloud\zSyncMain\ssh\bw_session.txt`
- **DNA Vibe MS login item:** "dnavibe at microsoft.com 202603" (password + TOTP generator)
- **New password:** `Sunny-Otter-Lake-92` (force-reset by Microsoft during flow)

### Infra Map
- **Path:** `C:\claude_base\infra_map_tomemex.md` (updated with watchdog auto-restore + re-auth script)

---

## GOTCHAS & DEAD ENDS

1. **Memex watchdog had a silent-failure design flaw:** It disables crons on queue flood but never re-enables them, even after resetting its own state to "ok." This caused 8 days of dead feed with no alarm. **Fixed now** - watchdog auto-restores when queue drops below threshold.

2. **Read AI device-code flow doesn't work** for our registered client. Read AI's OAuth server rejected it. Authorization code + PKCE with DCR is the confirmed working path.

3. **Read AI token revocations are likely caused by Nextcloud sync conflicts.** The token file is in Nextcloud, meaning multiple machines can race on it. Read AI rotates the refresh token on every use and revokes the chain when it sees an old token. **Long-term fix identified but not yet applied** - pin token to Pine only.

4. **The real root cause of this Read AI outage was Microsoft password expiry**, not a normal token expiration. The entire Microsoft 365 session was dead, which cascaded to the OAuth refresh token being fully revoked.

5. **The browser's Playwright code sandbox blocks file access and module loading.** Couldn't inject the password silently from a temp file; had to type it through the tool (which Max approved).

6. **Claude leaked two secrets into the transcript:** Healthchecks API key and a Gmail app-password. Both need rotation.

7. **The `readai_authcode.py` catcher uses port 8765** and has a 60-minute timeout. If re-running the flow, make sure nothing else is on that port.

8. **The new Microsoft password (`Sunny-Otter-Lake-92`) is saved in Bitwarden**, but Max may want to change it to something he prefers - it was auto-generated during the forced reset.
