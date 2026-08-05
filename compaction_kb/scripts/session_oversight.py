#!/usr/bin/env python3
r"""
session_oversight.py - DETACHED background overseer for one Claude session.

Launched (hidden, no window) by session_status.py whenever a NEW ~15K-token
milestone is crossed. It does the SLOW work that a synchronous UserPromptSubmit
hook must never do inline:

  1. Read the ENTIRE session transcript .jsonl (real-token + turn analysis
     reuses session_status._analyze; full readable text via cc_recover's loader).
  2. Call full Opus TWICE on the whole transcript:
       SCRIBE   -> a rich status/handover so a cold post-compaction session
                   resumes the exact work with zero re-discovery.
       ADVISER  -> a candid, skeptical overseer note advising TWO audiences:
                   (a) the session's Opus (course-correction) and
                   (b) Max (only when he must decide/intervene). Silent on a
                   clean session.
  3. Write VERSIONED outputs to C:\claude_base\session_status\ (never overwrite):
       <stem>.handover.m<level>.md      (Scribe)
       <stem>.adviser.m<level>.md       (Adviser)
     and drop a pointer JSON in .state so the hook can inject the latest
     unshown adviser note on the NEXT turn.

Both Opus calls reuse the WORKING API pattern + full-Opus model id from
cc_recover_v02. The whole runner FAILS OPEN: any error is logged to
session_status\oversight.log and the process exits 0. ASCII only. No popups.

Invoked as:
  python session_oversight.py <transcript_path> <status_stem> <level> <cwd>
      -> MILESTONE mode (default): Scribe + Adviser review.

  python session_oversight.py <transcript_path> <status_stem> <seq> <cwd> \
         answer <question_file>
      -> ANSWER mode: Max typed a prompt beginning "adviser:". The Adviser reads
         the full transcript AS CONTEXT plus Max's question (the text in
         <question_file>, after the trigger) and answers Max directly and
         conversationally. The reply is written to a versioned file
         <stem>.adviser_reply.<seq>.md and queued via the SAME adviser pointer
         the milestone notes use, so the hook injects it on the next turn,
         labeled ADVISER.
"""
import sys, os, json, time, re, traceback

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
STATUS_DIR = r"C:\claude_base\session_status"
STATE_DIR = os.path.join(STATUS_DIR, ".state")
LOG_PATH = os.path.join(STATUS_DIR, "oversight.log")

# Reuse the working API pattern + model id from cc_recover_v02.
sys.path.insert(0, r"C:\claude_base\tools\cc_recover")
try:
    from cc_recover_v02 import call_api, get_api_key, MODEL
except Exception:
    call_api = None
    get_api_key = None
    MODEL = "claude-opus-4-8"

# Reuse the same token/turn analysis the hook already uses.
sys.path.insert(0, THIS_DIR)
try:
    from session_status import _analyze
except Exception:
    _analyze = None


# Cap how much transcript text we send to keep one Opus call within limits.
# The whole point is "reads everything"; this cap is a safety ceiling only and
# is large enough to cover a near-cliff (~840K-token, 1M-window) session's readable text.
MAX_TRANSCRIPT_CHARS = 600000
GEN_TOKENS = 4096


