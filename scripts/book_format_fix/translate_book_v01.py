#!/usr/bin/env python3
"""Translate a per-chapter book folder from one language to English using the Claude API.

Reads NN_*.md chapter files from --src, translates each faithfully to English with
Claude, and writes same-named files to --dst. Preserves markdown structure and the
leading H1 "Book Title - SECTION" format so the existing flat importer still works.

Usage:
  python translate_book_v01.py --src <dir> --dst <dir> --book-title "Gods About Us" [--limit N] [--model ...]

Progress is printed (UTF-8) and also appended to <dst>/_translate_log.txt.
Failures are logged loudly and the file is SKIPPED (no silent fallback / no partial junk).
"""
import sys, os, re, argparse, datetime, json, urllib.request, urllib.error

# Switched off Anthropic 2026-06-13 (cost) to DeepSeek v4-pro (smart, 1M window).
KEY_FILE = r"C:\Users\maxre\Nextcloud\zSyncMain\ssh\deepseek_api_key_20260226.txt"
DS_URL = "https://api.deepseek.com/chat/completions"
DEFAULT_MODEL = "deepseek-v4-pro"


def ds_call(api_key, model, prompt, max_tokens=12000):
    # v4-pro is a reasoning model (spends reasoning tokens before the visible
    # answer), so the budget is generous to avoid truncating a long chapter.
    body = json.dumps({
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }).encode("utf-8")
    req = urllib.request.Request(DS_URL, data=body, headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }, method="POST")
    with urllib.request.urlopen(req, timeout=300) as r:
        data = json.loads(r.read().decode("utf-8"))
    return (data["choices"][0]["message"].get("content") or "").strip()


def log(dst, msg):
    line = f"[{datetime.datetime.now():%H:%M:%S}] {msg}"
    print(line, flush=True)
    with open(os.path.join(dst, "_translate_log.txt"), "a", encoding="utf-8") as f:
        f.write(line + "\n")


def translate_chapter(api_key, model, book_title, md):
    prompt = (
        "You are translating a chapter of the spiritual/metaphysical book "
        f"\"{book_title}\" by Max Rempel from Russian into natural, fluent English.\n\n"
        "RULES:\n"
        "- Translate faithfully and completely. Do not summarize, omit, or add anything.\n"
        "- Preserve the Markdown structure exactly (headings #/##/###, blank lines, *italics*, **bold**).\n"
        "- The first line is an H1 of the form '# <Book Title> - <SECTION NAME>'. Translate BOTH parts "
        f"to English, keeping the ' - ' separator and using the book title '{book_title}'.\n"
        "- If there is an attribution line like '*Из книги \"...\", Макс Ремпель*', render it in English "
        f"as '*From \"{book_title}\" by Max Rempel, Ph.D.*'.\n"
        "- Keep the author's calm, direct, teacherly voice. Keep metaphysical terms consistent.\n"
        "- Output ONLY the translated Markdown. No preamble, no notes, no code fences.\n\n"
        "RUSSIAN CHAPTER:\n\n" + md
    )
    return ds_call(api_key, model, prompt)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--dst", required=True)
    ap.add_argument("--book-title", required=True)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    args = ap.parse_args()

    os.makedirs(args.dst, exist_ok=True)
    key = open(KEY_FILE, encoding="utf-8").read().strip()

    files = sorted(f for f in os.listdir(args.src) if f.endswith(".md") and re.match(r"^\d+_", f))
    if args.limit:
        files = files[:args.limit]
    log(args.dst, f"=== translate start: {len(files)} files, model={args.model} ===")

    ok = fail = skip = 0
    for fn in files:
        out_path = os.path.join(args.dst, fn)
        if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
            skip += 1
            log(args.dst, f"skip (exists): {fn}")
            continue
        md = open(os.path.join(args.src, fn), encoding="utf-8").read()
        try:
            en = translate_chapter(key, args.model, args.book_title, md)
            if not en or len(en) < 20:
                raise ValueError(f"suspiciously short output ({len(en)} chars)")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(en + "\n")
            ok += 1
            log(args.dst, f"OK {fn} ({len(md)}->{len(en)} chars)")
        except Exception as e:
            fail += 1
            log(args.dst, f"FAIL {fn}: {e}")
    log(args.dst, f"=== done: ok={ok} skip={skip} fail={fail} ===")


if __name__ == "__main__":
    main()
