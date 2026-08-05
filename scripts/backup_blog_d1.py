"""
Backup the maxrempel.com site content D1 database (maxrempel-blog) to JSON.

Created 2026-06-02 by Claude Opus 4.8 for Max, to close the D1 backup GAP noted
in cf_backup_method_tomemex.md: maxrempel.com's source of truth (pages, nav,
books, book_chapters, blog_posts) lives in D1 and was NOT backed up by either
existing stream. This is canonical, NOT re-ingestable -- losing it loses the site.

Dumps every table via the Cloudflare REST D1 query API to one timestamped JSON
under backups/cf_d1/maxrempel-blog/, plus a stable latest.json. The wrapper bat
then commits to github.com/maxrempel/cloud_base (keep every version forever -- tiny text).

No silent fallbacks: any non-200 / non-success raises and exits non-zero so the
wrapper skips the git commit and the run is visibly broken.
"""
import json
import sys
import time
from pathlib import Path
from urllib import request as urlreq
from urllib.error import HTTPError, URLError

ACCOUNT_ID = "e4dc2224d6baa721873dca77dc6f057d"
DB_ID = "c25ab8ba-bab4-460a-b9c1-34790cdf7288"  # maxrempel-blog
DB_NAME = "maxrempel-blog"
TOKEN_FILE = Path(r"C:\Users\maxre\Nextcloud\zSyncMain\ssh\cloudflare_workers_kv_token_20260303.txt")
OUT_DIR = Path(r"C:\cloud_base\backups\cf_d1") / DB_NAME
LOG_FILE = Path(r"C:\cloud_base\backups\backup_cf.log")

CF = "https://api.cloudflare.com/client/v4"


def log(msg):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] d1:{DB_NAME} {msg}"
    print(line)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def load_token():
    for line in TOKEN_FILE.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s and not s.startswith("#"):
            return s
    raise RuntimeError(f"No token in {TOKEN_FILE}")


def d1_query(sql, token):
    body = json.dumps({"sql": sql}).encode()
    req = urlreq.Request(
        f"{CF}/accounts/{ACCOUNT_ID}/d1/database/{DB_ID}/query",
        data=body, method="POST",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    with urlreq.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if not data.get("success"):
        raise RuntimeError(f"D1 query failed: {sql!r} -> {data.get('errors')}")
    # result is a list of statement results; we run one statement
    return data["result"][0]["results"]


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    token = load_token()

    tables = [r["name"] for r in d1_query(
        "SELECT name FROM sqlite_master WHERE type='table' "
        "AND name NOT LIKE 'sqlite_%' AND name NOT LIKE '_cf_%' ORDER BY name", token)]
    log(f"tables: {tables}")

    snap = {
        "db_name": DB_NAME, "db_id": DB_ID,
        "dumped_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "tables": {},
    }
    for t in tables:
        rows = d1_query(f"SELECT * FROM {t}", token)
        snap["tables"][t] = rows

    ts = time.strftime("%Y%m%d_%H%M%S")
    payload = json.dumps(snap, indent=2, ensure_ascii=False)
    (OUT_DIR / f"d1_{ts}.json").write_text(payload, encoding="utf-8")
    (OUT_DIR / "latest.json").write_text(payload, encoding="utf-8")

    counts = {t: len(v) for t, v in snap["tables"].items()}
    log(f"dump ok: d1_{ts}.json ({len(payload)} bytes) rows={counts}")
    print("DONE")


if __name__ == "__main__":
    try:
        main()
    except (HTTPError, URLError) as e:
        log(f"FATAL HTTP {e}")
        sys.exit(2)
    except Exception as e:
        log(f"FATAL {e}")
        sys.exit(1)
