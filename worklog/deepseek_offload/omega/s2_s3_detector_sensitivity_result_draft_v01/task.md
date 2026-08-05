# Draft a concise OMEGA detector sensitivity pilot result

Write a short, scientifically cautious result note from these deidentified deterministic facts:

- Samples: focal S2, focal S3, one cultured African control, one cultured European control.
- One outcome-blind, clean, reference-database-novel chromosome 22 site was selected solely by the frozen mask, depth/quality, and gnomAD-SV v4.1 plus HPRC v1.1 gates.
- D10 depth at the site was 51, 50, 49, and 40, respectively. Every bounded interval had 1,401 D10 callable bases.
- A deterministic 120-base synthetic non-reference payload was injected at 8, 12, and 20 breakpoint-support reads per side, with high mapping/base quality and matched real read groups. A sham interval was run for every sample.
- Frozen gates were unchanged: clip at least 30 bases, cluster window 20, at least 5 clip records, clean mask, at least 8 per side, canonical two-sided junction, rare threshold 0.001.
- Across all 12 spikes, extraction recovered the expected support; all 12 passed two-sided clustering and clean-mask gates; all 12 produced an assembled contig.
- Zero of 12 spikes passed the canonical two-sided junction gate. The assembled contig followed the reference haplotype and did not retain a qualifying two-sided foreign overhang.
- Recovery by tier was 0/4 at 8+8, 0/4 at 12+12, and 0/4 at 20+20.
- There were zero canonical two-sided false-positive loci across four shams and zero off-target canonical two-sided loci across the spike runs.
- The run used two threads, had no restart, and all result/checksum gates passed.

The conclusion must say this is direct evidence of a detector sensitivity failure mode at the assembly-to-canonical stage and means low S2/S3 Omun counts could be partly technical. It must not claim that all low counts are explained, must not apply a correction factor, and must not interpret the cultured comparison biologically. Limitations must include one locus, one payload length/topology, synthetic high-quality reads, correlated tiers, and the possibility that real insertions assemble differently. Recommend the smallest next falsification: repeat at several outcome-blind loci and payload lengths, including a validated real-read positive control, before burden interpretation.

Do not include coordinates, read identifiers, private participant information, or unsupported statistics.
