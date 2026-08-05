# DNA Vibe live commentary audit

## 1. Critical defects that must be fixed before launch

- **Loopback capture is not guaranteed**. The capture setup appears to rely on the system default input path instead of explicitly selecting a WASAPI loopback device. On Windows, `soundcard.default_microphone()` is often the physical mic, not the Zoom speaker loopback, and using it will silently transcribe the operator’s voice instead of the meeting. `_choose_loopback()` must enumerate `soundcard.all_microphones(include_loopback=True)`, filter by a speaker-loopback name pattern, and fail loudly if no loopback device is found. Never fall back to a physical mic.

- **Single-threaded capture and transcription will cause audio loss**. If `_capture_and_transcribe()` records one block, transcribes it, then calls OpenAI before the next block, the soundcard buffer overruns. The design must split `_capture_loop()` and `_worker_loop()` so audio is continuously drained into `AUDIO_QUEUE`. The current `BLOCK_SIZE` is too small for inline API calls; even with threading, a slow Groq response can still overflow the queue.

- **Unbounded queue and no drop policy**. `AUDIO_QUEUE` is created without `maxsize`, so a stalled API can grow memory without limit and make commentary lag minutes behind the live call. Set `MAX_QUEUE_SIZE`, and when the queue is full, drop the oldest segments rather than blocking the capture thread. Track `segment_start_ms` so dropped audio is not later processed out of order.

- **Duplicate transcripts after restart or retry**. If the app restarts, the last chunk boundary is lost and the same final sentence may be transcribed twice. More importantly, if Groq times out and the code retries, the retry will often return the same transcription for the same audio. Deduplicate by storing a rolling `TRANSCRIPT_HISTORY` keyed by `(session_id, start_ms, end_ms)` and also by a normalized transcript hash. Before displaying, skip any hash already seen within the last `DEDUP_WINDOW_SECONDS`.

- **Shutdown is not reliable**. `_capture_loop` uses an infinite loop that is not guaranteed to observe `SHUTDOWN_EVENT`. The stream is not closed in a `finally`, and the worker thread may still be inside an OpenAI call during exit, leaving the process hanging or the loopback device locked. All loops must poll the event flag, workers must be joined with `SHUTDOWN_TIMEOUT_SECONDS`, and `stream.close()` must run on every shutdown path, including `KeyboardInterrupt`.

- **No timeout or exception handling on service calls**. `groq.audio.transcriptions.create()` and `openai.chat.completions.create()` need explicit `timeout=API_TIMEOUT_SECONDS` and controlled retry behavior. Currently, a transient network error can kill a thread and silently stop all future commentary. Wrap both calls in `_safe_transcribe()` and `_safe_commentary()` that return `None` and log only a sanitized error, never the meeting transcript.

- **The explanation prompt invites invented intent**. If `EXPLANATION_PROMPT` instructs the model to “infer what the speaker is really thinking” or “read between the lines without evidence,” it will produce misleading commentary. The prompt must require the model to distinguish between factual cultural explanation, plausible inference, and speculation. A better instruction is: "If an idiom or business reference has a known American corporate meaning, explain it briefly. If the speaker’s motive is unclear, say 'possibly' and cite the clues. Do not assert emotions, strategy, or hidden intent that are not directly supported by the transcript." Also add a fixed disclaimer such as "This is a possible interpretation, not the speaker's stated intent."

- **Privacy is not structurally enforced**. Audio and transcripts are sent to Groq and OpenAI, so the user must be able to see that before capture starts. The app should not write raw audio or full transcripts to log files. If `DEBUG_LOGGING` is enabled, transcripts must be redacted before logging; temporary WAV or FLAC files must be deleted in `finally` after upload. Avoid logging speaker names, meeting title, or unique personal data. The user should be informed that third-party APIs process this data.

## 2. Important improvements that can wait

- **Segmenter boundary handling**. `_segment_speech()` should require `MIN_SPEECH_MS` and `SILENCE_THRESHOLD` to be adapted to the speaker loopback level. A fixed silence threshold may split words or never end a segment during Zoom echo. Add a small trailing padding and ensure `last_segment_end` resets correctly.

- **Latency feedback and target**. Expose an on-screen latency measurement from first audio to commentary display. If median latency exceeds `LATENCY_TARGET_SECONDS`, reduce block size or stop sending already-stale segments, but never discard current live speech.

- **Device change recovery**. Zoom can disable loopback when audio is switched. Add a periodic device check and automatic reconnect with backoff instead of requiring an app restart.

- **Commentary caching**. Avoid regenerating commentary for repeated identical transcript text by using a `COMMENTARY_CACHE` keyed by transcript hash.

- **Context window for commentary**. Passing only the current segment makes explanations choppy. Maintain the last `CONTEXT_SEGMENTS` transcripts in the OpenAI prompt
