# Scribe handover - milestone 1 (~96K tokens)
# session: 20260626_focused_ride_1f38f1_856ff2ef
# cwd: C:\claude_base\.claude\worktrees\focused-ride-1f38f1
# written: 2026-06-26 15:20:33 by deepseek-v4-pro

# Handover - Video / Large File Migration from C: Drive

**Session** `focused-ride-1f38f1`  
**Turns so far:** 1 (Max ? Claude)  
**Status:** Awaiting Max's answers. No actions taken yet.

---

## GOAL (Max's words, lightly condensed)
Max wants to migrate video files and other large files off the C: drive. He's unsure about the best location. He mentioned two drives: "Lakarian" (probably the server host Lak, which he believes is full) and "Santuri" (likely Centauri). He's not sure if he wants to keep everything in Nextcloud and might want some files outside Nextcloud. He's uncertain about the whole approach.

## DECISIONS + WHY
No final decisions yet. The assistant proposed a single best-target candidate with rationale:
- **Target:** Centauri's **teal16** drive (16 TB, ~12.8 TB free, always-on over LAN SSH).
- **Why:** It's the biggest storage available, already hosts master backups for Tamza/Hucolo videos, and is suited for bulk video. Alternatives were ruled out for being too small (Dax 79 GB), down (Sol), or already busy (Lakarian with Nextcloud/apps).

## CURRENT STATE
- No investigation commands have been run (no SSH, no `df`, no file listing).
- The assistant has asked two clarifying questions, still unanswered. No migration plan has been created.

## EXACT NEXT STEP
Wait for Max to answer these two questions (or ask new ones):
1. **Storage location style:** Should the videos go inside Centauri's Nextcloud (synced everywhere, but consumes Nextcloud space) or as a plain folder on Centauri's D: drive (SSH-accessible, NOT synced)?
2. **Scope:** Roughly how much data is being moved, and which specific C: folders hold the video/large files?

Once Max clarifies those, the assistant will SSH into Centauri to confirm live free space, then design a migration plan.

## OPEN QUESTIONS
- Does Max want the data in Nextcloud or outside it? (He feels unsure, needs to decide.)
- What's the total volume and source paths?
- Are there any other drives or NAS targets beyond Centauri that might be relevant?
- Does Max need the assistant to inspect C: drive contents first to identify candidates?

## KEY PATHS / IDS / NAMES
- **C: drive** - source, contents unknown beyond "video files and other large files"
- **Centauri** - always-on LAN server, reachable via SSH; holds:
  - Drive `teal16` (likely mount point or device) - 16 TB, ~12.8 TB free
  - Presumably a D: drive (plain Windows drive letter for bulk storage)
- **Lak / Lakarian** - server host running Nextcloud and apps; considered too full for bulk video
- **Dax** - small drive (~79 GB), ruled out
- **Sol** - possibly a host/drive that's currently down
- **Tamza/Hucolo videos** - existing master backups on teal16, confirm prior workflow
- **Nextcloud** - running on Lak; may be an option if Max wants sync

## GOTCHAS & DEAD ENDS RULED OUT
- **"Santuri"** was interpreted as **Centauri** - if that's wrong, Max will correct.
- Dax (79 GB) and Sol (down) were explicitly ruled out as target candidates.
- Lakarian was identified as already occupied (Nextcloud + apps) and not ideal for heavy video.
- The assistant assumed plain D: folder is the default for heavy video to avoid sync overhead, but will defer to Max's preference. No sync vs. plain decision made yet.
