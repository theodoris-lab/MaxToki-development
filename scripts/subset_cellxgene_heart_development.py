#!/usr/bin/env python3
"""Subset CellxGene H5AD files to heart/development/normal cells.

The script uses AnnData backed reads for metadata filtering, then writes one
subset H5AD per input file that has at least one matching observation.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path

import anndata as ad


DATA_DIR = Path("/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data")
DEFAULT_SOURCE_DIR = DATA_DIR / "source_1_cellxgene"
DEFAULT_OUTPUT_DIR = DATA_DIR / "source_1_cellxgene_heart_development_subset"


TARGET_TISSUES = {
    "heart",
    "apical region of left ventricle",
    "right cardiac atrium",
    "left cardiac atrium",
    "heart right ventricle",
    "heart left ventricle",
    "interventricular septum",
    "apex of heart",
    "basal zone of heart",
    "outflow tract myocardium",
    "outflow tract",
}

TARGET_DEVELOPMENT_STAGES = {
    "embryonic stage",
    "10th week post-fertilization stage",
    "11th week post-fertilization stage",
    "12th week post-fertilization stage",
    "13th week post-fertilization stage",
    "14th week post-fertilization stage",
    "15th week post-fertilization stage",
    "16th week post-fertilization stage",
    "17th week post-fertilization stage",
    "18th week post-fertilization stage",
    "19th week post-fertilization stage",
    "19th week post-fertilization, stage",
    "20th week post-fertilization stage",
    "26th week post-fertilization stage",
    "Carnegie stage 17",
}

TARGET_DISEASES = {"normal"}
REQUIRED_OBS_COLUMNS = ("tissue", "development_stage", "disease")


def clean_series(series):
    return series.astype("string").fillna("")


def unique_join(series) -> str:
    values = sorted(v for v in clean_series(series).unique().tolist() if v)
    return "; ".join(values)


def existing_h5ad_shape(path: Path) -> tuple[int | None, int | None]:
    if not path.exists():
        return None, None
    adata = ad.read_h5ad(path, backed="r")
    try:
        return int(adata.n_obs), int(adata.n_vars)
    finally:
        adata.file.close()


def subset_one(path: Path, output_dir: Path, force: bool, dry_run: bool) -> dict[str, object]:
    adata = ad.read_h5ad(path, backed="r")
    try:
        missing = [col for col in REQUIRED_OBS_COLUMNS if col not in adata.obs.columns]
        if missing:
            return {
                "input_file": path.name,
                "status": "skipped_missing_metadata",
                "reason": f"missing obs columns: {', '.join(missing)}",
                "input_cells": int(adata.n_obs),
                "input_genes": int(adata.n_vars),
                "kept_cells": 0,
                "output_file": "",
                "kept_tissues": "",
                "kept_development_stages": "",
                "kept_diseases": "",
            }

        obs = adata.obs
        mask = (
            clean_series(obs["tissue"]).isin(TARGET_TISSUES)
            & clean_series(obs["development_stage"]).isin(TARGET_DEVELOPMENT_STAGES)
            & clean_series(obs["disease"]).isin(TARGET_DISEASES)
        )
        kept = int(mask.sum())
        output_path = output_dir / path.name.replace(".h5ad", "_heart_development_subset.h5ad")

        selected_obs = obs.loc[mask]
        result = {
            "input_file": path.name,
            "status": "dry_run" if dry_run else "pending",
            "reason": "",
            "input_cells": int(adata.n_obs),
            "input_genes": int(adata.n_vars),
            "kept_cells": kept,
            "output_file": str(output_path) if kept else "",
            "kept_tissues": unique_join(selected_obs["tissue"]) if kept else "",
            "kept_development_stages": unique_join(selected_obs["development_stage"]) if kept else "",
            "kept_diseases": unique_join(selected_obs["disease"]) if kept else "",
        }

        if dry_run:
            return result
        if kept == 0:
            result["status"] = "skipped_no_matching_cells"
            result["reason"] = "no observations matched the requested tissue/development_stage/disease filters"
            return result
        if output_path.exists() and not force:
            out_obs, out_vars = existing_h5ad_shape(output_path)
            result["status"] = "skipped_existing"
            result["reason"] = f"output already exists with shape {out_obs} x {out_vars}; use --force to overwrite"
            return result

        subset = adata[mask.to_numpy(), :].to_memory()
        subset.write_h5ad(output_path, compression="gzip")
        result["status"] = "written"
        return result
    finally:
        adata.file.close()


def write_manifest(rows: list[dict[str, object]], output_dir: Path, dry_run: bool) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix = "dry_run" if dry_run else "written"
    manifest = output_dir / f"cellxgene_heart_development_subset_manifest_{suffix}_{timestamp}.tsv"
    fieldnames = [
        "input_file",
        "status",
        "reason",
        "input_cells",
        "input_genes",
        "kept_cells",
        "output_file",
        "kept_tissues",
        "kept_development_stages",
        "kept_diseases",
    ]
    with manifest.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--dry-run", action="store_true", help="count matching cells without writing subset H5AD files")
    parser.add_argument("--force", action="store_true", help="overwrite existing subset H5AD outputs")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    files = sorted(args.source_dir.glob("*.h5ad"))
    if not files:
        raise SystemExit(f"No H5AD files found in {args.source_dir}")

    print(f"Source: {args.source_dir}", flush=True)
    print(f"Output: {args.output_dir}", flush=True)
    print(f"Mode: {'dry run' if args.dry_run else 'write subsets'}", flush=True)
    print(f"Files: {len(files)}", flush=True)

    rows = []
    for idx, path in enumerate(files, start=1):
        print(f"[{idx}/{len(files)}] {path.name}", flush=True)
        row = subset_one(path, args.output_dir, force=args.force, dry_run=args.dry_run)
        rows.append(row)
        print(f"  status={row['status']} kept={row['kept_cells']} / {row['input_cells']}", flush=True)

    manifest = write_manifest(rows, args.output_dir, dry_run=args.dry_run)
    total_kept = sum(int(row["kept_cells"]) for row in rows)
    print(f"Total kept cells: {total_kept}", flush=True)
    print(f"Manifest: {manifest}", flush=True)


if __name__ == "__main__":
    main()
