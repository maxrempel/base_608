"""Regression suite for the team-comms infra bugs fixed 2026-06-18.

Locks the THREE bugs reported + fixed that night so they cannot silently
regress, plus the wake_listener/wakeup mechanics they depend on:

  1. case-insensitive team + @-mention routing  (commit fdfeb9f5)
       - capital ids ('B26juniorconnector') must NOT form a phantom team
       - a cross-team @-mention auto-routes to the joint board even when the
         mention is in a DIFFERENT case than the registered id
       - same-team mentions do NOT false-trigger a cross-team route
       - version-string noise ('v01', 'preR7') must NOT invent phantom teams
  2. force-wake honesty                          (commit 1042d521)
       - a stamped-but-dead session_id (no fresh listener lock) is reported
         'queued', NEVER a false 'FORCE-WOKEN'
       - a provably-live listener (fresh lock) IS force-woken + gets a signal
  3. worklog cwd-split                            (commit 00d78039)
       - a subfolder cd resolves to the SAME git-worktree-root key as the root
       - off-git, keying fails open to the raw cwd

Plus the wake_listener firing path (force-wake signal, scheduled single +
recurring) and wakeup.py parsing/integration.

LEAK-PROOF: everything runs under a throwaway BCAST_BASE temp dir, and all
simulated sessions use cwds UNDER that temp dir, so the live board/state are
never touched. A final guard asserts the live state dir file-count is unchanged
(this is the exact pollution that produced a false '3x c16' collision when the
ad-hoc /tmp harnesses forgot to isolate os.environ).

Run:  python test_comms_regression.py   ->  exit 0 = all pass, 1 = failure.
"""
import os, sys, io, json, time, tempfile, shutil, subprocess, importlib
from contextlib import redirect_stdout

TMP = tempfile.mkdtemp(prefix="comms_regr_")
os.environ["BCAST_BASE"] = TMP   # MUST be set before importing the modules

BRANCH_DIR = r"C:\claude_base\branch_bulletin"
WAKE_DIR_SRC = r"C:\claude_base\tools\wake_listener"
WORKLOG_DIR_SRC = r"C:\claude_base\compaction_kb\scripts"
for p in (BRANCH_DIR, WAKE_DIR_SRC, WORKLOG_DIR_SRC):
    sys.path.insert(0, p)

import bcast; importlib.reload(bcast)        # picks up BCAST_BASE=TMP
import wakeup; importlib.reload(wakeup)
import worklog; importlib.reload(worklog)

LISTENER = os.path.join(WAKE_DIR_SRC, "wake_listener.py")
WAKEUP_PY = os.path.join(WAKE_DIR_SRC, "wakeup.py")
BCAST_PY = os.path.join(BRANCH_DIR, "bcast.py")
LIVE_STATE = r"C:\claude_base\branch_bulletin\state"

_live_before = set(os.listdir(LIVE_STATE)) if os.path.isdir(LIVE_STATE) else set()

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

def cwd(name):
    p = os.path.join(TMP, name)
    os.makedirs(p, exist_ok=True)
    return p

def run_listener(sid, cwd_path, timeout=30):
    env = dict(os.environ)  # already carries BCAST_BASE=TMP
    payload = json.dumps({"session_id": sid, "cwd": cwd_path})
    r = subprocess.run([sys.executable, LISTENER], input=payload, env=env,
                       capture_output=True, text=True, timeout=timeout)
    return r.returncode, (r.stderr or "")


# ======================================================================
# BUG 1 - case-insensitive team derivation + @-mention routing
# ======================================================================
check("team_of('B26juniorconnector') == 'b' (no phantom 'B' team)",
      bcast._team_of("B26juniorconnector") == "b")
check("team_of('D8') == 'd'", bcast._team_of("D8") == "d")

# register sessions on a throwaway split board
cap(bcast.cmd_migrate, cwd("m"), confirm=True)
check("split boards ON", bcast._split_on())
cap(bcast.cmd_whoami, cwd("s_b26"), "B26juniorconnector")  # capital -> team b
cap(bcast.cmd_whoami, cwd("s_b15"), "b15merger")           # team b
cap(bcast.cmd_whoami, cwd("s_d8"), "d8")                   # team d

