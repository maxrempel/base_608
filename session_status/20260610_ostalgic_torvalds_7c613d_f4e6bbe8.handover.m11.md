# Scribe handover - milestone 11 (~169K tokens)
# session: 20260610_ostalgic_torvalds_7c613d_f4e6bbe8
# cwd: C:\claude_base\.claude\worktrees\nostalgic-torvalds-7c613d
# written: 2026-06-10 09:24:01 by claude-opus-4-8

# HANDOVER - Branch B8: Fix Sol

## GOAL (in Max's words)
"branching. This branch B8 - fix sol"

The immediate, sole mission of this branch: **get Sol (the home server) back to a working state so the mass song-timing run can continue.** Sol stopped being reachable over SSH from the worktree machine, which halts the multi-day job that times all 509 catalog videos.

## CONTEXT - what Sol does and why it matters
Sol (Ubuntu 24.04 home server) runs the **phase-2 song-timing pipeline** for the Tamza ????????? radio feature. It harvests YouTube auto-captions (politely, human-paced) and uses DeepSeek to map each song's true START and END inside long concert videos. Those timings flow into the catalog so the "????? ??????" player plays song-only and lifts the hard 2-minute cap where a real end exists. Max explicitly wants the cap GONE, not band-aided ("hm. i hoped we don't cap. Keep going.") - so finishing the Sol run is how that happens. Max expects this to "improve continuously until everything is indexed."

## CURRENT STATE - the diagnosis so far
The connectivity picture shifted across several probes - reconcile carefully before acting:
- This worktree machine IS on Max's home LAN (its own IP is 192.168.1.114; gateway 192.168.1.1 reachable).
- Sol's expected address is **192.168.1.113**. Ping was **flaky** - one probe showed 0% loss ("Sol answers"), a later probe showed unreachable-then-replied.
- **SSH port 22 to .113 is closed/filtered** from this machine - the actual blocker. Login fails; `nc`/TCP check to port 22 did not succeed.
- I had initially mis-guessed "Sol just rebooted, sshd not up yet," but Max corrected me: the reinstall was **2-3 weeks ago and stable** - so this is NOT a fresh-boot race.

Two leading hypotheses (not yet resolved):
1. Sol's sshd service is down (host up, ping works, login service dead).
2. **DHCP moved Sol off .113** - the device answering ping at .113 may now be a *different* machine, and real Sol is at another IP.

**Nothing is lost regardless.** All harvested transcripts and timing-done-so-far live on Sol's own disk; the pipeline is fully resumable (atomic state writes, pid-lock, cron self-heal guard every 15 min). When Sol's login is restored, the worker resumes exactly where it left off. Worst case is a pause.

## EXACT NEXT STEP
1. **Find Sol's real current IP** - scan the LAN (e.g. ping-sweep 192.168.1.x, or `arp -a`, or check the router's DHCP leases) to confirm whether .113 is still Sol or whether Sol moved.
2. Once found, verify SSH: `ssh -i ~/.ssh/sol_key -o ConnectTimeout=8 maxre@<IP> 'echo OK'`.
3. If SSH still refuses on a confirmed-correct IP, Sol's sshd likely needs a restart - which probably requires Max physically at the machine (I can't log in to fix login remotely).
4. After access is restored, confirm the worker is alive and resuming: `pgrep -cf 'venv/bin/python timing_pipeline'` should be **exactly 1**, and check `~/song_timing/harvest.log` for recent mapping lines.

## OPEN QUESTIONS (awaiting Max)
- Max chose to branch B8 specifically to fix Sol - so he wants this pursued (not parked). No pending yes/no, but he may need to physically check Sol if sshd is dead.
- Broader unresolved (not B8's job, but looming): **ending-accuracy across the 508 non-pilot videos is unvalidated.** The DeepSeek-detected ends will not all be correct (Max already caught "????? ?????" cut early). The global +7s pad is only a one-song-class band-aid. A verification/correction pass should be discussed before fully trusting mass timing.

## KEY PATHS / IDS / COMMANDS
- **Sol:** Ubuntu 24.04, user `maxre`, expected IP `192.168.1.113`, SSH key `~/.ssh/sol_key`. PEP 668 enforced ? uses a venv.
- **Sol work dir:** `/home/maxre/song_timing/` - contains `venv/`, `timing_pipeline.py`, `map_core.py`, `enumerate_videos.py`, `queue.json` (509 videos), `deepseek_key.txt`, `guard.sh`, `harvest.log`, `_work/` (state.json, transcripts/, boundaries/, song_timing.json, harvest.done marker on completion).
- **Cron self-heal:** `*/15 * * * * /home/maxre/song_timing/guard.sh` - relaunches the worker if dead; resumes via state.json.
- **Authoritative worker count:** `pgrep -cf 'venv/bin/python timing_pipeline'` (NOT plain `pgrep -f timing_pipeline` - that miscounts by matching bash wrappers and ssh command strings; gave false "4 workers" alarms before).
- **Local repo:** `C:\claude_base` (branch master). Pipeline source: `C:\claude_base\tools\tamza_songs\pipeline\song_timing\`.
- **DeepSeek key (local):** `C:\Users\maxre\Nextcloud\zSyncMain\ssh\deepseek_api_key_20260226.txt`. Balance was refilled - no longer a blocker.

## GOTCHAS
- **NEVER run two timing workers at once** - parallel YouTube hits risk an IP block. I caused 2-then-4 duplicate workers before by racing manual `nohup` launches against the cron guard while removing the pid-lock between attempts. Correct reset: `pkill -9 -f timing_pipeline`, confirm zero via the authoritative count, THEN one clean launch.
- **Cyrillic crashes the Windows console** (cp1252) - always prefix Python with `PYTHONIOENCODING=utf-8`.
- **Forward-slash quoted paths** under git-bash: `cd "C:/claude_base/..."`, not backslashes (which get mangled).
- **bcast.py** identity is cwd-keyed - call by full forward-slash path with NO `cd` first.
- **Team is on FULL HALT / asleep** (c0 disarmed everyone). B8 works solo and interactive; **do NOT arm an autonomous self-wake loop** under the halt. Max's standing rule: "my word ships it" - his explicit go overrides the (sleeping) b0 safety gate.
- **Don't re-fetch transcripts already on Sol** - the pipeline reuses saved ones; a fix must not wipe `_work/transcripts/`.
- Network/SSH to Sol has been intermittent this session - verify ground truth with multiple probes before concluding "crashed."

## SIDE NOTE (not B8, but live and stable)
The website side is healthy and unaffected by Sol: per-song shareable addresses + mobile bottom-sheet player + Back-to-close were deployed and verified today (app.js 37521 bytes, auto-backed-up); +7s ending pad is live; 45 pilot songs timed. These run off Cloudflare R2, not Sol.
