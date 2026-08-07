#!/usr/bin/env python
"""
attention.py - local "I need a human" alarm for a Codex or Claude task.

Flashes a big, standardized message across EVERY monitor and speaks the
task name + number aloud so Max can find which of his many open tasks
wants attention - e.g. a captcha or any human-in-the-loop step. Sibling of the
Telegram/email channels; this one is for the human sitting at the machine.

Audio is forced to the LAPTOP BUILT-IN SPEAKERS at a moderate default volume
(42 percent, 15 percent quieter than the old 50), bypassing the Windows default
output device (so it is heard even when a headset is the default). If the
built-in device cannot be found, the alert plays on EVERY available output
device so it is heard on at least one speaker. Voice uses a high-quality
Microsoft neural voice when online and falls back to the offline Windows SAPI
synthesizer if synthesis is unavailable. The overlay is shown BEFORE the voice
starts, stays on top of every window, and any key or mouse button anywhere
dismisses it and silences the voice without stealing keyboard focus.

Usage (call via the Bash tool, forward slashes; launch with pythonw = no console):
  pythonw C:/claude_base/tools/attention/attention.py \
      --session "b7 grok-signup" --number 7 \
      --msg "Captcha to solve in the Playwright window"

Flags:
  --session   short label of the calling task (bcast id / name)
  --number    a number Max can match to a task (optional)
  --msg       the standardized request line shown big + spoken
  --seconds   fixed flash duration; default 0 stays through the spoken alert
  --repeat    how many times to speak the announcement (default 3)
  --device    output-device name substring (default the built-in Realtek speakers)
  --volume    target speaker volume 0-100 (default 42)
  --tts-voice Microsoft neural voice name (default en-GB-SoniaNeural)
  --no-voice  screen only, no TTS
  --no-screen voice only, no overlay
  --color     overlay background: amber (default) | red | green

Dismiss: click any overlay or press ANY key / mouse button anywhere -> all
overlays close, voice stops. The overlay never steals keyboard focus.
"""
import argparse
import ctypes
import json
import os
import subprocess
import sys
import tempfile
import threading
import warnings

warnings.filterwarnings("ignore")

DEFAULT_DEVICE = "Realtek"  # built-in laptop speakers
DEFAULT_TTS_VOICE = "en-GB-SoniaNeural"
ENDPOINT_HELPER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "audio_endpoint_helper.py"
)
BCAST_STATE_DIR = r"C:\claude_base\branch_bulletin\state"  # session-id by worktree
FLEETCOMM_DIR = r"C:\claude_base\tools\fleetcomm"  # transport for remote alarms


