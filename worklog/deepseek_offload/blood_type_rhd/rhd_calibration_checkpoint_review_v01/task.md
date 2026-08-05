You are a scientific methods reviewer. Draft a compact PRELIMINARY checkpoint structure for a bounded RHD short-read WGS calibration task. Do not infer any participant result or phenotype.

Facts already independently verified by Codex:
- Prior feasibility checkpoint commit cdf8b650 remains authoritative and preserved.
- 13 local public 1000 Genomes high-coverage GRCh38 CRAM+CRAI controls exist on Asto: HG00555, HG00639, HG00642, HG01505, HG01508, HG01511, HG01887, HG01888, HG01891, HG02492, HG02495, HG02602, HG02605. Their retained metadata provide sample/family/population/run accession, authoritative CRAM MD5, exact bytes, sequencing provenance, and accepted integrity. Local directories contain only CRAM and CRAI.
- Exact scoped repository and local metadata searches found no independently sourced sample-level serology or molecular RHD deletion/copy-number truth for any of the 13.
- Erythrogene/RBCeq/1000 Genomes structural calls are computational predictions from related sequence data and must not be used as independent calibration truth.
- RHtyper validation cohort has molecular/serologic truth, but its samples are not linked to these 13 approved local alignments.
- Therefore verified truth counts are RHD-positive 0 and RHD-negative/deletion 0. No one-pair pilot is permitted.
- Delly local binary is v1.2.6, 8,208,800 bytes, SHA256 f4663690302a5e6d0d4848039aa5a1db92de490b497cb3655f8e3692c3af67d4. Official source tag v1.2.6 resolves to commit e6246dbb18b7f6df2b7b381d542cdeaea6be8c82; codeload archive 3,815,981 bytes, SHA256 ae8e1fb6b61221da1d57017afc970de63490087c22197a2a8860b8761ee8763e. Existing frozen command form is `/home/rempel/genomics/popref/tools/delly call -g REF -o OUT.bcf INPUT.bam`.
- RHtyper official Git tag v0.2.0 resolves to commit b2c42c1614ddf30be07f426ee719cbdeba1bd1a1; source archive 38,441,323 bytes, SHA256 a7e7e5aa0e94ea7f1c90d1434d1b8177d9c0e3f7a14327d81e86dd58422eeeee. Its setup metadata says 0.2/Python <=3.7.12, but the tagged archive lacks the declared bin/RHtyper script. Official Anaconda ticchang/rhtyper latest is 1.1, linux-64 rhtyper-1.1-py37_0.tar.bz2, 174,431,712 bytes, official MD5 73ea6c02d508046542efefbd56690dc1. No local RHtyper runtime is installed; do not pretend otherwise. Planned CLI must be pinned only after installing and hashing the exact package in a versioned environment.
- A resource-limited whole-file SHA256 seal of the one previously unsealed related-participant BAM is running read-only at 16 MiB/s, nice 15, idle I/O, 256 MiB memory cap, atomic output, zero restarts, low I/O pressure. The result will be inserted only after completion.
- No participant RHD locus was queried. No phenotype or biological claim exists.

Required output:
1. A glance-first report outline with exact safe conclusion.
2. A fail-closed executable pilot-manifest schema. It must require at least one independently verified conventional RHD-positive and one independently verified homozygous whole-RHD deletion control, exact truth authority fields, build/alignment/tool checksums, bounded intervals, depth and breakpoint observables, attrition, and resource fields. It must refuse execution when the truth pair is absent.
3. The smallest lawful targeted acquisition specification, not a broad download plan: precisely the minimum public/approved inputs and truth documents needed to release the pilot, with a heterozygous deletion and hybrid/partial allele marked as strongly preferred additional controls.
4. A concise scientific critique covering false-positive and false-negative observables and why tool concordance from the same reads is not independent validation.

Do not draft participant calls, clinical claims, wet-lab recommendations, or acquisition commands. Keep it under 1,800 words.
