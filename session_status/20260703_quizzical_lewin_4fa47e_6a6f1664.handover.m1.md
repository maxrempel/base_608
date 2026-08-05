# Scribe handover - milestone 1 (~111K tokens)
# session: 20260703_quizzical_lewin_4fa47e_6a6f1664
# cwd: C:\claude_base\.claude\worktrees\quizzical-lewin-4fa47e
# written: 2026-07-03 12:54:35 by deepseek-v4-pro

# HANDOVER: Quizzical-Lewin-4fa47e - B11B

---

## GOAL (in Max's words, paraphrased)
Pick ~5-6 songs for his singing quartet (trio, actually quartet) from an existing catalog database. For each, find the **most recent performance video** already downloaded on the local drive (TEAL 16 / "Centauri"). Cut roughly the performance segment from the full video with ffmpeg, upload the resulting mp4 files to Cloudflare (R2 or similar), and present them as a **webpage with playable links** - a practice list for the four singers. This will be a batch system: a new subfolder for each week's songs, starting now.

---

## DECISIONS MADE + WHY (so far)
- **Attendance check:** Ran `bcast.py whoami B11B` - confirmed session identity as B11B. (0.36ms)  
- **Delivery method:** Cloudflare, not Nextcloud. Max explicitly said: "Forget Nextcloud... share them through Cloudflare." Reason: Cloudflare can handle small mp4 files; easier to make public/shareable.  
- **Cutting:** "very approximate cutting" - not precise trimming; just extract the relevant part from the full club recording.  
- **Batch folder structure:** Top-level folder will be created, then subfolders for each weekly batch.  
- **Toolchain:** Use ffmpeg for extraction. Source videos on teal16 (likely a mapped drive or accessible path). The catalog database is the TAMZA songs pipeline (handover file read was `TAMZA_HANDOVER_START_HERE_v01_tomemex.md`).  
- **Most recent performance:** Defined as "newest date the song was sung, pulled from the catalog." Confirmed with Max via a ? check; awaiting his confirmation before proceeding.  
- **Next action:** Waiting for the song list from Max before any further steps.

---

## CURRENT STATE
- Session is idle. Claude just read the TAMZA handover file to orient himself, confirmed identity, interpreted the task, and sent a prompt back to Max: "Send the list."  
- No file operations, no database queries, no video extraction started.  
- The last message (turn 3, tool result) ended with Claude asking for the songs.

---

## EXACT NEXT STEP
**Wait for Max to provide the list of 5-6 song titles/identifiers.** Once received, the plan (already outlined and agreed upon in principle) is:

1. Query the TAMZA catalog/database for the most recent performance of each song (by performance date).  
2. Locate the corresponding video file on teal16 (Centauri).  
3. Use ffmpeg to roughly cut/extract the song segment.  
4. Create the batch folder structure (new weekly subfolder).  
5. Upload cut mp4(s) to Cloudflare (R2 bucket or similar).  
6. Generate a simple webpage with playable links (likely linking to the Cloudflare-hosted files).  
7. Return the webpage URL/list to Max.

**Do not start until the song titles are provided.**

---

## OPEN QUESTIONS (awaiting user)
- **Did the ? confirmation of "most recent performance = newest date" get accepted?** Claude posed it as a confirm; Max hasn't explicitly replied yet. Assume it's accepted unless Max corrects.  
- **The song list itself** - not yet provided.

---

## KEY PATHS / IDS / NAMES
- **Session ID:** B11B  
- **Worktree:** `C:\claude_base\.claude\worktrees\quizzical-lewin-4fa47e`  
- **Attendance script:** `C:/claude_base/branch_bulletin/bcast.py` (accepted `whoami B11B`)  
- **TAMZA catalog handover:** `C:\claude_base\tools\tamza_songs\pipeline\TAMZA_HANDOVER_START_HERE_v01_tomemex.md` (content not shown, but indicates DB structure/location)  
- **Source video drive:** "TEAL 16" / "Centauri" - exact mount point or UNC path not yet resolved. Will need to discover it from the handover or environment.  
- **Cloudflare:** Likely R2 bucket name/token needed; not yet configured. Must be retrieved from project configuration.  
- **Batch folder naming:** Not defined yet; will need to decide a convention (e.g., `YYYY-MM-DD_Batch01`).  
- **Webpage hosting:** Not specified - maybe Cloudflare Pages or a simple static file served by R2. Need clarification or a default.

---

## GOTCHAS / DEAD ENDS RULED OUT
- **Nextcloud sharing is ruled out** - Max explicitly switched to Cloudflare. Do not attempt Nextcloud uploads.  
- **YouTube download not needed:** Files already exist locally on teal16. Do not try to scrape or download from YouTube.  
- **Not a full video trim:** Just approximate cutting, so precision is not required.
