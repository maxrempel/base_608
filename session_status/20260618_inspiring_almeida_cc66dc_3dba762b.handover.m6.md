# Scribe handover - milestone 6 (~477K tokens)
# session: 20260618_inspiring_almeida_cc66dc_3dba762b
# cwd: C:\claude_base\.claude\worktrees\inspiring-almeida-cc66dc
# written: 2026-06-18 19:13:25 by deepseek-v4-pro

# HANDOVER - Tamza Song Pipeline (b29 worker under B27)

## GOAL (Max's own words)

The project is a database + live website of songs from the Tamza concert video channel. Newly identified songs should go live; unknowns shouldn't. The pipeline is ~90% done. My specific task: pick the oldest good not-human-done video, build a handover table in the human timecoders' exact format, verify it properly, hand it off, repeat weekly. My priority task: develop the **method** of producing these handovers so the rules stop getting lost across sessions.

## CRITICAL RULES (re-established this session - must survive compaction)

Max was furious. These were known by old sessions, lost by newer ones, and the work was done blindly:

1. **NO TITLES. NO CANON NAMES.** Song identity = **first sung line only**, never a title, never an author name matched from a canon database. Kill all "????????" and "??????" fields in handover output - humans fill those.
2. **The LLM must actually READ the transcript data.** No mechanical matcher, no char-ngram aligner, no Python heuristic. A smart model (DS4 non-flash minimum) reads the heard text directly and identifies songs by comprehension. The Opus session (me) spot-checks.
3. **Performer identity needs thinking, not scripting.** The DB has one "?????????" - an LLM must reason whether that's the same person across concerts, not a Python name-collapse.
4. **First lines must be verified.** Not the ASR head (which is often the announcer's intro), but the actual first sung lyric after the music starts.

## DECISIONS MADE + WHY

- **Handover format must match the human Excel exactly.** I found the real file at `C:\Users\maxre\Downloads\????? ?? ?????.xlsx`, read its sheets, and mirrored the 11-column layout (?, ??????, ???????????, ????????, ??????, ?????? ??????, ??????? ?????, ??????, ???????, ????-????, ??????? ? ?????? ?????) with per-concert grouping. Reason: the human team shouldn't adapt to our format.
- **Killed all titles from the tool output.** ???????? and ?????? are now blank; the only identity field is ?????? ?????? (first sung line). Reason: Max's core principle - titles are noise, identity is the sung line.
- **Discovered the [??????] ASR marker technique.** The ASR (whisper on Sol) inserts `[??????]` at the speech?music transition. The first sung line starts right after it. Reading the full transcript window (not just the segment head) gives the real lyric. This flips the earlier "half the matches are wrong" panic - several canon matches were actually correct; the failure was nobody reading the full text.
- **Live NONH publish was PARKED.** b15merger (sole owner of the gate + live patch) went unreachable overnight despite repeated wake calls. I parked rather than risk a complex live deploy on unfamiliar code. Needs Max's attention in the morning.
- **Re-registered as b29 when Max split the roles.** B27 is now the manager; I (b29) am the worker doing the handover and - importantly - the METHOD of developing handovers. My focus is producing the work AND encoding the rules so future sessions don't forget them again.

## CURRENT STATE

**Done and pushed:**
- `timecoder_handover/nonh_handover.py` - reusable tool: `pick` (oldest good NONH video by upload date), `table` (emits Excel-format TSV)
- `timecoder_handover/verified/pX_1m8DlMbA.json` - my Opus-read first sung lines for the pilot video (13 verified, rest honestly marked intro-only or unknown)
- `timecoder_handover/HANDOVER_METHOD_v01_tomemex.md` - method doc enshrining the rules, the [??????]-marker technique, and the verification workflow
- `timecoder_handover/tables/handover_2020-03-30_pX_1m8DlMbA.tsv` - the pilot handover table (titles blank, first lines Opus-verified or honest-unknown)
- Rules sent to B25handoverer for folding into the canonical START-HERE handover

**In flight (autonomous):**
- ASR on Sol: 54/93 caption-disabled videos transcribed, process alive and grinding. b7nonhtimes owns the downstream seg?identify pipeline.
- b9's full 2842-video backup running on Lak, self-sustaining.

**Parked / awaiting Max:**
- Live publish of recognized NONH performances (b15merger unresponsive overnight). The gate was being built but never deployed.
- B27's archive cleanup plan (55 files to archive, zero live-import collisions verified) - ready, reversible, needs sign-off.
- The `_batch_aligner_v01.py` doc-vs-reality conflict (b15M owns it).

**Just arrived (not yet started):**
- B25handoverer woke me with a rules-harvest task: verify ~10 quotes from `C:/claude_base/tools/max_rules_harvest/max_rules_harvested_20260618_v01_tomemex.md` against their source files in `C:/claude_base/user_verbatim/`, then compare all 77 rules against the autoloaded instructions (`C:/Users/maxre/.claude/CLAUDE.md` + `C:/Users/maxre/Nextcloud/claude_md_synced/global2.md`), produce a gap doc `max_rules_GAP_vs_autoload_v01.md` in the harvest folder listing rules NOT yet in autoload. DO NOT edit CLAUDE.md/global2.

## EXACT NEXT STEP

1. **Immediately: process the B25handoverer task.** Read the harvested rules file, spot-check ~10 quotes against their cited sources, read the two autoloaded instruction files, cross-reference all 77 rules, write the gap doc, commit and push, report counts to B25handoverer.
2. **Then: resume the scaling question for handovers.** The pilot video is done (Opus-read). The method doc says scale via DS4-nonflash per-window reads with Opus spot-check. Max hasn't answered whether to wire this into the pipeline and who owns it. Ask B27 (my manager) when ready.
3. **Watch: ASR progress** on Sol (54/93, heading toward completion).
4. **Be ready for Max: live publish decision** on the parked NONH gate.

## OPEN QUESTIONS FOR MAX

- Who scales the smart-LLM first-line reading pipeline-wide - me (b29), or does it hand back to b15A/b15M/b7nonhtimes? What's the priority relative to the handover method work?
- b15merger's live publish - re-engage or hand to a fresh session?
- The ASR?seg?identify pipeline b7nonhtimes is running autonomously - need any spot-checks on its output, or trust it since end-to-end validation already passed?
- Archive cleanup sign-off still pending for the B27 plan.

## KEY PATHS / IDs

- **Pipeline root:** `C:\claude_base\tools\tamza_songs\pipeline\`
- **Handover tool:** `timecoder_handover/nonh_handover.py` (pick + table)
- **Verified first lines:** `timecoder_handover/verified/<vid>.json`
- **Output tables:** `timecoder_handover/tables/handover_<date>_<vid>.tsv`
- **Method doc:** `timecoder_handover/HANDOVER_METHOD_v01_tomemex.md`
- **Human Excel:** `C:\Users\maxre\Downloads\????? ?? ?????.xlsx`
- **Channel inventory (dates):** `output/channel_inventory.json`
- **Drafts (NONH segment data):** `song_timing/from_scratch_idx/_work/annotator/drafts_nonh_v01/nonh_<vid>.json`
- **Transcripts:** `song_timing/transcripts/<vid>.json`
- **ASR ready list:** `song_timing/_work/nonh_asr_ready_on_teal16.txt` (82/93)
- **ASR output on Sol:** `~/nonh_transcribe/out/` (via SSH `maxre@192.168.1.113`)
- **Caption-disabled IDs:** `song_timing/_work/nonh_caption_disabled_ids.txt` (93)
- **Board:** `python C:/claude_base/branch_bulletin/bcast.py read`
- **Worklog:** `python C:/claude_base/compaction_kb/scripts/worklog.py log`
- **Rules harvest:** `C:/claude_base/tools/max_rules_harvest/max_rules_harvested_20260618_v01_tomemex.md`
- **Autoloaded instructions:** `C:/Users/maxre/.claude/CLAUDE.md` + `C:/Users/maxre/Nextcloud/claude_md_synced/global2.md`
- **My session ID:** b29 (worker under B27 manager). Note: identity sometimes slips to "c6" when the shell is in a different worktree - re-assert `b29` with `bcast.py whoami b29` after directory changes.

## GOTCHAS

- **Identity = first sung line ONLY.** Never carry titles, never use canon-match names. If you put a ???????? in the handover, Max will be furious. The tool now outputs them blank.
- **The [??????] marker is the key.** The ASR inserts it at the speech?song boundary. Read the text AFTER it, not the segment head (which is mostly host chatter). The "half the matches are wrong" finding was an artifact of head-only reading.
- **No Python heuristics for identification.** The mechanical matcher (char-ngram + fuzzy align) drifts to famous songs when the announcer names a well-known author. An LLM must actually read the lyric text. Songs the matcher called "KNOWN" should be treated as guesses, not truth.
- **Do not hit YouTube for metadata.** Use `output/channel_inventory.json` for upload dates - it's already local (935 videos, id + upload_date + title). The ban on YouTube calls during ytdow runs is real.
- **The human Excel has per-concert sheets**, named like "2025.05.04.???-?? ?????? ??? ????? ??????????". Columns: ?, ??????, ???????????, ????????, ??????, ?????? ??????, ??????? ?????, ??????, ??????? + ???????????, ????-????, ??????? ? ?????? ?????.
- **b15merger went unreachable overnight.** The live NONH publish is NOT done. Do not assume it deployed. The publisher tool (`scripts/publish_catalog.py --dry-run`) is gated and reversible - the human-side catalog IS already live, but NONH recognized performances are not.
- **Board ID slip:** b29 vs c6. This worktree (`inspiring-almeida-cc66dc`) has its board identity as c6. Re-assert b29 after any cd that changes the worktree context.
- **No editing CLAUDE.md/global2 directly.** The B25 task explicitly forbids it - gap doc only, Max picks what to promote.
