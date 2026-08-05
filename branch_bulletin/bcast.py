#!/usr/bin/env python3
"""
bcast.py - local broadcast bulletin for coordinating sibling Claude branches.

Pure broadcast: one branch shouts, every OTHER branch hears it on its next turn.
No locking, no conflict logic. Just an append-only shared log + per-branch cursor.

Branch identity is set manually by Max ("you are b2") and stored keyed by the
branch's working directory (each worktree = its own cwd = its own identity).

Commands:
  python bcast.py whoami b2          set THIS branch's id to b2 (run once per session)
  python bcast.py post "message"     shout to your team; a cross-team @mention
                                     auto-routes to joint, own-team stays on team board
                                     (a --joint post naming no cross-team id is
                                     CHALLENGED - you may be polluting the shared board)
  python bcast.py post --all "msg"   broadcast to ALL teams (the only force-joint verb)
  python bcast.py post --as G2 "msg" post under an EXPLICIT id from any cwd (escape for
                                     posting from a shared cwd, e.g. the main checkout).
                                     A post whose leading self-id ('G2 -> ...') disagrees
                                     with the cwd's registered id is REFUSED as a likely
                                     cd mis-attribution - cd back or use --as.
  python bcast.py room <name> "msg"  post to a ROOM - an N-way side-channel OFF the
                                     team/joint boards (the third layer). Members get
                                     only a KNOCK that unread msgs exist and must OPEN
                                     it with `--read` to see them (NOT auto-loaded).
                                     `--with <id>` adds a partner (auto-names a pairwise
                                     room), `--add <id>` grows it, `--read [N]` shows
                                     history + clears your knock (ANY chat may read).
  python bcast.py rooms              list all rooms + their members (transparency view)
  python bcast.py dedupe [--apply]   ONE-SHOT sweep: resolve EVERY existing duplicate
                                     id at once (keep the freshest, auto-stamp the
                                     rest b/c/d). Dry-run without --apply. [Nhours]
                                     overrides the 24h "recently active" window.
  python bcast.py pin "rule"         PIN a standing rule to the TOP of your team
                                     board (--board <letter> targets another board,
                                     --joint pins for ALL teams). A pin re-shows at
                                     the top of the board EVERY turn until unpinned.
                                     MAX-ONLY: pin only when Max explicitly says to.
  python bcast.py unpin <id|--all>   remove a pin (id from `pins`); same --board/--joint
  python bcast.py pins               list current pins (your team board + joint)
  python bcast.py read               print messages from OTHER branches not yet seen
  python bcast.py read --hook        same, but reads cwd from hook stdin JSON (UserPromptSubmit)
  python bcast.py catchup [N]        print last N board entries (default 12) WITHOUT moving
                                     the cursor - use right after whoami to pull standing
                                     orders posted before you were named (read can't see them)
  python bcast.py standby "reason"   PAUSE work but workers KEEP their 4-min timers
                                     (stay reachable + auto-resume when cleared)
  python bcast.py halt "reason"      FULL halt: stop work AND stop timers (go quiet)
  python bcast.py resume             clear a standby/halt
  python bcast.py log                print the whole bulletin (debug)
  python bcast.py who                show this branch's id

Workers are PEERS by default - NO self-wake timer. You hear the board every turn
you take, so coordination is automatic; just do your part and MERGE+PUSH when
it's done. Arm a 4-min self-wake (ScheduleWakeup ~240s, sentinel
<<autonomous-loop-dynamic>>) ONLY when Max says "run autonomous" - i.e. you must
keep grinding while nobody is prompting you. In that autonomous mode re-arm every
wake; the heartbeat + two-mode halt keep that timer alive.

Fails open everywhere: a broken bulletin must never wedge a session.
"""
import sys, os, json, time, hashlib, re

# Windows consoles default to a legacy codepage (cp1251/charmap) that cannot
# encode Cyrillic (e.g. the ё char) - printing board entries then crashes.
# Force UTF-8 on our streams so catchup/read never choke on Russian text.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Injected by whoami when a branch registers as b1/manager - the core manager
# duties so a manager is NEVER named without instructions (the 2026-06-07
# disaster: a b1 with no playbook did all the work solo while siblings collided).
MANAGER_CORE = """
=== YOU ARE THE MANAGER (b1) - CORE INSTRUCTIONS ===
Your job is to COORDINATE, not to do the bulk of the work yourself.
1. CATCH UP FIRST: run `bcast.py catchup` to see standing orders posted before
   you were named (whoami pinned your cursor to 'now', so `read` won't show them).
2. DEFINE THE SPLIT + ASSIGN FILE/RESOURCE OWNERS *before* anyone edits. Brief
   EVERY named branch in one board message: each gets a crisp task AND the files
   it exclusively owns. Nobody edits a file they don't own. This is your #1 duty.
3. KNOW YOUR WORKERS: track who exists, what each is doing, and roughly HOW MUCH
   TIME is left until each is done. A worker you can't account for is about to
   drop off. Branching exists to SAVE TIME (parallel work) and CUT context cost -
   don't waste that by losing track.
4. RIGHT-SIZE TASKS: never hand a worker a task too large. Time is of the
   essence. Split big work into bounded pieces, then reassess.
5. SCALE THE TEAM: ask Max to create MORE workers when needed instead of
   overloading the few you have. Ask b0 for advice (usually free) on load/risk.
6. SAMPLE - TWO WAYS: (a) DESIGN TASKS as iterations of sampling, not one huge
   survey - cheaper, faster, you learn between rounds. (b) SELF-TEST EVERY CYCLE:
   do NOT rely on worker reports alone - actively sample the LIVE product
   yourself (fetch the live bytes, run real user queries, spot-check a handful of
   rows/results) to catch real bugs early. Light self-sampling is the MANAGER's
   job; exhaustive/repetitive verification stays delegated to the tester. (Max
   proved it: leaning on a worker report + a cache excuse missed a real 27% bug
   that a 30-second live self-sample exposed instantly.)
7. DELEGATE the heavy/parallel work; keep yourself light. If you catch yourself
   doing a worker's job, hand it off.
8. CLOSE THE LOOP: after edits land, confirm `git status` is clean and no
   conflicting copies sit in sibling worktrees. Resolve role/label conflicts.
9. PAUSES: use `standby "reason"` for a temporary break (keeps timers, auto-
   resumes); `halt "reason"` only for a full stop. `resume` clears either.
Full playbook: skill `bcast` -> MANAGER PLAYBOOK.
=== end manager core ===""".rstrip()

# BASE can be overridden via env (BCAST_BASE) so the split-board feature can be
# built and tested in an ISOLATED temp directory without ever touching the live
# board the b-team is using. Live sessions set no env -> real BASE.
BASE = os.environ.get("BCAST_BASE") or r"C:\claude_base\branch_bulletin"
BULLETIN = os.path.join(BASE, "bulletin.jsonl")
STATE_DIR = os.path.join(BASE, "state")
HALT_FILE = os.path.join(BASE, "shared", "HALT.txt")
JOINT_BOARD = os.path.join(BASE, "bulletin_joint.jsonl")

# --- STABLE SESSION IDENTITY (fix for the cwd-collision number swap, 2026-06-30) -
# Identity USED to be keyed only by the working directory. Two chats sharing a
# folder (e.g. both run from the main C:\moma checkout, or both from the bcast tool
# dir) shared ONE state file, so whoever ran whoami last set the id and the other
# read it back -> exactly the D60<->D53 number swap Max reported. The stable Claude
# session_id is the correct key: unique per chat, unchanged when a chat cd's.
# The session_id is only on the `read --hook` stdin, so the hook leaves an "owner
# pointer" (cwd -> session_id + timestamp) that the SAME chat's manual commands
# (whoami/post/who) read back IN THE SAME TURN - the UserPromptSubmit hook always
# fires just before the chat acts. With no fresh owner pointer (no hook wired, e.g.
# a non-Pine machine) we fall back to the legacy cwd keying: byte-identical to the
# old behaviour, so this degrades safely everywhere.
_SESSION_ID = None      # this process's resolved Claude session_id, or None
_SESSION_KEY = None     # state-file key derived from it, or None -> use cwd key
OWNER_FRESH_SEC = 180   # an owner pointer is trusted only this fresh (same-turn)
OWNER_DIR = os.path.join(STATE_DIR, "owners")  # subfolder: no STATE_DIR scanner sees it

# GRADUAL RETIREMENT: board entries older than this roll off to an on-demand
# archive (BASE/archive/<board>.archive.jsonl) so a growing board stops
# contaminating every session's auto-loaded context. The archive is NEVER
# auto-read - only `bcast.py archive` surfaces it. Safe because retired entries
# are the OLDEST (immutable, already behind every live cursor) and they move to
# a file no cursor indexes, so unlike a cross-board migration there is zero
# re-surface risk; cursors just shift down by the count removed (Max 2026-06-25).
RETENTION_DAYS = 5   # Max 2026-07-03: archive board entries older than 5 days
# ROOMS: N-way side-channels that live OFF the team/joint boards (see the ROOMS
# section below). One subfolder, one file per room + a small member manifest.
ROOMS_DIR = os.path.join(BASE, "rooms")
# When a room injects its content each turn (Max 2026-07-14: rooms + boards both
# INJECT and are for BROADCASTS; back-and-forth goes to DIRECT 1:1 pair rooms),
# cap the one-time backlog burst so flipping an old busy room on can't dump
# hundreds of lines at once. Older-than-cap messages are still openable with --read.
ROOM_INJECT_CAP = 20
# CUTOVER GATE: split-per-team boards are OFF until this flag file exists. While
# OFF, behaviour is byte-identical to the old single-board bcast (zero risk to
# the live b-team). `bcast.py migrate` creates the flag - run only on Max's go,
# when the b-team is idle.
SPLIT_FLAG = os.path.join(BASE, "SPLIT_BOARDS.on")


def _split_on():
    try:
        return os.path.exists(SPLIT_FLAG)
    except Exception:
        return False


def _team_of(bid):
    """Team = the leading letter(s) of an id. b1->b, c5->c, d2->d. Fail-safe to
    'misc' for an id with no leading letter."""
    m = re.match(r"[A-Za-z]+", bid or "")
    return m.group(0).lower() if m else "misc"


def _id_eq(a, b):
    """bcast ids are CASE-INSENSITIVE. _team_of already lowercases the team
    letter, so 'D53' and 'd53' are the SAME logical session - they must compare
    equal. Matching them case-sensitively was the 2026-06-30 bug: a session
    registered as live 'd53' could not be force-woken via `wake --name D53`
    because the only exact 'D53' state file was a stale dead twin."""
    return (a or "").strip().lower() == (b or "").strip().lower()


# --- ID ALIASES (2026-07-16): a renamed session stays reachable by its OLD name ---
# The dedupe/whoami auto-demote renames a colliding live session (X7A -> X7Ab) to
# stop the two-managers watcher spam. But that silently BROKE force-wakes: a wake
# aimed at 'X7A' (the name Max/the sender remembers) exact-matched nothing, so an
# ALIVE renamed session became unaddressable ("can't wake an active session", Max
# 2026-07-16). Fix: at demote time we remember the id the session is losing as an
# `aka`, and wake-matching accepts a session's id OR any of its akas. No fragile
# suffix-stripping - the lineage is recorded explicitly, so custom names (b15merger)
# are never mangled. A wake to any name in a session's lineage reaches the live twin.
def _akas_of(st):
    """Prior ids this session was auto-renamed away from (recorded at demote)."""
    v = st.get("aka") if isinstance(st, dict) else None
    return [x for x in v if x] if isinstance(v, list) else []


def _record_aka(hst, old_id):
    """Remember old_id as an alias of this session: front of the list, deduped
    (case-insensitive), capped. Chains across repeated demotes (X7A->X7Ab->X7Ac
    keeps BOTH X7A and X7Ab reachable). No-op if old_id is empty/already the id."""
    if not old_id or not isinstance(hst, dict):
        return
    aka = [x for x in _akas_of(hst) if not _id_eq(x, old_id)]
    aka.insert(0, old_id)
    hst["aka"] = aka[:8]


# --- VISUAL SIGNATURE: RESTORED 2026-07-13 (Max) ---
# Max wants sessions to report their identity in every reply again, WITH the
# per-chat emoji. It was removed 2026-07-07 (TTS can't pronounce emoji), but Max
# re-requested it 2026-07-13: he manually types the chat name he SEES at the top,
# and it often disagrees with what the session actually calls itself - so he needs
# each reply led by the session's real id + its stable icon to tell his many chats
# apart. ONE pretty emoji per chat, picked deterministically by hashing the id, so
# it is stable across a chat's turns and (almost always) differs between chats. The
# literal id still labels the tag, so a rare icon collision stays unambiguous.
SIG_POOL = [
    "❤️", "⭐",                                # heart, star
    "\U0001F53A", "\U0001F537", "\U0001F53B", "\U0001F536", "\U0001F538",  # shapes
    "\U0001F7E5", "\U0001F7E6", "\U0001F7E9", "\U0001F7E8",  # colored squares
    "\U0001F7E7", "\U0001F7EA", "\U0001F7EB",
    "\U0001F319", "\U0001F338", "\U0001F514", "\U0001F511",  # objects + nature
    "\U0001F3B2", "\U0001F3AF", "\U0001F98B", "\U0001F41A",
    "\U0001F341", "\U0001F335", "\U0001F388", "\U0001F9E9",
    "\U0001FA90", "\U0001F33B", "\U0001F352", "\U0001F40C",
    "\U0001F989", "\U0001F33D", "\U0001FA81", "\U0001F9ED",
    "\U0001FA97", "\U0001F349", "\U0001F41D", "\U0001F420",
]


def _signature(bid, salt=None):
    """One pretty icon + the bcast id, e.g. "🍉 E35". Deterministic from the id
    alone (salt accepted for call-site compatibility but ignored)."""
    if not bid:
        return ""
    h = int(hashlib.md5(bid.strip().lower().encode("utf-8")).hexdigest(), 16)
    return f"{SIG_POOL[h % len(SIG_POOL)]} {bid}"


def _team_board(team):
    return os.path.join(BASE, f"bulletin_{team}.jsonl")


def _board_for(bid):
    """The board a given id posts to / hears its own team on."""
    return _team_board(_team_of(bid))


# A session is presumed LIVE if its state file was touched within this window
# (state is rewritten on every board read, so mtime ~= last activity). 8 min =
# two missed 4-min heartbeats, matching the liveness window in the fix-list.
LIVENESS_WINDOW_SEC = 8 * 60

# --- TEAM WAKE (selective force-wake of teammates) ----------------------------
# A session that needs help can WAKE teammates: either everyone on its team who
# was active within a look-back window, or specific ids by name. The wake is a
# persistent REQUEST dropped in WAKE_DIR; the bcast read-hook FORCES it into a
# target session's context the moment that session next takes ANY turn (its own
# timer firing, Max prompting it, or its heartbeat). There is no way to wake a
# session that holds no armed timer and is never prompted - that's a platform
# limit, not a fallback - so this is loud best-effort delivery, honest about it:
# an asleep teammate gets the call the instant it next acts, within the TTL.
WAKE_DIR = os.path.join(BASE, "wake")
WAKE_ACTIVE_WINDOW_HOURS = 18   # default look-back for `wake --active`
WAKE_REQUEST_TTL_HOURS = 18     # a request stays deliverable this long, then expires
# A live wake_listener touches its lock every ~5s (REFRESH_SEC) and is treated as
# fresh within 20s (LOCK_FRESH_SEC) by the listener itself. We allow a slightly
# wider margin here: a lock touched within this window == a listener is ACTUALLY
# blocking and WILL catch a dropped signal. Stamped-but-stale session_id (session
# closed, listener exited after its block, or session restarted with a new id)
# leaves an OLD lock -> we must NOT claim "FORCE-WOKEN" for it (that was the b27
# false-positive: signal dropped to a dead session_id, reported as woken). Why a
# lock and not the state mtime: state mtime tracks bcast activity, which does NOT
# prove a listener process is alive; the lock is the listener's own heartbeat.
WAKE_LISTENER_FRESH_SEC = 30
# After dropping a signal we CONFIRM the wake by watching the signal file get
# consumed (a live listener removes it on wake). We poll up to this long so a
# teammate that is alive but momentarily between listener cycles / mid-rearm
# still confirms, instead of being written off as asleep on one stale-lock
# snapshot (the g1 false-negative, 2026-06-21). A live listener polls every ~1s
# and refreshes its lock every ~5s, so this comfortably covers a re-arm turn.
WAKE_CONFIRM_SEC = 14

