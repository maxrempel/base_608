# Adviser note - milestone 7 (~106K tokens)
# session: 20260615_focused_wilbur_d92388_ba76facd
# written: 2026-06-15 11:03:48 by deepseek-v4-pro

TO ASSISTANT: Stop polling that test output - you've burned 5+ turns and the monitor just timed out. This is a death spiral. The 400?13,670 matching is too heavy for a single synchronous Bash call. Restructure: either (a) shrink the pilot to 50 windows against top-10 candidate songs by first-line similarity, or (b) write results incrementally to a file and use a single Monitor on that file with a longer timeout. Do not re-enter the sleep+cat loop. Also, Max hasn't answered your first-lines question - proceed with what queue.json has and note the gap; don't block on it.
