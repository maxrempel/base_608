# Scribe handover - milestone 4 (~309K tokens)
# session: 20260728_ecursing_mccarthy_bee782_51f9197e
# cwd: C:\claude_base\.claude\worktrees\recursing-mccarthy-bee782
# written: 2026-07-28 10:40:14 by deepseek-v4-pro

**Handover for Telepathy Lesson 1 - Reel Production (H05 branch)**

**USER'S GOAL (in Max's own words)**
"Register as session H05 and grab the next five reels. Process the next five reels using whatever tools - use your LLM to produce gestures. For each line write a preceding gesture and following gesture, describe the gestures during that line and the woman's emotions. Plan about seven gestures in a whole reel of 15 seconds, proportionally less for shorter clips. Gestures should be tamed or vivid depending on the topic, and they must make sense. Allocate the reels in a group discussion board registry so other sessions don't collide."

This sits inside a larger standing goal: produce video reels for ALL remaining unrendered spots of Telepathy Lesson 1 (112 spots) through MoMA, with the correct locked-prompt header and meaning?driven gestures. Fill gaps only - never overwrite approved or held reels that are good.

**DECISIONS MADE AND WHY**

- **Branching into H05** - Max wanted parallel work; multiple sessions can render independently without stepping on each other. The group discussion board (`bcast`) is the minimal coordination layer.
- **Claiming spots 72-76** - H01 already had 67-71, H03 claimed 100-112. 72-76 was the next contiguous open block. The board registry prevents collisions.
- **Gesture method: LLM-authored, semantic, per?sentence** - The old keyword-based picker was abandoned because it matched wrong gestures (e.g. a "two?finger" counting gesture on a line about dying). Now every reel gets manually authored gestures that reflect the meaning of each sentence. Each line carries:
  - The woman's underlying emotion (calm, kind, heavy, awe, etc.)
  - A preceding gesture (what the hands do leading into the line)
  - A gesture during the line (change or hold, tied to the meaning)
  - A following gesture (where the hands settle or transition to the next line)
- **Proportional beats** - About 7 distinct gesture changes across a 15?second reel; fewer for shorter clips.
- **Prompt header stays locked** - The permanent base of every reel prompt is Max's exact original wording (verbatim):  
  `"A woman sits alone at a kitchen table at night in warm candlelight. She is completely alone in the room; no other people appear anywhere in the frame. She speaks very kindly, gently and warmly, her gaze resting calmly straight ahead in her original forward direction. She gestures naturally and warmly with her hands as she speaks, lifting them from the table in soft expressive movements. Gentle natural blinking and breathing. The camera slowly and gently pushes in, zooming toward her."`  
  Only the gesture descriptions are added after this header. (Scene?specific guard in the worker enforces the mandatory clauses - candlelight, "completely alone, no other people", gentle push?in.)
- **Still images** - Always use neutral hands-at-rest stills from `telepathy_tapes/tape1select_output/`. `table_low.png` is banned forever
