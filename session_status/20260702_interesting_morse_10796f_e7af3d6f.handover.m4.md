# Scribe handover - milestone 4 (~300K tokens)
# session: 20260702_interesting_morse_10796f_e7af3d6f
# cwd: C:\claude_base\.claude\worktrees\interesting-morse-10796f
# written: 2026-07-02 16:38:01 by deepseek-v4-pro

# HANDOVER - E25C (numpad 9 / plus key typer improvements)

## GOAL (in Max's own words)
- "So, your button will be number nine. Implement whatever on number nine, the best version you can with all improvements we discussed in it during the day."
- Later, after numpad 9 was working: "copy F9 to plus sign so that would be my main script right now." The good build was then promoted to the plus key (and F9) as Max's daily driver.
- Speed, sound quality, reliability, and eventually multi?message?in?order were the focus.

## WHAT HAPPENED
A new, isolated instance was built from the best?known config (fast Groq, large?v3, best?quality MP3, normalize, keystroke delivery) and placed on **both the numpad plus key and F9**, in the file `typer_e25c.py`. The old slow plus instance (which ran `typer_stable.py`) was killed. The zero?key instance, Russian, and all sibling sessions were left untouched.

During testing, three problems surfaced and were addressed:
1. **Numpad 9 dead** - NumLock was off. The instance now listens for the PageUp scan code as well so the key works regardless of NumLock.
2. **Speed oscillation** - Groq server response time swings wildly (0.4 s to 17 s), 100?% on their side. A keep?alive (warm?keeper) was turned on, then off, then back on with a new schedule after Max asked for it.
3. **Missing dictation** - One clip disappeared; the fix was switching from clipboard paste to **keystroke injection** (verifies every character, retries dropped ones, impossible to vanish silently).
4. **User wanted to distinguish recording vs. transcribing on the bar** - a custom purple progress bar was added.

## KEY DECISIONS AND THEIR REASONS
- **Use paid Groq + large?v3** - earlier commits proved "turbo" mis?recognises simple words; paid tier avoids rate?limit crises.
- **MP3 best quality** - the size difference among quality levels is tiny for short speech, and encoding takes ~0.15 s even for 20?second clips, so there's zero speed penalty.
- **Normalize ON** - boosts quiet audio, already fixed the "weird/quiet" bug.
- **Keystroke delivery, not instant paste** - silent disappearances are more disruptive than a brief typing animation; Max agreed.
- **Warm?keeper off** was tried, then back on because the first call after a pause was cold (up to 10?s). The pings are currently set to **every 20?seconds for 20 minutes** (Max's last request). The exact interval and duration may need tuning.
- **Recordings saved for every dictation** - requested by Max so he can check audio quality. All clips land in `Downloads\typer_recordings`.

## CURRENT STATE - WHAT IS IN FLIGHT
- **File**: `C:\claude_base\tools\typer\typer_e25c.py` plus its companion meter `meter_e25c.py` and launcher `start_typer_e25c.bat`.
- **Running processes**: The plus key **and** numpad 9 both run `typer_e25c.py` (same executable). The last action was editing the file to set warm?keeper to **20?s / 20?min** and then restarting both the plus key and numpad 9 instances. **The session was interrupted during that restart**, so we don't know if the new processes are alive and running with the new settings.
- **Audio quality assessment**: Rec files are being saved. Max said "I hate the quality of the sound" and wants to listen to every recording. He hasn't reported back on *how* it sounds bad (muffled/dull vs. crunchy). The next session needs to ask and then tune (likely either sample?rate down?saver or reduce normalisation).
- **Multi?message in order**: Max's request ("dictate several messages in a row, they come back in order while previous still processing") has **not** been implemented yet.
- **Board notice**: All siblings were told hands?off the plus key; no other session should be touching it.

## EXACT NEXT STEP (for the cold session)
1. **Check processes** - see if `typer_e25c.py` is running for both plus and numpad 9, and that the warm?keeper is active (grep log for 'WARM' or 'ping'). If not, restart them from the batch file `start_typer_e25c.bat` (or via PowerShell as in prior turns).
2. **Tell Max**: "Keep?alive is ON, pinging every 20 seconds for 20 minutes. The first dictation after a cold start may still be slow, but subsequent ones should stay warm. Test the speed and tell me if it still oscillates."
3. **Audio feedback loop**: "Have you listened to a few of the saved recordings? Please tell me if they sound muffled (dull, lacking highs) or crunchy (distorted, clipping). Based on your answer I'll fix the audio."
4. **Next feature (if speed/quality are satisfied)**: implement **multi?message pipelining** (queue dictations, process in background, deliver results in FIFO order, typed at the cursor). That's the major pending ask.

## OPEN QUESTIONS AWAITING MAX
- How does the audio actually sound? (muffled ? sample rate; crunchy ? normalisation)
- Is the warm?keeper at 20?s/20?min giving consistent speed? If not, should we try a different interval or switch to Groq's **turbo** model / **OpenAI** to compare?
- Does he prefer the keystroke animation on his main key, or revert to instant paste (with the small disappearance risk)?

## KEY PATHS, FILES, IDS
- `C:\claude_base\tools\typer\typer_e25c.py` - E25C's best build (now on plus/F9 and numpad 9). Contains the config.
- `C:\claude_base\tools\typer\meter_e25c.py` - custom meter with purple progress.
- `C:\claude_base\tools\typer\start_typer_e25c.bat` - launcher.
- Logs: `C:\claude_base\tools\typer\typer_runtime_e25c_en.log`
- Recordings: `C:\Users\maxre\Downloads\typer_recordings\rec_*.mp3`
- Sample files: `C:\Users\maxre\Downloads\typer_quality_samples\` (includes `SENT_TO_GROQ_*.mp3`)
- Repository: `C:\claude_base`, master branch, two additive files committed under E25C.
- Bulletin board: `python C:\claude_base\branch_bulletin\bcast.py`
- No other files (zero, Russian, sibling?owned `typer.py`) were touched.

## GOTCHAS & DEAD ENDS ALREADY RULED OUT
- **Lybraries**: `pyperclip` import is dead weight (not used). No need to fix unless cleaning up.
- **Groq model**: The "turbo" string bug is already fixed in the running version (it uses `large-v3`).
- **NumLock**: The numpad 9 fix listens for **both** the digit code (NumLock ON) and the PageUp code (NumLock OFF). No further NumLock sensitivity remains.
- **Slow responses are NOT local**. The logs prove the encode time is <0.2 s; the entire delay is Groq server response. File?size levers won't help.
- **Duplicate processes cause clipboard fights** - the zero?key instance already has a duplicate problem; we solved it for E25C instances by having only one per key. The new plus key instance doesn't duplicate.
- **Warm?keeper pinging on free tier can trigger rate limits** - safe on paid tier, but 20?s/20?min may still be heavy; monitor for any rate?limit responses in the log.
