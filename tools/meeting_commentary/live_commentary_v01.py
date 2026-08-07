"""DNA Vibe live meeting transcript and cultural/business commentary.

Last edited: 2026-08-07 by Codex (GPT-5.6 SOL)
"""

from __future__ import annotations

import collections
import logging
import os
import queue
import re
import tempfile
import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

import numpy as np
import soundcard as sc
import soundfile as sf
from openai import OpenAI


APP_TITLE = "DNA Vibe Live Meaning"
SAMPLE_RATE = 16_000
BLOCK_SECONDS = 0.20
BLOCK_FRAMES = int(SAMPLE_RATE * BLOCK_SECONDS)
MIN_CHUNK_SECONDS = 1.2
MAX_CHUNK_SECONDS = 7.0
END_SILENCE_SECONDS = 0.65
PRE_ROLL_BLOCKS = 2
VOICE_FLOOR = 0.0008
QUEUE_LIMIT = 3
COMMENTARY_MODEL = os.environ.get("MEETING_COMMENTARY_MODEL", "gpt-4.1-mini")

TOOL_DIR = Path(__file__).resolve().parent
TYPER_DIR = TOOL_DIR.parent / "typer"
OPENAI_ENV_CANDIDATES = (
    TYPER_DIR / ".env",
    Path(r"C:\tools\whisper-writer\.env"),
)
GROQ_KEY_PATH = Path(
    r"C:\Users\maxre\Nextcloud\zSyncMain\ssh\groq_api_key_20260611.txt"
)
RUNTIME_DIR = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / "DNA Vibe Commentary"
LOG_PATH = RUNTIME_DIR / "diagnostics.log"

SYSTEM_PROMPT = """You are Max's live interpreter during an American business meeting.
Max is an international Ph.D. who understands advanced scientific and technical ideas but can miss unstated American corporate meaning and unfamiliar cultural references.

For the CURRENT transcript segment, explain what a well-informed American insider would understand. Translate corporate jargon, indirect disagreement, euphemism, humor, politeness, power or status signals, sports metaphors, food references, and implied requests or commitments. Preserve technical precision. Do not dumb down scientific content. Never invent a hidden message, speaker identity, fact, or intention. Use recent transcript only as context, and clearly mark uncertainty.

Write for immediate reading during a live meeting. Always give one short line beginning "Meaning:". Then add only relevant lines from "Reference:", "Subtext:", and "Action:", in that order. Use each label at most once and combine multiple references into one sentence. "Action:" means a task or commitment requested by the speaker; omit it when there is no task, and never use it merely to say what Max should understand. Each line must be one plain sentence. If the statement is already literal and clear, the Meaning line alone is enough. Do not restate the full transcript. Do not advise Max what opinion to hold."""

_STOCK_HALLUCINATION = re.compile(
    r"^[\s\W]*(thank you(?: for watching)?|thanks for watching|you|bye|goodbye)[\s\W]*$",
    re.IGNORECASE,
)


def configure_logging() -> None:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=LOG_PATH,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        encoding="utf-8",
    )


def load_named_value(paths: tuple[Path, ...], name: str) -> str | None:
    for path in paths:
        try:
            for raw in path.read_text(encoding="utf-8").splitlines():
                line = raw.strip()
                if line.startswith(name + "="):
                    return line.split("=", 1)[1].strip().strip("'\"")
        except FileNotFoundError:
            continue
    return os.environ.get(name)


def normalize_audio(audio: np.ndarray, target_db: float = -20.0) -> np.ndarray:
    audio = np.asarray(audio, dtype=np.float32).reshape(-1)
    if not len(audio):
        return audio
    rms = float(np.sqrt(np.mean(np.square(audio, dtype=np.float64))))
    if rms < 1e-7:
        return audio
    target = 10 ** (target_db / 20.0)
    gain = min(target / rms, 20.0)
    audio = audio * gain
    peak = float(np.max(np.abs(audio)))
    if peak > 0.89:
        audio *= 0.89 / peak
    return audio.astype(np.float32)


def dedupe_overlap(previous: str, current: str) -> str:
    """Remove exact word overlap created by the audio boundary pre-roll."""
    old = previous.split()
    new = current.split()
    for count in range(min(10, len(old), len(new)), 1, -1):
        left = [re.sub(r"\W", "", x).lower() for x in old[-count:]]
        right = [re.sub(r"\W", "", x).lower() for x in new[:count]]
        if left == right:
            return " ".join(new[count:]).strip()
    return current.strip()


