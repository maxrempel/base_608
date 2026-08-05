# Adviser note - milestone 10 (~151K tokens)
# session: 20260609_zen_goldberg_e98cad_3e21795c
# written: 2026-06-09 12:54:35 by claude-opus-4-8

TO MAX:
You're on the right track stopping Wan i2v - 10 hours says it can't move an object without redrawing it. But notice the Assistant keeps proposing a different "winning" approach every turn (Kling, then compositing, then keyframes, then pod-on-black) and firing fast each time. Each idea is on its own branch, which is good housekeeping, but you're spreading effort thin. Pick one to actually prove end-to-end before the next pivot. The pod-on-black-then-overlay is genuinely the most promising lever - let it run to a real keyed-and-composited result, not just a raw clip.

TO ASSISTANT:
Stop reframing the strategy every turn - you flip-flopped on whether the input was good (Max and the adviser corrected you, you reversed twice mid-sentence). Lock the current branch and finish it: clip 2745 just completed, so do the luma-key AND the overlay onto a real background and SHOW Max the composited result. That is the only test that matters; a raw pod-on-black clip proves nothing on its own. Two more things: rembg luma-key on a soft/anti-aliased pod edge against black will fringe - check the key quality before declaring victory. And watch context - you're near compaction at ~151K; you've logged status well, keep clips lean and don't re-read large PNGs unless needed.
