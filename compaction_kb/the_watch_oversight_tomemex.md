# THE WATCH - per-session oversight by two full-Opus agents

Built 2026-06-07 (Max + c1). Status: build delegated to a worker; this doc is
the design + operating manual. Plain ASCII only.

## WHAT IT IS

Every Claude Code session (every project, including MOMA - not just named team
branches) is watched by TWO independent full-Opus agents that read the WHOLE
transcript at each token milestone and act on their own. Fully programmatic:
it does NOT depend on the session's own Opus cooperating (Opus ignores
instructions - that is the whole reason this exists).

The two watchers:
- THE SCRIBE - calm, neutral. Writes a rich status/handover to disk so a cold
  post-compaction session resumes the exact work. Never interrupts.
- THE ADVISER - skeptical, protective. Reads the chat, catches trouble
  (shortcuts, branching, death-spiral, drift, Max being ignored) and ADVISES
  two audiences: the session's Opus (course-correction) and Max (a heads-up
  when he must decide). Stays silent on a clean session.

## HOW IT WORKS

1. The existing UserPromptSubmit hook (`session_status.py`) already detects when
   a session crosses a ~15K-real-token milestone (token count read from each
   assistant line's message.usage in the transcript .jsonl). ~11 milestones
   before the ~169K auto-compaction cliff.
2. On a NEW milestone the hook launches a DETACHED, HIDDEN background process
   (no terminal popup) that does the slow work - reads the full transcript,
   calls Opus twice (Scribe, then Adviser), writes both results to disk. The
   hook itself returns instantly so Max's turn never freezes.
3. On every hook fire the hook first injects the latest not-yet-shown MILESTONE
   Adviser note via stdout (these unprompted notes are still async, so they land
   one turn after they are written - acceptable). TRIGGERED questions (`a'` /
   `adviser:`) are different: they are answered SYNCHRONOUSLY and printed in the
   same turn (see "TALKING TO THE ADVISER" below).
4. The old mechanical breadcrumb (Layer 1) still runs. Everything fails open -
   a broken Watch run must never wedge or slow a session.

Model: full Opus (same id as cc_recover_v02). Reads everything. Cost accepted.
API pattern copied from `C:\claude_base\tools\cc_recover\cc_recover_v02.py`.

## TALKING TO THE ADVISER (two-way, same chat)

Added 2026-06-07. The Adviser is no longer one-way. Max can ask it a question
inside the SAME chat.

Three named participants, used everywhere: MAX (the user), ASSISTANT (the model
working in the session), ADVISER (the overseer).

Trigger: start a prompt with `a'` or `adviser:` (case-insensitive; leading
spaces ok). Everything after the trigger is the question to the Adviser.
Example:
  a' are you sure scene 9 is the right input here?

What happens on that turn (SYNCHRONOUS as of 2026-06-08 - answer in the SAME
turn, no nudge):
- The hook detects the trigger and calls the Adviser INLINE (blocking): full
  Opus reads the whole transcript as context plus Max's question and answers him
  directly and conversationally. The hook prints that answer to stdout in the
  SAME invocation, so it lands in the same turn. Typical wait ~8-15s.
- The answer is wrapped exactly once in the compact marker pair
  `[purple dot] **ADVISER** ...answer... **ADVISER** [purple dot]`. Any
  self-labeling the model emits (a leading `ADVISER:`, its own `**ADVISER**`
  markers, or stray purple dots) is stripped first so there is never a
  double-wrap.
- A HARD ~20s timeout bounds the call. On timeout or any error the hook prints a
  one-line fallback (`...unreachable right now -- ask again`) and continues. The
  hook FAILS OPEN - it never wedges or crashes Max's turn.
- The hook also injects a short note telling the Assistant "this was addressed to
  the Adviser, its answer is already printed, do not answer it yourself" so the
  Assistant does not hijack the question.
- A turn that talks to the Adviser is NOT a token milestone - it does not also
  fire a Scribe/Adviser review. Normal (non-triggered) prompts behave exactly as
  before: milestone breadcrumb + review when a new ~15K token level is crossed.

This replaced the old async design (detached runner writes a reply file +
pointer JSON, answer surfaced one turn LATER on the next hook fire, which forced
Max to send a separate "nudge" message to pull the answer through). That
seq/pointer machinery is gone for triggered questions; the synchronous path
needs no state. The async runner's ANSWER mode (`session_oversight.run_answer`,
driven by the `answer` CLI subcommand) is retained only as a dormant fallback
and shares the new `compute_answer` core.

