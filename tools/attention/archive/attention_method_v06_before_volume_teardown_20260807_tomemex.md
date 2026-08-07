# Vocalize - Codex screen-flash and voice alert

Version 06, 2026-08-07, by Codex (GPT-5.6 SOL). Versions 01 through 05 remain
as historical sources.

## Purpose

Vocalize calls Max to a time-sensitive human step at the computer. It displays
a light, topmost message on every monitor and speaks the task name and request
through the built-in Realtek speakers at a moderate default volume (50 percent),
then restores the prior volume. It never changes the Windows default audio
device.

Use it only when waiting costs something within minutes: a captcha, an OAuth or
login approval, a live job at risk of failing, or a blocking decision that
cannot be deferred. Do not use it for completion notices, routine status, or
nonurgent questions.

## Codex integration

The canonical native skill is stored in Nextcloud at:

    C:\Users\maxre\Nextcloud\claude_md_synced\codex_skills\vocalize

Codex loads it through this local skill path:

    C:\Users\maxre\.codex\skills\vocalize

The stable triggers are `vocalize`, `vocalize 22`, `poke me`, and clear
equivalents asking for an in-person alert. A direct trigger fires immediately.
A standing instruction fires only when the named gated step actually arrives.

The integration is a Codex skill rather than a session hook. Vocalize is
intentional and event-specific; firing it on every prompt or session event
would be disruptive and would not identify whether a real human gate exists.

## Speech quality and fallback

Pine uses Microsoft's high-quality `en-GB-SoniaNeural` voice through the
installed `edge-tts` package. The British voice was selected to avoid the
raspy, vocal-fry-heavy American delivery Max dislikes. Attention synthesizes
once and repeats that same audio, so repeated alerts remain consistent.

Neural synthesis needs working internet access. If it fails or times out,
Attention automatically uses offline Windows SAPI speech. This fallback
preserves the alert instead of turning a temporary network problem into
silence. The output route, volume restoration, mute policy, and dismissal
behavior are identical for both voices.

Use `--tts-voice <Microsoft neural voice name>` only for a deliberate one-call
override. The stable default belongs in `attention.py`, not in individual
callers.

## Alert behavior (version 05)

- The toast is built and SHOWN before the voice thread starts, so Max always
  sees the dismiss control first. The voice never precedes the popup.
- Every toast is forced to the top of the Z-order on every monitor and stays
  there for its lifetime.
- ANY key press or ANY mouse button anywhere dismisses the alert and silences
  the voice immediately. Low-level keyboard and mouse hooks provide this
  without stealing focus; the overlay keeps WS_EX_NOACTIVATE so Max's
  dictation is never interrupted. The alert also auto-dismisses after the
  announcement finishes.
- Each alert resolves a deep link back to the session that called it and shows
  `Open session` on the toast. Codex tasks resolve to `codex://threads/<id>`
  through the `threads` table in `~/.codex/state_5.sqlite` (matched by working
  directory, newest first). Claude Code sessions resolve to
  `claude://resume?session=<id>` through the newest transcript in the matching
  `~/.claude/projects/<encoded-cwd>` folder. A caller may pass an explicit
  `--link` to override resolution.
- After an alert, a persistent history bar (`attention_history_bar.py`) shows
  a small collapsed box at the bottom of every monitor with the recent
  announcements. Clicking the box expands it into a readable list; each entry
  has an `Open session` link back to its calling task. The bar is single
  instance and refreshes from `attention.log` every two seconds.

## Local invocation

Run without a console window:

    pythonw C:/claude_base/tools/attention/attention.py \
        --session "Codex: <short task label>" \
        --msg "<short request>"

If no custom message is supplied, use `This Codex task needs your attention`.

Useful options:

- `--number`: optional task number.
- `--seconds`: fixed overlay duration. The default zero stays visible through the spoken announcement.
- `--repeat`: speech repetitions; default three.
- `--device`: output name substring; default `Realtek`.
- `--volume`: temporary target volume from 0 to 100; default 50.
- `--tts-voice`: Microsoft neural voice name; default `en-GB-SoniaNeural`.
- `--link`: explicit session deep link; auto-resolved when omitted.
- `--no-voice`: screen only.
- `--no-screen`: voice only.
- `--color`: `amber`, `red`, or `green`.
- `--to Pine`: send to another machine through fleetcomm. Delivery may take roughly two minutes.

Click anywhere, press any key, or click any mouse button to dismiss all
overlays and stop the voice. The history bar at the bottom of the screens
remains after dismissal so Max can read what was announced and reopen its
session.

## History and troubleshooting

Every call is appended to the local, ignored `attention.log` beside the
script. Inspect recent calls without firing another alert:

    python C:/claude_base/tools/attention/attention.py --history 15

Each completed invocation adds a second record: `played`, `dismissed`,
`failed`, or `suppressed-or-disabled`. A call record alone proves only that the
process started; require the result record before reporting that speech played.

On 2026-07-31, Windows recorded intermittent access violations in `_ctypes.pyd`
while pycaw/comtypes handled the Realtek endpoint. Version 03 isolates all Core
Audio COM access in `audio_endpoint_helper.py`, whose forced clean exit prevents
COM teardown from killing the flash-and-speech process.

On 2026-08-07, the alert process crashed inside Tk graphics (`tcl86t.dll`)
after the voice had started, leaving a call record with no result. Version 05
removes the window transparency attribute (a known Tk crash vector), shows the
overlay before starting the voice, and adds the low-level dismiss hooks, so the
popup is always dismissible before and during speech.

The log records the time, task label, request, working directory, process, and
local user so a mystery or repeated alarm can be traced.

## Standalone launcher (desktop and Start menu)

The history bar can also be opened on demand when no alert is running, so Max
can review recent announcements and reopen their sessions from the desktop or
Start. `launch\Install Attention History Shortcuts.ps1` creates two shortcuts
named `Attention History`:

- Desktop (`Attention History.lnk`), using the real Desktop path read from the
  registry (OneDrive-redirected on Pine).
- Start menu Programs folder, then pins the app to Start.

Both shortcuts run `pythonw.exe attention_history_bar.py` with the attention
tool folder as the working directory and use
`assets\attention_history_bar.ico` (rebuildable with
`assets\build_icon_v01.py`). The bar is single instance: if it is already
running, launching the shortcut is a harmless no-op because the named mutex
keeps only one bar alive.

Re-run the installer after moving the tool folder or changing the launcher;
it is idempotent.

Dependencies on a new Windows receiver are Python with tkinter plus `edge-tts`,
`sounddevice`, `soundfile`, `numpy`, `pycaw`, and `comtypes`. Offline Windows
SAPI is the speech fallback. Install missing packages with:

    python -m pip install edge-tts sounddevice soundfile numpy pycaw comtypes

## Verification procedure

1. Validate the skill structure with the Codex skill validator.
2. Confirm all Python dependencies import.
3. Synthesize a neural test clip and verify that `soundfile` reads it as 24 kHz mono audio.
4. Temporarily simulate neural failure and verify that SAPI still produces a playable wave file.
5. Run a screen-only one-second alert with one repetition.
6. Run one complete screen-and-voice alert and confirm it is logged as `played`.
7. Confirm the history bar appears at the bottom of every monitor, expands on
   click, and shows a deep link for the calling session.
8. Inspect history and verify the entry has the `Codex:` task label.
9. Verify the canonical global rules and the native Codex mirror contain the Vocalize rule and are byte-identical.
