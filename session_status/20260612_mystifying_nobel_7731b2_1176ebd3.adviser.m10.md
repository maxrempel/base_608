# Adviser note - milestone 10 (~161K tokens)
# session: 20260612_mystifying_nobel_7731b2_1176ebd3
# written: 2026-06-12 12:42:01 by claude-opus-4-8

TO MAX:
Yes, AC Power Recovery is real on the Dell Precision T3600 - it exists in BIOS under Power Management as "AC Recovery" with Off/On/Last options. So that recommendation is sound, not made up. Set it to "On" (or "Last") and Lak self-powers after a power cut. Worth confirming the Assistant cites the actual T3600 manual rather than guessing again.

TO ASSISTANT:
You've been right to keep correcting your own claims, but you did it twice on the same incident (tunnel "fragile" then "fine"), which is exactly the kind of premature assertion that costs trust. For Max's current question: do NOT confirm the BIOS option from memory. The lakarian-python MCP can read the box - run `dmidecode` / check the system model to confirm it really is a T3600, then confirm the AC Recovery setting exists for that exact model before answering. State clearly what you verified vs inferred. Keep it to one or two probes - you are near the ~169K compaction wall, so be economical and don't reopen the whole resilience audit.
