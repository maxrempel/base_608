#!/usr/bin/env python3
"""OMEGA v02 selector: positive-candidate quota audit only.

This script intentionally does not create a production manifest and does not
select shams. It parses only public GIAB/annotation sources and writes
coordinate-containing outputs to a private, non-Git directory supplied by the
caller.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
import sys
import bisect
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path


AUTOSOMES = {str(i) for i in range(1, 23)}
SIZE_BINS = [
    ("60-99", 60, 99),
    ("100-299", 100, 299),
    ("300-499", 300, 499),
    ("500-999", 500, 999),
    ("1000-4999", 1000, 4999),
    (">=5000", 5000, None),
]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_info(text: str) -> dict[str, str | bool]:
    out: dict[str, str | bool] = {}
    for item in text.split(";"):
        if not item:
            continue
        if "=" in item:
            key, value = item.split("=", 1)
            out[key] = value
        else:
            out[item] = True
    return out


def size_bin(length: int) -> str | None:
    for name, lo, hi in SIZE_BINS:
        if length >= lo and (hi is None or length <= hi):
            return name
    return None


def chrom_ucsc(chrom: str) -> str:
    return chrom if chrom.startswith("chr") else "chr" + chrom


def chrom_vcf(chrom: str) -> str:
    return chrom[3:] if chrom.startswith("chr") else chrom


@dataclass
class Candidate:
    chrom: str
    anchor_1b: int
    variant_id: str
    length: int
    size_bin: str
    inserted_sha256: str
    normalized_id: str
    source_rank_hash: str
    repeat_bp: int = 0
    umap_cov_bp: int = 0
    umap_one_bp: int = 0
    repeat_classes: set[str] = field(default_factory=set)
    repeat_families: set[str] = field(default_factory=set)
    excluded_by_prior: bool = False
    context: str = "unclassified"
    ineligible_reason: str = ""

    @property
    def win_start0(self) -> int:
        return self.anchor_1b - 151

    @property
    def win_end0(self) -> int:
        return self.anchor_1b + 150

    @property
    def extraction_start_1b(self) -> int:
        return self.anchor_1b - 1000

    @property
    def extraction_end_1b(self) -> int:
        return self.anchor_1b + 1000


def read_intervals(path: Path, chrom_col=0, start_col=1, end_col=2, skip_track=False):
    by_chrom: dict[str, list[tuple[int, int]]] = defaultdict(list)
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if not line.strip() or line.startswith("#"):
                continue
            if skip_track and line.startswith("track"):
                continue
            fields = line.rstrip("\n").split("\t")
            try:
                chrom = fields[chrom_col]
                start = int(fields[start_col])
                end = int(fields[end_col])
            except (IndexError, ValueError):
                continue
            by_chrom[chrom].append((start, end))
    for chrom in by_chrom:
        by_chrom[chrom].sort()
    return by_chrom


def interval_overlaps(intervals: list[tuple[int, int]], start: int, end: int) -> bool:
    # Small per-candidate check; interval lists are sorted.
    import bisect

    starts = [x[0] for x in intervals]
    idx = bisect.bisect_left(starts, end)
    for j in range(max(0, idx - 5), min(len(intervals), idx + 1)):
        a, b = intervals[j]
        if a < end and b > start:
            return True
    # Walk backwards if many intervals share nearby starts.
    j = idx - 6
    while j >= 0 and intervals[j][1] > start:
        a, b = intervals[j]
        if a < end and b > start:
            return True
        j -= 1
    return False


def point_in_intervals(intervals: list[tuple[int, int]], point0: int) -> bool:
    import bisect

    starts = [x[0] for x in intervals]
    idx = bisect.bisect_right(starts, point0) - 1
    return idx >= 0 and intervals[idx][0] <= point0 < intervals[idx][1]


def normalize_insertion(pos_1b: int, ref: str, alt: str):
    ref_work = ref.upper()
    alt_work = alt.upper()
    pos0 = pos_1b - 1
    while ref_work and alt_work and ref_work[-1] == alt_work[-1]:
        ref_work = ref_work[:-1]
        alt_work = alt_work[:-1]
    while ref_work and alt_work and ref_work[0] == alt_work[0]:
        ref_work = ref_work[1:]
        alt_work = alt_work[1:]
        pos0 += 1
    if ref_work == "" and alt_work:
        return pos0, alt_work
    return None, None


def load_chrom_sizes(path: Path) -> dict[str, int]:
    sizes = {}
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            fields = line.rstrip("\n").split("\t")
            if len(fields) >= 2:
                sizes[fields[0]] = int(fields[1])
    return sizes


def read_prior_giab32(vcf: Path) -> list[tuple[str, int, str]]:
    pools: dict[str, list[dict[str, object]]] = {name: [] for name, _, _ in [
        ("300-499", 300, 499),
        ("500-999", 500, 999),
        ("1000-4999", 1000, 4999),
        ("5000-plus", 5000, None),
    ]}
    with gzip.open(vcf, "rt", encoding="utf-8") as handle:
        for line in handle:
            if line.startswith("#"):
                continue
            fields = line.rstrip("\n").split("\t")
            chrom, pos_text, vid, ref, alt, _, filt, info_text, _, sample = fields[:10]
            info = parse_info(info_text)
            genotype = sample.split(":", 1)[0]
            if chrom not in AUTOSOMES:
                continue
            if filt != "PASS" or info.get("SVTYPE") != "INS" or genotype not in {"0/1", "1/1"}:
                continue
            try:
                length = abs(int(str(info["SVLEN"]).split(",", 1)[0]))
                illumina = int(info.get("Illcalls", 0))
            except Exception:
                continue
            band = None
            for name, lo, hi in [("300-499", 300, 499), ("500-999", 500, 999), ("1000-4999", 1000, 4999), ("5000-plus", 5000, None)]:
                if length >= lo and (hi is None or length <= hi):
                    band = name
                    break
            if band is None or illumina < 1:
                continue
            if alt.startswith("<") or "[" in alt or "]" in alt or "N" in alt.upper():
                continue
            if len(alt) - len(ref) != length:
                continue
            pos = int(pos_text)
            key = sha256_text(f"giab-hg002-v06|{chrom}|{pos}|{vid}|{length}")
            pools[band].append({"chrom": chrom, "pos": pos, "id": vid, "key": key})
    selected = []
    occupied: list[tuple[str, int]] = []
    for band in ["300-499", "500-999", "1000-4999", "5000-plus"]:
        count = 0
        for row in sorted(pools[band], key=lambda r: str(r["key"])):
            if any(row["chrom"] == c and abs(int(row["pos"]) - p) < 100000 for c, p in occupied):
                continue
            selected.append((str(row["chrom"]), int(row["pos"]), f"prior_giab32:{band}:{row['id']}"))
            occupied.append((str(row["chrom"]), int(row["pos"])))
            count += 1
            if count == 8:
                break
    return selected


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: audit_positive_quotas_v01.py SOURCE_DIR PRIVATE_OUT_DIR")
    source_dir = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)

    vcf = source_dir / "HG002_SVs_Tier1_v0.6.vcf.gz"
    bed = source_dir / "HG002_SVs_Tier1_v0.6.bed"
    chrom_info = source_dir / "chromInfo.hg19.ucsc.txt.gz"
    gap = source_dir / "gap.hg19.ucsc.txt.gz"
    rmsk = source_dir / "rmsk.hg19.ucsc.txt.gz"
    umap = source_dir / "k100.umap.hg19.multi_read.bedgraph.gz"

    source_manifest = []
    for path in [vcf, source_dir / "HG002_SVs_Tier1_v0.6.vcf.gz.tbi", bed, chrom_info, gap, rmsk, umap, source_dir / "README_SV_v0.6.txt"]:
        source_manifest.append({"name": path.name, "bytes": path.stat().st_size, "sha256": sha256_file(path)})

    hc = read_intervals(bed)
    gaps = read_intervals(gap, chrom_col=1, start_col=2, end_col=3)
    chrom_sizes = load_chrom_sizes(chrom_info)

    exposed: list[tuple[str, int, str]] = []
    exposed.extend(read_prior_giab32(vcf))
    coord_audit = Path(r"C:\claude_base\projects\XG1\kenefick\omega_detector\starseed_taygeta\retained_small\detector_real_read_coordinate_audit_v01\coordinate_mapping_v01.tsv")
    if coord_audit.exists():
        with coord_audit.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle, delimiter="\t"):
                for field_name in ("source_reported_boundary", "target_reported_boundary"):
                    try:
                        exposed.append((chrom_vcf(row["chrom"]), int(row[field_name]), f"real_read_coordinate_audit:{field_name}"))
                    except Exception:
                        pass
    recovered_private = out_dir.parent / "exposed_sources" / "prior_real_locus_panel_private_mapping_v01.tsv"
    if recovered_private.exists():
        with recovered_private.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle, delimiter="\t"):
                try:
                    exposed.append((chrom_vcf(row["chrom"]), int(row["signal_pos"]), "prior_three_real_three_sham_panel:signal_pos"))
                    exposed.append((chrom_vcf(row["chrom"]), int(row["sham_pos"]), "prior_three_real_three_sham_panel:sham_pos"))
                except Exception:
                    pass

    candidates: list[Candidate] = []
    reject_counts = defaultdict(int)
    with gzip.open(vcf, "rt", encoding="utf-8") as handle:
        for line in handle:
            if line.startswith("#"):
                continue
            fields = line.rstrip("\n").split("\t")
            if len(fields) < 10:
                reject_counts["malformed"] += 1
                continue
            chrom, pos_text, vid, ref, alt, _qual, filt, info_text, _fmt, sample = fields[:10]
            info = parse_info(info_text)
            if chrom not in AUTOSOMES:
                continue
            if filt != "PASS":
                reject_counts["not_pass"] += 1
                continue
            if info.get("SVTYPE") != "INS":
                continue
            if "," in alt:
                reject_counts["multiallelic"] += 1
                continue
            if alt.startswith("<") or "[" in alt or "]" in alt or "N" in alt.upper():
                reject_counts["symbolic_or_unresolved"] += 1
                continue
            if "IMPRECISE" in info or "CIPOS" in info or "CIEND" in info:
                reject_counts["imprecise_interval"] += 1
                continue
            pos_1b = int(pos_text)
            anchor_1b, inserted = normalize_insertion(pos_1b, ref, alt)
            if anchor_1b is None or inserted is None:
                reject_counts["not_pure_normalized_insertion"] += 1
                continue
            try:
                svlen = abs(int(str(info["SVLEN"]).split(",", 1)[0]))
            except Exception:
                reject_counts["missing_svlen"] += 1
                continue
            if svlen != len(inserted):
                reject_counts["svlen_mismatch"] += 1
                continue
            band = size_bin(len(inserted))
            if band is None:
                reject_counts["outside_size_bins"] += 1
                continue
            hc_intervals = hc.get(chrom, [])
            if not point_in_intervals(hc_intervals, anchor_1b - 1):
                reject_counts["outside_tier1_bed"] += 1
                continue
            ucsc = chrom_ucsc(chrom)
            chrom_len = chrom_sizes.get(ucsc)
            if chrom_len is None or anchor_1b - 1000 < 1 or anchor_1b + 1000 > chrom_len:
                reject_counts["chrom_edge"] += 1
                continue
            if interval_overlaps(gaps.get(ucsc, []), anchor_1b - 1001, anchor_1b + 1000):
                reject_counts["assembly_gap_2kb_window"] += 1
                continue
            norm_id = f"{chrom}:{anchor_1b}:{vid}:{len(inserted)}:{sha256_text(inserted)}"
            candidates.append(Candidate(
                chrom=chrom,
                anchor_1b=anchor_1b,
                variant_id=vid,
                length=len(inserted),
                size_bin=band,
                inserted_sha256=sha256_text(inserted),
                normalized_id=norm_id,
                source_rank_hash=sha256_text(f"OMEGA-v02|{norm_id}"),
            ))

    # Prior exposed ±10,000 filter.
    for cand in candidates:
        for e_chrom, e_pos, _why in exposed:
            if cand.chrom == e_chrom and abs(cand.anchor_1b - e_pos) <= 10000:
                cand.excluded_by_prior = True
                break

    # RepeatMasker annotation stream. UCSC rmsk columns: bin, swScore, ..., genoName, genoStart, genoEnd, ..., repName, repClass, repFamily
    by_chrom = defaultdict(list)
    for idx, cand in enumerate(candidates):
        by_chrom[chrom_ucsc(cand.chrom)].append((cand.win_start0, cand.win_end0, idx))
    for chrom in by_chrom:
        by_chrom[chrom].sort()
    window_starts = {chrom: [row[0] for row in rows] for chrom, rows in by_chrom.items()}

    def overlapping_candidate_indexes(chrom: str, start: int, end: int):
        rows = by_chrom.get(chrom)
        if not rows:
            return []
        starts = window_starts[chrom]
        limit = bisect.bisect_left(starts, end)
        hits = []
        j = limit - 1
        while j >= 0:
            wstart, wend, idx = rows[j]
            if wend <= start and wstart < start - 301:
                break
            if wstart < end and wend > start:
                hits.append((wstart, wend, idx))
            j -= 1
        return hits
    with gzip.open(rmsk, "rt", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            fields = line.rstrip("\n").split("\t")
            if len(fields) < 13:
                continue
            chrom = fields[5]
            if chrom not in by_chrom:
                continue
            try:
                start, end = int(fields[6]), int(fields[7])
            except ValueError:
                continue
            for wstart, wend, idx in overlapping_candidate_indexes(chrom, start, end):
                ov = max(0, min(end, wend) - max(start, wstart))
                if ov:
                    c = candidates[idx]
                    c.repeat_bp += ov
                    c.repeat_classes.add(fields[11])
                    c.repeat_families.add(fields[12])

    # Umap annotation stream.
    with gzip.open(umap, "rt", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if not line.strip() or line.startswith("track") or line.startswith("#"):
                continue
            fields = line.rstrip("\n").split("\t")
            if len(fields) < 4:
                continue
            chrom = fields[0]
            if chrom not in by_chrom:
                continue
            try:
                start, end = int(fields[1]), int(fields[2])
                score = float(fields[3])
            except ValueError:
                continue
            for wstart, wend, idx in overlapping_candidate_indexes(chrom, start, end):
                ov = max(0, min(end, wend) - max(start, wstart))
                if ov:
                    c = candidates[idx]
                    c.umap_cov_bp += ov
                    if score == 1.0:
                        c.umap_one_bp += ov

    quota_counts = defaultdict(int)
    eligible_rows = []
    for c in candidates:
        if c.excluded_by_prior:
            c.ineligible_reason = "prior_exposed_locus_10kb"
        elif c.umap_cov_bp < 271:
            c.ineligible_reason = "umap_coverage_below_90pct"
        elif c.repeat_bp >= 20:
            c.context = "repeat"
        elif c.repeat_bp == 0 and c.umap_cov_bp and c.umap_one_bp / c.umap_cov_bp >= 0.95:
            c.context = "high_mappability_non_repeat"
        elif c.repeat_bp < 20 and c.umap_cov_bp and c.umap_one_bp / c.umap_cov_bp <= 0.80:
            c.context = "low_mappability_non_repeat"
        else:
            c.ineligible_reason = "intermediate_context"
        if not c.ineligible_reason:
            quota_counts[(c.size_bin, c.context)] += 1
            eligible_rows.append(c)

    selected_by_cell = defaultdict(list)
    needs = {
        "high_mappability_non_repeat": 4,
        "repeat": 2,
        "low_mappability_non_repeat": 2,
    }
    for bin_name, _lo, _hi in SIZE_BINS:
        for ctx, need in needs.items():
            pool = [c for c in eligible_rows if c.size_bin == bin_name and c.context == ctx]
            pool.sort(key=lambda c: c.source_rank_hash)
            selected_by_cell[(bin_name, ctx)] = pool[:need]

    private_candidates = out_dir / "private_positive_candidates_v01.tsv"
    with private_candidates.open("w", newline="", encoding="utf-8") as handle:
        fields = [
            "chrom", "anchor_1b", "variant_id", "length", "size_bin", "context",
            "repeat_bp", "umap_cov_bp", "umap_one_bp", "excluded_by_prior",
            "ineligible_reason", "normalized_id", "rank_hash", "inserted_sha256",
            "repeat_classes", "repeat_families",
        ]
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for c in candidates:
            writer.writerow({
                "chrom": c.chrom,
                "anchor_1b": c.anchor_1b,
                "variant_id": c.variant_id,
                "length": c.length,
                "size_bin": c.size_bin,
                "context": c.context,
                "repeat_bp": c.repeat_bp,
                "umap_cov_bp": c.umap_cov_bp,
                "umap_one_bp": c.umap_one_bp,
                "excluded_by_prior": c.excluded_by_prior,
                "ineligible_reason": c.ineligible_reason,
                "normalized_id": c.normalized_id,
                "rank_hash": c.source_rank_hash,
                "inserted_sha256": c.inserted_sha256,
                "repeat_classes": ";".join(sorted(c.repeat_classes)),
                "repeat_families": ";".join(sorted(c.repeat_families)),
            })

    exposed_path = out_dir / "private_exposed_locus_anchors_v01.tsv"
    with exposed_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["chrom", "anchor_1b", "source"])
        for row in exposed:
            writer.writerow(row)

    source_manifest_path = out_dir / "source_manifest_private_v01.tsv"
    with source_manifest_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=["name", "bytes", "sha256"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(source_manifest)

    quota_rows = []
    blocked = []
    for bin_name, _lo, _hi in SIZE_BINS:
        for ctx, need in needs.items():
            count = quota_counts[(bin_name, ctx)]
            selected = len(selected_by_cell[(bin_name, ctx)])
            ok = count >= need
            quota_rows.append({
                "size_bin": bin_name,
                "context": ctx,
                "required": need,
                "eligible_denominator": count,
                "deterministically_selectable": selected,
                "status": "pass" if ok else "blocked_insufficient_positive_candidates",
            })
            if not ok:
                blocked.append(f"{bin_name}/{ctx}: {count} available, {need} required")
    quota_path = out_dir / "positive_quota_audit_private_v01.tsv"
    with quota_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=list(quota_rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(quota_rows)

    summary = {
        "schema": "omega_v02_positive_quota_audit_v01",
        "candidate_records_after_truth_filters": len(candidates),
        "eligible_positive_records_after_context_and_exclusions": len(eligible_rows),
        "quota_status": "pass" if not blocked else "blocked",
        "blocked_cells": blocked,
        "source_manifest_sha256": sha256_file(source_manifest_path),
        "private_candidates_sha256": sha256_file(private_candidates),
        "private_exposed_locus_anchors_sha256": sha256_file(exposed_path),
        "positive_quota_audit_sha256": sha256_file(quota_path),
        "reject_counts": dict(sorted(reject_counts.items())),
    }
    (out_dir / "positive_quota_audit_summary_private_v01.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
