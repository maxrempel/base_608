# Adviser note - milestone 11 (~169K tokens)
# session: 20260616_optimistic_napier_fe7263_8bc1b45b
# written: 2026-06-16 07:50:55 by deepseek-v4-pro

TO MAX: The full-catalog remap is only 33% done (6,992 of 21,438). The restarted job should finish in a few hours, but it was interrupted once already. Make sure the next session publishes what's done immediately - don't let it wait for 100% again. Also: the "unindexed videos may have YouTube captions" is a real gap those videos have no cached transcript file on Pine, so the remapper can't touch them without an extra download step first.

TO ASSISTANT: Before splitting, do three things. (1) Run publish_catalog.py NOW to ship the 6,992 completed timings live - don't batch-wait for 100%. (2) Commit the throwaway research scripts from _work/ (qc_starts.py, exp_cheap.py, analyze_windows.py) so the split sessions have them. (3) Fix deploy_catalog.py to reject unknown flags instead of silently falling back to its default file - that untimed-catalog deploy was a near-miss, and the script is still dangerous as-is. (4) Drop the autonomous heartbeat timer immediately - the job is incomplete and needs active supervision, not passive re-arming.
