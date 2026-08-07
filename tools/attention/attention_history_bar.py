#!/usr/bin/env python
"""
attention_history_bar.py - persistent collapsed history of attention alerts.

Shows a small box at the bottom of every monitor with the recent attention
announcements. Clicking the box expands it into a readable list where each
entry carries a deep link back to the session that called it (Codex tasks via
codex://threads/<id>, Claude Code sessions via claude://resume?session=<id>).

Single instance: only one bar runs at a time. attention.py launches it after
each alert so the history survives the alert being dismissed.

Safe by construction: every window is topmost but WS_EX_NOACTIVATE, so it
never steals keyboard focus from Max's dictation or other work.
"""

import ctypes
import ast
import glob
import json
import os
import subprocess
import sys
import time
import tkinter as tk
import warnings

warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(HERE, "attention.log")
LOCK_NAME = "Local\\AttentionHistoryBar_v01"
MAX_ENTRIES = 8
REFRESH_MS = 2000


# --- single instance via a named mutex ------------------------------------

def _take_lock():
    """Create a named mutex; return False if another bar is already running."""
    try:
        ERROR_ALREADY_EXISTS = 183
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.CreateMutexW(None, False, LOCK_NAME)
        return bool(handle) and kernel32.GetLastError() != ERROR_ALREADY_EXISTS
    except Exception:
        return True  # fail-open: let the bar start


# --- no-focus topmost window styling --------------------------------------

def _make_no_focus(win):
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
        u.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0002 | 0x0001 | 0x0010 | 0x0040 | 0x0020)
    except Exception:
        pass


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


# --- reading the attention log --------------------------------------------

def _read_entries():
    """Parse the newest attention.log call records into display entries."""
    entries = []
    try:
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception:
        return entries

    def _val(v):
        """Decode a Python-repr-logged value ('C:\\\\base...' or 'plain')."""
        try:
            return ast.literal_eval(v)
        except Exception:
            return v.strip("'")

    for ln in lines[-200:]:
        parts = dict(p.split("=", 1) for p in ln.strip().split("\t") if "=" in p)
        if "msg" not in parts:
            continue
        entries.append({
            "ts": ln.split("\t", 1)[0],
            "session": _val(parts.get("session", "")),
            "msg": _val(parts.get("msg", "")),
            "cwd": _val(parts.get("cwd", "")),
        })
    return entries[-MAX_ENTRIES:]


def _resolve_link(session, cwd):
    """Same resolution as attention.py: Codex threads table by cwd, then
    Claude Code transcripts by project folder."""
    try:
        norm = (cwd or "").replace("\\\\?\\", "").rstrip("\\/").lower()
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
            by_cwd = [r for r in rows
                      if (r[1] or "").replace("\\\\?\\", "").rstrip("\\/").lower() == norm]
            if by_cwd:
                by_cwd.sort(key=lambda r: r[3] or 0, reverse=True)
                return f"codex://threads/{by_cwd[0][0]}"
            label = (session or "").replace("Codex:", "", 1).strip().lower()
            if label:
                titled = [r for r in rows if label in (r[2] or "").lower()]
                if titled:
                    titled.sort(key=lambda r: r[3] or 0, reverse=True)
                    return f"codex://threads/{titled[0][0]}"
        import re
        enc = re.sub(r"[^A-Za-z0-9]", "-", (cwd or "").replace("\\\\?\\", ""))
        folder = os.path.join(os.path.expanduser("~"), ".claude", "projects", enc)
        files = sorted(glob.glob(os.path.join(folder, "*.jsonl")),
                       key=os.path.getmtime, reverse=True)
        if files:
            sid = os.path.splitext(os.path.basename(files[0]))[0]
            return f"claude://resume?session={sid}"
    except Exception:
        pass
    return None


def _open_link(url):
    try:
        subprocess.run(["powershell", "-NoProfile", "-NonInteractive",
                        "-Command", f"Start-Process '{url}'"],
                       creationflags=0x08000000, timeout=20)
    except Exception:
        pass


# --- the bar UI -----------------------------------------------------------

