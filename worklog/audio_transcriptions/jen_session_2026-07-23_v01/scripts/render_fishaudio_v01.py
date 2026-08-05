"""Render a retained text file to MP3 with Max's Fish Audio account."""

from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path


KEY_PATH = Path(r"C:\Users\maxre\Nextcloud\zSyncMain\ssh\fishaudio_api_key_20260226.txt")
URL = "https://api.fish.audio/v1/tts"
MODEL = "s1"
MALE_NARRATOR = "efc2f5153a24463dbfe54acd93a145f8"


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: render_fishaudio_v01.py INPUT.txt OUTPUT.mp3")
        return 2
    source = Path(sys.argv[1])
    output = Path(sys.argv[2])
    key = next(line.strip() for line in KEY_PATH.read_text(encoding="utf-8").splitlines() if line.strip())
    text = source.read_text(encoding="utf-8-sig").strip()
    payload = {
        "text": text,
        "format": "mp3",
        "reference_id": MALE_NARRATOR,
        "normalize": True,
        "latency": "normal",
    }
    request = urllib.request.Request(
        URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "model": MODEL,
        },
        method="POST",
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(request, timeout=1800) as response, output.open("wb") as target:
        while chunk := response.read(1024 * 1024):
            target.write(chunk)
    data = output.read_bytes()[:16]
    if not (data.startswith(b"ID3") or (len(data) > 1 and data[0] == 0xFF and data[1] & 0xE0 == 0xE0)):
        raise RuntimeError("Fish Audio response is not an MP3")
    print(f"Rendered {len(text)} characters to {output.stat().st_size} MP3 bytes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
