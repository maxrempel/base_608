#!/usr/bin/env python3
"""
session_status.py - PROGRAMMATIC per-session status dumps (Component 6b).

Goal (Max, 2026-06-07): EVERY Claude session (not only named team branches)
should, ~10 times over its lifetime, dump a status snapshot to a file - driven
by a hook so it does NOT depend on the model remembering ("Opus ignores
instructions"). Triggered BY TOKENS so the snapshots cluster toward the ~840K
context-refresh point (where older context gets summarized).

TWO LAYERS (belt and suspenders):
  LAYER 1 (guaranteed, mechanical): on each token milestone the HOOK itself
    appends a line to the session's status file - timestamp, real token est,
    turn count, tool calls, last user prompt. Happens whether or not the model
    cooperates.
  LAYER 2 (best-effort, semantic): the hook ALSO injects a short note telling
    the session to FINISH its current step, then append a richer human status
    (DID / STATE / NEXT) via `session_status.py report "..."`. The note arrives
    at the next turn boundary (UserPromptSubmit), so it never interrupts a step
    mid-action. If the model ignores it, Layer 1 still captured a breadcrumb.

Token source: each assistant line in the transcript .jsonl carries
message.usage (input_tokens + cache_read + cache_creation = real prompt size).
We use the latest such value as the real context fill; fall back to bytes/4.

Modes:
  python session_status.py --hook        UserPromptSubmit hook (stdin JSON)
  python session_status.py report "..."  model appends a human status line
  python session_status.py read          print this session's status file

Fails open everywhere: a broken status dump must NEVER wedge a session.
"""
import sys, os, json, glob, time, re, subprocess

KB_BASE = r"C:\claude_base\compaction_kb"
STATUS_DIR = r"C:\claude_base\session_status"
STATE_DIR = os.path.join(STATUS_DIR, ".state")
PROJECTS = os.path.expanduser(r"~\.claude\projects")
OVERSEER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "session_oversight.py")

MILESTONE_TOKENS = 75000   # dump every ~75K real tokens -> ~11 dumps before the ~840K cliff
COMPACT_CLIFF = 840000     # ~84% of the 1M Opus 4.8 window (1M default since 2026-05-28).
                           # Was 169000 in the 200K era. ESTIMATE pending first 1M compaction.


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


def _status_path(cwd, transcript):
    sid = _sid_from_transcript(transcript)
    tail = re.sub(r"[^A-Za-z0-9]+", "_", os.path.basename(os.path.abspath(cwd)))[-24:]
    day = time.strftime("%Y%m%d")
    return os.path.join(STATUS_DIR, f"{day}_{tail}_{sid[:8]}.md")


def _state_path(sid):
    return os.path.join(STATE_DIR, sid + ".json")


def _analyze(transcript):
    """Return (real_tokens, turns, tool_calls, last_user_prompt)."""
    real_tokens = 0
    turns = 0
    tool_calls = 0
    last_user = ""
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
                t = r.get("type")
                m = r.get("message")
                if t == "user":
                    turns += 1
                    if isinstance(m, dict):
                        c = m.get("content")
                        if isinstance(c, str):
                            last_user = c[:160]
                        elif isinstance(c, list):
                            for blk in c:
                                if isinstance(blk, dict) and blk.get("type") == "text":
                                    last_user = str(blk.get("text", ""))[:160]
                if isinstance(m, dict):
                    u = m.get("usage")
                    if isinstance(u, dict):
                        tot = (u.get("input_tokens", 0)
                               + u.get("cache_read_input_tokens", 0)
                               + u.get("cache_creation_input_tokens", 0))
                        if tot > real_tokens:
                            real_tokens = tot
                    c = m.get("content")
                    if isinstance(c, list):
                        for blk in c:
                            if isinstance(blk, dict) and blk.get("type") == "tool_use":
                                tool_calls += 1
    except Exception:
        pass
    if real_tokens == 0:  # fallback: bytes/4
        try:
            real_tokens = os.path.getsize(transcript) // 4
        except Exception:
            real_tokens = 0
    return real_tokens, turns, tool_calls, last_user


