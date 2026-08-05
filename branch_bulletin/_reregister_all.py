"""One-time op (2026-06-08 cutover): manually re-register every existing session
onto the new split-per-team boards, so no worker has to run whoami itself.

For each state file in state/: keep its id, and set per-board cursors to the
current end of its team board + the joint board (= 'start fresh from now', the
same effect whoami would have). Idempotent + fail-open per file.
"""
import os, json, glob, sys
sys.path.insert(0, r"C:\claude_base\branch_bulletin")
import bcast

if not bcast._split_on():
    print("ABORT: split flag is OFF - run migrate CONFIRM first.")
    sys.exit(1)

done, skipped = [], []
for p in glob.glob(os.path.join(bcast.STATE_DIR, "*.json")):
    try:
        with open(p, "r", encoding="utf-8") as f:
            st = json.load(f)
    except Exception as e:
        skipped.append((os.path.basename(p), f"unreadable: {e}"))
        continue
    bid = st.get("id")
    if not bid:
        skipped.append((os.path.basename(p), "no id (unnamed session)"))
        continue
    team_board = bcast._board_for(bid)
    st["cursors"] = {
        "team": len(bcast._read_lines(team_board)),
        "joint": len(bcast._read_lines(bcast.JOINT_BOARD)),
    }
    try:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(st, f)
        done.append((bid, bcast._team_of(bid)))
    except Exception as e:
        skipped.append((os.path.basename(p), f"write fail: {e}"))

print("RE-REGISTERED onto split boards:")
for bid, team in sorted(done):
    print(f"  {bid:>8}  -> team '{team}' board + joint")
if skipped:
    print("SKIPPED:")
    for name, why in skipped:
        print(f"  {name}: {why}")
print(f"\n{len(done)} sessions re-registered, {len(skipped)} skipped.")
