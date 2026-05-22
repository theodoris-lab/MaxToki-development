#!/usr/bin/env python3
"""Apply the cell-type harmonization map to each h5ad dataset.

For every AnnData file listed in DATASETS, reads the 'cell_type' column from
.obs and adds three new columns:

  cell_type_harmonized    – canonical label from the lineage tree
  harmonization_confidence– high / medium / low / none
  lineage_path_str        – ancestors joined with ' → '

Run with --dry-run to see coverage stats without modifying any file.
Run with --datasets <key> [<key> ...] to restrict to specific datasets.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import unicodedata
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Dataset registry
# ---------------------------------------------------------------------------
_DATA = Path("/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data")
_CXG  = _DATA / "source_1_cellxgene_heart_development_subset"
_SRC4 = _DATA / "source_2_3_4_h5ad_converted" / "source_4_lab_directory"

DATASETS: Dict[str, Path] = {
    "cxg_01_human_cell_landscape":   _CXG / "01_construction_of_a_human_cell_landscape_at_single_cell_level_heart_development_subset.h5ad",
    "cxg_02_million_cells":          _CXG / "02_survey_of_human_embryonic_development_1_million_cells_subset_heart_development_subset.h5ad",
    "cxg_03_embryonic_dev":          _CXG / "03_survey_of_human_embryonic_development_heart_development_subset.h5ad",
    "cxg_04_progesterone_receptor":  _CXG / "04_sex_specific_control_of_human_heart_maturation_by_the_progesterone_receptor_heart_development_subset.h5ad",
    "cxg_05_integrated_hearts":      _CXG / "05_integrated_adult_and_foetal_hearts_heart_development_subset.h5ad",
    "cxg_06_rotem_12w_c1":           _CXG / "06_rotem_12w_heart_c1_heart_development_subset.h5ad",
    "cxg_07_rotem_12w_b1":           _CXG / "07_rotem_12w_heart_b1_heart_development_subset.h5ad",
    "cxg_08_rotem_12w_d1":           _CXG / "08_rotem_12w_heart_d1_heart_development_subset.h5ad",
    "cxg_09_rotem_12w_a1":           _CXG / "09_rotem_12w_heart_a1_heart_development_subset.h5ad",
    "cxg_10_outflow_tract":          _CXG / "10_single_nuclei_rna_seq_human_outflow_tract_aortic_valve_heart_development_subset.h5ad",
    "epicardium":                    _SRC4 / "04_fetal_vs_adult_human_epicardium.h5ad",
}

CELL_TYPE_COLUMN = "cell_type"

# Labels observed in h5ad files but absent from the survey report Section 2
# table (so not in the CSV/JSON).  Map here to avoid spurious UNMAPPED counts.
_H5AD_EXTRA: Dict[str, Tuple[str, str, str]] = {
    # fat cell = adipocyte (Cell Ontology synonym used in some datasets)
    "fat cell": (
        "Adipocyte",
        "medium",
        "Epiblast \u2192 Primitive Streak \u2192 Mesoderm \u2192 Splanchnic Mesoderm"
        " \u2192 Proepicardial Organ \u2192 Epicardium \u2192 Epicardium Derived Cell"
        " \u2192 Adipocyte",
    ),
}

# ---------------------------------------------------------------------------
# Label normalisation (must match build_cell_type_harmonization.py exactly)
# ---------------------------------------------------------------------------

def _strip_accents(text: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFKD", text)
        if not unicodedata.combining(c)
    )


def _normalize(text: str) -> str:
    text = text.strip().replace("*", "")
    text = re.sub(r"['`\"]", "'", text)
    text = re.sub(r"\(.*?\)", " ", text)
    text = text.replace("/", " ").replace("-", " ")
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip().lower()


# ---------------------------------------------------------------------------
# Load lookup from harmonization outputs
# ---------------------------------------------------------------------------

_LookupEntry = Tuple[str, str, str]  # (canonical, confidence, lineage_path_str)


def load_lookup(csv_path: Path, json_path: Path) -> Dict[str, _LookupEntry]:
    """Build normalized-label → (canonical, confidence, path_str) from the CSV.

    Falls back to JSON synonym list with 'medium' confidence for any labels
    that appear in the JSON but not the CSV (e.g. future additions).
    """
    lookup: Dict[str, _LookupEntry] = {}

    # Primary: CSV rows have per-label confidence from the mapping strategy
    with csv_path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["mapping_status"] != "mapped":
                continue
            norm = row["normalized_observed_label"]
            lookup[norm] = (
                row["canonical_tree_label"],
                row["confidence_tier"],
                row["lineage_path"],
            )

    # Fallback: JSON synonym lists (in case CSV is stale)
    data = json.loads(json_path.read_text(encoding="utf-8"))
    for canonical, payload in data.get("harmonization_map", {}).items():
        path_str = payload.get("lineage_path_str", "")
        # Also index the canonical itself (high confidence)
        norm_canon = _normalize(canonical)
        if norm_canon not in lookup:
            lookup[norm_canon] = (canonical, "high", path_str)
        # Synonyms at medium confidence as fallback
        for syn in payload.get("synonyms", []):
            norm_syn = _normalize(syn)
            if norm_syn not in lookup:
                lookup[norm_syn] = (canonical, "medium", path_str)

    # Merge h5ad-specific extras (lower priority than CSV/JSON)
    for raw_label, entry in _H5AD_EXTRA.items():
        norm = _normalize(raw_label)
        if norm not in lookup:
            lookup[norm] = entry

    return lookup


# ---------------------------------------------------------------------------
# Per-cell mapping
# ---------------------------------------------------------------------------

def _map_cell_types(
    cell_types: List[str],
    lookup: Dict[str, _LookupEntry],
) -> Tuple[List[str], List[str], List[str]]:
    harmonized: List[str] = []
    confidences: List[str] = []
    paths: List[str] = []
    for ct in cell_types:
        entry = lookup.get(_normalize(str(ct)))
        if entry:
            canon, conf, path = entry
            harmonized.append(canon)
            confidences.append(conf)
            paths.append(path)
        else:
            harmonized.append("UNMAPPED")
            confidences.append("none")
            paths.append("")
    return harmonized, confidences, paths


# ---------------------------------------------------------------------------
# Per-file processing
# ---------------------------------------------------------------------------

def process_file(
    name: str,
    path: Path,
    lookup: Dict[str, _LookupEntry],
    dry_run: bool,
) -> None:
    import anndata as ad

    if not path.exists():
        print(f"  [SKIP] {name}: not found at {path}")
        return

    print(f"\n{'=' * 60}")
    print(f"  Dataset : {name}")
    print(f"  File    : {path.name}")

    # Read only obs (backed mode keeps memory low for large files)
    adata = ad.read_h5ad(path, backed="r")
    n_cells = adata.n_obs

    if CELL_TYPE_COLUMN not in adata.obs.columns:
        avail = list(adata.obs.columns)
        print(f"  [SKIP] Column '{CELL_TYPE_COLUMN}' not in .obs. Available: {avail[:10]}")
        adata.file.close()
        return

    cell_types_series = adata.obs[CELL_TYPE_COLUMN].copy()
    adata.file.close()

    cell_types = cell_types_series.tolist()
    unique_labels = sorted(set(cell_types))
    print(f"  Cells   : {n_cells:,}  |  Unique labels: {len(unique_labels)}")

    harmonized, confidences, paths = _map_cell_types(cell_types, lookup)

    mapped_n  = sum(1 for h in harmonized if h != "UNMAPPED")
    high_n    = sum(1 for c in confidences if c == "high")
    medium_n  = sum(1 for c in confidences if c == "medium")
    low_n     = sum(1 for c in confidences if c == "low")
    pct       = mapped_n / n_cells * 100 if n_cells else 0.0

    print(f"  Mapped  : {mapped_n:,}/{n_cells:,} cells ({pct:.1f}%)")
    print(f"    high={high_n:,}  medium={medium_n:,}  low={low_n:,}  unmapped={n_cells - mapped_n:,}")

    unmapped_labels = {ct for ct, h in zip(cell_types, harmonized) if h == "UNMAPPED"}
    if unmapped_labels:
        print(f"  Unmapped label(s): {sorted(unmapped_labels)}")

    if dry_run:
        print("  [DRY RUN] No changes written.")
        return

    # Full read for writing
    print("  Writing updated h5ad …")
    adata = ad.read_h5ad(path)
    adata.obs["cell_type_harmonized"]    = harmonized
    adata.obs["harmonization_confidence"] = confidences
    adata.obs["lineage_path_str"]        = paths
    adata.write_h5ad(path)
    print("  Done — added cell_type_harmonized, harmonization_confidence, lineage_path_str")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Apply harmonization map to h5ad datasets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--map-csv",
        type=Path,
        default=Path("cell_type_harmonization/cell_type_harmonization_table.csv"),
        help="Harmonization table CSV (produced by build_cell_type_harmonization.py)",
    )
    parser.add_argument(
        "--map-json",
        type=Path,
        default=Path("cell_type_harmonization/cell_type_harmonization_map.json"),
        help="Harmonization map JSON (produced by build_cell_type_harmonization.py)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print coverage stats without modifying any file",
    )
    parser.add_argument(
        "--datasets",
        nargs="*",
        metavar="KEY",
        default=list(DATASETS.keys()),
        help=f"Dataset keys to process (default: all). Choices: {list(DATASETS.keys())}",
    )
    args = parser.parse_args()

    print(f"Loading harmonization map from {args.map_csv} + {args.map_json}")
    lookup = load_lookup(args.map_csv, args.map_json)
    print(f"  {len(lookup)} normalized labels in lookup")

    if args.dry_run:
        print("\n*** DRY RUN MODE — no files will be modified ***")

    invalid = [k for k in args.datasets if k not in DATASETS]
    if invalid:
        parser.error(f"Unknown dataset key(s): {invalid}. Valid keys: {list(DATASETS.keys())}")

    for name in args.datasets:
        process_file(name, DATASETS[name], lookup, args.dry_run)

    print(f"\n{'=' * 60}")
    print("Done.")


if __name__ == "__main__":
    main()
