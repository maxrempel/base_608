"""
v01 initial download wrapper | 2026-05-02
Download an Odysee video via yt-dlp into ./downloads/
Usage: python download_odysee.py <odysee_url>
"""
import sys, subprocess, datetime, pathlib

VERSION = "v01"
HERE = pathlib.Path(__file__).parent
OUT = HERE / "downloads"
LOGS = HERE / "logs"
OUT.mkdir(exist_ok=True)
LOGS.mkdir(exist_ok=True)

def main():
    if len(sys.argv) < 2:
        print("Usage: python download_odysee.py <odysee_url>")
        sys.exit(1)
    url = sys.argv[1]
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log = LOGS / f"download_{stamp}.log"
    template = str(OUT / f"{stamp}_%(title).80s.%(ext)s")
    cmd = [
        "yt-dlp",
        "-f", "bv*+ba/b",
        "--merge-output-format", "mp4",
        "-o", template,
        "--no-playlist",
        url,
    ]
    print(f"[{VERSION}] downloading {url}")
    print(f"log: {log}")
    with open(log, "w", encoding="utf-8") as lf:
        r = subprocess.run(cmd, stdout=lf, stderr=subprocess.STDOUT)
    if r.returncode != 0:
        print(f"FAILED rc={r.returncode}, see {log}")
        sys.exit(r.returncode)
    files = sorted(OUT.glob(f"{stamp}_*"), key=lambda p: p.stat().st_mtime)
    if files:
        print(f"OK -> {files[-1]}")
    else:
        print("WARN: no output file detected")

if __name__ == "__main__":
    main()
