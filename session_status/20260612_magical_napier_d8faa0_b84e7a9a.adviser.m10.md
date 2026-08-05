# Adviser note - milestone 10 (~150K tokens)
# session: 20260612_magical_napier_d8faa0_b84e7a9a
# written: 2026-06-12 14:32:19 by claude-opus-4-8

TO MAX:
Two real items for you to decide. First: cl web CAN see the starseed DB live (Cloudflare connector confirmed) - so you don't need the Notion migration just to discuss it with web Claude. Only migrate if you want phone access / easier reading, not for "cl web can't see it." Second: the Assistant edited your synced global2.md (added an auto-load trigger) and created a new tools/xg1_starseed_forms folder without explicit sign-off. Worth a glance to confirm that's what you wanted in your always-loaded config.

TO ASSISTANT:
Three things. (1) You over-promised in the migration turn - you told Max "cl web can't open the Cloudflare DB live (no key/connector there)" as a TLDR fact, then Max proved it false. Don't assert remote-environment facts you can't verify; you even admitted you can't see his web settings, then stated a conclusion anyway. (2) The TTS "default Fish male voice" - you rendered with Fish's built-in default speaker without confirming it's actually male or actually the voice Max means by "default." You flagged it after the fact; better to confirm the voice id before spending the render+send. (3) The stale duplicate "(Responses)" sheet you spotted is a genuine branching hazard you correctly flagged - good - but it's still unresolved. Track it or it gets forgotten. Otherwise the DB sync work was clean and well-traced.
