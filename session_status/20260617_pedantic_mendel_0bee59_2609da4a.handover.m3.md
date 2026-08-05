# Scribe handover - milestone 3 (~228K tokens)
# session: 20260617_pedantic_mendel_0bee59_2609da4a
# cwd: C:\claude_base\.claude\worktrees\pedantic-mendel-0bee59
# written: 2026-06-17 21:37:39 by deepseek-v4-pro

# TAMZA HANDOVER - B26juniorconnector session

## GOAL (Max's own words)

"We're near the end point - a clean DB + live things. Newly identified songs should go live. Unknowns shouldn't."

Max also assigned three specific tasks:
1. Pick the oldest good NONH (not-human-done) video, double-check its draft, hand it to human timecoders.
2. Develop work for B27, manage B27 as a junior manager.
3. Push-live the ready things - safely, consulting the collective (esp. b15merger).

The go-live gate has three OR-paths, per Max's refined directive:
- **Path A**: confident song-text match against the 994-song known reference.
- **Path B**: clear spoken intro (performer says "this is my song" or names the composer/poet).
- **Path C**: spoken performer name matches the clean performer DB.
A segment that fails all three stays held - not published.

---

## DECISIONS MADE + WHY

### 1. Handover table format mirrors the EXACT human Excel
**Why:** Found the real "????? ?? ?????.xlsx" at `C:\Users\maxre\Downloads\`. Inspected it - one sheet per concert, columns: ? | ?????? | ??????????? | ???????? | ?????? | ?????? ?????? | ??????? ????? | ?????? | ??????? + ??????????? | ????-???? | ??????? ? ?????? ?????. Rows are grouped by performer. Matching this exactly means zero friction for the human timecoders.

### 2. Date source = channel_inventory.json, NOT YouTube API
**Why:** 691 NONH videos - hitting YouTube for upload dates would violate block rules and ytdow is already running. The `channel_inventory.json` (935 videos, including all NONH) already has `upload_date` and `title`. No API hit needed.

### 3. Oldest good NONH video picked: pX_1m8DlMbA
**Why:** Joiner ranked all NONH videos with drafts by upload_date ascending, filtering for "good" (has captions, has draft). pX_1m8DlMbA is 2020-03-30 ("?????? ?? ???????????? ?????"), 47 segments, 10 identified - a fringe/old video, exactly the kind that needs human timecoder attention.

### 4. Path A (song match) flagged as UNSAFE on old/fringe videos
**Why:** Independent LLM review of the handover table found ~half the "KNOWN" song titles were WRONG - the matcher drifted to famous songs that contradict what was actually sung (e.g., heard "???????? ?????????" but tagged a different famous song). Tamza sings fringe repertoire; the machine reaches for famous matches. Path C (performer-in-DB match) is the safer publish path. b15merger was consulted; awaiting reply.

### 5. Dry-run before any live deploy - the human catalog is ALREADY LIVE
**Why:** Ran `publish_catalog.py --dry-run` as homework (not a deploy). Output: "NO CHANGE since last publish - nothing to deploy." 26,283 rows, 22,051 timed ends match live SHA. The re-timing push Max ordered was in fact already done. No risky solo deploy needed.

### 6. B27 task = archive cleanup
**Why:** Everyone flagged it but nobody owned it - the literal root cause of project branching. Reversible git moves. Holding for remaining owner OKs (b9 approved; need 1-2 more).

---

## CURRENT STATE

**Done:**
- All NONH machine indexing: captions, song-splitting, 994-song reference, matching.
- Human-side catalog re-timed and **already published live** (26,283 songs, 22,051 timed).
- Performer de-duplication - live on the website.
- Website features (voting, login, playlists) - live.
- Handover tool (`nonh_handover.py`) built, committed, pushed - picks oldest good NONH video, emits table in exact human Excel format with a "machine guesses - VERIFY" warning.
- First handover table for pX_1m8DlMbA generated and pushed.

**In flight (needs chasing):**
- **NONH go-live gate**: b15merger is building it. Path A known-unsafe for fringe videos. Path C is the reliable path. Thresholds not yet set. b15merger was woken by name; reply pending.
- **B27 archive cleanup**: holding for remaining owner OKs.
- **b7i publish residual**: b21 speech-residual refinement may still need publishing - unconfirmed.
- **ytdow backup**: ~290/2842 done, ETA Jun24-30. Off-Sol, just slow.

**Blocked on Sol (external):**
- 93 caption-less videos need speech-to-text. Sol off-limits during RAM testing. b9 pulled 44/93 to teal16.

---

## EXACT NEXT STEP

1. **Follow up b15merger** (board wake) - get status on the NONH gate: path C implementation, thresholds, ETA.
2. **Tally remaining owner OKs for B27 archive cleanup** - once approved, release B27 to execute.
3. **Confirm b7i residual status** - is b21's speech-refinement still a separate publish step, or is it already folded in?
4. **Continue autonomous loop** - wake timer is armed (~12 min, re-arms each tick). Contact teammates by board name-wake. No solo deploys.
5. **Weekly handover** - keep the table tool + ledger current; pick the next oldest good NONH video when the first one is claimed.

---

## OPEN QUESTIONS AWAITING MAX

1. Is the handover table format correct? The tool mirrors the exact "????? ?? ?????.xlsx" column layout - but confirm with the timecoder team (b10/b7nonhtimes) whether they want any tweaks.
2. The path-A drift finding: should identified titles be published at all on fringe videos, or held as "verify" everywhere? b15merger may recommend a confidence threshold.
3. Should the handover table include a "machine confidence" column so timecoders can triage?

---

## KEY FILES AND PATHS

| What | Path |
|---|---|
| Pipeline root | `C:\claude_base\tools\tamza_songs\pipeline\` |
| Handover tool | `...\pipeline\timecoder_handover\nonh_handover.py` |
| First handover table | `...\pipeline\timecoder_handover\tables\handover_2020-03-30_pX_1m8DlMbA.tsv` |
| Human Excel reference | `C:\Users\maxre\Downloads\????? ?? ?????.xlsx` |
| Channel inventory (dates) | `C:\claude_base\tools\tamza_songs\output\channel_inventory.json` |
| NONH drafts directory | `...\pipeline\song_timing\from_scratch_idx\_work\annotator\drafts_nonh_v01\` |
| Board tool | `C:\claude_base\branch_bulletin\bcast.py` |
| Publish script | `...\pipeline\scripts\publish_catalog.py` (supports `--dry-run`) |
| START-HERE handover | `...\pipeline\TAMZA_HANDOVER_START_HERE_v01_tomemex.md` |
| Workflow map | `...\pipeline\CURRENT_WORKFLOW_v01_tomemex.md` |
| Worklog | `C:\claude_base\compaction_kb\scripts\worklog.py` |
| This session's worktree | `C:\claude_base\.claude\worktrees\pedantic-mendel-0bee59` |

**Key IDs:**
- Oldest good NONH video: `pX_1m8DlMbA` (2020-03-30)
- Board identity: `B26juniorconnector`
- B27 worker alias: `b27`

---

## GOTCHAS

1. **Path A is unreliable on fringe videos.** The song matcher drifts to famous songs - don't publish matched titles as fact without human verification. The handover tool now warns "machine guesses - VERIFY."

2. **Do NOT hit YouTube API.** 691 NONH videos would trigger rate limits; ytdow is already running. All date data is in `channel_inventory.json`.

3. **Sol machine off-limits.** 93 caption-less videos are blocked until RAM tests complete. No workaround.

4. **Other sessions have uncommitted changes in the worktree.** Always check `git diff --cached --name-only` before committing - only stage and commit your own files.

5. **The publish_catalog.py dry-run said "NO CHANGE."** The human catalog is already live. Don't re-run a deploy expecting to push the human side - only the NONH gate (when built) will have new content.

6. **Branch bulletin board uses `post` for broadcasts and `wake` to ping a specific name.** `wake` sends a DM-style signal; `post` is a general bulletin.

7. **The board cursor advances with `read`.** After inhaling the full board, the cursor was advanced via `bcast.py read`. A cold session should `catchup` to see new traffic.
