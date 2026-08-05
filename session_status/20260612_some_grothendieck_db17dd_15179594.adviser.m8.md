# Adviser note - milestone 8 (~121K tokens)
# session: 20260612_some_grothendieck_db17dd_15179594
# written: 2026-06-12 09:43:21 by claude-opus-4-8

TO ASSISTANT:
Max just corrected you twice. He says prior sessions on THIS machine already did Liz's applications and "had the system" - meaning the md instructions/pointers you proposed to write likely ALREADY EXIST. Do NOT add a new block to global2.md yet. First SEARCH the existing md files and md-index for the existing application instructions (grep for "lizmasters1", "transposon", "emm@", "Samuel", "Hannover", "applications"). Find what's already there before writing anything new - you risk creating a duplicate/competing instruction set, exactly the housekeeping mess to avoid.

Also note for the record: you wrote to the lizmasters1 D1 tracker with multiple UPDATE statements based on your own reading of emails/PDFs. That's live data on Max's behalf - fine, but you did several blind UPDATEs without first showing Max the diff. Lower risk now since done, but next time confirm before mutating a single-source-of-truth DB.

TO MAX:
Two things worth a glance. First, you set up the emm@ Gmail alias and the Assistant saved the emm@ password (TT2w3e4r5t6y=) into a plaintext creds file - that password is now in this transcript and on disk in clear text. If that mailbox matters, consider rotating it later. Second, the Assistant edited your live application tracker DB (K?ln=admitted, Hannover=end-of-June, etc.) - the changes look correct against the emails, but it was done without showing you the before/after, so spot-check the tracker matches what the web session expects.
