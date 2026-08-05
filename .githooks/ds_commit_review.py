#!/usr/bin/env python3
# ============================================================================
# ds_commit_review.py  -  "Guard B": a cheap DeepSeek second gate on commits
# ----------------------------------------------------------------------------
# Part of the claude_base anti-GitHub-bloat system (built 2026-07-16, E45).
#
# WHAT: the scripted size/extension guards in .githooks/pre-commit (Guard A)
# catch the obvious heavy files. This reviewer catches the GRAY cases they
# miss - e.g. an 8 MB .json that is really a data dump, a "backup_2026...".snapshot,
# a browser-cache file, a generated output table - things that look like source
# by extension/size but are actually junk that should never enter git history.
#
# HOW: sends ONLY the staged file LIST (path + size + extension, never content)
# to DeepSeek-chat (Max's own cheap key) and asks it to flag files that look
# like generated output / data / downloads / caches / versioned backup snapshots
# rather than source code, docs, or config. High-confidence flags BLOCK the
# commit (exit 2); the session can override with `git commit --no-verify`.
#
# SAFETY - FAILS OPEN, NEVER WEDGES A SESSION:
#   - no key / no network / timeout / any error  -> exit 0 (allow).
#   - SKIP_DS_REVIEW=1 in the environment          -> exit 0 (allow).
#   - nothing worth checking (all small code/docs) -> exit 0 (allow), no API call.
# So an offline or misconfigured box still commits normally; the gate only ever
# ADDS a block on a positive, high-confidence junk verdict.
# ============================================================================
import json
import os
import re
import subprocess
import sys
import urllib.request

SSH = os.path.expanduser(r"C:\Users\maxre\Nextcloud\zSyncMain\ssh")
# per-machine fallbacks (Sirius/Vega/Centauri roots differ)
for alt in (r"C:\Users\mremp\00HA1py\Nextcloud\zSyncMain\ssh",
            r"C:\Users\maxre\Nextcloud2\zSyncMain\ssh",
            r"D:\Nextcloud\zSyncMain\ssh"):
    if not os.path.isdir(SSH) and os.path.isdir(alt):
        SSH = alt
KEY_FILE = os.path.join(SSH, "deepseek_api_key_20260226.txt")
MODEL = "deepseek-chat"
DS_URL = "https://api.deepseek.com/chat/completions"
TIMEOUT_S = 20

# Extensions that are plausibly source/docs/config - never worth an LLM look on
# their own. If EVERY staged file is one of these AND small, skip the API call.
CODE_EXT = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".sh", ".ps1", ".bat", ".md", ".txt",
    ".html", ".css", ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".sql",
    ".c", ".h", ".cpp", ".go", ".rs", ".java", ".rb", ".php", ".xml", ".svg",
    ".gitignore", ".env", "",
}
# A staged file bigger than this (bytes) is always worth a look, whatever its type.
LOOK_IF_BIGGER = 1 * 1024 * 1024  # 1 MB


def read_key():
    try:
        with open(KEY_FILE, "r", encoding="utf-8", errors="ignore") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    return line.split()[0]
    except Exception:
        return None
    return None


def staged():
    out = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True, text=True,
    ).stdout
    files = []
    for f in out.splitlines():
        f = f.strip()
        if not f:
            continue
        try:
            sz = int(subprocess.run(
                ["git", "cat-file", "-s", ":" + f],
                capture_output=True, text=True,
            ).stdout.strip() or "0")
        except Exception:
            sz = 0
        files.append((f, sz))
    return files


def worth_checking(files):
    for f, sz in files:
        ext = os.path.splitext(f)[1].lower()
        if sz >= LOOK_IF_BIGGER:
            return True
        if ext not in CODE_EXT:
            return True
    return False


def deepseek(files):
    key = read_key()
    if not key:
        return None
    listing = "\n".join(f"{sz:>12} bytes  {f}" for f, sz in files)
    prompt = (
        "You are a git commit janitor for a code+tools repository. Below is the "
        "list of files staged for a commit (path and size only - not content).\n"
        "Flag ONLY files that are clearly GENERATED OUTPUT, DATA DUMPS, DOWNLOADS, "
        "MODEL WEIGHTS, BROWSER/APP CACHES, LOGS, or VERSIONED BACKUP SNAPSHOTS - "
        "things that must never enter git history because they bloat the repo. "
        "Do NOT flag source code, documentation, small config, or small hand-written "
        "data. When unsure, do NOT flag - false blocks annoy the team.\n\n"
        "Reply STRICTLY as JSON: {\"junk\": [\"path\", ...], \"reason\": \"one short line\"}. "
        "Empty list if all files look legitimate.\n\n"
        "STAGED FILES:\n" + listing
    )
    body = json.dumps({
        "model": MODEL,
        "max_tokens": 500,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }).encode()
    req = urllib.request.Request(DS_URL, data=body, headers={
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json",
    })
    try:
        resp = urllib.request.urlopen(req, timeout=TIMEOUT_S).read()
        text = json.loads(resp)["choices"][0]["message"].get("content") or ""
    except Exception:
        return None
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except Exception:
        return None


def main():
    if os.environ.get("SKIP_DS_REVIEW"):
        sys.exit(0)
    files = staged()
    if not files or not worth_checking(files):
        sys.exit(0)
    verdict = deepseek(files)
    if not verdict:
        sys.exit(0)  # fail open
    junk = [j for j in verdict.get("junk", []) if j]
    if not junk:
        sys.exit(0)
    reason = verdict.get("reason", "").strip()
    print("")
    print("==================================================================")
    print("  COMMIT BLOCKED by DeepSeek review (Guard B) - these staged files")
    print("  look like generated output / data / cache / backup, not source:")
    print("")
    for j in junk:
        print("     " + j)
    if reason:
        print("")
        print("  DeepSeek: " + reason)
    print("")
    print("  If this is real junk: unstage it and add it to .gitignore.")
    print("     git restore --staged <file>")
    print("")
    print("  If DeepSeek is WRONG (it is a real source file):")
    print("     git commit --no-verify        # override this gate")
    print("==================================================================")
    print("")
    sys.exit(2)


if __name__ == "__main__":
    main()
