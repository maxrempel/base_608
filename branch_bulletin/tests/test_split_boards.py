"""Isolated test for split-per-team boards (B1) + reassign-by-name (B2).

Runs entirely against a throwaway BCAST_BASE temp dir - NEVER touches the live
board. Simulates distinct sessions by passing distinct cwd keys to the cmd_*
functions (identity is keyed by cwd). Asserts: legacy single-board unchanged
when flag off; after migrate, team isolation + joint broadcast + reassignment.
"""
import os, sys, tempfile, io, importlib
from contextlib import redirect_stdout

TMP = tempfile.mkdtemp(prefix="bcast_test_")
os.environ["BCAST_BASE"] = TMP
sys.path.insert(0, r"C:\claude_base\branch_bulletin")
import bcast
importlib.reload(bcast)  # ensure BASE picks up the env

# distinct "sessions" = distinct cwd keys
B1, B2, C5, C0, D2 = (os.path.join(TMP, x) for x in ("s_b1", "s_b2", "s_c5", "s_c0", "s_d2"))

fails = []
def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)

def cap(fn, *a, **k):
    buf = io.StringIO()
    with redirect_stdout(buf):
        fn(*a, **k)
    return buf.getvalue()

# ---------- LEGACY MODE (flag off): everyone shares one board ----------
check("split off at start", not bcast._split_on())
cap(bcast.cmd_whoami, B1, "b1")
cap(bcast.cmd_whoami, C5, "c5")
cap(bcast.cmd_post, B1, "legacy b stuff")
out = cap(bcast.cmd_read, C5)
check("legacy: c5 HEARS b1 (single shared board)", "legacy b stuff" in out)

# ---------- CUTOVER ----------
cap(bcast.cmd_migrate, B1, confirm=True)
check("split on after migrate", bcast._split_on())

# re-whoami all (cursors rebind to team+joint)
for cwd, bid in ((B1, "b1"), (B2, "b2"), (C5, "c5"), (C0, "c0"), (D2, "d2")):
    cap(bcast.cmd_whoami, cwd, bid)

# ---------- TEAM ISOLATION ----------
cap(bcast.cmd_post, B1, "songs canonical take3")      # b-team board
out_c5 = cap(bcast.cmd_read, C5)
out_b2 = cap(bcast.cmd_read, B2)
check("team: c5 does NOT hear b-team post", "songs canonical take3" not in out_c5)
check("team: b2 DOES hear b-team post", "songs canonical take3" in out_b2)

cap(bcast.cmd_post, C5, "team-system spec ready")     # c-team board
out_c0 = cap(bcast.cmd_read, C0)
out_b2b = cap(bcast.cmd_read, B2)
check("team: c0 hears c-team post", "team-system spec ready" in out_c0)
check("team: b2 does NOT hear c-team post", "team-system spec ready" not in out_b2b)

# ---------- JOINT BROADCAST (true all-teams now uses --all/force_all) ----------
cap(bcast.cmd_post, B1, "ALL HANDS: freeze at 5pm", force_all=True)
hb = cap(bcast.cmd_read, B2)
hc = cap(bcast.cmd_read, C0)
hd = cap(bcast.cmd_read, D2)
check("joint: b2 hears joint", "ALL HANDS" in hb and "(joint)" in hb)
check("joint: c0 hears joint (cross-team)", "ALL HANDS" in hc)
check("joint: d2 hears joint (cross-team)", "ALL HANDS" in hd)

# ---------- NO SELF-HEAR ----------
cap(bcast.cmd_post, C0, "c0 self note")
self_out = cap(bcast.cmd_read, C0)
check("no self-hear: c0 does not hear its own post", "c0 self note" not in self_out)

# ---------- B2 REASSIGNMENT (c5 -> d2b) ----------
reassign_out = cap(bcast.cmd_whoami, C5, "d2b")
check("reassign: announces 'I am now d2b (was c5)'", "d2b" in reassign_out and "was c5" in reassign_out)
# the announcement landed on the JOINT board -> a d-teammate hears it
heard = cap(bcast.cmd_read, D2)
check("reassign: d2 hears the move on joint", "I am now d2b (was c5)" in heard)

# ---------- GUARD 1: COLLISION on adopting a LIVE id ----------
# C0 is live (it just posted above -> its state mtime is fresh). A DIFFERENT
# cwd adopting "c0" must get the collision warning.
C0_DUP = os.path.join(TMP, "s_c0_dup")
dup_out = cap(bcast.cmd_whoami, C0_DUP, "c0")
check("guard: 2nd session adopting live 'c0' is warned", "COLLISION" in dup_out)
# a FREE id must NOT warn
free_out = cap(bcast.cmd_whoami, os.path.join(TMP, "s_z9"), "z9")
check("guard: adopting a free id 'z9' does NOT warn", "COLLISION" not in free_out)

# ---------- GUARD 2: CHALLENGE intra-team --joint (Max's point-of-violation ask) ----------
# d2 sends a --joint that names no cross-team id -> CHALLENGED, still sent to joint
# (fail-open; the poster self-corrects). A --joint naming a cross-team id (b1) is
# correctly addressed -> joint, no challenge. --all is the explicit broadcast.
chal_out = cap(bcast.cmd_post, D2, "d5 take scene 3", joint=True)
check("guard: intra-team --joint is CHALLENGED + still sent to joint",
      "CHALLENGE" in chal_out and "JOINT" in chal_out)
ok_out = cap(bcast.cmd_post, D2, "b1 freeze please", joint=True)
check("guard: cross-team --joint stays on joint, no challenge",
      "JOINT" in ok_out and "CHALLENGE" not in ok_out)
all_out = cap(bcast.cmd_post, D2, "all-teams status, no mentions", force_all=True)
check("guard: --all forces joint, no challenge",
      "JOINT" in all_out and "CHALLENGE" not in all_out)

print("\nboards on disk:", sorted(f for f in os.listdir(TMP) if f.startswith("bulletin")))
print("RESULT:", "ALL PASS" if not fails else f"{len(fails)} FAILED: {fails}")
sys.exit(1 if fails else 0)
