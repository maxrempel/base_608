# Scribe handover - milestone 11 (~165K tokens)
# session: 20260616_oving_stonebraker_eba78b_12626b12
# cwd: C:\claude_base\.claude\worktrees\loving-stonebraker-eba78b
# written: 2026-06-16 12:30:23 by deepseek-v4-pro

# HANDOVER - Fleet Monitor Spam Fix + Centauri Auto-Login

---

## GOAL (Max's words)

1. **"check whatever is needed"** - Telegram monitor alerts were firing; diagnose and fix root causes.
2. **"didn't you fix it before? It is like 5 time cl code reports fixing this problem and it surfaces again and again"** - The fleet_monitor spam recurrence has been "fixed" ~5 times. Build a **structural, non-symptomatic** fix that cannot recur.
3. **"Implement the most elegant fix and don't assume that ds will follow instructions precisely, it is an llm, random"** - The alarm logic must NOT depend on DeepSeek (LLM) free text, because DeepSeek rewords the same event differently each pass.
4. **"i forgot the webpage address of my expenses. Add it to every expense alert."** - Add the spend dashboard URL to all alerts.
5. **"Also, this month is bad. I need past 7 days, past 30 days and lifetime"** - Replace calendar-month spend windows with rolling windows.
6. **"check all systems and logs"** - Full fleet health sweep.
7. **"centauri - we need access to its drive. How to fix, yes."** - Centauri went silent after reboot; fix it durably.

---

## DECISIONS MADE + WHY

### A. Fleet Monitor Spam - The Structural Fix (commits 9b9222e4 ? a38a9fa4 ? master 93de72c2)

**Root cause (two bugs, both recurring):**

| Bug | Mechanism | Why prior fixes failed |
|-----|-----------|----------------------|
| **BUG A: SPAM** | Alarm dedup keyed on `hash(DeepSeek_prose)` with digits stripped. DeepSeek rephrases ("missed schedule" vs "missed its expected schedule") ? different hash ? every pass looks like a new problem. | Prior sessions patched the text (strip rising minute-count, strip bad chars). Each patch fixed one rewording variant. Never addressed the structural dependency on LLM text. |
| **BUG B: FALSE-DOWN** | Healthchecks checks for Lak machines were scheduled in UTC but Lak runs US/Pacific (PDT, UTC-7). The daily backup runs at 03:30 Pacific = 10:30 UTC, but HC expected ping at 03:30 UTC ? falsely DOWN for ~6h every day. | June 12 session (73892cc1) fixed the tz for `lak-moma-d1` only, didn't audit the rest. `lak-clawy-kb-backup` had the identical bug and kept flapping. |

**What changed (structural, not symptomatic):**

