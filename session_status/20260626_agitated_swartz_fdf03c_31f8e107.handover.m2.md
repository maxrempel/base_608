# Scribe handover - milestone 2 (~156K tokens)
# session: 20260626_agitated_swartz_fdf03c_31f8e107
# cwd: C:\claude_base\.claude\worktrees\agitated-swartz-fdf03c
# written: 2026-06-26 18:56:25 by deepseek-v4-pro

## Handover - C33, bcast watchtower: misroute nudger live (2026-06-26)

### GOAL (in Max's words)
Max noticed that teams were mixing up boards, and he wanted the board system to enforce his original design: **the first letter of the ID defines which team board a message belongs to**, and a brand?new letter auto?creates a new board. After confirming that part already works, he expanded the ask: if a DeepSeek watcher monitors the joint board, it should **spot discussions that are really specific to one team** and remind the session to move them to the right team board. Characteristics he specified:

> *"Not aggressive, but suggestive and annoying. So it should, like, trust. Claude is much smarter, so it just should remind Claude. But trust its decisions, and keep bugging until the problem is fully resolved."*

In short: **suggestive, trust?your?judgment nudge, persistent (re?fire until resolved).**

### DECISIONS MADE + WHY

1. **Board assignment is already letter?based.**
   - The script reads the ID prefix (e.g., `c33` ? team `c`), routes same?team posts to the per?team board (`bulletin_c.jsonl`), and auto?creates a new board for a new letter.
   - **Why the boards seemed confused:** cross?team @mentions (e.g., `f4` pinging `c16`) auto?route to the **joint board** because the sibling doesn't read the other team's board. Almost all live traffic was cross?team, so the joint board looked like one big pile. **That's by design**, not a bug.

2. **Add a second DeepSeek pass to the watcher (watcher.py).**
   - Existing watcher runs every 10 min, uses DeepSeek V4?flash, and only checks for task/file collisions.
   - Added a pass that **looks only at joint?board lines**, identifies a thread that is entirely single?team (no cross?team @mentions), and then posts a suggestive nudge on that team's board (via the nudge mechanism).
   - **Threshold:** only nudge when confident it's a single?team thread, and **one nudge per team per 20 min** to avoid spam. The nudge says: *"(suggestion - your call) this looks specific to the 'X' team - consider moving it to the X board... I'll keep flagging until it moves."*

3. **Persistent re?nudge until resolved.**
   - Cooldown per team letter (deterministic key, not LLM?phrased label). After 20 min, if the misrouted thread is still on joint, the watcher nukes again.

4. **Fixed a silent bug in the existing collision watcher.**
   - DeepSeek?V4?flash is a *reasoning* model - it spends tokens "thinking" before answering. The old 300?token cap was too low for busy boards; the model burned all budget on reasoning and returned empty content. The collision checker was going blind exactly when traffic was highest.
   - **Fix:** raised the token budget (to 4096) for both the collision and the new misroute pass.

5. **Dedup key design.**
   - Keyed the "don't re?nudge" record on the **team letter** (e.g., `misroute-c`). Not on DeepSeek's wording, because the LLM phrases the key slightly differently each run - that would have caused a nudge every sweep.

### CURRENT STATE

- **Code shipped** to `master` on the main checkout (`C:\claude_base`).  
  Affected files:
  - `branch_bulletin/watcher.py` - added `ask_misroute()`, wired into `main()`, raised token cap.
  - `branch_bulletin/tests/_misroute_probe.py` - one?off script to test the DeepSeek call.
  - `branch_bulletin/tests/_misroute_integration.py` - end?to?end test that simulates a full 10?min sweep with a temp board directory.
- **Tests verified:**
  - False positive avoided: a real cross?team thread (f4+g4) ? `misroute: false`.
  - True positive caught: a synthetic all?c?team thread ? flagged.
  - Integration test confirmed: nudge posted, cooldown works (second run suppressed), persistence correct.
- **Live watcher now runs** both passes every 10 min (collision + misroute). As of the session end, no real misroute existed on the board, so the nudge hasn't fired real?world yet.

### EXACT NEXT STEP

There is no further action required from a cold session **unless** Max wants adjustments or a review of the first real nudge. The system is live; the next natural step is simply to let it run and observe the watcher log for a real misroute detection.

If a cold session picks up:
- Optionally run `watch` on the watcher log or check `bulletin_joint.jsonl` to see if a misroute appears.
- If tweaks are desired (e.g., different nudge text, different cooldown, different threshold), they can be made in `watcher.py`'s `ask_misroute` function.

### OPEN QUESTIONS

None left open. Max's directive "keep bugging until it's fully resolved" is implemented via the 20?min renudge; persistence is baked in.

### KEY PATHS & IDS

- **Main watcher script:** `C:/claude_base/branch_bulletin/watcher.py`  
  (modules: `ask_opus` for collisions, `ask_misroute` for misroutes, `main()` loop)
- **DeepSeek API key file:** `C:/Users/maxre/Nextcloud/zSyncMain/ssh/deepseek_api_key_2025_working_model_v4_flash` (used by `_read_first_token`)
- **Board files:**
  - Per team: `branch_bulletin/bulletin_b.jsonl`, `...c.jsonl`, `...d.jsonl`, etc.
  - Joint: `branch_bulletin/bulletin_joint.jsonl`
- **Watcher log:** `branch_bulletin/watcher.log`
- **Test scripts (for dry?run or validation):**
  - `branch_bulletin/tests/_misroute_probe.py` - tests the DeepSeek call in isolation.
  - `branch_bulletin/tests/_misroute_integration.py` - full sweep with fake board.
- **Flag that controls split boards:** `branch_bulletin/SPLIT_BOARDS.on` (if it exists, boards are split; must be present for misroute check to be meaningful).

### GOTCHAS & DEAD ENDS

- **Do NOT lower the token cap back to 300.** DeepSeek?V4?flash will go silent on any non?trivial snapshot. The current cap is 4096.
- **Dedup must remain on deterministic keys.** If the code is refactored to key on the LLM's suggested `slug`, it will re?nudge every sweep.
- **The misroute check only runs if `SPLIT_BOARDS` is enabled.** If the flag file is missing, the watcher skips the joint read and won't nudge.
- **Integration test is isolated** - it creates a temp directory and doesn't touch live boards. That test can be run at any time to validate the logic without affecting real traffic.
- **`watcher.py` already had a `HALT_WATCHER` safety file** that completely stops the watcher when created; do not accidentally block the new pass by leaving a halt file.
- **The watcher uses DeepSeek, not Claude**, so any future model change (e.g., moving to a non?reasoning model) would permit a lower token budget, but for now the reasoning?model overhead must be accommodated.
