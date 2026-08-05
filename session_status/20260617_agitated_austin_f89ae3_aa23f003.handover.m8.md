# Scribe handover - milestone 8 (~121K tokens)
# session: 20260617_agitated_austin_f89ae3_aa23f003
# cwd: C:\claude_base\.claude\worktrees\agitated-austin-f89ae3
# written: 2026-06-17 08:54:05 by deepseek-v4-pro

# HANDOVER - mass@tamza inbox watcher + instruction fixes session

---

## GOAL (in Max's words)
"Setup periodic email check of the mass@t mailbox, so you come to me with news. Right now it is minimal, but once it is in place, we will expand." Later refined to **20-minute checks** using the long-term wakeup timer.

Secondary goal that emerged mid-session: fix the global instructions so Claude stops guessing when it doesn't know Max-specific context.

---

## DECISIONS MADE + WHY

### 1. Built a read-only IMAP reader (not SMTP)
- **Why**: mxmail already sends mail but has no IMAP/read capability. Mass@tamza inbox needed reading without marking messages as seen.
- **Tool created**: `C:\claude_base\tools\mass_check\mass_check_v01.py`
- Pulls last N hours of mail (default 1h, adjustable via `--hours`). Filters to unseen messages, skips known noise (Healthchecks.io status pings, marketing). Reports interesting senders/subjects in plain English.
- Tested live: 101 messages over 7 days, mostly noise - reader works.

### 2. Scheduling: 20-minute recurring wake via the long-term timer
- **Why**: Max wanted hourly first, then switched to 20 min. The `wakeup.py` tool (made the prior day) survives laptop sleep - freezes when lid is closed, fires once on wake, then resumes cadence.
- **Command used**: `wakeup.py add --in "20 minutes" --msg "MASS@TAMZA CHECK..."`
- **Window**: `--hours 0.4` (~24 min) to match the cadence without repeating mail.
- **Limits acknowledged**: only fires while a session is alive in this worktree; laptop sleep = OK, session kill = won't fire until fresh session.

### 3. Instruction fix: "homework before asking" rule
- **Problem**: Max's earlier rule ("if you don't know, search Memex") was lost. Claude guessed instead of looking up Max-specific terms (like "Clawy").
- **Max's exact formula** (written to global2.md):
  > When a command implies context Claude doesn't know: (1) check autoloaded instructions - they hold short descriptions + paths to referenced files not themselves autoloaded; open any matching file. (2) If not found, search Memex - the semantic database that auto-ingests all memories and all session reports. (3) If still not found, ask Max. Never ask without doing basic homework first.

### 4. Machine job-placement policy (written to global2.md)
- **Low-CPU, low-memory crons** ? Dax
- **High-drive-capacity jobs** ? Lak, only if needed
- **Sol** is down now, might be up soon; once back, more goes on Sol (sparing Lak for high-responsibility long-term functions like Nextcloud)
- **Cent + Sol** are the less-valuable machines - jobs can go on them freely
- **Liz's computer** (asto/astolfo) available; Lak's work may offload there to reduce wear
- **Genomics high-CPU/memory** ? restore Sol or spin a temporary AWS VM
- **Claude does NOT get sudo on astolfo** (Liz's latest message, in session context but from outside - see open questions)

### 5. Clawy identified via Memex search
- **Clawy ?** = OpenClaw agent on Sol (192.168.1.113), with Telegram plugin - that's how Max uses it from phone. KB at `/home/maxre/Nextcloud/00_clawy_kb/`.

### 6. Sudo question for astolfo answered
- Liz asked whether she should give full admin or unprivileged user. Max asked about middle ground - scoped sudo with a whitelist. Answer drafted: regular user + sudoers.d drop-in allowing specific commands, optionally NOPASSWD.

---

## CURRENT STATE

### Done
- `mass_check_v01.py` reader built, tested, committed.
- 20-min wakeup timer active in this worktree. Fired twice during session (both times: nothing new).
- `global2.md` updated with homework/Memex rule + machine placement policy.
- Session milestone logged via worklog.py.

### In flight
- The mass@tamza 20-min timer is **actively running in this session only**. Not yet moved to a server (Dax).

### Blocked / awaiting
- Where to permanently host the mail check (Dax per policy, not yet set up).
- Reply to Liz about astolfo access - message drafted but not sent. Liz also said "Claude does not get sudo on astolfo, unless you want a VM."

---

## EXACT NEXT STEP

1. **Deploy the mass@tamza check to Dax** as a cron job (low-CPU, per the new policy). This makes it independent of this session/worktree and visible to Max even on phone (optionally via Telegram, same as Clawy).

2. **Resolve astolfo access**: Max needs to decide - accept no-sudo (group-based capabilities instead), push for scoped sudo, or spin a VM there. The Liz reply is drafted but not sent.

3. **Optionally expand the mail filter** once the Dax cron is stable - Max said "once it is in place, we will expand."

---

## OPEN QUESTIONS (awaiting Max)

1. **Liz/astolfo**: "Claude does not get sudo on astolfo, unless you want a VM." Does Max want a VM on astolfo, or accept no-sudo with group-based capabilities (docker group, adm, etc.)?
2. **Mass check delivery**: should the Dax cron push results to Telegram (where Clawy already talks to Max on phone), or just log/report in-session?
3. **Cent/Sol ambiguity resolved**: Max confirmed both Sol and Cent are less-valuable machines. The global2 line was fixed from the ambiguous "some things can go on sol" to correct meaning.

---

## KEY PATHS / IDs

| What | Path/ID |
|---|---|
| Mail reader | `C:\claude_base\tools\mass_check\mass_check_v01.py` |
| Reader docs | `C:\claude_base\tools\mass_check\mass_check_v01_tomemex.md` |
| Wakeup tool | `C:\claude_base\tools\wake_listener\wakeup.py` |
| Global instructions | `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md` |
| Wake timer message | "MASS@TAMZA CHECK (20-min): run 'PYTHONIOENCODING=utf-8 python C:/claude_base/tools/mass_check/mass_check_v01.py --hours 0.4'" |
| IMAP creds file | `C:\Users\maxre\Nextcloud\zSyncMain\ssh\` (contains mxroute creds) |
| Clawy KB path | `/home/maxre/Nextcloud/00_clawy_kb/` |
| Worklog script | `C:\claude_base\compaction_kb\scripts\worklog.py` |

---

## GOTCHAS

- **Wakeup timer is session-scoped**: survives laptop sleep but NOT session termination. Until moved to Dax cron, it's fragile.
- **The "worktree" term** confused Max briefly - it just means the folder this session lives in, not a git worktree. Session path: `C:\claude_base\.claude\worktrees\agitated-austin-f89ae3`.
- **mxmail is send-only** - no IMAP capability, hence the separate reader.
- **The homework/Memex rule previously existed but was lost** - this was the root of the Clawy confusion. Now restored.
- **astolfo ? asto**: same machine (Liz's computer), two names used interchangeably in session.
- **Compaction cliff ~169K tokens**: session was at ~121K real tokens at turn 51. This handover is the bridge.
