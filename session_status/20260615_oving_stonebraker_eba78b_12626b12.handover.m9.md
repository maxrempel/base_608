# Scribe handover - milestone 9 (~136K tokens)
# session: 20260615_oving_stonebraker_eba78b_12626b12
# cwd: C:\claude_base\.claude\worktrees\loving-stonebraker-eba78b
# written: 2026-06-15 08:59:58 by deepseek-v4-pro

# HANDOVER - Telegram Monitor Alert Spam & Backup False Alarms

---

## GOAL (Max's words)

"Check my Telegram monitor messages and fix whatever is needed." Then: "Check messages again. Sol might be down." Then frustration: "Didn't you fix it before? It's like 5 times Claude Code reports fixing this problem and it surfaces again and again."

---

## DECISIONS + WHY

### Session evolution (3 phases)

**Phase 1 - Thought the alarm was a real CF backup failure**
- Found `lak-r2-d1-backup` DOWN on Healthchecks (last ping 23 min ago)
- Logs showed HTTP 500 from Cloudflare D1 API on the `cozy2` database dump
- Manual re-run succeeded immediately - the 500 was transient
- **Fix applied**: added retry loop (up to 3 retries, 5-second backoff) to the per-DB dump in `/home/mrempadmin/cf_backups/backup_r2_restic.sh` on Lak
- Also synced fix to version-controlled repo copy at `scripts/blog_db_backup_worker/backup_r2_restic.sh`, committed, merged to master

**Phase 2 - Sol investigation (false lead)**
- Max said Sol might be down
- All 17 HC checks were green; Sol heartbeat steady every 4-5 min; UID direct SSH showed 1.5 days uptime, 57/62 GB RAM free
- Sol was never down - Max was misreading "in grace = normal" as a problem

**Phase 3 - Found the REAL spam source and the REAL bugs**
- Claude initially couldn't read bot outbound messages; admitted no log
- Max: "Fuck, are you saying you don't have a log of the messages?"
- Claude then found the log on **Dax** (where the monitor actually runs via cron), not on Pine (stale copy)
- The log revealed **~9 critical alerts over ~6 hours, all about `lak-clawy-kb-backup`**, not Sol
- Two bugs:

1. **Timezone trap** - The Healthchecks check for `lak-clawy-kb-backup` was scheduled at `30 3 * * *` in **UTC**, but the backup actually runs at 03:30 **US/Pacific** (UTC-7). So every day, the check flipped to DOWN at ~03:30 UTC and stayed DOWN until the real ping arrived at ~10:30 UTC - ~7 hours of false alarm. The backup itself ran fine; restic snapshots existed for every day.
   
2. **Monitor dedup/spam bug** - The monitor used DeepSeek's prose recap of the problem as the dedup key. DeepSeek reworded the same outage each pass (e.g., "missed schedule" vs "missed its expected schedule"), producing different hashes, so every 90-minute cooldown cycle treated it as a new problem and re-pinged Max.

### Fixes deployed

1. **Timezone fix**: Updated the Healthchecks check `677023d9-baaf-4d46-a04f-...` to use US/Pacific timezone via API PATCH. Audited all other scheduled checks - `lak-moma-d1-backup` was already correctly on Pacific; only `clawy` was wrong.

2. **Dedup fix in `fleet_monitor.py`** (lines ~228-280): Changed the alert key from DeepSeek's text hash to the **sorted tuple of down-check names** (stable, deterministic). New logic:
   - Alerts once per distinct problem set
   - Reminds at most every 12 hours
   - Sends a "RESOLVED" message when the problem clears
   - Deployed to Dax at `/home/bitnami/fleet_monitor/fleet_monitor.py` (with backup of previous version)
   - Live test run confirmed: silent (no problems ? no alert)
   - Synced to repo: `tools/fleet_monitor/fleet_monitor.py`, committed with message explaining both fixes, pushed to branch, merged to master

---

## CURRENT STATE

- **All 17 Healthchecks checks are GREEN** (verified live)
- **Sol is healthy** - uptime 1.5 days, idle, no freeze gaps in ping history
- **Lak backup data is safe** - restic snapshots exist daily, the backup itself never stopped working
- **The timezone fix is live** on Healthchecks API - `lak-clawy-kb-backup` now uses US/Pacific
- **The dedup spam fix is live** on Dax - new `fleet_monitor.py` deployed, syntax-checked, tested with a dry run
- **Repo is in sync** - commit on `scripts/blog_db_backup_worker/backup_r2_restic.sh` (retry hardening) and `tools/fleet_monitor/fleet_monitor.py` (dedup + timezone audit note) merged to master

---

## EXACT NEXT STEP

This is a **cold handover** - the next Claude session should:

