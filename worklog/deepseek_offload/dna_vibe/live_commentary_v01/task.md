# DNA Vibe live meeting commentary app, version 01

Last edited: 2026-07-31 by Codex (GPT-5.6 SOL)

## Objective

Design a compact, reliable Windows desktop app for Max that captures the current
default speaker output (especially a live Zoom meeting), transcribes speech in
short chunks using the existing Typewriter2 speech stack, and displays each
transcript segment beside a fast explanation in plain international Ph.D.-level
English.

The explanation must translate implicit American corporate meaning, business
jargon, sports or food metaphors, humor, euphemism, indirect disagreement,
status/power signals, and implied action. It must preserve technical depth and
must not dumb down scientific content. If no hidden meaning exists, say the
simple literal meaning briefly. Never invent context.

## Existing environment to inspect

- Current Typewriter2 implementation:
  `C:\claude_base\tools\typer\typer_e25c.py`
- Current method:
  `C:\claude_base\tools\typer\typer_method_v01_tomemex.md`
- Python runtime:
  `C:\claude_base\tools\typer\venv\Scripts\python.exe`
- Installed and verified: `soundcard`, `sounddevice`, `soundfile`, `numpy`,
  `openai`, `tkinter`.
- Verified speaker loopback capture works through SoundCard using the current
  default speaker, `Speakers (Realtek(R) Audio)`, at 16 kHz stereo.
- Typewriter2 loads the OpenAI key from its own `.env`; do not expose secrets.

## Product requirements

1. Light-theme desktop window, readable at a glance during Zoom.
2. Start/Stop control, clear status, latency display, and scrollable running feed.
3. Each item shows time, verbatim transcript, and a concise explanation.
4. A few seconds of delay is acceptable. Prefer robust 4-6 second rolling chunks
   with a small overlap or silence-aware boundaries so words are not clipped.
5. Capture speaker loopback only by default, not Max's microphone, to avoid echo
   and duplicate self-transcription.
6. Keep recent context so explanations understand pronouns and callbacks, but
   do not rewrite earlier transcript or fabricate speaker names.
7. Work remains usable if explanation fails: transcript appears immediately and
   the explanation can show a clear error/retry state.
8. Log de-identified runtime diagnostics, not meeting text. Do not persist audio
   or transcript unless Max explicitly chooses to save later.
9. Hidden launcher: no visible terminal window.
10. Clean stop, restart, default-device change handling, and bounded queues so a
    slow API cannot create unlimited lag.
11. Reuse Typewriter2 transcription mechanisms and credential loading where
    practical without modifying or destabilizing current dictation instances.
12. Create this as a sibling tool under
    `C:\claude_base\tools\meeting_commentary\`, with README and versioned names.

## Requested result

Return a concise but implementation-ready design in `result.md`, including:

- exact architecture and thread/queue boundaries;
- recommended chunking algorithm;
- how to call current Typewriter2 transcription safely;
- the exact commentary system prompt;
- a compact file plan;
- high-risk failure cases and acceptance tests;
- any specific Windows/SoundCard traps discovered from inspecting the code.

Do not use another model or fallback. Do not reveal credentials or meeting data.
