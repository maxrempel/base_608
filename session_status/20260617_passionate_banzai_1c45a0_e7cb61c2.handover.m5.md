# Scribe handover - milestone 5 (~83K tokens)
# session: 20260617_passionate_banzai_1c45a0_e7cb61c2
# cwd: C:\claude_base\.claude\worktrees\compassionate-banzai-1c45a0
# written: 2026-06-17 13:32:11 by deepseek-v4-pro

# HANDOVER - Sol RAM Diagnosis Session

## GOAL (Max's words)

**"just brainstorm this"** - Max wants open-ended analysis, fresh perspectives, and creative thinking about the Sol RAM fault pattern. Not a procedural next-step, not a formal handover. He interrupted a status check to pivot to brainstorming.

## WHAT JUST HAPPENED

The previous Claude (Opus, dreamy_bassi worktree) had left a detailed handover with a live test running: **slots 3+4 (green slot 3 + black slot 4, 27GB load)**. Claude polled it mid-session. The poll returned - the test **crashed/froze** while being checked, confirming the pattern: black slot 4 caused failure. The `campaign_boots.log` count ticked up by one. The answer arrived without needing to decide "let it run or stop it."

Max then interrupted and said **just brainstorm this.**

## DECISIONS MADE + WHY

| Decision | Reasoning |
|---|---|
| Phase B used fixed good sticks (2+3) in varied slots | Isolates slot from stick - definitive |
| "100% load" = ~85% installed RAM | Must stay below OOM-kill line; OOM = contamination, not proof |
| Solo stick passes don't clear a stick | Fault is load-threshold, ~27GB+ triggers it |
| Campaign loop with flags/counters | Survives freezes, auto-resumes, preserves cumulative bad_word counts across boots |

## CURRENT STATE

**The black-slot theory is now confirmed by the 3+4 test:** green slot 3 + black slot 4, under 27GB load (2?16GB sticks), produced climbing bit-flips and then froze. This mirrors the earlier slots 2+4 test (also froze). Every configuration containing a black slot (2 or 4) fails under sufficient load. Every green-only config (1+3, 1+2 at ?24GB) passes.

**Sol is a 32GB machine on green slots 1+3.** 48GB or 64GB forces at least one black slot and is not reliable.

## THE BRAINSTORM - what to think about

Here's what "brainstorm this" could mean, and the vectors to explore:

### 1. The root cause is still unknown - two competing hypotheses

- **Physical black-slot fault:** bad solder joints, oxidized contacts, cracked traces on slots 2 and 4 specifically. The board has a manufacturing defect on one side.
- **Controller-side weakness under 2DPC loading:** the CPU's on-die memory controller handles two DIMMs per channel fine, but the far-DIMM (black slots) sees worse signal integrity. Not a "fault" per se - just marginal design. Higher total load (more GB) increases controller stress, and the far slots are the canary.

These are NOT yet distinguished. Memtest86+ (OS-free, no contention) could help, but even memtest can't perfectly distinguish trace from controller.

### 2. Things not yet tested (gap analysis)

- **Single stick in black slot 2 or 4, max load (~12GB):** Does a solo stick in a black slot fail? If yes ? slot fault. If no ? it's the *combination* of both channels under load, pointing to controller.
- **Swap the green/black stick identities:** Put the "good" stick 2 in black slot 4 and a "known" stick in green slot 3. Does the failure follow the slot or the stick? (Probably slot, but not tested.)
- **Underclock the RAM** (2133 or 2400 instead of 2667): If black slots become stable at lower speed, it's a signal-integrity / controller-margin problem, not a hard slot fault.
- **Voltage bump** (if BIOS allows): DDR4 at 1.25V instead of 1.2V. Same logic - if stability improves, it's marginal timing/signal, not broken hardware.
- **Single-channel mode:** Populate only channel A (slots 1+2) or only channel B (slots 3+4). Does the failure only appear when BOTH channels are active? That would nail it as a controller cross-channel loading issue.

### 3. Pattern oddities worth puzzling over

