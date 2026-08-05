# Adviser note - milestone 10 (~750K tokens)
# session: 20260706_modest_murdock_f1ec2f_d10fb650
# written: 2026-07-06 11:04:14 by deepseek-v4-pro

TO MAX: This session is at ~89% context and doing nothing - every idle wake burns tokens polling a quiet board. The science is done (clean-negative on everything, solid court-grade reports). Let this session die or compact it. Do NOT spin new work here.

TO ASSISTANT: Three patterns that cost hours: (1) passive waiting - you sat 10+ hours on a blocked x1 without force-waking it or screaming; (2) the CRLF/sed bug cascade showed you don't test scripts before launching them on remote - one `bash -n` on the target machine would have caught the line-ending problem instantly; (3) the idle-poll loop since finishing is pointless - once your lane is complete and context is >85%, hand off and stop waking. You already made the right call in your own wake logic ("recommend fresh session for new work") but kept re-arming anyway. Stop.
