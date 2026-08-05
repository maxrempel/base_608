"""
v01 YouTube single-video downloader | 2026-05-04
Download one video to the standard Windows Downloads folder.

Usage:
  python yt_get.py <video_id | url | index_from_last_list> [--rate 12.5M]
                   [--out C:\\Users\\maxre\\Downloads]

Resolves a bare integer as an index into the most recent listing
(./logs/latest_list.json written by yt_list.py).

Filename template: yt_<upload_date>_<id>_<title80>.mp4
Format: bv*+ba/b merged to mp4
Default throttle: 12.5 MB/s (~100 Mbps)

Exit codes:
  0 ok
  2 bad args / unresolved index
  3 yt-dlp error
"""
import argparse, json, subprocess, sys, datetime, pathlib, re

VERSION = "v02"
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
HERE = pathlib.Path(__file__).parent
LOGS = HERE / "logs"
LOGS.mkdir(exist_ok=True)
DEFAULT_OUT = pathlib.Path(r"C:\Users\maxre\Downloads")

def resolve_target(arg):
    # full URL
    if arg.startswith("http"):
        return arg
    # 11-char YouTube id
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", arg):
        return f"https://www.youtube.com/watch?v={arg}"
    # integer index into latest list
    if arg.isdigit():
        latest = LOGS / "latest_list.json"
        if not latest.is_file():
            print("no latest_list.json; run yt_list.py first", file=sys.stderr); sys.exit(2)
        data = json.loads(latest.read_text(encoding="utf-8"))
        n = int(arg)
        for r in data["rows"]:
            if r["n"] == n:
                return r["url"]
        print(f"index {n} not found in latest list", file=sys.stderr); sys.exit(2)
    print(f"cannot interpret target: {arg}", file=sys.stderr); sys.exit(2)

def main():
    ap = argparse.ArgumentParser(description=f"YouTube downloader {VERSION}")
    ap.add_argument("target", help="video id, full URL, or index from last yt_list run")
    ap.add_argument("--rate", default="12.5M", help="yt-dlp --limit-rate (default 12.5M ~ 100 Mbps)")
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    args = ap.parse_args()

    out_dir = pathlib.Path(args.out); out_dir.mkdir(parents=True, exist_ok=True)
    url = resolve_target(args.target)
    template = str(out_dir / "yt_%(upload_date)s_%(id)s_%(title).80s.%(ext)s")
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log = LOGS / f"get_{stamp}.log"

    cmd = [
        "yt-dlp",
        "-f", "bv*+ba/b",
        "--merge-output-format", "mp4",
        "--limit-rate", args.rate,
        "--no-playlist",
        "-o", template,
        url,
    ]
    print(f"[{VERSION}] downloading {url}")
    print(f"out: {out_dir}")
    print(f"log: {log}")
    with open(log, "w", encoding="utf-8") as lf:
        r = subprocess.run(cmd, stdout=lf, stderr=subprocess.STDOUT)
    if r.returncode != 0:
        print(f"FAILED rc={r.returncode}, see {log}", file=sys.stderr); sys.exit(3)
    print("OK")

if __name__ == "__main__":
    main()