def _endpoint_helper(*args):
    """Run fragile pycaw/comtypes work outside the alert process."""
    result = subprocess.run(
        [sys.executable, ENDPOINT_HELPER, *args],
        capture_output=True,
        text=True,
        creationflags=0x08000000,
        timeout=15,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown error"
        raise RuntimeError(detail)
    payload = json.loads(result.stdout)
    if not payload.get("ok"):
        raise RuntimeError(payload.get("error", "endpoint helper failed"))
    return payload["result"]


def _device_is_muted(name_substr):
    """Return True if the target speaker endpoint OR the system default playback
    device is muted. If Max muted Pine to sleep, the alarm MUST stay silent
    instead of force-unmuting. Fail-open to False (audible) only if we truly
    cannot read the mute state, so a genuine emergency alarm is never lost.
    Set MOMA env/attention override with MUTE respected by default."""
    try:
        state = _endpoint_helper("inspect", "--device", name_substr)
        return bool(state["muted"] or state["default_muted"])
    except Exception as e:
        sys.stderr.write(f"[attention] mute check skipped: {e}\n")
    return False


def _fleetcomm():
    """Lazy import of the fleetcomm transport (machine_name / canon_machine)."""
    if FLEETCOMM_DIR not in sys.path:
        sys.path.insert(0, FLEETCOMM_DIR)
    import fleetcomm
    return fleetcomm


def _dispatch_remote(a):
    """--to a DIFFERENT machine: send the alarm there via fleetcomm instead of
    firing locally. A standalone poller on that machine flashes + speaks it."""
    import subprocess
    fc = _fleetcomm()
    target = fc.canon_machine(a.to)
    sess = _resolve_session(a.session)
    cmd = [sys.executable, os.path.join(FLEETCOMM_DIR, "fleetcomm.py"),
           "alarm", target, "--msg", a.msg, "--color", a.color,
           "--repeat", str(a.repeat), "--session", sess]
    if a.number:
        cmd += ["--number", str(a.number)]
    print(f"[attention] sending remote alarm to {target} (from {fc.machine_name()}/{sess}) ...")
    subprocess.run(cmd)


def _resolve_session(given):
    """If the caller passed a real --session, use it. Otherwise auto-identify
    the calling task from its worktree (the same key bcast uses) so the
    alarm never uses an anonymous product-specific label."""
    if given and given not in ("a Claude session", "a Codex task"):
        return given
    cwd = os.path.abspath(os.getcwd())
    # 1) bcast id whose recorded cwd matches this worktree
    try:
        import glob
        import json
        for fn in glob.glob(os.path.join(BCAST_STATE_DIR, "*.json")):
            try:
                with open(fn, "r", encoding="utf-8") as f:
                    st = json.load(f)
            except Exception:
                continue
            c = st.get("cwd")
            if c and os.path.abspath(c) == cwd and st.get("id"):
                return str(st["id"])
    except Exception:
        pass
    # 2) fall back to the worktree folder name (still tells Max where it is)
    base = os.path.basename(cwd.rstrip("\\/"))
    return base or "unknown session"


# --- session deep links: codex://threads/<id> and claude://resume?session=<id>

def _normalize_cwd(path):
    """Fold the verbatim-prefixed cwd the Codex DB stores into a plain path."""
    p = (path or "").replace("\\\\?\\", "")
    return p.rstrip("\\/").lower()


def _resolve_task_link(session, cwd):
    """Return a clickable deep link to the session that fired this alert, or
    None if it cannot be identified. Codex tasks resolve through the threads
    table by working directory (newest match wins), Claude Code sessions
    through the newest transcript in the matching project folder."""
    try:
        norm = _normalize_cwd(cwd)

        # Codex: state_5.sqlite threads table, match by cwd, newest first.
        db = os.path.join(os.path.expanduser("~"), ".codex", "state_5.sqlite")
        if os.path.exists(db):
            import sqlite3
            con = sqlite3.connect(db, timeout=5)
            try:
                rows = con.execute(
                    "SELECT id, cwd, title, updated_at_ms FROM threads "
                    "WHERE archived = 0"
                ).fetchall()
            finally:
                con.close()
            by_cwd = [r for r in rows if _normalize_cwd(r[1]) == norm]
            if by_cwd:
                by_cwd.sort(key=lambda r: r[3] or 0, reverse=True)
                return f"codex://threads/{by_cwd[0][0]}"
            # Fallback: session label ("Codex: <title>") against stored titles.
            label = (session or "").replace("Codex:", "", 1).strip().lower()
            if label:
                titled = [r for r in rows
                          if (r[2] or "").lower() == label
                          or label in (r[2] or "").lower()]
                if titled:
                    titled.sort(key=lambda r: r[3] or 0, reverse=True)
                    return f"codex://threads/{titled[0][0]}"

        # Claude Code: ~/.claude/projects/<cwd-encoded>/<session-id>.jsonl
        # Claude sanitizes the cwd to alphanumerics joined by dashes.
        import glob
        import re
        raw = (cwd or "").replace("\\\\?\\", "")
        enc = re.sub(r"[^A-Za-z0-9]", "-", raw)
        folder = os.path.join(os.path.expanduser("~"), ".claude", "projects", enc)
        files = sorted(glob.glob(os.path.join(folder, "*.jsonl")),
                       key=os.path.getmtime, reverse=True)
        if files:
            sid = os.path.splitext(os.path.basename(files[0]))[0]
            return f"claude://resume?session={sid}"
    except Exception as e:
        sys.stderr.write(f"[attention] task link resolution skipped: {e}\n")
    return None


def _open_task_link(url):
    """Open a session deep link without showing a console."""
    try:
        subprocess.run(["powershell", "-NoProfile", "-NonInteractive",
                        "-Command", f"Start-Process '{url}'"],
                       creationflags=0x08000000, timeout=20)
    except Exception as e:
        sys.stderr.write(f"[attention] could not open task link: {e}\n")


def _ensure_history_bar():
    """Start the persistent bottom history bar (single instance, no console)."""
    try:
        exe = sys.executable
        base, name = os.path.split(exe)
        if name.lower() == "python.exe":
            cand = os.path.join(base, "pythonw.exe")
            if os.path.exists(cand):
                exe = cand
        subprocess.Popen(
            [exe, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "attention_history_bar.py")],
            creationflags=0x08000000,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            close_fds=True,
        )
    except Exception as e:
        sys.stderr.write(f"[attention] history bar launch skipped: {e}\n")


