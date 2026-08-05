# Scribe handover - milestone 2 (~175K tokens)
# session: 20260718_nice_khorana_6f04b4_2eb1eb83
# cwd: C:\claude_base\.claude\worktrees\nice-khorana-6f04b4
# written: 2026-07-18 16:12:27 by deepseek-v4-pro

# SESSION HANDOVER - Max's Noeticus TTS + YT Summary Recovery

## GOAL (in Max's own words)
- Add spoken (TTS) voice to the Noeticus usage digest that gets sent to his Telegram.
- Build an on-demand Telegram bot so Max can type `questions` to get the last 60 visitor questions verbatim, then `elaborate N` to expand some, all with text + voice.
- After the above, pivot: DeepSeek ran out of money yesterday, causing many YouTube summaries to error. Find and remake those failed summaries. Today's are fine; the ones from yesterday need to be regenerated.

## DECISIONS MADE + WHY

### Noeticus Digest TTS
- **TTS via OpenAI** because the OpenAI key already existed on Dax and OpenAI's API can output Ogg/Opus directly (no ffmpeg needed).
- Voice added to the every?other?day digest (`noeticus_usage_report.py`) - numbers and "what people asked about" spoken alongside the text.
- A retry loop added to the voice?send function after a transient SSL EOF on the first live test.

### Noeticus Question Bot
- **Interface**: Max types keywords (`questions`, `elaborate 14`) into his existing critical?alarms Telegram bot. No separate bot needed.
- **No reply?to required** - a plain keyword receiver was simpler and sufficient for the "on?demand dump + elaborate" workflow.
- **60 questions chosen** as a reasonable default; can be adjusted later.
- **`elaborate` uses DeepSeek** (via API call) because that's what Noeticus already uses to talk to the AI. **This path is ready but untested because the DeepSeek balance on Dax was empty** at the time the bot was built. Max indicated it would be topped up soon.

### YT Summary Recovery
- **Pipeline**: YouTube transcript is cached first, then DeepSeek generates three summaries (short, deep?dive, follow?up), then FishAudio turns them into voice messages that are posted to Telegram. The failure point was **only the DeepSeek step** - transcripts were cached fine.
- **Recovery strategy**: Re?run the exact live pipeline function (`_summarize_and_push_audio`) on each failed video, feeding in the cached transcript (no YouTube refetch). This avoids any duplication or re?invention of the pipeline logic.
- **Reprocess script** written and launched in background on Lak with its own log file to avoid interfering with the live service.

## CURRENT STATE

### ? Completed & verified
- Noeticus digest now sends a **voice message** (OpenAI TTS) immediately after the text message. Deployed on Dax, committed, and pushed to the repo.
- Noeticus question bot built, deployed on Dax as an **always?on systemd service** (`noeticus?qbot`). The `questions` command works (gets last 60 verbatim, text + voice). The `elaborate` command is coded but **not yet tested** because it needs a DeepSeek balance on Dax - that balances is still TBD.
- Both scripts are in the repo's `tools/noeticus_usage_report/` folder and safely committed.

### ? In flight
- **Reprocessing yesterday's 9 failed YT summaries** on Lak. A reprocess script is running in the background (`nohup`) with its own log.  
  - **DeepSeek balance on Lak is restored ($19.16)** - the summariser should now succeed.  
  - **FishAudio balance is OK**, so TTS generation should work too.  
  - **First few videos** have already generated audio and posted to Telegram, as confirmed by a live check after ~45s.  
  - The script is still running; we do not yet have confirmation that all 9 are done.

The 9 video titles (as extracted from the log) are:
1. Missing scientists mystery  
2. Rep. Eric Burlison remarks  
3. Jesse Michels/Flying...  
4. BASHAR open contact  
5. UAP debate change  
6. Grok decodes crow sounds  
7. ?????? ??????? ????  
8. Ancestral Healing E11  
9. James Fox/Grusch leak

The exact YouTube IDs are recorded in the reprocess log (`/home/mrempadmin/00HA1py/out/reprocess_failed_summaries_20260718.log`).

