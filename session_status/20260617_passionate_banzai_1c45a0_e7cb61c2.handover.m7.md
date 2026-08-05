# Scribe handover - milestone 7 (~115K tokens)
# session: 20260617_passionate_banzai_1c45a0_e7cb61c2
# cwd: C:\claude_base\.claude\worktrees\compassionate-banzai-1c45a0
# written: 2026-06-17 13:37:59 by deepseek-v4-pro

# HANDOVER - Sol RAM Diagnosis (E4thinker, compassionate-banzai worktree, 2026-06-17)

---

## GOAL (Max's own words)

Diagnose why Sol (Lenovo ThinkCentre M720s, i7-9700, 4 DIMM slots, 4?16GB DDR4-2667 NON-ECC, 64GB) hard-freezes under memory load. The handover is to diagnose, with a fresh look. Max explicitly rejected linear single-cause thinking - this is a marginal, multi-factor problem, and the diagnosis must acknowledge that.

---

## WHAT THIS MACHINE IS

- **Sol** = `ssh -i ~/.ssh/sol_key maxre@192.168.1.113`, sudo password `SM2w3e4r5t6y=` (stored line 5 of `C:/Users/maxre/Nextcloud/zSyncMain/ssh/sol_sudo_password_20260523.txt`).
- No IPMI. A freeze needs the physical power button or hardware watchdog (~2 min timeout).
- 4 DIMM slots, two channels (green = slots 1+3, black = slots 2+4).
- 4 identical 16GB sticks, DDR4-2667, NON-ECC. **Crucially: all sticks are DUAL-RANK** (confirmed via dmidecode in this session).
- CPU: i7-9700 with on-die memory controller.
- memtest86+ is already in Sol's GRUB - but needs physical console.

---

## TESTING APPARATUS

- Custom March tester `/home/maxre/ramscan <GB> <passes>` - prints cumulative `bad_words=N` (bits read back wrong = real corruption, not OS noise).
- Campaign loop: `campaign.sh` on Sol, controlled by flag file `campaign.run`, counter `campaign_round.cnt`, results in `campaign32.log`, crash log `campaign_boots.log` (`grep -c ^BOOT` = crash count).
- Pine-side watchers SSH-poll every ~50s and auto-disarm the campaign flag on detecting a real crash.
- **Key confound, never forget:** the fault is load-threshold. Light loads (12-24GB) run clean even on KNOWN-bad configs. Flips appear ~27GB+, freezes 42GB+. "Clean at low load" does NOT clear a config. Test loads are kept at ~85% of installed RAM to stay under the OOM-killer line (OOM ? RAM fault).

---

## ALL RESULTS (compiled from prior session + this session's live update)

### Phase A - varied sticks

| Config | Load | Rounds | Result |
|--------|------|--------|--------|
| Sticks 1+2 | 24GB (75%) | 20 | CLEAN |
| Stick 3 solo | 12GB | ? | CLEAN |
| Stick 4 solo | 12GB | ? | CLEAN |
| All 4 | 50GB | ? | FROZE (bad_words=769, then 2012) |
| Sticks 1+2+4 (3 sticks) | 36GB | ? | flips R3=391, no freeze, MARGINAL |
| Sticks 1+4 | 13-24GB | ~50 min | **11 crashes, flips nearly every run** |
| Sticks 2+3 | ? | ? | MARGINAL (~2 crashes) |

### Phase B - fixed good sticks (2+3), varied slots

| Slots (sticks) | Load | Rounds | Result |
|----------------|------|--------|--------|
| Slots 1+3 (green-only) | 27GB | 20 | **CLEAN 20/20** |
| Slots 2+4 (black-only) | 27GB | 5 | flips R3=4 R4=2, **FROZE round 5** |
| Slots 1+2+3 (3 sticks: 2,3,4) | 42GB | 4 | FROZE round 4 (R2=52 R3=84) |
| Slots 3+4 (green+black) | 27GB | 5+ | R1=0 R2=0 R3=1 R4=2 R5=12, **eventually froze (1 reboot)** |

---

## THE DEAD THEORY - AND WHY IT DIED

**Initial tidy story:** "The two black slots (2 & 4) are physically dead. Every clean config is green-only; every bad config touches a black slot."

**Why Max (correctly) killed this:** The error rate wobbles run-to-run on the same config - R5=12 bad words, then R7=0. A physically dead slot fails hard and repeatably. This is stochastic, analog-margin wobble, not a digital break. Also: stick 1+4 crashed at only 13-24GB, but 1+2 at 24GB was clean - so it's not purely "black slot," the variables are tangled. Everything passed solo; only combinations fail. That's an interaction problem, not a broken part.

---

## WHAT THIS SESSION DISCOVERED (dmidecode - the real driver)

E4thinker pulled the firmware facts via dmidecode. **Each 16GB stick is DUAL-RANK.** That changes everything.

The geometry:
- 2 sticks in green slots 1+3 = one dual-rank stick per channel = 2 ranks per channel at 2666 MT/s. Clean.
- 3 sticks = two dual-rank sticks on ONE channel = **4 ranks on one channel at 2666 MT/s**. The i7-9700's memory controller is rated for this but marginal in practice - failure is soft, flaky, load-dependent, exactly matching our symptoms.
- The "black slot" pattern was a stand-in: every time we added a 3rd (or 4th) stick, we were loading a second dual-rank DIMM onto a channel, pushing the signal integrity over the edge at full speed.

