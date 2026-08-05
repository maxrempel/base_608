## Implementation Specification: Cumulative AluYa5 Trio Atlas

### Tables (Tab-Separated, UTF-8)

#### 1. trio_metadata
Stores family identity, ancestry, and completion status.

| Column              | Type       | Notes |
|---------------------|------------|-------|
| family_id           | string     | Primary key |
| child_id            | string     | |
| mother_id           | string     | |
| father_id           | string     | |
| population          | string     | Controlled: `"unknown"` if not available |
| superpopulation     | string     | Controlled: `"unknown"` if not available |
| batch               | string     | Controlled: `"not_reported"` if not available |
| sequencing_platform | string     | Controlled: `"not_reported"` if not available |
| completion_state    | string     | Enum: `complete`, `pending`, `failed`, `abandoned` |

#### 2. trio_chrom_stats
Frozen denominators and attrition counts per trio per chromosome.  
Primary key: (`family_id`, `chromosome`).  
`family_id` is foreign key to `trio_metadata`.

| Column                       | Type   | Notes |
|------------------------------|--------|-------|
| family_id                    | string | |
| chromosome                   | string | e.g. `chr1` |
| annotated_copies             | int    | Total reference copies annotated |
| alignment_rejected_copies    | int    | Copies rejected by alignment filters |
| accepted_copies              | int    | Remaining after alignment rejection |
| mapped_positions             | int    | Positions mapped after alignment |
| depth_rejected_positions     | int    | Positions rejected by depth filter |
| callable_positions           | int    | Final set for variant calling |
| child_supported_alleles      | int    | Alleles with child read support |
| parent_alleles               | int    | Alleles seen in at least one parent |
| loose_candidate_count        | int    | Before strict filters |
| strict_candidate_count       | int    | After strict filters |
| provenance_checksum          | string | hex hash of raw per-trio input data |
| validation_state             | string | Enum: `unreviewed`, `approved`, `rejected` |

#### 3. candidate_occurrence
One row per candidate per trio, preserving original read evidence.  
Primary key: (`family_id`, `chromosome`, `position`, `child_base`, `direction`).

| Column            | Type   | Notes |
|-------------------|--------|-------|
| family_id         | string | FK to trio_metadata |
| chromosome        | string | |
| position          | int    | 1-based |
| child_base        | char   | `A`, `C`, `G`, `T` (inserted allele) |
| direction         | string | Enum: `5prime`, `3prime`, `both` |
| read_support_text | string | Original evidence string (e.g., read counts) |
| validation_status | string | Enum: `unreviewed`, `validated`, `false_positive`, `parental_dropout`, `mosaic_mother`, `mosaic_father`, `mosaic_child`, `artifact` |
| evidence_checksum | string | hex hash of read evidence row |

#### 4. recurrence_registry
Curated aggregation by exact locus and allele.  
Primary key: (`chromosome`, `position`, `child_base`).

| Column             | Type   | Notes |
|--------------------|--------|-------|
| chromosome         | string | |
| position           | int    | |
| child_base         | char   | |
| total_occurrences  | int    | Number of candidate_occurrence rows for this locus |
| total_families     | int    | Distinct families |
| first_family       | string | Earliest trio (by order of intake) |
| first_batch        | string | Batch of first_family |
| last_family        | string | Most recent trio |
| last_batch         | string | Batch of last_family |
| recurrence_status  | string | Enum: `candidate`, `confirmed`, `recurrent`, `artifact` |
| curator_notes      | string | Free-text, nullable |

### Recurrence Key

Exact recurrence key = (`chromosome`, `position`, `child_base`).  
This defines the exact locus and the inserted allele. Direction (junction side) and read-support details are preserved in `candidate_occurrence` but do not affect aggregation key.

### Controlled Status Values

- **completion_state**: `complete`, `pending`, `failed`, `abandoned`
- **validation_state** (per trio-chrom): `unreviewed`, `approved`, `rejected`
- **validation_status** (per occurrence): `unreviewed`, `validated`, `false_positive`, `parental_dropout`, `mosaic_mother`, `mosaic_father`, `mosaic_child`, `artifact`
- **recurrence_status** (curated): `candidate`, `confirmed`, `recurrent`, `artifact`
- **missing metadata**: `"unknown"` for population/superpopulation; `"not_reported"` for batch/platform

### Automatic Generation vs Curated Registry

**Automatically generated** from existing per-trio outputs:
- `trio_metadata` (one row per trio, can be built from family info and extraction pipeline metadata)
- `trio_chrom_stats` (directly from each chromosome summary, including checksum)
- `candidate_occurrence` (directly from the candidate table, one row per candidate row per trio)

**Requires curated registry**:
- `recurrence_registry` – initial population can be automated by grouping `candidate_occurrence` on recurrence key, but status values (`curated`, `confirmed`, `artifact`) and curator notes must be set manually after reviewing cross-trio evidence, parental mosaicism calls, or known artifacts.

### Fail-Closed Validation Checks

1. **Foreign key integrity**: Every `family_id` in `trio_chrom_stats` and `candidate_occurrence` must exist in `trio_metadata`. If any missing, reject the entire load.

2. **Count arithmetic consistency**: For each row in `trio_chrom_stats`:
   - `annotated_copies` >= `alignment_rejected_copies` + `accepted_copies`
   - `callable_positions` <= `mapped_positions` - `depth_rejected_positions`
   - `strict_candidate_count` <= `loose_candidate_count` <= `accepted_copies`
   If any inequality fails, reject the row.

3. **Occurrence uniqueness per trio**: No duplicate combinations of (`family_id`, `chromosome`, `position`, `child_base`, `direction`) in `candidate_occurrence`. Enforce on insert.

4. **Recurrence registry locus consistency**: Every recurrence key in `recurrence_registry` must have at least one matching row in `candidate_occurrence`. If a curated entry exists with no supporting occurrences, reject the registry update.

5. **Controlled vocabulary adherence**: All columns with enumerated values (`population`, `superpopulation`, `batch`, `sequencing_platform`, all status fields) must use only the defined set. Any unrecognized string causes a hard failure. For `batch` and `platform`, allow free text only if flag `"not_reported"` is used for missing; otherwise require a pre‑registered vocabulary list (provided externally).
