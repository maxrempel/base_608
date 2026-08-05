# Scribe handover - milestone 5 (~381K tokens)
# session: 20260702_interesting_morse_10796f_e7af3d6f
# cwd: C:\claude_base\.claude\worktrees\interesting-morse-10796f
# written: 2026-07-02 17:25:58 by deepseek-v4-pro

**Handover - E25C (Max's typer session)**  

---

### **GOAL (in Max's words - the actual desired outcome)**  
Max wanted a **fast, reliable voice?typing system** that uses paid Groq (large?v3, not turbo), with no silent drops, accurate dictation, ability to recall the last message (Alt + key), a dictionary log he can copy from, a progress bar that shows real timings and lingers so he can read it, and recently: **a calibrated progress bar with logarithmic tick marks and second numbers** ("mark the seconds 1,2,3,4,5,6,7 seconds ... make logarithmic").  
All this should run on his three preferred keys: **numpad + (plus) / F9, numpad 9, and Russian on Right Ctrl**, with **no other typer instances competing for Groq**.

---

### **DECISIONS MADE + WHY**  

1. **Engine:** Paid Groq, model `large-v3` (not `turbo`).  
   - *Why:* Early testing showed turbo had poor accuracy ("sucks"). `large-v3` is slower but gets the words right, which Max values.

2. **Audio encoding:** MP3 (best quality, ``quality=0``), 16 kHz, with loudness **normalization** enabled.  
   - *Why:* MP3 files are tiny (~20-90 KB), encoding takes <0.5 s (proven from logs). Lossless would offer no speed gain. Normalization fixed the "quiet/weird" sound.

3. **Delivery method:** **Keystroke mode** (types characters directly, verifies each, re?sends dropped ones).  
   - *Why:* Clipboard paste (`Ctrl+V`) sometimes silently swallowed text (the "third message disappeared" bug). Keystroke mode cannot silently drop. The typing animation is a minor visual cost for total reliability.

4. **Recall (Alt + key):** Fixed; kept.  
   - *Why:* Originally the Alt modifier clashed with Windows numpad codes and broke typing. The fix releases Alt before pasting, and the key bindings accept both NumLock ON and OFF states so it works regardless.

5. **Warm?keeper (pinging Groq):** Experimented with; **NOT active** in the final canonical build.  
   - *Why:* On the free tier pings caused rate?limit crashes. Even on paid, pings sometimes increased Groq's latency (cold starts became worse). Leaving it off proved more stable; if Max later wants to re?enable, it can be done as a toggle.

6. **Isolation:** Each of the three keys runs the **same** good build but with its own talk?key binding and memory. No other typer processes (old zero, old num1, etc.) are allowed - all were killed to eliminate Groq competition.

7. **Progress bar calibration:** A **logarithmic scale with tick marks and numbers** (1,2,3,4,5,7,10,15,20 seconds) is currently **only on num9** (sandbox meter `meter_e25c_test.py`). The plain bar (no ticks) still runs on plus and Russian.  
   - *Why:* Max wants to see exactly how long Groq is taking, even on longer pauses. The logarithmic squeeze makes both short and long times readable.

---

### **CURRENT STATE**  

**What is done (live on the machine):**  

- Three typer instances running, all from the canonical good build (`typer_e25c.py`):  
  - **numpad + / F9** (English, main) - plain meter, recall Alt+plus works.  
  - **numpad 9** (English, test?bed) - **calibrated meter** (`meter_e25c_test.py`) with ticks and numbers; recall Alt+9 works.  
  - **Right Ctrl** (Russian) - plain meter, same good build.  

- The old `zero`, `num1`, stale Russian, and all other typer processes are **dead** - not competing for Groq.  

- Groq model: `large-v3`, with the paid API key from `C:\Users\maxre\Nextcloud\zSyncMain\ssh\groq_api_key_20260611.txt`.  

- Keystroke delivery: ON (no clipboard, no silent drops).  

- Normalization: ON (quiet boosts).  

- Recall: fixed (Alt released before typing).  

- Dictation text log: every dictation is appended to `C:\Users\maxre\Downloads\typer_dictation_log.txt`.  

- Timing log file (for Max to inspect): `Downloads\typer_timings_all.txt` (full 108?run table, local?encode vs Groq time).  

- Quality samples files: in `Downloads\typer_recordings\` (recording was stopped; a few old files may remain).  

- Launchers: `start_typer_e25c.bat` (for num9, add `--recall num9` etc.), and the canonical is started directly via Python with appropriate arguments for each key.  

**What is in flight / ready to test:**  

- The **calibrated progress bar** on **num9 only**. Max must test it, confirm the tick scale feels right, then give the go?ahead to move it to plus and Russian.  

---

### **EXACT NEXT STEP**  

1. **Max tests num9's calibrated bar.** He holds num9, dictates, watches the purple progress bar with tick marks and numbers (1,2,3,4,5,7,10,15,20), and sees the final time linger ~1.5?s.  
2. **Max reports back:** Does the scale look right? Are the ticks readable? Should any tick positions change?  
3. **Once Max approves,** this session (or a new session) needs to:  
   - Overwrite the plain meter (`meter_e25c.py`) with the calibrated version, or point plus and Russian's launchers to `meter_e25c_test.py`.  
   - Restart the plus and Russian instances (Max must **explicitly order** the restart - do NOT touch them otherwise).  

Note: The current num9 instance **already** uses the calibrated meter; no change needed for testing.

---

### **OPEN QUESTIONS STILL AWAITING MAX**  

- Does he want the warm?keeper re?enabled? (Not yet asked after the final three?key setup.)  
- Would he like the calibrated bar on plus and Russian after testing? (Explicit go?ahead needed before touching those keys.)  
- Should the old `typer_e25c_test.py` sandbox and `meter_e25c_test.py` be cleaned up after graduation, or kept as a separate test key?  

---

### **KEY FILE PATHS, IDS, COMMANDS**  

| Item | Path / Value |
|------|--------------|
| **Good build (canonical)** | `C:\claude_base\tools\typer\typer_e25c.py` |
| **Plain meter (plus / Russian)** | `C:\claude_base\tools\typer\meter_e25c.py` |
| **Calibrated meter (num9)** | `C:\claude_base\tools\typer\meter_e25c_test.py` |
| **Test sandbox (may be obsolete)** | `C:\claude_base\tools\typer\typer_e25c_test.py` |
| **Launcher for num9** | `C:\claude_base\tools\typer\start_typer_e25c.bat` |
| **Dictation text log** | `C:\Users\maxre\Downloads\typer_dictation_log.txt` |
| **Timing table (all runs)** | `C:\Users\maxre\Downloads\typer_timings_all.txt` |
| **Recordings folder (samples)** | `C:\Users\maxre\Downloads\typer_recordings\` |
| **Groq API key** | `C:\Users\maxre\Nextcloud\zSyncMain\ssh\groq_api_key_20260611.txt` |
| **Repo** | `C:\claude_base` (master branch) |
| **Branch bulletin board** | `python C:\claude_base\branch_bulletin\bcast.py` |

**Running instances (do NOT kill without Max's order):**  
- Process `pythonw.exe` with argument `typer_e25c.py` and `f9,numplus` ? plus/F9 main English.  
- Process with `num9,numpgup` ? num9 English (calibrated bar).  
- Process with `rctrl` ? Russian on Right Ctrl.

**How to restart plus (only after Max says "restart plus"):**  
```
Stop-Process the matching pythonw.exe, then launch:
pythonw.exe C:\claude_base\tools\typer\typer_e25c.py --key f9,numplus --recall numplus --log-en en
```
(Similarly for Russian, key `rctrl`).

---

### **GOTCHAS AND DEAD ENDS**  

1. **Never touch plus or Russian without Max's explicit "restart plus" command.**  
2. **Clipboard paste mode is a dead end** - it caused silent message loss. The canonical build always uses keystroke delivery; do not fall back to `--paste`.  
3. **Turbo model is a dead end** - Max found its accuracy unacceptable; do not offer it again.  
4. **Warm?keeper pings can backfire** - even on paid Groq they sometimes increased latency. The current canonical has pings OFF. If Max requests them, test carefully and log the effect.  
5. **NumLock dependency** - The key bindings already handle both states, but Max must be reminded that holding numpad digits with NumLock off sends different key codes; the bindings are set for both, so it works either way.  
6. **Alt?recall interference** - Originally Alt + key broke because Alt didn't release. The fix works now; if any breakage reappears, consult the patch that releases Alt (`pyautogui.keyUp('alt')`) before typing.  
7. **Log file names** - The canonical log is `typer_runtime_e25c_en.log`; the num9 sandbox used `typer_runtime_e25ctest_en.log` but after the final three?key cleanup, num9 was re?launched pointing to the same canonical `typer_e25c.py`, so the log location may have changed. Verify by checking the matching pythonw.exe command line.  
8. **The calibrated meter used on num9 is from `meter_e25c_test.py`** - if plus is restarted na?vely, it will still load the plain `meter_e25c.py`. When promoting the calibrated bar, either modify `meter_e25c.py` or point plus's launcher to the test meter.  

---

### **SESSION NOTE FOR RESUMPTION**  

This session built, tested, and deployed a full typer system from a bug?hunting start to a three?key stable setup. The only outstanding task is **Max's verdict on the calibrated progress bar** - that is the immediate next action. Once he's happy, the bar will be rolled out to his main keys, completing the project.
