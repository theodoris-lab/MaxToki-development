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

from datasets import Features, Value, concatenate_datasets, disable_caching, load_from_disk

disable_caching()

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_DATA = Path("/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data")
_SHARED = Path("/gladstone/theodoris/lab/enockniyonkuru/maxtoki_brain_aging_data/data")

# Path to the pre-tokenized Tyser 2021 gastrulation dataset (already in .dataset format,
# no re-tokenization needed).  All Tyser cells are CS7 gastrulation → fixed_pcw=2.5.
_TYSER_DATASET = (
    _DATA
    / "source_4_lab_directory"
    / "05_tyser_2021_gastrulation_atlas"
    / "E-MTAB-9388.dataset"
)

DEFAULT_SOURCE_DATASETS: dict[str, dict] = {
    # key           → tokenized .dataset path
    #               → native cell-type column name in the tokenized dataset
    #               → native stage column name (or None if fixed_pcw is set)
    #               → optional fixed pcw float (overrides stage parsing)
    #               → optional 'optional' bool — if True, skip gracefully when missing
    #
    # NOTE on stage_col: TranscriptomeTokenizer always stores the time_column as
    # "time" in the output dataset.  Tokenize-time custom_attr_name_dicts should
    # use time_column=<stage_obs_col> so the stage ends up as "time" here.
    "CXG": {
        "path": _DATA / "tokenized" / "cxg_heart_dev.dataset",
        "cell_type_col": "cell_type",
        "stage_col": "time",  # tokenizer stores development_stage → "time"
        "fixed_pcw": None,
        "optional": False,
    },
    "Tyser": {
        # Already tokenized; CS7 gastrulation → fixed PCW 2.5.
        # Contains 'cell_type' (cluster labels) but no development_stage column.
        "path": _TYSER_DATASET,
        "cell_type_col": "cell_type",
        "stage_col": None,
        "fixed_pcw": 2.5,
        "optional": True,
    },
    "Xu": {
        "path": _DATA / "tokenized" / "xu_heart_dev.dataset",
        "cell_type_col": "cell_type",   # tokenizer maps annotation → "cell_type"
        "stage_col": "time",            # tokenizer maps stage → "time"
        "fixed_pcw": None,
        "optional": False,
    },
    "Lazar": {
        "path": _DATA / "tokenized" / "lazar_hl_heart_dev.dataset",
        "cell_type_col": "cell_type",
        "stage_col": "time",  # tokenizer maps age/pcw → "time"
        "fixed_pcw": None,
        "optional": True,   # skip if not yet tokenized (source is R-only currently)
    },
}

DEFAULT_HARMONIZATION_MAP = Path(
    "/gladstone/theodoris/home/eniyonkuru/maxtoki_development/"
    "cell_type_harmonization/cell_type_harmonization_map.json"
)

DEFAULT_OUTPUT_DIR = _DATA / "finetuning_heart_dev"

# ── Finalized train / val / test split ───────────────────────────────────────
# Val  : PCW 10 (CXG + Lázár, cardiomyocyte maturation onset) and
#         PCW 20 (CXG only, mid-fetal).  Two disjoint timepoints, not a range.
# Test : PCW 7  (Lázár only; genuinely interpolated between PCW 6 and 8 train).
# Train: every other PCW timepoint not matched by val/test points.
# Lineage holdouts are withheld from ALL splits to probe cell-identity
#   generalisation independently of temporal generalisation.
DEFAULT_VAL_PCW_POINTS: list[float] = [10.0, 20.0]
DEFAULT_TEST_PCW_POINTS: list[float] = [7.0]
DEFAULT_PCW_TOLERANCE: float = 0.15   # ±PCW when matching a specific timepoint
DEFAULT_LINEAGE_HOLDOUT_CELL_TYPES: set[str] = {
    "Epicardial / EPDC",
    "Vascular EC",
}

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

# Carnegie-stage range: "CS13-14", "CS15–16" → average of both stages
_CARNEGIE_RANGE_RE = re.compile(
    r"(?:carnegie\s+stage|CS)\s*(\d+)[-\u2013](\d+)", re.IGNORECASE
)

