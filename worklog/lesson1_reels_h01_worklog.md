# Lesson1 reels - H01 worklog

Session: H01 (bcast id C51cb). Task: render Telepathy Lesson1 reels via MoMA (lipsie, wan26flau, ~$0.25 ea). Worker = shared singleton, never launch 2nd / never quit.

## State as of 2026-07-29 (post-compaction continuity)

- My earlier reels: spots 57-71 (12 approved, 3 done) and spots 83-99 all DONE (rendered, awaiting Max review). None junked.
- spot99/job3637 (fired via H03's v01 tool): EYEBALLED, GOOD. Palm-up text in its prompt did NOT render as the banned offering pose - keep it.
- Root-cause fix committed+pushed: moma **0108845** - stripped latent palm-up text from `contrast_turn_hand` + `counting_both_hands` catalog descriptions (they leaked into v01 prompts). JSON validated; no palm-up left in any non-banned gesture.
- H03 released **scripted_reel_pipeline_v02.py** (commit 8f16dff): sources gestures from the APPROVED rulebook vocab (gesture_rules_lesson1_v01.json), sends banned/palm-up/V-sign ids -> stillness by design, composes via MY gesture_authored_v01 format, enforces right-hand. This is the safe synthesis. USE V02 from now on.
- v02 validated end-to-end: dry-run + first real fire = **job 3643 (spot13), queued**. Provenance -> scripted_reel_log_v02.jsonl.

## Split (confirmed with H03)
- H01 (me): 13(fired), 15, 20, 22, 23, 24, 26, 27, 28, 29, 30, 31, 32, 51, 52, 53, 54, 55.
- H03: 100-112 (mostly done).

## Next
1. When job3643 renders (done), extract frames + eyeball (palm-up? captions? on-formula?).
2. If clean, produce remaining spots via `python scripted_reel_pipeline_v02.py --spot N` from C:\moma\sc10\combo_runner\code : dry-run + eyeball EACH (stochastic), small batches (~4).
3. Standing rules: never redo approved reels (esp. spot67/71 palm-up) without Max's ok; candlelight locked; table_low.png banned as input still; fire via fire_job only; eyeball every reel.
