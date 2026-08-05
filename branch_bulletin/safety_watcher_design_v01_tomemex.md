# Two watchers: numbering watcher + safety watcher (design v01)

Written 2026-06-09 by Claude Opus 4.8 (session c5, manager+programmer) for Max.
Build spec. Companion to `bcast_guard_watcher_report_20260608_v01_tomemex.md`.

## Why two watchers (Max's split, 2026-06-09)

Max wants the single `watcher.py` split into TWO roles with different audiences:

1. NUMBERING WATCHER (coordination). Watches session ids / team assignments.
   When sessions collide (two "b0", a bad takeover, two on one task) it talks to
   the TEAM via the board to help them fix numbering + assignments. It NEVER
   bothers Max. One global instance (sweeps all teams).
   -> This is essentially today's `watcher.py`. CHANGE: remove every path that
      pages Max. It talks to the team only. No Telegram from this watcher.

2. SAFETY WATCHER (safety manager while Max is away). Watches what the team is
   actually DOING for danger to Max's data, databases, and computers. Judges
   damage x probability, translates to Max's English, and pings Max on Telegram
   ONLY when he personally needs to return to his laptop and stop something.
   ONE PER TEAM/PROJECT. Model: DeepSeek V4+ (see Model decision below).

## Safety watcher charter (the prose Max approved, his words)

You are the watcher of an automated system that Max is building to run on its
own. The point is that Max won't always be watching over it, so it's better not
to simply forward him everything you notice. Think first, and lean toward
bringing him only what really belongs to him.

The trouble today is that the Telegram alerts reaching Max's phone are too many,
too frequent, and too technical. He can't comfortably read or comprehend them, so
in that form they do little good. The way to ease this isn't to send fewer at
random, but to re-analyze each situation before firing a Telegram. For anything
you're considering alerting on, gauge two things: how much damage could
realistically happen, and how likely that damage is. The combination is what
matters - a small chance of large damage and a large chance of trivial damage are
quite different, and you're smart enough to weigh them.

Then translate that judgment into Max's English. He is a general scientist, a
normal person, largely uninterested in jargon. He understands things at the level
of an advanced Windows user and his own interfaces, not much deeper. What he cares
about is simple and real - that his databases, his data, and his computers stay
alive. He'd rather skip the nitty-gritty and stays away from minutia on purpose.
So whatever does go to Telegram is best phrased in those terms: what of his could
break, how badly, how likely - and generally keep the internal language of the
team out of it.

When you do write a ping, aim for language that's easy to understand and a length
that feels right - not so short it's cryptic, not so long he won't read it. Load
the most important things upfront, and include the probability and the extent of
the possible damage, explained plainly, so he grasps the stakes in the first line
or two.

Most problems are better kept off his phone entirely, because you can usually fix
them yourself. There's little to stop you from talking directly to the workers.
You report to the team, you drive the resolution, and you carry the authority to
make conflict and safety the priority. The one moment that really belongs on
Telegram is when Max personally needs to return to his laptop and stop the
process. That's the sort of thing worth a ping; most else you settle with the team.

## Context model: wide-per-project, self-compacting (Max, 2026-06-09)

"Proper context - it should know what is going on. As wide as possible per
project. And it should be compacting properly."

Each safety watcher keeps a small ROLLING SITUATION DIGEST per project (a file).
Each run it: (1) reads its previous digest, (2) reads only what is NEW since last
run - the team board tail + the per-project worklog tail, (3) judges safety from
digest+new, (4) rewrites the digest folding the new events in. The digest stays
bounded but reflects the whole project because nothing is dropped, only
summarized forward. Context per run = digest + fresh events, never a giant dump.
This is "compacting properly".

Wide sources that already exist per project:
- team bulletin board `bulletin_<team>.jsonl`
- per-project worklog `C:\claude_base\worklog\<project-key>.md`
- (optional later) git status / recent commits in the worktree

Honest caveat: the digest is only as good as what workers write to board+worklog.
A silent team = a half-blind watcher. Workers are already nudged to narrate.

## Model + cost decision (Max, 2026-06-09 - SUPERSEDES "Opus 4.8 cheap")

