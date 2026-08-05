# Scribe handover - milestone 2 (~156K tokens)
# session: 20260713_ring_grothendieck_7efff2_41791e16
# cwd: C:\claude_base\.claude\worktrees\adoring-grothendieck-7efff2
# written: 2026-07-13 11:43:58 by deepseek-v4-pro

# HANDOVER - B61: Tamza Kartoteka Wipe Investigation

---

## GOAL (in Max's words)
"Read telegram notifications and fix problems - something weird with tamza." Later clarified: the alert said "every update deleting the previous data, which makes no sense, like dangerous deletion of lots of data."

---

## WHAT ACTUALLY HAPPENED
The tamza.com song catalog (kartoteka) automatic rebuild was silently wiping user-contributed data on every run:
- ~5,000 song end-times (the "free" times beyond 2 minutes for radio play) were being dropped
- ~7,800 newly-added performance rows were being dropped
- The catalog shrank from **34,062 rows ? 26,283** on one observed rebuild

The rebuild itself is normal/scheduled behavior. The problem is that **user overlays (end-times, new performances) live in a separate data layer that the rebuild was not merging back in** - so every rebuild effectively reset the catalog to its base state, erasing all community contributions.

---

## CURRENT STATE
- **Live catalog is intact right now**: 34,062 rows on tamza.com/wp-content/kartoteka/data.json (24 MB). The overlays have been re-applied since the last wipe.
- **The fix is coded** (by a session called "b15merger") but **not yet deployed live** to the Cloudflare worker. Rebuilds are being held (manually paused) until the fix is live.
- **B60** (another Claude Code session) is actively handling the deploy of the fix.
- **B61** (this session) offered to build a safety sanity-gate: block any deploy/rebuild that would drop the row count below 34,000, while B60 deploys the merge logic.

---

## EXACT NEXT STEP FOR B61
Wait for B60 to respond on the branch bulletin board (`bcast.py`) with which piece B61 should take. The two likely work items:
1. Deploy the b15merger overlay-preservation fix to the Cloudflare worker
2. Build a sanity-gate that prevents any future rebuild from dropping row count below 34,000

B61 posted to the board and is standing by.

---

## OPEN QUESTIONS (awaiting Max or B60)
- Did B60 already deploy? If so, does the sanity-gate still need building?
- Should the sanity-gate be in the worker itself, in the CI/deploy pipeline, or as a Healthchecks monitor?
- Is the temporary rebuild-freeze acceptable, or is there urgency to resume scheduled rebuilds?

---

## KEY PATHS & IDENTIFIERS
| What | Path / Value |
|---|---|
| Live kartoteka data | `https://tamza.com/wp-content/kartoteka/data.json` (34,062 rows, ~24 MB) |
| Telegram safety-watcher bot | `@MMMMonitorMaxBot` (sends alerts to Max's phone) |
| Telegram user API session file | `C:/Users/maxre/Nextcloud/zSyncMain/ssh/telegram_userapi_maxasst_20260612.txt` |
| Healthchecks fleet key | `C:/claude_base/tools/fleet_monitor/healthchecks.key` |
| Fleet monitor script | `C:/claude_base/tools/fleet_monitor/fleet_monitor.py` |
| Cloudflare KV backup dump | `C:/claude_base/backups/cf_kv_pages/` (commit c933ca4c) |
| Branch bulletin board | `python C:/claude_base/branch_bulletin/bcast.py` |
| tamza worker deploy reference | `C:/Users/maxre/.claude/projects/C--claude-base/memory/reference_tamza_worker_deploy_dezh.md` |
| b15merger fix (not yet deployed) | Referenced by B60; exact commit/file unknown to B61 |
| The two Telegram alerts | Pulled via user-API Telethon reader, output at scratchpad `tg_bots.py` output |

---

## GOTCHAS & DEAD ENDS ALREADY RULED OUT
- **Fundraising date stuck on July 4**: FALSE LEAD. The text "4 ????" on tamza.com/donate is body-text (a real event mention), not an auto-roll mechanic. The auto-roll date fix from commit f49d3edb was on the **Starseed** donate page, not tamza.
- **Bot API getUpdates**: DEAD END. Telegram bot API only returns messages sent *to* the bot, not outgoing alerts. You need the user API (Telethon with saved session) to read Max's message history.
- **Telethon full-dialog scan**: CAUSED HANG. Scanning all dialogs without targeting specific bots caused a multi-minute hang. The fix was targeting only the two known monitor bot usernames.
- **Nextcloud file locks on .session files**: Copy the Telethon session file locally before use to avoid locks and auth conflicts.
- **PowerShell vs Bash for Python**: Subtle execution-path differences exist; the final working reader ran under PowerShell with `$env:PYTHONUTF8=1` set.
- **The kartoteka itself is not corrupt** - it's structurally fine. The bug is purely in the rebuild pipeline not merging overlays before writing the final output.