class SpeechChunker:
    def __init__(self) -> None:
        self.pre_roll: collections.deque[np.ndarray] = collections.deque(maxlen=PRE_ROLL_BLOCKS)
        self.blocks: list[np.ndarray] = []
        self.silence_seconds = 0.0
        self.voiced_seconds = 0.0
        self.noise_floor = 0.00015

    def reset_active(self) -> None:
        self.blocks = []
        self.silence_seconds = 0.0
        self.voiced_seconds = 0.0

    def add(self, block: np.ndarray) -> np.ndarray | None:
        mono = np.asarray(block, dtype=np.float32)
        if mono.ndim == 2:
            mono = mono.mean(axis=1)
        mono = mono.reshape(-1)
        rms = float(np.sqrt(np.mean(np.square(mono, dtype=np.float64))))
        threshold = max(VOICE_FLOOR, self.noise_floor * 3.0)
        voiced = rms >= threshold

        if not self.blocks:
            if not voiced:
                self.noise_floor = 0.98 * self.noise_floor + 0.02 * min(rms, VOICE_FLOOR)
                self.pre_roll.append(mono)
                return None
            self.blocks.extend(self.pre_roll)
            self.pre_roll.clear()

        self.blocks.append(mono)
        if voiced:
            self.voiced_seconds += BLOCK_SECONDS
            self.silence_seconds = 0.0
        else:
            self.silence_seconds += BLOCK_SECONDS

        duration = len(self.blocks) * BLOCK_SECONDS
        natural_end = duration >= MIN_CHUNK_SECONDS and self.silence_seconds >= END_SILENCE_SECONDS
        forced_end = duration >= MAX_CHUNK_SECONDS
        if not (natural_end or forced_end):
            return None

        audio = np.concatenate(self.blocks)
        enough_speech = self.voiced_seconds >= 0.35
        overlap = list(self.blocks[-PRE_ROLL_BLOCKS:]) if forced_end else []
        self.reset_active()
        self.pre_roll.extend(overlap)
        return audio if enough_speech else None

    def finish(self) -> np.ndarray | None:
        if not self.blocks or self.voiced_seconds < 0.35:
            self.reset_active()
            return None
        audio = np.concatenate(self.blocks)
        self.reset_active()
        return audio


