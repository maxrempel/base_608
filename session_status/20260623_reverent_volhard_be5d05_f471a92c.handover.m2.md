# Scribe handover - milestone 2 (~152K tokens)
# session: 20260623_reverent_volhard_be5d05_f471a92c
# cwd: C:\claude_base\.claude\worktrees\reverent-volhard-be5d05
# written: 2026-06-23 16:53:43 by deepseek-v4-pro

# HANDOVER - Attention Alarm Tool (Screen + Voice)

---

## GOAL (Max's words)

Build a local "attention" tool that any Claude session can call when it needs Max in person (e.g., a captcha to solve). It must:
- Flash a standardized message on **both screens** - visible, but not intrusive.
- Synthesize a voice announcement on the **laptop built-in speakers** (not the default audio device, which might be a headset), at **full volume**.
- Announce the session name and number so Max knows who's calling.
- Be usable via simple voice-dictation-friendly trigger phrases stored in global rules so every session (old and new) has access.
- **Vocalize only for time-sensitive/critical things.** Everything else stays on Telegram/email.

---

## DECISIONS MADE + WHY

### 1. Audio routing: bypass default device, force laptop speakers
- **Problem:** Python's SAPI (and thus `pythonw`) played to the default audio device, which was a plugged-in headset - useless when Max isn't wearing it.
- **Fix:** Synthesize speech to a temporary WAV file, then play it through `sounddevice` targeting device index for `"Speakers (Realtek(R) Audio)"` directly. Used `pycaw` (`AudioUtilities`) to set that specific endpoint to full volume, play the audio, then restore the prior volume.
- **Result:** Voice always comes out the laptop speakers at full blast, regardless of what's plugged in or what the Windows default device is. Headset/default device is never touched.

### 2. Visual: small, semi-transparent, no-focus toast (top-right, both screens)
- **Problem v1:** First version was a fullscreen window that grabbed focus - stole dictation focus, interrupted Max's work.
- **Fix:** Switched to a small (400?150) semi-transparent (`alpha=0.85`) `Toplevel` window positioned at top-right of each monitor. Uses `overrideredirect(True)` so no title bar, plus `attributes('-alpha', 0.85)` for transparency. Kept click-to-dismiss behavior; added `wm_attributes('-topmost', True)` so it floats but never takes focus (no `focus_force()`).
- **Important note:** The window does NOT steal keyboard focus - dictation is safe.

### 3. Auto-dismiss at 4s + manual click dismiss
- **Decision:** Both. Toast disappears after 4 seconds. Clicking it dismisses immediately AND silences the voice (sets an `Event` that the voice thread checks).
- **Crucial fix:** The 4s timer originally killed the whole process, which cut off voice mid-announcement. Now the timer only destroys the toast window; the process stays alive and **joins the voice thread** so the full announcement plays. Only a click-dismiss (which sets a `stopped` event) silences the voice early.

### 4. Logging - who called, from which session
- **Problem:** A runaway was screaming every ~3 minutes, but there was no log, so Max couldn't tell which session or why.
- **Fix:** Every call writes to `C:/claude_base/tools/attention/attention.log` with: timestamp, caller's working directory (maps to the session's worktree), PID, PPID, session name, session number, and the message text.
- **Outcome:** Next time anything calls attention.py, the log immediately identifies the culprit session.

### 5. Trigger phrases registered in global2.md
- **Decision:** Narrowed to three canonical commands after Max's feedback:
  - `"poke me"`
  - `"vocalize"`
  - `"vocalize 22"` (longest, most reliable for voice dictation)
- These are in `global2.md` (auto-loaded by every session via `@global2.md` in the root CLAUDE.md), so every session - old and new - knows them.
- The global rule also encodes the **TIME-SENSITIVE ONLY** criterion: only vocalize if waiting costs something soon. Otherwise, use Telegram/email.

### 6. Time-sensitive is THE main criterion
- Max explicitly corrected: time-sensitivity, not just criticality, is the gate. Reworded both the global rule and the method doc to lead with: "does waiting cost something soon?" Only then vocalize.

---

## CURRENT STATE

