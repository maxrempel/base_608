# Task: review sensitivity-limited Omun synthesis

Privacy: private-authorized. Deidentified aggregate scientific report only. No coordinates, read IDs,
alignments, credentials, or private participant facts are included.

Review the following draft for scientific clarity and claim safety. Check whether it:

1. Preserves the observed S2/S3-versus-cultured-control detector-endpoint contrast.
2. Keeps culture/platform confounding prominent.
3. Separates accepted detector endpoints from exact biological insertion calls.
4. Explains locus-window or terminal evidence versus exact-junction/full-payload recovery.
5. Avoids any biological depletion, enrichment, absence, or sensitivity-corrected claim.
6. Gives useful "supported / unsupported / blocked" decision language.

Return only a concise review with any essential wording fixes. Do not invent new numbers.

Draft:

S2 has 3 accepted Omun detector endpoints, 2,664,221,029 callable D10 bases, and a raw detector rate
of 1.12603/Gb. S3 has 1 accepted Omun detector endpoint, 2,664,016,901 callable D10 bases, and a raw
detector rate of 0.3754/Gb. The 20 cultured controls span 143 to 224 endpoints and 53.6989 to
84.0128/Gb, with mean 187.55 endpoints and 70.322/Gb. S2 and S3 are therefore very low relative to
the cultured controls as accepted detector endpoints only.

The draft conclusion says this is a real pipeline observation but not a biological depletion claim.
The controls are cultured public-database samples; S2 and S3 are uncultured or not culture-matched to
the controls. OMEGA sensitivity for exact insertion calls is not established. Known-length
reconstruction failed with 0/32 exact lengths correct, 30 unresolved, and 2 false exact calls. A
new real-read full-payload bridge test had one two-sided parser hit in the accepted real-read control
but zero exact-coordinate hits, zero of two full terminal proxy matches, no checksum-accepted
spanning contig, and no internal-CIGAR insertion. The nearby sham had zero two-sided calls and passed
as a negative control. Therefore the method can report detector endpoints, but exact-junction,
full-payload, and biological event-count interpretation remain blocked.

The draft states there is no justified correction factor, no biological lower or upper bound, and no
S2/S3 Omun topology claim because S2 has only 3 Omun endpoints and S3 only 1.
