"""Compare accuracy-oriented Faster-Whisper decoding settings on one saved clip.

Last edited: 2026-07-31 by Codex (GPT-5.6 SOL).
"""

import argparse
import json
import time

from faster_whisper import WhisperModel


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("audio")
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--compute", default="float16")
    parser.add_argument("--model", default="large-v3")
    args = parser.parse_args()

    model = WhisperModel(args.model, device=args.device, compute_type=args.compute)
    cases = [
        ("greedy_no_context", dict(beam_size=1, condition_on_previous_text=False,
                                   temperature=0.0)),
        ("greedy_context", dict(beam_size=1, condition_on_previous_text=True,
                                temperature=0.0)),
        ("beam3_no_context", dict(beam_size=3, condition_on_previous_text=False,
                                  temperature=0.0)),
        ("beam5_no_context", dict(beam_size=5, condition_on_previous_text=False,
                                  temperature=0.0)),
        ("beam5_context", dict(beam_size=5, condition_on_previous_text=True,
                               temperature=0.0)),
        ("beam5_no_context_hotwords", dict(
            beam_size=5, condition_on_previous_text=False, temperature=0.0,
            hotwords="Taygeta Typer Whisper numeric plus Num4 I me my you your we us our")),
    ]
    for name, options in cases:
        started = time.perf_counter()
        segments, info = model.transcribe(args.audio, language="en", **options)
        text = "".join(segment.text for segment in segments).strip()
        print(json.dumps({"case": name, "seconds": round(time.perf_counter() - started, 3),
                          "text": text}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
