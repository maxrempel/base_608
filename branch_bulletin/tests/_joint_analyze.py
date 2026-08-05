import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bcast

recs = bcast._parse(bcast._read_lines(bcast.JOINT_BOARD))
total = len(recs)
single_team = collections.Counter()   # entries that name NO other team -> candidate to migrate
cross = 0
no_id = 0
watcher_posts = 0
for r in recs:
    rid = r.get("from", "") or r.get("id", "") or ""
    msg = r.get("msg", "") or ""
    if rid in ("watcher",):
        watcher_posts += 1
        continue
    team = bcast._team_of(rid)
    if team == "misc":
        no_id += 1
        continue
    others = bcast._names_other_team(rid, msg)
    if others:
        cross += 1
    else:
        single_team[team] += 1

print(f"TOTAL joint entries: {total}")
print(f"  cross-team (legit on joint): {cross}")
print(f"  watcher posts: {watcher_posts}")
print(f"  no-id/misc: {no_id}")
print(f"  SINGLE-TEAM (migration candidates): {sum(single_team.values())}")
print(f"    by team: {dict(single_team.most_common())}")
# how many distinct state files (cursors) would need fixing
sdir = os.path.join(bcast.BASE, "state")
nst = len([f for f in os.listdir(sdir) if f.endswith(".json")]) if os.path.isdir(sdir) else 0
print(f"STATE FILES (cursors to keep consistent): {nst}")