# AUTO-WAKE-ON-POST (2026-06-30, Max spec): whoever posts on the board pings
# every LIVE wakeable session on that board via _drop_signal, throttled per
# target so a burst of posts within 2 min does not re-wake. Joint post -> pings
# every live wakeable id (any team). Team post -> pings live wakeable ids on the
# same team letter. Sender excluded. A 1-on-1 post (exactly one whole-token
# @-mention of a known id) SKIPS the broadcast wake (still delivers via the
# normal message channel). Fail-open: any error is swallowed so a post never
# breaks. Throttle stamp files live under wake/auto_wake_throttle/.
AUTO_WAKE_THROTTLE_SEC = 120
AUTO_WAKE_THROTTLE_DIR = os.path.join(WAKE_DIR, "auto_wake_throttle")

# On ANY name/rename, backfill this many recent board entries so the session
# AUTOMATICALLY sees recent cross-talk (standing orders, a sibling's earlier
# posts, a brand-new team board it never read) without anyone remembering to run
# `catchup`. Applies to FRESH names too - a freshly-named session starting blind
# is the foot-gun, not a feature. 40 = plenty of context, still a tail not the
# whole log. (2026-06-12: B9<-D9 switched team d->b and saw none of b10's posts.)
WHOAMI_BACKFILL = 40


def _safe_key(cwd):
    norm = os.path.normcase(os.path.abspath(cwd))
    h = hashlib.sha1(norm.encode("utf-8", "replace")).hexdigest()[:10]
    tail = re.sub(r"[^A-Za-z0-9]+", "_", os.path.basename(norm))[-32:]
    return f"{tail}_{h}"


def _norm_cwd(cwd):
    try:
        return os.path.normcase(os.path.abspath(cwd)) if cwd else ""
    except Exception:
        return ""


def _is_worktree(cwd):
    """A git worktree cwd (path contains '.claude/worktrees') is 1:1 with a single
    Claude Code tab. A shared checkout (C:\\claude_base, C:\\moma) is NOT - many
    sessions post from there, so their identities must stay session_id-separated."""
    n = _norm_cwd(cwd)
    sep = os.sep
    return (sep + ".claude" + sep + "worktrees" + sep) in (n + sep)


# --- SESSION-KEYED IDENTITY (2026-06-30 fix for the D60<->D53 number swap) ---
# Identity used to be keyed to the cwd, so two chats sharing a folder (the main
# C:\moma checkout, or this tool's own dir) shared ONE state file and stole each
# other's number. We now key identity to the stable Claude session_id instead.
# The session_id is only handed to us on the read-hook's stdin, so the hook drops
# a short-lived "owner pointer" (cwd -> session_id) that a manual command run in
# the SAME turn reads back (the UserPromptSubmit hook fires before the assistant
# acts). With no fresh pointer (e.g. a machine with no hook wired) we fall back to
# the old cwd keying, so nothing regresses.
def _sess_hash(session_id):
    return "sess_" + hashlib.sha1((session_id or "").encode("utf-8", "replace")).hexdigest()[:16]


def _owner_path(cwd):
    return os.path.join(OWNER_DIR, _safe_key(cwd) + ".json")


def _write_owner(cwd, session_id):
    if not session_id:
        return
    try:
        os.makedirs(OWNER_DIR, exist_ok=True)
        with open(_owner_path(cwd), "w", encoding="utf-8") as f:
            json.dump({"session_id": session_id, "ts": time.time(),
                       "cwd": os.path.abspath(cwd)}, f)
    except Exception:
        pass


def _fresh_owner_sid(cwd):
    """Return the session_id from a FRESH (same-turn) owner pointer for this cwd,
    else None."""
    if not cwd:
        return None
    try:
        with open(_owner_path(cwd), "r", encoding="utf-8") as f:
            o = json.load(f)
        if time.time() - float(o.get("ts", 0)) <= OWNER_FRESH_SEC:
            return o.get("session_id")
    except Exception:
        pass
    return None


def _oldpwd_worktree():
    """Recover the chat's REAL worktree when a manual command `cd`'d before calling
    bcast (a known antipattern the watcher keeps flagging). The Bash tool resets the
    shell cwd to the chat's worktree before each command, so after `cd X` the env var
    $OLDPWD holds exactly that worktree. Git-bash writes it POSIX-style
    (/c/claude_base/...), so convert it to a Windows path to match owner-pointer keys.
    Deterministic (no cross-session race): OLDPWD is THIS shell's prior dir, nobody
    else's. Returns a path string or None."""
    op = os.environ.get("OLDPWD")
    if not op:
        return None
    cands = [op]
    m = re.match(r"^/([A-Za-z])/(.*)$", op)        # /c/foo/bar -> C:\foo\bar
    if m:
        cands.append(m.group(1).upper() + ":\\" + m.group(2).replace("/", "\\"))
    return cands


def _sid_from_transcript(cwd):
    """Deterministically recover a worktree's LIVE Claude session_id from its
    transcript file, for builds whose hook payload omits session_id (seen 2026-07-02:
    C12A/E45 ran the read-hook every turn but never got stamped -> UNWAKEABLE).
    Claude Code stores transcripts at
    ~/.claude/projects/<abspath-with-nonalnum->->/<session_id>.jsonl; the .jsonl
    filename IS the session_id, and the NEWEST one (being written this turn) is the
    live session. Worktree-only: a worktree is 1:1 with a tab so 'newest' is
    unambiguous; a SHARED checkout hosts many tabs so we never guess there."""
    if not cwd or not _is_worktree(cwd):
        return None
    try:
        enc = re.sub(r"[^A-Za-z0-9]", "-", os.path.abspath(cwd))
        proj = os.path.join(os.path.expanduser("~"), ".claude", "projects", enc)
        js = [os.path.join(proj, fn) for fn in os.listdir(proj) if fn.endswith(".jsonl")]
        if not js:
            return None
        newest = max(js, key=os.path.getmtime)
        # only trust a FRESH transcript (this session is actually live now)
        if time.time() - os.path.getmtime(newest) > LIVENESS_WINDOW_SEC:
            return None
        return os.path.basename(newest)[:-len(".jsonl")]
    except Exception:
        return None


def _resolve_session(cwd, session_id=None):
    """Set this process's _SESSION_ID / _SESSION_KEY. Prefer the id handed in
    (read-hook), else a FRESH owner pointer this turn's hook just wrote. If the
    caller `cd`'d (so this cwd has no pointer) recover identity from $OLDPWD = the
    real worktree. Still nothing -> derive it from the worktree's transcript file
    (covers builds that don't pass session_id to the hook). No source at all ->
    stay on legacy cwd keying."""
    global _SESSION_ID, _SESSION_KEY
    sid = session_id
    if not sid:
        sid = _fresh_owner_sid(cwd)
    if not sid:
        for alt in (_oldpwd_worktree() or []):
            sid = _fresh_owner_sid(alt)
            if sid:
                break
    if not sid:
        sid = _sid_from_transcript(cwd)
        if not sid:
            for alt in (_oldpwd_worktree() or []):
                sid = _sid_from_transcript(alt)
                if sid:
                    break
    if sid:
        _SESSION_ID = sid
        _SESSION_KEY = _sess_hash(sid)
    return _SESSION_ID


def _live_holders(target_id, exclude_key, my_cwd=None):
    """Other sessions whose id == target_id and whose state was touched within the
    liveness window. Used to catch a session adopting an id/role another LIVE
    session already holds (the 2026-06-08 two-manager collision class).
    exclude_key may be a single key or a set of keys (our own state files).

    NOT a collision (2026-07-02): a state file that shares OUR worktree cwd is the
    SAME physical tab whose Claude session_id churned (resume/restart/branch gave it
    a fresh hidden UUID). Max never clones ids; the phantom 'two live E125' was one
    tab split across a session_id boundary. So we skip same-worktree holders."""
    excl = exclude_key if isinstance(exclude_key, (set, frozenset, list, tuple)) else {exclude_key}
    excl = set(excl)
    my_n = _norm_cwd(my_cwd)
    out = []
    try:
        for fn in os.listdir(STATE_DIR):
            if not fn.endswith(".json") or fn[:-5] in excl:
                continue
            p = os.path.join(STATE_DIR, fn)
            try:
                with open(p, "r", encoding="utf-8") as f:
                    st = json.load(f)
            except Exception:
                continue
            # never count ourselves, even under a different filename
            if _SESSION_ID and st.get("session_id") == _SESSION_ID:
                continue
            # same worktree = same tab whose session_id churned, not a rival
            if my_n and _is_worktree(my_n) and _norm_cwd(st.get("cwd")) == my_n:
                continue
            if not _id_eq(st.get("id"), target_id):
                continue
            try:
                age = time.time() - os.path.getmtime(p)
            except Exception:
                continue
            if age <= LIVENESS_WINDOW_SEC:
                out.append(age)
    except Exception:
        pass
    return out


def _live_holder_files(target_id, exclude_key, my_cwd=None):
    """Like _live_holders but returns [{'path','age','st'}] for each OTHER live
    session holding target_id - so the caller can auto-demote them (rename their
    state id). Same exclusion rules as _live_holders (never self, never our own
    churned session_id, never same-worktree)."""
    excl = exclude_key if isinstance(exclude_key, (set, frozenset, list, tuple)) else {exclude_key}
    excl = set(excl)
    my_n = _norm_cwd(my_cwd)
    out = []
    try:
        for fn in os.listdir(STATE_DIR):
            if not fn.endswith(".json") or fn[:-5] in excl:
                continue
            p = os.path.join(STATE_DIR, fn)
            try:
                with open(p, "r", encoding="utf-8") as f:
                    st = json.load(f)
            except Exception:
                continue
            if _SESSION_ID and st.get("session_id") == _SESSION_ID:
                continue
            if my_n and _is_worktree(my_n) and _norm_cwd(st.get("cwd")) == my_n:
                continue
            if not _id_eq(st.get("id"), target_id):
                continue
            try:
                age = time.time() - os.path.getmtime(p)
            except Exception:
                continue
            if age <= LIVENESS_WINDOW_SEC:
                out.append({"path": p, "age": age, "st": st})
    except Exception:
        pass
    return out


def _next_free_suffix(base_id, taken=None):
    """First free 'stamped' id for base_id: base+'b', base+'c', ... skipping any id
    already registered anywhere (case-insensitive) or in `taken`. Max's mental
    model: a bare name is his; a collision auto-stamps the loser so both survive
    and stay distinct forever."""
    taken = set(x.lower() for x in (taken or set()))
    known = set(x.lower() for x in _known_ids())
    # 'b'..'z', then 'b2'.. as a safety valve for the absurd case
    import string
    for ch in string.ascii_lowercase[1:]:
        cand = f"{base_id}{ch}"
        if cand.lower() not in known and cand.lower() not in taken:
            return cand
    n = 2
    while True:
        cand = f"{base_id}b{n}"
        if cand.lower() not in known and cand.lower() not in taken:
            return cand
        n += 1


def _known_ids():
    """Every bcast id currently registered in a state file (live or stale),
    mapped lowercased -> canonical. @-mention routing resolves against THESE real
    ids, not a blind letter+digit regex. The old regex r'\\b([A-Za-z]\\d+)\\b'
    had TWO defects that made cross-team routing inconsistent (b15merger + b26
    reports, 2026-06-18): (a) it MISSED long ids like 'B26juniorconnector' - the
    \\b after the digits fails when a letter immediately follows, so a genuine
    cross-team @mention was never detected and the post stayed on the wrong team
    board; (b) it INVENTED phantom teams from version strings and stray tokens
    ('v01' -> team 'v', 'R7'/'preR7' -> team 'r'), so OTHER posts spuriously
    auto-routed to joint. Same @mention -> different routing depending on whether
    the body happened to contain a version string. Resolving against the real id
    set kills both."""
    out = {}
    try:
        for fn in os.listdir(STATE_DIR):
            if not fn.endswith(".json"):
                continue
            try:
                with open(os.path.join(STATE_DIR, fn), "r", encoding="utf-8") as f:
                    iid = (json.load(f).get("id") or "").strip()
            except Exception:
                continue
            if iid:
                out[iid.lower()] = iid
    except Exception:
        pass
    return out


def _mentioned_ids(me, msg):
    """Registered ids ADDRESSED in msg via an explicit '@' prefix (case-insensitive),
    excluding the sender's own id.

    ADDRESSING REQUIRES '@' (Max 2026-07-03). Previously a BARE whole-token match
    counted ('D8 -> B9' addressed b9), but that silently auto-promoted innocent
    single-team posts onto the joint board: ordinary technical text is full of tokens
    that collide with tiny ids - 'F_ROH', 'F1', 'F2', 'chrX' all matched a live f/x
    id, so a genomics session writing to its OWN team got force-routed to joint and
    then nagged to 'move' a post it never chose to send there (x1's diagnosis, the #1
    pollution source). Now ONLY '@f4' addresses f4; bare 'F1' in prose does not. To
    reach another team you @-mention them (or use --all/--joint for a global post).
    '@'-left-delimited, right-bounded by a non-alphanumeric so '@f4x' matches its own
    token, not '@f4'."""
    low = (msg or "").lower()
    meL = (me or "").lower()
    hits = set()
    for lid, canon in _known_ids().items():
        if lid == meL:
            continue
        if re.search(r"@" + re.escape(lid) + r"(?![a-z0-9])", low):
            hits.add(canon)
    return hits


def _leading_self_id(msg):
    """The id a message attributes ITSELF to, by the 'from X' convention of prefixing
    a post with your own id AND a separator: 'G2 -> @G3 ...', 'b15merger: status',
    'c16 = note'. Returns that leading id token, or None.

    REQUIRES the separator ('->', ':', '='). That is what distinguishes a SELF claim
    ('G2 -> ...' = from G2) from merely ADDRESSING a sibling by a bare name
    ('b1 freeze please' = 'b1, please freeze') - the latter must NOT be read as
    'from b1' or a legit address-without-@ gets wrongly refused. An '@'-prefixed
    leading token ('@G3 ...') is addressing too, so it never matches.

    Used to catch the silent cd mis-attribution (2026-06-19): a worktree session that
    cd's into the shared main checkout to commit then posts in the same chain gets
    attributed to the main checkout's id (G2's post went out as 'b29'). The leading
    self-id ('G2') disagreeing with the cwd's registered id ('b29') is the tell."""
    m = re.match(r"\s*([A-Za-z]+\d+[A-Za-z]*)\s*(?:->|:|=)", msg or "")
    return m.group(1) if m else None


def _names_other_team(me, msg):
    """Teams (other than the sender's own) @-ADDRESSED in the message (see
    _mentioned_ids, now '@'-only). A plain post that @-addresses a cross-team sibling
    (e.g. 'D8 -> @B9 ...') auto-promotes to joint so the target actually reads it.
    Returns the set of foreign team letters, e.g. {'b'}; empty set = none.
    (2026-06-13 B9<->D8 silence + 2026-06-18 long-id/version noise = fixed by
    resolving against _known_ids; 2026-07-03 the bare-token false-promote that
    polluted joint = fixed by requiring '@'.)"""
    mine = _team_of(me)
    return {_team_of(i) for i in _mentioned_ids(me, msg)} - {mine}


# ---- POLLUTION GATE: semantic check on explicit-global posts (Max 2026-07-03) ----
# A session can force a post onto the joint board with --all/--joint. Sessions ABUSE
# this by SELF-CERTIFYING their own team's work as "genuinely global, trust me" and
# leaking single-team docs to every team (the trigger: an X-team alignment POSTMORTEM
# self-labeled "cross-team, genuinely global" landed on joint). Only content judgment
# separates a real all-teams announcement ("master frozen", "asto down") from one
# team's work product (status/postmortem/handoff/lessons about that team's own task).
# So an explicit-global post that @-mentions NO other team is gated through a quick
# DeepSeek check at POST TIME - the only lever that PREVENTS the leak, because an
# append-only board cannot be un-posted after the fact. Plain posts never reach here
# (zero LLM cost); a genuinely cross-team post (@-mentions another team) SKIPS the gate.
# FAIL-OPEN everywhere: missing key / disabled flag / any error / timeout -> allow
# joint, so a broken or slow gate never blocks real coordination.
GATE_DISABLE_FLAG = os.path.join(BASE, "joint_gate.disabled")  # touch to bypass the gate


def _deepseek_key():
    """First non-empty line of the DeepSeek key file, across the per-machine Nextcloud
    layouts (Pine/Sirius/Vega=Nextcloud*, Centauri=D:). None if unreadable (fail-open)."""
    home = os.path.expanduser("~")
    for base in (os.path.join(home, "Nextcloud"), os.path.join(home, "Nextcloud2"),
                 r"D:\Nextcloud"):
        p = os.path.join(base, "zSyncMain", "ssh", "deepseek_api_key_20260226.txt")
        try:
            with open(p, encoding="utf-8") as f:
                for ln in f:
                    if ln.strip():
                        return ln.strip()
        except Exception:
            continue
    return None


