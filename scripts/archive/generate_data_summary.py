#!/usr/bin/env python3
"""Generate a lightweight summary report for Maxtoki development datasets.

This intentionally avoids importing pandas/anndata/h5py so it can run in the
minimal cluster shell environment. HDF5-backed files are inspected with h5ls and
h5dump; gzipped text files are streamed.
"""

from __future__ import annotations

import csv
import gzip
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Iterable


DATA_DIR = Path("/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data")
OUTFILE = Path("documents/maxtoki_development_data_summary.md")
HEAD_N = 5
MAX_PREVIEW_COLUMNS = 8
UNIQUE_VALUES_PER_LINE = 8


DATASETS = [
    ("CellxGene", "Construction of a human cell landscape at single-cell level", DATA_DIR / "source_1_cellxgene/01_construction_of_a_human_cell_landscape_at_single_cell_level.h5ad"),
    ("CellxGene", "Survey of human embryonic development (1 million cells subset)", DATA_DIR / "source_1_cellxgene/02_survey_of_human_embryonic_development_1_million_cells_subset.h5ad"),
    ("CellxGene", "Survey of human embryonic development", DATA_DIR / "source_1_cellxgene/03_survey_of_human_embryonic_development.h5ad"),
    ("CellxGene", "Sex-Specific Control of Human Heart Maturation by the Progesterone Receptor", DATA_DIR / "source_1_cellxgene/04_sex_specific_control_of_human_heart_maturation_by_the_progesterone_receptor.h5ad"),
    ("CellxGene", "Integrated adult and foetal hearts", DATA_DIR / "source_1_cellxgene/05_integrated_adult_and_foetal_hearts.h5ad"),
    ("CellxGene", "Rotem_12W_heart_C1", DATA_DIR / "source_1_cellxgene/06_rotem_12w_heart_c1.h5ad"),
    ("CellxGene", "Rotem_12W_heart_B1", DATA_DIR / "source_1_cellxgene/07_rotem_12w_heart_b1.h5ad"),
    ("CellxGene", "Rotem_12W_heart_D1", DATA_DIR / "source_1_cellxgene/08_rotem_12w_heart_d1.h5ad"),
    ("CellxGene", "Rotem_12W_heart_A1", DATA_DIR / "source_1_cellxgene/09_rotem_12w_heart_a1.h5ad"),
    ("CellxGene", "Single-nuclei RNA-seq of human outflow tract and aortic valve tissue", DATA_DIR / "source_1_cellxgene/10_single_nuclei_rna_seq_human_outflow_tract_aortic_valve.h5ad"),
    ("Human Early Embryogenesis Atlas", "GSE157329 raw counts", DATA_DIR / "source_2_human_early_embryogenesis_atlas/93a9e248-b704-419f-b5ab-a0b96eefeaa0/GSE157329_raw_counts.mtx.gz"),
    ("UCSC Cells", "Human cardiogenesis in vitro expression matrix", DATA_DIR / "source_3_ucsc_cells/01_human_cardiogenesis_in_vitro_exprMatrix.tsv.gz"),
    ("UCSC Cells", "Human cardiogenesis in vivo expression matrix", DATA_DIR / "source_3_ucsc_cells/02_human_cardiogenesis_in_vivo_exprMatrix.tsv.gz"),
    ("UCSC Cells", "Multiomic human heart snRNA-seq matrix", DATA_DIR / "source_3_ucsc_cells/03_multiomic_human_heart_snrna_seq_matrix.mtx.gz"),
    ("UCSC Cells", "Multiomic human heart snATAC-seq matrix", DATA_DIR / "source_3_ucsc_cells/04_multiomic_human_heart_snatac_seq_matrix.mtx.gz"),
    ("UCSC Cells", "Heart of Cells overall heart scRNA-seq expression matrix", DATA_DIR / "source_3_ucsc_cells/05_heart_of_cells_overall_heart_scrna_seq_exprMatrix.tsv.gz"),
    ("Lab Directory", "Human fetal cis-regulatory elements", DATA_DIR / "source_4_lab_directory/01_human_fetal_cis_regulatory_elements.loom"),
    ("Lab Directory", "Human fetal striatum atlas", DATA_DIR / "source_4_lab_directory/02_human_fetal_striatum_atlas.loom"),
    ("Lab Directory", "Human megakaryocyte development: yolk-sac stage", DATA_DIR / "source_4_lab_directory/03_human_megakaryocyte_development/GSE144024_YS_Stage_gene.loom"),
    ("Lab Directory", "Human megakaryocyte development: hESC Day 0", DATA_DIR / "source_4_lab_directory/03_human_megakaryocyte_development/GSE144024_hESC_Day0_gene.loom"),
    ("Lab Directory", "Fetal vs. adult human epicardium", DATA_DIR / "source_4_lab_directory/04_fetal_vs_adult_human_epicardium.loom"),
]


