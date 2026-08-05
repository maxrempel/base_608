# Scribe handover - milestone 4 (~306K tokens)
# session: 20260715_wesome_archimedes_f6a2aa_be1f264a
# cwd: C:\claude_base\.claude\worktrees\awesome-archimedes-f6a2aa
# written: 2026-07-15 10:50:37 by deepseek-v4-pro

# HANDOVER - Anna Avatar Commentary for Max's UEI Talk

**Branch:** D42B  
**Session:** Opus 4.8, Claude Code on Pine (~306K tokens, 233 turns)  
**Date:** 2026-07-14

---

## GOAL (in Max's words)

Build a computer-generated AI avatar named **Anna** who wraps Max's published UEI talk. She gives a **spoken intro**, a short **intermission between each chapter** (summarizes what Max just said + introduces the next topic - NO questions, just introduction), and a **conclusion**. Eventually this becomes an actual avatar video. The commentary is for the **Human Colony YouTube channel** (not Hucolo TV - that's where the raw talk lives).

Core constraints:
- **No lies.** Anna must never claim Max presents "evidence" or "proof" - he doesn't.
- **No overpromises.** Only thing Max offers: free DNA analysis, findings returned. Nothing else.
- **Story-first, not advertising.** Not about how great Max is. About the investigation.
- **Non-pushy, non-intrusive tone.** Light, curious, warm. Not ominous.
- **No hedging.** No defensive "this is not science fiction" - that was a Claude meta-instruction mistakenly put in Anna's mouth. Never reference the mainstream to defend the topic.

---

## DECISIONS + WHY

1. **Published raw talk on Hucolo TV as UNLISTED** (not Public) - so Max can review before flipping. Link: `youtu.be/jyMh4KBv-RU`. Title includes date: "Alien DNA, Telepathy & the Coming Contact by Max Rempel PhD - July 11, 2026." Description has 17 timestamped chapters.

2. **Used MOMA's existing "Anna" Fish Audio voice clone (#22, model s2-pro)** - it was already set up and named Anna, matching the avatar's name perfectly. Speaking rate: ~17 chars/sec. Each generation call takes ~2s.

3. **Chunked audio into ?15s pieces** because the video maker won't accept longer clips. Target ~10-15s. A tail-merge step prevents orphan 1-second fragments. Final v04 run: 55 clips, 3.4-13.8s range, avg 9.0s. v05 will produce similar.

4. **QC via assembled audio podcast** rather than jumping straight to avatar video. Max wanted to hear the whole thing interleaved (Anna + his talk) before committing. Published at `maxrempel.com/temp2` - a Cloudflare Worker route serving from R2 bucket `maxrempel-papers`, with an HTML player page that has clickable chapter cues.

5. **Anna's AI self-introduction moved to the end** (Max's request). She reveals she's an AI in a single light line at the very close, not up front.

6. **Fish bracket cues for tone** - `[warm]`, `[curious]`, `[bright]` - confirmed from MOMA's `sass_short_rich_tags.py` that Fish reads these as delivery direction, not spoken words.

7. **First voice is Nadalee (host), not Max.** Fixed label in podcast cuesheet. Anna now hands to "Nadalee, the host" rather than "here is Max."

8. **YouTube upload used Max's real logged-in Chrome** via claude-in-chrome MCP. Playwright couldn't work because it has its own Chromium instance (no Google login). File upload was the bottleneck - claude-in-chrome's sandbox only accepts files shared through its own mechanism, and the OS file dialog is Chrome-owned. Resolved by having Max drag the file in manually.

---

## CURRENT STATE

**The podcast is being rebuilt RIGHT NOW** with the two latest fixes:

- ? ~~"the evidence begins here"~~ - removed. Lie. Max presents no evidence.
- ? ~~"This is not science fiction"~~ - removed. Defensive hedging, Claude's meta-instruction mistakenly spoken aloud.
- Script being used: `anna_commentary_v05.md` (most recent edit with both fixes applied)

The build chain runs: regenerate 55 Anna audio clips ? loudness-match ? reassemble podcast ? re-upload to R2. The chain was kicked off at the very end of the session. When complete, the result will be live at **`maxrempel.com/temp2`** (just needs a browser refresh).

