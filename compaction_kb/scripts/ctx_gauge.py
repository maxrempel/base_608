#!/usr/bin/env python3
"""
ctx_gauge.py - tiny ALWAYS-ON context fill readout (Max, 2026-06-12).

Max: "I have little clue what is the size of the context and % to compaction."
This prints ONE compact line so the answer is always on screen: how full the
context is and how close to the ~840K context-refresh point (older context is summarized there).

It is intentionally separate from session_status.py (the Scribe/Adviser milestone
machinery): this is just a gauge, no Opus call, no nudge, no state needed beyond
remembering the last band so we can mark when a new ~10% band is crossed.

Cadence: prints every turn (one short line), and flags when a new 10% band is
crossed. To switch to "only on a new 10% band", set BAND_ONLY = True below.

Token source: each assistant line in the transcript .jsonl carries message.usage
(input + cache_read + cache_creation = the real prompt size). Latest = current
fill. Falls back to bytes/4.

Fails open: a broken gauge must never wedge or slow a session.
"""
import sys, os, json, glob

PROJECTS = os.path.expanduser(r"~\.claude\projects")
STATE_DIR = r"C:\claude_base\compaction_kb\.gauge_state"
COMPACT_CLIFF = 230000   # 2026-07-26: now an EXACT figure, not an estimate. Max pinned
                         # "model": "opus[1m]" plus CLAUDE_CODE_AUTO_COMPACT_WINDOW=230000
                         # in ~/.claude/settings.json, so auto-compaction fires against a
                         # 230K effective window. Keep this in sync with that env value.
                         # History: 840000 (guessed 1M-era cliff, showed a wildly
                         # optimistic gauge), 169000 in the 200K era.
BAR_W = 20               # width of the ASCII fill bar
BAND_ONLY = False        # 2026-06-12 Max: "switch to every message for testing"
                         # (was True = band-only; flip back once verified visible)


def _project_name_for_cwd(cwd):
    norm = os.path.abspath(cwd)
    return "".join("-" if ch in ":\\/._" else ch for ch in norm)


def _find_transcript(cwd):
    pdir = os.path.join(PROJECTS, _project_name_for_cwd(cwd))
    if not os.path.isdir(pdir):
        return None
    cands = glob.glob(os.path.join(pdir, "*.jsonl"))
    return max(cands, key=os.path.getmtime) if cands else None


def _sid(transcript):
    return os.path.splitext(os.path.basename(transcript))[0]


def _real_tokens(transcript):
    # CURRENT fill = the usage on the LATEST assistant line, NOT the peak. Using
    # the peak was a bug: after a compaction the context drops but the old high
    # lines stay in the .jsonl, so a max-reading gauge froze at the pre-compaction
    # number and (band-only) never re-printed. The most recent usage is the real
    # live context size.
    best = 0
    try:
        with open(transcript, "rb") as fh:
            for bl in fh:
                s = bl.strip()
                if not s or b"usage" not in s:
                    continue
                try:
                    r = json.loads(s.decode("utf-8", "replace"))
                except Exception:
                    continue
                m = r.get("message")
                if isinstance(m, dict):
                    u = m.get("usage")
                    if isinstance(u, dict):
                        tot = (u.get("input_tokens", 0)
                               + u.get("cache_read_input_tokens", 0)
                               + u.get("cache_creation_input_tokens", 0))
                        if tot > 0:
                            best = tot   # keep overwriting -> ends on the latest
    except Exception:
        pass
    if best == 0:
        try:
            best = os.path.getsize(transcript) // 4
        except Exception:
            best = 0
    return best


def _state_path(sid):
    return os.path.join(STATE_DIR, sid + ".json")


def _read_band(sid):
    try:
        with open(_state_path(sid), encoding="utf-8") as f:
            return int(json.load(f).get("band", -1))
    except Exception:
        return -1


def _write_band(sid, band):
    try:
        os.makedirs(STATE_DIR, exist_ok=True)
        with open(_state_path(sid), "w", encoding="utf-8") as f:
            json.dump({"band": band}, f)
    except Exception:
        pass


def _bar(pct):
    filled = max(0, min(BAR_W, round(BAR_W * pct / 100)))
    return "[" + "#" * filled + "-" * (BAR_W - filled) + "]"


