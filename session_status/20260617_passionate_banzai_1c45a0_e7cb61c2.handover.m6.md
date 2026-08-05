# Scribe handover - milestone 6 (~91K tokens)
# session: 20260617_passionate_banzai_1c45a0_e7cb61c2
# cwd: C:\claude_base\.claude\worktrees\compassionate-banzai-1c45a0
# written: 2026-06-17 13:34:17 by deepseek-v4-pro

# HANDOVER - Sol RAM diagnosis (Claude Opus, dreamy_bassi worktree, 2026-06-17)

## GOAL (Max's words, indirectly)

Diagnose why Sol hard-freezes under memory load. The working hypothesis has been narrowing toward "green slots clean, black slots fail," but **Max explicitly rejects this as unproven and calls out the risk of linear/single-cause thinking.** The diagnosis is not settled.

## WHAT'S KNOWN

**The machine:**
- Lenovo ThinkCentre M720s, i7-9700 (on-die memory controller), 4?16GB DDR4-2667 NON-ECC, 64GB total
- Slots labeled: 1+3 = "green" pair (one per channel, near DIMM), 2+4 = "black" pair (one per channel, far DIMM)
- LAN access only: `ssh -i ~/.ssh/sol_key maxre@192.168.1.113`
- No IPMI - a freeze needs physical power button or hardware watchdog (~2 min timeout)

**The tester:**
- `/home/maxre/ramscan <GB> <passes>` - custom March tester, prints cumulative `bad_words=N` = real bit-flips
- Campaign loop via `campaign.sh`, flag `campaign.run`, counter `campaign_round.cnt`, results in `campaign32.log`
- Pine-side watchers SSH-poll every ~50s, auto-disarm on crash detection

**Critical confound - LOAD THRESHOLD:**
Flips appear around 27GB+ load, freezes at 42GB+. Light loads (12-24GB) run clean even on KNOWN-bad configs. So **a clean result at low load does NOT clear a config.** "100%" testing means ~85% of installed RAM to stay below OOM-killer. OOM-kill contaminates a test; it is NOT proof of bad RAM.

**All experiments complete:**

| Config | Load | Result |
|---|---|---|
| Sticks 1+2 (solo sticks) | 24GB/75% | 20 rounds CLEAN |
| Stick 3 solo | 12GB | CLEAN |
| Stick 4 solo | 12GB | CLEAN |
| All 4 sticks | 50GB | FROZE (bad_words 769, repeat 2012) |
| Sticks 1+2+4 (3 sticks) | 36GB | Flips (R3=391), no freeze - MARGINAL |
| Sticks 1+4 | 13/24GB | **DISASTER: 11 crashes in ~50min, flips nearly every run** |
| Sticks 2+3 | - | MARGINAL (~2 crashes) |
| **Slots 1+3 (green), sticks 2+3** | **27GB** | **CLEAN 20/20** |
| Slots 2+4 (black), sticks 2+3 | 27GB | Flips R3=4 R4=2, FROZE round 5 |
| Slots 1+2+3 (green1+black2+green3), sticks 2,3,4 | 42GB | FROZE round 4 (R2=52 R3=84) |
| **Slots 3+4 (green3+black4)** | **27GB** | **R1=0 R2=0 R3=1 R4=2 R5=12, then 1 reboot/freeze** |

## THE THEORY THAT WAS EMERGING - AND MAX REJECTED

Earlier reasoning: every clean config uses only green slots (1+3). Every config touching a black slot (2 or 4) flips or freezes. This pattern held across all tests.

**Max's pushback:** the idea that "black slots are bad" or that there's a single cause is **not proven.** He explicitly called this linear thinking and said don't be an idiot about it. The handover session must approach with fresh skepticism and consider multifactor causes.

## COMPETING/COMPLEMENTARY EXPLANATIONS STILL IN PLAY

