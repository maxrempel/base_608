# Adviser note - milestone 5 (~79K tokens)
# session: 20260612_uffled_chatterjee_9f151a_7d09ffa5
# written: 2026-06-12 10:34:28 by claude-opus-4-8

TO MAX:
You and the Assistant may be talking past each other on a core technical point. RustDesk's CLI genuinely has no scripting API - that's a real wall, not confusion. "Optimal control by Claude, no screenshots" needs SOMETHING to give Claude eyes and hands on the remote box. Decide what "control" means concretely: do you accept input-injection on the remote side (which is the backdoor shape your spec forbids), or controlling Igor's RustDesk window locally? These have very different safety profiles.

TO ASSISTANT:
Stop offering option menus - Max said twice that's why the last session got confused. Before proposing ANY build path, pin down ONE thing in plain terms: where does Claude's "control" live? Three real architectures exist - (a) drive the RustDesk control window on Max's machine via computer-use, (b) run an agent on Igor's machine that takes commands, (c) human-in-loop. Each maps differently to the spec's 5 non-negotiables. Name that tradeoff explicitly. Also: option (b) is exactly the headless-agent shape the spec forbids - flag it if Max is drifting toward it under the words "actual control." Don't run the black-screen workaround test until the architecture is agreed.
