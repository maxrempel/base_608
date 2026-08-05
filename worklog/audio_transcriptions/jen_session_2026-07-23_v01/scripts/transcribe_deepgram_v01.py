"""Transcribe the Jen 2026-07-23 session with Deepgram Nova 3.

Writes both the provider JSON and a readable speaker/timestamp transcript.
The API key is read from Max's credential store and is never printed.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import requests


KEY_PATH = Path(r"C:\Users\maxre\Nextcloud\zSyncMain\ssh\deepgram_key_20260515.txt")


def stamp(seconds: float) -> str:
    total = int(seconds)
    return f"{total // 3600:02d}:{(total % 3600) // 60:02d}:{total % 60:02d}"


def main() -> int:
    if len(sys.argv) != 4:
        print("Usage: transcribe_deepgram_v01.py INPUT.mp3 OUTPUT.json OUTPUT.txt")
        return 2

    source, json_path, text_path = map(Path, sys.argv[1:])
    key = KEY_PATH.read_text(encoding="utf-8").strip()
    params = {
        "model": "nova-3",
        "language": "en",
        "smart_format": "true",
        "punctuate": "true",
        "paragraphs": "true",
        "utterances": "true",
        "diarize": "true",
        "detect_entities": "true",
    }
    with source.open("rb") as audio:
        response = requests.post(
            "https://api.deepgram.com/v1/listen",
            params=params,
            headers={"Authorization": f"Token {key}", "Content-Type": "audio/mpeg"},
            data=audio,
            timeout=(60, 1800),
        )
    response.raise_for_status()
    payload = response.json()
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    utterances = payload.get("results", {}).get("utterances", [])
    lines = [
        "Jen Session, July 23, 2026",
        "Automated transcript with Deepgram Nova 3 speaker separation",
        "Speaker numbers are inferred and may occasionally switch.",
        "",
    ]
    for utterance in utterances:
        speaker = int(utterance.get("speaker", 0)) + 1
        lines.append(f"[{stamp(float(utterance.get('start', 0)))}] Speaker {speaker}: {utterance.get('transcript', '').strip()}")
    if not utterances:
        transcript = payload["results"]["channels"][0]["alternatives"][0]["transcript"]
        lines.extend(["[00:00:00] Transcript:", transcript])
    text_path.write_text("\n\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {len(utterances)} utterances and {text_path.stat().st_size} transcript bytes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