## EXACT NEXT STEP

1. **On Lak** (SSH as `mrempadmin` on `100.110.225.89` using `~/.ssh/lakarian_key.pem`), read the reprocess log:  
   `cat /home/mrempadmin/00HA1py/out/reprocess_failed_summaries_20260718.log`  
2. Verify that all 9 entries show `DONE` (or equivalent success marker) and that audio files were posted.
3. If any are still marked ERROR (not due to balance), investigate and retry individually using the same pipeline call.
4. Once all 9 are confirmed complete, **report back to Max** - list the titles and confirm they arrived on Telegram.
5. (Optional but useful) Check the log for the exact video IDs if any need manual re?run.

## OPEN QUESTIONS FOR MAX

- **Is the DeepSeek balance on Dax** (needed for the Noeticus `elaborate` feature) now topped up? If so, test `elaborate` once Max is ready.
- The earlier digest's "what people asked about" section was blank because of the same DeepSeek outage - does that need a retroactive fill, or is it fine since future digests will work once the balance is back?

## KEY FILE PATHS & IDS

| What | Where |
|------|-------|
| **Noeticus digest script** | `C:\claude_base\tools\noeticus_usage_report\noeticus_usage_report.py` |
| **Noeticus question bot** | `C:\claude_base\tools\noeticus_usage_report\noeticus_question_bot.py` |
| **Dax (critical?alarms server)** | `bitnami@35.80.203.42` - SSH key `~/Nextcloud/zSyncMain/ssh/dax_lightsail_max_id_rsa.pem` |
| **Dax bot?related paths** | `/home/bitnami/noeticus/` (reports, TTS output, etc.) |
| **Lak (YT transcript server)** | `mrempadmin@100.110.225.89` - key `~/.ssh/lakarian_key.pem` |
| **YT transcript app** | `/home/mrempadmin/00HA1py/scripts/yt_transcript_app.py` |
| **Transcript cache** | `/home/mrempadmin/00HA1py/cache/` (contains `jobs.json`, `transcripts/`, etc.) |
| **YT pipeline log** | `/home/mrempadmin/00HA1py/out/yt_transcript_app.log` |
| **Reprocess script (temp)** | `/home/mrempadmin/00HA1py/scripts/reprocess_failed_summaries_20260718.py` |
| **Reprocess log** | `/home/mrempadmin/00HA1py/out/reprocess_failed_summaries_20260718.log` |
| **DeepSeek key (Lak)** | first line of `/home/mrempadmin/00HA1py/config/deepseek.key` |
| **FishAudio key (Lak)** | (likely in config, used by the pipeline) |
| **Noeticus qbot systemd unit** | `/etc/systemd/system/noeticus?qbot.service` on Dax |
| **Repo commits** | both scripts committed to `origin/devel` (or main) under `tools/noeticus_usage_report/` |

## GOTCHAS & DEAD ENDS RULED OUT

- **Do not try to refetch YouTube transcripts** for the 9 failed videos - the transcripts are already cached valid. Only the summary step needs re?running.
- The **DeepSeek "Insufficient Balance"** error was on Lak; the key now shows $19.16, so the error should be gone. Do not rotate keys or change model.
- **FishAudio was not the problem** - the failures were entirely on DeepSeek.
- The `clipfisher_monitor.log` is polluted with SOL?DOWN spam; for YT?level errors always look in `out/yt_transcript_app.log`.
- The Noeticus elaborate command will produce text+voice **using the same TTS pattern** as the digest (OpenAI voice, not FishAudio). That's done; just needs the DeepSeek key on Dax to be live.
- The background reprocess script was launched with `nohup` and redirects output to its own log. It's safe to check while still running.
- No existing services were stopped or reconfigured; both Dax and Lak are running normally.

---

**This handover provides everything a cold session needs to resume: verify Lak reprocess log, confirm all 9 done, update Max, and optionally test the Noeticus elaborate command once DeepSeek on Dax is restored.**
