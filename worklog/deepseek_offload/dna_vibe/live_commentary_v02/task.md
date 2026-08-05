# DNA Vibe live meeting commentary app, version 02

Last edited: 2026-07-31 by Codex (GPT-5.6 SOL)

## Objective

Design a compact, reliable Windows desktop app for Max that captures the current
default speaker output, especially a live Zoom meeting, transcribes speech in
short chunks using the existing Typewriter2 speech stack, and displays each
transcript segment beside a fast explanation in plain international Ph.D.-level
English.

The explanation must translate implicit American corporate meaning, business
jargon, sports or food metaphors, humor, euphemism, indirect disagreement,
status and power signals, and implied action. Preserve technical depth and do
not simplify scientific content. If no hidden meaning exists, give the simple
literal meaning briefly. Never invent context.

## Existing environment to inspect

- Typewriter2 implementation:
  `C:\claude_base\tools\typer\typer_e25c.py`
- Typewriter2 method:
  `C:\claude_base\tools\typer\typer_method_v01_tomemex.md`
- Python runtime:
  `C:\claude_base\tools\typer\venv\Scripts\python.exe`
- Installed and verified libraries: `soundcard`, `sounddevice`, `soundfile`,
  `numpy`, `openai`, and `tkinter`.
- Speaker loopback capture is verified through SoundCard using the current
  default speaker, `Speakers (Realtek(R) Audio)`, at 16 kHz stereo.
- Reuse the already configured Typewriter2 API setup without displaying or
  moving any private configuration values.

## Product requirements

1. Light-theme desktop window, readable at a glance during Zoom.
2. Start and Stop control, clear status, latency display, and scrollable feed.
3. Each item shows time, verbatim transcript, and a concise explanation.
4. A few seconds of delay is acceptable. Prefer robust 4 to 6 second rolling
   chunks with a small overlap or silence-aware boundaries so words are not cut.
5. Capture speaker loopback only by default, not Max's microphone, to avoid echo
   and duplicate self-transcription.
6. Keep recent context so explanations understand pronouns and callbacks, but
   do not rewrite earlier transcript or fabricate speaker names.
7. If explanation fails, show the transcript immediately and a clear retry state.
8. Log only runtime diagnostics, not meeting text. Do not persist meeting audio
   or transcript unless Max explicitly chooses to save later.
9. Hidden launcher with no visible terminal window.
10. Clean stop, restart, default-device change handling, and bounded queues so a
    slow service cannot create unlimited lag.
11. Reuse Typewriter2 transcription mechanisms where practical without changing
    or destabilizing the running dictation instances.
12. Create a sibling tool under `C:\claude_base\tools\meeting_commentary\`, with
    a concise README and versioned names.

## Requested result

Return a concise, implementation-ready design in `result.md`, including exact
thread and queue boundaries, chunking, safe reuse of current transcription,
the exact commentary system prompt, compact file plan, failure cases, acceptance
tests, and Windows or SoundCard traps found by inspecting the existing code.

Do not use another model or fallback. Do not expose private configuration values
or meeting data.
