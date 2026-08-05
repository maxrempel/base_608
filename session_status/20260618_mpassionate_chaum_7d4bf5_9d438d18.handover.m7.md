# Scribe handover - milestone 7 (~526K tokens)
# session: 20260618_mpassionate_chaum_7d4bf5_9d438d18
# cwd: C:\moma\.claude\worktrees\compassionate-chaum-7d4bf5
# written: 2026-06-18 15:41:45 by deepseek-v4-pro

# HANDOVER - D24: Merge Sync & Propagation

**SESSION:** D24 (checked in from D22)  
**CWD:** `C:\moma\.claude\worktrees\compassionate-chaum-7d4bf5`  
**TURNS:** 274, tool calls: 213, real tokens ~526K

---

## GOAL (Max's words, verbatim)
> "the process should be reverse of libup - yes the merges should propagate to notion!!! backwards!!! what happens to audio merges? BTW, i want smaller gaps in audio line merges. And audio needs to be reassembled with smaller gaps. I don't care about the direction. It should be synked. I ask a chat, please rearrange merges, and it should propagate synked merges all way though. ... someone did the merge!!! it must know . To avoid such confusions, there must be a trace of rearrangement started and propagation in database. The initial push- merge these 3 lines. Or rearrange - should be tracked!!!! No hidden surgery"

Later, after I proposed a `merge_ops` audit ledger:
> "should you own the sync or D21, i think you can do it"

**Interpretation:** Max wants a **traceable, synced merge pipeline** where any rearrangement command (merge lines into a beat) leaves a database record and propagates automatically through **audio reassembly ? script lines collapsing ? lipsie fire ? Notion update**, with **smaller silence gaps** between spliced audio lines. D24 is to **own** building this sync, not D21.

---

## DECISIONS MADE & WHY

1. **Merge operations must be tracked in a new D1 table (`merge_ops`)**  
   *Why:* Current merges are ad?hoc (throwaway Python scripts building synthetic hashes) with no record of what happened, making it impossible for a later session or Max to see what was done. A central ledger solves "no hidden surgery."

2. **The `merge_ops` table will include:**  
   - `id`, `created_at`, `session` (D?number)  
   - `op` = merge / split / rearrange  
   - `request` = the exact human command  
   - `scene_id`, `arrangement_id`, JSON array of `member_line_hashes`  
   - `merge_hash` (unique identifier for the combined audio)  
   - `gap_s` - the silence gap used when concatenating (Max wants this smaller; exact value TBD)  
   - A **propagation checklist** with timestamps: `audio_reassembled`, `script_lines_collapsed`, `lipsie_fired`, `notion_synced`  
   *Why:* This makes every step traceable and allows recovery if something breaks mid?propagation.

3. **Propagation must go through the *canonical* pipeline, not ad?hoc scripts**  
   The existing pipeline:  
   - `merges.json` (or equivalent) ? `sass.py` merge ? audio reassembly ? `libup.py` merge (collapses `script_lines`) ? lipsie fire (via `combo_gui` or worker) ? Notion update  
   *Why:* Bypassing it creates desync; using the canonical path guarantees all downstream consumers stay consistent.

4. **The gap in audio merges will be a first?class field (`gap_s`)** and must be **smaller than the 0.25-0.35 s currently used** (exact value TBD, likely 0.1-0.2 s).  

5. **Notion writes are risky** - every write must be preceded by a page snapshot and verified afterwards (Notion silently fails otherwise). The existing `libup.py` can lift *from* Notion, but reverse?writing is new ground.

6. **Ownership:** D24 will build the `merge_ops` table + the propagation function(s) and hook them into the existing sass/libup code. D21 can continue producing lipsies if needed, but the sync should be callable by any session.

---

## CURRENT STATE

**sc10 lipsie production:**  
- arr01 (greeting) is approved (job 2774), using a formal?officials prompt with characters described before lines.  
- arr02-04 were partially fired with various stills; many incorrect (wrong location, wrong speaker order) were junked.  
- The final rearrangement done by D21 attempted to cover the whole scene as ~4?line merged lipsies, using stills traced from the spine. Some chunks worked, others still have issues (e.g., alcove 2793 switched speakers, refired as 2796 with describe?both?first).  
- A large number of junk/error/orphan jobs clutter the scene view (143 junk lipsies, 36 error, 43 orphans) - a side effect of the scene?picker change that D22 implemented (now showing *all* jobs of a scene, not per?arrangement). This is a separate cleanup task.

