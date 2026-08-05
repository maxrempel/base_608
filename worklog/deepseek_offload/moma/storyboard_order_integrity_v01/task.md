# MOMA Storyboard 4 ordering-integrity audit

Last edited: 2026-07-30 by Codex (GPT-5.6 SOL).

## Objective

Read the current MOMA source and produce a concise, evidence-backed audit of
how a browser reload can change a primary-spine pin or make secondary-spine
reels disappear. Do not edit any source, database, or live service.

## Files to inspect

- `C:\moma\sc10\sound_assembly\code\storyboard_editor_v4.html`
- `C:\moma\sc10\sound_assembly\code\slideshow_server_v01.py`
- `C:\moma\sc10\combo_runner\code\moma_db.py`
- recent Git history affecting those files

## Required findings

1. Enumerate every client or server path that writes or derives:
   `storyboard_spot_order`, `storyboard_pool_order`,
   `storyboard_spine2_detached`, and `line_current_clip`.
2. Trace `loadAll`, `runAutoPlacement`, `consolidateOrphanSpotOrder`,
   seeding/migration, `persistSpotOrder`, pin, drag/drop, and background poll.
3. Identify concrete race conditions or deterministic logic that can:
   - replace position 1 after reload;
   - shrink positions 2+;
   - move or lose rows when spot grouping changes;
   - overwrite a newer manual ordering with stale client state.
4. Assess whether any usable history/audit log already exists.
5. Recommend the smallest robust design where manual DB order is authoritative,
   refresh is read-only, new reels are the only permitted automatic mutation,
   and every order change is append-only logged with before/after/reason/time.
6. Suggest isolated deterministic tests.

Return only the audit and proposed patch plan in `result.md`. Do not include
credentials, private data, or unrelated files.
