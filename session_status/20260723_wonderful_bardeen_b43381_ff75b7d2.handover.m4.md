# Scribe handover - milestone 4 (~316K tokens)
# session: 20260723_wonderful_bardeen_b43381_ff75b7d2
# cwd: C:\claude_base\.claude\worktrees\wonderful-bardeen-b43381
# written: 2026-07-23 16:54:04 by deepseek-v4-pro

# Handover: IONS Prize Letter of Intent - Editing & Submission

## GOAL (in Max's own words)
Finalize the Letter of Intent for the IONS $100,000 prize, submit it (even though the July?22 deadline passed by one day), and have the text be in **Max's own voice** - not AI?sounding. Max discovered that a previous draft had "90% AI writing style" per Grammarly and wants only formatting and typo cleanup on his raw dictation, with any editorial suggestions clearly marked (bold or strike?through) so he can decide. The immediate next step is for Max to paste his own version of a section (the Consciousness and verifiability paragraph) and then Claude to do that cleanup and nothing else.

## DECISIONS MADE + WHY
1. **Target grant**: IONS Linda G. O'Bryant Noetic Sciences Research Prize ($100k, 1?year) for consciousness?related UFO research. LOI due July?22, 2026 (passed yesterday). Full proposal deadline Sep?7 if invited.
2. **Project title**: "Genetic Analysis and Hypnotic Regression of Self-Reported Alien Hybrids" - chosen by Max after brainstorming, to be short, declarative, no question marks.
3. **Team composition** dropped **all unconfirmed people** per Max's instruction: only confirmed participants listed (Max, Ancha Baranova, Whitley Strieber, Stanley Krippner, Richard Alan Miller, Alan Steinfeld). No per?person "confirmed" tags - one line: "All participants have confirmed participation."
4. **Budget rounded** to clean numbers: short?read $40k, long?read (PacBio at UCSD) $30k, hypnotic regressions $25k, IRB $5k = $100k.
5. **Style required**: Max's own words, no hedging, confident but not naive, aimed at an IONS audience that wants evidence. He wants to avoid AI?idiocy, excessive wording, and the typical "signature AI writing style."
6. **Reference method for audio**: FishAudio SDK, default male narrator voice, chunked to ~200 characters, concatenated with ffmpeg. Key path: `C:\Users\maxre\Nextcloud\zSyncMain\credentials\fish_audio_api_key.txt`. This method was used to render the LOI as mp3 (already sent to Max). Now no audio is requested; focus is on text.
7. **Format for submission**: LOI is a simple online form (research.net/r/LGOBPrize_2026), max 1,200 words.

