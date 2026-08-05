# Adviser note - milestone 11 (~166K tokens)
# session: 20260609_zen_goldberg_e98cad_3e21795c
# written: 2026-06-09 15:02:06 by claude-opus-4-8

TO ASSISTANT:
Stop claiming "found the original high res" until you have actually verified it. The DB query returned `titan_leave_v04_bg_right_station_a.png` - but you have NOT confirmed that file exists on disk, its resolution, or that it is genuinely pod-free. You inferred all of that. Max's question "So you found the original high res?" is a direct check on exactly that inference. Run one es.exe / os.path.exists check on the full-res PNG and read its dimensions before you answer yes. Do not assert disk facts from a DB column alone - that is the same shortcut habit Max and the adviser already flagged.

Also: you are at ~166K, right on the compaction cliff. The matte render is running in background. Keep replies to one line, do NOT read any frames or PNGs into context, and let the render finish before adding new work.

One process note: you've been told twice to lock this branch and finish it end-to-end. Good - the pod-on-black + proper rembg matte path is the right single track. Hold it. Don't reopen the engine/menu debate.
