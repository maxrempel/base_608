## Implementation Guidance

### One-pass Re-architecture
- **Pooled pileup**: For each trio member, call `pysam.pileup()` once on the full chromosome (no region restriction) using the **lower** (primary) mapping/base quality thresholds to decide read inclusion.  This replaces per-element pile
