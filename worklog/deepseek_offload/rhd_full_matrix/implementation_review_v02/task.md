# Compact RHD full-matrix implementation audit

Last edited: 2026-08-03 by Codex (GPT-5.6 SOL)

Return at most 3,500 characters. Review this deterministic plan for critical errors only.

Frozen matrix: 3 RHD copy states x 3 coverages (15x/30x/45x) x 10 replicates, plus one seed/coverage/error-matched intact sham per truth = 180 coded datasets. Six valid 30x replicate-one pilot datasets must be checksum-reused, not regenerated. Same private master derives IDs and seeds. Caller manifests contain no truth/state/copy/haplotype/pair/seed fields. Truth stays escrowed until all 180 method markers and a coded manifest seal.

Proposed execution:
1. New full generator derives 180 escrow rows from the original pilot master, proves the six pilot rows match exactly, references the six pilot FASTQs by their verified hashes, and generates 174 new datasets atomically.
2. New mapper verifies the 180-row caller manifest, reuses six verified pilot BAM/BAI rows, maps 174 new datasets, and emits one truth-free 180-row mapped manifest.
3. Two truth-free caller shards process disjoint opaque IDs. Each dataset gets: frozen normalized depth; RHtyper evidence preflight then conditional RHtyper 1.1 or structured non-genotype state; Delly 1.2.6 breakpoint lane; complete raw hashes. Six pilot depth/Delly and canonical RHtyper outputs are reused by hash.
4. A seal verifies 180 unique completions, exact input/output hashes, disjoint shards, no truth fields, method attrition, and writes a coded method manifest.
5. Only then a scorer verifies escrow SHA, joins labels, and reports separate depth/RHtyper/Delly matrices, Wilson intervals, coverage strata, shams, depth ordering, and readiness gates. No tuning or participants.

State only:
- fatal design or privacy defects;
- reuse validations that are missing;
- atomic/resume hazards;
- scoring traps that could invalidate the frozen gates;
- the five most important pre-unblinding assertions.

Do not draft code or restate the plan.