def _deepseek_chat(prompt, max_tokens=800, timeout=15, retries=1):
    """ONE hardened DeepSeek call for every gate. Returns the reply text, or None on
    failure (caller decides the fail-open behavior). Uses the NON-REASONING model
    'deepseek-chat' on purpose: the reasoning model 'deepseek-v4-flash' spends its token
    budget on hidden reasoning and often returns EMPTY content, which looked like an
    outage 'every other day' (Max 2026-07-10). deepseek-chat answers directly, so a
    small budget still yields content. Retries once on an empty/errored reply so a single
    transient blip does not silently fall through."""
    key = _deepseek_key()
    if not key:
        return None
    import urllib.request
    body = json.dumps({"model": "deepseek-chat", "max_tokens": max_tokens,
                       "messages": [{"role": "user", "content": prompt}],
                       "stream": False}).encode()
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(
                "https://api.deepseek.com/chat/completions", data=body,
                headers={"Authorization": "Bearer " + key,
                         "Content-Type": "application/json"})
            resp = urllib.request.urlopen(req, timeout=timeout).read()
            text = (json.loads(resp)["choices"][0]["message"].get("content") or "").strip()
            if text:
                return text
        except Exception:
            pass
    return None


def _joint_is_genuinely_global(me, msg, timeout=15):
    """DeepSeek gate. True if this explicit-global post genuinely belongs on the joint
    (cross-team) board; False if it is really one team's internal work. FAIL-OPEN:
    returns True on disabled flag / missing key / any error, so it never blocks a post."""
    if os.path.exists(GATE_DISABLE_FLAG):
        return True
    prompt = (
        "A multi-agent system has ONE global board (every team reads it) plus a "
        "private board per team. A session asked to broadcast the message below to "
        "the GLOBAL board. The global board is ONLY for genuinely cross-team content: "
        "an all-teams announcement (e.g. 'master is frozen', a shared server is down) "
        "or coordination that really involves more than one team. One team's INTERNAL "
        "work - a status update, a postmortem, a handoff between same-team sessions, a "
        "lessons/notes doc about that team's own task - does NOT belong on the global "
        "board, EVEN IF the author calls it 'generally useful' or self-labels it "
        "'global'. Sender id: " + str(me) + " (its leading letter is its team).\n\n"
        "MESSAGE:\n" + (msg or "")[:2000] + "\n\nReply ONLY compact JSON: "
        "{\"global\": true|false, \"why\": \"<=10 words\"}. global=true ONLY if it "
        "genuinely needs every team's attention or involves multiple teams.")
    text = _deepseek_chat(prompt, max_tokens=200, timeout=timeout)
    if not text:
        return True  # fail-open
    try:
        s, e = text.find("{"), text.rfind("}")
        if s >= 0 and e > s:
            return bool(json.loads(text[s:e + 1]).get("global", True))  # fail-open field
    except Exception:
        return True
    return True


# BOARD CONTENT GATE (Max 2026-07-10): routine work reports must NOT leak onto a
# board - they belong in the project ROOM. The joint gate above only decides team-vs-
# joint ROUTING; this gate decides whether the content is board-worthy AT ALL. It is a
# HARD refuse at the post chokepoint (an append-only board cannot be un-posted). Only
# DATA/RESOURCE sharing, DANGER alerts, and Max-command relays pass; status/progress/
# postmortem/handoff/method-discussion/conclusions bounce back to the room. FAIL-OPEN
# (DeepSeek down / missing key / any error / timeout -> allow) so a broken gate never
# blocks real coordination. Enabled PER TEAM via a flag file (rollout control), so a
# team keeps posting freely until Max turns its gate on. Touch board_gate.<team>.on.
def _board_gate_on(team):
    """True if the hard content gate is enabled for this team (flag file present)."""
    try:
        return os.path.exists(os.path.join(BASE, "board_gate." + str(team) + ".on"))
    except Exception:
        return False


def _board_worthy(me, msg, timeout=15):
    """DeepSeek gate. (ok, why): ok=True if `msg` genuinely belongs on a shared board;
    False if it is routine per-session work that belongs in the project room. FAIL-OPEN:
    returns (True, ...) on missing key / any error, so it never wrongly blocks a post."""
    if not _deepseek_key():
        return True, "no key (fail-open)"
    try:
        prompt = (
            "A multi-agent system has a shared BOARD (many groups / sub-projects read it) "
            "and private ROOMS (each sub-project's own sessions talk there, off the board). "
            "A session wants to post the message below to the BOARD. THE ONE RULE: the board "
            "is ONLY for things of COMMON USE BETWEEN MULTIPLE GROUPS / SUB-PROJECTS - i.e. "
            "(1) shared DATA / RESOURCES useful to more than one group (file paths, numbers, "
            "distributions, where things live); (2) DANGER alerts that could break machines, "
            "data, or someone's work; (3) a relayed MAX COMMAND. Everything that is one "
            "group's OWN internal work is JUNK on the board and must stay in that group's "
            "ROOM: a status update, progress report, work-log, postmortem, a handoff between "
            "same-group sessions, method/principle discussion, or a conclusion/verdict "
            "(e.g. 'clean negative').\n\n"
            "MESSAGE:\n" + (msg or "")[:2000] + "\n\nReply ONLY compact JSON: "
            "{\"board\": true|false, \"why\": \"<=10 words\"}. board=true ONLY if it is of "
            "common use across multiple groups (shared data/resource), a danger alert, or a "
            "Max command. When genuinely unsure, answer true (fail-open).")
        text = _deepseek_chat(prompt, max_tokens=200, timeout=timeout)
        if not text:
            return True, "gate unreachable (fail-open)"
        s, e = text.find("{"), text.rfind("}")
        if s >= 0 and e > s:
            obj = json.loads(text[s:e + 1])
            return bool(obj.get("board", True)), str(obj.get("why", ""))[:60]
    except Exception:
        return True, "gate error (fail-open)"
    return True, "unparsed (fail-open)"


# REPEAT-OFFENSE ESCALATION (Max 2026-07-10): when a session keeps trying to post junk
# to the board, the refusal must NAG with INCREASINGLY STRICTER language - and the nag
# itself is written by DeepSeek flash (LLM on the other side), not a canned string. We
# keep a per-session offense counter; each blocked post bumps it and DeepSeek writes an
# order pitched at that severity. A CLEAN (passed) post resets the session to zero.
_OFFENSE_FILE = os.path.join(BASE, "board_gate_offenses.json")


def _offenses_load():
    try:
        with open(_OFFENSE_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _offense_bump(me):
    """Increment and persist this session's offense count; return the new count."""
    d = _offenses_load()
    n = int(d.get(me, 0)) + 1
    d[me] = n
    try:
        with open(_OFFENSE_FILE, "w", encoding="utf-8") as f:
            json.dump(d, f)
    except Exception:
        pass
    return n


def _offense_reset(me):
    """A clean board post wipes the session's strike count (back to civil tone)."""
    d = _offenses_load()
    if d.get(me):
        d[me] = 0
        try:
            with open(_OFFENSE_FILE, "w", encoding="utf-8") as f:
                json.dump(d, f)
        except Exception:
            pass


def _board_refusal_message(me, msg, why, level, room_hint, timeout=15):
    """DeepSeek flash writes the refusal/order, its sternness scaled to `level` (the
    session's running offense count). FAIL-OPEN: on any error, fall back to a plain
    canned order so the post is still refused with clear guidance."""
    fallback = (
        f"REFUSED (strike {level}) - this reads as one group's own work, not board "
        f"material ({why}). The board is ONLY for things of common use across groups, "
        f"danger alerts, or a Max command. Keep this in your room:\n"
        f"     bcast.py room {room_hint} \"...\"\n"
        f"If it TRULY is cross-group/danger/a Max command: bcast.py post --announce \"...\"")
    if not _deepseek_key():
        return fallback
    try:
        tone = ("polite but firm" if level <= 1 else
                "firmer, clearly impatient" if level == 2 else
                "stern and blunt" if level == 3 else
                "very stern, zero-tolerance - this session keeps ignoring the rule")
        prompt = (
            "You are the board gatekeeper in a multi-agent system. A session (id '" +
            str(me) + "') just tried to post JUNK to the shared board - its own internal "
            "work, not something of common use across groups. This is offense number " +
            str(level) + " for this session. Write a SHORT refusal (2-4 sentences, plain "
            "ASCII, no emoji) ORDERING it to keep such work in its private ROOM and to post "
            "ONLY things of common use between multiple groups/sub-projects, danger alerts, "
            "or a relayed Max command. Tone: " + tone + ". Escalate the language with the "
            "offense number - later strikes get blunter and less patient. End with the exact "
            "line: keep it in your room (bcast.py room " + str(room_hint) + " \"...\").\n\n"
            "The junk it tried to post was:\n" + (msg or "")[:800])
        text = _deepseek_chat(prompt, max_tokens=400, timeout=timeout)
        if text:
            return f"REFUSED (strike {level}):\n" + text
    except Exception:
        pass
    return fallback


def _state_path(cwd):
    if _SESSION_KEY:
        return os.path.join(STATE_DIR, _SESSION_KEY + ".json")
    return os.path.join(STATE_DIR, _safe_key(cwd) + ".json")


def _load_state(cwd):
    p = _state_path(cwd)
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        pass
    # MIGRATION: first run under a new session key. Inherit the legacy cwd-keyed
    # state (so an existing chat keeps its number through the deploy) -- but only
    # if that legacy file is NOT already owned by some OTHER live session (guard:
    # session_id is unset or already ours). Refusing a foreign id is what keeps a
    # shared-folder sibling from being adopted.
    if _SESSION_KEY:
        try:
            lp = os.path.join(STATE_DIR, _safe_key(cwd) + ".json")
            with open(lp, "r", encoding="utf-8") as f:
                lst = json.load(f)
            if lst.get("id") and lst.get("session_id") in (None, "", _SESSION_ID):
                return lst
        except Exception:
            pass
    return {"id": None, "cursor": 0}


def _save_state(cwd, st):
    os.makedirs(STATE_DIR, exist_ok=True)
    # Record the real working directory so tools keyed only by the cwd-hash
    # (e.g. the safety watcher's git eye) can reach the session's actual folder.
    st["cwd"] = os.path.abspath(cwd)
    if _SESSION_ID:
        st["session_id"] = _SESSION_ID
    mine = _state_path(cwd)
    with open(mine, "w", encoding="utf-8") as f:
        json.dump(st, f)
    _retire_stale_twins(cwd, mine)


def _retire_stale_twins(cwd, keep_path):
    """One worktree hosts exactly ONE live tab, so any OTHER state file sharing our
    worktree cwd is a stale twin left behind when this tab's Claude session_id
    churned (resume/restart/branch). Delete it so the phantom 'two live <id>' can
    never form again. Only for worktree cwds - a SHARED checkout (C:\\claude_base,
    C:\\moma) legitimately hosts many sessions, so we never touch those."""
    if not _is_worktree(cwd):
        return
    my_n = _norm_cwd(cwd)
    keep = os.path.normcase(os.path.abspath(keep_path))
    try:
        for fn in os.listdir(STATE_DIR):
            if not fn.endswith(".json"):
                continue
            p = os.path.join(STATE_DIR, fn)
            if os.path.normcase(os.path.abspath(p)) == keep:
                continue
            try:
                with open(p, "r", encoding="utf-8") as f:
                    other = json.load(f)
            except Exception:
                continue
            if _norm_cwd(other.get("cwd")) == my_n:
                try:
                    os.remove(p)
                except Exception:
                    pass
    except Exception:
        pass


def _read_lines(path=None):
    try:
        with open(path or BULLETIN, "r", encoding="utf-8") as f:
            return [l for l in f.read().splitlines() if l.strip()]
    except Exception:
        return []


def _parse(lines):
    out = []
    for l in lines:
        try:
            out.append(json.loads(l))
        except Exception:
            continue
    return out


def _my_boards(me):
    """In split mode a worker hears its own team board + the joint board."""
    return {"team": _board_for(me), "joint": JOINT_BOARD}


def _append_rec(path, me, msg):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    rec = {"ts": time.strftime("%Y-%m-%d %H:%M:%S"), "from": me, "msg": msg}
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=True) + "\n")


# --- ANTI-SPAM GATE for the unattended watchers (Max, 2026-07-13) --------------
# Root cause of the "safety bots spamming every board" complaint: both watchers
# (safety_watcher.py + watcher.py) re-posted the SAME unresolved nag on a flat
# 20-30 min cooldown with NO backoff and NO give-up. A problem nobody can/will
# fix (a duplicate session id open for days, a disk-cleanup proposal) therefore
# got re-nagged 8-13 times per board. Worse, the per-nag dedup key is an
# LLM-generated slug that DRIFTS run to run, so even the weak cooldown slipped.
#
# This gate is the ONE place a watcher asks "may I (re-)post about this thing?".
# Three layers, all deterministic (no LLM prose in the gate math):
#   1. per-key EXPONENTIAL BACKOFF: gaps grow 30m -> 1h -> 2h ... capped at 6h,
#      so a lingering issue is mentioned rarely, not every sweep.
#   2. per-key GIVE-UP CAP: after KEY_MAX_POSTS mentions the board goes SILENT on
#      that key. Nagging a thing 3 times over ~7h with no action proves more nags
#      are pure noise; real DANGER still reaches Max via the separate Telegram
#      page path (this gate covers only board chatter, never the Max page).
#   3. per-board DAILY CAP: a blunt backstop that survives key drift - at most
#      BOARD_DAILY_CAP watcher posts land on any one board per day, period.
# A key that has been quiet for KEY_RESET_QUIET_SEC is treated as fresh (a truly
# resolved-then-recurred problem may alert again, but the daily cap still bounds
# it). Fail-OPEN: any error -> allow the post (a broken gate must never mute a
# genuine safety message).
REPOST_LEDGER = os.path.join(BASE, "watcher_repost_ledger.json")
REPOST_BASE_SEC = 30 * 60        # first re-post gap
REPOST_MAX_SEC = 6 * 3600        # cap the growing gap at 6h
KEY_MAX_POSTS = 2                # give up nagging one key after this many posts
BOARD_DAILY_CAP = 2             # max watcher posts on one board per day (drift backstop)
KEY_RESET_QUIET_SEC = 24 * 3600  # a key quiet this long is treated as new again


def should_repost(board, key, now=None):
    """Return True if a watcher may (re-)post about `key` on `board` right now,
    recording the decision. `board` = board name ('g','d','joint'...); `key` =
    the problem slug. Fail-open (returns True) on any internal error."""
    if now is None:
        now = time.time()
    try:
        try:
            with open(REPOST_LEDGER, "r", encoding="utf-8") as f:
                led = json.load(f)
        except Exception:
            led = {}
        b = led.setdefault(board, {"day": "", "day_count": 0, "keys": {}})
        today = time.strftime("%Y-%m-%d", time.localtime(now))
        if b.get("day") != today:
            b["day"], b["day_count"] = today, 0
        key = (key or "misc").strip().lower()[:60]
        k = b["keys"].get(key)
        if k and (now - k.get("last", 0)) > KEY_RESET_QUIET_SEC:
            k = None  # long quiet -> resolved-then-recurred, start fresh
        # layer 3: per-board daily backstop (drift-proof)
        if b.get("day_count", 0) >= BOARD_DAILY_CAP:
            return False
        if k is None:
            b["keys"][key] = {"count": 1, "first": now, "last": now}
            b["day_count"] = b.get("day_count", 0) + 1
            _save_repost_ledger(led)
            return True
        # layer 2: give-up cap
        if k.get("count", 0) >= KEY_MAX_POSTS:
            return False
        # layer 1: exponential backoff
        gap = min(REPOST_BASE_SEC * (2 ** (k.get("count", 1) - 1)), REPOST_MAX_SEC)
        if (now - k.get("last", 0)) < gap:
            return False
        k["count"] = k.get("count", 1) + 1
        k["last"] = now
        b["day_count"] = b.get("day_count", 0) + 1
        _save_repost_ledger(led)
        return True
    except Exception:
        return True  # fail-open: never mute a real message on a gate bug


def _save_repost_ledger(led):
    try:
        tmp = REPOST_LEDGER + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(led, f)
        os.replace(tmp, REPOST_LEDGER)
    except Exception:
        pass


# --- PINS: Max's rules stuck to the TOP of a board (Max, 2026-07-07) -----------
# A pin is a short standing rule that a board's sessions must always see. Unlike
# a normal post (heard once, then scrolls off), a pin is re-injected at the TOP
# of the board EVERY turn, so Max's rules never fall out of context. Pins are set
# ONLY on Max's explicit command - a session must not self-pin. Stored per board
# (team letter, or 'joint' for all teams) in pins/<board>.json, tiny + rewritten
# whole on each change. Fail-open: a broken pins file never wedges a read.
PINS_DIR = os.path.join(BASE, "pins")


def _pins_path(board):
    return os.path.join(PINS_DIR, f"{board}.json")


