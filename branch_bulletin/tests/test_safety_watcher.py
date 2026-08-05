"""Isolated tests for the bcast SAFETY watcher.

Runs against a throwaway BCAST_BASE + temp worklog dir - NEVER touches the live
board or worklogs. DeepSeek and Telegram are monkeypatched so the test makes no
real API call and pages nobody. Asserts: a quiet team triggers no judgment; an
issue with a worker_message lands on the TEAM board and does NOT page Max; a
needs_max verdict pages Max once and is deduped by a deterministic issue key;
the daily cost cap skips judgment; context is bounded locally without a paid
compaction call; and an unchanged Git tree has a stable fingerprint.
"""
import os, sys, json, time, tempfile, importlib, inspect

TMP = tempfile.mkdtemp(prefix="safety_test_")
WL = tempfile.mkdtemp(prefix="safety_worklog_")
os.environ["BCAST_BASE"] = TMP
sys.path.insert(0, r"C:\claude_base\branch_bulletin")
import bcast
importlib.reload(bcast)
import safety_watcher as sw
importlib.reload(sw)

sw.WORKLOG_DIR = WL
deepseek_chat_source = inspect.getsource(sw.deepseek_chat)

fails = []
def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)

# ---- capture side effects instead of performing them ----
sent = []
sw.telegram_alert = lambda text: sent.append(text)

chat_calls = []          # list of ("judge"|"compact", max_tokens)
VERDICT = {"issue": False}
def fake_chat(messages, max_tokens):
    content = messages[0]["content"]
    usage = {"prompt_tokens": 100, "completion_tokens": 50}
    if "Reply ONLY compact JSON" in content:
        chat_calls.append(("judge", max_tokens))
        return json.dumps(VERDICT), usage
    chat_calls.append(("compact", max_tokens))
    return "COMPACTED HISTORY", usage
sw.deepseek_chat = fake_chat

os.makedirs(bcast.STATE_DIR, exist_ok=True)

