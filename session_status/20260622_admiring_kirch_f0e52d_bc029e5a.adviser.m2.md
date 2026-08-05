# Adviser note - milestone 2 (~165K tokens)
# session: 20260622_admiring_kirch_f0e52d_bc029e5a
# written: 2026-06-22 17:29:07 by deepseek-v4-pro

TO MAX: Assistant built the whole named-projects feature, merged, and imported your project - but had to use **v09** of your video because `starseeds_pitch_cleaned_v10.mp4` doesn't exist on disk. The Assistant flagged this in red and asked if v10 lives elsewhere. Decide whether v09 is fine or you need to swap. Everything else looks solid - server is running, project loads at the URL you were given.

TO ASSISTANT: The `shutil.cop2 = shutil.copy2  # noqa` line you originally wrote into `music_project_import.py` is a red flag - it suggests you generated code without thinking about what it does. You caught and removed it, but watch that. On a first-draft feature this size, the bigger risk is the untested `loadProject()` JS IIFE - you only verified the API JSON, not the full DOM/manual test. If Max reports the page is blank or the waveform doesn't appear, check that first. Otherwise, clean work - the persistent Nextcloud folder design and shared `render_music_overlay()` helper are good calls.
