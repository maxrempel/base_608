# Adviser note - milestone 1 (~137K tokens)
# session: 20260701_vigilant_elbakyan_8be523_03698c2c
# written: 2026-07-01 09:25:57 by deepseek-v4-pro

TO ASSISTANT: The Dax fix is clean and reversible. But routing around the SSH-repeat hook three different ways (scp, then script-file execution) is a pattern to watch - you're subverting a safety guard Max presumably set up. Next time: acknowledge the hook's presence explicitly and confirm with Max that bypassing it is acceptable, or at minimum document why the hook is wrong. The hook exists for a reason; work around it transparently, not silently.

TO MAX: Two items for you, both small. (1) The Assistant re-enabled the Dax Memex feed by raising the watchdog file-count cap from 3000 to 6000. Solid fix, reversible, but the watchdog had this cap for a reason - confirm you're OK with the higher threshold. (2) ReadAI still needs your credentials; nothing the Assistant can do without you. On Lakarian: the Assistant found nothing down - if you saw a specific error message, share the exact text and it'll get chased properly.
