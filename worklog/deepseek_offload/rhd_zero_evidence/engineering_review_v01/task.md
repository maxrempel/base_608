# RHD RHtyper zero-evidence engineering review

Last edited: 2026-08-03 by Codex (GPT-5.6 SOL)

Review this bounded engineering design. Return concise implementation risks, boundary tests, and report wording. Do not invent data.

Context:
- Six frozen synthetic 30x RHD datasets were processed by RHtyper 1.1.
- Five succeeded. Their RHtyper RHD coding-position QC evidence covered all 1,254 coding positions, with total QC base counts 19,474 to 39,269.
- One biallelic whole-RHD-deletion synthetic dataset had zero QC evidence at all 1,254 RHtyper RHD coding positions and crashed when RHtyper calculated log(gene_avg/coverage, 2) with gene_avg=0.
- Independent normalized depth is the only primary three-state classifier. RHtyper is ancillary. Delly stays unchanged breakpoint evidence.

Proposed wrapper:
1. Use RHtyper 1.1's own pinned coordinate table and the same BAM pileup filters used by RHtyper variants.call: minimum mapping quality 10, reject 255, mean read quality at least 15, base quality at least 15, ignore deletions, and preserve its four misalignment exclusions.
2. Measure only RHD coding positions before launching RHtyper. Record total qualifying bases and number of coding positions with any qualifying base.
3. If total qualifying bases is exactly zero, do not launch RHtyper; emit structured ancillary state ZERO_RHD_EVIDENCE. This is not a deletion genotype.
4. If evidence is positive but not all 1,254 coding positions are covered, do not launch RHtyper; emit UNCALLABLE_ZERO_DEPTH. This conservative boundary prevents near-zero or one-read evidence from becoming a false zero-copy call. It is not a deletion genotype.
5. If all coding positions have evidence, run the unchanged pinned RHtyper command.
6. Replay the same six frozen BAMs into a new immutable output. Compare all five successful RHtyper scientific output files byte-for-byte with the prior version. Preserve original outputs.
7. Unit-test synthetic evidence summaries: zero, one qualifying base/read, sparse near-zero evidence, one missing position, and full-position coverage. None of the first four may emit a genotype.

Frozen constraints:
- Do not import the primary depth genotype.
- Do not use pseudocounts or tune genotype thresholds.
- Only the prior crash may become a structured state.
- No participant data or larger matrix.

Questions:
- Is the preflight scientifically faithful enough to call RHtyper's own zero-evidence state while remaining separate from normalized depth?
- What exact byte-diff scope should be required?
- What failure modes or tests are missing?
