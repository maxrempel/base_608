"""
mdindex_sync.py v03 | 2026-04-10 14:30
Syncs _tomemex.md files to Memex via the Sol pipeline.
Scans registered folders for any file matching *_tomemex.md.
Copies to 00_clawy_kb/memories/local_*. Runs every 10 minutes.
Also builds mdindex.md as a flat reference.
"""

import hashlib
import shutil
import time
import logging
from datetime import datetime
from pathlib import Path

VERSION = "v03 | 2026-04-10"

FOLDER_REGISTRY = Path(r"C:\cloud_base\scripts\folder_registry.txt")
MDINDEX_FILE = Path(r"C:\cloud_base\mdindex.md")
MEMEX_DIR = Path(r"C:\Users\maxre\Nextcloud\00_clawy_kb\memories")
LOG_FILE = Path(r"C:\cloud_base\scripts\mdindex_sync.log")
HASH_CACHE = Path(r"C:\cloud_base\scripts\.mdindex_hashes.txt")
SCAN_INTERVAL = 600  # 10 minutes

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def load_registry():
    """Load folder roots and max depths from registry file."""
    roots = []
    for line in FOLDER_REGISTRY.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "|" in line:
            path_str, depth_str = line.rsplit("|", 1)
            roots.append((Path(path_str.strip()), int(depth_str.strip())))
        else:
            roots.append((Path(line), 5))
    return roots


def scan_for_memex_files(roots):
    """Find all *_tomemex.md files in registered folders."""
    found = []
    for root, max_depth in roots:
        if not root.exists():
            logging.warning("Registry root not found: %s", root)
            continue
        for md_file in root.rglob("*_tomemex.md"):
            try:
                rel = md_file.relative_to(root)
            except ValueError:
                continue
            if len(rel.parts) > max_depth:
                continue
            # Skip the memex staging folder to avoid double-counting
            if "00_clawy_kb" in md_file.parts:
                continue
            found.append(md_file)
    return found


def file_hash(path):
    try:
        return hashlib.md5(path.read_bytes()).hexdigest()
    except Exception:
        return None


def load_hash_cache():
    cache = {}
    if HASH_CACHE.exists():
        for line in HASH_CACHE.read_text(encoding="utf-8").splitlines():
            if "|" in line:
                h, p = line.split("|", 1)
                cache[p] = h
    return cache


def save_hash_cache(cache):
    lines = [f"{h}|{p}" for p, h in sorted(cache.items())]
    HASH_CACHE.write_text("\n".join(lines), encoding="utf-8")


def make_local_key(filepath):
    """Short unique filename for Memex staging."""
    return f"local_{filepath.parent.name}__{filepath.name}"


def first_meaningful_line(filepath):
    try:
        text = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""
    for line in text.splitlines():
        line = line.strip().lstrip("#").strip()
        if line and not line.startswith("---") and len(line) > 5:
            return line[:120]
    return ""


def classify_project(filepath):
    """Group file by project based on path."""
    path_str = str(filepath)
    if "moma" in path_str.lower():
        return "moma (video production)"
    if "ai_images" in path_str:
        return "kazarian episode (image/video/sound)"
    if "claude_md_synced" in path_str:
        return "claude code setup"
    if "z_kazarian_episode" in path_str:
        return "kazarian episode (scripts)"
    return "other"


def clean_name(filename):
    """Strip _tomemex suffix for display."""
    return filename.replace("_tomemex.md", "").replace("_", " ")


def build_mdindex(files):
    lines = [
        "# Instruction Files Index",
        f"# Auto-generated {datetime.now().strftime('%Y-%m-%d %H:%M')} by mdindex_sync",
        f"# {len(files)} files. Read any file for full instructions.",
        "#",
        "# Claude: read this index at session start to know what instructions exist.",
        "# To find a file by topic, search Memex. To read a file, use its path below.",
        "",
    ]

    grouped = {}
    for f in sorted(files):
        project = classify_project(f)
        grouped.setdefault(project, []).append(f)

    for project in sorted(grouped):
        lines.append(f"## {project}")
        for f in grouped[project]:
            desc = first_meaningful_line(f)
            name = clean_name(f.name)
            lines.append(f"  {name}: {desc}")
            lines.append(f"    path: {f}")
        lines.append("")

    return "\n".join(lines)


def sync_to_memex_staging(files, old_cache, new_cache):
    synced = 0
    current_keys = set()

    for f in files:
        key = make_local_key(f)
        current_keys.add(key)
        h = new_cache.get(str(f))
        old_h = old_cache.get(str(f))

        if h and h != old_h:
            dest = MEMEX_DIR / key
            try:
                shutil.copy2(str(f), str(dest))
                synced += 1
            except Exception as e:
                logging.error("Failed to copy %s -> %s: %s", f, dest, e)

    # Clean up local_ files no longer matching
    for existing in MEMEX_DIR.glob("local_*.md"):
        if existing.name not in current_keys:
            existing.unlink()
            logging.info("Removed stale: %s", existing.name)

    return synced


def run_once():
    roots = load_registry()
    files = scan_for_memex_files(roots)
    old_cache = load_hash_cache()

    new_cache = {}
    for f in files:
        h = file_hash(f)
        if h:
            new_cache[str(f)] = h

    index_content = build_mdindex(files)
    MDINDEX_FILE.write_text(index_content, encoding="utf-8")

    synced = sync_to_memex_staging(files, old_cache, new_cache)

    save_hash_cache(new_cache)
    logging.info("Sync: %d files found, %d synced", len(files), synced)


def main():
    logging.info("mdindex_sync started (%s)", VERSION)
    run_once()

    while True:
        time.sleep(SCAN_INTERVAL)
        try:
            run_once()
        except Exception as e:
            logging.error("Sync failed: %s", e)


if __name__ == "__main__":
    main()
