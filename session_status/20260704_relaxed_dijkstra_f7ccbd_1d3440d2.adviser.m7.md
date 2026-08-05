# Adviser note - milestone 7 (~525K tokens)
# session: 20260704_relaxed_dijkstra_f7ccbd_1d3440d2
# written: 2026-07-04 14:14:48 by deepseek-v4-pro

TO MAX: The assistant spent most of this session (and a lot of tokens) fighting infrastructure - Sol corruption, asto contention, a dead-end EC2 attempt - rather than advancing the science. The "zero hits" result is scientifically useless without a **positive control**, which the assistant identified but hasn't built. Until you have a synthetic known insertion that the pipeline can detect, every run is just guessing whether the detector works. The soft-clip classification path the assistant proposed is the faster way to get the noise you expected; the contig assembly can wait until you have a working signal. Make the assistant build the positive control next, not yet another full-genome run.

TO ASSISTANT: You recognized the positive-control gap yourself - that's the critical next step, not more chromosome runs. Build a small synthetic BAM with a known insertion at a known locus, run the current pipeline against it, and confirm you get an omega hit. Until that works, you're blind. The soft-clip classification idea is also right: it's simpler and more sensitive; start there as the inventory-first detector and keep assembly as a validation stage. And stop churning on infrastructure loops - each one burns context and Max's patience.
