# Scribe handover - milestone 1 (~105K tokens)
# session: 20260630_dreamy_lehmann_fea93b_6a0a19bf
# cwd: C:\claude_base\.claude\worktrees\dreamy-lehmann-fea93b
# written: 2026-06-30 12:10:22 by deepseek-v4-pro

# HANDOVER - Windows Read-Aloud Tool Research

## GOAL (Max's words)
Search for and identify the best tool for reading aloud on Windows - specifically, a common extension or utility capable of reading aloud selected text from many different types of applications (browser, Word, PDF, chat, etc.), triggered by a hotkey or floating toolbar.

## DECISIONS + WHY
Two standout free tools were identified, both fitting the "any app, select-and-read" requirement:

1. **NaturalReader** (recommended as best all-rounder)
   - Has a floating toolbar - highlight text anywhere (any app) and it reads immediately.
   - Best free experience; simple interface.
   - Good for ad-hoc, on-the-fly reading from anything.

2. **Balabolka** (recommended as best for saving to files)
   - Free, powerful, exports narration to MP3/WAV.
   - Better for long documents where you want a saved audio file.
   - Less slick for the "grab text from any app instantly" workflow compared to NaturalReader.

Additional options noted but not recommended as primary:
- **TextAloud / Pistonsoft** - paid, good hotkey support.
- **Speechify** - paid, most natural AI voices.
- Built-in free: Edge Read Aloud (web/PDF only), Word Read Aloud (docs only), Windows Narrator (full system, not selection-based).

Reasoning: NaturalReader wins for Max's stated "from very different things" use case because its floating toolbar works across all applications without being tied to a specific app (unlike Edge or Word built-ins). Balabolka is the backup if offline use or MP3 export matters more.

## CURRENT STATE
- Research phase is **complete**. Max has presented findings and recommendations.
- No software has been installed yet.
- Max ended by **offering to install** one tool on "Pine" and set up the hotkey - this offer has not yet been accepted or declined by the user.

## EXACT NEXT STEP
**Awaiting Max's decision.** The ball is in Max's court on two questions:
1. Which tool to install? NaturalReader (quick floating-toolbar reading) or Balabolka (free + MP3 export)?
2. Should the assistant proceed with installation and hotkey setup on the machine called "Pine"?

Once Max answers, the next actions are: download chosen tool, install it, configure the global hotkey, and verify it works across multiple app types (browser, text editor, PDF).

## OPEN QUESTIONS (awaiting Max)
- **NaturalReader or Balabolka?** (or a paid option?)
- **Proceed with install + hotkey setup now?**
- Any preference for specific voice/language settings?
- Confirm: the target machine is "Pine"?

## KEY PATHS / IDS
- Working directory: `C:\claude_base\.claude\worktrees\dreamy-lehmann-fea93b`
- Target machine name mentioned: **Pine**
- No files created or modified in this session - it was purely research via web search.
- Source URLs consulted:
  - TechRadar: best free text-to-speech software 2026
  - Arekore: Windows read-aloud apps guide
  - SourceForge: best TTS software for Windows 2026
  - Speechify official site

## GOTCHAS
- **No dead ends encountered.** The search was successful and produced clear winners.
- Windows Narrator was ruled out for this use case - it reads the entire UI, not just selected text on demand, making it overkill and awkward for quick "read this paragraph" workflows.
- Edge and Word built-in "Read Aloud" features are **application-locked** - they don't work across "very different things," which is the core requirement.
- NaturalReader's free tier may have voice limitations; this has not yet been checked. If Max finds the free voices robotic, Speechify's paid tier may become relevant later.
- The session is short (3 turns, ~105K tokens) - no prior context has been lost, but future compaction may summarize the research details above. This handover preserves the critical decision points.
