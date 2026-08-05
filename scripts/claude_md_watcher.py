"""
claude_md_watcher.py v01 | 2026-04-10 14:00
Watches global_CLAUDE.md for changes, keeps last 25 versions in archive.
Runs as background process, auto-started via Windows Task Scheduler.
Checks every 30 seconds. Copies on content change. Deletes oldest when >25.
"""

import hashlib
import shutil
import time
import logging
import sys
from datetime import datetime
from pathlib import Path

VERSION = "v01 | 2026-04-10"

WATCH_FILE = Path(r"C:\Users\maxre\Nextcloud\claude_md_synced\global_CLAUDE.md")
ARCHIVE_DIR = Path(r"C:\cloud_base\archive")
LOG_FILE = Path(r"C:\cloud_base\scripts\watcher.log")
MAX_VERSIONS = 25
CHECK_INTERVAL = 30  # seconds

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def file_hash(path):
    """Return MD5 hex digest of file contents."""
    return hashlib.md5(path.read_bytes()).hexdigest()


def archive_versions():
    """Return sorted list of archived versions, oldest first."""
    return sorted(ARCHIVE_DIR.glob("global_CLAUDE_*.md"))


def prune_old_versions():
    """Delete oldest versions if more than MAX_VERSIONS."""
    versions = archive_versions()
    while len(versions) > MAX_VERSIONS:
        oldest = versions.pop(0)
        oldest.unlink()
        logging.info("Pruned old version: %s", oldest.name)


def save_version():
    """Copy current file to archive with timestamp."""
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = ARCHIVE_DIR / f"global_CLAUDE_{stamp}.md"
    shutil.copy2(str(WATCH_FILE), str(dest))
    logging.info("Saved version: %s", dest.name)
    prune_old_versions()


def main():
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    logging.info("Watcher started (%s). Watching: %s", VERSION, WATCH_FILE)

    last_hash = None

    if WATCH_FILE.exists():
        last_hash = file_hash(WATCH_FILE)
        # Save initial version if archive is empty
        if not archive_versions():
            save_version()
            logging.info("Initial version archived.")

    while True:
        try:
            if WATCH_FILE.exists():
                current_hash = file_hash(WATCH_FILE)
                if current_hash != last_hash:
                    save_version()
                    last_hash = current_hash
            else:
                logging.warning("Watch file not found: %s", WATCH_FILE)
        except Exception as e:
            logging.error("Error: %s", e)

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
