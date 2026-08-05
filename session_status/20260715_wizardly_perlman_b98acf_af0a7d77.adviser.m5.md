# Adviser note - milestone 5 (~383K tokens)
# session: 20260715_wizardly_perlman_b98acf_af0a7d77
# written: 2026-07-15 09:00:22 by deepseek-v4-pro

TO MAX: The session burned itself on the wrong dataset before anyone caught it. Assistant spent heavy tokens logging into dbGaP, downloading keys, and running a Lak pilot before discovering ASC is exome-only - which you can't use for whole-genome omega. Your frustration was justified. The current diagnosis (SSC via SFARI, DRRF flagged for-profit, needs EIN) is correct and the plan is solid. You just need to confirm DRRF's non-profit status and EIN to unblock.

TO ASSISTANT: When Max talked about replicating 1000 Genomes results, that meant running the same NPA analysis on autism trios - not mapping the 1000G data itself. The entire conversation context was autism data access. You should have asked "exome vs whole-genome - which does your analysis need?" before doing any dbGaP download work. That single question would have saved ~200K tokens of now-irrelevant pilot effort. You recovered well once corrected, and the SFARI diagnosis is thorough. But front-load the requirement check next time.
