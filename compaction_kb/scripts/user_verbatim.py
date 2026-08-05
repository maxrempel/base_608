#!/usr/bin/env python3
"""
user_verbatim.py - durable VERBATIM record of everything MAX typed in a session.

Why (Max, 2026-06-12): a compaction wipes ~94% of context, so Max's own words -
the specs he dictated, the corrections he gave - are LOST to the session after a
compaction. This tool keeps an append-only, on-disk, verbatim copy of every Max
prompt, so:
  1. SPEC RECOVERY - after a compaction the session can re-read exactly what Max
     asked for (his wording is intentional; paraphrase loses function).
  2. TROUBLE INVESTIGATION - a faithful transcript of Max's side, easy to scan
     when debugging "what did he actually say / when did this go wrong".

Source of truth: the UserPromptSubmit hook's stdin `prompt` field is EXACTLY and
ONLY what Max typed (before any hook injection / system reminder / tool result),
so the live `--hook` path is the cleanest capture. `backfill` reconstructs the
same record from the transcript .jsonl for past turns (or after the fact).

Storage: one append-only markdown file PER SESSION, named with the SAME stem
scheme as session_status.py, under C:\\claude_base\\user_verbatim\\ . So an
investigator can match a session_status breadcrumb to its verbatim file by stem.

Post-compaction pointer: on the first turn after a NEW compaction appears in the
transcript, the hook injects a one-line note telling the session WHERE its
verbatim spec log is and HOW to read it - so a cold post-compaction session knows
to look it up (Max: "the session should know where to look it up").

Modes:
  python user_verbatim.py --hook            UserPromptSubmit hook (stdin JSON)
  python user_verbatim.py read [--cwd ...]  print this session's verbatim log
  python user_verbatim.py backfill [--cwd]  rebuild the log from the transcript
  python user_verbatim.py path [--cwd ...]  print this session's log path

Fails open everywhere: a broken verbatim log must NEVER wedge or slow a session.
"""
import sys, os, json, glob, time, re

VERBATIM_DIR = r"C:\claude_base\user_verbatim"
STATE_DIR = os.path.join(VERBATIM_DIR, ".state")
PROJECTS = os.path.expanduser(r"~\.claude\projects")

# Prompts that are pure machinery, not Max speaking - skip these so the verbatim
# record stays a clean transcript of Max's own words.
_SKIP_PREFIXES = ("<command-name>", "<local-command-stdout>", "Caveat:")


def _project_name_for_cwd(cwd):
    norm = os.path.abspath(cwd)
    return "".join("-" if ch in ":\\/._" else ch for ch in norm)


def _find_transcript(cwd):
    pdir = os.path.join(PROJECTS, _project_name_for_cwd(cwd))
    if not os.path.isdir(pdir):
        return None
    cands = glob.glob(os.path.join(pdir, "*.jsonl"))
    return max(cands, key=os.path.getmtime) if cands else None


def _sid_from_transcript(transcript):
    return os.path.splitext(os.path.basename(transcript))[0]


def _log_path(cwd, transcript):
    """SAME stem scheme as session_status._status_path so the two files pair up."""
    sid = _sid_from_transcript(transcript)
    tail = re.sub(r"[^A-Za-z0-9]+", "_", os.path.basename(os.path.abspath(cwd)))[-24:]
    day = time.strftime("%Y%m%d")
    return os.path.join(VERBATIM_DIR, f"{day}_{tail}_{sid[:8]}.verbatim.md")


def _state_path(sid):
    return os.path.join(STATE_DIR, sid + ".json")


