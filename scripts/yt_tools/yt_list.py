"""
v01 YouTube channel video lister | 2026-05-04
List recent videos from a YouTube channel using yt-dlp.

Usage:
  python yt_list.py <channel_url> [--limit 50]

Output:
  - prints numbered table to stdout: # | id | upload_date | duration | title
  - writes the same list as JSON to ./logs/list_<timestamp>.json
    so yt_get.py can resolve an index from the most recent listing.

Exit codes:
  0 ok
  2 bad args / no entries
  3 yt-dlp invocation error
"""
import argparse, json, subprocess, sys, datetime, pathlib

VERSION = "v02"
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
HERE = pathlib.Path(__file__).parent
LOGS = HERE / "logs"
LOGS.mkdir(exist_ok=True)

def fmt_dur(s):
    if not s: return "?"
    s = int(s); h, r = divmod(s, 3600); m, s = divmod(r, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

def main():
    ap = argparse.ArgumentParser(description=f"YouTube channel lister {VERSION}")
    ap.add_argument("channel_url")
    ap.add_argument("--limit", type=int, default=50)
    args = ap.parse_args()

    cmd = [
        "yt-dlp", "--flat-playlist", "-J",
        "--playlist-end", str(args.limit),
        args.channel_url,
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    except FileNotFoundError:
        print("yt-dlp not found in PATH", file=sys.stderr); sys.exit(3)
    if r.returncode != 0:
        print(r.stderr, file=sys.stderr); sys.exit(3)

    try:
        data = json.loads(r.stdout)
    except json.JSONDecodeError as e:
        print(f"bad JSON from yt-dlp: {e}", file=sys.stderr); sys.exit(3)

    entries = data.get("entries") or []
    # If channel page returns nested tabs (Videos / Shorts / Live), flatten one level.
    flat = []
    for e in entries:
        if e is None: continue
        if e.get("_type") == "playlist" and e.get("entries"):
            flat.extend([x for x in e["entries"] if x])
        else:
            flat.append(e)
    entries = flat[: args.limit]

    if not entries:
        print("no entries found", file=sys.stderr); sys.exit(2)

    rows = []
    for i, e in enumerate(entries, 1):
        rows.append({
            "n": i,
            "id": e.get("id"),
            "upload_date": e.get("upload_date") or "",
            "duration": e.get("duration"),
            "title": e.get("title") or "",
            "url": e.get("url") or f"https://www.youtube.com/watch?v={e.get('id')}",
        })

    print(f"{'#':>3}  {'id':<11}  {'date':<8}  {'dur':<8}  title")
    for r in rows:
        print(f"{r['n']:>3}  {r['id']:<11}  {r['upload_date']:<8}  {fmt_dur(r['duration']):<8}  {r['title'][:90]}")

    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out = LOGS / f"list_{stamp}.json"
    out.write_text(json.dumps({"channel": args.channel_url, "rows": rows}, ensure_ascii=False, indent=2), encoding="utf-8")
    # also overwrite a 'latest' pointer for easy lookup by yt_get
    (LOGS / "latest_list.json").write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"\nsaved: {out}")

if __name__ == "__main__":
    main()
