"""Isolated test for the bcast watcher's deterministic duplicate-live-id sweep.

Runs against a throwaway BCAST_BASE temp dir - NEVER touches the live board.
Telegram + Opus are monkeypatched so the test sends no real alert / API call.
Asserts: a duplicate LIVE id is detected, a nudge lands on the temp joint board,
the cooldown suppresses a second nudge, and a single-holder id is NOT flagged.
"""
import os, sys, json, time, tempfile, importlib

TMP = tempfile.mkdtemp(prefix="watcher_test_")
os.environ["BCAST_BASE"] = TMP
sys.path.insert(0, r"C:\claude_base\branch_bulletin")
import bcast
importlib.reload(bcast)
import watcher
importlib.reload(watcher)

fails = []
def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)

# capture alerts instead of sending
sent = []
watcher.telegram_alert = lambda text: sent.append(text)

os.makedirs(bcast.STATE_DIR, exist_ok=True)

def make_state(key, bid, age_sec):
    p = os.path.join(bcast.STATE_DIR, key + ".json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump({"id": bid, "cursor": 0}, f)
    t = time.time() - age_sec
    os.utime(p, (t, t))

# two LIVE b0 (collision) + one stale b0 (ignored) + one lone live c1
make_state("sess_a", "b0", 120)
make_state("sess_b", "b0", 200)
make_state("sess_c", "b0", 9999)
make_state("sess_d", "c1", 60)

wstate = {"joint_cursor": 0, "last_nudge": {}}
roster, dups, alerted = watcher.check_duplicates(wstate)

check("detects b0 as a live duplicate", "b0" in dups and len(dups["b0"]) == 2)
check("reports it alerted", alerted is True)
check("does NOT flag lone c1", "c1" not in dups)
check("telegram alerted once for b0", len(sent) == 1 and "b0" in sent[0])

joint = bcast._parse(bcast._read_lines(bcast.JOINT_BOARD))
check("nudge landed on joint board", any(r.get("from") == "watcher" and "b0" in r.get("msg", "") for r in joint))
check("cooldown timestamp recorded", "b0" in wstate["last_nudge"])

# second run within cooldown -> no new alert, no new nudge
sent.clear()
before = len(bcast._read_lines(bcast.JOINT_BOARD))
watcher.check_duplicates(wstate)
after = len(bcast._read_lines(bcast.JOINT_BOARD))
check("cooldown suppresses repeat alert", len(sent) == 0)
check("cooldown suppresses repeat nudge", after == before)

# ---------- OPUS-ALERT DEDUPE (only new problems re-ping) ----------
ws = {"last_opus_alert": {}}
now = time.time()
check("opus dedupe: first sight of an issue pings", watcher._opus_alert_is_new(ws, "b6-appjs-stale", now))
check("opus dedupe: same issue within cooldown is suppressed", not watcher._opus_alert_is_new(ws, "b6-appjs-stale", now + 60))
check("opus dedupe: a DIFFERENT issue still pings", watcher._opus_alert_is_new(ws, "c5-c0-double-manage", now + 60))
check("opus dedupe: same issue after cooldown re-pings",
      watcher._opus_alert_is_new(ws, "b6-appjs-stale", now + watcher.OPUS_ALERT_COOLDOWN_SEC + 1))

print("RESULT:", "ALL PASS" if not fails else f"{len(fails)} FAILED: {fails}")
sys.exit(1 if fails else 0)
