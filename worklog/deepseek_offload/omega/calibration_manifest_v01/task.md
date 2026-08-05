# OMEGA calibration manifest drafting task

Last edited: 2026-08-02 by Codex (GPT-5.6 SOL)

Draft a compact, fail-closed execution-manifest design and blocker summary for an OMEGA detector calibration. Do not invent data, tolerances, controls, or outcomes. Do not propose running a pilot unless every required cell is already satisfied.

Frozen gates:
- Blinded real positives plus matched shams.
- Minimum size coverage: short, medium, long.
- Minimum context coverage: unique plus repeat or low-mappability.
- Independently denominator-report: truth admitted, parser candidate formed, Omun accepted, exact left junction, exact right junction, payload or length reconstructed, and sham accepted. Every loss gets a reason and denominator.
- Biological-burden readiness requires at least 80% locus recovery overall, no tested size/context stratum with zero recovery, zero accepted matched shams, and stable recovery under mapper-boundary representation testing.
- Exact-junction claim requires at least 80% within a scientist-prespecified coordinate tolerance. The retained sources contain no explicit exact-junction coordinate tolerance. Treat that as a blocker.
- Length claim requires a known-length panel with at least 90% correct within a prespecified tolerance and zero false-exact calls. The retained sources define exact equality but no alternate length-error tolerance. Treat any broader tolerance as absent.
- Any code repair creates a new detector version and requires replay of the identical frozen blinded panel.

Verified inventory:
1. GIAB HG002 v0.6 Tier1 GRCh37 panel: 32 sequence-resolved real positives, eight in each of 300-499, 500-999, 1000-4999, and >=5000 bp; public HiSeq X PCR-free 30x reads. The panel was blinded originally but is now unblinded and may be training only. It has no 60-99 or 100-299 positives, no retained frozen unique/repeat/mappability stratification, and no matched shams. Prior result: all 32 read extractions usable; 0/32 correct exact lengths, 30 unresolved, 2 false exact.
2. Accepted cultured-control panel: 3 real loci plus 3 matched nearby shams, already unblinded and reused in multiple diagnostics. Result: 1/3 locus-window and junction-class recovery, 0/3 exact coordinate plus complete payload, 0/3 shams. Retained assemblies are terminal half-contigs, not known full-spanning truth. A prior stop decision forbids further tuning on this panel.
3. Synthetic tests: a 100-bp software unit test passed; a 5000-bp synthetic test was unresolved. These are not real positive controls and do not satisfy the real-positive requirement.
4. No lawful independent blinded panel meeting all size, context, truth, and sham cells is present in retained sources.

Return:
1. A concise TSV column schema and recommended row-level status categories for a versioned execution manifest.
2. A compact blocker table with evidence, owner, exit test, and active bypass.
3. A smallest-valid future pilot description without selecting or inventing loci.
4. A clear decision: pilot blocked versus runnable.

Keep the answer under 1,200 words and do not include coordinates, participant identities, reads, sequences, or credentials.