def _read_state(sid):
    try:
        with open(_state_path(sid), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"last_level": 0}


def _write_state(sid, st):
    try:
        os.makedirs(STATE_DIR, exist_ok=True)
        with open(_state_path(sid), "w", encoding="utf-8") as f:
            json.dump(st, f)
    except Exception:
        pass


def _append(path, text):
    os.makedirs(STATUS_DIR, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(text)


def _stem_for(cwd, transcript):
    """Filename stem (no .md) of this session's status file -- the overseer's
    versioned handover/adviser files are named off the same stem."""
    return os.path.splitext(os.path.basename(_status_path(cwd, transcript)))[0]


def _launch_overseer(transcript, stem, level, cwd, extra=None):
    """Launch session_oversight.py DETACHED + HIDDEN (no terminal popup on
    Windows). `extra` (list) appends mode-specific args (answer mode passes
    ["answer", <question_file>]). Fails open: a launch error must never wedge
    the hook."""
    try:
        flags = 0
        si = None
        if os.name == "nt":
            # CREATE_NO_WINDOW (0x08000000) + DETACHED_PROCESS (0x00000008):
            # no console window ever appears, and it survives this hook exiting.
            flags = 0x08000000 | 0x00000008
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            si.wShowWindow = 0  # SW_HIDE
        cmd = [sys.executable, OVERSEER, transcript, stem, str(level), cwd]
        if extra:
            cmd.extend(extra)
        subprocess.Popen(
            cmd,
            creationflags=flags, startupinfo=si,
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL, close_fds=True,
        )
    except Exception:
        pass  # fail open -- never wedge the session


def _inject_pending_adviser(cwd, transcript):
    """If the previous background MILESTONE run left a fresh, not-yet-shown,
    NON-CLEAN adviser note, print it (-> injected into the live chat) and mark
    it shown. Returns True if something was printed. Fails open (returns False).

    SCOPE: this handles ONLY the unprompted milestone Adviser notes, which are
    still produced async/detached by session_oversight.run(). Triggered ("a'" /
    "adviser:") questions are now answered SYNCHRONOUSLY in the same turn (see
    _answer_adviser_sync) and never go through this pointer.

    KNOWN LIMITATION (one-turn-late injection for MILESTONE notes): a milestone
    note is shown on the hook fire AFTER it is written, because the Opus call
    that produces it runs detached and has not finished when the triggering fire
    returns. The LAST note written right before a compaction can be lost. Left
    as-is by design for milestone notes (blocking every milestone would freeze
    turns); the triggered question path is now synchronous so it is unaffected."""
    try:
        stem = _stem_for(cwd, transcript)
        ptr = os.path.join(STATE_DIR, stem + ".adviser_ptr.json")
        if not os.path.isfile(ptr):
            return False
        with open(ptr, encoding="utf-8") as f:
            info = json.load(f)
        if info.get("shown") or info.get("clean"):
            return False
        # Triggered-reply pointers are obsolete (answers are now synchronous);
        # ignore any stale one so it can never be surfaced a turn late.
        if info.get("reply"):
            return False
        ap = info.get("path")
        if not ap or not os.path.isfile(ap):
            return False
        with open(ap, encoding="utf-8") as f:
            note = f.read()
        print("%s **ADVISER NOTE** %s **ADVISER NOTE** %s"
              % (_ADV_DOT, note.strip(), _ADV_DOT))
        info["shown"] = True
        with open(ptr, "w", encoding="utf-8") as f:
            json.dump(info, f)
        return True
    except Exception:
        return False


# Prefixes that route a prompt to the Adviser. Both the full word and the
# short form "a'" work (case-insensitive). Longest first so "adviser:" is
# matched before any shorter prefix.
ADVISER_TRIGGERS = ("adviser:", "a'")

# One bright marker so the Adviser's block does not blend into the grey
# system-noise lines (Max glances over plain blocks) -- kept COMPACT: a single
# purple circle + bold label before and after, no banner (screen space matters).
# UTF-8 stdout (set in main) keeps it from crashing on Windows cp1252.
_ADV_DOT = "\U0001F7E3"            # purple circle


def _last_user_prompt_from_transcript(transcript):
    """Fallback when the hook stdin lacks a 'prompt' field: return the text of
    the latest user turn in the transcript. Fails open (returns '')."""
    last = ""
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
                if r.get("type") != "user":
                    continue
                m = r.get("message")
                if not isinstance(m, dict):
                    continue
                c = m.get("content")
                if isinstance(c, str):
                    last = c
                elif isinstance(c, list):
                    for blk in c:
                        if isinstance(blk, dict) and blk.get("type") == "text":
                            last = str(blk.get("text", ""))
    except Exception:
        pass
    return last


def _adviser_question(prompt_text):
    """If `prompt_text` (first non-space text) begins with any Adviser trigger
    ('adviser:' or the short form "a'"), case-insensitive, return the question
    (text after the trigger, stripped). Otherwise return None."""
    if not isinstance(prompt_text, str):
        return None
    stripped = prompt_text.lstrip()
    low = stripped.lower()
    for trig in ADVISER_TRIGGERS:
        if low.startswith(trig):
            return stripped[len(trig):].strip()
    return None


# Hard ceiling on the synchronous Adviser call so the hook can never freeze
# Max's turn waiting on a hung API. On timeout we print a graceful fallback.
ADVISER_SYNC_TIMEOUT = 20   # seconds


def _clean_adviser_body(body):
    """Strip any self-labeling the model emitted so we wrap EXACTLY once. The
    model sometimes prepends 'ADVISER:' or wraps its own text in '**ADVISER**'
    markers / the purple dot; remove all of those so the single wrap below is
    the only marker pair Max sees."""
    if not body:
        return ""
    b = body.strip()
    # Drop any literal markers the model emitted anywhere in the text.
    b = b.replace("**ADVISER**", " ").replace(_ADV_DOT, " ")
    b = b.strip()
    # Drop a leading 'ADVISER:' label (case-insensitive), possibly repeated.
    low = b.lower()
    while low.startswith("adviser:"):
        b = b[len("adviser:"):].strip()
        low = b.lower()
    # Collapse the runs of spaces a stripped inline marker may have left.
    b = re.sub(r"[ \t]{2,}", " ", b).strip()
    return b


def _wrap_adviser(body):
    """Wrap the cleaned body in EXACTLY one compact marker pair, matching the
    existing style: purple dot + bold ADVISER label before and after."""
    return "%s **ADVISER** %s **ADVISER** %s" % (_ADV_DOT, body, _ADV_DOT)


def _answer_adviser_sync(cwd, transcript, question):
    """Answer Max's Adviser question SYNCHRONOUSLY and print it in THIS hook
    fire (so the answer lands in the same turn -- no nudge, no next-turn
    surfacing). Hard-bounded by ADVISER_SYNC_TIMEOUT; on timeout or ANY error
    prints a one-line graceful fallback. FAILS OPEN -- never raises."""
    try:
        sys.path.insert(0, os.path.dirname(OVERSEER))
        from session_oversight import compute_answer
        stem = _stem_for(cwd, transcript)
        result = {}

        def _work():
            try:
                result["body"] = compute_answer(transcript, stem, cwd, question)
            except Exception as e:  # noqa
                result["err"] = e

        import threading, time
        th = threading.Thread(target=_work, daemon=True)
        t0 = time.time()
        th.start()
        th.join(ADVISER_SYNC_TIMEOUT)
        if th.is_alive() or "body" not in result:
            # Timed out or failed inside the worker -- graceful fallback line.
            print(_wrap_adviser("unreachable right now -- ask again"))
            return
        elapsed = int(round(time.time() - t0))
        body = _clean_adviser_body(result.get("body") or "")
        if not body:
            print(_wrap_adviser("unreachable right now -- ask again"))
            return
        body = "%s  [%ds]" % (body, elapsed)
        print(_wrap_adviser(body))
    except Exception:
        try:
            print(_wrap_adviser("unreachable right now -- ask again"))
        except Exception:
            pass


def cmd_hook():
    cwd = os.getcwd()
    transcript = None
    prompt_text = None
    try:
        data = json.load(sys.stdin)
        cwd = data.get("cwd") or cwd
        transcript = data.get("transcript_path") or None
        # UserPromptSubmit provides the submitted text; field name is 'prompt'.
        pt = data.get("prompt")
        if isinstance(pt, str):
            prompt_text = pt
    except Exception:
        pass
    if not transcript:
        transcript = _find_transcript(cwd)
    if not transcript or not os.path.isfile(transcript):
        return 0

    # If stdin didn't carry the prompt, recover it from the transcript tail.
    if prompt_text is None:
        prompt_text = _last_user_prompt_from_transcript(transcript)

    # BEFORE anything else: surface any adviser note/reply the last background
    # run left. Advice/answers land one turn after they are written -- by design.
    _inject_pending_adviser(cwd, transcript)

    # TWO-WAY CHANNEL: did Max address the Adviser directly ("a'" / "adviser:")?
    question = _adviser_question(prompt_text)
    if question is not None:
        # Answer SYNCHRONOUSLY, in THIS same turn: call the Adviser inline
        # (blocking, ~8-15s, hard-capped at ADVISER_SYNC_TIMEOUT) and print its
        # answer to stdout right here. No background runner, no next-turn
        # surfacing, no nudge. The answer is wrapped exactly once.
        if question:
            _answer_adviser_sync(cwd, transcript, question)
        # Tell the Assistant this line was for the Adviser -- do not hijack it.
        print(
            "=== ADDRESSED TO THE ADVISER (do not answer this yourself) ===\n"
            "Max's last line was a question for the ADVISER (the independent "
            "overseer), not for you, the Assistant. The Adviser's answer was "
            "just printed above, in its own purple ADVISER block. Do NOT answer "
            "Max's question yourself. You may briefly acknowledge the Adviser "
            "replied, then continue any other work.\n"
            "=== end adviser routing note ===")
        # A turn spent talking to the Adviser is NOT a milestone event; skip the
        # token-milestone machinery entirely so we don't also fire a review.
        return 0

    real_tokens, turns, tool_calls, last_user = _analyze(transcript)
    level = real_tokens // MILESTONE_TOKENS
    sid = _sid_from_transcript(transcript)
    st = _read_state(sid)
    if level <= st.get("last_level", 0):
        return 0  # no new milestone crossed -> stay silent

    path = _status_path(cwd, transcript)
    pct = int(100 * real_tokens / COMPACT_CLIFF)
    # LAYER 1 - guaranteed mechanical snapshot
    if not os.path.isfile(path):
        _append(path, f"# Session status log - {sid}\n# cwd: {cwd}\n# auto-dumped every ~{MILESTONE_TOKENS//1000}K tokens; compaction ~{COMPACT_CLIFF//1000}K\n\n")
    _append(path,
            f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] AUTO milestone {level} "
            f"(~{real_tokens//1000}K tok, ~{pct}% full) | turns={turns} "
            f"tool_calls={tool_calls} | last_user: {last_user!r}\n")
    st["last_level"] = level
    _write_state(sid, st)

    # LAYER 3 - launch the DETACHED, HIDDEN overseer (Scribe + Adviser, full
    # Opus, reads the whole transcript). Returns instantly; results land on disk
    # and the adviser note is injected on the NEXT hook fire.
    _launch_overseer(transcript, _stem_for(cwd, transcript), level, cwd)

    # LAYER 2 - injected nudge (UserPromptSubmit stdout -> model context, no wedge)
    print(
        "=== a nice moment to jot status ===\n"
        f"You're about ~{real_tokens//1000}K tokens in (~{pct}% of the way to a context "
        f"refresh around ~{COMPACT_CLIFF//1000}K, when older context gets summarized). All "
        "is well -- a snapshot was auto-saved. When you wrap your current step, a short human "
        "status helps a later session continue smoothly:\n"
        '  python C:/claude_base/compaction_kb/scripts/session_status.py report "DID ... | STATE ... | NEXT ..."\n'
        "=== end ===")
    return 0


