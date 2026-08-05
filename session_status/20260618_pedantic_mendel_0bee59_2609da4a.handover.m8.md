# Scribe handover - milestone 8 (~601K tokens)
# session: 20260618_pedantic_mendel_0bee59_2609da4a
# cwd: C:\claude_base\.claude\worktrees\pedantic-mendel-0bee59
# written: 2026-06-18 15:20:51 by deepseek-v4-pro

# TAMZA HANDOVER - B26juniorconnector (Manager)

**Date:** 2026-06-18/19 (overnight watch into morning)
**From:** B26juniorconnector (junior connector/manager, grew into role)
**For:** Any cold session resuming this work

---

## GOAL (Max's words)

The project endpoint is a **clean database + live catalog**. Newly identified songs from NONH (not-yet-human-indexed) videos should go live. Unknowns stay held. The core identity principle: **song identity = first sung line only, no canon titles, no famous-name substitution, verified by a smart LLM reading the actual transcript, many rounds of hand-QC on pilots, cheap DS4 batch at scale.** Budget caps: ~$3 total for pilots/trials, ~$12 max for full Tamza runs.

Max is also managing personally: his radio performer page cuts songs at 2 min because end-times are missing for ~4,232 songs. Wants the generic fix (time everything, not special-case his own).

---

## CRITICAL RULES LOCKED IN (violating these caused major rework)

1. **Kill all titles.** No "????????" as identity anywhere. Song identity = **first sung line**, verified by smart LLM (DS4-nonflash minimum), spot-checked by manager by hand.
2. **No mechanical matching.** Python ngram/fuzzy matchers drift to famous songs when they hear an announcer say a famous author name. Only an LLM actually **reading** the transcript can faithfully identify what was sung.
3. **No Opus API** (sub-agents or direct) - a session recently burned $40 where DS4-nonflash would work. Already-running Opus session is free (subscription) and used for spot-checks only.
4. **No polishing toward canonical lyrics.** Faithful-to-heard text > polished canonical. If the heard text is too garbled to identify without guessing the famous line, mark VERIFY, don't substitute.
5. **Pilots + QC = by hand, many rounds.** Manager (me) hand-verifies every pilot before scale. Cheap DS4 batch only for final scale, with hand-QC on batch output too.
6. **No special-casing Max's own songs.** Generic fixes only.
7. **Old sessions knew these rules; new ones drifted.** They're now enshrined in the START-HERE handover and a method doc.

These were added to `global2.md` (the Opus-API prohibition) and the START-HERE handover (all 7 cardinal rules).

---

## DECISIONS MADE + WHY

### Go-live gate (3-path, later simplified)
- **Originally:** 3 paths to publish - (A) confident song-text match, (B) clear spoken intro naming author/composer, (C) performer matches the clean performer DB.
- **Corrected by Max:** Kill all titles, first-lines only. The gate must be titles-free. POEM, VERIFY, and INTRO-ONLY segments are held (not published).
- **b15merger** built the titles-free gate split: 6997 publish-candidates / 68 truly-unknown from the 697-video snapshot (current). Consumes verified first-lines from b27.
- **Why:** The mechanical matcher drifted to famous songs on old/fringe videos (~half the matches were wrong on the pilot video). The LLM-reading approach avoids this.

### Publish policy
- **Publishing recognized performances is safe** - the only real risk is losing data. Mitigated by: backup live catalog before deploy, keep held/unknown set on disk, reversible rollback, byte-verify.
- **HUM remap is already live** (verified via `publish_catalog.py --dry-run`: 26,283 rows, 22,051 timed, no change since last publish).
- **NONH recognized songs NOT live yet** - gated on b27's verified first-lines + b15merger's titles-free gate.

### ASR for 93 caption-disabled videos
- **93 videos had no YouTube captions.** b9 downloaded them as video to teal16. Speech-to-text runs on Sol (CPU-bound, ~7-9 min/video, resumable). Last count: 52+/93 done, grinding overnight, on track.
- **Pipeline validated end-to-end:** noisy ASR still yields reliable performer attribution (intros transcribe clean); garbled song lyrics stay "verify"; English/silent vids correctly fall to honest-unknown.
- **b7nonhtimes** owns the ASR?seg?identify chain. Drains batches as transcripts land.
- All 93 videos' mkv files are on teal16 (b9 finished the priority pull, 0 walls all night).

### Archive cleanup
- **B27** built a concrete plan (55 files + 2 data files, zero live-import collisions), parked on b27's branch. **Not yet merged** - awaiting owner sign-offs. b9 already approved. One conflict: `_batch_aligner_v01.py` doc-vs-reality (b15M should resolve).
- **Holding for Max's AM signoff.**

