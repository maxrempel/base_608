
## [2026-06-22 15:51] ? 0085b386
- DID: Fixed starseeds insert line A: clip had 2 attempts (incomplete + complete last take) with a real pause between; Deepgram garbled it and word-index cut doubled 'About eighty years ago'. Recut A by MEASURED audio times (silencedetect) keeping only the complete last take 39.74-43.90s on src1. Also changed assemble.py to cut each scripted line RAW (no gap-deletion inside a take).
- STATE: v06 rendered (43MB) at C:/Users/maxre/Videos/starseeds_pitch_20260622_cleanup/starseeds_pitch_cleaned_v06.mp4; v05 preserved. Awaiting Max's listen-check on line A.
- NEXT: If A good: archive v01-v05, finalize. Lesson: never trust ASR word-timestamps to cut audio inside a take; measure with silencedetect.
- LESSON: ASR (Deepgram) silently drops low-confidence words AND can mislabel which of two adjacent takes is the real one; for cutting, verify the actual audio with ffmpeg silencedetect rather than trusting per-word timestamps.

## [2026-06-22 17:02] ? 0085b386
- DID: Starseeds pitch fully done (v10 approved): retakes cut, line A spliced via measured silencedetect cut, two-layer ASS subtitles (crisp white + blurred shade, Calibri 112, bottom). Updated method docs + global2 story.
- STATE: v10 = final approved video at C:/Users/maxre/Videos/starseeds_pitch_20260622_cleanup/starseeds_pitch_cleaned_v10.mp4. Method+troubleshooting docs committed+pushed to claude_base master. global2 got 'Starseeds subtitles' parable.
- NEXT: Optional: archive v01-v09 + qc frames into archive/ subfolder.