def cmd_hook():
    cwd = os.getcwd()
    transcript = None
    try:
        data = json.load(sys.stdin)
        cwd = data.get("cwd") or cwd
        transcript = data.get("transcript_path") or None
    except Exception:
        pass
    if not transcript:
        transcript = _find_transcript(cwd)
    if not transcript or not os.path.isfile(transcript):
        return 0

    tok = _real_tokens(transcript)
    pct = int(round(100 * tok / COMPACT_CLIFF))
    sid = _sid(transcript)
    band = pct // 10
    last_band = _read_band(sid)
    new_band = band > last_band
    if new_band:
        _write_band(sid, band)
    if BAND_ONLY and not new_band:
        return 0

    mark = "  (passed %d%%)" % (band * 10) if new_band else ""
    # One compact line. Plain ASCII bar so Max can read fill at a glance.
    print("CONTEXT GAUGE: ~%dK / %dK tokens | %d%% full %s%s"
          % (tok // 1000, COMPACT_CLIFF // 1000, pct, _bar(pct), mark))
    return 0


def _model_guard(data):
    """Watchdog: Max never looks at the model name in the corner, and the app can
    silently drop Opus -> Sonnet (opusplan execution, overload fallback, etc.),
    wrecking his work. This returns a LOUD prefix for the status bar, and on any
    transition INTO a non-Opus model it fires a screen-flash + voice alarm ONCE
    (debounced per session, so it doesn't spam every render). Default expected
    model = Opus. Anything else = alarm."""
    m = data.get("model") or {}
    mid = (m.get("id") or "").lower()
    disp = m.get("display_name") or m.get("id") or "?"
    if not mid:
        return ""  # no model info in payload -> stay quiet
    is_opus = "opus" in mid
    sid = data.get("session_id") or "nosid"
    statef = os.path.join(STATE_DIR, "model_" + "".join(c if c.isalnum() else "_" for c in sid) + ".json")
    prev = None
    try:
        with open(statef) as f:
            prev = json.load(f).get("mid")
    except Exception:
        pass
    if prev != mid:
        try:
            os.makedirs(STATE_DIR, exist_ok=True)
            with open(statef, "w") as f:
                json.dump({"mid": mid}, f)
        except Exception:
            pass
        # Scream only on a genuine change into a non-Opus model.
        if not is_opus and prev is not None:
            try:
                import subprocess
                subprocess.Popen(
                    ["pythonw", r"C:/claude_base/tools/attention/attention.py",
                     "--msg", "MODEL DOWNGRADE. You are now on %s, not Opus. "
                              "Type slash model opus to fix it." % disp,
                     "--color", "amber",   # soft yellow window, as Max asked
                     "--seconds", "0",     # stay up until Max clicks/keys it away
                     "--repeat", "3"],
                    creationflags=0x08000000)  # CREATE_NO_WINDOW
            except Exception:
                pass
    if is_opus:
        return "%s | " % disp
    return "!!! NOT OPUS: %s -> run /model opus !!! | " % disp


def cmd_statusline():
    """Claude Code statusLine command: stdin = session JSON, stdout = ONE compact
    line shown PERSISTENTLY on Max's screen (the bottom bar). Unlike the --hook
    path (which prints into the model's context, invisible to Max), this is what
    MAX actually sees every turn. Compact so it fits the bar."""
    cwd = os.getcwd()
    transcript = None
    data = {}
    try:
        data = json.load(sys.stdin)
        cwd = (data.get("workspace") or {}).get("current_dir") or data.get("cwd") or cwd
        transcript = data.get("transcript_path") or None
    except Exception:
        pass
    guard = ""
    try:
        guard = _model_guard(data)
    except Exception:
        pass
    if not transcript:
        transcript = _find_transcript(cwd)
    if not transcript or not os.path.isfile(transcript):
        print("%sctx ?" % guard)
        return 0
    tok = _real_tokens(transcript)
    pct = int(round(100 * tok / COMPACT_CLIFF))
    # Compact: "Opus 4.8 | ctx 60% [############--------] 101K/840K full"
    print("%sctx %d%% %s %dK/%dK full"
          % (guard, pct, _bar(pct), tok // 1000, COMPACT_CLIFF // 1000))
    return 0


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    args = sys.argv[1:]
    if args and args[0] == "--hook":
        return cmd_hook()
    if args and args[0] == "--statusline":
        return cmd_statusline()
    # Manual readout for the current cwd.
    cwd = os.getcwd()
    transcript = _find_transcript(cwd)
    if not transcript:
        print("ctx_gauge: no transcript for this cwd")
        return 0
    tok = _real_tokens(transcript)
    pct = int(round(100 * tok / COMPACT_CLIFF))
    print("CONTEXT GAUGE: ~%dK / %dK tokens | %d%% full %s"
          % (tok // 1000, COMPACT_CLIFF // 1000, pct, _bar(pct)))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main() or 0)
    except Exception as e:
        sys.stderr.write(f"ctx_gauge error (ignored): {e}\n")
        sys.exit(0)
