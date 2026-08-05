import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import watcher

# Synthetic: a JOINT thread that is ENTIRELY c-team (c12<->c15, no other team) -> should flag.
synthetic = "\n".join([
    "[joint] c12: c15 can you take the arrangement_picker refactor while I do the loader?",
    "[joint] c15: c12 sure, I'll own arrangement_picker.js, you take loader.js. push when done.",
    "[joint] c12: c15 done with loader, pushed. your turn.",
    "[joint] d3: d7 unrelated d-team note here",
])
print("POSITIVE (single-team c thread on joint):")
print("  VERDICT:", watcher.ask_misroute(synthetic))