## CURRENT STATE
- **LOI draft**: The canonical **source file** is `C:\claude_base\projects\XG1\ions_prize_2026\ions_loi_draft_v04_20260723.md`. It contains:
  - Title, PI, $100k/1yr, Question, Methods, Preliminary data, Team, Budget, and a "Consciousness and verifiability" section (currently containing Max's earlier version, restored per his request).
- **Google Doc** (editable by Max): `https://docs.google.com/document/d/125PKjPvoKLN7s4kpJk2VsH3oe_11bFB8ysIHau4BgCg/edit` - was created from v04 HTML. Max had started editing it, but then instructed that he will provide his own text for the "Consciousness and verifiability" section.
- **Max's pending action**: He has just said "Just wait a second for the text." He intends to paste his own version of the "Consciousness and verifiability" paragraph (or possibly more sections) with his own wording, and expects Claude to:
  - Clean up **formatting and typos only**.
  - **Not rewrite or editorialize**.
  - If Claude wants to editorialize, mark suggestions with **bold** or ~~strike~~.
- **Late?submission note**: A draft email to research@noetic.org asking if they'll accept the LOI one day late is prepared and waiting for Max's "send" command. It has not been sent.
- **Audio**: Already rendered and emailed to Max for v03 and v03b; not currently requested.
- **File locations**:
  - Project folder: `C:\claude_base\projects\XG1\ions_prize_2026\`
  - Source markdown: `ions_loi_draft_v04_20260723.md`
  - Rendered word doc: `IONS_LOI_v04_20260723.docx` (for reference; not the canonical working format)
  - Google Doc ID: `125PKjPvoKLN7s4kpJk2VsH3oe_11bFB8ysIHau4BgCg`
- **Notion working notes**: "IONS Starseed Genetics Grant Application Working Notes" (last updated July?10) contains the detailed budget, team, and ideas. It's the source of truth for the original budget and team, but the LOI draft may diverge after Max's edits.

## EXACT NEXT STEP
1. **Wait for Max to paste his text.** He likely wants to replace the "Consciousness and verifiability" section (or possibly the entire LOI) with his own wording.
2. Once pasted, **do only**:
   - Fix obvious typos and punctuation (e.g., experieners?experiencers).
   - Normalize formatting (bold headings, bullet lists as needed) to match the overall LOI structure, without altering wording.
   - Ensure the section fits under the 1,200?word cap.
3. **If any phrase strikes you as needing editorial improvement**, mark it with **bold** for addition, or ~~strike~~ for deletion, or add a comment (e.g., [Editorial suggestion: ...]) so Max can see and decide. Do not apply substantive changes without this marking.
4. After Max's segment is integrated, the complete LOI text should be ready for review and potential submission (once the late?submission note is sent and the portal allows input).
5. The late?submission email remains pending; Max may want it sent after the LOI text is finalized.

## OPEN QUESTIONS
- Does the IONS portal still accept LOIs after July?22? The late?submission note was drafted but not sent; Max will likely either send it or decide to submit directly.
- Is there any additional section Max wants to add besides "Consciousness and verifiability"? He might provide the whole LOI text; we should handle whatever he gives.

## KEY PATHS & IDS
- **LOI source**: `C:\claude_base\projects\XG1\ions_prize_2026\ions_loi_draft_v04_20260723.md`
- **Google Doc**: `125PKjPvoKLN7s4kpJk2VsH3oe_11bFB8ysIHau4BgCg`
- **Project folder**: `C:\claude_base\projects\XG1\ions_prize_2026\`
- **IONS portal**: `https://www.research.net/r/LGOBPrize_2026`
- **IONS prize info**: `https://noetic.org/prize`
- **Notion working notes**: searchable in Notion under "IONS Starseed Genetics Grant Application Working Notes"
- **FishAudio key path**: `C:\Users\maxre\Nextcloud\zSyncMain\credentials\fish_audio_api_key.txt` (not needed now)
- **Confirmed participants for LOI**:
  - Max Myakishev?Rempel (PI)
  - Ancha Baranova (genomics)
  - Whitley Strieber (author/experiencer)
  - Stanley Krippner (hypnosis/consciousness)
  - Richard Alan Miller (UFO/hybridization, backup hypnosis)
  - Alan Steinfeld (adviser)

## GOTCHAS
- **AI style detection**: Max used Grammarly on a previous draft and it flagged 90% as AI?generated. He is highly sensitive to this. Any trace of AI?sounding phrase must be removed; his own voice must dominate. The session ended with his explicit instruction to only clean up formatting/typos and not rewrite.
- **"Return back the paragraph" confusion**: In a previous turn, Max asked to "return back the paragraph" (the Consciousness section) and thought Claude would restore an earlier wording. Claude edited the md file, but Max couldn't see it (not open). The restored paragraph is in the source but Max might still want to replace it with his own. Ensure any new edits are visibly accessible (maybe updated in the Google Doc or pasted in chat).
- **Hydration incident**: Earlier in the session, a background grep over Nextcloud caused hydration of a large file (Debian ISO). This is resolved and must not be repeated. No searching Nextcloud for credentials; use the known key path.
- **Two?master problem**: The Google Doc is editable by Max; the md file is maintained by Claude. To avoid divergence, after Max's edits are applied, it may be best to re?generate the Doc from the source, or just work in chat with Max's text and not touch the Doc until final. Max seems to prefer working in the Doc, but the session ended with him providing text via chat; adapt accordingly.
- **Late?submission email**: Must not be sent without Max's explicit "send" command. It's ready but waiting.
