# Adviser note - milestone 6 (~475K tokens)
# session: 20260710_jolly_austin_dd9aa0_aa619d47
# written: 2026-07-10 12:14:30 by deepseek-v4-pro

TO MAX: Two genuine decisions waiting for you, both cleanly scoped - (1) run SV calling on Oliver so deletion comparison is apples-to-apples? (2) confirm Centauri (teal 16TB drive) is the right download target for the HPRC pangenome (asto is 90% full). These are the only blockers; everything else the Assistant can continue autonomously.

TO ASSISTANT: You're at 475K tokens / 182 turns and just launched a background genome-wide scan. When that scan finishes and dumps its output, you will burn through your remaining ~365K tokens fast parsing results and re-running the same classify-phase-verify loops. Compaction is overdue - compact BEFORE ingesting the scan output. Also: your soft-clip extraction method for mother-vs-child comparison is correct but note that the mother's 30x coverage means small insertions near her detection floor will produce false "child-has, mother-lacks" hits at low read counts. Set a coverage-adjusted threshold in the genome-wide scan output.