**Script revision history in the folder:**
- v01 ? v02: moved AI reveal to end, tuned for 3 audiences
- v03: deeper Memex research, more conviction for starseed audience
- v04: no "room" (it's a YouTube recording), minimized AI self-consciousness, "the man" ? "the scientist"  
- v05: stripped overpromises, de-advertised Max, lighter tone via bracket cues, Nadalee fix, non-fiction framing
- Latest v05 edit: removed "evidence" lie + "not science fiction" hedge

**What the listener hears at maxrempel.com/temp2 (once live):**
- Anna intro ? Nadalee's introduction of Max ? Max's talk chapter 1 ? Anna intermission 1 ? Max chapter 2 ? ... ? Anna intermission 16 ? Max chapter 17 ? Anna conclusion
- ~22-23 minutes total, 42 Anna clips
- Clickable time markers on the page (blue = Anna, green = Max)
- Properly loudness-matched (-16 LUFS), short silence breaks between pieces

---

## EXACT NEXT STEP

1. **Confirm the latest build completed.** Check the background task output at the temp path pattern: `C:\Users\maxre\AppData\Local\Temp\claude\C--claude-base--claude-worktrees-awesome-archimedes-f6a2aa\be1f264a-aebb-4738-9304-57ad19af0cab\tasks\` - look for the most recent `.output` file. Verify it says exit code 0 and that the cue sheet timestamps look right (first speaker = Nadalee at ~0:48).

2. **Verify it's live.** Curl `https://maxrempel.com/temp2` and confirm the page loads. Do a byte-size check against the local mp3: `C:\Users\maxre\Videos\max talks\uei_max_talk_20260711\anna_uei_podcast_QC_v01.mp3`. If sizes match, it's the fresh version.

3. **Tell Max it's ready to review at maxrempel.com/temp2.** He needs to listen and approve the tone + content before proceeding.

4. **After Max approves the audio:** feed the 55 approved Anna clips + manifest to the avatar/video maker to produce the actual talking-avatar wrapper video. The clips are already ?15s, the manifest maps each to its chapter, and the v03_clean.mp4 talk video has matching chapter timestamps.

---

## OPEN QUESTIONS

- **Is the latest rebuild actually live and correct?** The session ended mid-rebuild. Need to check.
- **Does Max approve the v05 tone?** He said v05 was "substantially better" but then flagged two more issues (evidence claim, hedging) which are now fixed. He hasn't heard this final version.
- **Which avatar/video maker tool to use?** Not yet decided - the audio pipeline is proven, the video step is next.
- **Is the Fish Audio "Anna" voice the final voice?** Max said "acceptable" - not a strong yes. He might want it swapped later.

---

## KEY PATHS & IDs

| Thing | Path/Value |
|---|---|
| **Work folder** | `C:\Users\maxre\Videos\max talks\uei_max_talk_20260711\` |
| **Anna script (final)** | `anna_commentary_v05.md` |
| **Anna audio clips** | `anna_audio\` (55 WAVs + manifest.tsv + manifest.json) |
| **Build script** | `anna_tts_build.py` - parses v05, chunks ?15s, synths via Fish Audio, auto-verifies durations |
| **Podcast assembly** | `assemble_podcast_v01.py` - slices talk audio at chapter boundaries, interleaves Anna clips, loudness-matches, outputs mp3 |
| **Publishing** | `publish_temp2.py` - uploads mp3 + player HTML to R2 bucket `maxrempel-papers` |
| **QC podcast (local)** | `anna_uei_podcast_QC_v01.mp3` + `_cuesheet.txt` |
| **Raw talk video** | `Max Rempel talk UEI launch 20260711 v03_clean.mp4` (16:15, 1080p) |
| **Chapter timings** | `chapters_v01.py` - maps transcript word times to published v03 timeline |
| **17 chapters** | `deepgram_nova3_indexed.txt` and `deepgram_nova3.json` |
| **YouTube link** | `youtu.be/jyMh4KBv-RU` (UNLISTED, Hucolo TV channel UCj5wGWloHE8hKHPd5kqWsJQ) |
| **QC player page** | `https://maxrempel.com/temp2` |
| **Site source** | `C:\claude_base\sites\maxrempel-site\` (Cloudflare Worker, deploy via `deploy.sh`) |
| **R2 bucket** | `maxrempel-papers` (creds in `press_photos/make_press_photo.py` line 19) |
| **MOMA Anna voice** | Fish Audio clone #22, ID `da5554ea...`, model `s2-pro` |
| **Fish API key** | `zSyncMain\ssh\fishaudio_api_key_20260226.txt` |
| **MOMA voice config** | `C:\moma\sc10\sound_assembly\code\config\voices.json` |
| **MOMA synth** | `C:\moma\sc10\sound_assembly\code\sass.py` |
| **MOMA tags** | `sass_short_rich_tags.py` - confirms `[warm]`, `[curious]` syntax |

---

## GOTCHAS

- **Never put instructions to Claude into Anna's mouth.** When Max says "don't do X, do Y," that's for you, not a line for Anna. The "This is not science fiction" hedge happened because Claude took "make it non-fiction" literally as a spoken line. Don't repeat this.

- **No evidence claims.** Max presents no evidence. Anna must never say "the evidence" or "proof" or "proven." The talk describes a search, not results.

- **No overpromises.** Only offer: free DNA analysis, all findings returned. That's it. No "you'll discover your origins" or "you'll find your starseed lineage."

- **Anna is story-first, not advertising.** She's not there to sell Max. She's there to guide the listener through the ideas.

- **Tone: light, curious, warm. Not ominous.** Use Fish bracket cues `[warm]`, `[curious]`, `[bright]`. The old v04 tone was "sad and tense" per Max.

- **Audio clips must be ?15 seconds.** The video maker is hard-capped. Target 10-15s. The build script already handles this but if you edit the script and regenerate, don't break the chunking.

- **First speaker is Nadalee, not Max.** In any labeling or cuesheet, segment 0:48 onward is the host Nadalee introducing Max - not Max himself. Anna should hand off to "Nadalee" or "the host."

- **No AskUserQuestion-style choice lists.** Max prohibits this. Ask open questions.

- **YouTube upload path:** If re-uploading, use Max's already-logged-in Chrome via claude-in-chrome MCP. Playwright has no Google session. File upload sandbox means Max may need to drag the file.

- **Branch bulletin:** This session is D42B. Sister branch B70b also touched the Anna script. Check `bcast.py catchup` if you need cross-branch context, but D42B owns the final deliverable.

- **Site deployment:** The `/temp2` route was added to `C:\claude_base\sites\maxrempel-site\src\index.js` and committed + pushed. If you need to change the serving logic, edit that file, run `deploy.sh`, and commit. The R2 uploads are separate (via `publish_temp2.py` using boto3).

- **Max's spelling:** "Nadalee" (N-A-D-A-L-E-E) - the correct version per Max's last dictation. Earlier attempts "Nathalie" and "Nadalie" were wrong.
