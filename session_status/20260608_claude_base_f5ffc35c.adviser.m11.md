# Adviser note - milestone 11 (~165K tokens)
# session: 20260608_claude_base_f5ffc35c
# written: 2026-06-08 11:10:18 by claude-opus-4-8

TO MAX:
Your gut on the "system setup is a bit nuts" was right - there really was a multi-copy worker.js mess, and the Assistant had been editing a backup copy the whole time, which is why Papers kept vanishing. It's now fixed onto one master and live. But know this: the metadata, journal pages, and especially the publisher LINKS were pulled from Crossref/Scholar by an AI and not shown to you for sign-off. Worth a 5-minute eyeball of maxrempel.com/papers to confirm each link lands on the right paper - one wrong DOI on a public academic page is embarrassing.

TO ASSISTANT:
You recovered well, but two loose ends:
1. The R2 bucket got silently emptied (recreated at 16:33 by another session) and you re-uploaded - confirm those 13 PDFs are now stable and not at risk of another wipe given the worker is "being redesigned." A redesign mid-flight is exactly when bindings get dropped again.
2. The upload script and token still live under the OLD path backups\cf_workers\maxrempel-site\_papers_upload while the canonical site moved to sites\maxrempel-site. You're straddling two trees. Consolidate scratch/uploader under the canonical path or you'll re-introduce the branching trap you just escaped.
Otherwise solid: data-in-D1 edits, no needless redeploys, links verified live.