# --- monitor geometry via Win32 (no pip deps) -----------------------------

def _monitors():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

    rects = []

    class RECT(ctypes.Structure):
        _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long),
                    ("right", ctypes.c_long), ("bottom", ctypes.c_long)]

    MonitorEnumProc = ctypes.WINFUNCTYPE(
        ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong,
        ctypes.POINTER(RECT), ctypes.c_double)

    def _cb(hmon, hdc, lprc, data):
        r = lprc.contents
        rects.append((r.left, r.top, r.right - r.left, r.bottom - r.top))
        return 1

    ctypes.windll.user32.EnumDisplayMonitors(0, 0, MonitorEnumProc(_cb), 0)
    if not rects:
        u = ctypes.windll.user32
        rects.append((0, 0, u.GetSystemMetrics(0), u.GetSystemMetrics(1)))
    return rects


# --- force the built-in speakers to full volume ---------------------------

def _set_device_volume(name_substr, scalar):
    """Set the named output endpoint to `scalar` (0..1) and unmute.
    Returns (restore_callable) or None. Does NOT change the system default."""
    try:
        state = _endpoint_helper("inspect", "--device", name_substr)
        old = float(state["volume"])
        old_mute = bool(state["muted"])
        _endpoint_helper(
            "set", "--device", name_substr, "--volume",
            str(max(0.0, min(1.0, scalar))), "--muted", "false"
        )

        def restore():
            try:
                _endpoint_helper(
                    "set", "--device", name_substr, "--volume", str(old),
                    "--muted", str(old_mute).lower()
                )
            except Exception:
                pass
        return restore
    except Exception as e:
        sys.stderr.write(f"[attention] volume set skipped: {e}\n")
        return None


# --- voice: neural TTS (SAPI fallback), then chosen-device playback -------

def _synth_sapi_wav(text):
    safe = text.replace("'", "''")
    fd, path = tempfile.mkstemp(suffix=".wav", prefix="attn_")
    os.close(fd)
    ps = (
        "Add-Type -AssemblyName System.Speech;"
        "$s=New-Object System.Speech.Synthesis.SpeechSynthesizer;"
        "$s.Rate=0;"
        f"$s.SetOutputToWaveFile('{path}');"
        f"$s.Speak('{safe}');"
        "$s.Dispose();"
    )
    import subprocess
    subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
                   creationflags=0x08000000, timeout=30)
    return path if os.path.exists(path) and os.path.getsize(path) > 0 else None


def _synth_neural(text, voice):
    """Synthesize with Microsoft's high-quality neural service via edge-tts."""
    fd, path = tempfile.mkstemp(suffix=".mp3", prefix="attn_neural_")
    os.close(fd)
    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "edge_tts",
                "--voice",
                voice,
                "--text",
                text,
                "--write-media",
                path,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=0x08000000,
            timeout=30,
        )
        if result.returncode == 0 and os.path.getsize(path) > 0:
            return path
        detail = (result.stderr or "").strip()
        if detail:
            sys.stderr.write(f"[attention] neural TTS unavailable: {detail}\n")
    except Exception as e:
        sys.stderr.write(f"[attention] neural TTS unavailable: {e}\n")
    try:
        os.remove(path)
    except Exception:
        pass
    return None


def _synth_audio(text, voice):
    return _synth_neural(text, voice) or _synth_sapi_wav(text)