# Short week format: "w7", "w8.5" (Lázár-style age column)
_WEEK_SHORT_RE = re.compile(r"^w(\d+(?:\.\d+)?)$", re.IGNORECASE)


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

    # Short week format (Lázár-style): "w7" → 7.0 PCW
    match = _WEEK_SHORT_RE.match(text)
    if match:
        return float(match.group(1))

    # Carnegie-stage range: "CS13-14" → average PCW of both stages
    match = _CARNEGIE_RANGE_RE.search(text)
    if match:
        cs1 = int(match.group(1))
        cs2 = int(match.group(2))
        pcw1 = _CARNEGIE_TO_PCW.get(cs1)
        pcw2 = _CARNEGIE_TO_PCW.get(cs2)
        if pcw1 is not None and pcw2 is not None:
            return round((pcw1 + pcw2) / 2.0, 2)
        if pcw1 is not None:
            return pcw1
        if pcw2 is not None:
            return pcw2
        return None

    # Carnegie stage single: "Carnegie stage 17" or "CS17" → map to PCW
    match = _CARNEGIE_RE.search(text)
    if match:
        cs = int(match.group(1))
        return _CARNEGIE_TO_PCW.get(cs, None)

    # Embryonic day: "Day 16" → PCW
    match = _DAY_RE.search(text)
    if match:
        day = float(match.group(1))
        return round(day / 7.0, 2)

    # Generic "embryonic stage" / "embryonic human stage" → PCW 5.5
    # Decision: CXG labels ~22,557 cells with this vague UBERON term (no specific
    # week).  The human embryonic period spans PCW 3–8; PCW 5.5 is the midpoint
    # and corresponds to active cardiac morphogenesis (Carnegie stage ~13–15).
    # This is a documented approximation; see cell_type_harmonization/harmonization_decisions.md.
    if text.lower() in (
        "embryonic stage",
        "embryonic human stage",
        "human embryonic stage",
    ):
        return 5.5

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
            # Lowercase keys so lookup is case-insensitive
            alias_to_canonical[alias.strip().lower()] = canonical
        alias_to_canonical[canonical.strip().lower()] = canonical
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
    overwrite: bool = False,
) -> object:
    """Load one source tokenized dataset and add standardized columns."""
    ds_path = Path(cfg["path"])
    if not ds_path.exists():
        if cfg.get("optional", False):
            print(
                f"  [SKIP] {source_name}: tokenized dataset not found at {ds_path}. "
                "Mark as optional=False or run tokenization first to include it."
            )
            return None
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
            alias_to_canonical.get(str(ct).strip().lower(), None)
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

    # Build explicit output features so multiprocess workers agree on types
    # even when some shards have all-None values (which Arrow infers as 'null').
    _new_cols = Features({
        "canonical_cell_type": Value("string"),
        "dev_time_pcw":        Value("float64"),
        "dev_time_num":        Value("int32"),
        "source_dataset":      Value("string"),
    })
    out_features = Features({**ds.features, **_new_cols})
    use_cache = not overwrite
    ds = ds.map(
        add_standard_columns, batched=True, num_proc=num_proc,
        features=out_features, load_from_cache_file=use_cache,
    )

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
        load_from_cache_file=use_cache,
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
        "--data-root", type=Path, default=None,
        help=(
            "Base data root (e.g. /gladstone/theodoris/lab/.../maxtoki_development_data). "
            "When set, --output-dir defaults to DATA_ROOT/finetuning_heart_dev and "
            "per-source paths default to DATA_ROOT/tokenized/<source>.dataset."
        ),
    )
    parser.add_argument(
        "--output-dir", type=Path, default=None,
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
    # Point-based split (specific PCW values, not contiguous ranges)
    parser.add_argument(
        "--val-pcw-points",
        default=",".join(str(p) for p in DEFAULT_VAL_PCW_POINTS),
        help="Comma-separated PCW values to hold out for validation (e.g. '10.0,20.0').",
    )
    parser.add_argument(
        "--test-pcw-points",
        default=",".join(str(p) for p in DEFAULT_TEST_PCW_POINTS),
        help="Comma-separated PCW values to hold out for test (e.g. '7.0').",
    )
    parser.add_argument(
        "--pcw-tolerance", type=float, default=DEFAULT_PCW_TOLERANCE,
        help="±PCW tolerance when matching cells to a specific holdout timepoint.",
    )
    # Lineage holdouts — excluded from every split
    parser.add_argument(
        "--lineage-holdout-cell-types",
        default=",".join(sorted(DEFAULT_LINEAGE_HOLDOUT_CELL_TYPES)),
        help=(
            "Comma-separated canonical cell types to exclude from all train/val/test "
            "splits (lineage generalisation holdout)."
        ),
    )
    # Optional per-source cell caps (for debugging)
    parser.add_argument(
        "--max-cells-per-source", type=int, default=None,
        help="Cap cells per source dataset (for quick debug runs).",
    )
    parser.add_argument("--nproc", type=int, default=8)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    # Resolve data-root derived defaults
    if args.data_root is not None:
        data_root = args.data_root.resolve()
        if args.output_dir is None:
            args.output_dir = data_root / "finetuning_heart_dev"
        # Propagate tokenized sub-paths from data_root unless already overridden
        _tok = data_root / "tokenized"
        _tok_defaults = {
            "CXG":   _tok / "cxg_heart_dev.dataset",
            "Tyser": data_root / "source_4_lab_directory" / "05_tyser_2021_gastrulation_atlas" / "E-MTAB-9388.dataset",
            "Xu":    _tok / "xu_heart_dev.dataset",
            "Lazar": _tok / "lazar_hl_heart_dev.dataset",
        }
        if args.source_dataset_paths is None:
            args.source_dataset_paths = ",".join(
                f"{k}={v}" for k, v in _tok_defaults.items()
            )
    if args.output_dir is None:
        args.output_dir = DEFAULT_OUTPUT_DIR

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
            name, source_cfgs[name], alias_to_canonical, args.nproc, args.max_cells_per_source,
            overwrite=args.overwrite,
        )
        if ds is not None:
            all_datasets.append(ds)

    if not all_datasets:
        raise RuntimeError("No source datasets loaded. Check paths and tokenization.")

    # Align the 'time' column type across sources before concatenating.
    # The tokenizer stores development_stage as 'time'; CXG/Xu have it as
    # string (UBERON labels), Lázár stores numeric PCW floats, and Tyser has
    # no 'time' column at all.  Cast everything to string so concatenation
    # succeeds (dev_time_pcw already holds the parsed numeric value).
    def _cast_time_to_str(ds):
        if "time" not in ds.column_names:
            return ds
        if ds.features["time"] != Value("string"):
            ds = ds.cast_column("time", Value("string"))
        return ds

    all_datasets = [_cast_time_to_str(d) for d in all_datasets]

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

    # ── Lineage holdout filter ──────────────────────────────────────────────
    lineage_holdout_types: set[str] = {
        ct.strip()
        for ct in args.lineage_holdout_cell_types.split(",")
        if ct.strip()
    }
    if lineage_holdout_types:
        n_before = len(merged)
        merged = merged.filter(
            lambda ex: ex["canonical_cell_type"] not in lineage_holdout_types,
            num_proc=map_num_proc(args.nproc),
        )
        print(
            f"After removing lineage holdout cell types {sorted(lineage_holdout_types)}: "
            f"{len(merged):,} cells ({n_before - len(merged):,} dropped)"
        )

    # ── Point-based split ───────────────────────────────────────────────────
    val_pcw_points = [float(p) for p in args.val_pcw_points.split(",") if p.strip()]
    test_pcw_points = [float(p) for p in args.test_pcw_points.split(",") if p.strip()]
    pcw_tol = args.pcw_tolerance
    num_proc = map_num_proc(args.nproc)

    def _near(pcw: float, targets: list[float], tol: float) -> bool:
        return any(abs(pcw - t) <= tol for t in targets)

    def _is_val(ex):
        pcw = ex["dev_time_pcw"]
        return pcw is not None and _near(pcw, val_pcw_points, pcw_tol)

    def _is_test(ex):
        pcw = ex["dev_time_pcw"]
        return pcw is not None and _near(pcw, test_pcw_points, pcw_tol)

    def _is_train(ex):
        pcw = ex["dev_time_pcw"]
        return (
            pcw is not None
            and not _near(pcw, val_pcw_points, pcw_tol)
            and not _near(pcw, test_pcw_points, pcw_tol)
        )

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
        "split_strategy": "point-based",
        "val_pcw_points": val_pcw_points,
        "test_pcw_points": test_pcw_points,
        "pcw_tolerance": pcw_tol,
        "lineage_holdout_cell_types": sorted(lineage_holdout_types),
        "train_pcw_note": (
            f"All PCW not within ±{pcw_tol} of val {val_pcw_points} or "
            f"test {test_pcw_points} points; excludes lineage holdouts"
        ),
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
    print(f"Val:   {len(val_ds):,} cells  → {val_path}  (PCW {val_pcw_points}, ±{pcw_tol})")
    print(f"Test:  {len(test_ds):,} cells  → {test_path} (PCW {test_pcw_points}, ±{pcw_tol})")
    print(f"Lineage holdouts excluded: {sorted(lineage_holdout_types)}")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
