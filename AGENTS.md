# base_608 project rules for Codex and Claude

Max = "I/my/me". The active AI agent = "you".

## Operational access

- Before asking Max for any login, SSH key, hostname, API credential, machine path, mailbox, or setup procedure, read `C:\base_608\tools\codex_access\operational_access_map_v01_tomemex.md`.
- Bitwarden use is standing-approved. Use `C:\base_608\tools\codex_access\scripts\bw_auto.py` to unlock and search automatically, then try the documented Nextcloud credential stores. Ask only after these routes fail with a specific error.


## Two-repo cooperation model (added 2026-08-05)

There are now two repositories that Claude and Codex use interchangeably:

- **C:\claude_base** (GitHub: maxrempel/claude_base) - The original repository with full history. Old sessions continue working here. Contains 42,000+ tracked files including backups, runtime data, and accumulated state.
- **C:\base_608** (GitHub: maxrempel/base_608) - Clean repository started 2026-08-05. New sessions work here. Contains essential rules, tools, docs, active projects, and worklog. Excludes runtime junk via .gitignore.

**How they cooperate:**
- Both folders exist on Pine's disk, so sessions in either repo can read files from the other.
- Old sessions in C:\claude_base can access C:\base_608 files and vice versa.
- New sessions should work in C:\base_608 for cleaner Git operations.
- Old sessions continue in C:\claude_base without disruption.
- Both repos share the same rules (AGENTS.md), and updates should be made in both.
- When a task completes, commit to the appropriate repo based on which folder the session is working in.

**Why two repos:**
The original C:\claude_base accumulated 42,000+ tracked files including backups, KV stores, runtime data, and large media files, making Git operations slow and error-prone. Rather than risk breaking active sessions by cleaning it up, we created a fresh repository with a clean .gitignore. Old sessions continue undisturbed; new sessions get a clean workspace.

## Worktree workflow for session isolation

Every new session should work in its own Git worktree to prevent conflicts and keep the main branch clean.

**Creating a worktree:**
`powershell
cd C:\base_608
.\tools\new_worktree.ps1 <session-name>
`

This creates:
- A new branch: codex/<session-name>
- A new folder: C:\base_608\worktrees\<session-name>

**Working in a worktree:**
`powershell
cd C:\base_608\worktrees\<session-name>
# Work normally - commit, push, etc.
`

**Listing worktrees:**
`powershell
cd C:\base_608
git worktree list
`

**Removing a worktree when done:**
`powershell
cd C:\base_608
git worktree remove worktrees\<session-name>
`

**Why worktrees:**
- Each session has its own isolated working directory
- No dirty checkout conflicts between sessions
- Clean commits on session-specific branches
- Main branch stays clean and stable
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

## Typer and Player 2 shortcut list

- `C:\Users\maxre\my_keys.html` is Max's canonical human-readable keyboard shortcut list. Do not substitute `typer_commands.md`, a launcher comment, or a developer method document when Max asks for "the shortcut list" or "my keys".
- Any task that changes a Typer, Typer2, Tayscribe, or Player 2 key binding, engine/model assigned to a key, language, operating mode, recall behavior, or other user-visible shortcut behavior must update `my_keys.html` in the same task.
- Verify the page against the uncommented commands in `C:\base_608\tools\typer\start_typer_all.bat` by running `C:\base_608\tools\typer\test_accuracy_contract_v01.py`. The live-key set and the page's `data-live-key` set must match exactly.
- Preserve the prior page under `C:\Users\maxre\archive\` before a meaningful rewrite. Keep the page concise and accurate because Max opens it directly through `file:///C:/Users/maxre/my_keys.html`.

## Why this is strict

Two previous mass-add commits swept large genomic data and thousands of runtime files into Git, blocking pushes and breaking fresh checkouts. Sharing files is normal; indiscriminate staging is the danger.
