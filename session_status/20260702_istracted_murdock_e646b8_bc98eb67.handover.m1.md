# Scribe handover - milestone 1 (~102K tokens)
# session: 20260702_istracted_murdock_e646b8_bc98eb67
# cwd: C:\claude_base\.claude\worktrees\distracted-murdock-e646b8
# written: 2026-07-02 12:28:46 by deepseek-v4-pro

# HANDOVER: VLC Player Slow Startup Investigation

---

## GOAL (Max's words)

Max reports that a previous Claude Code session successfully sped up VLC player startup (making it start "very fast"), but after a restart, VLC reverted to its original very slow startup behavior. The speed-up fix did not survive the restart. Max wants the fix applied properly so it persists.

---

## DECISIONS + WHY

1. **Search for prior VLC work first** - Claude searched the compaction knowledge base (worklog), the entire `C:\claude_base` tree with grep, and Memex (long-term memory). No prior VLC-related work was documented anywhere. This means whatever the previous session did is not recoverable from institutional memory.

2. **Check the plugin cache** - Claude identified this machine runs the **32-bit** VLC (at `C:\Program Files (x86)\VideoLAN\VLC`), and confirmed `plugins.dat` exists in the plugins folder. A missing or stale plugin cache is a common cause of slow VLC startup because VLC rescans all plugins on every launch.

3. **Time core VLC startup** - Using `vlc.exe -I dummy --no-plugins-cache --reset-plugins-cache`, core init measured ~0.4 seconds. Plugin cache is healthy and not the source of slowness.

4. **Time Qt GUI startup** - Real GUI launch (`vlc.exe vlc://quit`) also completed in under 1 second. Tested with and without media library scanning, update checks, etc. Still fast.

5. **Check active VLC configuration** - Read `vlcrc` and `vlc-qt-interface.ini` from `%APPDATA%/vlc`. No obviously slow settings were found.

6. **Cannot reproduce the slowness** - After all testing, VLC starts in <1 second from every angle. The bug is not currently manifesting.

---

## CURRENT STATE

- **Investigation is stalled:** Claude cannot observe the "very slow start" behavior. All timing tests show VLC launching in <1 second.
- **Plugin cache is intact** at `C:\Program Files (x86)\VideoLAN\VLC\plugins\plugins.dat`.
- **VLC config is at** `%APPDATA%\vlc\vlcrc` (user-specific settings).
- **No prior session work on VLC was ever recorded** in worklog, project files, grep results, or Memex - the earlier session's changes are a mystery.
- **Session ended on an open question to Max** asking for clarification.

---

## EXACT NEXT STEP

**Wait for Max to answer two clarification questions** (see below). Once answered, the next action depends on the response:

- If slowdown is **after Windows reboot**, the issue likely involves the OS discarding the plugin cache, font cache, or some system-level caching. The fix might involve regenerating the plugin cache as a startup task.
- If slowdown is **after VLC close/reopen**, the issue likely involves VLC overwriting a config change on exit (e.g., a setting the previous session changed while VLC was running that got wiped when VLC wrote its final state to `vlcrc`).
- Once the trigger is known, Claude should re-time VLC startup immediately after that trigger to reproduce and profile the slowness.

---

## OPEN QUESTIONS (awaiting Max)

1. **How many seconds does VLC take to show its window when it's slow?** (e.g., 5 seconds? 30 seconds? A rough number matters for profiling.)
2. **What does "after restart" mean?** Restarting VLC (closing and reopening the program) or restarting Windows (rebooting the machine)?

These determine which mechanism is involved (config overwrite vs. system cache invalidation).

---

## KEY PATHS / IDs

| Item | Path/Value |
|---|---|
| VLC executable | `C:\Program Files (x86)\VideoLAN\VLC\vlc.exe` (32-bit) |
| Plugin cache | `C:\Program Files (x86)\VideoLAN\VLC\plugins\plugins.dat` |
| Plugin folder | `C:\Program Files (x86)\VideoLAN\VLC\plugins\` |
| User config | `%APPDATA%\vlc\vlcrc` |
| Qt interface config | `%APPDATA%\vlc\vlc-qt-interface.ini` |
| Cache generator | Not found (`vlc-cache-gen.exe`, `cachegen.exe` absent) |
| Worklog | `C:\claude_base\compaction_kb\scripts\worklog.py` - no VLC entries |
| Memex search tool | `mcp__876d399f-e171-42f5-a4dd-c5b1a0d2ca4a__memex_search` - no results |
| cwd for session | `C:\claude_base\.claude\worktrees\distracted-murdock-e646b8` |

---

## GOTCHAS / RULED OUT

- **Plugin cache is NOT the issue** - it exists and is functional. Core init is fast.
- **Media library scanning is NOT the issue** - Qt GUI test with `--no-media-library` was still fast.
- **Update check is NOT the issue** - tested without it, still fast.
- **Slowdown is intermittent or trigger-dependent** - it does not occur in a fresh shell environment during this session. The trigger ("restart") needs to be identified to reproduce it.
- **No prior work exists in records** - whatever the previous session did to speed up VLC left zero documentation. It may have been a transient change (e.g., editing vlcrc while VLC was closed, or a command-line flag that wasn't persisted to config).
