#!/usr/bin/env python3
"""Test the gradual board-retirement (rolloff) + on-demand archive.

Fully isolated: drives bcast.py as a SUBPROCESS with BCAST_BASE pointed at a
throwaway temp dir, so it can NEVER touch the live board/state. A final LEAK
GUARD asserts the live state dir file-count is unchanged.

Validates:
  - old entries (older than the window) move to BASE/archive/<board>.archive.jsonl
  - the live board keeps only the recent tail
  - a board with only recent entries is left alone (no archive file)
  - cursors shift down by exactly k per board, by the RIGHT scope:
      joint board  -> every session's cursors['joint']
      team board   -> only that team's sessions' cursors['team']
  - an active session's UNREAD tail count is preserved
  - a dormant cursor (< k) clamps to 0
  - dry-run changes nothing
  - `archive` surfaces retired entries on demand
"""
import os, sys, json, time, tempfile, shutil, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
BCAST = os.path.join(os.path.dirname(HERE), "bcast.py")
LIVE_STATE = r"C:\claude_base\branch_bulletin\state"

fails = []
def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)

def ts(offset_sec):
    return time.strftime("%Y-%m-%d %H:%M:%S",
                         time.localtime(time.time() + offset_sec))

OLD = -30 * 86400      # 30 days ago -> retired (window 7d)
NEW = -3600            # 1 hour ago  -> kept

def write_board(base, name, recs):
    with open(os.path.join(base, name), "w", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=True) + "\n")

def line(frm, off):
    return {"ts": ts(off), "from": frm, "msg": f"{frm} msg @ {off}"}

def board_lines(base, name):
    p = os.path.join(base, name)
    if not os.path.exists(p):
        return []
    return [l for l in open(p, encoding="utf-8").read().splitlines() if l.strip()]

def state(base, key):
    return json.load(open(os.path.join(base, "state", key + ".json"),
                         encoding="utf-8"))

def run(base, *cargs):
    env = dict(os.environ); env["BCAST_BASE"] = base
    return subprocess.run([sys.executable, BCAST, *cargs],
                          capture_output=True, text=True, env=env)

# snapshot live state dir for the leak guard
live_before = set(os.listdir(LIVE_STATE)) if os.path.isdir(LIVE_STATE) else set()

tmp = tempfile.mkdtemp(prefix="rolloff_test_")
try:
    os.makedirs(os.path.join(tmp, "state"), exist_ok=True)
    # flip split mode on so team boards are the model in play
    open(os.path.join(tmp, "SPLIT_BOARDS.on"), "w").write("on\n")

    # joint: 4 old + 3 recent  (k_joint = 4)
    write_board(tmp, "bulletin_joint.jsonl",
                [line("b27", OLD), line("b30", OLD), line("d15", OLD),
                 line("c6", OLD), line("d21", NEW), line("b27", NEW),
                 line("c16", NEW)])
    # b team: 3 old + 2 recent  (k_b = 3)
    write_board(tmp, "bulletin_b.jsonl",
                [line("b27", OLD), line("b30", OLD), line("b27", OLD),
                 line("b27", NEW), line("b30", NEW)])
    # c team: 2 recent only     (k_c = 0)
    write_board(tmp, "bulletin_c.jsonl",
                [line("c6", NEW), line("c16", NEW)])

    # states. cursors are line-counts into each board.
    def put_state(key, sid, team_cur, joint_cur):
        st = {"id": sid, "cursors": {"team": team_cur, "joint": joint_cur},
              "cwd": tmp}
        json.dump(st, open(os.path.join(tmp, "state", key + ".json"), "w"))

    put_state("A", "b27", 5, 7)   # active: read all of b + all joint
    put_state("B", "c6", 2, 6)    # active: read all c + 6/7 joint (1 unread)
    put_state("D", "b30", 1, 2)   # dormant: cursors below k -> clamp 0

    # --- DRY RUN changes nothing ---
    before_joint = board_lines(tmp, "bulletin_joint.jsonl")
    run(tmp, "rolloff", "7")
    check("dry-run leaves joint board untouched",
          board_lines(tmp, "bulletin_joint.jsonl") == before_joint)
    check("dry-run creates no archive dir",
          not os.path.exists(os.path.join(tmp, "archive")))

    # --- APPLY ---
    r = run(tmp, "rolloff", "7", "--apply")
    jl = board_lines(tmp, "bulletin_joint.jsonl")
    bl = board_lines(tmp, "bulletin_b.jsonl")
    cl = board_lines(tmp, "bulletin_c.jsonl")
    check("joint trimmed to 3 recent", len(jl) == 3)
    check("b trimmed to 2 recent", len(bl) == 2)
    check("c untouched (no old entries)", len(cl) == 2)

    aj = board_lines(tmp, os.path.join("archive", "bulletin_joint.archive.jsonl"))
    ab = board_lines(tmp, os.path.join("archive", "bulletin_b.archive.jsonl"))
    check("joint archive holds the 4 retired", len(aj) == 4)
    check("b archive holds the 3 retired", len(ab) == 3)
    check("no c archive file (nothing retired)",
          not os.path.exists(os.path.join(tmp, "archive",
                                          "bulletin_c.archive.jsonl")))

    A, B, D = state(tmp, "A"), state(tmp, "B"), state(tmp, "D")
    # joint cursors shift by k_joint=4
    check("A joint cursor 7 -> 3", A["cursors"]["joint"] == 3)
    check("B joint cursor 6 -> 2", B["cursors"]["joint"] == 2)
    check("B keeps its 1 unread joint (newlen3 - cur2 == 1)",
          len(jl) - B["cursors"]["joint"] == 1)
    check("D dormant joint cursor 2 -> clamp 0", D["cursors"]["joint"] == 0)
    # team cursors: b board k_b=3 affects only b-team sessions
    check("A(b) team cursor 5 -> 2", A["cursors"]["team"] == 2)
    check("D(b) dormant team cursor 1 -> clamp 0", D["cursors"]["team"] == 0)
    check("B(c) team cursor UNTOUCHED at 2 (c board had no rolloff)",
          B["cursors"]["team"] == 2)

    # --- archive readable on demand ---
    ra = run(tmp, "archive", "joint", "50")
    check("archive cmd prints retired joint entries",
          "BOARD ARCHIVE" in ra.stdout and "retired" in ra.stdout)

    # --- second rolloff is a clean no-op (recent tail is all < 7d) ---
    r2 = run(tmp, "rolloff", "7", "--apply")
    check("re-run rolloff is a no-op on the lean board",
          "already lean" in r2.stdout or "nothing older" in r2.stdout)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

live_after = set(os.listdir(LIVE_STATE)) if os.path.isdir(LIVE_STATE) else set()
check("LEAK GUARD: live state dir file set unchanged", live_before == live_after)

print("\nRESULT: " + ("ALL PASS" if not fails else f"{len(fails)} FAIL: {fails}"))
sys.exit(1 if fails else 0)
