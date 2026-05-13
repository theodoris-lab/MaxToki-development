#!/usr/bin/env python3
"""Create a dedicated cell-type by development-stage count report."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re

import anndata as ad
import h5py
import pandas as pd


DATA_DIR = Path("/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data")
SOURCE_DIR = DATA_DIR / "source_1_cellxgene"
SUBSET_DIR = DATA_DIR / "source_1_cellxgene_heart_development_subset"
OUTFILE = Path("documents/cellxgene_heart_development_subset_celltype_by_stage.md")
COMBINED_CSV_OUTFILE = Path("documents/cellxgene_heart_development_subset_celltype_by_stage_combined.csv")
METADATA_SOURCE = Path("data_extraction/output.txt")
EXCLUDED_SOURCE_FILES = {
    "02_survey_of_human_embryonic_development_1_million_cells_subset.h5ad",
}
EXCLUSION_REASONS = {
    "02_survey_of_human_embryonic_development_1_million_cells_subset.h5ad": (
        "Excluded because it is fully contained in "
        "`03_survey_of_human_embryonic_development.h5ad`."
    ),
}
STAGE_ORDER = [
    "embryonic stage",
    "6th week post-fertilization stage",
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
]
DATASET_NAME_RE = re.compile(r"([0-9]{2}_[A-Za-z0-9_]+\.h5ad)$")
FIELD_PREFIXES = (
    "Original size:",
    "Kept subset:",
    "Cell Types",
    "Cell types",
    "Tissue:",
    "Tissue Type:",
    "Development Stage",
    "Development Stages",
    "Disease:",
    "Assay:",
    "Publication:",
    "Publicaiton:",
    "Source:",
    "Paper:",
    "Abstract:",
)


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


def stage_sort_key(stage: str) -> tuple[int, str]:
    if stage in STAGE_ORDER:
        return (STAGE_ORDER.index(stage), stage)
    return (len(STAGE_ORDER), stage)


def normalize_stage_label(stage: object) -> str:
    text = "" if stage is None else str(stage)
    if text == "Carnegie stage 17":
        return "6th week post-fertilization stage"
    return text


def subset_path_for(source_path: Path) -> Path:
    return SUBSET_DIR / source_path.name.replace(".h5ad", "_heart_development_subset.h5ad")


def read_h5_scalar(group: h5py.Group, key: str) -> str:
    value = group[key][()]
    if isinstance(value, bytes):
        return value.decode("utf-8")
    if hasattr(value, "decode"):
        return value.decode("utf-8")
    return str(value)


def display_title(title: str) -> str:
    cleaned = title.strip()
    if "_" in cleaned:
        cleaned = cleaned.replace("_", " ")
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if cleaned.endswith("."):
        cleaned = cleaned[:-1]
    return cleaned


def dataset_title_for(source_path: Path) -> str:
    with h5py.File(source_path, "r") as handle:
        uns = handle["uns"]
        if "title" in uns:
            return display_title(read_h5_scalar(uns, "title"))
    return display_title(source_path.stem)


def clean_bullet(line: str) -> str:
    return line.strip().lstrip("•").strip()


def parse_output_metadata(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"Metadata source file not found: {path}")

    entries: dict[str, dict[str, str]] = {}
    current_name: str | None = None
    current_abstract_lines: list[str] = []
    in_abstract = False
    pending_source = False

    def finalize_abstract() -> None:
        nonlocal current_abstract_lines, in_abstract
        if current_name is not None and current_abstract_lines:
            abstract = "\n".join(line for line in current_abstract_lines if line != "").strip()
            entries[current_name]["abstract"] = abstract
        current_abstract_lines = []
        in_abstract = False

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.strip()
        dataset_match = DATASET_NAME_RE.search(stripped)
        if dataset_match:
            finalize_abstract()
            current_name = dataset_match.group(1)
            entries[current_name] = {
                "assay": "",
                "source_or_publication": "",
                "paper": "",
                "abstract": "",
            }
            pending_source = False
            continue

        if current_name is None:
            continue

        line = clean_bullet(raw_line)
        if not line:
            if in_abstract:
                current_abstract_lines.append("")
            continue

        if in_abstract and not any(line.startswith(prefix) for prefix in FIELD_PREFIXES):
            current_abstract_lines.append(line)
            continue
        if in_abstract:
            finalize_abstract()

        if pending_source:
            entries[current_name]["source_or_publication"] = line
            pending_source = False
            continue

        if line.startswith("Assay:"):
            entries[current_name]["assay"] = line.split(":", 1)[1].strip()
        elif line.startswith("Publication:") or line.startswith("Publicaiton:"):
            value = line.split(":", 1)[1].strip()
            if value:
                entries[current_name]["source_or_publication"] = value
            else:
                pending_source = True
        elif line.startswith("Source:"):
            entries[current_name]["source_or_publication"] = line.split(":", 1)[1].strip()
        elif line.startswith("Paper:"):
            entries[current_name]["paper"] = line.split(":", 1)[1].strip()
        elif line.startswith("Abstract:"):
            value = line.split(":", 1)[1].strip()
            current_abstract_lines = [value] if value else []
            in_abstract = True

    finalize_abstract()
    return entries


def dataset_table(path: Path) -> tuple[int, int, pd.DataFrame]:
    adata = ad.read_h5ad(path, backed="r")
    try:
        obs = adata.obs[["cell_type", "development_stage"]].copy()
        obs = obs.astype("string").fillna("")
        obs["development_stage"] = obs["development_stage"].map(normalize_stage_label)
        obs = obs[(obs["cell_type"] != "") & (obs["development_stage"] != "")]
        table = pd.crosstab(obs["cell_type"], obs["development_stage"])
        ordered_cols = sorted(table.columns.tolist(), key=stage_sort_key)
        table = table.loc[:, ordered_cols]
        table["Total"] = table.sum(axis=1)
        table = table.sort_values(by="Total", ascending=False)
        total_row = table.sum(axis=0).to_frame().T
        total_row.index = ["Total"]
        table = pd.concat([table, total_row], axis=0)
        return int(adata.n_obs), int(adata.n_vars), table
    finally:
        adata.file.close()


def cleaned_obs(path: Path) -> tuple[int, int, pd.DataFrame]:
    adata = ad.read_h5ad(path, backed="r")
    try:
        obs = adata.obs[["cell_type", "development_stage"]].copy()
        obs = obs.astype("string").fillna("")
        obs["development_stage"] = obs["development_stage"].map(normalize_stage_label)
        obs = obs[(obs["cell_type"] != "") & (obs["development_stage"] != "")]
        return int(adata.n_obs), int(adata.n_vars), obs
    finally:
        adata.file.close()


def combined_table(paths: list[Path]) -> tuple[int, pd.DataFrame]:
    all_obs: list[pd.DataFrame] = []
    total_cells = 0
    for path in paths:
        n_obs, _, obs = cleaned_obs(path)
        total_cells += n_obs
        all_obs.append(obs)
    combined_obs = pd.concat(all_obs, ignore_index=True)
    table = pd.crosstab(combined_obs["cell_type"], combined_obs["development_stage"])
    ordered_cols = sorted(table.columns.tolist(), key=stage_sort_key)
    table = table.loc[:, ordered_cols]
    table["Total"] = table.sum(axis=1)
    table = table.sort_values(by="Total", ascending=False)
    total_row = table.sum(axis=0).to_frame().T
    total_row.index = ["Total"]
    table = pd.concat([table, total_row], axis=0)
    return total_cells, table


def dataframe_to_markdown(table: pd.DataFrame) -> str:
    headers = ["cell type"] + [str(col) for col in table.columns]
    rows: list[list[object]] = []
    for idx, (_, row) in enumerate(table.iterrows()):
        name = str(row.name)
        cells = [fmt_int(int(value)) for value in row.tolist()]
        rows.append([name] + cells)
    return md_table(headers, rows)


def main() -> None:
    OUTFILE.parent.mkdir(parents=True, exist_ok=True)
    COMBINED_CSV_OUTFILE.parent.mkdir(parents=True, exist_ok=True)
    metadata = parse_output_metadata(METADATA_SOURCE)
    source_files = sorted(
        path for path in SOURCE_DIR.glob("*.h5ad")
        if path.name not in EXCLUDED_SOURCE_FILES
    )
    if not source_files:
        raise SystemExit(f"No source H5AD files found in {SOURCE_DIR}")

    dataset_rows = []
    sections: list[str] = []
    subset_paths: list[Path] = []
    for idx, source_path in enumerate(source_files, start=1):
        subset_path = subset_path_for(source_path)
        if not subset_path.exists():
            raise SystemExit(f"Missing subset for {source_path.name}: {subset_path}")
        subset_paths.append(subset_path)
        print(f"Summarizing {source_path.name}", flush=True)
        dataset_title = dataset_title_for(source_path)
        n_obs, n_vars, table = dataset_table(subset_path)
        info = metadata.get(source_path.name, {})
        dataset_rows.append([
            dataset_title,
            source_path.name,
            fmt_int(n_obs),
            fmt_int(n_vars),
            fmt_int(len(table.index) - 1),
            fmt_int(len(table.columns) - 1),
        ])
        sections.append(f"## {idx}. {dataset_title}")
        sections.append("")
        sections.append(f"- Source file: `{source_path.name}`")
        sections.append(f"- Subset file: `{subset_path.relative_to(DATA_DIR)}`")
        sections.append(f"- Cells in subset: {fmt_int(n_obs)}")
        sections.append(f"- Genes in subset: {fmt_int(n_vars)}")
        sections.append(f"- Unique cell types in subset: {fmt_int(len(table.index) - 1)}")
        sections.append(f"- Unique development stages in subset: {fmt_int(len(table.columns) - 1)}")
        sections.append("")
        sections.append("### Dataset Metadata")
        sections.append("")
        sections.append(md_table(
            ["field", "value"],
            [
                ["assay", info.get("assay") or "not listed in output.txt"],
                ["source / publication", info.get("source_or_publication") or "not listed in output.txt"],
                ["paper", info.get("paper") or "not listed in output.txt"],
            ],
        ))
        sections.append("")
        sections.append("### Abstract")
        sections.append("")
        sections.append(info.get("abstract") or "Not listed in output.txt.")
        sections.append("")
        sections.append(dataframe_to_markdown(table))
        sections.append("")

    combined_cells, combined = combined_table(subset_paths)
    combined_stage_names = [str(col) for col in combined.columns if str(col) != "Total"]
    combined_stage_counts = combined.loc["Total", combined_stage_names].tolist()
    combined_stage_rows = [
        [idx, stage, fmt_int(int(count))]
        for idx, (stage, count) in enumerate(zip(combined_stage_names, combined_stage_counts), start=1)
    ]

    lines: list[str] = []
    lines.append("# CellxGene Subset: Cell Type by Development Stage Counts")
    lines.append("")
    lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
    lines.append("")
    lines.append(f"Subset directory: `{SUBSET_DIR}`")
    lines.append("")
    lines.append("This document contains one table per reported dataset. Rows are subset cell types, columns are subset development stages, and each entry is the count of unique cells kept in that combination.")
    lines.append("")
    lines.append("Dataset omitted from this document:")
    lines.append("")
    for name in sorted(EXCLUDED_SOURCE_FILES):
        lines.append(f"- `{name}`: {EXCLUSION_REASONS[name]}")
    lines.append("")
    lines.append("## Overview")
    lines.append("")
    lines.append(md_table(
        ["dataset title", "source file", "subset cells", "subset genes", "unique cell types", "unique development stages"],
        dataset_rows,
    ))
    lines.append("")
    lines.extend(sections)
    lines.append("## Consolidated View")
    lines.append("")
    lines.append(
        "This section treats the 9 retained subset datasets as one combined collection. "
        "Counts are based on concatenating the subset observations after excluding the redundant "
        "`02_survey_of_human_embryonic_development_1_million_cells_subset.h5ad` dataset."
    )
    lines.append("")
    lines.append(f"- Combined cells across retained subsets: {fmt_int(combined_cells)}")
    lines.append(f"- Combined unique cell types: {fmt_int(len(combined.index) - 1)}")
    lines.append(f"- Combined development stages: {fmt_int(len(combined_stage_names))}")
    lines.append("")
    lines.append("### Combined Development Stage Order")
    lines.append("")
    lines.append(md_table(
        ["order", "development stage", "cells in combined data"],
        combined_stage_rows,
    ))
    lines.append("")
    lines.append("### Combined Cell Type by Development Stage Counts")
    lines.append("")
    lines.append(
        "Rows are all cell types observed anywhere in the retained subsets. Columns are the full "
        "ordered set of development stages present after combining the datasets."
    )
    lines.append("")
    lines.append(dataframe_to_markdown(combined))
    lines.append("")

    OUTFILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    combined_to_write = combined.copy()
    combined_to_write.index.name = "cell type"
    combined_to_write.to_csv(COMBINED_CSV_OUTFILE, encoding="utf-8")
    print(f"Wrote {OUTFILE}", flush=True)
    print(f"Wrote {COMBINED_CSV_OUTFILE}", flush=True)


if __name__ == "__main__":
    main()
