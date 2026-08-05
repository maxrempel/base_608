#!/usr/bin/env python3
"""
ctx_track.py - measure a Claude session's transcript size + detect compactions.

Part of the compaction-calibration KB (b2's project). Each run:
  - locates the session transcript (.jsonl) for a cwd (or an explicit path)
  - measures bytes, line count, estimated tokens, message-text tokens
  - scans for compaction marker lines (and logs unknown system subtypes so we
    discover the real marker the first time a compaction ever fires)
  - appends one record to logs/ctx_log.jsonl
  - if a NEW compaction is detected vs the last logged run, writes a calibration
    event to kb/compaction_events.jsonl (size-before = the gold number) and
    prints an ALERT line the caller can broadcast.

Usage:
  python ctx_track.py                         auto-detect transcript from cwd
  python ctx_track.py --cwd "C:\\path"        detect for a given cwd
  python ctx_track.py --transcript "X.jsonl"  use an explicit transcript
  python ctx_track.py --branch b2             tag the log record with a branch id
  python ctx_track.py --hook                  read cwd+transcript_path from stdin JSON

Fails open: prints what it can, never raises out.
"""
import sys, os, json, glob, time, collections

KB_BASE = r"C:\claude_base\compaction_kb"
LOG_PATH = os.path.join(KB_BASE, "logs", "ctx_log.jsonl")
EVENT_PATH = os.path.join(KB_BASE, "kb", "compaction_events.jsonl")
ARCHIVE_DIR = os.path.join(KB_BASE, "kb", "pre_compaction_archive")
PROJECTS = os.path.expanduser(r"~\.claude\projects")

# Candidate compaction markers - we don't yet know the real one, so be generous.
SUBTYPE_HINTS = ("compact",)
TEXT_HINTS = (
    "this session is being continued",
    "the conversation is summarized below",
    "compacted",
    "context low",
    "previous conversation",
)
KNOWN_SYSTEM_SUBTYPES = {"stop_hook_summary"}  # benign; not compaction


def _project_name_for_cwd(cwd):
    norm = os.path.abspath(cwd)
    out = []
    for ch in norm:
        out.append("-" if ch in ':\\/._' else ch)
    return "".join(out)


def _find_transcript(cwd):
    pname = _project_name_for_cwd(cwd)
    pdir = os.path.join(PROJECTS, pname)
    if not os.path.isdir(pdir):
        return None
    cands = [f for f in glob.glob(os.path.join(pdir, "*.jsonl"))]
    if not cands:
        return None
    return max(cands, key=os.path.getmtime)


def _branch_for_cwd(cwd):
    """Read the bcast identity for this cwd, so logs are tagged b1/b2/..."""
    try:
        import hashlib, re
        norm = os.path.normcase(os.path.abspath(cwd))
        h = hashlib.sha1(norm.encode("utf-8", "replace")).hexdigest()[:10]
        tail = re.sub(r"[^A-Za-z0-9]+", "_", os.path.basename(norm))[-32:]
        key = f"{tail}_{h}"
        p = os.path.join(r"C:\claude_base\branch_bulletin\state", key + ".json")
        with open(p, encoding="utf-8") as f:
            return json.load(f).get("id")
    except Exception:
        return None


def _analyze(path):
    size = os.path.getsize(path)
    lines = 0
    msg_chars = 0
    tool_calls = 0
    compaction_lines = []          # (line_index, marker_reason)
    text_hint_lines = 0            # diagnostic only, NOT counted as compactions
    unknown_sys = collections.Counter()
    byte_offsets = [0]             # cumulative bytes at each line end
    with open(path, "rb") as fh:
        raw = fh.read()
    text_lines = raw.split(b"\n")
    cum = 0
    for i, bl in enumerate(text_lines):
        cum += len(bl) + 1
        s = bl.strip()
        if not s:
            continue
        lines += 1
        byte_offsets.append(cum)
        try:
            r = json.loads(s.decode("utf-8", "replace"))
        except Exception:
            continue
        t = r.get("type")
        st = r.get("subtype")
        # message text size (better token proxy than raw file bytes)
        m = r.get("message")
        if isinstance(m, dict):
            c = m.get("content")
            msg_chars += len(json.dumps(c, ensure_ascii=False)) if c is not None else 0
            if isinstance(c, list):
                for blk in c:
                    if isinstance(blk, dict) and blk.get("type") == "tool_use":
                        tool_calls += 1
        # compaction detection - STRUCTURAL ONLY.
        # Lesson 2026-06-06: text-blob matching gives false positives when the
        # session merely DISCUSSES compaction (or CLAUDE.md mentions "continued
        # from a previous conversation"). Count only structural markers.
        reason = None
        if r.get("isCompactSummary") is True:
            reason = "isCompactSummary"
        elif t == "summary":
            reason = "type=summary"
        elif st and any(h in str(st).lower() for h in SUBTYPE_HINTS):
            reason = f"subtype={st}"
        if reason:
            compaction_lines.append((i, reason, cum))
        # discover unknown system subtypes (one of these may be the real marker)
        if t == "system" and st and st not in KNOWN_SYSTEM_SUBTYPES:
            unknown_sys[st] += 1
        # text hints kept only as a separate, NON-counting diagnostic
        if reason is None:
            blob = json.dumps(r, ensure_ascii=False).lower()
            for h in TEXT_HINTS:
                if h in blob:
                    text_hint_lines += 1
                    break

    est_tokens_file = size // 4
    est_tokens_msg = msg_chars // 4
    bytes_since_compaction = size
    if compaction_lines:
        bytes_since_compaction = size - compaction_lines[-1][2]
    return {
        "bytes": size,
        "lines": lines,
        "est_tokens_file": est_tokens_file,
        "est_tokens_msg": est_tokens_msg,
        "tool_calls": tool_calls,
        "compaction_count": len(compaction_lines),
        "compaction_markers": compaction_lines,
        "bytes_since_compaction": bytes_since_compaction,
        "unknown_system_subtypes": dict(unknown_sys),
        "text_hint_lines": text_hint_lines,
    }


