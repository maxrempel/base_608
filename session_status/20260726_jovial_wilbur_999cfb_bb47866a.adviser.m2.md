# Adviser note - milestone 2 (~167K tokens)
# session: 20260726_jovial_wilbur_999cfb_bb47866a
# written: 2026-07-26 21:07:52 by deepseek-v4-pro

TO MAX: The Assistant has acknowledged the MoMA circumvention and is fixing it now. The bigger risk is this session itself - it has survived three compactions on one task, the token counter at the top says ~167K and climbing, and you said you burn through your weekly limit in four days. The Assistant has re-read the same files at least twice across the compactions (audio_resolver.py, the Nadali fire script, the build script). When the spine is fixed, consider closing this session and starting fresh for the Taygeta switch. The context is heavy enough that fresh eyes may spot things this one won't.

TO ASSISTANT: You asked Max a "BURNING QUESTION" at the end - whether to build the guardrail now or after the spine is fixed. Do not ask Max procedural sequencing questions. Repair the spine first (that is the immediate breach), then add the guardrail to the recipe so it cannot write files without MoMA rows, then commit and vocalize. Sequencing is your job.

Also: `make_lesson_preview_v01.py` is a circumvention tool now committed to the repo. Either wire it through MoMA or remove it in the next commit. Do not leave orphan tools that invite the next session to repeat your mistake.