def _find_output_devices(name_substr):
    """Return output device ids to play on. Prefer the named built-in device
    (laptop speakers). If it is absent, return EVERY output device so the alert
    is heard on at least one speaker instead of silently using the default."""
    import sounddevice as sd
    sub = name_substr.lower()
    cands = []
    for i, d in enumerate(sd.query_devices()):
        if d["max_output_channels"] > 0 and sub in d["name"].lower():
            cands.append((i, d["name"]))
    if cands:
        # prefer a "Speakers (...)" entry over Headphones/Line
        for i, n in cands:
            if "speaker" in n.lower():
                return [(i, n)]
        return cands
    all_out = [(i, d["name"]) for i, d in enumerate(sd.query_devices())
               if d["max_output_channels"] > 0]
    return all_out


def _play_voice(text, device_substr, repeat, stop_event, tts_voice):
    audio_path = _synth_audio(text, tts_voice)
    if not audio_path:
        sys.stderr.write("[attention] TTS synthesis failed\n")
        return "failed"
    try:
        import time

        import numpy as np
        import soundfile as sf
        import sounddevice as sd
        data, fs = sf.read(audio_path, dtype="float32")
        peak = float(np.max(np.abs(data))) if data.size else 0.0
        if peak > 0:
            data = data * (0.99 / peak)  # peak-normalize to near full scale
        devs = _find_output_devices(device_substr)
        if not devs:
            sys.stderr.write(
                f"[attention] no output device found for '{device_substr}'\n")
        for _ in range(max(1, repeat)):
            if stop_event.is_set():
                break
            if devs:
                for dev, _name in devs:
                    sd.play(data, fs, device=dev)
            else:
                sd.play(data, fs)
            # Responsive wait: poll the stop flag so a click KILLS the sound
            # immediately (within ~50ms) instead of finishing the utterance.
            while True:
                if stop_event.is_set():
                    sd.stop()
                    break
                try:
                    if not sd.get_stream().active:
                        break  # this utterance finished naturally
                except Exception:
                    break
                time.sleep(0.05)
            if stop_event.is_set():
                break
        return "dismissed" if stop_event.is_set() else "played"
    except Exception as e:
        sys.stderr.write(f"[attention] playback error: {e}\n")
        return "failed"
    finally:
        try:
            os.remove(audio_path)
        except Exception:
            pass


# --- global input hooks: ANY key or mouse button anywhere dismisses ---------

def _install_dismiss_hooks(close):
    """Install low-level keyboard + mouse hooks so any key press or mouse
    button anywhere closes the alert and silences the voice. The overlay keeps
    WS_EX_NOACTIVATE, so focus stays with the app Max is using; the hooks see
    the input anyway. Returns a list of (handle, callback) kept alive for the
    overlay's lifetime. Fail-open: if hooks cannot install, the alert still
    works via its own click/key bindings."""
    try:
        import ctypes
        from ctypes import wintypes

        user32 = ctypes.windll.user32
        WH_KEYBOARD_LL = 13
        WH_MOUSE_LL = 14
        WM_KEYDOWN = 0x0100
        WM_SYSKEYDOWN = 0x0104
        MOUSE_DOWN = (0x0201, 0x0204, 0x0207, 0x020B)  # L/R/M/X down

        HookProc = ctypes.WINFUNCTYPE(
            wintypes.LPARAM, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)
        # Declare argtypes explicitly: on 64-bit Windows, LPARAM is 64-bit
        # and an untyped CallNextHookEx call would overflow (and swallow the
        # dismissed key/mouse event) because ctypes would default to c_int.
        user32.CallNextHookEx.argtypes = [
            wintypes.HHOOK, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM]
        user32.CallNextHookEx.restype = wintypes.LPARAM

        def _make(kind, triggers):
            @HookProc
            def _proc(code, wparam, lparam):
                if code >= 0 and wparam in triggers:
                    close()
                try:
                    return user32.CallNextHookEx(None, code, wparam, lparam)
                except Exception:
                    return 0  # never let a hook failure eat the input

            handle = user32.SetWindowsHookExW(
                kind, _proc, None, 0)
            if not handle:
                raise ctypes.WinError()
            return handle, _proc

        kept = []
        kept.append(_make(WH_KEYBOARD_LL, (WM_KEYDOWN, WM_SYSKEYDOWN)))
        kept.append(_make(WH_MOUSE_LL, MOUSE_DOWN))
        return kept
    except Exception as e:
        sys.stderr.write(f"[attention] global dismiss hooks unavailable: {e}\n")
        return []


# --- big overlay on every monitor -----------------------------------------

