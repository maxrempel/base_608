# Adviser note - milestone 7 (~530K tokens)
# session: 20260710_jolly_austin_dd9aa0_aa619d47
# written: 2026-07-10 15:29:56 by deepseek-v4-pro

TO MAX: Nothing needs your decision right now-both background jobs (HPRC download, delly SVs) are running unattended. But you should know: this session is at ~530K tokens and climbing fast. The Assistant keeps burning context on repeated bug-fix cycles (same chr-prefix and CRLF bugs, 3+ rounds each) and long-form TLDR summaries after every turn. The background jobs won't finish in this window. Consider compacting and resuming when the data lands, rather than burning a third of the remaining window on idle polls.

TO ASSISTANT: Three concrete changes. (1) Stop the TLDR after every single turn-Max reads the output, you don't need to re-summarize what you just said. That's your biggest token burn. (2) The chr-prefix / CRLF / pysam-contig bugs have hit you 8+ times now. Before any new script that touches BAMs or VCFs, check contig naming FIRST as a one-liner diagnostic, don't discover it from a silent failure 3 rounds later. (3) Max has told you twice that "clean negative" conclusions anger him-he wants distributions and categories, not verdicts. When delly and HPRC land, present the numbers and let him interpret. No more "zero confirmed" wrap-ups.
