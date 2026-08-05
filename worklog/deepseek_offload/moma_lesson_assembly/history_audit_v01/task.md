# MOMA Lesson 1 assembly failure-history audit

Last edited: 2026-08-01 by Codex (GPT-5.6 SOL)

## Objective

Audit the complete local Lesson 1 title-slide, closing-slide, music-overlay, and synchronization failure history. Produce a concise but thorough evidence inventory for a reusable cross-agent skill. Focus on what failed, why, how it was detected, why earlier quality control falsely passed, and what deterministic prevention and acceptance gates are required.

## Scope

Read only relevant files under:

- `C:\moma\sc10\sound_assembly\code`
- `C:\moma\tmp\lesson1_*` where metadata, reports, or logs are small and relevant
- `C:\Users\maxre\Nextcloud\ai_images\kazarian_episode\sound\lesson1_production\music_mix` but avoid broad hydration and large media reads except narrow ffprobe-style metadata if already local
- `C:\Users\maxre\.claude\skills\musicunder\SKILL.md`

Prioritize scripts and records mentioning v10, v12-v15, v116-v123, `LOSSLESS_clean`, `COMPLETE`, slides, timestamps, AAC, edit lists, skip samples, `asetpts`, `aresample`, `amix`, QC, correlation, and synchronization.

## Required output

Write `result.md` with:

1. Artifact and version chronology.
2. A bug matrix: symptom, affected versions, technical root cause, enabling process mistake, detection, permanent prevention.
3. The proven v123 architecture and why it preserves synchronization.
4. All false-positive QC patterns and stronger replacement gates.
5. Exact reusable media-format and timing invariants.
6. A recommended foolproof workflow and fail-closed promotion policy.
7. Specific defects or obsolete advice in the old `musicunder` skill.
8. Any uncertainty clearly labeled.

Do not draft generic filler. Cite exact local paths and concrete values where evidence supports them. Do not include credentials or unrelated private information.