The unprompted MILESTONE notes are still async/detached and still surface one
turn late via the pointer JSON in `.state` (`<stem>.adviser_ptr.json`) - only
the TRIGGERED question path was made synchronous.

Failure handling matches the rest of the Watch: everything fails open (a broken
Adviser path never wedges or slows Max's turn), ASCII only (except the one
intentional purple-dot marker), no popups.

Tested 2026-06-08 by driving the hook with an `a'` prompt on a ~165K-token
transcript: full Opus answered in ~5s, printed in ONE invocation, wrapped
exactly once, no leading `ADVISER:`.

## EDITING THE PERSONALITIES (no code change needed)

Each watcher's character lives in its own plain-text brief, loaded verbatim by
the runner. To change behavior, edit the file - do NOT touch code:
- Scribe:  `C:\claude_base\compaction_kb\personalities\scribe.md`
- Adviser: `C:\claude_base\compaction_kb\personalities\adviser.md`

As we start using the system we will tune these (e.g. teach the Adviser new
death-spiral shapes, adjust how loud it gets, refine what the Scribe captures).
Update them in place; the next session picks up the change automatically.

## OUTPUTS

Under `C:\claude_base\session_status\`:
- Scribe handover per milestone (versioned, never overwritten).
- Adviser note per milestone (versioned); the latest unshown one is injected.
- A runner logfile (so a silent Opus/API failure is debuggable, never a popup).

## FILES

- Hook + milestone logic: `C:\claude_base\compaction_kb\scripts\session_status.py`
- Background runner (the two Opus calls): added by the worker (see that script).
- Personalities: `C:\claude_base\compaction_kb\personalities\*.md`
- Wired in `C:\Users\maxre\.claude\settings.json` (UserPromptSubmit), Pine only.
- Background runner: `C:\claude_base\compaction_kb\scripts\session_oversight.py`.

## READING THE OUTPUT

For any session, look in `C:\claude_base\session_status\`:
- `<stem>.handover.m<level>.md` - the Scribe's handover at each milestone.
- `<stem>.adviser.m<level>.md` - the Adviser's note at each milestone.
- `<stem>_*.md` (no suffix) - the original mechanical breadcrumb log.
The `<stem>` encodes the date, the worktree/project, and the session id, so you
can tell whose session each file belongs to.

## TROUBLESHOOTING

- Nothing is being written: check `C:\claude_base\session_status\oversight.log`.
  Every run logs a milestone line plus SCRIBE ok / ADVISER ok (with char counts)
  or a failure with a traceback. A silent Opus/API error shows up here, never as
  a popup.
- No Adviser note appeared in a chat: the Adviser stays SILENT on a clean
  session (it replies "CLEAN - no action needed" and nothing is injected). That
  is by design - it only speaks when something needs attention.
- The whole thing is dark: confirm the hook is still wired in
  `~/.claude/settings.json` (the third UserPromptSubmit command) and that the
  Anthropic API key is present under `zSyncMain\ssh\`.

## COST

Full Opus, reading the entire transcript, twice per milestone, ~11 milestones
per long session. This is deliberate (Max chose full Opus that reads everything
over a cheaper/partial reader). Watch the spend as it rolls out across all
sessions and tune `MILESTONE_TOKENS` (in session_status.py) up if it is too
frequent.

## KNOWN LIMITATIONS (as of 2026-06-07, first build)

- MILESTONE advice lands ONE turn late (the unprompted Opus call runs in the
  background; the hook injects the previous run's note on the next turn).
  Acceptable by design. TRIGGERED `a'` questions are now synchronous (same turn).
- Em-dashes in model output become "?" because of the hard ASCII strip - purely
  cosmetic, on the polish list.
- Two paths were not yet exercised live: the "CLEAN -> stay silent" branch (the
  test session was non-clean) and the API-down fail-open path (verified by code
  reading, not by forcing an outage).
- Pine only - the hook lives in Pine's settings.json, which is not synced. Re-add
  the same UserPromptSubmit command on other machines to enable it there.

## DISABLING

Remove (or comment out) the third UserPromptSubmit command in
`~/.claude/settings.json`. The mechanical breadcrumb and the rest of the session
keep working; only the two Opus watchers stop.
