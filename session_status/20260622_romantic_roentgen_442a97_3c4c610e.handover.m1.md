# Scribe handover - milestone 1 (~89K tokens)
# session: 20260622_romantic_roentgen_442a97_3c4c610e
# cwd: C:\claude_base\.claude\worktrees\romantic-roentgen-442a97
# written: 2026-06-22 15:43:13 by deepseek-v4-pro

# HANDOVER - Retake Cleaner Research

---

## GOAL (in Max's own words)
> Research what was the tool for retakes, and what speech recognition did it use?

---

## DECISIONS + WHY

The tool for retakes was identified as **retake_cleaner**. The key technical decision in its design was the choice of speech recognition engine:

- **Chosen: Deepgram nova-3** - specifically in "verbatim" mode.
- **Explicitly rejected: Whisper** - because Whisper silently merges retakes (i.e., it "cleans up" false starts, corrections, and repeated phrases by dropping the abandoned fragments, which is exactly what a retake-aware tool needs to *preserve*).

**Reasoning:** Standard ASR engines like Whisper treat retakes as noise to be removed. The retake workflow *depends* on seeing those abandoned takes to determine what the speaker actually intended. Deepgram's verbatim mode surfaces them instead of hiding them.

---

## CURRENT STATE

- The tool's identity, location, and core speech-rec dependency have been identified.
- No further work has been initiated - this was a pure research question.

---

## EXACT NEXT STEP

None specified. The research question has been answered. If Max wants to:
- Run the tool, the script is at the path below.
- Modify which speech-rec backend is used, the relevant code lives in that file.
- Investigate *how* retake detection logic works beyond speech rec, the script is the entry point.

---

## OPEN QUESTIONS

- None explicitly asked. Possible unasked: Does retake_cleaner have a configurable ASR backend, or is Deepgram nova-3 hardcoded? What specifically qualifies a segment as a "retake"?

---

## KEY PATHS / IDS

| Item | Value |
|------|-------|
| Tool name | `retake_cleaner` |
| Script path | `C:\claude_base\tools\retake_cleaner\retake_cleaner.py` |
| Speech rec engine | Deepgram nova-3 (verbatim mode) |
| Rejected alternative | Whisper (silently merges retakes) |

---

## GOTCHAS

- **Do not swap in Whisper** as the ASR backend for any retake-related work - it will silently strip the very data the tool exists to capture.
- Deepgram verbatim mode is load-bearing; non-verbatim Deepgram modes may behave similarly to Whisper.