known = bcast._known_ids()
check("known_ids maps lowercased -> canonical",
      known.get("b26juniorconnector") == "B26juniorconnector")

# capital '@B26juniorconnector' in a message resolves to the canonical id
m = bcast._mentioned_ids("b15merger", "b15merger -> @B26juniorconnector: status")
check("capital @-mention resolves to canonical id", "B26juniorconnector" in m)

# whole-token: bare 'b15' must not match inside a longer id
m2 = bcast._mentioned_ids("d8", "ping b15merger now")
check("@-mention is whole-token (b15merger, not b15)", m2 == {"b15merger"})

# same-team mention (b15 -> b26, both team b) does NOT auto-route to joint
out_same = cap(bcast.cmd_post, cwd("s_b15"), "b15merger -> @B26juniorconnector hi")
check("same-team post is NOT auto-routed to joint",
      "Auto-routing to the JOINT" not in out_same)

# genuine cross-team mention (d8 -> b15merger) DOES auto-route to joint
out_cross = cap(bcast.cmd_post, cwd("s_d8"), "d8 -> b15merger please pull")
check("cross-team post auto-routes to joint", "JOINT" in out_cross)

# the cross-team target actually HEARS it on the joint board
heard = cap(bcast.cmd_read, cwd("s_b15"))
check("cross-team target hears the auto-routed post", "please pull" in heard)

# version-string noise must NOT invent phantom teams
check("version noise 'v01'/'preR7' does NOT create a phantom team",
      bcast._names_other_team("b15merger", "deployed v01 of preR7 build") == set())

# ---- CHALLENGE-at-point-of-violation: routing by who you address (2026-06-18) ----
# Max's rule: do NOT silently reroute - CHALLENGE the poster and still send (fail-open).
# own-team --joint (names only a same-team id) is challenged + still sent to joint
o_own = cap(bcast.cmd_post, cwd("s_b15"), "@B26juniorconnector intra-tamza note", joint=True)
check("own-team --joint is CHALLENGED", "CHALLENGE" in o_own)
check("own-team --joint still sends to joint (fail-open)", "JOINT" in o_own)
# a --joint with NO @mention at all is also challenged (the un-nudged status leak)
o_none = cap(bcast.cmd_post, cwd("s_b15"), "899-row fix is LIVE", joint=True)
check("no-@mention --joint is CHALLENGED", "CHALLENGE" in o_none)
# a plain post (NO --joint, no cross-team mention) goes to team board, NO challenge
o_plain = cap(bcast.cmd_post, cwd("s_b15"), "plain team status, no flag")
check("plain own-team post -> team board, no challenge",
      "team 'b'" in o_plain and "CHALLENGE" not in o_plain and "JOINT" not in o_plain)
# a cross-team @mention still PROMOTES to joint (no challenge - it's addressed right)
o_cross = cap(bcast.cmd_post, cwd("s_b15"), "b15merger -> d8 please pull", joint=True)
check("cross-team @mention routes to joint, NOT challenged",
      "JOINT" in o_cross and "CHALLENGE" not in o_cross)
# --all (force_all) ALWAYS reaches joint, no challenge (explicit broadcast escape)
o_all = cap(bcast.cmd_post, cwd("s_b15"), "genuine all-teams notice", force_all=True)
check("--all forces joint, no challenge", "JOINT" in o_all and "CHALLENGE" not in o_all)

# ---- cd MIS-ATTRIBUTION guard (2026-06-19, G2/g1 'posted as b29' bug) ----
# Simulate the bug: cwd 's_d8' is registered to 'd8', but a session that is REALLY
# b15merger cd'd here and posts a message that self-attributes as 'b15merger'.
o_mismatch = cap(bcast.cmd_post, cwd("s_d8"), "b15merger -> @d8 please pull (cd'd in)")
check("cd mis-attribution is REFUSED (leading self-id != cwd id)",
      "REFUSED" in o_mismatch)
