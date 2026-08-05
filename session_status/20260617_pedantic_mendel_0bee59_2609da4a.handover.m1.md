# Scribe handover - milestone 1 (~126K tokens)
# session: 20260617_pedantic_mendel_0bee59_2609da4a
# cwd: C:\claude_base\.claude\worktrees\pedantic-mendel-0bee59
# written: 2026-06-17 15:22:29 by deepseek-v4-pro

# HANDOVER - B26juniorconnector, Session 1

---

## GOAL (in Max's words)

Two jobs for this role:

1. **Junior connector/poker on the whole picture.** The project is reaching its end point: a clean database plus live catalogue. Newly-identified songs should go live; unknowns shouldn't. Don't decide unilaterally - poke the relevant owners, suggest what to do, but let them decide individually and collectively. Not a doer yet; qualify first.

2. **Pick one oldest good NONH video** (one not yet touched by human timecoders), annotate it, double-check the draft, and hand it over to human timecoders. Repeat this handover weekly.

---

## DECISIONS MADE + WHY

### Go-live publishing rule (Max's directive, clarified)
- **Identified songs go live** - the ~12-20% of NONH segments that matched a known song with high confidence get published to the live site.
- **Unknowns stay held** - the ~88% marked UNKNOWN remain off the live site until a human resolves them.
- **Nuance added by Max this session:** a spoken introduction also qualifies as "identified." If a performer says "this is my song," or names the authors (e.g., "this is Berkovsky, Nikitin, Sukharev"), that segment is treated as identified and can go live. The identification doesn't need to come only from the automated matcher - performer self-announcement counts too.

### Connector posture
- Registered as **B26juniorconnector** on the team board.
- Role is not to design solutions but to surface the directive, ask the right owners to react, and let them propose the path. Specifically, Max's rule was relayed to **b15merger**, **b7i**, and **b10** - the build-side owners - with an ask for them to propose the cleanest publish path with a confidence gate.

---

## CURRENT STATE

### Pipeline status (from B25's START-HERE handover + full board read)
- The song-indexing pipeline is **~90% built and mostly run**.
- **NONH (not-yet-human-indexed) videos:**
  - Captions fetched for 691 videos.
  - Songs split by spoken-intro boundaries (691).
  - A frozen reference set of 994 known songs built.
  - Every segment matched as KNOWN or UNKNOWN.
  - Reality: only ~12-20% come back confidently identified; the system deliberately kept precision high (~88% correct on identified ones). The rest are honest UNKNOWNs.
- **Human-side catalogue:** re-timed, ready to publish.
- **Website:** live (voting, login, playlists already working).
- **One real blocker:** 93 videos have no captions and need speech-to-text processing on Sol - but Sol is off-limits because its RAM is being tested. No workaround yet.

### Board communication done this session
- Posted introduction as B26juniorconnector.
- Posted Max's go-live directive to the whole board, specifically calling b15merger, b7i, and b10 to react and propose the publish path.
- Asked Max to confirm understanding of the rule - and Max confirmed, adding the spoken-introduction exception.

### Own hands-on task
- Read the per-stage workflow map (`CURRENT_WORKFLOW_v01_tomemex.md`) - aware of the 6-stage pipeline but haven't yet begun the "pick oldest good NONH video" task.

---

## EXACT NEXT STEP

1. **Start the hands-on task:** identify the oldest NONH video that is "good" (has captions, reasonable quality, not yet annotated by humans), open its draft match results, double-check the annotations, and prepare it for handoff to human timecoders. The workflow map in `CURRENT_WORKFLOW_v01_tomemex.md` describes the stages - likely at Stage 4 or 5 for this.

2. **Monitor board for responses** from b15merger, b7i, b10 on the publish-path proposal. If no response by next check, poke again.

3. **One blocker to track:** Sol availability for the 93 captionless videos. Someone needs a plan for when RAM testing finishes.

---

## OPEN QUESTIONS (awaiting Max or the team)

- **No response yet** from b15merger/b7i/b10 on the publish path design. The ball is in their court.
- **Sol ETA:** when does RAM testing finish, and who handles queuing the 93 captionless videos once Sol is available?
- **Confidence threshold:** what numeric threshold constitutes "confident" for the go-live gate? The team has precision at ~88% on identified ones; does that need formalising as a threshold or is the current matcher output good enough?

---

## KEY PATHS, IDS, COMMANDS

| What | Value |
|---|---|
| Board registration command | `python "C:/claude_base/branch_bulletin/bcast.py" whoami B26juniorconnector` |
| Catch-up command | `python "C:/claude_base/branch_bulletin/bcast.py" catchup` |
| Post to board | `python "C:/claude_base/branch_bulletin/bcast.py" post "..."` |
| Read board | `python "C:/claude_base/branch_bulletin/bcast.py" read` |
| Primary handover doc | `C:\claude_base\tools\tamza_songs\pipeline\TAMZA_HANDOVER_START_HERE_v01_tomemex.md` |
| Workflow map | `C:\claude_base\tools\tamza_songs\pipeline\CURRENT_WORKFLOW_v01_tomemex.md` |
| Board history dump | `C:\Users\maxre\.claude\projects\C--claude-base--claude-worktrees-pedantic-mendel-0bee59\2609da4a-ffe1-4a87-8816-db38b8138d59\tool-results\bbjr9lwex.txt` |
| My role ID | `B26juniorconnector` |
| Key owners to poke | `b15merger`, `b7i`, `b10` (build/publish); Sol owner unnamed (blocker) |
| Pipeline stages | 6-stage; segments are at matching/classification stage for NONH |
| Reference songs | 994 known songs in frozen reference |
| NONH total | 691 videos processed to segment+match stage |
| Captionless videos | 93 - blocked on Sol |

---

## GOTCHAS

- **Spoken introductions count as identification.** Max explicitly added: if a performer announces the song or credits the authors on tape, that segment IS considered identified and eligible for go-live - even if the automated matcher labelled it UNKNOWN. The connector and any publisher must account for this. It means the matcher output alone isn't the final word; human-visible intros override UNKNOWN to KNOWN.
- **Sol is a hard blocker** for 93 videos. No parallel path. Don't waste effort trying to route around it unless someone explicitly opens a workaround.
- **Precision was prioritised over recall** by design - so low identification rate (~12-20%) is a feature, not a bug. Don't push to loosen matching to raise coverage.
- **The board uses a cursor system** - always run `read` after `catchup` to advance past already-seen messages before posting.
- **This session had ~126K tokens** used; the 1M context window means older content will be summarized around ~840K. Future connector sessions should re-read the START-HERE handover if compacted.
