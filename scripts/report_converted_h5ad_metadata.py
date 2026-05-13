#!/usr/bin/env python3
"""Summarize the 11 converted source_2/source_3/source_4 H5AD files."""

from __future__ import annotations

import csv
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
import re

import anndata as ad
import pandas as pd


MANIFEST = Path(
    "/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data/"
    "source_2_3_4_h5ad_converted/conversion_manifest.tsv"
)
OUTFILE = Path("documents/converted_h5ad_metadata_report.md")


def md_escape(value: object) -> str:
    text = "" if value is None else str(value)
    return text.replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def md_table(headers: list[str], rows: list[list[object]]) -> str:
    lines = [
        "| " + " | ".join(md_escape(h) for h in headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(v) for v in row) + " |")
    return "\n".join(lines)


def fmt_int(value: int | float | None) -> str:
    if value is None:
        return "unknown"
    if isinstance(value, float):
        return f"{value:,.1f}"
    return f"{value:,}"


def display_name(row: dict[str, str]) -> str:
    path = Path(row["output_path"])
    name = path.stem
    name = re.sub(r"[_]+", " ", name).strip()
    name = re.sub(r"^\d+\s+", "", name)
    return name


def unique_manifest_rows(path: Path) -> list[dict[str, str]]:
    rows = list(csv.DictReader(path.open(), delimiter="\t"))
    by_output: OrderedDict[str, dict[str, str]] = OrderedDict()
    for row in rows:
        by_output[row["output_path"]] = row
    return list(by_output.values())


def candidate_columns(columns: list[str], patterns: list[str]) -> list[str]:
    found: list[str] = []
    for col in columns:
        lowered = col.lower()
        if any(re.search(pattern, lowered) for pattern in patterns):
            found.append(col)
    return found


def counts_table(series: pd.Series, label: str) -> str:
    values = series.astype("string").dropna()
    values = values[values != ""]
    if values.empty:
        return f"No non-empty values found in `{label}`."
    counts = values.value_counts(dropna=True).reset_index()
    counts.columns = [label, "cells"]
    counts["cells"] = counts["cells"].map(lambda x: fmt_int(int(x)))
    return md_table([label, "cells"], counts.values.tolist())


def summarize_dataset(row: dict[str, str]) -> dict[str, object]:
    output_path = Path(row["output_path"])
    adata = ad.read_h5ad(output_path, backed="r")
    try:
        obs_cols = list(adata.obs.columns)
        var_cols = list(adata.var.columns)

        cell_type_cols = candidate_columns(
            obs_cols,
            [r"(^|_)cell[_ ]?type($|_)", r"cell_subclass", r"cell_class"],
        )
        stage_cols = candidate_columns(
            obs_cols,
            [r"development[_ ]?stage", r"^stage$"],
        )
        metadata_cols = list(dict.fromkeys(cell_type_cols + stage_cols))
        obs = adata.obs[metadata_cols].copy() if metadata_cols else pd.DataFrame(index=adata.obs_names)

        return {
            "dataset_id": row["dataset_id"],
            "display_name": display_name(row),
            "output_path": output_path,
            "status": row["status"],
            "seconds": float(row["seconds"] or 0),
            "size_bytes": int(row["size_bytes"] or 0),
            "n_obs": int(adata.n_obs),
            "n_vars": int(adata.n_vars),
            "obs_cols": obs_cols,
            "var_cols": var_cols,
            "obs": obs,
            "cell_type_cols": cell_type_cols,
            "stage_cols": stage_cols,
        }
    finally:
        adata.file.close()


def main() -> None:
    OUTFILE.parent.mkdir(parents=True, exist_ok=True)
    manifest_rows = unique_manifest_rows(MANIFEST)
    datasets = [summarize_dataset(row) for row in manifest_rows]

    overview_rows: list[list[object]] = []
    sections: list[str] = []

    for idx, dataset in enumerate(datasets, start=1):
        obs_cols = dataset["obs_cols"]
        var_cols = dataset["var_cols"]
        cell_type_cols = dataset["cell_type_cols"]
        stage_cols = dataset["stage_cols"]
        obs = dataset["obs"]

        overview_rows.append([
            dataset["dataset_id"],
            dataset["display_name"],
            fmt_int(dataset["n_obs"]),
            fmt_int(dataset["n_vars"]),
            fmt_int(len(obs_cols)),
            fmt_int(len(var_cols)),
            ", ".join(cell_type_cols) if cell_type_cols else "none",
            ", ".join(stage_cols) if stage_cols else "none",
        ])

        sections.append(f"## {idx}. {dataset['display_name']}")
        sections.append("")
        sections.append(f"- Dataset ID: `{dataset['dataset_id']}`")
        sections.append(f"- Output file: `{dataset['output_path']}`")
        sections.append(f"- Conversion status: `{dataset['status']}`")
        sections.append(f"- Cells: {fmt_int(dataset['n_obs'])}")
        sections.append(f"- Genes / features: {fmt_int(dataset['n_vars'])}")
        sections.append(f"- Output size: {fmt_int(dataset['size_bytes'])} bytes")
        sections.append(f"- Conversion time: {dataset['seconds']:.1f} seconds")
        sections.append("")
        sections.append("### Columns")
        sections.append("")
        sections.append(f"- `obs` column count: {fmt_int(len(obs_cols))}")
        if len(obs_cols) < 20:
            sections.append(
                f"- `obs` column names: {', '.join(f'`{col}`' for col in obs_cols) if obs_cols else 'none'}"
            )
        sections.append(f"- `var` column count: {fmt_int(len(var_cols))}")
        if len(var_cols) < 20:
            sections.append(
                f"- `var` column names: {', '.join(f'`{col}`' for col in var_cols) if var_cols else 'none'}"
            )
        sections.append("")
        sections.append("### Cell Type Metadata")
        sections.append("")
        if cell_type_cols:
            for col in cell_type_cols:
                sections.append(f"#### `{col}`")
                sections.append("")
                sections.append(counts_table(obs[col], col))
                sections.append("")
        else:
            sections.append("No explicit cell type metadata column found in `obs`.")
            sections.append("")
        sections.append("### Development Stage Metadata")
        sections.append("")
        if stage_cols:
            for col in stage_cols:
                sections.append(f"#### `{col}`")
                sections.append("")
                sections.append(counts_table(obs[col], col))
                sections.append("")
        else:
            sections.append("No explicit development stage metadata column found in `obs`.")
            sections.append("")

    lines: list[str] = []
    lines.append("# Converted H5AD Metadata Report")
    lines.append("")
    lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
    lines.append("")
    lines.append(
        "This report covers the 11 unique converted `.h5ad` outputs from source 2, source 3, "
        "and source 4. For each file it lists cell/feature counts, metadata column names, and "
        "any explicit cell type or development stage annotations found in `obs`."
    )
    lines.append("")
    lines.append("## Overview")
    lines.append("")
    lines.append(
        md_table(
            [
                "dataset id",
                "dataset",
                "cells",
                "features",
                "obs cols",
                "var cols",
                "cell type cols",
                "development stage cols",
            ],
            overview_rows,
        )
    )
    lines.append("")
    lines.extend(sections)

    OUTFILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUTFILE}")


if __name__ == "__main__":
    main()