1. **First, address Max's frustration**: He says this problem has been "fixed" ~5 times and keeps surfacing. Investigate why previous fixes didn't stick. Likely possibilities:
   - The monitor code was being edited on Dax but the repo copy was stale (or vice versa), and a redeploy or rebuild from repo reverted the fix
   - The monitor runs from cron on Dax - is there a deploy script that syncs from the repo? Or was the fix only ever applied live on Dax and never committed?
   - The timezone bug specifically: was this check created via API with a default UTC timezone, overriding any previous manual fix?
   - Check git log on `tools/fleet_monitor/fleet_monitor.py` for previous commits that claimed to fix alert spam - see what changed and what got reverted

2. **Monitor for a few days**: Confirm the spam stops (next `lak-clawy-kb-backup` daily run at 03:30 Pacific / 10:30 UTC should NOT trigger a false alarm)

3. **Consider adding a deploy mechanism**: If fixes are applied directly on Dax, they're fragile. A documented deploy path (or Ansible, or a sync script) would prevent drift.

---

## OPEN QUESTIONS (awaiting Max)

- **Why did this keep recurring?** Max explicitly asked this. The history of previous "fixes" for the same alert-spam problem needs investigation - were they applied to the wrong copy? Reverted by a cron job? Applied only to Pine and never to Dax?
- **Is the monitor code on Dax the ONLY live copy**, or is there a build/deploy pipeline that overwrites it from the repo?
- **Should we audit all Healthchecks checks for timezone correctness** as a one-time sweep? (Only clawy was wrong; the audit found no others, but a systematic check would confirm.)

---

## KEY PATHS / IDs

| What | Where |
|---|---|
| **Monitor live script** | Dax: `/home/bitnami/fleet_monitor/fleet_monitor.py` (SSH via `dax_lightsail_max_id_rsa.pem`, user `bitnami@35.80.203.42`) |
| **Monitor logs** | Dax: `/home/bitnami/fleet_monitor/fleet_monitor.log` |
| **Monitor state** | Dax: `/home/bitnami/fleet_monitor/active_alert_signatures.json` (new dedup state file) |
| **Repo monitor script** | `C:\claude_base\.claude\worktrees\loving-stonebraker-eba78b\tools\fleet_monitor\fleet_monitor.py` (committed, merged to master) |
| **Healthchecks API key** | `C:\claude_base\tools\fleet_monitor\healthchecks.key` |
| **HC check - clawy backup** | UUID: `677023d9-baaf-4d46-a04f-446364d3cc15` (timezone now US/Pacific) |
| **HC check - moma backup** | UUID: `227913ee-7f11-419f-b227-7ca9c4fc19fb` (was already US/Pacific, confirmed correct) |
| **Backup script (live)** | Lak: `/home/mrempadmin/cf_backups/backup_r2_restic.sh` (retry logic added) |
| **Backup script (repo)** | `scripts/blog_db_backup_worker/backup_r2_restic.sh` (synced with retry fix) |
| **Telegram bot token** | `C:\claude_base\tools\fleet_monitor\telegram.token` |
| **Lak MCP bridge** | `mcp__lakarian-python__run_python_code` for running commands on Lak |
| **Sol SSH** | `ssh -i ~/.ssh/sol_key maxre@192.168.1.113` |

---

## GOTCHAS

1. **Pine vs Dax confusion**: The monitor log on Pine (`C:\claude_base\tools\fleet_monitor\fleet_monitor.log`) is STALE (last entry 2026-06-11). The real monitor runs on **Dax** via cron (`*/30 * * * *`). Claude initially read the Pine log, saw it was stale, and couldn't find the real log until Max pushed back. Future sessions: the canonical log is on Dax.

2. **Telegram bot API can't read outbound messages**: `getUpdates` only returns inbound messages to the bot. To see what the monitor sent, you MUST read the log on Dax, not the Telegram API.

3. **Healthchecks timezone gotcha**: When a check is created via API without specifying `tz`, it defaults to UTC. Lak servers run US/Pacific. Any Lak-based check must explicitly set `tz: "US/Pacific"` or the schedule will be off by 7-8 hours (depending on DST).

4. **DeepSeek rewording breaks text-based dedup**: The previous dedup key was `hashlib.sha256(deepseek_recap_text.encode()).hexdigest()`. AI text is inherently variable - even the same underlying problem gets described slightly differently each pass, producing different hashes. The fix (key on sorted tuple of down check names) is stable but needs to be remembered for any future refactors of this code.

5. **Max is frustrated about recurrence**: This is the most important thing for the next session. Don't just re-fix - find out WHY it kept coming back. Check git history, check if there's a deploy pipeline overwriting live code from repo, check if previous fixes were only ever applied live on Dax and lost on server rebuild/cron restart.