check("refusal names the real id and offers --as", "--as b15merger" in o_mismatch)
# a CORRECT self-attributed post (leading id == cwd id) is NOT refused
o_ok = cap(bcast.cmd_post, cwd("s_d8"), "d8 -> status update for my team")
check("correct self-attribution is NOT refused", "REFUSED" not in o_ok)
# @-addressing (not a self-claim) is NOT refused even if it names another id first
o_addr = cap(bcast.cmd_post, cwd("s_d8"), "@b15merger can you confirm?")
check("@-addressing a sibling is NOT refused", "REFUSED" not in o_addr)
# --as overrides: posts under the explicit id from any cwd, no refusal, stateless
o_as = cap(bcast.cmd_post, cwd("s_d8"), "b15merger -> @d8 via --as", as_id="b15merger")
check("--as posts under the explicit id (no refusal)",
      "REFUSED" not in o_as and "b15merger" in o_as and "--as" in o_as)
# a leading token that is NOT a registered id does not trip the guard (version etc.)
o_ver = cap(bcast.cmd_post, cwd("s_d8"), "d8 shipped v2 of the build")
check("non-id leading token does not trip the guard", "REFUSED" not in o_ver)


# ======================================================================
# BUG 2 - force-wake honesty (dead listener = queued, live = FORCE-WOKEN)
# ======================================================================
LOCK_DIR = os.path.join(TMP, "wake", "locks"); os.makedirs(LOCK_DIR, exist_ok=True)
c16c = cwd("s_c16"); c7c = cwd("s_c7")
cap(bcast.cmd_whoami, c16c, "c16")
cap(bcast.cmd_whoami, c7c, "c7")
# stamp a session_id for c7 but give it NO fresh lock => dead listener
st7 = bcast._load_state(c7c); st7["session_id"] = "sessDEAD"; bcast._save_state(c7c, st7)

# DEAD: stamped session_id but NO real listener -> confirm-by-consumption means
# the wake is honestly reported as queued, NEVER a false FORCE-WOKEN.
o_dead = cap(bcast.cmd_wake, c16c, ["--name", "c7", "ping c7"])
check("dead listener NOT reported FORCE-WOKEN", "FORCE-WOKEN" not in o_dead)
check("dead listener reported queued/no-armed-listener",
      "queued" in o_dead.lower() or "no armed listener" in o_dead.lower())

# LIVE: a REAL wake_listener subprocess is blocking for c7live. cmd_wake confirms
# delivery by watching the signal actually get CONSUMED, then reports FORCE-WOKEN
# (the 2026-06-19 honesty upgrade: a fresh lock alone is no longer trusted).
live_cwd = cwd("s_c7live")
cap(bcast.cmd_whoami, live_cwd, "c7live")
listener = subprocess.Popen([sys.executable, LISTENER], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True, env=dict(os.environ))
listener.stdin.write(json.dumps({"session_id": "sessLIVE", "cwd": live_cwd}))
listener.stdin.close()
# wait for the listener to arm: stamp its session_id into c7live state + lock
armed = False
for _ in range(60):
    st = bcast._load_state(live_cwd)
    if st.get("session_id") == "sessLIVE" and bcast._listener_alive("sessLIVE"):
        armed = True; break
    time.sleep(0.1)
check("real wake_listener armed (stamped session_id + live lock)", armed)
o_live = cap(bcast.cmd_wake, c16c, ["--name", "c7live", "real wake"])
check("live listener IS FORCE-WOKEN (signal consumed by a real listener)",
      "FORCE-WOKEN" in o_live and "c7live" in o_live)
try:
    rc_live = listener.wait(timeout=15)
except subprocess.TimeoutExpired:
    listener.kill(); rc_live = None
check("real listener exited 2 (woke) on the consumed signal", rc_live == 2)


# ======================================================================
# wake_listener firing path (force-wake signal + scheduled wakes)
# ======================================================================
SIG_DIR = os.path.join(TMP, "wake", "signals"); os.makedirs(SIG_DIR, exist_ok=True)
lc = cwd("s_listen")
sid_fw = "sessFW1"
with open(os.path.join(SIG_DIR, sid_fw + ".signal"), "w", encoding="utf-8") as f:
    f.write("WAKE CALL from tester: come to the board")
