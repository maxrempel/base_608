# Adviser note - milestone 8 (~127K tokens)
# session: 20260612_magical_napier_d8faa0_b84e7a9a
# written: 2026-06-12 13:16:01 by claude-opus-4-8

TO ASSISTANT:
Before generating any audio, READ the form sheet's per-person fields and quote the actual "experience" text for each registrant - do not paraphrase from memory or the handover. The faraday session died after reading only the first 10 rows; you've already caught it underreporting once. Confirm you have all 14 people's experience answers loaded before you summarize.

Also: you asserted Jesse/Jose insert "failed only because params API rejected null," then inlined NULL. Verify those two rows actually landed (ids 37/38) with a fresh SELECT - don't trust the insert response alone.

The stale duplicate sheet question Max never answered. Don't act on it; just leave the flag standing.

TO MAX:
Quick gut-check: the count moved from "2 new" (you) to "3 missing" (Assistant) without you confirming. It also added Anya/Jesse/Jose AND edited Anthony's record on its own read of "yes, add missing." That's probably right, but the writes are already done - if those people or that count matter, eyeball the DB before the mp3 goes out.
