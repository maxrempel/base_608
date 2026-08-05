Last edited: 2026-07-29 by Codex (GPT-5.6 SOL)

Design one defensible, result-producing extension of a blood-group genotype
project. Return a compact technical recommendation, not a report draft.

Known local data:
- 28 consumer genotype exports, 25 unique people, seven families.
- Five documented self-reported Starseed participants are focal.
- Platforms are 23andMe and MyHeritage. One trio has both platforms.
- Current ABO four-tag calls resolve 4/5 focal people: A, unresolved, A, O, A.
- RhD tag rs590787 exists for only 2/5. It must no longer be translated into
  Rh-positive or Rh-negative because RHD deletion/CNV is not directly observed.
- Full per-file marker inventory exists for ABO/RHD markers.
- Existing 155 parent-child marker transmissions and 13-marker duplicate
  checks are consistent.
- No clinical blood types are available.
- Public 1000 Genomes genotypes may be downloaded locally if useful.
- Taygeta is prohibited; local Pine or Asto only.

Manager directive:
1. Create a per-sample ABO/RHD callability matrix first.
2. Infer only alleles supported by observed markers, with ambiguous/no-call.
3. Separate predicted genotype from phenotype.
4. Use the largest defensible ancestry/platform-matched genotype control set.
5. If coverage supports it, estimate ABO and RhD-negative frequencies with
   exact small-sample uncertainty and matched-control comparison.
6. If RHD deletion/CNV is not observable, do not infer Rh-negative from tags.

Questions:
- What is the largest scientifically defensible control set we can construct
  now, and what makes it defensible?
- Is 1000 Genomes acceptable if restricted to the exact observed marker set,
  and how should ancestry matching be handled without inventing participant
  ancestry?
- What exact statistical endpoint is valid with 5 focal participants, one
  related pair among four known genomes in the wider project, and incomplete
  ABO calls?
- What must be labeled sensitivity analysis rather than matched control?
- Recommend a fail-closed implementation and acceptance checks.

Do not infer identities, ancestry, phenotype, or RhD status from missing data.
