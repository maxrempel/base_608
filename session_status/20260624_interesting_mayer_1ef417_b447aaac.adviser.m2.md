# Adviser note - milestone 2 (~151K tokens)
# session: 20260624_interesting_mayer_1ef417_b447aaac
# written: 2026-06-24 15:38:41 by deepseek-v4-pro

TO MAX: Passwords for Cent (maxre) and your OpenWRT router are sitting in plain text in this session log and were also written into global2.md. If anyone ever reads these logs or that file, they have credentials. Up to you whether that matters - just know it's there.

TO ASSISTANT: Stop echoing passwords in command output and avoid hardcoding them into persistent documentation (global2.md). Use cmdkey or credential manager references, not raw strings. Also: when Max says "it was implemented before," check for existing tools before building new ones - you had an SSH-enable pattern already, but you built a fresh Gist without confirming that pattern matches what was used before. Low risk this time, but it's a habit that creates version sprawl. The session otherwise was efficient and on-target.
