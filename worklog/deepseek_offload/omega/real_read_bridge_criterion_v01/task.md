# Task

Design the smallest deterministic mapper-boundary repair test for one accepted
real-read OMEGA insertion control and one nearby sham.

Facts:

- The accepted control uses two separate retained real-read contigs on the
  minus strand.
- The accepted R-anchor terminal boundary equals the frozen locus coordinate.
- Retained source terminal payload proxies are 116 bp (R anchor) and 117 bp
  (L anchor).
- Bounded remapping extended alignment endpoints, yielding a +9 bp R-anchor
  boundary and a -3 bp L-anchor boundary.
- The bounded R proxy is exactly the first 107 bp of its 116 bp source proxy.
- The bounded L proxy is exactly the last 114 bp of its 117 bp source proxy.
- There is no internal-CIGAR insertion and no externally validated complete
  insertion payload.
- The nearby sham has no two-sided call.
- Frozen detector thresholds and scientific endpoint cannot change.

Propose:

1. An explicit full-payload bridge acceptance criterion that rejects trimmed
   proxies and cannot manufacture missing sequence.
2. Exact deterministic checks for source/target coordinate and sequence
   relationships.
3. The correct interpretation if the retained full proxies cannot be bridged
   unambiguously.

Return concise implementation logic and a coordinate-free result schema. Do
not propose synthetic reads, relaxed thresholds, a correction factor, or a
biological-rate interpretation.