class HistoryBar:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()
        self.wins = []
        self.expanded = False
        self.last_signature = None
        self.last_monitors = None
        self.entries = []

    def _build_window(self, x, y, w, h, collapsed=True):
        win = tk.Toplevel(self.root)
        win.overrideredirect(True)
        win.configure(bg="#FFFAD6")
        win.attributes("-topmost", True)
        BW, BH = (440, 46) if collapsed else (780, 420)
        px = x + (w - BW) // 2
        py = y + h - BH - 14
        win.geometry(f"{BW}x{BH}+{px}+{py}")
        return win

    def _make_close_button(self, parent):
        """A clearly visible close control: bordered square with a bold X."""
        close = tk.Frame(parent, bg="#FFFAD6", highlightbackground="#C9B97A",
                         highlightthickness=1, cursor="hand2")
        lbl = tk.Label(close, text="\u2715", font=("Calibri", 15, "bold"),
                       bg="#FFFAD6", fg="#7A2E00", padx=7, pady=1)
        lbl.pack()
        close.bind("<Button-1>", lambda _e: (self.close_bar(), "break")[1])
        lbl.bind("<Button-1>", lambda _e: (self.close_bar(), "break")[1])
        return close

    def _collapsed_content(self, win):
        count = len(self.entries)
        latest = self.entries[-1] if self.entries else None
        if latest:
            text = f"\U0001F514 {count} alert(s)  {latest['session']}: {latest['msg']}"
            full = text
            if len(text) > 46:
                text = text[:43] + "..."
        else:
            text = "\U0001F514 No alerts yet"
            full = text
        # Background clicks toggle; interactive children return "break" so
        # their own handlers run and this binding is skipped (bindtags).
        win.bind("<Button-1>", lambda _e: (self.toggle(), "break")[1])
        lbl = tk.Label(win, text=text, font=("Calibri", 14, "bold"),
                       bg="#FFFAD6", fg="#000000", anchor="w", cursor="hand2")
        _bind_tooltip(lbl, full)
        lbl.pack(side="left", fill="x", expand=True, padx=12, pady=8)
        lbl.bind("<Button-1>", lambda _e: (self.toggle(), "break")[1])
        close = self._make_close_button(win)
        close.pack(side="right", padx=(0, 8), pady=6)

    def _expanded_content(self, win):
        head_row = tk.Frame(win, bg="#FFFAD6")
        head_row.pack(fill="x", padx=12, pady=(10, 4))
        head = tk.Label(head_row, text="Attention history \u2014 click an entry to open its session",
                        font=("Calibri", 15, "bold"), bg="#FFFAD6", fg="#000000",
                        anchor="w", cursor="hand2")
        head.pack(side="left", fill="x", expand=True)
        head.bind("<Button-1>", lambda _e: (self.toggle(), "break")[1])
        close = self._make_close_button(head_row)
        close.pack(side="right", padx=(8, 0))
        canvas = tk.Canvas(win, bg="#FFFAD6", highlightthickness=0)
        canvas.bind("<Button-1>", lambda _e: (self.toggle(), "break")[1])
        scroll = tk.Scrollbar(win, orient="vertical", command=canvas.yview)
        frame = tk.Frame(canvas, bg="#FFFAD6")
        frame.bind("<Configure>",
                   lambda _e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True, padx=(12, 0), pady=(0, 10))
        scroll.pack(side="right", fill="y", pady=(0, 10), padx=(0, 12))

        if not self.entries:
            tk.Label(frame, text="No alerts yet.", font=("Calibri", 13),
                     bg="#FFFAD6", fg="#000000").pack(anchor="w", pady=8)
        for e in reversed(self.entries):
            link = _resolve_link(e["session"], e["cwd"])
            card = tk.Frame(frame, bg="#FFFFFF", highlightbackground="#E3D7A8",
                            highlightthickness=1)
            card.pack(fill="x", padx=4, pady=5)
            head = tk.Frame(card, bg="#FFFFFF")
            head.pack(fill="x", padx=8, pady=(6, 2))
            tk.Label(head, text=e["ts"][11:16], font=("Calibri", 11),
                     bg="#FFFFFF", fg="#666666").pack(side="left")
            tk.Label(head, text=e["session"], font=("Calibri", 13, "bold"),
                     bg="#FFFFFF", fg="#000000").pack(side="left", padx=8)
            if link:
                open_lbl = tk.Label(head, text="Open session \u2197",
                                    font=("Calibri", 12, "bold"),
                                    bg="#FFFFFF", fg="#0B57D0", cursor="hand2")
                open_lbl.pack(side="right")
                open_lbl.bind("<Button-1>",
                              lambda _ev, u=link: (_open_link(u), "break")[1])
            tk.Label(card, text=e["msg"], font=("Calibri", 12),
                     bg="#FFFFFF", fg="#111111", wraplength=700,
                     justify="left").pack(fill="x", padx=8, pady=(0, 7))

    def _rebuild(self):
        for win in self.wins:
            try:
                win.destroy()
            except Exception:
                pass
        self.wins = []
        for (x, y, w, h) in _monitors():
            win = self._build_window(x, y, w, h, collapsed=not self.expanded)
            if self.expanded:
                self._expanded_content(win)
            else:
                self._collapsed_content(win)
            win.update_idletasks()
            _make_no_focus(win)
            win.lift()
            win.update()
            self.wins.append(win)

    def toggle(self):
        self.expanded = not self.expanded
        self._rebuild()

    def close_bar(self):
        try:
            self.root.quit()
        except Exception:
            pass

    def refresh(self):
        try:
            entries = _read_entries()
            sig = json.dumps(entries, ensure_ascii=False)
            mon_sig = json.dumps(_monitors())
            if sig != self.last_signature or mon_sig != self.last_monitors:
                self.last_signature = sig
                self.last_monitors = mon_sig
                self.entries = entries
                self._rebuild()
        except Exception as e:
            sys.stderr.write(f"[attention_history_bar] refresh error: {e}\n")
        # Always reschedule, even after an error, so the bar cannot die
        # silently from one bad refresh.
        try:
            self.root.after(REFRESH_MS, self.refresh)
        except Exception:
            pass

    def run(self):
        self._rebuild()
        self.root.after(REFRESH_MS, self.refresh)
        self.root.mainloop()


def _bind_tooltip(widget, text):
    """Show the full announcement as a small tooltip on hover."""
    tip = None

    def _show(_e):
        nonlocal tip
        if tip is not None or not text:
            return
        try:
            tip = tk.Toplevel(widget)
            tip.wm_overrideredirect(True)
            tip.attributes("-topmost", True)
            x = widget.winfo_rootx()
            y = widget.winfo_rooty() + widget.winfo_height() + 4
            tip.geometry(f"+{x}+{y}")
            tk.Label(tip, text=text, font=("Calibri", 11),
                     bg="#FFFFE1", fg="#000000", justify="left",
                     wraplength=640).pack()
            _make_no_focus(tip)
        except Exception:
            tip = None

    def _hide(_e):
        nonlocal tip
        if tip is not None:
            try:
                tip.destroy()
            except Exception:
                pass
            tip = None

    widget.bind("<Enter>", _show)
    widget.bind("<Leave>", _hide)


def main():
    if not _take_lock():
        return 0
    root = tk.Tk()
    bar = HistoryBar(root)
    bar.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
