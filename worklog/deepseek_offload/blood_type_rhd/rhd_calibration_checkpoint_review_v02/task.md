Draft a maximum 850-word PRELIMINARY scientific checkpoint, no participant call or phenotype.

Verified facts: 13 local high-coverage GRCh38 1000 Genomes CRAM controls (HG00555, HG00639, HG00642, HG01505, HG01508, HG01511, HG01887, HG01888, HG01891, HG02492, HG02495, HG02602, HG02605) have exact sequence provenance and integrity but no independent serology or molecular RHD structural truth. Erythrogene, RBCeq, and 1000 Genomes SV calls are computational predictions from related sequence and are not truth. Verified conventional RHD-positive controls=0; verified homozygous-deletion controls=0. Therefore no pilot may run.

Delly: local v1.2.6 binary SHA256 f4663690302a5e6d0d4848039aa5a1db92de490b497cb3655f8e3692c3af67d4; official tag commit e6246dbb18b7f6df2b7b381d542cdeaea6be8c82; source archive SHA256 ae8e1fb6b61221da1d57017afc970de63490087c22197a2a8860b8761ee8763e; command form `delly call -g REF -o OUT.bcf INPUT.bam`.

RHtyper: source tag v0.2.0 commit b2c42c1614ddf30be07f426ee719cbdeba1bd1a1, archive SHA256 a7e7e5aa0e94ea7f1c90d1434d1b8177d9c0e3f7a14327d81e86dd58422eeeee. Tagged setup says 0.2/Python<=3.7.12 but archive lacks declared bin/RHtyper. Official Anaconda latest 1.1 package is 174431712 bytes with MD5 73ea6c02d508046542efefbd56690dc1. No local runtime is installed. Runtime and CLI remain sealed pending exact package installation and hash.

A read-only resource-capped checksum of the one previously unsealed related-participant BAM is running; insert result only after atomic completion. No participant RHD locus was queried.

Output only:
1) safe conclusion;
2) minimal fail-closed pilot-manifest fields requiring one independent positive and one independent homozygous-deletion truth control, exact truth authority, build/alignment/tool hashes, bounded intervals, depth/breakpoint/copy-number/tool-concordance observables, attrition, resource use; refuse absent truth pair;
3) smallest targeted acquisition specification: exactly two public/approved GRCh38 short-read WGS alignments plus independent truth documents; heterozygous deletion and hybrid/partial allele strongly preferred extras;
4) brief false-positive/false-negative critique and explain why same-read tool concordance is not independent validation.

No commands, wet lab, clinical claims, downloads, or participant inference.
