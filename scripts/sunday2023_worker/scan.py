"""
scan.py - one-time scan of Tamza YT channel.
Strategy:
  1. Flat scan whole channel (titles + ids; fast).
  2. Probe each ID for upload_date + duration (slow; cached in metadata_cache.json).
  3. Filter: upload_date in 2023 + day of week = Sunday + duration > 60 min.
  4. Dedup against VK group by date markers in titles.
  5. Re-running merges with existing queue (preserves status/vk_url).
"""
import json, subprocess, sys, os, urllib3
from datetime import datetime
from pathlib import Path
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding='utf-8')

HERE = Path(__file__).parent
CFG = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
QUEUE = HERE / "queue.json"
META_CACHE = HERE / "metadata_cache.json"
FLAT_FILE = HERE / "_flat_scan.txt"

RU_MONTHS = {1:"января",2:"февраля",3:"марта",4:"апреля",5:"мая",6:"июня",
             7:"июля",8:"августа",9:"сентября",10:"октября",11:"ноября",12:"декабря"}

def date_markers(yyyymmdd):
    if len(yyyymmdd) != 8: return []
    y,m,d = int(yyyymmdd[0:4]), int(yyyymmdd[4:6]), int(yyyymmdd[6:8])
    out = [
        f"{d} {RU_MONTHS[m]} {y}",
        f"{d}.{m:02d}.{y}",
        f"{d:02d}.{m:02d}.{y}",
        f"{d}.{m:02d}.{str(y)[2:]}",
        f"{d:02d}.{m:02d}.{str(y)[2:]}",
        f"{d}/{m}/{y}",
    ]
    return [s.lower() for s in out]

def fetch_vk_titles():
    tok = open(CFG["vk_token_file"]).read().strip()
    all_t = []
    for off in (0,200,400,600,800):
        r = requests.get("https://api.vk.com/method/video.get",
            params={"owner_id":CFG["vk_group_id"],"count":200,"offset":off,
                    "access_token":tok,"v":"5.199"}, verify=False).json()
        its = r.get("response",{}).get("items",[])
        all_t += [i.get("title","") for i in its]
        if len(its) < 200: break
    return [t.lower() for t in all_t]

def flat_scan_channel():
    if FLAT_FILE.exists(): FLAT_FILE.unlink()
    cmd = ["yt-dlp","--cookies-from-browser","firefox","--flat-playlist",
           "--print-to-file","%(id)s|%(title)s", str(FLAT_FILE),
           CFG["channel_url"]]
    print("flat-scanning YT channel...", flush=True)
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        sys.stderr.buffer.write(b"yt-dlp flat scan failed:\n" + r.stderr[-2000:]); sys.exit(3)
    rows = []
    for line in FLAT_FILE.read_text(encoding="utf-8", errors="replace").splitlines():
        p = line.split("|",1)
        if len(p) == 2: rows.append({"yt_id":p[0], "title":p[1]})
    return rows

def load_meta_cache():
    if META_CACHE.exists():
        return json.loads(META_CACHE.read_text(encoding="utf-8"))
    return {}

def save_meta_cache(cache):
    META_CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")

def probe_one(yt_id):
    out_file = HERE / "_probe_one.txt"
    if out_file.exists(): out_file.unlink()
    cmd = ["yt-dlp","--cookies-from-browser","firefox","--no-playlist",
           "--no-download","--print-to-file","%(upload_date)s|%(duration)s",
           str(out_file), f"https://www.youtube.com/watch?v={yt_id}"]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0 or not out_file.exists():
        return None, None, r.stderr.decode("utf-8", errors="replace")[-300:]
    content = out_file.read_text(encoding="utf-8", errors="replace").strip().splitlines()
    if not content: return None, None, "empty"
    parts = content[-1].split("|",1)
    if len(parts) != 2: return None, None, f"bad parse: {content[-1]}"
    date, dur = parts
    try: dur = int(float(dur)) if dur and dur != "NA" else 0
    except: dur = 0
    return date, dur, ""

def main():
    print("=== STAGE 1: VK titles ===", flush=True)
    vk_titles = fetch_vk_titles()
    print(f"VK titles: {len(vk_titles)}")

    print("=== STAGE 2: flat scan channel ===", flush=True)
    rows = flat_scan_channel()
    print(f"channel rows: {len(rows)}")

    print("=== STAGE 3: probe upload_date + duration (cached) ===", flush=True)
    meta = load_meta_cache()
    to_probe = [r for r in rows if r["yt_id"] not in meta]
    print(f"need to probe: {len(to_probe)} (cached: {len(meta)})")
    save_every = 25
    for i, r in enumerate(to_probe, 1):
        date, dur, err = probe_one(r["yt_id"])
        meta[r["yt_id"]] = {"date": date or "", "duration": dur or 0,
                            "title": r["title"], "probe_error": err}
        if i % save_every == 0:
            save_meta_cache(meta)
            print(f"  probed {i}/{len(to_probe)} (saved cache)", flush=True)
    save_meta_cache(meta)

    print("=== STAGE 4: filter Sunday 2023 concerts ===", flush=True)
    sunday_2023 = []
    for r in rows:
        m = meta.get(r["yt_id"], {})
        d = m.get("date","")
        dur = m.get("duration", 0)
        if not d.startswith("2023"): continue
        try:
            dt = datetime.strptime(d, "%Y%m%d")
        except: continue
        if dt.weekday() != 6: continue  # Mon=0 ... Sun=6
        if dur < 60*60: continue  # > 60 min
        sunday_2023.append({"yt_id": r["yt_id"], "date": d, "title": r["title"],
                            "duration_min": dur//60})
    print(f"Sunday 2023 concerts (date in 2023, weekday=Sun, dur>60min): {len(sunday_2023)}")

    print("=== STAGE 5: dedup vs VK + write queue ===", flush=True)
    existing = {}
    if QUEUE.exists():
        for e in json.loads(QUEUE.read_text(encoding="utf-8")):
            existing[e["yt_id"]] = e
    queue = []
    for r in sunday_2023:
        prev = existing.get(r["yt_id"], {})
        already_vk = False
        for m in date_markers(r["date"]):
            if any(m in t for t in vk_titles):
                already_vk = True; break
        status = prev.get("status")
        if status in ("done","skipped_already_on_vk"): pass
        elif already_vk: status = "skipped_already_on_vk"
        else: status = status or "pending"
        queue.append({"yt_id": r["yt_id"], "date": r["date"], "title": r["title"],
                      "duration_min": r["duration_min"], "status": status,
                      "vk_url": prev.get("vk_url",""), "attempts": prev.get("attempts",0),
                      "last_error": prev.get("last_error","")})
    order = {"pending":0,"failed":1,"skipped_already_on_vk":2,"done":3}
    queue.sort(key=lambda e:(order.get(e["status"],9), e["date"]))
    QUEUE.write_text(json.dumps(queue, ensure_ascii=False, indent=2), encoding="utf-8")

    counts = {}
    for e in queue: counts[e["status"]] = counts.get(e["status"],0)+1
    print(f"queue counts: {counts}")
    print(f"queue written: {QUEUE}")

if __name__ == "__main__": main()
