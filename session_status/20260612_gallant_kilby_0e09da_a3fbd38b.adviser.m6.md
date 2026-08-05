# Adviser note - milestone 6 (~94K tokens)
# session: 20260612_gallant_kilby_0e09da_a3fbd38b
# written: 2026-06-12 11:50:27 by claude-opus-4-8

TO ASSISTANT:
You burned ~20 tool calls guessing at Lak's identity and IP before searching Memex/docs for fundamentals - which is where the real cause (wrong boot device) actually was. That's backwards: pull the core facts FIRST on infrastructure you don't have memorized. Stop the LAN sweeps and repeated SSH/curl probes; they told you nothing new after the third try.

Now Max asks "how to reset boot?" on a Dell Precision T3600. Answer plainly: power on, tap F2 for BIOS setup (or F12 for one-time boot menu), fix the boot order so the OS disk is first / remove the USB. Don't probe the network for this - it's a physical/BIOS step at the box. Keep it short.

When Lak comes up, do the one useful housekeeping thing you promised: record its actual LAN IP into the infra map so the next session isn't blind.

TO MAX:
You're at the BIOS, not the network. F12 at the Dell splash gives a one-time boot menu - pick the OS disk; or F2 to set permanent boot order, then pull the USB stick that hijacked it. Services should self-start after that.
