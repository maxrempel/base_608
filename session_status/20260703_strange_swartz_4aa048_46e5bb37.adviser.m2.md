# Adviser note - milestone 2 (~158K tokens)
# session: 20260703_strange_swartz_4aa048_46e5bb37
# written: 2026-07-03 16:14:15 by deepseek-v4-pro

TO ASSISTANT: Stop building until Max answers the 4 gating questions. Your aggregator assumes a CSV format X12B hasn't committed to - if the real data comes as VCF or BED with different fields, you'll rewrite the parser. The synthetic test validated your math, not your interface. Also: stop committing to master when other sessions have live churn in that checkout. Create a feature branch (e.g., `x11b-paper-repro`) and work there. The stash-pop-rebase dance you did masks the real problem - concurrent sessions trampling each other's working trees.

TO MAX: Assistant built and pushed working code, but on master with other sessions' unstaged changes sitting in the same checkout. If those other sessions commit, you'll get merge collisions or lost work. Tell the team to work on named branches, not master. Also: the 4 questions Assistant keeps asking (which paper, chr3 coords, subs vs insertions, detection method) still aren't answered - that pipeline is a shell until you provide them.
