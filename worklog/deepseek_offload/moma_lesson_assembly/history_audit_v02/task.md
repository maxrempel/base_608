# MOMA Lesson 1 failure-history synthesis

Last edited: 2026-08-01 by Codex (GPT-5.6 SOL)

## Objective

Turn the evidence below into a compact audit for a reusable video-assembly skill. Do not inspect the filesystem. Produce `result.md` only.

## Proven master

- v123 is human-approved after checks at beginning, middle, and end.
- 981.153255 seconds, 29,368 frames, 1280x720.
- Video stream is copied unchanged; elementary-stream MD5 is `c237405d06c5f645061afaf0398d6afb`.
- Mixed AAC track is default. A second original AAC voice-reference track is stream-copied with a 3.5-second container offset.
- The mixed voice is made directly from the original MP4 with `aresample=44100:async=1000:first_pts=0`, then `adelay=3500:all=1`. No intermediate WAV and no `asetpts=N/SR/TB`.
- Mixed versus reference voice measured zero lag at 10, 88, 300, 600, 900, 922, 943.5, and 963.5 film seconds. Packet timestamps are monotonic.

## Source timing fact

- Original voice AAC: 41,890 AAC frames, 1,024 samples each at 44.1 kHz, or 972.683900 seconds of encoded-sample time.
- MP4 presentation duration: 970.781156 seconds.
- Difference: 1.902744 seconds, carried by MP4 edit-list/skip-sample timing.

## Failure chain

- v10: synchronized in a good player; Chrome developed delay. Browser playback was confused with file sync.
- v12: slide was 1920x1080 while body was 1280x720; concat copied incompatible dimensions and container advertised wrong geometry.
- v13/v15: slide/body sync could work, but v15 used the wrong closing music. This was a content failure, not sync failure.
- Early v116: applied 168,000 delay samples before resampling a 44.1 kHz voice, producing 3.8095 seconds instead of 3.5. A corrected file reused the same version number, creating ambiguity.
- v117/v118/v119: automation reported alignment against references created by the same flattened-decode method. Human listening found drift. Correlated wrong against wrong.
- v121: fed a voice stream whose first timestamp was 3.5 seconds into `amix`; output audio began near 3.476 seconds, so players effectively lost the opening music and voice appeared at the start.
- v122: decoded source AAC to continuous PCM WAV, prefixed exactly 154,350 silent samples, proved PCM byte identity, mixed, then regenerated timestamps with `asetpts=N/SR/TB`. This erased the MP4 presentation timeline and produced large cumulative lip drift. Its QC falsely passed because both comparison lanes used the same flattened decode.
- v123 fixed the root cause using direct MP4 input, timestamp-aware asynchronous resampling, post-reconciliation title delay, a copied voice reference track, and multi-point plus human QC.

## Process failures

- Rejected candidates were copied into the normal output folder before QC, so Max opened them as if deliverable.
- A version number was reused for multiple attempts.
- Automation checked frame count and internally consistent audio but not presentation-timestamp fidelity against an independent reference.
- QC sampled too few places and initially omitted late-film checks.
- Assistants said “rendering video” even when using video stream copy, obscuring what changed.
- Upload/delivery began before human approval in the intended player.
- Music transitions and endings were not always checked against exact scene cuts and the actual last audible note.

## Required synthesis

Write:

1. A chronology.
2. A bug matrix with symptom, root cause, why QC missed it, and permanent guard.
3. The proven architecture.
4. Mandatory fail-closed gates, including source fingerprint, timestamp audit, candidate-only work area, video packet identity, exact frames/geometry, two audio tracks, zero-lag checks throughout, no voice before the title, monotonic timestamps, music transition/tail checks, intended-player human review, and promotion only after approval.
5. Defects in the obsolete v01 advice: its one-pass loudnorm command rewrote the voice, trailing loudnorm could truncate the tail, `-shortest` was unsafe, it lacked edit-list checks, it recommended separately scoring slide sections, and it treated re-encoding video as the cause of desync rather than distinguishing forbidden video mutation from the actual AAC timestamp bug.

Use exact technical nouns and avoid generic filler.
