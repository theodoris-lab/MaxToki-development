#!/usr/bin/env python3
"""Convert Lázár et al. 2025 HDCA SC data from shoji h5 format to h5ad.

The 21 CellRanger libraries are stored in the HDCA/SCope "shoji" h5 format
(not standard 10X h5).  This script reads each file, filters to ENSG genes
(stripping Ensembl version suffixes), joins with the exported metadata CSV,
removes excluded-cluster cells, expands abbreviated cell type labels to full
names that match the harmonization map synonyms, and writes one combined h5ad.

Input
-----
  H5 files  : .../lazar_et_al_2025/Spatial dynamics of.../
                   1_Chromium_cellranger_data_SC/*.h5
  Metadata  : .../lazar_et_al_2025/lazar_sc_metadata.csv
                  (barcode, sample_id, age_pcw, cell_type_abbr)

Output
------
  .../lazar_et_al_2025/lazar_sc_heart_dev.h5ad
      obs columns : cell_type (full name), age_pcw (float PCW),
                    sample_id, cell_type_abbr, n_counts, unique_cell_id
      var_names   : bare ENSG IDs (no version suffix), e.g. ENSG00000223972

Usage
-----
  conda run -n env_maxtoki python scripts/convert_lazar_to_h5ad.py
  conda run -n env_maxtoki python scripts/convert_lazar_to_h5ad.py \\
      --h5-dir /path/to/h5s --output /path/to/out.h5ad
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import h5py
import numpy as np
import pandas as pd
import scipy.sparse as sp
import anndata as ad


# ---------------------------------------------------------------------------
# Default paths
# ---------------------------------------------------------------------------

_DATA_ROOT = Path(
    "/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data"
)
_LAZAR_DIR = _DATA_ROOT / "lazar_et_al_2025"
_H5_DIR = (
    _LAZAR_DIR
    / "Spatial dynamics of the developing human heart, pa"
    / "1_Chromium_cellranger_data_SC"
)
_METADATA_CSV = _LAZAR_DIR / "lazar_sc_metadata.csv"
_OUTPUT_H5AD = _LAZAR_DIR / "lazar_sc_heart_dev.h5ad"


# ---------------------------------------------------------------------------
# Cell type mapping: abbreviation → canonical / alias name
# Values must exactly match an entry in lineage_tree_aliases (or be a canonical
# key) in cell_type_harmonization_map.json, because the prepare script does
# an exact-string lookup: alias_to_canonical.get(cell_type, None).
# Abbreviations not listed here keep their original value, which won't match
# any alias and will be dropped by the prepare filter (e.g. TMSB10high_*).
# ---------------------------------------------------------------------------

_CELL_TYPE_EXPANSION: dict[str, str] = {
    # Cardiomyocytes
    "Immat_CM":       "Cardiac Muscle Cell",
    "Prol_CM":        "Cardiac Muscle Cell",
    "Mat_vCM":        "Ventricular Cardiomyocytes",
    "MetAct_vCM_1":   "Ventricular Cardiomyocytes",
    "MetAct_vCM_2":   "Ventricular Cardiomyocytes",
    "Mat_aCM":        "Regular Atrial Cardiac Myocyte",
    "MetAct_aCM":     "Regular Atrial Cardiac Myocyte",
    # Endocardium
    "Endoc_EC":       "Endocardial Cell",
    "EndocCush_EC":   "Endocardial Cushion",
    # Endothelium
    "MicroVasc_EC":   "Capillary Endothelial Cell",
    "MacroVasc_EC":   "Vascular Endothelial Cell",
    "LEC":            "Lymphatic Endothelial Cell",
    "PDE4Chigh_EC":   "Capillary Endothelial Cell",   # PDE4C-high microvascular EC
    # Fibroblasts
    "Int_FB":         "Cardiac Fibroblast",
    "OFT_FB":         "Cardiac Fibroblast",
    "Prol_FB":        "Cardiac Fibroblast",
    "PDE4Chigh_FB":   "Cardiac Fibroblast",
    "AnnFibr_FB":     "Fibroblast",
    # Epicardium
    "EpC":            "Mesothelial Cell of Epicardium",
    "EPDC":           "Epicardium Derived Cell",
    # Smooth muscle / pericytes
    "CA_SMC":         "Vascular Smooth Muscle Cell",
    "OFT_SMC":        "Outflow Tract Smooth Muscle Cell",
    "PC":             "Pericyte",
    "Peric_MC":       "Pericyte-like Mesenchymal Cell",  # alias → Pericyte
    # Valve
    "Valve_MC":       "Valve Mesenchymal Cells",
    # Immune
    "MyC":            "Myeloid Cell",
    "LyC":            "Leukocyte",
    # Neural
    "NB-N":           "Neuron",
    "SCP-GC":         "Schwann Cell",
    # TMSB10high_C_1, TMSB10high_C_2: poorly defined — omitted, dropped downstream
}

# Cluster-label prefix that marks excluded / low-quality cells
_EXCL_PREFIX = "HL_excl"


# ---------------------------------------------------------------------------
# Core reader
# ---------------------------------------------------------------------------

def _read_shoji_h5(
    h5_path: Path,
    gene_idx: np.ndarray,
    gene_ids: np.ndarray,
) -> ad.AnnData:
    """Read one shoji h5 file; return AnnData limited to ENSG genes.

    Parameters
    ----------
    h5_path  : path to one .h5 file
    gene_idx : integer indices of ENSG columns in the full Expression matrix
    gene_ids : bare ENSG IDs (no version suffix) corresponding to gene_idx
    """
    with h5py.File(h5_path, "r") as f:
        g = f["shoji"]
        cell_ids = g["Cellid"][:].astype(str)
        # Expression: (n_cells, n_genes_total), uint16 raw UMI counts
        expr = g["Expression"][:, gene_idx].astype(np.float32)

    X = sp.csr_matrix(expr)
    del expr  # free dense allocation immediately

    n_counts = np.asarray(X.sum(axis=1)).flatten()
    obs = pd.DataFrame(
        {"n_counts": n_counts, "unique_cell_id": cell_ids},
        index=pd.Index(cell_ids, name="barcode"),
    )
    var = pd.DataFrame(index=pd.Index(gene_ids, name="gene_id"))
    return ad.AnnData(X=X, obs=obs, var=var)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Convert Lázár et al. 2025 HDCA SC shoji h5 files to a single h5ad "
            "for MaxToki tokenization."
        )
    )
    parser.add_argument(
        "--h5-dir", type=Path, default=_H5_DIR,
        help="Directory containing the 21 .h5 files (default: %(default)s).",
    )
    parser.add_argument(
        "--metadata-csv", type=Path, default=_METADATA_CSV,
        help="Cell metadata CSV exported from the Seurat RDS (default: %(default)s).",
    )
    parser.add_argument(
        "--output", type=Path, default=_OUTPUT_H5AD,
        help="Output h5ad path (default: %(default)s).",
    )
    args = parser.parse_args()

    # ── 1. Collect h5 files ───────────────────────────────────────────────────
    h5_files = sorted(args.h5_dir.glob("*.h5"))
    if not h5_files:
        sys.exit(f"No .h5 files found in {args.h5_dir}")
    print(f"Found {len(h5_files)} h5 file(s) in {args.h5_dir}")

    # ── 2. Build shared gene index from first file ────────────────────────────
    print("Reading gene reference from first h5 ...")
    with h5py.File(h5_files[0], "r") as f:
        accessions = f["shoji"]["Accession"][:].astype(str)

    # Keep only real human Ensembl gene IDs; strip version suffix
    gene_idx = np.where(np.array([a.startswith("ENSG") for a in accessions]))[0]
    gene_ids_raw = np.array([accessions[i].split(".")[0] for i in gene_idx])
    # Deduplicate: stripping versions can produce identical bare IDs; keep first
    seen: set[str] = set()
    keep = []
    for i, gid in enumerate(gene_ids_raw):
        if gid not in seen:
            seen.add(gid)
            keep.append(i)
    keep_arr = np.array(keep)
    gene_idx = gene_idx[keep_arr]
    gene_ids = gene_ids_raw[keep_arr]
    n_skipped = len(accessions) - len(gene_idx)
    print(f"ENSG genes: {len(gene_ids):,}  (non-ENSG / duplicate-version skipped: {n_skipped})")

    # ── 3. Read each h5 ───────────────────────────────────────────────────────
    adatas: list[ad.AnnData] = []
    for h5_path in h5_files:
        print(f"  Reading {h5_path.name} ...", end=" ", flush=True)
        adata = _read_shoji_h5(h5_path, gene_idx, gene_ids)
        print(f"{adata.n_obs:,} cells")
        adatas.append(adata)

    # ── 4. Concatenate ────────────────────────────────────────────────────────
    print("Concatenating ...")
    combined = ad.concat(adatas, join="inner")
    del adatas
    print(f"Combined: {combined.n_obs:,} cells × {combined.n_vars:,} genes")

    # ── 5. Join metadata ──────────────────────────────────────────────────────
    print("Loading metadata CSV ...")
    meta = pd.read_csv(args.metadata_csv, index_col="barcode")

    common_barcodes = list(combined.obs_names.intersection(meta.index))
    n_missing = combined.n_obs - len(common_barcodes)
    if n_missing:
        print(f"  Warning: {n_missing:,} cells absent from metadata — dropping.")
    combined = combined[common_barcodes].copy()
    combined.obs = combined.obs.join(
        meta[["sample_id", "age_pcw", "cell_type_abbr"]], how="left"
    )

    # ── 6. Filter excluded clusters ───────────────────────────────────────────
    excl_mask = combined.obs["cell_type_abbr"].str.startswith(_EXCL_PREFIX)
    print(f"Removing {excl_mask.sum():,} HL_excl_* cells ...")
    combined = combined[~excl_mask].copy()

    # ── 7. Expand abbreviated cell type labels to full names ──────────────────
    combined.obs["cell_type"] = combined.obs["cell_type_abbr"].map(
        lambda x: _CELL_TYPE_EXPANSION.get(x, x)
    )
    combined.obs["age_pcw"] = combined.obs["age_pcw"].astype(float)

    # ── 8. Write h5ad ─────────────────────────────────────────────────────────
    args.output.parent.mkdir(parents=True, exist_ok=True)
    print(f"Writing → {args.output}")
    combined.write_h5ad(args.output)

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\nDone.")
    print(f"  Cells   : {combined.n_obs:,}")
    print(f"  Genes   : {combined.n_vars:,}")
    print(f"  Age PCW : {combined.obs['age_pcw'].min()} – {combined.obs['age_pcw'].max()}")
    ct_counts = combined.obs["cell_type"].value_counts()
    print(f"  Cell types ({len(ct_counts)}):")
    for ct, n in ct_counts.items():
        print(f"    {ct}: {n:,}")


if __name__ == "__main__":
    main()
