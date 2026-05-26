#!/usr/bin/env python3
"""Prepare tokenized heart-development datasets for MaxToki fine-tuning.

Pre-requisite
-------------
Each source dataset must already be tokenized into HuggingFace ``datasets``
format (MaxToki ``input_ids``) using the standard TranscriptomeTokenizer
pipeline. Per-source tokenized files are expected at the paths defined by
``DEFAULT_SOURCE_DATASETS`` below. Run the upstream tokenization step first
if those files do not yet exist.

What this script does
---------------------
1. Load per-source tokenized ``.dataset`` files (CXG, Tyser, Xu, Lázár).
2. Standardize cell-type and developmental-stage columns across sources.
3. Add ``canonical_cell_type`` by applying the JSON harmonization map.
4. Add ``dev_time_num`` — integer developmental time in units of 0.1 PCW
   (post-conception weeks × 10), e.g. PCW 5.5 → 55. This is the time column
   used by the MaxToki trajectory assembler.
5. Add ``source_dataset`` tag (CXG / Tyser / Xu / Lazar).
6. Filter to cells that have a valid canonical cell type and a parseable
   developmental stage.
7. Concatenate all sources into a single merged dataset.
8. Write three stage-disjoint splits:
   - train  : dev_time_pcw < 10  OR  dev_time_pcw > 16
   - val    : 10 ≤ dev_time_pcw ≤ 12  (PCW 10–12 transition window)
   - test   : 13 ≤ dev_time_pcw ≤ 16  (mid-fetal window)

Stage-based splitting (not donor-based) is appropriate for developmental data
because donors are not interchangeable across time in the way brain-aging
donors are. Holding out entire PCW windows tests genuine temporal
generalisation.

Developmental time encoding
----------------------------
``dev_time_num = round(dev_time_pcw * 10)`` produces integers in roughly the
range 30 (PCW 3) to 400 (PCW 40). Timelapse values between two timepoints are
therefore in units of 0.1 PCW (e.g. a gap of 2 PCW → timelapse token 20).
These small integers overlap with the numeric token range already present in
the MaxToki token dictionary; verify coverage with
``scripts/check_token_dict_coverage.py`` before running.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime
from pathlib import Path

from datasets import concatenate_datasets, disable_caching, load_from_disk

disable_caching()

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_DATA = Path("/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data")
_SHARED = Path("/gladstone/theodoris/lab/enockniyonkuru/maxtoki_brain_aging_data/data")

DEFAULT_SOURCE_DATASETS: dict[str, dict] = {
    # key           → tokenized .dataset path
    #               → native cell-type column name
    #               → native developmental-stage column name (or None)
    #               → optional fixed pcw float (overrides stage parsing)
    "CXG": {
        "path": _DATA / "tokenized" / "cxg_heart_dev.dataset",
        "cell_type_col": "cell_type",
        "stage_col": "development_stage",
        "fixed_pcw": None,
    },
    "Tyser": {
        "path": _DATA / "tokenized" / "tyser_heart_dev.dataset",
        "cell_type_col": "cluster",
        "stage_col": "development_stage",
        "fixed_pcw": None,
    },
    "Xu": {
        "path": _DATA / "tokenized" / "xu_heart_dev.dataset",
        "cell_type_col": "cell_type",
        "stage_col": "development_stage",
        "fixed_pcw": None,
    },
    "Lazar": {
        "path": _DATA / "tokenized" / "lazar_hl_heart_dev.dataset",
        "cell_type_col": "cell_type",
        "stage_col": "pcw",      # Lázár often has a numeric PCW column
        "fixed_pcw": None,
    },
}

DEFAULT_HARMONIZATION_MAP = Path(
    "/gladstone/theodoris/home/eniyonkuru/maxtoki_development/"
    "cell_type_harmonization/cell_type_harmonization_map.json"
)

DEFAULT_OUTPUT_DIR = _DATA / "finetuning_heart_dev"

# Stage-based held-out windows (in PCW).
DEFAULT_VAL_PCW_MIN = 10.0
DEFAULT_VAL_PCW_MAX = 12.0
DEFAULT_TEST_PCW_MIN = 13.0
DEFAULT_TEST_PCW_MAX = 16.0

# ---------------------------------------------------------------------------
# PCW parsing helpers
# ---------------------------------------------------------------------------

# Matches "12th week post-fertilization stage", "5th week post-fertilization stage", etc.
_ORDINAL_WEEK_RE = re.compile(r"(\d+)(?:st|nd|rd|th)\s+week\s+post.fertilization", re.IGNORECASE)

# Matches Carnegie-stage labels: "Carnegie stage 17", "CS7", "cs 10", etc.
_CARNEGIE_RE = re.compile(r"(?:carnegie\s+stage|CS)\s*(\d+)", re.IGNORECASE)

# Carnegie-stage → approximate PCW midpoint (commonly used approximations)
_CARNEGIE_TO_PCW: dict[int, float] = {
    1: 0.14, 2: 0.29, 3: 0.43, 4: 0.57, 5: 0.86,
    6: 1.5,  7: 2.5,  8: 3.0,  9: 3.5, 10: 4.0,
    11: 4.5, 12: 5.0, 13: 5.5, 14: 6.0, 15: 6.5,
    16: 7.0, 17: 7.5, 18: 8.0, 19: 8.5, 20: 9.0,
    21: 9.5, 22: 10.0, 23: 10.5,
}

# Embryonic day → PCW (used for Tyser day-labeled cells; ~Day 16 = PCW 2.3)
_DAY_RE = re.compile(r"day\s*(\d+(?:\.\d+)?)", re.IGNORECASE)


def parse_pcw(stage_value) -> float | None:
    """Convert a developmental-stage label to a PCW float.

    Handles:
    - Numeric values already in PCW (Lázár-style numeric pcw column).
    - CXG/UBERON ordinal-week strings ("12th week post-fertilization stage").
    - Carnegie-stage strings ("Carnegie stage 17", "CS7").
    - Embryonic-day strings ("Day 16").
    Returns None if the value cannot be parsed.
    """
    if stage_value is None:
        return None
    # Already numeric → treat directly as PCW
    try:
        value = float(stage_value)
        if 0 < value < 50:       # sanity: valid PCW range
            return value
        if 1 <= value <= 300:    # might be embryonic days
            return round(value / 7.0, 2)
    except (TypeError, ValueError):
        pass

    text = str(stage_value).strip()

    # Ordinal week: "12th week post-fertilization stage" → 12.0
    match = _ORDINAL_WEEK_RE.search(text)
    if match:
        return float(match.group(1))

    # Carnegie stage: "Carnegie stage 17" or "CS17" → map to PCW
    match = _CARNEGIE_RE.search(text)
    if match:
        cs = int(match.group(1))
        return _CARNEGIE_TO_PCW.get(cs, None)

    # Embryonic day: "Day 16" → PCW
    match = _DAY_RE.search(text)
    if match:
        day = float(match.group(1))
        return round(day / 7.0, 2)

    return None


# ---------------------------------------------------------------------------
# Harmonization map helpers
# ---------------------------------------------------------------------------

def load_harmonization_map(path: Path) -> dict[str, str]:
    """Load the cell-type harmonization JSON and return alias → canonical mapping.

    The JSON structure is:
    {
      "lineage_tree_aliases": {
        "Canonical Name": ["alias1", "alias2", ...],
        ...
      }
    }
    Returns a flat dict mapping every alias (and canonical) → canonical name.
    """
    raw = json.loads(path.read_text())
    alias_to_canonical: dict[str, str] = {}
    for canonical, aliases in raw.get("lineage_tree_aliases", {}).items():
        # Skip meta-comment entries
        if canonical.startswith(":"):
            continue
        for alias in aliases:
            alias_to_canonical[alias.strip()] = canonical
        alias_to_canonical[canonical.strip()] = canonical
    return alias_to_canonical


# ---------------------------------------------------------------------------
# General helpers
# ---------------------------------------------------------------------------

def remove_if_needed(path: Path, overwrite: bool) -> None:
    if not path.exists():
        return
    if not overwrite:
        raise FileExistsError(f"{path} already exists. Pass --overwrite to replace it.")
    shutil.rmtree(path)


def save_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def map_num_proc(nproc: int) -> int | None:
    return nproc if nproc and nproc > 1 else None


# ---------------------------------------------------------------------------
# Per-source loading and standardisation
# ---------------------------------------------------------------------------

def load_and_standardize_source(
    source_name: str,
    cfg: dict,
    alias_to_canonical: dict[str, str],
    nproc: int,
    max_cells: int | None,
) -> object:
    """Load one source tokenized dataset and add standardized columns."""
    ds_path = Path(cfg["path"])
    if not ds_path.exists():
        raise FileNotFoundError(
            f"Tokenized dataset for source '{source_name}' not found at {ds_path}. "
            "Run the upstream tokenization step first."
        )
    print(f"Loading {source_name}: {ds_path}")
    ds = load_from_disk(str(ds_path))
    if "input_ids" not in ds.column_names:
        raise ValueError(f"Dataset {source_name} is missing 'input_ids'. Is it tokenized?")

    if max_cells is not None and len(ds) > max_cells:
        import random
        rng = random.Random(42)
        indices = sorted(rng.sample(range(len(ds)), max_cells))
        ds = ds.select(indices)

    cell_type_col = cfg["cell_type_col"]
    stage_col = cfg.get("stage_col")
    fixed_pcw = cfg.get("fixed_pcw")
    num_proc = map_num_proc(nproc)

    # Validate required columns
    if cell_type_col not in ds.column_names:
        raise ValueError(
            f"Source '{source_name}' is missing cell-type column '{cell_type_col}'. "
            f"Available columns: {ds.column_names}"
        )
    if stage_col and stage_col not in ds.column_names and fixed_pcw is None:
        raise ValueError(
            f"Source '{source_name}' is missing stage column '{stage_col}'. "
            f"Available columns: {ds.column_names}"
        )

    def add_standard_columns(batch):
        cell_types = batch[cell_type_col]
        canonical_types = [
            alias_to_canonical.get(str(ct).strip(), None)
            for ct in cell_types
        ]
        if fixed_pcw is not None:
            pcw_values = [fixed_pcw] * len(cell_types)
        elif stage_col:
            pcw_values = [parse_pcw(s) for s in batch[stage_col]]
        else:
            pcw_values = [None] * len(cell_types)

        dev_time_num = [
            int(round(pcw * 10)) if pcw is not None else None
            for pcw in pcw_values
        ]
        return {
            "canonical_cell_type": canonical_types,
            "dev_time_pcw": pcw_values,
            "dev_time_num": dev_time_num,
            "source_dataset": [source_name] * len(cell_types),
        }

    ds = ds.map(add_standard_columns, batched=True, num_proc=num_proc)

    # Filter to cells with valid canonical type and parseable PCW
    n_before = len(ds)
    ds = ds.filter(
        lambda ex: (
            ex["canonical_cell_type"] is not None
            and ex["dev_time_pcw"] is not None
            and ex["dev_time_num"] is not None
            and ex["dev_time_num"] > 0
        ),
        num_proc=num_proc,
    )
    n_after = len(ds)
    print(
        f"  {source_name}: {n_before:,} cells → {n_after:,} kept "
        f"(dropped {n_before - n_after:,} with unresolved type or stage)"
    )
    return ds


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Prepare merged heart-development data for MaxToki fine-tuning."
    )
    parser.add_argument(
        "--harmonization-map", type=Path, default=DEFAULT_HARMONIZATION_MAP,
        help="Path to the cell_type_harmonization_map.json file.",
    )
    parser.add_argument(
        "--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR,
        help="Root output directory for all prepared datasets and manifests.",
    )
    # Per-source dataset overrides (comma-separated key=path pairs)
    parser.add_argument(
        "--source-dataset-paths", default=None,
        help=(
            "Override source dataset paths as comma-separated 'KEY=path' pairs. "
            "e.g. 'CXG=/my/cxg.dataset,Tyser=/my/tyser.dataset'"
        ),
    )
    parser.add_argument(
        "--sources", default=",".join(DEFAULT_SOURCE_DATASETS.keys()),
        help="Comma-separated list of source names to include (default: all four).",
    )
    # Stage-based split thresholds
    parser.add_argument("--val-pcw-min", type=float, default=DEFAULT_VAL_PCW_MIN)
    parser.add_argument("--val-pcw-max", type=float, default=DEFAULT_VAL_PCW_MAX)
    parser.add_argument("--test-pcw-min", type=float, default=DEFAULT_TEST_PCW_MIN)
    parser.add_argument("--test-pcw-max", type=float, default=DEFAULT_TEST_PCW_MAX)
    # Optional per-source cell caps (for debugging)
    parser.add_argument(
        "--max-cells-per-source", type=int, default=None,
        help="Cap cells per source dataset (for quick debug runs).",
    )
    parser.add_argument("--nproc", type=int, default=8)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    train_path = output_dir / "source_train_heart_dev.dataset"
    val_path = output_dir / "source_val_heart_dev.dataset"
    test_path = output_dir / "source_test_heart_dev.dataset"
    manifest_path = output_dir / "prepared_source_manifest.json"
    for p in (train_path, val_path, test_path):
        remove_if_needed(p, args.overwrite)

    # Parse source overrides
    source_cfgs = {name: dict(cfg) for name, cfg in DEFAULT_SOURCE_DATASETS.items()}
    if args.source_dataset_paths:
        for pair in args.source_dataset_paths.split(","):
            pair = pair.strip()
            if "=" not in pair:
                raise ValueError(f"Invalid --source-dataset-paths entry: '{pair}'. Expected 'KEY=path'.")
            key, path_str = pair.split("=", 1)
            key = key.strip()
            if key not in source_cfgs:
                raise ValueError(f"Unknown source key '{key}'. Valid keys: {list(source_cfgs)}")
            source_cfgs[key]["path"] = Path(path_str.strip())

    active_sources = [s.strip() for s in args.sources.split(",") if s.strip()]
    for name in active_sources:
        if name not in source_cfgs:
            raise ValueError(f"Unknown source '{name}'. Valid: {list(source_cfgs)}")

    alias_to_canonical = load_harmonization_map(args.harmonization_map)
    print(f"Loaded harmonization map: {len(alias_to_canonical)} aliases → canonical types")

    # Load and standardize all sources
    all_datasets = []
    for name in active_sources:
        ds = load_and_standardize_source(
            name, source_cfgs[name], alias_to_canonical, args.nproc, args.max_cells_per_source
        )
        all_datasets.append(ds)

    print("Concatenating all sources...")
    merged = concatenate_datasets(all_datasets)
    print(f"Merged dataset: {len(merged):,} cells")

    # Cell types present per source
    from collections import Counter
    ct_counts = Counter(merged["canonical_cell_type"])
    print(f"Canonical cell types: {len(ct_counts)}")

    # Filter to canonical types with ≥2 distinct dev_time_num values
    # (need at least two PCW timepoints to form a trajectory)
    from collections import defaultdict
    type_to_times: defaultdict[str, set] = defaultdict(set)
    for ct, tn in zip(merged["canonical_cell_type"], merged["dev_time_num"]):
        if ct and tn is not None:
            type_to_times[ct].add(tn)
    multi_time_types = {ct for ct, times in type_to_times.items() if len(times) >= 2}
    n_before = len(merged)
    merged = merged.filter(
        lambda ex: ex["canonical_cell_type"] in multi_time_types,
        num_proc=map_num_proc(args.nproc),
    )
    print(
        f"After filtering to cell types with ≥2 PCW timepoints: "
        f"{len(merged):,} cells ({n_before - len(merged):,} dropped)"
    )
    print(f"Cell types with ≥2 PCW timepoints: {sorted(multi_time_types)}")

    # Stage-based split
    val_min = args.val_pcw_min
    val_max = args.val_pcw_max
    test_min = args.test_pcw_min
    test_max = args.test_pcw_max
    num_proc = map_num_proc(args.nproc)

    def _is_val(ex):
        pcw = ex["dev_time_pcw"]
        return pcw is not None and val_min <= pcw <= val_max

    def _is_test(ex):
        pcw = ex["dev_time_pcw"]
        return pcw is not None and test_min <= pcw <= test_max

    def _is_train(ex):
        pcw = ex["dev_time_pcw"]
        return pcw is not None and not (val_min <= pcw <= val_max) and not (test_min <= pcw <= test_max)

    train_ds = merged.filter(_is_train, num_proc=num_proc)
    val_ds = merged.filter(_is_val, num_proc=num_proc)
    test_ds = merged.filter(_is_test, num_proc=num_proc)

    if len(train_ds) == 0 or len(val_ds) == 0:
        raise RuntimeError(
            f"Empty split: train={len(train_ds):,}, val={len(val_ds):,}. "
            "Check that your datasets cover the expected PCW ranges."
        )

    train_ds.save_to_disk(str(train_path))
    val_ds.save_to_disk(str(val_path))
    test_ds.save_to_disk(str(test_path))

    manifest = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "harmonization_map": str(args.harmonization_map),
        "output_dir": str(output_dir),
        "active_sources": active_sources,
        "val_pcw_window": [val_min, val_max],
        "test_pcw_window": [test_min, test_max],
        "train_pcw_note": "PCW < val_min OR PCW > test_max",
        "n_merged_cells_after_filter": len(merged),
        "n_train_cells": len(train_ds),
        "n_val_cells": len(val_ds),
        "n_test_cells": len(test_ds),
        "n_canonical_cell_types": len(multi_time_types),
        "canonical_cell_types_with_multi_pcw": sorted(multi_time_types),
        "cell_type_counts": {k: v for k, v in sorted(ct_counts.items())},
        "train_dataset": str(train_path),
        "val_dataset": str(val_path),
        "test_dataset": str(test_path),
    }
    save_json(manifest_path, manifest)

    print(f"Train: {len(train_ds):,} cells → {train_path}")
    print(f"Val:   {len(val_ds):,} cells  → {val_path}  (PCW {val_min}–{val_max})")
    print(f"Test:  {len(test_ds):,} cells  → {test_path} (PCW {test_min}–{test_max})")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