rc, err = run_listener(sid_fw, lc)
check("listener force-wake exits 2", rc == 2)
check("listener force-wake delivers message", "come to the board" in err)
check("listener consumes the signal file",
      not os.path.exists(os.path.join(SIG_DIR, sid_fw + ".signal")))

# scheduled single wake (due in the past) fires + is removed
sched = cwd("s_sched")
SCHED_DIR = os.path.join(TMP, "wake", "schedules"); os.makedirs(SCHED_DIR, exist_ok=True)
sched_file = os.path.join(SCHED_DIR, bcast._safe_key(sched) + ".json")
with open(sched_file, "w", encoding="utf-8") as f:
    json.dump([{"due": time.time() - 100, "msg": "check the deploy", "repeat_sec": 0}], f)
rc, err = run_listener("sessSCHED1", sched)
check("scheduled single wake exits 2", rc == 2)
check("scheduled single wake delivers message", "check the deploy" in err)
check("scheduled single entry removed after firing", json.load(open(sched_file)) == [])

# recurring schedule advances instead of being removed
with open(sched_file, "w", encoding="utf-8") as f:
    json.dump([{"due": time.time() - 100, "msg": "daily check", "repeat_sec": 3600}], f)
rc, err = run_listener("sessSCHED2", sched)
rem = json.load(open(sched_file))
check("recurring entry kept + advanced to the future",
      len(rem) == 1 and rem[0]["due"] > time.time())


# ======================================================================
# wakeup.py parsing + integration with the listener
# ======================================================================
check("parse 'in 2 weeks' ~= +14d",
      abs(wakeup._parse_when("in 2 weeks") - (time.time() + 14 * 86400)) < 5)
check("parse repeat 'weekly' == 604800", wakeup._parse_repeat("weekly") == 604800)
check("parse repeat 'every 2 days'", wakeup._parse_repeat("every 2 days") == 2 * 86400)
check("parse repeat 'once' -> 0 (single)", wakeup._parse_repeat("once") == 0)

# wakeup add (run from a real cwd) -> listener fires it
wt = cwd("s_wakeup")
env = dict(os.environ)
r = subprocess.run([sys.executable, WAKEUP_PY, "add", "--in", "1 seconds",
                    "--msg", "resume parked task"], env=env, cwd=wt,
                   capture_output=True, text=True)
check("wakeup add returns 0 + prints SCHEDULED",
      r.returncode == 0 and "SCHEDULED" in r.stdout)
time.sleep(1.2)
rc, err = run_listener("sessWU1", wt)
check("listener fires the wakeup-added schedule (exit 2)", rc == 2)
check("listener delivers the wakeup message", "resume parked task" in err)


# ======================================================================
# BUG 3 - worklog cwd-split (git-worktree-root keying)
# ======================================================================
repo = os.path.join(TMP, "wl_repo")
deep = os.path.join(repo, "tools", "deep", "nested")
os.makedirs(deep)
subprocess.run(["git", "-C", repo, "init", "-q"], check=True)
check("worklog: subfolder key == repo-root key (no split)",
      worklog._project_key(deep) == worklog._project_key(repo))
nongit = cwd("nongit_dir")
check("worklog: off-git keying fails open to raw cwd",
      worklog._resolve_root(nongit) == nongit)