**Infrastructure built in this session (D22 ? D24):**  
- **lipser UI**: shows actual dialogue lines (parsed from prompts), comment boxes moved to the actions column.  
- **Scene picker**: replaced per?arrangement filter with a per?scene filter - shows all arrangements of a scene at once in clipper/lipser/imager. Mixboard/storyboard already worked per?scene.  
- **Lipsie trim dialog**: fixed audio going silent when scrubbing (video now unmuted in trim, start handle no longer force?pauses).  
- **Batches & comment timestamps**: added `commented_at` column to `jobs` (via Cloudflare D1 MCP), built `batches.py` that clusters lipsie fire?times into batches and can retrieve comments for the last N batches. Documented in `batches_method_v01_tomemex.md` and referenced in MEMORY.md; broadcast to D21.  
- **Memory rules**: raised "always merge+push before asking Max to verify" to HARD RULE #1.  
- All of the above is committed, pushed to master, and running live.

**What is NOT done - the merge sync:**  
- `merge_ops` table does not exist yet.  
- No function ties a rearrangement command to the canonical pipeline.  
- Audio reassembly with smaller gaps is still handled by one?off scripts; merges are not synced to `script_lines`/Notion.  
- D21 may still be firing ad?hoc merges (the batch is running). The new sync should be retro?fittable or D21 should switch to using it when ready.

---

## EXACT NEXT STEP

**Build the merge?sync pipeline, step?by?step:**

1. **Create the `merge_ops` table in D1** - use Cloudflare D1 MCP (since the HTTP API blocks ALTER). Columns as described above.

2. **Implement a canonical merge function** (e.g., a new module `merge_ops.py` or extend `sass.py`) that:  
   - Accepts: scene_id, arrangement_id, list of line_hashes, gap_s, an optional "auto?lipsie" flag.  
   - Inserts a `merge_ops` row with `status = 'started'`.  
   - Builds the merged audio via the **existing sass** audio concatenation, passing the new gap.  
   - Updates `merges.json` (or the equivalent configuration that `libup merge` reads).  
   - Runs `libup merge` to collapse the lines in `script_lines`.  
   - If `auto?lipsie` is true, fires a lipsie job on the appropriate still (needs a still?selection policy; perhaps the same prompt template as the approved arr01, but with the merged audio path).  
   - Calls the **Notion reverse?sync**: update the `## ARRANGEMENT ...` block on the scene's Notion page with the new member lines. (Must snapshot page first.)  
   - Stamps the propagation checklist fields as each step completes.  

3. **Expose a simple CLI** (`python merge_ops.py merge ...`) that any future session can call, so the command `"merge lines 6,7 with gap 0.15s"` directly creates the trace and triggers propagation.

4. **Once built, test with a small merge** (maybe one of the sc10 chunks) to see the full trace appear.

---

## OPEN QUESTIONS (awaiting Max)

1. **Exact desired audio gap?** Smaller than 0.25 s - is 0.1 s good, or something else?  
2. **Notion sync details:** Should we **only** update the `## ARRANGEMENT` blocks (replacing the member lines), or also adjust line numbering? Should the raw dialogue lines remain untouched? Should we fully rewrite the script page's structure or just touch arrangement blocks?  
3. **Lipsie firing:** Should the sync automatically **fire** a lipsie after every merge, or only when explicitly requested? If auto, which still to use? (We may need a still?to?arrangement mapping.)  
4. **Existing ad?hoc merges:** Should we back?fill `merge_ops` for the sc10 merges already done, or just establish the rule going forward?  
5. **D21's role:** D21 is currently the active production session. Does D24 take over production after building the sync, or should D21 start using the new merge?sync function once D24 finishes?

---

## KEY PATHS & IDs

- **D1 database:** accessed via `moma_db.py` in `sc10/combo_runner/code/`
- **Audio merge
