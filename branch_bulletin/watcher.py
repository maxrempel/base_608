"""bcast watcher - unsupervised safety net for the split-board team system.

Runs periodically as a scheduled task (no human, no live Claude session sitting
on the board). It is the AUTOMATED replacement for a session manually policing
coordination. Three passes per run:

  0. POLLUTION WATCHER (Max 2026-07-03, ENFORCING): the JOINT board is CROSS-TEAM
     ONLY. DeepSeek reads the joint tail; a thread that is entirely within one team
     is POLLUTION. The watcher posts a firm MOVE ORDER (not a suggestion) AND
     force-wakes the offending team's live sessions so the order actually lands.
     Persists until the thread moves or genuinely goes cross-team. This is the
     semantic backstop to bcast.cmd_post's source-side POLLUTION GUARD (which
     already reroutes an accidental --joint single-team post to the team board at
     post time). See the MISROUTE pass in main().


  1. DETERMINISTIC (cheap, always): sweep state files for duplicate LIVE ids -
     two+ sessions holding the same id, both touched within the liveness window.
     That is a manager/role collision (the 2026-06-08 two-manager bug) that
     slipped past the in-tool whoami guard. High confidence -> ONE cooled-down
     board nudge to the TEAM. NEVER pages Max.

  2. JUDGMENT (Opus, low context, only when the board MOVED since last run):
     hand a fresh tiny Opus context the recent cross-team traffic + the live
     roster and ask "is a coordination problem brewing?". If yes -> a board
     nudge to the TEAM. NEVER pages Max. Opus runs only on new activity, so a
     quiet board costs nothing.

  NOTE (Max split, 2026-06-09): this is the NUMBERING watcher - it watches ids /
  team assignments and helps the TEAM fix them. It must NEVER page Max. Max's
  phone belongs to the separate SAFETY watcher (safety_watcher.py, DeepSeek V4+).

Design rules (Max, 2026-06-08): systems must be SELF-EXPLANATORY - this never
lectures or trains the board, it acts/alerts only on real trouble. FAIL-OPEN
everywhere - a broken watcher must never wedge a session or crash a run.
"""
import os, re, sys, json, time, glob, urllib.request, urllib.parse, traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bcast

SSH = r"C:\Users\maxre\Nextcloud\zSyncMain\ssh"
# Switched 2026-06-13 from Anthropic Opus (~$10/day unattended) to DeepSeek
# (same key the safety watcher uses, ~50x cheaper). The Anthropic key must NOT be
# used by any unattended task without Max's explicit permission.
DEEPSEEK_KEY_FILE = os.path.join(SSH, "deepseek_api_key_20260226.txt")
DS_URL = "https://api.deepseek.com/chat/completions"
TELEGRAM_CRED_FILE = os.path.join(SSH, "telegram_critical_alarms_bot_token_20260604.txt")
WATCHER_STATE = os.path.join(bcast.BASE, "watcher_state.json")
WATCHER_LOG = os.path.join(bcast.BASE, "watcher.log")
# deepseek-chat = the NON-reasoning model (Max 2026-07-10 cost cut). The old
# deepseek-v4-flash is a reasoning model that spent tokens on hidden reasoning
# (forcing the 300->3000 cap below) and drove most of the unattributed spend.
MODEL = "deepseek-chat"
NUDGE_COOLDOWN_SEC = 30 * 60   # don't re-nudge the same collision within 30 min
OPUS_ALERT_COOLDOWN_SEC = 60 * 60  # don't re-Telegram the SAME Opus issue within 60 min
# POLLUTION WATCHER: a joint-board thread that is really single-team belongs on that
# team's board. Max's spec (2026-07-03, SUPERSEDES the 2026-06-26 "suggestive, trust
# their judgment" stance - that was TOOTHLESS and the joint board stayed polluted):
# be FIRM and ENFORCING, not a polite suggestion. A pollution nudge is a MOVE ORDER,
# and it FORCE-WAKES the offending team's live sessions so the order actually lands in
# a session's context instead of sitting unread. It persists (re-fires every cooldown
# while DeepSeek still sees it) and clears the instant DeepSeek no longer flags it.
# NOTE the source-side POLLUTION GUARD in bcast.cmd_post now blocks the common case
# (--joint with no cross-team is rerouted to the team board at post time); this watcher
# is the semantic backstop for --all abuse (single-team content force-pushed to joint),
# which the source guard intentionally cannot judge without reading the content.
MISROUTE_NUDGE_COOLDOWN_SEC = 20 * 60  # re-nudge the same pollution at most every 20 min


