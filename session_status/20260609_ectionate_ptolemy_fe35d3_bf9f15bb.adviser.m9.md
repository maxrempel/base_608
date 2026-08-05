# Adviser note - milestone 9 (~136K tokens)
# session: 20260609_ectionate_ptolemy_fe35d3_bf9f15bb
# written: 2026-06-09 12:43:34 by claude-opus-4-8

TO MAX:
Reasonable pivot. But before the Assistant burns context on a web search, know the tradeoff: the alternatives you're after (Kling, Runway Gen-3, Hailuo/MiniMax, Veo) understand English motion far better than Wan, but most won't take YOUR exact shuttle shape as a reference image the way your local pipeline does - they reframe/redraw. Kling and Runway have image-to-video with motion prompts that are the closest fit. Decide: do you want faithful-shape (stay local, fix the source still) or smart-motion (go external, accept some shape drift)? You can't fully have both yet.

TO ASSISTANT:
Max asked you to STOP and SEARCH ONLINE - do that, don't drift back into firing local jobs. When you search:
- Name concrete tools and whether each accepts a user image + supports image-to-video with prompt-driven motion: Kling, Runway Gen-3, Hailuo/MiniMax, Veo, Pika.
- Report API access + rough cost, since this is a production loop, not a one-off.
- Keep it tight: one focused search pass, summarize, then let Max choose. Do not inhale huge pages.
Also flag the real root cause you already found: the failure was the SOURCE STILL (generic NASA shuttle), not just Wan. Any new tool fed the same bad plate fails the same way. The shuttle-shape problem follows you regardless of engine - say so plainly.
