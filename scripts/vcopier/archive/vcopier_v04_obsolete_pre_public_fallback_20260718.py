"""
Vcopier v02 - YouTube to VK copier | 2026-05-11
Download a YouTube video and upload it to the configured VK community.
The YouTube title is copied automatically to the VK title.

Usage:
  python vcopier.py <youtube_url> [--no-wall] [--no-source-link] [--keep-days N]

Defaults:
  - VK token:    C:\\Users\\maxre\\Nextcloud\\zSyncMain\\ssh\\vk_user_token.txt
  - VK group id: C:\\Users\\maxre\\Nextcloud\\zSyncMain\\ssh\\vk_group_id.txt
  - Cache dir:   C:\\Users\\maxre\\Downloads\\vcopier_cache
  - Rate limit:  12.5 MB/s (~100 Mbps) on yt-dlp side
  - Retention:   cache files older than 30 days are deleted on every run

Skips re-download if a matching yt_<date>_<id>_*.mp4 (no .part) already
exists in the cache.

Exit codes:
  0 ok / 2 bad args/missing config / 3 yt-dlp error
  4 VK API error / 5 VK upload server error
"""
import argparse, subprocess, sys, pathlib, json, datetime, time
import requests

VERSION = "v04"  # 2026-05-11 tidy data root D:\vcopier\{cache,logs} on Cent
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

def _pick(paths):
    for p in paths:
        if pathlib.Path(p).exists():
            return pathlib.Path(p)
    return pathlib.Path(paths[0])

CACHE_DIR = _pick([
    r"C:\Users\maxre\Downloads\vcopier_cache",
    r"D:\vcopier\cache",
])
CACHE_DIR.mkdir(parents=True, exist_ok=True)
TOKEN_FILE = _pick([
    r"C:\Users\maxre\Nextcloud\zSyncMain\ssh\vk_user_token.txt",
    r"D:\Nextcloud\zSyncMain\ssh\vk_user_token.txt",
    r"C:\Users\mremp\Nextcloud\zSyncMain\ssh\vk_user_token.txt",
])
GROUP_FILE = _pick([
    r"C:\Users\maxre\Nextcloud\zSyncMain\ssh\vk_group_id.txt",
    r"D:\Nextcloud\zSyncMain\ssh\vk_group_id.txt",
    r"C:\Users\mremp\Nextcloud\zSyncMain\ssh\vk_group_id.txt",
])
# Logs sit next to the cache to keep code/data cleanly separated.
LOGS = CACHE_DIR.parent / "logs" if CACHE_DIR.name == "cache" else pathlib.Path(__file__).parent / "logs"
LOGS.mkdir(parents=True, exist_ok=True)
API = "https://api.vk.com/method"
API_VERSION = "5.199"
DEFAULT_KEEP_DAYS = 30


def prune_cache(keep_days):
    """Delete cached files older than keep_days. Only touches CACHE_DIR."""
    if not CACHE_DIR.is_dir():
        return 0
    cutoff = time.time() - keep_days * 86400
    deleted = 0
    for p in CACHE_DIR.iterdir():
        try:
            if p.is_file() and p.stat().st_mtime < cutoff:
                p.unlink()
                deleted += 1
        except OSError:
            pass
    if deleted:
        print(f"pruned {deleted} cached file(s) older than {keep_days} days")
    return deleted


def probe(url):
    """Return (id, title, upload_date). Uses --dump-json (always UTF-8) so Cyrillic survives."""
    r = subprocess.run(
        ["yt-dlp", "--cookies-from-browser", "firefox", "--no-playlist", "--no-download", "--dump-json", url],
        capture_output=True,
    )
    if r.returncode != 0:
        sys.stderr.buffer.write(b"yt-dlp probe failed:\n" + r.stderr); sys.exit(3)
    # Last non-empty line is the JSON for this video.
    last = b""
    for line in r.stdout.splitlines():
        if line.strip().startswith(b"{"):
            last = line
    if not last:
        sys.stderr.write("yt-dlp probe gave no JSON\n"); sys.exit(3)
    info = json.loads(last.decode("utf-8"))
    return info["id"], info["title"], info.get("upload_date", "")


