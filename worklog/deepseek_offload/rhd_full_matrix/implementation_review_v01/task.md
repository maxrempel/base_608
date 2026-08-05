# RHD full synthetic matrix implementation review

Last edited: 2026-08-03 by Codex (GPT-5.6 SOL)

Review and propose a compact deterministic implementation plan for expanding an already validated blinded RHD synthetic pilot to the frozen full matrix. Do not make scientific conclusions.

Frozen design:
- Three truth states: conventional two-copy RHD, heterozygous whole-RHD deletion, biallelic whole-RHD deletion.
- Coverage: 15x, 30x, 45x.
- Ten deterministic replicates per truth state and coverage.
- One matched intact sham for every truth dataset, sharing exact seed pair, coverage, read length, insert profile, and error profile. Total 180 datasets: 90 truths plus 90 shams.
- Existing valid pilot contains the six 30x replicate-one truth/sham datasets. Their opaque IDs and seeds must be reused exactly, and their completed FASTQ/BAM/caller evidence must not be regenerated.
- The same private 32-byte master derives IDs and seeds from `state|{coverage}x|rep{replicate:02d}` plus `|truth`, `|sham`, `|h1`, `|h2` using HMAC-SHA256.
- Caller-visible manifests must contain no truth, state, copy count, haplotype, pair label, or seed fields.
- Truth/seed escrow stays closed until all coded outputs and method manifests seal.

Methods and roles:
1. Normalized RHD:RHCE/flank depth is the only primary 3-state classifier and must use the frozen thresholds without tuning.
2. RHtyper 1.1 is conditional ancillary evidence. ZERO_RHD_EVIDENCE and UNCALLABLE_ZERO_DEPTH are structured non-genotype states. Callable outputs use the prospectively frozen canonical semantic contract; literal reproducibility remains FAILED_PERMANENTLY.
3. Delly 1.2.6 is breakpoint sensitivity only; zero records never imply deletion absence.
4. No composite unless separately named and scored.

Operational constraints:
- Asto only, bounded atomic datasets, at most two CPU cores and 6 GiB RAM per unit, no swap, nice 10.
- Preserve at least 23% free space. Existing six pilot datasets and outputs are immutable.
- Every dataset needs completion hashes and resumable state. Reuse must be checksum-verified, not assumed.
- Stop before truth opening; score only after every coded output and manifest seals.
- No participant input or phenotype.

Please return:
1. A recommended versioned storage/manifests layout.
2. Exact fail-closed validation rules for deriving 180 escrow rows and the 174 new coded datasets while reusing six.
3. A bounded execution sequence that minimizes duplicated work.
4. Critical implementation traps in generation, mapping, RHtyper canonical replay, Delly, depth, and scoring.
5. A short audit checklist for the pre-unblinding seal.

Keep the response under 8,000 characters.
