
## [2026-06-09 14:18] ? ????????
- DID: 3-line merge 448be6 done (job 2742). Max manually junked the old standalone per-line lipsies; sb auto-hides junked.
- STATE: STANDBY. Max wants merge step to AUTO-JUNK superseded per-line lipsies (those whose birth_line_hash = a merged member line_hash) so they drop off sb automatically. Right home = libup fold step.
- NEXT: On wake: add auto-junk-on-merge to libup _build_merge_stmts (junk lipsie jobs whose birth_line_hash matches any member line_hash when folding a merge slot). Coordinate with D4 (merge coordinator). Also still pending: fire_merge_lipsie NULL-lipsync_tool race fix.

## [2026-06-09 14:22] ? ????????
- DID: WIN: pod-on-black branch proven end-to-end. 2745 = Wan animated our real pod on pure black (shape HELD, Max confirmed good). Then ffmpeg lumakey(threshold=0.05:tolerance=0.07:softness=0.10) keyed black out + overlaid on Titan plate -> clean composite, no fringe, shape intact. Registered as done clip row for GUI view. Files in output_clips/: sc09_sc09_broll_podblack_20260609_v01_wan26.mp4 (pod/black) + sc09_broll_podcomposite_v01.mp4 (final). pod_on_black src in ships/space/broll_work/.
- STATE: Composite proof done + presented. Awaiting Max judgment on motion (pod drifts/scales).
- NEXT: If good: build factory - reverse clip for arrival direction, swap bg plates (Titan vs Earth station), tune motion prompt. Reuse: rembg cut 873 -> pod_on_black -> wan26 i2v -> ffmpeg lumakey overlay.