def _load_pins(board):
    try:
        with open(_pins_path(board), "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def _save_pins(board, pins):
    try:
        os.makedirs(PINS_DIR, exist_ok=True)
        with open(_pins_path(board), "w", encoding="utf-8") as f:
            json.dump(pins, f, ensure_ascii=True, indent=1)
        return True
    except Exception:
        return False


def _pins_block(board, label=None):
    """The render string for a board's pins, or '' if none. `label` overrides the
    heading (e.g. '(joint) PINNED')."""
    pins = _load_pins(board)
    if not pins:
        return ""
    head = label or f"PINNED RULES (board '{board}') - Max's standing orders, always in effect"
    body = "\n".join(f"  [{p.get('id')}] {p.get('text','')}" for p in pins)
    return f"=== {head} ===\n{body}\n=== end pinned ==="


def _resolve_board(cwd, board_arg=None, joint=False):
    """Which board a pin op targets: explicit --board wins, then --joint, then the
    caller's own team. Returns a board key ('x', 'p', 'joint', ...) or None."""
    if board_arg:
        return board_arg.strip().lower()
    if joint:
        return "joint"
    me = _load_state(cwd).get("id")
    return _team_of(me) if me else None


def cmd_pin(cwd, text, board_arg=None, joint=False):
    board = _resolve_board(cwd, board_arg, joint)
    if not board:
        print("no target board: name this session (whoami) or pass --board <letter> / --joint")
        return 1
    me = _load_state(cwd).get("id") or "?"
    pins = _load_pins(board)
    nid = (max((p.get("id", 0) for p in pins), default=0)) + 1
    pins.append({"id": nid, "ts": time.strftime("%Y-%m-%d %H:%M:%S"), "by": me, "text": text})
    if not _save_pins(board, pins):
        print("FAILED to write pin")
        return 1
    print(f"PINNED [{nid}] to board '{board}': {text}")
    print("This rule now shows at the TOP of the board every turn for that team. "
          "Unpin with: bcast.py unpin " + str(nid) + f" --board {board}")
    return 0


def cmd_unpin(cwd, which, board_arg=None, joint=False):
    board = _resolve_board(cwd, board_arg, joint)
    if not board:
        print("no target board: name this session (whoami) or pass --board <letter> / --joint")
        return 1
    pins = _load_pins(board)
    if not pins:
        print(f"board '{board}' has no pins")
        return 0
    if which == "--all":
        _save_pins(board, [])
        print(f"cleared ALL {len(pins)} pins on board '{board}'")
        return 0
    try:
        target = int(which)
    except Exception:
        print("usage: bcast.py unpin <id|--all> [--board <letter>|--joint]")
        return 1
    kept = [p for p in pins if p.get("id") != target]
    if len(kept) == len(pins):
        print(f"no pin [{target}] on board '{board}'")
        return 1
    _save_pins(board, kept)
    print(f"unpinned [{target}] from board '{board}'")
    return 0


def cmd_pins(cwd, board_arg=None):
    """List pins for a board (default: your team board + joint)."""
    me = _load_state(cwd).get("id")
    boards = [board_arg.strip().lower()] if board_arg else (
        [_team_of(me), "joint"] if me else ["joint"])
    shown = False
    for b in boards:
        block = _pins_block(b)
        if block:
            print(block)
            shown = True
    if not shown:
        print("(no pins on " + ", ".join(f"'{b}'" for b in boards) + ")")
    return 0


def cmd_dedupe(cwd, window_sec=None, apply=False):
    """ONE-SHOT SWEEP: resolve EVERY existing duplicate-id collision at once.

    The whoami auto-resolve only fires when a session is (re)named; pairs that
    already exist just sit there (the ~10 'two live <id>' the watcher keeps
    flagging). This sweep finds every id held by more than one distinct session
    within `window_sec`, KEEPS the freshest (the real active one), and auto-stamps
    the rest to the next free suffix (b/c/d...). Same-worktree churn (one tab whose
    hidden session_id changed) is collapsed, never counted as a rival. Dry-run by
    default; pass apply=True to actually rewrite + notify. Fail-open per file."""
    if window_sec is None:
        window_sec = 24 * 3600  # catch "active in the last 1-3 days" pairs Max sees
    now = time.time()
    groups = {}
    try:
        for fn in os.listdir(STATE_DIR):
            if not fn.endswith(".json"):
                continue
            p = os.path.join(STATE_DIR, fn)
            try:
                with open(p, "r", encoding="utf-8") as f:
                    st = json.load(f)
                age = now - os.path.getmtime(p)
            except Exception:
                continue
            sid = st.get("id")
            if not sid or age > window_sec:
                continue
            groups.setdefault(sid.strip().lower(), []).append(
                {"path": p, "age": age, "st": st, "cwd_n": _norm_cwd(st.get("cwd"))})
    except Exception:
        pass

    plan = []  # (holder, stamped_id, base_id)
    for idl, holders in groups.items():
        # collapse same-worktree churn: freshest file per distinct worktree cwd
        by_wt = {}
        for h in holders:
            key = h["cwd_n"] or h["path"]
            if key not in by_wt or h["age"] < by_wt[key]["age"]:
                by_wt[key] = h
        distinct = sorted(by_wt.values(), key=lambda h: h["age"])
        if len(distinct) <= 1:
            continue  # no real rival - single session (or one tab churned)
        keep = distinct[0]
        base = keep["st"].get("id")  # preserve Max's original casing
        taken = set()
        for h in distinct[1:]:
            stamped = _next_free_suffix(base, taken)
            taken.add(stamped)
            plan.append((h, stamped, base))

    if not plan:
        print("DEDUPE: no duplicate live ids found - nothing to resolve.")
        return 0

    print(f"DEDUPE: {len(plan)} duplicate session(s) to auto-stamp "
          f"(keeping the freshest of each id):")
    for h, stamped, base in plan:
        who = h["st"].get("cwd") or h["path"]
        mins = int(h["age"] / 60)
        print(f"  '{base}' -> '{stamped}'  (idle {mins}min, cwd={who})")
    if not apply:
        print("DRY-RUN. Re-run with --apply to rewrite state + notify each demoted session.")
        return 0

    done = 0
    for h, stamped, base in plan:
        hst = h["st"]
        _record_aka(hst, hst.get("id"))   # keep the vacated name reachable by wake
        hst["id"] = stamped
        try:
            with open(h["path"], "w", encoding="utf-8") as f:
                json.dump(hst, f)
        except Exception:
            continue
        done += 1
        note = (f"AUTO-RENAME (dedupe sweep): '{base}' was held by more than one live "
                f"session, so you were auto-stamped '{base}' -> '{stamped}' to prevent a "
                f"same-id file-corruption collision. You are now '{stamped}' - carry on.")
        try:
            _append_rec(_board_for(stamped), stamped, note)
        except Exception:
            pass
        try:
            if hst.get("session_id"):
                _drop_signal(hst["session_id"], note)
        except Exception:
            pass
    print(f"DEDUPE: resolved {done}/{len(plan)}. Each demoted session keeps its work, "
          f"got a new distinct id, and was notified + poked. Watcher will stop flagging these.")
    return 0


def cmd_whoami(cwd, new_id):
    st = _load_state(cwd)
    old_id = st.get("id")
    # AUTO-RESOLVE COLLISION (Max, 2026-07-13): Max names sessions from memory and
    # can't see what's retired, so he re-uses a name a live session still holds.
    # Old behavior only WARNED and told the humans to do an 8-min handshake - which
    # the sessions "keep ignoring", leaving a real corruption risk open for hours.
    # New behavior makes the collision IMPOSSIBLE to leave open: the session Max is
    # naming NOW keeps the clean id (his intent - a bare name is his), and every
    # OTHER live holder is AUTO-STAMPED to the next free suffix (E26 -> E26b -> ...).
    # Both survive and stay distinct forever; each demoted twin is told on the board
    # and force-woken so it learns its new id. Fail-open: any error -> just adopt.
    demoted = []
    if new_id != old_id:
        try:
            mine = {os.path.basename(_state_path(cwd))[:-5], _safe_key(cwd)}
            holders = _live_holder_files(new_id, mine, my_cwd=cwd)
            assigned = set()
            for h in holders:
                stamped = _next_free_suffix(new_id, assigned)
                assigned.add(stamped)
                hst = h["st"]
                _record_aka(hst, hst.get("id"))   # keep the vacated name wake-reachable
                hst["id"] = stamped
                try:
                    with open(h["path"], "w", encoding="utf-8") as f:
                        json.dump(hst, f)
                except Exception:
                    continue
                demoted.append((stamped, hst))
                # tell the demoted twin (board note on its team + a wake poke)
                note = (f"AUTO-RENAME: a newer session claimed '{new_id}' (Max named it), "
                        f"so you were auto-stamped '{new_id}' -> '{stamped}' to prevent a "
                        f"same-id file-corruption collision. You are now '{stamped}' - your "
                        f"state was updated automatically; just carry on under the new id.")
                try:
                    _append_rec(_board_for(stamped), stamped, note)
                except Exception:
                    pass
                try:
                    if hst.get("session_id"):
                        _drop_signal(hst["session_id"], note)
                except Exception:
                    pass
        except Exception:
            demoted = []
    st["id"] = new_id
    # Cursor placement on ANY (re)name: backfill a tail so the session
    # AUTOMATICALLY sees recent board context - standing orders posted before it
    # was named, a sibling's earlier posts, a brand-new team board it never read -
    # without anyone remembering to run `catchup`. A freshly-named session starting
    # blind is the foot-gun, not a feature, so fresh names get the tail too.
    # (2026-06-12: B9<-D9 switched team d->b and saw none of b10's earlier posts.)
    def _start_cursor(path):
        return max(0, len(_read_lines(path)) - WHOAMI_BACKFILL)
    if _split_on():
        boards = _my_boards(new_id)
        st["cursors"] = {k: _start_cursor(p) for k, p in boards.items()}
    else:
        st["cursor"] = _start_cursor(BULLETIN)
    _save_state(cwd, st)
    # B2 - REASSIGNMENT: if this cwd already had a DIFFERENT id, announce the move
    # so siblings track it (old posts keep their old label). Works in both modes:
    # to the joint board when split, else to the single board.
    if old_id and old_id != new_id:
        note = f"I am now {new_id} (was {old_id})."
        try:
            _append_rec(JOINT_BOARD if _split_on() else BULLETIN, new_id, note)
        except Exception:
            pass
        print(f"REASSIGNED: {old_id} -> {new_id}. Announced '{note}' to the board.")
        if _split_on() and _team_of(old_id) != _team_of(new_id):
            print(f"  Team switch: now on the '{_team_of(new_id)}'-team board "
                  f"(was '{_team_of(old_id)}'). You now hear that team + joint.")
    print(f"OK - this branch is now '{new_id}'. It will hear new sibling broadcasts from here on.")
    print(f"YOUR VISUAL SIGNATURE: {_signature(new_id)}  <- lead EVERY reply with this exact "
          f"tag so Max can tell your chats apart at a glance (one icon, auto-derived from your id).")
    if demoted:
        names = ", ".join(d[0] for d in demoted)
        print(f"  AUTO-RESOLVED COLLISION: {len(demoted)} other live session(s) also held "
              f"'{new_id}' - auto-stamped to: {names}. Each was notified on its board and poked. "
              f"You keep the clean '{new_id}'; no same-id corruption risk remains.")
    if _split_on():
        print(f"  SPLIT BOARDS ON - you hear the '{_team_of(new_id)}'-team board + the joint board.")
    print(
        "PEER DEFAULT - NO TIMER NEEDED: do your own part, read the board each "
        "turn (coordination is automatic), and MERGE+PUSH when your part is done.\n"
        "  MERGE+PUSH ETIQUETTE: post 'merging+pushing my part now', then push "
        "immediately - a push only updates the shared remote, it never touches a "
        "sibling's files, so nobody has to wait or remember to come back. Other "
        "sessions pull/rebase on their next turn; git surfaces any real conflict, "
        "no work is lost.\n"
        "  AUTONOMOUS (opt-in): ONLY if Max says 'run autonomous' - arm a ~240s "
        "ScheduleWakeup ('<<autonomous-loop-dynamic>>') and re-arm every wake so "
        "you keep grinding unattended. Otherwise stay timer-free.")
    if new_id.strip().lower() in ("b1", "manager"):
        print(MANAGER_CORE)


def cmd_who(cwd):
    st = _load_state(cwd)
    print(st.get("id") or "(no id set - run: python bcast.py whoami b2)")


def _auto_wake_board_peers(me, msg, to_joint):
    """Ping every LIVE wakeable session on the board this post lands on, minus
    the sender, throttled per target (AUTO_WAKE_THROTTLE_SEC). 1-on-1 (exactly
    one whole-token @-mention of a known id) skips the broadcast. Fail-open."""
    try:
        # 1-on-1 detection - skip broadcast wake (the addressee will hear via
        # its own board read + we still wake it below in the single-target list).
        mentioned = _mentioned_ids(me, msg or "")
        one_on_one = (len(mentioned) == 1)
        if one_on_one:
            targets = list(mentioned)
        else:
            live = _live_wakeable_ids()
            if to_joint:
                targets = [t for t in live if not _id_eq(t, me)]
            else:
                my_team = _team_of(me)
                targets = [t for t in live if _team_of(t) == my_team and not _id_eq(t, me)]
        if not targets:
            return
        os.makedirs(AUTO_WAKE_THROTTLE_DIR, exist_ok=True)
        now = time.time()
        signal_text = (f"AUTO-WAKE from {me} (new board post): {msg[:180]}\n"
                       f"Read the board (bcast.py read) and reply if relevant.")
        for tid in targets:
            try:
                stamp = os.path.join(AUTO_WAKE_THROTTLE_DIR, tid.lower() + ".ts")
                if os.path.exists(stamp) and (now - os.path.getmtime(stamp)) < AUTO_WAKE_THROTTLE_SEC:
                    continue
                sid = _session_id_for(tid)
                if not sid or not _listener_alive(sid):
                    continue
                if _drop_signal(sid, signal_text):
                    # touch throttle stamp AFTER successful signal drop
                    with open(stamp, "w", encoding="utf-8") as f:
                        f.write(str(now))
            except Exception:
                continue
    except Exception:
        pass


def cmd_post(cwd, msg, joint=False, force_all=False, as_id=None, announce=False):
    st = _load_state(cwd)
    # --as <id> = post under an EXPLICIT id regardless of this cwd's registered id.
    # The escape hatch for a session that legitimately posts from a shared cwd (e.g.
    # cd'd into the main checkout to commit): `bcast.py post --as G2 "..."`. It is
    # stateless - it does NOT touch this cwd's cursor (the cwd is not this session's
    # home), so it never disturbs the registered owner's bookkeeping.
    if as_id:
        me = as_id
        if not _split_on():
            _append_rec(BULLETIN, me, msg)
            _auto_wake_board_peers(me, msg, to_joint=True)
            print(f"BROADCAST sent as {me} (--as): {msg}")
            return 0
        # split mode falls through to routing below with stateless=True
    else:
        me = st.get("id")
        if not me:
            print("ERROR - no id set for this branch. Run: python bcast.py whoami b2")
            return 1
        # GUARD: silent cd mis-attribution (2026-06-19). A worktree session that cd's
        # into the shared MAIN checkout to commit, then posts in the same chain, gets
        # attributed to the main checkout's id (G2's post went out as 'b29'; g1 too).
        # Tell: the message's leading SELF-id disagrees with this cwd's registered id.
        # REFUSE (do not send wrong-attributed info - higher harm than joint noise) and
        # hand the exact fix. Precise: only fires when the leading bare id is a REAL
        # registered id different from the cwd's id, so correct self-attributed posts
        # ('b29 ...' from b29) and @-addressing ('@G3 ...') never trip it.
        claimed = _leading_self_id(msg)
        if claimed and claimed.lower() != me.lower() and claimed.lower() in _known_ids():
            real = _known_ids()[claimed.lower()]
            print("=" * 64)
            print(f"REFUSED - likely cd MIS-ATTRIBUTION. Your message starts with "
                  f"'{real}', but THIS directory is registered to '{me}', so the post "
                  f"would go out signed '{me}' (wrong).")
            print(f"  You probably cd'd into a shared dir (e.g. the main checkout) to "
                  f"commit. Fix EITHER way:")
            print(f"    1) cd back to YOUR worktree, then re-post; OR")
            print(f"    2) post explicitly:  bcast.py post --as {real} \"{msg[:40]}...\"")
            print(f"  (If you really are '{me}', drop the leading '{real}' from the message.)")
            print("=" * 64)
            return 1
    # BOARD CONTENT GATE (Max 2026-07-10): for a team whose gate is ON, HARD-refuse a
    # routine work report at the chokepoint - it belongs in the room, not the board.
    # Skipped for --as (shared-cwd escape) and --announce (explicit whole-board override).
    if not as_id and not announce and _board_gate_on(_team_of(me)):
        ok, why = _board_worthy(me, msg)
        if not ok:
            my_rooms = _rooms_of(me)
            room_hint = my_rooms[0] if my_rooms else "<project>"
            level = _offense_bump(me)  # repeat offenders get sterner language
            print("=" * 64)
            print(_board_refusal_message(me, msg, why, level, room_hint))
            print("=" * 64)
            return 1
        else:
            _offense_reset(me)  # a clean, board-worthy post clears the strike count
    # POSTING BARRIER (Max 2026-07-07): once a session has been moved into a room,
    # the boards (team AND joint) are for WHOLE-BOARD items only. A roomed session
    # gets RESISTANCE before posting to any board - it must confirm the post is one
    # of: (1) a resource/info of interest to the whole board, (2) a danger of
    # interest to the whole board, (3) a Max announcement. Otherwise it belongs in
    # the room. Un-roomed sessions (the '1-2 sessions, no rooms' case) post freely.
    # Override = re-run with --announce (the 'yes, this belongs to the whole board'
    # confirmation). Skipped for --as (the shared-cwd escape hatch).
    if not as_id and not announce:
        my_rooms = _rooms_of(me)
        if my_rooms:
            snippet = (msg or "")[:40]
            print("=" * 64)
            print(f"HOLD - you ({me}) are in room(s): {', '.join(my_rooms)}.")
            print("The board is for WHOLE-BOARD items only. Are you SURE this belongs")
            print("to the whole board? It should be ONE of:")
            print("  (1) a resource / info useful to the WHOLE board,")
            print("  (2) a DANGER to the whole board,")
            print("  (3) a MAX announcement (relaying Max's instruction).")
            print("If NOT, post it in your room instead:")
            print(f"     bcast.py room {my_rooms[0]} \"{snippet}...\"")
            print("If it TRULY belongs to the whole board, confirm with --announce:")
            print(f"     bcast.py post --announce \"{snippet}...\"")
            print("=" * 64)
            return 1
    os.makedirs(BASE, exist_ok=True)
    if _split_on():
        # ROUTING FOLLOWS WHO YOU ADDRESS, with a point-of-violation CHALLENGE -
        # because discipline alone did not hold (2026-06-18: the tamza project was
        # ~62% of joint traffic, flooding the unrelated MOMA project that shares the
        # joint board). Max's rule: do NOT silently reroute (a silent demote could
        # HIDE a real all-teams announcement); instead ASK the posting session if it
        # knows what it is doing, and still send (fail-open). The poster is a Claude
        # that reads the challenge and self-corrects.
        #   --all / @all           -> ALWAYS joint (the ONE explicit all-teams verb)
        #   names a CROSS-team id   -> joint   (auto-PROMOTE: a sibling on another
        #                                       team only reads joint, not your board)
        #   --joint / --all         -> joint (TRUSTED global verb; see below)
        #   plain post, no @        -> your TEAM board (the clean default)
        #
        # POLLUTION MODEL (Max 2026-07-03, SUPERSEDES both the 2026-06-18 challenge-
        # but-send AND the short-lived 2026-07-03 reroute-of-joint): the joint board
        # must stay CROSS-TEAM ONLY, but teams MUST still be able to post there for a
        # genuine global question. So the SOURCE trusts the author's explicit verb and
        # never second-guesses it - it only fixes the thing the author did NOT choose:
        # the false AUTO-promote. Two clean, intentional ways to reach joint:
        #   (a) --all / --joint  = "this is a global/cross-team post" (author declares)
        #   (b) @mention a sibling on another team (they read only joint, not you)
        # Everything else stays on the team board. Bare technical tokens (F1/F2/chrX)
        # no longer promote (that was the #1 accidental-pollution source; see
        # _mentioned_ids, now @-only). The semantic Pollution Watcher (watcher.py) is
        # the backstop for content that IS single-team yet was explicitly --joint'd.
        if force_all or joint:
            # Explicit global verb - TRUSTED only if it genuinely is cross-team:
            # either it @-addresses another team, OR it passes the semantic pollution
            # gate. A --all/--joint post that names no other team AND reads as one
            # team's internal work is REROUTED to the team board at post time (the
            # author self-certifying 'global' is exactly the abuse this stops). The
            # gate is fail-open, so if DeepSeek is unreachable this behaves as the old
            # trust-the-verb path and never blocks coordination.
            if _names_other_team(me, msg) or _joint_is_genuinely_global(me, msg):
                to_joint = True
            else:
                to_joint = False
                print("POLLUTION GATE - REROUTED to your team board. You flagged this "
                      "--all/--joint, but it reads as single-team work (a status/"
                      "postmortem/handoff about your own team's task), not a genuine "
                      "cross-team message, so it does NOT go on the GLOBAL board that "
                      f"every team reads. Your '{_team_of(me)}' teammates still hear it "
                      "on the team board. If it truly needs another team, @-mention "
                      "them; if it is a real all-teams announcement, keep it short and "
                      "about the shared thing.")
        else:
            foreign = _names_other_team(me, msg)
            to_joint = bool(foreign)
            if foreign:
                print(f"NOTE: auto-routed to JOINT - this @-addresses cross-team "
                      f"id(s) {sorted(foreign)}, who read only the joint board, not "
                      f"your '{_team_of(me)}' team board.")
        key = "joint" if to_joint else "team"
        path = JOINT_BOARD if to_joint else _board_for(me)
        _append_rec(path, me, msg)
        _auto_wake_board_peers(me, msg, to_joint=to_joint)
        # Advance own cursor on that board so a branch never hears its own shout -
        # but NOT for an --as post: this cwd is not that session's home, so touching
        # its cursor would corrupt the registered owner's bookkeeping.
        if not as_id:
            st.setdefault("cursors", {})
            st["cursors"][key] = len(_read_lines(path))
            _save_state(cwd, st)
        where = "JOINT (all teams)" if to_joint else f"team '{_team_of(me)}'"
        tag = " (--as)" if as_id else ""
        print(f"BROADCAST sent as {me}{tag} to {where}: {msg}")
    else:
        _append_rec(BULLETIN, me, msg)
        _auto_wake_board_peers(me, msg, to_joint=True)
        st["cursor"] = len(_read_lines())
        _save_state(cwd, st)
        print(f"BROADCAST sent as {me}: {msg}")


def cmd_catchup(cwd, n=12):
    """Print the last N board entries (all branches) without advancing the cursor.

    A freshly-named or reassigned branch has its cursor pinned to "now" by whoami,
    so `read` shows it nothing - it cannot see standing orders the manager posted
    BEFORE it was named. catchup lets it pull recent history on demand. It does NOT
    move the cursor, so it never interferes with the auto-hear hook.
    """
    if _split_on():
        me = _load_state(cwd).get("id") or ""
        recs = []
        recs += _parse(_read_lines(_board_for(me)))
        for r in _parse(_read_lines(JOINT_BOARD)):
            r = dict(r); r["_joint"] = True
            recs.append(r)
        recs.sort(key=lambda r: r.get("ts", ""))
        out = recs[-n:] if n and n > 0 else recs
        scope = f"team '{_team_of(me)}' + joint"
    else:
        out = _parse(_read_lines())
        out = out[-n:] if n and n > 0 else out
        scope = "all branches"
    if not out:
        print("(board empty)")
        return 0
    halt = _read_halt()
    if halt:
        print(f"=== HALT IN EFFECT ===\n{halt}\n=== end halt ===")
    # PINNED RULES at the very top of the catch-up too.
    if _split_on():
        for _b, _lbl in ((_team_of(me), None),
                         ("joint", "(joint) PINNED RULES - Max's standing orders for ALL teams")):
            _pb = _pins_block(_b, _lbl)
            if _pb:
                print(_pb)
    print(f"=== BOARD CATCH-UP ({scope}; last {len(out)} entries; cursor NOT advanced) ===")
    for r in out:
        tag = "(joint) " if r.get("_joint") else ""
        print(f"[{r.get('ts','?')}] {tag}{r.get('from','?')}: {r.get('msg','')}")
    print("=== end catch-up ===")
    return 0


def _active_team_sessions(team, window_sec, exclude_id=None):
    """[(id, age_sec)] for every session on `team` whose state file was touched
    within window_sec. Used to tell the requester who is likely to catch a wake
    soon (live) vs who is asleep (will catch it only when it next acts)."""
    out = []
    try:
        for fn in os.listdir(STATE_DIR):
            if not fn.endswith(".json"):
                continue
            p = os.path.join(STATE_DIR, fn)
            try:
                with open(p, "r", encoding="utf-8") as f:
                    st = json.load(f)
                age = time.time() - os.path.getmtime(p)
            except Exception:
                continue
            sid = st.get("id")
            if not sid or sid == exclude_id:
                continue
            if _team_of(sid) != team:
                continue
            if age <= window_sec:
                out.append((sid, age))
    except Exception:
        pass
    return out


def _drop_signal(session_id, msg):
    """Drop the file the per-session wake_listener is blocked on -> wakes that
    idle session (asyncRewake exit-2). Keyed by the stable Claude session_id."""
    if not session_id:
        return False
    sdir = os.path.join(WAKE_DIR, "signals")
    try:
        os.makedirs(sdir, exist_ok=True)
        with open(os.path.join(sdir, session_id + ".signal"), "w", encoding="utf-8") as f:
            f.write(msg)
        return True
    except Exception:
        return False


def _listener_alive(session_id):
    """True iff a wake_listener is ACTUALLY blocking for this session_id right now
    (its lock file was touched within WAKE_LISTENER_FRESH_SEC). This is the only
    honest proof that a dropped signal will be CAUGHT and wake the session - a
    stamped session_id alone does not prove the listener still lives."""
    if not session_id:
        return False
    lock = os.path.join(WAKE_DIR, "locks", session_id + ".lock")
    try:
        return os.path.exists(lock) and (
            time.time() - os.path.getmtime(lock) < WAKE_LISTENER_FRESH_SEC)
    except Exception:
        return False


def _wake_gc():
    """Prune expired dead-letter signal files and stale lock files so the wake
    dirs don't rot (they were piling up: 60+ day-old locks, orphaned signals).
    Only touches files older than the request TTL - anything within the honest
    delivery window is left in place for its target to catch when it next acts.
    A live listener refreshes its lock every ~5s, so its lock is never stale and
    is never pruned."""
    cutoff = time.time() - WAKE_REQUEST_TTL_HOURS * 3600
    for sub in ("signals", "locks"):
        d = os.path.join(WAKE_DIR, sub)
        try:
            for fn in os.listdir(d):
                p = os.path.join(d, fn)
                try:
                    if os.path.getmtime(p) < cutoff:
                        os.remove(p)
                except Exception:
                    pass
        except Exception:
            pass


def _wt_lock_path(cwd):
    """Path of the STABLE worktree wake-lock the listener maintains for a worktree
    session (content = its current session_id). None for a non-worktree cwd (shared
    checkouts host many sessions, so a worktree key would be ambiguous - those keep
    pure session_id keying)."""
    if not _is_worktree(cwd):
        return None
    return os.path.join(WAKE_DIR, "locks", "wt_" + _safe_key(cwd) + ".lock")


def _fresh_sid_from_worktree(cwd):
    """The CURRENTLY-LIVE session_id for a worktree, read from the worktree wake-lock
    the listener refreshes every few seconds - but only if that lock is FRESH (a live
    listener is really blocking). This is how a wake reaches a session whose bcast
    state file still holds a churned/stale session_id. None if not a worktree, no
    lock, stale, or unreadable. Fail-open."""
    p = _wt_lock_path(cwd)
    if not p:
        return None
    try:
        if os.path.exists(p) and (
                time.time() - os.path.getmtime(p) < WAKE_LISTENER_FRESH_SEC):
            with open(p, "r", encoding="utf-8") as f:
                return (f.read().strip() or None)
    except Exception:
        pass
    return None


def _idlock_path(bcast_id):
    """Lock the listener maintains keyed by the BCAST ID (content = its current
    session_id). Unlike the worktree lock, this ALSO covers SHARED-CHECKOUT sessions
    (C:\\claude_base, C:\\moma) that host many tabs - there the worktree bridge is a
    no-op, which silently made a shared-checkout session UNWAKEABLE once its
    session_id churned (the X32B->X12B force-wake failure, 2026-07-10: X12B ran from
    C:\\claude_base, its stamped sid went stale, no worktree lock existed to recover
    the live sid, so the signal dropped to a dead sid forever)."""
    if not bcast_id:
        return None
    slug = re.sub(r"[^A-Za-z0-9]+", "_", bcast_id.strip().lower())
    return os.path.join(WAKE_DIR, "locks", "id_" + slug + ".lock")


def _fresh_sid_from_idlock(bcast_id):
    """CURRENTLY-LIVE session_id for a bcast id, from the id-keyed listener lock, if
    FRESH (a live listener refreshes it every ~5s). Works for worktree AND shared
    checkouts. None if missing/stale/unreadable. Fail-open."""
    p = _idlock_path(bcast_id)
    if not p:
        return None
    try:
        if os.path.exists(p) and (
                time.time() - os.path.getmtime(p) < WAKE_LISTENER_FRESH_SEC):
            with open(p, "r", encoding="utf-8") as f:
                return (f.read().strip() or None)
    except Exception:
        pass
    return None


def _session_id_for(bcast_id):
    """Map a bcast id (b7) -> the Claude session_id stamped into its state file
    by the wake_listener. When SEVERAL state files share one id (a duplicate-id
    collision - common after Esc-Esc branching / re-naming), PREFER the candidate
    whose listener is LIVE right now, so a wake reaches the live twin instead of a
    dead one. Returns None if no state file for this id ever stamped a session_id."""
    # AUTHORITATIVE LIVE SIGNAL (2026-07-10): the id-keyed listener lock is refreshed
    # every ~5s by the live listener and keyed by the bcast id itself, so it names the
    # session that is ACTUALLY blocking right now - even for a shared-checkout session
    # whose stamped sid has churned and which has no worktree lock. Check it first; it
    # matches the healthy case too (the live listener writes its own current sid).
    id_live = _fresh_sid_from_idlock(bcast_id)
    if id_live:
        return id_live
    cands = []
    derived = []
    cwds = []
    try:
        for fn in os.listdir(STATE_DIR):
            if not fn.endswith(".json"):
                continue
            p = os.path.join(STATE_DIR, fn)
            with open(p, "r", encoding="utf-8") as f:
                st = json.load(f)
            if not _id_eq(st.get("id"), bcast_id) and not any(
                    _id_eq(a, bcast_id) for a in _akas_of(st)):
                continue     # neither the live id nor any alias matches this name
            if st.get("cwd"):
                cwds.append(st.get("cwd"))
            if st.get("session_id"):
                cands.append(st.get("session_id"))
            else:
                # A LIVE state file with no stamped session_id (a build whose hook
                # omits it - C12A/E45, 2026-07-02). Recover the id from the
                # worktree transcript so this session is wakeable NOW, not only
                # after its next turn re-stamps it.
                try:
                    fresh = time.time() - os.path.getmtime(p) <= LIVENESS_WINDOW_SEC
                except Exception:
                    fresh = False
                if fresh:
                    d = _sid_from_transcript(st.get("cwd"))
                    if d:
                        derived.append(d)
    except Exception:
        pass
    all_cands = cands + derived
    if not all_cands:
        # No stamped session_id anywhere - but the session may still be a LIVE
        # worktree whose listener maintains the stable worktree lock. Recover the
        # live sid from it (covers a state file that never stamped a session_id).
        for cw in cwds:
            rsid = _fresh_sid_from_worktree(cw)
            if rsid:
                return rsid
        return None
    for sid in all_cands:             # prefer a live twin over the first/dead one
        if _listener_alive(sid):
            return sid
    # WORKTREE RECOVERY (2026-07-04): every stamped session_id is STALE (no fresh
    # lock) yet the session is alive - the live listener re-armed under a NEW
    # session_id faster than the bcast state file was re-stamped, so a wake dropped
    # to the stale sid lands on a .signal no listener watches and the alive session
    # never wakes (the exact bug Max hit: force-wake ignored, manual wake worked).
    # For a worktree (1 session : 1 cwd) the listener also maintains a lock keyed by
    # the STABLE worktree path whose CONTENT is its current session_id; read that to
    # reach the session that is actually blocking right now.
    for cw in cwds:
        rsid = _fresh_sid_from_worktree(cw)
        if rsid:
            return rsid
    return all_cands[0]


def _live_wakeable_ids():
    """Every bcast id that has a LIVE wake_listener right now (reachable by
    force-wake this instant). Used to help a caller whose target NAME did not
    resolve - it can re-aim at a live name (e.g. 'x3' is stale/empty but 'x3old'
    is the live session). This is Max's 'report all names so the caller's LLM can
    conclude the right target' fix."""
    out = []
    try:
        for fn in os.listdir(STATE_DIR):
            if not fn.endswith(".json"):
                continue
            p = os.path.join(STATE_DIR, fn)
            with open(p, "r", encoding="utf-8") as f:
                st = json.load(f)
            bid = st.get("id"); sid = st.get("session_id")
            if not bid:
                continue
            if not sid:
                # recover from transcript for hook-omits-session_id builds
                try:
                    fresh = time.time() - os.path.getmtime(p) <= LIVENESS_WINDOW_SEC
                except Exception:
                    fresh = False
                if fresh:
                    sid = _sid_from_transcript(st.get("cwd"))
            # Reachable if the stamped sid has a live listener OR (worktree recovery)
            # the stable worktree lock is fresh even though the stamped sid is stale.
            if ((sid and _listener_alive(sid)) or _fresh_sid_from_worktree(st.get("cwd"))
                    or _fresh_sid_from_idlock(bid)):
                out.append(bid)
    except Exception:
        pass
    return sorted(set(out))


def _write_wake(rec):
    os.makedirs(WAKE_DIR, exist_ok=True)
    fn = f"wake_{time.strftime('%Y%m%d_%H%M%S')}_{os.urandom(3).hex()}.json"
    with open(os.path.join(WAKE_DIR, fn), "w", encoding="utf-8") as f:
        json.dump(rec, f)


def _pending_wakes_for(me, akas=None):
    """Undelivered, unexpired wake requests targeting `me` (or any of my `akas` -
    an id I was renamed away from, so a wake to my OLD name still reaches me).
    Side-effect: deletes expired request files so the queue self-cleans. Returns
    list of (path, rec)."""
    out = []
    my_names = [me] + list(akas or [])
    now = time.time()
    try:
        files = sorted(os.listdir(WAKE_DIR))
    except Exception:
        return out
    for fn in files:
        if not fn.endswith(".json"):
            continue
        p = os.path.join(WAKE_DIR, fn)
        try:
            with open(p, "r", encoding="utf-8") as f:
                rec = json.load(f)
        except Exception:
            continue
        if now >= rec.get("expires", 0):
            try: os.remove(p)
            except Exception: pass
            continue
        if rec.get("from") == me:
            continue
        if me in rec.get("delivered", []):
            continue
        mode = rec.get("mode")
        hit = False
        if mode == "name":
            hit = any(_id_eq(nm, t) for t in rec.get("targets", []) for nm in my_names)
        elif mode == "active":
            # any teammate that shows up within the TTL counts as "active now"
            hit = _team_of(me) == rec.get("team")
        if hit:
            out.append((p, rec))
    return out


def _mark_wake_delivered(path, rec, me):
    rec.setdefault("delivered", []).append(me)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(rec, f)
    except Exception:
        pass


def cmd_wake(cwd, args):
    """wake teammates. Two targeting modes (Max's spec - by time OR by name):
      wake --active [hours] "msg"   -> every teammate active in the last N hours
                                       (default WAKE_ACTIVE_WINDOW_HOURS)
      wake --name b1 b7 "msg"       -> those specific ids (cross-team allowed:
                                       a worker can wake its manager and back)
    Anyone may wake anyone. Delivery is forced into each target's context the
    moment it next takes a turn (timer/prompt/heartbeat), within the TTL."""
    st = _load_state(cwd)
    me = st.get("id")
    if not me:
        print("You must be named first (run `bcast.py whoami <id>`) before waking others.")
        return 1
    if not args:
        print('usage: bcast.py wake --active [hours] "msg"   |   wake --name b1 b7 "msg"')
        return 1

    mode = None
    window_h = WAKE_ACTIVE_WINDOW_HOURS
    targets = []
    rest = list(args)
    if rest[0] == "--active":
        mode = "active"
        rest = rest[1:]
        if rest and rest[0].isdigit():
            window_h = int(rest[0]); rest = rest[1:]
    elif rest[0] == "--name":
        mode = "name"
        rest = rest[1:]
        # consume leading tokens that look like ids (letter+digits, optional
        # trailing letters e.g. b15M / b7i / b15merger) as targets
        while rest and re.fullmatch(r"[A-Za-z]+\d+[A-Za-z]*", rest[0]):
            targets.append(rest[0]); rest = rest[1:]
    else:
        print('usage: bcast.py wake --active [hours] "msg"   |   wake --name b1 b7 "msg"')
        return 1

    msg = " ".join(rest).strip()
    if not msg:
        print("Refusing to wake with an empty message - say what you need them for.")
        return 1
    if mode == "name" and not targets:
        print("wake --name needs at least one id, e.g. wake --name b1 \"...\"")
        return 1

    _wake_gc()   # prune expired dead-letter signals + stale locks so the dirs stay clean
    now = time.time()
    rec = {
        "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
        "from": me,
        "team": _team_of(me),
        "mode": mode,
        "msg": msg,
        "delivered": [],
        "expires": now + WAKE_REQUEST_TTL_HOURS * 3600,
    }
    if mode == "active":
        rec["window_h"] = window_h
    else:
        rec["targets"] = targets
    _write_wake(rec)

    # Drop the force-wake signal for every resolved target that has a stamped
    # session_id, then CONFIRM the wake by watching that signal file get CONSUMED
    # (a live listener removes it the instant it wakes). Consumption is the only
    # honest proof the session actually woke: it fixes BOTH the false-negative (a
    # live teammate judged "asleep" by one stale-lock snapshot - the g1 case
    # 2026-06-21) and the false-positive (a signal dropped to a dead session_id,
    # never consumed - the old b27 bug). We poll up to WAKE_CONFIRM_SEC so a
    # teammate mid-rearm still confirms. The queued record (_write_wake above)
    # stays as belt-and-suspenders: any signal not consumed in-window is still
    # caught when the listener next arms, or via the read-hook, within the TTL.
    signal_text = (f"WAKE CALL from {me}: {msg}\n"
                   "Come to the bcast board NOW: run "
                   "`python C:/claude_base/branch_bulletin/bcast.py read`")
    if mode == "name":
        resolve_ids = targets
    else:
        resolve_ids = [sid for sid, _ in _active_team_sessions(_team_of(me), window_h * 3600, exclude_id=me)]

    pending, queued, unresolved = [], [], []   # pending = (tid, signal_path) awaiting confirm
    for tid in resolve_ids:
        ssid = _session_id_for(tid)
        if not ssid:
            unresolved.append(tid)     # NAME has no stamped session_id at all (stale/renamed)
        elif _drop_signal(ssid, signal_text):
            pending.append((tid, os.path.join(WAKE_DIR, "signals", ssid + ".signal")))
        else:
            queued.append(tid)     # had a session_id but signal-drop failed -> queued record

    woken, not_armed = [], []
    if pending:
        confirm_deadline = time.time() + WAKE_CONFIRM_SEC
        remaining = list(pending)
        while remaining and time.time() < confirm_deadline:
            still = []
            for tid, sigp in remaining:
                if not os.path.exists(sigp):    # consumed by a live listener -> awake
                    woken.append(tid)
                else:
                    still.append((tid, sigp))
            remaining = still
            if remaining:
                time.sleep(1.0)
        not_armed.extend(tid for tid, _ in remaining)   # signal still sitting -> queued
    not_armed.extend(queued)

    # Drop a visible line on the board history too (joint if it crosses teams).
    cross = mode == "name" and any(_team_of(t) != _team_of(me) for t in targets)
    label = (f"WAKE call -> team active<{window_h}h" if mode == "active"
             else f"WAKE call -> {', '.join(targets)}")
    try:
        _append_rec(JOINT_BOARD if (cross and _split_on()) else _board_for(me),
                    me, f"{label}: {msg}")
    except Exception:
        pass

    # Tell the requester who is live now (will catch it within ~one heartbeat)
    # vs who is asleep (catches it only when it next acts, within the TTL).
    if mode == "active":
        print(f"WAKE for team '{_team_of(me)}', look-back {window_h}h. Message: {msg}")
    else:
        print(f"WAKE for {', '.join(targets)}. Message: {msg}")
    if woken:
        print(f"FORCE-WOKEN now (confirmed - signal consumed): {', '.join(woken)}")
    if not_armed:
        print(f"Queued (no live listener confirmed within {WAKE_CONFIRM_SEC}s; "
              f"delivered when each next acts, within the TTL): {', '.join(not_armed)}")
    if unresolved:
        live = _live_wakeable_ids()
        print(f"NAME NOT FOUND - no live session is registered under: {', '.join(unresolved)}")
        print(f"  These names have NO stamped session (stale, retired, or renamed - "
              f"e.g. 'x3' is empty while the live session is 'x3old').")
        print(f"  LIVE wakeable names RIGHT NOW: "
              f"{', '.join(live) if live else '(none - nobody on Pine has a live listener)'}")
        print(f"  -> If your target renamed/branched, re-run `wake --name <id>` with the "
              f"matching live name above.")
    if not woken and not not_armed and not unresolved:
        print("No teammate matched - nobody to wake yet.")
    print(f"Force-wake confirms delivery by watching the signal get consumed (waited "
          f"up to {WAKE_CONFIRM_SEC}s). A session with a live wake_listener wakes "
          "within ~1-2s; a truly dormant one with no listener catches it only when "
          "it next acts - platform limit, honest, never a silent drop.")
    return 0


# --- ROOMS: N-way side-channels, visible but OFF the team/joint boards ---------
# A "room" is a named side-conversation among an explicit MEMBER set - the THIRD
# layer below the global (joint) board and the per-team board. Room posts go to
# rooms/<name>.jsonl and are NEVER mirrored to a team or the joint board, so N
# chats can talk without polluting the boards. Unlike the boards, room content is
# NOT auto-loaded: a member gets only a one-line KNOCK that unread messages exist
# and must OPEN THE DOOR with `room <name> --read` to see them (Max 2026-07-07:
# "not completely isolated, but not loaded by default - you knock in, with some
# resistance"). TRANSPARENT not secret: ANY chat (member or not) may `room <name>
# --read` or `rooms` to inspect a room. Grow it anytime with --with/--add.
# (Max 2026-06-21: "2 chats talk semi-privately, visible but not polluting the
# board; add any number of chats.")

def _room_name_ok(name):
    return bool(name) and re.fullmatch(r"[A-Za-z0-9_~.\-]+", name) is not None


def _room_msgs_path(name):
    return os.path.join(ROOMS_DIR, name + ".jsonl")


def _room_manifest_path(name):
    return os.path.join(ROOMS_DIR, name + ".room.json")


def _load_room(name):
    try:
        with open(_room_manifest_path(name), "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _save_room(name, manifest):
    os.makedirs(ROOMS_DIR, exist_ok=True)
    with open(_room_manifest_path(name), "w", encoding="utf-8") as f:
        json.dump(manifest, f)


def _all_rooms():
    out = []
    try:
        for fn in os.listdir(ROOMS_DIR):
            if fn.endswith(".room.json"):
                out.append(fn[:-len(".room.json")])
    except Exception:
        pass
    return sorted(out)


def _auto_pair_name(a, b):
    return "pair_" + "~".join(sorted([a, b]))


def _room_unread(me, st):
    """[(roomname, unread_count)] for every room `me` is a member of, counting
    messages from OTHERS the member has not yet READ. Does NOT mutate state: the
    per-room cursor advances ONLY when the member explicitly opens the room with
    `room <name> --read`. That is the whole point of the third layer - a room is a
    KNOCK, not an auto-load, so the notification must persist across turns until
    the member actually opens the door (Max 2026-07-07)."""
    res = []
    rc = st.get("room_cursors", {})
    for name in _all_rooms():
        m = _load_room(name)
        if not m or me not in (m.get("members") or []):
            continue
        lines = _read_lines(_room_msgs_path(name))
        new = [r for r in _parse(lines[rc.get(name, 0):]) if r.get("from") != me]
        if new:
            res.append((name, len(new)))
    return res


def cmd_rooms(cwd):
    """List every room with its members + message count (transparency view)."""
    names = _all_rooms()
    if not names:
        print("(no rooms yet - create one with: bcast.py room <name> --with <id> \"msg\")")
        return 0
    me = _load_state(cwd).get("id")
    print("=== ROOMS (side-channels, off the team/joint boards) ===")
    for name in names:
        m = _load_room(name) or {}
        members = m.get("members") or []
        n = len(_read_lines(_room_msgs_path(name)))
        mark = " *you*" if me in members else ""
        print(f"  {name}  [{n} msgs]  members: {', '.join(members)}{mark}")
    print("=== read one with: bcast.py room <name> --read [N] ===")
    return 0


def cmd_dm(cwd, args):
    """dm <name> "message" - a DIRECT 1:1 message to ONE session (Max 2026-07-14).

    This is THE default channel for any back-and-forth. It rides a private 2-member
    'pair_' room, so the message injects straight into that one recipient's next turn
    (and yours) and NOBODY else sees it - no group distraction. Keep the boards and
    rooms for broadcasts (a result/resource/danger the whole group needs).

    Sugar over `room --with <name> "msg"`; both hit the same pair_ channel, so a
    reply with either verb lands in the same thread. Read the full thread anytime:
    `bcast.py room pair_<a>~<b> --read`.
    """
    st = _load_state(cwd)
    me = st.get("id")
    if not me:
        print("ERROR - no id set. Run: python bcast.py whoami <id>")
        return 1
    if not args:
        print('usage: bcast.py dm <name> "message"')
        return 1
    target = args[0]
    msg = " ".join(args[1:]).strip()
    if _id_eq(target, me):
        print("dm: that's you. Pick another session.")
        return 1
    if not msg:
        print(f'usage: bcast.py dm {target} "message"  (message required)')
        return 1
    name = _auto_pair_name(me, target)
    m = _load_room(name) or {"members": [], "created": time.strftime("%Y-%m-%d %H:%M:%S")}
    m["members"] = list(dict.fromkeys((m.get("members") or []) + [me, target]))
    _save_room(name, m)
    os.makedirs(ROOMS_DIR, exist_ok=True)
    _append_rec(_room_msgs_path(name), me, msg)
    # advance my own cursor so I never hear my own message back
    st.setdefault("room_cursors", {})[name] = len(_read_lines(_room_msgs_path(name)))
    _save_state(cwd, st)
    # Best-effort: if the recipient is idle-but-alive, drop a signal so they notice
    # promptly rather than only on their next natural board read (fail-open).
    woke = ""
    try:
        sid = _session_id_for(target)
        if sid and _listener_alive(sid):
            _drop_signal(sid, f"Direct message from {me}: {msg[:80]}")
            woke = " (nudged - they're live)"
    except Exception:
        pass
    print(f"DIRECT message sent to {target}{woke}. Private 1:1 - only {target} sees "
          f"it, injected into their next turn. They reply with: bcast.py dm {me} \"...\"")
    return 0


def cmd_room(cwd, args):
    """room <name> "msg"           post to a room (creates it; you join as a member)
       room <name> --with x [y...] ensure x/y (and you) are members, optional msg
       room <name> --add x [y...]  add member(s) to an existing room
       room <name> --remove x [..] remove member(s) (alias --rm/--kick; x5==X5)
       room <name> --leave         remove yourself from the room
       room <name> --read [N]      print a room's history (ANY chat may read)
       room --with x "msg"         auto-named pairwise room between you and x"""
    st = _load_state(cwd)
    me = st.get("id")
    if not me:
        print("ERROR - no id set. Run: python bcast.py whoami <id>")
        return 1
    name = None
    withs, adds, removes, positionals = [], [], [], []
    read_mode = False
    leave = False
    read_n = 20
    i = 0
    while i < len(args):
        a = args[i]
        if a in ("--with", "--member") and i + 1 < len(args):
            withs.append(args[i + 1]); i += 2
        elif a == "--members" and i + 1 < len(args):
            withs.extend([x for x in re.split(r"[,\s]+", args[i + 1]) if x]); i += 2
        elif a == "--add" and i + 1 < len(args):
            adds.append(args[i + 1]); i += 2
        elif a in ("--remove", "--rm", "--kick") and i + 1 < len(args):
            removes.append(args[i + 1]); i += 2
        elif a == "--leave":
            leave = True; i += 1
        elif a == "--name" and i + 1 < len(args):
            name = args[i + 1]; i += 2
        elif a == "--read":
            read_mode = True
            if i + 1 < len(args) and args[i + 1].isdigit():
                read_n = int(args[i + 1]); i += 2
            else:
                i += 1
        else:
            positionals.append(a); i += 1
    # Distinguish NAME from MESSAGE among positionals: a room name is a single
    # clean token (no spaces); a message is usually a multi-word arg. So the first
    # positional becomes the name ONLY if it is a clean room-name token, else all
    # positionals are the message (and the name comes from --name/--with auto-pair).
    if name is None and positionals and " " not in positionals[0] and _room_name_ok(positionals[0]):
        name = positionals[0]
        msg_parts = positionals[1:]
    else:
        msg_parts = positionals
    msg = " ".join(msg_parts).strip()

    # Auto-name a pairwise room if no explicit name but exactly one --with partner.
    if not name and len(withs) == 1:
        name = _auto_pair_name(me, withs[0])
    if not name:
        print('usage: bcast.py room <name> [--with <id>...] [--add <id>...] '
              '[--read [N]] ["message"]   (or `bcast.py rooms` to list)')
        return 1
    if not _room_name_ok(name):
        print(f"bad room name '{name}' - use letters/digits/_~.- only.")
        return 1

    # REMOVE / LEAVE: take members OUT of a room (Max 2026-07-07 - cleanup). Any
    # session may prune a room (transparent, like --add); --leave removes yourself.
    # Case-insensitive match (x5 == X5). Removal is its own action - it does not
    # also post. Removing every member leaves an empty room (harmless; delete the
    # two files by hand if you want it gone).
    if leave:
        removes.append(me)
    if removes:
        m = _load_room(name)
        if not m:
            print(f"(no room '{name}')")
            return 0
        before = m.get("members") or []
        kept = [x for x in before if not any(_id_eq(x, r) for r in removes)]
        removed = [x for x in before if x not in kept]
        m["members"] = kept
        _save_room(name, m)
        print(f"room '{name}': removed {', '.join(removed) or '(none matched)'}. "
              f"Members now: {', '.join(kept) or '(empty)'}.")
        return 0

    # READ mode: anyone may inspect a room (transparent, not secret).
    if read_mode:
        m = _load_room(name)
        if not m:
            print(f"(no room '{name}')")
            return 0
        lines = _read_lines(_room_msgs_path(name))
        recs = _parse(lines)[-read_n:]
        print(f"=== ROOM '{name}'  members: {', '.join(m.get('members') or [])} ===")
        for r in recs:
            print(f"[{r.get('ts','?')}] {r.get('from','?')}: {r.get('msg','')}")
        print(f"=== end room '{name}' ({len(lines)} msgs total) ===")
        # Opening the door CLEARS this member's knock: advance the cursor so the
        # unread notification for this room stops showing next turn. (A non-member
        # who peeks leaves a cursor too - harmless, they get no knock regardless.)
        if me in (m.get("members") or []):
            st.setdefault("room_cursors", {})[name] = len(lines)
            _save_state(cwd, st)
        return 0

    # Ensure the room + membership (creating it on first touch; you always join).
    m = _load_room(name) or {"members": [], "created": time.strftime("%Y-%m-%d %H:%M:%S")}
    members = list(dict.fromkeys((m.get("members") or []) + [me] + withs + adds))
    created_now = not _load_room(name)
    m["members"] = members
    _save_room(name, m)

    if msg:
        os.makedirs(ROOMS_DIR, exist_ok=True)
        _append_rec(_room_msgs_path(name), me, msg)
        # advance my own room cursor so I never hear my own post
        st.setdefault("room_cursors", {})[name] = len(_read_lines(_room_msgs_path(name)))
        _save_state(cwd, st)

    others = [x for x in members if x != me]
    if created_now:
        print(f"ROOM '{name}' created. Members: {', '.join(members)}. "
              "It's a side-channel - off the team/joint boards. Members get a "
              "one-line KNOCK when it has unread messages but must open the door "
              "with `room {0} --read` to see them; anyone can read it.".format(name))
    if msg:
        print(f"posted to room '{name}' (heard by {', '.join(others) or 'just you so far'}).")
    elif not created_now:
        print(f"room '{name}' members now: {', '.join(members)}.")
    return 0


def _rooms_of(me):
    """Room names `me` is a member of (empty list if none). The posting barrier
    keys on this: a session that has been moved into a room faces resistance
    before posting to a board; a session in no room posts freely."""
    out = []
    if not me:
        return out
    for name in _all_rooms():
        m = _load_room(name)
        if m and me in (m.get("members") or []):
            out.append(name)
    return out


def _team_ids(team):
    """Every registered id whose team letter == `team` (live or stale), read from
    the state files. Used by moveteam to grab a whole team at once."""
    team = (team or "").strip().lower()
    ids = set()
    try:
        for fn in os.listdir(STATE_DIR):
            if not fn.endswith(".json"):
                continue
            try:
                with open(os.path.join(STATE_DIR, fn), encoding="utf-8") as f:
                    iid = (json.load(f).get("id") or "").strip()
            except Exception:
                continue
            if iid and _team_of(iid) == team:
                ids.add(iid)
    except Exception:
        pass
    return sorted(ids)


def cmd_moveteam(cwd, args):
    """moveteam <team> [room] ["message"] - move a WHOLE team into a room.

    ANY session (inside OR outside the team) may run it. Adds every registered id
    on that team to the room (created if needed) so the whole team talks there;
    the board posting-barrier then applies to those sessions (they must use
    --announce for a genuine whole-board message). Default room = 'team_<letter>'.
    """
    st = _load_state(cwd)
    me = st.get("id") or "?"
    if not args:
        print('usage: bcast.py moveteam <team> [room] ["message"]')
        return 1
    team = _team_of(args[0])   # accepts 'g' or 'g4' - both map to team 'g'
    rest = args[1:]
    room = None
    if rest and " " not in rest[0] and _room_name_ok(rest[0]):
        room = rest[0]; rest = rest[1:]
    if not room:
        room = "team_" + team
    if not _room_name_ok(room):
        print(f"bad room name '{room}' - use letters/digits/_~.- only.")
        return 1
    ids = _team_ids(team)
    if not ids:
        print(f"no registered sessions on team '{team}' - nothing to move.")
        return 1
    m = _load_room(room) or {"members": [], "created": time.strftime("%Y-%m-%d %H:%M:%S")}
    m["members"] = list(dict.fromkeys((m.get("members") or []) + ids))
    _save_room(room, m)
    note = (" ".join(rest).strip() or
            f"Team '{team}' moved into room '{room}' by {me}. Talk here now. The "
            "team/joint boards need a reason from here on (whole-board announcement "
            "only: shared resource, danger, or a Max announcement).")
    os.makedirs(ROOMS_DIR, exist_ok=True)
    _append_rec(_room_msgs_path(room), me, note)
    print(f"MOVED team '{team}' into room '{room}': {len(ids)} sessions "
          f"({', '.join(ids)}).")
    print("They get a knock next turn. The board posting-barrier is now in effect "
          "for them (they must confirm with --announce to post a whole-board item).")
    # Wake the moved sessions so they notice promptly (fail-open, best-effort).
    try:
        for tid in ids:
            if _id_eq(tid, me):
                continue
            sid = _session_id_for(tid)
            if sid and _listener_alive(sid):
                _drop_signal(sid, f"You were moved into room '{room}' by {me}. "
                                  f"Read it: bcast.py room {room} --read")
    except Exception:
        pass
    return 0


def cmd_read(cwd, hook=False, session_id=None):
    st = _load_state(cwd)
    me = st.get("id")
    # Only named branches hear the board. An unnamed chat (Max runs many
    # independent ones) gets nothing - no injection, no noise.
    if not me:
        return 0
    out = []
    if _split_on():
        # Hear your own team board + the joint board; per-board cursors.
        cursors = st.setdefault("cursors", {})
        for key, path in (("team", _board_for(me)), ("joint", JOINT_BOARD)):
            lines = _read_lines(path)
            for r in _parse(lines[cursors.get(key, 0):]):
                if r.get("from") == me:
                    continue
                if key == "joint":
                    r = dict(r); r["_joint"] = True
                out.append(r)
            cursors[key] = len(lines)
        out.sort(key=lambda r: r.get("ts", ""))
    else:
        lines = _read_lines()
        for r in _parse(lines[st.get("cursor", 0):]):
            if r.get("from") == me:
                continue
            out.append(r)
        st["cursor"] = len(lines)
    _save_state(cwd, st)

    # HALT banner: if a halt is in effect it is injected EVERY tick (even with
    # no new messages) so a looping branch reliably sees it and stops its loop.
    halt = _read_halt()
    full_halt = bool(halt and halt["mode"] == "FULL")
    chunks = []
    # PINNED RULES first - Max's standing orders for this board, re-shown EVERY
    # turn (like the halt banner) so they never scroll out of context. Shown even
    # under a halt: a rule is a rule. Team pins + any joint (all-team) pins.
    for _b, _lbl in ((_team_of(me), None),
                     ("joint", "(joint) PINNED RULES - Max's standing orders for ALL teams")):
        _pb = _pins_block(_b, _lbl)
        if _pb:
            chunks.append(_pb)
    if full_halt:
        chunks.append(
            "=== FULL HALT IN EFFECT ===\n"
            f"{halt['text']}\n"
            "STOP working AND STOP your timer: finish/abandon the current action, "
            "do NOT call ScheduleWakeup again, go quiet until Max re-arms you.\n"
            "=== end halt ===")
    elif halt and halt["mode"] == "STANDBY":
        chunks.append(
            "=== STANDBY - PAUSE, do NOT drop off ===\n"
            f"{halt['text']}\n"
            "PAUSE work: take no new or irreversible actions and start no new "
            "multi-step work. But KEEP your 4-min self-wake ARMED (re-arm "
            "ScheduleWakeup now) and keep reading the board every tick. The moment "
            "standby clears you resume work automatically - do NOT go silent.\n"
            "=== end standby ===")
    # WAKE CALLS - a teammate asked for you specifically (by name) or for any
    # active teammate (by time window). Surfaced LOUD and consumed once per
    # session so it never re-nags. Suppressed under a FULL halt (you're quiet).
    if not full_halt:
        for path, wrec in _pending_wakes_for(me, st.get("aka")):
            who = wrec.get("from", "?")
            if wrec.get("mode") == "name":
                aim = "you by name"
            else:
                aim = f"any teammate active in the last {wrec.get('window_h', WAKE_ACTIVE_WINDOW_HOURS)}h"
            chunks.append(
                "=== WAKE CALL - a teammate needs you ===\n"
                f"{who} woke {aim} at {wrec.get('ts','')}:\n"
                f"  \"{wrec.get('msg','')}\"\n"
                "If you can help: come to the board now - post a reply with "
                "`bcast.py post` (or `--joint`/`--name` to reach them) and pick up "
                "the thread. If you genuinely can't, a one-line 'can't help: <why>' "
                "still saves them waiting. You were pulled in on purpose.\n"
                "=== end wake call ===")
            _mark_wake_delivered(path, wrec, me)

    if out:
        header = "=== BROADCASTS FROM SIBLING BRANCHES (new since last turn) ==="
        body = "\n".join(
            f"[{r['ts']}] {'(joint) ' if r.get('_joint') else ''}{r['from']}: {r['msg']}"
            for r in out)
        footer = "=== end broadcasts ===" if not hook else (
            "=== end broadcasts (auto-injected; reply only if relevant) ===")
        chunks.append(f"{header}\n{body}\n{footer}")
    # ROOMS - INJECT the content (Max 2026-07-14). New model: boards AND rooms both
    # inject and are for BROADCASTS (a result/resource/danger the group needs). All
    # back-and-forth moves to a DIRECT 1:1 channel, which is simply a 2-member
    # 'pair_' room - so it injects into exactly those two sessions and never
    # contaminates the group. This SUPERSEDES the old knock-only design (2026-07-07):
    # rooms no longer just tap you, they deliver, consume-once like the boards (each
    # unread message shows exactly one turn, then the per-room cursor advances). A
    # one-time backlog is capped (ROOM_INJECT_CAP) so flipping an old busy room on
    # cannot dump hundreds of lines; older messages stay openable with --read.
    # Suppressed under a FULL halt (going quiet).
    if not full_halt:
        rc = st.setdefault("room_cursors", {})
        for name in _all_rooms():
            m = _load_room(name)
            if not m or me not in (m.get("members") or []):
                continue
            lines = _read_lines(_room_msgs_path(name))
            new = [r for r in _parse(lines[rc.get(name, 0):]) if r.get("from") != me]
            rc[name] = len(lines)  # consume-once: advance regardless of cap
            if not new:
                continue
            is_pair = name.startswith("pair_")
            shown = new[-ROOM_INJECT_CAP:]
            dropped = len(new) - len(shown)
            label = "DIRECT 1:1 MESSAGE" if is_pair else f"ROOM '{name}' (broadcast)"
            body = "\n".join(
                f"  [{r.get('ts','?')}] {r.get('from','?')}: {r.get('msg','')}"
                for r in shown)
            if dropped > 0:
                body = (f"  (+{dropped} older message(s) not shown - "
                        f"open with: bcast.py room {name} --read)\n" + body)
            close = "reply directly: bcast.py dm <them> \"...\"" if is_pair else \
                    "this is a broadcast; reply directly to one session with: bcast.py dm <name> \"...\""
            chunks.append(f"=== {label} - new since last turn ===\n{body}\n"
                          f"=== end ({close}) ===")
        _save_state(cwd, st)
    # HEARTBEAT - peer-default reminder. Fires on EVERY named-branch turn: peers
    # need no timer (the board is heard each turn); only an autonomous session
    # keeps a self-wake armed. Suppressed under a FULL halt (which stops the timer).
    if not full_halt:
        chunks.append(
            "[HEARTBEAT] Peer default: NO timer needed - do your part and "
            "merge+push when done (announce 'merging+pushing my part now', then "
            "push; a push never touches a sibling's files). ONLY if Max put you in "
            "autonomous mode: keep your ~240s self-wake armed and re-arm every wake.")
        # SIGNATURE reminder - injected every turn so the chat reliably stamps its
        # id + icon at the FRONT of every reply (Max needs to see what the session
        # actually calls itself; a hook can't edit the model's output, so the
        # visible stamp is behavioral - this keeps the tag in front of it each turn).
        chunks.append(
            f"[SIGNATURE] Lead EVERY reply with this tag so Max can tell your "
            f"chats apart: {_signature(me, session_id)}")
        # DIRECT-FIRST reflex (Max 2026-07-14): the boards + rooms are for BROADCASTS
        # only - a result/resource/danger the whole group needs. Any back-and-forth
        # with ONE session must go 1:1 so it never distracts the rest. Re-shown every
        # turn so 'DM them' becomes the instinct instead of shouting on the board.
        chunks.append(
            "[DIRECT-FIRST] Talk 1:1, broadcast only when the whole group needs it. "
            "For any back-and-forth with ONE session use a DIRECT message: "
            "bcast.py dm <name> \"msg\" - it reaches only them (a private 2-person "
            "channel, injected into their next turn), zero noise for everyone else. "
            "Keep the board/rooms for settled results, shared resources, and dangers.")
    if chunks:
        print("\n".join(chunks))
    return 0


def _read_halt():
    """Return {'mode': 'STANDBY'|'FULL', 'text': ...} or None.

    STANDBY = pause WORK but KEEP the 4-min timer armed (stay reachable, auto-resume).
    FULL    = stop work AND stop the timer (go fully quiet; Max must re-arm later).
    File format: first token before '|' is the mode; legacy files (no '|') = FULL.
    """
    try:
        with open(HALT_FILE, "r", encoding="utf-8") as f:
            raw = f.read().strip()
    except Exception:
        return None
    if not raw:
        return None
    mode, text = "FULL", raw
    head = raw.split("\n", 1)[0]
    if "|" in head:
        cand, rest = raw.split("|", 1)
        if cand.strip().upper() in ("STANDBY", "FULL"):
            mode, text = cand.strip().upper(), rest.strip()
    return {"mode": mode, "text": text}


def _set_halt(cwd, mode, reason):
    st = _load_state(cwd)
    me = st.get("id") or "?"
    os.makedirs(os.path.dirname(HALT_FILE), exist_ok=True)
    stamp = time.strftime('%Y-%m-%d %H:%M:%S')
    label = "STANDBY" if mode == "STANDBY" else "FULL HALT"
    body = f"[{stamp}] {label} set by {me}: {reason}"
    with open(HALT_FILE, "w", encoding="utf-8") as f:
        f.write(f"{mode}|{body}\n")
    # also drop a line on the board so it shows in history - on the JOINT board
    # when split is on (that's the cross-team history every worker actually reads),
    # else the legacy single board.
    try:
        _append_rec(JOINT_BOARD if _split_on() else BULLETIN, me, f"{label}: {reason}")
    except Exception:
        pass
    return me


def cmd_standby(cwd, reason):
    _set_halt(cwd, "STANDBY", reason)
    print(f"STANDBY set: {reason}\nWorkers PAUSE work but KEEP their 4-min timers "
          "(stay reachable + auto-resume the moment standby clears). Use 'resume' to clear.")


def cmd_halt(cwd, reason):
    _set_halt(cwd, "FULL", reason)
    print(f"FULL HALT set: {reason}\nWorkers stop working AND stop their timers on the "
          "next board read. Use 'resume' to clear; Max must re-arm timers after a full halt.")


def cmd_resume(cwd):
    try:
        os.remove(HALT_FILE)
        print("HALT/STANDBY cleared - workers resume. (After a STANDBY they auto-resume; "
              "after a FULL halt Max must re-arm their timers.)")
    except FileNotFoundError:
        print("No halt or standby was in effect.")
    except Exception as e:
        print(f"could not clear halt: {e}")


def _ts_epoch(ts):
    try:
        return time.mktime(time.strptime(ts, "%Y-%m-%d %H:%M:%S"))
    except Exception:
        return None


def _board_files():
    """Every LIVE board file in BASE (per-team bulletin_<x>.jsonl + joint +
    legacy bulletin.jsonl). Excludes the archive copies."""
    out = []
    try:
        for fn in os.listdir(BASE):
            if (fn.startswith("bulletin") and fn.endswith(".jsonl")
                    and ".archive" not in fn):
                out.append(os.path.join(BASE, fn))
    except Exception:
        pass
    return out


def _archive_path(board_path):
    d = os.path.join(BASE, "archive")
    os.makedirs(d, exist_ok=True)
    base = os.path.basename(board_path)[:-len(".jsonl")]
    return os.path.join(d, base + ".archive.jsonl")


def _cursor_key_for_board(board_path):
    """Which state cursor indexes this board:
      ('joint', None)  -> st['cursors']['joint'] for EVERY session
      ('team', <team>) -> st['cursors']['team'] only for sessions on that team
      ('legacy', None) -> st['cursor'] (old single board) for every session"""
    name = os.path.basename(board_path)
    if name == "bulletin_joint.jsonl":
        return ("joint", None)
    if name == "bulletin.jsonl":
        return ("legacy", None)
    m = re.match(r"bulletin_(.+)\.jsonl$", name)
    if m:
        return ("team", m.group(1))
    return (None, None)


def _adjust_cursors(kind, team, k):
    """Shift every affected cursor DOWN by k (the count of oldest lines removed
    from a board). Uniform subtraction is exact: removed lines are at indices
    [0,k) so any cursor >= k maps to cursor-k (same unread tail); a dormant
    cursor < k clamps to 0 (that session re-hears only the recent kept tail)."""
    if not kind or k <= 0:
        return
    try:
        files = os.listdir(STATE_DIR)
    except Exception:
        return
    for fn in files:
        if not fn.endswith(".json"):
            continue
        p = os.path.join(STATE_DIR, fn)
        try:
            with open(p, "r", encoding="utf-8") as f:
                st = json.load(f)
        except Exception:
            continue
        changed = False
        if kind == "legacy":
            if "cursor" in st:
                st["cursor"] = max(0, st.get("cursor", 0) - k)
                changed = True
        elif kind == "joint":
            cur = st.get("cursors")
            if isinstance(cur, dict) and "joint" in cur:
                cur["joint"] = max(0, cur["joint"] - k)
                changed = True
        elif kind == "team":
            if st.get("id") and _team_of(st["id"]) == team:
                cur = st.get("cursors")
                if isinstance(cur, dict) and "team" in cur:
                    cur["team"] = max(0, cur["team"] - k)
                    changed = True
        if changed:
            try:
                with open(p, "w", encoding="utf-8") as f:
                    json.dump(st, f)
            except Exception:
                pass


def cmd_rolloff(cwd, days=None, apply=False):
    """GRADUAL RETIREMENT: move board entries older than `days` (default
    RETENTION_DAYS) into the on-demand archive, trim them from the live board,
    and shift cursors so nobody re-hears or skips anything. Dry-run by default."""
    days = RETENTION_DAYS if days is None else days
    cutoff = time.time() - days * 86400
    plan = []  # (board_path, k, total)
    for bp in _board_files():
        lines = _read_lines(bp)
        k = 0
        for l in lines:
            try:
                rec = json.loads(l)
            except Exception:
                k += 1  # unparseable junk line at the front -> retire it too
                continue
            e = _ts_epoch(rec.get("ts", ""))
            if e is not None and e < cutoff:
                k += 1
            else:
                break  # boards are chronological: first recent line ends the prefix
        if k > 0:
            plan.append((bp, k, len(lines)))
    if not plan:
        print(f"rolloff: nothing older than {days}d on any board. Boards already lean.")
        return 0
    print(f"rolloff ({'APPLY' if apply else 'DRY-RUN'}) - retire entries older "
          f"than {days} days to the on-demand archive:")
    for bp, k, total in plan:
        print(f"  {os.path.basename(bp)}: retire {k} of {total} "
              f"(keep {total - k} recent)")
    if not apply:
        print("DRY-RUN only. To execute: python bcast.py rolloff --apply")
        return 0
    for bp, k, _total in plan:
        cur = _read_lines(bp)
        if k > len(cur):
            k = len(cur)
        old = cur[:k]
        ap = _archive_path(bp)
        with open(ap, "a", encoding="utf-8") as f:
            for l in old:
                f.write(l + "\n")
        # Re-read just before the rewrite and drop exactly the first k IMMUTABLE
        # lines, keeping everything from k onward incl. any append that landed
        # during processing (append-only board => the prefix can never change).
        fresh = _read_lines(bp)
        keep = fresh[k:] if len(fresh) >= k else []
        tmp = bp + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            for l in keep:
                f.write(l + "\n")
        os.replace(tmp, bp)  # atomic swap; no reader sees a half-written board
        kind, team = _cursor_key_for_board(bp)
        _adjust_cursors(kind, team, k)
        print(f"  retired {k} from {os.path.basename(bp)} -> {os.path.basename(ap)}")
    print("rolloff DONE. Retired entries stay readable on demand: "
          "python bcast.py archive [board] [n]")
    return 0


def cmd_archive(cwd, which=None, n=20):
    """Read the on-demand board archive (retired entries). Never auto-loaded."""
    d = os.path.join(BASE, "archive")
    files = []
    try:
        for fn in os.listdir(d):
            if fn.endswith(".archive.jsonl"):
                files.append(os.path.join(d, fn))
    except Exception:
        pass
    if which:
        files = [f for f in files if which in os.path.basename(f)]
    if not files:
        print("archive: nothing retired yet (or no board matches that name).")
        return 0
    recs = []
    for f in files:
        recs += _parse(_read_lines(f))
    recs.sort(key=lambda r: r.get("ts", ""))
    tail = recs[-n:] if n and len(recs) > n else recs
    print(f"=== BOARD ARCHIVE (last {len(tail)} of {len(recs)} retired entries) ===")
    for r in tail:
        print(f"[{r.get('ts', '')}] {r.get('from', '?')}: {r.get('msg', '')}")
    return 0


def cmd_migrate(cwd, confirm=False):
    """CUTOVER to split-per-team boards. Run ONLY on Max's go, b-team idle.
    Archives the live single board and flips the split flag on. Fail-safe:
    requires an explicit CONFIRM token and refuses if already split."""
    if _split_on():
        print("Split boards already ON. Nothing to do. (delete SPLIT_BOARDS.on to revert)")
        return 0
    if not confirm:
        print("DRY-RUN. This will:\n"
              f"  1. archive the live board {BULLETIN}\n"
              f"  2. create the flag {SPLIT_FLAG} (turns split ON for ALL sessions)\n"
              "After cutover every worker must re-run `whoami <id>` so its cursors\n"
              "rebind to its team board + joint. Do NOT run while the b-team is\n"
              "mid-deploy. To proceed: python bcast.py migrate CONFIRM")
        return 0
    stamp = time.strftime("%Y%m%d_%H%M%S")
    archived = None
    if os.path.exists(BULLETIN):
        arch_dir = os.path.join(BASE, "archive")
        os.makedirs(arch_dir, exist_ok=True)
        archived = os.path.join(arch_dir, f"bulletin_premigrate_{stamp}.jsonl")
        os.replace(BULLETIN, archived)
    with open(SPLIT_FLAG, "w", encoding="utf-8") as f:
        f.write(f"split boards enabled {stamp}\n")
    print("CUTOVER DONE. Split-per-team boards are now ON.")
    if archived:
        print(f"  Old mixed board archived to: {archived}")
    print("  Per-team boards (bulletin_<letter>.jsonl) + bulletin_joint.jsonl start fresh.")
    print("  TELL EVERY WORKER: re-run `python bcast.py whoami <your-id>` now so it\n"
          "  rebinds to its team board + joint (old cursors pointed at the archived board).")
    return 0


SIG_ENFORCE_EVERY = 10  # remind at most once per this many answers


def _last_assistant_text(transcript_path):
    """Return the text of the most recent assistant message in a Claude Code
    transcript (JSONL), or '' if it can't be read. Only the leading run of text
    matters for the tag check, so we join text blocks in order."""
    if not transcript_path or not os.path.exists(transcript_path):
        return ""
    last = ""
    try:
        with open(transcript_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                if rec.get("type") != "assistant":
                    continue
                msg = rec.get("message", {}) or {}
                if msg.get("role") != "assistant":
                    continue
                content = msg.get("content", "")
                if isinstance(content, str):
                    txt = content
                else:
                    txt = "".join(
                        b.get("text", "") for b in content
                        if isinstance(b, dict) and b.get("type") == "text")
                if txt.strip():
                    last = txt
    except Exception:
        return ""
    return last


def cmd_enforce_sig(data):
    """Stop-hook: periodically enforce that a named session leads its reply with
    its icon tag. Returns 0 to let the reply stand; prints a reminder to stderr
    and returns 2 to BLOCK (forcing a re-answer) on the enforcement tick when the
    tag is missing. Silent + harmless for unnamed sessions."""
    # Don't fire again on the redo we ourselves forced (built-in loop guard).
    if data.get("stop_hook_active"):
        return 0
    cwd = data.get("cwd") or os.getcwd()
    # Key state to THIS session exactly like the read-hook does, else _load_state
    # sees no id and enforcement silently no-ops (the "reported fixed but didn't"
    # trap). The Stop payload carries the same session_id the read-hook uses.
    _resolve_session(cwd, data.get("session_id"))
    me = _load_state(cwd).get("id")
    if not me:
        return 0  # unnamed chat - nothing to stamp
    st = _load_state(cwd)
    n = int(st.get("sig_enforce_count", 0)) + 1
    st["sig_enforce_count"] = n
    _save_state(cwd, st)
    if n % SIG_ENFORCE_EVERY != 0:
        return 0  # not an enforcement tick
    sig = _signature(me)
    icon = sig.split(" ", 1)[0]
    reply = _last_assistant_text(data.get("transcript_path"))
    # Already compliant (leads with the icon or the full tag)? Let it stand.
    if reply.lstrip().startswith(icon) or reply.lstrip().startswith(sig):
        return 0
    sys.stderr.write(
        f"[SIGNATURE ENFORCER] You are '{me}'. Max needs every reply led by your "
        f"tag so he can tell his chats apart. Re-send your answer starting with:\n"
        f"    {sig}\n"
        f"(reminder fires once every {SIG_ENFORCE_EVERY} answers)")
    return 2


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 0
    cmd = args[0]

    # For the hook, cwd comes from stdin JSON, not the process cwd. The same
    # stdin payload also carries the live Claude session_id (the per-branch
    # discriminator the wake_listener uses), so grab it for the auto branch glyph.
    if cmd == "read" and "--hook" in args:
        cwd, session_id = None, None
        try:
            data = json.load(sys.stdin)
            cwd = data.get("cwd")
            session_id = data.get("session_id")
        except Exception:
            cwd = None
        if not cwd:
            cwd = os.getcwd()
        # Drop the owner pointer (cwd -> session_id) so a manual command in the
        # SAME turn can key its state to this session, then key our own state too.
        _write_owner(cwd, session_id)
        _resolve_session(cwd, session_id)
        return cmd_read(cwd, hook=True, session_id=session_id)

    # STOP-HOOK SIGNATURE ENFORCER (Max 2026-07-16): after a reply is written,
    # every Nth answer this checks the reply led with the session's icon tag and,
    # if not, BLOCKS once to make the model re-answer WITH it. Periodic (not every
    # turn) so it reminds without nagging. cwd + transcript come from stdin JSON.
    if cmd == "enforce-sig":
        data = {}
        try:
            data = json.load(sys.stdin)
        except Exception:
            data = {}
        return cmd_enforce_sig(data)

    cwd = os.getcwd()
    _resolve_session(cwd)
    if cmd == "whoami":
        if len(args) < 2:
            print("usage: python bcast.py whoami b2")
            return 1
        return cmd_whoami(cwd, args[1])
    if cmd == "who":
        return cmd_who(cwd)
    if cmd == "rolloff":
        days = None
        apply = False
        for a in args[1:]:
            if a == "--apply":
                apply = True
            elif a.isdigit():
                days = int(a)
        return cmd_rolloff(cwd, days=days, apply=apply)
    if cmd == "archive":
        which = None
        n = 20
        for a in args[1:]:
            if a.isdigit():
                n = int(a)
            else:
                which = a
        return cmd_archive(cwd, which=which, n=n)
    if cmd == "post":
        rest = args[1:]
        joint = False
        force_all = False
        as_id = None
        # --all / @all = explicit broadcast to ALL teams (never demoted). --joint
        # is now just a hint: routing follows your @mentions (cross-team -> joint,
        # else -> your team board), so --joint and no-flag behave the same.
        # --as <id> = post under <id> regardless of cwd (escape for a session that
        # must post from a shared cwd, e.g. cd'd into the main checkout to commit).
        announce = False
        kept = []
        i = 0
        while i < len(rest):
            a = rest[i]
            if a in ("--all", "@all"):
                force_all = True
            elif a == "--joint":
                joint = True
            elif a in ("--announce", "--board-announce", "--yes-board"):
                announce = True
            elif a == "--as" and i + 1 < len(rest):
                as_id = rest[i + 1]; i += 1
            else:
                kept.append(a)
            i += 1
        if not kept:
            print('usage: python bcast.py post "message"   '
                  '(--all = broadcast to ALL teams; --announce = confirm a genuine '
                  'whole-board item when you are in a room; --as <id> = post under '
                  '<id> from any cwd; otherwise cross-team @mentions auto-route to '
                  'joint, own-team stays on your team board)')
            return 1
        return cmd_post(cwd, " ".join(kept), joint=joint, force_all=force_all,
                        as_id=as_id, announce=announce)
    if cmd == "read":
        return cmd_read(cwd, hook=False)
    if cmd in ("dm", "direct", "msg", "tell"):
        return cmd_dm(cwd, args[1:])
    if cmd == "room":
        return cmd_room(cwd, args[1:])
    if cmd == "rooms":
        return cmd_rooms(cwd)
    if cmd in ("moveteam", "herd"):
        return cmd_moveteam(cwd, args[1:])
    if cmd == "catchup":
        n = int(args[1]) if len(args) > 1 and args[1].isdigit() else 12
        return cmd_catchup(cwd, n)
    if cmd == "standby":
        reason = " ".join(args[1:]) if len(args) > 1 else "standby - pause work, keep timers"
        return cmd_standby(cwd, reason)
    if cmd == "halt":
        reason = " ".join(args[1:]) if len(args) > 1 else "manual full halt"
        return cmd_halt(cwd, reason)
    if cmd == "resume":
        return cmd_resume(cwd)
    if cmd in ("dedupe", "resolve"):
        window = None
        apply = False
        for a in args[1:]:
            if a == "--apply":
                apply = True
            elif a.isdigit():
                window = int(a) * 3600  # hours
        return cmd_dedupe(cwd, window_sec=window, apply=apply)
    if cmd in ("pin", "unpin", "pins"):
        rest = args[1:]
        board_arg = None
        joint = False
        kept = []
        i = 0
        while i < len(rest):
            a = rest[i]
            if a == "--board" and i + 1 < len(rest):
                board_arg = rest[i + 1]; i += 1
            elif a in ("--joint", "--all-teams"):
                joint = True
            else:
                kept.append(a)
            i += 1
        if cmd == "pins":
            return cmd_pins(cwd, board_arg=board_arg)
        if cmd == "unpin":
            which = kept[0] if kept else ("--all" if "--all" in rest else None)
            if not which:
                print("usage: bcast.py unpin <id|--all> [--board <letter>|--joint]")
                return 1
            return cmd_unpin(cwd, which, board_arg=board_arg, joint=joint)
        # pin
        if not kept:
            print('usage: bcast.py pin "rule text" [--board <letter>|--joint]   '
                  '(Max-only: pin ONLY when Max explicitly tells you to)')
            return 1
        return cmd_pin(cwd, " ".join(kept), board_arg=board_arg, joint=joint)
    if cmd == "wake":
        return cmd_wake(cwd, args[1:])
    if cmd == "migrate":
        return cmd_migrate(cwd, confirm=("CONFIRM" in args[1:]))
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
