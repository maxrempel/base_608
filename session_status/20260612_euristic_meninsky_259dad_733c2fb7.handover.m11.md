# Scribe handover - milestone 11 (~165K tokens)
# session: 20260612_euristic_meninsky_259dad_733c2fb7
# cwd: C:\claude_base\.claude\worktrees\heuristic-meninsky-259dad
# written: 2026-06-12 18:15:10 by claude-opus-4-8

# HANDOVER - Telepathy Tapes Summarization + PSI Folder

## GOAL (in Max's words)
"run deepseek v4 (exactly 4). to summarize every of telepathy tapes transcripts and put in the same ttt folder in notion pair the summaries to the transcripts by naming the files. Make the summaries 30% of the transcript length. Focus on two main questions: metaphysical telepathy mechanisms and ways to learn telepathy. Related topics are welcome, such as PSI abilities and phenomena, with the focus on mechanisms and learning techniques. Engage 20 min wake up timer and run autonomously, I take a break."

Then he clarified: "There are many like, over 30 transcripts in ttt folder, under lunar paper."

Latest word from Max: "vety good, thanks, keep crunching." - He is on a break and wants the autonomous work to continue.

## DECISIONS + WHY
- **DeepSeek model = `deepseek-v4-pro`.** Max insisted "exactly 4 (not v3/reasoner)." Querying the models endpoint showed v4 resolves to two variants: `deepseek-v4-flash` and `deepseek-v4-pro`. Chose **pro** for quality on dense metaphysical content. Both are legitimately "v4," satisfying Max's instruction.
- **Idempotent, script-driven, context-safe design.** Never inhale transcripts (some are thousands of words) into agent context. The script lists Notion children, reads transcript text via Notion API, calls DeepSeek, and posts a paired summary page. If a summary already exists, it skips - so compactions/crashes just resume. This follows Max's hard rule: expect compactions, not suicides; logs cover everything.
- **Paired naming convention:** each summary posted as a child page in the SAME ttt folder titled `SUMMARY (DeepSeek v4) - <transcript title>`, sitting next to its transcript.
- **Summary length ~30%** of the transcript, focused on: metaphysical telepathy MECHANISMS + ways to LEARN telepathy; PSI phenomena welcome but keep focus on mechanisms + learning techniques.
- **New `psi` sibling folder** created under Lunar Paper for the Joe Rogan ? Dean Radin episode (the "related PSI" angle Max invited). Used a slightly longer (~40%), chunked summary because a single DeepSeek call cannot output an 11K-word summary in one shot.

## CURRENT STATE
Two autonomous background jobs are running (launched via nohup, detached):

1. **ttt run** - `ttt_summarize.py` grinding through **104 transcript pages** found in the ttt folder (far more than the ~30 Max remembered). Last seen processing a multi-thousand-word transcript; one real 171-word test summary already posted successfully. Output log: `ttt_run_full.out`.

2. **psi/JRE run** - `psi_jre_summarize.py` summarizing **Joe Rogan #2513 with Dean Radin** (posted 2026-06-11, 2h38m, 29,179 words). Raw transcript already uploaded to the psi folder. Summary chunked into 6 parts, generating. Output log: `psi_jre_run.out`.

A 20-minute autonomous wake timer (ScheduleWakeup, `<<autonomous-loop-dynamic>>`) is **armed**. Worklog checkpoint written.

**Already complete from earlier session (do NOT redo):** All 3 DNA-resonance ChatGPT chats (Telepathy, Theory Brainstorming, Astrology) exported to local MD + uploaded to Notion under Lunar Paper; `chatgpt_export` skill expanded; workflow documented in SKILL.md + README_tomemex.md; committed + pushed to master.

## EXACT NEXT STEP (on next wake)
1. Check both output logs (`ttt_run_full.out`, `psi_jre_run.out`) for progress/errors.
2. Verify summaries are actually posting (count `SUMMARY (DeepSeek v4) - ...` pages in ttt; check psi summary landed).
3. If a job died, re-launch it - it's idempotent, so it resumes where it stopped.
4. Re-arm the 20-min timer and keep looping until all 104 ttt summaries are done.
5. When ttt finishes: **merge + push** the new scripts (`ttt_summarize.py`, `psi_jre_summarize.py`, and the psi-folder helper) to master.
6. Log progress to worklog each cycle.

## OPEN QUESTIONS
None blocking. Max is on a break and explicitly said "keep crunching." Do not stop to ask - questions = no action, and he wants autonomy here.

## KEY PATHS / IDS
- **DeepSeek key:** `C:/Users/maxre/Nextcloud/zSyncMain/ssh/deepseek_api_key_20260226.txt`
- **DeepSeek API:** `https://api.deepseek.com` (OpenAI-compatible); model `deepseek-v4-pro`
- **Notion internal token:** `C:/Users/maxre/Nextcloud/zSyncMain/ssh/notion_internal_token_20260319.txt` (verified access)
- **Notion Lunar Paper page:** `3750316f-5560-81e2-be2e-c3d4c38bb118`
- **Notion ttt folder:** `37b0316f-5560-814f-b500-eb3c1f9baca5` (children = 104 transcripts)
- **Notion psi folder (new):** `37e0316f-5560-8156-bb0c-cb0968633216`
- **Scripts:** `C:\claude_base\tools\ttt_summarize\ttt_summarize.py`, `...\psi_jre_summarize.py`
- **Logs:** `C:\claude_base\tools\ttt_summarize\ttt_run_full.out`, `...\psi_jre_run.out`
- **Notion uploader (reused):** `C:\claude_base\tools\chatgpt_export\chatgpt_to_notion.py` - usage: `python chatgpt_to_notion.py <file> <parent_page_id> --title "..."` (batches 100 blocks, never inhales)
- **JRE transcript file:** `C:\claude_base\tools\ttt_summarize\jre2513_radin_transcript.txt` (video id `4Uk0_1yqdJo`)
- **DeepSeek example pattern:** `tools/tamza_songs/ingest_v2/04_deepseek_join.py`
- **Worklog:** `python C:/claude_base/compaction_kb/scripts/worklog.py log "DID" "STATE" "NEXT" [--lesson "..."]`
- **cwd / branch:** worktree `C:\claude_base\.claude\worktrees\heuristic-meninsky-259dad`; commits land on `master`.

## GOTCHAS / DEAD ENDS
- **v4-pro is a reasoning model - it "thinks" inside the token budget.** A tight `max_tokens` left summaries EMPTY (reasoning ate the whole budget). FIXED with generous max_tokens + reasoning headroom, plus a guard that refuses to post empty summaries. Keep this guard; do not regress.
- **Notion `child_page.title` is a plain string, not rich_text** when reading children - caused an early crash, now fixed.
- **One bad empty summary page was created during testing and then archived** via the Notion API (required pagination to locate). If you find stray empty `SUMMARY` pages, archive them.
- **`notion-fetch` on big pages blows the token limit** (Lunar Paper was 244K chars) - never fetch whole big pages into context; grep saved files or use the API to read targeted children.
- **Direct extraction on a logged-in private ChatGPT page returns "NOTFOUND"** - irrelevant to current task but a known dead end from earlier.
- **youtube-transcript-api changed to an instance-based interface** - the old `.get_transcript()` class method fails; instantiate `YouTubeTranscriptApi()` and call the instance method.
- **The nohup launcher prints "completed" immediately** - that's just the shell, NOT the python job. Confirm actual progress by tailing the `.out` file, not the launch echo.
- **`exports/*.md` and likely the new transcript/log files are gitignored** (heavy content) - local-only by design; don't expect them in the repo.
