Review the MoMA ReelMaker frontend implementation in:
- C:\moma\sc10\combo_runner\code\runner_page.html
- C:\moma\sc10\combo_runner\code\runner_core.js
- C:\moma\sc10\combo_runner\code\runner_core.css

Goal: Add an easy selection workflow for reels: select all visible reels, select individual reels, clear selection, approve all visible, junk all visible, approve selected, and junk selected. Reuse the existing per-reel POST endpoints /api/video/approve/<id> and /api/video/junk/<id>. Do not edit files. Return a concise implementation design, likely edge cases, and focused tests. Preserve the existing Imager grid selection behavior.
