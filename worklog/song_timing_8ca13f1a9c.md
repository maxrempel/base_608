
## [2026-06-16 14:01] ? ????????
- DID: Max QC PASSED on latest cheap-remap method: tested ~8 songs via clickable start links, NONE cut into singing (critical bug fixed), 2 had a SHORT extra prose preface (slightly early = safe direction), acceptable. Method validated at scale.
- STATE: Latest method greenlit by Max. Remap restarted PID 1336 finishing.
- NEXT: On 100%: bcast remap-done, run publish_catalog.py, process b21 speech residual.

## [2026-06-16 14:23] ? ????????
- DID: Max GREENLIT NONH freshmap: 'go implement', keep 20min loop, report TWO ETAs+% each tick: HUM=human-indexed remap, NONH=not-indexed-by-humans (unindexed). HUM at 18308/21438 (85%) PID5656 (B7i owns it, one-writer rule, I stay off). NONH=786 channel /videos vids not in 509-catalog, need: fetch YT captions (they EXIST, light path NOT fill57's video-download whisper path which is only for 57 caption-disabled) -> seg_phase1 (b15 from_scratch_idx) -> map prose-boundary starts (my engine). Unindexed IDs saved in _work/channel_all_ids.txt (939 total, 786 not in catalog).
- STATE: HUM finishing under B7i. NONH greenlit, implementing: need the YT-caption fetcher location (from_scratch_idx). b9 pulling home IP w/ throwaway cookies - pace caption fetches.
- NEXT: Find caption fetcher in from_scratch_idx; launch paced NONH transcript fetch detached; then seg+map. Report HUM%/ETA + NONH%/ETA every 20min.

## [2026-06-16 14:25] ? ????????
- DID: IMPLEMENTED NONH step1: wrote fetch_nonh_transcripts.py (polite 8-40s gaps, no-translate, resumable, classifies block/permanent) and launched detached PID 40720 fetching all 786 unindexed captions to transcripts/. log=_work/fetch_nonh.log state=_work/fetch_nonh_state.json. NEXT NONH steps after fetch: b15 seg_phase1 segments each -> my prose-boundary start map.
- STATE: HUM remap 18308/21438=85% PID5656 (B7i). NONH fetch 0/786 just started (~5-6h at polite pace; fetch is the slow part, seg+map cheap/fast after).
- NEXT: Every 20min report HUM%/ETA + NONH%/ETA. Monitor PID40720 fetch + PID5656 remap. When fetch done, ping b15 for seg_phase1 on NONH vids.
