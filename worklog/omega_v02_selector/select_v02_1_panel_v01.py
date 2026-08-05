#!/usr/bin/env python3
"""OMEGA v02.1 blinded panel selector.

Private selector only. Writes truth/coordinate-bearing artifacts outside Git.
Production-facing manifest is produced but remains private/pending manager
release.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
import math
import sys
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

import numpy as np


SIZE_BINS = ["60-99", "100-299", "300-499", "500-999", "1000-4999", ">=5000"]
CONTEXTS = ["high_mappability_non_repeat", "repeat", "low_mappability_non_repeat"]
AUTOSOMES = {str(i) for i in range(1, 23)}
API_BASE = "https://api.genome.ucsc.edu/getData/sequence"


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_info(text: str) -> dict[str, str | bool]:
    out = {}
    for item in text.split(";"):
        if not item:
            continue
        if "=" in item:
            k, v = item.split("=", 1)
            out[k] = v
        else:
            out[item] = True
    return out


def chrom_ucsc(chrom: str) -> str:
    return chrom if chrom.startswith("chr") else "chr" + chrom


def chrom_plain(chrom: str) -> str:
    return chrom[3:] if chrom.startswith("chr") else chrom


def normalize_insertion(pos_1b: int, ref: str, alt: str):
    ref_w = ref.upper()
    alt_w = alt.upper()
    pos0 = pos_1b - 1
    while ref_w and alt_w and ref_w[-1] == alt_w[-1]:
        ref_w = ref_w[:-1]
        alt_w = alt_w[:-1]
    while ref_w and alt_w and ref_w[0] == alt_w[0]:
        ref_w = ref_w[1:]
        alt_w = alt_w[1:]
        pos0 += 1
    if not ref_w and alt_w:
        return pos0, alt_w
    return None, None


def read_intervals(path: Path, gzip_file: bool | None = None, chrom_col=0, start_col=1, end_col=2):
    by = defaultdict(list)
    opener = gzip.open if (gzip_file if gzip_file is not None else path.suffix == ".gz") else open
    with opener(path, "rt", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if not line.strip() or line.startswith("#") or line.startswith("track"):
                continue
            f = line.rstrip("\n").split("\t")
            try:
                by[f[chrom_col]].append((int(f[start_col]), int(f[end_col])))
            except Exception:
                continue
    for chrom in by:
        by[chrom].sort()
    return dict(by)


def read_chrom_sizes(path: Path):
    sizes = {}
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            f = line.rstrip("\n").split("\t")
            if len(f) >= 2:
                sizes[f[0]] = int(f[1])
    return sizes


def merge_intervals(intervals, pad=0):
    if not intervals:
        return []
    arr = sorted((max(0, a - pad), b + pad) for a, b in intervals)
    out = [list(arr[0])]
    for a, b in arr[1:]:
        if a <= out[-1][1]:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return [tuple(x) for x in out]


def mark_interval(mask: bytearray, base0: int, start0: int, end0: int, value: int = 1):
    a = max(0, start0 - base0)
    b = min(len(mask), end0 - base0)
    if a < b:
        mask[a:b] = bytes([value]) * (b - a)


def prefix_from_mask(mask: bytearray):
    pref = [0] * (len(mask) + 1)
    total = 0
    for i, val in enumerate(mask):
        total += 1 if val else 0
        pref[i + 1] = total
    return pref


def np_prefix(mask):
    arr = np.frombuffer(mask, dtype=np.uint8).astype(np.int32)
    return np.concatenate(([0], np.cumsum(arr, dtype=np.int64)))


def np_pref_sum(pref, starts, ends):
    starts = np.clip(starts, 0, len(pref) - 1)
    ends = np.clip(ends, 0, len(pref) - 1)
    return pref[ends] - pref[starts]


def pref_sum(pref, a, b):
    a = max(0, a)
    b = min(len(pref) - 1, b)
    if a >= b:
        return 0
    return pref[b] - pref[a]


def fetch_sequence(cache_dir: Path, chrom: str, start0: int, end0: int):
    cache_dir.mkdir(parents=True, exist_ok=True)
    name = f"{chrom}_{start0}_{end0}.json"
    path = cache_dir / name
    if not path.exists():
        params = urllib.parse.urlencode({"genome": "hg19", "chrom": chrom, "start": start0, "end": end0})
        with urllib.request.urlopen(API_BASE + "?" + params, timeout=60) as response:
            data = response.read()
        path.write_bytes(data)
        time.sleep(0.05)
    obj = json.loads(path.read_text(encoding="utf-8"))
    seq = obj["dna"].upper()
    if len(seq) != end0 - start0:
        raise RuntimeError(f"sequence length mismatch: {path} {len(seq)} != {end0-start0}")
    return seq, path


def gc_fraction(seq: str):
    s = seq.upper()
    good = sum(1 for c in s if c in "ACGT")
    if good == 0:
        return math.nan
    gc = sum(1 for c in s if c in "GC")
    return gc / good


def load_selected_positives(candidate_path: Path, source_vcf: Path):
    needs = {}
    for b in SIZE_BINS:
        needs[(b, "high_mappability_non_repeat")] = 4
        needs[(b, "repeat")] = 2
        needs[(b, "low_mappability_non_repeat")] = 2
    needs[(">=5000", "repeat")] = 4
    needs[(">=5000", "low_mappability_non_repeat")] = 0

    rows = []
    with candidate_path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            if row["ineligible_reason"] == "":
                rows.append(row)
    selected = []
    quota = []
    for b in SIZE_BINS:
        for ctx in CONTEXTS:
            need = needs.get((b, ctx), 0)
            pool = [r for r in rows if r["size_bin"] == b and r["context"] == ctx]
            pool.sort(key=lambda r: r["rank_hash"])
            selected.extend(pool[:need])
            quota.append({
                "size_bin": b,
                "context": ctx,
                "eligible_denominator": len(pool),
                "selected": need,
                "status": "not_tested_denominator_zero" if need == 0 else ("pass" if len(pool) >= need else "blocked"),
            })
    if len(selected) != 48:
        raise RuntimeError(f"selected {len(selected)} positives, expected 48")

    # Recover inserted sequences from the VCF for selected normalized IDs.
    wanted = {r["normalized_id"]: r for r in selected}
    with gzip.open(source_vcf, "rt", encoding="utf-8") as handle:
        for line in handle:
            if line.startswith("#"):
                continue
            f = line.rstrip("\n").split("\t")
            chrom, pos_text, vid, ref, alt = f[0], f[1], f[2], f[3], f[4]
            if "," in alt or chrom not in AUTOSOMES:
                continue
            anchor, inserted = normalize_insertion(int(pos_text), ref, alt)
            if anchor is None:
                continue
            norm = f"{chrom}:{anchor}:{vid}:{len(inserted)}:{sha_text(inserted)}"
            if norm in wanted:
                wanted[norm]["inserted_sequence"] = inserted
    missing = [r["normalized_id"] for r in selected if "inserted_sequence" not in r]
    if missing:
        raise RuntimeError(f"missing inserted sequence for {len(missing)} selected positives")

    for row in selected:
        row["coded_id"] = "OMV21_" + sha_text("OMEGA-v02.1-code|" + row["normalized_id"])[:14]
    return selected, quota


def load_sv_breakpoints(vcf: Path):
    by = defaultdict(list)
    with gzip.open(vcf, "rt", encoding="utf-8") as handle:
        for line in handle:
            if line.startswith("#"):
                continue
            f = line.rstrip("\n").split("\t")
            chrom = f[0]
            if chrom not in AUTOSOMES:
                continue
            info = parse_info(f[7])
            try:
                by[chrom].append(int(f[1]))
                if "END" in info:
                    by[chrom].append(int(str(info["END"]).split(",", 1)[0]))
            except Exception:
                pass
    return dict(by)


def main():
    if len(sys.argv) != 5:
        raise SystemExit("usage: select_v02_1_panel_v01.py SOURCE_DIR V02_AUDIT_DIR PRIVATE_V02_1_DIR PUBLIC_AUDIT_DIR")
    source_dir = Path(sys.argv[1])
    v02_audit = Path(sys.argv[2])
    private_root = Path(sys.argv[3])
    public_dir = Path(sys.argv[4])
    escrow = private_root / "truth_escrow"
    manifest_dir = private_root / "production_manifest_pending_manager_release"
    seq_cache = private_root / "reference_sequence_cache_ucsc_api"
    for d in (escrow, manifest_dir, public_dir):
        d.mkdir(parents=True, exist_ok=True)

    vcf = source_dir / "HG002_SVs_Tier1_v0.6.vcf.gz"
    bed = source_dir / "HG002_SVs_Tier1_v0.6.bed"
    chrom_info = source_dir / "chromInfo.hg19.ucsc.txt.gz"
    gap = source_dir / "gap.hg19.ucsc.txt.gz"
    rmsk = source_dir / "rmsk.hg19.ucsc.txt.gz"
    umap = source_dir / "k100.umap.hg19.multi_read.bedgraph.gz"
    candidates = v02_audit / "private_positive_candidates_v01.tsv"
    exposed_path = v02_audit / "private_exposed_locus_anchors_v01.tsv"

    positives, quota = load_selected_positives(candidates, vcf)
    hc = read_intervals(bed)
    gaps = read_intervals(gap, chrom_col=1, start_col=2, end_col=3)
    chrom_sizes = read_chrom_sizes(chrom_info)
    sv_breakpoints = load_sv_breakpoints(vcf)
    exposed = defaultdict(list)
    with exposed_path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            exposed[row["chrom"]].append(int(row["anchor_1b"]))

    pos_by_chrom = defaultdict(list)
    for p in positives:
        pos_by_chrom[p["chrom"]].append(p)

    selected_positive_positions = [(p["chrom"], int(p["anchor_1b"])) for p in positives]
    selected_shams = []
    used_shams = []
    best_sham_by_positive = {}
    seq_cache_files = []

    for chrom, chrom_positives in sorted(pos_by_chrom.items(), key=lambda item: int(item[0])):
        ucsc = chrom_ucsc(chrom)
        chrom_len = chrom_sizes[ucsc]
        spans = []
        for p in chrom_positives:
            anchor = int(p["anchor_1b"])
            spans.append((max(1001, anchor - 5_000_000), min(chrom_len - 1000, anchor + 5_000_000)))
        spans0 = [(a - 151, b + 150) for a, b in spans]
        spans0 = merge_intervals(spans0)

        chrom_repeat_intervals = []
        # RepeatMasker intervals for this chromosome only, with class/family retained not needed for sham audit.
        with gzip.open(rmsk, "rt", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                f = line.rstrip("\n").split("\t")
                if len(f) >= 13 and f[5] == ucsc:
                    try:
                        chrom_repeat_intervals.append((int(f[6]), int(f[7])))
                    except Exception:
                        pass
        chrom_repeat_intervals.sort()

        chrom_umap = []
        with gzip.open(umap, "rt", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                if not line.strip() or line.startswith("track") or line.startswith("#"):
                    continue
                f = line.rstrip("\n").split("\t")
                if len(f) >= 4 and f[0] == ucsc:
                    try:
                        chrom_umap.append((int(f[1]), int(f[2]), float(f[3])))
                    except Exception:
                        pass

        for fetch_start0, fetch_end0 in spans0:
            fetch_start0 = max(0, fetch_start0)
            fetch_end0 = min(chrom_len, fetch_end0)
            seq, seq_path = fetch_sequence(seq_cache, ucsc, fetch_start0, fetch_end0)
            seq_cache_files.append(seq_path)
            length = fetch_end0 - fetch_start0
            hc_mask = bytearray(length)
            gap_mask = bytearray(length)
            sv_mask = bytearray(length)
            exposed_mask = bytearray(length)
            repeat_mask = bytearray(length)
            umap_cov = bytearray(length)
            umap_one = bytearray(length)

            for a, b in hc.get(chrom, []):
                mark_interval(hc_mask, fetch_start0, a, b)
            for a, b in gaps.get(ucsc, []):
                mark_interval(gap_mask, fetch_start0, a, b)
            for bp in sv_breakpoints.get(chrom, []):
                mark_interval(sv_mask, fetch_start0, bp - 10001, bp + 10000)
            for bp in exposed.get(chrom, []):
                mark_interval(exposed_mask, fetch_start0, bp - 10001, bp + 10000)
            for a, b in chrom_repeat_intervals:
                if a < fetch_end0 and b > fetch_start0:
                    mark_interval(repeat_mask, fetch_start0, a, b)
            for a, b, score in chrom_umap:
                if a < fetch_end0 and b > fetch_start0:
                    mark_interval(umap_cov, fetch_start0, a, b)
                    if score == 1.0:
                        mark_interval(umap_one, fetch_start0, a, b)

            hc_pref = prefix_from_mask(hc_mask)
            gap_pref = prefix_from_mask(gap_mask)
            sv_pref = prefix_from_mask(sv_mask)
            exp_pref = prefix_from_mask(exposed_mask)
            rep_pref = prefix_from_mask(repeat_mask)
            cov_pref = prefix_from_mask(umap_cov)
            one_pref = prefix_from_mask(umap_one)
            np_hc = np.frombuffer(hc_mask, dtype=np.uint8)
            np_gap_pref = np_prefix(gap_mask)
            np_sv = np.frombuffer(sv_mask, dtype=np.uint8)
            np_exp = np.frombuffer(exposed_mask, dtype=np.uint8)
            np_rep_pref = np_prefix(repeat_mask)
            np_cov_pref = np_prefix(umap_cov)
            np_one_pref = np_prefix(umap_one)
            seq_arr = np.frombuffer(seq.encode("ascii"), dtype=np.uint8)
            gc_mask = np.isin(seq_arr, np.frombuffer(b"GC", dtype=np.uint8)).astype(np.uint8)
            good_mask = np.isin(seq_arr, np.frombuffer(b"ACGT", dtype=np.uint8)).astype(np.uint8)
            gc_pref = np.concatenate(([0], np.cumsum(gc_mask, dtype=np.int64)))
            good_pref = np.concatenate(([0], np.cumsum(good_mask, dtype=np.int64)))

            span_anchor_start = fetch_start0 + 151
            span_anchor_end = fetch_end0 - 150
            for p in chrom_positives:
                anchor = int(p["anchor_1b"])
                if anchor < span_anchor_start + 1000 or anchor > span_anchor_end - 1000:
                    continue
                # Positive GC and context annotation from same sequence cache.
                idx = anchor - 1 - fetch_start0
                if 150 <= idx < len(seq) - 150:
                    p["gc_301"] = f"{gc_fraction(seq[idx-150:idx+151]):.6f}"

                target_gc = float(p["gc_301"])
                lo = max(span_anchor_start + 1000, anchor - 5_000_000)
                hi = min(span_anchor_end - 1000, anchor + 5_000_000)
                if lo > hi:
                    continue
                anchors = np.arange(lo, hi + 1, dtype=np.int64)
                dist = np.abs(anchors - anchor)
                mask = (dist >= 100_000) & (dist <= 5_000_000)
                base_idx = anchors - 1 - fetch_start0
                win_a = base_idx - 150
                win_b = base_idx + 151
                ext_a = anchors - 1001 - fetch_start0
                ext_b = anchors + 1000 - fetch_start0
                mask &= (base_idx >= 0) & (win_a >= 0) & (win_b <= length) & (ext_a >= 0) & (ext_b <= length)
                if not mask.any():
                    continue
                mask &= np_hc[base_idx] == 1
                mask &= np_pref_sum(np_gap_pref, ext_a, ext_b) == 0
                mask &= np_sv[base_idx] == 0
                mask &= np_exp[base_idx] == 0
                for cpos_chrom, cpos in selected_positive_positions:
                    if cpos_chrom == chrom:
                        mask &= np.abs(anchors - cpos) >= 10_000
                for sham_chrom, sham_pos in used_shams:
                    if sham_chrom == chrom:
                        mask &= np.abs(anchors - sham_pos) >= 10_000
                if not mask.any():
                    continue
                rep_bp_arr = np_pref_sum(np_rep_pref, win_a, win_b)
                cov_bp_arr = np_pref_sum(np_cov_pref, win_a, win_b)
                one_bp_arr = np_pref_sum(np_one_pref, win_a, win_b)
                mask &= cov_bp_arr >= 271
                if p["context"] == "repeat":
                    mask &= rep_bp_arr >= 20
                elif p["context"] == "high_mappability_non_repeat":
                    mask &= (rep_bp_arr == 0) & (one_bp_arr / np.maximum(cov_bp_arr, 1) >= 0.95)
                elif p["context"] == "low_mappability_non_repeat":
                    mask &= (rep_bp_arr < 20) & (one_bp_arr / np.maximum(cov_bp_arr, 1) <= 0.80)
                else:
                    continue
                good_arr = np_pref_sum(good_pref, win_a, win_b)
                gc_arr = np_pref_sum(gc_pref, win_a, win_b)
                gc_frac = gc_arr / np.maximum(good_arr, 1)
                mask &= (good_arr > 0) & (np.abs(gc_frac - target_gc) <= 0.02)
                idxs = np.nonzero(mask)[0]
                current_best = best_sham_by_positive.get(p["coded_id"])
                for arr_idx in idxs.tolist():
                    sham_anchor = int(anchors[arr_idx])
                    digest = sha_text(f"OMEGA-v02-sham|{p['coded_id']}|{chrom}|{sham_anchor}")
                    if current_best is None or digest < current_best["sham_rank_hash"]:
                        current_best = {
                            "paired_positive_code": p["coded_id"],
                            "coded_id": "OMV21_" + sha_text(f"OMEGA-v02.1-code|sham|{p['coded_id']}|{chrom}|{sham_anchor}")[:14],
                            "chrom": chrom,
                            "anchor_1b": sham_anchor,
                            "context": p["context"],
                            "gc_301": f"{float(gc_frac[arr_idx]):.6f}",
                            "distance_to_positive_bp": int(dist[arr_idx]),
                            "sham_rank_hash": digest,
                            "repeat_bp": int(rep_bp_arr[arr_idx]),
                            "umap_cov_bp": int(cov_bp_arr[arr_idx]),
                            "umap_one_bp": int(one_bp_arr[arr_idx]),
                        }
                if current_best is not None:
                    best_sham_by_positive[p["coded_id"]] = current_best

    # Apply sham uniqueness in positive code order. If a best sham conflicts with an
    # already selected sham, this conservative pass blocks instead of re-ranking
    # after observing the conflict.
    for p in positives:
        best = best_sham_by_positive.get(p["coded_id"])
        if best and not any(c == best["chrom"] and abs(int(best["anchor_1b"]) - pos) < 10_000 for c, pos in used_shams):
            selected_shams.append(best)
            used_shams.append((best["chrom"], int(best["anchor_1b"])))

    missing_shams = [p["coded_id"] for p in positives if not any(s["paired_positive_code"] == p["coded_id"] for s in selected_shams)]
    status = "verified" if len(selected_shams) == 48 and not missing_shams else "blocked"

    # Write private escrow.
    pos_fields = ["coded_id","role","chrom","anchor_1b","window_start_1b","window_end_1b","size_bin","context","truth_length_bp","truth_inserted_sequence","truth_inserted_sha256","variant_id","normalized_id","gc_301","rank_hash"]
    pos_path = escrow / "positive_truth_escrow_v02_1.tsv"
    with pos_path.open("w", newline="", encoding="utf-8") as handle:
        w = csv.DictWriter(handle, delimiter="\t", fieldnames=pos_fields, lineterminator="\n")
        w.writeheader()
        for p in positives:
            anchor = int(p["anchor_1b"])
            w.writerow({
                "coded_id": p["coded_id"], "role": "positive", "chrom": p["chrom"], "anchor_1b": anchor,
                "window_start_1b": anchor - 1000, "window_end_1b": anchor + 1000,
                "size_bin": p["size_bin"], "context": p["context"], "truth_length_bp": p["length"],
                "truth_inserted_sequence": p["inserted_sequence"], "truth_inserted_sha256": p["inserted_sha256"],
                "variant_id": p["variant_id"], "normalized_id": p["normalized_id"], "gc_301": p.get("gc_301","NA"),
                "rank_hash": p["rank_hash"],
            })
    sham_fields = ["coded_id","role","chrom","anchor_1b","window_start_1b","window_end_1b","paired_positive_code","context","gc_301","distance_to_positive_bp","sham_rank_hash","repeat_bp","umap_cov_bp","umap_one_bp"]
    sham_path = escrow / "sham_truth_escrow_v02_1.tsv"
    with sham_path.open("w", newline="", encoding="utf-8") as handle:
        w = csv.DictWriter(handle, delimiter="\t", fieldnames=sham_fields, lineterminator="\n")
        w.writeheader()
        for s in selected_shams:
            anchor = int(s["anchor_1b"])
            row = dict(s)
            row.update({"role": "sham", "window_start_1b": anchor - 1000, "window_end_1b": anchor + 1000})
            w.writerow({k: row.get(k, "") for k in sham_fields})

    # Pending production-facing coded manifest: private until manager release.
    manifest_rows = []
    for p in positives:
        anchor = int(p["anchor_1b"])
        manifest_rows.append({"coded_id": p["coded_id"], "sample_id": "HG002", "reference_build": "GRCh37", "platform": "GIAB_HG002_HiSeqX_PCRfree_30x", "chrom": p["chrom"], "window_start_1b": anchor - 1000, "window_end_1b": anchor + 1000})
    for s in selected_shams:
        anchor = int(s["anchor_1b"])
        manifest_rows.append({"coded_id": s["coded_id"], "sample_id": "HG002", "reference_build": "GRCh37", "platform": "GIAB_HG002_HiSeqX_PCRfree_30x", "chrom": s["chrom"], "window_start_1b": anchor - 1000, "window_end_1b": anchor + 1000})
    manifest_rows.sort(key=lambda r: sha_text("OMEGA-v02-order|" + r["coded_id"]))
    manifest_path = manifest_dir / "omega_v02_1_coded_manifest_PENDING_MANAGER_RELEASE.tsv"
    with manifest_path.open("w", newline="", encoding="utf-8") as handle:
        fields = ["coded_id","sample_id","reference_build","platform","chrom","window_start_1b","window_end_1b"]
        w = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(manifest_rows)

    quota_path = escrow / "quota_audit_v02_1.tsv"
    with quota_path.open("w", newline="", encoding="utf-8") as handle:
        w = csv.DictWriter(handle, delimiter="\t", fieldnames=["size_bin","context","eligible_denominator","selected","status"], lineterminator="\n")
        w.writeheader()
        w.writerows(quota)

    # Privacy-safe audit: no coordinates or truth labels.
    public = {
        "schema": "omega_v02_1_selector_audit_v01",
        "status": status,
        "positive_count": len(positives),
        "sham_count": len(selected_shams),
        "manifest_rows": len(manifest_rows),
        "not_tested_joint_cell": {
            "size_bin": ">=5000",
            "context": "low_mappability_non_repeat",
            "eligible_truth_denominator": 0,
            "selected": 0,
            "interpretation": "not_tested_never_zero_sensitivity_or_pass",
        },
        "missing_shams": len(missing_shams),
        "quota": quota,
        "checksums": {
            "positive_truth_escrow_v02_1": sha_file(pos_path),
            "sham_truth_escrow_v02_1": sha_file(sham_path),
            "coded_manifest_pending_manager_release": sha_file(manifest_path),
            "quota_audit_v02_1": sha_file(quota_path),
            "v02_private_candidate_table": sha_file(candidates),
            "v02_private_exposed_locus_table": sha_file(exposed_path),
        },
        "sequence_cache_files": len(set(seq_cache_files)),
        "sequence_cache_sha256s_private": "stored_in_private_source_manifest_not_public",
        "outcome_inspection": "none",
        "production_handoff": "withheld_pending_manager_audit",
    }
    audit_json = public_dir / "omega_v02_1_selector_audit_public_v01.json"
    audit_json.write_text(json.dumps(public, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit_md = public_dir / "omega_v02_1_selector_audit_public_v01.md"
    lines = [
        "# OMEGA v02.1 selector audit v01",
        "",
        "Date: 2026-08-03",
        "",
        f"Status: {status.upper()}",
        "",
        f"Private escrow root: `{private_root}`",
        "",
        f"Coded manifest path, withheld from Production: `{manifest_path}`",
        "",
        f"Coded manifest SHA256: `{public['checksums']['coded_manifest_pending_manager_release']}`",
        "",
        f"Counts: {len(positives)} positives plus {len(selected_shams)} matched shams.",
        "",
        "The >=5000 bp / low-mappability non-repeat joint cell is NOT TESTED because the eligible truth denominator is 0. It is not zero sensitivity, not a passed stratum, and not extrapolated coverage.",
        "",
        "No OMEGA outcomes were inspected. No manifest was released to Production.",
        "",
        "## Quota denominators",
        "",
        "| Size bin | Context | Eligible denominator | Selected | Status |",
        "|---|---:|---:|---:|---|",
    ]
    for q in quota:
        lines.append(f"| {q['size_bin']} | {q['context']} | {q['eligible_denominator']} | {q['selected']} | {q['status']} |")
    lines += [
        "",
        "## Privacy-safe checksums",
        "",
    ]
    for k, v in public["checksums"].items():
        lines.append(f"- {k}: `{v}`")
    audit_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps(public, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
