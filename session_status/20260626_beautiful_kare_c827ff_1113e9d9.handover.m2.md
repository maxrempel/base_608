# Scribe handover - milestone 2 (~166K tokens)
# session: 20260626_beautiful_kare_c827ff_1113e9d9
# cwd: C:\claude_base\.claude\worktrees\beautiful-kare-c827ff
# written: 2026-06-26 16:00:43 by deepseek-v4-pro

# HANDOVER - Attention Alarm System (C30)

## GOAL (Max's own words)

Build a tool so any Claude Code session can **flash a message on both screens + speak aloud** when it needs Max in person (captcha/blocking). Then extend it so **Centauri (remote always-on Windows box) can sound the Pine alarm** for time-sensitive cloud tasks. The alarm must: auto-dismiss + be click-dismissable; play on laptop built-in speakers (bypass headset); say WHICH session; be loggable + lookupable; audio must not be cut off mid-word; **only TIME-SENSITIVE things vocalized**; not steal focus; be a small corner toast with big readable text; clicking must kill BOTH image and sound instantly.

Three trigger commands: **"poke me"**, **"vocalize"**, **"vocalize 22"** (the longest is most reliable for voice dictation).

---

## DECISIONS + WHY

1. **Cross-machine transport: fleetcomm "alarm" channel (Cloudflare KV)**
   - Reused existing fleetcomm infra (G4's cross-machine comms) but on a **separate, independent channel** named `alarm`. Max wanted reliability for emergencies - so I built a standalone Windows poller (`attention_poller`) that fires locally with no live Claude session needed, rather than relying on session-wake which was known buggy.

2. **Standalone OS poller, not session-driven**
   - The poller (`attention_poller.py`) runs every 1 minute via Windows Scheduled Task (`schtasks`), using `pythonw.exe` in the interactive session. This is deliberately decoupled - Max's exact words: "make it an independent straight channel so they can sound an alarm."

3. **Audio routing: Realtek built-in speakers at full volume**
   - Used `sounddevice` to play a synthesized WAV to the Realtek device specifically; `pycaw` to set that device's endpoint volume to full, then restore the prior volume. This bypasses Max's plugged-in headset (which is the Windows default device he isn't wearing).

4. **No-focus toast: WS_EX_NOACTIVATE + WS_EX_TOOLWINDOW**
   - The fullscreen version stole focus and killed Max's dictation mid-sentence. Solved by switching to a top-right corner overlay with `WS_EX_NOACTIVATE` (0x08000000), so dictation tools are never interrupted.

5. **Toast timing: stays through the full voice announcement**
   - Default `--seconds 0` means the overlay polls a `voice_done` thread event - stays up until the voice finishes, then auto-dismisses. Only clicking the toast kills both (sets `stop_event` which triggers `sd.stop()`).

6. **Audio cutoff fix: `sd.stop()` on click**
   - Previously `stop_event` was only checked *between* repeats - if you clicked mid-utterance, the full sentence played out (and any remaining repeats). Fixed by polling `stop_event.wait(0.1)` during playback and calling `sd.stop()` immediately on signal.

7. **Session auto-identification: resolve from bcast state files**
   - Even if a caller forgets `--session`, the tool scans `C:\claude_base\branch_bulletin\state\*.json` for a matching `cwd`, extracts the `id`. Fixed a false-match bug where a missing `cwd` key resolved to the current dir.

8. **History lookup: `--history` flag**
   - Parses `attention.log` (tab-separated: time, session, number, msg, cwd, pid, ppid) and prints a human-readable table. Solves "what just flashed and disappeared?"

9. **Worker `since` filter bug (fleet-wide)**
   - The Cloudflare Worker's `read()` parsed keys with `k.split(":")[2]`, but ISO timestamps contain colons - so `2026-06-24T21:22:08` truncated to `2026-06-24T21`. The `since` filter silently skipped all messages from the same hour, breaking polling on **all channels** (fleet, wake, alarm). Fixed by changing the key format from `split(":")` to splitting on `|` and using `parseInt(key.split("|")[2])` with a millisecond epoch timestamp. Deployed to Cloudflare.

10. **Pastel light yellow, Calibri bold, very large text**
    - Max's vision needs big text. Final sizing: session name 80pt, message 54pt, dismiss 26pt - all Calibri bold, black on pastel yellow (`#FEF9E7`). Single font throughout.

---

## CURRENT STATE - What is done

- **`C:/claude_base/tools/attention/attention.py`** - complete local alarm tool
  - Multi-monitor pastel-yellow no-focus overlay
  - TTS ? WAV ? sounddevice plays to Realtek speakers at full volume
  - `--to <machine>` remote dispatch via fleetcomm alarm channel
  - `--history [N]` lookup
  - Auto-session resolution from bcast worktree
  - Logging to `attention.log`
  - Click instantly stops both image and audio

- **`C:/claude_base/tools/attention/attention_poller.py`** - the standalone Pine receiver
  - Polls `fleetcomm /read?channel=alarm` single-shot
  - Fires `attention.py` locally for records targeting this machine
  - Baseline-at-start (doesn't replay old alarms on first run)
  - Cursor in `.attention_poller_cursor.json`

- **`C:/claude_base/tools/attention/install_poller.ps1`** - receiver installer for any machine

- **Windows Scheduled Task "attention_poller"** registered on Pine
  - State: Ready, runs every 1 minute, interactive session, `pythonw.exe`

- **`C:/claude_base/tools/fleetcomm/fleetcomm.py`** - added `alarm` subcommand (parallel to `wake`)

- **`C:/claude_base/tools/fleetcomm/worker/index.js`** - deployed fix for `since` filter bug (key format changed from ISO timestamp colons to pipe-delimited epoch ms)

- **Centauri** already has the two sender files (`attention.py`, `fleetcomm.py`) updated via one-shot authenticated git pull

- **Docs updated:** global2.md, attention_method_v01_tomemex.md, fleetcomm_method_v01_tomemex.md, infra_map_tomemex.md

- **TODO file:** `TODO_tomemex.md` - click-stops-sound marked DONE, remaining items empty

- **All commits pushed to master**

---

## EXACT NEXT STEP

**None pending - the task is complete.** The Centauri?Pine end-to-end chain was tested live: Centauri ran `attention.py --to Pine`, the alarm propagated through KV (~60s), Pine's poller picked it up and fired the local flash+voice. Log confirmed: `FIRED local alarm from Centauri C30`.

If Max wants the poller installed on another machine as a receiver: run `install_poller.ps1` there.

---

## OPEN QUESTIONS

? Does Max want the alarm poller on any other receiver machines, or is Pine the only place he sits?

---

## KEY FILE PATHS / IDs / COMMANDS

| What | Path / Value |
|------|-------------|
| Alarm tool | `C:\claude_base\tools\attention\attention.py` |
| Poller (Pine receiver) | `C:\claude_base\tools\attention\attention_poller.py` |
| Installer script | `C:\claude_base\tools\attention\install_poller.ps1` |
| TODO | `C:\claude_base\tools\attention\TODO_tomemex.md` |
| Method doc | `C:\claude_base\tools\attention\attention_method_v01_tomemex.md` |
| Log | `C:\claude_base\tools\attention\attention.log` |
| Poller cursor | `C:\claude_base\tools\attention\.attention_poller_cursor.json` |
| .gitignore | `C:\claude_base\tools\attention\.gitignore` |
| Fleetcomm tool (alarm cmd added) | `C:\claude_base\tools\fleetcomm\fleetcomm.py` |
| Cloudflare Worker (fixed) | `C:\claude_base\tools\fleetcomm\worker\index.js` |
| Worker URL | `https://fleetcomm.max-rempel2.workers.dev` |
| Fleetcomm KV token | `C:\Users\maxre\Nextcloud\zSyncMain\ssh\cloudflare_workers_kv_token_20260303.txt` |
| Account ID | `e4dc2224d6baa721873dca77dc6f05` (Max's CF account) |
| Global rules | `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md` (NOT git, Nextcloud-synced) |
| Infra map | `C:\claude_base\infra_map_tomemex.md` |
| Bcast state (session identity) | `C:\claude_base\branch_bulletin\state\*.json` |
| Laptop speaker device | `"Speakers (Realtek(R) Audio)"` |
| Scheduled task name | `attention_poller` |
| Pythonw path | `C:\Users\maxre\AppData\Local\Python\bin\pythonw.exe` |
| This session's identity | C30, signature ?? C30 |
| Worktree | `C:\claude_base\.claude\worktrees\reverent-volhard-be5d05` |
| Trigger commands | "poke me", "vocalize", "vocalize 22" |

Key command (Centauri sending alarm to Pine):
```
python tools\attention\attention.py --to Pine --session <name> --number <n> --msg "captcha waiting"
```

Key command (Pine history lookup):
```
python attention.py --history 15
```

---

## GOTCHAS / DEAD ENDS RULED OUT

1. **The 3-min screamer was never identified.** It predated logging and stopped on its own. The log is clean - only C30's own tests. But now every alarm is traceable by worktree in `attention.log`.

2. **Cloudflare Worker `since` filter was silently broken fleet-wide** - truncated ISO timestamps at the colon (e.g. `2026-06-24T21:22:08` ? `2026-06-24T21`). This made polling for new messages skip everything from the same hour. Fixed by switching key format to pipe-delimited epoch ms. **If `since` filtering breaks again, check the key parsing in the worker.**

3. **The 226MB MSI git push block** - another session's unpushed commit included `Nextcloud-33.0.6-x64.msi` (227MB). That session later gitignored it, and the blob was removed before my commits reached master. Already resolved.

4. **Click-stopping sound:** the original code only checked `stop_event` between repeats - not during `sd.play()` / `sd.wait()`. Fix: poll `stop_event.wait(0.1)` in a loop during playback, call `sd.stop()` immediately on signal.

5. **Audio cutoff (was):** the 4s toast timer killed the process before the voice finished because the voice ran in a daemon thread. Fixed: voice thread is non-daemon, joined before exit, and default `--seconds 0` keeps the toast alive through the full announcement.

6. **b1 false-match in `_resolve_session`:** `os.path.abspath("")` resolves to current dir, so any state file missing a `cwd` key falsely matched. Fixed with guard: `if c and os.path.abspath(c) == cwd and st.get("id")`.

7. **Don't use `git push ... | tail -5 && echo` to check push success** - the pipeline masks the exit code. Always check `$?` / `PIPESTATUS[0]` separately.

8. **global2.md is NOT git** - it's Nextcloud-synced. Edits there are immediate and need no commit, but can race with other sessions editing it simultaneously (caused an Edit failure mid-session; fixed by re-reading).

9. **Centauri's git uses Git Credential Manager over HTTPS** - non-interactive SSH can't prompt. Solved by using Pine's `gh auth token` + `https://x-access-token:<token>@github.com/maxrempel/claude_base.git` URL for one-shot authenticated pull.

10. **Toast pastel yellow = `#FEF9E7`** with black text. Font: Calibri bold throughout (80pt session / 54pt message / 26pt dismiss). The box is 1200?600. Semi-transparent (alpha 0.92).
