# Scribe handover - milestone 3 (~294K tokens)
# session: 20260715_fervent_gagarin_9d3b2f_a64f4c85
# cwd: C:\claude_base\.claude\worktrees\fervent-gagarin-9d3b2f
# written: 2026-07-15 09:37:47 by deepseek-v4-pro

# HANDOVER - Anna Avatar Commentary for UEI Talk

## GOAL (in Max's words)
Create a wrapper for the published UEI talk video: a computer-generated AI avatar named **Anna** who gives a spoken **intro**, a short **intermission** between each chapter (summarizing what Max just said and introducing the next topic - NO questions, just introduce), and a **conclusion**. Her "I am an AI" self-introduction must land at the **end** as a reveal. The finished script should also be turned into **audio files**, split into **?15-second chunks** (optimal 10-15s) because the video maker can only accept clips up to 15 seconds.

The audience is three groups: **starseeds**, **experiencers/ufologists**, and **scientists open to alien genetics**. Anna must speak from inside the worldview with conviction, not from a skeptical outside frame.

---

## DECISIONS + WHY

1. **Anna's AI reveal moved to the end**: Max explicitly asked for this - "Hello I am Anna, I am an AI..." opens v01/v02 but in v03 it lands at the close, tying into Max's theme that AI will be a vehicle for disclosure. Works much better as a punctuation mark than a greeting.

2. **v03 is the final script version**: Went through three rounds. v01 was a first draft. v02 added audience-tuning and moved the AI reveal. v03 deepened research (STARSEEDS chapter, Noeticus digest, DNA-resonance angle) and dropped the faint skeptical hedging - Anna now speaks *from inside* the worldview, not holding it at arm's length. The three audiences are addressed as allies, not doubters to be persuaded.

3. **"the man" killed per Max's feedback**: He hated it, called it "too sexualized." Changed in v03.

