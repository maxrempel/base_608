"""
v01 VK community video uploader | 2026-05-04
Uploads a local video file to a VK community via the official API.

Flow (per VK docs):
  1. video.save(name, description, group_id, access_token) -> {upload_url, video_id, owner_id}
  2. POST the file as multipart field 'video_file' to upload_url
  3. Upload server returns JSON with the saved video info

Usage:
  python vk_upload.py <file_path> --title "Title" [--desc "..."] [--group-id 12345]
                       [--token-file PATH] [--api-version 5.199]

Defaults:
  token-file:  C:\\Users\\maxre\\Nextcloud\\zSyncMain\\ssh\\vk_user_token.txt
  group-id:    read from C:\\Users\\maxre\\Nextcloud\\zSyncMain\\ssh\\vk_group_id.txt
  api-version: 5.199

Required token scopes: video, groups, offline.

Exit codes:
  0  ok
  2  bad args / missing files
  3  VK API error (returned in stderr as JSON)
  4  upload server error
"""
import argparse, json, sys, pathlib, time
import requests

VERSION = "v02"
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
DEFAULT_TOKEN_FILE = r"C:\Users\maxre\Nextcloud\zSyncMain\ssh\vk_user_token.txt"
DEFAULT_GROUP_FILE = r"C:\Users\maxre\Nextcloud\zSyncMain\ssh\vk_group_id.txt"
API = "https://api.vk.com/method"

def read_one_line(path):
    return pathlib.Path(path).read_text(encoding="utf-8").strip()

def vk_call(method, token, params, v):
    p = dict(params)
    p["access_token"] = token
    p["v"] = v
    r = requests.post(f"{API}/{method}", data=p, timeout=60)
    r.raise_for_status()
    j = r.json()
    if "error" in j:
        print(json.dumps(j["error"], ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(3)
    return j["response"]

def main():
    ap = argparse.ArgumentParser(description=f"VK community video uploader {VERSION}")
    ap.add_argument("file", help="local video file path")
    ap.add_argument("--title", required=True)
    ap.add_argument("--desc", default="")
    ap.add_argument("--group-id", type=int, default=None,
                    help="positive community id; if omitted, read from default file")
    ap.add_argument("--token-file", default=DEFAULT_TOKEN_FILE)
    ap.add_argument("--api-version", default="5.199")
    ap.add_argument("--no-wall", action="store_true",
                    help="do not post to community wall after upload")
    args = ap.parse_args()

    fpath = pathlib.Path(args.file)
    if not fpath.is_file():
        print(f"file not found: {fpath}", file=sys.stderr); sys.exit(2)

    try:
        token = read_one_line(args.token_file)
    except OSError as e:
        print(f"cannot read token: {e}", file=sys.stderr); sys.exit(2)
    if not token:
        print("token file empty", file=sys.stderr); sys.exit(2)

    group_id = args.group_id
    if group_id is None:
        try:
            group_id = int(read_one_line(DEFAULT_GROUP_FILE))
        except OSError as e:
            print(f"cannot read group id: {e}", file=sys.stderr); sys.exit(2)

    print(f"[{VERSION}] preparing upload: {fpath.name} -> club {group_id}")

    save = vk_call("video.save", token, {
        "name": args.title,
        "description": args.desc,
        "group_id": group_id,
        "wallpost": 0 if args.no_wall else 1,
        "is_private": 0,
    }, args.api_version)

    upload_url = save["upload_url"]
    video_id = save.get("video_id")
    owner_id = save.get("owner_id")
    print(f"got upload_url, video_id={video_id} owner_id={owner_id}")

    size = fpath.stat().st_size
    t0 = time.time()
    print(f"uploading {size/1e9:.2f} GB ...")
    with open(fpath, "rb") as f:
        r = requests.post(upload_url, files={"video_file": (fpath.name, f, "video/mp4")}, timeout=None)
    dt = time.time() - t0
    if r.status_code != 200:
        print(f"upload failed: {r.status_code} {r.text[:500]}", file=sys.stderr); sys.exit(4)
    try:
        body = r.json()
    except ValueError:
        body = {"raw": r.text[:500]}
    print(f"uploaded in {dt:.0f}s ({size/1e6/max(dt,1):.1f} MB/s)")
    print(json.dumps(body, ensure_ascii=False, indent=2))
    print(f"video URL: https://vk.com/video{owner_id}_{video_id}")

if __name__ == "__main__":
    main()