- **Stick 1+4 was the DISASTER config** (11 crashes in ~50min). Stick 1 is green slot 1, stick 4 is black slot 4. This is worse than 2+4 or 3+4. Why? Stick 1 was never in a bad slot - is stick 1 itself marginal and only exposed when paired with a black slot? Or is slot 1+4 a different channel pairing than 2+4 / 3+4?
- **Stick 4 solo passed** but stick 4 in any config with a green slot failed. That's the load-threshold effect, but the *magnitude* varies by which green stick it's paired with. Stick 1+4 was catastrophic; stick 3+4 was "climbing flips, then freeze." Is stick 1 slightly worse than stick 3, or is slot 1 electrically different from slot 3 despite both being green?

### 4. What does "fixed" even mean for Max?

- **32GB on green slots is stable.** Is that enough for Sol's intended workload? If Sol was meant to be a 64GB machine, this is a half-capacity outcome.
- **Replace the board?** Lenovo ThinkCentre M720s - proprietary form factor, not a standard ATX board. Cost/effort of replacement vs. just living with 32GB.
- **Replace the CPU?** If it's the controller, a different i7-9700 might behave identically - same stepping, same silicon margins.
- **What's Sol actually for?** The transcript never says. If it's a lab box for light experiments, 32GB is plenty. If it's meant to run large VMs or builds, it's constrained.

### 5. The memtest endgame - still relevant, still not done

Memtest86+ (already in GRUB) removes the OS variable entirely. It tests physical addresses without the kernel's mapping. If memtest also shows errors on black-slot configs, it's hardware. If memtest is CLEAN on black slots at full 64GB, then the Linux kernel's memory mapping is somehow tickling a marginal condition - which would be a genuinely weird and interesting result.

## OPEN QUESTIONS (for Max to answer, or for next session to chase)

1. **What is Sol's intended workload?** This determines whether 32GB-is-fine or we need a hardware fix.
2. **Can the BIOS underclock RAM or bump voltage?** These are the cheapest experiments to distinguish slot-fault from margin-issue.
3. **Is stick 1 actually worse than sticks 2/3?** The 1+4 disaster suggests asymmetry in the "green" pool.
4. **Single stick in a black slot - tested or not?** The transcript says solo tests were done (sticks 3 and 4 solo), but it's ambiguous which *slot* they were in. If solo tests were all in green slots, that's a gap.
5. **Does Max want to run memtest86+, or is the conclusion already sufficient for his needs?**

## KEY PATHS + COMMANDS

| What | Where/How |
|---|---|
| Sol SSH | `ssh -i ~/.ssh/sol_key maxre@192.168.1.113` |
| March tester | `/home/maxre/ramscan <GB> <passes>` |
| Campaign loop | `/home/maxre/campaign.sh` |
| Campaign flag | `~/campaign.run` (RUN/STOP) |
| Round counter | `~/campaign_round.cnt` |
| Results | `~/campaign32.log` |
| Crash counter | `~/campaign_boots.log` (grep -c ^BOOT) |
| Durable history doc | `C:\claude_base\tools\sol_resilience\sol_ram_experiment_history_20260617_v01_tomemex.md` |
| Worklog | `C:\claude_base\worklog\dreamy_bassi_ead69f_e1954e6c64.md` |
| Watch log | `C:\claude_base\worklog\sol_mon34_watch.log` |
| Pine (local) | The machine Claude runs on |

## GOTCHAS (do not rediscover)

- **OOM-kill is NOT a RAM fault.** A test that hits OOM is contaminated - discard it. Keep test size ~85% of installed RAM.
- **Clean at low load ? clean config.** The fault is load-threshold. A config needs testing at ?27GB (for 2 sticks) or ?42GB (for 4 sticks) to be declared clean.
- **Solo stick passes mean nothing** for the overall diagnosis. Every stick passed solo. The fault needs combined load.
- **No IPMI, no remote power.** A freeze requires physical power button or ~2min hardware watchdog timeout.
- **The campaign loop is reboot-survivable.** It restarts on boot if `campaign.run == RUN`. Make sure to disarm it (`echo STOP > ~/campaign.run`) before declaring victory.
- **The black-slot conclusion is strong but the root cause (trace vs. controller) is NOT resolved.** Don't overstate it.

---

**The floor is open.** Max said "brainstorm this" - the above is the full landscape. What angle does he want to chase?
