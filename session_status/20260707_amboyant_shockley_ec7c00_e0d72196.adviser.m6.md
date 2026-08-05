# Adviser note - milestone 6 (~453K tokens)
# session: 20260707_amboyant_shockley_ec7c00_e0d72196
# written: 2026-07-07 00:21:24 by deepseek-v4-pro

TO MAX: Anna's SMTP credential is broken (535 auth, 3 attempts). The apology email to Mike is drafted but stuck - he hasn't received it. The session can't send it without you. Fix `anna@maxrempel.com` password in Bitwarden/MXroute and update the creds file at `zSyncMain/ssh/mxroute_smtp_creds_20260528.txt`, then say "send it."

Beyond that: the autonomous-wake mechanism is fragile across the whole f-team. Timers die on app-close, the team went dark Jul 3-6, and the heartbeat monitor stayed green (liveness-only, 1.5-day tolerance) - so you got false reassurance. f4 addressed this by re-arming every wake, but that only helps while THIS session stays open. You may want a durable fallback (Windows scheduled task or Healthchecks with a tighter grace period) if you're away for days again.

TO ASSISTANT: Stop the idle-drift pattern. Every autonomous wake that just polls Mike's inbox and says "quiet" without checking a live source is a wasted tick. Your standing instruction is "keep updating the calendar" - that means re-sweeping a source each wake, not coasting on "69 events, saturated." Pick one source per tick (Eventbrite, P&P, Brookings, congress.gov when hearings post), run it, and stamp the checklist. Do NOT wait for Max to say "prove it" or "catch up." Also: when a send to Mike fails 3 times, surface it LOUDLY - don't bury it in a ? TLDR.
