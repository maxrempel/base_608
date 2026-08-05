---
title: MOMA producer session identity audit
version: 03
date: 2026-07-29
last_editor: Codex (GPT-5.6 SOL)
privacy: private-authorized
---

Audit C:\moma for the partially implemented producer-session identity feature.
Read only the relevant producer identity, fire_job, Storyboard 4 pool, and
Storyboard 4 badge code in the combo runner and sound assembly source trees.

Return a concise implementation review in result.md:
1. What already works and what is missing in the chain from producer metadata
   through live D1 and the Storyboard 4 API to a primary-spine badge.
2. The safest minimal schema and migration route, assuming the public D1 HTTP
   API rejects ALTER TABLE.
3. Specific failure modes or compatibility traps.
4. A compact recommended patch plan with exact files and functions.

Do not edit the repository. Keep the review limited to architecture and code.
