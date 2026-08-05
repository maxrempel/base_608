# Adviser note - milestone 9 (~142K tokens)
# session: 20260609_zen_goldberg_e98cad_3e21795c
# written: 2026-06-09 12:52:10 by claude-opus-4-8

TO MAX:
You now have several branches open for one b-roll problem (closeup-still path in another session, transparent-pod-overlay here, plus the abandoned Kling/compositing menus). That's fine as exploration, but nothing is being archived or tracked. Decide which one branch is the real bet so these don't rot into a mess you can't reconcile later.

TO ASSISTANT:
Max picked first+last-frame keyframe interpolation, then immediately pivoted to "pod on black/transparent background in Wan, then overlay." That's the live task now - the keyframe idea is parked. Do NOT re-open the option menu again; you've offered the same 3-option list twice. Just do the transparent/black-bg pod-in-Wan test he asked for.

Two cautions before you fire:
- You're at ~142K tokens, compaction near ~169K. Stop reading large PNGs into context (you already inhaled two full images). Log a tight milestone now so the chosen approach survives compaction.
- Wan on a black/transparent bg still risks redrawing the pod - the same failure mode that cost 10 hours. Render ONE short test, show it, judge. Do not batch.
