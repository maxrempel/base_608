#!/usr/bin/env python3
"""
resume.py - ONE catch-up command that pulls EVERY recovery source together.

Max, 2026-06-12: several processes now write recovery material (the Scribe
handover, the conscious work-log, the verbatim user-log, the mechanical
breadcrumb). The duplication is fine, but a resuming/post-compaction session
should TAKE ADVANTAGE OF ALL of them - not just one. This command gathers them
all for the current project/session and prints them in one shot, so a cold
session inherits the full picture with a single call.

  python C:/claude_base/compaction_kb/scripts/resume.py

Reads (each section fails open independently):
  1. VERBATIM  - Max's exact words this session       (user_verbatim/)
  2. WORK-LOG  - the model's conscious DID/STATE/NEXT  (worklog/<project-key>.md)
  3. SCRIBE    - the latest full-Opus handover         (session_status/<stem>.handover.m*.md)
  4. BREADCRUMB- the mechanical token/turn snapshots    (session_status/<stem>.md)
"""
import sys, os, glob, time, re, hashlib

PROJECTS = os.path.expanduser(r"~\.claude\projects")
WORKLOG_DIR = r"C:\claude_base\worklog"
STATUS_DIR = r"C:\claude_base\session_status"
VERBATIM_DIR = r"C:\claude_base\user_verbatim"


def _proj_name(cwd):
    return "".join("-" if ch in ":\\/._" else ch for ch in os.path.abspath(cwd))


def _find_transcript(cwd):
    pdir = os.path.join(PROJECTS, _proj_name(cwd))
    if not os.path.isdir(pdir):
        return None
    c = glob.glob(os.path.join(pdir, "*.jsonl"))
    return max(c, key=os.path.getmtime) if c else None


def _sid(t):
    return os.path.splitext(os.path.basename(t))[0]


def _stem(cwd, t):
    tail = re.sub(r"[^A-Za-z0-9]+", "_", os.path.basename(os.path.abspath(cwd)))[-24:]
    return f"{time.strftime('%Y%m%d')}_{tail}_{_sid(t)[:8]}"


def _worklog_path(cwd):
    norm = os.path.normcase(os.path.abspath(cwd))
    h = hashlib.sha1(norm.encode("utf-8", "replace")).hexdigest()[:10]
    tail = re.sub(r"[^A-Za-z0-9]+", "_", os.path.basename(norm))[-32:]
    return os.path.join(WORKLOG_DIR, f"{tail}_{h}.md")


def _section(title, body):
    print("\n" + "=" * 70)
    print("== " + title)
    print("=" * 70)
    print(body.rstrip() if body and body.strip() else "(none found)")


def _read(path, tail_chars=0):
    try:
        with open(path, encoding="utf-8") as f:
            txt = f.read()
        if tail_chars and len(txt) > tail_chars:
            txt = "...(truncated)...\n" + txt[-tail_chars:]
        return txt
    except Exception:
        return ""


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    cwd = os.getcwd()
    if "--cwd" in sys.argv:
        cwd = sys.argv[sys.argv.index("--cwd") + 1]
    t = _find_transcript(cwd)
    if not t:
        print("resume: no transcript for this cwd:", cwd)
        return 0
    stem = _stem(cwd, t)
    print("RESUME / CATCH-UP for cwd:", cwd)
    print("session:", _sid(t), "| stem:", stem)

    # 1. Verbatim (Max's exact words) - the spec source of truth.
    vp = os.path.join(VERBATIM_DIR, stem + ".verbatim.md")
    if not os.path.isfile(vp):  # day may differ; match by session id
        cand = glob.glob(os.path.join(VERBATIM_DIR, f"*_{_sid(t)[:8]}.verbatim.md"))
        vp = cand[0] if cand else vp
    _section("1. VERBATIM - what Max actually said (his specs/corrections)", _read(vp))

    # 2. Conscious work-log (model digest).
    _section("2. WORK-LOG - DID/STATE/NEXT digest", _read(_worklog_path(cwd), tail_chars=6000))

    # 3. Latest Scribe handover.
    hand = sorted(glob.glob(os.path.join(STATUS_DIR, stem + ".handover.m*.md")))
    _section("3. SCRIBE handover (latest full-Opus summary)",
             _read(hand[-1]) if hand else "")

    # 4. Mechanical breadcrumb.
    _section("4. BREADCRUMB - token/turn snapshots", _read(os.path.join(STATUS_DIR, stem + ".md")))
    print("\n=== end resume ===")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main() or 0)
    except Exception as e:
        sys.stderr.write(f"resume.py error (ignored): {e}\n")
        sys.exit(0)
