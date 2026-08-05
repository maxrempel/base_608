#!/usr/bin/env python3
"""
bcast.py - local broadcast bulletin for coordinating sibling Claude branches.

Pure broadcast: one branch shouts, every OTHER branch hears it on its next turn.
No locking, no conflict logic. Just an append-only shared log + per-branch cursor.

Branch identity is set manually by Max ("you are b2") and stored keyed by the
branch's working directory (each worktree = its own cwd = its own identity).

Commands:
  python bcast.py whoami b2          set THIS branch's id to b2 (run once per session)
  python bcast.py post "message"     shout a message to all sibling branches
  python bcast.py read               print messages from OTHER branches not yet seen
  python bcast.py read --hook        same, but reads cwd from hook stdin JSON (UserPromptSubmit)
  python bcast.py log                print the whole bulletin (debug)
  python bcast.py who                show this branch's id

Fails open everywhere: a broken bulletin must never wedge a session.
"""
import sys, os, json, time, hashlib, re

BASE = r"C:\claude_base\branch_bulletin"
BULLETIN = os.path.join(BASE, "bulletin.jsonl")
STATE_DIR = os.path.join(BASE, "state")
HALT_FILE = os.path.join(BASE, "shared", "HALT.txt")


def _safe_key(cwd):
    norm = os.path.normcase(os.path.abspath(cwd))
    h = hashlib.sha1(norm.encode("utf-8", "replace")).hexdigest()[:10]
    tail = re.sub(r"[^A-Za-z0-9]+", "_", os.path.basename(norm))[-32:]
    return f"{tail}_{h}"


def _state_path(cwd):
    return os.path.join(STATE_DIR, _safe_key(cwd) + ".json")


def _load_state(cwd):
    p = _state_path(cwd)
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"id": None, "cursor": 0}


def _save_state(cwd, st):
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(_state_path(cwd), "w", encoding="utf-8") as f:
        json.dump(st, f)


def _read_lines():
    try:
        with open(BULLETIN, "r", encoding="utf-8") as f:
            return [l for l in f.read().splitlines() if l.strip()]
    except Exception:
        return []


def cmd_whoami(cwd, new_id):
    st = _load_state(cwd)
    st["id"] = new_id
    # Don't replay history a branch never saw before it had a name:
    # start its cursor at the current end of the log.
    st["cursor"] = len(_read_lines())
    _save_state(cwd, st)
    print(f"OK - this branch is now '{new_id}'. It will hear new sibling broadcasts from here on.")


def cmd_who(cwd):
    st = _load_state(cwd)
    print(st.get("id") or "(no id set - run: python bcast.py whoami b2)")


def cmd_post(cwd, msg):
    st = _load_state(cwd)
    me = st.get("id")
    if not me:
        print("ERROR - no id set for this branch. Run: python bcast.py whoami b2")
        return 1
    os.makedirs(BASE, exist_ok=True)
    rec = {"ts": time.strftime("%Y-%m-%d %H:%M:%S"), "from": me, "msg": msg}
    with open(BULLETIN, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=True) + "\n")
    # Advance own cursor so a branch never hears its own shout.
    st["cursor"] = len(_read_lines())
    _save_state(cwd, st)
    print(f"BROADCAST sent as {me}: {msg}")


def cmd_read(cwd, hook=False):
    st = _load_state(cwd)
    me = st.get("id")
    # Only named branches hear the board. An unnamed chat (Max runs many
    # independent ones) gets nothing - no injection, no noise.
    if not me:
        return 0
    lines = _read_lines()
    cursor = st.get("cursor", 0)
    new = lines[cursor:]
    # show only OTHER branches' messages
    out = []
    for l in new:
        try:
            r = json.loads(l)
        except Exception:
            continue
        if r.get("from") == me:
            continue
        out.append(r)
    # advance cursor regardless (we've now seen up to end)
    st["cursor"] = len(lines)
    _save_state(cwd, st)

    # HALT banner: if a halt is in effect it is injected EVERY tick (even with
    # no new messages) so a looping branch reliably sees it and stops its loop.
    halt = _read_halt()
    chunks = []
    if halt:
        chunks.append(
            "=== HALT IN EFFECT ===\n"
            f"{halt}\n"
            "STOP your self-wake loop now: finish/abandon the current action, "
            "do NOT call ScheduleWakeup again, go quiet until Max or b1 resumes.\n"
            "=== end halt ===")
    if out:
        header = "=== BROADCASTS FROM SIBLING BRANCHES (new since last turn) ==="
        body = "\n".join(f"[{r['ts']}] {r['from']}: {r['msg']}" for r in out)
        footer = "=== end broadcasts ===" if not hook else (
            "=== end broadcasts (auto-injected; reply only if relevant) ===")
        chunks.append(f"{header}\n{body}\n{footer}")
    if chunks:
        print("\n".join(chunks))
    return 0


def _read_halt():
    try:
        with open(HALT_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return None


def cmd_halt(cwd, reason):
    st = _load_state(cwd)
    me = st.get("id") or "?"
    os.makedirs(os.path.dirname(HALT_FILE), exist_ok=True)
    text = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] HALT set by {me}: {reason}"
    with open(HALT_FILE, "w", encoding="utf-8") as f:
        f.write(text + "\n")
    # also drop a line on the board so it shows in history
    try:
        with open(BULLETIN, "a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": time.strftime("%Y-%m-%d %H:%M:%S"),
                                "from": me, "msg": f"HALT: {reason}"},
                               ensure_ascii=True) + "\n")
    except Exception:
        pass
    print(f"HALT set: {reason}\nAll looping branches will stop on their next board read. Use 'resume' to clear.")


def cmd_resume(cwd):
    try:
        os.remove(HALT_FILE)
        print("HALT cleared - branches may resume (Max must re-arm their loops).")
    except FileNotFoundError:
        print("No halt was in effect.")
    except Exception as e:
        print(f"could not clear halt: {e}")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 0
    cmd = args[0]

    # For the hook, cwd comes from stdin JSON, not the process cwd.
    if cmd == "read" and "--hook" in args:
        cwd = None
        try:
            data = json.load(sys.stdin)
            cwd = data.get("cwd")
        except Exception:
            cwd = None
        if not cwd:
            cwd = os.getcwd()
        return cmd_read(cwd, hook=True)

    cwd = os.getcwd()
    if cmd == "whoami":
        if len(args) < 2:
            print("usage: python bcast.py whoami b2")
            return 1
        return cmd_whoami(cwd, args[1])
    if cmd == "who":
        return cmd_who(cwd)
    if cmd == "post":
        if len(args) < 2:
            print('usage: python bcast.py post "message"')
            return 1
        return cmd_post(cwd, " ".join(args[1:]))
    if cmd == "read":
        return cmd_read(cwd, hook=False)
    if cmd == "halt":
        reason = " ".join(args[1:]) if len(args) > 1 else "manual halt"
        return cmd_halt(cwd, reason)
    if cmd == "resume":
        return cmd_resume(cwd)
    if cmd == "log":
        for l in _read_lines():
            print(l)
        return 0
    print(__doc__)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main() or 0)
    except Exception as e:
        # fail open - never wedge a session
        sys.stderr.write(f"bcast.py error (ignored): {e}\n")
        sys.exit(0)