def download(url, stamp):
    template = str(CACHE_DIR / "yt_%(upload_date)s_%(id)s_%(title).80s.%(ext)s")
    log = LOGS / f"yt2vk_{stamp}_ytdl.log"
    cmd = [
        "yt-dlp",
        "--cookies-from-browser", "firefox",
        "-f", "bv*[height<=720]+ba/b[height<=720]",
        "--merge-output-format", "mp4",
        "--limit-rate", "12.5M",
        "--no-playlist",
        "-o", template,
        url,
    ]
    print(f"downloading ({log.name})...", flush=True)
    with open(log, "w", encoding="utf-8") as lf:
        r = subprocess.run(cmd, stdout=lf, stderr=subprocess.STDOUT)
    if r.returncode != 0:
        print(f"yt-dlp download failed rc={r.returncode}, see {log}", file=sys.stderr); sys.exit(3)


def find_local(vid, date):
    candidates = [p for p in CACHE_DIR.glob(f"yt_{date}_{vid}_*.mp4")
                  if not p.name.endswith(".part")]
    return candidates[0] if candidates else None


def vk_call(method, token, params):
    p = dict(params); p["access_token"] = token; p["v"] = API_VERSION
    r = requests.post(f"{API}/{method}", data=p, timeout=60)
    r.raise_for_status()
    j = r.json()
    if "error" in j:
        print(json.dumps(j["error"], ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(4)
    return j["response"]


def upload(fpath, title, desc, token, group_id, post_to_wall):
    save = vk_call("video.save", token, {
        "name": title, "description": desc, "group_id": group_id,
        "wallpost": 1 if post_to_wall else 0, "is_private": 0,
    })
    upload_url = save["upload_url"]
    video_id = save.get("video_id"); owner_id = save.get("owner_id")
    size = fpath.stat().st_size
    print(f"uploading {size/1e9:.2f} GB to VK ...", flush=True)
    t0 = time.time()
    with open(fpath, "rb") as f:
        r = requests.post(upload_url, files={"video_file": (fpath.name, f, "video/mp4")}, timeout=None)
    if r.status_code != 200:
        print(f"upload server failed: {r.status_code} {r.text[:500]}", file=sys.stderr); sys.exit(5)
    dt = time.time() - t0
    print(f"uploaded in {dt:.0f}s ({size/1e6/max(dt,1):.1f} MB/s)")
    return owner_id, video_id


def main():
    ap = argparse.ArgumentParser(description=f"Vcopier {VERSION} - YouTube to VK")
    ap.add_argument("url", help="YouTube video URL")
    ap.add_argument("--no-wall", action="store_true", help="don't post to community wall")
    ap.add_argument("--no-source-link", action="store_true", help="don't add 'Source:' line to description")
    ap.add_argument("--keep-days", type=int, default=DEFAULT_KEEP_DAYS,
                    help=f"prune cached files older than N days (default {DEFAULT_KEEP_DAYS})")
    args = ap.parse_args()

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    prune_cache(args.keep_days)

    for p in (TOKEN_FILE, GROUP_FILE):
        if not p.is_file():
            print(f"missing config: {p}", file=sys.stderr); sys.exit(2)
    token = TOKEN_FILE.read_text(encoding="utf-8").strip()
    group_id = int(GROUP_FILE.read_text(encoding="utf-8").strip())

    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    vid, title, date = probe(args.url)
    print(f"[{VERSION}] {vid} {date}")
    print(f"title: {title}")

    fpath = find_local(vid, date)
    if fpath:
        print(f"already downloaded: {fpath.name}")
    else:
        download(args.url, stamp)
        fpath = find_local(vid, date)
        if not fpath:
            print("downloaded but file not found by glob", file=sys.stderr); sys.exit(3)
        print(f"downloaded: {fpath.name}")

    desc = "" if args.no_source_link else f"Источник / Source: {args.url}"
    owner_id, video_id = upload(fpath, title, desc, token, group_id, not args.no_wall)
    print(f"VK URL: https://vk.com/video{owner_id}_{video_id}")


if __name__ == "__main__":
    main()
