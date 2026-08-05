# Scribe handover - milestone 1 (~142K tokens)
# session: 20260617_competent_bouman_da35df_7d41c2b1
# cwd: C:\claude_base\.claude\worktrees\competent-bouman-da35df
# written: 2026-06-17 15:21:33 by deepseek-v4-pro

# TAMZA HANDOVER - Cold Start Here

## GOAL (Max's words)

"Interview every tamza session active last 48 hours, get their stories, and develop a handover so new sessions know the drill and where the things are. The history should be clearly separated from current status. There was too many dead ends and everyone current is dragged down by the dead ends. Need a clean way forward which is pretty simple. Also collect rules especially how to avoid being blocked by YouTube."

## DECISIONS MADE + WHY

1. **Handover lives at `tools/tamza_songs/pipeline/TAMZA_HANDOVER_START_HERE_v01_tomemex.md`** - chosen as the single cold-start entry point, pushed to master (commit `822ec689`), so any new session reads exactly one file.

2. **Interviewed live sessions + read worklogs** - live answers came from b7f, b9, b15B, b7nonhtimes via the bulletin board. Worklog reads covered b15A, b15M, b15merger, b7i, b10, b23, b22. Non-tamza sessions (c6, g1, G2monitor, b11b - Sol RAM, Mike calendar, infra) were identified and excluded from the handover scope.

3. **History section deliberately separated** - dead ends (40+ leftover scripts, aborted approaches, the "unknown pipeline" confusion, the proxy+curl YouTube attempt that got blocked) are quarantined in their own history section so current sessions stop carrying them.

4. **Two iron rules of the pipeline documented explicitly:**
   - Identify songs by first sung line + full text, never by titles/names.
   - Song start = after the spoken intro, not the video start.

5. **Live build chain resolved** - b15merger flagged it as "unknown," but the chain is actually: `build_catalog.py ? build_data_overlays.py ? deploy_catalog.py`. Confirmed by reading script headers. Handover states this unambiguously.

6. **Exactly ONE puller per home IP** - this is the cardinal YouTube anti-block rule discovered through painful dead ends. The handover also bans `.translate()` calls, mandates wide pacing between requests, and requires yt-dlp native (not proxy+curl hacks that got sessions blocked).

7. **One writer per file** - concurrent sessions must not write the same file. Handover enforces this.

8. **Remaining idiocies called out but not fixed on the spot:**
   - 40+ leftover scripts in the pipeline directory are neither archived nor deleted - they literally caused the branching problem.
   - The live build chain was being called "unknown" when it's straightforward and documented in script docstrings.

## CURRENT STATE

**Done:**
- The handover is written, committed, pushed to origin/master.
- All active tamza sessions have been interviewed or their worklogs read.
- The board has been updated with an announcement post.
- The worklog has been logged.

**In flight (the one real job):**
- Video backup - pulling and archiving YouTube videos.

**The one real blocker:**
- 93 ASR (automatic speech recognition) videos are waiting on Sol (b11b, which is not a tamza session - it's working on RAM infrastructure). Until Sol delivers, those 93 remain unprocessed.

**Session roster (active tamza sessions, last 48h):**
- b7f, b9 (YouTube downloader), b15B, b7nonhtimes - answered interview live
- b15A, b15M, b15merger, b7i, b10, b23, b22 - captured via worklogs

## EXACT NEXT STEP

For any new cold session joining:
1. Read `tools/tamza_songs/pipeline/TAMZA_HANDOVER_START_HERE_v01_tomemex.md` on master.
2. Join the bulletin board: `python C:/claude_base/branch_bulletin/bcast.py`
3. Use ONLY the live scripts: `build_catalog.py ? build_data_overlays.py ? deploy_catalog.py`
4. Continue the video backup job, or pick up the 93 ASR videos once Sol delivers.
5. Always merge + push when done (`git merge master`, checkout master, merge branch, push origin).
6. Do NOT touch the 40+ dead scripts - they are history, not current.

## OPEN QUESTIONS

- Some sessions may still send late interview answers - the handover can absorb them but is already complete for a cold reader.
- Whether the 40+ dead scripts should be archived into a `legacy/` subdirectory was flagged but not decided - no session volunteered to do it yet.

## KEY PATHS AND IDS

| What | Where |
|---|---|
| Handover (cold start) | `tools/tamza_songs/pipeline/TAMZA_HANDOVER_START_HERE_v01_tomemex.md` |
| Live build chain | `scripts/build_catalog.py` ? `song_timing/build_data_overlays.py` ? `song_timing/deploy_catalog.py` |
| YouTube method doc | `tools/tamza_songs/pipeline/song_timing/song_timing_v2_method_and_report_tomemex.md` |
| Current workflow (b23's map) | `tools/tamza_songs/pipeline/CURRENT_WORKFLOW_v01_tomemex.md` |
| Bulletin board | `C:/claude_base/branch_bulletin/bcast.py` |
| State files | `C:/claude_base/branch_bulletin/state/*.json` |
| Worklogs | `C:/claude_base/worklog/*.md` |
| Commit on master | `822ec689` |
| Branch for this worktree | `claude/competent-bouman-da35df` |
| Worktree path | `C:\claude_base\.claude\worktrees\competent-bouman-da35df` |
| Home IP (yt-dlp) | The user's home connection - only ONE puller allowed on it at a time |

## GOTCHAS

1. **YouTube block vector #1: multiple concurrent pullers on the same home IP.** Even two sessions pulling different videos from the same IP triggers blocks. Exactly one session may pull at a time. Other sessions must wait or coordinate.

2. **YouTube block vector #2: `.translate()` calls** - these trigger bot detection. Never call translate on fetched content. Work with raw responses only.

3. **YouTube block vector #3: proxy + curl hacks** - yt-dlp with socks proxies and curl wrappers was tried and burned. Use stock yt-dlp, native connection, wide pacing.

4. **Pacing rule:** space requests widely. No rapid-fire downloads.

5. **The "unknown pipeline" confusion:** multiple sessions didn't know what the live build chain was. It is now documented in the handover. Any session calling it "unknown" has not read the handover.

6. **File collision hazard:** multiple sessions writing the same output file will corrupt state. Coordinate before touching `deploy_catalog.py` outputs or worklog files.

7. **Song identification:** using song titles or artist names breaks the pipeline's key design (the system identifies by first sung line + full text). Never introduce name-based identification.

8. **Intro boundary:** the pipeline assumes songs start after the spoken intro. If a video lacks a clear spoken-intro ? singing transition, that video needs manual boundary marking - don't let automated timing guess.

9. **Merge dance required:** the workflow uses separate branches per worktree. Every session must merge its branch into master and push, then other sessions pull, to avoid divergence. The branch is `claude/competent-bouman-da35df` for this worktree.

10. **Dead scripts still present:** 40+ legacy/experimental scripts live alongside the live chain in `tools/tamza_songs/pipeline/scripts/` and `song_timing/`. A new session looking at directory listings will see them and may try to run them. Ignore everything except the three live scripts named above.