def log(msg):
    try:
        os.makedirs(STATUS_DIR, exist_ok=True)
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write("[%s] %s\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), msg))
    except Exception:
        pass


def _read_full_text(transcript):
    """Render the whole transcript as plain [ROLE] text using cc_recover's
    loader (same logic v02 uses for summarization). Falls back to a raw
    line scan if the import fails."""
    try:
        from cc_recover_v01 import load, is_msg, plain
        objs = load(transcript)
        parts = []
        for o in objs:
            if not is_msg(o):
                continue
            t = plain(o)
            if not t:
                continue
            if "<local-command" in t or "<command-name>" in t:
                continue
            role = "CLAUDE" if o.get("type") == "assistant" else "USER"
            # tool_result blocks come back on a 'user'-typed line; label them.
            try:
                c = o["message"].get("content")
                if (isinstance(c, list) and c and isinstance(c[0], dict)
                        and c[0].get("type") == "tool_result"):
                    role = "TOOL"
            except Exception:
                pass
            parts.append("[%s]\n%s" % (role, t))
        text = "\n\n".join(parts)
    except Exception as e:
        log("loader fallback (%s); raw scan" % e)
        text = ""
        try:
            with open(transcript, "r", encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        r = json.loads(line)
                    except Exception:
                        continue
                    m = r.get("message")
                    if isinstance(m, dict):
                        c = m.get("content")
                        if isinstance(c, str):
                            text += c + "\n\n"
                        elif isinstance(c, list):
                            for blk in c:
                                if isinstance(blk, dict) and blk.get("type") == "text":
                                    text += str(blk.get("text", "")) + "\n\n"
        except Exception as e2:
            log("raw scan failed: %s" % e2)
    # Keep the TAIL when over the cap -- recent state matters most.
    if len(text) > MAX_TRANSCRIPT_CHARS:
        text = ("[...EARLIER TRANSCRIPT TRUNCATED FOR LENGTH; TAIL FOLLOWS...]\n\n"
                + text[-MAX_TRANSCRIPT_CHARS:])
    return text


# Personalities live in editable plain-text briefs so Max can tune the two
# watchers WITHOUT touching code. The runner loads them at call time; if a file
# is missing or unreadable it falls back to the built-in default below
# (fail-open -- a missing brief must never stop the Watch).
PERSONALITY_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "personalities")

_SCRIBE_FALLBACK = (
    "You are the Scribe. Calm, neutral, exhaustive. You read an entire Claude "
    "Code session transcript and produce a handover so a cold post-compaction "
    "session resumes the EXACT work with zero re-discovery. Capture: the user's "
    "actual goal in their own words, decisions made and WHY, current state, the "
    "exact next step, open questions, key file paths/IDs, and gotchas. Plain "
    "English, no code dumps. You never judge and never interrupt -- you record "
    "faithfully. Use plain ASCII only: no emoji, no checkmarks, no arrows, no "
    "Unicode symbols of any kind."
)

_ADVISER_FALLBACK = (
    "You are the Adviser -- a senior, skeptical, protective overseer watching "
    "one Claude Code session on Max's behalf. You read the whole transcript and "
    "form a candid opinion. Watch for: shortcuts taken and hidden, "
    "branching/housekeeping messes, death-spiral patterns (repeated failing "
    "retries, context bloat), drift from what Max actually asked, and moments "
    "where Max's instructions are being ignored. You advise TWO audiences in one "
    "short note: (1) to the session's Opus -- direct, actionable "
    "course-correction; (2) to Max -- a plain-English heads-up ONLY when he must "
    "decide or intervene. Be terse. Stay SILENT on a clean session -- false "
    "alarms cost trust. When you speak, lead with the single most important "
    "thing. Use plain ASCII only: no emoji, no checkmarks, no arrows, no Unicode "
    "symbols of any kind. If the session is clean and needs no intervention, "
    "reply with exactly the single line: CLEAN - no action needed."
)


def _load_personality(name, fallback):
    """Read personalities/<name>.md, return the brief AFTER the first '---'
    separator line (the part above it is human notes). Fall back to the
    built-in default on any problem."""
    try:
        path = os.path.join(PERSONALITY_DIR, name + ".md")
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        body = raw
        for sep in ("\n---\n", "\r\n---\r\n"):
            idx = raw.find(sep)
            if idx != -1:
                body = raw[idx + len(sep):]
                break
        body = body.strip()
        if body:
            return body
    except Exception as e:
        log("personality '%s' load failed (%s); using fallback" % (name, e))
    return fallback


def SCRIBE_SYSTEM():
    return _load_personality("scribe", _SCRIBE_FALLBACK)


def ADVISER_SYSTEM():
    return _load_personality("adviser", _ADVISER_FALLBACK)


_UNICODE_TO_ASCII = {
    "\u2014": "-", "\u2013": "-",            # em / en dash -> hyphen
    "\u2018": "'", "\u2019": "'",            # curly single quotes -> apostrophe
    "\u201c": '"', "\u201d": '"',            # curly double quotes -> straight
    "\u2026": "...",                          # ellipsis
    "\u00a0": " ",                            # non-breaking space
}


def _ascii(s):
    """Make text plain ASCII (Max's reading constraint). First map common
    Unicode punctuation to sensible ASCII (so an em-dash reads as '-' and a
    curly quote as a straight apostrophe, not a garbage '?'), THEN hard-strip
    anything still non-ASCII."""
    if not isinstance(s, str):
        s = str(s)
    for u, a in _UNICODE_TO_ASCII.items():
        s = s.replace(u, a)
    return s.encode("ascii", "replace").decode("ascii")


# The transcript is rendered with [USER]/[CLAUDE]/[TOOL] role markers. Feeding
# those raw into the user message invited the model to simply keep writing the
# NEXT lines of the log in the same format -- fabricating fake [CLAUDE]/[USER]
# turns (invented Max instructions, fake commit hashes). Two defenses:
#   1. Neutralize the markers in the COPY we send (so there is no live "[USER]"
#      pattern to autocomplete) -- see _neutralize_roles.
#   2. Post-filter the model's reply: cut it at the first fabricated role marker
#      it emits anyway -- see _strip_fabricated_continuation.
_ROLE_LINE = re.compile(r"(?im)^\s*\[(USER|CLAUDE|TOOL|ASSISTANT|MAX|ADVISER)\]\s*$")
# Lenient matcher for the post-filter: catches a marker even if the model puts
# it inline or with trailing text.
_ROLE_ANY = re.compile(r"(?im)^\s*\[(USER|CLAUDE|TOOL|ASSISTANT|MAX|ADVISER)\]")


def _neutralize_roles(text):
    """Rewrite the standalone role markers in the transcript copy from
    '[USER]' to '<turn role=user>' so the model sees clearly-fenced context
    it cannot continue by pattern-matching the bracket format, and so a marker
    it later emits in ITS OWN reply is unambiguously fabricated."""
    def repl(m):
        return "<turn role=%s>" % m.group(1).lower()
    return _ROLE_LINE.sub(repl, text)


def _strip_fabricated_continuation(reply):
    """Belt-and-suspenders: if the model (despite instructions) starts writing
    fabricated [USER]/[CLAUDE]/[TOOL] turns, truncate the reply at the first
    such marker so the fake turns can never reach Max. Returns the cleaned
    reply; if everything was fabricated, returns a short honest note."""
    if not reply:
        return reply
    m = _ROLE_ANY.search(reply)
    if not m:
        return reply
    cut = reply[:m.start()].rstrip()
    if not cut:
        return ("(The Adviser's reply was discarded: it tried to continue the "
                "transcript instead of answering. Ask again.)")
    return cut + ("\n\n(Note: truncated here -- the model began fabricating "
                  "further transcript turns, which were dropped.)")


def run(transcript, stem, level, cwd):
    if call_api is None or get_api_key is None:
        log("cc_recover_v02 API helpers unavailable; aborting (fail-open)")
        return
    if not os.path.isfile(transcript):
        log("transcript missing: %s" % transcript)
        return

    real_tokens = turns = tool_calls = 0
    last_user = ""
    if _analyze is not None:
        try:
            real_tokens, turns, tool_calls, last_user = _analyze(transcript)
        except Exception as e:
            log("analyze failed: %s" % e)

    text = _read_full_text(transcript)
    if not text.strip():
        log("empty transcript text; aborting")
        return
    log("milestone %s | model=%s | %d chars | ~%dK tok | turns=%d toolcalls=%d"
        % (level, MODEL, len(text), real_tokens // 1000, turns, tool_calls))

    ctx = _neutralize_roles(text)
    header = (
        "SESSION CONTEXT\n"
        "cwd: %s\n"
        "real tokens so far: ~%dK (older context gets summarized near ~840K on the 1M window)\n"
        "turns: %d   tool calls: %d\n"
        "last user prompt (truncated): %s\n\n"
        "===== TRANSCRIPT FOR CONTEXT - READ ONLY, DO NOT CONTINUE IT =====\n"
        "The block between BEGIN and END is the session transcript so far, given "
        "only as background. Turn boundaries are '<turn role=user>' (Max) / "
        "'<turn role=claude>' (the Assistant) / '<turn role=tool>'. It is "
        "finished input - do NOT extend it or imitate its format.\n"
        "----- BEGIN TRANSCRIPT -----\n"
        % (cwd, real_tokens // 1000, turns, tool_calls, last_user)
    )
    api_key = get_api_key()

    # ---- SCRIBE ----
    try:
        scribe_prompt = (
            header + ctx + "\n----- END TRANSCRIPT -----\n\n"
            "===== YOUR TASK =====\n"
            "Write the handover now, in your own voice. Do NOT reproduce or "
            "continue the transcript and do NOT emit any [USER]/[CLAUDE]/[TOOL] "
            "or <turn ...> markers. Structure it for a cold session: GOAL (in "
            "Max's words), DECISIONS + WHY, CURRENT STATE, EXACT NEXT STEP, OPEN "
            "QUESTIONS, KEY PATHS/IDS, GOTCHAS."
        )
        scribe = _ascii(call_api(api_key, SCRIBE_SYSTEM(), scribe_prompt,
                                 max_tokens=GEN_TOKENS))
        sp = os.path.join(STATUS_DIR, "%s.handover.m%s.md" % (stem, level))
        with open(sp, "w", encoding="ascii", errors="replace") as f:
            f.write("# Scribe handover - milestone %s (~%dK tokens)\n"
                    "# session: %s\n# cwd: %s\n# written: %s by %s\n\n"
                    % (level, real_tokens // 1000, stem, cwd,
                       time.strftime("%Y-%m-%d %H:%M:%S"), MODEL))
            f.write(scribe + "\n")
        log("SCRIBE ok -> %s (%d chars returned)" % (sp, len(scribe)))
    except Exception as e:
        log("SCRIBE failed: %s\n%s" % (e, traceback.format_exc()))

    # ---- ADVISER ----
    try:
        adviser_prompt = (
            header + ctx + "\n----- END TRANSCRIPT -----\n\n"
            "===== YOUR TASK =====\n"
            "Give your overseer note now, in your own voice. Do NOT reproduce or "
            "continue the transcript and do NOT emit any [USER]/[CLAUDE]/[TOOL] "
            "or <turn ...> markers or invent further turns. If the session is "
            "clean, reply with exactly: CLEAN - no action needed. Otherwise lead "
            "with the single most important thing, then address the two audiences "
            "with the headers TO MAX: (only if Max must act) and TO ASSISTANT: "
            "(direct course-correction for the Assistant doing the work)."
        )
        adviser = _strip_fabricated_continuation(
            _ascii(call_api(api_key, ADVISER_SYSTEM(), adviser_prompt,
                            max_tokens=GEN_TOKENS))).strip()
        ap = os.path.join(STATUS_DIR, "%s.adviser.m%s.md" % (stem, level))
        with open(ap, "w", encoding="ascii", errors="replace") as f:
            f.write("# Adviser note - milestone %s (~%dK tokens)\n"
                    "# session: %s\n# written: %s by %s\n\n"
                    % (level, real_tokens // 1000, stem,
                       time.strftime("%Y-%m-%d %H:%M:%S"), MODEL))
            f.write(adviser + "\n")
        log("ADVISER ok -> %s (%d chars returned)" % (ap, len(adviser)))

        clean = adviser.upper().startswith("CLEAN")
        # Pointer for the hook to inject on the next turn (only if not clean).
        try:
            os.makedirs(STATE_DIR, exist_ok=True)
            ptr = os.path.join(STATE_DIR, stem + ".adviser_ptr.json")
            with open(ptr, "w", encoding="ascii", errors="replace") as f:
                json.dump({"level": level, "path": ap, "clean": clean,
                           "shown": False,
                           "written": time.strftime("%Y-%m-%d %H:%M:%S")}, f)
        except Exception as e:
            log("pointer write failed: %s" % e)
    except Exception as e:
        log("ADVISER failed: %s\n%s" % (e, traceback.format_exc()))


def compute_answer(transcript, stem, cwd, question):
    """Synchronous Adviser answer: read the whole transcript as context plus
    Max's question, call full Opus, and RETURN the reply STRING (no file I/O,
    no pointer). This is the shared core used by the SYNCHRONOUS hook path
    (session_status.cmd_hook calls it inline and prints the result in the same
    turn). Keeps the same quality guards as before: neutralized transcript role
    markers + post-filtered fabricated continuations. The returned body is the
    raw answer (any leading 'ADVISER:' / '**ADVISER**' wrapping is left for the
    caller to strip/wrap). Raises on failure -- the caller wraps in try/except
    + timeout and renders a graceful fallback."""
    question = (question or "").strip()
    if not question:
        raise ValueError("empty question")
    if call_api is None or get_api_key is None:
        raise RuntimeError("cc_recover_v02 API helpers unavailable")
    if not os.path.isfile(transcript):
        raise FileNotFoundError("transcript missing: %s" % transcript)

    real_tokens = turns = tool_calls = 0
    if _analyze is not None:
        try:
            real_tokens, turns, tool_calls, _ = _analyze(transcript)
        except Exception as e:
            log("compute_answer: analyze failed: %s" % e)

    text = _read_full_text(transcript)
    if not text.strip():
        raise RuntimeError("empty transcript text")
    log("compute_answer | model=%s | %d chars | ~%dK tok | q=%r"
        % (MODEL, len(text), real_tokens // 1000, question[:120]))

    ctx = _neutralize_roles(text)
    header = (
        "SESSION CONTEXT (you, the Adviser, are answering Max's direct question)\n"
        "cwd: %s\n"
        "real tokens so far: ~%dK (older context gets summarized near ~840K on the 1M window)\n"
        "turns: %d   tool calls: %d\n\n"
        % (cwd, real_tokens // 1000, turns, tool_calls)
    )
    answer_prompt = (
        header +
        "===== TRANSCRIPT FOR CONTEXT - READ ONLY, DO NOT CONTINUE IT =====\n"
        "The block between the BEGIN and END fences is a transcript of the "
        "session SO FAR, given to you only as background. Turn boundaries are "
        "marked '<turn role=user>' / '<turn role=claude>' / '<turn role=tool>' "
        "(user=Max, claude=the Assistant). It is finished input. You must NOT "
        "extend it, quote its format, or write any further turns.\n"
        "----- BEGIN TRANSCRIPT -----\n"
        + ctx +
        "\n----- END TRANSCRIPT -----\n\n"
        "===== YOUR TASK =====\n"
        "ANSWER MODE. Max just addressed YOU (the Adviser) directly. His "
        "question, with the 'adviser:' trigger stripped, is:\n\n"
        "    " + question + "\n\n"
        "Reply AS THE ADVISER, in your own voice, ONLY your answer to that "
        "question. Hard rules:\n"
        "- Output ONLY your answer. Do NOT reproduce, continue, or imitate the "
        "transcript.\n"
        "- Do NOT emit any '[USER]', '[CLAUDE]', '[TOOL]', or '<turn ...>' "
        "markers, and do NOT invent further turns, instructions from Max, tool "
        "calls, commit hashes, or claims about code being written.\n"
        "- Be terse, conversational, candid, plain English, ASCII only.\n"
        "- Do not use the milestone TO MAX / TO ASSISTANT headers - this is a "
        "one-on-one reply to Max."
    )
    api_key = get_api_key()
    reply = _ascii(call_api(api_key, ADVISER_SYSTEM(), answer_prompt,
                            max_tokens=GEN_TOKENS))
    reply = _strip_fabricated_continuation(reply).strip()
    log("compute_answer ok (%d chars returned)" % len(reply))
    return reply


def run_answer(transcript, stem, seq, cwd, question):
    """ANSWER mode (legacy async path, retained as a fallback). Max addressed
    the Adviser directly. Computes the answer via compute_answer, writes a
    versioned reply and queues it for injection via the same adviser pointer
    the milestone notes use. The live hook now answers SYNCHRONOUSLY and does
    not call this; kept so the `answer` CLI subcommand still works. Fails open."""
    if not os.path.isfile(transcript):
        log("ANSWER: transcript missing: %s" % transcript)
        return
    question = (question or "").strip()
    if not question:
        log("ANSWER: empty question; aborting")
        return
    try:
        reply = compute_answer(transcript, stem, cwd, question)
    except Exception as e:
        log("ANSWER: compute_answer failed: %s\n%s" % (e, traceback.format_exc()))
        return
    try:
        # Sign the answer so Max always sees it is the Adviser speaking: the body
        # reads as "ADVISER: ...". Idempotent (never double-prefix).
        if not reply.lower().lstrip().startswith("adviser:"):
            reply = "ADVISER: " + reply
        rp = os.path.join(STATUS_DIR, "%s.adviser_reply.%s.md" % (stem, seq))
        with open(rp, "w", encoding="ascii", errors="replace") as f:
            f.write("# Adviser reply to Max - seq %s\n"
                    "# session: %s\n# question: %s\n# written: %s by %s\n\n"
                    % (seq, stem, question[:200],
                       time.strftime("%Y-%m-%d %H:%M:%S"), MODEL))
            f.write(reply + "\n")
        log("ANSWER ok -> %s (%d chars returned)" % (rp, len(reply)))

        # Queue via the SAME adviser pointer the milestone notes use; the hook's
        # _inject_pending_adviser injects it once on the next turn. Mark it a
        # reply so the hook can label it as a direct answer to Max's question.
        try:
            os.makedirs(STATE_DIR, exist_ok=True)
            ptr = os.path.join(STATE_DIR, stem + ".adviser_ptr.json")
            with open(ptr, "w", encoding="ascii", errors="replace") as f:
                json.dump({"seq": seq, "path": rp, "clean": False,
                           "shown": False, "reply": True, "question": question[:200],
                           "written": time.strftime("%Y-%m-%d %H:%M:%S")}, f)
        except Exception as e:
            log("ANSWER: pointer write failed: %s" % e)
    except Exception as e:
        log("ANSWER failed: %s\n%s" % (e, traceback.format_exc()))


def main():
    if len(sys.argv) < 5:
        log("bad args: %r" % (sys.argv,))
        return 0
    transcript, stem, level, cwd = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    mode = sys.argv[5] if len(sys.argv) > 5 else "milestone"
    if mode == "answer":
        qfile = sys.argv[6] if len(sys.argv) > 6 else ""
        question = ""
        try:
            if qfile and os.path.isfile(qfile):
                with open(qfile, encoding="utf-8", errors="replace") as f:
                    question = f.read()
        except Exception as e:
            log("ANSWER: reading question file failed: %s" % e)
        try:
            run_answer(transcript, stem, level, cwd, question)
        except Exception as e:
            log("run_answer crashed: %s\n%s" % (e, traceback.format_exc()))
        return 0
    try:
        run(transcript, stem, level, cwd)
    except Exception as e:
        log("run crashed: %s\n%s" % (e, traceback.format_exc()))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main() or 0)
    except Exception as e:
        log("fatal (ignored): %s" % e)
        sys.exit(0)
