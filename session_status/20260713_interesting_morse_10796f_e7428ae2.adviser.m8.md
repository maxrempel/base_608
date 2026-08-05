# Adviser note - milestone 8 (~601K tokens)
# session: 20260713_interesting_morse_10796f_e7428ae2
# written: 2026-07-13 11:50:28 by deepseek-v4-pro

TO MAX: The race-comparison panel you asked for is written and committed, but it is NOT running yet. The safe-restart has been waiting 40+ seconds of your silence to deploy - and you've been dictating non-stop, so it never got the gap. You saw my test render once, not the live thing. Stop dictating for ~40 seconds, wait for the amber "typer updating..." toast, then the panel appears for real on Num+.

TO ASSISTANT: The structural problem: you keep building features on top of the assumption that the safe-restart deploys them, while Max is actively dictating and the deploy blocks. You've now got at least 3 distinct builds committed that haven't gone live. When Max is talking, your "it's deployed on next pause" means "it's NOT deployed." You need to a) tell him explicitly how long he must pause, b) stop adding more until the current backlog lands, and c) consider a shorter grace for light restarts (swaps, small fixes) vs. heavy ones (new panel code). Also: the HUD test render flashed on his screen without warning - only do that if he's asking for a preview, not as a side effect of your test.