# ======================================================================
# ROOMS - N-way side-channels, visible but OFF the boards (2026-06-21)
# ======================================================================
rA, rB, rC = cwd("s_roomA"), cwd("s_roomB"), cwd("s_roomC")
cap(bcast.cmd_whoami, rA, "rm1"); cap(bcast.cmd_whoami, rB, "rm2"); cap(bcast.cmd_whoami, rC, "rm3")
# rm1 opens a pairwise room with rm2 and posts (multi-word msg, no explicit name)
o_create = cap(bcast.cmd_room, rA, ["--with", "rm2", "lets sync in here"])
rn = "pair_" + "~".join(sorted(["rm1", "rm2"]))
check("room: pairwise auto-created + posted", "created" in o_create.lower() and "posted" in o_create.lower())
# KNOCK MODEL (2026-07-07): a member does NOT auto-hear the body - cmd_read shows
# only a one-line knock naming the room; the body appears only on an explicit
# --read, which then clears the knock.
_r2 = cap(bcast.cmd_read, rB)
check("room: member gets a KNOCK, not the body", (rn in _r2) and ("lets sync in here" not in _r2))
check("room: knock PERSISTS until --read (not cleared by plain read)", rn in cap(bcast.cmd_read, rB))
check("room: --read shows the body", "lets sync in here" in cap(bcast.cmd_room, rB, [rn, "--read"]))
check("room: knock CLEARED after --read", rn not in cap(bcast.cmd_read, rB))
# bidirectional: creator gets a knock, sees the reply on --read
cap(bcast.cmd_room, rB, [rn, "ack, syncing"])
check("room: bidirectional creator gets a knock", rn in cap(bcast.cmd_read, rA))
check("room: creator --read shows reply", "ack, syncing" in cap(bcast.cmd_room, rA, [rn, "--read"]))
# non-member rm3 gets NO knock, but CAN --read (transparent)
_r3 = cap(bcast.cmd_read, rC)
check("room: non-member gets no knock", (rn not in _r3) and ("lets sync in here" not in _r3))
check("room: ANY chat may --read (transparent)",
      "lets sync in here" in cap(bcast.cmd_room, rC, [rn, "--read"]))
# NO POLLUTION: the room message must never touch the joint or team boards
_joint_txt = open(os.path.join(TMP, "bulletin_joint.jsonl"), encoding="utf-8").read() if os.path.exists(os.path.join(TMP, "bulletin_joint.jsonl")) else ""
check("room: message does NOT pollute the joint board", "lets sync in here" not in _joint_txt)
# grow the room: add rm3, it now gets a knock for new messages
cap(bcast.cmd_room, rA, [rn, "--add", "rm3"])
cap(bcast.cmd_room, rA, [rn, "welcome rm3"])
_r3b = cap(bcast.cmd_read, rC)
check("room: added member now gets a knock", (rn in _r3b) and ("welcome rm3" not in _r3b))
# REMOVE / LEAVE (2026-07-07)
cap(bcast.cmd_room, rA, [rn, "--remove", "rm3"])
_mem = cap(bcast.cmd_room, rC, [rn, "--read"]).split("members:")[1].split("===")[0]
check("room: --remove drops a member", ("rm3" not in _mem) and ("rm1" in _mem))
cap(bcast.cmd_room, rB, [rn, "--leave"])
_mem2 = cap(bcast.cmd_room, rA, [rn, "--read"]).split("members:")[1].split("===")[0]
check("room: --leave removes self", "rm2" not in _mem2)

# ======================================================================
# EMOJI SIGNATURE (removed 2026-07-07, RESTORED 2026-07-13 per Max - he needs
# each reply led by the session's icon+id to tell his many chats apart)
# ======================================================================
check("signature() = one icon + the id", bcast._signature("c16").endswith(" c16") and bcast._signature("c16") != "c16")
check("signature is deterministic per id", bcast._signature("c16") == bcast._signature("c16"))
check("forked id c16b keeps its own tag", bcast._signature("c16b").endswith(" c16b"))
check("whoami output carries the emoji tag", "SIGNATURE" in cap(bcast.cmd_whoami, cwd("s_nosig"), "z9"))

# ======================================================================
# LEAK GUARD - the suite must NOT have touched the live state dir
# ======================================================================
_live_after = set(os.listdir(LIVE_STATE)) if os.path.isdir(LIVE_STATE) else set()
check("LEAK GUARD: live state dir untouched (no new files)",
      _live_after == _live_before)

print("\nRESULT:", "ALL PASS" if not fails else f"{len(fails)} FAILED: {fails}")
shutil.rmtree(TMP, ignore_errors=True)
sys.exit(1 if fails else 0)