### Handover table for human timecoders
- Built by me (B26). Mirrors the exact Excel format from `C:\Users\maxre\Downloads\????? ?? ?????.xlsx` (11 columns, performer-grouped, per-concert tabs).
- **Multi-pass LLM-vetted:** 1st pass caught famous-song drift (~half the matched titles wrong); 2nd pass demoted drift cases to "?????????" (verify). Only 2 of ~10 song matches on the pilot video (pX_1m8DlMbA) are trustworthy.
- **Now titles-free:** After Max's correction, all titles stripped. Table carries first sung lines + honest flags (OK/verify/guess).
- **Correction needed:** The earlier version still carried canon titles - that was the disaster Max called out. Fixed now.
- Tool: `tools/tamza_songs/pipeline/timecoder_handover/nonh_handover.py` (subcommands: `pick` = oldest good NONH video, `table` = generate handover in human format).

### 2-min cap on radio end-times (DIAGNOSED, FIX STAGED)
- **Root cause:** NOT a player bug, NOT stale publish. The radio player (`app.js:605-614`) plays a song to its full real end when it has `seg_end`; falls back to 2-min cap ONLY when `seg_end` is missing. 4,232 of 26,283 catalog rows have no `seg_end` ? those are the capped ones.
- **Three buckets found by B30:**
  - **(A) ~900 songs:** Have timed ends in the remap store but were stale in the live catalog. A **republish recovers all 899** - purely additive (0 changed, 0 lost, reversible with backup + byte-verify). **Staged, awaiting Max's "go" to deploy.** Zero spend, zero YouTube.
  - **(B) ~2,944 songs / 61 videos:** Have NO transcript at all. These need ASR from teal16 (where your full backup already downloads them) ? timing. No YouTube hit needed - use teal16 speech-to-text, not caption-fetch. 7 of the 61 are already on teal16 and can start ASR now; the rest as the backup reaches them.
  - **(C) ~338 songs:** Edge cases (very short songs near end of video, etc.).
- **Max's clarifying catch:** Do NOT frame this as "blocked on ytdow backup / YouTube puller." The 61 videos get speech-to-text from teal16 (no YouTube, no block), exactly like the 93 NONH videos. No second YouTube downloader needed.

### First-line extraction (the core ID fix)
- **Pilot video:** pX_1m8DlMbA (2020-03-30, "?????? ?? ???????????? ?????", 47 segments)
- **b27's progression:**
  - v01: Method solid, but drifted to famous canonical lyrics (seg09 ? "??????? ????????? ?????????..." instead of faithful "???????? ?????????..."). **Blocked.**
  - v02 FAITHFUL: All drift removed. seg09 ? VERIFY (honest), seg41 ? faithful heard text. POEM/VERIFY classes sound. **Passed my hand-spot-check.**
  - v03 (in progress): Tightening poem handling (POEM class sometimes over-triggers on sung couplets).
- **Key finding:** Cheap DS4 model does NOT drift to canonical - faithfulness is solved. The model stays honest to the heard text.
- **Scale path:** b27 runs DS4 pilot (~$0.03, under $3 cap) ? I hand-QC ? if solid, full DS4 run (~$12 max).
- **Output format:** JSON per video: `{seg_id: {first_line, class: SUNG|POEM|VERIFY|INTRO_ONLY}}`, consumed by b15merger's titles-free gate.

### Opus API prohibited
- **Rule added to global2.md:** Never use Opus API without Max's explicit permission - because it's very expensive. Covers Opus sub-agents (Agent tool `model: opus`) and direct Anthropic-API Opus calls. A session wasted $40 where DS4-nonflash would work.
- **Opus API key DISABLED** by Max - hard-enforced, no session can burn money on Opus sub-agents.
- Bulk LLM work ? DS4-nonflash (DeepSeek, separate key). Manager's spot-checks ? already-running Opus session (subscription, free).

### Wake/infra bugs discovered
- **Selective force-wake unreliable on idle sessions:** `bcast wake` reported "FORCE-WOKEN" without verifying a listener was alive. b27's session was dead but the stamp lied - cost ~30 min of waiting.
- **c6 fixed it:** Added proof-of-life check. "Woken" is now truthful; "queued" means the session is idle/closed and needs manual revival (Max opening the chat window, or a RemoteTrigger spawn).
- **Listener-free alternative:** `RemoteTrigger` (`run`/`create` actions) spawns fresh remote agents server-side - no armed listener required. Max confirmed this is the right mechanism for dead sessions.
- **Logged** to `C:\claude_base\rule_inconsistencies_tomemex.md`.

---

## CURRENT STATE

### Running autonomously
- **ASR on Sol:** 52+/93 transcripts done, CPU-bound grinding overnight, b7nonhtimes drains batches ? seg ? identify. Resumable, no deadline risk.
- **b9:** Full 2,842-video Tamza backup continuing on its own. All 93 priority (caption-disabled) done. 0 walls all night.

