# Adviser note - milestone 10 (~152K tokens)
# session: 20260610_pensive_ishizaka_ca20b3_85962d0f
# written: 2026-06-10 15:51:32 by claude-opus-4-8

TO ASSISTANT:
Context is at ~152K and compaction wipes near ~169K. The export step (ffmpeg mixing video + clip-audio + music-with-curve) is the heaviest task yet and could easily blow past the limit mid-build. Before you start: log a crisp resume note (you have, but update it with "export in progress" and the exact ffmpeg approach), so a fresh session can pick up cleanly.

Two technical watch-items for export:
- The shark-tooth curve lives in the browser as break points. You must serialize that curve and pass it to ffmpeg as a volume automation (e.g. volume filter with timed expressions or a sidechain). Don't hand-wave this - confirm the curve actually bakes in, don't just render music at flat gain.
- The video already carries its own clip-soundtrack. The mix must preserve that at full volume AND layer music under the curve. Verify with an actual rendered sample, not a console check.

Also: earlier `git status` showed "unrelated junk" in the tree you scoped your commit around. That tree is messy - flag to Max if it grows, but don't sweep it yourself.

CLEAN otherwise - the pingpong confirms, the drop-zone fix, and the commit-before-next-step were all handled well.
