# Scribe handover - milestone 2 (~153K tokens)
# session: 20260702_loving_dhawan_e04207_de7bc1bf
# cwd: C:\claude_base\.claude\worktrees\loving-dhawan-e04207
# written: 2026-07-02 07:53:02 by deepseek-v4-pro

# HANDOVER - Session E26 (loving-dhawan-e04207)

---

## GOAL (Max's words)

Two problems:

1. **"Something is messing up the Windows clipboard history, now it's frozen. Could you figure out what's freezing it up? And probably restarted too."**

2. **"Next trouble with typer is that some combination, including the numeric pad key number five, somehow hibernated the computer... I think it was zero five or something. I think I typed zero five and it just hibernated... hibernation is a big impediment."** - later clarified: **"How about a slash on a numeric pad? Forward slash."** (as the new sleep trigger key)

Max also stated: **"I didn't intend a special hibernate script, that makes no sense. That was not my intention, it was some session which misunderstood. I needed sleep key, but not hibernate key for sure."**

---

## DECISIONS MADE + WHY

### Problem 1: Frozen Win+V clipboard history panel

- **TextInputHost.exe (PID 13244) was the culprit** - it had burnt ~9073 seconds of CPU time (roughly 2.5 hours). This is the process that renders the Win+V panel.
- The clipboard service itself (`cbdhsvc_6544c`) was fine - this was purely the UI renderer stuck in a loop.
- **Fix applied: killed PID 13244.** Windows auto-respawned a fresh TextInputHost with CPU reset to ~1.3s. Panel works again.
- **Root cause identified but NOT yet fixed at source:** all 6 typer instances run with `--paste` mode, which uses the clipboard to deliver text. Every dictation fires two `WM_CLIPBOARDUPDATE` events (write new text ? restore previous clipboard). TextInputHost enumerates clipboard formats on every event. Multiply by 6 instances ? hours of dictating = thousands of events causing the render loop burnout.
- **Decision: identified the mechanism but did NOT switch typer away from `--paste` mode.** The trade-off was understood (remove `--paste` ? zero clipboard traffic ? TextInputHost stays idle, but typing becomes visible keystroke animation instead of instant paste) but Max didn't give a go/no-go on that change yet.
- Consulted E25 (didn't exist in registry) and E125 (had worked on clipboard contention earlier today - commit 100fdd47 - but their fix was about Left-Alt+recall, not the TextInputHost angle). E125's answer was "done" - didn't really address the panel-freeze issue.

### Problem 2: Accidental hibernate on numpad

- **Found `hibernate_ce.ahk`** running via AutoHotkey (PID 19592). Line 2: `vk0C::` - VK code 0x0C is VK_CLEAR, which is exactly what **numpad 5 sends when NumLock is OFF**. Line 3: `SetSuspendState(1,0,0)` - the `1` means hibernate.
- So the trigger was: NumLock was off (or briefly went off), numpad 5 was pressed, and the machine hibernated instantly. No combo needed - just bare numpad 5 with NumLock off.
- Also found: `hibernate_hotkey.ps1` (same numpad-5-off trigger but for Sleep, not hibernate; dormant, not in Startup).
- Also found: `sleep_hotkey.ps1` (misleading name - actually binds **Delete key** to **monitor-off**, not sleep. Linked in Startup but not currently running).
- **Max's statement was clear:** he NEVER wanted a hibernate key. A past session built it by mistake (misunderstanding). He wanted a **sleep** key, not hibernate.
- **Decision: nuke the hibernate binding entirely.**
  - Killed AutoHotkey PID 19592.
  - Moved `hibernate_ce.lnk` from Startup to `C:\Users\maxre\hibernate_disabled_20260701\`.
  - Also archived: `hibernate_ce.ahk` (renamed `obsolete_hibernate_ce.ahk`), `hibernate_hotkey.ps1` (renamed `obsolete_hibernate_hotkey.ps1`).
  - Left a README in the archive folder explaining why, to prevent future sessions from re-creating it.
- **Decision: build a new sleep hotkey on numpad `/` (forward slash).**
  - Max chose this key. Reasoning: it's the same VK code (VK_DIVIDE, 0x6F) regardless of NumLock state - no dual-identity trap like numpad 5 had.
  - Created `C:\Users\maxre\sleep_numpadslash.ahk` - maps `vk6F` to `SetSuspendState(hibernate=FALSE)` = **Sleep** (not hibernate).
  - Created Startup shortcut: `sleep_numpadslash.lnk` ? loads on boot.
  - Now running as PID 47912.

---

## CURRENT STATE

### What is DONE:
- Win+V clipboard panel: **fixed** (TextInputHost restarted, responsive again).
- Hibernate-on-numpad-5: **eliminated** (script killed, Startup link removed, files archived).
- New sleep-on-numpad-slash: **live and autostarting**.

### What is IN FLIGHT / UNRESOLVED:
- **Typer `--paste` mode is still active** on all 6 instances. This means the root cause of clipboard panel freezes is still present - it WILL happen again after enough dictation hours. The trade-off and proposed fix (drop `--paste` from `start_typer_all.bat` and siblings) was presented but Max hasn't decided.
- **The old broken `sleep_hotkey.lnk` / `sleep_hotkey.ps1`** (Delete ? monitor-off, not sleep, not running, misleading filename) is still in Startup. An open question was asked about archiving it - no answer yet.
- **NumLock state is fragile.** `NumLocker.lnk` in Startup only enforces NumLock ON at boot, not continuously. A stray NumLock press (easy to hit when reaching for `+` or `/`) can still flip it off, which would have made numpad 5 dangerous before (now harmless since hibernate binding is gone).

---

## EXACT NEXT STEP

**Awaiting Max's answer on the two open questions:**

1. **Switch typer away from `--paste` mode?** (prevents future clipboard panel freezes at the cost of visible typing animation instead of instant paste)

2. **Archive the old `sleep_hotkey.lnk` / `sleep_hotkey.ps1`?** (cleans up the misleading leftover - Delete key bound to monitor-off, currently not running, confusing filename)

If Max says yes to either/both, those are the next actions.

---

## OPEN QUESTIONS (awaiting Max)

1. Do you want to drop `--paste` from all typer startup scripts and restart the 6 instances? (sacrifice instant paste for zero clipboard-freeze risk)
2. Should we archive the old broken `sleep_hotkey.lnk` and `sleep_hotkey.ps1` so nothing confusing remains in Startup?

---

## KEY PATHS, IDs, NAMES

| What | Path / Value |
|------|-------------|
| Archive folder | `C:\Users\maxre\hibernate_disabled_20260701\` |
| Old hibernate script (archived) | `C:\Users\maxre\hibernate_disabled_20260701\obsolete_hibernate_ce.ahk` |
| Old hibernate PS1 (archived) | `C:\Users\maxre\hibernate_disabled_20260701\obsolete_hibernate_hotkey.ps1` |
| New sleep script (active) | `C:\Users\maxre\sleep_numpadslash.ahk` |
| New sleep Startup link | `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\sleep_numpadslash.lnk` |
| Old misleading sleep link | `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\sleep_hotkey.lnk` (points to `sleep_hotkey.ps1` - Delete?monitor-off, not sleep) |
| NumLock enforcer | `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\NumLocker.lnk` (boot-only, not continuous) |
| Key detector script | `C:\Users\maxre\detect_key.ahk` (harmless, not running) |
| Typer tool | `C:\claude_base\tools\typer2\` - 6 instances running with `--paste` |
| Current AutoHotkey PID | 47912 (sleep_numpadslash.ahk) |
| Clipboard service | `cbdhsvc_6544c` (running fine) |
| TextInputHost | Auto-respawned after kill, healthy now |
| Branch bulletin system | `C:\claude_base\branch_bulletin\bcast.py` |
| Consult system | `C:\claude_base\tools\consult\consult.py` |
| E125's fix commit | `100fdd47` (Left-Alt+recall, not directly related to TextInputHost) |

---

## GOTCHAS AND DEAD ENDS

- **Numpad 5 is VK_CLEAR (0x0C) when NumLock is OFF, but VK_NUMPAD5 (0x65) when ON.** This dual identity created the accidental-hibernate trap. Numpad `/` has no such dual identity - always VK_DIVIDE (0x6F) - which is why it's safe.
- **Typer's `--paste` mode correctly tags clipboard data with Win+V exclusion formats** (so pasted text isn't stored in history), but the clipboard **events themselves** still fire and TextInputHost still enumerates formats on every event. The exclusion only prevents storage, not the CPU load.
- **E25 doesn't exist** in the consult registry - a dead end when trying to consult a previous session.
- **E125's response ("done, fix is in commit 100fdd47") was about Left-Alt+recall**, not the TextInputHost clipboard panel freeze. Partial match, not directly applicable.
- **`sleep_hotkey.ps1` is misnamed** - it binds Delete key to monitor-off via `SendMessage(0x0112, 0xF170, 2)`, not sleep. The misleading name could cause confusion in future sessions.
- **`SetSuspendState(1,0,0)` = hibernate; `SetSuspendState(0,0,0)` = sleep (if hibernation disabled) or `SetSuspendState(false,false,false)` for clean sleep.** The `1` in parameter 1 is the critical difference that a past session got wrong.
