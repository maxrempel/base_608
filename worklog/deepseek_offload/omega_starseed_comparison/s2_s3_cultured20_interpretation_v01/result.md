### 1. What this says now (Max-friendly summary)

S3 carries exactly one Omun event, far below every cultured control (lowest control: 143). S1 also falls slightly below the control mean (58 vs 70), but 1 out of 20 controls has an even lower rate — so S1 is not unusual. The large gap between S3 and all controls cannot be taken at face value because the controls were cultured and S3 was not; culture conditions are known to affect callable genome composition and thus insertion detection.

### 2. Caution: observed contrast ≠ biological interpretation

The raw comparison shows S3’s Omun rate (0.38/Gb) is 99.5% lower than the control average. However, this contrast is exploratory and confounded by the culture-platform mismatch. Cultured samples may accumulate spurious insertion calls (e.g., from growth artifacts or altered chromatin) or, conversely, suppress certain insertions. Without culture-matched controls, the observed deficit cannot be attributed to S3’s biology, Starseed status, or any true absence of novel insertions. This is a technical observation, not a biological conclusion.

### 3. Sensitivity and next-analysis bullets

- **Culture-matched controls:** Obtain or generate a control panel cultured under the same conditions as S3 (or confirm that S3’s culture history is identical to controls) to eliminate the primary confound. Re-compute Omun ranges and rates with matched controls.
- **S2 value recovery:** Recover the deidentified Omun endpoint from the external OMEGA owner or via an allowed SSH key/sandbox. Do not assume S2 is zero; treat as missing until verified.
- **Topology by explicitly named larger categories:** For any spread or clustering analysis involving S3, use a preserved category – “all retained deduplicated loci” or “clean loci” – not Omun alone. S3’s single Omun cannot support a topology claim; any pattern must be demonstrated in the larger category and then separately reported.
- **Read/audit attrition kept separate from burden:** Report read depth, deduplication loss, and callable fraction as independent metrics. Do not mix attrition with Omun count or rate when interpreting burden differences between S3 and controls.
