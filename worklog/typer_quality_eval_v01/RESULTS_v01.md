# Typer accuracy-first decoding evaluation

Last edited: 2026-07-31 by Codex (GPT-5.6 SOL)

## Question

Which Faster-Whisper Large V3 decoding settings best preserve Max's literal commands,
especially pronouns and small meaning-changing words, without losing local speed?

## Evidence

The test used Max's saved 56.5-second incident recording from 2026-07-31. One model was
loaded once on Taygeta's GPU and the same normalized MP3 was transcribed six ways, forced
to English. No audio was trimmed. The temporary remote copy was removed after testing.

## Result

`beam_size=1`, `temperature=0.0`, and normal prior-segment context was the most literal
configuration. It retained `free`, `fix`, pronouns, and complete punctuation. Runtime was
1.76 seconds in the isolated matrix and 1.92 seconds through the deployed HTTP service.

Beam sizes 3 and 5 changed `free` to `three`, reordered `numeric plus`, and sometimes
changed `fix` to `fixed`. Disabling context lost punctuation and duplicated a phrase.
Hotwords severely degraded the whole transcript and are rejected for this workflow.

The previous production settings also forbade repeated three-word sequences, applied a
non-default repetition penalty, disabled prior context, and deleted stock-looking phrases
after transcription. All four behaviors are now inactive. Numpad Plus and Num4 are forced
to English because Max's accented English was once classified with Russian probability
0.876 versus English 0.059 and rendered phonetically in Cyrillic. Right Ctrl remains the
dedicated Russian key.

## Deployment

The chosen server was deployed to Taygeta (CUDA primary) and Asto (CPU fallback). Both
health checks passed. Plus and Num4 were safely reloaded after a dictation-idle interval.
`test_accuracy_contract_v01.py` enforces the selected decoding options, English bindings,
disabled phrase cleanup, and the exact three-leading-space paste prefix.
