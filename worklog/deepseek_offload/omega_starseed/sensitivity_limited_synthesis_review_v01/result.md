**Review**

The draft meets all six criteria:

1. **Contrast preserved**: S2 (3 endpoints, 1.126/Gb) and S3 (1 endpoint, 0.375/Gb) are explicitly compared against cultured controls (143–224 endpoints, 53.7–84.0/Gb, mean 187.5 endpoints and 70.3/Gb). The low count is stated as a “real pipeline observation.”

2. **Culture/platform confounding prominent**: Controls are identified as “cultured public-database samples” while S2/S3 are “uncultured or not culture-matched,” directly flagging the confound.

3. **Detector endpoints vs. biological insertion calls separated**: The text distinguishes “accepted detector endpoints” from “exact-junction, full-payload, and biological event-count interpretation,” which are explicitly “blocked.”

4. **Locus/terminal vs. exact-junction/full-payload evidence explained**: Known-length reconstruction (0/32 exact), full-payload bridge test (zero exact-coordinate hits, zero terminal proxy matches, no spanning contig, no internal CIGAR), and sham negative control are described. The distinction between detector endpoints (supported) and more detailed recovery (blocked) is clear.

5. **No depletion/absence/sensitivity-corrected claim**: The draft states “no justified correction factor, no biological lower or upper bound, and no S2/S3 Omun topology claim” and explicitly says it is “not a biological depletion claim.”

6. **Decision language**: “Supported” (detector endpoints), “blocked” (exact-junction, full-payload, biological event-count interpretation). The example “S2 has only 3 Omun endpoints and S3 only 1” reinforces the limitation.

**Essential wording fix** (minor clarity): In the first paragraph, change “as accepted detector endpoints only” to “considering only accepted detector endpoints.” Suggested edit:

> S2 and S3 are therefore very low relative to the cultured controls **considering only accepted detector endpoints**.

Otherwise, the draft is correct and safe. No new numbers invented.
