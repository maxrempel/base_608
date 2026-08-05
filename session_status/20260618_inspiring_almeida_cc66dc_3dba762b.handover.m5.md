# Scribe handover - milestone 5 (~408K tokens)
# session: 20260618_inspiring_almeida_cc66dc_3dba762b
# cwd: C:\claude_base\.claude\worktrees\inspiring-almeida-cc66dc
# written: 2026-06-18 06:33:48 by deepseek-v4-pro

# HANDOVER - NONH-to-Human-Timecoder Work & the Method for Developing It

## GOAL (in Max's own words)
"Pick one oldest good video not done by humans, so good among old nonh, and annotate, double check and give to human timecoders. And repeat handover once per week."

And, more critically: **the method** by which that handover is developed. Not just deliver a sheet - re-establish the *correct way* to do it, because the rules were lost and the earlier attempt was a disaster.

## THE RULES THAT GOT BROKEN (and must now be re-enshrined)
Max stated these explicitly after the first attempt failed:

1. **No titles. No canon song names anywhere in the handover.** The song's identity is its **first sung line only** - the actual lyric the singer starts with. Every "????????" column in the Google Sheet must contain either that verified first line or a blank/PROVERIT placeholder.
2. **All first lines must be verified by a smart LLM** - DeepSeek v4 non-flash minimum (i.e., a model that actually *reads and reasons* over the transcript, not a cheap mechanical matcher). The LLM reads the heard text, strips the intro, extracts the real first sung line, and says honestly "unknown" when the text doesn't support it.
3. **You (the worker) must spot-check** the LLM's output. No blind delegation. This mirrors the principle from the performer identity problem (the Margarita case: one name in the DB, but possibly several real people - only an LLM actually looking at the data can decide).
4. **No mechanical matching for identification** - the original pipeline's char-ngram/fuzzy-align matcher produced famous-song drift (e.g., announcer says "????????", matcher grabs a random famous Okudzhava song). That output is untrustworthy and must NOT be carried into the handover. The transcript must be *read*.

These rules were known to older sessions but got lost; your job includes making certain the next session can't miss them.

## DECISIONS MADE AND WHY

- **Pick video pX_1m8DlMbA** (2020-03-30, "?????? ?? ???????????? ?????"): oldest good NONH video by upload date, 47 segments across ~31 performer turns, only 10 segments had any machine-identification, making it a clean test case for the new method.
- **Handover format must exactly mirror the human team's Google Sheet**, which lives on disk as `C:\Users\maxre\Downloads\????? ?? ?????.xlsx`. One sheet per concert, columns: ?, ??????, ???????????, ????????, ??????, ?????? ??????, ??????? ?????, ??????, ??????? + ???????????, ????-????, ??????? ? ?????? ?????. But note: the "????????" column is now repurposed to hold the **first sung line** (or blank/verify), never a canon title.
- **The old handover attempt was built from mechanical matcher output** and therefore must be thrown out for identification purposes. The timing data (start/end/play_url) and performer segmentation are still usable because those came from the intro-separation step, which is reliable. The heard text is usable as raw input.
- **B27 is now your manager** - you (b29) do the work. B27 sets the direction, you build and report.

## CURRENT STATE (as of the handover split)
- **Handover tool exists** at `tools/tamza_songs/pipeline/timecoder_handover/nonh_handover.py`. It can pick the oldest video, join dates from the channel inventory, group by performer, and produce a table. But the table it produces *still carries machine-matched titles and first-lines that are often spoken intro*. It must be rewritten or replaced to use the new method (LLM-read first lines only).
- **A first-pass handover TSV was committed** at `tables/handover_2020-03-30_pX_1m8DlMbA.tsv`. Use it for timing/performer grouping only - **discard every song title and first-line cell**.
- **A QC file exists** at `qc/pX_1m8DlMbA.json` that labels which machine matches were trustworthy (only 2 of ~10 were OK, the rest verified as drift). That is a record of the old method's failure - useful as a lesson, not as input.
- **The draft JSON** with heard text per segment is at `song_timing/from_scratch_idx/_work/annotator/drafts_nonh_v01/nonh_pX_1m8DlMbA.json`. This is your primary input for extracting real first sung lines.
- **The pipeline for 93 caption-disabled videos** is running on Sol (ASR transcription). As those transcripts land, they will need the same handover treatment, so your method must be repeatable and scriptable.
- **The human team's Excel** is at `C:\Users\maxre\Downloads\????? ?? ?????.xlsx`. Inspect it with openpyxl to understand the exact formatting (merged cells for performer groups, the row numbering scheme, etc.).