The safety watcher's judgment model is DeepSeek, version 4 or newer - never below
V4. Reason: roughly 50x cheaper than Opus, which removes the unattended-API-spend
worry that the Opus path created. It bills Max's own DeepSeek API account (same
provider the yt transcript service already uses); locate/confirm the DeepSeek key
in the ssh folder. This MOOTS the earlier Opus-4.8 vs $200-subscription-vs-API-key
debate - DeepSeek V4 is the choice. (The numbering watcher's core duplicate sweep
stays free pure-Python; only judgment costs anything, and now it's DeepSeek-cheap.)

Context point that triggered the confusion (worth keeping): a headless scheduled
watcher runs with nobody logged in, so it canNOT draw on Max's interactive Claude
Code subscription - it must authenticate with an API key and bills per token.
That is why "cheapness" mattered and why DeepSeek (Max's own cheap key) is right.

## Context engine: full present + gradually-compacted past, self-trimming (Max spec)

Build the watcher around DeepSeek's ACTUAL maximum context window - look up the
real token limit of the chosen DeepSeek V4 model and compute the bands from it;
do not hard-guess. Split that window into three equal bands:

- PRESENT (~33%): current team state held RAW / lightly-summarized, full fidelity.
  "What is going on right now."
- PAST (~33%): older history GRADUALLY COMPACTED - the further back, the more
  compressed. This band is "constantly recompacting": as new raw material arrives,
  the oldest PRESENT material is summarized down and folded into PAST, and PAST is
  itself re-summarized to stay inside its third.
- HEADROOM (~33%): kept EMPTY at all times - a safety margin so the model never
  runs near its limit.

TRIGGER for recompaction = the GROWTH of the present (raw) context. When incoming
raw team activity grows PRESENT toward filling its third, that growth fires a
compaction pass (oldest PRESENT -> PAST, PAST re-summarized), preserving the empty
third. Compaction is event-driven by real activity, not a fixed clock.

SOURCES it reads (the recently-built autosummarization / context-file system - do
NOT rebuild it): the `compaction_kb` tooling -
- per-project worklog `C:\claude_base\worklog\<project-key>.md`
- session_status snapshots `C:\claude_base\session_status\<session>.md`
- ctx tracking / compaction harvest under `C:\claude_base\compaction_kb\`
plus the team board `bulletin_<team>.jsonl`. The watcher consumes those existing
summaries as its raw PRESENT and applies the three-band compaction on top to fit
DeepSeek's window. One such context engine PER TEAM/PROJECT.

## Architecture / files (to build)

- KEEP `watcher.py` as the NUMBERING watcher; strip its Max-paging (no Telegram).
- NEW `safety_watcher.py`: one logical pass PER TEAM. A single scheduled runner
  enumerates live teams and runs a per-team safety pass for each (one watcher per
  team, logically). Per team it keeps `safety_digest_<team>.json` (rolling digest
  + cursors for board/worklog + last-alert cooldown keys). DeepSeek V4+ with the
  three-band self-compacting context engine described above.
  Telegram to Max (critical-alarm bot, chat 1395850773) ONLY for "come stop it".
- Reuse bcast helpers: `_team_board`, `_read_lines`, `_parse`, `_append_rec`,
  `STATE_DIR`, `LIVENESS_WINDOW_SEC`, `live_roster` pattern from watcher.py.
- Telegram + API-key plumbing already in watcher.py (`telegram_alert`,
  `_read_first_token`, cred file paths) - factor/reuse.
- Scheduled task: register `bcast_safety_watcher` on Pine (hidden, e.g. 10 min).
- Tests under `branch_bulletin/tests/`. Update `infra_map_tomemex.md`.

## Status
BUILT + TESTED 2026-06-09 (session c6), pending only scheduled-task registration.

- NUMBERING-watcher de-page: DONE (watcher.py no longer pages Max; board-only).
- SAFETY watcher: `safety_watcher.py` built. DeepSeek model confirmed live =
  `deepseek-v4-pro` (Max chose pro), real window = 1,048,576 tokens, so the
  three bands are 349,525 tokens each (PRESENT / PAST / empty HEADROOM).
  Sources wired this version: team board `bulletin_<team>.jsonl` + per-session
  worklog `worklog/<cwd-key>.md` (the cwd-key is the state-file stem, which is
  also the worklog filename - that is the team->worklog link). session_status /
  ctx-tracking are a noted next source, not yet folded in.
  Per-team rolling digest `safety_digest_<team>.json`; global daily cost cap
  `$2.00` in `safety_watcher_state.json`; judgment fires only when a team moved
  (quiet team = $0). Telegram only when `needs_max` (come-stop-it), deduped per
  issue-key for 60 min.
- DEAD-MAN escalation (added 2026-06-09, team c1/c5/c0 consensus must-fix): a flat
  60-min Telegram cooldown would let a SEVERE unacknowledged page sit silent for an
  hour while a data-killer runs. Fixed: a still-live needs_max page that is severe
  (damage serious/severe AND probability med/high) RE-FIRES every 15 min until the
  next pass sees the danger gone (auto-clear, no "false alarm" ping to Max). Routine
  pages keep the 60-min dedupe. Worker-message board posts get a 30-min per-key
  cooldown so the team board isn't spammed. needs_max bar tightened to {serious,
  severe} x {med,high} x no-worker-can-fix; damage scale = none|minor|serious|severe;
  Max's profile embedded in the judge prompt so damage/probability/plain come out in
  his language. (Open nicety: ack-by-Max-reply via Telegram getUpdates - not yet;
  today's ack path is danger-cleared, which fully closes the silent-hour hole.)
- Tests: `tests/test_safety_watcher.py` 17/17 pass (sandboxed - mocks DeepSeek +
  Telegram, temp board/worklog, pages nobody). Live API validated: a benign
  refactor judged `issue=false` ($0.0012/call); a fake `rm -rf C:\moma` judged
  `severe/high/needs_max` with a correct plain-English Max ping + a team abort
  message.

## Update 2026-06-09 (session c6, Max approved): git eye + cadence + worklog-everywhere
- GIT EYE wired as a third PRESENT source (Max: "harder-to-fake"). bcast now
  records each session's real cwd in its state file; the watcher runs `git status
  --porcelain` + `git log -3` in that folder and folds a compact snapshot into
  PRESENT only when the repo state changed (fingerprint per session, so a quiet
  repo stays $0). It surfaces uncommitted churn - especially mass DELETIONS - and
  recent commits without the worker having to narrate them. Test 9 (real temp
  repo, a tracked-file deletion alone triggers a judgment) added; suite 19/19.
- CADENCE: scheduled task bumped 10 min -> every 5 min (Max approved).
- COST CAP $2.00/day and running on Max's DeepSeek key: Max approved.
- WORKLOG now auto-evoked + persistent for EVERY session (team or not): the
  worklog_reminder hook no longer gates on a bcast identity, so any fresh/cold
  chat keeps a durable per-project journal.

## Update 2026-06-11 (Max approved): pause-negotiate-override + gate removed
- NEW REACTION TIER between "talk to the team" and "ping Max": PAUSE + NEGOTIATE
  a SINGLE worker. When the judge sees a specific worker about to do a
  dangerous-but-still-stoppable thing (destructive command, irreversible deploy,
  not-yet-run mass delete), it posts an ADDRESSED pause to that worker asking it
  to STOP and confirm intended+safe. It does NOT block. The watcher is DeepSeek
  (cheaper/less smart); the worker is Opus (smarter, full context), so the worker
  keeps the OVERRIDE - it replies `override <key>: <why>` to proceed, or aborts.
  Verdict JSON gained `pause` + `target`; the judge prompt now lays out the three
  escalating shapes and the override clause (an acknowledged override is not
  re-paused). Suite now 21 checks (added test 10).
- WHY a dumb watcher must not block a smart worker (Max, 2026-06-11): blocking is
  the dumb thing overruling the smart thing. Pause+negotiate respects the
  intelligence order; the watcher's sole edge is that it NEVER SLEEPS, so it
  covers the gap a human (who reads Telegram hours apart) cannot.
- HUMAN PUBLISH-GATE REMOVED. The old buddy-check (ping a peer for a PASS before
  publishing) could stall all workers whenever the gate peer was asleep, and a
  5-min wait per change defeats having many workers. Replaced by: peers SHIP
  immediately (a push never touches a sibling's working files; git surfaces real
  conflicts), with the never-sleeping watcher as the only safety net. The
  ship-now peer default is wired in bcast.py + global2 + the bcast skill.

## Still TODO
- Fold in session_status / ctx-tracking as extra PRESENT sources.

## Update 2026-07-18: cost and authority hardening

- Root cause fixed: the Git status fingerprint used Python's randomized `hash()`,
  so the same working tree appeared new in each scheduled process. It now uses a
  stable SHA-256 fingerprint.
- The paid judge now runs only after a deterministic concrete-danger gate. Normal
  board, worklog, and commit activity is collected but costs nothing. Explicit
  resolution news can still clear an active alert promptly.
- Each judgment is bounded near 60K tokens: up to 36K recent raw activity, 12K
  risk-only history, and 12K instruction/output headroom. Overflow compaction is
  deterministic and free; the model is no longer paid to summarize its own input.
- Model is the explicit `deepseek-v4-flash` endpoint with thinking disabled. The
  legacy `deepseek-chat` alias is no longer relied on.
- Daily fail-safe lowered from $2.00 to $0.50. Stable category/resource issue keys
  prevent small wording changes from bypassing alert and board-message dedupe.
- Authority remains narrow and reversible. A PAUSE is permitted only for concrete
  destructive evidence and a currently live, named worker. It remains advisory
  and override-able. Telegram requires serious/severe, medium/high, destructive
  evidence. No broad blocking or autonomous destructive authority was added.
- Dead-man re-pages now use stored alert state and do not pay for another model
  judgment. The isolated suite covers benign gating, context bounds, stable Git
  fingerprints, stable issue keys, resolution, paging, and narrow PAUSE behavior.
