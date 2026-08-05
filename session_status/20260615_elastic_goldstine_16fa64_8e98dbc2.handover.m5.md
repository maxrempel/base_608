# Scribe handover - milestone 5 (~89K tokens)
# session: 20260615_elastic_goldstine_16fa64_8e98dbc2
# cwd: C:\claude_base\.claude\worktrees\elastic-goldstine-16fa64
# written: 2026-06-15 08:43:40 by deepseek-v4-pro

# HANDOVER - B12: Modify Top-20 Names (Performers + Authors)

---

## GOAL (in Max's words)

> "Your task is to modify the names."

Max provided a corrected/updated list of **???-20 ????????????** (Top 20 Performers), each with a name and a count. Then:

> "???-20 ??????? ?????? - ???-20 ??????? ?? ?????????? ??????????, ?? ?? ? ?????????????."

Translation: Add a **Top-20 Authors** section - authors ranked by number of performances, in the same format as the performers list. Also ensure the performers list uses the corrected names/counts provided.

---

## DATA PROVIDED BY MAX

Corrected **Top-20 Performers** list (name + count):

| # | Name | Count |
|---|------|-------|
| 1 | ?????? ?????? ??????? | 1159 |
| 2 | ?????? ??????? | 985 |
| 3 | ??????? ????????-??????? | 981 |
| 4 | ???? ??????? | 806 |
| 5 | ???? ???????? | 800 |
| 6 | ??? ????????? | 723 |
| 7 | ????? ???? | 602 |
| 8 | ???????? ???????? | 594 |
| 9 | ????????? ?????? | 565 |
| 10 | ???????? ?????? | 534 |
| 11 | ?? ??????? | 522 |
| 12 | ??????? ???????? | 447 |
| 13 | ????? ??????? | 435 |
| 14 | ?????? ????????? | 429 |
| 15 | ?????? ??????? | 422 |
| 16 | ????????? ?????? | 400 |
| 17 | ?????? ??????? | 399 |
| 18 | ???? ?????????? | 394 |
| 19 | ???? ??????? | 383 |
| 20 | ?????? ???????? | 363 |

Additionally: **???-20 ???????** (Top-20 Authors) must be generated - same ranking logic (by number of performances), same display format.

---

## DECISIONS + WHY

- **No decisions made yet** - this branch (B12) was just created from B10's session. The assignment was stated but zero work has been done. No tool calls occurred for B12.
- B10's work (adding a "????????" button to the player) was explicitly handed off and is **not** B12's concern.

---

## CURRENT STATE

- **Branch B12 is fresh**, with no modifications.
- The working directory is `C:\claude_base\.claude\worktrees\elastic-goldstine-16fa64`.
- The live application under modification is almost certainly:  
  **`C:\claude_base\tools\tamza_songs\pipeline\output\app.js`**  
  (This is the file B10 was inspecting and is the compiled/live frontend app.)
- The board/Max has not clarified *where* these top-20 lists live - likely they are either:
  - Hardcoded data arrays inside `app.js`, or
  - A data file that feeds into the pipeline, or
  - Part of an HTML template rendered by the pipeline.
- **No modifications have been made yet.**

---

## EXACT NEXT STEPS

1. **Locate the existing Top-20 performers in the codebase.** Search for known performer names (e.g. "??????", "??????", "???????") inside:
   - `tools/tamza_songs/pipeline/output/app.js`
   - Any data JSON/JS files in `tools/tamza_songs/pipeline/`
   - Any HTML templates in that pipeline.

2. **Update the performers list** to match Max's corrected names and counts exactly (including "???????" with the capital ?, which looks intentional - possibly a typo fix marker).

3. **Generate or add the Top-20 Authors list** following the same logic (by number of performances). This may require:
   - Finding the underlying song dataset (likely a JSON or JS array of songs, each with `author` and `performer` fields).
   - Aggregating counts by author.
   - Ranking top 20 by count.
   - Inserting the new list into the UI in the same format as performers.

4. **Confirm with Max** where the output should appear (same page/section as performers? a new section?).

---

## OPEN QUESTIONS (awaiting Max)

- **Where exactly do these top-20 lists live?** - in `app.js`? A separate data file? An HTML page?
- **Is the Top-20 Authors list pre-calculated and provided, or must it be computed from the song dataset?** - Max's phrasing "??????" suggests the data may need to be derived from existing source data.
- **What is the display context?** - Is this for the same radio/player page B10 was working on, or a different report/page entirely?
- **Is "???????" with mixed-case ? intentional**, or a typo to be normalized?
- **Should any corresponding pipeline build step be re-run** after modifying source data, or is direct editing of `app.js` acceptable?

---

## KEY PATHS / IDS

- **Working tree:** `C:\claude_base\.claude\worktrees\elastic-goldstine-16fa64`
- **Live app (probable target):** `C:\claude_base\tools\tamza_songs\pipeline\output\app.js`
- **Pipeline directory:** `C:\claude_base\tools\tamza_songs\pipeline\`
- **Branch bulletin system:** `C:\claude_base\branch_bulletin\bcast.py` (used with `whoami`, `catchup`, etc.)
- **Branch ID:** B12

---

## GOTCHAS

- **The previous session (B10) was doing file reads and greps in this same codebase**, but none of those reads modified anything. Still, B10 established that `app.js` is a large, minified-looking file (likely a webpack/Vite bundle). If the top-20 data is embedded inside it, it may be generated from upstream source files. Editing `app.js` directly could be fragile if a rebuild overwrites it.
- **The pipeline directory has a `README_tomemex.md`** - this may document the build process and upstream data sources. Check it before editing.
- **No data source for songs has been confirmed yet.** A search for song arrays, JSON files, or CSV dumps in `tools/tamza_songs/` will be necessary.
- **Max's performer counts are definitive** - do not recompute performer counts; use his numbers as-is. The author counts, however, likely need computation unless Max provides them separately.
