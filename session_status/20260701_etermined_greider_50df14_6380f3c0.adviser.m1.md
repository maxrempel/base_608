# Adviser note - milestone 1 (~142K tokens)
# session: 20260701_etermined_greider_50df14_6380f3c0
# written: 2026-07-01 12:19:43 by deepseek-v4-pro

TO MAX: The Assistant keeps rewriting prompts from scratch instead of making surgical changes. s3087 (v35) was good - only the background was wrong. But the Assistant threw out that proven prompt and wrote increasingly rigid new ones for v36/v37, adding things like "EXACTLY from ref 2" and "12/3/6/9 o'clock" that made the images worse (characters staring at camera, variable chairs). This is a classic death spiral. Also, you said "p1189 is correct" then immediately said "p1184" -- the Assistant is confused which plate you want as the interior. Clarify that.

TO ASSISTANT: Stop rewriting prompts. Take s3087's EXACT prompt text and ref list (the 12 refs that produced a good image), change ONE thing -- the interior ref -- and fire. Do not add "EXACTLY," "12 o'clock," "NO BOOTS," or any new constraints. Every word you add to fix one thing breaks three others. You are over-specifying and the model is over-fitting. Also, clean up the _d57_fire*.py temp files you keep leaving. Ask Max to clarify p1184 vs p1189 -- you got contradictory numbers in the same message.
