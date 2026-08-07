#!/usr/bin/env python3
"""Resumable downloader for 1KGP long-read trios (assemblies and aligned reads).

Design contract (see DOWNLOADER_SPEC_v01.md and ASSEMBLY_ONLY_PLAN_v01.md):
  * One sequential stream per file (exFAT-safe on Green24; no ranged splits).
    With --parallel N, up to N files of the same family transfer at once, but
    each file still gets exactly one sequential stream.
  * Byte-level resume via HTTP Range (curl -C - semantics).
  * Verify size, and md5 when the manifest provides one. Never trust the log line.
  * Per-family JSON state on Green24 survives machine replacement.
  * Partials are never deleted; anomalies are quarantined with a note.
  * Rate limit token bucket (RATE_KBPS env, default 8000 KiB/s per family,
    split evenly across the parallel streams of that family).
  * Best-effort fleet capacity monitor state publication.

Normally launched by kgp-assembly-dl-v01@.service or kgp-aligned-dl-v01@.service:
  assembly_downloader_v01.py --family 1_HG00514
  assembly_downloader_v01.py --family r8_NA12878 --manifest .../ALIGNED_READS_MANIFEST_v01.tsv
"""

import argparse
import concurrent.futures
import fcntl
import gzip
import hashlib
import json
import os
import subprocess
import sys
import threading
import time
import urllib.request

HOME_ROOT = os.environ.get("KGTRIO_ROOT", "/home/maxre/1kgp_longread_trios")
GREEN_ROOT = os.environ.get("KGTRIO_GREEN", "/mnt/green24/1kgp_longread_trios")
MANIFEST = os.environ.get("KGTRIO_MANIFEST", os.path.join(HOME_ROOT, "ASSEMBLY_MANIFEST_v01.tsv"))
PHASE = os.environ.get("KGTRIO_PHASE", "assembly")
FLEET_TOOL = os.path.expanduser("~/fleet_capacity_monitor/set_work_state.py")
CHUNK = 1024 * 1024
MAX_ATTEMPTS = 30
RETRY_SLEEP = 30.0


def utcnow():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


class FamilyLog:
    def __init__(self, family):
        self.path = os.path.join(GREEN_ROOT, "logs", family, "download.log")
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

    def write(self, msg):
        line = "[%s] %s" % (utcnow(), msg)
        print(line, flush=True)
        try:
            with open(self.path, "a", encoding="utf-8") as handle:
                handle.write(line + "\n")
        except OSError:
            pass


def load_manifest_rows(family):
    rows = []
    with open(MANIFEST, encoding="utf-8") as handle:
        header = handle.readline().rstrip("\n").split("\t")
        for line in handle:
            line = line.rstrip("\n")
            if not line:
                continue
            row = dict(zip(header, line.split("\t")))
            if row["family"] == family and row["priority"] == "essential":
                rows.append(row)
    return rows


def state_path(family):
    return os.path.join(GREEN_ROOT, "state", family + ".json")


def load_state(family, rows):
    path = state_path(family)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    files = []
    for row in rows:
        files.append({
            "member": row["member"],
            "role": row["role"],
            "resource": row["resource"],
            "assembler": row["assembler"],
            "url": row["url"],
            "local_path": os.path.join(GREEN_ROOT, row["relpath"]),
            "expected_bytes": int(row["expected_bytes"] or 0),
            "expected_md5": row["md5"] or "",
            "downloaded_bytes": 0,
            "status": "pending",
            "verified": False,
            "note": "",
        })
    return {"family": family, "status": "pending", "files": files, "updated_utc": utcnow()}


def save_state(state):
    path = state_path(state["family"])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    state["updated_utc"] = utcnow()
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, path)


def md5_of(path):
    digest = hashlib.md5()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(8 * CHUNK)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def fa_structure_ok(path):
    """FASTA starts with '>' and ends with a newline.

    For gzip-compressed FASTA, decompress the full stream so integrity
    (CRC) is checked too, not just the container bytes.
    """
    try:
        if path.lower().endswith(".gz"):
            with gzip.open(path, "rb") as handle:
                first = handle.read(1)
                if first != b">":
                    return False
                last = b""
                while True:
                    block = handle.read(8 * CHUNK)
                    if not block:
                        break
                    last = block[-1:]
                return last in (b"\n", b"\r")
        with open(path, "rb") as handle:
            first = handle.read(1)
            handle.seek(-1, 2)
            last = handle.read(1)
        return first == b">" and last in (b"\n", b"\r")
    except (OSError, EOFError, ValueError):
        return False


