Review the ALU-DeNovo-1 exact-copy AluYa5 trio workflow and identify elegant, scientifically lossless speedups that may have been missed.

Known state:
- Ten complete trios, 22 autosomes each.
- Current measured compute time is about 7 hours 56 minutes per trio on Asto, running one chromosome job at a time with 2 CPU cores and a 6 GiB cap.
- The method evaluates exact reference-anchored AluYa5 copies locus by locus, looking for a child-supported allele absent from both parents.
- Fourteen loose child-only signals, one map-quality-60 survivor, zero biologically validated de novo calls.
- Filters and validation quality must not be weakened.
- The same three large CRAM files may currently be opened/read separately for each chromosome; results are checkpointed by chromosome.
- Asto is a guest machine, so solutions should remain modest and preserve at least 23% disk free space.

Question:
Max suspects the prior estimate missed a major speedup. Analyze the likely computational structure, separating CPU, CRAM decompression/random access, process startup, repeated annotation parsing, per-locus samtools calls, and scheduling gaps. Look especially for algorithmic restructuring rather than merely adding cores:
1. Can all AluYa5 loci for a trio be processed in one genome-wide pass per person instead of 22 chromosome jobs or thousands of locus queries?
2. Can reads/pileups be extracted once, then child-parent comparison happen in compact local tables?
3. Can multi-region samtools, interval batching, or a single mpileup/call stream eliminate repeated CRAM seeks and reference decompression?
4. Can invariant loci be rejected cheaply before expensive allele analysis?
5. Can trio members be streamed concurrently without increasing scientific false negatives?
6. What benchmark would prove the gain without changing outputs?

Return:
- The most likely missed bottleneck and the best redesign.
- Expected speedup range, stated cautiously.
- A lossless benchmark plan comparing old and new outputs on one completed chromosome and then one full trio.
- Time estimates for 50, 100, and 300 total trios if the redesign works.
- Important risks that could silently change calls.

Do not propose lowering mapping quality, downsampling, skipping loci, or replacing real-read validation. Keep the answer technical but concise.
