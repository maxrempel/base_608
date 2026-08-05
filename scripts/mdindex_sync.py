"""Build Max's instruction index and safely stage documents for Memex.

Version 05, 2026-07-21. The previous version could interpret a partial
Nextcloud scan as mass deletion and erase staged knowledge. This version fails
closed on scan collapse, writes state atomically, quarantines rather than
deletes stale copies, and permits only one running instance.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import math
import os
import shutil
import socket
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


VERSION = "v05 | 2026-07-21"
SCAN_INTERVAL = 600
MIN_SAFE_SCAN_RATIO = 0.80
MIN_BASELINE_FOR_RATIO = 20


@dataclass(frozen=True)
class Config:
    folder_registry: Path = Path(r"C:\cloud_base\scripts\folder_registry.txt")
    mdindex_file: Path = Path(r"C:\cloud_base\mdindex.md")
    memex_dir: Path = Path(
        r"C:\Users\maxre\Nextcloud\00_clawy_kb\memories\from_tomemex"
    )
    log_file: Path = Path(r"C:\cloud_base\scripts\mdindex_sync.log")
    hash_cache: Path = Path(r"C:\cloud_base\scripts\.mdindex_hashes.txt")
    health_file: Path = Path(r"C:\cloud_base\scripts\.mdindex_health.json")
    lock_file: Path = Path(r"C:\cloud_base\scripts\.mdindex_sync.lock")

    @property
    def quarantine_dir(self) -> Path:
        return self.memex_dir.parent / "from_tomemex_archive"


def configure_logging(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=str(path),
        level=logging.INFO,
        format="%(asctime)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True,
    )


def load_registry(path: Path) -> list[tuple[Path, int]]:
    roots: list[tuple[Path, int]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "|" in line:
            path_str, depth_str = line.rsplit("|", 1)
            roots.append((Path(path_str.strip()), int(depth_str.strip())))
        else:
            roots.append((Path(line), 5))
    if not roots:
        raise RuntimeError("Folder registry contains no scan roots")
    return roots


def scan_for_memex_files(
    roots: list[tuple[Path, int]],
) -> tuple[list[Path], list[str]]:
    found: list[Path] = []
    issues: list[str] = []
    for root, max_depth in roots:
        if not root.is_dir():
            issues.append(f"registry root unavailable: {root}")
            continue
        try:
            candidates = root.rglob("*_tomemex.md")
            for md_file in candidates:
                try:
                    rel = md_file.relative_to(root)
                    if len(rel.parts) > max_depth:
                        continue
                    if "00_clawy_kb" in md_file.parts:
                        continue
                    if ".claude" in md_file.parts or ".git" in md_file.parts:
                        continue
                    found.append(md_file)
                except (OSError, ValueError) as exc:
                    issues.append(f"could not inspect {md_file}: {exc}")
        except OSError as exc:
            issues.append(f"scan failed for {root}: {exc}")
    return sorted(set(found)), issues


def file_hash(path: Path) -> str | None:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()
    except OSError:
        return None


def load_hash_cache(path: Path) -> dict[str, str]:
    cache: dict[str, str] = {}
    if not path.is_file():
        return cache
    for line in path.read_text(encoding="utf-8").splitlines():
        if "|" in line:
            digest, source = line.split("|", 1)
            cache[source] = digest
    return cache


def atomic_text_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temp.write_text(content, encoding="utf-8", newline="\n")
    os.replace(temp, path)


def save_hash_cache(path: Path, cache: dict[str, str]) -> None:
    lines = [f"{digest}|{source}" for source, digest in sorted(cache.items())]
    atomic_text_write(path, "\n".join(lines) + "\n")


def make_local_key(filepath: Path) -> str:
    return f"local_{filepath.parent.name}__{filepath.name}"


def first_meaningful_line(filepath: Path) -> str:
    try:
        text = filepath.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    for line in text.splitlines():
        line = line.strip().lstrip("#").strip()
        if line and not line.startswith("---") and len(line) > 5:
            return line[:120]
    return ""


def classify_project(filepath: Path) -> str:
    path_str = str(filepath).lower()
    if "moma" in path_str:
        return "moma (video production)"
    if "ai_images" in path_str:
        return "kazarian episode (image/video/sound)"
    if "claude_md_synced" in path_str:
        return "claude code setup"
    if "z_kazarian_episode" in path_str:
        return "kazarian episode (scripts)"
    if "cloud_base" in path_str:
        return "cloud_base (infrastructure)"
    if "claude_base" in path_str:
        return "claude_base (work logs)"
    return "other"


def clean_name(filename: str) -> str:
    return filename.replace("_tomemex.md", "").replace("_", " ")


def build_mdindex(files: list[Path]) -> str:
    lines = [
        "# Instruction Files Index",
        f"# Auto-generated {datetime.now().strftime('%Y-%m-%d %H:%M')} by mdindex_sync {VERSION}",
        f"# {len(files)} files. Read any file for full instructions.",
        "#",
        "# Codex and Claude: use this index for specialized instructions.",
        "# Search Memex by topic; read the canonical path below before acting.",
        "",
    ]
    grouped: dict[str, list[Path]] = {}
    for source in files:
        grouped.setdefault(classify_project(source), []).append(source)
    for project in sorted(grouped):
        lines.append(f"## {project}")
        for source in grouped[project]:
            lines.append(f"  {clean_name(source.name)}: {first_meaningful_line(source)}")
            lines.append(f"    path: {source}")
        lines.append("")
    return "\n".join(lines)


def validate_scan(
    files: list[Path], old_cache: dict[str, str], issues: list[str]
) -> list[str]:
    failures = list(issues)
    previous_count = len(old_cache)
    current_count = len(files)
    if previous_count >= MIN_BASELINE_FOR_RATIO:
        minimum = math.ceil(previous_count * MIN_SAFE_SCAN_RATIO)
        if current_count < minimum:
            failures.append(
                f"scan collapse: found {current_count}, below safe minimum {minimum} "
                f"from prior baseline {previous_count}"
            )
    if not files:
        failures.append("scan returned no instruction files")
    return failures


def build_new_cache(files: list[Path]) -> tuple[dict[str, str], list[str]]:
    cache: dict[str, str] = {}
    failures: list[str] = []
    for source in files:
        digest = file_hash(source)
        if digest is None:
            failures.append(f"could not read source: {source}")
        else:
            cache[str(source)] = digest
    return cache, failures


def copy_changed_sources(
    files: list[Path], old_cache: dict[str, str], new_cache: dict[str, str], memex_dir: Path
) -> int:
    memex_dir.mkdir(parents=True, exist_ok=True)
    copied = 0
    for source in files:
        destination = memex_dir / make_local_key(source)
        digest = new_cache[str(source)]
        if old_cache.get(str(source)) == digest and destination.is_file():
            continue
        temp = destination.with_name(f".{destination.name}.{os.getpid()}.tmp")
        try:
            shutil.copy2(source, temp)
            if file_hash(temp) != digest:
                raise OSError(f"copy verification failed for {source}")
            os.replace(temp, destination)
            copied += 1
        finally:
            if temp.exists():
                temp.unlink()
    return copied


def quarantine_stale_sources(files: list[Path], config: Config) -> int:
    current_keys = {make_local_key(source) for source in files}
    stale = [
        path
        for path in config.memex_dir.glob("local_*.md")
        if path.name not in current_keys
    ]
    if not stale:
        return 0
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    destination_dir = config.quarantine_dir / stamp
    destination_dir.mkdir(parents=True, exist_ok=True)
    for source in stale:
        os.replace(source, destination_dir / source.name)
        logging.info("Quarantined stale: %s", source.name)
    return len(stale)


def run_once(config: Config | None = None) -> dict:
    config = config or Config()
    roots = load_registry(config.folder_registry)
    files, scan_issues = scan_for_memex_files(roots)
    old_cache = load_hash_cache(config.hash_cache)
    failures = validate_scan(files, old_cache, scan_issues)
    new_cache, read_failures = build_new_cache(files)
    failures.extend(read_failures)

    event = {
        "checked_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "version": VERSION,
        "machine": socket.gethostname().lower(),
        "files_found": len(files),
        "prior_baseline": len(old_cache),
        "copied": 0,
        "quarantined": 0,
        "healthy": not failures,
        "failures": failures,
    }
    if failures:
        logging.error("Unsafe scan blocked; no state changed: %s", "; ".join(failures))
        atomic_text_write(config.health_file, json.dumps(event, indent=2) + "\n")
        return event

    event["copied"] = copy_changed_sources(files, old_cache, new_cache, config.memex_dir)
    event["quarantined"] = quarantine_stale_sources(files, config)
    atomic_text_write(config.mdindex_file, build_mdindex(files))
    save_hash_cache(config.hash_cache, new_cache)
    atomic_text_write(config.health_file, json.dumps(event, indent=2) + "\n")
    logging.info(
        "Healthy sync: %d files, %d copied, %d quarantined",
        len(files),
        event["copied"],
        event["quarantined"],
    )
    return event


def acquire_instance_lock(path: Path):
    """Return a locked file handle, or None when another instance owns it."""
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = path.open("a+b")
    handle.seek(0, os.SEEK_END)
    if handle.tell() == 0:
        handle.write(b"0")
        handle.flush()
    handle.seek(0)
    try:
        if os.name == "nt":
            import msvcrt

            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl

            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        handle.close()
        return None
    return handle


def release_instance_lock(handle) -> None:
    if handle is None:
        return
    handle.seek(0)
    if os.name == "nt":
        import msvcrt

        msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
    else:
        import fcntl

        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
    handle.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--once", action="store_true", help="run one scan and exit")
    parser.add_argument("--json", action="store_true", help="print the scan result")
    args = parser.parse_args()
    config = Config()
    configure_logging(config.log_file)
    lock = acquire_instance_lock(config.lock_file)
    if lock is None:
        logging.info("Duplicate mdindex_sync launch ignored")
        return 0
    try:
        logging.info("mdindex_sync started (%s)", VERSION)
        while True:
            try:
                event = run_once(config)
            except Exception as exc:
                logging.exception("Sync failed without changing prior healthy state: %s", exc)
                event = {"healthy": False, "failures": [str(exc)]}
            if args.json:
                print(json.dumps(event, indent=2))
            if args.once:
                return 0 if event.get("healthy") else 2
            time.sleep(SCAN_INTERVAL)
    finally:
        release_instance_lock(lock)


if __name__ == "__main__":
    raise SystemExit(main())
