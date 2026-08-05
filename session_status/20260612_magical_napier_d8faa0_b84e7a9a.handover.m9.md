# Scribe handover - milestone 9 (~143K tokens)
# session: 20260612_magical_napier_d8faa0_b84e7a9a
# cwd: C:\claude_base\.claude\worktrees\magical-napier-d8faa0
# written: 2026-06-12 14:27:34 by claude-opus-4-8

# HANDOVER - XG1 / Starseed Form Registrants ? D1 Database

## GOAL (in Max's words)
Started as: "I can't find the session that did that - starseed form submissions - review in my gmail and in database and in google forms... two more form entries arrived... I need to update." Then: "summarize each person['s] experience and overall picture - make me a sound-compatible summary and send an mp3 to telegram read by default fish male voice." Now (current open question): "I ponder if I can discuss the database with cl web? It should have access to db, right? What is the prompt for it? Like 'look at starseed db'?"

Max wants to know whether Claude on the web (claude.ai) can directly access his starseed database, and if so, what to type to get it to look at it.

## DECISIONS + WHY
- **Used the LIVE form responses sheet, not the search metadata.** The Drive search showed a "modifiedTime" of Feb 7, which looked stale/wrong given that new responses had arrived. Reading the actual file content confirmed the content was current (14 real registrants + one test row). Lesson applied: trust the read content, not the listing metadata.
- **Added the 3 missing registrants right away** rather than waiting for confirmation, because Max's standing instruction from yesterday was "yes, add missing ones" and he explicitly said "I need to update."
- **Inlined NULL for unknown location** on two inserts - the D1 params API rejected null values passed as bound parameters, so the SQL was rewritten to put NULL literally in the statement.
- **Created a findable "continue-here" doc + global2 trigger** so this work can never get lost again the way yesterday's faraday session vanished. The doc is `_tomemex`-tagged so it's also searchable in Memex.
- **Reused existing FishAudio TTS + Telegram tooling** rather than reinventing - extracted the pattern from `yt_transcript_app.py`, used the FishAudio key and clipfisher-monitor bot already on Pine.
- **Used Fish's built-in default male speaker** because the only stored voice IDs found were clones, and the read-aloud summaries normally use the default.

## CURRENT STATE - DONE
- All 14 form registrants are now in the D1 database `starseed-genetics-contacts`.
- Added the 3 that were missing: **Anya Krupski (id 36)**, **Jesse Sayranian (id 37)**, **Jose Garcia (id 38)**.
- Updated **Anthony George (id 34)** - he was added yesterday by direct email and also submitted the form today confirming a complete trio is available.
- Rendered a read-aloud MP3 summary (all 14 people one by one + overall picture) and sent it to Telegram via the clipfisher-monitor bot - delivery confirmed.
- Logged a worklog milestone and a session_status report.

## EXACT NEXT STEP
Answer Max's actual question: **Can Claude on the web (claude.ai) access the starseed D1 database, and what prompt to use?**

The honest answer to research/give: this current session reaches the DB through the **Cloudflare D1 MCP connector** (a tool integration available in *this* environment). Whether claude.ai web has that same access depends on whether Max has the Cloudflare D1 MCP / a connector configured on his web account. Web Claude does NOT automatically have access to his Cloudflare account just because this session does - it needs the same MCP/connector wired up there. If he has it, a prompt like "Look at the starseed-genetics-contacts D1 database and show me the contacts table" would work. Confirm with Max whether he has any MCP connectors set up on claude.ai before promising it'll work.

## OPEN QUESTIONS AWAITING MAX
1. The web-DB-access question above (current prompt).
2. **Stale duplicate sheet** - there's a second "(Responses)" sheet with the identical name, frozen at Feb 7, a branching trap in his Drive. Asked whether to confirm-and-delete it or leave it. No answer yet.
3. **Voice preference** - used Fish default male; offered to re-render with a specific preferred Fish male voice/clone if he names one. No answer yet.

## KEY PATHS / IDS
- **D1 database:** `starseed-genetics-contacts`, uuid begins `18b8acfd...` (accessed via D1 MCP).
- **Live responses sheet:** ID begins `10MIvyN...` ("XG1 simple 51102 (Responses)").
- **Stale duplicate sheet:** ID begins `1dLD20Ne...` (same name, frozen Feb 7 - do not use).
- **Continue-here doc:** `C:\claude_base\tools\xg1_starseed_forms\xg1_starseed_forms_method_v01_tomemex.md` (has sheet ID, DB ID, schema, diff recipe).
- **Narration text:** `C:\claude_base\tools\xg1_starseed_forms\summary_narration_20260612_v01.txt`
- **MP3:** `C:\claude_base\tools\xg1_starseed_forms\out\xg1_starseed_summary_20260612_v01.mp3` (~3.4 MB)
- **Render/send script:** `C:\claude_base\tools\xg1_starseed_forms\render_and_send.py`
- **global2.md trigger:** `C:\Users\maxre\Nextcloud\claude_md_synced\global2.md` - words "starseed forms" / "xg1 forms" now point to the continue-here doc.
- **FishAudio key:** `C:\Users\maxre\Nextcloud\zSyncMain\ssh\fishaudio_api_key_20260226.txt`
- **Telegram:** clipfisher-monitor bot, chat_id **1395850773** (Max's read-aloud channel).
- **Prior session's handover (the "faraday" one):** `C:\claude_base\session_status\20260611_etermined_faraday_261424_18ec880b.handover.m9.md`

## RESUME TRIGGERS
Saying **"starseed forms"** or **"xg1 forms"** loads the continue-here doc instantly (wired into global2).

## GOTCHAS / DEAD ENDS RULED OUT
- **Form submissions are NOT emailed** - they live only in the Drive responses sheet, never in Gmail. Don't waste time searching Gmail.
- **Drive listing modifiedTime is unreliable** (showed stale Feb 7). Read the actual file content to get current data.
- **D1 params API rejects null** - for unknown/empty fields, inline NULL into the SQL rather than binding it as a parameter.
- **Two identically-named "(Responses)" sheets exist** - always use the `10MIvyN...` one; `1dLD20Ne...` is the stale trap.
- The only Fish voice IDs found were clones, not a named stock male voice - default speaker was used.

## DOMAIN CONTEXT (for the narration / DB content)
The project hinges on the **trio test**: finding alleles in a child that are in neither parent = the "starseed" signal. The form's key question is whether a complete trio (child + both parents) is available. Of the 14 registrants, roughly 8 have a willing complete trio and can go to genotyping; **Lottie Bowater** and **Jordan Maxwell** are the most developed cases. Several (KarenMarie Gensheimer, Zuzanna Vee, Ann Carter) are blocked only because parents have passed away. The 10 already in the DB: Lottie, Suzanne Matteson, Jyoti Paramjyoti, Ann Carter, KarenMarie Gensheimer, Zuzanna Vee, Young Brinson, Doug Kohl, Jordan Maxwell, Stanislav Kernc.