def verify(entry, log):
    path = entry["local_path"]
    if not os.path.exists(path):
        return False
    size = os.path.getsize(path)
    if entry["expected_bytes"] and size != entry["expected_bytes"]:
        log.write("VERIFY FAIL size %s %s: got %d expected %d"
                  % (entry["member"], os.path.basename(path), size, entry["expected_bytes"]))
        return False
    if entry["expected_md5"]:
        actual = md5_of(path)
        if actual != entry["expected_md5"]:
            log.write("VERIFY FAIL md5 %s %s: got %s expected %s"
                      % (entry["member"], os.path.basename(path), actual, entry["expected_md5"]))
            return False
    if not entry["expected_md5"] and path.lower().endswith((".fasta", ".fa", ".fa.gz", ".fasta.gz", ".fas")):
        if not fa_structure_ok(path):
            log.write("VERIFY FAIL structure %s %s: not a complete FASTA (gzip+FASTA check failed)"
                      % (entry["member"], os.path.basename(path)))
            return False
    entry["verified"] = True
    entry["status"] = "verified"
    entry["downloaded_bytes"] = size
    log.write("VERIFIED %s %s (%d bytes)" % (entry["member"], os.path.basename(path), size))
    return True


def quarantine(entry, reason, log):
    src = entry["local_path"]
    qdir = os.path.join(GREEN_ROOT, "state", "quarantine")
    os.makedirs(qdir, exist_ok=True)
    stamp = int(time.time())
    dst = os.path.join(qdir, "%s_%s.%d" % (entry["member"], os.path.basename(src), stamp))
    try:
        os.replace(src, dst)
        entry["note"] = "quarantined to %s: %s" % (dst, reason)
        log.write("QUARANTINE %s -> %s (%s)" % (src, dst, reason))
    except OSError as exc:
        entry["note"] = "quarantine failed (%s); leaving file in place" % exc
        log.write("QUARANTINE FAILED %s: %s" % (src, exc))


def publish_fleet(family, state_name, progress_value):
    try:
        subprocess.run(
            [sys.executable, FLEET_TOOL, state_name,
             "--task", "1KGP trio %s downloads, family %s" % (PHASE, family),
             "--owner", "Q38/Codex",
             "--progress-path", state_path(family),
             "--progress-value", progress_value,
             "--process-regex", "assembly_downloader_v01"],
            timeout=30, check=False, capture_output=True)
    except Exception:
        pass


def download(entry, rate_bps, log):
    url = entry["url"]
    path = entry["local_path"]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    expected = entry["expected_bytes"]
    for attempt in range(1, MAX_ATTEMPTS + 1):
        have = os.path.getsize(path) if os.path.exists(path) else 0
        if expected and have > expected:
            quarantine(entry, "partial %d exceeds expected %d" % (have, expected), log)
            have = 0
        if expected and have == expected and entry.get("status") != "verify_failed":
            return True
        if expected and have == expected and entry.get("status") == "verify_failed":
            quarantine(entry, "size matched but md5 previously failed; re-downloading", log)
            have = 0
        req = urllib.request.Request(url)
        if have > 0:
            req.add_header("Range", "bytes=%d-" % have)
        try:
            resp = urllib.request.urlopen(req, timeout=300)
        except Exception as exc:
            log.write("attempt %d: open failed: %s (retry in %ds)" % (attempt, exc, int(RETRY_SLEEP)))
            time.sleep(RETRY_SLEEP)
            continue
        status = getattr(resp, "status", 200)
        if have > 0 and status == 200:
            log.write("server ignored Range; preserving partial as .restart and starting fresh")
            os.replace(path, path + ".restart_%d" % int(time.time()))
            have = 0
        if have > 0 and status == 206:
            mode = "ab"
        else:
            mode = "wb"
            have = 0
        content_length = resp.headers.get("Content-Length")
        if content_length:
            total = have + int(content_length)
            if expected and total != expected:
                log.write("WARNING: remote total %d != manifest expected %d" % (total, expected))
        entry["status"] = "downloading"
        start = time.monotonic()
        base = have
        last_state_write = start
        try:
            with open(path, mode) as out:
                while True:
                    chunk = resp.read(CHUNK)
                    if not chunk:
                        break
                    out.write(chunk)
                    have += len(chunk)
                    if rate_bps > 0:
                        wait = start + (have - base) / float(rate_bps) - time.monotonic()
                        if wait > 0:
                            time.sleep(wait)
                    if time.monotonic() - last_state_write > 10:
                        entry["downloaded_bytes"] = have
                        last_state_write = time.monotonic()
        except Exception as exc:
            log.write("attempt %d: transfer interrupted at %d bytes: %s" % (attempt, have, exc))
            entry["downloaded_bytes"] = have
            time.sleep(RETRY_SLEEP)
            continue
        entry["downloaded_bytes"] = have
        log.write("download finished %s %s (%d bytes)" % (entry["member"], os.path.basename(path), have))
        return True
    return False


