# Scribe handover - milestone 1 (~101K tokens)
# session: 20260626_cranky_euclid_9c3e48_3d14a5bb
# cwd: C:\claude_base\.claude\worktrees\cranky-euclid-9c3e48
# written: 2026-06-26 15:46:13 by deepseek-v4-pro

# HANDOVER - Video Publishing Registry System (B9 Session)

---

## GOAL (Max's own words)
Max is cleaning up C drive space. There are "tons of videos" in `C:\Users\maxre\Videos\max talks\VTP videos to publish` that need "proper treatment" - a system that has "not been yet developed." YouTube is closing some of his channels, so keeping videos only on YouTube is not safe. He wants a **tracking system for good videos that need publishing somewhere** - backup channels, backup places, other publishing destinations. This is "part of Tamza, but it goes much bigger... almost like Hewkola and other videos." The mandate: "let's just start the system and develop it."

---

## DECISIONS + WHY

### Design principle: separate Backup from Tracking
The system naturally splits into two halves that must stay separate but linked:
1. **Backup half** - Move heavy master video files OFF the C drive onto teal16 (the same external/network storage already used by the `ytdow` YouTube backup pipeline). This prevents cleanup from ever losing a master.
2. **Tracking half** - A single registry (one row per master video) with columns for: title, master location, origin/project, and a publish-status column per destination (URL + date). Same pattern as existing `lizmasters1` / `starseed-contacts` databases - a tracked table is the spine, publishing is filling status columns over time.

### Why this split
The C-drive cleanup is urgent (space pressure), but the master files are valuable. Moving them is step zero. The tracking registry is the durable system that survives moves and grows across projects.

### No building yet
Session stopped at design deliberation - deliberately. One question asked, awaiting answer before any code or file moves.

---

## CURRENT STATE

### Session identity
- Checked in as **B9** via `bcast.py whoami b9`
- Board catchup showed all Mike-DC traffic; nothing about videos in the bulletin system yet

### Folder inspected
- Path: `C:\Users\maxre\Videos\max talks\VTP videos to publish\`
- Contains exactly **one** file: `max - ufo release comments 20260515 v05.mp4` - 2.6 GB master
- Parent folder `C:\Users\maxre\Videos\max talks\` has the VTP subfolder plus likely more video material (not fully enumerated)

### Known systems referenced
- `ytdow` - existing YouTube download/backup pipeline that already saves to teal16
- `lizmasters1` / `starseed-contacts` - existing registry-style DBs that serve as the pattern template
- `bcast.py` at `C:/claude_base/branch_bulletin/bcast.py` - bulletin-board checkin system, functional

### Nothing has been built or moved
No files relocated. No schema created. No registry file initialized. Pure reconnaissance and design framing.

---

## EXACT NEXT STEP

**Await Max's answer to the open question:** What are the actual publish destinations to track?

Once he names the destination list (guesses offered: YouTube primary, a backup YouTube channel, Odysee, VK - Tamza-only under lekarstva rule -, maybe Rumble), the next actions are:
1. Design the registry schema around those destination columns
2. Create the registry file/DB
3. Move the existing 2.6 GB master off C: to teal16
4. Register that first video as row 1
5. Scan for other videos needing the same treatment

---

## OPEN QUESTIONS (awaiting Max)

- **Publish destinations** - exact list of platforms/channels to track as status columns
- **Scope boundary** - which video projects fall under this system? Tamza? Hewkola/Hucolo? max-talks? All of the above?
- **teal16 path** - what exact directory on teal16 should receive the masters? (may already exist from `ytdow`)
- **Registry format** - Markdown table? CSV? SQLite? Match `lizmasters1` format?
- **Origin tagging** - how to tag each video's project origin (Tamza, Hucolo, max talks, etc.)?

---

## KEY PATHS / IDS

| Item | Path/Identifier |
|---|---|
| Videos source folder | `C:\Users\maxre\Videos\max talks\VTP videos to publish\` |
| Lone master file | `C:\Users\maxre\Videos\max talks\VTP videos to publish\max - ufo release comments 20260515 v05.mp4` (2.6 GB) |
| Bulletin board script | `C:/claude_base/branch_bulletin/bcast.py` |
| Branch agent ID | `b9` |
| Worktree | `C:\claude_base\.claude\worktrees\cranky-euclid-9c3e48` |
| Likely teal16 backup root | (same destination `ytdow` uses - path not yet retrieved) |
| Pattern DBs | `lizmasters1`, `starseed-contacts` (exact paths not yet retrieved) |

---

## GOTCHAS / DEAD ENDS RULED OUT

- **No premature building.** The session deliberately stopped at the design question. Do not start coding or moving files until Max confirms the destination list.
- **One file only (for now).** The VTP folder currently holds only the single UFO-release-comments master. There are "tons of videos" but they may be elsewhere on C: - a broader scan will be needed after the registry is stood up.
- **Tamza has a platform restriction.** VK is only for Tamza content ("lekarstva rule") - destination tracking must support per-video or per-project applicability, not a flat "all destinations for all videos."
- **ytdow is the backup pipeline precedent.** Any teal16 paths or conventions it uses should be reused, not reinvented.
- **bcast bulletin board** is currently all Mike-DC activity - this video work is a new thread. Might want its own bulletin topic or tag once underway.
