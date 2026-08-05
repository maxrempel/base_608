# b3 Task Spec v01 - Management & Continuous-Improvement (Training) System

Author: b1 (lead), coordinating for b3. Owner/decider: Max. Date: 2026-06-06.

## Mission
Build the system by which the multi-branch team (boss b1 + employee branches +
b0 safety) LEARNS from each session and feeds continuously-improved INPUTS back
into future sessions. The deliverable is NOT production output - it is the
management/training machinery itself: better charters, specs, and instructions
that make every future boss and employee start smarter than the last.

## Why
We run many parallel + sequential Claude sessions. Today each one starts about
as naive as the last. Compaction destroys ~94% of in-session memory (b2's
finding: auto-fires ~169K tokens / ~85% of a 200K window, only ~6% survives).
The DURABLE layer - board + shared files + global2.md + CLAUDE.md - is what
survives. So the leverage point: capture what worked/failed in a session and
improve the durable INPUTS, so the next session inherits the lesson instead of
re-learning it.

## Scope (design + build)
1. LESSON-CAPTURE loop: at natural milestones / session end, distill what
   improved (or hurt) the team's effectiveness - good boss moves, bad boss
   moves, employee friction, spec gaps - into durable, structured notes.
2. INPUT IMPROVEMENT: turn those lessons into concrete edits to the ACTUAL
   inputs branches receive - the bcast SKILL, the b0 charter, task specs, and
   the global2 "BRANCH BROADCAST" section. Version + date everything; no "final".
3. ROLE CHARTERS: crisp, improvable charters for boss (b1), employee branches,
   and b0, so roles are explicit and refined over time (b0 already has
   shared/b0_charter_v01.md - follow that pattern).
4. SELF-IMPROVEMENT CADENCE: how often, and by what trigger, the team reviews
   and upgrades its own inputs.

## Hard rules
- You implement; b1 coordinates. Board a SHORT spec before building; b1 reviews.
- Learn from THIS session as the first case study: what made it go well (calm,
  durable-first, one authoritative finding instead of a 40-session rig) vs the
  earlier friction Max flagged (b1 acting "bossy/bureaucratic" with long
  directives). Encode both into improved inputs.
- No production work - meta-management only.
- Durable + branching-proof: every artifact dated/versioned, stored where future
  sessions auto-find it.
- Honor halt/stop conditions and b0's safety guidance.

## First step
This file is DIRECTION, not the detailed design. b3: write a SHORT spec of the
lesson-capture -> input-improvement loop, board "b3 spec ready", b1 reviews,
then build.
