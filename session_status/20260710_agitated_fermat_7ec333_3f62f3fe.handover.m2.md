# Scribe handover - milestone 2 (~161K tokens)
# session: 20260710_agitated_fermat_7ec333_3f62f3fe
# cwd: C:\claude_base\.claude\worktrees\agitated-fermat-7ec333
# written: 2026-07-10 08:36:56 by deepseek-v4-pro

# Handover - Session 2025-07-10

## GOAL (in Max's own words)
Address the unhappy monitors highlighted by Healthchecks:
- **Centauri Odysee Sync** (paused - Max already fixed the modem; just needs resuming).
- **Read AI** (weekly meeting transcript downloader - token expired; needs re-login and a permanent fix so it stops expiring).
- **Dax memex-feed** (memory pusher - silent for 8 days; needs fixing).

Max also wants to understand what "Read AI" is.

## DECISIONS AND REASONING

### 1. Centauri Odysee Sync - resumed via Healthchecks API
- **Why:** The monitor was paused (likely manually on July 4), but the root cause was the network modem, which Max restarted. No sync corruption.
- **Action:** Used the Healthchecks API key to POST to the check's UUID with `action=resume`. The check flipped to green on the next report from Centauri.

### 2. Dax memex-feed - watchdog circuit breaker was the real issue
- **Diagnosis:** The feed wasn't crashing - a watchdog script (`memex_watchdog_v02.py` on Dax) deliberately **disabled the cron jobs** on July 2 when the ingest queue briefly spiked to ~3200 files (threshold = 3000). The backlog later drained to safe levels (1472 files), but the watchdog **did not auto-re-enable** the crons - it just reset its own state to "ok".
- **Why this matters:** Memex's search index missed all memories from the last 8 days. The circuit-breaker was never designed to auto-restore.
- **Fix:** Manually ran the watchdog with `--restore` over SSH to re-enable the crons, then manually executed the memex push script once to force an immediate Healthchecks ping (it was still waiting for the next cron tick). Confirmed green within minutes.
- **Long-term improvement suggested (pending Max's yes):** Add auto-restore logic to the watchdog so it re-enables the pusher once the queue drains below a safe threshold.

### 3. Read AI - token irreversibly revoked; headless re-auth is impossible
- **Discovery:** The OAuth refresh token returned `invalid_grant` ("refresh token can not be found"). It's dead, not just expired.
- **Headless attempts exhausted:**
  - **Device-code flow:** The existing Read AI OAuth client is not registered for the `urn:ietf:params:oauth:grant-type:device_code` grant type - so it can't do a fully headless login.
  - **Dynamic client registration:** Registering a new public client via the Read API endpoint gave back a client that only supports `refresh_token` grant - no interactive/code flow - making it useless for bootstrapping a first token.
- **Conclusion:** **Read AI requires a real browser login** to Max's DNA Vibe Read AI account. No automated headless workaround exists.
- **Why the token expires so fast:** The token file (`readai_oauth_token.json`) lives inside Max's Nextcloud sync directory. Read AI rotates tokens on every use and likely revokes the whole chain when it sees an old token from a different machine. **Long-term fix: move the token file out of Nextcloud, onto Pine only.**

## CURRENT STATE

| Monitor | Status | What's left |
|---------|--------|-------------|
| **centauri-odysee-sync** | **Fixed and green.** | Nothing. |
| **dax-memex-feed** | **Fixed and green.** All 3 crons re-enabled, manual push pinged Healthchecks. The 8-day memory backlog will push into Memex over the next few runs. | None (unless Max wants the watchdog auto-restore improvement). |
| **Read AI (weekly transcripts)** | **Still down.** Token is dead. A re-auth helper script (`readai_reauth.py`) is ready to accept a new token once Max logs in via browser, but the login itself hasn't happened. | Token re-acquisition + move token store out of Nextcloud. |
| **All other monitors** (daily heartbeats, DeepSeek spend, money monitor, etc.) | All green and healthy. |

## EXACT NEXT STEP

### For Read AI - Max must choose one re-auth path (Claude asked at the end of the session):
**Option A:** Max reconnects the **Read AI MCP connector** in a normal Claude session (it pops a browser login, he approves). Then Claude can capture the fresh token on Pine and update the weekly download script.

**Option B:** Max opens Read AI in his browser himself, logs in, and lets Claude use Playwright to extract the token (or just manually supply the token data). The reauth script supports a `finish` subcommand to store the token.

After re-auth, the long-term fix:
1. Copy `readai_oauth_token.json` to a location outside Nextcloud (e.g., `/home/bitnami/readai/` on Pine, or a dedicated `tools/readai_transcripts` config dir).
2. Update `readai_weekly_download.py` to read from that new path.
3. Exclude the old Nextcloud copy to prevent sync conflicts in the future.

### For Dax watchdog improvement (if Max says yes)
- Modify `/home/bitnami/memex_watchdog_v02.py` to automatically call `--restore` when the queue size drops below the "warn" threshold (e.g., 500 files) **and** the crons are currently disabled.
- This will prevent future silent 8-day gaps.

## OPEN QUESTIONS AWAITING MAX

1. **Read AI re-auth method:** Option A (Claude session connector) or Option B (Playwright / manual)?  
2. **Watchdog auto-restore:** Do you want me to add the auto-re-enable logic to the Dax watchdog?  
3. **Token storage relocation:** When we re-auth Read AI, do you want me to move the token file to Pine-only now? (Claude strongly recommends it.)

## KEY PATHS, IDs, AND COMMANDS

### Healthchecks
- API key: `hcw_FURiOSiC9Vszzf2OWydsJumrkNj9` (from `healthchecks_io_creds_20260604.txt` in Nextcloud `ssh` folder)
- centauri-odysee-sync check UUID: `6dcbc67d-b557-4d41-81a4-b0186873bd76`
- dax-memex-feed check UUID: (can be looked up via API again or extracted from the push script - likely in cron on Dax)

### Dax (Lightsail instance)
- SSH: `ssh -i "C:\Users\maxre\Nextcloud\zSyncMain\ssh\dax_lightsail_max_id_rsa.pem" bitnami@35.80.203.42`
- Watchdog: `/home/bitnami/memex_watchdog_v02.py`
  - State file: `/home/bitnami/memex_watchdog_state.txt` (or `.json`)
  - Restore command: `python3 /home/bitnami/memex_watchdog_v02.py --restore`
- Memex push script: (exact filename not fully shown, but something like `memex_scrape_push.py` or similar; can be found via `crontab -l`)
  - Manual push: `/usr/bin/python3 /home/bitnami/memex_...` (the one that pings Healthchecks)
- Crontab: the watchdog disabled the memex crons by commenting them out; `--restore` uncomments them.

### Read AI
- Old token file (Nextcloud-synced): `C:\Users\maxre\Nextcloud\zSyncMain\ssh\readai_oauth_token.json`
- Weekly download script: `C:\claude_base\tools\readai_transcripts\readai_weekly_download.py`
- Log: `C:\claude_base\tools\readai_transcripts\readai_weekly_download.log`
- New re-auth helper: `C:\claude_base\tools\readai_transcripts\readai_reauth.py`
  - Subcommands: `start` (failed), `finish` (to store a new token, likely)
- Read AI MCP connector: configured in Claude's config (likely `%APPDATA%\Claude\claude_desktop_config.json` or similar), referencing `https://api.read.ai/mcp`

### Infra map reference
- `C:\claude_base\infra_map_tomemex.md` describes what "Read AI" is and where it runs.

## GOTCHAS AND DEAD ENDS

- **SSH key mix-up:** The first SSH attempt to Dax used the wrong key (likely a `lakarian_key.pem` from a different host). Always use
