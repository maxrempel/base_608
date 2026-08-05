from pathlib import Path

RUN = Path(r"C:\claude_base\worklog\deepseek_offload\xg1_participant_variants\evidence_extraction_v02")
TASK = RUN / "task.md"
MARKER = "[SOURCES_INSERTED_BY_DETERMINISTIC_COLLECTOR]"

SOURCES = [
    Path(r"C:\claude_base\projects\XG1\kenefick\kristen_claim_checks_20260713_v01_tomemex.md"),
    Path(r"C:\claude_base\projects\XG1\kenefick\kristen_control_table_20260713_v01_tomemex.md"),
    Path(r"C:\claude_base\projects\XG1\kenefick\kristen_insertion_report_v01_tomemex.md"),
    Path(r"C:\claude_base\projects\XG1\kenefick\kristen_insertion_detection_report_v01_tomemex.md"),
    Path(r"C:\claude_base\projects\XG1\kenefick\kristen_microchimerism_report_v01_tomemex.md"),
    Path(r"C:\claude_base\projects\XG1\kenefick\analysis\kristen_microchimerism_courtgrade_v04.txt"),
    Path(r"C:\claude_base\projects\XG1\kenefick\analysis\kristen_femaleY_mismap_mechanism_X1D_20260705_v01_tomemex.md"),
    Path(r"C:\claude_base\projects\XG1\kenefick\analysis\maternal_hap_candidates_MAF_gate_X1D_20260705_v02_tomemex.md"),
    Path(r"C:\claude_base\projects\XG1\kenefick\omega_detector\SNV_MATERNAL_PHASING_PILOT_v01_tomemex.md"),
    Path(r"C:\claude_base\projects\XG1\kenefick\omega_detector\INSERT_MATERNAL_PHASING_RESULTS_v01_tomemex.md"),
    Path(r"C:\claude_base\projects\XG1\kenefick\omega_detector\INSERTION_FREQUENCY_SIZE_REPORT_v01_tomemex.md"),
    Path(r"C:\claude_base\projects\XG1\kenefick\letters\kristen_maternal_point_substitutions_technical_report_v01.md"),
    Path(r"C:\claude_base\projects\XG1\kenefick\omega_detector\README.md"),
    Path(r"C:\claude_base\projects\XG1\kenefick\omega_detector\starseed_taygeta\indexes\project_index_v21.md"),
    Path(r"C:\claude_base\projects\XG1\kenefick\omega_detector\starseed_taygeta\indexes\terminology_index_v09.md"),
    Path(r"C:\claude_base\projects\XG1\vittorio\VITTORIO_PIANTEDOSI_STATUS_v01_tomemex.md"),
    Path(r"C:\claude_base\projects\XG1\vittorio\VITTORIO_RARITY_PILOT_chr22_v01_tomemex.md"),
    Path(r"C:\claude_base\projects\XG1\vittorio\VITTORIO_RARITY_RESULTS_v01_tomemex.md"),
    Path(r"C:\claude_base\projects\XG1\vittorio\catalogs\H48ZYY71E.insertion_out_of_place_census.txt"),
    Path(r"C:\claude_base\projects\XG1\vittorio\catalogs\H48ZYY71E.rare_deletion_catalog.tsv"),
    Path(r"C:\claude_base\projects\XG1\vittorio\catalogs\H48ZYY71E.rare_insertion_catalog.tsv"),
    Path(r"C:\claude_base\projects\XG1\vittorio\catalogs\HYMQHR3VV.insertion_out_of_place_census.txt"),
    Path(r"C:\claude_base\projects\XG1\vittorio\catalogs\HYMQHR3VV.rare_deletion_catalog.tsv"),
    Path(r"C:\claude_base\projects\XG1\vittorio\catalogs\HYMQHR3VV.rare_insertion_catalog.tsv"),
]

base = TASK.read_text(encoding="utf-8")
if MARKER not in base:
    raise SystemExit("task marker missing")

blocks = []
for source in SOURCES:
    if not source.is_file():
        raise SystemExit(f"missing source: {source}")
    text = source.read_text(encoding="utf-8", errors="replace")
    blocks.append(f"\n### SOURCE: {source}\n\n```text\n{text}\n```\n")

TASK.write_text(base.replace(MARKER, "\n".join(blocks)), encoding="utf-8")
print(f"packed {len(SOURCES)} sources into {TASK} ({TASK.stat().st_size} bytes)")