## EXACT NEXT STEP (for you, b29)
1. **Read the draft JSON** for video `pX_1m8DlMbA` and extract, for every segment, the raw `heard` text (this is the ASR/transcribed audio - may contain intro chatter followed by actual singing).
2. **Run a *smart* LLM reading pass** on each segment's heard text. The LLM must:
   - Strip spoken intro/chatter and locate the first sung line.
   - Extract that line as the identity.
   - If the segment contains no sung lyric (pure intro, applause), mark it clearly.
   - If the heard text is garbled/unclear, say "unknown" honestly.
   - Do NOT use any mechanical matcher or canon titles.
   - The LLM used should be DSeepSeek v4 non-flash or better (model that actually reads).
3. **Spot-check** the LLM's output yourself - compare several rows against what makes sense (performer consistency, known songs at that concert, etc.).
4. **Build the handover sheet in the exact human Excel format** (columns as above), with:
   - Performer as the grouping key.
   - Start time as clickable &t= link.
   - "????????" (song title) replaced with the verified first sung line (or "?????????" / blank if uncertain). **Absolutely no canon titles.**
   - "??????" may be left blank unless the LLM confidently identifies the author from context - but that's secondary; focus is first line.
   - "?????? ??????" in the human format may be redundant if we already put first line in the "????????" column - check the existing filled-in sheets to see how they're actually used - but Max's rule is first sung line is the identity, so ensure it appears clearly.
5. **Document the method** - create a concise `METHOD.md` or baked into the handover tool that future sessions cannot skip. It must include the four rules above, plus a practical checklist: read draft ? LLM extract first lines ? spot-check ? build sheet.

## OPEN QUESTIONS AWAITING THE USER
- None specifically for you - Max split to B27 as manager and you as worker. B27 should set further direction, but the above immediate step is clear from the transcript.
- Max was considering a re-enshrinement of rules in the handover doc - you should do that unblocked.

## KEY FILE PATHS AND IDS
- **Human Excel template**: `C:\Users\maxre\Downloads\????? ?? ?????.xlsx`
- **Pipeline base**: `tools/tamza_songs/pipeline/`
- **Draft of target video (heard text)**: `song_timing/from_scratch_idx/_work/annotator/drafts_nonh_v01/nonh_pX_1m8DlMbA.json`
- **Old handover TSV (timing/performer only)**: `timecoder_handover/tables/handover_2020-03-30_pX_1m8DlMbA.tsv`
- **Old QC record**: `timecoder_handover/qc/pX_1m8DlMbA.json`
- **Existing handover tool (needs rewrite)**: `timecoder_handover/nonh_handover.py`
- **YouTube video ID**: `pX_1m8DlMbA`
- **Channel inventory (upload dates)**: `output/channel_inventory.json`

## GOTCHAS AND DEAD ENDS ALREADY RULED OUT
- **Mechanical matcher (char-ngram/fuzzy align) is dead for song identification.** It drifts to famous songs whenever the announcer names an author. Do not pipe its output into the handover.
- **The old handover's "first line" cells often contain spoken intro**, not the sung first line. Do not trust them.
- **Do not use YouTube metadata calls** - the upload dates are already in the channel inventory JSON (no API hit needed).
- **The "0" files issue when checking ASR progress** was a shell-glob artifact - always verify with `ls` directly, not `wc -l` on a glob that might expand to nothing.
- **The handover was reviewed once by an independent LLM** but that was on the old mechanical output; a fresh review is needed after the new LLM-first-lines pass.
- **Under no circumstances publish live the mechanical matches** - the go-live gate for NONH songs is parked awaiting the user's morning decision, and it's outside your scope anyway. Your scope is the non-live, human-timecoder handover.

## SUMMARY OF YOUR TASK
You are b29, the doer. B27 is your manager. You must redo the handover for video `pX_1m8DlMbA` from scratch, using the correct method: extract the real first sung line from each segment's heard text using a smart LLM, spot-check it yourself, produce an Excel sheet matching the human team's format, and **kill all titles**. Additionally, document the method so this disaster never repeats.
