# Vocalize - Codex screen-flash and voice alert

Version 07, 2026-08-07, by Codex (GPT-5.6 SOL). Versions 01 through 06 remain
as historical sources.

## Purpose

Vocalize calls Max to a time-sensitive human step at the computer. It displays
a light, topmost message on every monitor and speaks the task name and request
through the built-in Realtek speakers at a moderate default volume (42 percent,
15 percent quieter than the old 50), then restores the prior volume. It never
changes the Windows default audio device.

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

## Alert behavior (version 07)

- The toast is built and SHOWN before the voice thread starts, so Max always
  sees the dismiss control first. The voice never precedes the popup.
- Every toast is forced to the top of the Z-order on every monitor and stays
  there for its lifetime.
- ANY key press or ANY mouse button anywhere dismisses the alert and silences
  the voice immediately. Low-level keyboard and mouse hooks provide this
  without stealing focus; the overlay keeps WS_EX_NOACTIVATE so Max's
  dictation is never interrupted. The alert also auto-dismisses after the
  announcement finishes.
- The dismiss hooks declare their 64-bit argument types explicitly, so the
  dismissing key or click is forwarded to the app below instead of being
  swallowed. Before this fix, a hook exception on 64-bit Windows consumed the
  input and Max's typing lost characters while an alert was open.
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
  instance and refreshes from `attention.log` every two seconds. Both the
  collapsed and the expanded bar have a visible X close button that closes the
  bar without toggling it.
- Speaker routing prefers the built-in Realtek speakers. If that device is
  absent, the alert plays on EVERY available output device so it is heard on
  at least one speaker instead of silently using the Windows default.

## Crash history and teardown safety (version 07)

On 2026-08-07 the alert process repeatedly aborted inside Tk graphics
(`tcl86t.dll`, exception `0x80000003`, Tcl panic `Tcl_AsyncDelete: async
handler deleted by the wrong thread`) a few seconds after an alert was
dismissed, leaving a call record with no `result` line: the silent-alert bug.
The crash only occurred while the voice thread was still alive during Tk
teardown; with `--no-voice` it never reproduced. Root cause: the Tcl
interpreter could be deallocated from the audio thread during teardown.

Version 07 changes the teardown order so this cannot happen:

1. The voice thread is joined (capped at 8 seconds) BEFORE any Tk window is
   destroyed, so no other thread is alive while the interpreter is released.
2. Pending `after` timers are cancelled before destruction, removing
   interpreter references to the polling callback.
3. Remaining Tkinter reference cycles are collected with `gc.collect()` on the
   Tk thread so the Tcl interpreter is released deterministically.

The fix is structurally verified (syntax, ordering, code review) and the crash
mechanism is reproduced in the WER log, but a final on-air confirmation alert
should be run before treating the silent-alert bug as closed (step 6 below).

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
- `--volume`: temporary target volume from 0 to 100; default 42.
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
removed the window transparency attribute (a known Tk crash vector), showed the
overlay before starting the voice, and added the low-level dismiss hooks.
Version 07 fixed the remaining teardown race (see "Crash history and teardown
safety" above) and the hook argument bug that swallowed dismissed keys.

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
6. Run one complete screen-and-voice alert and confirm it is logged as `played`
   (final on-air confirmation for the version 07 teardown fix; do this when
   Max can hear it).
7. Confirm the history bar appears at the bottom of every monitor, expands on
   click, shows a deep link for the calling session, and its X closes it in
   both states.
8. Inspect history and verify the entry has the `Codex:` task label.
9. Verify the canonical global rules and the native Codex mirror contain the Vocalize rule and are byte-identical.
