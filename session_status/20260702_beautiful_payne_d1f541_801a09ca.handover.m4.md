# Scribe handover - milestone 4 (~306K tokens)
# session: 20260702_beautiful_payne_d1f541_801a09ca
# cwd: C:\claude_base\.claude\worktrees\beautiful-payne-d1f541
# written: 2026-07-02 12:04:16 by deepseek-v4-pro

# HANDOVER: ytdow - Full YouTube Backup Steward (b9)

---

## GOAL (in Max's own words)

Back up ALL of Max's YouTube videos (Tamza + Hucolo, originally 2842 unique) at 720p to teal16 (Centauri D:), split into `tamza_channel/` and `hucolo_channel/` folders. Respect the one-puller-per-residential-IP bot-wall rule with a 4-minute gap between downloads.

After the original backup completed, Max said: **"the new videos and streams appear weekly, you need to keep pulling them."** So the system now self-refreshes - scans both channels twice a week for new uploads/streams and auto-queues them.

Max's framing: **"not part of the team, but more like separate worker helping out"** - a standalone utility feeding teal16. The only team coupling was the initial 93 caption-disabled priority pass (long done).

---

## DECISIONS + WHY

### 4-minute gap between downloads
The residential IP gets bot-walled on *volume of metadata resolves*, not on download bandwidth. A 4-minute gap (`--min-gap 180 --max-gap 300`) resulted in **0 breakage walls across the entire 2842-video run**. Any walls that did appear were sparse, self-healed (worker backs off and retries), and never cascaded. This gap is proven correct.

### "Walls" are non-critical unless climbing
Max initially panicked at "3 walls!" but investigation showed they were all >15 hours old with 380+ clean pulls since. A wall is just YouTube briefly rate-limiting - the worker backs off 2-4 min and keeps going. **Critical only if:** worker DOWN, OR no successful pull in 60+ min while walls exist (stuck), OR 4+ walls in the last 60 min (climbing). When non-critical: label them "non-critical walls (healed)" in reports. When critical: escalate via vocalize + email (max@tamza.com) + Telegram (critical-alarms bot, chat 1395850773).

### 3-hour report cadence (not 30-min)
Max disliked the brief 30-min tick reports and wanted the old full-format purple-circle reports. Switched to a CronCreate-driven 3-hourly cadence. **However:** this CronCreate is session-only - it dies if the Claude Code session ends (confirmed on Jul 2 restart: cron was gone and had to be re-created as `3680807a`). The backup itself survives because Lak's OS cron is independent.

### Self-refresh via proxy (not home IP)
Channel listing for new videos uses an **iproyal proxy** so it never touches the residential IP. This means weekly scans can be aggressive (listing full channels, both videos and streams tabs) without risking the bot-wall that the download worker must dodge. The proxy is baked into `refresh_queue.py` as `--proxy` arguments.

### Hucolo channel ID recovery
The Hucolo channel URL wasn't saved in any script from the original list-building. Recovered by running `yt-dlp --print channel_url` on a known Hucolo video ID through the proxy. Found: `UCj5wGWloHE8hKHPd5kqWsJQ` ("Hucolo TV / Channeling").

### Drainer routing
`hucolo_all_ids.txt` is the drainer's routing table: if a video ID is in that file, the drainer sends it to `hucolo_channel/` on teal16; otherwise it goes to `tamza_channel/`. This file gets rebuilt by `refresh_queue.py` whenever both Hucolo sources (videos + streams) scrape successfully.

### Safe list-building (no-sloppy-fallback)
`refresh_queue.py` never deletes entries and never swaps in a partial list. For each of the 4 scrapes (tamza/videos, tamza/streams, hucolo/videos, hucolo/streams), it writes to a `.new` file and only swaps it in if yt-dlp returned exit code 0 AND the new file has at least 80% as many lines as the old file. Then it appends genuinely-new IDs to the master `tamza_all.txt`. A failed scrape silently skips - nothing is lost.

---

## CURRENT STATE