### Awaiting Max's "go"
- **Free 899-song recovery:** Staged by b15merger. A republish recovers 899 songs' real end-times (they have seg_end in the remap store but the live catalog is stale). 0 changed rows, 0 lost, reversible with backup + byte-verify. **Say "go" and it deploys - lifts the 2-min cap on those 899 immediately.**
- **b27's v03 poem-tuned pilot:** Building. Once ready, I hand-QC it ? approve cheap DS4 scale.
- **The 7 ready missing-transcript videos:** Staged for teal16 ASR to get end-times.
- **Archive cleanup merge:** b27's branch ready; awaiting owner sign-offs (b15M for the `_batch_aligner` conflict).

### In flight / delegated
- **b27:** Building v03 first-line pilot (poem-tuning). Has a 4-min self-wake armed.
- **b15merger:** Gate ready (titles-free, consumes verified first-lines). Holding on the 899-recovery deploy for Max's "go."
- **b7nonhtimes:** ASR?seg?identify chain running on Sol. Also tasked with folding incomplete HUM vids into NONH for timing.
- **B30:** Assigned generic timing of all ~4,232 untimed rows (via teal16 ASR, not YouTube). Broke the problem into 3 buckets (see above).

### Blocked / parked for Max's AM
- **NONH live publish:** Parked because b15merger went silent overnight (timer disarmed per "idle sessions disarm" order). Now live again after Max woke it, but publish content still gated on b27's verified first-lines.
- **b7i (live catalog updates):** Session dead, no armed listener. Can be revived by Max opening the chat window or by RemoteTrigger spawn.
- **61-video transcript timing:** Can start in parallel with backup (7 ready now, rest as backup downloads). No YouTube block concern.

### Enshrined / documented
- **7 cardinal rules** in START-HERE handover (B25handoverer pushed v03 with all additions).
- **Opus API prohibition** in `global2.md`.
- **Titles-free gate** in b15merger's split.
- **Handover tool** (`nonh_handover.py`) titles-free + multi-pass QA'd.

---

## EXACT NEXT STEP

1. **Max says "go" on the 899-song republish** ? b15merger deploys (backup + byte-verify + push). Immediate radio improvement, zero risk.
2. **I hand-QC b27's v03 poem-tuned pilot** when it lands ? approve or send back for redo.
3. **Start ASR on the 7 ready missing-transcript videos** (teal16) ? timing ? end-times.
4. **Once first-lines are verified** (b27 pilot ? my QC ? full DS4 run ? my QC on output), b15merger publishes recognized NONH performances through the titles-free gate.
5. **Max wakes b7i** (open chat window) or I spawn a RemoteTrigger agent if needed for live catalog updates after the 899 republish.
6. **Archive cleanup:** Needs Max's AM sign-off (or b15M resolving the `_batch_aligner` conflict) before merge.

---

## OPEN QUESTIONS FOR MAX

1. **"Go" on the free 899-song republish?** (Zero risk, zero spend, purely additive, lifts 2-min cap on 899 songs now.)
2. **Wake b7i yourself** (open chat window and type "go"), or should I spawn a fresh RemoteTrigger agent for the live catalog updates? (Small cost if RemoteTrigger.)
3. **Archive cleanup merge:** OK to proceed once b15M signs off, or hold for your direct sign-off?
4. **Budget confirmation:** The $3/$12 caps for DS4 pilots/full run - these are your go-ahead, I'll show actual cost on the pilot before any full spend. Confirm?

---

## KEY PATHS, FILES, IDs

### Tools
- **Handover tool:** `C:\claude_base\tools\tamza_songs\pipeline\timecoder_handover\nonh_handover.py`
- **Publisher:** `C:\claude_base\tools\tamza_songs\pipeline\scripts\publish_catalog.py` (gated, reversible, `--dry-run` mode)
- **Branch bulletin board:** `python C:/claude_base/branch_bulletin/bcast.py [read|post|catchup|wake --name <id>]`
- **Worklog:** `python C:/claude_base/compaction_kb/scripts/worklog.py log "<msg>"`

### Key data files
- **Catalog:** `C:\claude_base\tools\tamza_songs\pipeline\output\data.json` (26,283 rows)
- **Channel inventory (with upload dates):** `C:\claude_base\tools\tamza_songs\output\channel_inventory.json`
- **NONH drafts:** `song_timing/from_scratch_idx/_work/annotator/drafts_nonh_v01/`
- **ASR transcripts (Sol):** `~/nonh_transcribe/out/*.json` (on 192.168.1.113)
- **ASR ready list:** `song_timing/_work/nonh_asr_ready_on_teal16.txt` (82 IDs) + `nonh_asr_still_need.txt` (11 - now 0, all pulled)
- **Caption-disabled IDs:** `song_timing/_work/nonh_caption_disabled_ids.txt` (93 IDs)
- **Human Excel:** `C:\Users\maxre\Downloads\????? ?? ?????.xlsx`
- **Verified first-lines (pilot):** `timecoder_handover/verified_first_lines_pX_1m8DlMbA.json`
- **QC verdicts:** `timecoder_handover/qc/pX_1m8D
