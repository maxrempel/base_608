# MoMA Storyboard 4 merge audit

Review the current files:
- C:\moma\sc10\sound_assembly\code\storyboard_editor_v2.html
- C:\moma\sc10\sound_assembly\code\storyboard_editor_v3.html
- C:\moma\sc10\sound_assembly\code\slideshow_server_v01.py

Goal: create a safe Storyboard 4 test candidate that preserves every current
Storyboard 2 behavior and UI feature, but moves pile scene/arrangement/role/junk
filtering to the server as Storyboard 3 attempted. Storyboard 2 and all current
canonical routes must remain untouched. Storyboard 4 should have its own HTML
file, route, and versioned server endpoint if needed.

Audit the exact data-contract differences between /api/approved_images and the
existing /api/sb_pool. Identify anything /api/sb_pool loses or changes, including
approved input stills, completed output media, field names/statuses, named
projects, scene scoping, arrangements, junk state, curated bin order, automatic
placement, and quiet polling. Recommend the smallest parity-safe implementation
and focused tests. Do not edit files. Write a concise result.md.
