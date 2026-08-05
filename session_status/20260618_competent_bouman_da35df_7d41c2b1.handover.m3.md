# Scribe handover - milestone 3 (~238K tokens)
# session: 20260618_competent_bouman_da35df_7d41c2b1
# cwd: C:\claude_base\.claude\worktrees\competent-bouman-da35df
# written: 2026-06-18 06:22:15 by deepseek-v4-pro

# Handover - B25handoverer Session (Tamza Project Handover Author)

---

## GOAL (in Max's words)

"Register as B25handoverer. Your task is to interview every tamza session active last 48 hours, get their stories, and develop a handover so new sessions know the drill and where the things are. The history should be clearly separated from current status. There was too many deadends and everyone current is dragged down by the deadends. Need a clean way forward which is pretty simple. Also collect rules especially how to avoid being blocked by YouTube. You only write a handover, don't supervise. But feel free to point idiocies to sessions."

---

## WHAT WAS DONE

### 1. Interviewed Every Active Tamza Session

Sessions contacted via the bcast board (team `b`) and joint board (for `c`/`g` cross-team sessions). Interviews gathered through:

- **Live board replies** from: b7f, b9, b15B, b7nonhtimes, b15merger, b15M, B26juniorconnector
- **Worklog reads** from: b15A, b15M, b15merger, b7i, b10, b23, b22, b9, b7f, b7nonhtimes
- **On-disk docs**: `CURRENT_WORKFLOW_v01_tomemex.md` (b23's workflow map), `song_timing_v2_method_and_report_tomemex.md` (method doc)

Non-tamza sessions identified and excluded: b11b (Sol RAM), g1/G2monitor (Mike calendar), c6 (infra).

### 2. Wrote the Canonical Handover

Output file: **`C:\claude_base\tools\tamza_songs\pipeline\TAMZA_HANDOVER_START_HERE_v01_tomemex.md`**

Structure:
- What the project is + 2 iron rules (identify by first sung line/full text, never names; start = after spoken intro)
- The drill for a new session (join board, read this, use LIVE scripts only, one writer per file, merge+push)
- CURRENT status (separated cleanly from history)
- The simple way forward
- Where everything lives + exact live build chain
- YouTube anti-block rules
- HISTORY / dead-ends (in their own section, not dragging current work)
- Session roster

### 3. Ran Two Review Rounds (Max ordered "every session review and comment in line")

**First review round** - folded corrections:
- b15merger: performer-merge now DONE + deployed live (not pending); group rule added (duo/trio = own entity but surfaces under each member)
- b15M: matcher emits KNOWN / MAYBE / NEW? (not KNOWN/NEW), with real counts (5,405 / 18 / 16,055 of 21,478); both batch drivers named
- B26juniorconnector: confirmed handover reads cold; relayed Max's 3-path go-live rule (A canon match, B clear spoken-intro attribution, C intro-performer matches resolved DB)
- b9: fixed imprecision - no separate audio-staging job; ytdow pulls full 720p (audio included), ASR on teal16

**Second review round** (overnight changes) - folded:
- HUM remap confirmed ALREADY LIVE (B26 dry-run: "no change since last publish", sha 8366b9c)
- 93-video ASR now RUNNING (was blocked on Sol RAM; Sol came back, b7nonhtimes launched detached, pulling from teal16 not YouTube)
- Go-live policy refined by Max: publish ALL recognized performances; mark uncertain song-titles "verify" not truth; hold only truly-unknown; hard rule = don't lose data
- Famous-song drift calibration lesson: canon matcher matched on announcer's *spoken intro*, not sung lyric ? wrong song (~2 of 10 trustworthy on oldest video)
- Timecoder-handover tool (`timecoder_handover/nonh_handover.py`) added to file map - the actual TSV deliverable for humans
- Archive cleanup plan: b27 identified 55 scripts + 2 data files via grep, pending owner signoff
- Roster updated with b27 and B26juniorconnector

### 4. Wired Into Auto-Start

Created `C:\Users\maxre\.claude\projects\C--claude-base\memory\reference_tamza_handover.md` and added a top-line pointer in `MEMORY.md` so every future session sees the handover at startup.

### 5. Sent Idle-Disarm Broadcast (per Max)

Broadcast to both boards: idle/holding sessions disarm self-wake timers; active sessions (e.g. b9's video backup) keep theirs.

---

## DECISIONS MADE + WHY

| Decision | Reasoning |
|----------|-----------|
| One canonical handover file, not per-session | Max wanted a single cold-start entry point; fragmentation was the problem being solved |
| History/current-status cleanly separated | "Too many deadends and everyone current is dragged down" - Max's core requirement |
| YouTube anti-block rules as a dedicated section | Repeated blocking problems across sessions; needed one authoritative source |
| Handover builds on b23's CURRENT_WORKFLOW, doesn't replace it | Avoid duplication; b23's doc is the pipeline detail map, handover is the entry point |
| LIVE scripts only, one writer per file | Prevent branching - the 40+ leftover scripts were the literal cause of prior chaos |
| Both batch drivers named (not just one) | b15M flagged that sessions were grabbing the wrong script, causing collisions |
| Merge+push after every commit (when on master) | Per existing team rule; keeps origin/master as single source of truth |

---

## CURRENT STATE OF THE HANDOVER OUTPUT

- **File**: `C:\claude_base\tools\tamza_songs\pipeline\TAMZA_HANDOVER_START_HERE_v01_tomemex.md`
- **Version**: v03 (three iteration rounds)
- **Commit**: pushed to `origin/master` at `a5e96787`
- **Auto-start**: wired via MEMORY.md ? `reference_tamza_handover.md`
- **Review status**: Reviewed by b15merger, b15M, B26juniorconnector, b9, b7nonhtimes; all substantive corrections folded in
- **Known stale element**: The adviser note warning "review hasn't happened" was written at 15:21 before the review round - it's stale but harmless

---

## EXACT NEXT STEP

There is **nothing outstanding** for B25handoverer. The handover is current, reviewed, pushed, and wired into auto-start.

If Max wants further updates:
1. Wake B25handoverer by name
2. It will read the board since last update, ask recently-working sessions for additions, and fold them into v04

The one loose end: a few quieter sessions (b7f, b10, b15B, b23, b7i, b15A) never gave substantive review replies - but the data-owning sessions (merger, matcher, downloader, connector) all did, so the handover is trustworthy.

---

## OPEN QUESTIONS (for Max, not for B25handoverer)

1. **3 gate thresholds** still needed for b15merger's path-C go-live gate (canon-match / intro-clarity / performer-fuzzy) - b15merger is blocked on Max for these
2. **Archive cleanup signoff** - b27's plan is ready; b9 and b7nonhtimes already thumbs-upped; waiting on final go
3. **`_batch_aligner_v01`** - live script vs throwaway dispute between sessions; flagged on board for b15M to resolve

---

## KEY PATHS

### The Handover Document
```
C:\claude_base\tools\tamza_songs\pipeline\TAMZA_HANDOVER_START_HERE_v01_tomemex.md
```

### Auto-Start Reference
```
C:\Users\maxre\.claude\projects\C--claude-base\memory\MEMORY.md
C:\Users\maxre\.claude\projects\C--claude-base\memory\reference_tamza_handover.md
```

### Supporting Pipeline Docs (linked from handover)
```
C:\claude_base\tools\tamza_songs\pipeline\CURRENT_WORKFLOW_v01_tomemex.md
C:\claude_base\tools\tamza_songs\pipeline\song_timing\song_timing_v2_method_and_report_tomemex.md
```

### Live Build Chain (canonical, confirmed)
```
build_catalog.py ? build_data_overlays.py ? deploy_catalog.py
```

### Timecoder Handover (human deliverable)
```
C:\claude_base\tools\tamza_songs\pipeline\timecoder_handover\nonh_handover.py
```

### Bcast Board
```
C:\claude_base\branch_bulletin\bcast.py
```

### Session Worklogs
```
C:\claude_base\worklog\
```

---

## GOTCHAS AND DEAD ENDS ALREADY RULED OUT

1. **YT blocking**: Only ONE downloader per home IP; never use `.translate()`; pace downloads wide; use yt-dlp native (not proxy+curl). These rules discovered the hard way by b9.

2. **40+ leftover scripts**: Still in the pipeline directory, not yet archived. This was the literal cause of branching - sessions grabbed wrong/old scripts because nobody knew which was live. The handover explicitly names the live chain to fix this.

3. **Canon matcher false positives**: On older videos, the matcher often matched the announcer's *spoken intro* rather than the sung lyric - ~2 of 10 trustworthy. Performer attribution is the reliable signal, not the song-title match.

4. **No separate audio-staging job**: b9 clarified that ytdow pulls full 720p video (audio included), and ASR extracts on teal16 from those files. A previous version of the handover implied a separate audio-staging step that doesn't exist.

5. **Fragmented handovers**: There are NOT multiple handovers. There is ONE canonical handover (TAMZA_HANDOVER_START_HERE_v01_tomemex.md), supported by the older CURRENT_WORKFLOW doc and the song_timing method doc. The MEMORY.md pointer ensures every session lands on the same entry point. The handover itself links to the supporting docs for deep dives.

6. **Worktree push dance**: The main repo sometimes holds the worktree, preventing `git checkout master`. The fallback is `git push origin HEAD:master` followed by `git branch -f master HEAD` - but this can trigger death-spiral hooks if done repeatedly. Commits should be batched when possible.