def log(msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S')}  {msg}"
    try:
        with open(WATCHER_LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass
    print(line)


def _read_first_token(path, prefix="Token:"):
    """Pull a 'Token: xxx' value from a cred file, else the first non-empty line."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            txt = f.read()
    except Exception:
        return None
    for ln in txt.splitlines():
        if ln.strip().lower().startswith(prefix.lower()):
            return ln.split(":", 1)[1].strip()
    for ln in txt.splitlines():
        if ln.strip():
            return ln.strip()
    return None


def telegram_alert(text):
    token = _read_first_token(TELEGRAM_CRED_FILE)
    if not token:
        log("ALERT-SKIP: no telegram token")
        return
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = urllib.parse.urlencode({
            "chat_id": "1395850773",
            "text": "[bcast watcher] " + text,
        }).encode()
        urllib.request.urlopen(url, data=data, timeout=15).read()
        log(f"ALERT-SENT: {text[:120]}")
    except Exception as e:
        log(f"ALERT-FAIL: {e}")


def _watch_state():
    try:
        with open(WATCHER_STATE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"joint_cursor": 0, "last_nudge": {}}


def _save_watch_state(st):
    try:
        with open(WATCHER_STATE, "w", encoding="utf-8") as f:
            json.dump(st, f)
    except Exception as e:
        log(f"STATE-SAVE-FAIL: {e}")


# ---------------- PASS 1: deterministic duplicate-live-id sweep ----------------

def _identity_key(st, path):
    """The stable 'which physical tab' key for a state file. For a worktree cwd
    (1:1 with a tab) that IS the cwd - so a tab whose Claude session_id churned
    (resume/restart) collapses to ONE key instead of looking like two rivals. For a
    shared checkout (many sessions) fall back to session_id/filename."""
    cwd = st.get("cwd")
    try:
        if cwd and bcast._is_worktree(cwd):
            return "cwd:" + bcast._norm_cwd(cwd)
    except Exception:
        pass
    return "sid:" + (st.get("session_id") or path)


def live_roster():
    """Map id -> {identity_key: youngest_age} among LIVE state files. Keying by
    physical-tab identity (not per-file) means one tab across a session_id boundary
    counts ONCE, so the phantom 'two live E125' no longer trips the dup alarm."""
    roster = {}
    for p in glob.glob(os.path.join(bcast.STATE_DIR, "*.json")):
        try:
            with open(p, "r", encoding="utf-8") as f:
                st = json.load(f)
        except Exception:
            continue
        bid = st.get("id")
        if not bid:
            continue
        try:
            age = time.time() - os.path.getmtime(p)
        except Exception:
            continue
        if age <= bcast.LIVENESS_WINDOW_SEC:
            k = _identity_key(st, p)
            d = roster.setdefault(bid, {})
            if k not in d or age < d[k]:
                d[k] = age
    return roster


def check_duplicates(wstate):
    """A duplicate live id is a team-resolvable conflict. The watcher has the
    AUTHORITY to make conflict + safety the priority, so it drives the TEAM to
    fix it via the board and does NOT page Max -- no human action is required."""
    roster = live_roster()
    # A REAL duplicate = the same id held by 2+ DISTINCT physical tabs (different
    # worktrees / shared-checkout sessions). Same id in ONE worktree across a
    # session_id churn collapsed to a single key upstream, so it never lands here.
    dups = {bid: keys for bid, keys in roster.items() if len(keys) >= 2}
    acted = False
    if dups:
        # ELEGANT FIX (Max 2026-07-14, "fix the board spam long-term"): a duplicate
        # id is a CODE-RESOLVABLE collision, so RESOLVE it in code - never nag the
        # board about it. cmd_dedupe keeps the freshest session's id and auto-stamps
        # each younger rival to a free suffix (b/c/d...), notifying that one demoted
        # session on its OWN board exactly once. This obeys Max's law "hard rules
        # must be scripted, not broadcast": the old repeating "two live sessions are
        # BOTH 'X' - hand-resolve it" nag (hundreds of identical posts over days)
        # is GONE. The watcher now silently makes the collision impossible instead
        # of asking humans to fix it forever. Fail-open: a dedupe error never wedges
        # the sweep and never falls back to nagging.
        try:
            bcast.cmd_dedupe(bcast.BASE, apply=True)
            acted = True
            log(f"DUP auto-resolved in code (dedupe sweep): {sorted(dups)}")
        except Exception as e:
            log(f"DEDUPE-FAIL (fail-open, no board nag): {e}")
    return roster, dups, acted


# ---------------- PASS 2: low-context Opus judgment (only on new traffic) -------

# The judgment pass must never feed on the MONITORS' own posts. A record whose
# author is a monitor (watcher/safety) is a nudge ABOUT a problem, not a session
# doing work - if we let DeepSeek read the watcher's own "two live X" nudges it
# re-derives them as a fresh "coordination risk", which becomes a new board post,
# which the next run reads and re-raises: a self-sustaining echo-loop spam (seen
# live 2026-07-02; the dup-collision domain is Pass 1's deterministic job anyway).
_MONITOR_AUTHORS = {"watcher", "safety", "pollution-watcher"}


def recent_board_snapshot(limit=18):
    """Merge the tail of every team board + joint, newest last, as compact text.
    Excludes the monitors' own posts so the judgment pass cannot echo-loop on its
    own nudges (author field is 'from', not 'id')."""
    paths = sorted(glob.glob(os.path.join(bcast.BASE, "bulletin_*.jsonl")))
    recs = []
    for p in paths:
        team = os.path.basename(p)[len("bulletin_"):-len(".jsonl")]
        for r in bcast._parse(bcast._read_lines(p)):
            if (r.get("from") or "").strip().lower() in _MONITOR_AUTHORS:
                continue
            r = dict(r)
            r["_team"] = team
            recs.append(r)
    recs.sort(key=lambda r: r.get("ts", ""))
    recs = recs[-limit:]
    lines = []
    for r in recs:
        who = r.get("from", "?")
        board = r.get("_team", "?")
        lines.append(f"[{board}] {who}: {r.get('msg','')}")
    return "\n".join(lines), len(recs)


def joint_len():
    try:
        return len(bcast._read_lines(bcast.JOINT_BOARD))
    except Exception:
        return 0


def ask_opus(snapshot, roster):
    # Name kept for callers; now backed by DeepSeek, not Opus (cost switch 2026-06-13).
    key = _read_first_token(DEEPSEEK_KEY_FILE)
    if not key:
        log("DS-SKIP: no deepseek key")
        return None
    roster_txt = ", ".join(f"{bid}(~{int(min(a.values()))}s)" for bid, a in sorted(roster.items()))
    prompt = (
        "You are a silent watcher over a multi-agent coordination board. Teams are "
        "lettered (b-team, c-team, ...). Each session has an id like b1/c5. Sessions "
        "must NOT both manage the same task, must NOT both edit the same file blindly, "
        "and a takeover requires a liveness handshake.\n\n"
        f"LIVE sessions now: {roster_txt or '(none)'}\n\n"
        f"RECENT BOARD TRAFFIC (oldest first):\n{snapshot or '(empty)'}\n\n"
        "Is a coordination problem BREWING that a sibling acting unaware would get "
        "wrong (e.g. two sessions on the same task, an unconfirmed takeover, two "
        "sessions about to edit the same resource)? Reply ONLY compact JSON: "
        '{\"issue\": true|false, \"severity\": \"low\"|\"high\", \"key\": \"...\", \"summary\": \"...\"}'
        "\n\"key\" is a SHORT STABLE slug naming THIS specific problem (the sessions "
        "+ resource involved, lowercase-hyphenated, e.g. \"b0-collision\" or "
        "\"b6-appjs-stale-baseline\"). Use the SAME key on later runs while it is the "
        "SAME underlying problem, so repeats can be deduped; a different problem gets "
        "a different key."
    )
    body = json.dumps({
        "model": MODEL,
        "max_tokens": 3000,  # flash is a reasoning model; 300 silently returned empty
                             # content (finish=length) on full snapshots - see _ds_json
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }).encode()
    req = urllib.request.Request(
        DS_URL, data=body,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
    )
    try:
        resp = urllib.request.urlopen(req, timeout=180).read()
        data = json.loads(resp)
        text = (data["choices"][0]["message"].get("content") or "")
        s, e = text.find("{"), text.rfind("}")
        if s >= 0 and e > s:
            return json.loads(text[s:e + 1])
    except Exception as e:
        log(f"DS-FAIL: {e}")
    return None


def _ds_json(prompt, max_tokens=3000):
    """One DeepSeek call returning the embedded JSON object, or None. Shared by the
    misroute pass; ask_opus keeps its own inline call so working code is untouched.
    NOTE: MODEL is now deepseek-chat (non-reasoning) - it emits the JSON directly, so
    the old empty-content-on-tight-budget problem is gone. The 3000 cap is kept as a
    harmless ceiling (chat only bills the ~tiny actual answer, not the cap)."""
    key = _read_first_token(DEEPSEEK_KEY_FILE)
    if not key:
        log("DS-SKIP: no deepseek key")
        return None
    body = json.dumps({
        "model": MODEL,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }).encode()
    req = urllib.request.Request(
        DS_URL, data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    try:
        resp = urllib.request.urlopen(req, timeout=180).read()
        data = json.loads(resp)
        text = (data["choices"][0]["message"].get("content") or "")
        s, e = text.find("{"), text.rfind("}")
        if s >= 0 and e > s:
            return json.loads(text[s:e + 1])
    except Exception as ex:
        log(f"DS-FAIL(misroute): {ex}")
    return None


def ask_misroute(snapshot):
    """Look ONLY at [joint]-tagged lines: is a discussion really single-team and so
    belongs on that team's own board? Conservative - any cross-team participant or
    @mention means it is CORRECTLY on joint. Returns {misroute,team,key,summary}."""
    prompt = (
        "You are a silent watcher over a multi-agent board. Teams are lettered "
        "(b-team, c-team, ...); a session id's leading letter is its team (f4->f, "
        "c16->c). There is a shared JOINT board plus one board per team. JOINT is "
        "ONLY for CROSS-team coordination. A COMMON MISTAKE: sessions hold a "
        "discussion on JOINT that actually involves only ONE team (every participant "
        "shares the same team letter, and it does not address/@mention any other "
        "team) - that belongs on that team's own board.\n\n"
        f"RECENT BOARD TRAFFIC (oldest first; each line tagged [board]):\n{snapshot or '(empty)'}\n\n"
        "Look ONLY at lines tagged [joint]. Is there a discussion there that is "
        "ENTIRELY within ONE team and so should move to that team's board? Be "
        "CONSERVATIVE: if any cross-team participant or @mention of another team's id "
        "is involved, it is CORRECTLY on joint - report misroute=false. Reply ONLY "
        "compact JSON: {\"misroute\": true|false, \"team\": \"<single letter>\", "
        "\"key\": \"<short stable slug naming this thread>\", \"summary\": \"<one line>\"}"
    )
    return _ds_json(prompt)


_SESSION_ID_RE = re.compile(r'\b([a-z])\d+[a-z]?\b')


def _fingerprint(summ):
    """Deterministic dedup key derived from a FACT in the summary, not the LLM slug.

    The DeepSeek judge rewords its own slug every run - the same real event
    ("x15b is worried about the Kenefick BAM deletion") became 8 different keys in
    70 minutes on 2026-07-13, defeating the LLM-slug-based dedup and flooding the
    joint board with `coordination risk (watcher): ...` every 10 min.

    Watcher alarms are always ABOUT a team (coordination inside team x, team d,
    team p, etc.). Team letter is the strongest deterministic FACT in the alarm:
    it comes straight from a session id like `x15b` / `X7A` / `d56a`, which the
    LLM includes even while rewording every noun around it. So dedup on the SET
    of team-letters mentioned. Same underlying event -> same team-letter set ->
    same fingerprint across every LLM rewording.

    Trade-off: two GENUINELY different high-severity coord risks on the SAME team
    within one cooldown collapse to one alarm. That's fine - the watcher only
    posts to the joint board (not Max's phone), the cooldown is short (30-60 min),
    and one alarm per team per cooldown matches the coarseness of the problem this
    watcher is looking at (a whole-team coordination pattern, not a per-file thing).

    Empty string on empty input; caller should fall back to the LLM slug.
    """
    if not summ:
        return ""
    letters = sorted({m.group(1) for m in _SESSION_ID_RE.finditer(summ.lower())})
    if not letters:
        return ""
    return "team-" + "".join(letters)


def _opus_alert_is_new(wstate, key, now):
    """True if this Opus issue-key has NOT been Telegram-alerted within the
    cooldown. Records the alert time when it returns True. Keeps Max's phone to
    one ping per distinct problem per hour; genuinely NEW problems still ping."""
    seen = wstate.setdefault("last_opus_alert", {})
    last = seen.get(key, 0)
    if now - last < OPUS_ALERT_COOLDOWN_SEC:
        return False
    seen[key] = now
    return True


def _wake_team(team, msg):
    """Force-wake every LIVE session on `team` so the pollution order actually
    lands in a session's context instead of sitting unread on the board. Reuses
    bcast's own live-listener detection + signal drop. Fail-open, returns count."""
    woke = 0
    try:
        for bid in bcast._live_wakeable_ids():
            try:
                if bcast._team_of(bid) != team:
                    continue
                sid = bcast._session_id_for(bid)
                if sid and bcast._listener_alive(sid) and bcast._drop_signal(sid, msg):
                    woke += 1
            except Exception:
                continue
    except Exception:
        pass
    return woke


def main():
    try:
        wstate = _watch_state()

        # 5-DAY BOARD CLEANUP (Max 2026-07-03): archive entries older than
        # RETENTION_DAYS (=5) off EVERY board each run, so boards stay lean and no
        # session's auto-loaded context carries week-old junk. cmd_rolloff MOVES aged
        # entries to the on-demand archive (never deletes) and shifts cursors so nobody
        # re-hears or skips anything; idempotent - a no-op once boards are already lean.
        # Folded into the existing 10-min watcher run instead of a separate scheduled
        # task (one unattended job already exists - reuse it).
        try:
            bcast.cmd_rolloff(None, days=bcast.RETENTION_DAYS, apply=True)
        except Exception as e:
            log(f"ROLLOFF-FAIL (fail-open): {e}")

        # Flush the housekeeping-flag daily digest if a day has passed (any session
        # can `flag` a meta problem; routine flags batch into one daily Telegram+email
        # digest, urgent ones page immediately). Reuses this one unattended job.
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                            "..", "tools", "flag"))
            import flag as _flagmod
            _flagmod.flush_digest()
        except Exception as e:
            log(f"FLAG-DIGEST-FAIL (fail-open): {e}")

        roster, dups, det_alerted = check_duplicates(wstate)
        log(f"sweep: {len(roster)} live ids, {len(dups)} collisions")

        cur = joint_len()
        moved = cur != wstate.get("joint_cursor", 0)
        # Also run judgment if any TEAM board grew - cheap heuristic: run when joint
        # moved OR at most once per run regardless; here gate on joint movement to
        # keep Opus cost near zero on a quiet board.
        if moved:
            snapshot, n = recent_board_snapshot()
            verdict = ask_opus(snapshot, roster)
            if verdict and verdict.get("issue"):
                sev = verdict.get("severity", "low")
                summ = verdict.get("summary", "(no summary)")
                ikey = (verdict.get("key") or summ[:40]).strip().lower()
                # DEDUP KEY IS THE FINGERPRINT, NOT THE LLM SLUG (2026-07-15 X8A).
                # The LLM re-worded its own slug every run for the SAME real event
                # (8 slugs in 70 min for the Kenefick-BAM alarm, 2026-07-13), which
                # defeated the 30-min repost gate and 60-min alert cooldown. Prior
                # attempts to "fix" this stayed on the LLM slug and added a coarse
                # per-board daily cap as a backstop; the cap alone still lets the
                # same event re-fire many times before it kicks in. The fingerprint
                # is derived from the SUMMARY tokens (session ids, file names,
                # machine names) so the same real event fingerprints identically
                # across LLM rewordings. Fall back to `ikey` if the fingerprint
                # is empty (short summaries). ikey stays in the log for tracing.
                fkey = _fingerprint(summ) or ikey
                log(f"OPUS issue ({sev}) [{ikey}] fp[{fkey}]: {summ}")
                # NUMBERING WATCHER NEVER PAGES MAX (Max, 2026-06-09 split). A
                # high-severity, genuinely NEW coordination problem the
                # deterministic pass didn't already nudge -> post to the TEAM's
                # joint board so the team fixes it. Same issue within the hour
                # -> log only. Max's phone is the SAFETY watcher's job, not this.
                # Anti-spam gate on the JOINT board too (bcast.should_repost).
                if sev == "high" and not det_alerted and _opus_alert_is_new(wstate, fkey, time.time()) \
                        and bcast.should_repost("joint", fkey, time.time()):
                    try:
                        bcast._append_rec(bcast.JOINT_BOARD, "watcher",
                                          f"coordination risk (watcher): {summ}")
                        log(f"OPUS board-nudge sent [{ikey}] fp[{fkey}]")
                    except Exception as e:
                        log(f"NUDGE-FAIL: {e}")
                elif sev == "high":
                    log(f"OPUS alert gated (repeat/backoff/cap) [{ikey}] fp[{fkey}]")
            else:
                log("OPUS: clear")
            wstate["joint_cursor"] = cur
        else:
            log("board quiet since last run - skipped Opus pass")

        # --- MISROUTE pass: a joint thread that is really single-team -> SUGGEST it
        # move. Suggestive + trusting (the session decides), but PERSISTENT: re-nudge
        # every cooldown while DeepSeek still sees it, and clear the instant it stops
        # (Max 2026-06-26 "not aggressive but suggestive... trust its decisions, keep
        # bugging until the problem is fully resolved"). Run when joint moved OR while
        # a misroute is still pending (so it keeps bugging even on an otherwise quiet
        # board), but not forever on a clean board.
        pending = dict(wstate.get("pending_misroutes", {}))
        if moved or pending:
            snap2, _ = recent_board_snapshot()
            mv = ask_misroute(snap2)
            now = time.time()
            still = {}
            if mv and mv.get("misroute"):
                team = (mv.get("team") or "?").strip().lower()
                summ = mv.get("summary", "(no summary)")
                # Cooldown key is DETERMINISTIC (the team letter), NEVER DeepSeek's
                # free-text slug: the LLM phrases its key slightly differently each run
                # (e.g. ..._ownership vs ...-ownership), which would defeat the cooldown
                # and re-nudge every sweep - the exact "dedup keyed on LLM prose" trap.
                # One misrouted joint thread per team at a time is the right unit.
                mkey = f"misroute-{team}"
                # Anti-spam gate (bcast.should_repost): per-key backoff + give-up
                # cap + per-board daily backstop. The old flat 20-min cooldown let
                # the pollution nudge re-fire indefinitely while DeepSeek kept
                # seeing the same joint thread - part of the board spam Max flagged
                # 2026-07-13. After a few move-orders the watcher lets it rest.
                if bcast.should_repost(team, mkey, now):
                    try:
                        # Post the order to the OFFENDING TEAM'S OWN board, NOT joint -
                        # the anti-pollution watcher must not itself add to the joint
                        # clutter it is policing (that made it a top polluter). The
                        # team hears it on its board + gets force-woken below.
                        team_board = os.path.join(bcast.BASE, f"bulletin_{team}.jsonl")
                        order = (
                            f"POLLUTION - team '{team}' has single-team traffic on the "
                            f"GLOBAL/joint board: {summ}. This HARMS everyone, so move it "
                            f"to your own '{team}' board now. WHY IT MATTERS: (1) it "
                            f"DISTRACTS every other team - they are force-fed your "
                            f"internal chatter in their auto-loaded context, which blocks "
                            f"THEIR communication too; (2) it POLLUTES the one global "
                            f"channel, so genuinely cross-team messages get buried and "
                            f"important announcements stop coming through. The joint board "
                            f"only works if it stays cross-team only. HOW: use plain "
                            f"'bcast.py post' (no --joint/--all) - every '{team}' teammate "
                            f"STILL auto-hears it on the team board; reserve --all/--joint "
                            f"and @other-team mentions for genuinely global questions. I "
                            f"keep flagging + force-waking team '{team}' until it moves.")
                        bcast._append_rec(team_board, "Pollution-Watcher", order)
                        n_woke = _wake_team(team, order)
                        still[mkey] = now
                        log(f"POLLUTION order+wake -> team {team} board (woke {n_woke}) [{mkey}]")
                    except Exception as e:
                        still[mkey] = now
                        log(f"MISROUTE-NUDGE-FAIL: {e}")
                else:
                    # still pending (DeepSeek still sees it) but the gate is holding
                    # off the re-post - keep it marked so the pass keeps checking.
                    still[mkey] = pending.get(mkey, now)
                    log(f"MISROUTE pending, gated (backoff/cap) [{mkey}]")
            elif pending:
                log("MISROUTE: cleared")
            wstate["pending_misroutes"] = still

        _save_watch_state(wstate)
    except Exception:
        log("WATCHER-CRASH (fail-open):\n" + traceback.format_exc())


if __name__ == "__main__":
    main()
