# Scribe handover - milestone 7 (~540K tokens)
# session: 20260702_kind_johnson_0e5da3_e84ca26a
# cwd: C:\claude_base\.claude\worktrees\kind-johnson-0e5da3
# written: 2026-07-02 14:54:14 by deepseek-v4-pro

# HANDOVER - typer session E25B (kind-johnson-0e5da3)

## GOAL (Max's words)
"Paid Groq" - switch typer's speech-to-text from OpenAI Whisper (slow/unreliable) to **Groq's paid tier** so dictation is fast and consistent. The free Groq tier was rate-limiting us into 5-14s delays per call.

## WHAT JUST HAPPENED
The session spent hours chasing slowness (Groq free-tier rate limits, orphaned process stacks, the warm-keeper pinger making the rate limit worse, a collision with session E45 also editing typer.py). Eventually reverted the live tool to yesterday's stable OpenAI version to stop the bleeding. Max then said "let's do paid Groq" and I drove Playwright to upgrade the Groq account.

**Playwright is currently sitting at the Groq payment/card page** - billing address filled, waiting for Max to complete the card/SMS step in the automation browser window on his screen.

## CURRENT STATE

**Typer is RUNNING** - 3 instances on the stable OpenAI version (slow but working):
- **Plus** (F9/numpad+) ? English
- **Zero** (numpad 0) ? English backup
- **Right Ctrl** ? Russian
All use `typer.py` or `typer_stable.py` at `C:\claude_base\tools\typer\`

**The Groq upgrade is mid-flight:**
- Logged into console.groq.com via Google (max.rempel2@gmail.com)
- Developer plan upgrade flow reached the payment step
- Address pre-filled (Mass Rempel, 111 Summit Ave etc.)
- Stripe has a saved card ending ??00; it texted a 6-digit code
- **Waiting for Max to enter the SMS code or card, then click "Upgrade"**

## EXACT NEXT STEPS

**Step 1 - Max finishes payment (his action):** In the Playwright browser window on his screen, enter the SMS code (or card details if using a new card), tick "I accept", click "Upgrade." He'll say "done."

**Step 2 - Create fresh API key:** Once the account shows "Developer" plan, navigate to API Keys, create a new key, copy it.

**Step 3 - Wire the key into typer:**
- Drop the new Groq key into `C:\claude_base\tools\typer\.env` (or create a `.env.groq` and point the loader at it).
- In `typer.py` (the CURRENT live version, already reverted to stable), flip `STT_PROVIDER = "openai"` ? `"groq"` and set the model to `"whisper-large-v3"`.
- Kill all 6 pythonw typer processes (use psutil - installed and proven reliable via `C:\Users\maxre\AppData\Local\Temp\typer_stable_launch.py` which does exactly this).
- Relaunch 3 instances (Plus, Zero, Russian) via `Start-Process pythonw.exe -WindowStyle Hidden`. The launcher script is at `C:\Users\maxre\AppData\Local\Temp\typer_stable_launch.py`.

**Step 4 - Verify:** Test English on Plus, Russian on Right Ctrl. Dictation should now be fast (~0.5-1s) and consistent (paid Groq has no rate limit).

## KEY FILES & PATHS

| What | Where |
|---|---|
| Live typer (stable, running now) | `C:\claude_base\tools\typer\typer.py` |
| Stable fallback (yesterday's version) | `C:\claude_base\tools\typer\typer_stable.py` |
| Git commit with yesterday's stable | `74bfdf56` in `C:\claude_base` repo |
| Reliable kill+relaunch script | `C:\Users\maxre\AppData\Local\Temp\typer_stable_launch.py` |
| typer venv | `C:\claude_base\tools\typer\venv\` |
| Groq API key file (EXISTING, possibly free-tier) | `C:\Users\maxre\Nextcloud\zSyncMain\ssh\groq_api_key_20260611.txt` |
| typer .env | `C:\claude_base\tools\typer\.env` |
| Stable version tracker/meter | `C:\claude_base\tools\typer\meter.py` (note: meter.py was NOT reverted - it's today's thicker bar) |
| Launcher bats | `C:\claude_base\tools\typer\start_typer.bat`, `start_typer_ru.bat`, `start_typer_all.bat` |
| Process tool (installed, works) | `psutil` in the typer venv |
| Groq login email | mass@tamza.com (forwards to Gmail), but account is via Google (max.rempel2@gmail.com) |
| Groq console session | Active in Playwright, payment page open |

## OPEN QUESTIONS

1. **Is the Playwright browser still open?** The last action was `browser_close` - but the payment page was still waiting for Max's input. I may need to re-navigate and re-login, which means another magic-link email cycle.
2. **Which key format does this Groq account use?** Their API keys start with `gsk_`. The existing key file has one - we may need a NEW one tied to the paid account.
3. **Does the `.env` loading in typer.py still work?** The stable version reads `C:\claude_base\tools\typer\.env` first, then falls back to env vars. The `.env` currently has OpenAI keys - needs the Groq key added.

## GOTCHAS & DEAD ENDS

- **DO NOT edit typer from two sessions simultaneously.** E45 and E25B collided today - file edits clobbered each other, process management killed each other's launches. ONE session owns typer at a time. If E45 is still active, tell it to stand down (it already agreed once via bcast).
- **Do NOT use the warm-keeper** - the 20s background ping to Groq hammered the free tier past its rate limit. With paid Groq the rate limit is gone, but the warm-keeper is still unnecessary and was a source of orphaned process stacks.
- **Do NOT launch typer via `cmd /c start ...bat`** - it flashes black console windows. Use `Start-Process pythonw.exe -WindowStyle Hidden`.
- **The machine-load problem from earlier is resolved** - Max rebooted. Orphaned processes, memory pressure, and CPU saturation from stacked Claude sessions are all cleared. Do NOT create new orphan stacks with repeated restarts - always kill all pythonw typer processes first, then launch exactly 3.
- **Meter.py is out of sync** - the stable code was reverted but `meter.py` (the green VU bar) is still the newer thicker version from today. This is cosmetic; does not affect transcription. A sharp observer (Max) will notice the bar thickness doesn't match yesterday's.
- **The normalization + best-MP3 improvements from today are NOT on the stable version** - they were built but the stable revert wiped them. They're safe to re-apply AFTER the paid Groq switch is working (they're good improvements, just got swept up in the chaos).
- **Psutil is installed in the typer venv** - the reliable kill script uses it. Do not remove it or the kill-all script breaks.
- **Playwright MCP was in use** for Groq login. Browser was closed at the end. If re-opening, note the magic-link auth flow (email to mass@tamza.com, click link). Google login requires Max's password+2FA - he must do that step himself.
- **The `_last_sample.mp3` diagnostic file** path was changed from local to temp during today's edits - if playing back a sample to Max, check where the live code writes it.
- **Commit `4a8a462a` on master is E45's FLAC change** - it's between the stable revert and HEAD. If checking out the stable commit explicitly (`74bfdf56`), that FLAC commit is NOT included (it came later).

## STABLE TYPER FEATURES (what's live right now)
- Physical key-release to send (hold Shift on release = type-only, no Enter)
- Unicode keystroke injection or `--paste` instant clipboard (history-excluded)
- Resilient warm-pool recorder: 2.0s pre-roll ring buffer, 120s idle-close, high-latency driver buffer
- 0.45s quick-tap floor (accidental bumps type nothing)
- 3.0s empty-notify threshold (short empty clips stay silent)
- Left Alt + numpad+ = RECALL (re-send last dictation)
- numpad 0 = English backup (NumLock ON or OFF)
- Right Ctrl = Russian
- Stopwatch timing instrumentation (`log_event` START/STOP/TRANSCRIBE with ms breakdown)
