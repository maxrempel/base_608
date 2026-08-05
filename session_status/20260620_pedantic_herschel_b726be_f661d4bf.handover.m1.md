# Scribe handover - milestone 1 (~121K tokens)
# session: 20260620_pedantic_herschel_b726be_f661d4bf
# cwd: C:\moma\.claude\worktrees\pedantic-herschel-b726be
# written: 2026-06-20 16:32:32 by deepseek-v4-pro

# HANDOVER - Grammarly Alternative Research Session

---

## GOAL (Max's words)

Find an open-source or free Grammarly substitute that:
- Edits inline (underlines + click-to-fix popovers, Grammarly-style)
- Uses a real LLM - OpenAI API is fine, but open to better alternatives
- Is tunable (unlike Grammarly's locked-down behavior)
- Browser-only is sufficient (Chrome extension)
- Is **safe** - no API key theft, no data exfiltration to third parties
- Not Harper (Max explicitly rejected it: rule-based, not LLM-driven)

> *"harper is certainly not What I want? I want real LLM-based. I'm happy with OpenAI API, so certainly OpenAI API."*

---

## DECISIONS MADE + WHY

| Decision | Reasoning |
|---|---|
| Harper ruled out | It's 100% local rule-based Rust engine - excellent grammar/spelling but zero LLM, zero tunable rewrites. Max wants LLM tone/style control, which is the whole point of using OpenAI. |
| LanguageTool ruled out | Formerly good open-source option, but browser extension has moved toward paid/premium - same subscription annoyance as Grammarly. |
| Not installing anything unvetted | Several 0-3-star GitHub repos claim to be OpenAI-grammar extensions. Claude flagged these as too risky without source audit: they get your API key + live keystroke feed. Max's safety bar is high. |
| Web search in this environment is weak | Initial WebSearch calls returned generic AI-landing-page noise, not real project pages. Claude pivoted to GitHub API queries (`gh search repos`, `gh api`) which are authoritative. |
| ChatGPT's training data is stale/distrusted | Max explicitly told Claude not to trust its training. The names ChatGPT suggested (TextChecker, Correctly, Scramble) need independent verification. |

---

## CURRENT STATE - What's Done

- **Harper**: Fully confirmed real. GitHub: `Automattic/harper`, 10.9k stars, active, safe, Chrome extension, inline underlines + click-to-fix. **But rejected by Max** - wrong category (rule-based, not LLM).
- **TextChecker**: **Not yet verified.** Claude attempted to find it via WebSearch, GitHub search, and WebFetch of `github.com/dotcorr/correctly` (confabulated path). No confirmed repo located yet. Max believes TextChecker should be the best option and wants it properly researched.
- **Correctly / Scramble**: Also unverified - likely ChatGPT confabulations or extremely obscure single-author repos. Claude hasn't ruled them out definitively but couldn't confirm them.
- **Security posture established**: Claude's audit-first stance before any OpenAI-extension install. Max hasn't pushed back on this - safety requirement stands.

---

## EXACT NEXT STEP

**Research TextChecker properly with fresh online search.** Max's instruction:

> *"check out TextChecker. I think TextChecker should be the best, but search online. Don't trust your training, which is very old."*

What a cold session should do:

1. **Search for "TextChecker" specifically** - use multiple approaches:
   - `gh search repos "TextChecker"` - exact name match on GitHub
   - Web search for `TextChecker chrome extension grammar openai`
   - Check Chrome Web Store for "TextChecker"
   - Check for a website, docs, or npm package
   
2. **If TextChecker is real**: Fetch its README, check stars, last commit, author credibility, and audit what it sends where (API calls, telemetry). Determine if it does inline real-time checking vs. highlight-then-fix.

3. **If TextChecker is confabulated/doesn't exist**: Acknowledge this honestly, then pivot to finding the **actual best** existing alternative. The gap is real: no polished open-source Chrome extension that does inline Grammarly-style underlines + OpenAI-tunable rewrites. Options to explore:
   - Any newer projects since training cutoff
   - Self-built approach (this was mentioned as a fallback earlier - a lightweight Chrome extension that calls OpenAI API is architecturally simple)
   - Any "bring your own key" extensions on Chrome Web Store with actual user bases

4. **Report back** with: existence, safety, capabilities, install method.

---

## OPEN QUESTIONS (awaiting Max)

- **What exactly does Max want tuned?** Is it tone (formal/casual), domain vocabulary, rewrite aggressiveness, or something else? Grammarly's annoyance was being un-tunable, but the specific pain points weren't detailed. This matters for prompt design.
- **Budget posture**: Max is happy paying OpenAI API costs (cents/month with GPT-4o-mini). Not clarified whether he wants GPT-4o-mini, GPT-4o, or wants recommendation.
- **Willingness to self-build** if nothing safe exists? This was briefly floated earlier but not addressed.

---

## KEY PATHS / IDS / COMMANDS

| Item | Detail |
|---|---|
| Working directory | `C:\moma\.claude\worktrees\pedantic-herschel-b726be` |
| Real project confirmed | `Automattic/harper` - 10.9k stars, Rust, local-only grammar engine |
| Harper web demo | `https://writewithharper.com` |
| Harper Chrome extension | Available, fully local |
| TextChecker | **UNVERIFIED** - target of next search |
| Correctly | **UNVERIFIED** - likely confabulated; `github.com/dotcorr/correctly` returned 404 |
| Scramble | **UNVERIFIED** |
| GitHub search tool | `gh search repos` and `gh api` are available and work in this environment |
| Web tools available | WebSearch, WebFetch - but WebSearch proved weak for niche tools |
| Session tokens so far | ~121K (1M window, compacts near ~840K) |
| Turns | 13 turns, 11 tool calls |

---

## GOTCHAS - Dead Ends Ruled Out

- **Do not trust ChatGPT's project names.** It confidently named TextChecker, Correctly, Scramble. At minimum Correctly was a 404 when Claude tried the obvious GitHub path. Assume any name needs verification.
- **Do not use WebSearch alone.** It returned generic AI-tool directory SEO spam. GitHub direct queries (`gh search repos`, `gh api`) are higher-signal.
- **Harper is not a fallback.** Max was unambiguous - he wants LLM-based, not rule-based. Don't re-suggest it.
- **LanguageTool is a dead end** for this use case (browser extension went paid/premium).
- **Most "Grammarly + OpenAI" Chrome extensions on GitHub are 0-3 stars, single-author, unmaintained.** The ones that exist are unvetted. An audit-first approach is correct.
- **No code was written or installed yet.** This session was purely research. Nothing is in flight.
