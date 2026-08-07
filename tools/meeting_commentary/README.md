# DNA Vibe live meeting commentary

Last edited: 2026-08-07 by Codex (GPT-5.6 SOL)

## Purpose

This light-theme Windows app listens to the current default speaker output,
transcribes a live Zoom meeting through the established Typewriter2 speech
service, and explains each segment in plain international Ph.D.-level English.
It focuses on American corporate subtext, indirect speech, business jargon,
food and sports references, humor, and implied actions.

## Version and location

- Current first release: `live_commentary_v01.py`
- Hidden launcher: `start_live_commentary_v01.vbs`
- Parent project: `C:\claude_base\tools`

The tool reuses Typewriter2's maintained Python environment and service setup.
It does not alter or stop any Typewriter2 dictation instance.

## Use

1. Keep Zoom playing through the Windows default speaker.
2. Open `start_live_commentary_v01.vbs`.
3. Select **Start listening**.
4. Read each **HEARD** transcript followed by **WHAT IT MEANS**.
5. Select **Stop listening** before changing Zoom's speaker output.

The app notices a default-output change and reconnects automatically. It captures
speaker output only, not Max's microphone, so Max's own voice is not duplicated.

Optional auto-start: set the environment variable `MEETING_COMMENTARY_AUTOSTART=1`
before launching and the app begins listening on its own a moment after the
window opens, with no button click needed.

## Privacy and retention

Meeting audio goes to the same Groq speech-to-text route used by Typewriter2.
Short transcript fragments go to OpenAI for explanation. The app does not save
meeting audio, transcript, or commentary. It writes only timing and error data to
`%LOCALAPPDATA%\DNA Vibe Commentary\diagnostics.log`.

## Retention and recovery

Source and documentation belong in Git. The diagnostic log is disposable and
must not be committed. No unique meeting material is retained by this version.

## Troubleshooting

- If nothing appears, confirm Zoom is playing through the Windows default speaker.
- If the app reports a setup error, Typewriter2's existing provider setup needs repair.
- If delay grows, stop and restart; the bounded queue deliberately drops an older
  segment instead of allowing unlimited lag.