def _last_logged(transcript):
    """Return the most recent log record for this transcript, if any."""
    try:
        last = None
        with open(LOG_PATH, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                if r.get("transcript") == transcript:
                    last = r
        return last
    except Exception:
        return None


def run(cwd, transcript=None, branch=None, hook=False):
    if not transcript:
        transcript = _find_transcript(cwd)
    if not transcript or not os.path.isfile(transcript):
        print(f"ctx_track: no transcript found for cwd={cwd}")
        return 0
    if not branch:
        branch = _branch_for_cwd(cwd)
    a = _analyze(transcript)
    prev = _last_logged(transcript)
    new_compaction = False
    if prev and a["compaction_count"] > prev.get("compaction_count", 0):
        new_compaction = True

    rec = {
        "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
        "branch": branch,
        "transcript": transcript,
        "bytes": a["bytes"],
        "lines": a["lines"],
        "est_tokens_file": a["est_tokens_file"],
        "est_tokens_msg": a["est_tokens_msg"],
        "tool_calls": a["tool_calls"],
        "compaction_count": a["compaction_count"],
        "bytes_since_compaction": a["bytes_since_compaction"],
        "unknown_system_subtypes": a["unknown_system_subtypes"],
    }
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=True) + "\n")

    alert = None
    if new_compaction:
        # gold calibration number = size at the run JUST BEFORE compaction
        size_before = prev.get("bytes")
        tok_before = prev.get("est_tokens_file")
        ev = {
            "ts": rec["ts"],
            "branch": branch,
            "transcript": transcript,
            "size_before_bytes": size_before,
            "est_tokens_before": tok_before,
            "size_after_bytes": a["bytes"],
            "marker": a["compaction_markers"][-1][1] if a["compaction_markers"] else None,
            "compaction_count": a["compaction_count"],
        }
        os.makedirs(os.path.dirname(EVENT_PATH), exist_ok=True)
        with open(EVENT_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(ev, ensure_ascii=True) + "\n")
        alert = (f"COMPACTION DETECTED branch={branch} fired near "
                 f"{size_before} bytes (~{tok_before} tk). Event logged.")

    unk = a["unknown_system_subtypes"]
    summary = (f"ctx_track {branch or '?'}: {a['bytes']} bytes, {a['lines']} lines, "
               f"~{a['est_tokens_file']} tk(file)/~{a['est_tokens_msg']} tk(msg), "
               f"tools={a['tool_calls']}, compactions={a['compaction_count']}")
    print(summary)
    if unk:
        print(f"  NEW unknown system subtypes (possible compaction marker?): {unk}")
    if alert:
        print("ALERT: " + alert)
    return 0


def main():
    args = sys.argv[1:]
    cwd = os.getcwd()
    transcript = None
    branch = None
    if "--hook" in args:
        try:
            data = json.load(sys.stdin)
            cwd = data.get("cwd") or cwd
            transcript = data.get("transcript_path") or None
        except Exception:
            pass
    if "--cwd" in args:
        cwd = args[args.index("--cwd") + 1]
    if "--transcript" in args:
        transcript = args[args.index("--transcript") + 1]
    if "--branch" in args:
        branch = args[args.index("--branch") + 1]
    return run(cwd, transcript=transcript, branch=branch, hook="--hook" in args)


if __name__ == "__main__":
    try:
        sys.exit(main() or 0)
    except Exception as e:
        sys.stderr.write(f"ctx_track error (ignored): {e}\n")
        sys.exit(0)