**Backup: 2851/2851 complete, 0 pending.** All on teal16 with `.done` sentinels (drainer writes `.done` only after scp + size-verify, so anything with `.done` is safe for b7's ASR).

**Worker:** idle (nothing to pull). pace_controller (Lak cron */5) keeps it alive; it'll auto-start pulling when new IDs appear in `tamza_all.txt`.

**Self-refresh:** `refresh_queue.py` runs on Lak cron: `37 4 * * 1,4` (Mon + Thu, 04:37 Lak time). First run on Jul 2 caught 9 new videos - all pulled and drained within ~1 hour. Next scheduled run: **Mon Jul 7, 04:37 Lak time**.

**Reporting:** 3-hourly CronCreate (`3680807a`) re-armed after Jul 2 session restart. Session-only - will need re-creation if this session dies again.

**Walls:** 0 in the current segment. All historical walls were sparse and self-healed.

---

## EXACT NEXT STEP

**No action required.** The system is self-sustaining. The standing watch is:

1. If this is a fresh cold session: re-arm the 3-hourly CronCreate report (the old one dies on session restart). The cron instruction is to SSH into Lak, check done count, walls, worker liveness, judge criticality, and report.
2. If you see a CronCreate-driven report (purple circle, timestamped): read it. If it says non-critical, nothing to do. If it says critical, escalate.
3. The backup worker and refresh cron run on Lak independently - nothing to touch there unless Max asks.
4. If Max asks for status: run the Lak check snippet, report.
5. If Max asks to stand down: stop the CronCreate and ScheduleWakeup loop. Do NOT stop Lak crons - those are his infrastructure.

---

## OPEN QUESTIONS (awaiting Max)

- **Stray local .mkv on Lak:** 1 leftover file in `/home/mrempadmin/yt_backup/out/` that has a `.done` sentinel (so teal16 already has it) but the drainer didn't delete the local copy. Harmless but takes space. Max hasn't asked about it.
- **Stand-down decision:** I've been running a light hourly ScheduleWakeup keep-alive loop since completion, waiting for Max to say "stand down" or "stop." He hasn't given that word yet. Until then: maintain the watch.
- **Escalation threshold:** Set at "walls climbing (4+/hour) with OKs stalled, OR worker down." Max accepted this but hasn't been tested with a real critical event yet.

---

## KEY PATHS / IDs / COMMANDS

### Machines
- **Lak:** `mrempadmin@192.168.1.199`, SSH key at `C:/Users/maxre/Nextcloud/zSyncMain/ssh/lakarian_key.pem`
- **teal16 (Centauri D:):** `maxre@192.168.1.176`, SSH key at `~/.ssh/sol_key` on Lak. Destination: `D:\tamza_yt_full_backup\tamza_channel\` and `D:\tamza_yt_full_backup\hucolo_channel\`

### Lak paths (all under `/home/mrempadmin/yt_backup/`)
- `tamza_all.txt` - master queue (currently 2851 lines). Worker pulls from this.
- `hucolo_all_ids.txt` - drainer routing table (1286 lines). Rebuilt by refresh_queue.py.
- `refresh_queue.py` - the self-refresh engine. Runs Mon+Thu 04:37 via Lak cron.
- `refresh_queue.log` - refresh output log.
- `out/backup.log` - source-of-truth download log. Check the last START segment for WALL/OK counts.
- `out/*.mkv` + `out/*.done` - completed downloads and drain sentinels.
- `split_backup.py` - the yt-dlp worker.
- `drainer.sh` - scp to teal16 + size-verify + write `.done` + delete local.
- `pace_controller.sh` - cron */5, keeps one worker alive.

### Lak crontab (mrempadmin)
```
*/5 * * * * /home/mrempadmin/yt_backup/pace_controller.sh
*/10 * * * * /home/mrempadmin/yt_backup/drainer.sh
37 4 * * 1,4 /home/mrempadmin/yt_backup/refresh_queue.py
```

### Channel IDs
- **Tamza:** `UCo-O_aBrW8J3hEGEdow71Iw`
- **Hucolo:** `UCj5wGWloHE8hKHPd5kqWsJQ`

### Repo paths (source of truth on Pine)
- Script: `C:\claude_base\tools\tamza_hucolo_backup\refresh_queue.py`
- Method doc: `C:\claude_base\tools\tamza_hucolo_backup\ytdow_method_v01_tomemex.md`
- Infra map: `C:\claude_base\infra_map_tomemex.md`
- Commits: `f38ad82c` (script + doc), `0434722d` (infra map). Both pushed to master.

### Escalation tools
- **Vocalize:** `pythonw C:/claude_base/tools/attention/attention.py --session "b9 ytdow" --number 9 --msg "..."`
- **Email:** mxmail send_mail to max@tamza.com
- **Telegram:** Bot token at `C:/Users/maxre/Nextcloud/zSyncMain/ssh/telegram_critical_alarms_bot_token_20260604.txt` (first non-comment line), POST to `https://api.telegram.org/bot<token>/sendMessage` with `chat_id=1395850773`

### Standard status-check snippet (run on Lak via SSH)
```python
import subprocess, os, glob, time
from datetime import datetime

D = "/home/mrempadmin/yt_backup"
OUT = D + "/out"

# Count done
all_ids = [l.split("|")[0].strip() for l in open(D + "/tamza_all.txt") if l.strip()]
done = [i for i in all_ids if os.path.exists(f"{OUT}/{i}.mkv") or os.path.exists(f"{OUT}/{i}.done")]
pending = [i for i in all_ids if i not in done]

# Worker check
w = subprocess.run("pgrep -af split_backup.py", shell=True, capture_output=True, text=True).stdout.strip()
worker_alive = "tamza_all" in w

# Walls/OKs from last START segment
log_lines = open(OUT + "/backup.log").read().splitlines()
starts = [i for i, l in enumerate(log_lines) if "START pid=" in l]
if starts:
    seg = log_lines[starts[-1]:]
    walls = sum(1 for l in seg if " WALL " in l)
    oks = sum(1 for l in seg if " OK " in l)
    # Timestamps of most recent WALL and OK
    wall_lines = [l for l in seg if " WALL " in l]
    ok_lines = [l for l in seg if " OK " in l]
    last_wall_ts = wall_lines[-1].split()[0] + " " + wall_lines[-1].split()[1] if wall_lines else "none"
    last_ok_ts = ok_lines[-1].split()[0] + " " + ok_lines[-1].split()[1] if ok_lines else "none"

print(f"NOW: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print(f"DONE: {len(done)}/{len(all_ids)}")
print(f"PENDING: {len(pending)}")
print(f"WORKER: {'ALIVE' if worker_alive else 'DOWN'}")
print(f"WALLS: {walls}, OKS: {oks}")
print(f"LAST WALL: {last_wall_ts}, LAST OK: {last_ok_ts}")
```

### Criticality judgment
- Non-critical: worker alive, last OK within 60 min, walls < 4 in last hour.
- Critical: worker DOWN, OR last OK > 60 min old with recent walls, OR 4+ walls in last 60 min.
- If critical: vocalize + email + Telegram, then report with ? instead of ?.
- If non-critical: report with ?, label walls "non-critical (healed)", no alarm.

---

## GOTCHAS

- **CronCreate is session-only.** If this Claude Code session restarts, the 3-hourly report cron is GONE. Must be re-created. The backup itself doesn't care (Lak crons are independent), but reporting goes silent. On any cold start: check `CronList`, and if empty, re-create the 3-hourly report job.

- **Hibernation freezes the timer.** If Pine hibernates overnight, the CronCreate won't fire on schedule - it'll fire once on wake, not 4 times. The backup keeps running on Lak regardless. Reports may have gaps; that's normal and harmless.

- **Do NOT put channel listing through the home IP.** The refresh script MUST use the proxy. The home IP is for the paced download worker only (one video every 4 minutes). Listing a full channel on the home IP would trip the bot-wall immediately.

- **3 walls is not a disaster.** Max panicked once. Check timestamps before alarming. Walls are only a problem if they're climbing and OKs stopped. Sparse old walls = normal YouTube rate-limiting that the worker self-heals from.

- **The "b9/b10" identity conflict was resolved.** Another session spawned with the same b9 name; that one renamed to b10. This session is the original and sole b9.

- **Do not stop Lak's crons.** pace_controller, drainer, and refresh_queue are Max's infrastructure. Only stop the in-session CronCreate and ScheduleWakeup if he says "stand down."

- **The stray .mkv on Lak:** if Max asks about disk space on Lak, check `/home/mrempadmin/yt_backup/out/` for any `.mkv` files that have corresponding `.done` files - those can be safely deleted (teal16 already has them).

- **Worklog:** `C:\claude_base\worklog\beautiful_payne_d1f541_22ddb95249.md` - append with `python C:/claude_base/compaction_kb/scripts/worklog.py log "DID" "STATE" "NEXT"` for durable record.

- **Communication rules:** Every reply leads with `?? b9`. Purple ? TLDR. Plain English, no code shown to Max. Default = ACT not ask. Keep replies short (~100-300 characters plus report). Give rationales when making decisions.
