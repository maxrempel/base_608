# Scribe handover - milestone 2 (~151K tokens)
# session: 20260629_sweet_hofstadter_288bd4_cba82651
# cwd: C:\moma\.claude\worktrees\sweet-hofstadter-288bd4
# written: 2026-06-29 22:16:40 by deepseek-v4-pro

GOAL (Max's words)  
"in image preview why don't i see the libretto lines in image popup? Fix, there is space under comments."

DECISIONS + WHY  
- The assistant traced the popup's line-rendering logic to `popup.js` (shared_ui) and the `/api/vocal_lines` endpoint. The popup container `jp-vocal-lines` is populated for all job types, but the data comes from the server, keyed by scene.  
- No decision has been made yet. The assistant hypothesised that sc11 has **no script lines loaded**, unlike sc10/sc09 which do, and asked Max whether to load sc11's lines and whether to show them under the comments (right panel) instead of the left panel.  
- The assistant also brought up a separate staging/prompt issue for sc11 (circle vs. line arrangement), but that is not the primary focus; it is an open question.

CURRENT STATE  
- The image popup renders fine otherwise; the `jp-vocal-lines` section is present but empty for sc11.  
- No code changes have been made. The assistant is awaiting user input on two things:  
  1. Whether to load script lines for sc11.  
  2. Where to display them - they currently suggest under comments (right panel).  
- The staging discussion about circle prompts and camera angles is a distinct issue that Max may or may not want help with.

EXACT NEXT STEP  
1. Get Max's confirmation: load sc11's libretto lines (via the `/api/vocal_lines` or equivalent data entry) and display them in the popup.  
2. Clarify placement: "right panel, under comments" means moving the `jp-vocal-lines` container into the comments column (likely inside `jp-comments` or after it in the right-side layout) rather than keeping it in the left information panel.  
3. Implement:  
   - Ensure sc11 has script lines in the database.  
   - Adjust the popup template/CSS to move the libretto lines block to the right panel, beneath the comments list, to use the existing space.  
   - Test with an sc11 image to verify lines appear and layout is correct.

OPEN QUESTIONS (awaiting Max)  
- "Do you want sc11's script lines loaded so they appear, and shown under the comments (right panel) rather than the left?"  
- (Separate) Should the assistant draft circle-staging prompts for sc11 and update the staging bible to use a circular arrangement with varied camera angles?

KEY PATHS / IDS  
- Core file: `C:\moma\.claude\worktrees\sweet-hofstadter-288bd4\sc10\shared_ui\popup.js` - line-rendering logic, `_getVocalLines` around line 1159, HTML template with `jp-vocal-lines` container.  
- API: `/api/vocal_lines` (scene key ? array of line objects).  
- CSS classes: `jp-vocal-lines`, `jp-vl-current`, `jp-vl-other`.  
- Worktree: `sweet-hofstadter-288bd4`, scene sc11.

GOTCHAS / DEAD ENDS  
- The popup file is shared across all scenes; any template/code changes affect sc09, sc10, etc. Be aware that moving the libretto block may disrupt other scenes' popups if they rely on the current left-panel position. Test across scenes.  
- The reason the lines are missing is almost certainly that sc11's database has no vocal/script lines. Loading them is a separate data entry task (perhaps import from script).  
- The user mentioned "space under comments" - the assistant interpreted this as the right panel having unused vertical space where libretto lines could be placed. Confirm if the design intent is to fully relocate the block or merely duplicate/supplement it.