def _read_state(sid):
    try:
        with open(_state_path(sid), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _write_state(sid, st):
    try:
        os.makedirs(STATE_DIR, exist_ok=True)
        with open(_state_path(sid), "w", encoding="utf-8") as f:
            json.dump(st, f)
    except Exception:
        pass


def _ensure_header(path, cwd, sid):
    if not os.path.isfile(path):
        os.makedirs(VERBATIM_DIR, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(
                f"# VERBATIM user (Max) log - session {sid}\n"
                f"# cwd: {cwd}\n"
                "# Every line Max typed, saved verbatim, so it survives compaction.\n"
                "# Recover specs / investigate trouble by reading this file.\n\n")


def _append_entry(path, text, turn):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"\n## [{ts}] turn {turn}\n{text.rstrip()}\n")


def _is_skippable(text):
    t = text.lstrip()
    return any(t.startswith(p) for p in _SKIP_PREFIXES)


def _count_compactions(transcript):
    """How many compaction boundaries the transcript currently holds. Claude Code
    writes type=system, subtype=compact_boundary on each compaction."""
    n = 0
    try:
        with open(transcript, "rb") as fh:
            for bl in fh:
                s = bl.strip()
                if not s or b"compact_boundary" not in s:
                    continue
                try:
                    r = json.loads(s.decode("utf-8", "replace"))
                except Exception:
                    continue
                if r.get("type") == "system" and r.get("subtype") == "compact_boundary":
                    n += 1
    except Exception:
        pass
    return n


def _iter_max_messages(transcript):
    """Yield each genuine Max-typed message text from the transcript, in order.
    Skips tool-result user turns, meta turns, and machinery prompts."""
    try:
        with open(transcript, "rb") as fh:
            for bl in fh:
                s = bl.strip()
                if not s:
                    continue
                try:
                    r = json.loads(s.decode("utf-8", "replace"))
                except Exception:
                    continue
                if r.get("type") != "user" or r.get("isMeta"):
                    continue
                m = r.get("message")
                if not isinstance(m, dict):
                    continue
                c = m.get("content")
                text = None
                if isinstance(c, str):
                    text = c
                elif isinstance(c, list):
                    # Real typed turn = has text blocks and NO tool_result blocks.
                    if any(isinstance(b, dict) and b.get("type") == "tool_result" for b in c):
                        continue
                    parts = [str(b.get("text", "")) for b in c
                             if isinstance(b, dict) and b.get("type") == "text"]
                    text = "\n".join(p for p in parts if p)
                if not text or not text.strip() or _is_skippable(text):
                    continue
                yield text.strip()
    except Exception:
        return


def _strip_injected(text):
    """Remove system-reminder / hook-injected blocks that ride along on a user
    turn, leaving only what Max actually typed. The live --hook path needs none
    of this (stdin `prompt` is already pure); backfill uses it defensively."""
    out = re.sub(r"<system-reminder>.*?</system-reminder>", "", text, flags=re.DOTALL)
    out = re.sub(r"<user-prompt-submit-hook>.*?</user-prompt-submit-hook>", "", out, flags=re.DOTALL)
    return out.strip()


def cmd_hook():
    cwd = os.getcwd()
    transcript = None
    prompt_text = None
    try:
        data = json.load(sys.stdin)
        cwd = data.get("cwd") or cwd
        transcript = data.get("transcript_path") or None
        pt = data.get("prompt")
        if isinstance(pt, str):
            prompt_text = pt
    except Exception:
        pass
    if not transcript:
        transcript = _find_transcript(cwd)
    if not transcript or not os.path.isfile(transcript):
        return 0

    sid = _sid_from_transcript(transcript)
    path = _log_path(cwd, transcript)
    st = _read_state(sid)

    # 1. Append Max's verbatim words (stdin prompt is the pure source).
    if prompt_text and prompt_text.strip() and not _is_skippable(prompt_text):
        st["turn"] = int(st.get("turn", 0)) + 1
        _ensure_header(path, cwd, sid)
        _append_entry(path, prompt_text, st["turn"])

    # 2. Post-compaction pointer: if a NEW compaction appeared, tell the session
    #    where its verbatim spec log lives so it can recover Max's exact words.
    comp = _count_compactions(transcript)
    if comp > int(st.get("compactions", 0)):
        st["compactions"] = comp
        print(
            "=== CONTEXT WAS JUST COMPACTED (~94%% of context lost) ===\n"
            "To recover the full picture, run the ONE catch-up command - it pulls "
            "ALL recovery sources together (Max's verbatim words, the work-log, the "
            "Scribe handover, the breadcrumb):\n"
            "  python C:/claude_base/compaction_kb/scripts/resume.py\n"
            "Or just Max's exact words:\n"
            "  python C:/claude_base/compaction_kb/scripts/user_verbatim.py read\n"
            f"  (verbatim file: {path})\n"
            "=== end compaction-recovery pointer ===")

    _write_state(sid, st)
    return 0


def cmd_read(cwd):
    transcript = _find_transcript(cwd)
    if not transcript:
        print("user_verbatim: no transcript found for this cwd")
        return 0
    path = _log_path(cwd, transcript)
    if not os.path.isfile(path):
        print(f"user_verbatim: no verbatim log yet at {path}")
        return 0
    with open(path, encoding="utf-8") as f:
        sys.stdout.write(f.read())
    return 0


def cmd_path(cwd):
    transcript = _find_transcript(cwd)
    if not transcript:
        print("user_verbatim: no transcript found for this cwd")
        return 0
    print(_log_path(cwd, transcript))
    return 0


def cmd_backfill(cwd):
    """Rebuild this session's verbatim log from the transcript - catches turns
    from before the hook was installed, and repairs a lost file. Overwrites the
    file with the full reconstructed record."""
    transcript = _find_transcript(cwd)
    if not transcript:
        print("user_verbatim: no transcript found for this cwd")
        return 0
    sid = _sid_from_transcript(transcript)
    path = _log_path(cwd, transcript)
    msgs = list(_iter_max_messages(transcript))
    os.makedirs(VERBATIM_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(
            f"# VERBATIM user (Max) log - session {sid} (BACKFILLED from transcript)\n"
            f"# cwd: {cwd}\n"
            "# Every line Max typed, saved verbatim, so it survives compaction.\n\n")
    n = 0
    for i, raw in enumerate(msgs, 1):
        clean = _strip_injected(raw)
        if not clean:
            continue
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"\n## turn {i}\n{clean}\n")
        n += 1
    # Keep the live counter ahead of the backfill so we don't renumber on resume.
    st = _read_state(sid)
    st["turn"] = max(int(st.get("turn", 0)), len(msgs))
    st["compactions"] = _count_compactions(transcript)
    _write_state(sid, st)
    print(f"user_verbatim: backfilled {n} Max messages -> {path}")
    return 0


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    args = sys.argv[1:]
    cwd = os.getcwd()
    if "--cwd" in args:
        i = args.index("--cwd")
        cwd = args[i + 1]
        del args[i:i + 2]
    if not args:
        print("usage: user_verbatim.py [--hook | read | backfill | path] [--cwd ...]")
        return 0
    if args[0] == "--hook":
        return cmd_hook()
    if args[0] == "read":
        return cmd_read(cwd)
    if args[0] == "backfill":
        return cmd_backfill(cwd)
    if args[0] == "path":
        return cmd_path(cwd)
    print("usage: user_verbatim.py [--hook | read | backfill | path] [--cwd ...]")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main() or 0)
    except Exception as e:
        sys.stderr.write(f"user_verbatim error (ignored): {e}\n")
        sys.exit(0)
