# Scribe handover - milestone 1 (~132K tokens)
# session: 20260627_elastic_antonelli_fcac29_35956bf7
# cwd: C:\claude_base\.claude\worktrees\elastic-antonelli-fcac29
# written: 2026-06-27 18:24:24 by deepseek-v4-pro

## HANDOVER - Wakeability Project (Track-2, C42)

### GOAL (Max's words)
Make his **existing 30ish desktop Claude Code tabs** "answer the phone" - wake up on demand or on schedule, retaining context, and survive **both a Windows restart and an app restart**. Max **explicitly rejects** headless/cloud workers and cloned/forked workers. He wants the **actual original in?app tabs** woken, not a substitute.

### DECISIONS + WHY
1. **Two?timer distinction resolved**  
   - **Harness ScheduleWakeup** (the good one): the desktop app disk?persists a wakeup timer; when it fires, the app **loads the dormant tab by itself** without needing a click. Survives app restart + OS hibernate.  
   - **wakeup.py disk?schedule timer** (tab?level): convenience layer that requires a live polling listener - useless after app restart.

2. **The "zombie?eats?wake" bug**  
   - After app restart, pre?restart listeners keep running as **detached zombies**. They race?win the schedule poll, consume a due wake, and exit with code 2 into the void ? wake silently lost.  
   - The orphan?guard (commit e88b7f54) makes the listener capture its spawning `claude.exe` PID+create_time at arm time. If the app dies, the listener exits gracefully (exit 0) **without consuming the wake**.  
   - However, **parent?chain walking is unreliable** for orphan detection (intermediate bash wrappers die, so no `claude.exe` ancestor appears even when the app is alive). The fix: **arm?files** - each listener writes a JSON file recording its PID, the parent `claude.exe` PID, and the app's create_time. This provides a reliable, unambiguous signal of the listener?app relationship.

3. **Arm?file zombie_sweep**  
   - Built `zombie_sweep.py` (commit 033fd1a5): reads arm?files, checks whether the associated app process is alive (by PID existence + create_time match + name containing "claude").  
   - It **only kills provable orphans** (app dead, PID reused, or process not claude). Fail?closed on uncertainty. Dry?run by default; `--apply` required to actually kill.  
   - **Production validation**: ran dry?run against 14 live arm?files ? 0 false positives, proving the kill tool is safe.

4. **restart_evidence.py** - read?only analyzer to make the decisive restart test one command. Scans wake listener debug logs and categorises events (launch burst, survival candidates, orphan exit, wake firing). It **honestly labels** candidate self?loads as "candidates", not proof, because `src=resume` can also come from clicks or compaction.

5. **Headless track dropped** - C41 confirmed it conflicts with Max's "no headless" rule; C42 is not to build it.

### CURRENT STATE
- **All track?2 code is committed, pushed, and accepted by C41**:  
  - `wake_listener.py` with arm?file mechanism (e88b7f54)  
  - `zombie_sweep.py` (033fd1a5)  
  - Documentation update in `wakeable_grid_method_v01_tomemex.md` (6a65c137)  
  - `restart_evidence.py` with honest labeling (458e5a9a)  

- **C42 is in a self?wake loop** (15?min steady ScheduleWakeup) during Max's break. Each tick: checks the broadcast board, re?arms the timer. The loop continues until Max returns and explicitly says "go sleep" or "off".  
- The board is quiet; no outstanding peer questions for C42.  
- The zombie?eats?wake hazard is fully documented and the fix is live in production (14 arm?files observed healthy).  

- **The actual survival mechanism remains the harness ScheduleWakeup**. The C42 fix makes the **on?demand force?wake half reliable across restart** (zombies no longer steal it). The full?circle test (tab self?loads from dormant state after a clean restart, with no clicks/compaction) has **not yet been run** - it requires Max to restart the machine/app, so it's pending his return.

### EXACT NEXT STEP
**When Max returns** (a real human message - not the loop prompt):  
1. C42 should stop re?arming and deliver a short TLDR status ("track?2 shipped, pending: restart test + sweep wiring").  
2. Run the **live restart pressure?test**: restart the app (or Windows), then use `restart_evidence.py` to verify that the orphan?guard preserved the wake and that a live listener won the force?wake over its zombie.  
3. Run the **decisive un?clicked self?load test**: verify that a dormant tab with a pending ScheduleWakeup actually comes back (src=resume) with no human click, no compaction - the clean proof of survival.  
4. Get Max's **OK to wire `zombie_sweep.py` as a periodic scheduled task** (it's a kill tool, so it needs his explicit blessing).  

If the user "stopped by" or another message that is not Max's return, the loop continues with no additional action.

### OPEN QUESTIONS (awaiting Max)
- None beyond the pending tasks above. The headless track is dead; the two?timer confusion resolved; the safety of the sweep is proven.

### KEY FILE PATHS / IDs / NAMES
- **Worktree**: `C:\claude_base\.claude\worktrees\elastic-antonelli-fcac29`  
- **C42 session ID**: `b02b594e-6bfd-43f2-a506-08ceb0759381`  
- **B9 session ID** (reference for ScheduleWakeup survival): `46651386`  
- **Primary tools**:  
  - `C:\claude_base\tools\wake_listener\wake_listener.py` (arm?file, orphan?guard)  
  - `C:\claude_base\tools\wake_listener\zombie_sweep.py` (kill tool, dry?run by default)  
  - `C:\claude_base\tools\wake_listener\restart_evidence.py` (read?only log analyzer)  
- **Documentation**: `C:\claude_base\tools\wake_listener\wakeable_grid_method_v01_tomemex.md`  
- **Broadcast board**: `C:\claude_base\branch_bulletin\bcast.py` (catchup, whoami, post, etc.)  
- **Timer helper**: `C:\claude_base\tools\timer_decel\timer_decel.py set 15 steady` (prints DELAY_SECONDS=900)  
- **Arm?file directory**: `C:\claude_base\branch_bulletin\wake\listeners\` (each file named `<sid>.<pid>.json`)  
- **ScheduleWakeup hook**: defined inside the system/Claude?specific paths (not a separate script, but the app listens to it).  

### GOTCHAS ALREADY RULED OUT
- **Parent?process walking for orphan detection** - breaks on intermediate bash wrappers; discarded.  
- **Relying on `src=resume` alone to prove self?load** - contaminated by clicks and compaction; must be cross?referenced with a clean no?interaction test.  
- **Auto?wiring the zombie_sweep as a scheduled task** - not done, must wait for Max's OK.  
- **Running a restart while Max is away** - strictly forbidden; only Max can initiate that test.  
- **Building a headless/cloud worker** - explicitly rejected by Max; C41 confirmed the track should be dropped.
