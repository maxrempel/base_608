# Typer transcription-quality investigation

Last edited: 2026-07-31 by Codex (GPT-5.6 SOL)

Analyze this evidence and propose a compact, low-risk pilot plan. Do not edit files.

Problem: Max reports that Typer's audio is excellent but transcription is sloppy. It substitutes semantically plausible generic sentences and changes pronouns, especially `me` or `you` into `we`, which can reverse instructions to an AI agent.

Current main Numpad Plus path:

- Faster-Whisper Large V3 on Taygeta, with Asto fallback.
- Forced English or Russian after constrained language detection.
- `beam_size=1`, `condition_on_previous_text=False`, `no_repeat_ngram_size=3`, and `repetition_penalty=1.15`.
- These settings were added primarily for speed and to prevent repetition loops.

Current official OpenAI documentation recommends `gpt-transcribe` for completed recordings. It supports `prompt`, `keywords`, and expected `languages`.

Measured same-audio examples:

- 37-second clip: current Taygeta Large V3 took 2.72 seconds; `gpt-transcribe` took 4.81 seconds unprompted and 1.66 seconds on a second prompted call. Outputs were similar, but GPT had cleaner capitalization and grammar.
- 12.8-second clip: current Taygeta Large V3 took 1.33 seconds and misspelled Taygeta twice. Asto took 5.39 seconds and misspelled it. `gpt-transcribe` with a strict verbatim prompt plus keywords took 2.95 seconds, spelled Taygeta correctly twice, and preserved `You should improve the logs`.
- Prompt used: transcribe exactly and verbatim; do not paraphrase, summarize, repair grammar, or substitute generic wording; preserve I/me/my/you/your/we/us/our exactly; speaker dictates technical instructions to AI assistants.
- Keywords included Taygeta, Aneta, Anna, Codex, Claude, MOMA, Fish Audio, and Typer; expected languages were English and Russian.

Need: identify likely failure mechanisms, rank candidate fixes, and propose a small A/B pilot that protects Max from regressions. Prefer accuracy over shaving one or two seconds, but preserve reasonable latency. Do not recommend an LLM text post-processor that could further rewrite pronouns. Include a concrete acceptance test for pronoun fidelity and uncommon technical terms.

Write only the analysis and pilot plan to `result.md`.
