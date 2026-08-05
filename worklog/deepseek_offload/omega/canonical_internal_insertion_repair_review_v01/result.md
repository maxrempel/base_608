**Smallest valid test:** Yes. The proposal minimally isolates the missing internal‑insertion detection by adding one spike and one sham, using only a versioned parser and `-c` flag. No thresholds, correction factors, or redesign steps are introduced.

**Coordinate/strand/CIGAR pitfalls:**

- **CIGAR extraction:** The parser must read the `cg:Z` tag (PAF optional field). Verify the tag exists; if absent, fail closed.
- **Strand handling:** When alignment strand is `-`, the CIGAR is still processed left‑to‑right in query order, but the reference position of the insertion is computed from `ref_start + sum_of_leading_M/D/N_lengths`. This works because the reference coordinate increases monotonically. No strand‑specific inversion is needed.
- **Query‑base counting:** Count only query‑consuming operations that represent aligned bases: `M`, `=`, `X` (not `S`, `H`, `P`, `I`, `D`, `N`). The left‑side count must be ≥100 before the `I` block, and the right‑side count ≥100 after it. The `I` length itself (query‑only) must be ≥30.
- **Multiple insertions:** The parser should emit one entry per qualifying `I` operation, each at the reference position immediately preceding that `I`. The test expects exactly one for the spike; reject zero or >1.
- **End‑soft‑clip confusion:** The 10‑bp left and 2‑bp right soft clips (likely `S` operations) will not meet the “≥100 aligned bases on both sides” criterion, so they are safely ignored.

**Fail‑closed acceptance checks (all must pass):**
1. The canonical mapper output for the spike contig contains a `cg:Z` tag with a CIGAR string that has at least one `I` operation.
2. For the spike contig, exactly one insertion record is emitted.
3. The reported insertion sequence (the `I` block’s query bases) exactly equals the known 120‑bp synthetic payload.
4. The reported insertion reference position matches the expected locus (derivable from the spike design).
5. For the sham contig, zero insertion records are emitted.
6. All hashes of intermediate and final outputs match the expected precomputed values.
7. The original failed‑pilot dataset is unchanged (provenance preserved; verify by hash or file timestamp).

If any check fails, the test must be reported as failed with a clear diagnostic pointing to the violated condition. No fallback to terminal‑overhang logic is allowed.
