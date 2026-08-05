# Codex Session Board implementation review

Last edited: 2026-08-01 by Codex (GPT-5.6 SOL)

Review the public Codex++ source and its tweak API for a minimal Windows tweak
that adds a full-screen Kanban selection board for existing Codex tasks. Focus
on the safest supported APIs for: adding an in-app entry point, listing existing
tasks, navigating to an existing task, persisting tweak-owned JSON data, and
HTML drag-and-drop. Identify compatibility risks and propose a minimal file
layout and deterministic tests. Do not include credentials. Do not modify or
install anything. Return a concise implementation brief in result.md.

The reviewed checkout is:
`C:\claude_base\tools\codex_session_board\upstream\codex-plusplus`
at release tag `v1.0.0`, commit
`f98e7e9d1fa068dde9e0dddfb43b128acb4e2fd7`.

Reference tweaks are in sibling directories `horizontal-tabs` and
`project-home`. Inspect only files needed for this brief.
