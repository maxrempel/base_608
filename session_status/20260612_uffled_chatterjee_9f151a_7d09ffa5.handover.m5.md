# Scribe handover - milestone 5 (~79K tokens)
# session: 20260612_uffled_chatterjee_9f151a_7d09ffa5
# cwd: C:\claude_base\.claude\worktrees\unruffled-chatterjee-9f151a
# written: 2026-06-12 10:34:20 by claude-opus-4-8

# HANDOVER - Claude-Drivable RustDesk Remote Support

## GOAL (in Max's words)
Max wants "actual optimal control of the remote computer by Claude" - NOT screenshots, NOT a human-in-the-loop guide-and-watch arrangement. The explicit task: "your task specifically [is] to cli rust desk to drive the remote sessions." Claude Code is to be the driver that talks to Max, and stops for Max's yes/no approval before *every dangerous step* - meaning any step that changes the connection or touches the remote computer. Max is the approval gate on top of the remote user's own consent banner.

The underlying mission (from the spec): build a transparent, consent-based, AI-drivable attended remote-support tool - a "Claude-drivable RustDesk" - so Claude/Max can help a non-technical Russian user (Igor) on Windows fix things (e.g. Zoom audio). It must NOT have the backdoor shape of the old `tamza_connect` tool that was correctly safety-blocked.

Max's last message cut off mid-sentence ("Screenshots are...") and flags that the *previous* session "seemed to be utterly confused." So Max is signalling: don't repeat that confusion, and don't drift back toward a screenshots/human-eyes compromise. He wants the real thing if it's feasible.

## DECISIONS + WHY
- **Scope locked to Option A**: Claude drives remote sessions through RustDesk's CLI. Max ruled out the human-in-the-loop fallback as the goal.
- **Approval-gated driving is the shape**: Claude proposes each dangerous action, Max approves, then Claude acts. This is a *stronger* guardrail than the old tool - chosen deliberately to stay clear of backdoor territory.
- **Hard rule from the spec - do NOT fall back to a headless SSH shell.** That is precisely what made the old `tamza_connect` malware. If true Claude-driving turns out infeasible, the answer is honesty, not a hidden shell.
- **Five non-negotiables** govern everything (in the spec): transparent distribution, a visible ongoing consent banner, attended/per-session OTP, no hidden persistence, fully auditable.

## CURRENT STATE
The gating research question has been partially answered, and the answer is bad for the naive plan:

- RustDesk **is installed locally** at `C:\Program Files\RustDesk\rustdesk.exe`.
- Its CLI was tested (`--help`). The flags `--get-id`, `--password`, `--connect` only **poke the GUI**. There is **no scripting API**. A script cannot pull remote-screen frames or inject input *through the RustDesk CLI*.
- `rustdesk --connect <id>` opens RustDesk's control *window*; a human normally watches it.
- Attempting to screenshot that window yields a **black image** because it is GPU/hardware-rendered.

So: the literal "Claude sees Igor's screen and clicks, via RustDesk CLI" does not exist out of the box. This is the friction point Max is now pushing against - he's just said screenshots are not what he wants anyway; he wants real control.

Two forward options were put to Max but he has NOT chosen - he instead redirected toward "actual optimal control":
1. Accept the reduced shape (Claude drives connection + guides, someone else is the eyes). Max appears to be rejecting this.
2. Test a workaround for the black-screen problem (disable RustDesk's hardware/texture rendering) so computer-use *can* see the window - restoring real Claude-driving.

## EXACT NEXT STEP
Max's reply was cut off, so first: **let him finish the thought** ("Screenshots are...") OR confirm the interpretation - that he wants genuine programmatic eyes+hands on the remote machine, not screenshots, and not a watch-the-window setup.

Then, given he wants real control and not screenshots, the live technical task is: **determine whether Claude can get true input-injection + screen-read on the remote session by means OTHER than RustDesk's (non-existent) scripting API.** Concretely worth investigating:
- The black-screen workaround (option 2): disable RustDesk hardware/texture rendering via advanced settings so the control window becomes capturable - but note Max says he doesn't want screenshots, so this may not satisfy him.
- Whether "optimal control" should instead mean Claude runs/automates input *on the remote machine itself* (i.e. an agent on Igor's side) rather than driving RustDesk's viewer locally - which changes the architecture and must be checked hard against the five non-negotiables and the no-hidden-shell rule.

Clarify with Max which of these "real control" means before building, because they have very different safety profiles.

## OPEN QUESTIONS (awaiting Max)
- Finish the cut-off sentence: what exactly does Max mean by "optimal control" vs screenshots - Claude driving the *local RustDesk viewer*, or Claude automating *on Igor's remote machine*?
- Given RustDesk's CLI has no scripting API, is Max willing to accept a workaround layer (e.g. local input automation against the RustDesk window once it's visible), or does he consider that another form of "confusion"?
- Does Max want the black-screen rendering workaround tested at all, or is that off the table because it's screenshot-adjacent?

## KEY PATHS / IDS / COMMANDS
- Spec (READ FIRST): `C:\claude_base\tools\claude_remote_help\SPEC_claude_remote_help_v01_tomemex.md`
- RustDesk binary: `C:\Program Files\RustDesk\rustdesk.exe`
- cwd: `C:\claude_base\.claude\worktrees\unruffled-chatterjee-9f151a`
- Tested CLI flags: `--get-id`, `--password`, `--connect <id>`, `--help` (GUI-poking only)
- Remote user: Igor (non-technical, Russian, Windows; example task = fix Zoom audio, e.g. "Original Sound for Musicians" toggle)
- Old blocked tool to be deleted: `tamza_connect` folder + its associated gist.

## GOTCHAS / DEAD ENDS RULED OUT
- **RustDesk CLI is NOT a scripting API** - confirmed by test. Don't re-discover this; don't promise Claude can see/click "via the CLI."
- **Screenshotting RustDesk's control window returns black** (GPU rendering). And Max has now said he doesn't want screenshots anyway, so even a fixed screenshot path may not satisfy the goal.
- **NEVER fall back to a headless SSH shell** - that is the backdoor shape that got the predecessor correctly blocked. This is the single hardest line.
- The **previous session was "utterly confused"** per Max - likely by drifting between the screenshots/human-eyes compromise and true driving. Avoid that: be precise about what "control" means before building anything.
- Don't start building until the cut-off message is resolved and the architecture (drive-local-viewer vs remote-agent) is pinned down against the five non-negotiables.
