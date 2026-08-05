# Typer Numpad Plus dual-target failover review

Last edited: 2026-07-31 by Codex (GPT-5.6 SOL)

Review `C:\claude_base\tools\typer\typer_e25c.py`, focusing on `_remote_gpu_busy` and `_remote_transcribe` around lines 954-1000.

Observed incident: the primary remote health probe at `192.168.1.142:8123` reported busy or unreachable, so the code selected fallback `100.83.187.123:8123`; that fallback returned HTTP 500. About one minute later the primary worked again. The existing code chooses only one endpoint per clip and does not try the other endpoint if the selected `/transcribe` request fails.

Propose a minimal, safe patch that:

- preserves the current preference: primary when its health check is good, fallback first when primary is busy/unreachable;
- if the first selected endpoint's transcription request raises, immediately tries the other configured endpoint once;
- logs the first endpoint failure and the retry endpoint without exposing secrets;
- if both fail, raises an informative error containing both endpoint failures;
- makes no changes to recording, keyboard hooks, language clamping, or paste behavior;
- preserves the exact three-leading-space behavior in `paste_text`;
- is easy to test without real network calls by monkeypatching `urllib.request.urlopen`.

Return only a compact proposed diff and test recommendations in `result.md`. Do not modify project files.
