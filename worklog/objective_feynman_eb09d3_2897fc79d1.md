
## [2026-07-04 15:22] ? 05b2458f
- DID: Fixed sc11 merged audio via documented Protocol: built 18 missing merge_<sphash>.mp3 (concat existing per-line voices, no TTS) in lines_20260704_152108_sc11merges/; all 19 sc11 merges resolve via audio_resolver Tier-0
- STATE: Root cause: d53 registered merges but never ran propagation; merge_ops.upsert_by_hash falsely stamps sass_built at registration (merge_ops.py:132) - reported, not fixed
- NEXT: Remaining: libup collapse + Notion [[MERGE]] wrap for sc11; possible merge_ops stamp fix (coordinate with D-team)

## [2026-07-26 13:57] ? b5f68f00
- DID: Tape 1Select: fired+approved 15 Anna night-kitchen table frames (jobs 3381-3402); redo v2 angles 3397-3402 beat the imager's gaze/squish/big-table defects, 5 of 6 approved (v2_room 3401 junked - unpredictable gaze).
- STATE: 15 approved image frames in scene 'Tape 1Select', all via fire_job/2048x1152. No slideshow assembled, no audio yet.
- NEXT: New session does the AUDIO (sass TTS per-line) for Tape 1.
