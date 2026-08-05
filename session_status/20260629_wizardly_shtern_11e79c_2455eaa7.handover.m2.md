# Scribe handover - milestone 2 (~157K tokens)
# session: 20260629_wizardly_shtern_11e79c_2455eaa7
# cwd: C:\moma\.claude\worktrees\wizardly-shtern-11e79c
# written: 2026-06-29 16:42:14 by deepseek-v4-pro

# HANDOVER - Scene 11 Arrangements (Contact Countdown)

---

## GOAL (Max's words)

> "We are working on scene 11 of MoMA, Contact Countdown. We need to create arrangements by meaning. Learn the arrangements, learn the format, learn the actual script from Notion, and propose. Start from simple, like first three arrangements - combination merges of the lines."

> "Let's experiment with unlimited number. I think it can handle many."

---

## DECISIONS MADE + WHY

**1. Merge style: group-room (all 4 people), not 2-person.**
- Max rejected the safer 2-person-only approach. He wants to push turn-count high within single merges and trusts the model can handle many faces in one shot.
- Reasoning: scene 11 is a 4-person room (Anna, Ishtab, Werner/Gunther, Derek in the Art Nouveau room). Realism demands everyone visible; cutting back and forth for 2-person would fragment the conversation unnaturally.

**2. The real ceiling is clip LENGTH, not speaker count.**
- Verified by reading `project_wan26flau_lane.md`: the i2v model hard-caps `clip_dur` at `[3, 15]` seconds. Unlimited people = fine. Unlimited seconds = no.
- Therefore merge by meaning until audio hits ~14s, then break. Short staccato lines (1-2 words) are the ideal place to pack many turns; long monologues eat the budget fast.

**3. Arrangement grouping principle: meaning-units.**
- Each merge captures a complete narrative beat. Speakers and turn-count are flexible as long as the audio fits ~15s and the beat is coherent.

---

## CURRENT STATE

Two proposed reels are drafted (not fired, not exported - purely proposal stage):

**Reel 1 - "The probe" (~8.5s, 8 turns, all 4 visible)**
ANNA: The AI shutdown / DEREK: Yes / ANNA: All three countries / DEREK: Yes / ANNA: At the same time / DEREK: Yes / ANNA: By coincidence? / WERNER: Suspicion is infectious.

**Reel 2 - "The bias reveal" (~10s, 6 turns, all 4 visible)**
ANNA: What did they find? / DEREK: Bias / ANNA: In their own AI? / DEREK: Yes. Each discovered their own AI favoring their enemy / ANNA: So they turned it off / WERNER: They stepped back four years.

The earlier "Merge 1" (welcome/who's-who) was set aside - no verdict yet on whether it gets absorbed or kept separate.

---

## EXACT NEXT STEP

Claude ended with an open question to Max:

> **"Want me to keep proposing the whole scene this way - packing each meaning-unit as full as the 15s budget allows - or stop here and test Reel 1+2 first?"**

The ball is in Max's court. The cold session should NOT continue proposing. It should either:
- Wait for Max to choose "continue proposing" vs. "test first," OR
- Pick up whichever path Max selects next.

---

## OPEN QUESTIONS AWAITING MAX

1. Continue proposing the rest of scene 11 in this group-room style, or stop and test Reels 1+2 first?
2. What happens to the original "Merge 1" (the welcome: Ishtab introducing Anna, Werner's "favorite troublemaker" line)? Does it become its own reel before Reel 1, or get dropped?
3. Are the ~8.5s and ~10s durations acceptable, or does Max want them tighter to leave room for pauses/visual breathing?

---

## KEY PATHS & IDS

- **Scene script source (Notion):** Page titled `"11 scene Service Desk and Crisis Briefing (20260502)"` - fetched via Notion MCP tool.
- **Technical ceiling reference:** `C:/Users/maxre/.claude/projects/C--moma/memory/project_wan26flau_lane.md` - contains `clip_dur clamped [3,15]` rule.
- **Worktree:** `C:\moma\.claude\worktrees\wizardly-shtern-11e79c`
- **Branch bulletin:** `C:/claude_base/branch_bulletin/bcast.py` - used for `whoami` and `catchup`.
- **Agent ID:** `d53`

---

## GOTCHAS & DEAD ENDS RULED OUT

- **Do NOT assume merges must be 2-person.** Max explicitly overrode that constraint.
- **Do NOT propose merges where total spoken audio exceeds ~14s.** The 15s clamp is real and verified in code - not configurable.
- **Long Werner/Ishtab monologues** (e.g., Atlantis speech) cannot be merged with other lines - they'll eat a full reel alone. Plan for that.
- **Nothing has been fired or rendered.** This is a pure proposal/discussion phase. No files were written, no API calls to wan26flau were made.
- The script was successfully fetched from Notion, and the wan26flau lane config was successfully read - no tool failures blocked discovery.
