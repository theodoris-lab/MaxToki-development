#!/usr/bin/env python3
"""Create a short report comparing CellxGene originals with heart subsets."""

from __future__ import annotations

from collections import Counter
from datetime import datetime
from pathlib import Path

import anndata as ad


DATA_DIR = Path("/gladstone/theodoris/lab/enockniyonkuru/maxtoki_development_data")
SOURCE_DIR = DATA_DIR / "source_1_cellxgene"
SUBSET_DIR = DATA_DIR / "source_1_cellxgene_heart_development_subset"
OUTFILE = Path("documents/cellxgene_heart_development_subset_report.md")
EXCLUDED_SOURCE_FILES = {
    "02_survey_of_human_embryonic_development_1_million_cells_subset.h5ad",
}
EXCLUSION_REASONS = {
    "02_survey_of_human_embryonic_development_1_million_cells_subset.h5ad": (
        "Excluded from this report because it is fully contained in "
        "`03_survey_of_human_embryonic_development.h5ad`."
    ),
}

METADATA_FIELDS = ["cell_type", "tissue", "development_stage", "disease"]
DISPLAY_NAMES = {
    "cell_type": "cell types",
    "tissue": "tissues",
    "development_stage": "development stages",
    "disease": "diseases",
}
FULL_VALUE_LIMIT = 16
FIELD_VALUE_LIMITS = {
    "cell_type": 16,
    "tissue": 100,
    "development_stage": 100,
    "disease": 100,
}


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


def fmt_pct(value: float) -> str:
    return f"{value:.1f}%"


def unique_values(adata, field: str) -> list[str]:
    if field not in adata.obs.columns:
        return []
    series = adata.obs[field].astype("string").fillna("")
    return sorted(v for v in series.unique().tolist() if v)


def value_counts(adata, field: str) -> list[tuple[str, int]]:
    if field not in adata.obs.columns:
        return []
    series = adata.obs[field].astype("string").fillna("")
    counts = series.value_counts(dropna=False)
    rows = []
    for key, value in counts.items():
        if not key:
            continue
        rows.append((str(key), int(value)))
    rows.sort(key=lambda item: (-item[1], item[0]))
    return rows


def format_values(values: list[str], limit: int = FULL_VALUE_LIMIT) -> str:
    if not values:
        return "none"
    if len(values) <= limit:
        return ", ".join(f"`{v}`" for v in values)
    shown = ", ".join(f"`{v}`" for v in values[:limit])
    return f"{shown}, ... plus {len(values) - limit:,} more"


def subset_path_for(source_path: Path) -> Path:
    return SUBSET_DIR / source_path.name.replace(".h5ad", "_heart_development_subset.h5ad")


def read_summary(path: Path, include_counts: bool = False) -> dict[str, object]:
    adata = ad.read_h5ad(path, backed="r")
    try:
        summary = {
            "path": path,
            "cells": int(adata.n_obs),
            "genes": int(adata.n_vars),
            "metadata": {field: unique_values(adata, field) for field in METADATA_FIELDS},
        }
        if include_counts:
            summary["counts"] = {
                "cell_type": value_counts(adata, "cell_type"),
                "development_stage": value_counts(adata, "development_stage"),
                "tissue": value_counts(adata, "tissue"),
                "disease": value_counts(adata, "disease"),
            }
        return summary
    finally:
        adata.file.close()


def counts_table_rows(counts: list[tuple[str, int]], total: int) -> list[list[object]]:
    rows = []
    for name, count in counts:
        pct = count / total * 100 if total else 0.0
        rows.append([name, fmt_int(count), fmt_pct(pct)])
    return rows


def write_dataset_section(lines: list[str], idx: int, source: dict[str, object], subset: dict[str, object]) -> None:
    source_path = Path(source["path"])
    subset_path = Path(subset["path"])
    original_cells = int(source["cells"])
    kept_cells = int(subset["cells"])
    removed_cells = original_cells - kept_cells
    kept_pct = kept_cells / original_cells * 100 if original_cells else 0.0

    lines.append(f"## {idx}. {source_path.name}")
    lines.append("")
    lines.append(f"- Original file: `{source_path.relative_to(DATA_DIR)}`")
    lines.append(f"- Subset file: `{subset_path.relative_to(DATA_DIR)}`")
    lines.append(f"- Original size: {fmt_int(original_cells)} cells x {fmt_int(source['genes'])} genes")
    lines.append(f"- Kept subset: {fmt_int(kept_cells)} cells x {fmt_int(subset['genes'])} genes ({fmt_pct(kept_pct)} of original cells)")
    lines.append(f"- Removed by filter: {fmt_int(removed_cells)} cells")
    lines.append("")

    source_meta = source["metadata"]
    subset_meta = subset["metadata"]
    assert isinstance(source_meta, dict)
    assert isinstance(subset_meta, dict)

    comparison_rows = []
    for field in METADATA_FIELDS:
        original_values = list(source_meta[field])
        kept_values = list(subset_meta[field])
        excluded_values = sorted(set(original_values) - set(kept_values))
        value_limit = FIELD_VALUE_LIMITS.get(field, FULL_VALUE_LIMIT)
        comparison_rows.append([
            DISPLAY_NAMES[field],
            len(original_values),
            format_values(original_values, limit=value_limit),
            len(kept_values),
            format_values(kept_values, limit=value_limit),
            format_values(excluded_values, limit=value_limit),
        ])

    lines.append(md_table([
        "metadata",
        "original unique count",
        "original values",
        "kept unique count",
        "kept values",
        "original values not kept",
    ], comparison_rows))
    lines.append("")

    subset_counts = subset.get("counts", {})
    assert isinstance(subset_counts, dict)

    lines.append("### Subset Cell Type Counts")
    lines.append("")
    lines.append(md_table(
        ["cell type", "cells in subset", "subset %"],
        counts_table_rows(list(subset_counts.get("cell_type", [])), kept_cells),
    ))
    lines.append("")

    lines.append("### Subset Development Stage Counts")
    lines.append("")
    lines.append(md_table(
        ["development stage", "cells in subset", "subset %"],
        counts_table_rows(list(subset_counts.get("development_stage", [])), kept_cells),
    ))
    lines.append("")