4. **MOMA Fish Audio, not ElevenLabs**: MOMA already has an ANNA voice clone (#22) using Fish Audio model s2-pro. Same pipeline already in use for other projects - no reason to route around it.

5. **Pilot-first then build**: Ran a 3-sentence pilot (`anna_tts_pilot.py`) to measure speaking rate (~17 chars/sec) and generation speed (~2s per call) before designing the chunker. This means 15s ? ~255 chars; targeting ~210 chars (~12s) gives a safe margin.

6. **Post-generation verification planned**: The build script was designed to generate all clips, then measure *actual* durations with `wave` and auto-resplit anything over 15s. The real duration check is the safety net, not a character-count heuristic.

7. **YouTube upload required manual drag**: The Chrome extension's file_upload is sandboxed to session-shared files only - it wouldn't accept files from the Videos folder, the scratchpad, or the ccd_directory grant. The native OS file dialog is Chrome-owned and the desktop-control tool is read-tier on browsers. The 682 MB video file had to be dragged in by Max manually. This is a hard wall if future uploads are needed.

---

## CURRENT STATE

### COMPLETED
- **Video download**: 1080p from YouTube, ~1.3 GB, in `Videos/yt/`
- **Talk cut & cleaned**: v03 final clip, 16:15, 1080p, in `C:\Users\maxre\Videos\max talks\uei_max_talk_20260711\Max Rempel talk UEI launch 20260711 v03_clean.mp4`
  - Intro starts exactly at host's "...a unique scientific perspective to the conversation around contact in human DNA and alien DNA - quite possibly inside of our genome. Thank you so much, Max. Welcome in."
  - Outro ends after host's "Thank you so much, Max, that was amazing as always"
  - 11 long pauses shortened to ~0.6s each (~26s dead air removed)
- **Published to Hucolo TV** (unlisted): https://youtu.be/jyMh4KBv-RU
  - Title: "Alien DNA, Telepathy & the Coming Contact by Max Rempel PhD - July 11, 2026"
  - Description with 17 chapter timestamps in place
  - Channel confirmed: HUCOLO TV (UCj5wGWloHE8hKHPd5kqWsJQ, 6,110 subscribers)
- **Anna commentary script v03**: `anna_commentary_v03.md` in the same folder. Contains 1 intro, ~16 intermissions (one between each content chapter), 1 conclusion. Anna's "I am an AI" reveal at the end.
- **Transcript & chapter map**: `deepgram_nova3.json`, `deepgram_nova3_indexed.txt`, `chapters_v01.py` all in the work folder.
- **B70b branch checked in**: This session registered as branch B70b (Anna script focus).

### IN FLIGHT / STOPPED
- **Anna audio generation**: The background task (`bj9x76erx`, running `anna_tts_build.py`) was **stopped** - no completion record. The output file at the session's temp path may have partial results or nothing at all. It was supposed to:
  1. Parse `anna_commentary_v03.md` into ~35 spoken blocks
  2. Chunk each block into ?15s pieces (targeting ~12s)
  3. Call Fish Audio API (voice ANNA, clone #22, model s2-pro) for each chunk
  4. Save WAV files to an `anna_audio/` subfolder
  5. Measure actual durations and auto-resplit anything over 15s
  6. Produce a manifest

  The output file path from the task notification is:
  `C:\Users\maxre\AppData\Local\Temp\claude\C--claude-base--claude-worktrees-awesome-archimedes-f6a2aa\be1f264a-aebb-4738-9304-57ad19af0cab\tasks\bj9x76erx.output`

  **This output file must be checked first** - it may contain partial generated audio, error messages, or nothing at all. The build script itself lives at `C:\Users\maxre\Videos\max talks\uei_max_talk_20260711\anna_tts_build.py` and the pilot at `anna_tts_pilot.py`.

---

## EXACT NEXT STEP

1. **Check the stopped task output**: Read `bj9x76erx.output` from the temp path above. See if any WAV files were generated, and if any errors killed it.

2. **Check for partial audio**: Look for an `anna_audio/` folder in `C:\Users\maxre\Videos\max talks\uei_max_talk_20260711\`. If files exist, list them and check if the generation completed or was mid-stream.

3. **Resume or restart the build**:
   - If the script crashed on an API error or network issue, fix and re-run `anna_tts_build.py`.
   - If it was killed mid-stream, re-run it - the script should be idempotent enough to skip already-generated clips, but verify that logic.
   - If no audio was generated at all, just run it fresh.

4. **Post-generation**: Once all clips exist, verify every file is ?15.0 seconds. Anything over needs re-splitting.

5. **Next after audio**: Feed the audio clips + script into the video avatar maker (not yet discussed - Max will likely specify which tool).

---

## OPEN QUESTIONS (awaiting Max)

- **None raised yet about the script content** - v03 is presumably accepted unless Max reads it and flags changes. He started reading it, hated "the man" (fixed), but hasn't confirmed the rest.
- **Video avatar maker**: Not specified yet. Max mentioned "the video maker takes only up to 15 seconds" - which tool is this? May need investigation.
- **Should the avatar video segments be assembled into a full wrapper video**, or just delivered as standalone clips for Max to drop into an editor? Not discussed.

---

## KEY PATHS / IDs

| What | Path/ID |
|---|---|
| Work folder | `C:\Users\maxre\Videos\max talks\uei_max_talk_20260711\` |
| Final cleaned talk | `Max Rempel talk UEI launch 20260711 v03_clean.mp4` (16:15, 1080p) |
| Deepgram transcript | `deepgram_nova3.json` / `deepgram_nova3_indexed.txt` |
| Chapter map script | `chapters_v01.py` |
| Assemble/cut script | `assemble_v01.py` |
| Anna final script | `anna_commentary_v03.md` |
| Anna audio build | `anna_tts_build.py` |
| Anna audio pilot | `anna_tts_pilot.py` |
| Published video | `https://youtu.be/jyMh4KBv-RU` (unlisted, Hucolo TV) |
| YouTube channel | HUCOLO TV, UCj5wGWloHE8hKHPd5kqWsJQ |
| MOMA Anna voice | clone #22, Fish Audio, model s2-pro |
| MOMA sound assembly | `C:\moma\sc10\sound_assembly\code\sass.py` |
| MOMA voice config | `C:\moma\sc10\sound_assembly\code\config\voices.json` |
| Fish Audio key file | Via `SSH_FOLDER`/`fish_key.txt` (sass.py config) |
| Stopped task output | `C:\Users\maxre\AppData\Local\Temp\claude\C--claude-base--claude-worktrees-awesome-archimedes-f6a2aa\be1f264a-aebb-4738-9304-57ad19af0cab\tasks\bj9x76erx.output` |
| Branch bulletin | B70b (Anna script branch) |
| Session transcript (full) | `C:\Users\maxre\.claude\projects\C--claude-base--claude-worktrees-nice-khorana-6f04b4\faa85602-dd73-4efb-9a6b-5f89960232eb.jsonl` |
| Memex (Max's materials) | Searched for alien/hybridization/starseed/pleiadian content |
| Notion presentation script | id `39a0316f-5560-8108-ba46-fd875c0f6236` (Max's cheat sheet for THIS talk) |

---

## GOTCHAS

1. **YouTube upload is manual-only for large files**: The Chrome extension's file_upload sandbox blocks everything except session-shared files. The OS file dialog is Chrome-owned and the desktop-control tool can't type into it (read-tier on browsers). For any future upload to Hucolo TV, the 682 MB file **must** be dragged in by Max. Don't waste turns fishing for programmatic workarounds.

2. **ffmpeg filtergraph needs semicolons**: When building the concat filter, segments joined with empty strings fail with "trailing garbage." Must use `";".join(parts)`.

3. **No choice lists**: Max prohibits AskUserQuestion-style cards. Ask open questions, never present numbered options.

4. **Speaking rate is ~17 chars/sec for Anna's Fish Audio voice** - build the chunker around that. Any re-chunking attempts should re-measure.

5. **The script "the man" is a banned phrase** - Max found it sexualized. Don't use it in any Anna script revisions.

6. **Worktree may differ from cwd**: The session was in a worktree (`fervent-gagarin-9d3b2f`) but the task output references a different one (`awesome-archimedes-f6a2aa`). Paths to temp files may need cross-worktree navigation.

7. **B70b is the branch identity for this task** - check in if continuing. Other branches (Tamza, typer, sibling genomics) are irrelevant noise to this task.
