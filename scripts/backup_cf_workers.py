"""
Backup all Cloudflare Workers source code + KV namespace content to cloud_base git repo.

Created 2026-05-22 by Claude Opus 4.7 for Max after the noeticus front-page-loss disaster.
Pattern: nightly cron pulls every worker's bundle from CF API, writes to
backups/cf_workers/<worker_name>/, then a wrapper bat commits to cloud_base git.

Sister scope: KV content (the page bodies that are silently editable and currently
unversioned) is dumped to backups/cf_kv_pages/. Note: the existing
cf_kv_backup/backup_cf_kv_all_v01.py on DAX dumps KV daily too -- this is the
Pine-side duplicate (off-DAX safety, lives in maxrempel/cloud_base on GitHub).

Auth: cloudflare_workers_kv_token_20260303.txt (Workers Scripts, KV, R2, Pages,
Routes, all zones).

No fallbacks. If CF API returns non-200, raise and exit non-zero -- the wrapper bat
will skip git commit and the cron run will be visibly broken (per Max's no-silent-
fallback rule).
"""
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib import request as urlreq
from urllib.error import HTTPError, URLError

ACCOUNT_ID = "e4dc2224d6baa721873dca77dc6f057d"
TOKEN_FILE = Path(r"C:\Users\maxre\Nextcloud\zSyncMain\ssh\cloudflare_workers_kv_token_20260303.txt")
OUT_ROOT = Path(r"C:\cloud_base\backups")
WORKERS_DIR = OUT_ROOT / "cf_workers"
KV_DIR = OUT_ROOT / "cf_kv_pages"
LOG_FILE = OUT_ROOT / "backup_cf.log"

CF = "https://api.cloudflare.com/client/v4"


def log(msg):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def load_token():
    text = TOKEN_FILE.read_text(encoding="utf-8")
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        return s
    raise RuntimeError(f"No token found in {TOKEN_FILE}")


def cf_get(path, token, raw=False):
    req = urlreq.Request(f"{CF}{path}", headers={"Authorization": f"Bearer {token}"})
    with urlreq.urlopen(req, timeout=60) as resp:
        body = resp.read()
        ctype = resp.headers.get("Content-Type", "")
    if raw:
        return body, ctype
    return json.loads(body.decode("utf-8"))


def list_workers(token):
    data = cf_get(f"/accounts/{ACCOUNT_ID}/workers/scripts", token)
    if not data.get("success"):
        raise RuntimeError(f"list_workers failed: {data}")
    return data["result"]


def fetch_worker(name, token):
    body, ctype = cf_get(f"/accounts/{ACCOUNT_ID}/workers/scripts/{name}", token, raw=True)
    return body, ctype


def parse_multipart(body, ctype):
    """Parse the multipart/form-data response from CF worker script GET.
    Returns dict {filename: content_bytes}."""
    m = re.search(r'boundary="?([^";]+)"?', ctype)
    if not m:
        return {"worker.bin": body}
    boundary = ("--" + m.group(1)).encode()
    parts = body.split(boundary)
    out = {}
    for part in parts:
        part = part.strip(b"\r\n-")
        if not part or part == b"--":
            continue
        if b"\r\n\r\n" not in part:
            continue
        headers, content = part.split(b"\r\n\r\n", 1)
        hdr_text = headers.decode("utf-8", errors="replace")
        fn = re.search(r'filename="([^"]+)"', hdr_text)
        if not fn:
            nm = re.search(r'name="([^"]+)"', hdr_text)
            if not nm:
                continue
            fname = nm.group(1)
        else:
            fname = fn.group(1)
        content = content.rstrip(b"\r\n-")
        out[fname] = content
    return out


def list_kv_namespaces(token):
    out = []
    page = 1
    while True:
        data = cf_get(f"/accounts/{ACCOUNT_ID}/storage/kv/namespaces?per_page=100&page={page}", token)
        if not data.get("success"):
            raise RuntimeError(f"list_kv_namespaces failed: {data}")
        out.extend(data["result"])
        if len(data["result"]) < 100:
            break
        page += 1
    return out


def list_kv_keys(ns_id, token):
    out = []
    cursor = None
    while True:
        path = f"/accounts/{ACCOUNT_ID}/storage/kv/namespaces/{ns_id}/keys?limit=1000"
        if cursor:
            path += f"&cursor={cursor}"
        data = cf_get(path, token)
        if not data.get("success"):
            raise RuntimeError(f"list_kv_keys failed ns={ns_id}: {data}")
        out.extend(data["result"])
        cursor = (data.get("result_info") or {}).get("cursor")
        if not cursor:
            break
    return out


def get_kv_value(ns_id, key, token):
    from urllib.parse import quote
    body, _ = cf_get(
        f"/accounts/{ACCOUNT_ID}/storage/kv/namespaces/{ns_id}/values/{quote(key, safe='')}",
        token, raw=True,
    )
    return body


def safe_name(s):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", s)[:120]


def main():
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    WORKERS_DIR.mkdir(parents=True, exist_ok=True)
    KV_DIR.mkdir(parents=True, exist_ok=True)
    token = load_token()

    log("=== Workers ===")
    workers = list_workers(token)
    log(f"Found {len(workers)} workers")
    for w in workers:
        name = w["id"]
        wdir = WORKERS_DIR / safe_name(name)
        wdir.mkdir(parents=True, exist_ok=True)
        try:
            body, ctype = fetch_worker(name, token)
            files = parse_multipart(body, ctype)
            # Wipe stale files so deletions show in git diff.
            for old in wdir.iterdir():
                if old.is_file():
                    old.unlink()
            for fname, content in files.items():
                (wdir / safe_name(fname)).write_bytes(content)
            (wdir / "_meta.json").write_text(json.dumps(w, indent=2, sort_keys=True), encoding="utf-8")
            log(f"  {name}: {len(files)} file(s), {sum(len(c) for c in files.values())} bytes")
        except Exception as e:
            log(f"  {name}: ERROR {e}")
            raise

    log("=== KV namespaces ===")
    namespaces = list_kv_namespaces(token)
    log(f"Found {len(namespaces)} namespaces")
    for ns in namespaces:
        ns_id = ns["id"]
        ns_name = ns["title"]
        ndir = KV_DIR / safe_name(ns_name)
        ndir.mkdir(parents=True, exist_ok=True)
        try:
            keys = list_kv_keys(ns_id, token)
            # Wipe stale so deletions show up.
            for old in ndir.iterdir():
                if old.is_file():
                    old.unlink()
            (ndir / "_meta.json").write_text(
                json.dumps({"id": ns_id, "title": ns_name, "key_count": len(keys)}, indent=2),
                encoding="utf-8",
            )
            for k in keys:
                kname = k["name"]
                val = get_kv_value(ns_id, kname, token)
                (ndir / safe_name(kname)).write_bytes(val)
            log(f"  {ns_name}: {len(keys)} key(s)")
        except Exception as e:
            log(f"  {ns_name}: ERROR {e}")
            raise

    log("DONE")


if __name__ == "__main__":
    try:
        main()
    except (HTTPError, URLError) as e:
        log(f"FATAL HTTP {e}")
        sys.exit(2)
    except Exception as e:
        log(f"FATAL {e}")
        sys.exit(1)