def _make_no_focus(win):
    """Apply WS_EX_NOACTIVATE so the window never steals keyboard focus."""
    try:
        GA_ROOT = 2
        GWL_EXSTYLE = -20
        WS_EX_NOACTIVATE = 0x08000000
        WS_EX_TOOLWINDOW = 0x00000080
        WS_EX_TOPMOST = 0x00000008
        u = ctypes.windll.user32
        hwnd = u.GetAncestor(win.winfo_id(), GA_ROOT)
        ex = u.GetWindowLongW(hwnd, GWL_EXSTYLE)
        u.SetWindowLongW(hwnd, GWL_EXSTYLE,
                         ex | WS_EX_NOACTIVATE | WS_EX_TOOLWINDOW | WS_EX_TOPMOST)
        # HWND_TOPMOST=-1, SWP_NOMOVE|NOSIZE|NOACTIVATE|SHOWWINDOW|FRAMECHANGED
        u.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0002 | 0x0001 | 0x0010 | 0x0040 | 0x0020)
    except Exception:
        pass


def _show_overlay(title, body, color, seconds, stop_event, voice_done=None,
                  on_visible=None, on_teardown=None, link=None):
    import tkinter as tk
    import gc

    # amber is the default - a soft PASTEL light yellow (low saturation, very
    # readable with black text); red/green stay strong for genuine alerts.
    bg = {"amber": "#FFFAD6", "red": "#D32F2F", "green": "#2E7D32"}.get(color, "#FFFAD6")
    fg = "#FFFFFF" if color in ("red", "green") else "#000000"

    root = tk.Tk()
    root.withdraw()
    wins = []

    def close(*_):
        # explicit user dismiss -> also stop the voice
        stop_event.set()
        try:
            root.quit()
        except Exception:
            pass

    def timer_close():
        # auto-dismiss the toast but DO NOT cut the voice off
        try:
            root.quit()
        except Exception:
            pass

    FONT = "Calibri"  # one font everywhere - easier to read
    W, H = 820, 380  # corner toast, readable but not overwhelming
    for (x, y, w, h) in _monitors():
        win = tk.Toplevel(root)
        win.overrideredirect(True)
        px = x + w - W - 30          # top-right corner of this monitor
        py = y + 40
        win.geometry(f"{W}x{H}+{px}+{py}")
        win.configure(bg=bg)
        win.attributes("-topmost", True)
        # WHO is calling (the session) - bold
        tk.Label(win, text=title, font=(FONT, 34, "bold"),
                 bg=bg, fg=fg, wraplength=W - 40).pack(pady=(24, 12), padx=20)
        # WHAT it wants (the message) - bold
        tk.Label(win, text=body, font=(FONT, 28, "bold"),
                 bg=bg, fg=fg, wraplength=W - 40, justify="center").pack(padx=20, expand=True)
        bottom = tk.Frame(win, bg=bg)
        bottom.pack(side="bottom", fill="x", pady=(0, 14))
        if link:
            link_fg = "#0B57D0" if color == "amber" else "#FFFFFF"
            lbl = tk.Label(bottom, text="Open session \u2197", font=(FONT, 18, "bold"),
                           bg=bg, fg=link_fg, cursor="hand2")
            lbl.pack(side="left", padx=24)
            lbl.bind("<Button-1>", lambda _e: (_open_task_link(link), close()))
        tk.Label(bottom, text="click anywhere or press any key to dismiss",
                 font=(FONT, 18), bg=bg, fg=fg).pack(side="right", padx=24)
        win.bind("<Button-1>", close)
        # NO focus_force: must not interrupt Max's dictation
        win.update_idletasks()
        _make_no_focus(win)
        wins.append(win)

    # Force every toast to the very top of the Z-order and SHOW it BEFORE any
    # sound starts, so Max always sees the dismiss control first.
    for win in wins:
        try:
            _make_no_focus(win)          # re-applies topmost + no-activate
            win.lift()
            win.update()
        except Exception:
            pass

    hooks = _install_dismiss_hooks(close)
    after_ids = []

    def _schedule(ms, fn):
        after_ids.append(root.after(ms, fn))

    if on_visible is not None:
        try:
            on_visible()                  # now start the voice thread
        except Exception:
            pass

    if seconds and seconds > 0:
        # explicit fixed duration override
        _schedule(int(seconds * 1000), timer_close)
    else:
        # stay through the whole announcement: dismiss once the voice has
        # finished AND a 3s minimum has passed; hard cap 40s so we never hang.
        MIN_MS, CAP_MS, STEP = 3000, 40000, 250
        state = {"elapsed": 0}

        def _poll():
            state["elapsed"] += STEP
            done = (voice_done is None) or voice_done.is_set()
            if (done and state["elapsed"] >= MIN_MS) or state["elapsed"] >= CAP_MS:
                timer_close()
            else:
                _schedule(STEP, _poll)

        _schedule(STEP, _poll)

    root.mainloop()
    for handle, _cb in hooks:
        try:
            ctypes.windll.user32.UnhookWindowsHookEx(handle)
        except Exception:
            pass
    for after_id in after_ids:
        try:
            root.after_cancel(after_id)
        except Exception:
            pass
    # CRITICAL ORDERING: the Tcl interpreter must be torn down only after the
    # voice thread has fully finished. If another thread is still alive while
    # the Tkinter reference cycles are collected, CPython can run
    # Tcl_DeleteInterp in that thread and Tcl aborts with
    # "Tcl_AsyncDelete: async handler deleted by the wrong thread" - the
    # silent-alert crash. Join the voice thread here, on the Tk thread, before
    # touching any Tk window.
    if on_teardown is not None:
        try:
            on_teardown()
        except Exception:
            pass
    for win in wins:
        try:
            win.destroy()
        except Exception:
            pass
    try:
        root.destroy()
    except Exception:
        pass
    # Collect remaining Tkinter cycles in THIS thread so the interpreter is
    # released deterministically instead of by GC in some other thread.
    try:
        gc.collect()
    except Exception:
        pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--session", default="")
    ap.add_argument("--number", default="")
    ap.add_argument("--msg", default="needs your attention")
    ap.add_argument("--seconds", type=float, default=0,
                    help="fixed flash duration; 0 (default) = stay through the "
                         "whole spoken announcement, then auto-dismiss")
    ap.add_argument("--repeat", type=int, default=3)
    ap.add_argument("--device", default=DEFAULT_DEVICE)
    ap.add_argument("--volume", type=int, default=42)
    ap.add_argument("--tts-voice", default=DEFAULT_TTS_VOICE,
                    help="Microsoft neural voice; offline SAPI is automatic fallback")
    ap.add_argument("--no-voice", action="store_true")
    ap.add_argument("--force-voice", action="store_true",
                    help="speak even when the speakers are muted (emergency only)")
    ap.add_argument("--no-screen", action="store_true")
    ap.add_argument("--color", default="amber")
    ap.add_argument("--history", nargs="?", const=15, type=int,
                    help="show the last N alarms (what just flashed) and exit")
    ap.add_argument("--link", default="",
                    help="explicit session deep link; auto-resolved when omitted")
    ap.add_argument("--to", default="",
                    help="target machine; if it is a DIFFERENT machine, send the "
                         "alarm there via fleetcomm instead of firing locally")
    a = ap.parse_args()

    # "what just flashed and disappeared" - look up recent alarms and exit
    if a.history is not None:
        _print_history(a.history)
        return

    # remote dispatch: --to a machine other than this one -> send via fleetcomm
    if a.to:
        try:
            fc = _fleetcomm()
            if fc.canon_machine(a.to) != fc.machine_name():
                _dispatch_remote(a)
                return
        except Exception as e:
            sys.stderr.write(f"[attention] remote dispatch failed: {e}\n")
            return
        # else: --to is THIS machine -> fall through and fire locally

    session = _resolve_session(a.session)  # never anonymous
    num = f" number {a.number}" if a.number else ""
    # Toast shows just WHO (the task) + WHAT (the message); no extra name.
    title = f"TASK {session}"
    spoken = f"Attention. Task {session}{num}. {a.msg}"
    link = a.link or _resolve_task_link(session, os.getcwd())

    _log_call(session, a)
    _ensure_history_bar()

    stop = threading.Event()       # set on explicit click -> silence voice
    voice_done = threading.Event() # set when the announcement has fully played
    restore = None
    vthread = None
    voice_outcome = {"status": "not-run"}

    # Respect mute: if Max muted Pine (speaker endpoint or system default),
    # stay SILENT and show the overlay only. Override with --force-voice for a
    # true can't-miss emergency.
    if not a.no_voice and not a.force_voice and _device_is_muted(a.device):
        sys.stderr.write("[attention] speakers muted -> voice suppressed, screen only\n")
        a.no_voice = True

    if not a.no_voice:
        restore = _set_device_volume(a.device, a.volume / 100.0)

        def _voice_runner():
            try:
                voice_outcome["status"] = _play_voice(
                    spoken, a.device, a.repeat, stop, a.tts_voice
                )
            finally:
                voice_done.set()

        def _start_voice():
            nonlocal vthread
            vthread = threading.Thread(target=_voice_runner)
            vthread.start()

        def _on_teardown():
            # Voice thread must end before the Tk overlay is destroyed (see
            # _show_overlay). Cap the wait so a stuck audio driver cannot hang
            # the dismiss; the sound is stopped by the dismiss event already.
            nonlocal vthread
            if vthread is not None:
                vthread.join(timeout=8)

        if a.no_screen:
            _start_voice()          # no overlay to wait for
    else:
        voice_outcome["status"] = "suppressed-or-disabled"
        voice_done.set()

    if not a.no_screen:
        # Build and SHOW the toast first, then start the voice only once the
        # overlay is visible and dismissible (on_visible). --seconds (if >0)
        # is a fixed duration override.
        _show_overlay(
            title, a.msg, a.color, a.seconds, stop, voice_done,
            on_visible=(_start_voice if not a.no_voice else None),
            on_teardown=(_on_teardown if not a.no_voice else None),
            link=link,
        )

    # ensure the voice fully finishes before we exit / restore volume
    if vthread is not None:
        vthread.join(timeout=max(1, a.repeat) * 30)

    if restore:
        import time
        time.sleep(0.2)
        restore()
    _log_result(session, voice_outcome["status"])


