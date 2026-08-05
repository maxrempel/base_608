# Adviser note - milestone 3 (~264K tokens)
# session: 20260713_claude_base_92fbfc9d
# written: 2026-07-13 14:20:15 by deepseek-v4-pro

TO MAX: the analysis is done but the NPA scanner script that produced your 7-family results last January was never saved to disk. Assistant re-created it from the output format. It's probably right (the logic is simple) but nobody can prove it's the same. Also the outputs landed in a new 260713 folder rather than extending the existing 260124 one - so now you have two competing master summaries. Low urgency, but worth knowing when you review.

TO ASSISTANT: two problems you must not leave uncleaned. (1) The scanner is a re-implementation of a lost script - you must say this plainly in the report file and note that cross-family comparisons depend on the reimplementation being faithful. (2) You forked the analysis into a new directory (260713_NPA_Bowater_23andme_trio) with its own master summary instead of extending the canonical 260124_NPA_7fam_11children structure. That means the old 01_master_npa_summary.tsv is stale and there are now two "master" summaries. Pick one canonical location, update the original master summary there, and archive or delete the duplicate.
