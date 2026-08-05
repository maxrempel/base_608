# Scribe handover - milestone 1 (~137K tokens)
# session: 20260628_wonderful_liskov_dcda0b_589c5f13
# cwd: C:\moma\.claude\worktrees\wonderful-liskov-dcda0b
# written: 2026-06-28 22:55:34 by deepseek-v4-pro

# Handover: Music Saving for Finished Scenes (Before SC11)

## Goal (in Max's own words)
> "We need to fix and back up proper music saving. ... We need to have multiple music save options, maybe 15. The system should save the current setup of the music, input files and actually collect them - not only link to them, but collect them. We need everything in one place. All parameters used for music overlay should be saved. That's what we should do now, before moving to 11."

## Decisions Made + Why
- **Do the music-saving work before starting scene 11 (SC11).** The finished-scene music is currently "overlaid and lost" - it's not persisted, so moving ahead would be premature.
- **Hold off implementation until we confirm the landscape.** The assistant chose to first understand what already exists, so we don't duplicate or miss an easy extension path.

## Current State
- Assistant (checked in as D01) found an existing **music-projects system** (D40, from 2026-06-22):
  - It *already does* much of what Max described: it collects the video + music file (not just links), and saves overlay parameters (offset, volume curve).
  - It stores multiple named-project folders, synced via Nextcloud.
- Two gaps identified for finished scenes:
  1. **No scene-pipeline integration** - the music-projects system was built for standalone clips, not tied into the finished-scene workflow.
  2. **No versioning** - no ability to keep ~15 saves per project and pick a non-latest one.
- No code has been changed yet; purely reconnaissance.

## Exact Next Step
1. **Get the answer to the open question below** (where is the music overlay for finished scenes currently performed?).
2. Then decide: extend the existing music-projects system (add scene binding + version slots) or replace an isolated, lossy overlay path that is separate from it.

## Open Questions (Needing User Input)
- **Where does Max currently overlay music for a finished scene?** Is it the Music tab in the browser (the same place the music-projects system lives), or a different/single-overlay screen that exists in the scene editor but isn't connected to that system?

## Key Paths / Identifiers
- Worktree: `C:\moma\.claude\worktrees\wonderful-liskov-dcda0b`
- Existing music-projects method document: `C:\moma\sc10\sound_assembly\code\music_projects_method_v01_tomemex.md`
- Next scene folder would be SC11; current scene likely SC10 or earlier.
- Music-projects identifier: D40.

## Gotchas / Dead Ends Ruled Out
- The music being "overlaid and lost" means whatever UI currently sets the finished-scene music does **not** persist that information between sessions. That's the lossy path we need to close.
- The existing music-projects system is promising but was not designed for the scene pipeline - we must verify it's the same code path before building versioning on top of it.
- No alternative approaches have been explored yet; this was stopped at the fact-finding stage.
