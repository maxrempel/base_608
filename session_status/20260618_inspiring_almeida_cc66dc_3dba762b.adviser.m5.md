# Adviser note - milestone 5 (~408K tokens)
# session: 20260618_inspiring_almeida_cc66dc_3dba762b
# written: 2026-06-18 06:34:04 by deepseek-v4-pro

TO MAX: The handover table is built on blind mechanical matching. The Assistant never once read an actual transcript segment - it delegated everything to scripts and subagents. The song titles are ~half wrong because a dumb matcher grabbed famous songs off announced names, not what was actually sung. Your core rule (first sung line only, no titles, smart LLM must read the data) was lost across sessions. The method itself is the disaster - fix that before shipping any more tables.

TO ASSISTANT: You worked blind the entire session. The handover was produced by mechanical char-ngram matching + cheap metadata - at no point did Opus (or any smart LLM) actually read a single segment transcript to identify what was sung. You then burned ~200 turns on autonomous-loop busywork that added zero intelligence. The principle is first-sung-line only, verified by a smart reader, spot-checked by you personally. Write that rule into the handover doc's first section so the next session can't miss it. For B29: before building any new handover, read 3-5 segment transcripts yourself first to understand the data. Then design a method where Opus reads, not scripts.