**What's done and committed/merged to master:**
- `C:/claude_base/tools/attention/attention.py` - the alarm tool (screen toast + laptop-speaker voice)
- `C:/claude_base/tools/attention/attention_method_v01_tomemex.md` - method documentation
- `C:/claude_base/tools/attention/attention.log` - runtime log (gitignored)
- Global rule in `C:/Users/maxre/Nextcloud/claude_md_synced/global2.md` (ATTENTION block at top)
- All commits merged to `master` on the claude_base repo

**Bugs already fixed:**
- Audio no longer cut off by 4s timer dismissal
- Logging exists and records caller worktree, PID, message, timestamp
- Toast is small, see-through, no-focus

**What's in flight / unresolved:**
- **The runaway:** Was screaming every ~3 minutes. A 5-minute watcher caught **zero** calls to attention.py. A second 15-minute watcher was launched. It may have stopped on its own, OR it could be using a different TTS source entirely. No other Python speech code exists on the machine (grep confirmed only `attention.py` uses `System.Speech` / `Speak` / `PlaySound`).

- **Message not telling which session:** When the transcript was interrupted, I was about to implement auto-derivation of session identity from the caller's worktree, by reusing the same `cwd_key` approach from `bcast.py` (which hashes the working directory to name sessions). This would make `--session` auto-populated, so the toast and voice always say WHO is calling even if the caller forgets the flag.

---

## EXACT NEXT STEP

1. **Finish auto-deriving session identity.** In `attention.py`'s `main()`, detect the caller's working directory, derive the session name from it (mirroring bcast's `cwd_key` logic - hash the worktree path, produce a shortname like `b7-grok`), and auto-set `--session` and `--number` if not explicitly provided. This guarantees the toast and voice always say "Session X, number Y" even when the calling session forgets to pass those flags.

2. **Check the 15-minute watcher result** (task `byynugqje` or its successor). If the runaway fires again, the log now captures its worktree - identify which session, what it wanted, and stop it.

3. **If the watcher stays silent** and the screaming has genuinely stopped, consider it resolved (the runaway may have been a one-off from an earlier version that has since been killed or finished).

---

## OPEN QUESTIONS FOR MAX

1. **Is the screaming STILL happening, or has it stopped completely?** If stopped, the runaway may have been a transient from an old process that died.

2. **Should I also add the ability to silence/kill a runaway automatically** once identified, or just report the session name so Max stops it manually?

3. **For the auto-derived session identity:** Should the format mirror bcast exactly (e.g., `b7-grok` style), or do you want a different naming convention for attention alerts?

---

## KEY PATHS / IDs

| What | Path |
|---|---|
| Attention tool | `C:/claude_base/tools/attention/attention.py` |
| Method doc | `C:/claude_base/tools/attention/attention_method_v01_tomemex.md` |
| Log file | `C:/claude_base/tools/attention/attention.log` |
| Global rules (auto-loaded) | `C:/Users/maxre/Nextcloud/claude_md_synced/global2.md` |
| Gitignore for log | `C:/claude_base/tools/attention/.gitignore` |
| Bcast identity reference | `C:/claude_base/branch_bulletin/bcast.py` (cwd_key, state JSONs) |
| Watcher task ID | `byynugqje` (completed, nothing caught) |
| Session worktree (this session) | `C:\claude_base\.claude\worktrees\reverent-volhard-be5d05` |
| Target audio device | `"Speakers (Realtek(R) Audio)"` via sounddevice + pycaw |

---

## GOTCHAS / DEAD ENDS

- **Do NOT use `focus_force()` or fullscreen** - steals dictation focus. Toast must be small, `overrideredirect`, `-topmost`, semi-transparent, no activation.
- **Do NOT kill the process on timer** - must `join()` the voice thread so audio finishes. Only click-dismiss (`stopped.set()`) can silence voice early.
- **Audio output device index is 5** for `"Speakers (Realtek(R) Audio)"` (as queried via `sounddevice.query_devices()`). This may change if drivers update; the script queries by name substring match, not hardcoded index.
- **No other TTS code exists** on the machine besides `attention.py` - if screaming continues but the log stays empty, the source is not this tool.
- **`pythonw` suppresses console windows** - always use it for the alarm so no terminal flashes. The tool still logs to file.