def cmd_report(text):
    cwd = os.getcwd()
    transcript = _find_transcript(cwd)
    if not transcript:
        print("session_status: no transcript found for this cwd (nothing written)")
        return 0
    path = _status_path(cwd, transcript)
    if not os.path.isfile(path):
        _append(path, f"# Session status log - {_sid_from_transcript(transcript)}\n# cwd: {cwd}\n\n")
    _append(path, f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] REPORT: {text}\n")
    print(f"session_status: report appended -> {path}")
    return 0


def cmd_read():
    cwd = os.getcwd()
    transcript = _find_transcript(cwd)
    if not transcript:
        print("session_status: no transcript found for this cwd")
        return 0
    path = _status_path(cwd, transcript)
    if not os.path.isfile(path):
        print(f"session_status: no status file yet at {path}")
        return 0
    with open(path, encoding="utf-8") as f:
        sys.stdout.write(f.read())
    return 0


def cmd_selftest():
    """Prove the SYNCHRONOUS Adviser answer formatting: the model body is
    stripped of any self-emitted markers ('ADVISER:', '**ADVISER**', purple
    dot) and wrapped in EXACTLY one marker pair (Max saw a double-wrap bug).
    Pure string logic -- no API call, no disk, no session state touched."""
    ok = True

    def _check(name, raw, want_body):
        nonlocal ok
        wrapped = _wrap_adviser(_clean_adviser_body(raw))
        n_pairs = wrapped.count("**ADVISER**")
        n_dots = wrapped.count(_ADV_DOT)
        body_ok = (want_body in wrapped) and not wrapped.lower().count("adviser: adviser")
        single = (n_pairs == 2 and n_dots == 2)
        if not (single and body_ok):
            print("FAIL [%s]: pairs=%d dots=%d -> %r" % (name, n_pairs, n_dots, wrapped))
            ok = False
        else:
            print("OK   [%s]: single wrap, body intact" % name)

    # 1. Plain body: wrapped once.
    _check("plain", "Yes, scene 9 is the right input.", "Yes, scene 9 is the right input.")
    # 2. Model prefixed its own 'ADVISER:' label -> stripped, wrapped once.
    _check("self-label", "ADVISER: Watch the housekeeping mess.", "Watch the housekeeping mess.")
    # 3. Model emitted its own **ADVISER** markers (the double-wrap bug).
    _check("self-markers",
           "%s **ADVISER** You are drifting from the task. **ADVISER** %s"
           % (_ADV_DOT, _ADV_DOT),
           "You are drifting from the task.")
    # 4. Combination of both.
    _check("combo",
           "ADVISER: %s **ADVISER** Stop and commit first. **ADVISER**" % _ADV_DOT,
           "Stop and commit first.")
    print("SELFTEST:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    # Hook stdout carries emoji markers now; force UTF-8 so Windows cp1252 can't
    # raise UnicodeEncodeError and silently kill the injection. Fails open.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    args = sys.argv[1:]
    if not args:
        print("usage: session_status.py [--hook | report \"...\" | read | selftest]")
        return 0
    if args[0] == "--hook":
        return cmd_hook()
    if args[0] == "report":
        return cmd_report(args[1] if len(args) > 1 else "")
    if args[0] == "read":
        return cmd_read()
    if args[0] == "selftest":
        return cmd_selftest()
    print("usage: session_status.py [--hook | report \"...\" | read | selftest]")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main() or 0)
    except Exception as e:
        sys.stderr.write(f"session_status error (ignored): {e}\n")
        sys.exit(0)