1. **Physically bad black slots** (contact, trace, solder) - the simplest reading of the data
2. **2-DIMM-per-channel signal stress** - black slots are the far DIMM on each channel; populating them increases electrical load on the on-die controller. This isn't "bad slots" - it's a marginal controller at 2DPC. Same symptoms, different root cause.
3. **Speed-dependent instability** - 2667 MHz with 2DPC might be the real trigger; dropping to 2133 in BIOS could stabilize 3 or even 4 sticks
4. **Something not yet tested** - the fixed-stick experiments only used sticks 2+3 in varied slots. Sticks 1+4 were never tested in slots 1+3 (green). There are untested permutations.
5. **Load threshold is the real variable** and green-1+3 at 27GB was just lucky (weak theory - 20 clean rounds makes luck unlikely, but not impossible)

## WRINKLES KEEPING THIS HONEST

- Green slots 1+2 were only ever clean up to 24GB, never tested at 27GB
- Each stick individually passed solo - this is **multifactor**: the trigger needs high total load engaging the full controller
- "Black slots bad" vs "controller weak under 2DPC loading" are NOT distinguished by tests done so far

## THE UNTESTED GOLD STANDARD

**memtest86+** - already in Sol's GRUB boot menu. No OS, no OOM, no contention. This needs Max physically at Sol's console for ~2 minutes. It's the only test that cleanly separates stick-vs-slot-vs-controller because it tests all combinations at native speed with no OS interference.

**Also untested:** reduce RAM speed in BIOS (2667?2133) and re-test a known-failing config. Free fix if it works.

## CURRENT STATE

- Sol is running on slots 1+3 (green) with 2 sticks = 32GB rock-solid. Usable in this state.
- The slots 3+4 test completed (froze, as expected from the pattern)
- No live test is running now
- Diagnosis is **NOT concluded** - Max wants fresh thinking, not a premature "black slots bad" closure

## EXACT NEXT STEP (when Max resumes)

1. **DO NOT** re-run the same slot-swapping tests - the pattern has been observed. Further slot-swap tests won't break the tie between the competing theories.
2. **DO** bring fresh hypotheses: what else could produce this exact symptom set that isn't "black slots physically bad"?
3. Memtest86+ is the next experimental step when Max has console access
4. The "drop speed to 2133 and test 4 sticks" idea is on the table but untested
5. Untested stick permutations (e.g., sticks 1+4 in green slots 1+3) exist but may not add value without a new hypothesis driving them

## OPEN QUESTIONS AWAITING MAX

- Does Max buy the "2DPC controller stress" alternative, or something else entirely?
- Is memtest86+ acceptable as next step, or does Max want a different diagnostic approach?
- Is 32GB stable on green slots 1+3 an acceptable interim outcome, or does the goal require 48/64GB?
- What other failure modes could produce bit-flips only when a "far DIMM" slot is populated?

## KEY FILES & PATHS

| What | Where |
|---|---|
| Durable history doc (full tables) | `C:\claude_base\tools\sol_resilience\sol_ram_experiment_history_20260617_v01_tomemex.md` |
| Worklog (e1sol) | `C:\claude_base\worklog\dreamy_bassi_ead69f_e1954e6c64.md` |
| Sol SSH | `ssh -i ~/.ssh/sol_key -o ConnectTimeout=12 maxre@192.168.1.113` |
| Campaign results | `~/campaign32.log` on Sol |
| Campaign state | `~/campaign.run`, `~/campaign_round.cnt`, `~/campaign_maxrounds`, `~/campaign_boots.log` |
| Ranscan binary | `/home/maxre/ramscan` on Sol |

## GOTCHAS - DO NOT FORGET

- **Load threshold is real.** A clean low-load test proves nothing. Always test at ~85% of installed RAM.
- **OOM-kill ? RAM failure.** If the OOM killer fires, that run is contaminated - discard it.
- **No IPMI.** A freeze means wait for watchdog or push the physical power button.
- **Dmidecode needs sudo password** - read-only firmware queries are safe but gated.
- **Max called bullshit on single-cause thinking.** The handover session should not walk in and declare "black slots are bad." That conclusion is premature and Max explicitly rejected it.
- **The "black slots" pattern is real data but not a settled diagnosis.** Correlation observed, causation NOT established.
