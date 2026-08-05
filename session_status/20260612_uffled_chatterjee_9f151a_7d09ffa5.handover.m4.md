# Scribe handover - milestone 4 (~71K tokens)
# session: 20260612_uffled_chatterjee_9f151a_7d09ffa5
# cwd: C:\claude_base\.claude\worktrees\unruffled-chatterjee-9f151a
# written: 2026-06-12 10:32:34 by claude-opus-4-8

# HANDOVER - Claude-drivable RustDesk / claude_remote_help

## GOAL (in Max's words)
Max wants "a cl code [Claude Code] to talk to me, and for every dangerous step - that changes connection or remote computer - get my approval." 

Plainly: build a transparent, consent-based, AI-drivable attended remote-support tool - informally "Claude-drivable RustDesk" - so Claude (with Max in the loop) can help a non-technical Russian user named Igor on Windows. The defining feature Max just emphasized: Claude narrates/converses with Max throughout, and any action that changes the connection or touches the remote computer must be gated behind Max's explicit approval (human-in-the-loop on every dangerous step).

This is a deliberate clean redesign of an earlier tool, `tamza_connect`, which was correctly safety-blocked because it had the shape of a backdoor. The new design must NOT rebuild that backdoor.

## DECISIONS + WHY
- **Read the spec before doing anything.** Done - the assistant read the full spec file. It defines 5 non-negotiables: transparent distribution, a visible ongoing consent banner, attended/per-session OTP, no hidden persistence, and auditability.
- **The whole project hinges on ONE research question:** Can RustDesk (or AnyDesk / MeshCentral) hand a script BOTH the remote-screen frames AND input injection (clicks/keys) while the user's visible consent banner stays up? This must be answered first because it forks the architecture.
  - **If YES ? build Option A:** wrap RustDesk's CLI so Claude can actually see the screen and drive input itself. Cleanest path.
  - **If NO ? human-in-the-loop only:** Max watches/drives RustDesk, Claude scripts and advises. Still legitimate.
- **Hard prohibition:** If the answer is no, do NOT fall back to a headless SSH shell. That is exactly the hidden-shell shape that made the old `tamza_connect` malware. This is non-negotiable.
- Max's latest message reinforces that even in the Option-A "Claude drives" case, dangerous steps stay gated behind his approval - so the design is consent-gated regardless of which architecture wins.

## CURRENT STATE
- Still in the **discussion / design phase**. Nothing has been built or tested.
- The spec has been read and summarized back to Max.
- The assistant offered Max three paths: (a) go research/test whether RustDesk can give a script eyes+hands, (b) just help Igor by hand today (Max drives official RustDesk, fixes Igor's Zoom audio), or (c) keep discussing the design.
- Max responded not by picking a/b/c cleanly, but by clarifying the core requirement: Claude-talks-to-Max + per-dangerous-step approval. That clarification points strongly toward the human-in-the-loop / consent-gated model - but the RustDesk eyes+hands research question is still unanswered.

## EXACT NEXT STEP
Confirm with Max how to read his last message: he has essentially specified the *interaction model* (Claude converses, approval required on every connection-changing or remote-machine-changing step). The assistant should:
1. Acknowledge that this interaction model is compatible with both Option A and the human-in-the-loop fallback.
2. Confirm whether Max wants to proceed to actually **research/test the RustDesk CLI** (commands to probe: `--get-id`, `--password`, `--connect`, and OTP behavior) to settle the one decisive question - OR whether he wants to lock in the human-in-the-loop design and start building the approval-gated conversation layer now.

Do not start building or running connection commands until Max confirms which of those two he wants.

## OPEN QUESTIONS (awaiting Max)
- Does RustDesk's CLI actually let a script both receive screen frames and inject input while the consent banner stays visible? (THE decisive unanswered research question.)
- Is Max asking to start the RustDesk research now, or to commit to the human-in-the-loop build now?
- Is there a "help Igor today by hand" task that's urgent and separate from the build (his Zoom audio issue)?

## KEY PATHS / IDS / COMMANDS
- Spec file (READ FIRST): `C:\claude_base\tools\claude_remote_help\SPEC_claude_remote_help_v01_tomemex.md`
- Tool folder: `C:\claude_base\tools\claude_remote_help\`
- Working directory: `C:\claude_base\.claude\worktrees\unruffled-chatterjee-9f151a`
- Dead/to-be-deleted: the old `tamza_connect` folder **and its associated gist** - both should be deleted.
- RustDesk CLI flags to test: `--get-id`, `--password`, `--connect`, plus per-session OTP.
- People: Max (the operator), Igor (the non-technical Russian Windows end-user being helped). Igor's concrete problem mentioned: Zoom audio - fix is flipping Zoom's "Original Sound for Musicians."

## GOTCHAS / DEAD ENDS ALREADY RULED OUT
- **No hidden SSH shell fallback.** This is the line that made the old tool a backdoor; rebuilding it is forbidden even if RustDesk research fails.
- **No hidden persistence**, no silent distribution - distribution must be transparent.
- The visible consent banner must stay up at all times; an architecture that suppresses or hides it violates the spec.
- The old `tamza_connect` was *correctly* safety-blocked - don't treat that as an obstacle to route around; the redesign exists specifically to avoid its shape.
- Don't skip the research question by assuming Option A works - it's explicitly unverified.
- Spec origin note: authored by Claude Opus 4.8 in Claude Code on "Pine," 2026-06-12; the 5 non-negotiables and two architecture options live in that spec file - re-read it before acting.
