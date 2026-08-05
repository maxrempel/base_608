import os, sys, json, tempfile, shutil

base = tempfile.mkdtemp(prefix="bcast_misroute_")
os.environ["BCAST_BASE"] = base
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bcast, watcher  # import AFTER env set so BASE picks up temp dir

os.makedirs(os.path.join(base, "state"), exist_ok=True)
os.makedirs(os.path.join(base, "shared"), exist_ok=True)

# Seed a JOINT board with a single-team (c) thread -> should be flagged + nudged.
for m in [
    "c12: c15 take arrangement_picker, I take loader",
    "c15: c12 ok I own arrangement_picker.js, push when done",
    "c12: c15 loader pushed, your turn",
]:
    who, msg = m.split(": ", 1)
    bcast._append_rec(bcast.JOINT_BOARD, who, msg)

def joint_lines():
    return bcast._read_lines(bcast.JOINT_BOARD)

before = len(joint_lines())
print("RUN 1 (expect a nudge appended + pending key stored)")
watcher.main()
after1 = joint_lines()
nudges = [l for l in after1 if '"watcher"' in l or '"id": "watcher"' in l or 'watcher' in l and 'suggestion' in l]
last = json.loads(after1[-1]) if after1 else {}
print("  joint grew:", len(after1) - before, "| last poster:", last.get("id"), "| msg head:", (last.get("msg","")[:70]))
st = json.load(open(os.path.join(base, "watcher_state.json")))
print("  pending_misroutes:", list(st.get("pending_misroutes", {}).keys()))

print("RUN 2 immediately (expect NO new nudge - within 20min cooldown)")
n_before = len(joint_lines())
watcher.main()
n_after = len(joint_lines())
print("  joint grew by:", n_after - n_before, "(should be 0)")

shutil.rmtree(base, ignore_errors=True)
print("DONE")
