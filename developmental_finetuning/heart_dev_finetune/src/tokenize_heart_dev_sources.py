#!/usr/bin/env python3
"""Tokenize heart-development source h5ads into HuggingFace .dataset format.

Reads raw h5ad files from the source directories and writes tokenized
HuggingFace ``.dataset`` files under ``$DATA_ROOT/tokenized/``.

Sources handled
---------------
CXG
    ``$DATA_ROOT/source_1_cellxgene_heart_development_subset/`` (14 h5ads).
    Variable index already contains Ensembl IDs → ``use_h5ad_index=True``.
    Obs columns used: ``cell_type``, ``development_stage`` (→ "time").
    Output: ``tokenized/cxg_heart_dev.dataset``

Xu
    ``/gladstone/theodoris/lab/dwen/data/organogenesis_data/organogenesis/
    organogenesis_processed.h5ad`` (~185 k cells; var has ``ensembl_id`` col).
    Obs columns used: ``annotation`` (→ "cell_type"), ``stage`` (→ "time").
    All cells are tokenized; non-cardiac cells are dropped by the downstream
    prepare step via the harmonization map.
    Output: ``tokenized/xu_heart_dev.dataset``

Tyser (SKIP)
    Already tokenized as ``E-MTAB-9388.dataset`` in
    ``$DATA_ROOT/source_4_lab_directory/05_tyser_2021_gastrulation_atlas/``.
    The prepare script reads it directly; no re-tokenization needed.

Lázár
    ``$DATA_ROOT/lazar_et_al_2025/lazar_sc_heart_dev.h5ad`` (73 k cells;
    var_names = bare ENSG IDs, obs has ``cell_type`` and ``age_pcw`` columns).
    ``use_h5ad_index=True`` because var_names are already ENSG IDs.
    Output: ``tokenized/lazar_hl_heart_dev.dataset``

Usage
-----
  # tokenize everything that's ready (CXG + Xu + Lázár)
  python tokenize_heart_dev_sources.py

  # specify only one source
  python tokenize_heart_dev_sources.py --sources cxg

  # override data root
  python tokenize_heart_dev_sources.py --data-root /path/to/data_root

  # specify custom token dictionary
  python tokenize_heart_dev_sources.py --token-dict /path/to/token_dictionary.pkl

Notes
-----
* The TranscriptomeTokenizer stores ``time_column`` as "time" in the output
  dataset.  Both CXG and Xu use ``time_column=<stage_obs_col>`` so that the
  developmental-stage string is available as "time" for the prepare step's
  ``parse_pcw`` function.
* ``model_input_size=16384`` — MaxToki uses the same extended context as
  Geneformer 95M.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import numpy as np


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_DATA_ROOT = Path(
    "/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data"
)

_TOKEN_DICT = Path(
    "/gladstone/theodoris/lab/enockniyonkuru/maxtoki_brain_aging_data"
    "/data/token_dictionary_aging_gc95M.pkl"
)

_XU_H5AD = Path(
    "/gladstone/theodoris/lab/dwen/data/organogenesis_data"
    "/organogenesis/organogenesis_processed.h5ad"
)

_LAZAR_H5AD = Path(
    "/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data"
    "/lazar_et_al_2025/lazar_sc_heart_dev.h5ad"
)

# The 5 CellxGene datasets covered by the data survey report (file-name prefixes).
# Files 02 (1M-cells subset) and 06-09 (Rotem 12w batches) are excluded — they
# are not part of the curated 5-dataset panel.
_CXG_INCLUDE_PREFIXES = (
    "01_",   # Han et al. 2020 — Human Cell Landscape
    "03_",   # Cao et al. 2020 — Survey of Human Embryonic Development (4M cells)
    "04_",   # Sim et al. 2021 — Sex-Specific Control of Heart Maturation
    "05_",   # Knight-Schrijver et al. 2022 — Integrated Adult and Foetal Hearts
    "10_",   # Leshem et al. 2025 — snRNA-seq OFT & Aortic Valve
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_tokenizer(custom_attr_name_dict, time_column, nproc, model_input_size,
                    use_h5ad_index, token_dict, time_group_column=None):
    """Import and instantiate TranscriptomeTokenizer."""
    try:
        from maxtoki.tokenizer import TranscriptomeTokenizer
    except ImportError as exc:
        sys.exit(
            f"Cannot import maxtoki: {exc}\n"
            "Install it into your conda environment:\n"
            "  pip install /path/to/maxtoki_brain_aging/MaxToki/"
        )
    return TranscriptomeTokenizer(
        custom_attr_name_dict=custom_attr_name_dict,
        time_column=time_column,
        time_group_column=time_group_column,
        nproc=nproc,
        model_input_size=model_input_size,
        use_h5ad_index=use_h5ad_index,
        token_dictionary_file=token_dict,
    )


def _prepare_output_dir(output_dir: Path, prefix: str, overwrite: bool) -> None:
    """Remove existing dataset at output_dir/prefix.dataset if overwrite=True."""
    target = output_dir / f"{prefix}.dataset"
    if target.exists():
        if not overwrite:
            raise FileExistsError(
                f"{target} already exists. Pass --overwrite to replace it."
            )
        print(f"  Removing existing dataset: {target}")
        shutil.rmtree(target)


# ---------------------------------------------------------------------------
# Source-specific tokenization functions
# ---------------------------------------------------------------------------

def _ensure_n_counts(h5ad_path: Path, out_dir: Path) -> Path:
    """Return a path to an h5ad guaranteed to have obs['n_counts'].

    If the file already has n_counts, symlinks it into out_dir (fast).
    Otherwise loads it, computes n_counts from X (or nCount_RNA), writes
    a new h5ad into out_dir, and returns that path.
    """
    import anndata as ad
    import scipy.sparse as sp

    adata = ad.read_h5ad(h5ad_path, backed="r")
    needs_ncounts = "n_counts" not in adata.obs.columns
    needs_cell_id = "unique_cell_id" not in adata.obs.columns

    if not needs_ncounts and not needs_cell_id:
        dest = out_dir / h5ad_path.name
        if not dest.exists():
            dest.symlink_to(h5ad_path)
        return dest

    # Need to add one or more columns — load fully into memory
    print(f"    Preprocessing {h5ad_path.name} (n_counts={needs_ncounts}, unique_cell_id={needs_cell_id}) ...")
    adata = ad.read_h5ad(h5ad_path)  # not backed

    if needs_ncounts:
        if "nCount_RNA" in adata.obs.columns:
            adata.obs["n_counts"] = adata.obs["nCount_RNA"].values.astype(float)
        else:
            X = adata.X
            if sp.issparse(X):
                n_counts = np.asarray(X.sum(axis=1)).flatten()
            else:
                n_counts = X.sum(axis=1)
            adata.obs["n_counts"] = n_counts.astype(float)

    if needs_cell_id:
        adata.obs["unique_cell_id"] = adata.obs.index.astype(str)

    dest = out_dir / h5ad_path.name
    adata.write_h5ad(dest)
    return dest


def tokenize_cxg(data_root: Path, output_dir: Path, token_dict: Path,
                 nproc: int, model_input_size: int, overwrite: bool) -> None:
    """Tokenize the 14 CXG heart-development h5ads."""
    source_dir = data_root / "source_1_cellxgene_heart_development_subset"
    if not source_dir.exists():
        sys.exit(f"CXG source directory not found: {source_dir}")

    h5ads = sorted(source_dir.glob("*.h5ad"))
    if not h5ads:
        sys.exit(f"No .h5ad files found in {source_dir}")
    print(f"CXG: found {len(h5ads)} h5ad file(s) in {source_dir}")

    prefix = "cxg_heart_dev"
    _prepare_output_dir(output_dir, prefix, overwrite)

    tok = _make_tokenizer(
        custom_attr_name_dict={"cell_type": "cell_type"},
        time_column="development_stage",   # stored as "time" in output dataset
        nproc=nproc,
        model_input_size=model_input_size,
        use_h5ad_index=True,               # CXG var.index = Ensembl IDs
        token_dict=token_dict,
    )
    print(f"CXG: tokenizing {len(h5ads)} h5ad(s) → {output_dir}/{prefix}.dataset ...")

    # Ensure all h5ads have obs['n_counts'] and obs['unique_cell_id'].
    # Use a staging dir on the same filesystem as the data (not /tmp) to
    # avoid cross-device copies and /tmp space limits.
    prep_dir = output_dir / "_cxg_prep"
    prep_dir.mkdir(parents=True, exist_ok=True)
    try:
        print("  Preprocessing h5ads (adding missing obs columns) ...")
        for h5ad in h5ads:
            _ensure_n_counts(h5ad, prep_dir)
        tok.tokenize_data(
            data_directory=str(prep_dir),
            output_directory=str(output_dir),
            output_prefix=prefix,
            file_format="h5ad",
        )
    finally:
        shutil.rmtree(prep_dir, ignore_errors=True)
    print(f"CXG: done → {output_dir}/{prefix}.dataset")


def tokenize_xu(data_root: Path, output_dir: Path, token_dict: Path,
                nproc: int, model_input_size: int, overwrite: bool,
                xu_h5ad: Path) -> None:
    """Tokenize the Xu et al. 2024 organogenesis h5ad.

    The h5ad contains cells from multiple organs; non-cardiac cells will be
    discarded by the downstream prepare step via the harmonization map.
    ``var`` has an ``ensembl_id`` column → use_h5ad_index=False (default).
    """
    if not xu_h5ad.exists():
        print(
            f"  [SKIP] Xu: h5ad not found at {xu_h5ad}. "
            "Check the path with --xu-h5ad."
        )
        return

    prefix = "xu_heart_dev"
    _prepare_output_dir(output_dir, prefix, overwrite)

    print(
        f"Xu: tokenizing {xu_h5ad.name} ({xu_h5ad.stat().st_size / 1e9:.1f} GB) "
        f"→ {output_dir}/{prefix}.dataset ..."
    )
    tok = _make_tokenizer(
        custom_attr_name_dict={"annotation": "cell_type"},
        time_column="stage",           # "CS12", "CS13-14", … → stored as "time"
        nproc=nproc,
        model_input_size=model_input_size,
        use_h5ad_index=False,          # var has ensembl_id column
        token_dict=token_dict,
    )
    # Use a staging dir on the same filesystem as output to avoid /tmp
    # size limits (Xu h5ad can be several GB).
    prep_dir = output_dir / "_xu_prep"
    prep_dir.mkdir(parents=True, exist_ok=True)
    try:
        _ensure_n_counts(xu_h5ad, prep_dir)
        tok.tokenize_data(
            data_directory=str(prep_dir),
            output_directory=str(output_dir),
            output_prefix=prefix,
            file_format="h5ad",
        )
    finally:
        shutil.rmtree(prep_dir, ignore_errors=True)
    print(f"Xu: done → {output_dir}/{prefix}.dataset")


def tokenize_lazar(data_root: Path, output_dir: Path, token_dict: Path,
                   nproc: int, model_input_size: int, overwrite: bool,
                   lazar_h5ad: Path) -> None:
    """Tokenize the Lázár et al. 2025 HDCA SC h5ad.

    The h5ad was converted from the original shoji h5 files via
    scripts/convert_lazar_to_h5ad.py.  Its var_names are bare ENSG IDs
    (no version suffix) → use_h5ad_index=True.
    obs columns: ``cell_type`` (canonical/alias name), ``age_pcw`` (float PCW).
    Output: ``tokenized/lazar_hl_heart_dev.dataset``
    """
    if not lazar_h5ad.exists():
        print(
            f"  [SKIP] Lázár: h5ad not found at {lazar_h5ad}. "
            "Run scripts/convert_lazar_to_h5ad.py first."
        )
        return

    prefix = "lazar_hl_heart_dev"
    _prepare_output_dir(output_dir, prefix, overwrite)

    print(
        f"Lázár: tokenizing {lazar_h5ad.name} "
        f"({lazar_h5ad.stat().st_size / 1e9:.1f} GB) "
        f"→ {output_dir}/{prefix}.dataset ..."
    )
    tok = _make_tokenizer(
        custom_attr_name_dict={"cell_type": "cell_type"},
        time_column="age_pcw",       # numeric float PCW → stored as "time"
        nproc=nproc,
        model_input_size=model_input_size,
        use_h5ad_index=True,         # var_names are bare ENSG IDs
        token_dict=token_dict,
    )
    prep_dir = output_dir / "_lazar_prep"
    prep_dir.mkdir(parents=True, exist_ok=True)
    try:
        _ensure_n_counts(lazar_h5ad, prep_dir)
        tok.tokenize_data(
            data_directory=str(prep_dir),
            output_directory=str(output_dir),
            output_prefix=prefix,
            file_format="h5ad",
        )
    finally:
        shutil.rmtree(prep_dir, ignore_errors=True)
    print(f"Lázár: done → {output_dir}/{prefix}.dataset")

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Tokenize heart-dev source h5ads into HuggingFace .dataset format "
            "for the MaxToki finetuning pipeline."
        )
    )
    parser.add_argument(
        "--data-root", type=Path, default=_DATA_ROOT,
        help="Base data directory (default: %(default)s).",
    )
    parser.add_argument(
        "--output-dir", type=Path, default=None,
        help=(
            "Output directory for tokenized datasets "
            "(default: DATA_ROOT/tokenized/)."
        ),
    )
    parser.add_argument(
        "--token-dict", type=Path, default=_TOKEN_DICT,
        help="Path to the MaxToki token dictionary pickle (default: %(default)s).",
    )
    parser.add_argument(
        "--xu-h5ad", type=Path, default=_XU_H5AD,
        help="Path to organogenesis_processed.h5ad for the Xu source.",
    )
    parser.add_argument(
        "--lazar-h5ad", type=Path, default=_LAZAR_H5AD,
        help="Path to lazar_sc_heart_dev.h5ad for the Lázár source.",
    )
    parser.add_argument(
        "--sources", nargs="+", choices=["cxg", "xu", "lazar"],
        default=["cxg", "xu", "lazar"],
        help="Which sources to tokenize (default: cxg xu).",
    )
    parser.add_argument(
        "--nproc", type=int, default=16,
        help="Number of parallel processes for the tokenizer (default: 16).",
    )
    parser.add_argument(
        "--model-input-size", type=int, default=16384,
        help="MaxToki model input size / max token sequence length (default: 16384).",
    )
    parser.add_argument(
        "--overwrite", action="store_true",
        help="Overwrite existing output datasets.",
    )
    args = parser.parse_args()

    data_root = args.data_root.resolve()
    output_dir = (args.output_dir or (data_root / "tokenized")).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    if not args.token_dict.exists():
        sys.exit(f"Token dictionary not found: {args.token_dict}")

    print(f"Data root  : {data_root}")
    print(f"Output dir : {output_dir}")
    print(f"Token dict : {args.token_dict}")
    print(f"Sources    : {args.sources}")
    print(f"nproc      : {args.nproc}")
    print(f"Model size : {args.model_input_size}")
    print()

    if "cxg" in args.sources:
        tokenize_cxg(
            data_root=data_root,
            output_dir=output_dir,
            token_dict=args.token_dict,
            nproc=args.nproc,
            model_input_size=args.model_input_size,
            overwrite=args.overwrite,
        )

    if "xu" in args.sources:
        tokenize_xu(
            data_root=data_root,
            output_dir=output_dir,
            token_dict=args.token_dict,
            nproc=args.nproc,
            model_input_size=args.model_input_size,
            overwrite=args.overwrite,
            xu_h5ad=args.xu_h5ad,
        )

    if "lazar" in args.sources:
        tokenize_lazar(
            data_root=data_root,
            output_dir=output_dir,
            token_dict=args.token_dict,
            nproc=args.nproc,
            model_input_size=args.model_input_size,
            overwrite=args.overwrite,
            lazar_h5ad=args.lazar_h5ad,
        )

    print("\nTokenization complete.")
    print("Next steps:")
    print("  1. Run prepare_heart_dev_finetune_data.py to harmonize and split datasets.")
    print("  2. Run build_heart_dev_trajectories.py to assemble MaxToki trajectories.")
    print("  3. Run finetune_heart_dev.py to start fine-tuning.")


if __name__ == "__main__":
    main()
