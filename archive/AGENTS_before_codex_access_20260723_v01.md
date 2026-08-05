# claude_base project rules for Codex and Claude

Max = "I/my/me". The active AI agent = "you".

## Shared dirty checkout safety

This repository is worked on by many sessions at once. The main checkout is normally dirty with other sessions' files and runtime state.

- Stage only explicitly named files changed for the current task.
- Never use `git add -A`, `git add .`, or `git commit -am` here.
- Never run broad noisy diagnostics such as unrestricted `git status`, recursive listings, or giant logs in this dirty checkout. Scope commands to exact paths, cap output, or write raw output to a local file and summarize only the useful facts.
- Never discard, overwrite, clean, move, or commit unrelated changes.
- Prefer an isolated worktree for broad changes. If working in the shared checkout, keep the edit set narrow and inspect the exact staged diff.
- Runtime litter, generated data, backups, media, databases, and large outputs do not belong in Git.
- The repository pre-commit guards are required. Do not bypass them unless Max explicitly authorizes a genuine exception.

## Commit and push discipline

- Commit meaningful completed changes with a thorough message stating scale, major changes, and testing status.
- Merge and push authorized completed work without asking.
- A push never authorizes sweeping sibling changes into the commit. Resolve only real conflicts involving files owned by this task.

## Why this is strict

Two previous mass-add commits swept large genomic data and thousands of runtime files into Git, blocking pushes and breaking fresh checkouts. Sharing files is normal; indiscriminate staging is the danger.
