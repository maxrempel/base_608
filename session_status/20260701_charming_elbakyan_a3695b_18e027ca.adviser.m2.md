# Adviser note - milestone 2 (~166K tokens)
# session: 20260701_charming_elbakyan_a3695b_18e027ca
# written: 2026-07-01 13:05:20 by deepseek-v4-pro

TO ASSISTANT: You fired J3097 before checking that the wan26au worker was alive. The worker was down (crashed on Nextcloud placeholder blip at LIPSYNC_TEMP makedirs). The reel rendered only because the worker had auto-recovered independently from a different pid before you ever touched the code. If it hadn't, Max would have a spine-pinned job sitting queued and invisible. Check pipeline health BEFORE firing - one `cat pidfile` or `grep` on the worker log takes 2 seconds. You got lucky here.

Also: 6 diagnostic scripts for line_hash vs merge_hash disambiguation is too many. The first diag already told you `e3d6d39b36f10a NOT in merge_ops` - that should have triggered the merge_hash lookup immediately, not 3 scripts later.

CLEAN - no action needed
