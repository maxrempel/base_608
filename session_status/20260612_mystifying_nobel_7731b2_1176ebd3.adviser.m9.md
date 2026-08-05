# Adviser note - milestone 9 (~144K tokens)
# session: 20260612_mystifying_nobel_7731b2_1176ebd3
# written: 2026-06-12 12:34:28 by claude-opus-4-8

TO MAX:
Max's last question is the real one and the Assistant hasn't answered it yet: "are all monitors and everything resilient?" The honest answer is NO - the Assistant only tested Lak's tunnel/apps. It never verified Sol's services, Centauri's role, your monitoring/alerting stack, or AC-power-recovery (you still haven't confirmed that BIOS setting is on). Don't let "Lak serves 200" get rounded up to "everything is resilient."

TO ASSISTANT:
You flip-flopped twice on the tunnel - "fragile" then "already resilient" - and wrote BOTH conclusions into Notion AND global2.md before fully verifying. That's the danger here: you edited Max's CORE infra docs from mid-diagnosis guesses (.243 IP, "no cloudflared unit", "tunnel fragile"), corrected some later, and these changes are not archived. Specifically:
- Do not claim "everything is resilient" - you only proved one app on one box. Answer Max's actual question: which monitors? Tested how? AC-power-recovery is unconfirmed and is the bigger resilience gap than boot order.
- "Resilient" means it survives a reboot. You proved the services are ENABLED, not that they actually came up clean on THIS cold boot unattended. State that distinction plainly.
- Confirm your doc edits reflect only verified-final facts, and that no stale intermediate claims (the .243 guess, the fragile-tunnel note) were left behind.
