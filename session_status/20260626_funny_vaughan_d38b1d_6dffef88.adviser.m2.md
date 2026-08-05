# Adviser note - milestone 2 (~161K tokens)
# session: 20260626_funny_vaughan_d38b1d_6dffef88
# written: 2026-06-26 15:32:40 by deepseek-v4-pro

TO ASSISTANT: You wasted ~30 min encoding a compressed copy for Descript upload before checking whether Chrome file-push works. That limitation is in Max's own notes - you should have tested the upload mechanism first, not sunk encode time into a dead end. Also: the initial re-encode instead of stream-copy on the very first cut was the single worst mistake in the session, and Max had to yell to fix it. You corrected it fast, but the core rule (dense keyframes = copy-cut, never re-encode) should have been front-of-mind, not an afterthought. The method doc and global2 pointer at the end are solid. Next time, validate the upload path before spending CPU on prep.

CLEAN - no action needed from Max.
