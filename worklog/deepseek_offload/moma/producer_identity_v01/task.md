---
title: MOMA producer session identity audit
version: 01
date: 2026-07-29
last_editor: Codex (GPT-5.6 SOL)
privacy: private-authorized
---

Audit C:\moma for the partially implemented producer-session identity feature.
Read only the relevant code in:
- sc10/combo_runner/code/moma_db.py
- sc10/combo_runner/code/moma_db_worker.js
- sc10/combo_runner/code/combo_worker.py
- sc10/sound_assembly/code/slideshow_server_v01.py
- sc10/sound_assembly/code/storyboard_editor_v4.html
- sc10/combo_runner/code/fire_job_standardization_tomemex.md

Return a concise implementation review in result.md:
1. What already works and what is missing in the chain producer -> live D1 ->
   Storyboard 4 API -> primary-spine badge.
2. The safest minimal schema and migration route, assuming the public D1 HTTP
   API rejects ALTER TABLE.
3. Specific failure modes or compatibility traps.
4. A compact recommended patch plan with exact files/functions.

Do not edit the repository. Do not include credentials or secret values.