def main() -> None:
    OUTFILE.parent.mkdir(parents=True, exist_ok=True)
    source_files = sorted(
        path for path in SOURCE_DIR.glob("*.h5ad")
        if path.name not in EXCLUDED_SOURCE_FILES
    )
    if not source_files:
        raise SystemExit(f"No source H5AD files found in {SOURCE_DIR}")

    pairs = []
    for source_path in source_files:
        subset_path = subset_path_for(source_path)
        if not subset_path.exists():
            raise SystemExit(f"Missing subset for {source_path.name}: {subset_path}")
        print(f"Summarizing {source_path.name}", flush=True)
        pairs.append((read_summary(source_path), read_summary(subset_path, include_counts=True)))

    total_original = sum(int(source["cells"]) for source, _ in pairs)
    total_kept = sum(int(subset["cells"]) for _, subset in pairs)
    total_removed = total_original - total_kept
    kept_pct = total_kept / total_original * 100 if total_original else 0.0

    overall_cell_type_counts: Counter[str] = Counter()
    overall_stage_counts: Counter[str] = Counter()
    for _, subset in pairs:
        subset_counts = subset.get("counts", {})
        assert isinstance(subset_counts, dict)
        for name, count in list(subset_counts.get("cell_type", [])):
            overall_cell_type_counts[name] += count
        for name, count in list(subset_counts.get("development_stage", [])):
            overall_stage_counts[name] += count

    lines: list[str] = []
    lines.append("# CellxGene Heart Development Subset Report")
    lines.append("")
    lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
    lines.append("")
    lines.append(f"Original CellxGene directory: `{SOURCE_DIR}`")
    lines.append(f"Subset directory: `{SUBSET_DIR}`")
    lines.append("")
    lines.append("This report compares the original CellxGene `.h5ad` files with the filtered heart-development subset. The subset keeps observations where `disease == normal`, where `tissue` is one of the requested heart/outflow/atrium/ventricle regions, and where `development_stage` is one of the requested embryonic, fetal, or Carnegie stages.")
    lines.append("")
    lines.append("Dataset omitted from this report:")
    lines.append("")
    for name in sorted(EXCLUDED_SOURCE_FILES):
        lines.append(f"- `{name}`: {EXCLUSION_REASONS[name]}")
    lines.append("")
    lines.append("## Overall Summary")
    lines.append("")
    lines.append(f"- Original input observations across the {len(pairs)} reported CellxGene files: {fmt_int(total_original)} cells")
    lines.append(f"- Kept observations across the subset files: {fmt_int(total_kept)} cells ({fmt_pct(kept_pct)} of original)")
    lines.append(f"- Removed observations: {fmt_int(total_removed)} cells")
    lines.append("- Genes/features were preserved per dataset; the subset changes cells/observations, not the gene axis.")
    lines.append("")

    overview_rows = []
    for source, subset in pairs:
        original_cells = int(source["cells"])
        kept_cells = int(subset["cells"])
        overview_rows.append([
            Path(source["path"]).name,
            fmt_int(original_cells),
            fmt_int(source["genes"]),
            fmt_int(kept_cells),
            fmt_pct(kept_cells / original_cells * 100 if original_cells else 0.0),
            fmt_int(subset["genes"]),
        ])
    lines.append(md_table([
        "dataset",
        "original cells",
        "original genes",
        "kept cells",
        "kept %",
        "kept genes",
    ], overview_rows))
    lines.append("")

    lines.append("## Overall Subset Composition")
    lines.append("")
    lines.append("### Cell Type Counts Across Reported Subsets")
    lines.append("")
    lines.append(md_table(
        ["cell type", "cells across reported subsets", "reported subset %"],
        counts_table_rows(sorted(overall_cell_type_counts.items(), key=lambda item: (-item[1], item[0])), total_kept),
    ))
    lines.append("")
    lines.append("### Development Stage Counts Across Reported Subsets")
    lines.append("")
    lines.append(md_table(
        ["development stage", "cells across reported subsets", "reported subset %"],
        counts_table_rows(sorted(overall_stage_counts.items(), key=lambda item: (-item[1], item[0])), total_kept),
    ))
    lines.append("")

    lines.append("## Dataset Details")
    lines.append("")
    for idx, (source, subset) in enumerate(pairs, start=1):
        write_dataset_section(lines, idx, source, subset)

    OUTFILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUTFILE}", flush=True)


if __name__ == "__main__":
    main()
