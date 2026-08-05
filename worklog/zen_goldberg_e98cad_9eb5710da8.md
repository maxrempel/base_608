
## [2026-06-09 12:52] ? 3e21795c
- DID: NEW BRANCH approach: isolate our real pod on black/transparent bg, feed to Wan i2v for MOVEMENT ONLY (Wan can't reinvent a near-empty frame, and we keep its non-linear motion), then luma/chroma-key the moving pod and OVERLAY on our own background plate (station/Titan/Earth). Sidesteps the redraw problem because Wan only sees a pod on black. Canonical pod still=plate 873 shuttle_v148a_bottom_bulge_a.png (pod over Earth, Anna+Driver in canopy).
- STATE: Starting: isolate pod (rembg on 873 or find existing pod-on-black still), composite on solid black, fire wan26 i2v silent with minimal motion prompt.
- NEXT: 1) get pod_on_black.png 2) fire wan26 i2v motion-only 3) bg-watch 4) ffmpeg colorkey/luma key + overlay on bg plate 5) present
- LESSON: Single-frame i2v of a SMALL pod in a full scene = engine redraws it into a NASA shuttle+chemtrail. Isolating the subject on black removes the reinvention surface.

## [2026-06-09 15:01] ? 3e21795c
- DID: Traced job 1210 full-res bg via D1 output_file = ships/space/titan_leave_v04_bg_right_station_a.png; thumbs_cache jpgs are tiny by design
- STATE: matte render running (bg bl5hvvgew): pod clip 2745 over that plate -> sc09_broll_podcomposite_v02_rembg.mp4
- NEXT: register done clip row, present /clipper link, then fix choppy flight

## [2026-06-10 14:08] ? 3e21795c
- DID: matte v02 solid (Max: terrific). job1210 bg verified 1536x1024 real. composite clip 2756 registered
- STATE: fixing jumpy Wan motion via frame interpolation; starting ffmpeg motion-compensated (minterpolate) on pod-black clip, RIFE if not smooth
- NEXT: interp pod-black->60fps, re-matte, re-composite, present

## [2026-06-10 17:18] ? 3e21795c
- DID: Confirmed Wan morphs rigid pod even small/on-black (EXP-A 2759 collapsed 2 people to 1). Input verified clean. EXP-B 2760 (pod on real cloud+station plate) done, Max reviewing
- STATE: Wan deemed unusable for rigid vehicle motion. Worker had died, restarted, processed 2759+2760 then exited
- NEXT: if EXP-B also morphs -> build no-Wan programmatic eased motion of exact cutout over plate (rigid, perfect faces)