class MeetingEngine:
    def __init__(self, emit) -> None:
        self.emit = emit
        self.running = threading.Event()
        self.audio_queue: queue.Queue[tuple[float, np.ndarray]] = queue.Queue(maxsize=QUEUE_LIMIT)
        self.capture_thread: threading.Thread | None = None
        self.worker_thread: threading.Thread | None = None
        self.stt_client: OpenAI | None = None
        self.comment_client: OpenAI | None = None
        self.context: collections.deque[str] = collections.deque(maxlen=4)
        self.last_transcript = ""
        self.started_at = 0.0

    def _make_clients(self) -> None:
        groq_key = GROQ_KEY_PATH.read_text(encoding="utf-8").strip()
        openai_key = load_named_value(OPENAI_ENV_CANDIDATES, "OPENAI_API_KEY")
        if not groq_key:
            raise RuntimeError("Typewriter2 Groq setup is empty")
        if not openai_key:
            raise RuntimeError("Typewriter2 OpenAI setup was not found")
        self.stt_client = OpenAI(
            api_key=groq_key,
            base_url="https://api.groq.com/openai/v1",
            max_retries=1,
            timeout=20.0,
        )
        self.comment_client = OpenAI(
            api_key=openai_key,
            base_url="https://api.openai.com/v1",
            max_retries=1,
            timeout=20.0,
        )

    def start(self) -> None:
        if self.running.is_set():
            return
        self._make_clients()
        self.running.set()
        self.started_at = time.time()
        self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.worker_thread = threading.Thread(target=self._work_loop, daemon=True)
        self.capture_thread.start()
        self.worker_thread.start()

    def stop(self) -> None:
        self.running.clear()

    def _enqueue(self, audio: np.ndarray) -> None:
        job = (time.time(), audio)
        try:
            self.audio_queue.put_nowait(job)
        except queue.Full:
            try:
                self.audio_queue.get_nowait()
            except queue.Empty:
                pass
            self.audio_queue.put_nowait(job)
            logging.warning("audio queue full; oldest unprocessed chunk dropped")
            self.emit("warning", "Commentary fell behind; one older segment was skipped.")

    def _capture_loop(self) -> None:
        chunker = SpeechChunker()
        while self.running.is_set():
            try:
                speaker = sc.default_speaker()
                loopback = sc.get_microphone(speaker.id, include_loopback=True)
                self.emit("device", speaker.name)
                logging.info("capture opened on default speaker: %s", speaker.name)
                opened_at = time.monotonic()
                with loopback.recorder(samplerate=SAMPLE_RATE, blocksize=BLOCK_FRAMES) as recorder:
                    while self.running.is_set():
                        block = recorder.record(numframes=BLOCK_FRAMES)
                        complete = chunker.add(block)
                        if complete is not None:
                            self._enqueue(complete)
                        if time.monotonic() - opened_at >= 5.0:
                            current = sc.default_speaker()
                            if current.id != speaker.id:
                                self.emit("status", "Audio output changed; reconnecting...")
                                break
                            opened_at = time.monotonic()
            except Exception as exc:
                logging.exception("capture error")
                self.emit("error", "Audio capture problem: %s" % exc)
                time.sleep(1.0)
        tail = chunker.finish()
        if tail is not None:
            self._enqueue(tail)
        self.emit("status", "Finishing the last captured segment...")

    def _transcribe(self, audio: np.ndarray) -> str:
        assert self.stt_client is not None
        audio = normalize_audio(audio)
        temp_path = Path(tempfile.gettempdir()) / ("meeting_commentary_%d.wav" % time.time_ns())
        sf.write(temp_path, audio, SAMPLE_RATE, format="WAV", subtype="PCM_16")
        try:
            with temp_path.open("rb") as handle:
                result = self.stt_client.audio.transcriptions.create(
                    model="whisper-large-v3",
                    file=handle,
                    language="en",
                    response_format="json",
                )
            text = (result.text or "").strip()
            if _STOCK_HALLUCINATION.fullmatch(text):
                return ""
            return dedupe_overlap(self.last_transcript, text)
        finally:
            try:
                temp_path.unlink()
            except FileNotFoundError:
                pass

    def _comment(self, text: str) -> str:
        assert self.comment_client is not None
        recent = "\n".join("- " + item for item in self.context)
        user_input = "RECENT CONTEXT:\n%s\n\nCURRENT SEGMENT:\n%s" % (recent or "(none)", text)
        result = self.comment_client.responses.create(
            model=COMMENTARY_MODEL,
            instructions=SYSTEM_PROMPT,
            input=user_input,
            max_output_tokens=180,
        )
        return (result.output_text or "Meaning: No explanation was returned.").strip()

    def _work_loop(self) -> None:
        while (
            self.running.is_set()
            or (self.capture_thread is not None and self.capture_thread.is_alive())
            or not self.audio_queue.empty()
        ):
            try:
                captured_at, audio = self.audio_queue.get(timeout=0.25)
            except queue.Empty:
                continue
            try:
                stt_start = time.time()
                text = self._transcribe(audio)
                if not text:
                    continue
                self.last_transcript = text
                stt_seconds = time.time() - stt_start
                self.emit("transcript", (captured_at, text, stt_seconds))
                self.context.append(text)
                try:
                    comment_start = time.time()
                    explanation = self._comment(text)
                    total_lag = time.time() - captured_at
                    comment_seconds = time.time() - comment_start
                    self.emit("commentary", (explanation, total_lag, comment_seconds))
                    logging.info(
                        "segment complete audio=%.1fs stt=%.2fs comment=%.2fs total_lag=%.2fs",
                        len(audio) / SAMPLE_RATE,
                        stt_seconds,
                        comment_seconds,
                        total_lag,
                    )
                except Exception as exc:
                    logging.exception("commentary error")
                    self.emit("commentary", ("Meaning: Commentary failed: %s" % exc, time.time() - captured_at, 0.0))
            except Exception as exc:
                logging.exception("transcription error")
                self.emit("error", "Transcription problem: %s" % exc)
        self.emit("stopped", "Stopped")


class MeetingApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.events: queue.Queue[tuple[str, object]] = queue.Queue()
        self.engine = MeetingEngine(self.emit)
        self.root.title(APP_TITLE)
        self.root.geometry("920x720")
        self.root.minsize(680, 480)
        self.root.configure(bg="#f5f7fb")
        self._build()
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.after(80, self._drain_events)

    def _build(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#f5f7fb")
        style.configure("TLabel", background="#f5f7fb", foreground="#172033", font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI Semibold", 18), foreground="#12213f")
        style.configure("Start.TButton", font=("Segoe UI Semibold", 10), padding=(18, 9))

        top = ttk.Frame(self.root, padding=(18, 15, 18, 10))
        top.pack(fill="x")
        ttk.Label(top, text="DNA Vibe Live Meaning", style="Title.TLabel").pack(side="left")
        self.start_button = ttk.Button(top, text="Start listening", style="Start.TButton", command=self.toggle)
        self.start_button.pack(side="right")

        status_bar = ttk.Frame(self.root, padding=(18, 0, 18, 10))
        status_bar.pack(fill="x")
        self.status_var = tk.StringVar(value="Ready. Captures the sound coming from Zoom.")
        self.latency_var = tk.StringVar(value="")
        ttk.Label(status_bar, textvariable=self.status_var).pack(side="left")
        ttk.Label(status_bar, textvariable=self.latency_var).pack(side="right")

        footer = ttk.Label(
            self.root,
            text="Audio is transcribed through Typewriter2's existing service. Meeting text is not saved by this app.",
            padding=(18, 0, 18, 12),
            foreground="#667085",
        )
        footer.pack(side="bottom", fill="x")

        self.feed = tk.Text(
            self.root,
            wrap="word",
            bg="#ffffff",
            fg="#1c2433",
            relief="flat",
            padx=20,
            pady=16,
            font=("Segoe UI", 11),
            spacing1=2,
            spacing3=5,
            state="disabled",
        )
        scroll = ttk.Scrollbar(self.root, orient="vertical", command=self.feed.yview)
        self.feed.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y", padx=(0, 10), pady=(0, 12))
        self.feed.pack(fill="both", expand=True, padx=(18, 0), pady=(0, 12))
        self.feed.tag_configure("time", foreground="#6b7280", font=("Segoe UI Semibold", 9))
        self.feed.tag_configure("transcript_label", foreground="#2855a6", font=("Segoe UI Semibold", 10))
        self.feed.tag_configure("transcript", foreground="#172033", font=("Segoe UI", 12))
        self.feed.tag_configure("meaning_label", foreground="#19734d", font=("Segoe UI Semibold", 10))
        self.feed.tag_configure("meaning", foreground="#164e3c", font=("Segoe UI", 11))
        self.feed.tag_configure("warning", foreground="#9a3412", font=("Segoe UI Semibold", 10))

    def emit(self, kind: str, value: object) -> None:
        self.events.put((kind, value))

    def toggle(self) -> None:
        if self.engine.running.is_set():
            self.engine.stop()
            self.start_button.configure(text="Start listening", state="disabled")
            self.status_var.set("Stopping after the current audio block...")
            return
        try:
            self.engine.start()
            self.start_button.configure(text="Stop listening")
            self.status_var.set("Connecting to Zoom audio...")
        except Exception as exc:
            logging.exception("startup failed")
            messagebox.showerror(APP_TITLE, "Could not start: %s" % exc)

    def _append(self, parts: list[tuple[str, str]]) -> None:
        self.feed.configure(state="normal")
        for text, tag in parts:
            self.feed.insert("end", text, tag)
        self.feed.see("end")
        self.feed.configure(state="disabled")

    def _drain_events(self) -> None:
        try:
            while True:
                kind, value = self.events.get_nowait()
                if kind == "device":
                    self.status_var.set("Listening to Zoom audio through %s" % value)
                elif kind == "status":
                    self.status_var.set(str(value))
                elif kind == "stopped":
                    self.status_var.set("Stopped")
                    self.start_button.configure(text="Start listening", state="normal")
                elif kind == "error":
                    self.status_var.set(str(value))
                    self._append([("\n%s\n" % value, "warning")])
                elif kind == "warning":
                    self._append([("\n%s\n" % value, "warning")])
                elif kind == "transcript":
                    captured_at, text, stt_seconds = value
                    stamp = time.strftime("%I:%M:%S %p").lstrip("0")
                    self.latency_var.set("Transcript %.1fs" % stt_seconds)
                    self._append(
                        [
                            ("\n%s\n" % stamp, "time"),
                            ("HEARD\n", "transcript_label"),
                            (text + "\n", "transcript"),
                        ]
                    )
                elif kind == "commentary":
                    explanation, total_lag, comment_seconds = value
                    self.latency_var.set("Total delay %.1fs" % total_lag)
                    self._append(
                        [
                            ("WHAT IT MEANS\n", "meaning_label"),
                            (explanation + "\n", "meaning"),
                        ]
                    )
        except queue.Empty:
            pass
        self.root.after(80, self._drain_events)

    def close(self) -> None:
        self.engine.stop()
        self.root.destroy()


def main() -> None:
    configure_logging()
    logging.info("application started; meeting content logging disabled")
    root = tk.Tk()
    app = MeetingApp(root)
    autostart = os.environ.get("MEETING_COMMENTARY_AUTOSTART", "")
    if autostart and autostart.lower() not in ("0", "false", "no"):
        root.after(800, app.toggle)
    root.mainloop()


if __name__ == "__main__":
    main()