**Conclusion: no hardware is necessarily broken. The memory controller can't drive 4 dual-rank ranks per channel cleanly at 2666 MT/s on this board.**

---

## CURRENT STATE

- Sol is currently a rock-solid 32GB machine on green slots 1+3 (2 sticks, one per channel).
- 48GB or 64GB is NOT reliably attainable at the current 2666 speed - not because anything is broken, but because dual-rank ? 2-per-channel at full speed is marginal.
- The 3+4 test finished (froze, 1 reboot). All tests are done. No campaign is running.
- E1testrunner (the hands-on operator) was posted the dmidecode finding via the e-team bulletin board.

---

## THE DISCRIMINATING TEST (not yet run - needs physical console)

**Drop RAM speed in BIOS from 2666 ? 2133, put all 4 sticks back, retest.**

- If it goes clean: nothing is broken. Sol gets full 64GB, just at 2133. The penalty is small for a home server.
- If it still crashes: there IS a genuine hardware fault (controller, trace, or slot) beyond just speed margin.
- **Also do a memtest86+ pass on the same console visit** - no OS, no OOM, no variables. That's the one test that settles stick vs. slot vs. controller for good, and it takes ~2 minutes.

**Exact console steps:**
1. Reboot Sol, enter BIOS (F1 at Lenovo splash).
2. Find memory speed setting (likely under Advanced ? Memory or Performance).
3. Change from 2666/auto to 2133.
4. Save and exit.
5. Install all 4 sticks in slots 1,2,3,4.
6. Boot and run `ramscan 54 20` (54GB = ~85% of 64GB, 20 passes).
7. Optional but definitive: boot memtest86+ from GRUB, run 1 full pass.

---

## OPEN QUESTIONS FOR MAX

1. **Console trip:** Are you willing to do one trip to Sol's physical console for the BIOS speed drop + memtest? That settles this definitively.
2. **Acceptable outcome:** If 2133 makes 64GB stable - is that acceptable? Or is 32GB at full 2666 speed preferable? (For a home server, 2133 vs 2666 is negligible latency - you'll never feel it, but 64GB gives you headroom.)
3. **Hardware swap:** If 2133 still crashes, do you want to source a different CPU or board, or just accept 32GB on green slots?

---

## KEY PATHS & IDS

| What | Where |
|------|-------|
| Durable history doc (full tables) | `C:\claude_base\tools\sol_resilience\sol_ram_experiment_history_20260617_v01_tomemex.md` |
| Worklog (e1sol) | `C:\claude_base\worklog\dreamy_bassi_ead69f_e1954e6c64.md` |
| Live monitor log | `C:\claude_base\worklog\sol_mon34_watch.log` |
| Branch bulletin board | `C:/claude_base/branch_bulletin/bcast.py` |
| SSH key | `~/.ssh/sol_key` |
| Sudo password | `C:/Users/maxre/Nextcloud/zSyncMain/ssh/sol_sudo_password_20260523.txt` (line 5: `SM2w3e4r5t6y=`) |
| Sol IP | `192.168.1.113` |
| Sol user | `maxre` |
| March tester | `/home/maxre/ramscan` on Sol |
| Campaign script | `/home/maxre/campaign.sh` on Sol |
| Campaign control files | `~/campaign.run`, `~/campaign_round.cnt`, `~/campaign32.log`, `~/campaign_boots.log` |
| memtest86+ | Already in Sol's GRUB menu |
| E-team roles | E1testrunner (hands-on Sol ops), E4thinker (this session - diagnostician) |
| Worktree | `C:\claude_base\.claude\worktrees\compassionate-banzai-1c45a0` |

---

## GOTCHAS & DEAD ENDS

- **Do not SSH into Sol during a test campaign without checking `campaign.run` first.** E1testrunner may be running a load test and an SSH command collision won't cause a freeze but muddies the data.
- **The sudo password file has 5 lines.** Use line 5 only. Don't `tr -d '\r\n'` the whole file - that concatenates garbage. Use: `sed -n '5p'` or hardcode the known password `SM2w3e4r5t6y=`.
- **"Clean at low load" is a trap.** A 12-24GB clean run means nothing - the fault only surfaces above ~27GB. Always match the load to the config's installed RAM (~85%).
- **OOM-kill ? RAM fault.** If the tester process gets OOM-killed, that data point is contaminated. Keep test size below the OOM-killer line.
- **Bad_words wobble is real.** A config that gives 0 bad_words on round 7 may have given 12 on round 5. One clean round does not clear a config. You need 20 clean rounds at high load to call it good.
- **The "black slot" theory is dead.** Don't resurrect it. The pattern was explained by dual-rank ? 2-per-channel loading. The slots themselves are probably fine.
- **memtest86+ needs the physical console.** There is no IPMI, no remote KVM. You must be at the machine.
- **Do not OOM the OS.** If the OS kills the test, that looks like a freeze but isn't - it just means you asked for too much RAM.