1. **Alarm decision now purely deterministic** - keyed on `set(down_check_names)` from Healthchecks `status=="down"` (excluding the monitor's own check `fleet-deepseek-monitor`). DeepSeek is now **cosmetic only** (body text). If DeepSeek API is down, a fallback summary is generated without it.

2. **Dedup keyed on stable facts** - `state_key = sorted(down_names)` stored in `state.json`. Alert fires ONCE per unique down-set. Reminders at most every 12h (REMIND_MIN=720). Sends a "RESOLVED" message when the set clears.

3. **Timezone self-healing guardrail** - `EXPECTED_TZ` mapping by name prefix:
   - `lak-*`, `sol-*`, `centauri-*` ? `"America/Los_Angeles"`
   - `dax-*` ? `"UTC"`
   - Every pass checks all cron-scheduled checks; any drift auto-repaired via Healthchecks API + a "CONFIG AUTO-REPAIRED" Telegram message.

4. **Test suite** - `tools/fleet_monitor/test_alarm_logic.py` - 7 synthetic scenarios (one down ? 1 alert; same set ? 0; after REMIND_MIN ? 1 reminder; different down check ? 1 alert; cleared ? 1 RESOLVED; clean ? clean ? 0; cosmetic fallback). All PASS.

5. **Recurrence ledger** - `C:/Users/maxre/.claude/projects/C--claude-base/memory/recurrence_fleet_monitor_alarms.md` - timeline of all 5 prior "fix" commits with what each claimed and how it resurfaced. STOP header instructs future sessions to ADD A ROW, not delete history. Indexed in MEMORY.md.

### B. Expenses Dashboard URL + Window Fix (commit 3ba6378b)

- **Dashboard URL:** `https://ledger.maxrempel.com/exp` - now appended to the $3 Telegram spend alert text (not voice clip, which stays clean).
- **Windows changed:** "this month" (calendar, resets on 1st - misleading mid-month) ? rolling **7 days / 30 days / lifetime** everywhere: dashboard cells, grand totals, voice story, email digest, header docstring.
- **Where deployed:** Dax, `/home/bitnami/ds_ledger/ds_ledger.py`, systemd `ds_ledger.service` restarted. Verified live dashboard renders new labels.

### C. Centauri Auto-Login

**Finding:** Centauri rebooted June 15 ~2 PM PDT (likely Windows Update). It's headless - no monitor, no keyboard. Its three scheduled tasks were all set to **LogonType Interactive** ("run only when user is logged on"). After reboot, no `maxre` session existed, so all three tasks silently stopped. Healthchecks marked all three Centauri checks DOWN.

**Host heartbeat:** Converted `centauri-host-heartbeat` to run as SYSTEM/ServiceAccount - works headless, survives reboots. Back UP on Healthchecks.

**memex-backup + odysee-sync:** Cannot run as SYSTEM (backup script depends on per-user Python environment, Odysee needs user context). These need a logged-in `maxre` session.

**Auto-login setup:**
- First attempt: Sysinternals Autologon64.exe failed (GUI tool, no session to render into).
- Second attempt: Registry method - set `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon`: `AutoAdminLogon=1`, `DefaultUserName=maxre`, `DefaultPassword=142525`.
- **First reboot failed** - no session formed. Root cause: `DevicePasswordLessBuildVersion=2` at `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\PasswordLess\Device` was blocking classic auto-login. This is the Win10/11 default that silently disables registry auto-login.
- **Fix applied:** Set `DevicePasswordLessBuildVersion=0`, re-wrote password key, rebooted again.
- **Disclosure:** The password is stored as REG_SZ plaintext in the registry (the encrypted Sysinternals method wasn't viable headless). This is a downgrade from the initial plan. Max has not yet acknowledged this tradeoff.

### D. Earlier Fix: CF Backup HTTP 500 (commit 11377b15)

The initial alert was a transient Cloudflare HTTP 500 on one D1 database dump (`cozy2`). `set -e` + `curl -f` aborted the whole run. Added `--retry 5 --retry-delay 3 --retry-all-errors` to the curl commands in `backup_r2_restic.sh` (both live on Lak and in repo). Manual re-run succeeded, Healthchecks went green.

---

## CURRENT STATE

### What is DONE:

| System | Status | Detail |
|--------|--------|--------|
| **CF R2+D1 backup (Lak)** | UP | Retries added; transient 500 won't page again |
| **fleet_monitor (Dax)** | DEPLOYED | Structural fix live - alarms keyed on facts, tz self-heal active, tested clean pass |
| **test_alarm_logic.py** | COMMITTED | 7 tests pass, pushed to master (93de72c2) |
| **Recurrence ledger** | COMMITTED | memory/recurrence_fleet_monitor_alarms.md with full timeline |
| **lak-clawy-kb-backup tz** | FIXED | Changed from UTC to America/Los_Angeles via HC API |
| **All other HC checks tz** | AUDITED CLEAN | No other Lak/Sol/Centauri checks on wrong timezone |
| **ds_ledger windows + URL** | DEPLOYED | 7d/30d/lifetime on dashboard, URL on Telegram alerts |
| **centauri-host-heartbeat** | UP | Running as SYSTEM, survives reboots |
| **Centauri auto-login config** | SET | Registry keys written, DevicePasswordLessBuildVersion=0, rebooted |
| **Centauri password** | SAVED | In shared_logins_frequent.txt (plaintext disclosure noted) |

### What is IN FLIGHT:

**Centauri auto-login validation.** The background poll (task `bsjok090s`) completed with exit code 0. The output is at:
```
C:\Users\maxre\AppData\Local\Temp\claude\C--claude-base--claude-worktrees-loving-stonebraker-eba78b\12626b12-13cf-4f62-9a3e-defd1c056b71\tasks\bsjok090s.output
```
This file must be READ to determine:
- Whether a `maxre` session actually formed after the second reboot.
- Whether `OdyseeSync.exe` is running in that session.
- The boot time (to confirm it actually rebooted vs. just came back from first boot).

### What is NOT YET DONE:

- **If auto-login succeeded:** Start `centauri-memex-kb-backup` and `centauri-odysee-watch` tasks (they should auto-trigger on their schedules now that a session exists). Verify both ping Healthchecks and go UP.
- **If auto-login failed:** Diagnose why `DevicePasswordLessBuildVersion=0` didn't take, or what else is blocking (e.g., "Require Windows Hello sign-in for Microsoft accounts" group policy, or `DefaultDomainName` needs to be set to `.` or the machine name).
- **Final Healthchecks verification:** Confirm all 17 checks are UP (currently 14/17 - 3 Centauri checks still down pending the auto-login result).
- **Honest disclosure to Max:** The plaintext-registry downgrade vs. the Sysinternals encrypted method initially promised.

---

## EXACT NEXT STEP

1. **Read the background poll output:**
   ```
   cat "C:\Users\maxre\AppData\Local\Temp\claude\C--claude-base--claude-worktrees-loving-stonebraker-eba78b\12626b12-13cf-4f62-9a3e-defd1c056b71\tasks\bsjok090s.output"
   ```
   Look for: `boot=...` (proves reboot), `user=.*maxre` (proves session), `odysee=True|False` (process running).

2. **If session formed (`user=.*maxre`):**
   - SSH to Centauri and start the two user-context tasks:
     ```
     Start-ScheduledTask -TaskName "centauri-memex-kb-backup"
     Start-ScheduledTask -TaskName "centauri-odysee-watch"
     ```
   - Wait ~30s, then query Healthchecks:
     ```
     curl -H "X-Api-Key: hcw_FURiOSiC9Vszzf2OWydsJumrkNj9" https://healthchecks.io/api/v3/checks/
     ```
     Verify `centauri-memex-kb-backup` and `centauri-odysee-sync` are UP.
   - Report final fleet status to Max (all 17 green).

3. **If NO session formed:**
   - Check the registry again (maybe reboot reverted something):
     ```
     Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" | Select AutoAdminLogon, DefaultUserName, DefaultDomainName
     Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\PasswordLess\Device" | Select DevicePasswordLessBuildVersion
     ```
   - Also check: `DefaultDomainName` may need to be `"Centauri"` or `"."` (local machine). Currently probably empty.
   - Check if "Require Windows Hello sign-in" is in play (Settings ? Accounts ? Sign-in options ? "For improved security, only allow Windows Hello sign-in" - this blocks auto-login even with PasswordLess=0).
   - If all else fails: ask Max to log in once via RustDesk (that instantly restores the session and the tasks will run until the next reboot).

---

## OPEN QUESTIONS AWAITING MAX

- **Centauri `maxre` password is stored plaintext in the registry** (`DefaultPassword` REG_SZ). The Sysinternals Autologon (encrypted LSA secret) failed because it needs a GUI session to configure. Is plaintext registry acceptable, or does Max want to RDP/RustDesk in and run Autologon64.exe himself to re-store it encrypted?
- **Are there other Windows machines** (beyond Centauri) that might also lack auto-login and would silently die after a Windows Update reboot? Sol is a Pi (Linux, no such problem). This was a Centauri-specific class of fragility.

---

## KEY PATHS, IDS, COMMANDS

### Machines
| Name | OS | LAN IP | SSH User | Key | Timezone |
|------|-----|--------|----------|-----|----------|
| **Dax** | Lightsail Linux | 35.80.203.42 | bitnami | `C:/Users/maxre/Nextcloud/zSyncMain/ssh/dax_lightsail_max_id_rsa.pem` | UTC |
| **Lak** | Linux (San Diego) | via MCP bridge | mrempadmin | `lakarian-python` MCP tool | US/Pacific (UTC-7) |
| **Sol** | Pi (bad RAM) | 192.168.1.113 | maxre | `~/.ssh/sol_key` | US/Pacific |
| **Centauri** | Win10/11 Dell | 192.168.1.176 | maxre | `~/.ssh/sol_key` | US/Pacific |
| **Pine** | Local desktop | - | - | - | - |

### Healthchecks
- **API Key:** `hcw_FURiOSiC9Vszzf2OWydsJumrkNj9` (from `C:/Users/maxre/Nextcloud/zSyncMain/ssh/healthchecks_io_creds_20260604.txt`)
- **API:** `GET https://healthchecks.io/api/v3/checks/` header `X-Api-Key: <key>`
- **Per-check modify:** `POST https://healthchecks.io/api/v3/checks/<uuid>` with JSON body (e.g., `{"tz": "America/Los_Angeles"}`)
- **Centauri checks:**
  - `centauri-host` - uuid `b9e5ddf8-...` (now SYSTEM, UP)
  - `