def make_state(key, bid, age_sec=60):
    p = os.path.join(bcast.STATE_DIR, key + ".json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump({"id": bid, "cursor": 0}, f)
    t = time.time() - age_sec
    os.utime(p, (t, t))

def write_worklog(key, text):
    with open(os.path.join(WL, key + ".md"), "w", encoding="utf-8") as f:
        f.write(text)

def team_board_lines(team):
    return bcast._parse(bcast._read_lines(bcast._team_board(team)))

def allow_judge(team="c"):
    d = sw._load_digest(team)
    d["last_judge"] = 0
    sw._save_digest(team, d)

# one live c-team session
make_state("sess_c1", "c1", 60)

# ---- 1: quiet team -> no judgment, no alert ----
chat_calls.clear()
g = {"cost": {"date": time.strftime("%Y-%m-%d"), "usd": 0.0}}
sw.run_team("c", [{"id": "c1", "key": "sess_c1", "age": 60}], g)
check("quiet team makes no DeepSeek call", chat_calls == [])
check("quiet team sends no telegram", sent == [])

# ---- 2: benign activity is free; concrete danger is judged ----
chat_calls.clear(); sent.clear()
write_worklog("sess_c1", "started editing app.js on a fresh branch")
sw.run_team("c", [{"id": "c1", "key": "sess_c1", "age": 60}], g)
check("ordinary activity makes no DeepSeek call", chat_calls == [])

chat_calls.clear(); sent.clear()
VERDICT = {"issue": True, "damage": "medium", "probability": "low",
           "worker_message": "two sessions editing app.js - coordinate",
           "needs_max": False, "key": "appjs-race", "summary": "appjs race"}
write_worklog("sess_c1", "started editing app.js on a fresh branch\nabout to overwrite app.js from a stale baseline")
g = {"cost": {"date": time.strftime("%Y-%m-%d"), "usd": 0.0}}
allow_judge()
sw.run_team("c", [{"id": "c1", "key": "sess_c1", "age": 60}], g)
check("concrete safety signal triggers one judgment",
      len([c for c in chat_calls if c[0] == "judge"]) == 1)
lines = team_board_lines("c")
check("worker_message posted to TEAM board",
      any(r.get("from") == "safety" and "app.js" in r.get("msg", "") for r in lines))
check("fixable issue does NOT page Max", sent == [])

# ---- 3: needs_max -> page once, dedupe within cooldown ----
chat_calls.clear(); sent.clear()
VERDICT = {"issue": True, "damage": "severe", "probability": "high",
           "worker_message": "", "needs_max": True,
           "plain": "A worker is about to wipe your song database.",
           "key": "db-wipe", "summary": "mass delete"}
write_worklog("sess_c1", "running DROP DATABASE kartoteka now")
g = {"cost": {"date": time.strftime("%Y-%m-%d"), "usd": 0.0}}
allow_judge()
sw.run_team("c", [{"id": "c1", "key": "sess_c1", "age": 60}], g)
check("needs_max pages Max once", len(sent) == 1)
check("ping carries the plain text", sent and "song database" in sent[0])
check("ping carries damage + probability", sent and "severe" in sent[0] and "high" in sent[0])

# same key again within cooldown -> NOT re-paged
write_worklog("sess_c1", "running DROP DATABASE kartoteka now\nstill going")
sw.run_team("c", [{"id": "c1", "key": "sess_c1", "age": 60}], g)
check("same issue-key is not re-paged within cooldown", len(sent) == 1)

# ---- 4: daily cost cap skips judgment ----
chat_calls.clear()
write_worklog("sess_c1", "running DROP DATABASE kartoteka now\nstill going\nmore")
g = {"cost": {"date": time.strftime("%Y-%m-%d"), "usd": sw.DAILY_USD_CAP + 1}}
sw.run_team("c", [{"id": "c1", "key": "sess_c1", "age": 60}], g)
check("over cap -> no judgment call", [c for c in chat_calls if c[0] == "judge"] == [])

# ---- 5: PRESENT compacts locally and keeps only risk-bearing overflow ----
chat_calls.clear()
old_budget = sw.PRESENT_BUDGET_TOKENS
sw.PRESENT_BUDGET_TOKENS = 5    # ~20 chars: any real activity overflows it
d = {"present": ["old harmless event", "about to delete database backup",
                   "fresh harmless activity"], "past": ""}
sw._compact_digest_free(d)
sw.PRESENT_BUDGET_TOKENS = old_budget
check("local compaction makes no DeepSeek call", chat_calls == [])
check("risk-bearing overflow is retained in PAST", "delete database" in d.get("past", ""))
check("PRESENT stays within its configured budget", sw._est_tokens("\n".join(d["present"])) <= 6)

# ---- 6: dead-man re-page - a SEVERE unacked live page re-fires after ~15 min ----
chat_calls.clear(); sent.clear()
d = sw._load_digest("c")
d["alerts"] = {}          # fresh alert state
d["board_last"] = {}
sw._save_digest("c", d)
VERDICT = {"issue": True, "damage": "severe", "probability": "high",
           "worker_message": "", "needs_max": True,
           "plain": "Your database is being wiped right now.",
           "key": "live-wipe", "summary": "live wipe"}
write_worklog("sess_c1", "DROP DATABASE kartoteka -- executing")
g = {"cost": {"date": time.strftime("%Y-%m-%d"), "usd": 0.0}}
allow_judge()
sw.run_team("c", [{"id": "c1", "key": "sess_c1", "age": 60}], g)
check("severe page fires first time", len(sent) == 1)
# backdate last-page 16 min and re-run with the SAME live danger -> must re-page
d = sw._load_digest("c")
alert_key = next(iter(d["alerts"]))
d["alerts"][alert_key]["last"] -= 16 * 60
sw._save_digest("c", d)
# No new evidence and no paid re-judgment: dead-man state alone re-pages.
sw.run_team("c", [{"id": "c1", "key": "sess_c1", "age": 60}], g)
check("severe unacked page RE-FIRES after 15 min (dead-man)", len(sent) == 2)
check("dead-man re-page makes no additional judge call",
      len([c for c in chat_calls if c[0] == "judge"]) == 1)

# ---- 7: auto-clear - danger resolves -> alert dropped, escalation stops ----
chat_calls.clear(); sent.clear()
VERDICT = {"issue": False}      # next pass sees the danger gone
write_worklog("sess_c1", "DROP DATABASE kartoteka -- executing\nstill running\nstopped, restored")
sw.run_team("c", [{"id": "c1", "key": "sess_c1", "age": 60}], g)
d = sw._load_digest("c")
check("resolved danger auto-clears its alert", not d.get("alerts"))
check("auto-clear sends no page", sent == [])

# ---- 8: board-post cooldown - same worker_message not re-posted within 30 min ----
chat_calls.clear()
d = sw._load_digest("c"); d["board_last"] = {}; sw._save_digest("c", d)
VERDICT = {"issue": True, "damage": "minor", "probability": "low",
           "worker_message": "coordinate before deleting the temp files", "needs_max": False,
           "plain": "", "key": "tidy", "summary": "tidy"}
before = len(team_board_lines("c"))
allow_judge()
write_worklog("sess_c1", "about to delete 50 temp files")
sw.run_team("c", [{"id": "c1", "key": "sess_c1", "age": 60}], g)
write_worklog("sess_c1", "about to delete 50 temp files\nand delete 50 more")
sw.run_team("c", [{"id": "c1", "key": "sess_c1", "age": 60}], g)
after = len(team_board_lines("c"))
check("same worker_message posts once, not twice, within board cooldown", after - before == 1)

# ---- 9: git eye - a working-tree change alone (no worklog) triggers judgment ----
import subprocess
chat_calls.clear(); sent.clear()
GREPO = tempfile.mkdtemp(prefix="safety_gitrepo_")
def _g(*a):
    subprocess.run(["git", "-C", GREPO, *a], capture_output=True, text=True)
_g("init"); _g("config", "user.email", "t@t"); _g("config", "user.name", "t")
with open(os.path.join(GREPO, "data.txt"), "w") as f:
    f.write("important\n")
_g("add", "-A"); _g("commit", "-m", "seed")
# Stable across calls and processes: no randomized built-in hash.
first_text, first_fp = sw._read_git_new(GREPO, "")
second_text, second_fp = sw._read_git_new(GREPO, first_fp)
check("unchanged Git status has a stable fingerprint",
      first_fp == second_fp and second_text == "")
# now DELETE the tracked file in the working tree (a danger signal)
os.remove(os.path.join(GREPO, "data.txt"))
# fresh digest so cursors/fingerprints start clean
d = sw._load_digest("c")
d["worklog_cursors"] = {}; d["git_fps"] = {}; d["present"] = []
sw._save_digest("c", d)
VERDICT = {"issue": False}
# NOTE: no worklog change this run - movement must come from git alone
write_worklog("sess_c1", "")
g = {"cost": {"date": time.strftime("%Y-%m-%d"), "usd": 0.0}}
allow_judge()
sw.run_team("c", [{"id": "c1", "key": "sess_c1", "age": 60, "cwd": GREPO}], g)
check("git working-tree change alone triggers a judgment",
      any(c[0] == "judge" for c in chat_calls))
d = sw._load_digest("c")
present_txt = "\n".join(d.get("present", []))
check("git deletion surfaces in PRESENT", "DELETION" in present_txt)
check("git deletion evidence has a machine-readable recovery audit",
      "GIT-DELETE-AUDIT head_recoverable=1 not_in_head=0" in present_txt)

# The paid judge may contradict the Git audit. The deterministic post-judgment
# guard suppresses only a Git-loss page, never a mixed destructive operation.
git_page = {"plain": "These archive files will be gone forever if committed",
            "summary": "unrecoverable Git working-tree deletion",
            "worker_message": "", "key": "delete-git"}
audit = "GIT-DELETE-AUDIT head_recoverable=498 not_in_head=0"
check("recoverable-only Git loss page is suppressed",
      sw._recoverable_git_only_page(git_page, audit))
check("one deletion absent from HEAD keeps the page",
      not sw._recoverable_git_only_page(
          git_page, "GIT-DELETE-AUDIT head_recoverable=497 not_in_head=1"))
force_page = dict(git_page)
force_page["summary"] = "force-push will rewrite Git history"
check("force-push danger is never suppressed",
      not sw._recoverable_git_only_page(force_page, audit))
database_page = dict(git_page)
database_page["summary"] = "database overwrite plus Git deletion"
check("database overwrite danger is never suppressed",
      not sw._recoverable_git_only_page(database_page, audit))

# ---- 10: pause-negotiate - a dangerous-but-stoppable op gets an ADDRESSED,
#          override-able PAUSE on the team board, and does NOT page Max ----
chat_calls.clear(); sent.clear()
d = sw._load_digest("p"); d["board_last"] = {}; sw._save_digest("p", d)
VERDICT = {"issue": True, "damage": "serious", "probability": "med",
           "worker_message": "you appear about to overwrite the live data.json",
           "pause": True, "target": "p1", "needs_max": False,
           "plain": "", "key": "live-overwrite", "summary": "stoppable overwrite"}
write_worklog("sess_c1", "about to overwrite live data.json with my local copy")
g = {"cost": {"date": time.strftime("%Y-%m-%d"), "usd": 0.0}}
allow_judge("p")
sw.run_team("p", [{"id": "p1", "key": "sess_c1", "age": 60}], g)
pl = [r for r in team_board_lines("p") if r.get("from") == "safety"
      and "PAUSE" in r.get("msg", "") and "override" in r.get("msg", "")]
check("pause posts an addressed override-able PAUSE to the team board",
      any("p1" in r.get("msg", "") for r in pl))
check("pause does NOT page Max", sent == [])

# ---- 11: model and dedupe controls are explicit and stable ----
check("watcher uses explicit V4 Flash", sw.MODEL == "deepseek-v4-flash")
check("V4 Flash hidden thinking is explicitly disabled",
      '"thinking"' in deepseek_chat_source and '"disabled"' in deepseek_chat_source)
check("issue key ignores changing counts and model wording",
      sw._stable_issue_key("c", "delete 50 database rows") ==
      sw._stable_issue_key("c", "deleted 900 database rows with different wording"))

print("\n" + ("ALL PASS" if not fails else f"FAILURES: {fails}"))
sys.exit(1 if fails else 0)
