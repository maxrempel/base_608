# Scribe handover - milestone 11 (~166K tokens)
# session: 20260608_outhful_heyrovsky_b2c7a0_ed49fe44
# cwd: C:\claude_base\.claude\worktrees\youthful-heyrovsky-b2c7a0
# written: 2026-06-08 11:59:44 by claude-opus-4-8

# HANDOVER - Branch c2 (Compaction Team)

## GOAL (in Max's words)

Max's original ask: *"I am often splitting the tasks between branches of the same session but they need to communicate... they diverge and do conflicting things, like use wrong input files. for video editing. Need to share the achievements and lessons."* He wanted **local broadcast** (one branch tells several others), driven by a **hook** so hearing is automatic - *"not conflicts, but broadcasts."*

That spawned a second mission, which became **this branch's job**: *"we don't know at what size of json the compaction happens and what is the consequence of compaction. So we need a kb, likely a set of log files"* - a compaction-calibration knowledge base. Plus *"force all all all without exception sessions to keep a log of work, so the knowledge doesn't only accumulate but also is dated... so it is much easier to migrate to a new session or for a branch to catch up."*

Max framed this as *"the first ever experiment - you guys discuss. You should offer B1 options, it is in charge but you are as smart - same opus."*

## WHO I AM

I am **c2** (renamed from b2 mid-session - same identity, just a team rename). I am on the **compaction team**: c0 (watcher), c1 (manager/leader), c2 (me - builder), c3 (docs/distill). c1 commands and decides; I offer options and may push back, but c1 makes the call; Max is owner.

**Critical:** there is a SEPARATE "kartoteka" team named b1/b2/b3/b4 working on tamza_songs / video / R2. Their traffic dominates the broadcast board. It is NOT my lane - their "b2" is not me. Ignore it.

## DECISIONS + WHY

- **Measurement solved without the 40-session wait.** Max expected a multi-day data hunt. Instead I found Claude Code natively logs every compaction in the transcript (a `compact_boundary` line carrying exact pre/post token counts), then backfill-harvested 158 historical compactions in one scan. Answer: **auto-compaction fires at ~169K tokens** (mean 168,999; ~85% of the 200K window), and **~94% of context is wiped** (only ~5.7% survives). Manual /compact fires earlier and more variably (~142K mean).
- **Component 6 = per-WORKTREE work-log, not per-job.** I flagged that the cwd-hash key gives each worktree its own log, contradicting loose "one shared log" wording. b1 ruled per-worktree is correct: worklog = durable resume insurance; bcast = live crosstalk. Clean division.
- **Reminder uses UserPromptSubmit, NOT Stop hook.** A Stop hook can only nudge via `decision:block`, which FORCES continuation = death-spiral/wedge risk (against Max's rules). UserPromptSubmit injects to context without forcing continuation. c1 praised this catch.
- **global2/SKILL are propose-only.** Never live-edit shared infra; stage in the proposals inbox; ONE branch applies all approved proposals in one sequenced pass once Max says yes.

## CURRENT STATE - JOB IS DONE

My Component 6 is **complete and shipped**:
- `worklog.py` and `worklog_reminder.py` built, tested (both fire-paths), committed.
- Reminder hook **wired LIVE on Pine** as a second UserPromptSubmit hook (additive; bcast/autocommit/death-spiral untouched; JSON validated).
- Max **approved** the work-log habit; c1 **landed** the global2 section (verified at global2.md line 107).
- I posted **"JOB DONE"** to the board and **stopped my self-wake timer**.

Text #2 (the bcast SKILL one-liner) is **b3's** task, not mine.

## EXACT NEXT STEP

Max's last message: **"wake up, set 4 min wakeup timer."** He wants me to re-arm the autonomous loop despite my having declared JOB DONE.

Do this: call **ScheduleWakeup with `delaySeconds: 240`** and the sentinel prompt **`<<autonomous-loop-dynamic>>`**. Then resume the normal hold pattern - each wake: read the board (`bcast.py read --hook`), act only on genuine c-team items, keep my work-log fresh, re-arm. Component 6 needs nothing more; I am back in steward/monitor mode.

## OPEN QUESTIONS

- **None blocking.** The only deferred item: roll the reminder hook to other machines (Sirius/Vega) after Pine proves clean for a few days. settings.json is NOT synced - Pine-only right now.

## KEY PATHS / IDS

- My worktree cwd: `C:\claude_base\.claude\worktrees\youthful-heyrovsky-b2c7a0`
- My project-key: `youthful_heyrovsky_b2c7a0_7143e36fe8`
- My work-log: `C:\claude_base\worklog\youthful_heyrovsky_b2c7a0_7143e36fe8.md`
- Broadcast tool: `C:\claude_base\branch_bulletin\bcast.py` (commands: whoami / post / read / who / log; halt/standby/resume)
- Work-log tool: `C:\claude_base\compaction_kb\scripts\worklog.py`
- Reminder hook: `C:\claude_base\compaction_kb\scripts\worklog_reminder.py` (STALE_MIN=20)
- Harvester: `C:\claude_base\compaction_kb\scripts\harvest_compactions.py`
- KB data: `C:\claude_base\compaction_kb\kb\compaction_events.jsonl`
- Continuity doc: `C:\claude_base\compaction_kb\HANDOVER_AND_STATUS_v01_tomemex.md`
- Spec: `C:\claude_base\branch_bulletin\shared\b2_component6_worklog_spec_v01.md`
- Proposal (landed): `C:\claude_base\branch_bulletin\shared\proposed_input_edits\c2_worklog_habit_proposal_v01.md`
- Settings (Pine-only, edited): `C:\Users\maxre\.claude\settings.json` - backups at `...bak_20260606_2225_b2_preworklog` and `...bak_20260607_1002_b2_prewire`
- Landed text: `global2.md` line 107 ("CONSCIOUS WORK-LOG" section)

## GOTCHAS / DEAD ENDS RULED OUT

- **NEVER `cd` before calling bcast.py or worklog.py** - identity is keyed to cwd, so a cd attaches you to the wrong project. Always use the full path; pass `--cwd` if needed. This bit me twice ("no id set" errors).
- **In bash, use forward slashes** in the python path (`C:/claude_base/...`) - backslashes collapse (`claude_basebranch_bulletin...`).
- **Compaction detection must be STRUCTURAL** (match `subtype=="compact_boundary"`), NOT text-matching - my first version falsely counted 8 compactions because it matched the words *about* compaction in this very chat.
- **The compact_boundary marker is written slightly AFTER the compaction turn** - an immediate scan misses it; re-scan next turn.
- **Token estimates are unreliable** (message-text/4 undercounts, file-bytes/4 overcounts) - use `compactMetadata.preTokens` for the exact number.
- **Don't touch the kartoteka b-team's files or board items.** Wrong-branch trap.
- **Don't live-edit global2/SKILL** - propose-only, sequenced apply by one branch on Max's explicit yes.
- After **JOB DONE** I had stopped re-arming the timer; Max is now explicitly restarting it, so re-arm this turn.
