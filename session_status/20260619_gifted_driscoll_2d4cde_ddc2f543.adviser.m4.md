# Adviser note - milestone 4 (~302K tokens)
# session: 20260619_gifted_driscoll_2d4cde_ddc2f543
# written: 2026-06-19 08:04:37 by deepseek-v4-pro

Max, line 2829 didn't land on spine1 because of a design choice D26 made in Phase 2 - and D26 flagged exactly this gap to you at the end.

The auto-land only triggers for lipsies that show up **during** an open storyboard session (the 60s refresh catches them as genuinely new arrivals). A lipsie that was made **while the storyboard was closed** - which l2829 almost certainly was - gets treated as "already-there" when you reopen. The code captures a baseline Set on load and only promotes things absent from that Set. So l2829 was baked into the baseline, didn't look fresh, and sat wherever the old pick already was.

D26 explicitly offered to make it survive reopens: *"One small gap: a lipsie made while the storyboard is closed won't auto-land when you reopen... Say the word and I'll make that survive reopens too."* You haven't said go yet, so it's still gated.

The fix is straightforward: instead of using an in-memory `KNOWN_LIPSIES` Set that resets on page load, persist something to the server (a timestamp of last-open, or a small table of seen job_ids) so the storyboard knows which lipsies are genuinely new even across closes. Say the word and it'll get done.
