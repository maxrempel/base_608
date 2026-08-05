"""
worker.py - resumable Sunday2023 batch worker.
- Reads config.json + queue.json each iteration (live tunable).
- Processes ONE pending video at a time: download (yt-dlp 720p + firefox cookies)
  -> upload (vk_upload via vcopier) -> mark done -> wait delay -> next.
- Respects max_per_day (UTC).
- On yt-dlp bot-block, long backoff. On VK reset, short retry.
- Deletes mp4 after successful upload if delete_after_upload.
- Lock file prevents two instances.
- Re-run picks up from where it stopped.
"""
import json, subprocess, sys, time, random, os, re, glob
from pathlib import Path
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding='utf-8')

HERE = Path(__file__).parent
LOCK = HERE / "worker.lock"
QUEUE = HERE / "queue.json"
LOG = HERE / "worker.log"
STATUS = HERE / "status.txt"
HISTORY = HERE / "history.txt"  # one line per processed video (with date)

def load_cfg(): return json.loads((HERE / "config.json").read_text(encoding="utf-8"))
def load_queue(): return json.loads(QUEUE.read_text(encoding="utf-8"))
def save_queue(q): QUEUE.write_text(json.dumps(q, ensure_ascii=False, indent=2), encoding="utf-8")
def logln(msg):
    line = f"[{datetime.now().isoformat(timespec='seconds')}] {msg}"
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as f: f.write(line + "\n")

def today_count():
    if not HISTORY.exists(): return 0
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    n = 0
    for line in HISTORY.read_text(encoding="utf-8").splitlines():
        if line.startswith(today): n += 1
    return n

def record_history(yt_id):
    with open(HISTORY, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}Z {yt_id}\n")

def write_status(queue, msg=""):
    counts = {}
    for e in queue: counts[e["status"]] = counts.get(e["status"],0)+1
    STATUS.write_text(
        f"updated: {datetime.now().isoformat(timespec='seconds')}\n"
        f"counts: {counts}\n"
        f"today_processed: {today_count()}\n"
        f"note: {msg}\n", encoding="utf-8")

def acquire_lock():
    if LOCK.exists():
        try: pid = int(LOCK.read_text().strip())
        except: pid = -1
        # Best-effort check: on Windows, just trust the lock; user must delete to override.
        logln(f"lock exists ({LOCK}, pid={pid}). exit. delete file to force unlock.")
        sys.exit(0)
    LOCK.write_text(str(os.getpid()))

def release_lock():
    try: LOCK.unlink()
    except: pass

def jitter(seconds, pct):
    delta = seconds * pct / 100
    return max(1, int(seconds + random.uniform(-delta, delta)))

def process_one(cfg, item):
    """Run vcopier on one item. Returns (status, vk_url, error_msg)."""
    url = f"https://www.youtube.com/watch?v={item['yt_id']}"
    cmd = ["python", cfg["vcopier_path"], url]
    logln(f"start: {item['yt_id']} | {item['title'][:80]}")
    p = subprocess.run(cmd, capture_output=True)
    out = p.stdout.decode("utf-8", errors="replace")
    err = p.stderr.decode("utf-8", errors="replace")
    logln(out.strip()[-1500:])
    if err.strip(): logln("STDERR: " + err.strip()[-800:])
    if p.returncode != 0:
        msg = (err + "\n" + out)[-500:]
        if "Sign in to confirm" in msg or "not a bot" in msg:
            return "failed_botblock", "", msg
        return "failed", "", msg
    m = re.search(r"VK URL:\s*(\S+)", out)
    vk = m.group(1) if m else ""
    return "done", vk, ""

def cleanup_cache(cfg, yt_id):
    if not cfg.get("delete_after_upload"): return
    cache = Path(cfg["cache_dir"])
    if not cache.exists(): return
    for f in cache.glob(f"yt_*_{yt_id}_*.mp4"):
        try: f.unlink(); logln(f"deleted cache: {f.name}")
        except Exception as e: logln(f"cache delete failed: {e}")

def main():
    acquire_lock()
    try:
        while True:
            cfg = load_cfg()
            q = load_queue()
            # Find next pending or retryable failed
            next_item = None
            for e in q:
                if e["status"] == "pending":
                    next_item = e; break
                if e["status"] == "failed" and e["attempts"] < cfg["max_retries"]:
                    next_item = e; break
            if not next_item:
                write_status(q, "no more work")
                logln("nothing pending. exiting.")
                break
            # Daily cap
            if today_count() >= cfg["max_per_day"]:
                write_status(q, f"daily cap reached ({cfg['max_per_day']}); sleeping 1h")
                logln(f"daily cap reached ({cfg['max_per_day']}); sleeping 1h")
                time.sleep(3600); continue
            # Process
            next_item["attempts"] += 1
            write_status(q, f"processing {next_item['yt_id']}")
            status, vk_url, err = process_one(cfg, next_item)
            next_item["status"] = status if status != "failed_botblock" else "failed"
            next_item["vk_url"] = vk_url
            next_item["last_error"] = err
            save_queue(q)
            if status == "done":
                record_history(next_item["yt_id"])
                cleanup_cache(cfg, next_item["yt_id"])
                wait = jitter(cfg["delay_seconds_between_videos"], cfg["delay_jitter_pct"])
                logln(f"done. vk={vk_url}. sleeping {wait}s before next.")
                write_status(q, f"sleeping {wait}s after success")
                time.sleep(wait)
            elif status == "failed_botblock":
                wait = cfg["ytdlp_botblock_backoff_seconds"]
                logln(f"YT bot-block. sleeping {wait}s.")
                write_status(q, f"bot-block backoff {wait}s")
                time.sleep(wait)
            else:
                wait = cfg["retry_backoff_seconds"]
                logln(f"failure. attempt={next_item['attempts']}. sleeping {wait}s.")
                write_status(q, f"failure backoff {wait}s")
                time.sleep(wait)
    finally:
        release_lock()

if __name__ == "__main__": main()
