# Scribe handover - milestone 6 (~93K tokens)
# session: 20260610_pensive_ishizaka_ca20b3_85962d0f
# cwd: C:\moma\.claude\worktrees\pensive-ishizaka-ca20b3
# written: 2026-06-10 14:01:21 by claude-opus-4-8

# HANDOVER - Music Overlay Tab (D10 / MOMA)

## GOAL (in Max's words)
Max wants to "overlay the music" onto an assembled video. His vision: he manually produces an assembled video, then opens a **music addition tab**. That tab has:
- A little video viewing rectangle (the assembled export playing)
- The current soundtrack made of clips (the assembly's own audio)
- A drop / load-music interface - he drags in a music file, longer or shorter than the assembly
- He aligns it
- He drags the line to create **break points** and builds a **volume curve**
- The curve is **shark-tooth shape** (piecewise straight lines). If he wants smoothness, he just adds more break points - that's the whole mechanism.
- Then play, with ability to scroll back and forth and adjust. Pieces are ~4 minutes each.

His exact framing of the workflow this session: **"First we export. Adjust and then bring it back. Bringing it back will be later. Right now just an extra tab, postprocessing."**

## DECISIONS + WHY
- **Music goes on AFTER assembly**, not before. Max reasoned he'd "rather see it assembled and edit" - paint music onto a finished assembly rather than weave it in earlier. Cleaner.
- **Volume curve = shark-tooth only** (piecewise linear between break points). Deliberately simple: no bezier/smooth curves. Smoothness is achieved purely by adding more break points. This is the standard video-editor mental model Max is invoking.
- **Scope this session = an EXTRA TAB for postprocessing.** This is a new tab, separate from existing assembly UI.
- **Export-first, not preview-first.** D10 offered two paths: (a) live preview/tune only, render final separately; (b) export a final mixed file. Max chose export ("First we export"). The "bring it back" - re-importing the adjusted/mixed result into the main pipeline - is explicitly **deferred to later**, NOT part of this session.

## CURRENT STATE
- Nothing built yet. Zero tool calls, zero file reads. Pure planning conversation.
- D10 confirmed the feature is buildable natively in the browser via Web Audio.
- D10's restatement of the picture was implicitly accepted (Max didn't correct it).
- The one open design question D10 raised (export vs preview) has now been answered: **export.**

## EXACT NEXT STEP
1. Orient in the actual codebase first - this session has read NO files. Find the "sound server" D10 referenced and how its tabs are structured, so the new tab fits the existing pattern.
2. Build the new postprocessing tab containing: video rectangle showing the assembled export, the existing clip-soundtrack lane, a drop/load-music interface, alignment control for music start, click-to-add break points on the music lane, draggable shark-tooth volume curve, scrub + play.
3. Since Max said "First we export" - the deliverable this round is the tab that produces an exported final mixed output (video + clip audio + music with the volume curve baked in), with live tuning of the curve before export.
4. Do NOT build the re-import / "bring it back" step - that's later.

## OPEN QUESTIONS (awaiting Max)
- What exactly does the export produce? Assume final mixed MP4 (video + clips + curved music baked) unless Max says otherwise - but confirm format if it matters to the build.
- How is the "assembled export" produced/located? Max says he manually produces the assembled video - need to know where that file lives so the tab can load it.
- Music overhang handling: D10 assumed overhang clips or leaves silence - not explicitly confirmed by Max.

## KEY PATHS / IDS / NAMES
- cwd: `C:\moma\.claude\worktrees\pensive-ishizaka-ca20b3`
- Project: **MOMA**. Agent persona: **D10**.
- D10 referred to "the sound server" as the host for the new tab - locate it; tab pattern lives there.
- Tech: **Web Audio API** (browser-native) for playback/curve; an **ffmpeg-style render step** for the export.
- No file paths, IDs, or commands have been established yet - they must be discovered.

## GOTCHAS
- Don't over-engineer the curve: shark-tooth (linear segments) ONLY. No smoothing math.
- Don't build the re-import pipeline - explicitly deferred.
- Don't confuse the two audio streams: the assembly already has its own clip soundtrack; music rides UNDER it following the curve. Both must coexist in the mix.
- This is a brand-new tab - find and match the existing tab/UI conventions of the sound server before writing UI from scratch.
- Token budget: ~93K used, compaction near ~169K. The codebase hasn't been read yet, so reading the sound server will consume budget - be targeted.