def _logpath():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "attention.log")


def _log_call(session, a):
    """Append every invocation to a log so any alarm can be looked up later
    and a runaway caller can be traced."""
    import datetime
    import getpass
    try:
        ppid = os.getppid()
    except Exception:
        ppid = "?"
    line = (
        f"{datetime.datetime.now().isoformat(timespec='seconds')}\t"
        f"session={session!r}\tnumber={a.number!r}\tmsg={a.msg!r}\t"
        f"cwd={os.getcwd()!r}\tpid={os.getpid()}\tppid={ppid}\t"
        f"user={getpass.getuser()}\n"
    )
    try:
        with open(_logpath(), "a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass
    sys.stderr.write("[attention] " + line)


def _log_result(session, result):
    """Record whether speech completed, not merely whether the process launched."""
    import datetime
    line = (
        f"{datetime.datetime.now().isoformat(timespec='seconds')}\t"
        f"session={session!r}\tresult={result!r}\n"
    )
    try:
        with open(_logpath(), "a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass
    sys.stderr.write("[attention] " + line)


def _print_history(n):
    """Show the last N alarms - 'what just flashed and disappeared'."""
    try:
        with open(_logpath(), "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception:
        print("(no attention.log yet)")
        return
    if not lines:
        print("(attention.log is empty)")
        return
    print(f"Last {min(n, len(lines))} attention alarms (newest last):\n")

    def _val(v):
        """Decode a Python-repr-logged value ('C:\\\\base...' or 'plain')."""
        try:
            import ast
            return ast.literal_eval(v)
        except Exception:
            return v.strip("'")

    for ln in lines[-n:]:
        parts = dict(p.split("=", 1) for p in ln.strip().split("\t") if "=" in p)
        ts = ln.split("\t", 1)[0]
        sess = _val(parts.get("session", "?"))
        num = _val(parts.get("number", ""))
        msg = _val(parts.get("msg", ""))
        cwd = _val(parts.get("cwd", ""))
        tag = f"{sess}" + (f" #{num}" if num else "")
        if "result" in parts:
            result = _val(parts["result"])
            print(f"  {ts}  [{tag}]  result: {result}")
            continue
        print(f"  {ts}  [{tag}]  {msg}")
        print(f"             from: {cwd}")


if __name__ == "__main__":
    sys.exit(main())
