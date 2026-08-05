# Scribe handover - milestone 2 (~166K tokens)
# session: 20260620_pedantic_herschel_b726be_f661d4bf
# cwd: C:\moma\.claude\worktrees\pedantic-herschel-b726be
# written: 2026-06-20 16:49:02 by deepseek-v4-pro

# Handover: TextChecker Gmail Inline Fix

## GOAL (Max's words)
Find an open-source/free Grammarly replacement that works inline in the browser, uses the OpenAI API (so it's tunable), and is safe - no data leakage. Install it and make it work on Gmail compose, not just simple text boxes.

## DECISIONS + WHY
- **TextChecker (`codextde/textchecker`)** chosen over other candidates. Claude audited its source: API key stored in browser storage, all outbound calls go directly to `api.openai.com` via the official AI SDK - no proxy, no analytics, no phone-home. This satisfied the "if safe" bar.
- Installed from audited source, not a pre-built zip, to guarantee the code base matches the audit.
- Built locally (Node 22, npm install + `npm run build`). Output is a Chrome MV3 unpacked extension.
- Used the **regular OpenAI project key** (`sk-proj-GnZSL...`), not the admin-scoped key, to limit blast radius.
- Quick test: works on simple text areas (TextChecker's own test page), but completely silent on Gmail's compose window - zero underlines.
- Claude's analysis of the content script: it knows how to handle Google Docs (special class selectors), but **Gmail is treated as a generic `contenteditable` inside iframes** and the hooking logic doesn't fire. The project's open issue tracker has a similar bug for Google Docs.
- Decision: **reproduce the bug in a Playwright-driven Chrome with the extension loaded, then patch the content script** to support Gmail. That avoids guesswork and leverages the existing source.

## CURRENT STATE
- **Extension is installed** in Max's everyday Chrome, pointing to `C:\claude_base\tools\textchecker\chrome-mv3` (the built MV3 output). It is loaded as an unpacked extension. Max has pasted the OpenAI key and selected gpt-4o-mini.
- Real-time mode is enabled, but Gmail compose doesn't trigger anything. The extension shows no errors even with intentionally bad English typed into a reply/compose body.
- The tool's test page (simple textarea) works fine, confirming the extension is alive and the API integration is healthy.
- **Source code** from the audit is at `C:\Users\maxre\AppData\Local\Temp\textchecker_audit` (Windows temp path, also accessible as `/tmp/textchecker_audit` in WSL). This is the full working tree including `src/entrypoints/content.ts`. The built artifact at `C:\claude_base\tools\textchecker\chrome-mv3` contains only the compiled output (no source).
- No code patch has been attempted yet.

## EXACT NEXT STEP
**Set up a Playwright-powered Chrome instance with the unpacked extension loaded, open a Gmail compose window, type errors, and observe the DOM (underlines, console logs, network requests) to diagnose why the extension is silent.**  
Then, **modify `content.ts`** (likely to inject into Gmail's compose iframe and attach proper listeners to its `contenteditable` element) to make inline checking work.  
After a fix, **rebuild the extension** (the source has a build script) and **update the unpacked extension** in Max's real Chrome (or hand him the rebuilt folder).

Crucially, the cold session will need to handle the **Gmail login problem** - either:
- Use a real Gmail account with pre-saved credentials in Playwright's persistent context (risk of touching real data),
- Or create a **local HTML mock** that mimics Gmail's compose structure (iframe + `contenteditable`), allowing isolation of the text-extraction/highlight logic without involving live Gmail. This is safer and faster.

Given the "measure, not guess" directive, start with the mock if possible, then graduate to real Gmail once the patch looks solid.

## OPEN QUESTIONS (still need Max)
- Does Max have a throwaway Gmail account we can use for testing, or should we build a mock page first?
- Does he want the patched extension to also work on Google Docs (the open issue), or is Gmail the priority?
- After the fix, should we preserve the patched source in a permanent location (e.g., a repo fork or a local versioned folder under `c:\claude_base\tools\textchecker-src`) so future updates can be rebased?

## KEY PATHS / IDS
- **Extension folder (live)**: `C:\claude_base\tools\textchecker\chrome-mv3`
- **Audited source clone**: `C:\Users\maxre\AppData\Local\Temp\textchecker_audit` (temporary - may be gone after reboot)
- **Content script to patch**: `src/entrypoints/content.ts` inside the source clone
- **Build command**: `npm run build` (generates `dist` or `.output` folder)
- **OpenAI key used**: `sk-proj-GnZSL...` (the regular project key, already pasted into extension options)
- **Tool repo**: `https://github.com/codextde/textchecker`
- **Relevant issue**: Open issue "Not working on Google Docs" (same root cause suspected)

## GOTCHAS
- Gmail compose is an **iframe with a `contenteditable` div**, not a standard `<textarea>` or `<input>`. The extension's content script must run inside the iframe or use `all_frames: true` and then listen to the correct element.
- The extension's real-time check uses a `MutationObserver` that may not trigger on `input` events within `contenteditable` - it might rely on `keyup` or selection changes.
- The forced-check shortcut `Ctrl+Shift+G` (mentioned in the code) might also fail if the script doesn't know which "field" to check.
- The existing code already has a **special Google Docs path** (looks for `kix-*` classes), but Gmail uses completely different DOM structures (e.g., `div[aria-label="Message Body"]` or similar). Any Gmail fix must coexist with that.
- The source clone was in `/tmp`; if the session restarts and the /tmp is cleared, **re-clone from GitHub** and then apply any fixes. Better: immediately copy the source to `C:\claude_base\tools\textchecker\src` as a permanent working tree.
- The extension's manifest uses `<all_urls>` permission, which means it can inject into any iframe - good for Gmail, but the content script's `match` patterns might need to include Gmail's email page URLs (e.g., `*://mail.google.com/*`). Check that the injected script actually runs in the Gmail tab's main frame; if not, adjust manifest or use `content_scripts` with `all_frames: true`.
