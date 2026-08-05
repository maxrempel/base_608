#!/usr/bin/env python3
import hashlib
import importlib.util
import json
from collections import Counter
from pathlib import Path

ANALYZER = Path(
    "/home/rempel/genomics/_analysis/aluya5_exact_copy_npa_v01/code/"
    "analyze_aluya5_exact_copy_npa_onepass_v02.py"
)
CRAM_ROOT = Path(
    "/home/rempel/genomics/_analysis/aluya5_exact_copy_npa_v01/temp/"
    "target_crams/PR04/chr11"
)
SAMPLES = {"father": "HG00640", "mother": "HG00641", "child": "HG00642"}
POSITION_0 = 125871105

spec = importlib.util.spec_from_file_location("analyzer", ANALYZER)
analyzer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analyzer)

result = {
    "status": "technical_screen_candidate_not_biological",
    "family": "PR04",
    "chromosome": "chr11",
    "position_1based": POSITION_0 + 1,
    "reference_base": "C",
    "child_candidate_base": "T",
    "tiers": {},
}
for tier, mapq, baseq in (("primary", 30, 25), ("strict", 60, 30)):
    result["tiers"][tier] = {"min_mapq": mapq, "min_baseq": baseq, "roles": {}}
    for role, sample in SAMPLES.items():
        cram = CRAM_ROOT / sample / f"{sample}.final.cram"
        with analyzer.pysam.AlignmentFile(
            str(cram), "rc",
            reference_filename="/home/rempel/genomics/controls/GRCh38DH.fa",
        ) as bam:
            evidence = analyzer.pileup_chromosome(
                bam, "chr11", {POSITION_0}, mapq, baseq
            )
        base_rows = evidence.get(POSITION_0, {})
        counts = Counter({base: len(rows) for base, rows in base_rows.items()})
        alt_rows = base_rows.get("T", [])
        result["tiers"][tier]["roles"][role] = {
            "depth": sum(counts.values()),
            "base_counts": {base: counts.get(base, 0) for base in "ACGT"},
            "candidate_reads": len(alt_rows),
            "candidate_forward": sum(row[3] == "forward" for row in alt_rows),
            "candidate_reverse": sum(row[3] == "reverse" for row in alt_rows),
            "candidate_read_hashes": sorted({
                hashlib.sha256(row[4].encode()).hexdigest()[:16]
                for row in alt_rows
            }),
            "candidate_mapq": sorted(row[0] for row in alt_rows),
            "candidate_baseq": sorted(row[1] for row in alt_rows),
            "candidate_edge_distance": sorted(row[2] for row in alt_rows),
        }

print(json.dumps(result, indent=2))
