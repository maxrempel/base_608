
## [2026-06-18 14:11] ? ????????
- DID: Wired gate to consume real LLM-verified first-lines: auto-scans timecoder_handover/verified_first_lines_*.json, keys by vid|SECONDS (HMS->sec), value {first_line,performer}, folds verified performer. Fixed INTRO-ONLY hyphen-normalization bug. Proven on B26's pX_1m8DlMbA file.
- STATE: pX routes 18 sung + 29 INTRO-ONLY = exact match to B26 gold standard. Split totals PUBLISH 7810/HELD 71/INTRO-ONLY 29. Consumer ready to auto-ingest every per-video verified file b27/B26 drops. No deploy.
- NEXT: As b27/B26 produce more verified_first_lines_<vid>.json, gate auto-consumes; freeze worklist when b7 set hits 81, await Max deploy-scope okay.
- LESSON: Verified-lines contract: file timecoder_handover/verified_first_lines_<vid>.json, key 'vid|START_SECONDS', value {first_line:'INTRO-ONLY'|faithful heard line, performer}. Gate converts draft HMS to sec to match.
