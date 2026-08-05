# Adviser note - milestone 11 (~166K tokens)
# session: 20260608_dmiring_sanderson_f37aff_1e4b4f69
# written: 2026-06-08 15:27:24 by claude-opus-4-8

TO ASSISTANT:
New task is clear and unrelated to past phases: in the 2nd spine, clicking a lipsie opens a still image instead of the lipsie video in the popup. Stop everything else. Do NOT re-litigate mixboard/trim/redo - those are resolved or parked.

Before touching code: observe live with Playwright (your strongest tool here) - open a 2nd-spine lipsie popup, inspect what MomaPopup.open receives for that job (jobId, audioUrl, the media URL it builds), and confirm whether the popup is being handed an image src vs a video src. The likely fault is upstream: the 2nd spine passes a still/source path where a lipsie video URL is expected. Find where the 2nd spine builds its popup-open call and compare to the working 1st spine path. Fix at that source, not by branching popup.js.

Watch your token budget - you are at ~166K and compaction wipes near ~169K. Write a status snapshot NOW with the new task framed, before you start digging, or you risk losing the thread mid-investigation again.

TO MAX:
Each compaction is costing you - the Assistant burns a chunk of every fresh context re-reading the same files. This is the 3rd distinct bug in one long session. Consider starting genuinely fresh sessions per bug rather than forking mid-context; you'll get sharper work and fewer "I can't reproduce" loops.
