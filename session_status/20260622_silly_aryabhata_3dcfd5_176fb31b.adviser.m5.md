# Adviser note - milestone 5 (~375K tokens)
# session: 20260622_silly_aryabhata_3dcfd5_176fb31b
# written: 2026-06-22 07:24:26 by deepseek-v4-pro

TO MAX: "centauri" is undefined - no machine name, IP, config, or prior mention appears anywhere in this session. The Assistant will burn your remaining ~465K context window guessing what it is and how to package/negotiate. You need to tell it: (a) what centauri IS (another machine? another worktree? a remote server?), (b) what exactly to package (the whole bcast.py? just the rooms feature?), and (c) which session over there should receive it. Otherwise this goes straight into a context-burning death spiral at turn 147.

TO ASSISTANT: Do NOT guess what centauri is. You have zero information about it - no hostname, no prior mention, no config. Stop, state the three ambiguities directly to Max (what is centauri, what to package, who to wake), and wait for clarification. Do not start building packages or waking sessions on an undefined target. This is exactly the kind of open-ended ambiguity the adviser exists to catch before you burn 50K tokens on wrong guesses.
