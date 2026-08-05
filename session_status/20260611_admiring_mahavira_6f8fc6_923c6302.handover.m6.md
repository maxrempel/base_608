# Scribe handover - milestone 6 (~103K tokens)
# session: 20260611_admiring_mahavira_6f8fc6_923c6302
# cwd: C:\moma\.claude\worktrees\admiring-mahavira-6f8fc6
# written: 2026-06-11 13:47:17 by claude-opus-4-8

# HANDOVER - Retroactivity / Traceability Work

## GOAL (in Max's words)
"Plan and implement but make sure not to break. How can it be done?" - Max wants the **Retroactivity** concept (read from a Notion memo) turned from agreed-on-paper into a real, working implementation, without breaking the existing MOMA pipeline. He's working in parallel ("finishing this arrangement and moving to the next one"), so he expects this to proceed while he's occupied elsewhere.

## CONTEXT - what "Retroactivity" means
The memo Max referred to (he half-remembered the word as "retractability/retraceability" - the actual term is **Retroactivity**) addresses a real problem with the MOMA project:

- MOMA keeps changing across ~50 sessions. By the time episodes 2-3 are done, episode 1 will no longer auto-assemble. Worst case: the video exists but nobody can trace which clip came from which image / prompt / audio.

The agreed fix (concept only, **nothing built yet**) has three parts:
1. **Manifest** - every render writes one file that freezes the full timeline plus the lineage (provenance) of each clip.
2. **Lockbox** - on approval, freeze a folder containing: the manifest + final clips/audio + a D1 snapshot + a git tag. This folder is never edited again.
3. **Swap, not re-run** - to change a single word later, regenerate just that one clip and swap it in, rather than re-running the whole pipeline.

The **"oops forgot" addendum** (this was the specific thing Max came back about): **trims and flips currently have no history.** They're done by hand, baked directly into the files, with no record. That's the untracked gap. The plan to close it:
- Make trims/flips into **recorded data applied at render time** (not destructive hand-edits baked into files).
- Build episode 2 to be **traceable from the start**.
- Audit the system by trying to **regenerate one clip purely from D1**.

## DECISIONS + WHY
- Word confirmed as **Retroactivity** (not retractability/retraceability) - resolved by searching Notion.
- Concept was already agreed in a prior session; the three-part fix above is settled. The reasoning: long project lifespan + constant change means provenance must be frozen at render/approval time or it's lost forever.
- Trims/flips must become declarative data applied at render time **because** destructive hand-edits leave no trail and break the swap-not-re-run model.

## CURRENT STATE
- Concept fully read and confirmed from the Notion memo.
- **Nothing implemented.** No code written, no files changed this session.
- Max has just given the go-ahead to plan + implement carefully.

## EXACT NEXT STEP
1. Inspect the actual MOMA render pipeline and D1 schema to understand how clips, timeline, trims, and flips currently flow (especially where trims/flips get baked in by hand today).
2. Produce a concrete, non-breaking implementation plan covering: manifest write-on-render, lockbox-on-approval, swap-not-re-run, and making trims/flips recorded data.
3. Implement incrementally, preserving existing behavior - additive first (write manifests, record trims/flips as data) before changing any render path.
4. Validate via the agreed audit: regenerate one clip purely from D1.

## OPEN QUESTIONS (awaiting Max)
- None explicitly pending - Max said "plan and implement." But the plan should be surfaced to him before anything destructive, given the strong "make sure not to break" constraint.
- Unconfirmed: which episode/arrangement Max is currently finishing, and whether ep 2 traceability must be in place before he starts the next arrangement.

## KEY PATHS / IDS / NAMES
- cwd: `C:\moma\.claude\worktrees\admiring-mahavira-6f8fc6`
- Notion memo title: **Retroactivity** (fetched this session via Notion MCP search/fetch).
- Notion MCP server id: `56b90699-44a5-4951-add8-3e26a5a18809`.
- Data store: **D1** (database holding clip/timeline data; target of the "regenerate one clip from D1" audit).
- Concepts to implement: **Manifest**, **Lockbox**, **Swap-not-re-run**.

## GOTCHAS
- "make sure not to break" is the hard constraint - favor additive changes; do not touch the working render path until manifests/recorded-trims are proven alongside it.
- Trims and flips are the silent gap - they're currently baked into files by hand with zero record. Any plan that forgets these repeats the original mistake.
- The word is **Retroactivity** - Max misremembers it; don't get derailed re-searching for "retractability."
- Max is multitasking and wants progress while away - keep moving, but checkpoint the plan before irreversible steps.
- Token budget: ~103K used; compaction near ~169K. This handover exists to survive that.
