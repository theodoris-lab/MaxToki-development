#!/usr/bin/env python3
"""Convert non-CellxGene Maxtoki datasets into AnnData H5AD files.

Original files are left untouched. Outputs are written under:
  /gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data/source_2_3_4_h5ad_converted

For huge Matrix Market and TSV expression matrices, this writes sparse H5AD
layout directly with h5py. That keeps cells on the AnnData obs axis without
requiring the full matrix in memory.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import os
import shutil
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

import anndata as ad
import h5py
import numpy as np


DATA_DIR = Path("/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data")
OUTPUT_DIR = DATA_DIR / "source_2_3_4_h5ad_converted"
PYTHON = "/gladstone/theodoris/home/eniyonkuru/miniconda3/envs/env_maxtoki/bin/python"
MANIFEST_NAME = "conversion_manifest.tsv"
TMP_SUFFIX = ".tmp"
APPEND_CHUNK = 1_000_000
WRITE_CHUNK = 1_000_000


@dataclass(frozen=True)
class Dataset:
    dataset_id: str
    source_group: str
    name: str
    input_path: Path
    output_rel: Path
    converter: str
    storage: str = ""


DATASETS = [
    Dataset(
        "source2_hca_raw_counts",
        "Human Early Embryogenesis Atlas",
        "GSE157329 raw counts",
        DATA_DIR / "source_2_human_early_embryogenesis_atlas/93a9e248-b704-419f-b5ab-a0b96eefeaa0/GSE157329_raw_counts.mtx.gz",
        Path("source_2_human_early_embryogenesis_atlas/GSE157329_raw_counts.h5ad"),
        "mtx",
        "csr_by_original_column",
    ),
    Dataset(
        "source3_ucsc_in_vitro_expr",
        "UCSC Cells",
        "Human cardiogenesis in vitro expression matrix",
        DATA_DIR / "source_3_ucsc_cells/01_human_cardiogenesis_in_vitro_exprMatrix.tsv.gz",
        Path("source_3_ucsc_cells/01_human_cardiogenesis_in_vitro_exprMatrix.h5ad"),
        "tsv",
        "csc_by_gene_row",
    ),
    Dataset(
        "source3_ucsc_in_vivo_expr",
        "UCSC Cells",
        "Human cardiogenesis in vivo expression matrix",
        DATA_DIR / "source_3_ucsc_cells/02_human_cardiogenesis_in_vivo_exprMatrix.tsv.gz",
        Path("source_3_ucsc_cells/02_human_cardiogenesis_in_vivo_exprMatrix.h5ad"),
        "tsv",
        "csc_by_gene_row",
    ),
    Dataset(
        "source3_ucsc_multiomic_snrna",
        "UCSC Cells",
        "Multiomic human heart snRNA-seq matrix",
        DATA_DIR / "source_3_ucsc_cells/03_multiomic_human_heart_snrna_seq_matrix.mtx.gz",
        Path("source_3_ucsc_cells/03_multiomic_human_heart_snrna_seq_matrix.h5ad"),
        "mtx",
        "csc_by_original_row",
    ),
    Dataset(
        "source3_ucsc_multiomic_snatac",
        "UCSC Cells",
        "Multiomic human heart snATAC-seq matrix",
        DATA_DIR / "source_3_ucsc_cells/04_multiomic_human_heart_snatac_seq_matrix.mtx.gz",
        Path("source_3_ucsc_cells/04_multiomic_human_heart_snatac_seq_matrix.h5ad"),
        "mtx",
        "csc_by_original_row",
    ),
    Dataset(
        "source3_ucsc_heart_of_cells_expr",
        "UCSC Cells",
        "Heart of Cells overall heart scRNA-seq expression matrix",
        DATA_DIR / "source_3_ucsc_cells/05_heart_of_cells_overall_heart_scrna_seq_exprMatrix.tsv.gz",
        Path("source_3_ucsc_cells/05_heart_of_cells_overall_heart_scrna_seq_exprMatrix.h5ad"),
        "tsv",
        "csc_by_gene_row",
    ),
    Dataset(
        "source4_fetal_cre",
        "Lab Directory",
        "Human fetal cis-regulatory elements",
        DATA_DIR / "source_4_lab_directory/01_human_fetal_cis_regulatory_elements.loom",
        Path("source_4_lab_directory/01_human_fetal_cis_regulatory_elements.h5ad"),
        "loom",
    ),
    Dataset(
        "source4_fetal_striatum",
        "Lab Directory",
        "Human fetal striatum atlas",
        DATA_DIR / "source_4_lab_directory/02_human_fetal_striatum_atlas.loom",
        Path("source_4_lab_directory/02_human_fetal_striatum_atlas.h5ad"),
        "loom",
    ),
    Dataset(
        "source4_megakaryocyte_ys",
        "Lab Directory",
        "Human megakaryocyte development: yolk-sac stage",
        DATA_DIR / "source_4_lab_directory/03_human_megakaryocyte_development/GSE144024_YS_Stage_gene.loom",
        Path("source_4_lab_directory/03_human_megakaryocyte_development/GSE144024_YS_Stage_gene.h5ad"),
        "loom",
    ),
    Dataset(
        "source4_megakaryocyte_hesc_day0",
        "Lab Directory",
        "Human megakaryocyte development: hESC Day 0",
        DATA_DIR / "source_4_lab_directory/03_human_megakaryocyte_development/GSE144024_hESC_Day0_gene.loom",
        Path("source_4_lab_directory/03_human_megakaryocyte_development/GSE144024_hESC_Day0_gene.h5ad"),
        "loom",
    ),
    Dataset(
        "source4_epicardium",
        "Lab Directory",
        "Fetal vs. adult human epicardium",
        DATA_DIR / "source_4_lab_directory/04_fetal_vs_adult_human_epicardium.loom",
        Path("source_4_lab_directory/04_fetal_vs_adult_human_epicardium.h5ad"),
        "loom",
    ),
    Dataset(
        "source4_tyser_gastrulation",
        "Lab Directory",
        "Tyser et al. 2021 gastrulation atlas",
        DATA_DIR / "source_4_lab_directory/05_tyser_2021_gastrulation_atlas/E-MTAB-9388.loom",
        Path("source_4_lab_directory/05_tyser_2021_gastrulation_atlas/E-MTAB-9388.h5ad"),
        "loom",
    ),
    Dataset(
        "source4_xu_organogenesis",
        "Lab Directory",
        "Xu et al. 2023 organogenesis atlas (cardiac subset)",
        DATA_DIR / "source_4_lab_directory/06_xu_2023_organogenesis_atlas/organogenesis_processed_orgcell.loom",
        Path("source_4_lab_directory/06_xu_2023_organogenesis_atlas/xu_2023_organogenesis_cardiac.h5ad"),
        "loom",
    ),
]


def h5_string_dtype():
    return h5py.string_dtype(encoding="utf-8")


def set_encoding(obj, encoding_type: str, encoding_version: str) -> None:
    obj.attrs["encoding-type"] = encoding_type
    obj.attrs["encoding-version"] = encoding_version


def create_string_dataset(group: h5py.Group, name: str, values: Iterable[str], compression: str | None = "gzip") -> h5py.Dataset:
    data = np.asarray([str(value) for value in values], dtype=object)
    ds = group.create_dataset(
        name,
        data=data,
        dtype=h5_string_dtype(),
        chunks=True if len(data) else None,
        compression=compression if len(data) else None,
    )
    set_encoding(ds, "string-array", "0.2.0")
    return ds


def create_array_dataset(group: h5py.Group, name: str, values: np.ndarray, compression: str | None = "gzip") -> h5py.Dataset:
    ds = group.create_dataset(name, data=values, chunks=True, compression=compression)
    set_encoding(ds, "array", "0.2.0")
    return ds


def write_dataframe_group(parent: h5py.File, name: str, index_values: Iterable[str], columns: dict[str, Iterable[object]] | None = None) -> None:
    columns = columns or {}
    group = parent.create_group(name)
    set_encoding(group, "dataframe", "0.2.0")
    group.attrs["_index"] = "_index"
    group.attrs.create("column-order", np.asarray(list(columns.keys()), dtype=object), dtype=h5_string_dtype())
    create_string_dataset(group, "_index", index_values)
    for col_name, values in columns.items():
        arr = np.asarray(list(values))
        if arr.dtype.kind in {"i", "u", "f", "b"}:
            create_array_dataset(group, col_name, arr)
        else:
            create_string_dataset(group, col_name, ["" if value is None else str(value) for value in arr.tolist()])


def write_empty_dict_groups(parent: h5py.File) -> None:
    for name in ["layers", "obsm", "obsp", "uns", "varm", "varp"]:
        group = parent.create_group(name)
        set_encoding(group, "dict", "0.1.0")


def create_h5ad_base(output_path: Path, n_obs: int, n_vars: int, obs_names: Iterable[str], var_names: Iterable[str], var_columns: dict[str, Iterable[object]] | None = None) -> h5py.File:
    handle = h5py.File(output_path, "w")
    set_encoding(handle, "anndata", "0.1.0")
    write_dataframe_group(handle, "obs", obs_names)
    write_dataframe_group(handle, "var", var_names, var_columns)
    write_empty_dict_groups(handle)
    return handle


class ResizableArrayWriter:
    def __init__(self, group: h5py.Group, name: str, dtype: np.dtype, compression: str = "gzip"):
        self.size = 0
        self.capacity = APPEND_CHUNK
        self.ds = group.create_dataset(
            name,
            shape=(self.capacity,),
            maxshape=(None,),
            dtype=dtype,
            chunks=(APPEND_CHUNK,),
            compression=compression,
        )

    def append(self, values: np.ndarray) -> None:
        if values.size == 0:
            return
        needed = self.size + values.size
        if needed > self.capacity:
            while self.capacity < needed:
                self.capacity *= 2
            self.ds.resize((self.capacity,))
        self.ds[self.size : self.size + values.size] = values
        self.size += values.size

    def finish(self) -> None:
        self.ds.resize((self.size,))


def matrix_market_header(path: Path) -> tuple[str, int, int, int]:
    header = ""
    with gzip.open(path, "rt", errors="replace") as handle:
        first = handle.readline().strip()
        header = first
        for line in handle:
            line = line.strip()
            if not line or line.startswith("%"):
                continue
            n_rows, n_cols, nnz = map(int, line.split()[:3])
            return header, n_rows, n_cols, nnz
    raise ValueError(f"Could not find Matrix Market dimensions in {path}")


def iter_matrix_market_entries(path: Path):
    with gzip.open(path, "rt", errors="replace") as handle:
        dims_seen = False
        for line in handle:
            if not line.strip() or line.startswith("%"):
                continue
            if not dims_seen:
                dims_seen = True
                continue
            parts = line.split()
            if len(parts) < 3:
                continue
            yield int(parts[0]) - 1, int(parts[1]) - 1, float(parts[2])


def write_mtx_h5ad(dataset: Dataset, output_path: Path) -> dict[str, object]:
    _, n_features, n_cells, nnz = matrix_market_header(dataset.input_path)
    n_obs, n_vars = n_cells, n_features
    obs_names = (f"cell_{i + 1:09d}" for i in range(n_obs))
    var_names = (f"feature_{i + 1:09d}" for i in range(n_vars))

    tmp_path = output_path.with_suffix(output_path.suffix + TMP_SUFFIX)
    if tmp_path.exists():
        tmp_path.unlink()
    with create_h5ad_base(tmp_path, n_obs, n_vars, obs_names, var_names) as handle:
        data_chunks = (min(WRITE_CHUNK, max(1, nnz)),)
        if dataset.storage == "csr_by_original_column":
            x_group = handle.create_group("X")
            set_encoding(x_group, "csr_matrix", "0.1.0")
            x_group.attrs["shape"] = np.asarray([n_obs, n_vars], dtype=np.int64)
            data_ds = x_group.create_dataset("data", shape=(nnz,), dtype=np.float32, chunks=data_chunks, compression="gzip")
            indices_ds = x_group.create_dataset("indices", shape=(nnz,), dtype=np.int32, chunks=data_chunks, compression="gzip")
            indptr = np.zeros(n_obs + 1, dtype=np.int64)
            current_row = 0
            position = 0
            data_buf = np.empty(WRITE_CHUNK, dtype=np.float32)
            indices_buf = np.empty(WRITE_CHUNK, dtype=np.int32)
            buf_n = 0
            for feature_i, cell_i, value in iter_matrix_market_entries(dataset.input_path):
                if cell_i < current_row:
                    raise ValueError(f"{dataset.input_path} is not sorted by original column; cannot stream as CSR")
                while current_row < cell_i:
                    indptr[current_row + 1] = position
                    current_row += 1
                data_buf[buf_n] = value
                indices_buf[buf_n] = feature_i
                buf_n += 1
                position += 1
                if buf_n == WRITE_CHUNK:
                    start = position - buf_n
                    data_ds[start:position] = data_buf
                    indices_ds[start:position] = indices_buf
                    buf_n = 0
            if buf_n:
                start = position - buf_n
                data_ds[start:position] = data_buf[:buf_n]
                indices_ds[start:position] = indices_buf[:buf_n]
            while current_row < n_obs:
                indptr[current_row + 1] = position
                current_row += 1
            x_group.create_dataset("indptr", data=indptr, chunks=True, compression="gzip")
        elif dataset.storage == "csc_by_original_row":
            x_group = handle.create_group("X")
            set_encoding(x_group, "csc_matrix", "0.1.0")
            x_group.attrs["shape"] = np.asarray([n_obs, n_vars], dtype=np.int64)
            data_ds = x_group.create_dataset("data", shape=(nnz,), dtype=np.float32, chunks=data_chunks, compression="gzip")
            indices_ds = x_group.create_dataset("indices", shape=(nnz,), dtype=np.int32, chunks=data_chunks, compression="gzip")
            indptr = np.zeros(n_vars + 1, dtype=np.int64)
            current_col = 0
            position = 0
            data_buf = np.empty(WRITE_CHUNK, dtype=np.float32)
            indices_buf = np.empty(WRITE_CHUNK, dtype=np.int32)
            buf_n = 0
            for feature_i, cell_i, value in iter_matrix_market_entries(dataset.input_path):
                if feature_i < current_col:
                    raise ValueError(f"{dataset.input_path} is not sorted by original row; cannot stream as CSC")
                while current_col < feature_i:
                    indptr[current_col + 1] = position
                    current_col += 1
                data_buf[buf_n] = value
                indices_buf[buf_n] = cell_i
                buf_n += 1
                position += 1
                if buf_n == WRITE_CHUNK:
                    start = position - buf_n
                    data_ds[start:position] = data_buf
                    indices_ds[start:position] = indices_buf
                    buf_n = 0
            if buf_n:
                start = position - buf_n
                data_ds[start:position] = data_buf[:buf_n]
                indices_ds[start:position] = indices_buf[:buf_n]
            while current_col < n_vars:
                indptr[current_col + 1] = position
                current_col += 1
            x_group.create_dataset("indptr", data=indptr, chunks=True, compression="gzip")
        else:
            raise ValueError(f"Unsupported MTX storage mode: {dataset.storage}")
    tmp_path.rename(output_path)
    return {"n_obs": n_obs, "n_vars": n_vars, "nnz": nnz, "storage": dataset.storage}


def parse_float_values(values: list[str]) -> tuple[np.ndarray, np.ndarray]:
    indices = []
    data = []
    for idx, text in enumerate(values):
        if text in {"", "0", "0.0", "0.00", "0.000"}:
            continue
        value = float(text)
        if value != 0.0:
            indices.append(idx)
            data.append(value)
    return np.asarray(indices, dtype=np.int32), np.asarray(data, dtype=np.float32)


def tsv_dimensions_and_names(path: Path) -> tuple[list[str], list[str]]:
    genes = []
    with gzip.open(path, "rt", errors="replace", newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        header = next(reader)
        first_col = header[0].strip().lower() if header else ""
        has_feature_col = first_col in {"", "gene", "genes", "feature", "features", "gene_id", "gene_name"}
        cell_names = header[1:] if has_feature_col else header
        for i, row in enumerate(reader, start=1):
            gene = row[0] if has_feature_col and row else f"feature_{i:09d}"
            genes.append(gene or f"feature_{i:09d}")
    return cell_names, genes


def write_tsv_h5ad(dataset: Dataset, output_path: Path) -> dict[str, object]:
    cell_names, gene_names = tsv_dimensions_and_names(dataset.input_path)
    n_obs = len(cell_names)
    n_vars = len(gene_names)
    tmp_path = output_path.with_suffix(output_path.suffix + TMP_SUFFIX)
    if tmp_path.exists():
        tmp_path.unlink()
    with create_h5ad_base(tmp_path, n_obs, n_vars, cell_names, gene_names) as handle:
        x_group = handle.create_group("X")
        set_encoding(x_group, "csc_matrix", "0.1.0")
        x_group.attrs["shape"] = np.asarray([n_obs, n_vars], dtype=np.int64)
        data_writer = ResizableArrayWriter(x_group, "data", np.dtype("float32"))
        indices_writer = ResizableArrayWriter(x_group, "indices", np.dtype("int32"))
        indptr = np.zeros(n_vars + 1, dtype=np.int64)
        nnz = 0
        with gzip.open(dataset.input_path, "rt", errors="replace", newline="") as handle_in:
            reader = csv.reader(handle_in, delimiter="\t")
            header = next(reader)
            first_col = header[0].strip().lower() if header else ""
            has_feature_col = first_col in {"", "gene", "genes", "feature", "features", "gene_id", "gene_name"}
            for gene_i, row in enumerate(reader):
                values = row[1:] if has_feature_col else row
                indices, data = parse_float_values(values)
                indices_writer.append(indices)
                data_writer.append(data)
                nnz += int(data.size)
                indptr[gene_i + 1] = nnz
        data_writer.finish()
        indices_writer.finish()
        x_group.create_dataset("indptr", data=indptr, chunks=True, compression="gzip")
    tmp_path.rename(output_path)
    return {"n_obs": n_obs, "n_vars": n_vars, "nnz": nnz, "storage": "csc_by_gene_row"}


def pick_loom_names(path: Path) -> tuple[str, str]:
    with h5py.File(path, "r") as handle:
        col_attrs = set(handle["col_attrs"].keys())
        row_attrs = set(handle["row_attrs"].keys())
    obs_name = "cell_id" if "cell_id" in col_attrs else "unique_cell_id" if "unique_cell_id" in col_attrs else "CellID"
    var_name = "gene_name" if "gene_name" in row_attrs else "Gene" if "Gene" in row_attrs else "gene"
    return obs_name, var_name


def write_loom_h5ad(dataset: Dataset, output_path: Path) -> dict[str, object]:
    tmp_path = output_path.with_suffix(output_path.suffix + TMP_SUFFIX)
    if tmp_path.exists():
        tmp_path.unlink()
    obs_name, var_name = pick_loom_names(dataset.input_path)
    adata = ad.read_loom(dataset.input_path, sparse=True, obs_names=obs_name, var_names=var_name, dtype="float32")
    adata.obs_names_make_unique()
    adata.var_names_make_unique()
    adata.write_h5ad(tmp_path, compression="gzip")
    n_obs, n_vars = adata.n_obs, adata.n_vars
    nnz = int(adata.X.nnz) if hasattr(adata.X, "nnz") else None
    del adata
    tmp_path.rename(output_path)
    return {"n_obs": n_obs, "n_vars": n_vars, "nnz": nnz, "storage": "csr_from_loom"}


def validate_h5ad(path: Path) -> tuple[int, int]:
    adata = ad.read_h5ad(path, backed="r")
    try:
        return int(adata.n_obs), int(adata.n_vars)
    finally:
        adata.file.close()


def convert_dataset(dataset: Dataset, output_dir: Path, force: bool) -> dict[str, object]:
    output_path = output_dir / dataset.output_rel
    output_path.parent.mkdir(parents=True, exist_ok=True)
    start = time.time()
    if output_path.exists() and not force:
        n_obs, n_vars = validate_h5ad(output_path)
        return {
            "dataset_id": dataset.dataset_id,
            "status": "skipped_existing",
            "input_path": str(dataset.input_path),
            "output_path": str(output_path),
            "n_obs": n_obs,
            "n_vars": n_vars,
            "nnz": "",
            "storage": "existing",
            "seconds": 0,
            "size_bytes": output_path.stat().st_size,
            "message": "output already exists",
        }
    if output_path.exists() and force:
        output_path.unlink()

    if dataset.converter == "mtx":
        stats = write_mtx_h5ad(dataset, output_path)
    elif dataset.converter == "tsv":
        stats = write_tsv_h5ad(dataset, output_path)
    elif dataset.converter == "loom":
        stats = write_loom_h5ad(dataset, output_path)
    else:
        raise ValueError(f"Unknown converter: {dataset.converter}")

    n_obs, n_vars = validate_h5ad(output_path)
    elapsed = time.time() - start
    return {
        "dataset_id": dataset.dataset_id,
        "status": "written",
        "input_path": str(dataset.input_path),
        "output_path": str(output_path),
        "n_obs": n_obs,
        "n_vars": n_vars,
        "nnz": stats.get("nnz", ""),
        "storage": stats.get("storage", ""),
        "seconds": f"{elapsed:.1f}",
        "size_bytes": output_path.stat().st_size,
        "message": "",
    }


def append_manifest(output_dir: Path, row: dict[str, object]) -> None:
    manifest = output_dir / MANIFEST_NAME
    fieldnames = [
        "timestamp",
        "dataset_id",
        "status",
        "input_path",
        "output_path",
        "n_obs",
        "n_vars",
        "nnz",
        "storage",
        "seconds",
        "size_bytes",
        "message",
    ]
    exists = manifest.exists()
    with manifest.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        if not exists:
            writer.writeheader()
        writer.writerow({"timestamp": datetime.now().isoformat(timespec="seconds"), **row})


def selected_datasets(selectors: list[str]) -> list[Dataset]:
    if not selectors:
        return DATASETS
    selected = []
    wanted = set(selectors)
    for dataset in DATASETS:
        if dataset.dataset_id in wanted or dataset.converter in wanted or dataset.source_group in wanted:
            selected.append(dataset)
    missing = wanted - {d.dataset_id for d in selected} - {d.converter for d in selected} - {d.source_group for d in selected}
    if missing:
        raise SystemExit(f"Unknown --only selector(s): {', '.join(sorted(missing))}")
    return selected


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--only", action="append", default=[], help="Dataset id, converter type (mtx/tsv/loom), or source group to convert. May be repeated.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing H5AD outputs.")
    parser.add_argument("--list", action="store_true", help="List datasets and exit.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    datasets = selected_datasets(args.only)
    if args.list:
        for dataset in datasets:
            print(f"{dataset.dataset_id}\t{dataset.converter}\t{dataset.input_path}\t{args.output_dir / dataset.output_rel}")
        return

    args.output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {args.output_dir}", flush=True)
    print(f"Datasets selected: {len(datasets)}", flush=True)
    for idx, dataset in enumerate(datasets, start=1):
        print(f"[{idx}/{len(datasets)}] {dataset.dataset_id}: {dataset.name}", flush=True)
        try:
            row = convert_dataset(dataset, args.output_dir, force=args.force)
            print(f"  {row['status']} shape={row['n_obs']} x {row['n_vars']} size={row['size_bytes']} bytes", flush=True)
        except Exception as exc:
            row = {
                "dataset_id": dataset.dataset_id,
                "status": "failed",
                "input_path": str(dataset.input_path),
                "output_path": str(args.output_dir / dataset.output_rel),
                "n_obs": "",
                "n_vars": "",
                "nnz": "",
                "storage": dataset.storage,
                "seconds": "",
                "size_bytes": "",
                "message": repr(exc),
            }
            print(f"  FAILED: {exc!r}", flush=True)
            append_manifest(args.output_dir, row)
            raise
        append_manifest(args.output_dir, row)


if __name__ == "__main__":
    main()
