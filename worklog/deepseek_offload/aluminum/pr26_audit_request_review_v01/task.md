# PR26 technical-audit request review v01

Last edited: 2026-07-29 by Codex (GPT-5.6 SOL)

Review this deidentified, already-frozen bounded audit design. Do not invent
candidate identities, coordinates, thresholds, outcomes, or biological claims.

Context:

- An 11-family repeat-element atlas contains 10 primary strand-surviving
  technical candidates and one strict-tier survivor.
- One family, PR26, contains four of the 10 primary survivors.
- A separate outcome-blind enrichment analysis found no
  multiplicity-corrected signal.
- The PR26 audit freeze was written and checksum-sealed before private
  candidate details were opened.
- Cohorts are all four PR26 primary strand survivors, all PR26 primary loose
  non-survivors if any, and eight callable negatives per survivor.
- In the sealed atlas there are zero PR26 primary loose non-survivors under the
  frozen gate; this is recorded as an observed zero, not missingness.
- Negatives are four within the same repeat element and four in another
  same-chromosome element. Exact matching and a deterministic relaxation order
  are frozen for repeat strand, alignment identity and coverage bins,
  reference/consensus bases, depth, callability, and candidate exclusion.
- The audit measures mapping and base quality, read-edge distance, clipping,
  insert size, paired orientation, duplicates, alternative alignments, read
  group/lane/flowcell/library/platform, mate placement, source ambiguity,
  full-reference remap multiplicity, repeat-copy properties, depth ratios, and
  independent strict-tier presence.
- A shared technical mechanism is supported only if the same predefined
  feature deviates in the same direction for at least three of four survivors
  against both negative strata, with effect size and uncertainty.
- Production rerun is forbidden. Biological validation remains NO.
- The private request is immutable, checksum-pinned, and access-restricted.

Return a concise review with:

1. Any logical contradiction or missing technical control that would make the
   frozen question unanswerable.
2. Any implementation check Ben must perform without changing frozen cohorts,
   matching rules, or thresholds.
3. A minimal deidentified result schema that preserves exact attrition,
   uncertainty, and unavailable fields.
4. A clear PASS or FAIL for handing this request to production.

Prefer precise corrections over broad redesign. Do not recommend rerunning
whole-family or chromosome production.
