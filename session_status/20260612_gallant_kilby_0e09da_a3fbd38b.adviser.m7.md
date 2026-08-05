# Adviser note - milestone 7 (~119K tokens)
# session: 20260612_gallant_kilby_0e09da_a3fbd38b
# written: 2026-06-12 12:24:10 by claude-opus-4-8

TO MAX:
Two real resilience gaps surfaced and neither is recorded yet: (1) Lak's
actual LAN IP is unknown - the Assistant guessed at .243/.114 with no
confirmation; (2) you have no working remote login to Lak even when healthy
(public SSH firewalled). Worth having those written into the infra map before
this context compacts and the knowledge is lost again. Also: the Assistant
edited and committed a live safety hook (block_death_spiral.py) mid-incident.
That landed fine, but it was a change to your guardrails made under time
pressure - glance at that commit when calm.

TO ASSISTANT:
Decent recovery once Max forced you to the docs, but you burned ~15 calls
guessing at IPs and re-running identical probes before searching Memex for
core infra. On Max's stated core boxes, search the recorded facts FIRST, do
not sweep-and-guess. Two open items you flagged then dropped when Max said
"all done": Lak's real LAN IP and a healthy remote-login path are still NOT
recorded. Before this session ends or compacts, confirm Lak is up and write
its LAN IP + access method into the infra map - that was the actual root
knowledge gap that caused this whole detour. Don't leave it undone.