H5AD_PREVIEW_COLUMNS = [
    "cell_type",
    "tissue",
    "development_stage",
    "disease",
    "assay",
    "sex",
]

H5AD_INDEX_CANDIDATES = ["_index", "index"]

METADATA_FIELD_CANDIDATES = {
    "cell types": ["cell_type", "cell_subclass", "author_cell_type", "celltype", "cell_type_name"],
    "tissues": ["tissue", "tissue_general", "tissue_original", "organ", "organ_name"],
    "development stages": ["development_stage", "stage", "age", "donor_age"],
    "diseases": ["disease", "disease_state", "condition"],
}


def run_cmd(args: list[str], timeout: int | None = None) -> str:
    result = subprocess.run(
        args,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )
    if result.returncode != 0:
        raise RuntimeError(f"{' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def run_shell(command: str, timeout: int | None = None) -> str:
    result = subprocess.run(
        ["bash", "-lc", command],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )
    if result.returncode != 0:
        raise RuntimeError(f"{command} failed: {result.stderr.strip()}")
    return result.stdout


def format_bytes(num_bytes: int | None) -> str:
    if num_bytes is None:
        return "missing"
    value = float(num_bytes)
    units = ["B", "KiB", "MiB", "GiB", "TiB"]
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{int(value)}{unit}" if unit == "B" else f"{value:.1f}{unit}"
        value /= 1024
    return f"{num_bytes}B"


def md_escape(value: object) -> str:
    text = "" if value is None else str(value)
    text = text.replace("\\", "\\\\").replace("|", "\\|")
    text = text.replace("\n", "<br>")
    return text


def md_table(headers: list[str], rows: Iterable[Iterable[object]]) -> str:
    lines = [
        "| " + " | ".join(md_escape(h) for h in headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(v) for v in row) + " |")
    return "\n".join(lines)


def shape_from_h5ls_line(line: str) -> tuple[int, ...] | None:
    match = re.search(r"\{([^}]*)\}", line)
    if not match:
        return None
    dims = []
    for part in match.group(1).split(","):
        value = part.strip().split("/")[0].strip()
        if value == "SCALAR":
            return ()
        if value:
            try:
                dims.append(int(value))
            except ValueError:
                pass
    return tuple(dims) if dims else None


def parse_h5ls_children(output: str) -> list[dict[str, object]]:
    children = []
    for line in output.splitlines():
        match = re.match(r"^(.*?)\s{2,}(Dataset|Group)\s*(.*)$", line)
        if not match:
            continue
        name, kind, rest = match.groups()
        children.append(
            {
                "name": name.strip(),
                "kind": kind,
                "shape": shape_from_h5ls_line(rest),
                "raw": line,
            }
        )
    return children


def h5_children(path: Path, group: str) -> list[dict[str, object]]:
    return parse_h5ls_children(run_cmd(["h5ls", f"{path}{group}"]))


def h5_dataset_values(path: Path, dataset: str, count: int | None = HEAD_N, start: str = "0") -> list[str]:
    args = ["h5dump", "-A", "0", "-y", "-w", "0", "-d", dataset]
    if count is not None:
        args += ["-s", start, "-c", str(count)]
    args.append(str(path))
    output = run_cmd(args)
    if "DATA {" not in output:
        return []
    block = output.split("DATA {", 1)[1].split("\n      }", 1)[0]
    strings = re.findall(r'"((?:[^"\\]|\\.)*)"', block)
    if strings:
        return [s.encode("utf-8").decode("unicode_escape", errors="replace") for s in strings]
    nums = re.findall(r"[-+]?(?:\d+\.\d+|\d+)(?:[eE][-+]?\d+)?", block)
    return nums


def h5_dataset_matrix(path: Path, dataset: str, rows: int = HEAD_N, cols: int = HEAD_N) -> list[list[str]]:
    args = ["h5dump", "-A", "0", "-y", "-w", "0", "-d", dataset, "-s", "0,0", "-c", f"{rows},{cols}", str(path)]
    output = run_cmd(args)
    if "DATA {" not in output:
        return []
    block = output.split("DATA {", 1)[1].split("\n      }", 1)[0]
    nums = re.findall(r"[-+]?(?:\d+\.\d+|\d+)(?:[eE][-+]?\d+)?", block)
    return [nums[i : i + cols] for i in range(0, min(len(nums), rows * cols), cols)]


def h5_group_values(path: Path, base: str, count: int = HEAD_N) -> list[str]:
    children = {item["name"]: item for item in h5_children(path, base)}
    if "categories" in children and "codes" in children:
        categories = h5_dataset_values(path, f"{base}/categories", count=None)
        codes = h5_dataset_values(path, f"{base}/codes", count=count)
        values = []
        for code in codes:
            try:
                idx = int(float(code))
                values.append(categories[idx] if 0 <= idx < len(categories) else "")
            except ValueError:
                values.append(code)
        return values
    return []


def unique_preserve_order(values: Iterable[str]) -> list[str]:
    seen = set()
    unique_values = []
    for value in values:
        text = "" if value is None else str(value)
        if text == "" or text in seen:
            continue
        seen.add(text)
        unique_values.append(text)
    return unique_values


def h5_group_unique_values(path: Path, base: str) -> list[str]:
    children = {item["name"]: item for item in h5_children(path, base)}
    if "categories" in children:
        return unique_preserve_order(h5_dataset_values(path, f"{base}/categories", count=None))
    return []


def h5_unique_values_for_child(path: Path, base_group: str, child: dict[str, object]) -> list[str]:
    field = str(child["name"])
    dataset = f"{base_group}/{field}"
    if child["kind"] == "Group":
        return h5_group_unique_values(path, dataset)
    return unique_preserve_order(h5_dataset_values(path, dataset, count=None))


def h5_metadata_uniques(path: Path, base_group: str, children: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    child_by_name = {str(child["name"]): child for child in children}
    metadata: dict[str, dict[str, object]] = {}
    for label, candidates in METADATA_FIELD_CANDIDATES.items():
        found = None
        for candidate in candidates:
            if candidate in child_by_name:
                found = child_by_name[candidate]
                break
        if not found:
            metadata[label] = {"field": None, "values": []}
            continue
        try:
            values = h5_unique_values_for_child(path, base_group, found)
        except Exception as exc:
            values = [f"<error while reading {found['name']}: {exc}>"]
        metadata[label] = {"field": found["name"], "values": values}
    return metadata


def first_shape(children: list[dict[str, object]], exclude: set[str] | None = None) -> int | None:
    exclude = exclude or set()
    for child in children:
        if child["name"] in exclude:
            continue
        shape = child.get("shape")
        if child["kind"] == "Dataset" and isinstance(shape, tuple) and len(shape) >= 1:
            return int(shape[0])
    return None


def h5_child_by_name(children: list[dict[str, object]], names: list[str]) -> dict[str, object] | None:
    for name in names:
        child = next((c for c in children if c["name"] == name), None)
        if child:
            return child
    return None


def h5ad_summary(path: Path) -> dict[str, object]:
    obs_children = h5_children(path, "/obs")
    var_children = h5_children(path, "/var")
    x_children = h5_children(path, "/X")

    obs_names = [c["name"] for c in obs_children if c["name"] not in H5AD_INDEX_CANDIDATES]
    var_names = [c["name"] for c in var_children if c["name"] not in H5AD_INDEX_CANDIDATES]

    obs_index = h5_child_by_name(obs_children, H5AD_INDEX_CANDIDATES)
    var_index = h5_child_by_name(var_children, H5AD_INDEX_CANDIDATES)

    n_obs = None
    if obs_index and isinstance(obs_index.get("shape"), tuple) and obs_index["shape"]:
        n_obs = obs_index["shape"][0]
    n_obs = n_obs or first_shape(obs_children)

    n_vars = None
    if var_index and isinstance(var_index.get("shape"), tuple) and var_index["shape"]:
        n_vars = var_index["shape"][0]
    n_vars = n_vars or first_shape(var_children)

    nnz = first_shape(x_children, exclude={"indices", "indptr"})
    x_format = "sparse CSR-like HDF5 group" if x_children else "unknown"

    child_kind = {c["name"]: c["kind"] for c in obs_children}
    preview_index_name = str(obs_index["name"]) if obs_index else None
    preview_cols = (["_index"] if preview_index_name else []) + [c for c in H5AD_PREVIEW_COLUMNS if c in child_kind]
    col_values = {}
    for col in preview_cols:
        try:
            if col == "_index":
                col_values[col] = h5_dataset_values(path, f"/obs/{preview_index_name}", count=HEAD_N)
            elif child_kind.get(col) == "Dataset":
                col_values[col] = h5_dataset_values(path, f"/obs/{col}", count=HEAD_N)
            else:
                col_values[col] = h5_group_values(path, f"/obs/{col}", count=HEAD_N)
        except Exception as exc:
            col_values[col] = [f"<error: {exc}>"]

    rows = []
    for i in range(HEAD_N):
        rows.append([col_values.get(col, [""] * HEAD_N)[i] if i < len(col_values.get(col, [])) else "" for col in preview_cols])

    return {
        "kind": "AnnData H5AD",
        "dimensions": f"{n_obs:,} observations x {n_vars:,} variables" if n_obs and n_vars else "unknown",
        "rows": n_obs,
        "columns": n_vars,
        "unique_cells": n_obs,
        "unique_cells_note": "observation/cell axis count",
        "metadata_uniques": h5_metadata_uniques(path, "/obs", obs_children),
        "matrix_info": f"{x_format}; non-zero values: {nnz:,}" if nnz else x_format,
        "obs_columns": obs_names,
        "var_columns": var_names,
        "preview_headers": preview_cols,
        "preview_rows": rows,
    }


def loom_summary(path: Path) -> dict[str, object]:
    root_children = h5_children(path, "")
    matrix = next((c for c in root_children if c["name"] == "matrix"), None)
    shape = matrix.get("shape") if matrix else None
    n_genes = shape[0] if isinstance(shape, tuple) and len(shape) >= 2 else None
    n_cells = shape[1] if isinstance(shape, tuple) and len(shape) >= 2 else None

    row_attrs = [c["name"] for c in h5_children(path, "/row_attrs")]
    col_attrs = [c["name"] for c in h5_children(path, "/col_attrs")]
    cell_ids = []
    gene_names = []
    for candidate in ["cell_id", "CellID", "unique_cell_id"]:
        if candidate in col_attrs:
            cell_ids = h5_dataset_values(path, f"/col_attrs/{candidate}", count=HEAD_N)
            break
    for candidate in ["gene_name", "Gene", "gene", "ensembl_id"]:
        if candidate in row_attrs:
            gene_names = h5_dataset_values(path, f"/row_attrs/{candidate}", count=HEAD_N)
            break
    matrix_preview = h5_dataset_matrix(path, "/matrix", rows=HEAD_N, cols=HEAD_N)

    headers = ["gene"] + [f"cell_{i+1}" for i in range(HEAD_N)]
    if cell_ids:
        headers = ["gene"] + cell_ids[:HEAD_N]
    rows = []
    for i, values in enumerate(matrix_preview[:HEAD_N]):
        label = gene_names[i] if i < len(gene_names) else f"row_{i+1}"
        rows.append([label] + values[:HEAD_N])

    return {
        "kind": "Loom HDF5 matrix",
        "dimensions": f"{n_genes:,} genes/features x {n_cells:,} cells" if n_genes and n_cells else "unknown",
        "rows": n_genes,
        "columns": n_cells,
        "unique_cells": n_cells,
        "unique_cells_note": "cell axis count",
        "metadata_uniques": h5_metadata_uniques(path, "/col_attrs", h5_children(path, "/col_attrs")),
        "matrix_info": "Dense /matrix dataset in loom HDF5 file",
        "row_attrs": row_attrs,
        "col_attrs": col_attrs,
        "preview_headers": headers,
        "preview_rows": rows,
    }


def mtx_summary(path: Path) -> dict[str, object]:
    header = ""
    comments = []
    dims = None
    entries = []
    with gzip.open(path, "rt", errors="replace") as handle:
        header = handle.readline().strip()
        for line in handle:
            line = line.strip()
            if not line:
                continue
            if line.startswith("%"):
                if len(comments) < 3:
                    comments.append(line)
                continue
            dims = line
            break
        for line in handle:
            line = line.strip()
            if not line or line.startswith("%"):
                continue
            entries.append(line.split()[:3])
            if len(entries) >= HEAD_N:
                break
    n_rows = n_cols = nnz = None
    if dims:
        parts = dims.split()
        if len(parts) >= 3:
            n_rows, n_cols, nnz = map(int, parts[:3])
    return {
        "kind": "Matrix Market sparse coordinate matrix",
        "dimensions": f"{n_rows:,} rows x {n_cols:,} columns" if n_rows and n_cols else "unknown",
        "rows": n_rows,
        "columns": n_cols,
        "unique_cells": n_cols,
        "unique_cells_note": "matrix column count; metadata fields are not embedded in this Matrix Market file",
        "metadata_uniques": {},
        "matrix_info": f"{header}; non-zero entries: {nnz:,}" if nnz else header,
        "column_names": [],
        "preview_headers": ["row", "column", "value"],
        "preview_rows": entries,
    }


def infer_sample_dtype(values: list[str]) -> str:
    observed = [v for v in values if v not in ("", "NA", "NaN", "nan", "null", "None")]
    if not observed:
        return "empty/unknown"
    try:
        for value in observed:
            int(value)
        return "int-like"
    except ValueError:
        pass
    try:
        for value in observed:
            float(value)
        return "float-like"
    except ValueError:
        return "object/string-like"


def count_gzip_lines(path: Path) -> int:
    escaped = str(path).replace("'", "'\\''")
    output = run_shell(f"gzip -dc '{escaped}' | wc -l", timeout=None)
    return int(output.strip().split()[0])


def tsv_gz_summary(path: Path) -> dict[str, object]:
    with gzip.open(path, "rt", errors="replace", newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        header = next(reader)
        rows = []
        sample_by_col = [[] for _ in header[:MAX_PREVIEW_COLUMNS]]
        for row in reader:
            rows.append(row[:MAX_PREVIEW_COLUMNS])
            for i, value in enumerate(row[:MAX_PREVIEW_COLUMNS]):
                sample_by_col[i].append(value)
            if len(rows) >= HEAD_N:
                break

    total_lines = count_gzip_lines(path)
    n_rows = max(total_lines - 1, 0)
    n_cols = len(header)
    first_col = header[0].strip().lower() if header else ""
    has_feature_column = first_col in {"", "gene", "genes", "feature", "features", "gene_id", "gene_name"}
    cell_columns = n_cols - 1 if has_feature_column and n_cols > 0 else n_cols
    preview_headers = header[:MAX_PREVIEW_COLUMNS]
    if n_cols > MAX_PREVIEW_COLUMNS:
        preview_headers = preview_headers + [f"... {n_cols - MAX_PREVIEW_COLUMNS} more columns"]
        rows = [row + ["..."] for row in rows]

    dtype_rows = []
    for col, values in zip(header[:MAX_PREVIEW_COLUMNS], sample_by_col):
        dtype_rows.append([col, infer_sample_dtype(values)])

    return {
        "kind": "Gzipped tab-separated expression matrix",
        "dimensions": f"{n_rows:,} rows x {n_cols:,} columns",
        "rows": n_rows,
        "columns": n_cols,
        "unique_cells": cell_columns,
        "unique_cells_note": "cell/barcode columns in the expression matrix header",
        "metadata_uniques": {},
        "matrix_info": "Header row plus gene/feature rows; dtypes inferred from first five data rows",
        "column_names": header,
        "dtype_rows": dtype_rows,
        "preview_headers": preview_headers,
        "preview_rows": rows,
    }


def summarize_dataset(path: Path) -> dict[str, object]:
    suffixes = "".join(path.suffixes).lower()
    if suffixes.endswith(".h5ad"):
        return h5ad_summary(path)
    if suffixes.endswith(".loom"):
        return loom_summary(path)
    if suffixes.endswith(".mtx.gz"):
        return mtx_summary(path)
    if suffixes.endswith(".tsv.gz"):
        return tsv_gz_summary(path)
    raise ValueError(f"No summary handler for {path}")


def names_if_less_than_20(names: list[str]) -> str:
    if not names:
        return "not embedded or unavailable"
    if len(names) < 20:
        return ", ".join(f"`{name}`" for name in names)
    return f"not listed because count is {len(names):,} (>= 20)"


def format_count(value: object) -> str:
    return f"{value:,}" if isinstance(value, int) else str(value)


def append_unique_values(lines: list[str], values: list[str]) -> None:
    for start in range(0, len(values), UNIQUE_VALUES_PER_LINE):
        chunk = values[start : start + UNIQUE_VALUES_PER_LINE]
        lines.append("  - " + ", ".join(f"`{value}`" for value in chunk))


def write_metadata_section(lines: list[str], summary: dict[str, object]) -> None:
    lines.append("### Cell/tissue/stage/disease metadata")
    lines.append("")
    unique_cells = summary.get("unique_cells", "unknown")
    note = summary.get("unique_cells_note", "")
    note_text = f" ({note})" if note else ""
    lines.append(f"- Unique cells recorded: {format_count(unique_cells)}{note_text}")
    metadata = summary.get("metadata_uniques")
    if not metadata:
        lines.append("- Unique cell types: not embedded in this file")
        lines.append("- Unique tissues: not embedded in this file")
        lines.append("- Unique development stages: not embedded in this file")
        lines.append("- Unique diseases: not embedded in this file")
        lines.append("")
        return
    for label in ["cell types", "tissues", "development stages", "diseases"]:
        item = metadata.get(label, {}) if isinstance(metadata, dict) else {}
        field = item.get("field")
        values = item.get("values") or []
        if not field:
            lines.append(f"- Unique {label}: not embedded in this file")
            continue
        lines.append(f"- Unique {label}: {len(values):,} values from `{field}`")
        append_unique_values(lines, list(values))
    lines.append("")


def write_dataset_section(lines: list[str], idx: int, source: str, name: str, path: Path, summary: dict[str, object]) -> None:
    rel = path.relative_to(DATA_DIR)
    size = path.stat().st_size if path.exists() else None
    lines.append(f"## {idx}. {name}")
    lines.append("")
    lines.append(f"- Source group: `{source}`")
    lines.append(f"- File: `{rel}`")
    lines.append(f"- Size: {format_bytes(size)}")
    lines.append(f"- Data kind: {summary['kind']}")
    lines.append(f"- Dimension: {summary['dimensions']}")
    lines.append(f"- Row count: {summary.get('rows'):,}" if isinstance(summary.get("rows"), int) else f"- Row count: {summary.get('rows', 'unknown')}")
    lines.append(f"- Column count: {summary.get('columns'):,}" if isinstance(summary.get("columns"), int) else f"- Column count: {summary.get('columns', 'unknown')}")
    lines.append("")
    lines.append("### Info-like summary")
    lines.append("")
    info_rows = [
        ["storage type", summary["kind"]],
        ["matrix/data shape", summary["dimensions"]],
        ["matrix details", summary.get("matrix_info", "")],
        ["file size", format_bytes(size)],
    ]
    if "obs_columns" in summary:
        info_rows.append(["obs columns", f"{len(summary['obs_columns']):,}"])
        info_rows.append(["var columns", f"{len(summary['var_columns']):,}"])
    if "row_attrs" in summary:
        info_rows.append(["row attributes", f"{len(summary['row_attrs']):,}"])
        info_rows.append(["column attributes", f"{len(summary['col_attrs']):,}"])
    lines.append(md_table(["field", "value"], info_rows))
    lines.append("")
    lines.append("### Columns")
    lines.append("")
    if "column_names" in summary:
        lines.append(f"- Column count: {summary.get('columns'):,}")
        lines.append(f"- Column names: {names_if_less_than_20(summary['column_names'])}")
    elif "obs_columns" in summary:
        lines.append(f"- `obs` column count: {len(summary['obs_columns']):,}")
        lines.append(f"- `obs` column names: {names_if_less_than_20(summary['obs_columns'])}")
        lines.append(f"- `var` column count: {len(summary['var_columns']):,}")
        lines.append(f"- `var` column names: {names_if_less_than_20(summary['var_columns'])}")
    elif "row_attrs" in summary:
        lines.append(f"- Row attribute count: {len(summary['row_attrs']):,}")
        lines.append(f"- Row attribute names: {names_if_less_than_20(summary['row_attrs'])}")
        lines.append(f"- Column attribute count: {len(summary['col_attrs']):,}")
        lines.append(f"- Column attribute names: {names_if_less_than_20(summary['col_attrs'])}")
    else:
        lines.append("- Column names: not embedded or unavailable")
    if "dtype_rows" in summary:
        lines.append("")
        lines.append("Sample-inferred dtypes for preview columns:")
        lines.append("")
        lines.append(md_table(["column", "sample dtype"], summary["dtype_rows"]))
    lines.append("")
    write_metadata_section(lines, summary)
    lines.append("### Top 5 rows / preview")
    lines.append("")
    preview_headers = summary.get("preview_headers") or []
    preview_rows = summary.get("preview_rows") or []
    if preview_headers and preview_rows:
        lines.append(md_table(list(preview_headers), preview_rows))
    else:
        lines.append("No preview available.")
    lines.append("")


def main() -> None:
    OUTFILE.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append("# Maxtoki Development Data: Shape and Head Summary")
    lines.append("")
    lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
    lines.append("")
    lines.append(f"Data directory: `{DATA_DIR}`")
    lines.append("")
    lines.append("This report summarizes each main dataset file with dimensions, row and column counts, an info-like structural summary, and a top-five preview. Large files were inspected by streaming or HDF5 metadata reads rather than full in-memory loading.")
    lines.append("")

    overview_rows = []
    summaries = []
    for idx, (source, name, path) in enumerate(DATASETS, start=1):
        print(f"[{idx}/{len(DATASETS)}] summarizing {path}")
        summary = summarize_dataset(path)
        summaries.append((idx, source, name, path, summary))
        overview_rows.append([
            idx,
            source,
            name,
            format_bytes(path.stat().st_size if path.exists() else None),
            summary["dimensions"],
            format_count(summary.get("unique_cells", "unknown")),
            summary["kind"],
        ])

    lines.append("## Overview")
    lines.append("")
    lines.append(md_table(["#", "source", "dataset", "size", "dimension", "unique cells", "kind"], overview_rows))
    lines.append("")

    for item in summaries:
        write_dataset_section(lines, *item)

    OUTFILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUTFILE}")


if __name__ == "__main__":
    main()