def regenerate_progress():
    state_dir = os.path.join(GREEN_ROOT, "state")
    lines = ["# 1KGP trio downloads - PROGRESS (all phases)", "",
             "Updated: " + utcnow(), "",
             "| family | resource | status | verified files | bytes on disk |",
             "|---|---|---|---|---|"]
    if os.path.isdir(state_dir):
        for name in sorted(os.listdir(state_dir)):
            if not name.endswith(".json"):
                continue
            try:
                with open(os.path.join(state_dir, name), encoding="utf-8") as handle:
                    st = json.load(handle)
            except Exception:
                continue
            verified = sum(1 for f in st["files"] if f.get("verified"))
            total_bytes = sum(f.get("downloaded_bytes", 0) for f in st["files"])
            resource = st["files"][0]["resource"] if st["files"] else "?"
            lines.append("| %s | %s | %s | %d/%d | %s |"
                         % (st["family"], resource, st["status"], verified, len(st["files"]), format(total_bytes, ",")))
    with open(os.path.join(state_dir, "PROGRESS.md"), "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(description="1KGP trio downloader (assemblies and aligned reads)")
    parser.add_argument("--family", required=True)
    parser.add_argument("--manifest", default=None,
                        help="manifest TSV; default is KGTRIO_MANIFEST env or the assembly manifest")
    parser.add_argument("--parallel", type=int,
                        default=int(os.environ.get("KGTRIO_PARALLEL", "1")),
                        help="files of this family to transfer at once (one stream each)")
    args = parser.parse_args()
    global MANIFEST
    if args.manifest:
        MANIFEST = args.manifest
    family = args.family
    rows = load_manifest_rows(family)
    if not rows:
        print("no essential manifest rows for family %s" % family)
        return 2
    log = FamilyLog(family)
    os.makedirs(os.path.join(GREEN_ROOT, "state"), exist_ok=True)
    lock = open(os.path.join(GREEN_ROOT, "state", family + ".lock"), "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        print("another worker holds family %s; exiting" % family)
        return 0
    state = load_state(family, rows)
    if state["status"] == "complete":
        log.write("family already complete; nothing to do")
        return 0
    state["status"] = "downloading"
    save_state(state)
    rate_bps = int(os.environ.get("RATE_KBPS", "8000")) * 1024
    total_expected = sum(f["expected_bytes"] for f in state["files"])
    parallel = max(1, args.parallel)
    stream_rate = max(rate_bps // parallel, 256 * 1024)
    log.write("starting family %s: %d files, %s bytes expected, rate cap %d KiB/s, %d stream(s)"
              % (family, len(state["files"]), format(total_expected, ","), rate_bps // 1024, parallel))
    publish_fleet(family, "working", "0/%d" % total_expected)
    state_lock = threading.Lock()

    def work(entry):
        with state_lock:
            if entry.get("verified") or verify(entry, log):
                save_state(state)
                return True
        ok = download(entry, stream_rate, log)
        with state_lock:
            if ok and verify(entry, log):
                save_state(state)
                done = sum(f.get("downloaded_bytes", 0) for f in state["files"])
                publish_fleet(family, "working", "%d/%d" % (done, total_expected))
                regenerate_progress()
                return True
            if not ok:
                log.write("GIVING UP this run on %s %s after %d attempts"
                          % (entry["member"], os.path.basename(entry["local_path"]), MAX_ATTEMPTS))
                entry["status"] = "failed"
            else:
                entry["status"] = "verify_failed"
            save_state(state)
            return False

    if parallel == 1:
        results = [work(entry) for entry in state["files"]]
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=parallel) as pool:
            results = list(pool.map(work, state["files"]))
    failed = not all(results)
    if not failed and all(f.get("verified") for f in state["files"]):
        state["status"] = "complete"
        log.write("FAMILY COMPLETE %s" % family)
        publish_fleet(family, "complete", "%d/%d" % (total_expected, total_expected))
    else:
        state["status"] = "failed" if failed else "downloading"
        if failed:
            publish_fleet(family, "waiting", "family needs attention")
    save_state(state)
    regenerate_progress()
    return 0 if state["status"] == "complete" else 1


if __name__ == "__main__":
    sys.exit(main())
